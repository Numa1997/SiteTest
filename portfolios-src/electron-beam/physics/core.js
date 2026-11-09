/* The Electron Beam, from Tip to Measurement · physics/core.js
   Shared physics core, owned by the scaffold (PLAN.md section 7). Constants, unit helpers and number formatting.

   The module pattern every physics/chNN.js follows (see physics/ch00.js for a worked example):
   - one file, wrapped so that it runs unchanged in the page (a plain <script>, registers itself as EB.<name>) and in Node
     (require('./core.js') returns the same object);
   - pure: compute(p) reads a plain object of SI inputs (keys from contract.json) and returns a plain object of SI outputs;
     no DOM, no global state, no randomness unless a seed is passed in p;
   - optional draw(ctx, w, h, p, out) paints one canvas in the browser from p and out only; it computes nothing new.
   The Python reference ref/core.py mirrors every constant here; checks/check_parity.py compares the two.

   Constants: CODATA 2018 recommended values (E. Tiesinga et al., Rev. Mod. Phys. 93, 025010 (2021);
   https://physics.nist.gov/cuu/Constants/). c, h, e, k_B and N_A are exact since the SI redefinition of 20 May 2019. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else { root.EB = root.EB || {}; root.EB.core = factory(); }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const C = Object.freeze({
    c: 299792458,                 // m/s, speed of light in vacuum (exact)
    h: 6.62607015e-34,            // J s, Planck constant (exact)
    e: 1.602176634e-19,           // C, elementary charge (exact)
    k_B: 1.380649e-23,            // J/K, Boltzmann constant (exact)
    N_A: 6.02214076e23,           // 1/mol, Avogadro constant (exact)
    m_e: 9.1093837015e-31,        // kg, electron mass (CODATA 2018)
    eps0: 8.8541878128e-12,       // F/m, vacuum electric permittivity (CODATA 2018)
    mu0: 1.25663706212e-6,        // N/A^2, vacuum magnetic permeability (CODATA 2018)
    u: 1.66053906660e-27,         // kg, atomic mass constant (CODATA 2018)
    a0: 5.29177210903e-11,        // m, Bohr radius (CODATA 2018)
    alpha_fs: 7.2973525693e-3,    // 1, fine-structure constant (CODATA 2018)
  });
  // derived, computed here once so that every chapter uses the same double
  const D = Object.freeze({
    hbar: C.h / (2 * Math.PI),                     // J s
    e_over_m: C.e / C.m_e,                         // C/kg, specific charge of the electron (CODATA 2018 lists 1.75882001076e11)
    mc2: C.m_e * C.c * C.c,                        // J, electron rest energy
    mc2_eV: C.m_e * C.c * C.c / C.e,               // eV-equivalent of the rest energy, as a plain number (CODATA 2018: 510998.95000)
    A_R: 4 * Math.PI * C.m_e * C.e * C.k_B * C.k_B / Math.pow(C.h, 3),   // A m^-2 K^-2, Richardson constant
  });

  // ------------------------------------------------------------------ units: every stored value is SI; these convert at the edges
  const U = Object.freeze({
    eV: C.e,                 // J per eV
    keV: 1e3 * C.e,
    nm: 1e-9, pm: 1e-12, um: 1e-6, mm: 1e-3,
    mbar: 100,               // Pa per mbar
    Torr: 101325 / 760,      // Pa per Torr
    hour: 3600,              // s per hour
    deg: Math.PI / 180,      // rad per degree
    zeroC: 273.15,           // K at 0 degrees Celsius
  });
  const toSI = (x, unit) => { if (!(unit in U)) throw new Error('unknown unit ' + unit); return x * U[unit]; };
  const fromSI = (x, unit) => { if (!(unit in U)) throw new Error('unknown unit ' + unit); return x / U[unit]; };

  // ------------------------------------------------------------------ number formatting (mirrored by ref/core.py fmt; the build uses the Python one)
  const SUP = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };
  // x to `sig` significant figures; plain decimals between 1e-3 and 1e5, otherwise m × 10ⁿ
  function fmt(x, sig) {
    sig = sig || 3;
    if (!isFinite(x)) return String(x);
    if (x === 0) return '0';
    const neg = x < 0; x = Math.abs(x);
    let e = Math.floor(Math.log10(x));
    let m = x / Math.pow(10, e);
    let ms = m.toFixed(sig - 1);
    if (+ms >= 10) { e += 1; m /= 10; ms = m.toFixed(sig - 1); }
    let s;
    if (e >= -3 && e < 5) {
      const dec = Math.max(0, sig - 1 - e);
      s = (+ms * Math.pow(10, e)).toFixed(dec);
    } else {
      s = ms + ' × 10' + String(e).split('').map(ch => SUP[ch]).join('');
    }
    return (neg ? '−' : '') + s;
  }

  // ------------------------------------------------------------------ small numerical helpers shared by the chapters
  const clamp = (x, lo, hi) => Math.min(hi, Math.max(lo, x));
  // deterministic random numbers for Monte Carlo chapters: mulberry32, a 32-bit generator; same seed, same sequence in page and Node
  function rng(seed) {
    let a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      let t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // ------------------------------------------------------------------ the contract: fill a module's inputs with their defaults
  function withDefaults(contract, names, p) {
    const out = {};
    for (const k of names) {
      const s = contract.symbols[k];
      if (!s) throw new Error('symbol not in contract.json: ' + k);
      out[k] = (p && k in p) ? p[k] : s.default;
      if (out[k] === undefined) throw new Error('no value and no default for ' + k);
    }
    return out;
  }

  return { C, D, U, toSI, fromSI, fmt, clamp, rng, withDefaults, version: 1 };
});
