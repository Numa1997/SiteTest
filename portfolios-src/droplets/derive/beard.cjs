// Beard (1976) three-regime terminal speed (prototype copy for derive/; the model's copy lives in physics.cjs)
'use strict';
const g = 9.81, RW = 1000;
const B2 = [-3.18657, 0.992696, -1.53193e-3, -9.87059e-4, -5.78878e-4, 8.55176e-5, -3.27815e-6];
const B3 = [-5.00015, 5.23778, -2.04914, 0.475294, -0.0542819, 0.00238449];
function air(T, p) { const rho = p / (287.05 * T), mu = 1.72e-5 * Math.pow(T / 273, 1.5) * 393 / (T + 120); return { T, p, rho, mu }; }
function sigma(T) { const t = 1 - T / 647.096; return 0.2358 * Math.pow(t, 1.256) * (1 - 0.625 * t); }
function vt(a, A, rhop) {
  rhop = rhop || RW; const d = 2 * a, dr = rhop - A.rho;
  const l = 6.62e-8 * (A.mu / 1.818e-5) * (101325 / A.p) * Math.sqrt(A.T / 293.15), csc = 1 + 2.51 * l / d;
  if (d < 19e-6) return dr * g / (18 * A.mu) * csc * d * d;
  if (d < 1.07e-3 || rhop !== RW) {
    const X = Math.log(4 * A.rho * dr * g / (3 * A.mu * A.mu) * d * d * d);
    let Y = 0; for (let k = 6; k >= 0; k--) Y = Y * X + B2[k];
    return A.mu * csc * Math.exp(Y) / (A.rho * d);
  }
  const s = sigma(A.T), Bo = 4 * dr * g * d * d / (3 * s), NP = s * s * s * A.rho * A.rho / (Math.pow(A.mu, 4) * dr * g);
  const X = Math.log(Bo * Math.pow(NP, 1 / 6));
  let Y = 0; for (let k = 5; k >= 0; k--) Y = Y * X + B3[k];
  return A.mu * Math.pow(NP, 1 / 6) * Math.exp(Y) / (A.rho * d);
}
module.exports = { air, sigma, vt, g };
