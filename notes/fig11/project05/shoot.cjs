// "Did you shoot?": an energy-pumping swing-up with the motor at its limit, in every medium, for several force limits.
// Bang-bang pump u = −u_max sign(𝒫) (𝒫 = d1 cos θ1 θ̇1 + d2 cos θ2 θ̇2, the rate at which the cart's acceleration feeds the rods, (21)),
// with a spring that keeps the cart within ±1.5 m. Integrated with the page's own rk4 and the full fluid force (35), 1 ms steps, 20 s.
// Reports: the rods' highest energy reached as a share of what upright needs, the motor's work, the drag's heat, and the books' residual.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage();
  await pg.goto('http://localhost:8765/simulations/double-inverted-pendulum.html', { waitUntil: 'load' }); await pg.waitForTimeout(1500);
  const meds = (process.env.MEDS || 'vacuum,air,water,glycerol,honey').split(','), Fs = (process.env.FS || '60,100,200,400').split(',').map(Number);
  for (const med of meds) {
    const r = await pg.evaluate(([m, Fs, Tend]) => {
      const e = (id, v) => { const s = document.getElementById(id); s.value = v; s.dispatchEvent(new Event('change', { bubbles: true })); }; e('med', m); if (m !== 'vacuum') e('flow', 'still');
      const p = DIPC.p, d = p.d, out = [];
      const V = s => p.f[0] * Math.cos(s[1]) + p.f[1] * Math.cos(s[2]), Vtop = p.f[0] + p.f[1];
      const Erods = s => { const c12 = Math.cos(s[1] - s[2]); return 0.5 * (d[3] * s[4] * s[4] + 2 * d[4] * c12 * s[4] * s[5] + d[5] * s[5] * s[5]) + V(s); };   // (20), rods only, cart's motion left out
      for (const F of Fs) {
        let s = [0, Math.PI - 0.05, Math.PI - 0.02, 0, 0, 0], t = 0, Wm = 0, Wf = 0, Hc = 0, Hr = 0, o3 = new Float64Array(3), best = -1e9, tBest = 0, both = 0, Vb = -1e9, xm = 0, vm = 0, Pm = 0;
        const E0 = Erods(s);
        for (let n = 0; n < Tend * 1000; n++) {
          const P = d[1] * Math.cos(s[1]) * s[4] + d[2] * Math.cos(s[2]) * s[5];
          let u = -F * Math.sign(P || 1);
          if (Math.abs(s[0]) > 1.2) u = -F * Math.sign(s[0] + 0.3 * s[3]);   // the rail: turn back before 1.5 m
          if (p.fl) { DIPC.dragF(p, s, o3); const fc = -p.fl.cl * s[3] - p.fl.cc * Math.abs(s[3]) * s[3]; Hc -= fc * s[3] * 0.001; Hr -= ((o3[0] - fc) * s[3] + o3[1] * s[4] + o3[2] * s[5]) * 0.001; }
          const s1 = DIPC.rk4(p, s, u, 0.001, t); Wf += DIPC.rk4.W || 0; Wm += u * 0.5 * (s[3] + s1[3]) * 0.001; s = s1; t += 0.001;
          xm = Math.max(xm, Math.abs(s[0])); vm = Math.max(vm, Math.abs(s[3])); Pm = Math.max(Pm, Math.abs(u * s[3]));
          const Er = Erods(s); if (Er > best) { best = Er; tBest = t; }
          const c1 = Math.cos(s[1]), c2 = Math.cos(s[2]); if (c1 > 0.95 && c2 > 0.95) both++;
          Vb = Math.max(Vb, V(s)); }
        out.push({ F, need_J: +(2 * Vtop).toFixed(2), peakShare: +((best - E0) / (Vtop - E0)).toFixed(3), tPeak: +tBest.toFixed(1), Vmax_share: +((Vb + Vtop) / (2 * Vtop)).toFixed(3), msNearTop: both, motor_J: +Wm.toFixed(1), fluid_J: +Wf.toFixed(1), cartHeat_J: +Hc.toFixed(0), rodHeat_J: +Hr.toFixed(0), maxPow_W: +Pm.toFixed(0), vmax: +vm.toFixed(2), xmax: +xm.toFixed(2) });
      }
      return out; }, [med, Fs, +(process.env.T || 20)]);
    for (const o of r) console.log(med.padEnd(9), JSON.stringify(o));
  }
  await b.close();
})();
