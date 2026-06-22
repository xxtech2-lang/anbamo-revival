#!/usr/bin/env python3
# build_v10231.py — Model Fix: 6 sections, multi-facade, category correction
# Base:   AN_BAMO_Command_Center_v10_4_23_Core_Engine_Fast.html
# Output: AN_BAMO_Command_Center_v10_4_23_1_Model_Fix.html

import os, sys

BASE = 'AN_BAMO_Command_Center_v10_4_23_Core_Engine_Fast.html'
OUT  = 'AN_BAMO_Command_Center_v10_4_23_1_Model_Fix.html'
DIR  = os.path.dirname(os.path.abspath(__file__))

LAYER = r"""
<style>
/* ── v10.4.23.1 Model Fix ── */
.v10231-fcard{border:1px solid var(--divider,rgba(0,0,0,.1));border-radius:10px;padding:12px;margin-bottom:10px;background:var(--card-bg,var(--surface));}
.v10231-fcard-head{display:flex;align-items:center;gap:8px;margin-bottom:10px;}
.v10231-fcard-label{flex:1;padding:6px 8px;border:1px solid var(--divider,rgba(0,0,0,.1));border-radius:8px;font-size:13px;background:var(--card-bg,var(--surface));color:var(--txt,var(--ink));}
.v10231-fcard-matsel{width:100%;padding:7px 8px;border:1px solid var(--divider,rgba(0,0,0,.1));border-radius:8px;font-size:13px;background:var(--card-bg,var(--surface));color:var(--txt,var(--ink));margin-bottom:8px;}
.v10231-fcard-remove{width:28px;height:28px;border-radius:50%;border:1px solid rgba(239,68,68,.3);background:transparent;color:#ef4444;font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.v10231-fcard-remove:hover{background:rgba(239,68,68,.08);}
.v10231-fcard-dims{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;}
.v10231-fcard-dims .field{margin:0;}
.v10231-fcard-dims label{font-size:11px;}
.v10231-fcard-dims input{font-size:13px;padding:6px 8px;}
.v10231-fcard-ctrls{display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-bottom:4px;}
.v10231-fcard-sub{font-size:11px;color:var(--muted,var(--ink-muted));margin-top:6px;padding-top:6px;border-top:1px solid var(--divider,rgba(0,0,0,.06));}
.v10231-rec-flag{display:inline-flex;align-items:center;gap:3px;padding:3px 8px;border-radius:6px;border:1px solid rgba(245,158,11,.4);background:transparent;color:#d97706;font-size:11px;cursor:pointer;white-space:nowrap;}
.v10231-rec-flag.on{background:rgba(245,158,11,.15);border-color:rgba(245,158,11,.6);}
.v10231-led-inline{display:flex;flex-wrap:wrap;gap:8px;margin-top:6px;padding:8px 0 4px;}
.v10231-led-inline .field{margin:0;}
.v10231-led-inline label{font-size:11px;}
</style>

<script>
(function(){
'use strict';
var V10231='v10.4.23.1 Model Fix';

// ── helpers ──────────────────────────────────────────────────────────
function n1(v){return typeof num==='function'?num(v):(Number(String(v==null?0:v).replace(',','.'))||0);}
function m1(v){return typeof money==='function'?money(v):(Math.round(n1(v))+' €');}
function e1(v){return String(v==null?'':v).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function uid1(p){return p+'_'+Date.now().toString(36)+Math.random().toString(36).slice(2,6);}
function pbGet1(book,id){for(var i=0;i<book.length;i++){if(book[i].id===id)return book[i];}return null;}
function getFits(it){var f={};try{f=JSON.parse((it&&it.fits)||'{}');}catch(e){}return f;}

// Facade-based helpers (work off order.facades directly)
function fDoors1(){return((state.order&&state.order.facades)||[]).reduce(function(a,f){return a+(f.included!==false?n1(f.doors):0);},0);}
function fDrawers1(){return((state.order&&state.order.facades)||[]).reduce(function(a,f){return a+(f.included!==false?n1(f.drawers):0);},0);}
function fHinges1(){return((state.order&&state.order.facades)||[]).reduce(function(a,f){
  if(f.included===false)return a;
  var h=n1(f.height)||2000;
  return a+n1(f.doors)*(h>1600?4:h>900?3:2);
},0);}
function fArea1(){return((state.order&&state.order.facades)||[]).reduce(function(a,f){
  if(f.included===false)return a;
  return a+Math.max(0,n1(f.len)*n1(f.height)/1000-n1(f.deduct||0));
},0);}

// ── 1. Category patches on priceBook ─────────────────────────────────
var LEGS_IDS=['ew_legs','svc_legs'];
var MAT_IDS=['ew_plinth','ew_cornice','ew_corpus'];
function fixPriceBook10231(book){
  book.forEach(function(it){
    if(!it)return;
    if(it.id.indexOf('led_')===0)            it.category='hardware';
    else if(it.id.indexOf('opt_')===0)       it.category='hardware';
    else if(LEGS_IDS.indexOf(it.id)>=0)      it.category='hardware';
    else if(MAT_IDS.indexOf(it.id)>=0)       it.category='material';
  });
  return book;
}

// ── 2. Re-migration (idempotent via _v10231migrated) ─────────────────
function migrateToOrder10231(){
  if(!state)return;
  if(typeof migrateToOrder1423==='function')migrateToOrder1423();
  if(!Array.isArray(state.priceBook)||state.priceBook.length<5)return;
  fixPriceBook10231(state.priceBook);
  if(state._v10231migrated)return;

  var order=state.order;
  if(!order)return;
  var book=state.priceBook;

  // 2a. Move order.options → order.hardware
  var newHw=order.hardware?order.hardware.slice():[];
  (order.options||[]).forEach(function(o){
    if(newHw.some(function(h){return h.itemId===o.itemId;}))return;
    var it=pbGet1(book,o.itemId);
    var fits=getFits(it);
    var cfg=o.config||{};
    var qa;
    if(fits.unit==='hinge')   qa=fHinges1();
    else if(fits.unit==='drawer') qa=fDrawers1();
    else if(fits.unit==='led')    qa=n1(cfg.meters)||0;
    else if(fits.unit==='mdfArea')qa=fArea1();
    else qa=1;
    newHw.push({id:uid1('hw'),itemId:o.itemId,qtyAuto:qa,qtyOverride:null,
      included:!!o.enabled,recommend:!!o.recommend,config:cfg});
  });
  order.hardware=newHw;
  order.options=[];

  // 2b. Move legs from services → hardware; plinth/cornice → materials
  var newSvc=[];
  if(!order.materials)order.materials=[];
  (order.services||[]).forEach(function(s){
    if(LEGS_IDS.indexOf(s.itemId)>=0){
      if(!order.hardware.some(function(h){return h.itemId===s.itemId;}))
        order.hardware.push({id:uid1('hw'),itemId:s.itemId,qtyAuto:1,qtyOverride:null,
          included:!!s.enabled,recommend:false,config:{}});
    } else if(MAT_IDS.indexOf(s.itemId)>=0){
      if(!order.materials.some(function(m){return m.itemId===s.itemId;}))
        order.materials.push({id:uid1('mat'),itemId:s.itemId,qty:n1(s.qty)||1,
          included:!!s.enabled,recommend:false});
    } else {
      if(s.recommend===undefined)s.recommend=false;
      newSvc.push(s);
    }
  });
  order.services=newSvc;

  // 2c. Ensure recommend + config on all hardware
  order.hardware.forEach(function(h){
    if(h.recommend===undefined)h.recommend=false;
    if(!h.config)h.config={};
  });

  // 2d. Augment facade positions with len/height from zones
  var zones10231=[];
  try{if(typeof ensureV1043State==='function')ensureV1043State();zones10231=state.zones||[];}catch(e){}
  (order.facades||[]).forEach(function(f){
    if(!f.label)f.label=f.zoneName||'Зона';
    if(!(f.len>0)||!(f.height>0)){
      var z=zones10231.find(function(x){return x.id===f.zoneId;});
      if(z){f.len=n1(z.len)||0;f.height=n1(z.height)||2000;}
      else if(n1(f.qty)>0){f.height=2000;f.len=+(n1(f.qty)*1000/2000).toFixed(2);}
    }
  });

  state._v10231migrated=true;
  if(typeof markDirty==='function')markDirty();
}

// ── 3. Totals (6-section) ─────────────────────────────────────────────
function orderTotals10231(){
  if(!state.order||!state.priceBook)return null;
  var book=state.priceBook,order=state.order;
  var sell=0,cost=0,baseS=0;

  // Facades
  (order.facades||[]).forEach(function(f){
    if(f.included===false)return;
    var area=Math.max(0,n1(f.len)*n1(f.height)/1000-n1(f.deduct||0));
    if(area<=0&&n1(f.qty)>0)area=n1(f.qty);
    if(area<=0)return;
    var it=pbGet1(book,f.itemId);
    var lf=pbGet1(book,'labor_facade');
    var ld=pbGet1(book,'labor_door');
    if(it){var s=area*it.price;sell+=s;cost+=area*it.cost;baseS+=s;}
    if(lf){var s2=area*lf.price;sell+=s2;cost+=area*lf.cost;baseS+=s2;}
    if(ld&&n1(f.doors)>0){var s3=n1(f.doors)*ld.price;sell+=s3;cost+=n1(f.doors)*ld.cost;baseS+=s3;}
  });

  // Counter
  (order.counter||[]).forEach(function(c){
    if(!c.enabled)return;
    var it=pbGet1(book,c.itemId);
    var cs=pbGet1(book,'cut_sink');var ch=pbGet1(book,'cut_hob');
    var cst=pbGet1(book,'ctr_stitch');var cun=pbGet1(book,'ctr_under');
    var len=c.shape==='corner'?(n1(c.lenA)+n1(c.lenB)):n1(c.len);
    if(it&&len>0){var s=len*it.price;sell+=s;cost+=len*it.cost;baseS+=s;}
    if(cs&&n1(c.sinkCuts)>0){var s2=n1(c.sinkCuts)*cs.price;sell+=s2;cost+=n1(c.sinkCuts)*cs.cost;baseS+=s2;}
    if(ch&&n1(c.hobCuts)>0){var s3=n1(c.hobCuts)*ch.price;sell+=s3;cost+=n1(c.hobCuts)*ch.cost;baseS+=s3;}
    if(cst&&c.needsStitch){sell+=cst.price;cost+=cst.cost;baseS+=cst.price;}
    if(cun&&c.sinkType==='under'){
      var tmObj=(state.topMaterials||{})[c.itemId.replace('ctr_','')]||{};
      if(tmObj.under){sell+=cun.price;cost+=cun.cost;baseS+=cun.price;}
    }
  });

  // Hardware (included only; fits-based qty for dynamic items)
  (order.hardware||[]).forEach(function(h){
    if(!h.included)return;
    var it=pbGet1(book,h.itemId);if(!it)return;
    var fits=getFits(it);
    var qty;
    if(fits.unit==='led')         qty=n1((h.config||{}).meters)||0;
    else if(fits.unit==='hinge')  qty=fHinges1();
    else if(fits.unit==='drawer') qty=fDrawers1();
    else if(fits.unit==='mdfArea')qty=fArea1();
    else qty=h.qtyOverride!=null?n1(h.qtyOverride):n1(h.qtyAuto);
    if(qty>0&&it.price>0){sell+=qty*it.price;cost+=qty*it.cost;baseS+=qty*it.price;}
  });

  // Services (enabled only)
  (order.services||[]).forEach(function(s){
    if(!s.enabled)return;
    var it=pbGet1(book,s.itemId);if(!it)return;
    var qty=n1(s.qty)||1;
    if(it.price>0){sell+=qty*it.price;cost+=qty*it.cost;baseS+=qty*it.price;}
  });

  // Extra materials (included only)
  (order.materials||[]).forEach(function(m){
    if(!m.included)return;
    var it=pbGet1(book,m.itemId);if(!it)return;
    var qty=n1(m.qty)||1;
    if(it.price>0){sell+=qty*it.price;cost+=qty*it.cost;baseS+=qty*it.price;}
  });

  var expenses=(state.expenses||[]).reduce(function(a,x){return a+n1(x.amount);},0);
  var paid=(state.payments||[]).reduce(function(a,x){return a+n1(x.amount);},0);
  var profit=sell-cost-expenses;
  var margin=sell>0?profit/sell*100:0;
  return{totalClient:sell,totalCost:cost+expenses,profit:profit,margin:margin,
    paid:paid,remaining:Math.max(0,sell-paid),
    base:{sell:baseS,cost:cost},improvements:{sell:0,cost:0}};
}

// ── 4. Section wrapper + local form helpers ───────────────────────────
state.accOpen10231=state.accOpen10231||{};
function iF1(label,bind,val,ph){
  return'<div class="field"><label>'+e1(label)+'</label>'
    +'<input value="'+e1(val)+'" placeholder="'+(ph||'')+'" data-bind="'+e1(bind)+'"></div>';
}
function sF1(label,bind,val,opts){
  return'<div class="field"><label>'+e1(label)+'</label><select data-bind="'+e1(bind)+'">'
    +opts.map(function(o){return'<option'+(o===val?' selected':'')+'>'+e1(o)+'</option>';}).join('')
    +'</select></div>';
}
function sec10231(num,id,title,summary,body){
  var open=!!(state.accOpen10231&&state.accOpen10231[id]);
  return '<div class="v1423-acc card'+(open?' open':'')+'" data-v10231acc="'+id+'">'
    +'<button class="v1423-acc-head" data-action="v10231-acc" data-id="'+e1(id)+'">'
    +'<span class="v1423-acc-num">'+e1(num)+'</span>'
    +'<span class="v1423-acc-title">'+e1(title)+'</span>'
    +'<span class="v1423-acc-sum">'+e1(summary)+'</span>'
    +'<span class="v1423-chev">&#9662;</span>'
    +'</button>'
    +'<div class="v1423-acc-body">'+body+'</div>'
    +'</div>';
}

// ── 4b. Паспорт ───────────────────────────────────────────────────────
function buildPassport10231(){
  var p=state.project||{};
  var body='<div class="grid g2">'
    +'<div>'+iF1('Клиент','project.client',p.client||'','Иванов / кухня')+'</div>'
    +'<div>'+iF1('Телефон','project.phone',p.phone||'','+372...')+'</div>'
    +'<div>'+iF1('Адрес','project.address',p.address||'','Tallinn...')+'</div>'
    +'<div>'+sF1('Статус','project.status',p.status||'Новая заявка',
      ['Новая заявка','ПредКП подготовлено','ПредКП отправлено','Замер назначен','Замер сделан',
       'Ожидаем аванс','Аванс получен','В производстве','Монтаж назначен','Установлено','Закрыт','Отказ'])+'</div>'
    +'<div>'+sF1('Запрос','project.want',p.want||'Фасады + столешница',
      ['Только фасады','Фасады + столешница','Фасады + фурнитура','Полное обновление кухни'])+'</div>'
    +'</div>';
  var summ=(p.client||'не заполнен')+(p.status?' · '+p.status:'');
  return sec10231('1','passport','Паспорт',summ,body);
}

// ── 4c. Столешница ────────────────────────────────────────────────────
function buildCounter10231(){
  var book=state.priceBook||[];
  var order=state.order||{};
  var ctr=order.counter&&order.counter[0];
  var top=state.top||{};
  var counterCat=book.filter(function(x){return x.category==='counter';});

  var enableBtn='<div style="margin-bottom:12px"><button class="chip'+(top.enabled?' active':'')+'" data-action="toggleTop">'
    +(top.enabled?'&#10003; ':'')+'Столешница нужна</button></div>';
  var body=enableBtn;

  if(top.enabled){
    var selMatId=ctr?ctr.itemId:'';
    body+='<div class="chip-row" style="margin-bottom:12px">'
      +counterCat.map(function(it){
        return'<button class="chip'+(selMatId===it.id?' active':'')+'" data-action="v1423-ctr-mat" data-id="'+e1(it.id)+'">'+e1(it.client_name||it.name)+'</button>';
      }).join('')+'</div>';

    var shape=ctr?ctr.shape:'straight';
    body+='<div class="v1423-ztabs" style="margin-bottom:12px">'
      +'<button class="v1423-ztab'+(shape==='straight'?' active':'')+'" data-action="v1422-top-shape" data-shape="straight">Прямая</button>'
      +'<button class="v1423-ztab'+(shape==='corner'?' active':'')+'" data-action="v1422-top-shape" data-shape="corner">Угловая (L)</button>'
      +'</div>';

    if(shape==='straight'){
      body+='<div class="grid g2" style="margin-bottom:10px">'
        +'<div class="field"><label>Длина, м</label><input data-bind="top.len" value="'+e1(top.len||'')+'" type="number" inputmode="decimal"></div>'
        +'<div class="field"><label>Глубина, мм</label><input data-bind="top.depth" value="'+e1(top.depth||'')+'" type="number" inputmode="decimal"></div>'
        +'</div>';
      if(typeof stepper==='function'){
        body+='<div class="grid g2" style="margin-bottom:10px"><div>'+stepper('Вырез мойка','sinkCuts',top.sinkCuts,'top')
          +'</div><div>'+stepper('Вырез плита','hobCuts',top.hobCuts,'top')+'</div></div>';
      }
    } else {
      var la=ctr?n1(ctr.lenA):n1(top.len)||0;
      var lb=ctr?n1(ctr.lenB):0;
      var jt=ctr?ctr.jointType:'euro';
      body+='<div class="grid g2" style="margin-bottom:10px">'
        +'<div class="field"><label>Длина A, м</label><input data-action="v1422-top-lena" value="'+la+'" type="number" inputmode="decimal"></div>'
        +'<div class="field"><label>Длина B, м</label><input data-action="v1422-top-lenb" value="'+lb+'" type="number" inputmode="decimal"></div>'
        +'</div>'
        +'<div class="chip-row" style="margin-bottom:10px">'
        +'<button class="chip'+(jt==='euro'?' active':'')+'" data-action="v1422-corner" data-v="euro">Еврозапил (+54€)</button>'
        +'<button class="chip'+(jt==='miter'?' active':'')+'" data-action="v1422-corner" data-v="miter">Стык</button>'
        +'<button class="chip'+(jt==='custom'?' active':'')+'" data-action="v1422-corner" data-v="custom">Вручную</button>'
        +'</div>';
    }

    body+='<div class="chip-row">'
      +'<button class="chip'+(top.sinkType==='surface'?' active':'')+'" data-action="sinkType" data-type="surface">Мойка: накладная</button>'
      +'<button class="chip'+(top.sinkType==='under'?' active':'')+'" data-action="sinkType" data-type="under">Мойка: подстольная</button>'
      +'</div>';
  }

  var ctrIt=ctr?pbGet1(book,ctr.itemId):null;
  var summ=top.enabled?(ctrIt?e1((ctrIt.client_name||ctrIt.name).slice(0,15))+' · '+n1(top.len).toFixed(1)+' м':'нет материала'):'не нужна';
  return sec10231('3','counter','Столешница',summ,body);
}

// ── 5. Фасады — multi-position list ──────────────────────────────────
var ZONE_LABELS=['Нижние','Верхние','Пенал','Панели','Доборы','Другое'];
function buildFacades10231(){
  var book=state.priceBook||[];
  var facadeCat=book.filter(function(x){return x.category==='facade';});
  var facades=(state.order&&state.order.facades)||[];
  var lf=pbGet1(book,'labor_facade');
  var ld=pbGet1(book,'labor_door');

  var cards=facades.map(function(f){
    var area=Math.max(0,n1(f.len)*n1(f.height)/1000-n1(f.deduct||0));
    if(area<=0&&n1(f.qty)>0)area=n1(f.qty);
    var selIt=pbGet1(book,f.itemId);
    var lineTotal=(selIt?area*selIt.price:0)+(lf?area*lf.price:0)+(ld?n1(f.doors)*ld.price:0);

    // Label select
    var curLabel=f.label||'Нижние';
    var inList=ZONE_LABELS.indexOf(curLabel)>=0;
    var labelSel='<select class="v10231-fcard-label" data-action="v10231-f-label" data-fid="'+e1(f.id)+'">'
      +ZONE_LABELS.map(function(l){return'<option'+(curLabel===l?' selected':'')+'>'+e1(l)+'</option>';}).join('')
      +'<option'+((!inList&&curLabel)?' selected':'')+' value="'+e1(!inList&&curLabel?curLabel:'')+'">'
      +e1(!inList&&curLabel?curLabel:'Другое...')+'</option>'
      +'</select>';

    // Material select
    var matSel='<select class="v10231-fcard-matsel" data-action="v10231-f-mat" data-fid="'+e1(f.id)+'">'
      +'<option value="">— выберите материал —</option>'
      +facadeCat.map(function(it){
        return'<option value="'+e1(it.id)+'"'+(f.itemId===it.id?' selected':'')+'>'
          +e1((it.client_name||it.name).slice(0,30))+' · '+m1(it.price)+'/м²</option>';
      }).join('')
      +'</select>';

    // Dims
    var dims='<div class="v10231-fcard-dims">'
      +'<div class="field"><label>Длина, м</label>'
      +'<input type="number" inputmode="decimal" data-action="v10231-f-len" data-fid="'+e1(f.id)+'" value="'+e1(f.len>0?f.len:'')+'" placeholder="0.00"></div>'
      +'<div class="field"><label>Высота, мм</label>'
      +'<input type="number" inputmode="decimal" data-action="v10231-f-h" data-fid="'+e1(f.id)+'" value="'+e1(f.height>0?f.height:'')+'" placeholder="2000"></div>'
      +'</div>';

    // Steppers
    var ctrlRow='<div class="v10231-fcard-ctrls">'
      +'<div style="display:flex;align-items:center;gap:6px">'
      +'<span style="font-size:12px;color:var(--muted,var(--ink-muted))">Двери</span>'
      +'<div class="v1423-stepper">'
      +'<button data-action="v10231-f-door-minus" data-fid="'+e1(f.id)+'">&#8722;</button>'
      +'<span class="v1423-qty">'+n1(f.doors)+'</span>'
      +'<button data-action="v10231-f-door-plus" data-fid="'+e1(f.id)+'">+</button>'
      +'</div></div>'
      +'<div style="display:flex;align-items:center;gap:6px">'
      +'<span style="font-size:12px;color:var(--muted,var(--ink-muted))">Ящики</span>'
      +'<div class="v1423-stepper">'
      +'<button data-action="v10231-f-drw-minus" data-fid="'+e1(f.id)+'">&#8722;</button>'
      +'<span class="v1423-qty">'+n1(f.drawers)+'</span>'
      +'<button data-action="v10231-f-drw-plus" data-fid="'+e1(f.id)+'">+</button>'
      +'</div></div>'
      +'</div>';

    var sub='<div class="v10231-fcard-sub">'
      +area.toFixed(2)+' м²'+(selIt?' · '+e1((selIt.client_name||selIt.name).slice(0,18)):'')
      +(lineTotal>0?' = <b>'+m1(lineTotal)+'</b>':'')
      +'</div>';

    return'<div class="v10231-fcard">'
      +'<div class="v10231-fcard-head">'+labelSel
      +'<button class="v10231-fcard-remove" data-action="v10231-f-remove" data-fid="'+e1(f.id)+'" title="Убрать позицию">&#215;</button>'
      +'</div>'
      +matSel+dims+ctrlRow+sub
      +'</div>';
  }).join('');

  if(!facades.length)
    cards='<div class="v1423-row-empty">Нажмите «+ Добавить фасад» чтобы добавить первую позицию.</div>';

  // Summary
  var totalArea=fArea1();
  var totalSell=facades.reduce(function(a,f){
    if(f.included===false)return a;
    var area=Math.max(0,n1(f.len)*n1(f.height)/1000-n1(f.deduct||0));
    if(area<=0&&n1(f.qty)>0)area=n1(f.qty);
    var it=pbGet1(book,f.itemId);
    return a+(it?area*it.price:0)+(lf?area*lf.price:0)+(ld?n1(f.doors)*ld.price:0);
  },0);
  var summ=facades.length
    ?(facades.length+' поз. · '+totalArea.toFixed(1)+' м²'+(totalSell>0?' · '+m1(totalSell):''))
    :'не добавлены';

  return sec10231('2','facades','Фасады',summ,
    cards+'<button class="v1423-add-btn" data-action="v10231-f-add">&#65291; Добавить фасад</button>');
}

// ── 6. Фурнитура (hardware + ex-улучшения + рекомендации) ─────────────
function buildHardware10231(){
  var book=state.priceBook||[];
  var order=state.order||{};
  var hw=state.hardware||{};
  var hMode=hw.handlesMode||'we';

  var handleHtml='<div style="margin-bottom:12px">'
    +'<div style="font-size:12px;font-weight:600;color:var(--muted,var(--ink-muted));margin-bottom:6px">Ручки</div>'
    +'<div class="chip-row">'
    +'<button class="chip'+(hMode==='client'?' active':'')+'" data-action="setHandleMode" data-mode="client">Клиент покупает</button>'
    +'<button class="chip'+(hMode==='we'?' active':'')+'" data-action="setHandleMode" data-mode="we">Мы подберём</button>'
    +'<button class="chip'+(hMode==='later'?' active':'')+'" data-action="setHandleMode" data-mode="later">Позже</button>'
    +'</div></div>';

  var rows=(order.hardware||[]).map(function(h){
    var it=pbGet1(book,h.itemId);if(!it)return'';
    var fits=getFits(it);
    var isLed=fits.unit==='led';
    var isHinge=fits.unit==='hinge';
    var isDrawer=fits.unit==='drawer';
    var isMdfA=fits.unit==='mdfArea';
    var isDynamic=isHinge||isDrawer||isMdfA;

    var qty;
    if(isLed)         qty=n1((h.config||{}).meters)||0;
    else if(isHinge)  qty=fHinges1();
    else if(isDrawer) qty=fDrawers1();
    else if(isMdfA)   qty=fArea1();
    else qty=h.qtyOverride!=null?n1(h.qtyOverride):n1(h.qtyAuto);

    var isOverride=!isDynamic&&!isLed&&h.qtyOverride!=null;
    var price=it.price;
    var lineTotal=qty*price;
    var priceStr=price>0?(qty>0?m1(lineTotal):'&#8212;'):'<span class="v1423-honest">уточнить цену</span>';

    // qty control
    var qtyHtml='';
    if(isLed){
      qtyHtml='<div style="display:flex;align-items:center;gap:4px">'
        +'<input type="number" inputmode="decimal" style="width:58px;padding:4px 6px;font-size:12px;border:1px solid var(--divider,rgba(0,0,0,.12));border-radius:6px;background:var(--card-bg,var(--surface));color:var(--txt,var(--ink))"'
        +' data-action="v10231-hw-led-m" data-hid="'+e1(h.id)+'" value="'+e1((h.config||{}).meters||'')+'" placeholder="м">'
        +'<span style="font-size:11px;color:var(--muted,var(--ink-muted))">м</span></div>';
    } else {
      qtyHtml='<div class="v1423-stepper">'
        +'<button data-action="v10231-hw-minus" data-hid="'+e1(h.id)+'">&#8722;</button>'
        +'<span class="v1423-qty">'+qty+'</span>'
        +'<button data-action="v10231-hw-plus" data-hid="'+e1(h.id)+'">+</button>'
        +(isOverride?'<button data-action="v10231-hw-reset" data-hid="'+e1(h.id)+'" title="Сбросить к авто" style="font-size:10px;width:auto;padding:0 6px">&#8635;</button>':'')
        +'</div>'+(isDynamic||isOverride?'':'<span class="v1423-auto-badge">авто</span>');
    }

    var recBtn='<button class="v10231-rec-flag'+(h.recommend?' on':'')+'" data-action="v10231-rec" data-hid="'+e1(h.id)+'" title="Рекомендовать клиенту">&#9733; рек.</button>';

    return'<div class="v1423-row">'
      +'<div style="flex:1"><div class="v1423-row-name">'+e1(it.client_name||it.name)+'</div>'
      +(price>0?'<div class="v1423-row-sub">'+m1(price)+' / '+e1(it.unit)+'</div>':'')+'</div>'
      +qtyHtml+recBtn
      +'<button class="v1423-toggle'+(h.included?' on':'')+'" data-action="v10231-hw-incl" data-hid="'+e1(h.id)+'">'+(h.included?'Включ':'Выкл')+'</button>'
      +'<div class="v1423-row-price">'+(h.included?priceStr:'<span style="color:var(--muted,var(--ink-muted))">откл.</span>')+'</div>'
      +'</div>';
  }).join('');

  var inclTotal=(order.hardware||[]).reduce(function(a,h){
    if(!h.included)return a;
    var it=pbGet1(book,h.itemId);if(!it)return a;
    var fits=getFits(it);
    var qty;
    if(fits.unit==='led')         qty=n1((h.config||{}).meters)||0;
    else if(fits.unit==='hinge')  qty=fHinges1();
    else if(fits.unit==='drawer') qty=fDrawers1();
    else if(fits.unit==='mdfArea')qty=fArea1();
    else qty=h.qtyOverride!=null?n1(h.qtyOverride):n1(h.qtyAuto);
    return a+qty*it.price;
  },0);

  var summ=inclTotal>0?m1(inclTotal)+' в расчёте':'не включена';
  return sec10231('5','hardware','Фурнитура',summ,handleHtml+(rows||'<div class="v1423-row-empty">Фурнитура не добавлена.</div>'));
}

// ── 7. Услуги (работа only, с флагом рекомендации) ──────────────────
function buildServices10231(){
  var book=state.priceBook||[];
  var order=state.order||{};

  var rows=(order.services||[]).map(function(s){
    var it=pbGet1(book,s.itemId);if(!it)return'';
    var qty=n1(s.qty)||1;
    var price=it.price;
    var lineStr=price>0
      ?(s.enabled?m1(qty*price)+'<small style="font-size:10px;color:var(--muted,var(--ink-muted))"> ('+m1(price)+'/'+e1(it.unit)+')</small>'
        :'<span style="color:var(--muted,var(--ink-muted))">'+m1(price)+'/'+e1(it.unit)+'</span>')
      :'<span class="v1423-honest">уточнить цену</span>';
    var recBtn='<button class="v10231-rec-flag'+(s.recommend?' on':'')+'" data-action="v10231-svc-rec" data-sid="'+e1(s.id)+'" title="Рекомендовать клиенту">&#9733; рек.</button>';
    return'<div class="v1423-row">'
      +'<button class="v1423-toggle'+(s.enabled?' on':'')+'" data-action="v10231-svc-tog" data-sid="'+e1(s.id)+'">'+(s.enabled?'ВКЛ':'ВЫКЛ')+'</button>'
      +'<div class="v1423-row-name">'+e1(it.client_name||it.name)+'</div>'
      +(s.enabled&&price>0?('<div class="v1423-stepper">'
        +'<button data-action="v10231-svc-minus" data-sid="'+e1(s.id)+'">&#8722;</button>'
        +'<span class="v1423-qty">'+qty+'</span>'
        +'<button data-action="v10231-svc-plus" data-sid="'+e1(s.id)+'">+</button>'
        +'</div>'):'')
      +recBtn
      +'<div class="v1423-row-price">'+lineStr+'</div>'
      +'</div>';
  }).join('');

  var addBtn='<button class="v1423-add-btn" data-action="v10231-svc-add">&#65291; Добавить услугу</button>';
  var onCount=(order.services||[]).filter(function(s){return s.enabled;}).length;
  var summ=onCount?onCount+' вкл.':'не выбраны';
  return sec10231('6','services','Услуги',summ,rows+addBtn);
}

// ── 8. Материалы (BOM + доп. плиты) ─────────────────────────────────
function buildMaterials10231(){
  var book=state.priceBook||[];
  var order=state.order||{};
  var lf=pbGet1(book,'labor_facade');
  var ld=pbGet1(book,'labor_door');
  var rows='';

  (order.facades||[]).forEach(function(f){
    if(f.included===false)return;
    var area=Math.max(0,n1(f.len)*n1(f.height)/1000-n1(f.deduct||0));
    if(area<=0&&n1(f.qty)>0)area=n1(f.qty);
    if(area<=0)return;
    var it=pbGet1(book,f.itemId);
    rows+='<div class="v1423-bom-row"><span><b>'+e1(f.label||f.zoneName||'Зона')+'</b> · '
      +(it?e1(it.name):'—')+'</span><span>'+area.toFixed(2)+' м² × '+m1(it?it.price:0)+'</span></div>';
  });
  var ta=fArea1(),td=fDoors1();
  if(lf&&ta>0)rows+='<div class="v1423-bom-row"><span><b>Работа</b> · фасады</span><span>'+ta.toFixed(2)+' м² × '+m1(lf.price)+'</span></div>';
  if(ld&&td>0)rows+='<div class="v1423-bom-row"><span><b>Работа</b> · двери</span><span>'+td+' шт × '+m1(ld.price)+'</span></div>';

  (order.counter||[]).forEach(function(c){
    if(!c.enabled)return;
    var it=pbGet1(book,c.itemId);
    var len=c.shape==='corner'?(n1(c.lenA)+n1(c.lenB)):n1(c.len);
    if(it&&len>0)rows+='<div class="v1423-bom-row"><span><b>Столешница</b> · '+e1(it.client_name||it.name)+'</span><span>'+len.toFixed(2)+' м × '+m1(it.price)+'</span></div>';
  });

  // Extra material items
  var extraItems=(order.materials||[]).filter(function(m){
    return pbGet1(book,m.itemId);
  });
  if(extraItems.length){
    rows+='<div style="margin-top:8px;margin-bottom:4px;font-size:11px;font-weight:600;color:var(--muted,var(--ink-muted))">Доп. материалы:</div>';
    extraItems.forEach(function(m){
      var it=pbGet1(book,m.itemId);if(!it)return;
      rows+='<div class="v1423-row">'
        +'<button class="v1423-toggle'+(m.included?' on':'')+'" data-action="v10231-mat-tog" data-mid="'+e1(m.id)+'">'+(m.included?'ВКЛ':'ВЫКЛ')+'</button>'
        +'<div class="v1423-row-name">'+e1(it.client_name||it.name)+'</div>'
        +'<div class="v1423-row-price">'+(m.included&&it.price>0?m1(n1(m.qty)*it.price):'&#8212;')+'</div>'
        +'</div>';
    });
  }

  if(!rows)rows='<div class="v1423-row-empty">Добавьте позиции фасадов и столешницы.</div>';
  var summ=ta>0?ta.toFixed(1)+' м² фасады':'заполните позиции';
  return sec10231('4','materials','Материалы',summ,rows);
}

// ── 9. Auto-count refresh ─────────────────────────────────────────────
function refreshHwAuto10231(){
  if(!state.order)return;
  var td=fDoors1(),tdr=fDrawers1(),th=fHinges1(),ta=fArea1();
  var hwMode=(state.hardware||{}).handlesMode||'we';
  var book=state.priceBook||[];
  (state.order.hardware||[]).forEach(function(h){
    if(h.itemId==='hw_hinges')  h.qtyAuto=th;
    if(h.itemId==='hw_runners') h.qtyAuto=tdr;
    if(h.itemId==='hw_handles') h.qtyAuto=hwMode==='client'?0:td+tdr;
    var it=pbGet1(book,h.itemId);
    if(it){
      var fits=getFits(it);
      if(fits.unit==='hinge')  h.qtyAuto=th;
      if(fits.unit==='drawer') h.qtyAuto=tdr;
      if(fits.unit==='mdfArea')h.qtyAuto=ta;
    }
  });
}

// ── 10. Main render (6 sections) ──────────────────────────────────────
function renderOrder10231(){
  migrateToOrder10231();
  refreshHwAuto10231();
  var t=orderTotals10231()||{totalClient:0,margin:0};
  var p=state.project||{};
  var hdr='<div class="v1423-hdr">'
    +'<div class="v1423-hdr-left">'
    +'<div class="v1423-hdr-name">'+e1(p.client||'Новый проект')+'</div>'
    +'<div class="v1423-hdr-sub">'+e1(p.status||'')+(p.want?' · '+e1(p.want):'')+'</div>'
    +'</div>'
    +'<div class="v1423-hdr-total"><b>'+m1(t.totalClient)+'</b>'
    +'<small>'+Math.round(t.margin||0)+'% маржа</small>'
    +'</div></div>';
  return'<div class="v1423-view">'
    +hdr
    +buildPassport10231()
    +buildFacades10231()
    +buildCounter10231()
    +buildMaterials10231()
    +buildHardware10231()
    +buildServices10231()
    +'</div>';
}

// ── 11. Override renderFast + totals ──────────────────────────────────
window.renderFast=function(){
  var pane=document.getElementById('pane-fast');
  if(pane)pane.innerHTML=renderOrder10231();
};
var _orig10231=window.totals;
window.totals=function(){
  if(state&&state.order&&Array.isArray(state.priceBook)&&state.priceBook.length){
    var r=orderTotals10231();if(r)return r;
  }
  return _orig10231?_orig10231():{base:{sell:0,cost:0},improvements:{sell:0,cost:0},totalClient:0,totalCost:0,profit:0,margin:0,paid:0,remaining:0};
};

// ── 12. Click handler ─────────────────────────────────────────────────
document.addEventListener('click',function(ev){
  var b=ev.target.closest('[data-action]');if(!b)return;
  var a=b.dataset.action;
  if(!a||a.indexOf('v10231-')<0)return;
  ev.preventDefault();ev.stopImmediatePropagation();
  migrateToOrder10231();
  state.accOpen10231=state.accOpen10231||{};
  var order=state.order;

  if(a==='v10231-acc'){
    var id=b.dataset.id;
    state.accOpen10231[id]=!state.accOpen10231[id];
  }
  // Facades
  else if(a==='v10231-f-add'){
    var lbl=ZONE_LABELS[(order.facades||[]).length%ZONE_LABELS.length]||'Нижние';
    (order.facades=order.facades||[]).push({
      id:uid1('f'),label:lbl,itemId:null,len:0,height:2000,doors:0,drawers:0,deduct:0,included:true});
  }
  else if(a==='v10231-f-remove'){
    order.facades=(order.facades||[]).filter(function(f){return f.id!==b.dataset.fid;});
  }
  else if(a==='v10231-f-door-plus'){
    var f=order.facades.find(function(x){return x.id===b.dataset.fid;});
    if(f)f.doors=n1(f.doors)+1;
  }
  else if(a==='v10231-f-door-minus'){
    var f=order.facades.find(function(x){return x.id===b.dataset.fid;});
    if(f)f.doors=Math.max(0,n1(f.doors)-1);
  }
  else if(a==='v10231-f-drw-plus'){
    var f=order.facades.find(function(x){return x.id===b.dataset.fid;});
    if(f)f.drawers=n1(f.drawers)+1;
  }
  else if(a==='v10231-f-drw-minus'){
    var f=order.facades.find(function(x){return x.id===b.dataset.fid;});
    if(f)f.drawers=Math.max(0,n1(f.drawers)-1);
  }
  // Hardware
  else if(a==='v10231-hw-plus'){
    var h=order.hardware.find(function(x){return x.id===b.dataset.hid;});
    if(h)h.qtyOverride=(h.qtyOverride!=null?n1(h.qtyOverride):n1(h.qtyAuto))+1;
  }
  else if(a==='v10231-hw-minus'){
    var h=order.hardware.find(function(x){return x.id===b.dataset.hid;});
    if(h){var nq=(h.qtyOverride!=null?n1(h.qtyOverride):n1(h.qtyAuto))-1;h.qtyOverride=Math.max(0,nq);}
  }
  else if(a==='v10231-hw-reset'){
    var h=order.hardware.find(function(x){return x.id===b.dataset.hid;});
    if(h)h.qtyOverride=null;
  }
  else if(a==='v10231-hw-incl'){
    var h=order.hardware.find(function(x){return x.id===b.dataset.hid;});
    if(h)h.included=!h.included;
  }
  else if(a==='v10231-rec'){
    var h=order.hardware.find(function(x){return x.id===b.dataset.hid;});
    if(h)h.recommend=!h.recommend;
  }
  // Services
  else if(a==='v10231-svc-tog'){
    var s=order.services.find(function(x){return x.id===b.dataset.sid;});
    if(s){s.enabled=!s.enabled;if(s.enabled&&!s.qty)s.qty=1;}
  }
  else if(a==='v10231-svc-plus'){
    var s=order.services.find(function(x){return x.id===b.dataset.sid;});
    if(s)s.qty=(n1(s.qty)||1)+1;
  }
  else if(a==='v10231-svc-minus'){
    var s=order.services.find(function(x){return x.id===b.dataset.sid;});
    if(s)s.qty=Math.max(1,(n1(s.qty)||1)-1);
  }
  else if(a==='v10231-svc-rec'){
    var s=order.services.find(function(x){return x.id===b.dataset.sid;});
    if(s)s.recommend=!s.recommend;
  }
  else if(a==='v10231-svc-add'){
    var nm=prompt('Название услуги:','');
    if(nm){
      var pr=n1(prompt('Цена €:','0'));
      var cid='custom_'+uid1('s');
      state.priceBook.push({id:cid,name:nm,client_name:nm,category:'service',
        unit:'усл.',price:pr,cost:0,supplier:'',art:'',fits:'',hint:''});
      (order.services=order.services||[]).push({id:uid1('svc'),itemId:cid,enabled:true,qty:1,recommend:false});
    }
  }
  // Materials
  else if(a==='v10231-mat-tog'){
    var m=(order.materials||[]).find(function(x){return x.id===b.dataset.mid;});
    if(m)m.included=!m.included;
  }

  if(typeof markDirty==='function')markDirty();
  if(typeof renderCurrent==='function')renderCurrent();
},true);

// ── 13. Input handler ─────────────────────────────────────────────────
document.addEventListener('input',function(ev){
  var x=ev.target;var a=x.dataset.action;
  if(!a||a.indexOf('v10231-')<0)return;
  ev.stopImmediatePropagation();
  migrateToOrder10231();
  var order=state.order;

  if(a==='v10231-f-len'){
    var f=(order.facades||[]).find(function(f2){return f2.id===x.dataset.fid;});
    if(f)f.len=n1(x.value);
  } else if(a==='v10231-f-h'){
    var f=(order.facades||[]).find(function(f2){return f2.id===x.dataset.fid;});
    if(f)f.height=n1(x.value)||2000;
  } else if(a==='v10231-f-mat'){
    var f=(order.facades||[]).find(function(f2){return f2.id===x.dataset.fid;});
    if(f)f.itemId=x.value||null;
  } else if(a==='v10231-f-label'){
    var f=(order.facades||[]).find(function(f2){return f2.id===x.dataset.fid;});
    if(f&&x.value&&x.value!=='')f.label=x.value;
  } else if(a==='v10231-hw-led-m'){
    var h=(order.hardware||[]).find(function(h2){return h2.id===x.dataset.hid;});
    if(h){h.config=h.config||{};h.config.meters=n1(x.value);}
  }

  if(typeof markDirty==='function')markDirty();
  if(typeof renderCurrent==='function')renderCurrent();
},true);

// ── 14. Init ──────────────────────────────────────────────────────────
(function(){
  try{
    if(typeof ensureV1414==='function')ensureV1414();
    if(typeof ensureV1043State==='function')ensureV1043State();
    migrateToOrder10231();
  }catch(err){console.error('[v10231] init:',err);}
})();

window.__v10231={V:V10231,fixPriceBook10231:fixPriceBook10231,migrateToOrder10231:migrateToOrder10231,
  orderTotals10231:orderTotals10231,renderOrder10231:renderOrder10231};
console.info('[v10.4.23.1] Model Fix loaded');
})();
</script>
"""

