// Page loads as a phone sees them (docs/performance.md). node tools/perf/measure.cjs <base URL> <out.json> <runs> <path> [<path> ...]
// Cold visit (empty cache) then a repeat visit in the same browser; the median of <runs> runs. NET=4g for 85 ms / 9 Mbit/s instead of Slow 4G.
// Mobile profile: 390x844, DPR 3, CPU 4x, Lighthouse "Slow 4G" devtools throttling (562.5 ms RTT, 1474.56 kbit/s down, 675 kbit/s up).
const {chromium}=require('playwright'); const fs=require('fs');
const [base,out,runsS,...paths]=process.argv.slice(2); const RUNS=+runsS||3;
const NET=process.env.NET==='4g'?{offline:false,latency:85,downloadThroughput:9000*1024/8,uploadThroughput:3000*1024/8}:{offline:false,latency:562.5,downloadThroughput:1474.56*1024/8,uploadThroughput:675*1024/8};
const INIT=`(()=>{window.__m={lcp:0,cls:0,lt:[],fcp:0};
 new PerformanceObserver(l=>{for(const e of l.getEntries())__m.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});
 new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)__m.cls+=e.value}).observe({type:'layout-shift',buffered:true});
 new PerformanceObserver(l=>{for(const e of l.getEntries())__m.lt.push([e.startTime,e.duration])}).observe({type:'longtask',buffered:true});
 new PerformanceObserver(l=>{for(const e of l.getEntries())if(e.name==='first-contentful-paint')__m.fcp=e.startTime}).observe({type:'paint',buffered:true});})()`;
async function metric(cdp){const r=await cdp.send('Performance.getMetrics');const o={};for(const m of r.metrics)o[m.name]=m.value;return o;}
async function one(browser,p){
 const ctx=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true,ignoreHTTPSErrors:true,userAgent:'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36'});
 await ctx.addInitScript(INIT);
 const page=await ctx.newPage(); const cdp=await ctx.newCDPSession(page);
 await cdp.send('Network.enable'); await cdp.send('Performance.enable');
 await cdp.send('Network.emulateNetworkConditions',NET); await cdp.send('Emulation.setCPUThrottlingRate',{rate:4});
 let bytes=0,reqs=0,s304=0,s3xx=0,errs=[],htmlB=0; const status={},net={},isDoc={};
 cdp.on('Network.responseReceived',e=>{status[e.requestId]=e.response.status; if(e.response.status===304)s304++;});
 cdp.on('Network.requestWillBeSent',e=>{if(!/^https?:/.test(e.request.url))return; net[e.requestId]=1; if(e.type==='Document')isDoc[e.requestId]=1; reqs++; if(e.redirectResponse)s3xx++;});
 cdp.on('Network.loadingFinished',e=>{if(!net[e.requestId])return; bytes+=e.encodedDataLength; if(isDoc[e.requestId])htmlB+=e.encodedDataLength;});
 page.on('console',m=>{if(m.type()==='error')errs.push(m.text().slice(0,160))}); page.on('pageerror',e=>errs.push('pageerror '+String(e).slice(0,160)));
 const t0=Date.now(); await page.goto(base+p,{waitUntil:'load',timeout:180000}); const loadWall=Date.now()-t0;
 await page.waitForTimeout(3000);
 const m1=await metric(cdp); await page.waitForTimeout(5000); const m2=await metric(cdp);
 const r=await page.evaluate(()=>{const n=performance.getEntriesByType('navigation')[0];const fcp=__m.fcp;
   const tbt=__m.lt.filter(x=>x[0]>=fcp).reduce((a,x)=>a+Math.max(0,x[1]-50),0);
   return {fcp,lcp:__m.lcp,cls:__m.cls,longTasks:__m.lt.length,maxTask:Math.max(0,...__m.lt.map(x=>x[1])),tbt,
     ttfb:n.responseStart,redirect:n.redirectEnd-n.redirectStart,domContentLoaded:n.domContentLoadedEventEnd,load:n.loadEventEnd,
     scrollW:document.documentElement.scrollWidth}});
 const cold={...r,bytes,htmlB,reqs,s3xx,loadWall,taskMs:m1.TaskDuration*1000,scriptMs:m1.ScriptDuration*1000,layoutMs:m1.LayoutDuration*1000,styleMs:m1.RecalcStyleDuration*1000,
   heapMB:m1.JSHeapUsedSize/1048576,idleBusyPct:100*(m2.TaskDuration-m1.TaskDuration)/5,errs:[...new Set(errs)]};
 // warm: second visit in the same browser context (HTTP cache kept)
 bytes=0;htmlB=0;reqs=0;s304=0;s3xx=0; const t1=Date.now();
 await page.goto('about:blank'); await page.goto(base+p,{waitUntil:'load',timeout:180000}); const warmWall=Date.now()-t1;
 await page.waitForTimeout(1500);
 const w=await page.evaluate(()=>({lcp:__m.lcp,fcp:__m.fcp,load:performance.getEntriesByType('navigation')[0].loadEventEnd}));
 const warm={...w,bytes,htmlB,reqs,s304,s3xx,loadWall:warmWall};
 await ctx.close(); return {cold,warm};
}
const med=a=>{const s=[...a].sort((x,y)=>x-y);return s[Math.floor(s.length/2)]};
(async()=>{const browser=await chromium.launch(); const res={};
 for(const p of paths){const runs=[];for(let i=0;i<RUNS;i++){try{runs.push(await one(browser,p))}catch(e){console.error(p,e.message)}}
   const agg={cold:{},warm:{}}; for(const k of ['cold','warm'])for(const f of Object.keys(runs[0]?.[k]||{}))if(typeof runs[0][k][f]==='number')agg[k][f]=med(runs.map(r=>r[k][f]));
   if(!runs.length){console.log(p.padEnd(48)+' every run failed'); res[p]={failed:true}; continue;}
   agg.errs=runs[0]?.cold.errs; res[p]=agg;
   const c=agg.cold,w=agg.warm; console.log(`${p.padEnd(48)} LCP ${(c.lcp/1000).toFixed(2)}s FCP ${(c.fcp/1000).toFixed(2)} CLS ${c.cls.toFixed(3)} TBT ${c.tbt|0}ms maxTask ${c.maxTask|0} task ${c.taskMs|0}ms heap ${c.heapMB.toFixed(1)}MB ${(c.bytes/1024)|0}kB/${c.reqs}req 3xx ${c.s3xx} idle ${c.idleBusyPct.toFixed(1)}% | warm LCP ${(w.lcp/1000).toFixed(2)}s ${(w.bytes/1024)|0}kB (html ${(w.htmlB/1024)|0}) ${w.reqs}req 304 ${w.s304} | errs ${(agg.errs||[]).length} sw ${c.scrollW}`);
 }
 fs.writeFileSync(out,JSON.stringify(res,null,1)); await browser.close();})();
