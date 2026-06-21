#!/usr/bin/env python3
# build_v1423.py — ФАЗА 1: Core Engine Fast
# Base:   AN_BAMO_Command_Center_v10_4_22_WorkView_Price.html
# Output: AN_BAMO_Command_Center_v10_4_23_Core_Engine_Fast.html

import re, os, sys

BASE  = 'AN_BAMO_Command_Center_v10_4_22_WorkView_Price.html'
OUT   = 'AN_BAMO_Command_Center_v10_4_23_Core_Engine_Fast.html'
DIR   = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────────────────
# LAYER  — injected before </body>
# ─────────────────────────────────────────────────────────────────────
LAYER = r"""
<style>
/* ── v10.4.23 Core Engine ── */
.v1423-view { max-width:800px; margin:0 auto; }
.v1423-hdr  { display:flex; align-items:center; justify-content:space-between;
              background:var(--card-bg,var(--surface)); border-radius:12px;
              padding:14px 18px; margin-bottom:10px; gap:12px; }
.v1423-hdr-left { flex:1; min-width:0; }
.v1423-hdr-name { font-size:16px; font-weight:700; color:var(--txt,var(--ink)); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.v1423-hdr-sub  { font-size:12px; color:var(--muted,var(--ink-muted)); margin-top:2px; }
.v1423-hdr-total{ text-align:right; white-space:nowrap; }
.v1423-hdr-total b { font-size:22px; font-weight:800; color:var(--txt,var(--ink)); }
.v1423-hdr-total small { display:block; font-size:11px; color:var(--muted,var(--ink-muted)); }
.v1423-acc  { background:var(--card-bg,var(--surface)); border-radius:12px;
              margin-bottom:8px; overflow:hidden; }
.v1423-acc-head { width:100%; display:flex; align-items:center; justify-content:space-between;
                  padding:14px 18px; border:none; background:transparent; cursor:pointer;
                  text-align:left; gap:10px; }
.v1423-acc-head:hover { background:var(--hover-bg,rgba(0,0,0,.04)); }
.v1423-acc-num  { display:inline-flex; align-items:center; justify-content:center;
                  width:22px; height:22px; border-radius:50%; background:var(--primary,#2563eb);
                  color:#fff; font-size:11px; font-weight:700; flex-shrink:0; }
.v1423-acc-title{ font-weight:650; font-size:14px; color:var(--txt,var(--ink)); flex:1; }
.v1423-acc-sum  { font-size:12px; color:var(--muted,var(--ink-muted)); white-space:nowrap; }
.v1423-chev     { color:var(--muted,var(--ink-muted)); font-size:14px; transition:transform .2s; flex-shrink:0; }
.v1423-acc.open .v1423-chev { transform:rotate(180deg); }
.v1423-acc-body { display:none; padding:0 18px 16px; }
.v1423-acc.open .v1423-acc-body { display:block; }
.v1423-row  { display:flex; align-items:center; gap:8px; padding:8px 0;
              border-bottom:1px solid var(--divider,rgba(0,0,0,.06)); }
.v1423-row:last-child { border-bottom:none; }
.v1423-row-name { flex:1; font-size:13px; color:var(--txt,var(--ink)); }
.v1423-row-sub  { font-size:11px; color:var(--muted,var(--ink-muted)); }
.v1423-row-price{ font-size:13px; font-weight:600; color:var(--txt,var(--ink)); white-space:nowrap; }
.v1423-row-empty{ font-size:12px; color:var(--muted,var(--ink-muted)); padding:8px 0; }
.v1423-stepper  { display:flex; align-items:center; gap:4px; }
.v1423-stepper button { width:28px; height:28px; border-radius:8px; border:1px solid var(--divider,rgba(0,0,0,.12));
                         background:var(--card-bg,var(--surface)); color:var(--txt,var(--ink));
                         font-size:16px; font-weight:700; cursor:pointer; display:flex; align-items:center; justify-content:center; }
.v1423-stepper .v1423-qty { min-width:32px; text-align:center; font-size:13px; font-weight:600; }
.v1423-auto-badge { font-size:10px; color:var(--primary,#2563eb); background:var(--primary-bg,rgba(37,99,235,.1));
                     padding:2px 6px; border-radius:4px; white-space:nowrap; }
.v1423-toggle { display:inline-flex; align-items:center; gap:4px;
                padding:4px 10px; border-radius:8px; border:1px solid var(--divider,rgba(0,0,0,.12));
                background:var(--card-bg,var(--surface)); font-size:11px; font-weight:600;
                cursor:pointer; color:var(--muted,var(--ink-muted)); }
.v1423-toggle.on { background:var(--primary,#2563eb); border-color:var(--primary,#2563eb); color:#fff; }
.v1423-toggle.rec { background:var(--amber-bg,rgba(245,158,11,.12)); border-color:rgba(245,158,11,.4);
                     color:var(--amber,#d97706); }
.v1423-catalog-card { display:flex; align-items:center; justify-content:space-between; gap:8px;
                       padding:10px 12px; border-radius:10px; border:1px solid var(--divider,rgba(0,0,0,.08));
                       background:var(--card-bg,var(--surface)); margin-bottom:6px; cursor:pointer; }
.v1423-catalog-card.sel { border-color:var(--primary,#2563eb); background:var(--primary-bg,rgba(37,99,235,.06)); }
.v1423-card-name { font-size:13px; font-weight:600; color:var(--txt,var(--ink)); }
.v1423-card-sup  { font-size:11px; color:var(--muted,var(--ink-muted)); }
.v1423-card-price{ font-size:12px; font-weight:600; color:var(--primary,#2563eb); white-space:nowrap; }
.v1423-card-sel  { font-size:11px; padding:4px 10px; border-radius:6px; border:1px solid currentColor;
                    background:transparent; cursor:pointer; color:var(--primary,#2563eb); }
.v1423-ztabs    { display:flex; gap:4px; flex-wrap:wrap; margin-bottom:12px; }
.v1423-ztab     { padding:6px 12px; border-radius:8px; border:1px solid var(--divider,rgba(0,0,0,.12));
                   background:var(--card-bg,var(--surface)); font-size:12px; font-weight:600;
                   cursor:pointer; color:var(--muted,var(--ink-muted)); }
.v1423-ztab.active { background:var(--primary,#2563eb); border-color:var(--primary,#2563eb); color:#fff; }
.v1423-led-cfg  { display:flex; flex-wrap:wrap; gap:8px; margin-top:8px; }
.v1423-led-cfg .field { margin:0; }
.v1423-sep { border-top:1px solid var(--divider,rgba(0,0,0,.06)); margin:12px 0; }
.v1423-totline { display:flex; justify-content:space-between; padding:6px 0;
                  font-size:13px; color:var(--txt,var(--ink)); }
.v1423-totline.grand { font-weight:700; font-size:15px; border-top:2px solid var(--divider,rgba(0,0,0,.1)); margin-top:4px; padding-top:8px; }
.v1423-add-btn  { width:100%; margin-top:10px; padding:8px; border-radius:8px;
                   border:1px dashed var(--divider,rgba(0,0,0,.18)); background:transparent;
                   color:var(--primary,#2563eb); font-size:13px; cursor:pointer; }
.v1423-add-btn:hover { background:var(--primary-bg,rgba(37,99,235,.05)); }
.v1423-bom-row  { display:flex; justify-content:space-between; font-size:12px;
                   padding:5px 0; border-bottom:1px solid var(--divider,rgba(0,0,0,.04)); color:var(--muted,var(--ink-muted)); }
.v1423-bom-row b { color:var(--txt,var(--ink)); font-size:13px; }
.v1423-honest   { font-size:11px; color:var(--amber,#d97706); font-style:italic; }
</style>

<script>
(function(){
'use strict';
var V1423 = 'v10.4.23 Core Engine Fast';

// ── helpers ──────────────────────────────────────────────────────────
function n23(v){return typeof num==='function'?num(v):(Number(String(v==null?0:v).replace(',','.'))||0);}
function m23(v){return typeof money==='function'?money(v):(Math.round(n23(v))+' €');}
function e23(v){return String(v==null?'':v).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function uid23(p){return p+'_'+Date.now().toString(36)+Math.random().toString(36).slice(2,5);}
function pbGet(book,id){for(var i=0;i<book.length;i++){if(book[i].id===id)return book[i];}return null;}
function zones23(){return (typeof ensureV1043State==='function'?(ensureV1043State(),state.zones):state.zones)||[];}
function doors23(){return zones23().reduce(function(a,z){return a+n23(z.doors);},0);}
function drawers23(){return zones23().reduce(function(a,z){return a+n23(z.drawers);},0);}
function hinges23(){return zones23().reduce(function(a,z){return a+n23(z.doors)*(n23(z.height)>1600?4:n23(z.height)>900?3:2);},0);}
function area23(){return zones23().reduce(function(a,z){return a+Math.max(0,n23(z.len)*n23(z.height)/1000-n23(z.deduct));},0);}

// ── 1. priceBook builder ─────────────────────────────────────────────
function buildPriceBook1423(){
  if(typeof ensureV1414==='function')ensureV1414();
  if(typeof ensureV1043State==='function')ensureV1043State();
  var book=[];
  function add(o){
    if(!book.some(function(x){return x.id===o.id;}))
      book.push({id:o.id,name:o.name||'',client_name:o.client_name||o.name||'',
        category:o.category||'option',unit:o.unit||'шт',
        price:n23(o.price),cost:n23(o.cost),
        supplier:o.supplier||'',art:o.art||'',fits:o.fits||'',hint:o.hint||''});
  }

  // (a) 106-item facade catalog (base)
  var cpi=Array.isArray(state.customPriceItems)?state.customPriceItems:[];
  cpi.filter(function(x){return (x.cat||x.category)==='facade';}).forEach(function(x){
    add({id:x.id||('cat_'+x.name.replace(/\s+/g,'_').slice(0,20)),
      name:x.name||x.clientName||'',client_name:x.clientName||x.name||'',
      category:'facade',unit:x.unit||'м²',price:n23(x.price),cost:n23(x.cost),
      supplier:x.supplier||'',art:x.art||'',fits:x.fits||'',hint:x.hint||''});
  });

  // (b) Legacy facade variants (state.materials) — needed for integrity
  (state.materials||[]).forEach(function(m){
    add({id:'fv_'+m.id,name:m.tech||m.client||m.id,client_name:m.client||m.id,
      category:'facade',unit:'м²',price:n23(m.price),cost:n23(m.cost),
      supplier:'',art:'',fits:'',hint:m.desc||''});
  });

  // (c) Counter materials (topMaterials)
  Object.keys(state.topMaterials||{}).forEach(function(id){
    var m=state.topMaterials[id];
    add({id:'ctr_'+id,name:m.name||m.client||id,client_name:m.client||m.name||id,
      category:'counter',unit:'м.п.',price:n23(m.price),cost:n23(m.cost),
      supplier:'',art:'',fits:JSON.stringify({blank:m.blank,under:!!m.under}),hint:''});
  });

  // (d) Labor rates (formerly hardcoded) — now in priceBook, editable
  [{id:'labor_facade',name:'Работа с фасадами',unit:'м²',price:42,cost:18},
   {id:'labor_door',  name:'Работа за дверь',  unit:'шт',price:4, cost:0 },
   {id:'cut_sink',    name:'Вырез под мойку',   unit:'шт',price:35,cost:12},
   {id:'cut_hob',     name:'Вырез под плиту',   unit:'шт',price:25,cost:8 },
   {id:'ctr_stitch',  name:'Стык столешницы',   unit:'шт',price:60,cost:25},
   {id:'ctr_under',   name:'Доплата подстольная',unit:'шт',price:45,cost:18}
  ].forEach(function(o){add({category:'labor',supplier:'',art:'',fits:'',hint:'',client_name:o.name,
    id:o.id,name:o.name,unit:o.unit,price:o.price,cost:o.cost});});

  // (e) Hardware catalog
  Object.keys(state.hardwareCatalog||{}).forEach(function(id){
    var m=state.hardwareCatalog[id];
    add({id:'hw_'+id,name:m.client||m.tech||id,client_name:m.client||id,
      category:'hardware',unit:m.unit||'шт',price:n23(m.price),cost:n23(m.cost),
      supplier:'',art:'',fits:'',hint:''});
  });

  // (f) Services catalog
  Object.keys(state.servicesCatalog||{}).forEach(function(id){
    var m=state.servicesCatalog[id];
    add({id:'svc_'+id,name:m.client||id,client_name:m.client||id,
      category:'service',unit:m.unit||'усл.',price:n23(m.price),cost:n23(m.cost),
      supplier:'',art:'',fits:'',hint:''});
  });

  // (g) LED catalog
  Object.keys(state.ledCatalog||{}).forEach(function(id){
    var m=state.ledCatalog[id];
    add({id:'led_'+id,name:m.client||id,client_name:m.client||id,
      category:'option',unit:m.unit||'м',price:n23(m.price),cost:n23(m.cost),
      supplier:'',art:'',fits:'',hint:''});
  });

  // (h) Extra works catalog
  Object.keys(state.extraWorksCatalog||{}).forEach(function(id){
    var m=state.extraWorksCatalog[id];
    add({id:'ew_'+id,name:m.client||id,client_name:m.client||id,
      category:'service',unit:m.unit||'усл.',price:n23(m.price),cost:n23(m.cost),
      supplier:'',art:'',fits:'',hint:''});
  });

  // (i) Improvements / options
  (state.improvements||[]).forEach(function(i){
    add({id:'opt_'+i.id,name:i.title||i.id,client_name:i.client||i.title||i.id,
      category:'option',unit:i.unit||'шт',price:n23(i.price),cost:n23(i.cost),
      supplier:'',art:'',fits:JSON.stringify({unit:i.unit}),hint:i.desc||''});
  });

  // (j) Edge / lacquer from productionSettings
  var ps=state.productionSettings||{};
  if(ps.laserEdgingPrice!==undefined)
    add({id:'edge_laser',name:'Лазерная кромка',client_name:'Лазерная кромка',
      category:'option',unit:'пог.м',price:n23(ps.laserEdgingPrice),cost:n23(ps.laserEdgingCost),
      supplier:'',art:'',fits:'',hint:''});
  if(ps.extraLacquerPrice!==undefined)
    add({id:'opt_extraLacquer',name:'Доп. лак MDF',client_name:'Доп. лак MDF',
      category:'option',unit:'м²',price:n23(ps.extraLacquerPrice),cost:n23(ps.extraLacquerCost),
      supplier:'',art:'',fits:JSON.stringify({unit:'mdfArea'}),hint:''});

  return book;
}

// ── 2. Order defaults ─────────────────────────────────────────────────
function defaultOrder1423(){
  return {facades:[],counter:[],materials:[],hardware:[],services:[],options:[]};
}

// ── 3. Migration (idempotent) ────────────────────────────────────────
function migrateToOrder1423(){
  if(!state)return;
  // Always (re)build priceBook so new catalog imports are picked up
  if(!Array.isArray(state.priceBook)||state.priceBook.length<5){
    state.priceBook=buildPriceBook1423();
  }
  if(state._v1423migV2)return;

  var book=state.priceBook;
  var order=defaultOrder1423();
  var wf=state.wf1422||{};
  var zz=zones23();

  // Facades: one entry per zone
  zz.forEach(function(z){
    var area=Math.max(0,n23(z.len)*n23(z.height)/1000-n23(z.deduct));
    var selName=wf['sel_'+z.id]||'';
    var pbItem=null;
    // Try catalog match by name
    if(selName){
      for(var i=0;i<book.length;i++){
        if(book[i].category==='facade'&&book[i].name===selName){pbItem=book[i];break;}
      }
    }
    // Fallback: match by active material price (legacy variant)
    if(!pbItem){
      var mat=typeof activeMaterial==='function'?activeMaterial():null;
      var matId=mat?('fv_'+mat.id):null;
      if(matId)pbItem=pbGet(book,matId);
      // If still nothing (shouldn't happen after buildPriceBook), add synthetic
      if(!pbItem&&mat){
        pbItem={id:'fv_'+mat.id,name:mat.tech||mat.client||mat.id,
          client_name:mat.client||mat.id,category:'facade',unit:'м²',
          price:n23(mat.price),cost:n23(mat.cost),
          supplier:'',art:'',fits:'',hint:''};
        book.push(pbItem);
      }
    }
    order.facades.push({
      id:uid23('f'),zoneId:z.id,zoneName:z.name,
      itemId:pbItem?pbItem.id:null,
      qty:area,doors:n23(z.doors),drawers:n23(z.drawers),
      included:true
    });
  });

  // Counter
  var top=state.top||{};
  if(top.enabled){
    var topMatId='ctr_'+(top.material||'ldsp38');
    var topMatObj=(state.topMaterials||{})[top.material||'ldsp38']||{};
    var blank=n23(topMatObj.blank)||4.1;
    var len=n23(top.len)||0;
    order.counter.push({
      id:uid23('ctr'),itemId:topMatId,
      shape:state.topShape1422||'straight',
      len:len,
      lenA:n23(state.topLenA1422)||len,
      lenB:n23(state.topLenB1422)||0,
      depth:n23(top.depth)||600,
      sinkCuts:n23(top.sinkCuts)||0,
      hobCuts:n23(top.hobCuts)||0,
      sinkType:top.sinkType||'surface',
      jointType:state.topCorner1422||'euro',
      needsStitch:len>blank,
      enabled:true
    });
  }

  // Hardware (auto-count, NOT included in total by default — matches old behaviour)
  var hw=state.hardware||{};
  var totalDoors=doors23(),totalDrawers=drawers23(),totalHinges=hinges23();
  order.hardware=[
    {id:uid23('hw'),itemId:'hw_hinges',   qtyAuto:totalHinges,  qtyOverride:null,included:false},
    {id:uid23('hw'),itemId:'hw_runners',  qtyAuto:totalDrawers, qtyOverride:null,included:false},
    {id:uid23('hw'),itemId:'hw_handles',  qtyAuto:hw.handlesMode==='client'?0:totalDoors+totalDrawers,
      qtyOverride:hw.handlesMode==='client'?n23(hw.handlesCount):null,
      mode:hw.handlesMode||'we',included:false}
  ];
  // Extra hardware — only named catalog items (not imp_* from 106-import)
  var knownHwIds=['softClose','liftGas','aventos','handleBar','handleProfile'];
  knownHwIds.forEach(function(id){
    if(state.hardwareCatalog&&state.hardwareCatalog[id])
      order.hardware.push({id:uid23('hw'),itemId:'hw_'+id,qtyAuto:0,qtyOverride:null,included:false});
  });

  // Services: only named EXTRA_DEFAULTS (skip imp_* from 106-import)
  var knownSvcIds=['delivery','carrying','installation','dismantleOld','plinth','cornice','legs','trimming','custom'];
  knownSvcIds.forEach(function(id){
    var item=(state.extraWorksCatalog||{})[id];
    if(item) order.services.push({id:uid23('svc'),itemId:'ew_'+id,enabled:!!item.v1422on,qty:n23(item.v1422qty)||1});
  });
  // Base servicesCatalog (only named: measure, dismantle, delivery)
  var knownBaseSvc=['measure','dismantle','delivery'];
  knownBaseSvc.forEach(function(id){
    if((state.servicesCatalog||{})[id]&&!order.services.some(function(s){return s.itemId==='svc_'+id;}))
      order.services.push({id:uid23('svc'),itemId:'svc_'+id,enabled:false,qty:1});
  });

  // Options/improvements
  (state.improvements||[]).forEach(function(i){
    var cfg={};
    if(i.id==='led')cfg.meters=n23(i.meters);
    order.options.push({
      id:uid23('opt'),itemId:'opt_'+i.id,
      enabled:!!(i.selected||i.status==='included'),
      recommend:i.mode==='recommend'||i.status==='recommend',
      config:cfg
    });
  });
  if(!order.options.some(function(o){return o.itemId==='opt_extraLacquer';}))
    order.options.push({id:uid23('opt'),itemId:'opt_extraLacquer',enabled:false,recommend:false,config:{}});

  state.order=order;
  state._v1423migV2=true;
  if(typeof markDirty==='function')markDirty();
}

// ── 4. Refresh hw auto counts ─────────────────────────────────────────
function refreshHwAuto1423(){
  if(!state.order)return;
  var td=doors23(),tdr=drawers23(),th=hinges23();
  var hw=state.hardware||{};
  state.order.hardware.forEach(function(h){
    if(h.itemId==='hw_hinges')  h.qtyAuto=th;
    if(h.itemId==='hw_runners') h.qtyAuto=tdr;
    if(h.itemId==='hw_handles') h.qtyAuto=hw.handlesMode==='client'?0:td+tdr;
  });
  // Sync zone data into facades
  var zz=zones23();
  state.order.facades.forEach(function(f){
    var z=zz.find(function(x){return x.id===f.zoneId;});
    if(z){
      f.qty=Math.max(0,n23(z.len)*n23(z.height)/1000-n23(z.deduct));
      f.doors=n23(z.doors);
      f.drawers=n23(z.drawers);
    }
  });
  // Sync counter
  var top=state.top||{};
  if(state.order.counter.length&&top.enabled){
    var c=state.order.counter[0];
    var len=n23(top.len);
    var topMatObj=(state.topMaterials||{})[top.material||'ldsp38']||{};
    var blank=n23(topMatObj.blank)||4.1;
    c.len=len;
    c.sinkCuts=n23(top.sinkCuts);
    c.hobCuts=n23(top.hobCuts);
    c.sinkType=top.sinkType||'surface';
    c.needsStitch=len>blank;
    if(state.topShape1422)c.shape=state.topShape1422;
    if(state.topLenA1422!=null)c.lenA=n23(state.topLenA1422);
    if(state.topLenB1422!=null)c.lenB=n23(state.topLenB1422);
    if(state.topCorner1422)c.jointType=state.topCorner1422;
  }
}

// ── 5. Order-based totals ─────────────────────────────────────────────
function orderTotals1423(){
  if(!state.order||!state.priceBook)return null;
  var book=state.priceBook,order=state.order;
  var sell=0,cost=0;
  var baseS=0,optS=0;

  // Facades
  order.facades.forEach(function(f){
    if(!f.included||f.qty<=0)return;
    var it=pbGet(book,f.itemId);
    var lf=pbGet(book,'labor_facade');
    var ld=pbGet(book,'labor_door');
    if(it){var s=f.qty*it.price;sell+=s;cost+=f.qty*it.cost;baseS+=s;}
    if(lf){var s2=f.qty*lf.price;sell+=s2;cost+=f.qty*lf.cost;baseS+=s2;}
    if(ld&&f.doors>0){var s3=f.doors*ld.price;sell+=s3;cost+=f.doors*ld.cost;baseS+=s3;}
  });

  // Counter
  order.counter.forEach(function(c){
    if(!c.enabled)return;
    var it=pbGet(book,c.itemId);
    var cs=pbGet(book,'cut_sink');
    var ch=pbGet(book,'cut_hob');
    var cst=pbGet(book,'ctr_stitch');
    var cun=pbGet(book,'ctr_under');
    var len=c.shape==='corner'?(n23(c.lenA)+n23(c.lenB)):n23(c.len);
    if(it&&len>0){var s=len*it.price;sell+=s;cost+=len*it.cost;baseS+=s;}
    if(cs&&n23(c.sinkCuts)>0){var s2=n23(c.sinkCuts)*cs.price;sell+=s2;cost+=n23(c.sinkCuts)*cs.cost;baseS+=s2;}
    if(ch&&n23(c.hobCuts)>0){var s3=n23(c.hobCuts)*ch.price;sell+=s3;cost+=n23(c.hobCuts)*ch.cost;baseS+=s3;}
    if(cst&&c.needsStitch){sell+=cst.price;cost+=cst.cost;baseS+=cst.price;}
    if(cun&&c.sinkType==='under'){
      var topMatObj=(state.topMaterials||{})[c.itemId.replace('ctr_','')]||{};
      if(topMatObj.under){sell+=cun.price;cost+=cun.cost;baseS+=cun.price;}
    }
  });

  // Hardware (only if included)
  order.hardware.forEach(function(h){
    if(!h.included)return;
    var it=pbGet(book,h.itemId);
    if(!it)return;
    var qty=h.qtyOverride!=null?n23(h.qtyOverride):n23(h.qtyAuto);
    if(qty>0&&it.price>0){sell+=qty*it.price;cost+=qty*it.cost;baseS+=qty*it.price;}
  });

  // Services
  order.services.forEach(function(s){
    if(!s.enabled)return;
    var it=pbGet(book,s.itemId);
    if(!it)return;
    var qty=n23(s.qty)||1;
    if(it.price>0){sell+=qty*it.price;cost+=qty*it.cost;baseS+=qty*it.price;}
  });

  // Options (enabled only)
  order.options.forEach(function(o){
    if(!o.enabled)return;
    var it=pbGet(book,o.itemId);
    if(!it)return;
    var qty=1;
    var fits={};try{fits=JSON.parse(it.fits||'{}');}catch(e){}
    if(fits.unit==='hinge')qty=hinges23();
    else if(fits.unit==='drawer')qty=drawers23();
    else if(fits.unit==='led')qty=n23((o.config||{}).meters)||0;
    else if(fits.unit==='mdfArea')qty=area23();
    // LED: no price if no meters
    if(fits.unit==='led'&&qty<=0)return;
    if(qty>0){var s=qty*it.price;sell+=s;cost+=qty*it.cost;optS+=s;}
  });

  var expenses=(state.expenses||[]).reduce(function(a,x){return a+n23(x.amount);},0);
  var paid=(state.payments||[]).reduce(function(a,x){return a+n23(x.amount);},0);
  var profit=sell-cost-expenses;
  var margin=sell>0?profit/sell*100:0;
  return {
    totalClient:sell,totalCost:cost+expenses,profit:profit,margin:margin,
    paid:paid,remaining:Math.max(0,sell-paid),
    base:{sell:baseS,cost:cost},improvements:{sell:optS,cost:0}
  };
}

// ── 6. Section renderers ──────────────────────────────────────────────
state.accOpen1423=state.accOpen1423||{};
state.wf1423=state.wf1423||{zone:'lower'};

function accOpen1423(id){return !!(state.accOpen1423&&state.accOpen1423[id]);}

function sec1423(num,id,title,summary,body){
  var open=accOpen1423(id);
  return '<div class="v1423-acc card'+(open?' open':'')+'" data-v1423acc="'+id+'">'
    +'<button class="v1423-acc-head" data-action="v1423-acc" data-id="'+id+'">'
    +'<span class="v1423-acc-num">'+e23(num)+'</span>'
    +'<span class="v1423-acc-title">'+e23(title)+'</span>'
    +'<span class="v1423-acc-sum">'+e23(summary)+'</span>'
    +'<span class="v1423-chev">▾</span>'
    +'</button>'
    +'<div class="v1423-acc-body">'+body+'</div>'
    +'</div>';
}

// Section 1: Паспорт
function buildPassport1423(){
  var p=state.project||{};
  var body='<div class="grid g2">'
    +'<div>'+inputF('Клиент','project.client',p.client||'','Иванов / кухня')+'</div>'
    +'<div>'+inputF('Телефон','project.phone',p.phone||'','+372...')+'</div>'
    +'<div>'+inputF('Адрес','project.address',p.address||'','Tallinn...')+'</div>'
    +'<div>'+selF('Статус','project.status',p.status||'Новая заявка',
      ['Новая заявка','ПредКП подготовлено','ПредКП отправлено','Замер назначен','Замер сделан',
       'Ожидаем аванс','Аванс получен','В производстве','Монтаж назначен','Установлено','Закрыт','Отказ'])+'</div>'
    +'<div>'+selF('Запрос','project.want',p.want||'Фасады + столешница',
      ['Только фасады','Фасады + столешница','Фасады + фурнитура','Полное обновление кухни'])+'</div>'
    +'</div>';
  var summ=(p.client||'не заполнен')+(p.status?' · '+p.status:'');
  return sec1423('1','passport','Паспорт',summ,body);
}

// Section 2: Фасады
function buildFacades1423(){
  var book=state.priceBook||[];
  var facadeCat=book.filter(function(x){return x.category==='facade';});
  var order=state.order||{};
  var facades=order.facades||[];
  var zz=zones23();
  var wf=state.wf1423;
  var activeZone=wf.zone||'lower';

  // Zone tabs
  var tabs='<div class="v1423-ztabs">'
    +zz.map(function(z){
      return '<button class="v1423-ztab'+(z.id===activeZone?' active':'')+'"'
        +' data-action="v1423-zone" data-zone="'+z.id+'">'+e23(z.name)+'</button>';
    }).join('')+'</div>';

  var zone=zz.find(function(z){return z.id===activeZone;})||zz[0];
  var zoneFacade=facades.find(function(f){return f.zoneId===(zone?zone.id:'lower');})||null;
  var selItemId=zoneFacade?zoneFacade.itemId:'';
  var area=zoneFacade?n23(zoneFacade.qty):0;

  // Size inputs
  var sizeHtml='';
  if(zone){
    sizeHtml='<div class="grid g2" style="margin-bottom:12px">'
      +'<div class="field"><label>Длина, м</label>'
      +'<input data-bind="zone:'+zone.id+'.len" value="'+e23(zone.len)+'" type="number" inputmode="decimal"></div>'
      +'<div class="field"><label>Высота, мм</label>'
      +'<input data-bind="zone:'+zone.id+'.height" value="'+e23(zone.height)+'" type="number" inputmode="decimal"></div>'
      +'</div>'
      +(typeof stepper==='function'
        ?('<div class="grid g2" style="margin-bottom:12px"><div>'+stepper('Двери','doors',zone.doors,zone.id)
          +'</div><div>'+stepper('Ящики','drawers',zone.drawers,zone.id)+'</div></div>'):'');
  }

  // Catalog cards
  var cards='<div class="v1423-seclbl" style="margin:12px 0 8px;font-size:12px;font-weight:600;color:var(--muted,var(--ink-muted))">Материал '+(zone?e23(zone.name):activeZone)+'</div>';
  if(facadeCat.length){
    cards+=facadeCat.map(function(it){
      var isSel=selItemId===it.id;
      return '<div class="v1423-catalog-card'+(isSel?' sel':'')+'"'
        +' data-action="v1423-facade" data-id="'+e23(it.id)+'" data-zone="'+e23(activeZone)+'">'
        +'<div><div class="v1423-card-name">'+e23(it.name)+'</div>'
        +'<div class="v1423-card-sup">'+e23(it.supplier)+'</div></div>'
        +'<div style="display:flex;flex-direction:column;align-items:flex-end;gap:4px">'
        +'<div class="v1423-card-price">'+m23(it.price)+' / '+e23(it.unit||'м²')+'</div>'
        +'<button class="v1423-card-sel">'+(isSel?'✓ Выбрано':'Выбрать')+'</button>'
        +'</div></div>';
    }).join('');
  }else{
    cards+='<div class="notice warn">Каталог пуст — импортируйте прайс в Настройках.</div>';
  }

  // Per-zone summary
  var summParts=[];
  var lbFacade=pbGet(book,'labor_facade');
  facades.forEach(function(f){
    if(!f.included||f.qty<=0)return;
    var it=pbGet(book,f.itemId);
    var total=f.qty*(it?it.price:0)+(lbFacade?f.qty*lbFacade.price:0);
    summParts.push(e23(f.zoneName)+': '+(it?e23(it.name.slice(0,12)):'—')+' '+m23(total));
  });
  var summ=summParts.length?summParts.join(' · '):'не заполнены';

  return sec1423('2','facades','Фасады',summ,tabs+sizeHtml+cards);
}

// Section 3: Столешница
function buildCounter1423(){
  var order=state.order||{};
  var book=state.priceBook||[];
  var ctr=order.counter&&order.counter[0];
  var top=state.top||{};

  var enableBtn='<div style="margin-bottom:12px"><button class="chip'+(top.enabled?' active':'')+'" data-action="toggleTop">'
    +(top.enabled?'✓ ':'')+'Столешница нужна</button></div>';

  var body=enableBtn;
  if(top.enabled){
    // Material chips
    var counterCat=book.filter(function(x){return x.category==='counter';});
    var selMatId=ctr?ctr.itemId:'';
    body+='<div class="v1423-seclbl" style="margin:0 0 8px;font-size:12px;font-weight:600;color:var(--muted,var(--ink-muted))">Материал</div>'
      +'<div class="chip-row" style="margin-bottom:12px">'
      +counterCat.map(function(it){
        return '<button class="chip'+(selMatId===it.id?' active':'')+'"'
          +' data-action="v1423-ctr-mat" data-id="'+e23(it.id)+'">'+e23(it.client_name||it.name)+'</button>';
      }).join('')+'</div>';

    // Shape
    var shape=ctr?ctr.shape:'straight';
    body+='<div class="v1423-seclbl" style="margin:0 0 8px;font-size:12px;font-weight:600;color:var(--muted,var(--ink-muted))">Форма</div>'
      +'<div class="v1423-ztabs" style="margin-bottom:12px">'
      +'<button class="v1423-ztab'+(shape==='straight'?' active':'')+'" data-action="v1422-top-shape" data-shape="straight">Прямая</button>'
      +'<button class="v1423-ztab'+(shape==='corner'?' active':'')+'" data-action="v1422-top-shape" data-shape="corner">Угловая (L)</button>'
      +'</div>';

    if(shape==='straight'){
      body+='<div class="grid g2" style="margin-bottom:10px">'
        +'<div class="field"><label>Длина, м</label><input data-bind="top.len" value="'+e23(top.len)+'" type="number" inputmode="decimal"></div>'
        +'<div class="field"><label>Глубина, мм</label><input data-bind="top.depth" value="'+e23(top.depth)+'" type="number" inputmode="decimal"></div>'
        +'</div>';
      if(typeof stepper==='function'){
        body+='<div class="grid g2" style="margin-bottom:10px"><div>'
          +stepper('Вырез мойка','sinkCuts',top.sinkCuts,'top')
          +'</div><div>'+stepper('Вырез плита','hobCuts',top.hobCuts,'top')+'</div></div>';
      }
    }else{
      var la=ctr?n23(ctr.lenA):n23(top.len)||0;
      var lb=ctr?n23(ctr.lenB):0;
      var jointType=ctr?ctr.jointType:'euro';
      body+='<div class="grid g2" style="margin-bottom:10px">'
        +'<div class="field"><label>Длина A, м</label><input data-action="v1422-top-lena" value="'+la+'" type="number" inputmode="decimal"></div>'
        +'<div class="field"><label>Длина B, м</label><input data-action="v1422-top-lenb" value="'+lb+'" type="number" inputmode="decimal"></div>'
        +'</div>'
        +'<div class="field" style="margin-bottom:10px"><label>Глубина, мм</label><input data-bind="top.depth" value="'+e23(top.depth)+'" type="number" inputmode="decimal"></div>'
        +'<div class="chip-row" style="margin-bottom:10px">'
        +'<button class="chip'+(jointType==='euro'?' active':'')+'" data-action="v1422-corner" data-v="euro">Еврозапил (+54€)</button>'
        +'<button class="chip'+(jointType==='miter'?' active':'')+'" data-action="v1422-corner" data-v="miter">Стык</button>'
        +'<button class="chip'+(jointType==='custom'?' active':'')+'" data-action="v1422-corner" data-v="custom">Вручную</button>'
        +'</div>'
        +'<div class="notice" style="font-size:12px">В расчёт: '+(la+lb).toFixed(2)+' м.п. (A '+la.toFixed(2)+' + B '+lb.toFixed(2)+')</div>';
    }

    body+='<div class="v1423-seclbl" style="margin:12px 0 8px;font-size:12px;font-weight:600;color:var(--muted,var(--ink-muted))">Тип мойки</div>'
      +'<div class="chip-row">'
      +'<button class="chip'+(top.sinkType==='surface'?' active':'')+'" data-action="sinkType" data-type="surface">Накладная</button>'
      +'<button class="chip'+(top.sinkType==='under'?' active':'')+'" data-action="sinkType" data-type="under">Подстольная</button>'
      +'</div>';

    // Price preview
    if(ctr){
      var ctrIt=pbGet(book,ctr.itemId);
      var ctrLen=shape==='corner'?(n23(ctr.lenA)+n23(ctr.lenB)):n23(ctr.len);
      var ctrPrice=ctrIt?ctrLen*ctrIt.price:0;
      var ctrCuts=n23(ctr.sinkCuts)*35+n23(ctr.hobCuts)*25;
      var ctrExtra=(ctr.needsStitch?60:0)+(ctr.sinkType==='under'&&ctrIt&&(state.topMaterials||{})[ctr.itemId.replace('ctr_','')]&&(state.topMaterials||{})[ctr.itemId.replace('ctr_','')].under?45:0);
      body+='<div class="v1423-sep"></div><div style="font-size:12px;color:var(--muted,var(--ink-muted))">Итого: '+m23(ctrPrice+ctrCuts+ctrExtra)+'</div>';
    }
  }

  var ctrIt2=ctr?pbGet(book,ctr.itemId):null;
  var summ=top.enabled?(ctrIt2?e23((ctrIt2.client_name||ctrIt2.name).slice(0,15))+' · '+n23(top.len).toFixed(1)+' м':'нет материала'):'не нужна';
  return sec1423('3','counter','Столешница',summ,body);
}

// Section 4: Материалы (BOM view)
function buildMaterials1423(){
  var book=state.priceBook||[];
  var order=state.order||{};
  var rows='';

  // Facade materials per zone
  (order.facades||[]).forEach(function(f){
    if(f.qty<=0)return;
    var it=pbGet(book,f.itemId);
    rows+='<div class="v1423-bom-row"><span><b>'+e23(f.zoneName||f.zoneId)+'</b> · '+(it?e23(it.name):'—')+'</span>'
      +'<span>'+n23(f.qty).toFixed(2)+' м² × '+m23(it?it.price:0)+'</span></div>';
  });

  // Labor
  var lf=pbGet(book,'labor_facade');
  var ld=pbGet(book,'labor_door');
  var totalArea=area23();
  var totalDoors2=doors23();
  if(lf&&totalArea>0){
    rows+='<div class="v1423-bom-row"><span><b>Работа</b> · фасады</span><span>'+totalArea.toFixed(2)+' м² × '+m23(lf.price)+'</span></div>';
  }
  if(ld&&totalDoors2>0){
    rows+='<div class="v1423-bom-row"><span><b>Работа</b> · двери</span><span>'+totalDoors2+' шт × '+m23(ld.price)+'</span></div>';
  }

  // Counter
  (order.counter||[]).forEach(function(c){
    if(!c.enabled)return;
    var it=pbGet(book,c.itemId);
    var len=c.shape==='corner'?(n23(c.lenA)+n23(c.lenB)):n23(c.len);
    if(it&&len>0){
      rows+='<div class="v1423-bom-row"><span><b>Столешница</b> · '+e23(it.client_name||it.name)+'</span><span>'+len.toFixed(2)+' м × '+m23(it.price)+'</span></div>';
    }
    if(n23(c.sinkCuts)>0)rows+='<div class="v1423-bom-row"><span>Вырез под мойку</span><span>'+n23(c.sinkCuts)+' шт × '+m23(35)+'</span></div>';
    if(n23(c.hobCuts)>0)rows+='<div class="v1423-bom-row"><span>Вырез под плиту</span><span>'+n23(c.hobCuts)+' шт × '+m23(25)+'</span></div>';
    if(c.needsStitch)rows+='<div class="v1423-bom-row"><span>Стык / еврозапил</span><span>1 шт × '+m23(60)+'</span></div>';
  });

  if(!rows)rows='<div class="v1423-row-empty">Заполните зоны и материалы в разделах 2–3.</div>';
  var body=rows+'<div style="font-size:11px;color:var(--muted,var(--ink-muted));margin-top:8px">Цены берутся из прайс-книги. Редактировать расценки: Настройки.</div>';

  var summ=totalArea>0?totalArea.toFixed(1)+' м² фасады':'заполните зоны';
  return sec1423('4','materials','Материалы',summ,body);
}

// Section 5: Фурнитура
function buildHardware1423(){
  var book=state.priceBook||[];
  var order=state.order||{};
  var hw=state.hardware||{};
  var hMode=hw.handlesMode||'we';

  // Handle mode (reuse existing handlers)
  var handleHtml='<div style="margin-bottom:12px">'
    +'<div style="font-size:12px;font-weight:600;color:var(--muted,var(--ink-muted));margin-bottom:8px">Ручки</div>'
    +'<div class="chip-row">'
    +'<button class="chip'+(hMode==='client'?' active':'')+'" data-action="setHandleMode" data-mode="client">Клиент покупает</button>'
    +'<button class="chip'+(hMode==='we'?' active':'')+'" data-action="setHandleMode" data-mode="we">Мы подберём</button>'
    +'<button class="chip'+(hMode==='later'?' active':'')+'" data-action="setHandleMode" data-mode="later">Уточнить позже</button>'
    +'</div></div>';

  var hwRows=(order.hardware||[]).map(function(h){
    var it=pbGet(book,h.itemId);if(!it)return '';
    var qty=h.qtyOverride!=null?n23(h.qtyOverride):n23(h.qtyAuto);
    var isOverride=h.qtyOverride!=null;
    var price=it.price;
    var lineTotal=qty*price;
    var priceStr=price>0?(qty>0?m23(lineTotal):'—'):'—';
    if(price===0&&qty>0)priceStr='<span class="v1423-honest">уточнить цену</span>';
    return '<div class="v1423-row">'
      +'<div style="flex:1"><div class="v1423-row-name">'+e23(it.client_name||it.name)+'</div>'
      +'<div class="v1423-row-sub">'+m23(price)+' / '+e23(it.unit)+'</div></div>'
      +'<div class="v1423-stepper">'
      +'<button data-action="v1423-hw-minus" data-id="'+e23(h.id)+'">−</button>'
      +'<span class="v1423-qty">'+qty+'</span>'
      +'<button data-action="v1423-hw-plus"  data-id="'+e23(h.id)+'">+</button>'
      +(isOverride?'<button data-action="v1423-hw-reset" data-id="'+e23(h.id)+'" title="Сбросить к авто" style="font-size:10px;width:auto;padding:0 6px">⟳</button>':'')
      +'</div>'
      +(isOverride?'':'<span class="v1423-auto-badge">авто</span>')
      +'<button class="v1423-toggle'+(h.included?' on':'')+'" data-action="v1423-hw-incl" data-id="'+e23(h.id)+'">'+(h.included?'Включ':'Выкл')+'</button>'
      +'<div class="v1423-row-price">'+(h.included?priceStr:'<span style="color:var(--muted,var(--ink-muted))">откл.</span>')+'</div>'
      +'</div>';
  }).join('');

  var inclTotal=(order.hardware||[]).reduce(function(a,h){
    if(!h.included)return a;
    var it=pbGet(book,h.itemId);if(!it)return a;
    var qty=h.qtyOverride!=null?n23(h.qtyOverride):n23(h.qtyAuto);
    return a+qty*it.price;
  },0);

  var summ=inclTotal>0?m23(inclTotal)+' в расчёте':'не включена (авто-подсчёт)';
  return sec1423('5','hardware','Фурнитура',summ,handleHtml+hwRows);
}

// Section 6: Услуги
function buildServices1423(){
  var book=state.priceBook||[];
  var order=state.order||{};
  var rows=(order.services||[]).map(function(s){
    var it=pbGet(book,s.itemId);if(!it)return '';
    var qty=n23(s.qty)||1;
    var price=it.price;
    var lineStr=price>0?(s.enabled?m23(qty*price)+'<small style="font-size:10px;color:var(--muted,var(--ink-muted))"> ('+m23(price)+'/'+e23(it.unit)+')</small>':'<span style="color:var(--muted,var(--ink-muted))">'+m23(price)+'/'+e23(it.unit)+'</span>'):'<span class="v1423-honest">уточнить цену</span>';
    return '<div class="v1423-row">'
      +'<button class="v1423-toggle'+(s.enabled?' on':'')+'" data-action="v1423-svc" data-id="'+e23(s.id)+'">'+(s.enabled?'ВКЛ':'ВЫКЛ')+'</button>'
      +'<div class="v1423-row-name">'+e23(it.client_name||it.name)+'</div>'
      +(s.enabled&&price>0?('<div class="v1423-stepper"><button data-action="v1423-svc-minus" data-id="'+e23(s.id)+'">−</button>'
        +'<span class="v1423-qty">'+qty+'</span>'
        +'<button data-action="v1423-svc-plus" data-id="'+e23(s.id)+'">+</button></div>'):'')
      +'<div class="v1423-row-price">'+lineStr+'</div>'
      +'</div>';
  }).join('');

  var addBtn='<button class="v1423-add-btn" data-action="v1423-svc-add">＋ Добавить свою позицию</button>';
  var onCount=(order.services||[]).filter(function(s){return s.enabled;}).length;
  var summ=onCount?onCount+' вкл.':'не выбраны';
  return sec1423('6','services','Услуги',summ,rows+addBtn);
}

// Section 7: Улучшения (options)
function buildOptions1423(){
  var book=state.priceBook||[];
  var order=state.order||{};
  var rows=(order.options||[]).map(function(o){
    var it=pbGet(book,o.itemId);if(!it)return '';
    var fits={};try{fits=JSON.parse(it.fits||'{}');}catch(e){}
    var qty=1;
    if(fits.unit==='hinge')qty=hinges23();
    else if(fits.unit==='drawer')qty=drawers23();
    else if(fits.unit==='led')qty=n23((o.config||{}).meters)||0;
    else if(fits.unit==='mdfArea')qty=area23();
    var priceStr='';
    if(fits.unit==='led'){
      if(o.enabled&&qty<=0)priceStr='<span class="v1423-honest">укажите длину</span>';
      else if(o.enabled)priceStr=m23(qty*it.price);
      else priceStr='+'+m23(it.price)+'/м';
    }else{
      priceStr='+'+m23(qty*it.price);
    }
    var row='<div class="v1423-row">'
      +'<button class="v1423-toggle'+(o.enabled?' on':o.recommend?' rec':'')+'" data-action="v1423-opt" data-id="'+e23(o.id)+'">'+(o.enabled?'ВКЛ':o.recommend?'РЕК':'ВЫКЛ')+'</button>'
      +'<div style="flex:1"><div class="v1423-row-name">'+e23(it.client_name||it.name)+'</div>'
      +(it.hint?'<div class="v1423-row-sub">'+e23(it.hint.slice(0,60))+'</div>':'')+'</div>'
      +'<div class="v1423-row-price">'+priceStr+'</div>'
      +'</div>';
    // LED config inline
    if(fits.unit==='led'&&o.enabled){
      var ledRow=pbGet(book,'led_ledStrip');
      var ledProf=pbGet(book,'led_ledProfile');
      var ledPwr=pbGet(book,'led_ledPower');
      row+='<div class="v1423-led-cfg" style="padding:0 0 8px 36px">'
        +'<div class="field"><label style="font-size:11px">Длина, м</label>'
        +'<input type="number" inputmode="decimal" data-action="v1423-opt-led-m" data-id="'+e23(o.id)+'"'
        +' value="'+e23((o.config||{}).meters||'')+'" placeholder="м" style="width:70px"></div>'
        +(ledProf?'<div class="field"><label style="font-size:11px">Профиль</label>'
          +'<select data-action="v1423-opt-led-prof" data-id="'+e23(o.id)+'">'
          +'<option>накладной</option><option>встраиваемый</option><option>угловой</option></select></div>':'')
        +(ledPwr?'<div class="field"><label style="font-size:11px">Блок питания</label>'
          +'<select data-action="v1423-opt-led-psu" data-id="'+e23(o.id)+'">'
          +'<option>нужен</option><option>есть</option></select></div>':'')
        +'</div>';
    }
    return row;
  }).join('');

  var enabledOpts=(order.options||[]).filter(function(o){return o.enabled;}).length;
  var summ=enabledOpts?enabledOpts+' вкл.':'не выбраны';
  return sec1423('7','options','Улучшения',summ,rows);
}

// ── 7. Main render ─────────────────────────────────────────────────────
function renderOrder1423(){
  migrateToOrder1423();
  refreshHwAuto1423();
  var t=orderTotals1423()||{totalClient:0,margin:0,profit:0};
  var p=state.project||{};
  var hdr='<div class="v1423-hdr">'
    +'<div class="v1423-hdr-left">'
    +'<div class="v1423-hdr-name">'+e23(p.client||'Новый проект')+'</div>'
    +'<div class="v1423-hdr-sub">'+e23(p.status||'')+(p.want?' · '+e23(p.want):'')+'</div>'
    +'</div>'
    +'<div class="v1423-hdr-total">'
    +'<b>'+m23(t.totalClient)+'</b>'
    +'<small>'+Math.round(t.margin||0)+'% маржа</small>'
    +'</div></div>';

  return '<div class="v1423-view">'
    +hdr
    +buildPassport1423()
    +buildFacades1423()
    +buildCounter1423()
    +buildMaterials1423()
    +buildHardware1423()
    +buildServices1423()
    +buildOptions1423()
    +'</div>';
}

// ── 8. Replace renderFast ──────────────────────────────────────────────
window.renderFast=function(){
  var pane=document.getElementById('pane-fast');
  if(pane)pane.innerHTML=renderOrder1423();
};

// ── 9. Replace totals() (wraps old as fallback) ───────────────────────
var _origTotals1423=typeof totals==='function'?totals:null;
window.totals=function(){
  if(state&&state.order&&Array.isArray(state.priceBook)&&state.priceBook.length){
    var r=orderTotals1423();
    if(r)return r;
  }
  return _origTotals1423?_origTotals1423():{base:{sell:0,cost:0},improvements:{sell:0,cost:0},totalClient:0,totalCost:0,profit:0,margin:0,paid:0,remaining:0};
};

// ── 10. Click handler (capture, v1423-* only) ─────────────────────────
document.addEventListener('click',function(ev){
  var b=ev.target.closest('[data-action]');if(!b)return;
  var a=b.dataset.action;
  if(!a||a.indexOf('v1423-')<0)return;
  ev.preventDefault();ev.stopImmediatePropagation();
  migrateToOrder1423();
  state.accOpen1423=state.accOpen1423||{};
  state.wf1423=state.wf1423||{};
  var order=state.order;

  if(a==='v1423-acc'){
    state.accOpen1423[b.dataset.id]=!state.accOpen1423[b.dataset.id];
  }
  else if(a==='v1423-zone'){
    state.wf1423.zone=b.dataset.zone;
  }
  else if(a==='v1423-facade'){
    var zoneId=b.dataset.zone||state.wf1423.zone||'lower';
    var fEntry=order.facades.find(function(f){return f.zoneId===zoneId;});
    if(fEntry){
      fEntry.itemId=b.dataset.id;
      fEntry.included=true;
      // Also sync to old state for legacy totals compat
      var it2=pbGet(state.priceBook,b.dataset.id);
      if(it2){
        var mat=typeof activeMaterial==='function'?activeMaterial():null;
        if(mat){mat.price=n23(it2.price);mat.cost=n23(it2.cost);mat.tech=it2.name;}
        state.wf1422=state.wf1422||{};
        state.wf1422['sel_'+zoneId]=it2.name;
      }
    }
  }
  else if(a==='v1423-ctr-mat'){
    if(order.counter&&order.counter[0]){
      order.counter[0].itemId=b.dataset.id;
      // Sync to state.top.material
      var matKey=b.dataset.id.replace('ctr_','');
      if(state.top)state.top.material=matKey;
    }
  }
  else if(a==='v1423-hw-plus'){
    var hw=order.hardware.find(function(h){return h.id===b.dataset.id;});
    if(hw){hw.qtyOverride=(hw.qtyOverride!=null?n23(hw.qtyOverride):n23(hw.qtyAuto))+1;}
  }
  else if(a==='v1423-hw-minus'){
    var hw=order.hardware.find(function(h){return h.id===b.dataset.id;});
    if(hw){var newQ=(hw.qtyOverride!=null?n23(hw.qtyOverride):n23(hw.qtyAuto))-1;hw.qtyOverride=Math.max(0,newQ);}
  }
  else if(a==='v1423-hw-reset'){
    var hw=order.hardware.find(function(h){return h.id===b.dataset.id;});
    if(hw)hw.qtyOverride=null;
  }
  else if(a==='v1423-hw-incl'){
    var hw=order.hardware.find(function(h){return h.id===b.dataset.id;});
    if(hw)hw.included=!hw.included;
  }
  else if(a==='v1423-svc'){
    var s=order.services.find(function(x){return x.id===b.dataset.id;});
    if(s){s.enabled=!s.enabled;if(s.enabled&&!s.qty)s.qty=1;}
  }
  else if(a==='v1423-svc-plus'){
    var s=order.services.find(function(x){return x.id===b.dataset.id;});
    if(s)s.qty=(n23(s.qty)||1)+1;
  }
  else if(a==='v1423-svc-minus'){
    var s=order.services.find(function(x){return x.id===b.dataset.id;});
    if(s)s.qty=Math.max(1,(n23(s.qty)||1)-1);
  }
  else if(a==='v1423-svc-add'){
    var name=prompt('Название позиции:','');
    if(name){
      var price=n23(prompt('Цена €:','0'));
      var customId='custom_'+uid23('s');
      state.priceBook.push({id:customId,name:name,client_name:name,category:'service',
        unit:'усл.',price:price,cost:0,supplier:'',art:'',fits:'',hint:''});
      order.services.push({id:uid23('svc'),itemId:customId,enabled:true,qty:1});
    }
  }
  else if(a==='v1423-opt'){
    var o=order.options.find(function(x){return x.id===b.dataset.id;});
    if(o){
      if(!o.enabled&&!o.recommend){o.enabled=false;o.recommend=true;}
      else if(!o.enabled&&o.recommend){o.enabled=true;o.recommend=false;}
      else{o.enabled=false;o.recommend=false;}
      // Sync to old improvements for compat
      var im=state.improvements&&state.improvements.find(function(i){return 'opt_'+i.id===o.itemId;});
      if(im&&typeof setImproveStatus==='function')
        setImproveStatus(im.id,o.enabled?'included':o.recommend?'recommend':'recommend');
    }
  }

  if(typeof markDirty==='function')markDirty();
  if(typeof renderCurrent==='function')renderCurrent();
},true);

// ── 11. Input handler ─────────────────────────────────────────────────
document.addEventListener('input',function(ev){
  var x=ev.target;var a=x.dataset.action;
  if(!a||a.indexOf('v1423-')<0)return;
  migrateToOrder1423();
  var order=state.order;

  if(a==='v1423-opt-led-m'){
    var o=order.options.find(function(x2){return x2.id===ev.target.dataset.id;});
    if(o){o.config=o.config||{};o.config.meters=n23(x.value);
      // Also sync to old improvements
      var im=state.improvements&&state.improvements.find(function(i){return 'opt_'+i.id===o.itemId;});
      if(im)im.meters=n23(x.value);
    }
    if(typeof markDirty==='function')markDirty();
    if(typeof renderHeader==='function')renderHeader();
  }
  // led-prof / led-psu config
  if(a==='v1423-opt-led-prof'||a==='v1423-opt-led-psu'){
    var o=order.options.find(function(x2){return x2.id===ev.target.dataset.id;});
    if(o){o.config=o.config||{};o.config[a.replace('v1423-opt-led-','')]=x.value;}
    if(typeof markDirty==='function')markDirty();
  }
},true);

// ── 12. Helper: input/select renderers (local copies) ─────────────────
function inputF(label,bind,val,ph){
  return '<div class="field"><label>'+e23(label)+'</label>'
    +'<input value="'+e23(val)+'" placeholder="'+(ph||'')+'" data-bind="'+e23(bind)+'"></div>';
}
function selF(label,bind,val,opts){
  return '<div class="field"><label>'+e23(label)+'</label><select data-bind="'+e23(bind)+'">'
    +opts.map(function(o){return '<option'+(o===val?' selected':'')+'>'+e23(o)+'</option>';}).join('')
    +'</select></div>';
}

// ── 13. Init ──────────────────────────────────────────────────────────
(function(){
  try{
    if(typeof ensureV1414==='function')ensureV1414();
    if(typeof ensureV1043State==='function')ensureV1043State();
    migrateToOrder1423();
  }catch(err){console.error('[v1423] init error:',err);}
})();

window.__v1423={V:V1423,buildPriceBook1423:buildPriceBook1423,migrateToOrder1423:migrateToOrder1423,
  orderTotals1423:orderTotals1423,renderOrder1423:renderOrder1423};
console.info('[v10.4.23] Core Engine Fast loaded');
})();
</script>
"""

