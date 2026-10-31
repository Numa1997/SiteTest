// The long main-thread pieces (parse, layout, script) of a study page's cold load, until its first tab is ready.
// node tools/perf/loadtrace.cjs <url>   (docs/performance.md)
// node loadtrace.js <url> : trace a cold load (CPU 4x, Slow 4G) until #loading hides; list tasks > 200 ms with their biggest children
const {chromium}=require('playwright');
(async()=>{const url=process.argv[2]; const b=await chromium.launch(); const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true,ignoreHTTPSErrors:true});
 const p=await ctx.newPage(); const c=await ctx.newCDPSession(p); await c.send('Network.enable');
 await c.send('Network.emulateNetworkConditions',{offline:false,latency:562.5,downloadThroughput:1474.56*1024/8,uploadThroughput:675*1024/8}); await c.send('Emulation.setCPUThrottlingRate',{rate:4});
 const ev=[]; c.on('Tracing.dataCollected',d=>ev.push(...d.value));
 await c.send('Tracing.start',{categories:'devtools.timeline,blink.user_timing,loading',transferMode:'ReportEvents'});
 const t0=Date.now(); await p.goto(url,{waitUntil:'commit'}); await p.waitForFunction(()=>document.getElementById('loading')&&document.getElementById('loading').hidden,null,{timeout:180000,polling:50}); const ready=Date.now()-t0; await p.waitForTimeout(4000);
 const done=new Promise(r=>c.once('Tracing.tracingComplete',r)); await c.send('Tracing.end'); await done;
 const tasks=ev.filter(e=>(e.name==='RunTask'||e.name==='ThreadControllerImpl::RunTask')&&e.dur>200000); if(!tasks.length){const tm=Math.min(...ev.filter(e=>e.ts>0).map(e=>e.ts));ev.filter(e=>e.dur>150000&&['Layout','UpdateLayoutTree','ParseHTML','EvaluateScript','PrePaint','Paint'].includes(e.name)).sort((a,b)=>a.ts-b.ts).forEach(e=>console.log('   ',e.name.padEnd(16),'at',((e.ts-tm)/1000|0),'ms dur',(e.dur/1000|0),'ms'));} const fonts=ev.filter(e=>e.name==='ResourceFinish'||e.name==='ResourceReceiveResponse');
 const tmin=Math.min(...ev.filter(e=>e.ts>0).map(e=>e.ts));
 console.log('ready after',ready,'ms; long tasks > 200 ms:');
 for(const t of tasks){ const kids=ev.filter(e=>e.ph==='X'&&e.tid===t.tid&&e.ts>=t.ts&&e.ts+e.dur<=t.ts+t.dur&&e!==t&&['Layout','UpdateLayoutTree','ParseHTML','EvaluateScript','FunctionCall','Paint','PrePaint','RunMicrotasks','HitTest','Commit','ParseAuthorStyleSheet','v8.compile'].includes(e.name));
   const agg={}; kids.forEach(k=>agg[k.name]=(agg[k.name]||0)+k.dur/1000);
   console.log('  at',((t.ts-tmin)/1000|0),'ms, ',(t.dur/1000|0),'ms:',Object.entries(agg).sort((a,b)=>b[1]-a[1]).slice(0,5).map(([k,v])=>k+' '+(v|0)).join(', '));}
 await b.close();})();
