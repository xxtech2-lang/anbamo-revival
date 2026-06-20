#!/usr/bin/env python3
"""Build v10.4.22 — Theme fix (Block 3.1) + Working technical view (Block 4)
Block 3.1: persist theme to dedicated quick-load key (anbamo_theme_v1422); default LIGHT
Block 4:   replace pane-fast with compact technical working view
  4.1 no duplicate variants   4.2 compact catalog cards   4.3 facade from 106-item catalog
  4.4 accordion grouping      4.5 honest LED pricing       4.6 on/off toggles
  4.7 technical services      4.8 corner/L countertop      4.9 measure→Паспорт default
  4.10 handle buttons under "Ручки" label
Invariants: totals(), MAIN_KEY=anbamo_v10_4_6_mvp_stabilization, statusClassV473 — UNTOUCHED
"""
import os

BASE = r"C:\Users\Win\OneDrive\Документы\New project 4\Фасадный калькулятор\revival"
SRC  = os.path.join(BASE, "AN_BAMO_Command_Center_v10_4_21b_Projects_Fix.html")
OUT  = os.path.join(BASE, "AN_BAMO_Command_Center_v10_4_22_WorkView_Price.html")

with open(SRC, encoding="utf-8") as f:
    src = f.read()

assert "</body>"   in src, "ASSERT: no </body>"
assert "<body"     in src, "ASSERT: no <body>"
assert "anbamo_v10_4_6_mvp_stabilization" in src, "ASSERT: MAIN_KEY missing"
assert "openProjects1421" in src, "ASSERT: v10.4.21b layer missing"

# ── Injection 1: after <body> ── early theme, before first paint ──────────────
EARLY = ('<script>'
 '/* v10.4.22 early theme — runs before first paint */'
 'try{'
 'var _t1422=localStorage.getItem(\'anbamo_theme_v1422\')||\'light\';'
 'if(_t1422===\'system\')_t1422=matchMedia(\'(prefers-color-scheme:dark)\').matches?\'dark\':\'light\';'
 'document.body.dataset.theme=_t1422;'
 '}catch(e){}'
 '</script>')

