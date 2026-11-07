// Honesty tests of the data panel's store on project 05 (Balancing Two Rods on a Cart) and, with PAGE=rods-in-liquid.html, project 06 (in a liquid).
// b  replay: every stored step again, with the page's own rk4 (bit for bit) and with the independent RK4 of ref.cjs; continuity of the step log; a chained replay
// c  controller: every stored force recomputed from the stored sample alone; zero-order hold of every 1 ms step; sample times on the loop period's grid
// d  picture: cart, hinge between the rods and top of the upper rod found in the canvas pixels (alpha first) and compared with the stored state turned into pixels
// e  scenarios: rest, flick, drag, swing-up, random falls (rolling and STOP), T_s = 10 and 40 ms, a glide, a change of the force limit;
//    wind (Kármán street in air), water (a swell), windcart (the cart in your hand in a breeze): section 13; pumpwater: the pump of 13.7 (law 5)
// Usage: NODE_PATH=$(npm root -g) node hon.cjs [scenario ...]     ROOT=<repo>  PAGE=<file in public/simulations>  DPR=1|2
'use strict';
const { chromium } = require('playwright'); const path = require('path'); const R = require('./ref.cjs');
const ROOT = process.env.ROOT || require('path').resolve(__dirname, '../../..'), PAGE = process.env.PAGE || 'double-inverted-pendulum.html', H = 0.001;
const out = (...a) => console.log(...a);
const fmt = (v) => (v === 0 ? '0' : Math.abs(v) < 1e-3 || Math.abs(v) > 1e5 ? v.toExponential(2) : +v.toPrecision(4));

/* ---------- in the page: copy out the logs written since the last copy, and replay each new step with the page's own rk4 ---------- */
const EXTRACT = (a) => {
  const CART = JSON.parse(document.getElementById('dipc-page').textContent).cart;   // the page's cart: project 05's box or project 06's carriage
  const ds = DIPC.ds, g = (n) => ds.get(n), ver = g('ver'), A = (n, r, w) => Array.from(g(n).subarray(r * w, (r + 1) * w));
  const st = [], cs = []; let b1n = 0, b1x = 0, b1skip = 0;
  for (let r = 0; r < g('st_n'); r++) { const i = g('st_i')[r]; if (i <= a.lastI) continue;
    const row = { i, t: g('st_t')[r], s0: A('st_s0', r, 6), s1: A('st_s1', r, 6), u: g('st_u')[r], xh: g('st_xh')[r], j: g('st_j')[r], kind: g('st_kind')[r], jump: g('st_jump')[r], ver: g('st_ver')[r] };
    if ((row.kind === 0 || row.kind === 2) && row.ver === ver) { const q = DIPC.rk4(DIPC.p, row.s0, row.u, 0.001, row.t); b1n++; if (q.every((v, k) => v === row.s1[k])) b1x++; } else if (row.kind === 0 || row.kind === 2) b1skip++;
    st.push(row); }
  for (let r = 0; r < g('cs_n'); r++) { const i = g('cs_i')[r]; if (i <= a.lastJ) continue;
    cs.push({ i, t: g('cs_t')[r], k: g('cs_k')[r], due: g('cs_due')[r], next: g('cs_next')[r], s: A('cs_s', r, 6), u: g('cs_u')[r], mode: g('cs_mode')[r], rk: g('cs_rk')[r], rx: g('cs_rx')[r], rv: g('cs_rv')[r], rt0: g('cs_rt0')[r], re0: g('cs_re0')[r], xc: g('cs_xc')[r], tp: g('cs_tp')[r], pl: g('cs_pl')[r], ver: g('cs_ver')[r], umax: g('cs_umax')[r], bite: g('cs_bite')[r], vb: g('cs_vb')[r], e1: g('cs_e1')[r], e2: g('cs_e2')[r], us: g('cs_us')[r] }); }
  const ctx = { ver, d: Array.from(g('d')), f: Array.from(g('f')), K: Array.from(g('K')), P: Array.from(g('P')), cs: g('c_star'), gamma: g('gamma'), Ts: g('Ts'), gw: g('glide_w'), kc: g('calm_k'), hw: g('hand_w'), ha: g('hand_amax'), fl: g('medium') === 'vacuum' ? null : { CH: CART.h, flow: g('flow'), U: g('U_f'), nu: g('mu_f') / g('rho_f'), xi: Array.from(g('xi_r')), cq: g('c_q'), cl: g('c_lin'), cc: g('c_quad'), L1: g('L1'), L2: g('L2'), kr: g('rho_f') * Math.PI * 1e-4 + g('mu_a'), kc: g('rho_f') * 4 / 3 * Math.PI * (CART.w / 2) * (CART.h / 2) * (CART.b / 2) + g('m_ac'), acc: g('flow') !== 'still', ma: { mu: g('mu_a'), mc: g('m_ac') } } };
  const pl = g('pl_serial'), plan = pl && pl !== a.plSerial ? { serial: pl, u: Array.from(g('pl_u')), K: Array.from(g('pl_K')), nom: Array.from(g('pl_nom')) } : null;
  return { st, cs, ctx, plan, sig: g('sig')[0], b1: { n: b1n, exact: b1x, skip: b1skip }, t: DIPC.t, mode: DIPC.mode };
};

