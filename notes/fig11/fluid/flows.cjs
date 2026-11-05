// project 05 with a medium and a flow: page errors, the book, the Q check (Simpson vs Gauss), replay of the last steps, P check; screenshots
const { chromium } = require('playwright'); const path = require('path');
const BASE = process.env.BASE || 'file:///home/user/SiteTest/public/';
const CASES = process.env.CASES ? JSON.parse(process.env.CASES) : [['vacuum', 'still'], ['air', 'still'], ['air', 'breeze'], ['air', 'gusts'], ['air', 'ground'], ['air', 'lorry'], ['air', 'fan'], ['air', 'eddy'], ['water', 'river'], ['water', 'waves'], ['air', 'shear'], ['air', 'jets'], ['honey', 'cells'], ['air', 'street'], ['water', 'still'], ['glycerol', 'still'], ['honey', 'still']];
(async () => { const b = await chromium.launch();
  for (const [med, flow] of CASES) {
    const pg = await b.newPage({ viewport: { width: 1366, height: 625 } }), errs = []; pg.on('pageerror', e => errs.push(e.message));
    await pg.goto(BASE + 'simulations/double-inverted-pendulum.html'); await pg.waitForTimeout(1200);
    await pg.evaluate(([m, f]) => { const M = document.getElementById('med'), F = document.getElementById('flow'); M.value = m; M.dispatchEvent(new Event('change')); F.value = f; F.dispatchEvent(new Event('change')); }, [med, flow]);
    await pg.waitForTimeout(+(process.env.WAIT || 4000));
    const r = await pg.evaluate(() => { const ds = DIPC.ds, ch = Sim.data.check, g = (n) => ds.get(n);
      const Q = Array.from(g('Q_fl')), Qc = [0, 1, 2].map(i => ch.Q_fl(i).value), n = g('st_n'); let rep = 0, cnt = 0;
      for (let r = Math.max(0, n - 300); r < n; r++) { if (g('st_kind')[r] !== 0 || g('st_ver')[r] !== g('ver')) continue; for (let i = 0; i < 6; i++) { const c = ch.st_s1(6 * r + i); rep = Math.max(rep, Math.abs(c.value - g('st_s1')[6 * r + i])); } cnt++; }
      return { med: g('medium'), flow: g('flow'), t: g('t'), x: g('x'), th1: g('th1w'), th2: g('th2w'), mode: g('mode'), lost: g('lost'), Q, dQ: Q.map((v, i) => Math.abs(v - Qc[i])), P: g('P_fl'), dP: Math.abs(ch.P_fl().value - g('P_fl')), W: g('W_fl'), bal: g('bal'), E: g('E'), Re: g('Re_tip'), replayed: cnt, maxReplay: rep, dGu: Math.abs(ch.fg_u(200).value - g('fg_u')[200]), f: Array.from(g('f')), df: [0, 1].map(i => Math.abs(ch.f(i).value - g('f')[i])) }; });
    await pg.evaluate(() => window.scrollTo(0, document.getElementById('stage').getBoundingClientRect().top + scrollY - 8)); await pg.waitForTimeout(300);
    await pg.screenshot({ path: path.join(process.env.OUT || __dirname, `flu-${med}-${flow}.png`) });
    const fx = (v, d = 3) => (typeof v === 'number' ? (Math.abs(v) < 1e-3 && v !== 0 ? v.toExponential(2) : v.toFixed(d)) : v);
    console.log(`${med}/${flow}`.padEnd(17), 't', fx(r.t, 1), 'x', fx(r.x), 'θ', fx(r.th1), fx(r.th2), r.mode, r.lost ? 'LOST' : '', '| Q', r.Q.map(v => fx(v)).join(' '), 'ΔQ', r.dQ.map(v => v.toExponential(1)).join(' '),
      '| P', fx(r.P), 'ΔP', r.dP.toExponential(1), 'W', fx(r.W), 'bal', fx(r.bal), '| Re', fx(r.Re, 0), '| replay', r.replayed, r.maxReplay.toExponential(1), 'Δgrid', r.dGu.toExponential(1), 'Δf', r.df.map(v => v.toExponential(1)).join(' '), '| errors', errs.join('|') || 'none');
    await pg.close(); }
  await b.close(); })();
