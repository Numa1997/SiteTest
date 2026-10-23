// Gate 2, L3: what if "500 um and 250 um" in chapter 4 meant diameters (radii 250 and 125 um)?
const P = require('/home/user/SiteTest/portfolios-src/droplets/physics.cjs'); const A = P.air(283.15, 85000);
const dv = Math.abs(P.vBeard(250e-6, A) - P.vBeard(125e-6, A)); const w = P.weber(250e-6, 125e-6, dv, P.sigmaWater(283.15));
console.log('diameters 500/250 um: dv', dv, 'We', w, 'E', Math.exp(-1.15 * w));
