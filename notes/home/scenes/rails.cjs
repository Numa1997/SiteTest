// Film the right margin of the home page (the globes in the wind) after scrolling: frames every STEP s, cropped to the margin.
// node notes/home/scenes/rails.cjs <tag> [width]   (serves dist/ on :8766)
const { chromium } = require('playwright'), fs = require('fs');
const tag = process.argv[2] || 'now', w = +(process.argv[3] || 1920), DIR = `notes/home/scenes/${tag}`, STEP = +(process.env.STEP || 2), N = +(process.env.N || 14);
fs.mkdirSync(DIR, { recursive: true });
(async () => { const b = await chromium.launch(), p = await b.newPage({ viewport: { width: w, height: 1080 } }), errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto((process.env.BASE || 'http://localhost:8766/') + 'index.html', { waitUntil: 'networkidle' }); await p.evaluate(() => scrollTo(0, 900)); await p.waitForTimeout(3000);
  const g = await p.evaluate(() => { const s = document.querySelector('[data-bg=rails]').__bgScene; return { r0: s.g && s.g.r0, r1: s.g && s.g.r1, ok: s.ok, err: s.err || null, data: !!s.D, sha_ok: s.D && s.D.sha_ok, beams: (s.Bs || []).length, pairs: 0 }; });
  console.log(w, JSON.stringify(g), 'errors', errs.length, errs.slice(0, 3));
  if (!g.ok) { await b.close(); return; }
  for (let k = 0; k < N; k++) { await p.screenshot({ path: `${DIR}/rails-${w}-${String(k).padStart(2, '0')}.png`, clip: { x: Math.max(0, g.r0 - 10), y: 0, width: Math.min(w, g.r1 + 10) - Math.max(0, g.r0 - 10), height: 1080 } }); await p.waitForTimeout(STEP * 1000); }
  await b.close(); })();
