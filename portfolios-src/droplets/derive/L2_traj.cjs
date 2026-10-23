// L2 prototype: a partner droplet in the flow around a collector (superposition: the collector's flow alone).
// Collector frame, lengths in R, speeds in U = v_t(R), time in R/U. The air rises past the collector, +z.
// Partner:  dy/ds = w,  St dw/ds = a(y) - w - S e_z,  St = tau U / R,  S = v_t(r)/U,  tau = v_t(r)/g* (drag-corrected).
// Contact at |y| = 1 + p, p = r/R. Grazing offset b_c by bisection; E from the partner flux through the start disc.
'use strict';

function flowField(flow) {
  // returns function (x, z) -> [ax, az] and stream function psi(x, z), both in units of U and U R^2
  if (flow === 'potential') {
    return {
      a(x, z) {
        const q2 = x * x + z * z, q = Math.sqrt(q2), q3 = q2 * q, c = z / q, s = x / q;
        const ur = c * (1 - 1 / q3), ut = -s * (1 + 0.5 / q3);
        return [ur * s + ut * c, ur * c - ut * s];
      },
      psi(x, z) { const q = Math.hypot(x, z), s = x / q; return 0.5 * q * q * s * s * (1 - 1 / (q * q * q)); }
    };
  }
  return {
    a(x, z) {
      const q2 = x * x + z * z, q = Math.sqrt(q2), q3 = q2 * q, c = z / q, s = x / q;
      const ur = c * (1 - 1.5 / q + 0.5 / q3), ut = -s * (1 - 0.75 / q - 0.25 / q3);
      return [ur * s + ut * c, ur * c - ut * s];
    },
    psi(x, z) { const q = Math.hypot(x, z), s = x / q; return 0.5 * q * q * s * s * (1 - 1.5 / q + 0.5 / (q * q * q)); }
  };
}

// Dormand-Prince 5(4) coefficients
const DA = [[], [1 / 5], [3 / 40, 9 / 40], [44 / 45, -56 / 15, 32 / 9], [19372 / 6561, -25360 / 2187, 64448 / 6561, -212 / 729],
  [9017 / 3168, -355 / 33, 46732 / 5247, 49 / 176, -5103 / 18656], [35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84]];
const B5 = [35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84, 0];
const B4 = [5179 / 57600, 0, 7571 / 16695, 393 / 640, -92097 / 339200, 187 / 2100, 1 / 40];

// One trajectory. Returns true if the partner touches the collector.
function hits(F, St, S, p, b, Z) {
  const rc = 1 + p;
  const inertialess = St < 1e-3;
  let x = b, z = -Z;
  if (inertialess) {   // dy/ds = a(y) - S e_z
    const f = (x, z) => { const a = F.a(x, z); return [a[0], a[1] - S]; };
    let h = 0.05, y = [x, z];
    for (let n = 0; n < 2e6; n++) {
      const k = [];
      for (let i = 0; i < 7; i++) {
        const yi = [y[0], y[1]];
        for (let j = 0; j < i; j++) { yi[0] += h * DA[i][j] * k[j][0]; yi[1] += h * DA[i][j] * k[j][1]; }
        k.push(f(yi[0], yi[1]));
      }
      let y5 = [y[0], y[1]], e0 = 0, e1 = 0;
      for (let i = 0; i < 7; i++) { y5[0] += h * B5[i] * k[i][0]; y5[1] += h * B5[i] * k[i][1]; e0 += h * (B5[i] - B4[i]) * k[i][0]; e1 += h * (B5[i] - B4[i]) * k[i][1]; }
      const dist = Math.hypot(y5[0], y5[1]) - rc;
      const tol = 1e-9 + 1e-7 * Math.max(0, Math.min(Math.abs(dist), 10));
      const err = Math.max(Math.abs(e0), Math.abs(e1)) / tol;
      if (err <= 1) {
        y = y5;
        if (dist <= 0) return true;
        if (y[1] > rc) return false;
      }
      h *= Math.min(4, Math.max(0.2, 0.9 * Math.pow(1 / (err + 1e-300), 0.2)));
    }
    throw new Error('trajectory did not finish');
  }
  const a0 = F.a(x, z);
  let y = [x, z, a0[0], a0[1] - S];
  const f = (y) => { const a = F.a(y[0], y[1]); return [y[2], y[3], (a[0] - y[2]) / St, (a[1] - y[3] - S) / St]; };
  let h = 0.02 * St;
  for (let n = 0; n < 5e6; n++) {
    const k = [];
    for (let i = 0; i < 7; i++) {
      const yi = y.slice();
      for (let j = 0; j < i; j++) for (let d = 0; d < 4; d++) yi[d] += h * DA[i][j] * k[j][d];
      k.push(f(yi));
    }
    const y5 = y.slice(); let err = 0;
    const dist0 = Math.hypot(y[0], y[1]) - rc;
    for (let d = 0; d < 4; d++) {
      let e = 0;
      for (let i = 0; i < 7; i++) { y5[d] += h * B5[i] * k[i][d]; e += h * (B5[i] - B4[i]) * k[i][d]; }
      const sc = d < 2 ? 1e-9 + 1e-7 * Math.max(0, Math.min(Math.abs(dist0), 10)) : 1e-8 + 1e-7 * Math.abs(y[d]);
      err = Math.max(err, Math.abs(e) / sc);
    }
    if (err <= 1) {
      y = y5;
      const dist = Math.hypot(y[0], y[1]) - rc;
      if (dist <= 0) return true;
      if (y[1] > rc) return false;
    }
    h *= Math.min(4, Math.max(0.2, 0.9 * Math.pow(1 / (err + 1e-300), 0.2)));
  }
  throw new Error('trajectory did not finish');
}

