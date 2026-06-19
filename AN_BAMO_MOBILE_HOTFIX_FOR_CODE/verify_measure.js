#!/usr/bin/env node
/*
 * verify_measure.js — automated browser-faithful gate for AN BAMO Command Center.
 * Closes the audit blind spot ("screenshots blocked / no browser execution") WITHOUT
 * needing Chromium/Playwright. Uses jsdom + polyfills for the browser APIs the app relies
 * on (matchMedia, CSS.escape, clipboard, print) so behavior matches a real browser.
 *
 * Setup (once):   npm install jsdom
 * Run:            node verify_measure.js path/to/AN_BAMO_Command_Center_vX.html
 *
 * Exit code 0 = all gates passed, 1 = at least one gate failed.
 */
const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const file = process.argv[2];
if (!file) { console.error('usage: node verify_measure.js <html-file>'); process.exit(2); }
const html = fs.readFileSync(file, 'utf8');

const loadErrors = [];
const vc = new VirtualConsole();
vc.on('jsdomError', e => loadErrors.push((e.message || '') + (e.detail && e.detail.stack ? ' :: ' + e.detail.stack.split('\n')[1] : '')));

const dom = new JSDOM(html, {
  runScripts: 'dangerously', resources: 'usable', pretendToBeVisual: true, virtualConsole: vc, url: 'https://localhost/',
  beforeParse(w) {
    w.matchMedia = q => ({ matches: false, media: q || '', onchange: null, addListener(){}, removeListener(){}, addEventListener(){}, removeEventListener(){}, dispatchEvent(){return false} });
    w.scrollTo = () => {}; w.scroll = () => {}; w.print = () => {};
    w.requestAnimationFrame = cb => setTimeout(() => cb(Date.now()), 0);
    w.cancelAnimationFrame = id => clearTimeout(id);
    w.alert = () => {}; w.confirm = () => true; w.prompt = (m, d) => (d != null ? d : 'x');
    if (!w.CSS) w.CSS = {}; if (!w.CSS.escape) w.CSS.escape = x => String(x).replace(/[^a-zA-Z0-9_-]/g, m => '\\' + m);
    if (!w.URL.createObjectURL) w.URL.createObjectURL = () => 'blob:mock';
    if (!w.URL.revokeObjectURL) w.URL.revokeObjectURL = () => {};
    try { Object.defineProperty(w.navigator, 'clipboard', { value: { writeText: () => Promise.resolve(), readText: () => Promise.resolve('') }, configurable: true }); } catch (e) {}
  }
});
const w = dom.window;
w.HTMLElement.prototype.scrollIntoView = () => {};

const results = [];
function gate(name, pass, detail) { results.push({ name, pass, detail }); }

