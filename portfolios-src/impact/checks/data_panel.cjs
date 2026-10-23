// The checks of the skill phyein-usul-data-panel, section 6, on the built study. From dist/: python3 -m http.server 8766, then
// NODE_PATH=$(npm root -g) node portfolios-src/impact/checks/data_panel.cjs index.html 1100 <outdir>  (also ar.html, other widths).
// Writes <page>-<width>.json, screenshots and the saved archive into <outdir>.
const { chromium } = require('playwright');
const fs=require('fs');
(async()=>{
 const page=process.argv[2]||'index.html',w=+(process.argv[3]||1100),out=process.argv[4]||'.';
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'});
 const ctx=await b.newContext({viewport:{width:w,height:1000},acceptDownloads:true});
 const p=await ctx.newPage();const errs=[];
 p.on('pageerror',e=>errs.push('pageerror '+e.message));p.on('console',m=>{if(m.type()==='error')errs.push('console '+m.text())});
 await p.goto('http://localhost:8766/portfolios/impact/'+page,{timeout:180000,waitUntil:'domcontentloaded'});
 await p.waitForFunction(()=>typeof ds!=='undefined'&&ds.get('done'),null,{timeout:300000});
 const R={page,w};
 // 1-2: panel present; every variable in a group with its attributes
 R.vars=await p.evaluate(()=>{const inG=new Set(Sim.data.groups.flatMap(g=>g.vars));const miss=[],noattr=[];
   for(const n of ds.order){if(!inG.has(n))miss.push(n);const a=ds.vars[n].attrs;if(!a.symbol||!a.long_name||!a.computed_in||a.digits===undefined)noattr.push(n)}
   const unitless=ds.order.filter(n=>!ds.vars[n].attrs.units);
   return {n:ds.order.length,groups:Sim.data.groups.length,notInGroup:miss,missingAttrs:noattr,unitless:unitless.length,ledgerRows:document.querySelectorAll('.dp-item').length,tab:!!document.querySelector('.dp-tab')}});
 // 3: every check, scalars and sampled indices of every array, with the panel's own agreement rule
 R.check=await p.evaluate(()=>{
   function agree(st,v,dt){if(typeof st!=='number'||typeof v!=='number')return String(st)===String(v)?'identical':'DIFFER '+st+' / '+v;
     if(!isFinite(st)||!isFinite(v))return String(st)===String(v)?'both undefined':'DIFFER one undefined '+st+' / '+v;
     const d=Math.abs(st-v),s=Math.max(Math.abs(st),Math.abs(v),1e-300),tol=(dt==='float32'?2e-6:1e-9)*Math.max(s,1e-12)+(dt==='float32'?1e-7:1e-12);
     return d===0?'identical':d<=tol?'agree '+Math.floor(-Math.log10(d/s))+' figs':'DIFFER by '+d.toExponential(2)}
   const res={},count={identical:0,agree:0,undefined:0,differ:0,nocheck:[]};const t0=performance.now();
   for(const n of ds.order){const v=ds.vars[n],f=Sim.data.check[n];if(!f){count.nocheck.push(n);continue}
     const len=v.dims.length?v.data.length:0,rows=v.dims.length?ds.dims[v.dims[0]]:0,cols=v.dims.length>1?ds.dims[v.dims[1]]:1;
     let idx=[null];if(len){const pick=[0,1,Math.floor(rows*0.159),Math.floor(rows*0.25),Math.floor(rows/2),rows-1];idx=[...new Set(pick)].map(r=>r*cols+(cols>1?(r*37)%cols:0));
       if(/^ck_/.test(n))idx=idx.filter(i=>Math.floor(i/cols)<=3||Math.floor(i/cols)===rows-1)}
     for(const i of idx){let x;try{x=f(i)}catch(e){res[n+'['+i+']']='THROW '+e.message;count.differ++;continue}
       const st=len?v.data[i]:v.data,a=agree(st,x.value,ds.dtype(n));res[n+(len?'['+i+']':'')]=a;
       if(a==='identical')count.identical++;else if(a.startsWith('agree'))count.agree++;else if(a.startsWith('both'))count.undefined++;else count.differ++}}
   count.ms=Math.round(performance.now()-t0);
   return {count,differ:Object.entries(res).filter(([k,v])=>/DIFF|THROW/.test(v)),agreeing:Object.entries(res).filter(([k,v])=>v.startsWith('agree')).slice(0,12),undef:Object.entries(res).filter(([k,v])=>v.startsWith('both'))}});
console.log('VARS',JSON.stringify(R.vars));console.log('CHECK',JSON.stringify(R.check));
 // 4: read-back at a moment in the impact (playback paused there) and at the end
 async function drawnAll(tag){return p.evaluate(tag=>{const out={},n=ds.get('i_now');
   for(const name in Sim.data.drawn){const v=ds.vars[name];let idx=null;
     if(v.dims.length===2){const N=ds.dims[v.dims[1]];idx=n*N+7}else if(v.dims.length===1)idx=n;
     const r=Sim.data.drawn[name](idx);out[name]=(r.ok===true?'ok':r.ok===null?'null':'FAIL')+' · '+r.drawn+' · expected '+r.expected}
   const late=Sim.data.drawn.F_iron(Math.max(0,n-300));out['F_iron[n-300]']=(late.ok===true?'ok':late.ok===null?'null':'FAIL')+' · '+late.drawn;
   const latec=Sim.data.drawn.F_cot(Math.max(0,n-300));out['F_cot[n-300]']=(latec.ok===true?'ok':latec.ok===null?'null':'FAIL')+' · '+latec.drawn;
   return {tag,n,t:ds.get('t_now'),out}},tag)}
 await p.evaluate(()=>{setSpeed(20);startDrop()});
 await p.waitForFunction(()=>tPlay>1.452,null,{timeout:60000});await p.evaluate(()=>{playing=false});await p.waitForTimeout(150);
 R.drawnImpact=await drawnAll('impact');console.log('DRAWN',JSON.stringify(R.drawnImpact));
 // 5: Read values. Sweep with Read off, then on; overlay pixels painted
 const st=await p.$('#stage'),bb=await st.boundingBox();
 const overlayPix=()=>p.evaluate(()=>{const o=document.querySelector('.dp-overlay');const d=o.getContext('2d').getImageData(0,0,o.width,o.height).data;let c=0;for(let i=3;i<d.length;i+=4)if(d[i])c++;return c});
 async function sweep(){await st.scrollIntoViewIfNeeded();const bb=await st.boundingBox();for(let q=0;q<=40;q++){await p.mouse.move(bb.x+bb.width*(0.1+0.8*q/40),bb.y+bb.height*(0.2+0.5*q/40));await p.waitForTimeout(16)}}
 await p.evaluate(()=>{playing=true;setSpeed(20)});
 await sweep();R.sweepOff=await overlayPix();
 await p.evaluate(()=>document.querySelector('.dp-readbtn').click());await sweep();R.sweepOn=await overlayPix();R.runningReadNoPin=await p.evaluate(()=>__dataPanel.running());
 // pin an iron atom: from the stored positions at the shown sample
 await p.evaluate(()=>{playing=false;tPlay=1.2});await p.waitForTimeout(100);
 const at=await p.evaluate(()=>partXY('iron',ds.get('i_now'),45));
 {await st.scrollIntoViewIfNeeded();const b2=await st.boundingBox();await p.mouse.click(b2.x+at.x,b2.y+at.y);}await p.waitForTimeout(400);
 R.pinIron=await p.evaluate(()=>({title:document.querySelector('.dp-read__title').textContent,vals:[...document.querySelectorAll('.dp-read__v')].map(e=>e.textContent)}));
 const sb=await (await p.$('.dp-read')).boundingBox(),b3=await st.boundingBox();R.stripBelow={stripTop:sb.y,figureBottom:b3.y+b3.height,overlap:sb.y<b3.y+b3.height-0.5};
 R.overlayPinned=await overlayPix();R.overlayFrac=R.overlayPinned/await p.evaluate(()=>{const o=document.querySelector('.dp-overlay');return o.width*o.height});
 // values rewritten at most ~4/s while running
 await p.evaluate(()=>{setSpeed(4);playing=true});
 const changes=await p.evaluate(()=>new Promise(res=>{const el=document.querySelector('.dp-read__vals');let c=0;const mo=new MutationObserver(()=>c++);mo.observe(el,{subtree:true,characterData:true,childList:true});
   const t0=performance.now();let last='';let batches=0;function tick(){const s=el.textContent;if(s!==last){batches++;last=s}if(performance.now()-t0<3000)requestAnimationFrame(tick);else{mo.disconnect();res({batches,perSecond:batches/3})}}tick()}));
 R.stripRate=changes;
 await p.screenshot({path:out+'/'+page+'-'+w+'-pinned-atom.png'});
 // pin a cotton bead and a scale
 await p.evaluate(()=>{playing=false;tPlay=1.7});await p.waitForTimeout(100);
 const atc=await p.evaluate(()=>partXY('cot',ds.get('i_now'),300));{const b2=await st.boundingBox();await p.mouse.click(b2.x+atc.x,b2.y+atc.y);}await p.waitForTimeout(400);
 R.pinCot=await p.evaluate(()=>({title:document.querySelector('.dp-read__title').textContent,vals:[...document.querySelectorAll('.dp-read__v')].map(e=>e.textContent)}));
 await p.screenshot({path:out+'/'+page+'-'+w+'-pinned-bead.png'});
 const gs=await p.evaluate(()=>({x:ds.get('bx_cot'),y:ds.get('gauge_cy')}));{const b2=await st.boundingBox();await p.mouse.click(b2.x+gs.x,b2.y+gs.y);}await p.waitForTimeout(400);
 R.pinScale=await p.evaluate(()=>({title:document.querySelector('.dp-read__title').textContent,vals:[...document.querySelectorAll('.dp-read__v')].map(e=>e.textContent)}));
 await p.screenshot({path:out+'/'+page+'-'+w+'-pinned-scale.png'});
 // a Check through the panel's own interface, from the strip: the scale reading F
 await p.click('.dp-read__v[data-check="F_now_cot"]');await p.waitForTimeout(500);
 R.uiCheckF=await p.evaluate(()=>document.querySelector('.dp-check__body')?.innerText.replace(/\s+/g,' ').slice(0,900));
 await p.screenshot({path:out+'/'+page+'-'+w+'-check-F.png'});
 const pane=await p.$('#data-panel');if(pane)await pane.screenshot({path:out+'/'+page+'-'+w+'-panel-check-F.png'});
 await p.evaluate(()=>document.querySelector('.dp-readbtn').click());   // Read off (the open panel covers the switch)
 // 6: record one round (one drop), at real speed
 await p.evaluate(()=>{setSpeed(1);playing=false;tPlay=P.tmax});
 await p.evaluate(()=>document.querySelector('[data-rec]').click());
 await p.waitForFunction(()=>__dataPanel.rounds().length>0,null,{timeout:60000});
 R.round=await p.evaluate(()=>{const r=__dataPanel.rounds()[0];return {n:r.n,frames:r.frames,len:r.len,el:r.el,series:r.series.map(s=>s.key),first:r.series[0].data[0],last:r.series[0].data[r.series[0].data.length-1],charts:document.querySelectorAll('.dp-rounds canvas').length,pointNaN:r.series.filter(s=>s.point).map(s=>s.key+':'+Array.from(s.data).filter(v=>v!==v).length+'/'+s.data.length)}});
 await p.waitForTimeout(300);if(pane)await pane.screenshot({path:out+'/'+page+'-'+w+'-panel-round.png'});
 const [dl]=await Promise.all([p.waitForEvent('download'),p.evaluate(()=>document.querySelector('[data-save]').click())]);await dl.saveAs(out+'/'+page+'-'+w+'-store.zip');
 // 7: idle
 await p.evaluate(()=>{document.querySelector('.dp__close').click()});await p.waitForTimeout(300);
 R.idleRunning=await p.evaluate(()=>__dataPanel.running());
 R.layout=await p.evaluate(()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth}));
 R.errors=errs;
 fs.writeFileSync(out+'/'+page+'-'+w+'.json',JSON.stringify(R,null,1));console.log(JSON.stringify(R,null,1).slice(0,6000));
 await b.close();})();
