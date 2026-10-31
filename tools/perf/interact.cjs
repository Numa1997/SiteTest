// Interactions a reader makes: page-to-page clicks, Solve, the data panel, folds, the study tabs; Event Timing durations (what INP is made of).
// node tools/perf/interact.cjs <base URL> <out.json> <runs>   (docs/performance.md)
const {chromium}=require('playwright'); const fs=require('fs');
const [base,out,runsS]=process.argv.slice(2); const RUNS=+runsS||3;
const NET=process.env.NET==='4g'?{offline:false,latency:85,downloadThroughput:9000*1024/8,uploadThroughput:3000*1024/8}:{offline:false,latency:562.5,downloadThroughput:1474.56*1024/8,uploadThroughput:675*1024/8};
const INIT=`if(window.top===window){window.__ready={};addEventListener('message',function(e){var d=e.data||{};for(var k in d)if(/Ready$/.test(k)&&typeof d[k]==='string'&&!(d[k] in __ready))__ready[d[k]]=performance.now();});}(()=>{window.__m={lcp:0,ev:[]};
 new PerformanceObserver(l=>{for(const e of l.getEntries())__m.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});
 try{new PerformanceObserver(l=>{for(const e of l.getEntries())if(e.interactionId)__m.ev.push({n:e.name,d:e.duration,id:e.interactionId,t:e.startTime,pd:e.processingStart-e.startTime,pr:e.processingEnd-e.processingStart})}).observe({type:'event',durationThreshold:16,buffered:true});}catch(e){}})()`;
async function setup(browser){
 const ctx=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true,ignoreHTTPSErrors:true});
 await ctx.addInitScript(INIT); const page=await ctx.newPage(); const cdp=await ctx.newCDPSession(page);
 await cdp.send('Network.enable'); await cdp.send('Network.emulateNetworkConditions',NET); await cdp.send('Emulation.setCPUThrottlingRate',{rate:4});
 const net={bytes:0,reqs:0,redir:0}; cdp.on('Network.requestWillBeSent',e=>{net.reqs++;if(e.redirectResponse)net.redir++;}); cdp.on('Network.loadingFinished',e=>net.bytes+=e.encodedDataLength);
 return {ctx,page,net};}
async function inp(page,fn,settle=1500){ // returns max event duration of interactions triggered by fn
 await page.evaluate(()=>__m.ev=[]); await fn(); await page.waitForTimeout(settle);
 const ev=await page.evaluate(()=>__m.ev); const by={}; for(const e of ev){by[e.id]=Math.max(by[e.id]||0,e.d);} const v=Object.values(by); return v.length?Math.max(...v):0;}
async function navStep(page,net,sel,label,pre){ if(pre){await pre(); await page.waitForTimeout(800);} net.bytes=0;net.reqs=0;net.redir=0; const t=Date.now();
 await Promise.all([page.waitForNavigation({waitUntil:'load',timeout:180000}), page.locator(sel).first().click()]);
 const wallLoad=Date.now()-t; await page.waitForTimeout(2500);
 const r=await page.evaluate(()=>{const n=performance.getEntriesByType('navigation')[0];return {lcp:__m.lcp,redirect:n.redirectEnd-n.redirectStart,ttfb:n.responseStart,url:location.pathname}});
 return {label,...r,wallLoad,bytes:net.bytes,reqs:net.reqs,redir:net.redir};}
async function run(browser){ const R={};
 try{ // Flow 1: navigation, warm-as-you-go, as a reader clicks
 {const {ctx,page,net}=await setup(browser); await page.goto(base+'/',{waitUntil:'load'}); await page.waitForTimeout(2000);
  R.nav=[]; 
  R.nav.push(await navStep(page,net,'a[href="simulations.html"]:visible','home → simulations'));
  const openCard=()=>page.locator('.fs-head',{hasText:'Driven Oscillator'}).first().click();
  R.nav.push(await navStep(page,net,'a.entry__open[href$="driven-oscillator.html"]','simulations → Fig. 9',openCard));
  R.nav.push(await navStep(page,net,'a[href$="simulations.html"]:visible','Fig. 9 → simulations (back by link)'));
  R.nav.push(await navStep(page,net,'a.entry__open[href$="driven-oscillator.html"]','simulations → Fig. 9 again',async()=>{if(!(await page.locator('a.entry__open[href$="driven-oscillator.html"]').isVisible()))await openCard();}));
  await ctx.close();}}catch(e){R.err1=e.message.slice(0,200)}
 try{ // Flow 2: simulation page interactions
 {const {ctx,page}=await setup(browser); await page.goto(base+'/simulations/driven-oscillator.html',{waitUntil:'load'}); await page.waitForTimeout(4000);
  R.solve=await inp(page,()=>page.locator('#solve').click(),3000);
  await page.evaluate(()=>scrollBy(0,40)); await page.waitForTimeout(300); await page.evaluate(()=>scrollBy(0,-40)); await page.waitForTimeout(800);
  R.dataOpen=await inp(page,()=>page.locator('.dp-tab').click());
  R.dataClose=await inp(page,()=>page.locator('.dp__close').click());
  const t=page.locator('.psec .fs-toggle').first(); await t.scrollIntoViewIfNeeded(); await page.waitForTimeout(800);
  R.foldClose=await inp(page,()=>t.click()); R.foldOpen=await inp(page,()=>t.click());
  await ctx.close();}}catch(e){R.err2=e.message.slice(0,200)}
 try{ // Flow 3: rotor tabs
 {const {ctx,page,net}=await setup(browser); await page.goto(base+'/portfolios/rotor-pendula/index.html',{waitUntil:'load',timeout:180000});
  await page.waitForFunction(()=>window.__ready&&window.__ready.notes!==undefined,null,{timeout:120000,polling:50}); await page.waitForTimeout(1500);
  // a tab is ready when its frame posts rotorReady to the shell (the shell's 'Loading…' is hidden only once); a tab seen before is ready at once
  for(const tb of ['sim','wind','notes','sim']){ let readyMs=0; const d=await inp(page,async()=>{const t0=await page.evaluate(()=>performance.now()); await page.locator('#tab-'+tb).click(); await page.waitForFunction(t=>window.__ready&&window.__ready[t]!==undefined,tb,{timeout:120000,polling:50}); readyMs=Math.max(0,await page.evaluate(t=>__ready[t],tb)-t0);},1000);
    R['rotorTab_'+tb+(R['rotorTab_'+tb]?'_2':'')]={inp:d,readyMs};}
  R.rotorHeapMB=(await page.evaluate(()=>performance.memory?performance.memory.usedJSHeapSize/1048576:0));
  await ctx.close();}}catch(e){R.err3=e.message.slice(0,200)}
 return R;}
(async()=>{const browser=await chromium.launch(); const all=[];
 for(let i=0;i<RUNS;i++){try{const r=await run(browser);all.push(r);console.log(JSON.stringify(r));}catch(e){console.log('ERR',e.message.slice(0,300))}}
 fs.writeFileSync(out,JSON.stringify(all,null,1)); await browser.close();})();
