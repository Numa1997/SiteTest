// Gate 2, L0: the model (physics.cjs) against the printed numbers. The model is read, not edited.
const P = require('/home/user/SiteTest/portfolios-src/droplets/physics.cjs');
const A = P.air(283.15, 85000);
const W = 300e6 * P.massOf(8e-6);
console.log('k (10 C, 850 hPa) =', P.stokesK(A), '(text 1.2296e8)   W =', W * 1e3, 'g/m3');
console.log('t(40->100) finite r, min =', P.L0time(40e-6, 100e-6, 8e-6, W, A, 1) / 60, '(text 9.96)');
console.log('t(40->100) r<<R,   min =', (1 / (P.stokesK(A) * W / 4000 * 40e-6)) * 0.6 / 60, '(text 12.64)');
console.log('blow-up (1.3) t* min =', 1 / (P.stokesK(A) * W / 4000 * 40e-6) / 60, '(text 21.1);  model L0blowup finite r =', P.L0blowup(40e-6, 8e-6, W, A, 1) / 60);
console.log('L0radius(t=0.5t*) / R0 =', P.L0radius(0.5 / (P.stokesK(A) * W / 4000 * 40e-6), 40e-6, W, A, 1) / 40e-6, '(expect 2)');