/* ---------- in the page (test code, not the page's): find the cart, the hinge and the tip in the canvas ---------- */
const PICTURE = () => {
  const ds = DIPC.ds, g = (n) => ds.get(n), cv = document.getElementById('cv'), cx2 = cv.getContext('2d'), dpr = cv.width / cv.getBoundingClientRect().width;
  const img = cx2.getImageData(0, 0, cv.width, cv.height).data, W = cv.width, Hh = cv.height;
  const px = (i, j) => (i < 0 || j < 0 || i >= W || j >= Hh ? [0, 0, 0, 0] : [img[4 * (j * W + i)], img[4 * (j * W + i) + 1], img[4 * (j * W + i) + 2], img[4 * (j * W + i) + 3]]);
  const is = (c, rgb, tol) => c[3] === 255 && Math.abs(c[0] - rgb[0]) <= tol && Math.abs(c[1] - rgb[1]) <= tol && Math.abs(c[2] - rgb[2]) <= tol;   // alpha first: only a fully painted pixel counts
  const PGS = JSON.parse(document.getElementById('dipc-page').textContent), CART = PGS.cart, store = { CH: CART.h, CW: CART.w, LOOK: PGS.look, s: Array.from(g('s_now')), cam: g('cam_x'), sc: g('sc'), w: g('box_w'), h: g('box_h'), y0: g('y0'), L1: g('L1'), L2: g('L2'), m2: g('m2'), cart_px: g('cart_px'), cart_py: g('cart_py'), mid_px: g('mid_px'), mid_py: g('mid_py'), tip_px: g('tip_px'), tip_py: g('tip_py'), cart_w: g('cart_w') };
  const CARD = [255, 250, 243], WHITE = [255, 255, 255], ACC = [122, 31, 43], m = {};
  // where the stored state says things are (the test's own formulas): every scan is centred there, not on the drawing's own stored pixels
  const S = store.s, chh = Math.max(20, store.CH * store.sc), e = {}; e.cx = store.w / 2 + (S[0] - store.cam) * store.sc; e.hy = store.y0 - chh + 4; e.ex = e.cx + store.L1 * store.sc * Math.sin(S[1]); e.ey = e.hy - store.L1 * store.sc * Math.cos(S[1]);
  e.tx = e.ex + store.L2 * store.sc * Math.sin(S[2]); e.ty = e.ey - store.L2 * store.sc * Math.cos(S[2]); e.cw2 = Math.max(46, store.CW * store.sc) / 2;
  // the cart: on the device row 4 css px under the top (project 06: half way down), the leftmost and rightmost fully cream pixels within 12 px of the stored edges
  const jr = Math.round((e.hy + (store.LOOK === 'hull' ? chh / 2 : 4)) * dpr), cw2 = e.cw2; let L = null, Rr = null;   // project 06's carriage: at half its height, below a rod lying flat on its top
  for (let i = Math.floor((e.cx - cw2 - 12) * dpr); i <= Math.ceil((e.cx + cw2 + 12) * dpr); i++) if (is(px(i, jr), CARD, 2)) { if (L === null) L = i; Rr = i; }
  m.cart = L === null ? null : { left: L / dpr, right: (Rr + 1) / dpr, centre: (L + Rr + 1) / (2 * dpr), alphaAt: px(Math.round(e.cx * dpr), jr)[3] };
  // the hinge between the rods: centroid of the pure white pixels within 6 css px of where the store says it is
  let sx = 0, sy = 0, n = 0; const r6 = Math.ceil(6 * dpr), ci = Math.round(e.ex * dpr), cj = Math.round(e.ey * dpr);
  for (let j = cj - r6; j <= cj + r6; j++) for (let i = ci - r6; i <= ci + r6; i++) if (is(px(i, j), WHITE, 0)) { sx += i + 0.5; sy += j + 0.5; n++; }
  m.mid = n ? { x: sx / n / dpr, y: sy / n / dpr, n } : null;
  // the top of the upper rod: along the rod, the last fully burgundy sample, from 12 px inside the rod to 12 px beyond its stored end
  const ux = e.tx - e.ex, uy = e.ty - e.ey, ul = Math.hypot(ux, uy); let last = null, clear = null;
  for (let t = -12; t <= 12; t += 0.05) { const x = e.tx + t * ux / ul, y = e.ty + t * uy / ul, c = px(Math.floor(x * dpr), Math.floor(y * dpr)); if (is(c, ACC, 2)) { last = t; clear = null; } else if (last !== null && clear === null && c[3] === 0) clear = t; }
  let lo = null, hi = null; const bx = e.tx - 6 * ux / ul, by = e.ty - 6 * uy / ul;   // across the rod, 6 px below its top: the burgundy run must be centred on the axis
  for (let t = -10; t <= 10; t += 0.05) { const x = bx - t * uy / ul, y = by + t * ux / ul; if (is(px(Math.floor(x * dpr), Math.floor(y * dpr)), ACC, 2)) { if (lo === null) lo = t; hi = t; } }
  m.tip = last === null ? null : { end: last, clear, lw: 4 + 6 * Math.min(1, store.m2), across: lo === null ? null : (lo + hi) / 2, width: lo === null ? 0 : hi - lo };
  return { store, m, dpr };
};

