// What fills the main thread while a page sits idle: 4 s of trace and CPU profile, at the top or scrolled to <scrollY>.
// node tools/perf/trace.cjs <url> [scrollY]   (docs/performance.md)
const {chromium}=require('playwright');
(async()=>{const [url,scroll]=process.argv.slice(2); const b=await chromium.launch(); const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true,ignoreHTTPSErrors:true});
 const p=await ctx.newPage(); const c=await ctx.newCDPSession(p); await p.goto(url,{waitUntil:'load',timeout:120000}); await p.waitForTimeout(4000);
 if(scroll) {await p.evaluate(y=>scrollTo(0,+y),scroll); await p.waitForTimeout(1500);}
 await c.send('Emulation.setCPUThrottlingRate',{rate:4});
 const ev=[]; c.on('Tracing.dataCollected',d=>ev.push(...d.value));
 await c.send('Profiler.enable'); await c.send('Profiler.start');
 await c.send('Tracing.start',{categories:'devtools.timeline,disabled-by-default-devtools.timeline,disabled-by-default-devtools.timeline.stack',transferMode:'ReportEvents'});
 await p.waitForTimeout(4000);
 const done=new Promise(r=>c.once('Tracing.tracingComplete',r)); await c.send('Tracing.end'); await done;
 const {profile}=await c.send('Profiler.stop');

 const tot={},cnt={}; const layoutStacks={};
 for(const e of ev){ if(e.ph!=='X'||!e.dur)continue; if(!['Layout','UpdateLayoutTree','Paint','RasterTask','FunctionCall','EvaluateScript','Animation Frame Fired','FireAnimationFrame','CompositeLayers','PrePaint','Layerize','UpdateLayer','ScheduleStyleRecalculation','HitTest','ParseHTML','GPUTask','Commit'].includes(e.name))continue;
   tot[e.name]=(tot[e.name]||0)+e.dur/1000; cnt[e.name]=(cnt[e.name]||0)+1;
   if(e.name==='Layout'&&e.args&&e.args.beginData&&e.args.beginData.stackTrace){const f=e.args.beginData.stackTrace.slice(0,3).map(s=>s.functionName+':'+s.lineNumber).join(' < ');layoutStacks[f]=(layoutStacks[f]||0)+1;}}
 console.log('per 4 s idle window (ms, count):'); for(const k of Object.keys(tot).sort((a,b)=>tot[b]-tot[a])) console.log(' ',k.padEnd(24),tot[k].toFixed(0),cnt[k]);
 console.log('forced layouts by JS stack:'); Object.entries(layoutStacks).sort((a,b)=>b[1]-a[1]).slice(0,8).forEach(([k,v])=>console.log(' ',v,k));
 // JS self time
 const self={}; const dt=profile.timeDeltas; const idIdx={}; profile.nodes.forEach(n=>idIdx[n.id]=n);
 for(let i=0;i<profile.samples.length;i++){const n=idIdx[profile.samples[i]];const k=n.callFrame.functionName+' '+(n.callFrame.url.split('/').pop()||'')+':'+n.callFrame.lineNumber; self[k]=(self[k]||0)+(dt[i]||0)/1000;}
 console.log('top JS self time (ms):'); Object.entries(self).sort((a,b)=>b[1]-a[1]).slice(0,14).forEach(([k,v])=>console.log(' ',v.toFixed(0),k.slice(0,90)));
 await b.close();})();
