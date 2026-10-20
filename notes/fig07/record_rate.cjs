// Fig. 7: how often Record takes a snapshot (perform(), L1184-1193), measured in headless Chromium.
'use strict';
const { execSync } = require('child_process');
const { chromium } = require(execSync('npm root -g').toString().trim() + '/playwright');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('http://localhost:8707/simulations/phasor-sums.html', { waitUntil: 'load' });
  await page.waitForTimeout(1500);
  const r = await page.evaluate(async () => {
    const ds = Sim.data.ds, f0 = ds.get('frames');
    document.getElementById('rec').click();
    const t0 = performance.now();
    await new Promise(r => setTimeout(r, 6000));
    const txt = document.getElementById('rec-status').textContent, t1 = performance.now();
    document.getElementById('rec-stop').click();
    const n = +txt.match(/(\d+) snapshots/)[1];
    return { status: txt, seconds: (t1 - t0) / 1000, snapshots: n, ms_per_snapshot: (t1 - t0) / (n - 1), frames: ds.get('frames') - f0, fps: ds.get('fps') };
  });
  console.log(JSON.stringify(r, null, 1));
  await browser.close();
})();