def build():
    src=os.path.join(DIR,BASE)
    out=os.path.join(DIR,OUT)
    with open(src,'r',encoding='utf-8') as f:
        html=f.read()
    if html.count('</body>')!=1:
        print('ERROR: expected 1 </body>'); sys.exit(1)
    result=html.replace('</body>',LAYER+'\n</body>',1)
    with open(out,'w',encoding='utf-8') as f:
        f.write(result)
    print(f'Built: {OUT}')
    print(f'Lines: {result.count(chr(10))+1}')
    print(f'Chars: {len(result)}')
    return result

def gate(html):
    checks=[
        ('MAIN_KEY intact',              'anbamo_v10_4_6_mvp_stabilization'),
        ('v10231 version marker',        'v10.4.23.1 Model Fix'),
        ('fixPriceBook10231',            'fixPriceBook10231'),
        ('migrateToOrder10231',          'migrateToOrder10231'),
        ('orderTotals10231',             'orderTotals10231'),
        ('renderOrder10231',             'renderOrder10231'),
        ('buildPassport10231',            'buildPassport10231'),
        ('buildCounter10231',             'buildCounter10231'),
        ('6-section render (no sect 7)', 'buildFacades10231'),
        ('buildHardware10231',           'buildHardware10231'),
        ('buildServices10231',           'buildServices10231'),
        ('buildMaterials10231',          'buildMaterials10231'),
        ('_v10231migrated flag',         '_v10231migrated'),
        ('Legs-to-hw (LEGS_IDS)',          'LEGS_IDS'),
        ('MAT_IDS plinth/cornice',       'MAT_IDS'),
        ('recommend flag hw',            'v10231-rec'),
        ('recommend flag svc',           'v10231-svc-rec'),
        ('facade add button',            'v10231-f-add'),
        ('facade remove button',         'v10231-f-remove'),
        ('facade mat select',            'v10231-f-mat'),
        ('facade len input',             'v10231-f-len'),
        ('facade height input',          'v10231-f-h'),
        ('LED meters input',             'v10231-hw-led-m'),
        ('window.__v10231',              'window.__v10231'),
        ('window.__v1423 intact',        'window.__v1423'),
        ('window.__v1422 intact',        'window.__v1422'),
        ('window.__v10472 intact',       'window.__v10472'),
        ('single </body>',               None),
    ]
    errors=[]
    print('\n=== GATE CHECKS ===')
    for label,needle in checks:
        if needle is None:
            c=html.count('</body>')
            if c!=1: errors.append(f'[FAIL] {label}: got {c}')
            else: print(f'  [PASS] {label}')
        elif needle in html:
            print(f'  [PASS] {label}'.encode('ascii','replace').decode())
        else:
            errors.append(f'[FAIL] {label}: "{needle}" not found')
    print()
    if errors:
        for e in errors: print(e.encode('ascii','replace').decode())
        sys.exit(1)
    print('All gates PASS')

if __name__=='__main__':
    html=build()
    gate(html)
