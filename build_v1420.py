#!/usr/bin/env python3
"""Build v10.4.20 — Block 2: Header ZF + compact layout + dead-mode-btn removal + snapshot move"""

import os

BASE = r"C:\Users\Win\OneDrive\Документы\New project 4\Фасадный калькулятор\revival"
SRC  = os.path.join(BASE, "AN_BAMO_Command_Center_v10_4_19_Block1_DeadButtons.html")
OUT  = os.path.join(BASE, "AN_BAMO_Command_Center_v10_4_20_Header_ZF.html")

with open(SRC, encoding="utf-8") as f:
    src = f.read()

assert "</body>" in src,            "ASSERT: no </body>"
assert "injectTopbar" in src,       "ASSERT: no injectTopbar"
assert "openMenu17" in src,         "ASSERT: no openMenu17"
assert "v10.4.19" in src or "v1419" in src.lower(), "ASSERT: base not v10.4.19"

LAYER = """
<style>
/* ====================================================
   v10.4.20 Block 2 — Header ZF
   ==================================================== */

/* 1. Remove mode button from header (moved to menu) */
#v1417-mode { display: none !important; }

/* 2. Single-row header on ALL widths */
.v1417-bar { flex-wrap: nowrap !important; }

/* 3. DOM order fix: brand(1) | center(2) | right(3) */
.v1417-brand  { order: 1 !important; flex-shrink: 0 !important; }
.v1417-center { order: 2 !important; flex: 1 1 0 !important; min-width: 0 !important; margin: 0 6px !important; }
.v1417-right  { order: 3 !important; margin-left: 0 !important; }

/* 4. App name fits (ZF = 2 chars) */
.v1417-appname { font-size: 14px !important; }

/* 5. Compact project name */
.v1417-proj-name { max-width: 100px !important; }

/* 6. Status text no overflow */
#v1417-status-text {
  overflow: hidden; text-overflow: ellipsis;
  white-space: nowrap; max-width: 72px;
  display: inline-block; vertical-align: middle;
}
</style>

<script>
// v10.4.20 Block 2 — Header ZF
// Wrap-don't-rewrite. Cross-block helpers -> window.
// Invariants: totals(), localStorage key, window.statusClassV473 unchanged.
(function(){
'use strict';
var V='v10.4.20 Block2 HeaderZF';

/* ---- A: one-time ZF migration ---- */
function ensure1420(){
  if(!state._zfMigrated1420){
    if(!state.appName||state.appName==='Замена фасадов')state.appName='ZF';
    state._zfMigrated1420=true;
    if(typeof markDirty==='function')markDirty();
  }
  if(!state.ui)state.ui={};
}

/* ---- B: DOM sync after topbar injection ---- */
function patchTopbar1420(){
  var el=document.getElementById('v1417-appname');
  if(el)el.textContent=(state&&state.appName)||'ZF';
  var mBtn=document.getElementById('v1417-mode');
  if(mBtn)mBtn.style.setProperty('display','none','important');
}
window.patchTopbar1420=patchTopbar1420;

/* ---- C: wrap renderHeader ---- */
var _rh20=typeof renderHeader==='function'?renderHeader:null;
if(_rh20){
  window.renderHeader=renderHeader=function(){
    _rh20.apply(this,arguments);
    ensure1420();
    patchTopbar1420();
  };
}

/* ---- D: wrap renderRequest — hide "Версии / слепки" card ---- */
var _rr20=typeof renderRequest==='function'?renderRequest:null;
if(_rr20){
  window.renderRequest=renderRequest=function(){
    _rr20.apply(this,arguments);
    var pane=document.getElementById('pane-request');
    if(!pane)return;
    pane.querySelectorAll('.card').forEach(function(c){
      var t=c.querySelector('.title');
      if(t&&/Версии|слепк/i.test(t.textContent))c.style.display='none';
    });
  };
}

/* ---- E: intercept menu click (capture) -> patched menu ---- */
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-action]');
  if(!b)return;
  if(b.dataset.action!=='v1417-menu')return;
  e.preventDefault();
  e.stopImmediatePropagation();
  openMenu1420();
},true);

/* ---- F: patched menu ---- */
function openMenu1420(){
  if(typeof state==='undefined')return;
  var isTech=!!(state.ui&&state.ui.tech);
  var theme=(state.ui&&state.ui.theme)||'system';
  var html=
    '<div style="padding:4px 0">'+
    '<div class="section-title">Режим просмотра</div>'+
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:14px">'+
      '<button class="btn'+(isTech?'':' primary')+'" data-action="v1420-mode" data-tech="0">👁 Для клиента</button>'+
      '<button class="btn'+(isTech?' primary':'')+'" data-action="v1420-mode" data-tech="1">🔧 Внутренний</button>'+
    '</div>'+
    '<div class="section-title">Проект</div>'+
    '<div style="display:grid;gap:6px;margin-bottom:14px">'+
      '<button class="btn primary" data-action="v1417-projects">📁 Открыть / переключить проект</button>'+
      '<button class="btn" data-action="v1420-snapshot">📷 Слепок версии</button>'+
    '</div>'+
    '<div class="section-title">Тема</div>'+
    '<div class="chip-row" style="margin-bottom:16px">'+
      '<button class="chip'+(theme==='light'?' active':'')+'" data-action="v1417-theme" data-value="light">☀️ Светлая</button>'+
      '<button class="chip'+(theme==='dark'?' active':'')+'" data-action="v1417-theme" data-value="dark">🌙 Тёмная</button>'+
      '<button class="chip'+(theme==='system'?' active':'')+'" data-action="v1417-theme" data-value="system">◐ Авто</button>'+
    '</div>'+
    '<div class="grid" style="gap:8px">'+
      '<button class="btn" data-action="v1417-goto-settings">⚙ Настройки</button>'+
      '<button class="btn" data-action="v1417-export">↓ Экспорт JSON</button>'+
      '<button class="btn" data-action="v1417-import">↑ Импорт JSON</button>'+
      '<button class="btn" data-action="v1417-about">ℹ О программе</button>'+
    '</div>'+
    '</div>';
  if(typeof openModal==='function')openModal('Меню',html);
}
window.openMenu1420=openMenu1420;

/* ---- G: v1420-* action handlers (capture) ---- */
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-action]');
  if(!b)return;
  var a=b.dataset.action;

  if(a==='v1420-mode'){
    e.preventDefault();e.stopImmediatePropagation();
    if(typeof state==='undefined'||!state.ui)return;
    var tech=b.dataset.tech==='1';
    state.ui.tech=tech;
    if(typeof closeModal==='function')closeModal();
    if(typeof toast==='function')toast(tech
      ?'Внутренний режим: маржа и себестоимость видны.'
      :'Режим клиента: себестоимость скрыта.');
    if(typeof renderCurrent==='function')renderCurrent();
    return;
  }

  if(a==='v1420-snapshot'){
    e.preventDefault();e.stopImmediatePropagation();
    if(typeof closeModal==='function')closeModal();
    setTimeout(function(){
      if(typeof totals!=='function'||typeof state==='undefined')return;
      var t=totals();
      var name=prompt('Название слепка','После замера');
      if(name===null)return;
      if(!name)name='Версия '+((state.versions||[]).length+1);
      if(!Array.isArray(state.versions))state.versions=[];
      var id=typeof uid==='function'?uid('ver'):Date.now().toString(36);
      var snap=typeof clone==='function'?clone(state):JSON.parse(JSON.stringify(state));
      state.versions.unshift({id:id,name:name,date:new Date().toISOString(),total:t.totalClient,snapshot:snap});
      if(typeof toast==='function')toast('«'+name+'» сохранён');
      if(typeof saveNow==='function')saveNow();
    },80);
    return;
  }
},true);

/* ---- H: initial patch ---- */
try{ensure1420();}catch(e){}
patchTopbar1420();

window.__v1420={V:V,ensure1420:ensure1420,patchTopbar1420:patchTopbar1420,openMenu1420:openMenu1420,built:'2026-06-19'};
})();
</script>
"""

result = src.replace("</body>", LAYER + "\n</body>", 1)

assert "v1420-mode"      in result, "ASSERT: v1420-mode missing"
assert "openMenu1420"    in result, "ASSERT: openMenu1420 missing"
assert "v1420-snapshot"  in result, "ASSERT: v1420-snapshot missing"
assert "#v1417-mode"     in result, "ASSERT: mode hide CSS missing"
assert "_zfMigrated1420" in result, "ASSERT: ZF migration missing"
assert "patchTopbar1420" in result, "ASSERT: patchTopbar1420 missing"
assert "Версии|слепк"    in result, "ASSERT: snapshot card removal missing"
assert "Открыть / переключить проект" in result, "ASSERT: open project missing"
assert result.count("</body>") == 1, "ASSERT: multiple </body>"

with open(OUT, "w", encoding="utf-8") as f:
    f.write(result)

sl, ol = src.count("\n"), result.count("\n")
print(f"OK  {os.path.basename(OUT)}")
print(f"    {sl} -> {ol} lines  (+{ol-sl})")
print(f"    {len(src):,} -> {len(result):,} chars  (+{len(result)-len(src):,})")
