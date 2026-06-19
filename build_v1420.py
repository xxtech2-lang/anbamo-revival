#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build v10.4.20 — Header ZF + Project Context
Reads v10.4.19 base, appends one <style>+<script> IIFE layer before </body>.
"""
import sys, io, os, re, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(BASE_DIR, 'AN_BAMO_Command_Center_v10_4_19_Block1_DeadButtons.html')
DEST = os.path.join(BASE_DIR, 'AN_BAMO_Command_Center_v10_4_20_Header_ZF.html')

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

assert '</body>' in html, 'ERROR: no </body> in source file'

# ── New layer: style + script ──────────────────────────────────────────────────
LAYER = r"""
<style>
/* v10.4.20 Header ZF — compact single-row, mode in menu, project always visible */

/* 1. Hide legacy mode button (moved to ⋯ menu) */
#v1417-mode { display: none !important; }

/* 2. Always single-row header — no second-row wrap */
.v1417-bar { flex-wrap: nowrap !important; }
.v1417-center {
  order: 2;
  flex: 1 1 auto !important;
  max-width: none !important;
  min-width: 0;
  margin: 0 8px;
}
.v1417-right { order: 3; margin-left: 0; }

/* 3. Project name truncation on narrow screens */
.v1417-project-btn { max-width: min(200px, 38vw); }
.v1417-proj-name   { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 140px; }

/* 4. On very narrow screens compress the label */
@media (max-width: 420px) {
  .v1417-appname { font-size: 13px; }
  .v1417-logo { width: 26px; height: 26px; font-size: 10px; border-radius: 8px; }
  .v1417-proj-label { display: none; }
  .v1417-proj-name  { max-width: 90px; }
}
</style>

<script>
// v10.4.20 Header ZF + Project Context
// Architecture: one appended IIFE — wrap, not rewrite.
// Invariants: totals(), localStorage key, statusClassV473, state.company.name — untouched.
(function(){
'use strict';
var V='v10.4.20 Header ZF';
document.title='AN BAMO Command Center '+V;
if(typeof DEFAULT==='object'&&DEFAULT!==null)DEFAULT.version=V;

/* --- escape helper --- */
function h20(v){
  return String(v==null?'':v).replace(/[&<>"']/g,function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
  });
}

/* --- 1. Migrate appName default "Замена фасадов" → "ZF" --- */
function migrateAppName(){
  if(typeof state!=='object'||!state)return;
  if(!state.appName||state.appName==='Замена фасадов'){
    state.appName='ZF';
    var el=document.getElementById('v1417-appname');
    if(el)el.textContent='ZF';
    if(typeof markDirty==='function')markDirty();
  }
}

/* --- 2. updateH17 patch: change fallback text to 'ZF' --- */
/* We re-use the updateH17 exposed by __v1417, then patch the DOM fallback */
function syncAppNameEl(){
  var el=document.getElementById('v1417-appname');
  if(el&&typeof state!=='undefined'){
    el.textContent=state.appName||'ZF';
  }
}

/* Wrap renderHeader to also sync appName after header re-draws */
var _rhBase20=typeof renderHeader==='function'?renderHeader:null;
if(_rhBase20){
  window.renderHeader=renderHeader=function(){
    _rhBase20.apply(this,arguments);
    try{syncAppNameEl();}catch(e){}
  };
}

/* --- 3. Enhanced ⋯ menu with Mode + Open Project + Snapshots --- */
function openMenu1420(){
  if(typeof state!=='object'||!state)return;
  if(!state.ui)state.ui={};
  var isTech=!!state.ui.tech;
  var theme=state.ui.theme||'system';
  var versions=Array.isArray(state.versions)?state.versions:[];

  var html=
    '<div style="padding:4px 0">'+

    /* — Projects section — */
    '<div class="section-title">Проект</div>'+
    '<div class="grid g2" style="gap:8px;margin-bottom:14px">'+
      '<button class="btn primary" data-action="v1420-open-projects">📂 Открыть проект</button>'+
      '<button class="btn" data-action="v1420-new-project">＋ Новый проект</button>'+
    '</div>'+

    /* — Mode section — */
    '<div class="section-title">Режим просмотра</div>'+
    '<div class="chip-row" style="margin-bottom:14px">'+
      '<button class="chip'+(!isTech?' active':'')+'" data-action="v1420-mode" data-value="client">👁 Для клиента</button>'+
      '<button class="chip'+(isTech?' active':'')+'" data-action="v1420-mode" data-value="tech">🔧 Внутренний</button>'+
    '</div>'+

    /* — Theme section — */
    '<div class="section-title">Тема</div>'+
    '<div class="chip-row" style="margin-bottom:14px">'+
      '<button class="chip'+(theme==='light'?' active':'')+'" data-action="v1417-theme" data-value="light">☀️ Светлая</button>'+
      '<button class="chip'+(theme==='dark'?' active':'')+'" data-action="v1417-theme" data-value="dark">🌙 Тёмная</button>'+
      '<button class="chip'+(theme==='system'?' active':'')+'" data-action="v1417-theme" data-value="system">◐ Авто</button>'+
    '</div>'+

    /* — Actions — */
    '<div class="grid" style="gap:8px;margin-bottom:14px">'+
      '<button class="btn" data-action="v1417-goto-settings">⚙ Настройки</button>'+
      '<button class="btn" data-action="v1417-export">↓ Бэкап ⬇</button>'+
      '<button class="btn" data-action="v1417-import">↑ Импорт</button>'+
      '<button class="btn" data-action="v1417-about">ℹ О программе</button>'+
    '</div>'+

    /* — Snapshots (moved from Заявка) — */
    '<div class="section-title">Версии / слепки'+
      (versions.length?' ('+versions.length+')':'')+
    '</div>'+
    '<button class="btn" data-action="v1420-snapshots" style="width:100%;margin-bottom:4px">'+
      '📋 Слепки версий'+
    '</button>'+
    '</div>';

  if(typeof openModal==='function')openModal('Меню',html);
}

/* --- Snapshots modal --- */
function openSnapshotsModal1420(){
  var versions=Array.isArray(state&&state.versions)?state.versions:[];
  var html='<button class="btn primary" data-action="snapshot" style="width:100%;margin-bottom:12px">'+
    '+ Сделать слепок текущей версии</button>';
  if(versions.length){
    html+='<div class="row-list">'+
      versions.map(function(v){
        return '<div class="row-item">'+
          '<div><b>'+h20(v.name)+'</b>'+
          '<div class="meta">'+new Date(v.date).toLocaleString('ru-RU')+
          (typeof money==='function'?' · '+money(v.total):'')+
          '</div></div>'+
          '<div class="toolbar">'+
            '<button class="btn sm" data-action="restoreVersion" data-id="'+h20(v.id)+'">Открыть</button>'+
            '<button class="btn sm red" data-action="deleteVersion" data-id="'+h20(v.id)+'">✕</button>'+
          '</div></div>';
      }).join('')+
      '</div>';
  }else{
    html+='<div class="empty">Слепков пока нет — нажмите кнопку выше.</div>';
  }
  if(typeof openModal==='function')openModal('Версии / слепки',html);
}

/* --- 4. Capture click handler: intercept v1417-menu + new v1420 actions --- */
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-action]');
  if(!b)return;
  var a=b.dataset.action;
  if(!a)return;

  /* Replace the old ⋯ menu with our enhanced one */
  if(a==='v1417-menu'){
    e.stopImmediatePropagation();
    openMenu1420();
    return;
  }

  if(a==='v1420-open-projects'){
    e.stopImmediatePropagation();
    if(typeof closeModal==='function')closeModal();
    if(typeof openProjectsModal==='function')openProjectsModal();
    return;
  }

  if(a==='v1420-new-project'){
    e.stopImmediatePropagation();
    if(typeof closeModal==='function')closeModal();
    /* Small delay so modal closes before confirm dialog */
    setTimeout(function(){
      if(window.confirm('Очистить текущий проект?')){
        if(typeof DEFAULT!=='undefined'&&typeof clone==='function'){
          state=clone(DEFAULT);
          if(typeof toast==='function')toast('Новый проект создан');
          if(typeof renderCurrent==='function')renderCurrent();
        }
      }
    },120);
    return;
  }

  if(a==='v1420-mode'){
    e.stopImmediatePropagation();
    if(!state.ui)state.ui={};
    state.ui.tech=(b.dataset.value==='tech');
    if(typeof toast==='function')toast(state.ui.tech?'Внутренний режим: маржа и себестоимость видны.':'Режим клиента: себестоимость скрыта.');
    if(typeof closeModal==='function')closeModal();
    if(typeof renderCurrent==='function')renderCurrent();
    return;
  }

  if(a==='v1420-snapshots'){
    e.stopImmediatePropagation();
    if(typeof closeModal==='function')closeModal();
    openSnapshotsModal1420();
    return;
  }
},true); /* capture phase: fires before v10.4.17 bubble-phase handler */