# ── Injection 2: before </body> ── main layer ─────────────────────────────────
LAYER = """
<style>
/* v10.4.22 — WorkView + Theme */
.v1422-header{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:14px 16px;background:var(--surface);border:1px solid var(--brd,var(--line));border-radius:var(--r14,14px);margin-bottom:12px}
.v1422-client-name{font-weight:var(--fw-bold,760);font-size:var(--fs-md,14px);color:var(--txt,var(--ink))}
.v1422-client-sub{font-size:var(--fs-xs,11px);color:var(--muted);margin-top:2px}
.v1422-total{text-align:right;font-size:var(--fs-lg,17px);font-weight:var(--fw-bold,760);color:var(--txt,var(--ink))}
.v1422-total small{display:block;font-size:var(--fs-xs,11px);color:var(--muted);font-weight:400}
.v1422-acc{border:1px solid var(--brd,var(--line));border-radius:var(--r14,14px);margin-bottom:10px;overflow:hidden;background:var(--surface)}
.v1422-acc-head{display:flex;justify-content:space-between;align-items:center;gap:10px;width:100%;padding:14px 16px;min-height:48px;background:transparent;border:none;cursor:pointer;text-align:left;color:var(--txt,var(--ink))}
.v1422-acc-head-left{flex:1;min-width:0}
.v1422-acc-title{font-weight:var(--fw-bold,760);font-size:var(--fs-md,14px);display:block}
.v1422-acc-sum{font-size:var(--fs-xs,11px);color:var(--muted);display:block;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.v1422-chev{color:var(--muted);font-size:18px;transition:transform .15s;flex-shrink:0}
.v1422-acc.open .v1422-chev{transform:rotate(180deg)}
.v1422-acc-body{display:none;padding:14px 16px;border-top:1px solid var(--brd,var(--line))}
.v1422-acc.open .v1422-acc-body{display:block}
.v1422-zone-tab{background:transparent;border:1px solid var(--brd,var(--line));border-radius:8px;padding:6px 12px;font-size:13px;cursor:pointer;color:var(--muted);font-weight:var(--fw-semibold,650)}
.v1422-zone-tab.active{background:var(--primary,#2563eb);color:#fff;border-color:var(--primary,#2563eb)}
.v1422-ztabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
.v1422-catalog-card{display:flex;align-items:center;justify-content:space-between;padding:9px 12px;border:1px solid var(--brd,var(--line));border-radius:8px;margin-bottom:6px;gap:10px;cursor:pointer;background:var(--surface-2,var(--surface))}
.v1422-catalog-card.sel{border-color:var(--primary,#2563eb);background:rgba(37,99,235,.06)}
.v1422-card-name{font-weight:var(--fw-semibold,650);font-size:13px;color:var(--txt,var(--ink))}
.v1422-card-sup{color:var(--muted);font-size:11px;margin-top:1px}
.v1422-card-right{text-align:right;flex-shrink:0}
.v1422-card-price{font-weight:var(--fw-bold,760);font-size:13px;color:var(--txt,var(--ink))}
.v1422-card-select{margin-top:4px;border:1px solid var(--brd,var(--line));background:var(--surface);border-radius:999px;padding:2px 10px;font-size:11px;font-weight:var(--fw-semibold,650);cursor:pointer;color:var(--muted)}
.v1422-catalog-card.sel .v1422-card-select{background:var(--primary,#2563eb);color:#fff;border-color:var(--primary,#2563eb)}
.v1422-svc-row{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--brd,var(--line))}
.v1422-svc-row:last-child{border-bottom:none}
.v1422-toggle{border:1px solid var(--brd,var(--line));background:var(--surface-2,var(--surface));color:var(--muted);border-radius:999px;min-height:32px;padding:0 12px;font-size:12px;font-weight:var(--fw-semibold,650);cursor:pointer;flex-shrink:0;white-space:nowrap}
.v1422-toggle.on{background:var(--ok-bg,rgba(34,197,94,.1));color:var(--green,#16a34a);border-color:var(--green,#16a34a)}
.v1422-svc-name{flex:1;font-size:13px;color:var(--txt,var(--ink))}
.v1422-svc-price{font-size:12px;color:var(--muted);white-space:nowrap}
.v1422-qty{width:56px;border:1px solid var(--brd,var(--line));background:var(--surface-2);color:var(--txt,var(--ink));border-radius:8px;padding:4px 8px;font-size:12px}
.v1422-handle-label{font-size:12px;font-weight:var(--fw-semibold,650);color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px}
.v1422-handle-row{display:flex;gap:8px;flex-wrap:wrap}
.v1422-hbtn{border:1px solid var(--brd,var(--line));border-radius:999px;padding:6px 16px;font-size:13px;cursor:pointer;background:var(--surface-2);color:var(--txt,var(--ink));font-weight:var(--fw-semibold,650)}
.v1422-hbtn.active{background:var(--primary,#2563eb);color:#fff;border-color:var(--primary,#2563eb)}
.v1422-sep{height:1px;background:var(--brd,var(--line));margin:14px 0}
.v1422-seclbl{font-size:12px;font-weight:var(--fw-semibold,650);color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px;margin-top:14px}
.v1422-shape-row{display:flex;gap:8px;margin-bottom:12px}
.v1422-led-len{width:72px;border:1px solid var(--brd,var(--line));background:var(--surface-2);color:var(--txt,var(--ink));border-radius:8px;padding:4px 8px;font-size:12px}
.v1422-wv{max-width:800px;margin:0 auto;padding:4px}
</style>
<script>
// v10.4.22 — Block 3.1 Theme fix + Block 4 WorkView
// Wrap-don't-rewrite. Cross-block via window. UNTOUCHED: totals(), MAIN_KEY, statusClassV473
(function(){
'use strict';
var V = 'v10.4.22 WorkView+Theme';
var TKEY = 'anbamo_theme_v1422';

// ═══════════════════════════════════════════════════════════════════
// BLOCK 3.1 — THEME PERSISTENCE
// ═══════════════════════════════════════════════════════════════════
(function() {
  var stored;
  try { stored = localStorage.getItem(TKEY); } catch(err) {}
  if (stored) {
    if (typeof state !== 'undefined' && state.ui) state.ui.theme = stored;
  } else {
    var init = (typeof state !== 'undefined' && state.ui && state.ui.theme && state.ui.theme !== 'system')
      ? state.ui.theme : 'light';
    try { localStorage.setItem(TKEY, init); } catch(err) {}
    if (typeof state !== 'undefined' && state.ui) state.ui.theme = init;
  }
})();

var _origAT1422 = (typeof applyTheme === 'function') ? applyTheme : null;
if (_origAT1422) {
  window.applyTheme = function() {
    _origAT1422.apply(this, arguments);
    if (typeof state !== 'undefined' && state.ui) {
      try { localStorage.setItem(TKEY, state.ui.theme || 'light'); } catch(err) {}
    }
  };
  window.applyTheme();
}

// ═══════════════════════════════════════════════════════════════════
// BLOCK 4.9 — MEASURE DEFAULT TAB → ПАСПОРТ (one-time migration)
// ═══════════════════════════════════════════════════════════════════
(function() {
  if (typeof state !== 'undefined' && state.measureUi && !state.measureUi._v1422p) {
    if (!state.measureUi.activeStep || state.measureUi.activeStep === 'positions') {
      state.measureUi.activeStep = 'passport';
    }
    state.measureUi._v1422p = true;
    if (typeof markDirty === 'function') markDirty();
  }
})();

// ═══════════════════════════════════════════════════════════════════
// BLOCK 4 — WORKING TECHNICAL VIEW: HELPERS
// ═══════════════════════════════════════════════════════════════════
function n1422(v) { return typeof num === 'function' ? num(v) : (Number(String(v == null ? 0 : v).replace(',', '.')) || 0); }
function m1422(v) { return typeof money === 'function' ? money(v) : (Math.round(n1422(v)) + ' €'); }
function e1422(v) {
  return String(v == null ? '' : v).replace(/[&<>"']/g, function(c) {
    return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c];
  });
}

function getFacadeCatalog() {
  var fromState = (typeof state !== 'undefined' && Array.isArray(state.customPriceItems))
    ? state.customPriceItems.filter(function(x) { return (x.cat || x.category) === 'facade'; })
    : [];
  if (fromState.length) return fromState;
  var s = document.getElementById('ownerCatalogV1415');
  if (s) {
    try { return JSON.parse(s.textContent).filter(function(x) { return x.cat === 'facade'; }); } catch(e2) {}
  }
  return [];
}

function accHtml(id, title, summary, body) {
  var open = !!(state.accOpen1422 && state.accOpen1422[id]);
  return '<div class="v1422-acc card' + (open ? ' open' : '') + '" data-v1422acc="' + id + '">'
    + '<button class="v1422-acc-head" data-action="v1422-acc" data-id="' + id + '">'
    + '<div class="v1422-acc-head-left">'
    + '<span class="v1422-acc-title">' + e1422(title) + '</span>'
    + '<span class="v1422-acc-sum">' + e1422(summary) + '</span>'
    + '</div><span class="v1422-chev">▾</span>'
    + '</button>'
    + '<div class="v1422-acc-body">' + body + '</div>'
    + '</div>';
}

// ── 4.1/4.2/4.3: Facade accordion ──────────────────────────────────────────
function buildFacadeAcc() {
  if (typeof ensureV1043State === 'function') ensureV1043State();
  state.wf1422 = state.wf1422 || {zone: 'lower'};
  var wf = state.wf1422;
  var activeZone = wf.zone || 'lower';
  var zoneIds = ['lower', 'upper', 'tall', 'panels'];
  var zones = (state.zones || []).filter(function(z) { return zoneIds.indexOf(z.id) >= 0; });
  var zone = null;
  for (var zi = 0; zi < zones.length; zi++) { if (zones[zi].id === activeZone) { zone = zones[zi]; break; } }
  if (!zone && zones.length) zone = zones[0];

  // Zone tabs
  var tabsHtml = '<div class="v1422-ztabs">'
    + zones.map(function(z) {
        return '<button class="v1422-zone-tab' + (z.id === activeZone ? ' active' : '') + '"'
          + ' data-action="v1422-zone" data-zone="' + z.id + '">' + e1422(z.name) + '</button>';
      }).join('') + '</div>';

  // Zone size inputs + steppers
  var sizeHtml = '';
  if (zone) {
    var stpr = (typeof stepper === 'function')
      ? '<div class="grid g2" style="margin-bottom:12px"><div>' + stepper('Двери', 'doors', zone.doors, zone.id) + '</div><div>' + stepper('Ящики', 'drawers', zone.drawers, zone.id) + '</div></div>'
      : '';
    sizeHtml = '<div class="grid g2" style="margin-bottom:12px">'
      + '<div class="field"><label>Длина, м</label>'
      + '<input data-bind="zone:' + zone.id + '.len" value="' + e1422(zone.len) + '" type="number" inputmode="decimal"></div>'
      + '<div class="field"><label>Высота, мм</label>'
      + '<input data-bind="zone:' + zone.id + '.height" value="' + e1422(zone.height) + '" type="number" inputmode="decimal"></div>'
      + '</div>' + stpr;
  }

  // Facade catalog cards (4.2/4.3: compact, no selling copy)
  var catalog = getFacadeCatalog();
  var selName = wf['sel_' + activeZone] || '';
  var seclbl = '<div class="v1422-seclbl">Материал ' + e1422(zone ? zone.name : activeZone) + '</div>';
  var cardsHtml = seclbl;
  if (catalog.length) {
    cardsHtml += catalog.map(function(item, idx) {
      var isSel = selName === item.name;
      return '<div class="v1422-catalog-card' + (isSel ? ' sel' : '') + '"'
        + ' data-action="v1422-facade" data-idx="' + idx + '" data-zone="' + activeZone + '">'
        + '<div><div class="v1422-card-name">' + e1422(item.name) + '</div>'
        + '<div class="v1422-card-sup">' + e1422(item.supplier || '') + '</div></div>'
        + '<div class="v1422-card-right">'
        + '<div class="v1422-card-price">' + m1422(item.price) + ' / ' + e1422(item.unit || 'м\xb2') + '</div>'
        + '<button class="v1422-card-select">' + (isSel ? '✓ Выбрано' : 'Выбрать') + '</button>'
        + '</div></div>';
    }).join('');
  } else {
    cardsHtml += '<div class="notice warn">Каталог пуст — импортируйте прайс в Настройках.</div>';
  }

  var lName = (wf.sel_lower || '—').substring(0, 20);
  var uName = (wf.sel_upper || '—').substring(0, 20);
  var summary = 'Низ: ' + lName + ' \xb7 Верх: ' + uName;
  return accHtml('facades', 'Фасады', summary, tabsHtml + sizeHtml + cardsHtml);
}

// ── 4.8: Countertop accordion with corner option ─────────────────────────────
function buildTopAcc() {
  var t = state.top || {};
  var shape = state.topShape1422 || 'straight';
  var available = [];
  var topMats = state.topMaterials || {};
  var keys = Object.keys(topMats);
  for (var ki = 0; ki < keys.length; ki++) {
    var m = topMats[keys[ki]];
    if (m.active !== false) available.push([keys[ki], m]);
  }

  var enableBtn = '<div style="margin-bottom:12px"><button class="chip' + (t.enabled ? ' active' : '') + '" data-action="toggleTop">'
    + (t.enabled ? '✓ ' : '') + 'Столешница нужна</button></div>';

  var body = enableBtn;
  if (t.enabled) {
    body += '<div class="v1422-seclbl">Материал</div>'
      + '<div class="chip-row" style="margin-bottom:12px">'
      + available.map(function(pair) {
          return '<button class="chip' + (t.material === pair[0] ? ' active' : '') + '" data-action="setTopMaterial" data-id="' + pair[0] + '">'
            + e1422(pair[1].client || pair[1].name) + '</button>';
        }).join('')
      + '</div>';

    body += '<div class="v1422-seclbl">Форма</div>'
      + '<div class="v1422-shape-row">'
      + '<button class="v1422-zone-tab' + (shape === 'straight' ? ' active' : '') + '" data-action="v1422-top-shape" data-shape="straight">Прямая</button>'
      + '<button class="v1422-zone-tab' + (shape === 'corner' ? ' active' : '') + '" data-action="v1422-top-shape" data-shape="corner">Угловая (L)</button>'
      + '</div>';

    if (shape === 'straight') {
      body += '<div class="grid g2" style="margin-bottom:10px">'
        + '<div class="field"><label>Длина, м</label><input data-bind="top.len" value="' + e1422(t.len) + '" type="number" inputmode="decimal"></div>'
        + '<div class="field"><label>Глубина, мм</label><input data-bind="top.depth" value="' + e1422(t.depth) + '" type="number" inputmode="decimal"></div>'
        + '</div>';
      if (typeof stepper === 'function') {
        body += '<div class="grid g2" style="margin-bottom:10px"><div>'
          + stepper('Вырез мойка', 'sinkCuts', t.sinkCuts, 'top')
          + '</div><div>' + stepper('Вырез плита', 'hobCuts', t.hobCuts, 'top') + '</div></div>';
      }
    } else {
      var la = n1422(state.topLenA1422 != null ? state.topLenA1422 : (t.len || 0));
      var lb = n1422(state.topLenB1422 || 0);
      var cornerV = state.topCorner1422 || 'euro';
      body += '<div class="grid g2" style="margin-bottom:10px">'
        + '<div class="field"><label>Длина A, м</label><input data-action="v1422-top-lena" value="' + la + '" type="number" inputmode="decimal"></div>'
        + '<div class="field"><label>Длина B, м</label><input data-action="v1422-top-lenb" value="' + lb + '" type="number" inputmode="decimal"></div>'
        + '</div>'
        + '<div class="field" style="margin-bottom:10px"><label>Глубина, мм</label><input data-bind="top.depth" value="' + e1422(t.depth) + '" type="number" inputmode="decimal"></div>'
        + '<div class="v1422-seclbl">Тип угла</div>'
        + '<div class="chip-row" style="margin-bottom:10px">'
        + '<button class="chip' + (cornerV === 'euro' ? ' active' : '') + '" data-action="v1422-corner" data-v="euro">Еврозапил (+54€)</button>'
        + '<button class="chip' + (cornerV === 'miter' ? ' active' : '') + '" data-action="v1422-corner" data-v="miter">Стык</button>'
        + '<button class="chip' + (cornerV === 'custom' ? ' active' : '') + '" data-action="v1422-corner" data-v="custom">Вручную</button>'
        + '</div>'
        + '<div class="notice" style="font-size:12px">В расчёт: ' + (la + lb).toFixed(2) + ' м.п. (A ' + la.toFixed(2) + ' + B ' + lb.toFixed(2) + ')</div>';
    }

    body += '<div class="v1422-seclbl" style="margin-top:12px">Тип мойки</div>'
      + '<div class="chip-row">'
      + '<button class="chip' + (t.sinkType === 'surface' ? ' active' : '') + '" data-action="sinkType" data-type="surface">Накладная</button>'
      + '<button class="chip' + (t.sinkType === 'under' ? ' active' : '') + '" data-action="sinkType" data-type="under">Подстольная</button>'
      + '</div>';
  }

  var matName = '';
  if (t.enabled && topMats[t.material]) matName = topMats[t.material].client || topMats[t.material].name || '';
  var shapeNote = (shape === 'corner') ? ' (L)' : '';
  var summ = t.enabled
    ? (e1422(matName) + ' \xb7 ' + n1422(t.len).toFixed(1) + ' м' + shapeNote)
    : 'не нужна';
  return accHtml('countertop', 'Столешница', summ, body);
}

// ── 4.6/4.10: Hardware + improvements accordion ──────────────────────────────
function buildHwAcc() {
  if (typeof ensureV1043State === 'function') ensureV1043State();
  var hw = state.hardware || {};
  var hMode = hw.handlesMode || 'we';
  var imprs = state.improvements || [];

  // 4.10: Ручки group with label
  var handlesHtml = '<div class="v1422-handle-label">Ручки</div>'
    + '<div class="v1422-handle-row">'
    + '<button class="v1422-hbtn' + (hMode === 'client' ? ' active' : '') + '" data-action="setHandleMode" data-mode="client">Клиент покупает сам</button>'
    + '<button class="v1422-hbtn' + (hMode === 'we' ? ' active' : '') + '" data-action="setHandleMode" data-mode="we">Мы подберём</button>'
    + '<button class="v1422-hbtn' + (hMode === 'later' ? ' active' : '') + '" data-action="setHandleMode" data-mode="later">Уточнить позже</button>'
    + '</div>'
    + (hMode === 'client'
      ? '<div class="field" style="margin-top:10px;max-width:160px"><label>Ручки, шт.</label>'
        + '<input data-bind="hardware.handlesCount" value="' + e1422(hw.handlesCount) + '" type="number" inputmode="decimal"></div>'
      : '');

  // 4.6: improvements as simple on/off toggles
  var visible = imprs.filter(function(i) { return i.show !== false && i.active !== false; });
  var improveHtml = visible.length
    ? ('<div class="v1422-sep"></div><div class="v1422-handle-label">Доп. опции</div>'
      + visible.map(function(i) {
          var v = typeof improvementValue === 'function' ? improvementValue(i) : {sell: n1422(i.price), visible: true};
          var isOn = i.status === 'included';
          var sellVal = n1422(v.sell);
          var priceStr;
          if (i.id === 'led') {
            if (isOn && n1422(i.meters) > 0) priceStr = '+' + m1422(sellVal);
            else if (isOn) priceStr = 'укажите длину';
            else priceStr = '+' + m1422(sellVal) + '/м';
          } else {
            priceStr = '+' + m1422(sellVal);
          }
          var ledInput = (i.id === 'led' && isOn)
            ? ('<input class="v1422-led-len" data-bind="improvement:led.meters"'
               + ' value="' + e1422(i.meters || '') + '" type="number" inputmode="decimal" placeholder="м">')
            : '';
          return '<div class="v1422-svc-row">'
            + '<button class="v1422-toggle' + (isOn ? ' on' : '') + '" data-action="v1422-impr" data-id="' + i.id + '">'
            + (isOn ? 'ВКЛ' : 'ВЫКЛ') + '</button>'
            + '<span class="v1422-svc-name">' + e1422(i.title) + '</span>'
            + '<span class="v1422-svc-price">' + priceStr + '</span>'
            + ledInput + '</div>';
        }).join(''))
    : '';

  var hLabel = hMode === 'client' ? 'клиент' : hMode === 'later' ? 'уточнить' : 'мы';
  var hasOn = imprs.some(function(i) { return i.status === 'included'; });
  var summ = 'Ручки: ' + hLabel + (hasOn ? ' \xb7 есть доп.' : '');
  return accHtml('hardware', 'Комплектующие и опции', summ, handlesHtml + improveHtml);
}

// ── 4.7: Services accordion ───────────────────────────────────────────────────
function buildSvcAcc() {
  if (typeof ensureV1414 === 'function') ensureV1414();
  var extras = state.extraWorksCatalog ? Object.keys(state.extraWorksCatalog) : [];
  if (!extras.length) {
    return accHtml('services', 'Услуги', 'нет',
      '<div class="notice">Каталог услуг пуст. Откройте Настройки.</div>');
  }
  var body = extras.map(function(id) {
    var item = state.extraWorksCatalog[id];
    var isOn = !!item.v1422on;
    var price = n1422(item.price);
    var priceStr = price > 0 ? (m1422(price) + '/' + e1422(item.unit || 'усл.')) : '—';
    return '<div class="v1422-svc-row">'
      + '<button class="v1422-toggle' + (isOn ? ' on' : '') + '" data-action="v1422-svc" data-id="' + e1422(id) + '">'
      + (isOn ? 'ВКЛ' : 'ВЫКЛ') + '</button>'
      + '<span class="v1422-svc-name">' + e1422(item.client || item.tech || id) + '</span>'
      + '<span class="v1422-svc-price">' + priceStr + '</span>'
      + (isOn
        ? ('<input class="v1422-qty" data-action="v1422-svc-qty" data-id="' + e1422(id) + '"'
           + ' value="' + e1422(item.v1422qty || 1) + '" type="number" inputmode="decimal">')
        : '')
      + '</div>';
  }).join('');

  var onCount = extras.filter(function(id) { return state.extraWorksCatalog[id].v1422on; }).length;
  var summ = onCount ? (onCount + ' вкл.') : 'не выбраны';
  return accHtml('services', 'Услуги', summ, body);
}

// ── Main render ───────────────────────────────────────────────────────────────
function renderWorkView1422() {
  if (typeof ensureV1043State === 'function') ensureV1043State();
  var t = typeof totals === 'function' ? totals() : {totalClient: 0, margin: 0};
  var trafficHtml = typeof renderTrafficBox === 'function'
    ? ('<div class="card" style="margin-top:10px">' + renderTrafficBox() + '</div>') : '';

  var hdr = '<div class="v1422-header">'
    + '<div><div class="v1422-client-name">' + e1422(state.project.client || 'Новый проект') + '</div>'
    + '<div class="v1422-client-sub">'
    + e1422(state.project.status || '') + ' \xb7 ' + e1422(state.project.want || '')
    + '</div></div>'
    + '<div class="v1422-total">' + m1422(t.totalClient)
    + '<small>' + Math.round(t.margin || 0) + '% маржа</small></div>'
    + '</div>';

  return '<div class="v1422-wv">'
    + hdr
    + buildFacadeAcc()
    + buildTopAcc()
    + buildHwAcc()
    + buildSvcAcc()
    + trafficHtml
    + '</div>';
}

// Replace renderFast (4.1-4.10)
window.renderFast = function() {
  var pane = document.getElementById('pane-fast');
  if (pane) pane.innerHTML = renderWorkView1422();
};

// ── Click handler (capture phase, v1422-* actions only) ───────────────────────
document.addEventListener('click', function(e) {
  var b = e.target.closest('[data-action]');
  if (!b) return;
  var a = b.dataset.action;
  if (!a || a.indexOf('v1422-') !== 0) return;
  e.preventDefault();
  e.stopImmediatePropagation();

  state.accOpen1422 = state.accOpen1422 || {};
  state.wf1422 = state.wf1422 || {};

  if (a === 'v1422-acc') {
    state.accOpen1422[b.dataset.id] = !state.accOpen1422[b.dataset.id];
    if (typeof renderCurrent === 'function') renderCurrent();
    return;
  }

  if (a === 'v1422-zone') {
    state.wf1422.zone = b.dataset.zone;
    if (typeof renderCurrent === 'function') renderCurrent();
    return;
  }

  if (a === 'v1422-facade') {
    var cat = getFacadeCatalog();
    var idx = parseInt(b.dataset.idx, 10);
    var item = cat[idx];
    if (!item) return;
    var zone = b.dataset.zone || state.wf1422.zone || 'lower';
    state.wf1422['sel_' + zone] = item.name;
    // Bridge: update selected material price/cost so totals() uses catalog price
    var matId = state.selectedMaterial || (state.materials && state.materials[0] && state.materials[0].id);
    var mat = null;
    if (matId && state.materials) {
      for (var mi = 0; mi < state.materials.length; mi++) {
        if (state.materials[mi].id === matId) { mat = state.materials[mi]; break; }
      }
    }
    if (mat && n1422(item.price) > 0) {
      mat.price = n1422(item.price);
      mat.cost = n1422(item.cost);
      mat.tech = item.name;
    }
    if (typeof renderCurrent === 'function') renderCurrent();
    return;
  }

  if (a === 'v1422-top-shape') {
    state.topShape1422 = b.dataset.shape;
    if (b.dataset.shape === 'straight') { state.topLenA1422 = null; state.topLenB1422 = null; }
    if (typeof renderCurrent === 'function') renderCurrent();
    return;
  }

  if (a === 'v1422-corner') {
    state.topCorner1422 = b.dataset.v;
    if (typeof renderCurrent === 'function') renderCurrent();
    return;
  }

  if (a === 'v1422-impr') {
    var impr = null;
    var imprs = state.improvements || [];
    for (var ii = 0; ii < imprs.length; ii++) {
      if (imprs[ii].id === b.dataset.id) { impr = imprs[ii]; break; }
    }
    if (impr) {
      var nowOn = impr.status !== 'included';
      if (typeof setImproveStatus === 'function') {
        setImproveStatus(impr.id, nowOn ? 'included' : 'recommend');
      } else {
        impr.status = nowOn ? 'included' : 'recommend';
        impr.selected = nowOn;
      }
    }
    if (typeof renderCurrent === 'function') renderCurrent();
    return;
  }

  if (a === 'v1422-svc') {
    var svcId = b.dataset.id;
    var svcItem = state.extraWorksCatalog && state.extraWorksCatalog[svcId];
    if (svcItem) {
      svcItem.v1422on = !svcItem.v1422on;
      if (svcItem.v1422on && !svcItem.v1422qty) svcItem.v1422qty = 1;
    }
    if (typeof renderCurrent === 'function') renderCurrent();
    return;
  }
}, true);

// ── Input handler for corner top lengths + service qty ────────────────────────
document.addEventListener('input', function(e) {
  var x = e.target;
  if (x.dataset.action === 'v1422-top-lena') {
    state.topLenA1422 = n1422(x.value);
    if (!state.top) state.top = {};
    state.top.len = n1422(state.topLenA1422) + n1422(state.topLenB1422 || 0);
    if (typeof renderHeader === 'function') renderHeader();
    if (typeof markDirty === 'function') markDirty();
    return;
  }
  if (x.dataset.action === 'v1422-top-lenb') {
    state.topLenB1422 = n1422(x.value);
    if (!state.top) state.top = {};
    state.top.len = n1422(state.topLenA1422 || 0) + n1422(state.topLenB1422);
    if (typeof renderHeader === 'function') renderHeader();
    if (typeof markDirty === 'function') markDirty();
    return;
  }
  if (x.dataset.action === 'v1422-svc-qty') {
    var svcItem = state.extraWorksCatalog && state.extraWorksCatalog[x.dataset.id];
    if (svcItem) svcItem.v1422qty = n1422(x.value);
    if (typeof markDirty === 'function') markDirty();
    return;
  }
}, true);

window.__v1422 = {V: V, renderWorkView1422: renderWorkView1422};
console.info('[v10.4.22] Theme fix + WorkView layer loaded');
})();
</script>
"""