// Efficiency for one flow: bisection on the start offset b, then the flux through the start disc.
function efficiency(flow, St, S, p, Z) {
  const F = flowField(flow), rc = 1 + p;
  let lo = 0, hi = rc * 1.5;
  if (!hits(F, St, S, p, 1e-6, Z)) return { E: 0, bc: 0 };
  while (hits(F, St, S, p, hi, Z)) hi *= 1.5;
  for (let it = 0; it < 40; it++) {
    const mid = 0.5 * (lo + hi);
    if (hits(F, St, S, p, mid, Z)) lo = mid; else hi = mid;
    if (hi - lo < 1e-7 * rc) break;
  }
  const bc = 0.5 * (lo + hi);
  const E = 2 * (F.psi(bc, -Z) - 0.5 * S * bc * bc) / ((1 - S) * rc * rc);
  return { E, bc };
}

// Critical Stokes number: a point partner (p = 0, S = 0) on the upstream axis. In log variables xi = ln(eta),
// u = w/eta (eta = gap in R, w = d eta/ds):  xi' = u,  St u' = A(eta)/eta - u - St u^2,  A = radial air speed.
// A hit is a finite-time blow-up of u (eta reaches 0 with finite speed); a miss is u settling on a fixed point.
// Potential flow: A/eta -> -3, the fixed points exist iff 12 St < 1. Creeping flow: A/eta ~ -1.5 eta -> 0, fixed
// points u = 0 (riding the air: miss) and u = -1/St (unstable); below eta = 1e-9 the side of -1/St decides.
function axisHits(flow, St, Z) {
  const A = flow === 'potential' ? (q) => -(1 - 1 / (q * q * q)) : (q) => -(1 - 1.5 / q + 0.5 / (q * q * q));
  const Aeta = (xi) => { const eta = Math.exp(xi); return eta > 1e-6 ? A(1 + eta) / eta : (flow === 'potential' ? -3 + 6 * eta : -1.5 * eta); };
  let y = [Math.log(Z), Aeta(Math.log(Z))], h = 1e-3 * St;
  const f = (y) => [y[1], (Aeta(y[0]) - y[1]) / St - y[1] * y[1]];
  for (let n = 0; n < 2e7; n++) {
    const k = [];
    for (let i = 0; i < 7; i++) {
      const yi = y.slice();
      for (let j = 0; j < i; j++) for (let d = 0; d < 2; d++) yi[d] += h * DA[i][j] * k[j][d];
      k.push(f(yi));
    }
    const y5 = y.slice(); let err = 0;
    for (let d = 0; d < 2; d++) {
      let e = 0;
      for (let i = 0; i < 7; i++) { y5[d] += h * B5[i] * k[i][d]; e += h * (B5[i] - B4[i]) * k[i][d]; }
      err = Math.max(err, Math.abs(e) / (1e-10 + 1e-10 * Math.abs(y[d])));
    }
    if (err <= 1) {
      y = y5;
      if (y[1] < -1e6 / St) return true;                       // blow-up: contact in finite time
      const eta = Math.exp(y[0]), c = Aeta(y[0]);
      if (flow === 'stokes' && eta < 1e-3) {
        // c = A/eta rises to 0 as eta -> 0, so the unstable fixed point u_- moves down to -1/St: below -1/St is a
        // certain hit, above the current u_- a certain miss (the basin of the fixed point u = 0 only grows)
        if (y[1] < -1 / St) return true;
        const disc = 1 + 4 * St * c;
        if (disc >= 0 && y[1] > (-1 - Math.sqrt(disc)) / (2 * St)) return false;
      }
      if (flow === 'potential' && eta < 1e-8) {
        // c -> -3: no fixed point (12 St > 1) means blow-up; otherwise the side of the unstable fixed point decides
        const disc = 1 + 4 * St * c;
        return disc < 0 ? true : y[1] < (-1 - Math.sqrt(disc)) / (2 * St);
      }
    }
    h *= Math.min(4, Math.max(0.2, 0.9 * Math.pow(1 / (err + 1e-300), 0.2)));
  }
  throw new Error('axis trajectory did not finish');
}
function stc(flow, Z) {
  let lo = flow === 'potential' ? 0.02 : 0.5, hi = flow === 'potential' ? 0.3 : 3;
  for (let it = 0; it < 45; it++) {
    const mid = 0.5 * (lo + hi);
    if (axisHits(flow, mid, Z)) hi = mid; else lo = mid;
  }
  return 0.5 * (lo + hi);
}

module.exports = { flowField, hits, efficiency, stc };

if (require.main === module) {
  const t0 = Date.now();
  for (const Z of [20, 100]) console.log(`Z=${Z}: St_c potential ${stc('potential', Z).toFixed(5)} (1/12 = 0.08333), Stokes ${stc('stokes', Z).toFixed(5)} (Michael and Norey 1.21194)`);
  console.log('time', (Date.now() - t0) / 1000, 's');
}
