// Each figure on screen, held off screen, resumed; the store live for an open data panel; the walkthrough's values.
// node tools/perf/clockcheck.cjs <base URL> <page> ...   (docs/performance.md, change 3)
// Does each figure run on screen, hold off screen, resume, keep the store live for an open data panel and the walkthrough?
const {chromium}=require('playwright');
const base=process.argv[2]; const pages=process.argv.slice(3);
async function hash(p){ return p.evaluate(()=>{ const c=[...document.querySelectorAll('.sim__grid canvas')].filter(c=>c.width>0&&c.getBoundingClientRect().height>0)[0]; if(!c) return 'nocanvas';
  const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let h=0,a=0; for(let i=0;i<d.length;i+=97){h=(h*31+d[i])|0; if(i%4===3&&d[i])a++;} return h+':'+a; }); }
const live=p=>p.evaluate(()=>{try{return JSON.stringify(window.Sim&&Sim.live?Sim.live():{})}catch(e){return 'err'}});
(async()=>{const b=await chromium.launch();
 for(const pg of pages){ const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true}); const p=await ctx.newPage(); const errs=[];
  p.on('console',m=>{if(m.type()==='error')errs.push(m.text().slice(0,80))}); p.on('pageerror',e=>errs.push('pageerror '+String(e).slice(0,80)));
  await p.goto(base+pg,{waitUntil:'load'}); await p.waitForTimeout(3000);
  const solve=p.locator('#solve'); if(await solve.count()){ await solve.first().click(); await p.waitForTimeout(3000); }
  const h1=await hash(p); await p.waitForTimeout(1200); const h2=await hash(p); const runsTop=h1!==h2;
  const l0=await live(p);
  await p.evaluate(()=>window.scrollTo(0,document.querySelector('.paper').offsetTop+2500)); await p.waitForTimeout(1500);
  const la=await live(p); await p.waitForTimeout(1200); const lb=await live(p); const storeMovesAway=la!==lb;
  // open the data panel while away (a scroll up brings its tab back)
  await p.evaluate(()=>scrollBy(0,-30)); await p.waitForTimeout(600); let panel='no tab';
  const tab=p.locator('.dp-tab'); if(await tab.count()){ await tab.click(); await p.waitForTimeout(800); const x=await live(p); await p.waitForTimeout(1200); const y=await live(p); panel=x!==y?'store live':'store still'; await p.locator('.dp__close').click().catch(()=>{}); await p.waitForTimeout(400);}
  // walkthrough in view
  let walk='no walk'; const w=p.locator('#walk'); if(await w.count()){ await w.scrollIntoViewIfNeeded(); await p.waitForTimeout(1200);
    const c1=await p.evaluate(()=>[...document.querySelectorAll('#walk [data-v]')].map(t=>t.textContent).join('|')); await p.waitForTimeout(1500);
    const c2=await p.evaluate(()=>[...document.querySelectorAll('#walk [data-v]')].map(t=>t.textContent).join('|')); walk=c1===''?'no live cells':(c1!==c2?'values move':'values still'); }
  await p.evaluate(()=>window.scrollTo(0,0)); await p.waitForTimeout(1500); const h3=await hash(p); await p.waitForTimeout(1200); const h4=await hash(p);
  console.log(decodeURIComponent(pg).slice(0,46).padEnd(46),'top runs:',runsTop,'| store moves while away:',storeMovesAway,'| panel open away:',panel,'| walkthrough:',walk,'| resumes:',h3!==h4,'| errors:',errs.length?errs.join(';'):'none');
  await ctx.close();}
 await b.close();})();
