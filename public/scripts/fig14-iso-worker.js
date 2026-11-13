/* fig14-iso-worker.js: cuts the sheets Re psi = +c and -c of Fig. 14 off the page's main thread (a module worker).
   In: { id, F (Float32Array: Re psi on nx * ny * nz points, h apart from (x0, y0, z0)), level, upx, upy }.
   The field is first resampled finer (1/upx along x, 1/upy along y and z) with the Lanczos kernel of three lobes, which returns
   the stored values at the stored points; then marching cubes (marching.js) finds the triangles of both sheets.
   Out: { id, crest: { pos, nor }, trough: { pos, nor } } as Float32Arrays in three's axes. Docs: docs/scripts/wave3d-view.md. */
import { marching } from './marching.js';
let UP = null;
function lanczos(x) { if (x === 0) return 1; if (Math.abs(x) >= 3) return 0; const px = Math.PI * x; return 3 * Math.sin(px) * Math.sin(px / 3) / (px * px); }
function upAxis(n, fac) { const m = Math.round(n * fac), I = new Int32Array(m * 6), W = new Float32Array(m * 6); for (let a = 0; a < m; a++) { const u = a / fac, b = Math.floor(u); let s = 0; for (let t = 0; t < 6; t++) { const i = b - 2 + t, w = lanczos(u - i); I[a * 6 + t] = Math.max(0, Math.min(n - 1, i)); W[a * 6 + t] = w; s += w; } for (let t = 0; t < 6; t++) W[a * 6 + t] /= s; } return { m, I, W }; }
function upsample(F, nx, ny, nz, fx, fy) {
    if (!UP || UP.nx !== nx || UP.ny !== ny || UP.fx !== fx || UP.fy !== fy) { const ax = upAxis(nx, fx), ay = upAxis(ny, fy); UP = { nx, ny, fx, fy, ax, ay, A: new Float32Array(ax.m * ny * nz), B: new Float32Array(ax.m * ay.m * nz), C: new Float32Array(ax.m * ay.m * ay.m) }; }
    const ax = UP.ax, ay = UP.ay, mx = ax.m, my = ay.m, A = UP.A, B = UP.B, C = UP.C, s1 = ny * nz;
    for (let a = 0; a < mx; a++) { const o = a * s1; for (let q = 0; q < s1; q++) A[o + q] = 0; for (let t = 0; t < 6; t++) { const w = ax.W[a * 6 + t], src = ax.I[a * 6 + t] * s1; for (let q = 0; q < s1; q++) A[o + q] += w * F[src + q]; } }
    for (let a = 0; a < mx; a++) for (let j = 0; j < my; j++) { const o = (a * my + j) * nz; for (let k = 0; k < nz; k++) B[o + k] = 0; for (let t = 0; t < 6; t++) { const w = ay.W[j * 6 + t], s2 = (a * ny + ay.I[j * 6 + t]) * nz; for (let k = 0; k < nz; k++) B[o + k] += w * A[s2 + k]; } }
    for (let a = 0; a < mx * my; a++) { const o = a * my, s3 = a * nz; for (let k = 0; k < my; k++) { const k6 = k * 6; C[o + k] = ay.W[k6] * B[s3 + ay.I[k6]] + ay.W[k6 + 1] * B[s3 + ay.I[k6 + 1]] + ay.W[k6 + 2] * B[s3 + ay.I[k6 + 2]] + ay.W[k6 + 3] * B[s3 + ay.I[k6 + 3]] + ay.W[k6 + 4] * B[s3 + ay.I[k6 + 4]] + ay.W[k6 + 5] * B[s3 + ay.I[k6 + 5]]; } }
    return { F: C, nx: mx, ny: my, nz: my };
}
self.onmessage = (e) => {
    const m = e.data, U = upsample(m.F, m.nx, m.ny, m.nz, m.upx, m.upy), h = m.h / m.upy, hx = m.h / m.upx;
    const c = marching(U.F, U.nx, U.ny, U.nz, m.level, 1, m.x0, m.y0, m.z0, h, hx), t = marching(U.F, U.nx, U.ny, U.nz, m.level, -1, m.x0, m.y0, m.z0, h, hx);
    self.postMessage({ id: m.id, crest: c, trough: t }, [c.pos.buffer, c.nor.buffer, t.pos.buffer, t.nor.buffer]);
};
self.postMessage({ ready: true });
