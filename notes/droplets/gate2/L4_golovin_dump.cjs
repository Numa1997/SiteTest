// Gate 2, L4: golovinDensity (read only from physics.cjs) on a grid, units m_bar = N0 = b = 1 and with the text's SI parameters
const P = require('/home/user/SiteTest/portfolios-src/droplets/physics.cjs');
const out = { unit: [], besselI1e: [], si: [] };
for (const T of [0.3, 1.0, 2.0, 5.4]) for (const u of [0.05, 0.4, 1, 2.5, 6, 15, 30]) out.unit.push({ T, u, n: P.golovinDensity(u, T, 1, 1, 1) });
for (const x of [0.01, 0.5, 1, 3, 3.75, 4, 10, 50, 300, 2000]) out.besselI1e.push({ x, v: P.besselI1e(x) });
const mbar = P.massOf(10e-6), N0 = 1e-3 / mbar, b = 1.5;
for (const t of [600, 1800, 3600]) for (const rum of [3, 10, 20, 40, 100]) { const m = P.massOf(rum * 1e-6); out.si.push({ t, rum, n: P.golovinDensity(m, t, b, N0, mbar) }); }
out.mbar = mbar; out.N0 = N0;
console.log(JSON.stringify(out));
