// Fig. 8 note, Figure 4 caption and section 6.2: corner rounding and overshoot of the K-term curve.
// Page code (resamp, dft, chainAt via pagecode.cjs); the curve evaluated at 601 points (as the page draws it) and at 60 001.
'use strict';
const P = require('./pagecode.cjs');
const TAU = 2 * Math.PI;
function curve(d, K, M) { const out = []; for (let i = 0; i <= M; i++) out.push(P.P60.chainAt(TAU * i / M, K, d.coefs)); return out; }
const R = {};
// square: corners of the centred square at (±0.7 − mx, ±0.7 − my)
{
    const d = P.decompose(P.SHAPES.square());
    R.square_mean = [d.mx, d.my];
    for (const M of [600, 60000]) for (const K of [10, 50]) {
        const c = curve(d, K, M);
        const corners = [[0.7, 0.7], [-0.7, 0.7], [-0.7, -0.7], [0.7, -0.7]].map(p => [p[0] - d.mx, p[1] - d.my]);
        // distance from each corner to the nearest curve point, measured along the diagonal: inside means toward the centre
        const inside = corners.map(q => Math.min(...c.map(p => Math.hypot(p.x - q[0], p.y - q[1]))));
        // crossing of the side lines: how far the curve goes beyond x = ±0.7 − mx or y = ±0.7 − my
        let over = 0, where = null;
        c.forEach(p => {
            const ex = Math.max(p.x - (0.7 - d.mx), -(p.x - (-0.7 - d.mx))), ey = Math.max(p.y - (0.7 - d.my), -(p.y - (-0.7 - d.my)));
            const e = Math.max(ex, ey); if (e > over) { over = e; where = [p.x, p.y]; }
        });
        R['square_K' + K + '_M' + M] = { corner_inside: inside, max_beyond_side: over, at: where };
    }
}
// open wave: ends at x = ±0.85 − mx
{
    const d = P.decompose(P.SHAPES.wave());
    for (const M of [600, 60000]) for (const K of [24, 50, 120]) {
        const c = curve(d, K, M);
        const xr = Math.max(...c.map(p => p.x)) - (0.85 - d.mx), xl = (-0.85 - d.mx) - Math.min(...c.map(p => p.x));
        R['wave_K' + K + '_M' + M] = { right_over: xr, left_over: xl, pct_right: 100 * xr / 1.7, pct_left: 100 * xl / 1.7 };
    }
}
console.log(JSON.stringify(R, null, 1));
require('fs').writeFileSync(__dirname + '/overshoot-out.json', JSON.stringify(R, null, 1));