/* ---------- in Node: the checks ---------- */
function checkPicture(P, label) {
  const s = P.store, S = s.s, ch = Math.max(20, s.CH * s.sc);
  const cx = s.w / 2 + (S[0] - s.cam) * s.sc, hy = s.y0 - ch + 4, ex = cx + s.L1 * s.sc * Math.sin(S[1]), ey = hy - s.L1 * s.sc * Math.cos(S[1]), tx = ex + s.L2 * s.sc * Math.sin(S[2]), ty = ey - s.L2 * s.sc * Math.cos(S[2]);
  const dst = Math.max(Math.abs(cx - s.cart_px), Math.abs(hy - s.cart_py), Math.abs(ex - s.mid_px), Math.abs(ey - s.mid_py), Math.abs(tx - s.tip_px), Math.abs(ty - s.tip_py));
  const m = P.m, res = [];
  res.push(`stored px vs state→px (Node formulas): max |Δ| = ${fmt(dst)} px`);
  const okCart = m.cart && Math.abs(m.cart.centre - cx) <= 0.75 && m.cart.alphaAt === 255;
  res.push(`cart: cream from ${m.cart ? fmt(m.cart.left) : '–'} to ${m.cart ? fmt(m.cart.right) : '–'} px, centre ${m.cart ? fmt(m.cart.centre) : 'NOT FOUND'} vs x→px ${fmt(cx)} (Δ ${m.cart ? fmt(m.cart.centre - cx) : '–'} px, alpha at centre ${m.cart ? m.cart.alphaAt : '–'}) ${okCart ? 'PASS' : 'FAIL'}`);
  const okMid = m.mid && Math.hypot(m.mid.x - ex, m.mid.y - ey) <= 0.3;
  res.push(`hinge between the rods: white centroid (${m.mid ? fmt(m.mid.x) + ', ' + fmt(m.mid.y) : 'NOT FOUND'}) of ${m.mid ? m.mid.n : 0} px vs θ₁→px (${fmt(ex)}, ${fmt(ey)}) (Δ ${m.mid ? fmt(Math.hypot(m.mid.x - ex, m.mid.y - ey)) : '–'} px) ${okMid ? 'PASS' : 'FAIL'}`);
  const tipIn = tx > 6 && tx < s.w - 6 && ty > 6 && ty < s.h - 6;
  const rc = m.tip ? m.tip.lw / 2 : 0, okTip = !tipIn || (m.tip && m.tip.end >= rc - 1.5 && m.tip.end <= rc + 0.5 && m.tip.clear !== null && m.tip.clear <= rc + 1.5 && m.tip.across !== null && Math.abs(m.tip.across) <= 0.75);
  res.push(`top of the upper rod at θ₂→px (${fmt(tx)}, ${fmt(ty)}): along the rod, fully burgundy to ${m.tip ? fmt(m.tip.end) : 'NOT FOUND'} px beyond it and transparent from ${m.tip && m.tip.clear !== null ? fmt(m.tip.clear) : '–'} px, round cap radius ${m.tip ? fmt(rc) : '–'} px; across the rod 6 px below the top the burgundy (${m.tip ? fmt(m.tip.width) : '–'} px wide) is centred ${m.tip && m.tip.across !== null ? fmt(m.tip.across) : '–'} px off the axis ${tipIn ? (okTip ? 'PASS' : 'FAIL') : 'outside the figure, not tested'}`);
  return { ok: dst === 0 && okCart && okMid && okTip, lines: res.map((l) => `  d ${label}: ${l}`) };
}

