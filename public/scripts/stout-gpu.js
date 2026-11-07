/* Fig. 12: the stout solver on the reader's graphics chip (WebGPU compute shaders).
 *
 * The same equations and the same method as the CPU solver in stout-cart.js (Fluid): the incompressible Navier–Stokes
 * equations in the glass's frame,
 *     Du/Dt = -grad(p)/rho + nu lap(u) + g - a_glass(t),   div u = 0,   p = 0 on the free surface,
 * solved by APIC (particles carry velocity and its gradient) on a staggered MAC grid with the glass wall cut through the
 * cells (open face fractions), a Zhu–Bridson level set from the particles with images in the wall, ghost-fluid pressure at
 * the surface, and a pressure Poisson solve by conjugate gradients. Differences from the CPU solver, each stated in the
 * lecture note: the whole glass is computed (no mirror plane, so the stout can swirl); float32 arithmetic; the pressure
 * solve is Jacobi-preconditioned CG in one 256-thread workgroup (the CPU uses MIC(0)); the particle-to-grid transfer is
 * a gather over the particles sorted by cell (each cell's list in particle order), so every sum is formed in a fixed order
 * and a run repeats exactly on one device; the cut-cell "inherit" rule for wall cells is two Jacobi passes instead of two
 * sweeps. Nothing is modelled that the CPU solver does not model, and nothing of it is left out.
 *
 * Runs only in a browser with WebGPU (navigator.gpu). A step is asynchronous: GpuFluid.steps(list) runs several steps in
 * one submission and reads back what the cart and the probes need (momentum, spill, column counts, the fastest particle),
 * once per batch. World.advanceGpu in stout-cart.js drives it. Units SI throughout.
 */
