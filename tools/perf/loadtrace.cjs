// The long main-thread pieces (parse, layout, script) of a study page's cold load, until its first tab is ready.
// node tools/perf/loadtrace.cjs <url>   (docs/performance.md)
const {chromium}=require('playwright');
(async()=>{const url=process.argv[2]; const b=await chromium.launch(); const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true,ignoreHTTPSErrors:true});
 const p=await ctx.newPage(); const c=await ctx.newCDPSession(p); await c.send('Network.enable');
 await c.send('Network.emulateNetworkConditions',{offline:false,latency:562.5,downloadThroughput:1474.56*1024/8,uploadThroughput:675*1024/8}); await c.send('Emulation.setCPUThrottlingRate',{rate:4});
 const ev=[]; c.on('Tracing.dataCollected',d=>ev.push(...d.value));
 await c.send('Tracing.start',{categories:'devtools.timeline,blink.user_timing,loading',transferMode:'ReportEvents'});
 const t0=Date.now(); await p.goto(url,{waitUntil:'commit'}); await p.waitForFunction(()=>document.getElementById('loading')&&document.getElementById('loading').hidden,null,{timeout:180000,polling:50}); const ready=Date.now()-t0; await p.waitForTimeout(4000);
 const done=new Promise(r=>c.once('Tracing.tracingComplete',r)); await c.send('Tracing.end'); await done;
 const tm=Math.min(...ev.filter(e=>e.ts>0).map(e=>e.ts));ev.filter(e=>e.dur>150000&&['Layout','UpdateLayoutTree','ParseHTML','EvaluateScript','PrePaint','Paint'].includes(e.name)).sort((a,b)=>a.ts-b.ts).forEach(e=>console.log('   ',e.name.padEnd(16),'at',((e.ts-tm)/1000|0),'ms dur',(e.dur/1000|0),'ms'));
 console.log('ready after',ready,'ms');
 await b.close();})();
