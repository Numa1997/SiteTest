// How close a study tab comes to the shell's 8 s limit: the time from its frame being created to its ready message.
// node tools/perf/margin.cjs <base URL> <CPU slowdown, e.g. 6> <runs> [<path>#<tab> ...]   (Slow 4G; docs/performance.md)
// The shell replaces a frame still not ready after 8 s only if its srcdoc was refused (since 31 October 2026); before, it replaced
// any such frame, and the site's security policy blocks the replacement, so a tab waiting on the network at 8 s ended blank.
const {chromium}=require('playwright');
const NET={offline:false,latency:562.5,downloadThroughput:1474.56*1024/8,uploadThroughput:675*1024/8};
(async()=>{const [base,rateS,runsS,...specs]=process.argv.slice(2); const rate=+rateS||6, RUNS=+runsS||2;
 const list=specs.length?specs:['/portfolios/rotor-pendula/#notes','/portfolios/rotor-pendula/#sim','/portfolios/hydraulics/#servo'];
 const b=await chromium.launch();
 for(const spec of list) for(let run=0;run<RUNS;run++){
  const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,ignoreHTTPSErrors:true});
  await ctx.addInitScript(()=>{ if(window.top!==window) return; window.__made=null; window.__rdy=null;
    new MutationObserver(()=>{ if(!window.__made&&document.querySelector('#stage iframe')) window.__made=performance.now(); }).observe(document,{childList:true,subtree:true});
    addEventListener('message',e=>{const d=e.data||{}; for(const k in d) if(/Ready$/.test(k)&&!window.__rdy) window.__rdy=performance.now();}); });
  const p=await ctx.newPage(); const c=await ctx.newCDPSession(p); await c.send('Network.enable'); await c.send('Network.emulateNetworkConditions',NET); await c.send('Emulation.setCPUThrottlingRate',{rate});
  await p.goto(base+spec,{waitUntil:'commit'});
  await p.waitForFunction(()=>window.__rdy||(window.__made&&performance.now()-window.__made>15000),null,{timeout:180000,polling:100}).catch(()=>{});
  const r=await p.evaluate(()=>({made:window.__made,rdy:window.__rdy,src:(document.querySelector('#stage iframe')||{}).src||''}));
  console.log(spec.padEnd(36),'CPU '+rate+'x','frame created at',(r.made/1000).toFixed(1),'s; ready',r.rdy?((r.rdy-r.made)/1000).toFixed(2)+' s after creation':'not ready within 15 s','| replaced by a blob frame:',r.src.startsWith('blob:'));
  await ctx.close();}
 await b.close();})();
