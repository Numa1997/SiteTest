/* The Electron Beam, from Tip to Measurement · physics/ch08.js
   Chapter 8, the whole machine: chapters 2, 4, 5 and 7 chained through their own modules, chapter 6 read from its stored Monte Carlo runs
   (the table below is written by derive/ch06.py from data/ch06/mc_runs.json; 2000 electrons per point, interpolated in log E).
   No new physics except two stated additions for the tolerance study:
     defocus: an objective excitation off by the fraction eps moves the focus by dz = 2 C_c eps (lens strength goes as B^2/V*, and C_c is the
       focus shift per relative change of V*); a wafer height error adds to dz. The probe grows to sqrt(d_p^2 + 2 alpha^2 dz^2) (the FW50 of a
       uniform disc of radius alpha |dz| is sqrt(2) alpha |dz|).
     current at fixed condensers: the column is set up for I_p at the nominal source; if the source changes, the current scales as B_r d_v^2
       (brightness times source area, the same demagnification) and the source image as d_v.
   The aperture is always set to the best angle of chapter 5 (alpha_opt), so the probe is chapter 5's d_p_opt.
   Sensitivities: (x/y) dy/dx by central differences of +-1 % in x. Process window: sigma_CD on a 14 x 14 grid of V_land and I_p.
   Tolerance Monte Carlo: 300 samples, tip radius and ln(pressure) normal with the given spreads (through a 5 x 5 grid of chapter 2 runs,
   interpolated bilinearly in ln r and ln p), excitation and wafer height normal; seed fixed. No Python twin (PLAN.md section 4 lets chapter 8
   go without one); derive/ch08.py checks the chain against the separate chapters instead. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory(require('./core.js'), () => ({ ch02: require('./ch02.js'), ch04: require('./ch04.js'), ch05: require('./ch05.js'), ch07: require('./ch07.js') }));
  else { root.EB = root.EB || {}; root.EB.ch08 = factory(root.EB.core, () => root.EB); }
})(typeof self !== 'undefined' ? self : this, function (core, mods) {
  'use strict';
  /* TABLE-START (written by derive/ch06.py) */
  const YT = {"Si":{"E":[0.5,0.7,1.0,1.5,2.0,3.0,5.0,7.0,10.0,15.0,20.0,30.0],"delta":[0.8423961514743549,0.8005149891095269,0.6660268810105558,0.4795562558655266,0.3782519269068307,0.2540286813222287,0.16215055109282747,0.12189028700611304,0.09375692653399646,0.0658092903055202,0.0482688194869875,0.0364137126986614],"eta":[0.263,0.2545,0.23,0.2245,0.2225,0.201,0.186,0.186,0.184,0.1805,0.1635,0.1745],"core":[1.262469352128887,1.7600128040032577,2.306774938265391,2.2942841139244257,2.0893607904523335,0.7199093917195702,0.14820467902236412,0.031475390900309486,0.0015511423946061433,0.0015445829849405055,0.00153780854036352,0.001538510408027452],"fcore":[0.9165810293069907,0.8817393833906813,0.8107324469226259,0.7084406643053889,0.638794691458189,0.5793839201791868,0.5639476198994077,0.5447509794271115,0.5131921849933222,0.5656540929019678,0.6330447773919723,0.6244624127181438],"halo":[4.909252330949869,7.390861106272424,11.035372673353496,16.708356920751296,25.762718134538314,42.21840110446582,93.86728382743408,165.3130592460497,319.6950818399546,602.6209354071168,970.7365897480893,2244.868550623104]},"Al":{"E":[0.5,0.7,1.0,1.5,2.0,3.0,5.0,7.0,10.0,15.0,20.0,30.0],"delta":[1.8095765231863816,1.5892120479091802,1.2533861748992894,0.8922427646449935,0.7088944331743539,0.48042757852203083,0.30908262586819074,0.2373731118607266,0.17767798283102115,0.1242001019712589,0.10049237080658785,0.07164032296310975],"eta":[0.243,0.23,0.219,0.2105,0.201,0.186,0.1685,0.1705,0.1705,0.1625,0.164,0.1665],"core":[0.9547736769007409,1.2078866396180898,1.3760743544974603,1.0280696424918423,0.7628653801806538,0.17694711875521324,0.009565747180378718,0.001548103769562751,0.0015435111178496849,0.0015384518627519271,0.001538143937445796,0.0015362808867222918],"fcore":[0.879680124975743,0.8310602345478145,0.7400055461888033,0.6431090219221982,0.589489572216789,0.5685472870694187,0.5277597810006249,0.5376484706799748,0.576296116811753,0.6266672916738948,0.629611013879663,0.6502351336434175],"halo":[3.9758970036857586,5.786449670931798,8.619582011952069,13.0519052887692,20.804935810925063,36.01995663702328,77.80251403277411,134.99691465569165,282.41223169067433,551.0500284297492,899.2304386331165,2044.7392939789072]},"Cu":{"E":[0.5,0.7,1.0,1.5,2.0,3.0,5.0,7.0,10.0,15.0,20.0,30.0],"delta":[1.580089441221815,1.513587766895194,1.274191467722427,0.948111905865553,0.7534362206775117,0.5123062878858194,0.3548152587849211,0.26013588532292564,0.19121441128641758,0.14048222342500785,0.10748421353449035,0.07988694024230096],"eta":[0.435,0.4215,0.3945,0.393,0.4035,0.372,0.36,0.353,0.344,0.328,0.3205,0.3245],"core":[0.4192334943219921,0.5909540628785988,0.8304452147991421,1.028857749407397,1.405758330963764,1.0055105679299434,1.7735499118272484,0.4333290470059892,0.09948160969041056,0.04230423129037109,0.0015521247385405707,0.0015513145182174985],"fcore":[0.938485609886647,0.9163176762948526,0.8836519881090078,0.7945907197696829,0.728367131083351,0.6177463855333551,0.573814032984768,0.5266009037501266,0.5236227440630216,0.5210991147018368,0.5100144247730455,0.5140777624419535],"halo":[1.600941237846183,2.3651908039525416,3.6311489189972725,5.494942851541092,8.609508472063943,12.708232918182828,26.896575939623332,48.55958093717863,81.91134842428289,168.04513502118007,267.7040567172476,533.7470518251995]},"Au":{"E":[0.5,0.7,1.0,1.5,2.0,3.0,5.0,7.0,10.0,15.0,20.0,30.0],"delta":[1.3200892967999154,1.4673074423885408,1.4730249099919979,1.2725787835540145,1.0559088780987076,0.7799291435752124,0.5235597554537296,0.3965598115556851,0.2924574832438178,0.20457320468604653,0.17314030432314773,0.11955720350976454],"eta":[0.6875,0.6665,0.6445,0.6275,0.5885,0.597,0.5785,0.574,0.564,0.545,0.567,0.5375],"core":[0.27216411849828914,0.3816897530477157,0.5717883329230208,0.8309476095235993,0.9770374009568092,1.4733403681292259,2.4119455154090184,3.496070556306942,4.735024976312048,6.364101600032069,15.585757992583552,17.87515023252598],"fcore":[0.9497722337537546,0.9417995830899515,0.9289211853195553,0.9055699117748535,0.8687372078478058,0.8367552488701568,0.7601005298756023,0.7401240774684154,0.6821845397290786,0.6262722129672769,0.6909622303620526,0.6055652804358571],"halo":[1.0527093373018839,1.4940209372648532,2.1705340619834543,3.632627345327829,4.690705745909573,7.571841691479916,16.032190959259495,25.528453606917026,41.49346284548418,74.13060625866056,128.7690186153977,231.43063113875343]}};
  /* TABLE-END */
  const FIX = { phi: 7.209794853e-19, T: 300, k_f: 5, u_obj: 0.2, pitch: 4e-8, height: 3e-8, sidewall: 0.03490658503988659, px: 1e-9, t_ov: 1 };
  const SENS_IN = ['r_t', 'V_ex', 'p', 'V_land', 'I_p', 'WD', 'a_lens', 't_d', 'N_px', 'eta_c'];
  const SENS_OUT = ['d_p', 'I_beam', 'sigma_CD', 'MPH'];
  const NPW = 14, NTOL = 300, SEED = 8082026;
  const cache = new Map();
  function memo(key, f) {
    if (cache.has(key)) return cache.get(key);
    if (cache.size > 400) cache.clear();
    const v = f(); cache.set(key, v); return v;
  }
  // chapter 6 from the stored runs, log-linear in E, clamped to the stored range 0.5-30 keV
  function yields(mat, V) {
    const t = YT[mat], E = Math.min(30, Math.max(0.5, V / 1000)), le = Math.log(E);
    let i = 0; while (i < t.E.length - 2 && t.E[i + 1] < E) i++;
    const f = (le - Math.log(t.E[i])) / (Math.log(t.E[i + 1]) - Math.log(t.E[i]));
    const lin = a => a[i] + f * (a[i + 1] - a[i]), lg = a => Math.exp(Math.log(a[i]) + f * (Math.log(a[i + 1]) - Math.log(a[i])));
    return { delta: lg(t.delta), eta: lin(t.eta), core: lg(t.core) * 1e-9, fcore: lin(t.fcore), halo: lg(t.halo) * 1e-9 };
  }
  const src = (q) => memo('s' + [q.r_t, q.V_ex, q.p, q.t_clean].join(','), () => mods().ch02.compute({ r_t: q.r_t, V_ex: q.V_ex, phi: FIX.phi, T: FIX.T, p: q.p, t_clean: q.t_clean, k_f: FIX.k_f }));
  const lens = (q) => memo('l' + [q.a_lens, q.WD].join(','), () => mods().ch04.compute({ a_lens: q.a_lens, u_obj: FIX.u_obj, WD: q.WD, V_land: 800 }));
  // one pass through the machine; nom = the nominal source (for the current at fixed condensers); dz = defocus
  function chain(q, nom, dz, mcOff) {
    const M = mods(), s = q.srcOverride || src(q), L = lens(q);
    const Ibeam = q.I_p * (s.B_r * s.d_v * s.d_v) / (nom.B_r * nom.d_v * nom.d_v);
    const sp = M.ch05.compute({ C_s: L.C_s, C_c: L.C_c, B_r: s.B_r, dE: s.dE, dE50: s.dE50, V_land: q.V_land, alpha: 5e-3, I_p: Ibeam, probe_convention: 'fw50' });
    const a = sp.alpha_opt, dp = Math.sqrt(sp.d_p_opt * sp.d_p_opt + 2 * a * a * dz * dz);
    const y = yields(q.material, q.V_land);
    let m = null;
    try {
      m = M.ch07.compute({ d_p: dp, I_p: Ibeam, t_d: q.t_d, N_px: q.N_px, eta_c: q.eta_c, cd: q.cd, pitch: FIX.pitch, height: FIX.height, sidewall: FIX.sidewall,
        px: FIX.px, t_ov: FIX.t_ov, delta_SE: y.delta, eta_BSE: y.eta, sig_core: y.core, f_core: y.fcore, sig_halo: y.halo }, mcOff ? { mc: false } : undefined);
    } catch (e) { m = { sigma_CD: NaN, CD_meas: NaN, dose: q.I_p * q.t_d / (FIX.px * FIX.px), MPH: 1 / (q.N_px * q.N_px * q.t_d + FIX.t_ov) }; }
    return { d_p: dp, alpha_opt: a, I_beam: Ibeam, delta_SE: y.delta, eta_BSE: y.eta, f_core: y.fcore, sigma_CD: m.sigma_CD, CD_meas: m.CD_meas, dose: m.dose, MPH: m.MPH, C_c: L.C_c };
  }
  function compute(p) {
    const q = Object.assign({}, p), nom = src(q), base = chain(q, nom, 0, true);
    // sensitivities
    const sens = [];
    const rows = SENS_OUT.map(() => []);
    for (const k of SENS_IN) {
      const up = Object.assign({}, q), dn = Object.assign({}, q);
      up[k] = q[k] * 1.01; dn[k] = q[k] * 0.99;
      if (k === 'N_px') { up[k] = Math.round(q[k] * 1.01) || q[k] + 1; dn[k] = Math.round(q[k] * 0.99); }
      const a = chain(up, nom, 0, true), b = chain(dn, nom, 0, true), dx = Math.log(up[k] / dn[k]);
      SENS_OUT.forEach((o, i) => rows[i].push((Math.log(a[o]) - Math.log(b[o])) / dx));
    }
    rows.forEach(r => sens.push(...r));
    // process window: sigma_CD over V_land and I_p, best aperture at each point
    const pwin = [];
    for (let i = 0; i < NPW; i++) for (let j = 0; j < NPW; j++) {
      const V = 500 * Math.pow(10, i / (NPW - 1)), I = 1e-12 * Math.pow(1000, j / (NPW - 1));
      pwin.push(chain(Object.assign({}, q, { V_land: V, I_p: I }), nom, 0, true).sigma_CD);
    }
    // tolerance Monte Carlo
    const rnd = core.rng(SEED), g = () => Math.sqrt(-2 * Math.log(1 - rnd())) * Math.cos(2 * Math.PI * rnd());
    const grid = memo('g' + [q.r_t, q.V_ex, q.p, q.t_clean, q.tol_rt, q.tol_p].join(','), () => {
      const G = [];
      for (let i = 0; i < 5; i++) for (let j = 0; j < 5; j++) {
        const r = q.r_t * Math.exp((i - 2) * 1.5 * Math.log(1 + q.tol_rt)), pr = q.p * Math.exp((j - 2) * 1.5 * q.tol_p);
        G.push(mods().ch02.compute({ r_t: r, V_ex: q.V_ex, phi: FIX.phi, T: FIX.T, p: pr, t_clean: q.t_clean, k_f: FIX.k_f }));
      }
      return G;
    });
    const sr = 1.5 * Math.log(1 + q.tol_rt) || 1, spr = 1.5 * q.tol_p || 1;
    const interp = (u, v) => {                                             // u, v in grid steps from the centre
      const x = Math.min(2, Math.max(-2, u)) + 2, y = Math.min(2, Math.max(-2, v)) + 2, i = Math.min(3, Math.floor(x)), j = Math.min(3, Math.floor(y)), fx = x - i, fy = y - j;
      const at = (a, b, k) => Math.log(grid[5 * a + b][k]);
      const o = {};
      for (const k of ['B_r', 'dE', 'dE50', 'd_v']) o[k] = Math.exp((1 - fx) * (1 - fy) * at(i, j, k) + fx * (1 - fy) * at(i + 1, j, k) + (1 - fx) * fy * at(i, j + 1, k) + fx * fy * at(i + 1, j + 1, k));
      return o;
    };
    const dps = [], cds = [];
    let ok = 0;
    for (let n = 0; n < NTOL; n++) {
      const zr = g(), zp = g(), zi = g(), zz = g();
      const u = q.tol_rt > 0 ? zr * Math.log(1 + q.tol_rt) / sr : 0, v = q.tol_p > 0 ? zp * q.tol_p / spr : 0;
      const s = interp(u, v), dz = 2 * base.C_c * q.tol_NI * zi + q.tol_z * zz;
      const r = chain(Object.assign({}, q, { srcOverride: s }), nom, dz, true);
      dps.push(r.d_p); cds.push(r.sigma_CD);
      if (r.sigma_CD <= q.spec_cd) ok++;
    }
    const mean = a => a.reduce((x, y) => x + y, 0) / a.length;
    const sd = a => { const m = mean(a); return Math.sqrt(a.reduce((x, y) => x + (y - m) * (y - m), 0) / (a.length - 1)); };
    const srt = cds.filter(x => isFinite(x)).sort((x, y) => x - y);
    return {
      d_p: base.d_p, alpha_opt: base.alpha_opt, I_beam: base.I_beam, delta_SE: base.delta_SE, eta_BSE: base.eta_BSE, f_core: base.f_core,
      sigma_CD: base.sigma_CD, CD_meas: base.CD_meas, dose: base.dose, MPH: base.MPH, sens, pwin,
      tol_dp_sd: sd(dps), tol_cd_p95: srt.length ? srt[Math.min(srt.length - 1, Math.floor(0.95 * srt.length))] : NaN, tol_yield: ok / NTOL,
    };
  }

  // left: the measurement window (sigma_CD over landing voltage and current, the spec contour, the dose limit); right: the sensitivity table
  function draw(ctx, w, h, p, out) {
    ctx.clearRect(0, 0, w, h);
    const wide = w >= 620, pw = wide ? Math.floor(w * 0.52) : w, ph = wide ? h : Math.floor(h * 0.55);
    const L = 54, R = pw - 10, T = 22, B = ph - 36;
    ctx.font = "11px 'IBM Plex Mono', monospace";
    const cw = (R - L) / NPW, chh = (B - T) / NPW, lv = Math.log10(p.spec_cd);
    for (let i = 0; i < NPW; i++) for (let j = 0; j < NPW; j++) {
      const v = out.pwin[NPW * i + j], x = L + i * cw, y = B - (j + 1) * chh;
      let col = '#d9d0c2';
      if (isFinite(v)) { const t = Math.max(0, Math.min(1, (Math.log10(v) - lv + 1) / 2)); const a = v <= p.spec_cd ? 0.15 + 0.5 * (1 - t) : 0.06; col = v <= p.spec_cd ? 'rgba(122,31,43,' + a.toFixed(3) + ')' : 'rgba(58,50,46,' + (0.08 + 0.3 * t).toFixed(3) + ')'; }
      ctx.fillStyle = col; ctx.fillRect(x, y, cw + 0.5, chh + 0.5);
    }
    // dose limit: I_p t_d / px^2 = dose_max
    const Imax = p.dose_max * 1e-18 / p.t_d, jy = Math.log10(Imax / 1e-12) / 3;
    if (jy > 0 && jy < 1) { const y = B - jy * (B - T); ctx.strokeStyle = '#1c1518'; ctx.setLineDash([5, 3]); ctx.beginPath(); ctx.moveTo(L, y); ctx.lineTo(R, y); ctx.stroke(); ctx.setLineDash([]); ctx.fillStyle = '#1c1518'; ctx.textAlign = 'right'; ctx.fillText('dose limit', R - 2, y - 4); }
    // the present setting
    const xi = Math.log10(p.V_land / 500), yj = Math.log10(p.I_p / 1e-12) / 3;
    if (xi >= 0 && xi <= 1 && yj >= 0 && yj <= 1) { ctx.fillStyle = '#1c1518'; ctx.beginPath(); ctx.arc(L + xi * (R - L), B - yj * (B - T), 4, 0, 2 * Math.PI); ctx.fill(); }
    ctx.strokeStyle = '#d9d0c2'; ctx.strokeRect(L, T, R - L, B - T);
    ctx.fillStyle = '#6f655f'; ctx.textAlign = 'center';
    [[500, '0.5'], [1000, '1'], [2000, '2'], [5000, '5']].forEach(([V, t]) => ctx.fillText(t, L + Math.log10(V / 500) * (R - L), B + 14));
    ctx.fillText('landing voltage (kV)', (L + R) / 2, B + 28);
    ctx.textAlign = 'right';
    [[1e-12, '1 pA'], [1e-11, '10 pA'], [1e-10, '100 pA'], [1e-9, '1 nA']].forEach(([I, t]) => ctx.fillText(t, L - 4, B - Math.log10(I / 1e-12) / 3 * (B - T) + 4));
    ctx.textAlign = 'left'; ctx.fillStyle = '#3a322e';
    ctx.fillText('wine: σ_CD within spec', L, 13);
    // sensitivity table
    const x0 = wide ? pw + 12 : 8, y0 = wide ? 24 : ph + 18, colw = wide ? (w - x0 - 8) / 5 : (w - 16) / 5, rowh = wide ? (h - 40) / 11.5 : (h - ph - 24) / 11.5;
    const heads = ['d_p', 'I', 'σ_CD', 'rate'], names = ['tip r', 'V_ex', 'pressure', 'V_land', 'I_p', 'WD', 'lens a', 'dwell', 'lines', 'η_c'];
    ctx.fillStyle = '#3a322e'; ctx.textAlign = 'left'; ctx.fillText('(x/y) ∂y/∂x', x0, y0 - 8);
    heads.forEach((t, i) => { ctx.textAlign = 'right'; ctx.fillText(t, x0 + colw * (i + 2) - 4, y0 + rowh * 0.7); });
    names.forEach((t, r) => {
      const y = y0 + rowh * (r + 1.7);
      ctx.textAlign = 'left'; ctx.fillStyle = '#3a322e'; ctx.fillText(t, x0, y);
      for (let c = 0; c < 4; c++) {
        const v = out.sens[c * SENS_IN.length + r], a = Math.min(1, Math.abs(v));
        ctx.fillStyle = isFinite(v) ? (v > 0 ? 'rgba(122,31,43,' : 'rgba(58,50,46,') + (0.08 + 0.5 * a).toFixed(3) + ')' : '#eee';
        ctx.fillRect(x0 + colw * (c + 1) + 2, y - rowh * 0.72, colw - 4, rowh * 0.9);
        ctx.fillStyle = '#1c1518'; ctx.textAlign = 'right';
        ctx.fillText(isFinite(v) ? (Math.abs(v) < 0.005 ? '0' : (v > 0 ? '+' : '−') + Math.abs(v).toFixed(2)) : '–', x0 + colw * (c + 2) - 4, y);
      }
    });
  }

  return {
    id: 'ch08',
    inputs: ['r_t', 'V_ex', 'p', 't_clean', 'V_land', 'I_p', 'WD', 'a_lens', 'material', 't_d', 'N_px', 'eta_c', 'cd', 'tol_rt', 'tol_NI', 'tol_p', 'tol_z', 'spec_cd', 'dose_max'],
    outputs: ['d_p', 'alpha_opt', 'I_beam', 'delta_SE', 'eta_BSE', 'f_core', 'sigma_CD', 'CD_meas', 'dose', 'MPH', 'sens', 'pwin', 'tol_dp_sd', 'tol_cd_p95', 'tol_yield'],
    tolerance: { rel: 0, abs: 0, note: 'no Python twin: chapter 8 only chains the checked modules of chapters 2, 4, 5 and 7 and the stored runs of chapter 6; derive/ch08.py checks the chain against the separate chapters' },
    cases: [{}],
    ui: {
      controls: ['V_land', 'I_p', 't_d', 'N_px', 'material', 'r_t', 'V_ex', 'p', 't_clean', 'WD', 'a_lens', 'eta_c', 'cd', 'tol_rt', 'tol_NI', 'tol_p', 'tol_z', 'spec_cd', 'dose_max'],
      readouts: ['d_p', 'alpha_opt', 'I_beam', 'delta_SE', 'sigma_CD', 'CD_meas', 'dose', 'MPH', 'tol_dp_sd', 'tol_cd_p95', 'tol_yield'],
      aspect: '16 / 9', aspectPhone: '3 / 4',
      caption: 'The whole column at once. Left: the precision of a width over landing voltage and probe current, with the aperture set to its best angle at every point; wine squares meet the precision spec, darker grey ones miss it more, the dashed line is the dose limit for the dwell time chosen, and the dot is the present setting. Right: how strongly each output answers a one per cent change of each input (wine: rises with it, grey: falls). The readouts below include the tolerance Monte Carlo over tip radius, pressure, lens drift and wafer height.',
    },
    compute, draw, chain, yields, SENS_IN, SENS_OUT, FIX,
  };
});
