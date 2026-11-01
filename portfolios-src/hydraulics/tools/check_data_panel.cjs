// Data-panel checks (skill phyein-usul-data-panel, section 6) inside the study's frames. With the built site served on port 8767:
// NODE_PATH=$(npm root -g) node tools/check_data_panel.cjs ideal|servo <width> <outdir>  (Read values, pins, a Check, one round, Save, idle).
const { chromium } = require('playwright');const fs=require('fs');
(async()=>{
 const tab=process.argv[2],w=+process.argv[3],out=process.argv[4]||'.';
 const b=await chromium.launch();
 const ctx=await b.newContext({viewport:{width:w,height:1000},acceptDownloads:true});const p=await ctx.newPage();const errs=[];
 p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
 await p.goto('http://localhost:8767/portfolios/hydraulics/index.html#'+tab,{timeout:120000});await p.waitForTimeout(3000);
 let fr=null;for(const x of p.frames()){const t=await x.evaluate(()=>document.title).catch(()=>null);if(t&&(tab==='ideal'?/Ideal/.test(t):/servo/i.test(t))){fr=x;break}}
 await fr.waitForFunction(()=>window.Sim&&Sim.data&&Sim.data.ds.get(Sim.data.ds.has('r_tEnd')?'r_tEnd':'r_tEnd')>0,null,{timeout:180000});
 const R={tab,w};
 const fe=await fr.frameElement();const fb=await fe.boundingBox();
 const st=await fr.$('#stage');
 const box=async()=>{await st.scrollIntoViewIfNeeded();const s=await st.boundingBox();return s};
 const pix=()=>fr.evaluate(()=>{const o=document.querySelector('.dp-overlay');const d=o.getContext('2d').getImageData(0,0,o.width,o.height).data;let c=0;for(let i=3;i<d.length;i+=4)if(d[i])c++;return c});
 async function sweep(){const s=await box();for(let q=0;q<=40;q++){await p.mouse.move(s.x+s.width*(0.1+0.8*q/40),s.y+s.height*(0.15+0.7*q/40));await p.waitForTimeout(16)}}
 await fr.evaluate(()=>{document.getElementById('play').click()});
 await sweep();R.sweepOff=await pix();
 await fr.evaluate(()=>document.querySelector('.dp-readbtn').click());await sweep();R.sweepOn=await pix();
 // pin the first dial
 const at=await fr.evaluate(()=>Sim.data.inspect({what:'dial',j:0}).at);let s=await box();await p.mouse.click(s.x+at.x,s.y+at.y);await p.waitForTimeout(500);
 R.pinDial=await fr.evaluate(()=>({title:document.querySelector('.dp-read__title').textContent,vals:[...document.querySelectorAll('.dp-read__v')].map(e=>e.textContent)}));
 // pin the piston (ideal) or the ram (servo)
 const at2=await fr.evaluate(t=>t==='ideal'?Sim.data.inspect({what:'piston',k:1}).at:Sim.data.inspect({what:'ram'}).at,tab);s=await box();await p.mouse.click(s.x+at2.x,s.y+at2.y);await p.waitForTimeout(500);
 R.pinBody=await fr.evaluate(()=>({title:document.querySelector('.dp-read__title').textContent,vals:[...document.querySelectorAll('.dp-read__v')].map(e=>e.textContent)}));
 const sb=await (await fr.$('.dp-read')).boundingBox();s=await st.boundingBox();R.stripBelow={stripTop:sb.y,figureBottom:s.y+s.height,overlap:sb.y<s.y+s.height-0.5};
 R.stripRate=await fr.evaluate(()=>new Promise(res=>{const el=document.querySelector('.dp-read__vals');let last='',n=0;const t0=performance.now();(function f(){const x=el.textContent;if(x!==last){n++;last=x}if(performance.now()-t0<3000)requestAnimationFrame(f);else res({batches:n,perSecond:n/3})})()}));
 await p.screenshot({path:`${out}/hyd-${tab}-${w}-pinned.png`});
 await fr.evaluate(()=>document.querySelector('.dp-read__v[data-check]').click());await p.waitForTimeout(800);
 R.uiCheck=await fr.evaluate(()=>document.querySelector('.dp-check__body')?.innerText.replace(/\s+/g,' ').slice(0,600));
 await p.screenshot({path:`${out}/hyd-${tab}-${w}-check.png`});
 await fr.evaluate(()=>document.querySelector('.dp-readbtn').click());
 // one round, at the fastest speed the page offers
 await fr.evaluate(()=>{const b=[...document.querySelectorAll('.seg button')].pop();b.click();document.getElementById('reset').click()});
 await fr.evaluate(()=>document.querySelector('[data-rec]').click());
 await fr.waitForFunction(()=>__dataPanel.rounds().length>0,null,{timeout:120000});
 R.round=await fr.evaluate(()=>{const r=__dataPanel.rounds()[0];return {n:r.n,len:r.len,el:r.el,first:r.series[0].data[0],pointNaN:r.series.filter(s=>s.point).map(s=>s.key+':'+Array.from(s.data).filter(v=>v!==v).length+'/'+s.data.length)}});
 await p.screenshot({path:`${out}/hyd-${tab}-${w}-round.png`});
 const [dl]=await Promise.all([p.waitForEvent('download'),fr.evaluate(()=>document.querySelector('[data-save]').click())]);await dl.saveAs(`${out}/hyd-${tab}-${w}.zip`);
 await fr.evaluate(()=>document.querySelector('.dp__close').click());await p.waitForTimeout(300);R.idleRunning=await fr.evaluate(()=>__dataPanel.running());
 R.layout=await fr.evaluate(()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth}));R.errors=errs;
 fs.writeFileSync(`${out}/hyd-${tab}-${w}.json`,JSON.stringify(R,null,1));console.log(JSON.stringify(R).slice(0,2500));
 await b.close();})();
