// Fig. 8: (a) the alias-only change of the heart's three largest radii (both transforms sampled at spacing L/N, no repeated
// start point, so only aliasing differs); (b) the figure eight's radii from the exact parametric curve at equal arc length.
// Runs the page's dft() (verbatim via pagecode.cjs). Run: node notes/fig08/analyse2.cjs
'use strict';
const P = require('./pagecode.cjs');
const TAU = 2 * Math.PI;
const byK = cs => { const m = {}; cs.forEach(c => { m[c.k] = c; }); return m; };
function periodicCoefs(pts, N) { const q = P.resampPeriodic(pts, N); const c = P.centre(q.r); return byK(P.P60.dft(c.samples)); }
const out = {};
for (const name of ['heart', 'wave']) {
    const pts = P.SHAPES[name]();
    const a = periodicCoefs(pts, 256), b = periodicCoefs(pts, 65536);
    const top = Object.values(b).sort((p, q) => q.amp - p.amp).slice(0, 3).map(c => c.k);
    out[name + '_alias_only_top3'] = top.map(k => [k, a[k].amp / b[k].amp - 1]);
}
// exact parametric figure eight: x = 0.85 sin u, y = 0.85 sin u cos u; arc length by a fine trapezoid sum
{
    const M = 400000, xs = [], ys = [];
    for (let i = 0; i <= M; i++) { const u = TAU * i / M; xs.push(0.85 * Math.sin(u)); ys.push(0.85 * Math.sin(u) * Math.cos(u)); }
    const pts = xs.map((x, i) => ({ x, y: ys[i] }));
    const c = periodicCoefs(pts, 65536);
    out.eight_exact = [1, 10, 20, 30, 40].map(k => [k, c[k].amp]);
}
console.log(JSON.stringify(out, null, 1));
require('fs').writeFileSync(__dirname + '/analyse2-out.json', JSON.stringify(out, null, 1));
