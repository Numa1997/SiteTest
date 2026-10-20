const { execSync } = require('child_process');
const { chromium } = require(execSync('npm root -g').toString().trim() + '/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const [w, h] of [[390, 844], [1440, 900]]) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.goto('http://127.0.0.1:8702/simulations/Double%20Pendulum.html'); await p.waitForTimeout(2000);
    const r = await p.evaluate(() => {
      const body = document.querySelector('#paper .paper__body').getBoundingClientRect();
      return Array.from(document.querySelectorAll('#paper .katex-html, #paper p, #paper li')).filter(e => { const q = e.getBoundingClientRect(); return q.width > 0 && q.right > body.right + 0.5 && !e.closest('.katex-display'); })
        .map(e => ({ sec: e.closest('section') && e.closest('section').id, tag: e.tagName, right: Math.round(e.getBoundingClientRect().right), bodyRight: Math.round(body.right), text: e.textContent.slice(0, 50) }));
    });
    console.log(w, JSON.stringify(r));
    await p.close();
  }
  await b.close();
})();
