// Fig. 11 layout check: with the grid scrolled to the top of the window, are the picture and every knob on screen together,
// and do the two control columns stay pinned while the figures scroll? node notes/fig11/layout.cjs [en|de|ar]
const { chromium } = require('playwright');
const lang = process.argv[2] || 'en', pre = lang === 'en' ? '' : lang + '/';
const URL = `${process.env.BASE || 'http://localhost:8765/'}${pre}simulations/pendulum-control.html`;
const KNOBS = ['r', 'qa', 'qx', 'qv', 'rho', 'N0', 'ks', 'Imax', 'speed', 'solve'];
(async () => {
  const b = await chromium.launch();
  for (const [w, hgt] of [[1920, 1080], [1440, 900], [1280, 800], [1100, 900], [390, 844]]) {
    const p = await b.newPage({ viewport: { width: w, height: hgt } }); const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    await p.goto(URL, { waitUntil: 'networkidle' }); await p.waitForTimeout(1500);
    await p.evaluate(() => { const g = document.querySelector('.sim__grid'); window.scrollTo(0, g.getBoundingClientRect().top + scrollY - 8); });
    await p.waitForTimeout(400);
    const look = () => p.evaluate((knobs) => {
      const vh = innerHeight, vis = el => { const r = el.getBoundingClientRect(); return r.bottom > 0 && r.top < vh && r.width > 0 ? Math.max(0, Math.min(r.bottom, vh) - Math.max(r.top, 0)) / r.height : 0; };
      const st = document.getElementById('stage'), out = { stage: +vis(st).toFixed(2), knobs: {} };
      for (const k of knobs) { const el = document.getElementById(k); out.knobs[k] = el ? +(vis(el) > 0.99) : 'missing'; }
      const take = document.querySelector('.take'), pan = document.querySelector('.sim__grid > .panel');
      out.takeScroll = take.scrollHeight - take.clientHeight; out.panelScroll = pan.scrollHeight - pan.clientHeight;
      out.sideways = document.documentElement.scrollWidth - document.documentElement.clientWidth;
      return out;
    }, KNOBS);
    const top = await look();
    await p.screenshot({ path: `notes/fig11/shots/layout-${lang}-${w}.png` });
    await p.mouse.wheel(0, 500); await p.waitForTimeout(400);
    const down = await look();
    const on = o => Object.values(o.knobs).filter(v => v === 1).length;
    const tab = await p.$('.dp-tab'); let open = null;
    if (tab && w >= 1100) { if (!(await p.evaluate(() => document.body.classList.contains('dp-open')))) await tab.click(); await p.waitForTimeout(900); open = await p.evaluate(() => ({ stage: Math.round(document.getElementById('stage').getBoundingClientRect().width), cols: getComputedStyle(document.querySelector('.sim__grid')).gridTemplateColumns.split(' ').length, side: document.documentElement.scrollWidth - document.documentElement.clientWidth })); await p.screenshot({ path: `notes/fig11/shots/layout-open-${lang}-${w}.png` }); }
    console.log(`${lang} ${w}×${hgt}: errors ${errs.length} · at the grid's top: picture ${Math.round(top.stage * 100)}% on screen, knobs on screen ${on(top)}/${KNOBS.length} · 500 px further down: knobs ${on(down)}/${KNOBS.length} · inner scroll take ${top.takeScroll} px, panel ${top.panelScroll} px · sideways ${top.sideways} px` + (open ? ` · data panel open: ${open.cols} columns, picture ${open.stage} px wide, sideways ${open.side} px` : ''));
    await p.close();
  }
  await b.close();
})();
