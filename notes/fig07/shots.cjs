// Screenshots of the edited paragraphs, 1440 and 390 px wide. node notes/fig07/shots.cjs
'use strict';
const { execSync } = require('child_process');
const { chromium } = require(execSync('npm root -g').toString().trim() + '/playwright');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const [w, h] of [[1440, 900], [390, 844]]) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    await page.goto('http://localhost:8707/simulations/phasor-sums.html', { waitUntil: 'load' });
    await page.waitForFunction(() => document.querySelectorAll('#paper .katex').length > 50);
    await page.waitForTimeout(800);
    const targets = [['closure', '#p-closure p:nth-of-type(2)', '#p-closure p:nth-of-type(4)'], ['refs', '#p-limits .prefs', '#p-limits .prefs'], ['record', '#p-screen > p:last-of-type, #p-screen .fs-fold p:last-of-type', null]];
    for (const [name, a, b] of targets) {
      const box = await page.evaluate(([a, b]) => {
        const A = document.querySelector(a); if (!A) return null;
        const B = b ? document.querySelector(b) : A; A.scrollIntoView({ block: 'center' });
        const r1 = A.getBoundingClientRect(), r2 = B.getBoundingClientRect();
        return { x: Math.min(r1.left, r2.left) - 8, y: r1.top + window.scrollY - 8, w: Math.max(r1.right, r2.right) - Math.min(r1.left, r2.left) + 16, h: r2.bottom - r1.top + 16 };
      }, [a, b]);
      if (!box) { console.log('missing', name); continue; }
      await page.screenshot({ path: `${__dirname}/edit-${name}-${w}.png`, fullPage: true, clip: { x: Math.max(0, box.x), y: box.y, width: Math.min(box.w, w), height: box.h } });
    }
    await page.close();
  }
  await browser.close();
  console.log('done');
})();
