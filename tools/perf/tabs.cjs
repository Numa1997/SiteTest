// The study pages with tabs (Rotor Pendula, Hydraulic Press Study): time until the first tab is drawn, each tab switch, a repeat visit.
// node tools/perf/tabs.cjs <base URL> <path> <tab,tab,...> <runs>   (docs/performance.md)
// Times run from the start of navigation (or from just before the click, for a switch) to the moment the shell receives the tab's
// ready message, which its frame posts at the end of its body; both ends are the page's own clock (performance.now), so the script's
// polling does not add to them. kB are 1000 bytes. tbt and maxTask: long tasks from navigation start until 1.5 s after the script
// sees the first tab ready.
const {chromium}=require('playwright');
const [base,path,tabsS,runsS]=process.argv.slice(2); const TABS=tabsS.split(','); const RUNS=+runsS||3;
const NET=process.env.NET==='4g'?{offline:false,latency:85,downloadThroughput:9000*1024/8,uploadThroughput:3000*1024/8}:{offline:false,latency:562.5,downloadThroughput:1474.56*1024/8,uploadThroughput:675*1024/8};
const med=a=>{const s=[...a].sort((x,y)=>x-y);return s[Math.floor(s.length/2)]};
const INIT=`if(window.top===window){window.__ready={};addEventListener('message',function(e){var d=e.data||{};for(var k in d)if(/Ready$/.test(k)&&typeof d[k]==='string'&&!(d[k] in __ready))__ready[d[k]]=performance.now();});}window.__lt=[];try{new PerformanceObserver(l=>{for(const e of l.getEntries())__lt.push(e.duration)}).observe({type:'longtask',buffered:true})}catch(e){}`;
(async()=>{const b=await chromium.launch(); const rows=[];
 for(let r=0;r<RUNS;r++){
  const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true,ignoreHTTPSErrors:true}); await ctx.addInitScript(INIT);
  const p=await ctx.newPage(); const c=await ctx.newCDPSession(p); await c.send('Network.enable'); await c.send('Network.emulateNetworkConditions',NET); await c.send('Emulation.setCPUThrottlingRate',{rate:4});
  let bytes=0; const net={}; c.on('Network.requestWillBeSent',e=>{if(/^https?:/.test(e.request.url))net[e.requestId]=1}); c.on('Network.loadingFinished',e=>{if(net[e.requestId])bytes+=e.encodedDataLength});
  const errs=[]; p.on('console',m=>{if(m.type()==='error')errs.push(m.text().slice(0,120))}); p.on('pageerror',e=>errs.push(String(e).slice(0,120)));
  // a tab is ready when its frame has posted its ready message (…Ready: tab) to the shell; the shell's 'Loading…' is hidden only once
  const ready=(tab)=>p.waitForFunction(t=>window.__ready&&window.__ready[t]!==undefined,tab,{timeout:180000,polling:50});
  await p.goto(base+path+'#'+TABS[0],{waitUntil:'commit',timeout:180000}); await ready(TABS[0]); const first=await p.evaluate(t=>__ready[t],TABS[0]);   // the frame's own time, from the start of navigation
  await p.waitForTimeout(1500); const lt1=await p.evaluate(()=>({n:__lt.length,max:Math.max(0,...__lt),tbt:__lt.reduce((a,d)=>a+Math.max(0,d-50),0)})); const coldBytes=bytes;
  const sw={}; for(const t of TABS.slice(1)){ const t1=await p.evaluate(()=>performance.now()); await p.locator('#tab-'+t).click(); await ready(t); sw[t]=await p.evaluate(x=>__ready[x],t)-t1; await p.waitForTimeout(800);}
  const heap=await p.evaluate(()=>performance.memory.usedJSHeapSize/1048576);
  bytes=0; await p.goto('about:blank'); await p.goto(base+path+'#'+TABS[0],{waitUntil:'commit'}); await ready(TABS[0]); const warm=await p.evaluate(t=>__ready[t],TABS[0]); await p.waitForTimeout(500);
  rows.push({first,warm,coldKB:coldBytes/1000,warmKB:bytes/1000,maxTask:lt1.max,tbt:lt1.tbt,heap,...Object.fromEntries(Object.entries(sw).map(([k,v])=>['to_'+k,v])),errs:errs.length});
  await ctx.close();}
 const keys=Object.keys(rows[0]); const m={}; for(const k of keys)m[k]=med(rows.map(x=>x[k]));
 console.log(base+path, Object.entries(m).map(([k,v])=>k+'='+(typeof v==='number'?Math.round(v):v)).join(' '));
 await b.close();})();
