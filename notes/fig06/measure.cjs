// Fig. 6 measurements in headless Chromium: the page's own store and readouts, and the page checks
// (console errors, KaTeX errors, sideways scroll, folds). Needs the build served by serve.cjs.
// Run: node notes/fig06/measure.cjs [out.json]
'use strict';
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const URL = 'http://127.0.0.1:8606/simulations/wave-interference.html';
const wait = ms => new Promise(r => setTimeout(r, ms));

async function run(vw, vh, full) {
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: vw, height: vh } });
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', e => errors.push(String(e)));
    await page.goto(URL, { waitUntil: 'networkidle' });
    await page.waitForFunction(() => document.querySelector('.paper.is-typeset'));
    await wait(600);
    const R = { viewport: vw + ' x ' + vh };
    const ds = k => page.evaluate(k => { const v = Sim.data.ds.get(k); return (v && v.length !== undefined) ? Array.from(v) : v; }, k);
    const click = sel => page.evaluate(s => document.querySelector(s).click(), sel);
    const setSlider = (card, which, v) => page.evaluate(([c, w, v]) => {
        const inp = document.querySelectorAll('.wave')[c].querySelector('input[id$="' + w + '"]');
        inp.value = v; inp.dispatchEvent(new Event('input', { bubbles: true }));
        return inp.value;
    }, [card, which, String(v)]);
    const readout = () => page.evaluate(() => ({ sum: document.getElementById('r-sum').textContent, peak: document.getElementById('r-peak').textContent }));
    R.layout = { box_w: await ds('box_w'), box_h: await ds('box_h'), M: await ds('M'), dX: await ds('dX'), spec_w: await ds('spec_w'), spec_h: await ds('spec_h') };

    // pause, so every number belongs to one instant
    if (await page.evaluate(() => Sim.data.playing())) await click('#play');
    await wait(300);

    // Section 3.1: One wave, then Add wave +, then Phase of Wave 2 to its nearest step to pi
    await click('#p-one'); await click('#add'); await wait(400);
    R.twoCopies = { peak: await ds('peak'), A_line: await ds('A_line'), readout: await readout() };
    R.twoCopies.phaseSet = await setSlider(1, 'p', 3.15); await wait(400);
    R.twoCopies.after = { phi: await ds('phi'), peak: await ds('peak'), A_line: await ds('A_line'), readout: await readout(),
        phaseLabel: await page.evaluate(() => document.querySelectorAll('.wave')[1].querySelector('output[id$="p-out"]').textContent) };

    // Section 4 and Exercise 4.1
    await click('#p-beats'); await wait(300);
    R.beats = { bl: await ds('bl'), venv: await ds('venv'), nu: await ds('nu') };
    await setSlider(1, 'f', 1.1); await wait(300);
    R.beats.f110 = { f: await ds('f'), bl: await ds('bl') };
    await setSlider(1, 'f', 1.25); await setSlider(1, 's', 0.5); await wait(300);
    R.beats.s050 = { s: await ds('s'), v: await ds('v'), venv: await ds('venv') };

    // Sections 5, 6, 8 and Exercise 6.1: Square wave
    await click('#p-square'); await wait(400);
    R.square = { A: await ds('A'), f: await ds('f'), sum_A: await ds('sum_A'), R: await ds('R'), hSum: await ds('hSum'), peak: await ds('peak'), readout: await readout(),
        card4Amp: await page.evaluate(() => document.querySelectorAll('.wave')[3].querySelector('output[id$="A-out"]').textContent),
        round: await page.evaluate(() => Sim.data.round.length()), A_line: await ds('A_line'), nu_line: await ds('nu_line') };
    await page.evaluate(() => document.querySelectorAll('.wave')[3].querySelector('.wave__x').click()); await wait(400);
    await wait(600); R.square.noWave4 = { N: await ds('N'), peak: await ds('peak'), readout: await readout() };
    await click('#p-square'); await wait(200);
    await setSlider(1, 'p', 3.15); await wait(400);
    R.square.phase2 = { peak: await ds('peak'), readout: await readout(), A_line: await ds('A_line'),
        phaseLabel: await page.evaluate(() => document.querySelectorAll('.wave')[1].querySelector('output[id$="p-out"]').textContent) };

    if (full) {
        R.katexErrors = await page.evaluate(() => document.querySelectorAll('.katex-error').length);
        R.sideways = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
        // folds: close all, then open every fold by its own toggle, outermost first
        R.folds = await page.evaluate(async () => {
            const nodes = Array.from(document.querySelectorAll('[data-fold-level]'));
            const tools = Array.from(document.querySelectorAll('.fold-tool'));
            const collapse = tools.find(b => b.textContent === 'Collapse all');
            if (collapse) collapse.click();
            await new Promise(r => setTimeout(r, 200));
            const closed = nodes.filter(n => n.getAttribute('data-collapsed') === '1').length;
            const sorted = nodes.slice().sort((a, b) => (+a.getAttribute('data-fold-level')) - (+b.getAttribute('data-fold-level')));
            for (const n of sorted) {
                const btn = n.querySelector(':scope > .fs-head .fs-toggle');
                if (btn && n.getAttribute('data-collapsed') === '1') btn.click();
                await new Promise(r => setTimeout(r, 30));
            }
            await new Promise(r => setTimeout(r, 600));
            const open = nodes.filter(n => n.getAttribute('data-collapsed') === '0').length;
            return { folds: nodes.length, closedAfterCollapseAll: closed, openAfterToggles: open };
        });
        await page.evaluate(() => document.getElementById('paper').scrollIntoView());
        await wait(300);
        R.sidewaysAfterFolds = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
        R.prefsLinks = await page.evaluate(() => Array.from(document.querySelectorAll('.prefs a')).map(a => a.href));
        R.eqTags = await page.evaluate(() => Array.from(document.querySelectorAll('#paper .katex-display .tag')).map(t => t.textContent.trim()));
        const shot = process.env.SHOT_DIR;
        if (shot) {
            for (const id of ['p-beat', 'p-spectrum', 'p-limits']) {
                const el = await page.$('#' + id);
                await el.screenshot({ path: shot + '/' + id + '-' + vw + '.png' });
            }
        }
    }
    R.consoleErrors = errors;
    await browser.close();
    return R;
}
(async () => {
    const out = { wide: await run(1440, 900, true), phone: await run(390, 844, true) };
    const s = JSON.stringify(out, null, 1);
    if (process.argv[2]) fs.writeFileSync(process.argv[2], s);
    console.log(s);
})();
