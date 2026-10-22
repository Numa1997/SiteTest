// Open the Portfolios page of the built site and screenshot the new project; check its links resolve.
const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'});
 for(const w of [1100,390]){const p=await b.newPage({viewport:{width:w,height:1000}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
  const bad=[];p.on('response',r=>{if(r.status()>=400)bad.push(r.status()+' '+r.url())});
  await p.goto('http://localhost:8766/portfolios.html');await p.waitForTimeout(800);
  const el=await p.$('#iron-cotton');await el.scrollIntoViewIfNeeded();await p.evaluate(()=>{for(const i of document.querySelectorAll('#iron-cotton img'))i.loading='eager'});await p.waitForTimeout(1200);
  await el.screenshot({path:`/tmp/portfolio-${w}.png`});
  const links=await p.$$eval('#iron-cotton a',as=>as.map(a=>a.href));const st=[];
  for(const u of [...new Set(links)].filter(u=>u.startsWith('http://localhost'))){const r=await p.request.get(u);st.push(r.status()+' '+u.replace('http://localhost:8766/',''))}
  const imgs=await p.$$eval('#iron-cotton img',is=>is.map(i=>i.naturalWidth));
  console.log(w,'links',st,'imgs',imgs,'errors',errs,'bad',bad,'sw',await p.evaluate(()=>document.documentElement.scrollWidth));await p.close()}
 await b.close()})();
