// Gate 2, L2: the model's own trajectory code (read only) against the independent SciPy integrator (L2_route2_numeric.py)
const P = require('/home/user/SiteTest/portfolios-src/droplets/physics.cjs');
const A = P.air(283.15, 85000);
console.log('St_c potential =', P.criticalStokes('potential'), ' (1/12 =', 1 / 12, ');  St_c creeping =', P.criticalStokes('stokes'), '(text 1.21194)');
const pe = P.pairEfficiency(40e-6, 8e-6, A);
console.log('pairEfficiency(40 um, 8 um): E =', pe.E, 'ES =', pe.ES, 'EP =', pe.EP, 'St =', pe.St, 'S =', pe.S, 'Re =', pe.Re);
console.log('zero-inertia creeping p=0.2 (St tiny): E =', P.flowEfficiency('stokes', 1e-4, 0, 0.2, 60).E, ' closed form 0.039352; potential:', P.flowEfficiency('potential', 1e-4, 0, 0.2, 15).E, ' closed form 0.421296');
