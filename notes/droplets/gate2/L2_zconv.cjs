const P = require('/home/user/SiteTest/portfolios-src/droplets/physics.cjs');
const A = P.air(283.15, 85000); const pe = P.pairEfficiency(40e-6, 8e-6, A);
for (const Z of [50, 100, 200, 400, 800]) { const t = Date.now(); const e = P.flowEfficiency('stokes', pe.St, pe.S, 0.2, Z); console.log('model creeping Z =', Z, 'E_S =', e.E.toFixed(6), 'b_c =', e.bc.toFixed(6), ((Date.now() - t) / 1000).toFixed(1) + ' s'); }
