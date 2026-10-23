// Make the four plates of the Portfolios entry from the built page (run from a local server of dist/).
const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell'});
 const p=await b.newPage({viewport:{width:1100,height:1000},deviceScaleFactor:2});
 await p.goto('http://localhost:8766/portfolios/impact/index.html');
 await p.waitForFunction(()=>computed>=NF,null,{timeout:300000});await p.evaluate(()=>document.fonts.ready);
 await p.click('#drop');await p.evaluate(()=>setSpeed(20));
 await p.waitForFunction(()=>tPlay>1.447,null,{timeout:60000});await p.evaluate(()=>{playing=false});await p.waitForTimeout(150);
 await (await p.$('#sim')).screenshot({path:'/tmp/p01.png'});
 await p.evaluate(()=>{playing=true;setSpeed(1)});await p.waitForFunction(()=>!playing,null,{timeout:60000});await p.waitForTimeout(200);
 await (await p.$('#sim')).screenshot({path:'/tmp/p04.png'});
 await (await p.$('#pZoom')).screenshot({path:'/tmp/p02.png'});
 await (await p.$('#en')).screenshot({path:'/tmp/p03.png'});
 console.log(await p.evaluate(()=>JSON.stringify({t:tPlay})));
 await b.close();})();
