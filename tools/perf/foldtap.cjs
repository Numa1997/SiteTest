// A reader in a figure's lecture note: the main thread's busy share while reading, and the Event Timing duration of closing and
// opening a fold there (CPU 4x). node tools/perf/foldtap.cjs <base URL> <runs> <page> ...   (docs/performance.md, change 3)
// A reader in the lecture note: scroll to a middle section, close and open its fold; Event Timing duration of each tap. CPU 4x.
const {chromium}=require('playwright');
const [base,runsS,...pages]=process.argv.slice(2); const RUNS=+runsS||3;
const med=a=>{const s=[...a].sort((x,y)=>x-y);return s[Math.floor(s.length/2)]};
(async()=>{const b=await chromium.launch();
 for(const pg of pages){ const R={close:[],open:[],busy:[]};
  for(let r=0;r<RUNS;r++){
   const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true});
   await ctx.addInitScript(()=>{window.__ev=[];new PerformanceObserver(l=>{for(const e of l.getEntries())if(e.interactionId)__ev.push(e.duration)}).observe({type:'event',durationThreshold:16,buffered:true});});
   const p=await ctx.newPage(); const c=await ctx.newCDPSession(p); await c.send('Performance.enable');
   await p.goto(base+pg,{waitUntil:'load'}); await p.waitForTimeout(3000); await c.send('Emulation.setCPUThrottlingRate',{rate:4});
   const t=p.locator('.paper .psec .fs-toggle'); const n=await t.count(); const k=t.nth(Math.floor(n/2));
   await k.scrollIntoViewIfNeeded(); await p.waitForTimeout(2000);
   const m0=(await c.send('Performance.getMetrics')).metrics.find(x=>x.name==='TaskDuration').value; const w0=Date.now(); await p.waitForTimeout(3000);
   const m1=(await c.send('Performance.getMetrics')).metrics.find(x=>x.name==='TaskDuration').value; R.busy.push(100*(m1-m0)/((Date.now()-w0)/1000));
   for(const kind of ['close','open']){ await p.evaluate(()=>__ev=[]); await k.click(); await p.waitForTimeout(1500); const ev=await p.evaluate(()=>__ev); R[kind].push(ev.length?Math.max(...ev):0);}
   await ctx.close();}
  console.log(decodeURIComponent(pg).padEnd(42),'busy while reading',med(R.busy).toFixed(0)+' %','| close fold',med(R.close)|0,'ms','| open fold',med(R.open)|0,'ms','  (runs: '+R.close.map(x=>x|0).join('/')+' ; '+R.open.map(x=>x|0).join('/')+')');}
 await b.close();})();