(function (root) {
  'use strict';

  const WG = 256;

  // ------------------------------------------------------------------ shaders
  // Common declarations: the parameters of the grid and the step. One uniform block, written once per step.
  const COMMON = /* wgsl */`
struct P {
  nx: i32, ny: i32, nz: i32, nc: i32,
  np: i32, npCap: i32, oV: i32, oW: i32,
  dx: f32, x0: f32, y0: f32, H: f32,
  dt: f32, ax: f32, az: f32, g: f32,
  nu: f32, rp: f32, Rk: f32, zRim: f32,
  Rrim: f32, Rbox: f32, Vp: f32, sliver: f32,
  thetaMin: f32, forcedPhi: f32, tol: f32, maxIt: f32,
  nProf: i32, dzProf: f32, pad1: f32, pad2: f32,
};
@group(0) @binding(0) var<uniform> P_: P;
@group(0) @binding(1) var<uniform> profV: array<vec4f, 128>;      // the glass's inner radius every dzProf (the measured tulip), 4 to a vec4
fn prof(i: i32) -> f32 { return profV[i >> 2u][i & 3]; }
// the three face arrays of a MAC quantity live in one buffer: u from 0, v from oV, w from oW
fn off(comp: i32) -> i32 { return select(select(P_.oW, P_.oV, comp == 1), 0, comp == 0); }

// inner radius of the glass at height z; above the rim there is no wall
fn Rz(z: f32) -> f32 {
  if (z > P_.zRim) { return 10.0; }
  let f = max(z, 0.0) / P_.dzProf; let i = i32(floor(f));
  if (i >= P_.nProf - 1) { return prof(P_.nProf - 1); }
  return prof(i) + (f - f32(i)) * (prof(i + 1) - prof(i));
}
fn dRz(z: f32) -> f32 {
  if (z >= P_.zRim) { return 0.0; }
  let f = max(z, 0.0) / P_.dzProf; let i = min(P_.nProf - 2, i32(floor(f)));
  return (prof(i + 1) - prof(i)) / P_.dzProf;
}
fn cellId(i: i32, j: i32, k: i32) -> i32 { return i + P_.nx * (j + P_.ny * k); }
fn U(i: i32, j: i32, k: i32) -> i32 { return i + (P_.nx + 1) * (j + P_.ny * k); }
fn V(i: i32, j: i32, k: i32) -> i32 { return i + P_.nx * (j + (P_.ny + 1) * k); }
fn Wf(i: i32, j: i32, k: i32) -> i32 { return i + P_.nx * (j + P_.ny * k); }
`;

  // 1. Counting sort of the particles by cell. pos: xyz + w (w < 0: dead). Dead particles get no cell and vanish from the
  //    sorted arrays, which become next step's particle arrays (np = cellStart[nc]).
  const SORT = COMMON + /* wgsl */`
@group(0) @binding(2) var<storage, read> posA: array<vec4f>;
@group(0) @binding(3) var<storage, read_write> cnt: array<atomic<i32>>;    // nc + 1: counts, then cellStart (scan)
@group(0) @binding(4) var<storage, read_write> pcell: array<i32>;         // cell of particle p (-1: dead)
@group(0) @binding(5) var<storage, read_write> fillp: array<atomic<i32>>; // scatter pointers
@group(0) @binding(6) var<storage, read_write> order: array<i32>;         // sorted slot -> original particle
@group(0) @binding(7) var<storage, read_write> cellStart: array<i32>;     // nc + 1
@group(0) @binding(8) var<storage, read> nslot: array<i32>;              // the slots the previous sort filled (live and dead)

@compute @workgroup_size(${WG})
fn count(@builtin(global_invocation_id) id: vec3u) {
  let p = i32(id.x); if (p >= nslot[0]) { return; }
  let q = posA[p];
  if (q.w < 0.0) { pcell[p] = -1; return; }
  var i = i32(floor((q.x - P_.x0) / P_.dx)); var j = i32(floor((q.y - P_.y0) / P_.dx)); var k = i32(floor(q.z / P_.dx));
  i = clamp(i, 0, P_.nx - 1); j = clamp(j, 0, P_.ny - 1); k = clamp(k, 0, P_.nz - 1);
  let c = cellId(i, j, k); pcell[p] = c; atomicAdd(&cnt[c], 1);
}
// exclusive prefix sum over the nc counts, one workgroup (nc is at most a few tens of thousands)
var<workgroup> sh: array<i32, ${WG}>;
@compute @workgroup_size(${WG})
fn scan(@builtin(local_invocation_id) lid: vec3u) {
  let t = i32(lid.x); let n = P_.nc; let per = (n + ${WG} - 1) / ${WG};
  let a = t * per; let b = min(n, a + per);
  var s = 0; for (var c = a; c < b; c++) { s += atomicLoad(&cnt[c]); }
  sh[t] = s; workgroupBarrier();
  if (t == 0) { var acc = 0; for (var u = 0; u < ${WG}; u++) { let v = sh[u]; sh[u] = acc; acc += v; } cellStart[n] = acc; }
  workgroupBarrier();
  var acc = sh[t];
  for (var c = a; c < b; c++) { cellStart[c] = acc; atomicStore(&fillp[c], acc); acc += atomicLoad(&cnt[c]); }
}
@compute @workgroup_size(${WG})
fn scatter(@builtin(global_invocation_id) id: vec3u) {
  let p = i32(id.x); if (p >= nslot[0]) { return; }
  let c = pcell[p]; if (c < 0) { return; }
  let s = atomicAdd(&fillp[c], 1); order[s] = p;
}
// each cell's list in particle order (insertion sort of a short list): the sums below are then formed in a fixed order
@compute @workgroup_size(${WG})
fn sortCell(@builtin(global_invocation_id) id: vec3u) {
  let c = i32(id.x); if (c >= P_.nc) { return; }
  let a = cellStart[c]; let b = cellStart[c + 1];
  for (var s = a + 1; s < b; s++) {
    let v = order[s]; var t = s - 1;
    while (t >= a && order[t] > v) { order[t + 1] = order[t]; t--; }
    order[t + 1] = v;
  }
}
`;
  // 2. Permute the particle arrays into cell order (the sorted arrays are the step's working set and next step's input).
  const PERMUTE = COMMON + /* wgsl */`
@group(0) @binding(2) var<storage, read> cellStart: array<i32>;
@group(0) @binding(3) var<storage, read> order: array<i32>;
@group(0) @binding(4) var<storage, read> posA: array<vec4f>;
@group(0) @binding(5) var<storage, read> velA: array<vec4f>;
@group(0) @binding(6) var<storage, read> cA: array<vec4f>;      // 3 vec4 per particle: rows of the APIC gradient (du/dx,du/dy,du/dz), (dv/..), (dw/..)
@group(0) @binding(7) var<storage, read_write> posB: array<vec4f>;
@group(0) @binding(8) var<storage, read_write> velB: array<vec4f>;
@group(0) @binding(9) var<storage, read_write> cB: array<vec4f>;
@compute @workgroup_size(${WG})
fn permute(@builtin(global_invocation_id) id: vec3u) {
  let s = i32(id.x); if (s >= cellStart[P_.nc]) { return; }   // the live particles: those the sort counted
  let p = order[s];
  posB[s] = posA[p]; velB[s] = velA[p]; cB[3 * s] = cA[3 * p]; cB[3 * s + 1] = cA[3 * p + 1]; cB[3 * s + 2] = cA[3 * p + 2];
}
`;
  // 3. Level set. Masks per cell, then phi where a search is needed (Zhu & Bridson 2005: phi = |x - xbar| - r, xbar the
  //    kernel-weighted mean of the particles within Rk = 2 dx, each with its image in the wall near the wall).
  const LEVELSET = COMMON + /* wgsl */`
@group(0) @binding(2) var<storage, read> cellStart: array<i32>;
@group(0) @binding(3) var<storage, read> pos: array<vec4f>;
@group(0) @binding(4) var<storage, read_write> maskA: array<u32>;   // bit 0: empty (no particle, inside the glass); bit 1: near (within 2 cells of an empty cell); bit 2: occ dilated; bit 3: a particle with a wall image lies here
@group(0) @binding(5) var<storage, read_write> maskB: array<u32>;   // scratch for the dilations
@group(0) @binding(6) var<storage, read_write> phi: array<f32>;
@group(0) @binding(7) var<storage, read_write> fluid: array<u32>;
@group(0) @binding(8) var<storage, read_write> imgF: array<f32>;    // per sorted particle: (2R - r)/r, or 0 when it has no wall image

fn ijk(c: i32) -> vec3i { let nxy = P_.nx * P_.ny; return vec3i(c % P_.nx, (c / P_.nx) % P_.ny, c / nxy); }

// per cell: empty and occupied; per particle: its wall image (the same numbers the CPU's levelSetParticles makes)
@compute @workgroup_size(${WG})
fn masks(@builtin(global_invocation_id) id: vec3u) {
  let c = i32(id.x); if (c >= P_.nc) { return; }
  let q = ijk(c); let dx = P_.dx;
  let Rc = min(Rz((f32(q.z) + 0.5) * dx), P_.Rbox) - 0.5 * dx;
  let xc = P_.x0 + (f32(q.x) + 0.5) * dx; let yc = P_.y0 + (f32(q.y) + 0.5) * dx;
  let n = cellStart[c + 1] - cellStart[c];
  var m: u32 = 0u;
  if (n == 0 && xc * xc + yc * yc < Rc * Rc) { m |= 1u; }
  if (n > 0) { m |= 4u; }
  var img = 0u;
  for (var s = cellStart[c]; s < cellStart[c + 1]; s++) {
    let p = pos[s]; let rr = sqrt(p.x * p.x + p.y * p.y); let Rw = Rz(p.z);
    let has = p.z < P_.zRim && rr > Rw - P_.Rk;
    imgF[s] = select(0.0, select(0.0, (2.0 * Rw - rr) / rr, rr > 1e-9), has);
    if (has) { img = 8u; }
  }
  maskA[c] = m | img;
}
// dilate bits 0 (empty -> near, bit 1) and 2 (occupied) by 2 cells along one axis; src/dst alternate (ping-pong)
fn dil(c: i32, axis: i32, srcIsA: bool) -> u32 {
  let q = ijk(c);
  let st = select(select(P_.nx * P_.ny, P_.nx, axis == 1), 1, axis == 0);
  let a = select(select(q.z, q.y, axis == 1), q.x, axis == 0);
  let n = select(select(P_.nz, P_.ny, axis == 1), P_.nx, axis == 0);
  let lo = select(-2, -a, a < 2); let hi = select(2, n - 1 - a, a + 2 >= n);
  var e = 0u; var o = 0u;
  for (var d = lo; d <= hi; d++) {
    let v = select(maskB[c + d * st], maskA[c + d * st], srcIsA);
    if ((v & 2u) != 0u) { e = 2u; }
    if ((v & 4u) != 0u) { o = 4u; }
  }
  let keep = select(maskB[c], maskA[c], srcIsA) & 9u;   // bits 0 and 3 ride along
  return keep | e | o;
}
// the first dilation reads "empty" as the seed of "near"
@compute @workgroup_size(${WG})
fn dilate0(@builtin(global_invocation_id) id: vec3u) {
  let c = i32(id.x); if (c >= P_.nc) { return; }
  let m = maskA[c]; maskA[c] = m | select(0u, 2u, (m & 1u) != 0u);
}
@compute @workgroup_size(${WG})
fn dilateX(@builtin(global_invocation_id) id: vec3u) { let c = i32(id.x); if (c >= P_.nc) { return; } maskB[c] = dil(c, 0, true); }
@compute @workgroup_size(${WG})
fn dilateY(@builtin(global_invocation_id) id: vec3u) { let c = i32(id.x); if (c >= P_.nc) { return; } maskA[c] = dil(c, 1, false); }
@compute @workgroup_size(${WG})
fn dilateZ(@builtin(global_invocation_id) id: vec3u) { let c = i32(id.x); if (c >= P_.nc) { return; } maskB[c] = dil(c, 2, true); }

// phi at the cell centre: the search over the 5 x 5 x 5 block; cells whose nearest point is 2 dx or more away are
// skipped unless one of their particles has a wall image (the CPU's blockOff table, in the same order)
@compute @workgroup_size(${WG})
fn phiCells(@builtin(global_invocation_id) id: vec3u) {
  let c = i32(id.x); if (c >= P_.nc) { return; }
  let m = maskB[c]; let dx = P_.dx; let n = cellStart[c + 1] - cellStart[c];
  if ((m & 2u) == 0u) { phi[c] = select(2.0 * dx, -2.0 * dx, n > 0); return; }   // not near the surface: liquid or air by occupancy
  if ((m & 4u) == 0u) { phi[c] = 3.0 * dx; return; }                              // no particle within reach
  let q = ijk(c);
  let x = P_.x0 + (f32(q.x) + 0.5) * dx; let y = P_.y0 + (f32(q.y) + 0.5) * dx; let z = (f32(q.z) + 0.5) * dx;
  let R2 = P_.Rk * P_.Rk;
  var W = 0.0; var sx = 0.0; var sy = 0.0; var sz = 0.0;
  for (var dk = -2; dk <= 2; dk++) { for (var dj = -2; dj <= 2; dj++) { for (var di = -2; di <= 2; di++) {
    let i = q.x + di; let j = q.y + dj; let k = q.z + dk;
    if (i < 0 || i >= P_.nx || j < 0 || j >= P_.ny || k < 0 || k >= P_.nz) { continue; }
    let gi = select((abs(f32(di)) - 0.5) * (abs(f32(di)) - 0.5), 0.0, abs(di) < 1);
    let gj = select((abs(f32(dj)) - 0.5) * (abs(f32(dj)) - 0.5), 0.0, abs(dj) < 1);
    let gk = select((abs(f32(dk)) - 0.5) * (abs(f32(dk)) - 0.5), 0.0, abs(dk) < 1);
    let reach = gi + gj + gk < 4.0;
    let cc = cellId(i, j, k);
    if (!reach && (maskB[cc] & 8u) == 0u) { continue; }
    for (var s = cellStart[cc]; s < cellStart[cc + 1]; s++) {
      let p = pos[s]; let ddz = p.z - z; let dz2 = ddz * ddz;
      if (reach) {
        let ddx = p.x - x; let ddy = p.y - y; let d2 = ddx * ddx + ddy * ddy + dz2;
        if (d2 < R2) { let u = 1.0 - d2 / R2; let wt = u * u * u; W += wt; sx += wt * p.x; sy += wt * p.y; sz += wt * p.z; }
      }
      let fw = imgF[s];
      if (fw != 0.0) {
        let qx = p.x * fw; let qy = p.y * fw; let ddx = qx - x; let ddy = qy - y; let d2 = ddx * ddx + ddy * ddy + dz2;
        if (d2 < R2) { let u = 1.0 - d2 / R2; let wt = u * u * u; W += wt; sx += wt * qx; sy += wt * qy; sz += wt * p.z; }
      }
    }
  } } }
  if (W < 1e-12) { phi[c] = 3.0 * dx; return; }
  let mx = sx / W - x; let my = sy / W - y; let mz = sz / W - z;
  phi[c] = sqrt(mx * mx + my * my + mz * mz) - P_.rp;
}
// liquid cells: phi < 0 or holding particles (then phi at least -forcedPhi dx)
@compute @workgroup_size(${WG})
fn flags(@builtin(global_invocation_id) id: vec3u) {
  let c = i32(id.x); if (c >= P_.nc) { return; }
  let n = cellStart[c + 1] - cellStart[c];
  var ph = phi[c];
  let fl = ph < 0.0 || n > 0;
  if (n > 0 && ph >= 0.0) { ph = -P_.forcedPhi * P_.dx; phi[c] = ph; }
  fluid[c] = select(0u, 1u, fl);
}
`;
  // 3b. The wall cells: a cut cell is liquid when it shares an open face with liquid beside it, or above it well below the
  //     surface (Fluid.inheritWallPhi). Jacobi form: reads the flags of the previous pass (maskB used as the copy).
  const INHERIT = COMMON + /* wgsl */`
@group(0) @binding(2) var<storage, read> faces: array<f32>;   // open fractions: u faces, then v from oV, w from oW
@group(0) @binding(3) var<storage, read_write> phi: array<f32>;
@group(0) @binding(4) var<storage, read_write> fluid: array<u32>;
@group(0) @binding(5) var<storage, read_write> flagCopy: array<u32>;
@group(0) @binding(6) var<storage, read_write> phiCopy: array<f32>;
fn au(n: i32) -> f32 { return faces[n]; }
fn av(n: i32) -> f32 { return faces[P_.oV + n]; }
fn aw(n: i32) -> f32 { return faces[P_.oW + n]; }
fn ijk(c: i32) -> vec3i { let nxy = P_.nx * P_.ny; return vec3i(c % P_.nx, (c / P_.nx) % P_.ny, c / nxy); }
@compute @workgroup_size(${WG})
fn copy(@builtin(global_invocation_id) id: vec3u) { let c = i32(id.x); if (c >= P_.nc) { return; } flagCopy[c] = fluid[c]; phiCopy[c] = phi[c]; }
@compute @workgroup_size(${WG})
fn inherit(@builtin(global_invocation_id) id: vec3u) {
  let c = i32(id.x); if (c >= P_.nc) { return; }
  if (flagCopy[c] != 0u) { return; }
  let q = ijk(c); let dx = P_.dx;
  let x = P_.x0 + (f32(q.x) + 0.5) * dx; let y = P_.y0 + (f32(q.y) + 0.5) * dx; let R = Rz((f32(q.z) + 0.5) * dx);
  if (R > P_.Rbox || x * x + y * y < (R - 0.5 * dx) * (R - 0.5 * dx)) { return; }   // only cells cut by the wall
  var best = 1.0; let nxy = P_.nx * P_.ny;
  if (q.x > 0 && au(U(q.x, q.y, q.z)) > 0.0 && flagCopy[c - 1] != 0u) { best = min(best, phiCopy[c - 1]); }
  if (q.x < P_.nx - 1 && au(U(q.x + 1, q.y, q.z)) > 0.0 && flagCopy[c + 1] != 0u) { best = min(best, phiCopy[c + 1]); }
  if (q.y > 0 && av(V(q.x, q.y, q.z)) > 0.0 && flagCopy[c - P_.nx] != 0u) { best = min(best, phiCopy[c - P_.nx]); }
  if (q.y < P_.ny - 1 && av(V(q.x, q.y + 1, q.z)) > 0.0 && flagCopy[c + P_.nx] != 0u) { best = min(best, phiCopy[c + P_.nx]); }
  if (q.z < P_.nz - 1 && aw(Wf(q.x, q.y, q.z + 1)) > 0.0 && flagCopy[c + nxy] != 0u && phiCopy[c + nxy] < -0.5 * dx) { best = min(best, phiCopy[c + nxy]); }
  if (best < 1.0) { fluid[c] = 1u; phi[c] = min(best, -0.05 * dx); }
}
`;
  // 4. Particle-to-grid by gathering: a face node of component comp sums, over the particles whose trilinear stencil holds
  //    it, w (u_p + C_p . (x_node - x_p)) and w, in cell order and particle order (Fluid.transfer's terms).
  const P2G = COMMON + /* wgsl */`
@group(0) @binding(2) var<storage, read> cellStart: array<i32>;
@group(0) @binding(3) var<storage, read> pos: array<vec4f>;
@group(0) @binding(4) var<storage, read> vel: array<vec4f>;
@group(0) @binding(5) var<storage, read> cg: array<vec4f>;
@group(0) @binding(6) var<storage, read_write> grid: array<f32>;   // u, then v from oV, w from oW
fn gather(comp: i32, n: i32) -> f32 {
  let nx = P_.nx; let ny = P_.ny; let nz = P_.nz; let dx = P_.dx; let inv = 1.0 / dx;
  var sx = nx; var sy = ny; var sz = nz; var ox = 0.5; var oy = 0.5; var oz = 0.5;
  if (comp == 0) { sx = nx + 1; ox = 0.0; } else if (comp == 1) { sy = ny + 1; oy = 0.0; } else { sz = nz + 1; oz = 0.0; }
  let i = n % sx; let j = (n / sx) % sy; let k = n / (sx * sy);
  // the node's position in cells: nodes sit at (i + ox, j + oy, k + oz); a particle at (fx, fy, fz) (in cells, from the
  // node lattice's origin) reaches nodes floor(fx) and floor(fx) + 1
  let nxp = f32(i) + ox; let nyp = f32(j) + oy; let nzp = f32(k) + oz;
  var S = 0.0; var M = 0.0;
  // cells that can hold such particles: those overlapping [node - 1, node + 1) in each direction
  let i0 = max(0, i32(floor(nxp - 1.0))); let i1 = min(nx - 1, i32(floor(nxp + 1.0 - 1e-6)));
  let j0 = max(0, i32(floor(nyp - 1.0))); let j1 = min(ny - 1, i32(floor(nyp + 1.0 - 1e-6)));
  let k0 = max(0, i32(floor(nzp - 1.0))); let k1 = min(nz - 1, i32(floor(nzp + 1.0 - 1e-6)));
  for (var ck = k0; ck <= k1; ck++) { for (var cj = j0; cj <= j1; cj++) { for (var ci = i0; ci <= i1; ci++) {
    let c = cellId(ci, cj, ck);
    for (var s = cellStart[c]; s < cellStart[c + 1]; s++) {
      let p = pos[s];
      let fx = (p.x - P_.x0) * inv; let fy = (p.y - P_.y0) * inv; let fz = p.z * inv;
      let tx = fx - nxp; let ty = fy - nyp; let tz = fz - nzp;      // node minus particle would be -t: offsets in cells
      if (tx <= -1.0 || tx >= 1.0 || ty <= -1.0 || ty >= 1.0 || tz <= -1.0 || tz >= 1.0) { continue; }
      let wt = (1.0 - abs(tx)) * (1.0 - abs(ty)) * (1.0 - abs(tz));
      let g = cg[3 * s + comp];                                          // the gradient row of this component
      let up = select(select(vel[s].z, vel[s].y, comp == 1), vel[s].x, comp == 0);
      // APIC: value at the node = u_p + C_p . (x_node - x_p), x_node - x_p = (-tx, -ty, -tz) dx
      S += wt * (up + (-tx * g.x - ty * g.y - tz * g.z) * dx); M += wt;
    }
  } } }
  return select(0.0, S / M, M > 1e-9);
}
@compute @workgroup_size(${WG})
fn p2gU(@builtin(global_invocation_id) id: vec3u) { let n = i32(id.x); if (n >= (P_.nx + 1) * P_.ny * P_.nz) { return; } grid[n] = gather(0, n); }
@compute @workgroup_size(${WG})
fn p2gV(@builtin(global_invocation_id) id: vec3u) { let n = i32(id.x); if (n >= P_.nx * (P_.ny + 1) * P_.nz) { return; } grid[P_.oV + n] = gather(1, n); }
@compute @workgroup_size(${WG})
fn p2gW(@builtin(global_invocation_id) id: vec3u) { let n = i32(id.x); if (n >= P_.nx * P_.ny * (P_.nz + 1)) { return; } grid[P_.oW + n] = gather(2, n); }
`;
  // 5. Body force (gravity and the fictitious force of the glass's acceleration) and explicit viscosity on open faces.
  const FORCES = COMMON + /* wgsl */`
@group(0) @binding(2) var<storage, read> faces: array<f32>;
@group(0) @binding(3) var<storage, read_write> grid: array<f32>;
@group(0) @binding(4) var<storage, read_write> tgrid: array<f32>;
@group(0) @binding(5) var<uniform> which: vec4i;    // comp, sx, sy, sz
fn open(n: i32) -> f32 { return faces[off(which.x) + n]; }
@compute @workgroup_size(${WG})
fn force(@builtin(global_invocation_id) id: vec3u) {
  let n = i32(id.x); if (n >= which.y * which.z * which.w) { return; }
  if (open(n) <= 0.0) { return; }
  let o = off(which.x);
  if (which.x == 0) { grid[o + n] += P_.dt * (-P_.ax); } else if (which.x == 2) { grid[o + n] += P_.dt * (-P_.g - P_.az); }
}
@compute @workgroup_size(${WG})
fn copyT(@builtin(global_invocation_id) id: vec3u) { let n = i32(id.x); if (n >= which.y * which.z * which.w) { return; } let o = off(which.x); tgrid[o + n] = grid[o + n]; }
@compute @workgroup_size(${WG})
fn visc(@builtin(global_invocation_id) id: vec3u) {
  let n = i32(id.x); let sx = which.y; let sy = which.z; let sz = which.w; if (n >= sx * sy * sz) { return; }
  let i = n % sx; let j = (n / sx) % sy; let k = n / (sx * sy);
  if (i < 1 || i >= sx - 1 || j < 1 || j >= sy - 1 || k < 1 || k >= sz - 1) { return; }
  if (open(n) <= 0.0) { return; }
  let c = P_.nu * P_.dt / (P_.dx * P_.dx); let m = off(which.x) + n;
  let lap = tgrid[m - 1] + tgrid[m + 1] + tgrid[m - sx] + tgrid[m + sx] + tgrid[m - sx * sy] + tgrid[m + sx * sy] - 6.0 * tgrid[m];
  grid[m] += c * lap;
}
`;
  // 6. The pressure system: A q = b on the liquid cells (q = p dt/rho), face weights the open fractions, ghost-fluid
  //    surface (theta >= thetaMin). Then a list of the liquid cells (scan) and Jacobi-preconditioned CG in one workgroup.
  const PRESSURE = COMMON + /* wgsl */`
@group(0) @binding(2) var<storage, read> faces: array<f32>;
@group(0) @binding(3) var<storage, read> grid: array<f32>;
@group(0) @binding(4) var<storage, read> phi: array<f32>;
@group(0) @binding(5) var<storage, read> fluid: array<u32>;
@group(0) @binding(6) var<storage, read_write> A: array<vec4f>;    // per cell: Ad, Ax, Ay, Az
@group(0) @binding(7) var<storage, read_write> b: array<f32>;
fn au(n: i32) -> f32 { return faces[n]; }
fn av(n: i32) -> f32 { return faces[P_.oV + n]; }
fn aw(n: i32) -> f32 { return faces[P_.oW + n]; }
fn u(n: i32) -> f32 { return grid[n]; }
fn v(n: i32) -> f32 { return grid[P_.oV + n]; }
fn w(n: i32) -> f32 { return grid[P_.oW + n]; }
fn ijk(c: i32) -> vec3i { let nxy = P_.nx * P_.ny; return vec3i(c % P_.nx, (c / P_.nx) % P_.ny, c / nxy); }
fn th(c: i32, n: i32) -> f32 { let t = phi[c] / (phi[c] - phi[n]); return clamp(t, P_.thetaMin, 1.0); }
@compute @workgroup_size(${WG})
fn assemble(@builtin(global_invocation_id) id: vec3u) {
  let c = i32(id.x); if (c >= P_.nc) { return; }
  if (fluid[c] == 0u) { A[c] = vec4f(0.0); b[c] = 0.0; return; }
  let q = ijk(c); let i = q.x; let j = q.y; let k = q.z; let nx = P_.nx; let ny = P_.ny; let nz = P_.nz; let nxy = nx * ny;
  var Ad = 0.0; var Ax = 0.0; var Ay = 0.0; var Az = 0.0; var div = 0.0; var wt = 0.0;
  wt = au(U(i + 1, j, k)); if (wt > 0.0) { div += wt * u(U(i + 1, j, k)); if (i + 1 < nx) { if (fluid[c + 1] != 0u) { Ad += wt; Ax = -wt; } else { Ad += wt / th(c, c + 1); } } }
  wt = au(U(i, j, k)); if (wt > 0.0) { div -= wt * u(U(i, j, k)); if (i > 0) { if (fluid[c - 1] != 0u) { Ad += wt; } else { Ad += wt / th(c, c - 1); } } }
  wt = av(V(i, j + 1, k)); if (wt > 0.0) { div += wt * v(V(i, j + 1, k)); if (j + 1 < ny) { if (fluid[c + nx] != 0u) { Ad += wt; Ay = -wt; } else { Ad += wt / th(c, c + nx); } } }
  wt = av(V(i, j, k)); if (wt > 0.0) { div -= wt * v(V(i, j, k)); if (j > 0) { if (fluid[c - nx] != 0u) { Ad += wt; } else { Ad += wt / th(c, c - nx); } } }
  wt = aw(Wf(i, j, k + 1)); if (wt > 0.0) { div += wt * w(Wf(i, j, k + 1)); if (k + 1 < nz) { if (fluid[c + nxy] != 0u) { Ad += wt; Az = -wt; } else { Ad += wt / th(c, c + nxy); } } }
  wt = aw(Wf(i, j, k)); if (wt > 0.0) { div -= wt * w(Wf(i, j, k)); if (k > 0) { if (fluid[c - nxy] != 0u) { Ad += wt; } else { Ad += wt / th(c, c - nxy); } } }
  A[c] = vec4f(Ad, Ax, Ay, Az); b[c] = -P_.dx * div;
}
`;
  const CG = COMMON + /* wgsl */`
@group(0) @binding(2) var<storage, read> fluid: array<u32>;
@group(0) @binding(3) var<storage, read> A: array<vec4f>;
@group(0) @binding(4) var<storage, read> b: array<f32>;
@group(0) @binding(5) var<storage, read_write> q: array<f32>;      // the solution, warm-started from the last step
@group(0) @binding(6) var<storage, read_write> L: array<i32>;      // the liquid cells, then (nc + 0) nf
@group(0) @binding(7) var<storage, read_write> work: array<f32>;   // r, z, s: three vectors of nc
@group(0) @binding(8) var<storage, read_write> stat: array<f32>;  // [iterations, residual, |b|max, nf]
var<workgroup> sh: array<f32, ${WG}>;
var<workgroup> shi: array<i32, ${WG}>;
var<workgroup> flag: i32;
fn reduce(t: i32, vv: f32) -> f32 {      // sum over the workgroup, fixed tree order
  sh[t] = vv; workgroupBarrier();
  for (var h = ${WG / 2}; h > 0; h = h / 2) { if (t < h) { sh[t] = sh[t] + sh[t + h]; } workgroupBarrier(); }
  let out = workgroupUniformLoad(&sh[0]); workgroupBarrier(); return out;
}
fn reduceMax(t: i32, vv: f32) -> f32 {
  sh[t] = vv; workgroupBarrier();
  for (var h = ${WG / 2}; h > 0; h = h / 2) { if (t < h) { sh[t] = max(sh[t], sh[t + h]); } workgroupBarrier(); }
  let out = workgroupUniformLoad(&sh[0]); workgroupBarrier(); return out;
}
// A x at cell c, x the vector at offset xo of q (xo < 0) or of work
fn xv(xo: i32, c: i32) -> f32 { if (xo < 0) { return q[c]; } return work[xo + c]; }
fn applyA(c: i32, xo: i32) -> f32 {
  let nx = P_.nx; let ny = P_.ny; let nz = P_.nz; let nxy = nx * ny;
  let i = c % nx; let j = (c / nx) % ny; let k = c / nxy; let a = A[c];
  var val = a.x * xv(xo, c);
  if (i + 1 < nx) { val += a.y * xv(xo, c + 1); }
  if (i > 0) { val += A[c - 1].y * xv(xo, c - 1); }
  if (j + 1 < ny) { val += a.z * xv(xo, c + nx); }
  if (j > 0) { val += A[c - nx].z * xv(xo, c - nx); }
  if (k + 1 < nz) { val += a.w * xv(xo, c + nxy); }
  if (k > 0) { val += A[c - nxy].w * xv(xo, c - nxy); }
  return val;
}
// the whole solve in one workgroup: list the liquid cells, then PCG with the Jacobi preconditioner 1/Ad
@compute @workgroup_size(${WG})
fn pcg(@builtin(local_invocation_id) lid: vec3u) {
  let t = i32(lid.x); let nc = P_.nc; let per = (nc + ${WG} - 1) / ${WG};
  // list of liquid cells (a scan of the flags, as in the sort)
  let a0 = t * per; let a1 = min(nc, a0 + per);
  var cnt = 0; for (var c = a0; c < a1; c++) { if (fluid[c] != 0u) { cnt++; } }
  shi[t] = cnt; workgroupBarrier();
  if (t == 0) { var acc = 0; for (var u2 = 0; u2 < ${WG}; u2++) { let vv = shi[u2]; shi[u2] = acc; acc += vv; } flag = acc; }
  let nf = workgroupUniformLoad(&flag);
  var pos = shi[t]; let R0 = 0; let Z0 = P_.nc; let S0 = 2 * P_.nc;
  for (var c = a0; c < a1; c++) { if (fluid[c] != 0u) { L[pos] = c; pos++; } else { q[c] = 0.0; work[R0 + c] = 0.0; work[Z0 + c] = 0.0; work[S0 + c] = 0.0; } }
  workgroupBarrier();
  // |b|max
  var bm = 0.0; for (var n = t; n < nf; n += ${WG}) { bm = max(bm, abs(b[L[n]])); }
  bm = reduceMax(t, bm);
  if (t == 0) { stat[2] = bm; stat[3] = f32(nf); }
  if (bm < 1e-14) { for (var n = t; n < nf; n += ${WG}) { q[L[n]] = 0.0; } if (t == 0) { stat[0] = 0.0; stat[1] = 0.0; } return; }
  // r = b - A q; z = M^-1 r; s = z; sigma = z.r
  var rm = 0.0;
  for (var n = t; n < nf; n += ${WG}) { let c = L[n]; let rr = b[c] - applyA(c, -1); work[R0 + c] = rr; rm = max(rm, abs(rr)); }
  workgroupBarrier();
  rm = reduceMax(t, rm);
  let tol = P_.tol * bm;
  if (rm < tol) { if (t == 0) { stat[0] = 0.0; stat[1] = rm; } return; }
  var sg = 0.0;
  for (var n = t; n < nf; n += ${WG}) { let c = L[n]; let zz = select(0.0, work[R0 + c] / A[c].x, A[c].x > 0.0); work[Z0 + c] = zz; work[S0 + c] = zz; sg += zz * work[R0 + c]; }
  workgroupBarrier();
  var sigma = reduce(t, sg);
  var it = 0; let maxIt = i32(P_.maxIt);
  for (; it < maxIt; it++) {
    var sz = 0.0;
    for (var n = t; n < nf; n += ${WG}) { let c = L[n]; let zz = applyA(c, S0); work[Z0 + c] = zz; sz += work[S0 + c] * zz; }
    workgroupBarrier();
    sz = reduce(t, sz);
    let alpha = sigma / sz;
    rm = 0.0;
    for (var n = t; n < nf; n += ${WG}) { let c = L[n]; q[c] += alpha * work[S0 + c]; work[R0 + c] -= alpha * work[Z0 + c]; rm = max(rm, abs(work[R0 + c])); }
    workgroupBarrier();
    rm = reduceMax(t, rm);
    if (rm < tol) { break; }
    var sn = 0.0;
    for (var n = t; n < nf; n += ${WG}) { let c = L[n]; let zz = select(0.0, work[R0 + c] / A[c].x, A[c].x > 0.0); work[Z0 + c] = zz; sn += zz * work[R0 + c]; }
    workgroupBarrier();
    sn = reduce(t, sn);
    let beta = sn / sigma; sigma = sn;
    for (var n = t; n < nf; n += ${WG}) { let c = L[n]; work[S0 + c] = work[Z0 + c] + beta * work[S0 + c]; }
    workgroupBarrier();
  }
  if (t == 0) { stat[0] = f32(it + 1); stat[1] = rm; }
}
`;
  // 7. Velocity update from the pressure (ghost fluid at the surface), the valid flags, and extrapolation into the air.
  const PROJECT = COMMON + /* wgsl */`
@group(0) @binding(2) var<storage, read> faces: array<f32>;
@group(0) @binding(3) var<storage, read> phi: array<f32>;
@group(0) @binding(4) var<storage, read> fluid: array<u32>;
@group(0) @binding(5) var<storage, read> q: array<f32>;
@group(0) @binding(6) var<storage, read_write> grid: array<f32>;
@group(0) @binding(7) var<storage, read_write> valid: array<u32>;
@group(0) @binding(8) var<storage, read_write> tgrid: array<f32>;
@group(0) @binding(9) var<storage, read_write> validT: array<u32>;
@group(0) @binding(10) var<uniform> which: vec4i;    // comp, sx, sy, sz
fn th(c: i32, n: i32) -> f32 { let tt = phi[c] / (phi[c] - phi[n]); return clamp(tt, P_.thetaMin, 1.0); }
fn ghost(c: i32, n: i32) -> f32 { return q[c] * (1.0 - 1.0 / th(c, n)); }
@compute @workgroup_size(${WG})
fn gradient(@builtin(global_invocation_id) id: vec3u) {
  let n = i32(id.x); let comp = which.x; let sx = which.y; let sy = which.z; let sz = which.w; if (n >= sx * sy * sz) { return; }
  let o = off(comp);
  let i = n % sx; let j = (n / sx) % sy; let k = n / (sx * sy); let nx = P_.nx; let ny = P_.ny; let nz = P_.nz;
  valid[o + n] = 0u;
  // the planes where the velocity is known exactly: the floor and the lid (w = 0)
  if (comp == 2 && (k == 0 || k == nz)) { grid[o + n] = 0.0; valid[o + n] = 1u; return; }
  if ((comp == 0 && (i == 0 || i == nx)) || (comp == 1 && (j == 0 || j == ny))) { return; }
  if (faces[o + n] <= 0.0) { return; }
  var cl = 0; var cr = 0;
  if (comp == 0) { cl = (i - 1) + nx * (j + ny * k); cr = cl + 1; } else if (comp == 1) { cl = i + nx * ((j - 1) + ny * k); cr = cl + nx; } else { cl = i + nx * (j + ny * (k - 1)); cr = cl + nx * ny; }
  let fl = fluid[cl] != 0u; let fr = fluid[cr] != 0u;
  if (!fl && !fr) { return; }
  let ql = select(ghost(cr, cl), q[cl], fl); let qr = select(ghost(cl, cr), q[cr], fr);
  grid[o + n] -= (qr - ql) / P_.dx; valid[o + n] = 1u;
}
@compute @workgroup_size(${WG})
fn copyV(@builtin(global_invocation_id) id: vec3u) { let o = off(which.x); let n = i32(id.x); if (n >= which.y * which.z * which.w) { return; } tgrid[o + n] = grid[o + n]; validT[o + n] = valid[o + n]; }
// one layer of extrapolation: an invalid face takes the mean of its valid neighbours (from the copy)
@compute @workgroup_size(${WG})
fn extend(@builtin(global_invocation_id) id: vec3u) { let o = off(which.x);
  let n = i32(id.x); let sx = which.y; let sy = which.z; let sz = which.w; if (n >= sx * sy * sz) { return; }
  if (validT[o + n] != 0u) { return; }
  let i = n % sx; let j = (n / sx) % sy; let k = n / (sx * sy);
  var s = 0.0; var m = 0.0;
  if (i > 0 && validT[o + n - 1] != 0u) { s += tgrid[o + n - 1]; m += 1.0; }
  if (i < sx - 1 && validT[o + n + 1] != 0u) { s += tgrid[o + n + 1]; m += 1.0; }
  if (j > 0 && validT[o + n - sx] != 0u) { s += tgrid[o + n - sx]; m += 1.0; }
  if (j < sy - 1 && validT[o + n + sx] != 0u) { s += tgrid[o + n + sx]; m += 1.0; }
  if (k > 0 && validT[o + n - sx * sy] != 0u) { s += tgrid[o + n - sx * sy]; m += 1.0; }
  if (k < sz - 1 && validT[o + n + sx * sy] != 0u) { s += tgrid[o + n + sx * sy]; m += 1.0; }
  if (m > 0.0) { grid[o + n] = s / m; valid[o + n] = 1u; }
}
@compute @workgroup_size(${WG})
fn zeroInvalid(@builtin(global_invocation_id) id: vec3u) { let o = off(which.x); let n = i32(id.x); if (n >= which.y * which.z * which.w) { return; } if (valid[o + n] == 0u) { grid[o + n] = 0.0; } }
`;
  // 8. Grid-to-particle (APIC: velocity and its gradient from the trilinear weights), RK2 advection through the grid, the
  //    wall, the floor, the box top, and the spill over the rim.
  const G2P = COMMON + /* wgsl */`
@group(0) @binding(2) var<storage, read> cellStart: array<i32>;
@group(0) @binding(3) var<storage, read> grid: array<f32>;
@group(0) @binding(4) var<storage, read_write> pos: array<vec4f>;
@group(0) @binding(5) var<storage, read_write> vel: array<vec4f>;
@group(0) @binding(6) var<storage, read_write> cg: array<vec4f>;
@group(0) @binding(7) var<storage, read_write> spill: array<vec4f>;      // pos, vel of each particle that spilled this step
@group(0) @binding(8) var<storage, read_write> spillN: atomic<i32>;
fn gv(comp: i32, n: i32) -> f32 { return grid[off(comp) + n]; }
fn sample(comp: i32, x: f32, y: f32, z: f32) -> f32 {
  let nx = P_.nx; let ny = P_.ny; let nz = P_.nz; let dx = P_.dx;
  var sx = nx; var sy = ny; var sz = nz; var fx = (x - P_.x0) / dx; var fy = (y - P_.y0) / dx; var fz = z / dx;
  if (comp == 0) { sx = nx + 1; fy -= 0.5; fz -= 0.5; } else if (comp == 1) { sy = ny + 1; fx -= 0.5; fz -= 0.5; } else { sz = nz + 1; fx -= 0.5; fy -= 0.5; }
  let i = i32(floor(fx)); let j = i32(floor(fy)); let k = i32(floor(fz)); let tx = fx - f32(i); let ty = fy - f32(j); let tz = fz - f32(k);
  let i0 = clamp(i, 0, sx - 1); let i1 = clamp(i + 1, 0, sx - 1); let j0 = clamp(j, 0, sy - 1); let j1 = clamp(j + 1, 0, sy - 1); let k0 = clamp(k, 0, sz - 1); let k1 = clamp(k + 1, 0, sz - 1);
  let sxy = sx * sy; let b00 = j0 * sx + k0 * sxy; let b10 = j1 * sx + k0 * sxy; let b01 = j0 * sx + k1 * sxy; let b11 = j1 * sx + k1 * sxy;
  var c00 = 0.0; var c10 = 0.0; var c01 = 0.0; var c11 = 0.0;
  if (comp == 0) { c00 = gv(comp, i0 + b00) + tx * (gv(comp, i1 + b00) - gv(comp, i0 + b00)); c10 = gv(comp, i0 + b10) + tx * (gv(comp, i1 + b10) - gv(comp, i0 + b10)); c01 = gv(comp, i0 + b01) + tx * (gv(comp, i1 + b01) - gv(comp, i0 + b01)); c11 = gv(comp, i0 + b11) + tx * (gv(comp, i1 + b11) - gv(comp, i0 + b11)); }
  else if (comp == 1) { c00 = gv(comp, i0 + b00) + tx * (gv(comp, i1 + b00) - gv(comp, i0 + b00)); c10 = gv(comp, i0 + b10) + tx * (gv(comp, i1 + b10) - gv(comp, i0 + b10)); c01 = gv(comp, i0 + b01) + tx * (gv(comp, i1 + b01) - gv(comp, i0 + b01)); c11 = gv(comp, i0 + b11) + tx * (gv(comp, i1 + b11) - gv(comp, i0 + b11)); }
  else { c00 = gv(comp, i0 + b00) + tx * (gv(comp, i1 + b00) - gv(comp, i0 + b00)); c10 = gv(comp, i0 + b10) + tx * (gv(comp, i1 + b10) - gv(comp, i0 + b10)); c01 = gv(comp, i0 + b01) + tx * (gv(comp, i1 + b01) - gv(comp, i0 + b01)); c11 = gv(comp, i0 + b11) + tx * (gv(comp, i1 + b11) - gv(comp, i0 + b11)); }
  let d0 = c00 + ty * (c10 - c00); let d1 = c01 + ty * (c11 - c01);
  return d0 + tz * (d1 - d0);
}
// velocity and gradient of component comp at the particle (Fluid.transfer, toGrid = false)
fn g2pComp(comp: i32, x: f32, y: f32, z: f32) -> vec4f {
  let nx = P_.nx; let ny = P_.ny; let nz = P_.nz; let dx = P_.dx; let inv = 1.0 / dx;
  var sx = nx; var sy = ny; var sz = nz; var fx = (x - P_.x0) * inv; var fy = (y - P_.y0) * inv; var fz = z * inv;
  if (comp == 0) { sx = nx + 1; fy -= 0.5; fz -= 0.5; } else if (comp == 1) { sy = ny + 1; fx -= 0.5; fz -= 0.5; } else { sz = nz + 1; fx -= 0.5; fy -= 0.5; }
  let i = i32(floor(fx)); let j = i32(floor(fy)); let k = i32(floor(fz)); let tx = fx - f32(i); let ty = fy - f32(j); let tz = fz - f32(k);
  let I0 = clamp(i, 0, sx - 1); let I1 = clamp(i + 1, 0, sx - 1); let J0 = clamp(j, 0, sy - 1); let J1 = clamp(j + 1, 0, sy - 1); let K0 = clamp(k, 0, sz - 1); let K1 = clamp(k + 1, 0, sz - 1);
  let sxy = sx * sy;
  let n000 = I0 + J0 * sx + K0 * sxy; let n100 = I1 + J0 * sx + K0 * sxy; let n010 = I0 + J1 * sx + K0 * sxy; let n110 = I1 + J1 * sx + K0 * sxy;
  let n001 = I0 + J0 * sx + K1 * sxy; let n101 = I1 + J0 * sx + K1 * sxy; let n011 = I0 + J1 * sx + K1 * sxy; let n111 = I1 + J1 * sx + K1 * sxy;
  var q000 = 0.0; var q100 = 0.0; var q010 = 0.0; var q110 = 0.0; var q001 = 0.0; var q101 = 0.0; var q011 = 0.0; var q111 = 0.0;
  if (comp == 0) { q000 = gv(comp, n000); q100 = gv(comp, n100); q010 = gv(comp, n010); q110 = gv(comp, n110); q001 = gv(comp, n001); q101 = gv(comp, n101); q011 = gv(comp, n011); q111 = gv(comp, n111); }
  else if (comp == 1) { q000 = gv(comp, n000); q100 = gv(comp, n100); q010 = gv(comp, n010); q110 = gv(comp, n110); q001 = gv(comp, n001); q101 = gv(comp, n101); q011 = gv(comp, n011); q111 = gv(comp, n111); }
  else { q000 = gv(comp, n000); q100 = gv(comp, n100); q010 = gv(comp, n010); q110 = gv(comp, n110); q001 = gv(comp, n001); q101 = gv(comp, n101); q011 = gv(comp, n011); q111 = gv(comp, n111); }
  let ux = 1.0 - tx; let uy = 1.0 - ty; let uz = 1.0 - tz;
  let val = ux * uy * uz * q000 + tx * uy * uz * q100 + ux * ty * uz * q010 + tx * ty * uz * q110 + ux * uy * tz * q001 + tx * uy * tz * q101 + ux * ty * tz * q011 + tx * ty * tz * q111;
  let gx = inv * (uy * uz * (q100 - q000) + ty * uz * (q110 - q010) + uy * tz * (q101 - q001) + ty * tz * (q111 - q011));
  let gy = inv * (ux * uz * (q010 - q000) + tx * uz * (q110 - q100) + ux * tz * (q011 - q001) + tx * tz * (q111 - q101));
  let gz = inv * (ux * uy * (q001 - q000) + tx * uy * (q101 - q100) + ux * ty * (q011 - q010) + tx * ty * (q111 - q110));
  return vec4f(val, gx, gy, gz);
}
@compute @workgroup_size(${WG})
fn g2p(@builtin(global_invocation_id) id: vec3u) {
  let s = i32(id.x); if (s >= cellStart[P_.nc]) { return; }
  let p = pos[s];
  let a = g2pComp(0, p.x, p.y, p.z); let bq = g2pComp(1, p.x, p.y, p.z); let c = g2pComp(2, p.x, p.y, p.z);
  vel[s] = vec4f(a.x, bq.x, c.x, 0.0);
  cg[3 * s] = vec4f(a.yzw, 0.0); cg[3 * s + 1] = vec4f(bq.yzw, 0.0); cg[3 * s + 2] = vec4f(c.yzw, 0.0);
}
// RK2 (midpoint) through the grid velocity, then the wall: back onto r = R(z) along the wall's normal, losing the speed
// along the outward normal; the floor and the box top; above the rim and outside its radius the particle has spilled
@compute @workgroup_size(${WG})
fn advect(@builtin(global_invocation_id) id: vec3u) {
  let s = i32(id.x); if (s >= cellStart[P_.nc]) { return; }
  let p = pos[s]; let dt = P_.dt; let h = 0.5 * dt;
  var x = p.x; var y = p.y; var z = p.z;
  let u1 = sample(0, x, y, z); let v1 = sample(1, x, y, z); let w1 = sample(2, x, y, z);
  let xm = x + h * u1; let ym = y + h * v1; let zm = z + h * w1;
  x += dt * sample(0, xm, ym, zm); y += dt * sample(1, xm, ym, zm); z += dt * sample(2, xm, ym, zm);
  var vv = vel[s];
  let e = 0.02 * P_.dx;
  let r2 = x * x + y * y;
  if (z > P_.zRim && r2 > P_.Rrim * P_.Rrim) {
    let n = atomicAdd(&spillN, 1);
    if (n < 4096) { spill[2 * n] = vec4f(x, y, z, 1.0); spill[2 * n + 1] = vv; }
    pos[s] = vec4f(x, y, z, -1.0); return;
  }
  let Rin = min(Rz(z), P_.Rbox) - e;
  if (r2 > Rin * Rin) {
    let r = sqrt(r2); let cx = x / r; let cy = y / r; let sl = dRz(z); let l2 = 1.0 + sl * sl; let l = sqrt(l2);
    let nx = cx / l; let ny = cy / l; let nz = -sl / l; let pen = r - Rin;
    let rn = r - pen / l2; z += sl * pen / l2;
    x = cx * rn; y = cy * rn;
    let un = vv.x * nx + vv.y * ny + vv.z * nz;
    if (un > 0.0) { vv = vec4f(vv.x - un * nx, vv.y - un * ny, vv.z - un * nz, 0.0); }
  }
  if (z < e) { z = e; if (vv.z < 0.0) { vv.z = 0.0; } }
  if (z > P_.H - e) { z = P_.H - e; if (vv.z > 0.0) { vv.z = 0.0; } }
  pos[s] = vec4f(x, y, z, 1.0); vel[s] = vv;
}
`;
  // 9. Reductions the host needs each step: momentum (sum of u, w over the live particles), the fastest particle, and the
  //    particle volume standing on each grid column (integer counts: exact). Per-workgroup partial sums in fixed order.
  const REDUCE = COMMON + /* wgsl */`
@group(0) @binding(2) var<storage, read> cellStart: array<i32>;
@group(0) @binding(3) var<storage, read> pos: array<vec4f>;
@group(0) @binding(4) var<storage, read> vel: array<vec4f>;
@group(0) @binding(5) var<storage, read_write> part: array<vec4f>;      // per workgroup: sum u, sum v, sum w, max |v|^2
@group(0) @binding(6) var<storage, read_write> col: array<atomic<i32>>;  // particles per column
var<workgroup> sh: array<vec4f, ${WG}>;
@compute @workgroup_size(${WG})
fn momentum(@builtin(global_invocation_id) id: vec3u, @builtin(local_invocation_id) lid: vec3u, @builtin(workgroup_id) wid: vec3u) {
  let s = i32(id.x); let t = i32(lid.x);
  var vv = vec4f(0.0);
  if (s < cellStart[P_.nc] && pos[s].w >= 0.0) { let q = vel[s]; vv = vec4f(q.x, q.y, q.z, q.x * q.x + q.y * q.y + q.z * q.z);
    var i = i32(floor((pos[s].x - P_.x0) / P_.dx)); var j = i32(floor((pos[s].y - P_.y0) / P_.dx));
    i = clamp(i, 0, P_.nx - 1); j = clamp(j, 0, P_.ny - 1); atomicAdd(&col[i + P_.nx * j], 1); }
  sh[t] = vv; workgroupBarrier();
  for (var h = ${WG / 2}; h > 0; h = h / 2) { if (t < h) { let a = sh[t]; let b = sh[t + h]; sh[t] = vec4f(a.xyz + b.xyz, max(a.w, b.w)); } workgroupBarrier(); }
  if (t == 0) { part[wid.x] = sh[0]; }
}
`;

  // ------------------------------------------------------------------ host side
  function GpuFluid(o) {
    o = o || {};
    this.profile = o.profile; const P = this.profile.R;
    this.zRim = (P.length - 1) * this.profile.dz; this.R = Math.max.apply(null, P); this.Rrim = P[P.length - 1];
    this.h0 = o.h0 || 0.125; this.dx = o.dx || 0.004; this.rho = o.rho || 1000; this.nu = o.nu != null ? o.nu : 1e-6; this.g = o.g || 9.81;
    const dx = this.dx;
    this.nx = 2 * Math.ceil(this.R / dx); this.ny = this.nx; this.nz = Math.ceil((o.H || 0.092) / dx);
    this.H = this.nz * dx; this.x0 = -(this.nx / 2) * dx; this.y0 = -(this.ny / 2) * dx; this.Rbox = (this.nx / 2) * dx;
    this.nc = this.nx * this.ny * this.nz;
    this.nu_ = (this.nx + 1) * this.ny * this.nz; this.nv_ = this.nx * (this.ny + 1) * this.nz; this.nw_ = this.nx * this.ny * (this.nz + 1);
    this.ppcSide = o.ppcSide || 2; this.rpFactor = o.rpFactor || 1.8; this.kernel = 2; this.sliver = 0.1; this.thetaMin = 0.05; this.forcedPhi = 0.05;
    this.tol = o.tol || 1e-5; this.maxIt = o.maxIt || 300;
    this.modal = false; this.gpu = true; this.whole = true;
    this.t = 0; this.cgIters = 0; this.cgResidual = 0; this.spilled = 0; this.spillNow = 0; this.spillPx = 0; this.spillPz = 0; this.spillList = [];
    this.faceFractions();
    this.seed(this.ppcSide, o.seed || 12345);
    this.colH = new Float64Array(this.nx * this.ny); this.colCnt = new Int32Array(this.nx * this.ny);
    this.P = [0, 0]; this.vmax = 0;
    this.ready = false;
  }
  GpuFluid.prototype.Rz = function (z) { if (z > this.zRim) return 10; const P = this.profile.R, f = (z < 0 ? 0 : z) / this.profile.dz, i = Math.floor(f); if (i >= P.length - 1) return P[P.length - 1]; return P[i] + (f - i) * (P[i + 1] - P[i]); };
  GpuFluid.prototype.dRz = function (z) { if (z >= this.zRim) return 0; const P = this.profile.R, f = (z < 0 ? 0 : z) / this.profile.dz, i = Math.min(P.length - 2, Math.floor(f)); return (P[i + 1] - P[i]) / this.profile.dz; };
  GpuFluid.prototype.volumeTo = function (h) { const n = Math.max(1, Math.round(h / 5e-5)), d = h / n; let v = 0; for (let k = 0; k <= n; k++) { const r = this.Rz(k * d); v += (k === 0 || k === n ? 0.5 : 1) * Math.PI * r * r * d; } return v; };
  // open face fractions, as Fluid.faceFractions, over the whole glass (y from y0)
  GpuFluid.prototype.faceFractions = function () {
    const dx = this.dx, nx = this.nx, ny = this.ny, nz = this.nz, x0 = this.x0, y0 = this.y0, sl = this.sliver;
    const au = this.au = new Float32Array(this.nu_), av = this.av = new Float32Array(this.nv_), aw = this.aw = new Float32Array(this.nw_);
    const clamp = (a) => { a = Math.max(0, Math.min(1, a)); return a < sl ? 0 : a; };
    for (let k = 0; k < nz; k++) {
      const R = Math.min(this.Rz((k + 0.5) * dx), this.Rbox * 2);
      for (let j = 0; j < ny; j++) for (let i = 0; i <= nx; i++) {
        const xf = x0 + i * dx, Y = R * R - xf * xf > 0 ? Math.sqrt(R * R - xf * xf) : 0, a = y0 + j * dx, b = a + dx;
        au[i + (nx + 1) * (j + ny * k)] = (i === 0 || i === nx) ? 0 : clamp(Math.max(0, Math.min(b, Y) - Math.max(a, -Y)) / dx);
      }
      for (let j = 0; j <= ny; j++) for (let i = 0; i < nx; i++) {
        const yf = y0 + j * dx, X = R * R - yf * yf > 0 ? Math.sqrt(R * R - yf * yf) : 0, a = x0 + i * dx, b = a + dx;
        av[i + nx * (j + (ny + 1) * k)] = (j === 0 || j === ny) ? 0 : clamp(Math.max(0, Math.min(b, X) - Math.max(a, -X)) / dx);
      }
    }
    const S = 10;
    for (let k = 0; k <= nz; k++) {
      const R = Math.min(this.Rz(k * dx), this.Rbox * 2);
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
        let inside = 0;
        for (let a = 0; a < S; a++) for (let b = 0; b < S; b++) { const x = x0 + (i + (a + 0.5) / S) * dx, y = y0 + (j + (b + 0.5) / S) * dx; if (x * x + y * y < R * R) inside++; }
        let f = inside / (S * S); if (f < sl) f = 0;
        aw[i + nx * (j + ny * k)] = (k === 0 || k === nz) ? 0 : f;
      }
    }
  };
  // the same seeding as Fluid.seed, over the whole glass: each half gets the CPU's particles and their mirror images in
  // the same jitter, so the liquid starts as the CPU's does
  GpuFluid.prototype.seed = function (s, seed) {
    let st = seed >>> 0; const rnd = () => { st = (st * 1664525 + 1013904223) >>> 0; return st / 4294967296; };
    const dx = this.dx, xs = [], ys = [], zs = [], nyh = this.ny / 2;
    for (let k = 0; k < this.nz; k++) for (let j = 0; j < nyh; j++) for (let i = 0; i < this.nx; i++)
      for (let a = 0; a < s; a++) for (let b = 0; b < s; b++) for (let c = 0; c < s; c++) {
        const x = this.x0 + (i + (a + 0.5 + 0.6 * (rnd() - 0.5)) / s) * dx, y = (j + (b + 0.5 + 0.6 * (rnd() - 0.5)) / s) * dx, z = (k + (c + 0.5 + 0.6 * (rnd() - 0.5)) / s) * dx;
        if (x * x + y * y < (this.Rz(z) - 0.15 * dx) ** 2 && z < this.h0 && y > 0) { xs.push(x, x); ys.push(y, -y); zs.push(z, z); }
      }
    const n = this.np = xs.length; this.npStart = n;
    this.px = new Float64Array(n); this.py = new Float64Array(n); this.pz = new Float64Array(n); this.px.set(xs); this.py.set(ys); this.pz.set(zs);
    this.pu = new Float64Array(n); this.pv = new Float64Array(n); this.pw = new Float64Array(n);
    this.mLiquid = this.rho * this.volumeTo(this.h0); this.mp = this.mLiquid / n;
    this.rp = dx / s * this.rpFactor; this.Vseed = (dx / s) ** 3;
  };
  GpuFluid.prototype.liquidMass = function () { return this.mp * this.np; };
  GpuFluid.prototype.momentum = function () { return this.P.slice(); };
  GpuFluid.prototype.maxSpeed = function () { return this.vmax; };
  GpuFluid.prototype.levelSet = function () {};

  // ---- device, buffers, pipelines
  GpuFluid.prototype.init = async function (device) {
    const d = this.device = device;
    const ST = GPUBufferUsage.STORAGE | GPUBufferUsage.COPY_DST | GPUBufferUsage.COPY_SRC, UN = GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST;
    const mk = (n, usage, label) => d.createBuffer({ label, size: Math.max(16, Math.ceil(n / 4) * 4), usage: usage || ST });
    const cap = this.npCap = this.np, nc = this.nc, nf3 = this.nu_ + this.nv_ + this.nw_;
    this.oV = this.nu_; this.oW = this.nu_ + this.nv_;
    if (this.profile.R.length > 512) throw new Error('stout-gpu: the glass profile has more than 512 points');
    this.B = {
      params: mk(256 * GpuFluid.MAXB, UN, 'params'), nslot: mk(16, null, 'nslot'), prof: mk(16 * 128, UN, 'profile'),
      posA: mk(16 * cap, null, 'posA'), velA: mk(16 * cap, null, 'velA'), cA: mk(48 * cap, null, 'cA'),
      posB: mk(16 * cap, null, 'posB'), velB: mk(16 * cap, null, 'velB'), cB: mk(48 * cap, null, 'cB'),
      cnt: mk(4 * (nc + 1), null, 'cnt'), pcell: mk(4 * cap, null, 'pcell'), fillp: mk(4 * (nc + 1), null, 'fillp'), order: mk(4 * cap, null, 'order'), cellStart: mk(4 * (nc + 1), null, 'cellStart'),
      maskA: mk(4 * nc, null, 'maskA'), maskB: mk(4 * nc, null, 'maskB'), phi: mk(4 * nc, null, 'phi'), fluid: mk(4 * nc, null, 'fluid'), imgF: mk(4 * cap, null, 'imgF'),
      flagCopy: mk(4 * nc, null, 'flagCopy'), phiCopy: mk(4 * nc, null, 'phiCopy'),
      faces: mk(4 * nf3, null, 'faces'), grid: mk(4 * nf3, null, 'grid'), tgrid: mk(4 * nf3, null, 'tgrid'), valid: mk(4 * nf3, null, 'valid'), validT: mk(4 * nf3, null, 'validT'),
      A: mk(16 * nc, null, 'A'), b: mk(4 * nc, null, 'b'), q: mk(4 * nc, null, 'q'), L: mk(4 * (nc + 1), null, 'L'), work: mk(12 * nc, null, 'work'),
      stat: mk(16, null, 'stat'), spill: mk(32 * GpuFluid.SPILLCAP, null, 'spill'), spillN: mk(16, null, 'spillN'),
      part: mk(16 * Math.ceil(cap / WG), null, 'part'), col: mk(4 * this.nx * this.ny, null, 'col'),
      whichU: mk(16, UN, 'whichU'), whichV: mk(16, UN, 'whichV'), whichW: mk(16, UN, 'whichW'),
      read: d.createBuffer({ label: 'readback', size: this.readLayout(cap).total, usage: GPUBufferUsage.MAP_READ | GPUBufferUsage.COPY_DST }),
      readPos: d.createBuffer({ label: 'readback positions', size: 16 * cap, usage: GPUBufferUsage.MAP_READ | GPUBufferUsage.COPY_DST })
    };
    const pr = new Float32Array(512); pr.set(this.profile.R); d.queue.writeBuffer(this.B.prof, 0, pr);
    const fa = new Float32Array(nf3); fa.set(this.au, 0); fa.set(this.av, this.oV); fa.set(this.aw, this.oW); d.queue.writeBuffer(this.B.faces, 0, fa);
    d.queue.writeBuffer(this.B.whichU, 0, new Int32Array([0, this.nx + 1, this.ny, this.nz]));
    d.queue.writeBuffer(this.B.whichV, 0, new Int32Array([1, this.nx, this.ny + 1, this.nz]));
    d.queue.writeBuffer(this.B.whichW, 0, new Int32Array([2, this.nx, this.ny, this.nz + 1]));
    this.uploadParticles();
    // Explicit layouts, one per shader module (u uniform, r read-only storage, s storage): every entry point of a module
    // shares its bind groups, used bindings or not. At most 8 storage buffers per stage, the limit every device gives.
    const KINDS = {
      sort: 'uursssssr', perm: 'uurrrrrsss', ls: 'uurrsssss', inh: 'uurssss', p2g: 'uurrrrs', forces: 'uurssu', pr: 'uurrrrss', cg: 'uurrrssss', proj: 'uurrrrssssu', g2p: 'uurrsssss', red: 'uurrrss'
    };
    const SRC = { sort: SORT, perm: PERMUTE, ls: LEVELSET, inh: INHERIT, p2g: P2G, forces: FORCES, pr: PRESSURE, cg: CG, proj: PROJECT, g2p: G2P, red: REDUCE };
    const L = this.layouts = {}, M = {};
    for (const k in KINDS) {
      L[k] = d.createBindGroupLayout({ label: k, entries: KINDS[k].split('').map((t, i) => ({ binding: i, visibility: GPUShaderStage.COMPUTE, buffer: { type: t === 'u' ? 'uniform' : t === 'r' ? 'read-only-storage' : 'storage', hasDynamicOffset: i === 0 } })) });
      M[k] = d.createShaderModule({ label: k, code: SRC[k] });
    }
    const K = this.K = {}, PL = {};
    for (const k in KINDS) PL[k] = d.createPipelineLayout({ bindGroupLayouts: [L[k]] });
    for (const [k, m, e] of [['count', 'sort', 'count'], ['scan', 'sort', 'scan'], ['scatter', 'sort', 'scatter'], ['sortCell', 'sort', 'sortCell'], ['permute', 'perm', 'permute'],
      ['masks', 'ls', 'masks'], ['dilate0', 'ls', 'dilate0'], ['dilateX', 'ls', 'dilateX'], ['dilateY', 'ls', 'dilateY'], ['dilateZ', 'ls', 'dilateZ'], ['phiCells', 'ls', 'phiCells'], ['flags', 'ls', 'flags'],
      ['copyF', 'inh', 'copy'], ['inherit', 'inh', 'inherit'], ['p2gU', 'p2g', 'p2gU'], ['p2gV', 'p2g', 'p2gV'], ['p2gW', 'p2g', 'p2gW'],
      ['force', 'forces', 'force'], ['copyT', 'forces', 'copyT'], ['visc', 'forces', 'visc'], ['assemble', 'pr', 'assemble'], ['pcg', 'cg', 'pcg'],
      ['gradient', 'proj', 'gradient'], ['copyV', 'proj', 'copyV'], ['extend', 'proj', 'extend'], ['zeroInvalid', 'proj', 'zeroInvalid'], ['g2p', 'g2p', 'g2p'], ['advect', 'g2p', 'advect'], ['momentum', 'red', 'momentum']])
      K[k] = d.createComputePipeline({ label: e, layout: PL[m], compute: { module: M[m], entryPoint: e } });
    const bg = (k, bufs) => d.createBindGroup({ label: k, layout: L[k], entries: bufs.map((bf, i) => ({ binding: i, resource: i === 0 ? { buffer: bf, size: 128 } : { buffer: bf } })) });
    const B = this.B, G = this.G = {}, base = [B.params, B.prof];
    // the particle arrays ping-pong: index 0 sorts A into B and works on B; index 1 sorts B into A and works on A
    G.count = [bg('sort', base.concat([B.posA, B.cnt, B.pcell, B.fillp, B.order, B.cellStart, B.nslot])), bg('sort', base.concat([B.posB, B.cnt, B.pcell, B.fillp, B.order, B.cellStart, B.nslot]))];
    G.permute = [bg('perm', base.concat([B.cellStart, B.order, B.posA, B.velA, B.cA, B.posB, B.velB, B.cB])), bg('perm', base.concat([B.cellStart, B.order, B.posB, B.velB, B.cB, B.posA, B.velA, B.cA]))];
    const work = [[B.posB, B.velB, B.cB], [B.posA, B.velA, B.cA]];
    G.ls = work.map((w) => bg('ls', base.concat([B.cellStart, w[0], B.maskA, B.maskB, B.phi, B.fluid, B.imgF])));
    G.inh = bg('inh', base.concat([B.faces, B.phi, B.fluid, B.flagCopy, B.phiCopy]));
    G.p2g = work.map((w) => bg('p2g', base.concat([B.cellStart, w[0], w[1], w[2], B.grid])));
    G.forces = [B.whichU, B.whichV, B.whichW].map((wb) => bg('forces', base.concat([B.faces, B.grid, B.tgrid, wb])));
    G.assemble = bg('pr', base.concat([B.faces, B.grid, B.phi, B.fluid, B.A, B.b]));
    G.pcg = bg('cg', base.concat([B.fluid, B.A, B.b, B.q, B.L, B.work, B.stat]));
    G.proj = [B.whichU, B.whichV, B.whichW].map((wb) => bg('proj', base.concat([B.faces, B.phi, B.fluid, B.q, B.grid, B.valid, B.tgrid, B.validT, wb])));
    G.g2p = work.map((w) => bg('g2p', base.concat([B.cellStart, B.grid, w[0], w[1], w[2], B.spill, B.spillN])));
    G.red = work.map((w) => bg('red', base.concat([B.cellStart, w[0], w[1], B.part, B.col])));
    this.params = new ArrayBuffer(256 * GpuFluid.MAXB); this.pi = new Int32Array(this.params); this.pf = new Float32Array(this.params);
    this.errors = [];
    d.addEventListener && d.addEventListener('uncapturederror', (e) => { if (this.errors.length < 20) this.errors.push(e.error.message); });
    this.ready = true;
    // one empty step builds the level set and the column heights, so the surface can be read before the first step
    await this.steps([{ dt: 0, ax: 0, az: 0 }]);
  };
  // the particles into array set A; the slots the next sort reads (live and dead) are this.slots
  GpuFluid.prototype.uploadParticles = function () {
    const n = this.np, pos = new Float32Array(4 * n), vel = new Float32Array(4 * n), c = new Float32Array(12 * n);
    for (let p = 0; p < n; p++) { pos[4 * p] = this.px[p]; pos[4 * p + 1] = this.py[p]; pos[4 * p + 2] = this.pz[p]; pos[4 * p + 3] = 1; vel[4 * p] = this.pu[p]; vel[4 * p + 1] = this.pv[p]; vel[4 * p + 2] = this.pw[p]; }
    this.device.queue.writeBuffer(this.B.posA, 0, pos); this.device.queue.writeBuffer(this.B.velA, 0, vel); this.device.queue.writeBuffer(this.B.cA, 0, c);
    this.device.queue.writeBuffer(this.B.q, 0, new Float32Array(this.nc));
    this.device.queue.writeBuffer(this.B.cellStart, 4 * this.nc, new Int32Array([n]));   // the slots the first sort reads
    this.side = 0; this.slots = n;
  };
  GpuFluid.prototype.writeParams = function (st, si) {
    const o = 64 * si, pi = this.pi.subarray(o, o + 32), pf = this.pf.subarray(o, o + 32);
    pi[0] = this.nx; pi[1] = this.ny; pi[2] = this.nz; pi[3] = this.nc; pi[4] = this.slots; pi[5] = this.npCap; pi[6] = this.oV; pi[7] = this.oW;
    pf[8] = this.dx; pf[9] = this.x0; pf[10] = this.y0; pf[11] = this.H; pf[12] = st.dt; pf[13] = st.ax; pf[14] = st.az; pf[15] = this.g;
    pf[16] = this.nu; pf[17] = this.rp; pf[18] = this.kernel * this.dx; pf[19] = this.zRim; pf[20] = this.Rrim; pf[21] = this.Rbox; pf[22] = this.Vseed; pf[23] = this.sliver;
    pf[24] = this.thetaMin; pf[25] = this.forcedPhi; pf[26] = this.tol; pf[27] = this.maxIt; pi[28] = this.profile.R.length; pf[29] = this.profile.dz;
  };
  GpuFluid.MAXB = 16;          // steps in one submission at most
  GpuFluid.SPILLCAP = 1024;    // spilled particles recorded per step at most
  // where each step's numbers land in the read-back buffer
  GpuFluid.prototype.readLayout = function (cap) {
    const nPart = Math.ceil(Math.max(1, cap) / WG), per = 64 + 16 * nPart + 32 * GpuFluid.SPILLCAP, ncol = this.nx * this.ny;
    return { nPart, per, col: per * GpuFluid.MAXB, total: per * GpuFluid.MAXB + 4 * ncol };
  };
  // Steps, each {dt, ax, az}, each followed by a read-back of what the cart and the probes need: the live count, the
  // pressure solve's iterations and residual, the particles that spilled (positions and velocities), the momentum relative
  // to the glass and the fastest particle (per-workgroup partial sums in a fixed order, added here in a fixed order), and
  // the particles per column. Spill totals are summed over the list; the rest describes the last step.
  GpuFluid.prototype.steps = async function (list) {
    const d = this.device, B = this.B, K = this.K, G = this.G, nc = this.nc, MAXB = GpuFluid.MAXB;
    const wg = (n) => Math.ceil(Math.max(1, n) / WG);
    const batchSpill = [], perStep = [];
    let spillPx = 0, spillPz = 0, spillCount = 0;
    for (let b0 = 0; b0 < list.length; b0 += MAXB) {
      const chunk = list.slice(b0, b0 + MAXB), slots = this.slots, RL = this.readLayout(this.npCap);
      chunk.forEach((st, si) => this.writeParams(st, si));
      d.queue.writeBuffer(B.params, 0, this.params, 0, 256 * chunk.length);
      const enc = d.createCommandEncoder();
      let side = this.side;
      chunk.forEach((st, si) => {
        const dyn = [256 * si], other = 1 - side;
        // the slots this step's sort reads: what the previous sort kept (cellStart[nc])
        enc.copyBufferToBuffer(B.cellStart, 4 * nc, B.nslot, 0, 4);
        enc.clearBuffer(B.cnt); enc.clearBuffer(B.spillN); enc.clearBuffer(B.col); enc.clearBuffer(B.part);
        const pass = enc.beginComputePass();
        const run = (k, g, n) => { pass.setPipeline(K[k]); pass.setBindGroup(0, g, dyn); pass.dispatchWorkgroups(wg(n)); };
        run('count', G.count[side], slots); pass.setPipeline(K.scan); pass.setBindGroup(0, G.count[side], dyn); pass.dispatchWorkgroups(1);
        run('scatter', G.count[side], slots); run('sortCell', G.count[side], nc);
        run('permute', G.permute[side], slots);
        const gl = G.ls[side], gp = G.p2g[side], gg = G.g2p[side], gr = G.red[side];   // index `side` works on the other set
        run('masks', gl, nc); run('dilate0', gl, nc); run('dilateX', gl, nc); run('dilateY', gl, nc); run('dilateZ', gl, nc);
        run('phiCells', gl, nc); run('flags', gl, nc);
        run('copyF', G.inh, nc); run('inherit', G.inh, nc); run('copyF', G.inh, nc); run('inherit', G.inh, nc);
        if (st.dt > 0) {
          run('p2gU', gp, this.nu_); run('p2gV', gp, this.nv_); run('p2gW', gp, this.nw_);
          const sizes = [this.nu_, this.nv_, this.nw_];
          for (let c = 0; c < 3; c++) run('force', G.forces[c], sizes[c]);
          if (this.nu > 0) for (let c = 0; c < 3; c++) { run('copyT', G.forces[c], sizes[c]); run('visc', G.forces[c], sizes[c]); }
          run('assemble', G.assemble, nc);
          pass.setPipeline(K.pcg); pass.setBindGroup(0, G.pcg, dyn); pass.dispatchWorkgroups(1);
          for (let c = 0; c < 3; c++) {
            run('gradient', G.proj[c], sizes[c]);
            for (let l = 0; l < 3; l++) { run('copyV', G.proj[c], sizes[c]); run('extend', G.proj[c], sizes[c]); }
            run('zeroInvalid', G.proj[c], sizes[c]);
          }
          run('g2p', gg, slots); run('advect', gg, slots);
        }
        run('momentum', gr, slots);
        pass.end();
        const o = RL.per * si;
        enc.copyBufferToBuffer(B.cellStart, 4 * nc, B.read, o, 4);
        enc.copyBufferToBuffer(B.stat, 0, B.read, o + 16, 16);
        enc.copyBufferToBuffer(B.spillN, 0, B.read, o + 32, 4);
        enc.copyBufferToBuffer(B.part, 0, B.read, o + 64, 16 * RL.nPart);
        enc.copyBufferToBuffer(B.spill, 0, B.read, o + 64 + 16 * RL.nPart, 32 * GpuFluid.SPILLCAP);
        side = other;
      });
      enc.copyBufferToBuffer(B.col, 0, B.read, RL.col, 4 * this.nx * this.ny);
      d.queue.submit([enc.finish()]);
      await B.read.mapAsync(GPUMapMode.READ);
      const buf = B.read.getMappedRange().slice(0); B.read.unmap();
      const I = new Int32Array(buf), F = new Float32Array(buf), mp = this.mp;
      chunk.forEach((st, si) => {
        const o = RL.per * si / 4, sorted = I[o], it = F[o + 4], res = F[o + 5], nSp = Math.min(GpuFluid.SPILLCAP, I[o + 8]);
        let sx = 0, sy = 0, sz = 0, vm = 0;
        for (let k = 0; k < RL.nPart; k++) { const q = o + 16 + 4 * k; sx += F[q]; sy += F[q + 1]; sz += F[q + 2]; vm = Math.max(vm, F[q + 3]); }
        let px = 0, pz = 0;
        for (let k = 0; k < nSp; k++) { const q = o + 16 + 4 * RL.nPart + 8 * k; batchSpill.push([F[q], F[q + 1], F[q + 2], F[q + 4], F[q + 5], F[q + 6]]); px += F[q + 4]; pz += F[q + 6]; }
        spillPx += px; spillPz += pz; spillCount += nSp;
        // the sort kept `sorted` particles (in cell order, in the other set); those that spilled in this step are marked
        // dead there and drop out at the next sort
        this.slots = sorted; this.np = sorted - nSp; this.cgIters = it; this.cgResidual = res;
        this.P = [mp * sx, mp * sz]; this.Py = mp * sy; this.vmax = Math.sqrt(vm);
        if (st.dt > 0) this.t += st.dt;
        perStep.push({ P: this.P.slice(), spillN: nSp, spillPx: mp * px, spillPz: mp * pz, cg: it, vmax: this.vmax, np: this.np });
      });
      this.side = side;
      const col = this.colCnt; for (let k = 0; k < col.length; k++) col[k] = I[RL.col / 4 + k];
    }
    this.spillNow = spillCount; this.spilled += spillCount; this.spillPx = this.mp * spillPx; this.spillPz = this.mp * spillPz; this.spillList = batchSpill;
    this.perStep = perStep;
    this.columnHeights();
    return perStep;
  };
  // read the particle positions back (for the store and the drawing), the live ones only, into px, py, pz
  GpuFluid.prototype.readPositions = async function () {
    const d = this.device, B = this.B, src = this.side === 0 ? B.posA : B.posB, n = this.slots;
    if (n === 0) { this.nRead = 0; return; }
    const enc = d.createCommandEncoder(); enc.copyBufferToBuffer(src, 0, B.readPos, 0, 16 * n); d.queue.submit([enc.finish()]);
    await B.readPos.mapAsync(GPUMapMode.READ, 0, 16 * n);
    const F = new Float32Array(B.readPos.getMappedRange(0, 16 * n).slice(0)); B.readPos.unmap();
    if (this.px.length < n) { this.px = new Float64Array(n); this.py = new Float64Array(n); this.pz = new Float64Array(n); }
    let m = 0;
    for (let p = 0; p < n; p++) { if (F[4 * p + 3] < 0) continue; this.px[m] = F[4 * p]; this.py[m] = F[4 * p + 1]; this.pz[m] = F[4 * p + 2]; m++; }
    this.nRead = m;
  };
  // Column heights from the integer particle counts per column (Fluid.columnHeights: the 3 x 3 binomial filter, the
  // smoothed open volume table inverted), over the whole glass (no fold)
  GpuFluid.prototype.columnHeights = function () {
    const nx = this.nx, ny = this.ny, dx = this.dx, ncol = nx * ny, out = this.colH;
    const vol = this.colVol || (this.colVol = new Float64Array(ncol)), Vp = this.Vseed;
    for (let n = 0; n < ncol; n++) vol[n] = this.colCnt[n] * Vp;
    const blur = (src, dst, off, stride) => {
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
        let a = 0;
        for (let dj = -1; dj <= 1; dj++) for (let di = -1; di <= 1; di++) {
          const ii = i + di, jj = j + dj; if (ii < 0 || ii >= nx || jj < 0 || jj >= ny) continue;
          a += (di ? 0.25 : 0.5) * (dj ? 0.25 : 0.5) * src[(ii + nx * jj) * stride + off];
        }
        dst[(i + nx * j) * stride + off] = a;
      }
    };
    if (!this.colVb) this.buildColumnTables(blur);
    const t1 = this.colT1 || (this.colT1 = new Float64Array(ncol));
    blur(vol, t1, 0, 1);
    const M = this.colM, Vb = this.colVb, dz = this.colDz;
    for (let n = 0; n < ncol; n++) {
      const v = t1[n], base = n * (M + 1);
      if (Vb[base + M] <= 0) { out[n] = 0; continue; }
      if (v >= Vb[base + M]) { out[n] = M * dz; continue; }
      let lo = 0, hi = M;
      while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (Vb[base + mid] <= v) lo = mid; else hi = mid; }
      const a = Vb[base + lo], b = Vb[base + hi];
      out[n] = (lo + (b > a ? (v - a) / (b - a) : 0)) * dz;
    }
    return out;
  };
  GpuFluid.prototype.buildColumnTables = function (blur) {
    const nx = this.nx, ny = this.ny, dx = this.dx, ncol = nx * ny, dz = 0.0005, M = Math.round(this.H / dz), S = 12;
    const Vc = new Float64Array(ncol * (M + 1)), Vb = new Float64Array(ncol * (M + 1));
    for (let m = 1; m <= M; m++) {
      const R = Math.min(this.Rz((m - 0.5) * dz), 2 * this.Rbox), R2 = R * R;
      for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
        let n = 0;
        for (let a = 0; a < S; a++) for (let b = 0; b < S; b++) { const x = this.x0 + (i + (a + 0.5) / S) * dx, y = this.y0 + (j + (b + 0.5) / S) * dx; if (x * x + y * y < R2) n++; }
        const c = i + nx * j;
        Vc[c * (M + 1) + m] = Vc[c * (M + 1) + m - 1] + n / (S * S) * dx * dx * dz;
      }
    }
    for (let m = 0; m <= M; m++) blur(Vc, Vb, m, M + 1);
    this.colVc = Vc; this.colVb = Vb; this.colM = M; this.colDz = dz;
    this.colArea = new Float64Array(ncol); for (let c = 0; c < ncol; c++) this.colArea[c] = Vc[c * (M + 1) + 1] / dz;
  };
  // the column height at (x, y), bilinear between column centres, extended linearly along the radius near the wall
  GpuFluid.prototype.columnHeightAt = function (x, y) {
    const dx = this.dx, r = Math.hypot(x, y), r1 = this.Rz(Math.min(this.h0, this.zRim)) - 2.5 * dx, r2 = r1 - 1.5 * dx;
    if (r > r1) { const cx = x / r, cy = y / r, h1 = this.colBilinear(cx * r1, cy * r1), h2 = this.colBilinear(cx * r2, cy * r2); return h1 + (r - r1) * (h1 - h2) / (r1 - r2); }
    return this.colBilinear(x, y);
  };
  GpuFluid.prototype.colBilinear = function (x, y) {
    const nx = this.nx, ny = this.ny, dx = this.dx, H = this.colH;
    const fx = (x - this.x0) / dx - 0.5, fy = (y - this.y0) / dx - 0.5, i = Math.floor(fx), j = Math.floor(fy), tx = fx - i, ty = fy - j;
    const at = (a, b) => { a = a < 0 ? 0 : a >= nx ? nx - 1 : a; b = b < 0 ? 0 : b >= ny ? ny - 1 : b; return H[a + nx * b]; };
    return (1 - tx) * (1 - ty) * at(i, j) + tx * (1 - ty) * at(i + 1, j) + (1 - tx) * ty * at(i, j + 1) + tx * ty * at(i + 1, j + 1);
  };
  // a WebGPU device, or null where the browser has none
  GpuFluid.device = async function () {
    if (typeof navigator === 'undefined' || !navigator.gpu) return null;
    const a = await navigator.gpu.requestAdapter(); if (!a) return null;
    const dev = await a.requestDevice();
    const info = a.info || {};
    dev.gpuInfo = { vendor: info.vendor || '', architecture: info.architecture || '', description: info.description || '' };
    return dev;
  };

  root.StoutGpu = { GpuFluid, WG };
})(typeof self !== 'undefined' ? self : this);
