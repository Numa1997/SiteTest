/* marching.js: marching cubes on a rectangular grid, for the sheets of Fig. 14. Its own module so that both the page's 3D view
   (wave3d-view.js) and the worker that cuts the sheets off the main thread (fig14-iso-worker.js) use the same code.
   Tables from three.js (vendor/three/MarchingCubes.js, corner and edge order after Bourke). Docs: docs/scripts/wave3d-view.md. */
import { edgeTable, triTable } from '../vendor/three/MarchingCubes.js';

/* ---------- marching cubes on a rectangular grid: field[(i * ny + j) * nz + k] at (x0 + i h, y0 + j h, z0 + k h) ---------- */
/* corners as in vendor/three/MarchingCubes.js (Bourke): bit b of the cube index is set when corner b is below the level */
const CORNER = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]];
const EDGE = [[0, 1], [1, 2], [3, 2], [0, 3], [4, 5], [5, 6], [7, 6], [4, 7], [0, 4], [1, 5], [2, 6], [3, 7]];
export function marching(field, nx, ny, nz, level, sign, x0, y0, z0, h, hx) {   /* hx: the spacing along x when it differs from h */
    hx = hx || h;
    let cap = 1 << 16, pos = new Float32Array(cap), nor = new Float32Array(cap), n = 0;      /* grown as needed: no per-number pushes */
    const vx = new Float32Array(12 * 3), vn = new Float32Array(12 * 3);
    const at = (i, j, k) => sign * field[(i * ny + j) * nz + k];
    const grad = (i, j, k, out, o) => {         /* -grad of (sign * field): points from the crest out into lower values */
        const i0 = Math.max(0, i - 1), i1 = Math.min(nx - 1, i + 1), j0 = Math.max(0, j - 1), j1 = Math.min(ny - 1, j + 1), k0 = Math.max(0, k - 1), k1 = Math.min(nz - 1, k + 1);
        out[o] = -(at(i1, j, k) - at(i0, j, k)) / (i1 - i0) * (h / hx); out[o + 1] = -(at(i, j1, k) - at(i, j0, k)) / (j1 - j0); out[o + 2] = -(at(i, j, k1) - at(i, j, k0)) / (k1 - k0);
    };
    const g0 = new Float32Array(3), g1 = new Float32Array(3), val = new Float32Array(8);
    const sx = ny * nz, sy = nz, L = sign * level;                    /* sign * f < level  <=>  f < L (sign +1) or f > L (sign -1) */
    for (let i = 0; i < nx - 1; i++) for (let j = 0; j < ny - 1; j++) {
        let b = (i * ny + j) * nz;
        for (let k = 0; k < nz - 1; k++, b++) {
            /* the eight corners straight from the array; most cubes lie wholly on one side of the level and are left at once */
            const f0 = field[b], f1 = field[b + sx], f2 = field[b + sx + sy], f3 = field[b + sy], f4 = field[b + 1], f5 = field[b + sx + 1], f6 = field[b + sx + sy + 1], f7 = field[b + sy + 1];
            let ci;
            if (sign > 0) ci = (f0 < L ? 1 : 0) | (f1 < L ? 2 : 0) | (f2 < L ? 4 : 0) | (f3 < L ? 8 : 0) | (f4 < L ? 16 : 0) | (f5 < L ? 32 : 0) | (f6 < L ? 64 : 0) | (f7 < L ? 128 : 0);
            else ci = (f0 > L ? 1 : 0) | (f1 > L ? 2 : 0) | (f2 > L ? 4 : 0) | (f3 > L ? 8 : 0) | (f4 > L ? 16 : 0) | (f5 > L ? 32 : 0) | (f6 > L ? 64 : 0) | (f7 > L ? 128 : 0);
            if (ci === 0 || ci === 255) continue;
            const bits = edgeTable[ci]; if (!bits) continue;
            val[0] = sign * f0; val[1] = sign * f1; val[2] = sign * f2; val[3] = sign * f3; val[4] = sign * f4; val[5] = sign * f5; val[6] = sign * f6; val[7] = sign * f7;
            for (let e = 0; e < 12; e++) {
                if (!(bits & (1 << e))) continue;
                const a = EDGE[e][0], c2 = EDGE[e][1], A = CORNER[a], B = CORNER[c2];
                const t = (level - val[a]) / (val[c2] - val[a]);
                vx[3 * e] = x0 + hx * (i + A[0] + t * (B[0] - A[0])); vx[3 * e + 1] = y0 + h * (j + A[1] + t * (B[1] - A[1])); vx[3 * e + 2] = z0 + h * (k + A[2] + t * (B[2] - A[2]));
                grad(i + A[0], j + A[1], k + A[2], g0, 0); grad(i + B[0], j + B[1], k + B[2], g1, 0);
                let nxv = g0[0] + t * (g1[0] - g0[0]), nyv = g0[1] + t * (g1[1] - g0[1]), nzv = g0[2] + t * (g1[2] - g0[2]); const m = Math.hypot(nxv, nyv, nzv) || 1;
                vn[3 * e] = nxv / m; vn[3 * e + 1] = nyv / m; vn[3 * e + 2] = nzv / m;
            }
            const o = ci * 16;
            for (let q = 0; triTable[o + q] !== -1; q += 3) {
                let e0 = triTable[o + q], e1 = triTable[o + q + 1], e2 = triTable[o + q + 2];
                /* wind each triangle so that its face normal agrees with the gradient normal: lighting is then right on both sides.
                   (The test is made in physics axes; swapping y and z for three's axes mirrors the space and reverses the winding,
                   so a triangle agreeing here is kept as it is only when the dot product is negative.) */
                const ax = vx[3 * e1] - vx[3 * e0], ay = vx[3 * e1 + 1] - vx[3 * e0 + 1], az = vx[3 * e1 + 2] - vx[3 * e0 + 2];
                const bx = vx[3 * e2] - vx[3 * e0], by = vx[3 * e2 + 1] - vx[3 * e0 + 1], bz = vx[3 * e2 + 2] - vx[3 * e0 + 2];
                const fx = ay * bz - az * by, fy = az * bx - ax * bz, fz = ax * by - ay * bx;
                if (fx * (vn[3 * e0] + vn[3 * e1] + vn[3 * e2]) + fy * (vn[3 * e0 + 1] + vn[3 * e1 + 1] + vn[3 * e2 + 1]) + fz * (vn[3 * e0 + 2] + vn[3 * e1 + 2] + vn[3 * e2 + 2]) > 0) { const s = e1; e1 = e2; e2 = s; }
                if (n + 9 > cap) { cap *= 2; const p2 = new Float32Array(cap), n2 = new Float32Array(cap); p2.set(pos); n2.set(nor); pos = p2; nor = n2; }
                for (let w = 0; w < 3; w++) { const e = w === 0 ? e0 : w === 1 ? e1 : e2; pos[n] = vx[3 * e]; pos[n + 1] = vx[3 * e + 2]; pos[n + 2] = vx[3 * e + 1]; nor[n] = vn[3 * e]; nor[n + 1] = vn[3 * e + 2]; nor[n + 2] = vn[3 * e + 1]; n += 3; }   /* to three's axes */
            }
        }
    }
    return { pos: pos.slice(0, n), nor: nor.slice(0, n) };
}
