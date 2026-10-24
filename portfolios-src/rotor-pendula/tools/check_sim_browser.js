#!/usr/bin/env node
// Browser check of rotor_sim.html in headless Chromium (Playwright), at 360, 390, 1024 and 1440 px:
//  1. loads the page, waits for the default solve, plays; no console errors or page errors;
//  2. horizontal overflow of the page must be 0;
//  3. a hover sweep across the scene and the three plots (playback paused, Read values off, then on) changes nothing:
//     the page's text and the pixels of every canvas are compared before and after;
//  4. Read values: switch it on, click the rod-angle plot, check the pin's marker is drawn (alpha first, then colour, at the
//     ring around the pinned point), then play for 5 s and count how often the readout strip's text changes (must be about
//     4 per second at most);
//  5. screenshots of the page top and of the plots;
//  6. at the widest width, every "Try it" button of the worked solutions sets the page and solves it without an error.
// Usage: node tools/check_sim_browser.js [outdir]
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');             // the preinstalled Playwright and its own Chromium

const PAGE = 'file://' + path.join(__dirname, '..', 'rotor_sim.html');
const OUT = process.argv[2] || path.join(require('os').tmpdir(), 'rotor_sim_shots');
fs.mkdirSync(OUT, { recursive: true });
const WIDTHS = [360, 390, 1024, 1440];

async function canvasHashes(page) {
  return page.evaluate(() => [...document.querySelectorAll('canvas')].map(c => {
    const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
    let h = 2166136261;
    for (let i = 0; i < d.length; i += 7) h = Math.imul(h ^ d[i], 16777619) >>> 0;
    return c.id + ':' + c.width + 'x' + c.height + ':' + h;
  }));
}
const bodyText = page => page.evaluate(() => document.body.innerText);

async function hoverSweep(page) {
  for (const sel of ['#scene', '#plotTh', '#plotP', '#plotK']) {
    const box = await page.locator(sel).boundingBox();
    if (!box) continue;
    for (let i = 0; i <= 24; i++) {
      await page.mouse.move(box.x + 2 + (box.width - 4) * i / 24, box.y + box.height * (0.2 + 0.6 * ((i % 5) / 4)));
    }
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 5 });
  }
  await page.mouse.move(2, 2);
  await page.waitForTimeout(400);
}