function checkLogs(acc) {
  const lines = [], st = acc.st, cs = acc.cs, byI = new Map(cs.map((c, n) => [c.i, n])); let ok = true;
  // b: one-step replays
  const b1 = acc.b1; if (b1.exact !== b1.n) ok = false;
  lines.push(`  b page's own rk4 on every stored step: ${b1.exact}/${b1.n} bit-identical (${b1.skip} steps of an earlier machine not replayed) ${b1.exact === b1.n ? 'PASS' : 'FAIL'}`);
  let n2 = 0, m2 = 0, m2rel = 0, skip2 = 0;
  for (const r of st) { if (r.kind !== 0 && r.kind !== 2) continue; const c = acc.ctx[r.ver]; if (!c) { skip2++; continue; }
    const q = R.rk4(c.d, c.f, r.s0, r.u, H, r.t, c.fl); n2++; for (let k = 0; k < 6; k++) { const d = Math.abs(q[k] - r.s1[k]); m2 = Math.max(m2, d); m2rel = Math.max(m2rel, d / Math.max(1e-300, Math.abs(r.s1[k] - r.s0[k]) || Math.abs(r.s1[k]))); } }
  const ok2 = m2 < 1e-12; if (!ok2) ok = false;
  lines.push(`  b independent RK4 (Cramer, from (8a), (8), (8b)) on every stored step: ${n2} steps, max |Δs| = ${fmt(m2)}, max |Δs| / |step change| = ${fmt(m2rel)} ${ok2 ? 'PASS (float64 rounding)' : 'FAIL'}`);
  // b: continuity of the step log
  let cont = 0, brk = 0, gaps = 0; const jumps = {};
  for (let n = 1; n < st.length; n++) { const a = st[n - 1], b = st[n]; if (b.i !== a.i + 1) { gaps++; if (gaps <= 3) lines.push(`    gap after step ${a.i} (t ${a.t}) → ${b.i} (t ${b.t}), rows ${n - 1}, ${n}`); continue; }
    if (b.jump) { jumps[b.jump] = (jumps[b.jump] || 0) + 1; continue; } if (b.s0.every((v, k) => v === a.s1[k])) cont++; else brk++; }
  if (brk || gaps || jumps[9]) ok = false;
  lines.push(`  b step log continuity: ${cont} joins exact, ${brk} broken, ${gaps} gaps; outside changes by code ${JSON.stringify(jumps)} (1 flick, 2 hand, 3 reset/new state, 4 wrap at hand-over, 9 unexplained) ${!brk && !gaps && !jumps[9] ? 'PASS' : 'FAIL'}`);
  // b: chained replay over the longest stretch of RK4 steps without an outside change, with the stored forces
  let best = [0, 0], a0 = 0; for (let n = 1; n <= st.length; n++) { if (n === st.length || st[n].kind !== 0 || st[n].jump || st[n].ver !== st[a0].ver || st[n].i !== st[n - 1].i + 1 || st[a0].kind !== 0) { if (n - a0 > best[1] - best[0]) best = [a0, n]; a0 = n; } }
  if (best[1] - best[0] > 10) { const c = acc.ctx[st[best[0]].ver]; let q = st[best[0]].s0.slice(), worst = 0, marks = []; const T0 = st[best[0]].t;
    for (let n = best[0]; n < best[1]; n++) { q = R.rk4(c.d, c.f, q, st[n].u, H, st[n].t, c.fl); const d = Math.max(...q.map((v, k) => Math.abs(v - st[n].s1[k]))); worst = Math.max(worst, d);
      const el = st[n].t + H - T0; if ([0.1, 0.5, 1, 1.5, 2, 2.5, 3, 4, 6, 8].some((m) => Math.abs(el - m) < H / 2)) marks.push([+el.toFixed(1), d]); }
    const rates = []; for (let k = 1; k < marks.length; k++) if (marks[k - 1][1] > 1e-15 && marks[k][1] < 1e-3) rates.push((Math.log(marks[k][1] / marks[k - 1][1]) / (marks[k][0] - marks[k - 1][0])).toFixed(1));
    lines.push(`  b chained independent replay from one stored state with the stored forces, ${best[1] - best[0]} steps (${fmt((best[1] - best[0]) * H)} s): max |Δs| ${marks.map((m) => m[0] + ' s: ' + fmt(m[1])).join(', ')}; growth rate of the gap between marks ${rates.join(', ')} 1/s (open loop: the gap grows as fast as nearby motions part, at the fall rate σ₁ = ${fmt(acc.sig || NaN)} 1/s near upright, slower while hanging or caught)`); }
  // c: every stored force from its own row
  let nc = 0, mc = 0, unc = 0, modes = [0, 0, 0, 0, 0, 0], worstRow = null;
  for (const r of cs) { modes[r.mode]++; const c = acc.ctx[r.ver]; let v;
    if (r.mode === 3 || r.mode === 4) v = 0;
    else if (!c) { unc++; continue; }
    else if (r.mode === 0) { const rv = R.refAt(r.rk, r.rx, r.rv, r.rt0, r.re0, r.t, c.gw);
      if (r.e1 === 0 && r.e2 === 0 && r.us === 0) v = R.lawBalance(c.K, r.s, rv[0], rv[1], r.umax);
      else { const e = [r.s[0] - rv[0], R.wrap(r.s[1]) - r.e1, R.wrap(r.s[2]) - r.e2, r.s[3] - rv[1], r.s[4], r.s[5]]; v = r.us; for (let i = 0; i < 6; i++) v -= c.K[i] * e[i]; v = R.sat(v, r.umax); } }   // 13.8: about the flow's rest state
    else if (r.mode === 1) v = R.lawCalm(c.d, c.f, r.s, r.xc, c.kc, r.umax, c.fl ? { ma: c.fl.ma, L1: c.fl.L1, L2: c.fl.L2 } : null);
    else if (r.mode === 5) { const Vt = c.f[0] + c.f[1], s = r.s, e = s[0] - r.xc, P = c.d[1] * Math.cos(s[1]) * s[4] + c.d[2] * Math.cos(s[2]) * s[5], Ep = 0.5 * (c.d[3] * s[4] * s[4] + 2 * c.d[4] * Math.cos(s[1] - s[2]) * s[4] * s[5] + c.d[5] * s[5] * s[5]) + c.f[0] * Math.cos(s[1]) + c.f[1] * Math.cos(s[2]);   // the pump of 13.7
      v = Math.abs(e) > 1.2 ? -r.umax * (e + 0.3 * s[3] >= 0 ? 1 : -1) : -r.umax * Math.tanh(3 * (Vt - Ep) / Vt) * (P >= 0 ? 1 : -1); }
    else { const p = acc.plans[r.pl]; if (!p) { unc++; continue; } v = R.lawTrack(p, r.s, r.t, r.tp, r.xc, r.umax); }
    nc++; const d = Math.abs(v - r.u); if (d > mc) { mc = d; worstRow = r; } }
  const okc = mc <= 1e-9 && unc === 0; if (!okc) ok = false;
  lines.push(`  c force recomputed from each stored sample (state, reference, gains, limit, plan): ${nc} samples (balance ${modes[0]}, calm ${modes[1]}, track ${modes[2]}, off ${modes[3]}, cut ${modes[4]}, pump ${modes[5]}), max |Δu| = ${fmt(mc)} N${worstRow ? ' (law ' + worstRow.mode + ')' : ''}, ${unc} unchecked ${okc ? 'PASS' : 'FAIL'}`);
  // c: the governor's bites (27), each from its own row: the error from the member of (25) at the cart with the speed before the bite
  let nb = 0, mb = 0, wworst = 0, ub = 0;
  for (const r of cs) { if (!(r.bite === r.bite)) continue; const c = acc.ctx[r.ver]; if (!c || !(c.cs > 0)) { ub++; continue; }
    const e = [0, R.wrap(r.s[1]), R.wrap(r.s[2]), r.s[3] - r.vb, r.s[4], r.s[5]], P = (i, j) => c.P[6 * i + j], sg = r.vb > 0 ? 1 : -1;
    let Pe4 = 0, W = 0; for (let i = 0; i < 6; i++) { Pe4 += P(3, i) * e[i]; for (let j = 0; j < 6; j++) W += e[i] * P(i, j) * e[j]; }
    const D = Math.min(Math.abs(r.vb), (-sg * Pe4 + Math.sqrt(Pe4 * Pe4 - P(3, 3) * (W - c.gamma * c.cs))) / P(3, 3));
    const ep = e.slice(); ep[3] += sg * r.bite; let Wp = 0; for (let i = 0; i < 6; i++) for (let j = 0; j < 6; j++) Wp += ep[i] * P(i, j) * ep[j];
    nb++; mb = Math.max(mb, Math.abs(D - r.bite)); wworst = Math.max(wworst, Wp / c.cs); }
  if (nb) { const okb = mb < 1e-9 && wworst <= cs.filter((r) => r.bite === r.bite).reduce((a, r) => Math.max(a, acc.ctx[r.ver] ? acc.ctx[r.ver].gamma : 0), 0) + 1e-9 && ub === 0; if (!okb) ok = false;
    lines.push(`  c governor (27): ${nb} bites recomputed from their rows, max |ΔD| = ${fmt(mb)} m/s; after every bite W ≤ ${fmt(wworst)} c* (allowed γ); ${ub} unchecked ${okb ? 'PASS' : 'FAIL'}`); }
  // c: your hand on the cart: each step's force from (29) and row 1 of (9), from the stored state and pointer alone (the independent forceFor of ref.cjs)
  let nh = 0, mh = 0, uh = 0;
  for (const r of st) { if (r.kind !== 2) continue; const c = acc.ctx[r.ver]; if (!c || !(c.hw > 0)) { uh++; continue; }
    const a = Math.max(-c.ha, Math.min(c.ha, c.hw * c.hw * (r.xh - r.s0[0]) - 2 * c.hw * r.s0[3])); nh++; mh = Math.max(mh, Math.abs(R.forceFor(c.d, c.f, r.s0, a, r.t, c.fl) - r.u)); }
  if (nh) { const okh = mh < 1e-9 && uh === 0; if (!okh) ok = false;
    lines.push(`  c hand on the cart (29)-(30): ${nh} steps, force recomputed from each stored row, max |Δu| = ${fmt(mh)} N, ${uh} unchecked ${okh ? 'PASS' : 'FAIL'}`); }
  // c: zero-order hold
  let zh = 0, zbad = 0, held = 0, hbad = 0, firstBad = null;
  for (const r of st) { if (r.kind === 2) continue; if (r.kind === 1) { held++; if (r.u !== 0 || r.j !== -1) hbad++; continue; }
    const n = byI.get(r.j); if (n === undefined) continue; const c = cs[n], nx = cs[n + 1];
    const inWin = c.k <= r.i && (!nx || nx.k > r.i); if (r.u === c.u && inWin) zh++; else { zbad++; if (!firstBad) firstBad = { step: r.i, u: r.u, sample: c.i, cu: c.u }; } }
  if (zbad || hbad) ok = false;
  lines.push(`  c zero-order hold: ${zh} RK4 steps hold exactly the force of the latest sample, ${zbad} do not${firstBad ? ' (first: ' + JSON.stringify(firstBad) + ')' : ''}; ${held} held steps with u = 0, ${hbad} not ${!zbad && !hbad ? 'PASS' : 'FAIL'}`);
  // c: sample times
  let chain = 0, anchors = 0, bad = 0, per = {}, early = 0; const ctl = cs.filter((r) => r.mode !== 4);
  for (const r of ctl) if (!(r.t - r.due > -1e-9 && r.t - r.due < H)) early++;
  for (let n = 1; n < ctl.length; n++) { const a = ctl[n - 1], b = ctl[n]; if (b.due !== a.next) { anchors++; continue; }
    const steps = b.k - a.k, want = Math.round((a.next - a.due) / H), Ts = acc.ctx[a.ver] ? acc.ctx[a.ver].Ts : null, perOk = a.mode === 0 ? Math.abs(a.next - a.due - Ts) < 1e-12 : Math.abs(a.next - a.due - 0.01) < 1e-12;
    if (steps === want && perOk) { chain++; per[steps] = (per[steps] || 0) + 1; } else bad++; }
  if (bad || early) ok = false;
  lines.push(`  c sample times: ${chain} intervals on the grid (steps per interval: ${JSON.stringify(per)}), ${bad} off it, ${anchors} restarts of the clock (reset, release, track start, hand-over), ${early} samples away from their due time ${!bad && !early ? 'PASS' : 'FAIL'}`);
  return { ok, lines };
}

