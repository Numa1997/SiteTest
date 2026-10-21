// Fig. 8 note checks that need more than the page's fixed N = 256: aliasing, the endpoint pause, the smooth figure eight.
// Runs the page's own resamp(), dft(), chainAt(), SHAPES (extracted verbatim by pagecode.cjs). Run: node notes/fig08/analyse.cjs
'use strict';
const P = require('./pagecode.cjs');
const TAU = 2 * Math.PI;
const R = {};
const byK = cs => { const m = {}; cs.forEach(c => { m[c.k] = c; }); return m; };
function relErr(d, K) { let kept = 0; for (let i = 0; i < K; i++) kept += d.coefs[i].amp ** 2; return Math.sqrt(Math.max(0, d.meanZ2 - kept)) / Math.sqrt(d.meanZ2); }

// --- 4.2 aliasing: page (256, L/255 spacing) against 65 536 samples; and the pure alias part (both periodic L/N spacing)
for (const name of ['heart', 'wave', 'square', 'eight']) {
    const pts = P.SHAPES[name]();
    const d256 = P.decompose(pts, 256), d64k = P.decompose(pts, 65536);
    const per256 = (() => { const q = P.resampPeriodic(pts, 256); const c = P.centre(q.r); return Object.assign(c, { coefs: P.P60.dft(c.samples) }); })();
    const per64k = (() => { const q = P.resampPeriodic(pts, 65536); const c = P.centre(q.r); return Object.assign(c, { coefs: P.P60.dft(c.samples) }); })();
    const a = byK(d256.coefs), b = byK(d64k.coefs), pa = byK(per256.coefs), pb = byK(per64k.coefs);
    const top3 = d64k.coefs.slice(0, 3).map(c => c.k);
    R[name] = {
        L: d256.L, step: d256.step, E: d256.meanZ2,
        top3_k: top3,
        top3_rel_change_page_vs_64k: top3.map(k => Math.abs(a[k].amp / b[k].amp - 1)),
        near60: [56, 58, 60, -56, -58, -60, 59, -59, 57, -57].map(k => ({ k, page: a[k].amp, ref64k: b[k].amp, rel_page_vs_64k: a[k].amp / b[k].amp - 1, rel_alias_only: pa[k].amp / pb[k].amp - 1 })),
        relErr: { K1: relErr(d256, 1), K10: relErr(d256, 10), K24: relErr(d256, 24), K50: relErr(d256, 50), K80: relErr(d256, 80), K100: relErr(d256, 100), K120: relErr(d256, 120) },
        relErr_periodic_K120: relErr(per256, 120),
        // Fig. 3 caption: split e_K^2 at K = 80 into computed-but-unused and not computed (|k| > 60)
        split_K80: (() => { let all = 0, used = 0; d256.coefs.forEach((c, i) => { all += c.amp ** 2; if (i < 80) used += c.amp ** 2; }); return { computed_unused: all - used, not_computed: d256.meanZ2 - all, rel_floor: Math.sqrt(d256.meanZ2 - all) / Math.sqrt(d256.meanZ2) }; })()
    };
    if (name === 'eight') {
        // "computed from the shape itself": many samples, periodic spacing, no pause
        R.eight.shape_radii = [1, -1, 10, -10, 20, -20, 30, -30, 40, -40].map(k => [k, pb[k].amp]);
        R.eight.page_c60 = [a[60].amp, a[-60].amp];
        R.eight.estimate_pause_c60 = d256.step / (TAU * 60);
    }
    if (name === 'square') {
        R.square.page_radii = [1, -3, 5, 2, -1, -7].map(k => [k, a[k].amp]);
        R.square.eq14 = [1, -3, 5].map(k => Math.SQRT2 * d256.L / (Math.PI * Math.PI * k * k));
        R.square.first4 = d256.coefs.slice(0, 4).map(c => c.k);
        R.square.ratio_page_to_eq14 = [1, -3, 5].map(k => a[k].amp / (Math.SQRT2 * d256.L / (Math.PI * Math.PI * k * k)));
        R.square.ratio_periodic_to_eq14 = [1, -3, 5].map(k => pa[k].amp / (Math.SQRT2 * d256.L / (Math.PI * Math.PI * k * k)));
        R.square.periodic_k2_km1 = [pa[2].amp, pa[-1].amp];
    }
    if (name === 'heart') R.heart.k2c = [10, 20, 30, -10, -20, -30].map(k => [k, k * k * a[k].amp]);
    if (name === 'wave') R.wave.kc10 = [10 * a[10].amp, 10 * a[-10].amp];
}

// --- 4.3 timing of dft() alone in Node (V8); Chromium timing is in measure.cjs
{
    const d = P.decompose(P.SHAPES.heart(), 256);
    const t0 = process.hrtime.bigint(); for (let i = 0; i < 200; i++) P.P60.dft(d.samples); const t1 = process.hrtime.bigint();
    R.node_dft_ms = Number(t1 - t0) / 1e6 / 200;
}
console.log(JSON.stringify(R, null, 1));
require('fs').writeFileSync(__dirname + '/analyse-out.json', JSON.stringify(R, null, 1));