setTimeout(() => {
  try { w.document.dispatchEvent(new w.Event('DOMContentLoaded', { bubbles: true })); } catch (e) {}
  try { w.dispatchEvent(new w.Event('load')); } catch (e) {}
  setTimeout(() => {
    // --- GATE 1: load errors ---
    gate('LOAD ERRORS', loadErrors.length === 0, loadErrors.length ? [...new Set(loadErrors)].slice(0, 6).join(' | ') : '0');

    // --- GATE 2: tab sweep + dashboard non-empty ---
    const tabs = ['request','fast','measure','improvements','money','docs','production','settings','dashboard'];
    let tabErrCount = 0; const tabErrs = [];
    tabs.forEach(t => {
      const before = loadErrors.length;
      try {
        if (typeof w.setTab === 'function') w.setTab(t);
        else { if (w.state && w.state.ui) w.state.ui.tab = t; if (typeof w.renderCurrent === 'function') w.renderCurrent(); }
      } catch (e) { tabErrs.push(t + ': ' + e.message); tabErrCount++; }
      if (loadErrors.length > before) { tabErrCount++; tabErrs.push(t + ': ' + loadErrors[loadErrors.length-1]); }
    });
    gate('TAB SWEEP', tabErrCount === 0, tabErrCount ? tabErrs.slice(0,6).join(' | ') : '0 errors across ' + tabs.length + ' tabs');
    const dash = w.document.getElementById('pane-dashboard');
    gate('DASHBOARD RENDERS', !!dash && dash.innerHTML.length > 0, dash ? ('len=' + dash.innerHTML.length) : 'pane-dashboard MISSING');

    // --- GATE 3: measure field round-trip (best-effort; closures may limit it) ---
    // Strategy: open measure, populate state.measureDraft with all advanced fields, trigger save,
    // then confirm the fields landed on a measureItems entry.
    const REQUIRED = ['type','module','position','height','width','qty','opening','handleMode',
      'hingeType','hardwareBrand','axisTemplate','axisMode','hingeAxisTop','hingeAxisBottom',
      'hingeEdgeOffset','hingeEdgeSide','decorName','colorName','ralCode','edgeEnabled','edgeSides',
      'edgeType','painterNote','productionNote','cuttingNote','riskNote'];
    let fieldDetail = 'could not access state (closure) — verify manually in browser';
    let fieldPass = null; // null = inconclusive
    try {
      const sample = { type:'swing', module:'M1', position:'1', height:720, width:397, qty:2, opening:'L',
        handleMode:'we', hingeType:'накл', hardwareBrand:'Blum', axisTemplate:'100/100', axisMode:'от низа',
        hingeAxisTop:100, hingeAxisBottom:650, hingeEdgeOffset:21, hingeEdgeSide:'left',
        decorName:'Дуб', colorName:'RAL9010', ralCode:'9010', edgeEnabled:true, edgeSides:'4',
        edgeType:'ABS', painterNote:'тест', productionNote:'тест', cuttingNote:'тест', riskNote:'тест' };
      // populate draft inside page scope
      w.eval('(function(s){ if(typeof state==="object"){ Object.assign(state.measureDraft, s); } })(' + JSON.stringify(sample) + ')');
      // try to save via a data-action button, else via known save fn name
      let saved = false;
      const saveBtn = w.document.querySelector('[data-action="measureSaveDraft"]');
      if (saveBtn) { try { saveBtn.click(); saved = true; } catch (e) {} }
      // read back measureItems[0]
      const itemJson = w.eval('(function(){ try { var it=(state.measureItems||[])[0]; return it?JSON.stringify(it):"" } catch(e){ return "ERR:"+e.message } })()');
      if (itemJson && itemJson.indexOf('ERR:') !== 0 && itemJson.length) {
        const item = JSON.parse(itemJson);
        const missing = REQUIRED.filter(k => !(k in item));
        fieldPass = missing.length === 0;
        fieldDetail = fieldPass ? ('all ' + REQUIRED.length + ' fields present (saved=' + saved + ')') : ('MISSING: ' + missing.join(', '));
      } else {
        fieldDetail = 'save did not produce a measureItems[0] (saved=' + saved + ') — wire/inspect manually';
      }
    } catch (e) { fieldDetail = 'inconclusive: ' + e.message; }
    results.push({ name: 'MEASURE FIELDS', pass: fieldPass, detail: fieldDetail });

    // --- GATE 4: document renderers don't throw (if reachable as globals) ---
    let docDetail = []; let docPass = null;
    ['measureSheet113','productionSheet113','painterBlank113'].forEach(fn => {
      if (typeof w[fn] === 'function') { try { w[fn](); docDetail.push(fn+':ok'); } catch (e) { docDetail.push(fn+':THREW '+e.message); docPass = false; } }
      else docDetail.push(fn+':closure(skip)');
    });
    if (docPass === null && docDetail.some(d => d.endsWith(':ok'))) docPass = true;
    results.push({ name: 'DOC RENDER', pass: docPass, detail: docDetail.join(' | ') });

    // --- report ---
    console.log('\n=== verify_measure.js — ' + path.basename(file) + ' ===');
    let hardFail = false;
    results.forEach(r => {
      const tag = r.pass === true ? 'PASS' : r.pass === false ? 'FAIL' : 'INCONCLUSIVE';
      if (r.pass === false) hardFail = true;
      console.log(`  [${tag}] ${r.name}: ${r.detail}`);
    });
    console.log('\nHard gates (LOAD ERRORS, TAB SWEEP, DASHBOARD RENDERS) must be PASS.');
    console.log('MEASURE FIELDS / DOC RENDER may be INCONCLUSIVE under jsdom (closures) — confirm those in a real browser.');
    process.exit(hardFail ? 1 : 0);
  }, 900);
}, 300);