# ─────────────────────────────────────────────────────────────────────
# BUILD
# ─────────────────────────────────────────────────────────────────────
def build():
    src = os.path.join(DIR, BASE)
    out = os.path.join(DIR, OUT)

    with open(src, 'r', encoding='utf-8') as f:
        html = f.read()

    # Safety: must be exactly one </body>
    if html.count('</body>') != 1:
        print('ERROR: expected exactly 1 </body> in base file')
        sys.exit(1)

    result = html.replace('</body>', LAYER + '\n</body>', 1)

    with open(out, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f'Built: {OUT}')
    print(f'Lines: {result.count(chr(10))+1}')
    print(f'Chars: {len(result)}')
    return result

# ─────────────────────────────────────────────────────────────────────
# GATE ASSERTIONS
# ─────────────────────────────────────────────────────────────────────
def gate(html):
    errors = []
    checks = [
        ('MAIN_KEY intact',           'anbamo_v10_4_6_mvp_stabilization'),
        ('priceBook builder',          'buildPriceBook1423'),
        ('order model',                'defaultOrder1423'),
        ('migrateToOrder',             'migrateToOrder1423'),
        ('orderTotals',                'orderTotals1423'),
        ('renderOrder',                'renderOrder1423'),
        ('v1423-facade action',        'v1423-facade'),
        ('v1423-hw-incl action',       'v1423-hw-incl'),
        ('v1423-svc action',           'v1423-svc'),
        ('v1423-opt action',           'v1423-opt'),
        ('v1423-svc-add action',       'v1423-svc-add'),
        ('labor_facade in priceBook',  'labor_facade'),
        ('Section 1 Паспорт',          'buildPassport1423'),
        ('Section 2 Фасады',           'buildFacades1423'),
        ('Section 3 Столешница',       'buildCounter1423'),
        ('Section 4 Материалы',        'buildMaterials1423'),
        ('Section 5 Фурнитура',        'buildHardware1423'),
        ('Section 6 Услуги',           'buildServices1423'),
        ('Section 7 Улучшения',        'buildOptions1423'),
        ('LED config inline',          'v1423-opt-led-m'),
        ('hw auto-count refresh',      'refreshHwAuto1423'),
        ('window.__v1423',             'window.__v1423'),
        ('single </body>',             None),  # special check
        ('v10.4.22 layer intact',      'window.__v1422'),
        ('v10.4.21b layer intact',     'window.__v1421b'),
        ('multi-project API intact',   'window.__v10472'),
    ]

    for label, needle in checks:
        if needle is None:
            count = html.count('</body>')
            if count != 1:
                errors.append(f'[FAIL] {label}: expected 1, got {count}')
            else:
                print(f'  [PASS] {label}')
        elif needle in html:
            print(f'  [PASS] {label}')
        else:
            errors.append(f'[FAIL] {label}: "{needle}" not found')

    print()
    if errors:
        for e in errors:
            print(e)
        sys.exit(1)
    print('All gates PASS')

if __name__ == '__main__':
    html = build()
    print('\n=== GATE CHECKS ===')
    gate(html)
