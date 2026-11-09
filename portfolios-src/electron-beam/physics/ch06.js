/* The Electron Beam, from Tip to Measurement · physics/ch06.js
   Chapter 6, scan and hit: what the electrons do inside the wafer. Single-scattering Monte Carlo after D. C. Joy, "An introduction to
   Monte Carlo simulations", Scanning Microscopy 5 (1991) 329-337 (read in full), with the secondary-electron model and constants of
   Y. Lin and D. C. Joy, Surf. Interface Anal. 37 (2005) 895-900 (read). Pure module (physics/core.js pattern); mirrored by ref/ch06.py.

   Units inside: energies in keV, lengths in nm (converted at the end to SI).
   Elastic scattering, screened Rutherford with relativistic factor (Joy Eqs. 1-3):
       sigma_E = 5.21e-21 (Z^2/E^2) 4 pi / (a (1 + a)) ((E + 511) / (E + 1024))^2  cm^2,   a = 3.4e-3 Z^0.67 / E   (Bishop 1976)
       lambda_el = A / (N_A rho sigma_E)
   Step and angles (Joy Eqs. 4, 6, 7): s = -lambda_el ln R1,  cos phi = 1 - 2 a R2 / (1 + a - R2),  psi = 2 pi R3.
   Direction: rotation of the unit vector by (phi, psi) about its own axis; the form used avoids Joy's AN = -cx/cz, which diverges for
   cz = 0 (derive/ch06.py checks that it keeps unit length and turns by exactly phi).
   Energy loss, continuous (Joy-Luo modified Bethe, k = 0.85 as Lin and Joy Eq. 13):
       dE/ds = -78500 (rho Z / (A E)) ln(1.166 (E + 0.85 J) / J)  keV/cm,   J = (9.76 Z + 58.5 Z^-0.19) eV   (Joy Eq. 12, Berger-Seltzer)
   Secondary electrons (Lin and Joy Eqs. 1-3): generated at (1/eps) |dE/ds| per path length, each escapes with probability 0.5 exp(-z/lambda_s);
   the integral over each straight step is done exactly; delta_SE counts SE from primaries on the way in and on the way out.
   An electron that crosses z = 0 with E > 50 eV is backscattered; one whose energy falls to 50 eV is absorbed (Joy: the stopping power holds
   to about 50 eV). Range R: Kanaya-Okayama, R = 27.6 A E^1.67 / (Z^0.89 rho) nm (A g/mol, rho g/cm^3, E keV).
   Interaction volume: hemisphere about the point of impact whose radius r90 holds 90 % of the energy left in the wafer (step energy put at the
   step's midpoint; histogram of 4000 bins up to 3 R).  sigma_sig: rms of one lateral coordinate (x) of the escaping SE, weight = escape weight.
   Random numbers: core.rng (mulberry32), one generator per electron seeded with SEED + 7919 i, so a last-bit difference in a library function
   can change at most that one electron's path (parity tolerance in `tolerance`). */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./core.js'));
  else { root.EB = root.EB || {}; root.EB.ch06 = factory(root.EB.core); }
})(typeof self !== 'undefined' ? self : this, function (core) {
  'use strict';
  const { C } = core;
  const NA = C.N_A, SEED = 20261109, NEL = 2000, EMIN = 0.05, NPATH = 40, NBIN = 4000;
  // Z, A (g/mol, IUPAC standard atomic weights), rho (g/cm^3, the densities NIST ESTAR uses), eps (eV) and lambda_s (nm) from Lin and Joy Table 1
  const MAT = {
    Si: { Z: 14, A: 28.0855, rho: 2.33, eps: 90, ls: 2.7 },
    Al: { Z: 13, A: 26.9815, rho: 2.6989, eps: 32, ls: 1.7 },
    Cu: { Z: 29, A: 63.546, rho: 8.96, eps: 35, ls: 0.6 },
    Au: { Z: 79, A: 196.967, rho: 19.32, eps: 35, ls: 0.5 },
  };
  const Jkev = Z => (9.76 * Z + 58.5 * Math.pow(Z, -0.19)) * 1e-3;
  const screen = (Z, E) => 3.4e-3 * Math.pow(Z, 0.67) / E;
  function mfp(m, E) {                                                    // elastic mean free path, nm
    const a = screen(m.Z, E), r = (E + 511) / (E + 1024);
    const sig = 5.21e-21 * (m.Z * m.Z) / (E * E) * 4 * Math.PI / (a * (1 + a)) * r * r;   // cm^2
    return m.A / (NA * m.rho * sig) * 1e7;
  }
  function stop(m, E, J) {                                                // |dE/ds|, keV per nm
    return 78500 * m.rho * m.Z / (m.A * E) * Math.log(1.166 * (E + 0.85 * J) / J) * 1e-7;
  }
  const rangeKO = (m, E) => 27.6 * m.A * Math.pow(E, 1.67) / (Math.pow(m.Z, 0.89) * m.rho);   // nm
  // exact integral of exp(-z/ls) along a straight piece from depth zA to zB of length s (both depths >= 0)
  function escInt(zA, zB, s, ls) {
    const dz = zB - zA;
    if (Math.abs(dz) < 1e-6 * ls) return s * Math.exp(-0.5 * (zA + zB) / ls);
    return s * ls / dz * (Math.exp(-zA / ls) - Math.exp(-zB / ls));
  }
  function turn(c, phi, psi) {                                            // rotate unit vector c by polar angle phi, azimuth psi
    const cp = Math.cos(phi), sp = Math.sin(phi), cs = Math.cos(psi), ss = Math.sin(psi);
    const [cx, cy, cz] = c;
    let n;
    if (Math.abs(cz) > 0.99999) n = [sp * cs, sp * ss, (cz > 0 ? 1 : -1) * cp];
    else {
      const t = Math.sqrt(1 - cz * cz);
      n = [sp * (cx * cz * cs - cy * ss) / t + cx * cp, sp * (cy * cz * cs + cx * ss) / t + cy * cp, -sp * cs * t + cz * cp];
    }
    const l = Math.sqrt(n[0] * n[0] + n[1] * n[1] + n[2] * n[2]);
    return [n[0] / l, n[1] / l, n[2] / l];
  }

  function run(p, opts) {
    opts = opts || {};
    const m = MAT[p.material];
    if (!m) throw new Error('unknown material ' + p.material);
    const E0 = p.V_land * 1e-3, J = Jkev(m.Z), R = rangeKO(m, E0), N = opts.N || NEL;
    const binW = 3 * R / NBIN, hist = new Float64Array(NBIN);
    let nBS = 0, seSum = 0, seSq = 0, wx2 = 0, wTot = 0, depTot = 0;
    const paths = [];
    for (let i = 0; i < N; i++) {
      const rnd = core.rng(SEED + 7919 * i);
      let x = 0, y = 0, z = 0, c = [0, 0, 1], E = E0, se = 0, alive = true, bs = false;
      const rec = i < NPATH ? [0, 0] : null;
      let guard = 0;
      while (alive && guard++ < 200000) {
        const lam = mfp(m, E), S = stop(m, E, J);
        let s = -lam * Math.log(1 - rnd());                              // 1 - R keeps the argument in (0, 1]
        let zn = z + c[2] * s, exit = false;
        if (zn < 0) { s = -z / c[2]; zn = 0; exit = true; }              // leaves through the surface on this step
        let dead = false;
        if (S * s >= E - EMIN) { s = (E - EMIN) / S; zn = z + c[2] * s; dead = true; exit = false; }
        const xn = x + c[0] * s, yn = y + c[1] * s;
        // secondary electrons generated along this piece, split into short parts for the lateral moment
        if (Math.min(z, zn) < 12 * m.ls) {
          const np = Math.min(200, Math.max(1, Math.ceil(s / (0.5 * m.ls))));
          for (let k = 0; k < np; k++) {
            const u0 = s * k / np, u1 = s * (k + 1) / np, um = 0.5 * (u0 + u1);
            const wk = 0.5 * S / (m.eps * 1e-3) * escInt(z + c[2] * u0, z + c[2] * u1, u1 - u0, m.ls);
            const xm = x + c[0] * um;
            se += wk; wx2 += wk * xm * xm; wTot += wk;
          }
        }
        // energy left in the wafer on this piece, at its midpoint
        const dE = S * s, mx = 0.5 * (x + xn), my = 0.5 * (y + yn), mz = 0.5 * (z + zn), rm = Math.sqrt(mx * mx + my * my + mz * mz);
        hist[Math.min(NBIN - 1, Math.floor(rm / binW))] += dE; depTot += dE;
        x = xn; y = yn; z = zn; E -= dE;
        if (rec) rec.push(x, z);
        if (exit) { bs = E > EMIN; alive = false; break; }
        if (dead) { alive = false; break; }
        const a = screen(m.Z, E), r2 = rnd();
        const cphi = 1 - 2 * a * r2 / (1 + a - r2);
        c = turn(c, Math.acos(Math.max(-1, Math.min(1, cphi))), 2 * Math.PI * rnd());
      }
      if (bs) nBS++;
      seSum += se; seSq += se * se;
      if (rec) { rec[0] = (rec.length - 2) / 2; rec[1] = bs ? 1 : 0; paths.push(...rec); }
    }
    const eta = nBS / N, delta = seSum / N;
    const uDelta = Math.sqrt(Math.max(0, seSq / N - delta * delta) / N);
    let acc = 0, r90 = 3 * R;
    for (let b = 0; b < NBIN; b++) {
      if (acc + hist[b] >= 0.9 * depTot) { r90 = (b + (0.9 * depTot - acc) / hist[b]) * binW; break; }
      acc += hist[b];
    }
    return {
      E_land: p.V_land * C.e, delta_SE: delta, eta_BSE: eta, R: R * 1e-9, V_int: 2 / 3 * Math.PI * Math.pow(r90 * 1e-9, 3),
      sigma_sig: Math.sqrt(wx2 / wTot) * 1e-9, u_eta: Math.sqrt(eta * (1 - eta) / N), u_delta: uDelta, r90: r90 * 1e-9, mc_paths: paths,
    };
  }
  const compute = p => run(p);

  // the first 40 trajectories in the x-z plane, wine if backscattered; the Kanaya-Okayama range as a dashed arc; SE escape depth shaded
  function draw(ctx, w, h, p, out) {
    ctx.clearRect(0, 0, w, h);
    const R = out.R * 1e9, top = 28, sc = Math.min((w - 40) / (2.4 * R), (h - top - 30) / (1.25 * R)), cx = w / 2;
    const X = v => cx + v * sc, Y = v => top + v * sc;
    ctx.fillStyle = '#f3ede2'; ctx.fillRect(0, top, w, h - top);
    const m = MAT[p.material];
    ctx.fillStyle = 'rgba(122,31,43,0.10)'; ctx.fillRect(0, top, w, Math.max(1, 3 * m.ls * sc));
    ctx.strokeStyle = '#1c1518'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(0, top); ctx.lineTo(w, top); ctx.stroke();
    ctx.strokeStyle = '#8b8079'; ctx.setLineDash([5, 4]); ctx.beginPath(); ctx.arc(cx, top, R * sc, 0, Math.PI); ctx.stroke(); ctx.setLineDash([]);
    const pts = out.mc_paths;
    let k = 0;
    ctx.save(); ctx.beginPath(); ctx.rect(0, 0, w, h); ctx.clip();
    for (const pass of [0, 1]) {                                          // stopped electrons first, backscattered on top
      k = 0;
      while (k < pts.length) {
        const n = pts[k], bs = pts[k + 1]; k += 2;
        if (bs === pass) {
          ctx.strokeStyle = bs ? '#7a1f2b' : 'rgba(58,50,46,0.5)'; ctx.lineWidth = bs ? 1.3 : 0.8;
          ctx.beginPath(); ctx.moveTo(cx, top);
          for (let j = 0; j < n; j++) ctx.lineTo(X(pts[k + 2 * j]), Y(pts[k + 2 * j + 1]));
          ctx.stroke();
        }
        k += 2 * n;
      }
    }
    ctx.restore();
    ctx.strokeStyle = '#1c1518'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(cx, 4); ctx.lineTo(cx, top); ctx.stroke();
    ctx.font = "11px 'IBM Plex Mono', monospace"; ctx.fillStyle = '#3a322e'; ctx.textAlign = 'left';
    ctx.fillText('beam, ' + core.fmt(p.V_land * 1e-3, 3) + ' kV into ' + p.material, 6, 14);
    // scale bar: a round length near R/2
    const raw = R / 2, pw = Math.pow(10, Math.floor(Math.log10(raw))), bar = [1, 2, 5].map(f => f * pw).filter(v => v <= raw).pop() || pw;
    const yb = h - 10; ctx.strokeStyle = '#1c1518'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(10, yb); ctx.lineTo(10 + bar * sc, yb); ctx.stroke();
    ctx.fillText(bar >= 1000 ? core.fmt(bar / 1000, 2) + ' µm' : core.fmt(bar, 2) + ' nm', 14 + bar * sc, yb + 4);
    ctx.textAlign = 'right'; ctx.fillStyle = '#6f655f'; ctx.fillText('dashed: Kanaya–Okayama range', w - 6, h - 6);
  }

  return {
    id: 'ch06',
    inputs: ['V_land', 'material'],
    outputs: ['E_land', 'delta_SE', 'eta_BSE', 'R', 'V_int', 'sigma_sig', 'u_eta', 'u_delta', 'r90', 'mc_paths'],
    tolerance: { rel: 1e-7, abs: 1e-12, note: 'same random numbers and the same arithmetic on both sides; library functions (log, exp, acos, pow) may differ in the last bit, which moves paths by about 1e-15 and, through the energy histogram, r90 and V_int by about 1e-9 (measured); each electron has its own generator, so a flipped branch would change one electron only' },
    cases: [{}, { V_land: 3000 }, { V_land: 30000, material: 'Au' }, { V_land: 1000, material: 'Cu' }, { V_land: 5000, material: 'Al' }],
    ui: {
      controls: ['material', 'V_land'],
      readouts: ['eta_BSE', 'delta_SE', 'R', 'r90', 'sigma_sig'],
      aspect: '16 / 10', aspectPhone: '1 / 1',
      caption: 'Forty electron paths in the wafer, seen from the side (wine: the electron came back out, a backscattered electron; grey: it stopped inside). The dashed arc is the Kanaya–Okayama range; the shaded band at the surface is three escape depths deep, the layer from which secondary electrons get out. The readouts come from 2000 electrons with fixed random numbers, so the same settings always give the same numbers; their statistical uncertainty is stated in the text.',
    },
    compute, draw, run, MAT, mfp, stop, Jkev, rangeKO, turn, escInt,
  };
});
