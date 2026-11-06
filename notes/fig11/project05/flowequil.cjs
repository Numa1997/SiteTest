// Numa, 6 Nov 2026: "reach the arms whatever the equilibrium equivalent is according to the vector field".
// Feasibility, with the flow KNOWN (the scan and learning come later): in a steady stream, find the rest states of the rods with the cart held still,
// θ̈ = 0 and ẍ = 0 at θ̇ = ẋ = 0 for some steady motor force u*; linearise the page's full equations there (finite differences of rhs),
// design the page's sampled LQR (dlqr, Q as the page, ρ = 1, T_s = 10 ms) for that rest state, and hold it for 30 s with u = sat(u* − K(s − s*)).
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1200);
  const cases = (process.env.CASES || 'water:breeze:0.3,water:breeze:0.6,glycerol:breeze:0.1,glycerol:breeze:0.3,honey:breeze:0.05,honey:breeze:0.15').split(',');
  for (const c of cases) {
    const [med, fl, U] = c.split(':');
    const r = await pg.evaluate(([m, fl, U]) => {
      const set = (id, v, ev) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event(ev, { bubbles: true })); };
      set('med', m, 'change'); set('flow', fl, 'change'); set('Uf', U, 'input');
      const p = DIPC.p, F = 60, acc = (z) => DIPC.rhs(p, [0, z[0], z[1], 0, 0, 0], z[2], 0).slice(3, 6);
      const newton = (z) => { for (let it = 0; it < 60; it++) { const f = acc(z), J = [0, 1, 2].map(j => { const e = 1e-6, zz = z.slice(); zz[j] += e; const g = acc(zz); return g.map((v, i) => (v - f[i]) / e); });
          // solve J^T-columns system: J[j][i] = ∂f_i/∂z_j
          const A = [0, 1, 2].map(i => [J[0][i], J[1][i], J[2][i], -f[i]]); for (let i = 0; i < 3; i++) { let pv = i; for (let k = i + 1; k < 3; k++) if (Math.abs(A[k][i]) > Math.abs(A[pv][i])) pv = k; [A[i], A[pv]] = [A[pv], A[i]]; for (let k = i + 1; k < 3; k++) { const q = A[k][i] / A[i][i]; for (let l = i; l < 4; l++) A[k][l] -= q * A[i][l]; } }
          const d = [0, 0, 0]; for (let i = 2; i >= 0; i--) { let s = A[i][3]; for (let k = i + 1; k < 3; k++) s -= A[i][k] * d[k]; d[i] = s / A[i][i]; }
          z = z.map((v, i) => v + d[i]); if (Math.hypot(...d) < 1e-12) break; } return { z, res: Math.hypot(...acc(z)) }; };
      const out = [];
      for (const z0 of [[0, 0, 0], [Math.PI, Math.PI, 0]]) {
        const eq = newton(z0), [a1, a2, us] = eq.z, ss = [0, a1, a2, 0, 0, 0];
        const A = [], B = []; const f0 = DIPC.rhs(p, ss, us, 0);
        for (let j = 0; j < 6; j++) { const e = 1e-6, s1 = ss.slice(); s1[j] += e; const g = DIPC.rhs(p, s1, us, 0); A.push(g.map((v, i) => (v - f0[i]) / e)); }
        const gu = DIPC.rhs(p, ss, us + 1e-6, 0), At = [0, 1, 2, 3, 4, 5].map(i => [0, 1, 2, 3, 4, 5].map(j => A[j][i])), Bt = [0, 1, 2, 3, 4, 5].map(i => [(gu[i] - f0[i]) / 1e-6]);
        const K = DIPC.dlqr(At, Bt, 1, 0.01).K;
        let s = ss.slice(); s[1] += 0.035; s[2] -= 0.02; let t = 0, u = 0, dmax = 0, umin = 1e9, umax = -1e9, ok = true;
        for (let n = 0; n < 30000; n++) { if (n % 10 === 0) { u = us; for (let i = 0; i < 6; i++) u -= K[i] * (s[i] - ss[i]); u = Math.max(-F, Math.min(F, u)); umin = Math.min(umin, u); umax = Math.max(umax, u); }
          s = DIPC.rk4(p, s, u, 0.001, t); t += 0.001; const dv = Math.max(Math.abs(s[1] - a1), Math.abs(s[2] - a2)); dmax = Math.max(dmax, n > 5000 ? dv : 0); if (dv > 1) { ok = false; break; } }
        out.push({ from: z0[0] ? 'hanging' : 'upright', th1: +(a1 * 180 / Math.PI).toFixed(1), th2: +(a2 * 180 / Math.PI).toFixed(1), u_star: +us.toFixed(2), residual: +eq.res.toExponential(1), held30s: ok, dev_after5s_deg: +(dmax * 180 / Math.PI).toFixed(2), u_range: [+umin.toFixed(1), +umax.toFixed(1)] }); }
      return out; }, [med, fl, +U]);
    for (const o of r) console.log(c.padEnd(22), JSON.stringify(o)); }
  await b.close();
})();
