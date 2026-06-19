#!/usr/bin/env python3
"""Build v10.4.21 — Block 3: Projects + Safety
- Enhanced projects modal (rename, delete, duplicate, new with name)
- Backup ALL projects → single JSON; Restore with replace/add choice
- Last backup age indicator
- Bulletproof 'Версии/слепки' card removal: c.remove() not style.display
"""

import os

BASE = r"C:\Users\Win\OneDrive\Документы\New project 4\Фасадный калькулятор\revival"
SRC  = os.path.join(BASE, "AN_BAMO_Command_Center_v10_4_20_Header_ZF.html")
OUT  = os.path.join(BASE, "AN_BAMO_Command_Center_v10_4_21_Projects_Safety.html")

with open(SRC, encoding="utf-8") as f:
    src = f.read()

assert "</body>"       in src,       "ASSERT: no </body>"
assert "openProjectsModal" in src,   "ASSERT: no openProjectsModal"
assert "PROJECT_REGISTER_KEY" in src,"ASSERT: no PROJECT_REGISTER_KEY"
assert "v10.4.20"      in src or "v1420" in src.lower(), "ASSERT: base not v10.4.20"

LAYER = r"""
<style>
/* ====================================================
   v10.4.21 Block 3 — Projects + Safety
   ==================================================== */
.v1421-prj-card {
  border: 1px solid var(--brd, var(--line, #e5e7eb));
  border-radius: 12px; padding: 12px; margin-bottom: 10px;
}
.v1421-prj-card.cur {
  border-color: var(--primary, #2563eb);
  background: rgba(37,99,235,0.06);
}
.v1421-prj-actions { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
.v1421-prj-actions .btn { padding: 4px 10px; font-size: 12px; }
.v1421-prj-title { font-weight: 600; font-size: 15px; }
.v1421-prj-meta { font-size: 12px; opacity: .65; margin: 3px 0 6px; }
</style>

<script>
// v10.4.21 Block 3 — Projects + Safety
// Wrap-don't-rewrite. Cross-block helpers -> window.
// Invariants: totals(), anbamo_v10_4_6_mvp_stabilization key, statusClassV473 — untouched.
(function(){
'use strict';
var V='v10.4.21 Block3 ProjectsSafety';

// Known localStorage key strings — no variable references needed
var PROJ_REG_KEY  ='anbamo_project_register_v10_4_7_2';
var CURR_PROJ_KEY ='anbamo_current_project_id_v10_4_7_2';
var MAIN_KEY      ='anbamo_v10_4_6_mvp_stabilization'; // FROZEN — DO NOT RENAME
var BK_META_KEY   ='anbamo_last_backup_v1421';

/* ---- Local helpers (no scope-chain dependencies) ---- */
function myLoadReg(){try{return JSON.parse(localStorage.getItem(PROJ_REG_KEY)||'[]');}catch(e){return[];}}
function mySaveReg(list){localStorage.setItem(PROJ_REG_KEY,JSON.stringify(list||[]));}
function myCurId(){return localStorage.getItem(CURR_PROJ_KEY)||'';}
function myH(v){return String(v==null?'':v).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function myD(v){try{return new Date(v).toLocaleString('ru-RU',{day:'2-digit',month:'2-digit',year:'2-digit',hour:'2-digit',minute:'2-digit'});}catch(e){return String(v||'—');}}
function dl1421(fname,text){
  var blob=new Blob([text],{type:'application/json'});
  var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=fname;
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  setTimeout(function(){URL.revokeObjectURL(a.href);},1000);
}
function myUpsert(){
  var api=window.__v10472;
  if(api&&typeof api.upsertCurrentProject==='function')api.upsertCurrentProject();
}
function mySay(msg,kind){if(typeof toast==='function')toast(msg,kind);}

/* ---- Enhanced projects modal ---- */
function openProjects1421(){
  myUpsert();
  var reg=myLoadReg();
  var curId=myCurId();

  // Backup age banner
  var bkTs=localStorage.getItem(BK_META_KEY);
  var bkBanner;
  if(bkTs){
    var days=Math.floor((Date.now()-parseInt(bkTs,10))/86400000);
    var label=days===0?'сегодня':days===1?'вчера':days+' дн. назад';
    var warn=days>7;
    bkBanner='<div class="notice '+(warn?'warn':'ok')+'" style="margin-bottom:12px">'
      +'Последний бэкап: <b>'+myH(label)+'</b>'+(warn?' ⚠️ Давно — сделайте бэкап':'')+'</div>';
  }else{
    bkBanner='<div class="notice warn" style="margin-bottom:12px">⚠️ Бэкап не делался. Скачайте перед началом работы.</div>';
  }

  // Project cards
  var cardsHtml=reg.length?reg.map(function(p){
    var isActive=p.projectId===curId;
    var total=p.total?Math.round(p.total)+' €':'—';
    var dt=myD(p.updatedAt||p.createdAt||'');
    var extra=p.clientName&&p.clientName!==p.title?'<div style="font-size:12px;opacity:.6">'+myH(p.clientName)+'</div>':'';
    return '<div class="v1421-prj-card'+(isActive?' cur':'')+'">'
      +'<div style="display:flex;justify-content:space-between;gap:8px;align-items:flex-start">'
        +'<div class="v1421-prj-title">'+myH(p.title||'Без названия')+extra+'</div>'
        +'<span class="chip" style="font-size:11px;white-space:nowrap">'+myH(p.status||'—')+'</span>'
      +'</div>'
      +'<div class="v1421-prj-meta">'+myH(total)+' · '+myH(dt)+(p.phone?' · '+myH(p.phone):'')+'</div>'
      +'<div class="v1421-prj-actions">'
        +(isActive
          ?'<button class="btn" disabled>Открыт</button>'
          :'<button class="btn primary" data-action="projectOpen" data-id="'+myH(p.projectId)+'">Открыть</button>')
        +'<button class="btn" data-action="v1421-rename" data-id="'+myH(p.projectId)+'">Переименовать</button>'
        +'<button class="btn" data-action="v1421-dup" data-id="'+myH(p.projectId)+'">Копия</button>'
        +(isActive?'':'<button class="btn red" style="padding:4px 10px;font-size:12px" data-action="v1421-del" data-id="'+myH(p.projectId)+'">Удалить</button>')
      +'</div>'
    +'</div>';
  }).join(''):'<div class="notice">Проектов нет. Создайте первый.</div>';

  var html='<div style="padding:4px 0">'
    +bkBanner
    +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px">'
      +'<button class="btn primary" data-action="v1421-backup">⬇ Бэкап всех проектов</button>'
      +'<button class="btn" data-action="v1421-restore">⬆ Восстановить из файла</button>'
    +'</div>'
    +'<div class="section-title">Проекты ('+reg.length+')</div>'
    +cardsHtml
    +'<div style="margin-top:12px">'
      +'<button class="btn primary" style="width:100%" data-action="v1421-new">+ Новый проект</button>'
    +'</div>'
  +'</div>';

  if(typeof openModal==='function')openModal('Проекты',html);
}
window.openProjects1421=openProjects1421;

// Replace global openProjectsModal → all existing callers (v10.4.7.2 "openProjects" action,
// v10.4.17 "v1417-projects" bubble handler) now get the enhanced version.
openProjectsModal=openProjects1421;

/* ---- Rename ---- */
function renameProject1421(id){
  var reg=myLoadReg();
  var p=reg.find(function(x){return x.projectId===id;});
  var curName=p?p.title||'':'';
  var name=prompt('Название проекта',curName);
  if(!name)return;
  name=name.trim();
  if(!name)return;
  var curId=myCurId();
  if(id===curId){
    // Update live state
    if(typeof state!=='undefined'&&state.project)state.project.client=name;
    myUpsert();
  }else{
    // Update register entry only
    mySaveReg(reg.map(function(x){
      if(x.projectId!==id)return x;
      var r=Object.assign({},x,{title:name,clientName:name});
      if(r.currentSnapshot&&r.currentSnapshot.project)r.currentSnapshot.project.client=name;
      return r;
    }));
  }
  mySay('Переименовано');
  openProjects1421();
}
window.renameProject1421=renameProject1421;

/* ---- Delete ---- */
function deleteProject1421(id){
  var curId=myCurId();
  if(id===curId){mySay('Нельзя удалить открытый проект','bad');return;}
  var reg=myLoadReg();
  var p=reg.find(function(x){return x.projectId===id;});
  if(!p)return;
  if(!confirm('Удалить «'+(p.title||'Без названия')+'»?\nОтменить нельзя.'))return;
  mySaveReg(reg.filter(function(x){return x.projectId!==id;}));
  mySay('Проект удалён');
  openProjects1421();
}
window.deleteProject1421=deleteProject1421;

/* ---- Duplicate ---- */
function dupProject1421(id){
  var curId=myCurId();
  // Make sure current project is saved first
  myUpsert();
  var reg=myLoadReg();
  var p=reg.find(function(x){return x.projectId===id;});
  // Prefer in-memory state for current project (freshest data)
  var snap;
  if(id===curId&&typeof state!=='undefined'){
    snap=JSON.parse(JSON.stringify(state));
  }else if(p&&p.currentSnapshot){
    snap=JSON.parse(JSON.stringify(p.currentSnapshot));
  }else{
    mySay('Данные проекта не найдены','bad');return;
  }
  var newId='prj_'+Date.now().toString(36)+'_'+Math.random().toString(36).slice(2,5);
  snap.projectId=newId;
  var origName=snap.project&&snap.project.client||'Проект';
  if(snap.project)snap.project.client=origName+' (копия)';
  snap.createdAt=new Date().toISOString();
  snap.updatedAt=snap.createdAt;
  var entry={
    projectId:newId,
    title:origName+' (копия)',
    clientName:origName+' (копия)',
    phone:snap.project&&snap.project.phone||'',
    address:snap.project&&snap.project.address||'',
    status:snap.project&&snap.project.status||'Новая заявка',
    createdAt:snap.createdAt,
    updatedAt:snap.updatedAt,
    total:p&&p.total||0,
    currentSnapshot:snap
  };
  reg.unshift(entry);
  mySaveReg(reg);
  mySay('Продублировано');
  openProjects1421();
}
window.dupProject1421=dupProject1421;

/* ---- New project with name prompt ---- */
function newProject1421(){
  if(typeof closeModal==='function')closeModal();
  var name=prompt('Название нового проекта','Новый проект');
  if(!name)return;
  name=name.trim()||'Новый проект';
  // Save current first
  myUpsert();
  // Clear to fresh draft keeping settings/catalogs
  var api=window.__v10472;
  if(api&&typeof api.clearProjectDraftKeepSettings==='function'){
    api.clearProjectDraftKeepSettings();
  }
  // Set the name on fresh state
  if(typeof state!=='undefined'){
    if(!state.project)state.project={};
    state.project.client=name;
  }
  myUpsert();
  mySay('Новый проект «'+name+'» создан');
  if(typeof renderCurrent==='function')renderCurrent();
}
window.newProject1421=newProject1421;

/* ---- Backup ALL projects ---- */
function backupAll1421(){
  myUpsert();
  var reg=myLoadReg();
  var d=new Date();
  var ds=d.getFullYear()+'-'+(d.getMonth()+1).toString().padStart(2,'0')+'-'+d.getDate().toString().padStart(2,'0');
  var bk={
    version:'v10.4.21-backup',
    exportedAt:d.toISOString(),
    projectCount:reg.length,
    currentProjectId:myCurId(),
    projectRegister:reg
  };
  dl1421('AN_BAMO_backup_'+ds+'_'+reg.length+'proj.json',JSON.stringify(bk,null,2));
  localStorage.setItem(BK_META_KEY,Date.now().toString());
  mySay('Бэкап '+reg.length+' проектов скачан');
  openProjects1421();
}
window.backupAll1421=backupAll1421;

/* ---- Restore from backup ---- */
function restoreBackup1421(){
  var inp=document.createElement('input');
  inp.type='file';inp.accept='.json,application/json';inp.style.display='none';
  document.body.appendChild(inp);
  inp.onchange=function(){
    var file=inp.files&&inp.files[0];
    if(inp.parentNode)inp.parentNode.removeChild(inp);
    if(!file)return;
    var reader=new FileReader();
    reader.onload=function(){
      try{
        var data=JSON.parse(reader.result);
        // Support v10.4.21-backup format and older exportProject format
        var reg=data.projectRegister;
        if(!Array.isArray(reg)||!reg.length){mySay('Нет данных проектов в файле','bad');return;}
        var n=reg.length;
        var expAt=data.exportedAt?myD(data.exportedAt):'неизвестно';
        var choice=prompt(
          'Бэкап от '+expAt+'\n'+n+' проектов.\n\n'+
          'Введите:\n'+
          '  «заменить» — заменить весь реестр (полное восстановление)\n'+
          '  «добавить» — добавить только новые проекты к текущим\n\n'+
          'Пустое поле / Отмена — не восстанавливать',
          'заменить'
        );
        if(!choice)return;
        choice=choice.trim().toLowerCase();
        if(choice==='заменить'){
          mySaveReg(reg);
          // Restore main state for current project from backup
          var bkCurId=data.currentProjectId;
          var bkCur=bkCurId&&reg.find(function(x){return x.projectId===bkCurId;});
          if(bkCur&&bkCur.currentSnapshot){
            localStorage.setItem(MAIN_KEY,JSON.stringify(bkCur.currentSnapshot));
            localStorage.setItem(CURR_PROJ_KEY,bkCurId);
          }
          localStorage.setItem(BK_META_KEY,Date.now().toString());
          mySay('Восстановлено '+n+' проектов — перезагрузка...');
          setTimeout(function(){window.location.reload();},1500);
        }else if(choice==='добавить'){
          var existing=myLoadReg();
          var ids={};existing.forEach(function(x){ids[x.projectId]=true;});
          var added=reg.filter(function(x){return !ids[x.projectId];});
          mySaveReg(existing.concat(added));
          localStorage.setItem(BK_META_KEY,Date.now().toString());
          mySay('Добавлено '+added.length+' проектов');
          openProjects1421();
        }else{
          mySay('Введите «заменить» или «добавить»','bad');
        }
      }catch(err){
        mySay('Ошибка чтения файла: '+(err.message||String(err)),'bad');
      }
    };
    reader.readAsText(file);
  };
  inp.click();
}
window.restoreBackup1421=restoreBackup1421;

/* ---- Bulletproof card removal: c.remove() not style.display ---- */
// Wraps the v10.4.20 wrapper which wraps the v10.4.14B wrapper which wraps original.
// On every renderRequest() call the card is physically removed from DOM.
var _rr21=typeof renderRequest==='function'?renderRequest:null;
if(_rr21){
  window.renderRequest=renderRequest=function(){
    _rr21.apply(this,arguments);
    var pane=document.getElementById('pane-request');
    if(!pane)return;
    pane.querySelectorAll('.card').forEach(function(c){
      var t=c.querySelector('.title,.card-title');
      if(t&&/Версии|слепк/i.test(t.textContent))c.remove();
    });
  };
}

/* ---- Action hub (capture phase) ---- */
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-action]');if(!b)return;
  var a=b.dataset.action, id=b.dataset.id;
  if(a==='v1421-rename'){e.preventDefault();e.stopImmediatePropagation();renameProject1421(id);return;}
  if(a==='v1421-del')   {e.preventDefault();e.stopImmediatePropagation();deleteProject1421(id);return;}
  if(a==='v1421-dup')   {e.preventDefault();e.stopImmediatePropagation();dupProject1421(id);return;}
  if(a==='v1421-new')   {e.preventDefault();e.stopImmediatePropagation();newProject1421();return;}
  if(a==='v1421-backup'){e.preventDefault();e.stopImmediatePropagation();backupAll1421();return;}
  if(a==='v1421-restore'){e.preventDefault();e.stopImmediatePropagation();restoreBackup1421();return;}
},true);

/* ---- Immediate card removal on load (for current active pane) ---- */
try{
  var _p=document.getElementById('pane-request');
  if(_p)_p.querySelectorAll('.card').forEach(function(c){
    var t=c.querySelector('.title,.card-title');
    if(t&&/Версии|слепк/i.test(t.textContent))c.remove();
  });
}catch(_e){}

window.__v1421={V:V,openProjects1421:openProjects1421,backupAll1421:backupAll1421,restoreBackup1421:restoreBackup1421,built:'2026-06-19'};
})();
</script>
"""

