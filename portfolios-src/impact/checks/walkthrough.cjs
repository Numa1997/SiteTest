const { chromium } = require('playwright');
(async()=>{
 const file=process.argv[2],tag=process.argv[3];
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'});
 for(const [w,h] of [[1100,950],[390,1200]]){
  const p=await b.newPage({viewport:{width:w,height:h}});
  const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+process.cwd()+'/'+file);
  await p.waitForTimeout(1500);
  const sim=await p.$('#sim');
  await p.screenshot({path:`${tag}-${w}-0open.png`});
  await p.waitForFunction(()=>computed>=NF,null,{timeout:300000});
  await p.evaluate(()=>{setSpeed(1)});await p.click('#drop');
  await p.waitForFunction(()=>tPlay>0.8,null,{timeout:20000});await sim.screenshot({path:`${tag}-${w}-1fall.png`});
  await p.evaluate(()=>{setSpeed(20)});
  await p.waitForFunction(()=>tPlay>1.44,null,{timeout:60000});await sim.screenshot({path:`${tag}-${w}-2impact.png`});
  await p.evaluate(()=>{setSpeed(1)});
  await p.waitForFunction(()=>!playing,null,{timeout:60000});await p.waitForTimeout(200);
  await sim.screenshot({path:`${tag}-${w}-3end.png`});
  const r=await p.evaluate(()=>{const k=NF-1,d=s=>ds.get(s);window._w=[d('W_iron')[kOf(6.5)],d('W_cot')[kOf(6.5)]];return {ti:d('t_touch_iron'),tc:d('t_touch_cot'),Fi:d('Fpeak_iron'),Fc:d('Fpeak_cot'),wi:d('W_end_iron'),wc:d('W_end_cot'),
   books:['iron','cot'].map(s=>+d('books_'+s)[k].toFixed(3)),heat:['iron','cot'].map(s=>[d('Qb_'+s)[k].toFixed(1),d('Qh_'+s)[k].toFixed(1)]),
   w65:window._w,sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth}});
  console.log(w,JSON.stringify(r),'errors',errs);
  await (await p.$('#en')).screenshot({path:`${tag}-${w}-4energy.png`});
  await (await p.$('#pZoom')).screenshot({path:`${tag}-${w}-5plot.png`});
  await p.close();
 }
 await b.close();})();