(async () => {
  const browser = await chromium.launch();
  let allPass = true;
  const report = [];
  for (const W of WIDTHS) {
    const ctx = await browser.newContext({ viewport: { width: W, height: 900 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', e => errors.push(String(e)));
    await page.goto(PAGE);
    await page.waitForFunction(() => window.rotorSim && window.rotorSim.solved(), null, { timeout: 60000 });
    await page.waitForTimeout(1500);                                     // play a little
    const r = { width: W };
    r.overflow = await page.evaluate(() => Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth));
    r.wideElements = await page.evaluate(() => {
      const vw = document.documentElement.clientWidth;
      return [...document.querySelectorAll('body *')].filter(e => { const b = e.getBoundingClientRect(); return b.width > 0 && b.right > vw + 0.5; })
        .slice(0, 5).map(e => e.tagName + (e.id ? '#' + e.id : '') + '.' + e.className);
    });
    await page.screenshot({ path: path.join(OUT, `sim_${W}_top.png`) });

    // 3. hover sweep with playback paused: nothing may change
    await page.evaluate(() => window.rotorSim.pause());
    await page.waitForTimeout(500);
    const t0 = await bodyText(page), c0 = await canvasHashes(page);
    await hoverSweep(page);
    const t1 = await bodyText(page), c1 = await canvasHashes(page);
    r.hoverTextSame = t0 === t1;
    r.hoverPixelsSame = JSON.stringify(c0) === JSON.stringify(c1);

    // 4. Read values on: the hover sweep still changes nothing; then pin by a click
    await page.click('#readBtn');
    await page.waitForTimeout(400);
    const t2 = await bodyText(page), c2 = await canvasHashes(page);
    await hoverSweep(page);
    const t3 = await bodyText(page), c3 = await canvasHashes(page);
    r.hoverReadSame = t2 === t3 && JSON.stringify(c2) === JSON.stringify(c3);
    await page.locator('#plotTh').scrollIntoViewIfNeeded();
    const box2 = await page.locator('#plotTh').boundingBox();
    const cx = box2.x + box2.width * 0.62, cy = box2.y + box2.height / 2;
    await page.mouse.click(cx, cy);
    await page.waitForTimeout(400);
    // precise check at the ring: the page draws the ring at (X(turn), Y(theta)); ask the page where
    r.ring = await page.evaluate(() => {
      const cv = document.getElementById('plotTh'), ctx = cv.getContext('2d');
      const s = cv.width / cv.clientWidth;
      const mp = window.rotorSim.pinXY();
      if (!mp) return null;
      const out = [];
      for (let a = 0; a < 16; a++) {
        const x = Math.round((mp.x + 7 * Math.cos(a * Math.PI / 8)) * s), y = Math.round((mp.y + 7 * Math.sin(a * Math.PI / 8)) * s);
        const d = ctx.getImageData(x, y, 1, 1).data;
        out.push([d[0], d[1], d[2], d[3]]);
      }
      const drawn = out.filter(p => p[3] > 200).length;
      const wineish = out.filter(p => p[3] > 200 && p[0] > p[1] + 40 && p[0] > p[2] + 30).length;
      return { at: mp, samples: 16, opaque: drawn, wine: wineish };
    });
    // count rewrites of the strip during 5 s of playback
    await page.click('#play');
    const changes = await page.evaluate(() => new Promise(res => {
      const el = document.getElementById('readout'), lab = document.getElementById('turnLbl');
      let n = 0, nl = 0, last = el.innerHTML, lastL = lab.textContent;
      const ob = new MutationObserver(() => { if (el.innerHTML !== last) { n++; last = el.innerHTML; } if (lab.textContent !== lastL) { nl++; lastL = lab.textContent; } });
      ob.observe(el, { childList: true, subtree: true, characterData: true });
      ob.observe(lab, { childList: true, subtree: true, characterData: true });
      setTimeout(() => { ob.disconnect(); res({ strip: n, turnLabel: nl, seconds: 5 }); }, 5000);
    }));
    r.stripPerSecond = changes.strip / changes.seconds;
    r.turnLabelPerSecond = changes.turnLabel / changes.seconds;
    // whole-page text rewrite rate during playback
    r.pageTextPerSecond = await page.evaluate(() => new Promise(res => {
      let n = 0, last = document.body.innerText;
      const iv = setInterval(() => { const t = document.body.innerText; if (t !== last) { n++; last = t; } }, 20);
      setTimeout(() => { clearInterval(iv); res(n / 3); }, 3000);
    }));
    await page.locator('#plotTh').scrollIntoViewIfNeeded();
    await page.screenshot({ path: path.join(OUT, `sim_${W}_plots.png`) });
    await page.screenshot({ path: path.join(OUT, `sim_${W}_full.png`), fullPage: true });
    if (W === WIDTHS[WIDTHS.length - 1]) {        // 6. the worked solutions' buttons
      const n = await page.locator('#solutions [data-apply]').count();
      r.tryButtons = { n, solved: 0 };
      for (let i = 0; i < n; i++) {
        await page.locator('#solutions [data-apply]').nth(i).click();
        await page.waitForTimeout(300);
        await page.waitForFunction(() => window.rotorSim.solved(), null, { timeout: 120000 });
        r.tryButtons.solved++;
      }
    }
    r.errors = errors;
    r.pass = (!r.tryButtons || r.tryButtons.solved === r.tryButtons.n) && r.overflow === 0 && errors.length === 0 && r.hoverTextSame && r.hoverPixelsSame && r.hoverReadSame &&
      r.ring && r.ring.opaque >= 8 && r.ring.wine >= 4 && r.stripPerSecond <= 4.4 && r.turnLabelPerSecond <= 4.4 && r.pageTextPerSecond <= 4.4;
    allPass = allPass && r.pass;
    report.push(r);
    console.log(JSON.stringify(r));
    await ctx.close();
  }
  await browser.close();
  console.log(allPass ? 'ALL PASS' : 'FAIL');
  process.exit(allPass ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