/* --- 5. Hide "Версии / слепки" card on Заявка tab --- */
function hideVersionsCard1420(){
  var pane=document.getElementById('pane-request');
  if(!pane)return;
  pane.querySelectorAll('.card').forEach(function(c){
    var t=c.querySelector('.title');
    if(t&&/Версии|слепк/i.test(t.textContent)){
      c.style.display='none';
    }
  });
}

var _rrBase1420=typeof renderRequest==='function'?renderRequest:null;
if(_rrBase1420){
  window.renderRequest=renderRequest=function(){
    _rrBase1420.apply(this,arguments);
    try{hideVersionsCard1420();}catch(e){}
  };
}

/* --- 6. Settings block: update appName placeholder to 'ZF' --- */
var _rsBase1420=typeof renderSettings==='function'?renderSettings:null;
if(_rsBase1420){
  window.renderSettings=renderSettings=function(){
    _rsBase1420.apply(this,arguments);
    /* Patch the appName input placeholder from 'Замена фасадов' to 'ZF' */
    var pane=document.getElementById('pane-settings');
    if(!pane)return;
    pane.querySelectorAll('input[data-v1417bind="appName"]').forEach(function(inp){
      inp.placeholder='ZF';
      /* If the input still shows old default text, update it */
      if(inp.value==='Замена фасадов'){
        inp.value='ZF';
        if(typeof state!=='undefined')state.appName='ZF';
      }
    });
  };
}

/* --- 7. Init --- */
window.__v1420={V:V,hideVersionsCard1420:hideVersionsCard1420,openSnapshotsModal1420:openSnapshotsModal1420,built:'2026-06-19'};
migrateAppName();
hideVersionsCard1420();
if(typeof renderCurrent==='function')renderCurrent();

})();
</script>
"""

# Insert before </body>
html_new = html.replace('</body>', LAYER + '</body>', 1)
assert html_new != html, 'ERROR: replacement did not change the file'

with open(DEST, 'w', encoding='utf-8') as f:
    f.write(html_new)

lines_src  = html.count('\n')
lines_dest = html_new.count('\n')
print(f'OK  {os.path.basename(SRC)}  ({lines_src} lines)')
print(f'→   {os.path.basename(DEST)} ({lines_dest} lines, +{lines_dest-lines_src} lines)')
print('Build complete.')