# ── Build ─────────────────────────────────────────────────────────────────────
body_tag = '<body'
body_open_end = src.index(body_tag) + src[src.index(body_tag):].index('>') + src.index(body_tag) + 1
# Find the end of <body ...> tag
pos = src.index(body_tag)
end = src.index('>', pos) + 1
result = src[:end] + '\n' + EARLY + src[end:]
result = result.replace('</body>', LAYER + '\n</body>', 1)

# ── Gate assertions ───────────────────────────────────────────────────────────
assert 'anbamo_theme_v1422'            in result, "ASSERT: TKEY missing"
assert '_origAT1422'                   in result, "ASSERT: applyTheme wrap missing"
assert 'v1422-facade'                  in result, "ASSERT: facade action missing"
assert 'v1422-impr'                    in result, "ASSERT: impr toggle missing"
assert 'v1422-svc'                     in result, "ASSERT: svc toggle missing"
assert 'v1422-top-shape'               in result, "ASSERT: shape toggle missing"
assert 'v1422-top-lenb'                in result, "ASSERT: corner lenB missing"
assert 'setHandleMode'                 in result, "ASSERT: handle mode missing"
assert 'v1422-acc'                     in result, "ASSERT: accordion missing"
assert '_v1422p'                       in result, "ASSERT: passport migration missing"
assert 'anbamo_theme_v1422'            in result, "ASSERT: quick theme key missing"
assert 'renderWorkView1422'            in result, "ASSERT: working view function missing"
assert 'ownerCatalogV1415'             in result, "ASSERT: catalog fallback missing"
assert 'v1422-zone'                    in result, "ASSERT: zone tab missing"
assert 'anbamo_v10_4_6_mvp_stabilization' in result, "ASSERT: MAIN_KEY still present"
assert result.count('</body>') == 1,              "ASSERT: multiple </body>"
assert result.count('</script>') > 5,             "ASSERT: scripts missing"

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(result)

sl = src.count('\n')
ol = result.count('\n')
print(f"OK  {os.path.basename(OUT)}")
print(f"    {sl} -> {ol} lines  (+{ol-sl})")
print(f"    {len(src):,} -> {len(result):,} chars  (+{len(result)-len(src):,})")
