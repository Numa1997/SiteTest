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
  await p.waitForFunction(()=>computed>=NF,null,{timeout:120000});
  await p.evaluate(()=>{setSpeed(1)});await p.click('#drop');
  await p.waitForFunction(()=>tPlay>0.8,null,{timeout:20000});await sim.screenshot({path:`${tag}-${w}-1fall.png`});
  await p.evaluate(()=>{setSpeed(20)});
  await p.waitForFunction(()=>tPlay>1.44,null,{timeout:60000});await sim.screenshot({path:`${tag}-${w}-2impact.png`});
  await p.evaluate(()=>{setSpeed(1)});
  await p.waitForFunction(()=>!playing,null,{timeout:60000});await p.waitForTimeout(200);
  await sim.screenshot({path:`${tag}-${w}-3end.png`});
  const r=await p.evaluate(()=>{const k=NF-1;window._w=[wAvg(S.iron,kOf(6.5)),wAvg(S.cot,kOf(6.5))];return {ti:S.iron.tImpact,tc:S.cot.tImpact,Fi:S.iron.Fmax[k],Fc:S.cot.Fmax[k],wi:wAvg(S.iron,k),wc:wAvg(S.cot,k),
   books:[S.iron,S.cot].map(st=>{const E=st.E.subarray(k*7,k*7+7);return +(E[0]+E[2]+E[3]+E[4]+E[5]-(E[6]-E[1])).toFixed(3)}),heat:[S.iron,S.cot].map(st=>[st.E[k*7+4].toFixed(1),st.E[k*7+5].toFixed(1)]),
   w65:window._w,sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth}});
  console.log(w,JSON.stringify(r),'errors',errs);
  await (await p.$('#en')).screenshot({path:`${tag}-${w}-4energy.png`});
  await (await p.$('#pZoom')).screenshot({path:`${tag}-${w}-5plot.png`});
  await p.close();
 }
 await b.close();})();
