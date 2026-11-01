// Open the built site pages through a local server, as a reader would, and check fonts, policy and the run.
const { chromium } = require('playwright');
(async()=>{
 const base=process.argv[2]||'http://localhost:8766/portfolios/impact/';
 const b=await chromium.launch();
 for(const page of ['index.html','ar.html'])for(const w of [1100,390]){
  const p=await b.newPage({viewport:{width:w,height:1000}});const errs=[];
  p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  const failed=[];p.on('requestfailed',r=>failed.push(r.url()));
  const outside=[];p.on('request',r=>{if(!r.url().startsWith('http://localhost')&&!r.url().startsWith('data:'))outside.push(r.url())});
  await p.goto(base+page);await p.waitForFunction(()=>computed>=NF,null,{timeout:300000});
  await p.evaluate(()=>document.fonts.ready);
  const r=await p.evaluate(()=>({
    fonts:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family.replace(/"/g,'')+' '+f.weight).filter((v,i,a)=>a.indexOf(v)===i),
    Fi:ds.get('Fpeak_iron').toFixed(1),Fc:ds.get('Fpeak_cot').toFixed(1),wi:ds.get('W_end_iron').toFixed(2),wc:ds.get('W_end_cot').toFixed(2),
    back:document.querySelector('.sitebar a').getAttribute('href'),sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth}));
  console.log(page,w,JSON.stringify(r),'errors',errs,'failed',failed,'outside',outside);
  if(w===1100){await p.click('#drop');await p.evaluate(()=>setSpeed(20));await p.waitForFunction(()=>tPlay>1.445,null,{timeout:60000});
    await (await p.$('#sim')).screenshot({path:`site-${page}-impact.png`});}
  await p.close();
 }
 await b.close();})();