result = src.replace("</body>", LAYER + "\n</body>", 1)

# Gate assertions
assert "v1421-backup"        in result, "ASSERT: v1421-backup missing"
assert "v1421-restore"       in result, "ASSERT: v1421-restore missing"
assert "v1421-rename"        in result, "ASSERT: v1421-rename missing"
assert "v1421-del"           in result, "ASSERT: v1421-del missing"
assert "v1421-new"           in result, "ASSERT: v1421-new missing"
assert "openProjects1421"    in result, "ASSERT: openProjects1421 missing"
assert "backupAll1421"       in result, "ASSERT: backupAll1421 missing"
assert "restoreBackup1421"   in result, "ASSERT: restoreBackup1421 missing"
assert "c.remove()"          in result, "ASSERT: c.remove() missing"
assert "openProjectsModal=openProjects1421" in result, "ASSERT: modal replacement missing"
assert "anbamo_v10_4_6_mvp_stabilization" in result, "ASSERT: main key reference missing"
assert "BK_META_KEY"         in result, "ASSERT: BK_META_KEY missing"
assert result.count("</body>") == 1, "ASSERT: multiple </body>"

with open(OUT, "w", encoding="utf-8") as f:
    f.write(result)

sl, ol = src.count("\n"), result.count("\n")
print(f"OK  {os.path.basename(OUT)}")
print(f"    {sl} -> {ol} lines  (+{ol-sl})")
print(f"    {len(src):,} -> {len(result):,} chars  (+{len(result)-len(src):,})")