async function main() {
  const want = process.argv.slice(2), dpr = +(process.env.DPR || 1);
  const b = await chromium.launch(), pg = await b.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: dpr });
  const errs = []; pg.on('pageerror', (e) => errs.push(e.message));
  await pg.goto('file://' + path.resolve(ROOT + '/public/simulations/' + PAGE)); await pg.waitForTimeout(1500);
  await pg.evaluate(() => DIPC.finishCatch());
  const frame = () => pg.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))));
  const pause = async (on) => { await pg.evaluate((on) => { const bt = document.getElementById('play'), playing = bt.getAttribute('aria-pressed') === 'false'; if (playing !== on) bt.click(); }, on); await frame(); };
  const set = (o) => pg.evaluate((o) => { for (const k in o) { const el = document.getElementById(k); el.value = o[k]; el.dispatchEvent(new Event('input', { bubbles: true })); } }, o);
  let acc;
  const fresh = () => { acc = { st: [], cs: [], ctx: {}, plans: {}, b1: { n: 0, exact: 0, skip: 0 }, lastI: -1, lastJ: -1, plSerial: 0 }; };
  const pull = async () => { const r = await pg.evaluate(EXTRACT, { lastI: acc.lastI, lastJ: acc.lastJ, plSerial: acc.plSerial });
    acc.st.push(...r.st); acc.cs.push(...r.cs); acc.ctx[r.ctx.ver] = r.ctx; acc.sig = r.sig; if (r.plan) { acc.plans[r.plan.serial] = r.plan; acc.plSerial = r.plan.serial; }
    acc.b1.n += r.b1.n; acc.b1.exact += r.b1.exact; acc.b1.skip += r.b1.skip; if (r.st.length) acc.lastI = r.st[r.st.length - 1].i; if (r.cs.length) acc.lastJ = r.cs[r.cs.length - 1].i; return r; };
  const start = async () => { fresh(); await pg.evaluate(() => { const ds = DIPC.ds; }); const r = await pg.evaluate(() => ({ i: DIPC.ds.get('st_i')[DIPC.ds.get('st_n') - 1], j: DIPC.ds.get('cs_i')[DIPC.ds.get('cs_n') - 1] })); acc.lastI = r.i; acc.lastJ = r.j; await pull(); };
  const drive = async (sec) => { const chunks = Math.ceil(sec); for (let c = 0; c < chunks; c++) { await pg.evaluate((n) => { for (let i = 0; i < n; i++) { DIPC.step(1 / 60); DIPC.think(8); } }, Math.round(60 * Math.min(1, sec - c))); await pull(); } await frame(); };
  const live = async (ms) => { for (let t = 0; t < ms; t += 1000) { await pg.waitForTimeout(Math.min(1000, ms - t)); await pull(); } };
  const pic = async (label) => { await pause(false); await frame(); const P = await pg.evaluate(PICTURE); const r = checkPicture(P, label); r.lines.forEach((l) => out(l)); return r.ok; };
  let seed = 7; const rnd = () => { seed = (seed * 1664525 + 1013904223) % 4294967296; return seed / 4294967296; };
  const randomState = () => [(rnd() - 0.5), (rnd() * 2 - 1) * Math.PI, (rnd() * 2 - 1) * Math.PI, (rnd() - 0.5), (rnd() - 0.5) * 6, (rnd() - 0.5) * 6];
  const medium = (m, f, U) => pg.evaluate((a) => { const M = document.getElementById('med'), F = document.getElementById('flow'), S = document.getElementById('Uf'); S.value = a.U; S.dispatchEvent(new Event('input', { bubbles: true })); M.value = a.m; M.dispatchEvent(new Event('change')); F.value = a.f; F.dispatchEvent(new Event('change')); }, { m, f, U });
  const F0 = await pg.evaluate(() => +document.getElementById('Fmax').value), home = () => pg.evaluate(() => { const M = document.getElementById('med'), F = document.getElementById('flow'); M.value = M.options[0].value; M.dispatchEvent(new Event('change')); F.value = 'still'; F.dispatchEvent(new Event('change')); });   // the page's own motor, and its first medium (05: vacuum, 06: water)
  const results = [];
  const scen = {
    rest: async () => { await pause(true); await pg.click('#reset'); await start(); await live(5000); await pull(); return pic('rest'); },
    flick: async () => { await pause(true); await pg.click('#reset'); await pg.waitForTimeout(1500); await start(); await pg.click('#flickR'); await live(2500); const a = await pic('flick, 2.5 s after'); await pause(true); await pg.click('#flickL'); await live(3000); return a; },
    drag: async () => { await pause(true); await pg.click('#reset'); await pg.waitForTimeout(1000); await start();
      const box = await (await pg.$('#cv')).boundingBox(), tp = await pg.evaluate(() => ({ x: DIPC.ds.get('tip_px'), y: DIPC.ds.get('tip_py'), mx: DIPC.ds.get('mid_px'), my: DIPC.ds.get('mid_py') }));
      const gx = box.x + (tp.mx + tp.x) / 2, gy = box.y + (tp.my + tp.y) / 2; await pg.mouse.move(gx, gy); await pg.mouse.down();
      for (let k = 1; k <= 10; k++) { await pg.mouse.move(gx - 6 * k, gy + 2 * k); await pg.waitForTimeout(60); }
      await pg.waitForTimeout(600); const heldNow = await pg.evaluate(() => DIPC.held); const a = await pic('while held'); await pause(true); await pg.mouse.up(); await live(4000); await pull(); out(`  e drag: rod held by the mouse = ${heldNow} (2 = upper)`); return a && heldNow === 2; },
    cart: async () => { await pause(true); await pg.click('#reset'); await pg.waitForTimeout(1000); await start();
      const box = await (await pg.$('#cv')).boundingBox(), cp = await pg.evaluate(() => ({ x: DIPC.ds.get('cart_px'), y: DIPC.ds.get('cart_py') + 10 }));
      const gx = box.x + cp.x, gy = box.y + cp.y; await pg.mouse.move(gx, gy); await pg.mouse.down();
      for (let k = 1; k <= 10; k++) { await pg.mouse.move(gx + 8 * k, gy); await pg.waitForTimeout(30); }
      await pg.waitForTimeout(300); const h = await pg.evaluate(() => ({ held: DIPC.held, th1: DIPC.ds.get('th1w'), u: DIPC.ds.get('u'), uh: DIPC.ds.get('hand_u') })); const a = await pic('cart in your hand');
      await pause(true); await pg.mouse.up(); await live(4000); await pull();
      out(`  e cart: held by the mouse = ${h.held} (3 = cart), motor ${fmt(h.u)} N, hand ${fmt(h.uh)} N, lower rod at ${fmt(h.th1 * 180 / Math.PI)}° 0.6 s after the grab`); return a && h.held === 3 && h.u === 0; },
    swingup: async () => { await pause(false); await pg.evaluate(() => { DIPC.finishCatch(); DIPC.swingUp(); }); await start(); let t = 0, a = true;
      for (; t < 40; t += 2) { await drive(2); if (t === 4) a = (await pic('swing-up, rods hanging')) && a; const m = await pg.evaluate(() => DIPC.mode); if (m === 'balance' && t > 6) break; }
      await drive(2); const m = await pg.evaluate(() => ({ mode: DIPC.mode, W: DIPC.W(), t: DIPC.t })); out(`  e swing-up: mode ${m.mode} at t = ${fmt(m.t)} s, W = ${fmt(m.W)}`); return (await pic('after the swing-up')) && a && m.mode === 'balance'; },
    random: async (stop) => { const s0 = randomState(); await pause(false); await pg.evaluate((a) => { DIPC.finishCatch(); document.getElementById('reset').click(); DIPC.rolling = !a.stop; DIPC.s = a.s0; }, { s0, stop: !!stop }); await start(); let t = 0;
      for (; t < 60; t += 2) { await drive(2); const m = await pg.evaluate(() => ({ mode: DIPC.mode, W: DIPC.W() })); if (m.mode === 'balance' && t > 4 && m.W < 1) break; }
      await drive(2); const m = await pg.evaluate(() => ({ mode: DIPC.mode, t: DIPC.t, x: DIPC.s[0], v: DIPC.s[3], ref: DIPC.ref.kind })); out(`  e random fall from ${JSON.stringify(s0.map((v) => +v.toFixed(2)))}: mode ${m.mode} at t = ${fmt(m.t)} s, cart at ${fmt(m.x)} m moving ${fmt(m.v)} m/s, reference ${m.ref}`);
      await pg.evaluate(() => { DIPC.rolling = true; }); return (await pic('after the catch')) && m.mode === 'balance'; },
    glide: async () => { await pause(false); let s0; for (let k = 0; k < 6; k++) { s0 = randomState(); await pg.evaluate((s0) => { DIPC.finishCatch(); document.getElementById('reset').click(); DIPC.rolling = true; DIPC.s = s0; }, s0);
        for (let t = 0; t < 60; t += 2) { await pg.evaluate(() => { for (let i = 0; i < 120; i++) { DIPC.step(1 / 60); DIPC.think(8); } }); const m = await pg.evaluate(() => DIPC.ref.kind); if (m === 'cruise') break; }
        if ((await pg.evaluate(() => DIPC.ref.kind)) === 'cruise') break; }
      await start(); const v0 = await pg.evaluate(() => DIPC.ds.get('xd') || DIPC.s[3]); await pg.click('[data-go="1"]'); const k1 = await pg.evaluate(() => DIPC.ref.kind); await drive(8); const a = await pic('gliding'); await drive(6);
      const m = await pg.evaluate(() => ({ ref: DIPC.ref.kind, x: DIPC.s[0], v: DIPC.s[3], mode: DIPC.mode })); out(`  e glide: reference ${k1} after the button (cart moving at ${fmt(v0)} m/s), 14 s later cart at ${fmt(m.x)} m moving ${fmt(m.v)} m/s, mode ${m.mode}`); return a && k1 === 'glide'; },
    ts40: async () => { await set({ Ts: 40 }); await pg.evaluate(() => DIPC.finishCatch()); const r = await scen.random(false); const tilt = await (async () => { await pause(false); await pg.click('#tilt'); await start(); await drive(6); return pic('T_s = 40 ms, tilt and let go'); })(); await set({ Ts: 10 }); await pg.evaluate(() => DIPC.finishCatch()); return r && tilt; },
    brake: async () => { await pause(false); let s0, got = false; for (let k = 0; k < 8 && !got; k++) { s0 = randomState(); await pg.evaluate((s0) => { DIPC.finishCatch(); document.getElementById('reset').click(); DIPC.rolling = true; DIPC.s = s0; }, s0);
        for (let t = 0; t < 60; t += 1) { await pg.evaluate(() => { for (let i = 0; i < 60; i++) { DIPC.step(1 / 60); DIPC.think(8); } }); const r = await pg.evaluate(() => ({ b: !!DIPC.ref.brake, v: DIPC.ref.v || 0 })); if (r.b && Math.abs(r.v) > 1) { got = true; break; } } }
      await start(); const v0 = await pg.evaluate(() => DIPC.ref.v); let t = 0; for (; t < 20; t += 2) { await drive(2); if ((await pg.evaluate(() => DIPC.ref.kind)) === 'fixed') break; } await drive(6);   // the reference is at rest; let the balancer settle the last bite
      const m = await pg.evaluate(() => ({ ref: DIPC.ref.kind, v: DIPC.s[3], mode: DIPC.mode })); out(`  e brake: braking from ${fmt(v0)} m/s; reference ${m.ref} after about ${t + 2} s, cart speed 6 s later ${fmt(m.v)} m/s, mode ${m.mode}`);
      return (await pic('braked to rest')) && m.ref === 'fixed' && Math.abs(m.v) < 0.01; },
    wind: async () => { await medium('air', 'street', 2); await pause(true); await pg.click('#reset'); await start(); await drive(8); const a = await pic('in a Kármán street, U = 2 m/s'); await home(); return a; },
    water: async () => { await medium('water', 'waves', 0.4); await pause(true); await pg.click('#reset'); await start(); await drive(8); const a = await pic('in a swell, U = 0.4 m/s'); await home(); return a; },
    pumpwater: async () => { await medium('water', 'still', 2); if (PAGE !== 'double-inverted-pendulum.html') await set({ Fmax: 60 }); await pause(false); await pg.evaluate(() => { DIPC.finishCatch(); DIPC.swingUp(); }); await start(); await drive(16);   // 13.7: no plan in water with the default machine, so after the first failed plan the cart pumps (law 5)
      const n5 = await pg.evaluate(() => { const g = (k) => DIPC.ds.get(k); let n = 0; for (let r = 0; r < g('cs_n'); r++) if (g('cs_mode')[r] === 5) n++; return n; }); out(`  e pump in still water: ${n5} samples with law 5 in the store`);
      const a = await pic('in still water, pumping after a failed plan'); await set({ Fmax: F0 }); await home(); return a && n5 > 0; },
    stillwater: async () => { await medium('water', 'still', 2); await pause(true); await pg.click('#reset'); await start(); await drive(4); await pg.click('#flickR'); await drive(4); const a = await pic('in still water, after a flick'); await home(); return a; },
    windcart: async () => { await medium('air', 'breeze', 3); const a = await scen.cart(); await home(); return a; },
    limit: async () => { await pause(false); await pg.click('#tilt'); await start(); await drive(1); await set({ Fmax: Math.round(F0 * 25 / 60) }); await drive(3); await set({ Fmax: F0 }); await pg.evaluate(() => DIPC.finishCatch()); await drive(2); return pic('force limit changed while balancing'); }
  };
  const order = want.length ? want : PAGE === 'double-inverted-pendulum.html' ? ['rest', 'flick', 'drag', 'cart', 'swingup', 'random', 'randomSTOP', 'ts40', 'glide', 'brake', 'limit', 'wind', 'windcart']   // project 05: vacuum and air
    : ['rest', 'flick', 'drag', 'cart', 'swingup', 'random', 'limit', 'water', 'stillwater', 'pumpwater'];   // project 06 (PAGE=rods-in-liquid.html): starts in water; pumpwater with its motor cut to 60 N, where no plan is found; no glide: in a liquid the cart is never left cruising after a catch (13.7), so there is no glide to test
  for (const name of order) { out(`== ${name}${dpr !== 1 ? ' (device pixel ratio ' + dpr + ')' : ''}`); const okPic = await (name === 'randomSTOP' ? scen.random(true) : scen[name]());
    await frame(); const bk = await pg.evaluate(() => { const g = (n) => DIPC.ds.get(n), rows = [g('E0'), g('W_motor'), g('E_ext'), g('E_wait')]; return { rows, E: g('E'), bal: g('bal'), rel: Math.abs(g('bal')) / (rows.reduce((a, v) => a + Math.abs(v), 0) + Math.abs(g('E'))) }; });
    out(`  energy book: E0 ${fmt(bk.rows[0])} + W_motor ${fmt(bk.rows[1])} + E_ext ${fmt(bk.rows[2])} + E_wait ${fmt(bk.rows[3])} − E ${fmt(bk.E)} = ${fmt(bk.bal)} J, ${fmt(bk.rel)} of the flows`);
    await pull(); const c = checkLogs(acc); c.lines.forEach((l) => out(l)); const span = acc.st.length ? `${fmt(acc.st[0].t)}–${fmt(acc.st[acc.st.length - 1].t + H)} s` : '';
    out(`  ${name}: ${acc.st.length} steps (${span}), ${acc.cs.length} samples → ${c.ok && okPic ? 'ALL PASS' : 'SOMETHING FAILED'}`); results.push([name, c.ok && okPic]); }
  out(`summary: ${results.filter((r) => r[1]).length}/${results.length} scenarios pass: ${results.map((r) => r[0] + (r[1] ? ' ✓' : ' ✗')).join(', ')}`);
  out('page errors:', errs.join(' | ') || 'none'); await b.close();
}
if (require.main === module) main();
module.exports = { EXTRACT, PICTURE, checkLogs, checkPicture };
