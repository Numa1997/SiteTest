// Fig. 10 measurements, scratch. Runs the built page (/tmp/fig10-dist) in headless Chromium and reads its own store
// (window.Sim.data.ds). For the step-size study the page is served with only the line
//   var H = 0.01, TEND = 120, EVERY = 2, ...   (L555)
// changed to H = 0.005, EVERY = 4 (and H = 0.02, EVERY = 1), so that the 6 001 stored rows fall at the same times.
// Build first:  cd /home/user/SiteTest && APPDEPLOY_VITE_OUT_DIR=/tmp/fig10-dist npm run build
// Run:          node notes/fig10/measure.cjs  > notes/fig10/measure-out.json
'use strict';
const http = require('http'), fs = require('fs'), path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
const ROOT = '/tmp/fig10-dist', PORT = 8710;
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.webp': 'image/webp', '.json': 'application/json' };
const server = http.createServer((req, res) => {
    const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
    fs.readFile(p, (err, data) => {
        if (err) { res.writeHead(404); res.end(); return; }
        res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); res.end(data);
    });
});
const ORIG = 'var H = 0.01, TEND = 120, EVERY = 2,';
const COMBOS = [['pi', 'steady'], ['opt', 'steady'], ['pi', 'gust'], ['opt', 'gust'], ['pi', 'step'], ['opt', 'step'], ['pi', 'turb'], ['opt', 'turb']];

async function run(browser, h, every) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const errors = [];
    page.on('pageerror', e => errors.push(String(e)));
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    if (h !== 0.01) {
        await page.route('**/wind-turbine.html', async route => {
            const body = fs.readFileSync(path.join(ROOT, 'simulations/wind-turbine.html'), 'utf8');
            if (body.indexOf(ORIG) < 0) throw new Error('step line not found');
            await route.fulfill({ contentType: 'text/html', body: body.replace(ORIG, 'var H = ' + h + ', TEND = 120, EVERY = ' + every + ',') });
        });
    }
    await page.goto('http://127.0.0.1:' + PORT + '/simulations/wind-turbine.html');
    await page.waitForFunction(() => window.Sim && Sim.data && Sim.data.ds && Sim.data.ds.get('Eg_end') > 0);
    const res = {};
    for (const [ctrl, prof] of COMBOS) {
        await page.click('#ctrl button[data-v="' + ctrl + '"]');
        await page.click('#prof button[data-v="' + prof + '"]');
        await page.click('#solve');
        res[ctrl + '/' + prof] = await page.evaluate(() => {
            const ds = Sim.data.ds, g = n => ds.get(n);
            const om = Array.from(g('om')), rpm = Array.from(g('rpm')), vw = Array.from(g('vw')), tg = Array.from(g('tg')), cpv = Array.from(g('cpv'));
            const ts = Array.from(g('ts'));
            const mean = vw.reduce((s, x) => s + x, 0) / vw.length;
            const sd = Math.sqrt(vw.reduce((s, x) => s + (x - mean) * (x - mean), 0) / vw.length);
            // the Step run: overshoot of the rotor speed above the target after the step, and the dip below it after that
            let peak = -Infinity, ipeak = 0;
            for (let n = 0; n < rpm.length; n++) if (ts[n] >= 30 && rpm[n] > peak) { peak = rpm[n]; ipeak = n; }
            let dip = Infinity, idip = ipeak;
            for (let n = ipeak; n < rpm.length; n++) if (rpm[n] < dip) { dip = rpm[n]; idip = n; }
            return {
                kWh: g('Eg_end') / 3.6e6, kW: g('P_mean') / 1000, rpm_min: g('rpm_min'), rpm_max: g('rpm_max'),
                share: g('Ea') / g('Ew'), balance: g('balance'), h: g('h'), steps: g('steps'),
                tg_max: Math.max(...tg), tg_min: Math.min(...tg), tg_at_limit: tg.filter(x => x >= 1.2e6 - 1 || x <= 1).length,
                wind_sd: sd, wind_mean: mean, cp_end: cpv[cpv.length - 1], lam_end: g('lam')[g('lam').length - 1], rpm_end: rpm[rpm.length - 1],
                peak_rpm: peak, t_peak: ts[ipeak], dip_rpm: dip, t_dip: ts[idip], rpm_ref: g('rpm_ref'),
                lam_opt: g('lam_opt'), cp_max: g('cp_max'), K_opt: g('K_opt'), Kp: g('Kp'), Ki: g('Ki'), dtau_dw: g('dtau_dw'), tau0: g('tau0'),
                solve_ms: g('solve_ms'), om
            };
        });
    }
    res.errors = errors;
    await page.close();
    return res;
}

(async () => {
    await new Promise(r => server.listen(PORT, r));
    const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
    const base = await run(browser, 0.01, 2), half = await run(browser, 0.005, 4), dbl = await run(browser, 0.02, 1);
    const out = { errors: { base: base.errors, half: half.errors, dbl: dbl.errors }, combos: {} };
    for (const [ctrl, prof] of COMBOS) {
        const k = ctrl + '/' + prof, b = base[k], hf = half[k], d = dbl[k];
        let e1 = 0, e2 = 0;
        for (let n = 0; n < b.om.length; n++) { e1 = Math.max(e1, Math.abs(b.om[n] - hf.om[n])); e2 = Math.max(e2, Math.abs(d.om[n] - b.om[n])); }
        const rpmOf = w => w * 60 / (2 * Math.PI);
        delete b.om;
        out.combos[k] = Object.assign(b, {
            h_check: [b.h, hf.h, d.h],
            max_domega_h_vs_half_rpm: rpmOf(e1), max_domega_2h_vs_h_rpm: rpmOf(e2), order_ratio: e2 / e1,
            kWh_half: hf.kWh, kWh_dbl: d.kWh, balance_half: hf.balance, balance_dbl: d.balance
        });
    }
    console.log(JSON.stringify(out, null, 1));
    await browser.close(); server.close();
})().catch(e => { console.error(e); process.exit(1); });
