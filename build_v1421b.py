#!/usr/bin/env python3
"""Build v10.4.21b — Block 3 Fix: Multi-project flow
Fix 1: openModal wrapper intercepts 'Проекты' from v10.4.7.2 local scope
Fix 2: wrap clearProjectDraftKeepSettings via window.__v10472 + microtask persist MAIN_KEY
"""
import os

BASE = r"C:\Users\Win\OneDrive\Документы\New project 4\Фасадный калькулятор\revival"
SRC  = os.path.join(BASE, "AN_BAMO_Command_Center_v10_4_21_Projects_Safety.html")
OUT  = os.path.join(BASE, "AN_BAMO_Command_Center_v10_4_21b_Projects_Fix.html")

with open(SRC, encoding="utf-8") as f:
    src = f.read()

assert "</body>"          in src, "ASSERT: no </body>"
assert "openProjects1421" in src, "ASSERT: v10.4.21 layer not found in base"
assert "anbamo_v10_4_6_mvp_stabilization" in src, "ASSERT: MAIN_KEY missing"

LAYER = """
<style>
/* v10.4.21b fix — no additional styles */
</style>
<script>
// v10.4.21b — Block 3 Fix: Multi-project flow
// Fix 1: Wrap openModal to catch ALL 'Проекты' calls (incl. v10.4.7.2 local scope)
// Fix 2: Wrap clearProjectDraftKeepSettings in window.__v10472 — persists MAIN_KEY via microtask
// Invariants: totals(), anbamo_v10_4_6_mvp_stabilization key, statusClassV473 — untouched
(function(){
'use strict';
var V='v10.4.21b Fix MultiProject';
var CURR_PROJ_KEY='anbamo_current_project_id_v10_4_7_2';
var MAIN_KEY='anbamo_v10_4_6_mvp_stabilization'; // FROZEN — DO NOT RENAME

function myUpsert1421b(){
  var api=window.__v10472;
  if(api&&typeof api.upsertCurrentProject==='function')api.upsertCurrentProject();
}
function mySay1421b(msg,k){if(typeof toast==='function')toast(msg,k);}

/* ====================================================
   FIX 1: openModal wrapper
   ====================================================
   Root cause: v10.4.7.2 IIFE declares openProjectsModal as a LOCAL function.
   Its 'openProjects' click handler calls this LOCAL reference via closure —
   NOT window.openProjectsModal. v10.4.21's assignment openProjectsModal=openProjects1421
   only updates window.openProjectsModal, leaving the closure reference unchanged.
   The capture listener also calls stopImmediatePropagation() so later listeners can't fix it.

   Solution: wrap the GLOBAL openModal. ALL paths (including v10.4.7.2's local
   openProjectsModal) eventually call openModal('Проекты', html). Intercept there and
   route to openProjects1421(). Re-entrancy flag prevents infinite loop when
   openProjects1421() itself calls openModal().
   ==================================================== */
var _inProj1421b=false;
var _origOM1421b=openModal;
window.openModal=function(title,html){
  if(title==='Проекты'&&!_inProj1421b){
    _inProj1421b=true;
    try{if(typeof openProjects1421==='function')openProjects1421();}
    finally{_inProj1421b=false;}
    return;
  }
  _origOM1421b.apply(this,arguments);
};

/* ====================================================
   FIX 2: clearProjectDraftKeepSettings wrapper
   ====================================================
   Root cause (scope bug): v10.4.21's action hub calls LOCAL newProject1421() from
   v10.4.21's own IIFE closure — NOT window.newProject1421. So replacing
   window.newProject1421 doesn't help; the local reference is unaffected.

   Root cause (persistence bug): clearProjectDraftKeepSettings() creates fresh state
   (new projectId) and sets CURR_PROJ_KEY, but does NOT write new state to MAIN_KEY.
   On reload: MAIN_KEY has old projectId → currentProjectId() returns old ID →
   overwrites CURR_PROJ_KEY back to old ID → new project appears lost.

   Solution: wrap clearProjectDraftKeepSettings in window.__v10472 (the API object that
   v10.4.21's LOCAL newProject1421 calls as: api=window.__v10472; api.clearProjectDraftKeepSettings()).
   Use Promise.resolve().then() to persist MAIN_KEY AFTER the caller sets
   state.project.client=name and calls myUpsert(). At that point state has the complete
   new project data (new projectId + name) — safe to persist.
   ==================================================== */
var _api1421b=window.__v10472;
if(_api1421b&&typeof _api1421b.clearProjectDraftKeepSettings==='function'){
  var _origClear1421b=_api1421b.clearProjectDraftKeepSettings;
  _api1421b.clearProjectDraftKeepSettings=function(){
    var result=_origClear1421b.apply(this,arguments);
    Promise.resolve().then(function(){
      if(typeof state!=='undefined'){
        try{localStorage.setItem(MAIN_KEY,JSON.stringify(state));}catch(_e){}
        if(state.projectId)localStorage.setItem(CURR_PROJ_KEY,state.projectId);
      }
    });
    return result;
  };
}

/* ---- Fixed newProject for external/direct callers (not from UI button) ---- */
function newProject1421b(){
  if(typeof closeModal==='function')closeModal();
  var name=prompt('Название нового проекта','Новый проект');
  if(!name)return;
  name=name.trim()||'Новый проект';

  // Save current to register AND MAIN_KEY
  myUpsert1421b();
  if(typeof state!=='undefined'){
    try{localStorage.setItem(MAIN_KEY,JSON.stringify(state));}catch(_e){}
  }

  // Create fresh state (wrapped version also queues microtask — belt+suspenders)
  var api=window.__v10472;
  if(api&&typeof api.clearProjectDraftKeepSettings==='function'){
    api.clearProjectDraftKeepSettings();
  }

  // Apply name and status
  if(typeof state!=='undefined'){
    if(!state.project)state.project={};
    state.project.client=name;
    if(!state.project.status)state.project.status='Новая заявка';
  }

  // Ensure CURR_PROJ_KEY matches new state
  if(typeof state!=='undefined'&&state.projectId){
    localStorage.setItem(CURR_PROJ_KEY,state.projectId);
  }

  // Persist new state to MAIN_KEY immediately (synchronous, includes name)
  if(typeof state!=='undefined'){
    try{localStorage.setItem(MAIN_KEY,JSON.stringify(state));}catch(_e){}
  }

  // Save new project stub to register
  myUpsert1421b();

  mySay1421b('Новый проект \xab'+name+'\xbb создан');
  if(typeof renderCurrent==='function')renderCurrent();
}
window.newProject1421=newProject1421b;
window.newProject1421b=newProject1421b;

window.__v1421b={V:V,newProject1421b:newProject1421b,built:'2026-06-20'};
console.info('[v10.4.21b] Fix layer loaded — openModal wrapped, clearProjectDraftKeepSettings wrapped');
})();
</script>
"""

result = src.replace("</body>", LAYER + "\n</body>", 1)

# Gate assertions
assert "_inProj1421b"            in result, "ASSERT: re-entrancy flag missing"
assert "_origOM1421b"            in result, "ASSERT: openModal wrapper missing"
assert "_origClear1421b"         in result, "ASSERT: clearProjectDraftKeepSettings wrapper missing"
assert "Promise.resolve"         in result, "ASSERT: microtask persist missing"
assert "newProject1421b"         in result, "ASSERT: newProject1421b missing"
assert "__v1421b"                in result, "ASSERT: v10.4.21b marker missing"
assert result.count("</body>") == 1,       "ASSERT: multiple </body>"

with open(OUT, "w", encoding="utf-8") as f:
    f.write(result)

sl, ol = src.count("\n"), result.count("\n")
print(f"OK  {os.path.basename(OUT)}")
print(f"    {sl} -> {ol} lines  (+{ol-sl})")
print(f"    {len(src):,} -> {len(result):,} chars  (+{len(result)-len(src):,})")
