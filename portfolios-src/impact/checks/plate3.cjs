const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'});
 const p=await b.newPage({viewport:{width:680,height:1000},deviceScaleFactor:2});
 await p.goto('http://localhost:8766/portfolios/impact/index.html');await p.waitForFunction(()=>computed>=NF,null,{timeout:180000});await p.evaluate(()=>document.fonts.ready);
 await p.click('#drop');await p.evaluate(()=>setSpeed(1));await p.evaluate(()=>{tPlay=8.9});await p.waitForFunction(()=>!playing,null,{timeout:60000});await p.waitForTimeout(200);
 await (await p.$('#en')).screenshot({path:'/tmp/p03.png'});await b.close()})();
