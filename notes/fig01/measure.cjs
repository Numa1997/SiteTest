// Fig. 1: measure the page's own numbers in headless Chromium.
// Run: node notes/fig01/measure.cjs   (with notes/fig01/serve.cjs serving /tmp/fig01-dist on port 8701)
const { execSync } = require('child_process');
const { chromium } = require(execSync('npm root -g').toString().trim() + '/playwright');
const URL = 'http://localhost:8701/simulations/' + encodeURIComponent('Circular Wave Interference Visualization.html');
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const browser = await chromium.launch();
  const out = {};

  // 1. grid on each screen
  out.grids = [];
  for (const [w, h] of [[1280, 900], [1440, 900], [1600, 900], [880, 900], [390, 844]]) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    await page.goto(URL); await sleep(800);
    out.grids.push(await page.evaluate(([w]) => { const d = Sim.data.ds; return { window: w, box: d.get('box_w') + ' x ' + d.get('box_h'), grid: d.get('cols') + ' x ' + d.get('rows'), P: d.get('P'), worldH: +d.get('worldH').toFixed(3), y_s: +d.get('y_s').toFixed(3), y_centre: +d.get('y')[d.get('j_c')].toFixed(3) }; }, [w]));
    await page.close();
  }

  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(URL); await sleep(1000);

  // 2. crest speed straight up the middle of the two Reset sources, from the stored C and S maps
  await page.click('#reset'); await sleep(200);
  if (await page.evaluate(() => Sim.data.playing())) await page.click('#play');
  await sleep(300);
  out.crest_gradient = await page.evaluate(() => {
    const d = Sim.data.ds, C = d.get('C'), S = d.get('S'), cols = d.get('cols'), rows = d.get('rows');
    const xs = d.get('x'), ys = d.get('y'), jc = d.get('j_c'), ic = d.get('i_c'), f = d.get('f'), v = d.get('v');
    const arg = (j, i) => Math.atan2(S[j * cols + i], C[j * cols + i]);
    const wrap = a => Math.atan2(Math.sin(a), Math.cos(a));
    const res = [];
    for (const i of [ic - 1, ic]) {
      const gx = wrap(arg(jc, i + 1) - arg(jc, i - 1)) / (xs[i + 1] - xs[i - 1]);
      const gy = wrap(arg(jc + 1, i) - arg(jc - 1, i)) / (ys[jc + 1] - ys[jc - 1]);
      const speed = 2 * Math.PI * f / Math.hypot(gx, gy);
      res.push({ i, x: +xs[i].toFixed(2), y: +ys[jc].toFixed(2), local_wavelength_px: +(2 * Math.PI / Math.hypot(gx, gy)).toFixed(2), crest_speed: +speed.toFixed(2), v, ratio: +(speed / v).toFixed(4) });
    }
    return res;
  });

  // 3. the same, measured by following one crest up the column next to x = 400 px while the page plays
  const snap = () => page.evaluate(() => {
    const d = Sim.data.ds, psi = d.get('psi'), cols = d.get('cols'), rows = d.get('rows'), ic = d.get('i_c') - 1;
    const col = []; for (let j = 0; j < rows; j++) col.push(psi[j * cols + ic]);
    return { omegaT: d.get('omegaT'), f: d.get('f'), v: d.get('v'), dy: d.get('dy'), ys: Array.from(d.get('y')), col, jc: d.get('j_c'), x: d.get('x')[ic] };
  });
  const crestNear = (s, y0) => { // crest = local maximum of psi; parabolic refinement
    let best = null;
    for (let j = 1; j < s.col.length - 1; j++) if (s.col[j] > s.col[j - 1] && s.col[j] >= s.col[j + 1] && s.col[j] > 0.2) {
      const a = s.col[j - 1], b = s.col[j], c = s.col[j + 1], off = 0.5 * (a - c) / (a - 2 * b + c);
      const y = s.ys[j] + off * s.dy;
      if (!best || Math.abs(y - y0) < Math.abs(best - y0)) best = y;
    }
    return best;
  };
  out.crest_track = [];
  for (let run = 0; run < 3; run++) {
    const a = await snap();
    await page.click('#play'); await sleep(250); await page.click('#play'); await sleep(150);
    const b = await snap();
    const ya = crestNear(a, a.ys[a.jc]), yb = crestNear(b, ya - 5);
    const dt = (b.omegaT - a.omegaT) / (2 * Math.PI * a.f);
    out.crest_track.push({ x: +a.x.toFixed(2), y_from: +ya.toFixed(2), y_to: +yb.toFixed(2), dt_s: +dt.toFixed(4), speed: +((ya - yb) / dt).toFixed(2), v: a.v, ratio: +(((ya - yb) / dt) / a.v).toFixed(3) });
  }

  // 4. Line of 16: rebuild and frame times
  out.line16 = [];
  for (let run = 0; run < 3; run++) {
    await page.click('#line'); await sleep(400);
    out.line16.push(await page.evaluate(() => { const d = Sim.data.ds; return { N: d.get('N'), trig_calls: d.get('trig_calls'), build_ms: +d.get('build_ms').toFixed(1) }; }));
  }
  await page.click('#play'); await sleep(1500);
  const draws = [];
  for (let q = 0; q < 10; q++) { draws.push(await page.evaluate(() => Sim.data.ds.get('draw_ms'))); await sleep(97); }
  out.line16_draw_ms = { min: +Math.min(...draws).toFixed(2), max: +Math.max(...draws).toFixed(2) };
  await page.click('#play');

  // 5. far field of Line of 16 from the page's stored inputs (x_s, y_s, k, g): eq. (12) against the exact sum,
  //    without damping and with the page's damping (normalised by the sum of the arrow lengths), at 10^6 px
  out.farfield = await page.evaluate(() => {
    const d = Sim.data.ds, xs = Array.from(d.get('x_s')), ys = d.get('y_s'), k = d.get('k'), g = d.get('g'), N = xs.length;
    const s = xs[1] - xs[0], xc = (xs[0] + xs[N - 1]) / 2, Rf = 1e6;
    let worst0 = 0, worstG = 0, at = 0;
    for (let q = -900; q <= 900; q++) {
      const th = q / 10 * Math.PI / 180, beta = k * s * Math.sin(th);
      const F = Math.abs(Math.sin(N * beta / 2) / (N * Math.sin(beta / 2))) || 1;
      const px = xc + Rf * Math.sin(th), py = ys - Rf * Math.cos(th);
      let re0 = 0, im0 = 0, re = 0, im = 0, wsum = 0;
      for (const x of xs) {
        const r = Math.hypot(px - x, py - ys), w = Math.exp(-g * (r - Rf));
        re0 += Math.cos(k * r); im0 += Math.sin(k * r);
        re += w * Math.cos(k * r); im += w * Math.sin(k * r); wsum += w;
      }
      const d0 = Math.abs(Math.hypot(re0, im0) / N - F), dg = Math.abs(Math.hypot(re, im) / wsum - F);
      if (d0 > worst0) worst0 = d0;
      if (dg > worstG) { worstG = dg; at = q / 10; }
    }
    return { N, s, lambda: d.get('lambda'), gamma: d.get('damp'), max_diff_gamma0: worst0, max_diff_with_damping: worstG, at_deg: at };
  });
  // the same at the largest damping
  await page.evaluate(() => { const el = document.getElementById('damp'); el.value = 0.6; el.dispatchEvent(new Event('input', { bubbles: true })); });
  await sleep(400);
  out.farfield_06 = await page.evaluate(() => {
    const d = Sim.data.ds, xs = Array.from(d.get('x_s')), ys = d.get('y_s'), k = d.get('k'), g = d.get('g'), N = xs.length;
    const s = xs[1] - xs[0], xc = (xs[0] + xs[N - 1]) / 2, Rf = 1e6;
    let worstG = 0, at = 0;
    for (let q = -900; q <= 900; q++) {
      const th = q / 10 * Math.PI / 180, beta = k * s * Math.sin(th);
      const F = Math.abs(Math.sin(N * beta / 2) / (N * Math.sin(beta / 2))) || 1;
      const px = xc + Rf * Math.sin(th), py = ys - Rf * Math.cos(th);
      let re = 0, im = 0, wsum = 0;
      for (const x of xs) { const r = Math.hypot(px - x, py - ys), w = Math.exp(-g * (r - Rf)); re += w * Math.cos(k * r); im += w * Math.sin(k * r); wsum += w; }
      const dg = Math.abs(Math.hypot(re, im) / wsum - F);
      if (dg > worstG) { worstG = dg; at = q / 10; }
    }
    return { gamma: d.get('damp'), g, max_diff_with_damping: worstG, at_deg: at };
  });

  out.errors = errors;
  console.log(JSON.stringify(out, null, 1));
  await browser.close();
})();
