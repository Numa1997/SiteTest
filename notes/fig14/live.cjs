// Fig. 14: runs the page's live-preview worker (public/scripts/schrodinger-live-worker.js) unchanged in Node, with a stub
// postMessage, and compares its last frame with the stored Kaggle run. Usage: node notes/fig14/live.cjs [E V0 R ...]
'use strict';
const fs = require('fs'), vm = require('vm'), path = require('path'), zlib = require('zlib');
const ROOT = path.join(__dirname, '..', '..');
const src = fs.readFileSync(path.join(ROOT, 'public/scripts/schrodinger-live-worker.js'), 'utf8');
const DATA = path.join(ROOT, 'public/data/schrodinger-sphere/2026-11-12');
const idx = JSON.parse(fs.readFileSync(path.join(DATA, 'index.json'), 'utf8'));
function stored(E, V, R) {
    const r = idx.runs.find(q => Math.abs(q.E - E) < 1e-9 && Math.abs(q.V0 - V) < 1e-9 && Math.abs(q.R - R) < 1e-9);
    if (!r) return null;
    const b = fs.readFileSync(path.join(DATA, r.file)), H = b.readUInt32LE(4); return JSON.parse(b.slice(8, 8 + H).toString());
}
function live(E, V0, R) {
    return new Promise(res => {
        const frames = []; let t0;
        const ctx = { Math, Float32Array, Float64Array, Uint32Array, Uint8Array, Date, setTimeout: (f) => f(), String,
            postMessage: m => { if (m.type === 'frame') frames.push(m.curve); else if (m.type === 'done') res({ frames, ms: m.ms, steps: m.steps, wall: Date.now() - t0 }); else res({ error: m.message }); } };
        vm.createContext(ctx); vm.runInContext(src, ctx);
        t0 = Date.now(); ctx.onmessage({ data: { id: 1, E, V0, R } });
    });
}
(async () => {
    const a = process.argv.slice(2).map(Number), out = {};
    for (let i = 0; i < a.length; i += 3) {
        const [E, V0, R] = a.slice(i, i + 3), r = await live(E, V0, R), k = stored(E, V0, R), L = 64 * Math.min(1, Math.PI / (Math.sqrt(2 * E) + 0.67));
        const lf = r.frames[r.frames.length - 1], kf = k ? k.curves[k.curves.length - 1] : null;
        out[`${E}_${V0}_${R}`] = { L, dx: L / 64, steps: r.steps, dt: lf[0] / r.steps, ms: r.ms, live_end: lf, kaggle_end: kf };
        console.log(`E=${E} V0=${V0} R=${R}: box ${L.toFixed(2)} a, dx ${(L / 64).toFixed(3)} a, ${r.steps} steps of ${(lf[0] / r.steps).toFixed(4)}, ${(r.ms / 1000).toFixed(1)} s` +
            `\n   live   t=${lf[0].toFixed(2)} norm=${lf[1].toFixed(4)} behind=${lf[2].toFixed(4)} ahead=${lf[3].toFixed(4)} sy=${lf[4].toFixed(3)}` +
            (kf ? `\n   kaggle t=${kf[0].toFixed(2)} norm=${kf[1].toFixed(4)} behind=${kf[2].toFixed(4)} ahead=${kf[3].toFixed(4)} sy=${kf[4].toFixed(3)}` : ''));
        if (kf) { let m = 0; r.frames.forEach((f, j) => { const q = k.curves[j]; m = Math.max(m, Math.abs(f[2] - q[2]), Math.abs(f[3] - q[3])); }); console.log('   largest difference over all 48 frames, behind or ahead: ' + m.toFixed(4)); out[`${E}_${V0}_${R}`].maxdiff = m; }
    }
    fs.writeFileSync(path.join(__dirname, 'live-' + process.argv.slice(2).join('_') + '.json'), JSON.stringify(out, null, 1));
})();
