// A repeat visit seen as a reader sees it: screenshots at fixed times after the navigation starts, and every largest-contentful-paint
// candidate with its element and text, so a change in LCP can be told apart from a change in what is on the screen (docs/performance.md).
// node tools/perf/film.cjs <URL> <out prefix>   writes <prefix>-<ms>.png for 2500, 3000, 3500, 4500, 6000 and 8000 ms, and <prefix>.png
// with the six side by side (needs Python with Pillow). Mobile profile as measure.cjs (390x844, CPU 4x, Slow 4G), at DPR 1 to keep the
// screenshots small. The first visit fills the cache; only the second is filmed.
const {chromium}=require('playwright'); const fs=require('fs'); const {execFileSync}=require('child_process');
const [url,prefix]=process.argv.slice(2); const TIMES=[2500,3000,3500,4500,6000,8000];
const NET={offline:false,latency:562.5,downloadThroughput:1474.56*1024/8,uploadThroughput:675*1024/8};
const INIT=`window.__l=[];new PerformanceObserver(l=>{for(const e of l.getEntries()){const el=e.element;
 __l.push({t:Math.round(e.startTime),size:e.size,el:el?el.tagName.toLowerCase()+(el.className?'.'+String(el.className).split(' ')[0]:'')+' "'+(el.textContent||'').trim().slice(0,40)+'"'+(el.parentElement?' in '+el.parentElement.tagName.toLowerCase()+(el.parentElement.className?'.'+String(el.parentElement.className).split(' ')[0]:''):''):'(removed)'})}})
 .observe({type:'largest-contentful-paint',buffered:true});`;
(async()=>{const b=await chromium.launch();
 const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
 await ctx.addInitScript(INIT); const page=await ctx.newPage(); const cdp=await ctx.newCDPSession(page);
 await cdp.send('Network.enable'); await cdp.send('Network.emulateNetworkConditions',NET); await cdp.send('Emulation.setCPUThrottlingRate',{rate:4});
 await page.goto(url,{waitUntil:'load',timeout:180000}); await page.waitForTimeout(3000);
 await page.goto('about:blank'); const t0=Date.now(); const nav=page.goto(url,{waitUntil:'load',timeout:180000});
 for(const t of TIMES){const w=t-(Date.now()-t0); if(w>0)await new Promise(r=>setTimeout(r,w));
   const s=await cdp.send('Page.captureScreenshot',{format:'png'}); fs.writeFileSync(`${prefix}-${t}.png`,Buffer.from(s.data,'base64'));}
 await nav; await page.waitForTimeout(1500);
 const r=await page.evaluate(()=>({lcp:__l,load:Math.round(performance.getEntriesByType('navigation')[0].loadEventEnd)}));
 console.log(`load event ${r.load} ms; LCP candidates (ms, area in CSS px², element):`); for(const c of r.lcp)console.log(`  ${c.t}  ${c.size}  ${c.el}`);
 await b.close();
 try{execFileSync('python3',['-c',`import sys
from PIL import Image
ims=[Image.open(f) for f in sys.argv[2:]]; o=Image.new('RGB',(sum(i.width for i in ims),max(i.height for i in ims)),'white'); x=0
for i in ims: o.paste(i,(x,0)); x+=i.width
o.save(sys.argv[1])`,`${prefix}.png`,...TIMES.map(t=>`${prefix}-${t}.png`)]); console.log(`filmstrip ${prefix}.png`);}catch(e){console.log('no filmstrip (python3 with Pillow needed); the single frames are written');}
})();
