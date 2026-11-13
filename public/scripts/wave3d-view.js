/* Wave3D: the lit 3D views of Fig. 14 (three.js 0.170, vendored in vendor/three/). Three ways to draw the same stored wave:
     'sheets'  - the surfaces Re psi = +c (crests, wine) and Re psi = -c (troughs, slate), lit and shaded, in a room with a floor;
     'cutaway' - the same sheets with the quarter y > 0, z > 0 cut away, so the inside of the wave and of the barrier shows;
     'surface' - the plane z = 0 through the flight axis, lifted by Re psi: a height map, coloured by the sign of Re psi;
     'mesh'    - the default: the plane z = 0 as a smooth height surface with a thin wire mesh on it, in the house colours (paper
                 at zero, wine on the crests, ink slate in the troughs), no floor and no box; the barrier as an outline on the sheet.
   The page hands over numbers it read from Kaggle's files; this module only draws them: a 3D field of Re psi on a grid (for the
   sheets, found by marching cubes), or a 2D plane of Re psi (for the surface). Physics axes: x along the flight, z up on screen.
   Turning: press and drag on the canvas (never a mere pass of the pointer). Docs: docs/scripts/wave3d-view.md. */
import * as THREE from '../vendor/three/three.module.min.js';
import { marching } from './marching.js';
export { marching };

const PAPER = 0xf5f1ea, CARD = 0xfbf6ee, WINE = 0xa3303f, SLATE = 0x55607a, ROSE = 0xe2a2aa, TAN = 0xd9b56b;
const P = (x, y, z) => new THREE.Vector3(x, z, y);          /* physics (x, y, z) -> three (x, y = up, z) */

/* the colour of the height surface for a value v of Re psi (fraction of the first frame's peak): paper at 0, towards wine (v > 0)
   or slate (v < 0), full at |v| = 0.5. Exported so that the page's data panel can state the rule it checks pixels against. */
export function surfaceColour(v) {
    const a = Math.min(1, Math.abs(v) / 0.5), c = new THREE.Color(CARD), t = new THREE.Color(v > 0 ? WINE : SLATE);
    return c.lerp(t, a);
}

/* the colour of the meshed sheet, in the house colours, for v in [-1, 1] (the height drawn over the largest on the sheet):
   card paper at 0, towards wine for v > 0 (crests) and towards the ink slate for v < 0 (troughs), full at |v| = 1; mixed in
   sRGB as the page states it. Exported so that the data panel can invert it from a read-back pixel. */
export const MESH_ZERO = [0xfb, 0xf6, 0xee], MESH_CREST = [0xa3, 0x30, 0x3f], MESH_TROUGH = [0x55, 0x60, 0x7a];
export function meshColour(v) {
    v = Math.max(-1, Math.min(1, v)); const e = v >= 0 ? MESH_CREST : MESH_TROUGH, a = Math.abs(v);
    return new THREE.Color((MESH_ZERO[0] + a * (e[0] - MESH_ZERO[0])) / 255, (MESH_ZERO[1] + a * (e[1] - MESH_ZERO[1])) / 255, (MESH_ZERO[2] + a * (e[2] - MESH_ZERO[2])) / 255);
}
/* the inverse used by the pixel check. White light scales a colour's three linear components by one factor, which leaves the
   ratios of its sRGB components nearly unchanged. Towards wine the ratio g / r falls from 246/251 to 48/163; towards slate the
   ratio r / b falls from 251/238 to 85/122. Each ratio is solved for |v|; a pixel with more blue against red than the paper has is on the slate side. */
export function meshV(px) {
    const r = px[0], g = px[1], b = px[2]; if (r <= 0 || b <= 0) return NaN;
    const Z = MESH_ZERO, C = MESH_CREST, T = MESH_TROUGH, q1 = g / r, q2 = r / b;
    const vw = (Z[1] - q1 * Z[0]) / ((Z[1] - C[1]) - q1 * (Z[0] - C[0]));      /* g / r = (Zg - v (Zg - Cg)) / (Zr - v (Zr - Cr)) */
    const vs = (Z[0] - q2 * Z[2]) / ((Z[0] - T[0]) - q2 * (Z[2] - T[2]));      /* r / b = (Zr - v (Zr - Tr)) / (Zb - v (Zb - Tb)) */
    return q2 < Z[0] / Z[2] ? -vs : vw;                                        /* more blue than the paper has: the slate side */
}

export function create(canvas, opt) {
    opt = opt || {};
    const r = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, alpha: false });
    r.setClearColor(PAPER); r.shadowMap.enabled = true; r.shadowMap.type = THREE.PCFSoftShadowMap; r.localClippingEnabled = true;
    r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = 1.15;
    const scene = new THREE.Scene(); scene.fog = new THREE.Fog(PAPER, 80, 160);
    const cam = new THREE.PerspectiveCamera(34, 1, 0.5, 400);
    const hemi = new THREE.HemisphereLight(0xfffaf3, 0xb8aea4, 1.6); scene.add(hemi); const roomFog = scene.fog;
    const sun = new THREE.DirectionalLight(0xffffff, 2.2); sun.position.set(-18, 40, 22); sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -36, right: 36, top: 30, bottom: -30, near: 1, far: 140 });
    sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.06; scene.add(sun);
    const fill = new THREE.DirectionalLight(0xffeedd, 0.9); fill.position.set(-40, 5, 30); scene.add(fill);
    const FLOOR = -17.5;
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(110, 90), new THREE.MeshStandardMaterial({ color: CARD, roughness: 1 }));
    floor.rotation.x = -Math.PI / 2; floor.position.y = FLOOR; floor.receiveShadow = true; scene.add(floor);
    const grid = new THREE.GridHelper(110, 55, 0xd9d0c2, 0xe6dfd2); grid.scale.z = 90 / 110; grid.position.y = FLOOR + 0.01; scene.add(grid);
    const axisLine = new THREE.Line(new THREE.BufferGeometry().setFromPoints([P(-26, 0, 0), P(26, 0, 0)]), new THREE.LineDashedMaterial({ color: 0x8b8079, dashSize: 0.8, gapSize: 0.5 }));
    axisLine.computeLineDistances(); scene.add(axisLine);
    const arrow = new THREE.ArrowHelper(new THREE.Vector3(1, 0, 0), P(-27, 0, 0), 5, 0x1c1518, 1.1, 0.55); scene.add(arrow);
    /* the cutaway removes the quarter y > 0 and z > 0 (physics): three's z > 0 and y > 0; an object is clipped only where both planes clip */
    const cut = [new THREE.Plane(new THREE.Vector3(0, 0, -1), 0), new THREE.Plane(new THREE.Vector3(0, -1, 0), 0)];
    const matSheet = (color) => new THREE.MeshPhysicalMaterial({ color, roughness: 0.32, metalness: 0, clearcoat: 0.6, clearcoatRoughness: 0.3, side: THREE.DoubleSide, clipIntersection: true });
    const crestMat = matSheet(WINE), troughMat = matSheet(SLATE);
    const crest = new THREE.Mesh(new THREE.BufferGeometry(), crestMat), trough = new THREE.Mesh(new THREE.BufferGeometry(), troughMat);
    for (const m of [crest, trough]) { m.castShadow = true; m.receiveShadow = true; m.frustumCulled = false; scene.add(m); }
    const surfMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.55, side: THREE.DoubleSide });
    const surf = new THREE.Mesh(new THREE.BufferGeometry(), surfMat); surf.castShadow = true; surf.receiveShadow = false;   /* no self-shadow: a lifted sheet shadowing itself shows moiré */ surf.frustumCulled = false; scene.add(surf);
    const barrier = new THREE.Group(); scene.add(barrier);
    /* ---------- the meshed sheet (mode 'mesh'): one smooth surface, a thin wire mesh lying on it, the barrier's outline ---------- */
    const meshMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.6, metalness: 0, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
    meshMat.toneMapped = false;   /* the ramp's colours as stated, only shaded by the light: the pixel check inverts them */
    const sheet = new THREE.Mesh(new THREE.BufferGeometry(), meshMat); sheet.frustumCulled = false; scene.add(sheet);
    const wireMat = new THREE.LineBasicMaterial({ color: 0x1c1518, transparent: true, opacity: 0.26 }); wireMat.toneMapped = false;
    const wire = new THREE.LineSegments(new THREE.BufferGeometry(), wireMat); wire.frustumCulled = false; scene.add(wire);
    const outMat = new THREE.LineBasicMaterial({ color: 0x1c1518, transparent: true, opacity: 0.85 }); outMat.toneMapped = false;
    const outline = new THREE.Group(); scene.add(outline);
    const LUT = new Float32Array(1025 * 3); for (let q = 0; q <= 1024; q++) { const c = meshColour(q / 512 - 1).convertSRGBToLinear(); LUT[3 * q] = c.r; LUT[3 * q + 1] = c.g; LUT[3 * q + 2] = c.b; }
    const api = { yaw: -0.62, pitch: 0.42, dist: 64, mode: 'sheets', level: 0.25, height: 6, ok: true, renderer: r, THREE, meshCam: { yaw: -0.79, pitch: 0.55, dist: 80 } };

    /* ---------- the barrier as its true solid: glass for a finite height, opaque for a hard wall, tan for a well ---------- */
    api.setBarrier = function (b) {
        while (barrier.children.length) { const c = barrier.children.pop(); c.geometry.dispose(); c.material.dispose(); }
        if (!b || !b.shape) return;
        const hard = !!b.hard, well = !hard && b.V0 < 0;
        const mat = new THREE.MeshPhysicalMaterial({ color: well ? TAN : ROSE, roughness: hard ? 0.55 : 0.15, clearcoat: hard ? 0 : 1, transparent: !hard, opacity: hard ? 1 : (well ? 0.32 : 0.3), depthWrite: hard, side: THREE.DoubleSide, clipIntersection: true });
        let g = null, mesh;
        if (b.shape === 'sphere') g = new THREE.SphereGeometry(b.R, 96, 64);
        else if (b.shape === 'slab') { g = new THREE.BoxGeometry(b.a, 32, 32); }                       /* |x| < a/2; drawn over the box |y|, |z| <= 16 */
        else if (b.shape === 'pillar') { g = new THREE.CylinderGeometry(b.R, b.R, 32, 96, 1, false); }  /* axis = physics z = three's y: unbounded, drawn 32 a tall */
        else if (b.shape === 'coin') { g = new THREE.CylinderGeometry(b.R, b.R, b.a, 96, 1, false); }
        else if (b.shape === 'tube') { g = new THREE.CylinderGeometry(b.R, b.R, 48, 96, 1, true); }
        if (!g) return;
        mesh = new THREE.Mesh(g, mat);
        if (b.shape === 'coin' || b.shape === 'tube') mesh.rotation.z = Math.PI / 2;                  /* axis along the flight */
        mesh.castShadow = true; mesh.renderOrder = 2; barrier.add(mesh);
        api.barrier = b; applyMode();
    };

    /* ---------- data in ---------- */
    api.setField = function (field, nx, ny, nz, x0, y0, z0, h, level, hx) {
        if (level != null) api.level = level;
        const c = marching(field, nx, ny, nz, api.level, 1, x0, y0, z0, h, hx), t = marching(field, nx, ny, nz, api.level, -1, x0, y0, z0, h, hx);
        setGeo(crest, c); setGeo(trough, t);
        api.lastField = { field, nx, ny, nz, x0, y0, z0, h }; api.triangles = (c.pos.length + t.pos.length) / 9;
    };
    api.setSheets = function (c, t) {   /* the two sheets as triangles already found (by the worker): { pos, nor } each, in three's axes */
        setGeo(crest, c); setGeo(trough, t); api.triangles = (c.pos.length + t.pos.length) / 9;
    };
    function setGeo(m, d) {
        const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(d.pos, 3)); g.setAttribute('normal', new THREE.BufferAttribute(d.nor, 3));
        m.geometry.dispose(); m.geometry = g;
    }
    api.setPlane = function (plane, nx, ny, x0, y0, h, scale) {        /* plane[i * ny + j] = Re psi at (x0 + i h, y0 + j h, z = 0); scale: the |Re psi| drawn at full colour and height */
        api.scale = scale || 1;
        let g = surf.geometry;
        if (!g.attributes.position || g.attributes.position.count !== nx * ny) {
            g.dispose(); g = new THREE.BufferGeometry();
            g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(nx * ny * 3), 3)); g.setAttribute('color', new THREE.BufferAttribute(new Float32Array(nx * ny * 3), 3));
            const idx = []; for (let i = 0; i < nx - 1; i++) for (let j = 0; j < ny - 1; j++) { const a = i * ny + j, b = a + ny; idx.push(a, b, a + 1, a + 1, b, b + 1); }
            g.setIndex(idx); surf.geometry = g;
        }
        const pos = g.attributes.position.array, col = g.attributes.color.array;
        for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++) {
            const q = i * ny + j, v = plane[q] / api.scale, c = surfaceColour(v).convertSRGBToLinear();   /* vertex colours are linear in three */
            pos[3 * q] = x0 + i * h; pos[3 * q + 1] = v * api.height; pos[3 * q + 2] = y0 + j * h;
            col[3 * q] = c.r; col[3 * q + 1] = c.g; col[3 * q + 2] = c.b;
        }
        g.attributes.position.needsUpdate = true; g.attributes.color.needsUpdate = true; g.computeVertexNormals();
        api.lastPlane = { plane, nx, ny, x0, y0, h };
    };
    /* spherical waves: psi depends on r alone, so the surfaces Re psi = +c and -c are exact spheres, at the radii where the
       stored radial profile crosses +c and -c (the page finds them). Drawn as true spheres, not by marching cubes on a grid. */
    function spheresGeo(radii) {
        const parts = radii.map((rr) => new THREE.SphereGeometry(rr, 128, 64).toNonIndexed());
        let n = 0; parts.forEach((g) => { n += g.attributes.position.count; });
        const pos = new Float32Array(3 * n), nor = new Float32Array(3 * n); let o = 0;
        parts.forEach((g) => { pos.set(g.attributes.position.array, o); nor.set(g.attributes.normal.array, o); o += g.attributes.position.array.length; g.dispose(); });
        return { pos, nor };
    }
    api.setShells = function (crestRadii, troughRadii) {
        const c = spheresGeo(crestRadii), t = spheresGeo(troughRadii);
        setGeo(crest, c); setGeo(trough, t); api.triangles = (c.pos.length + t.pos.length) / 9; api.shells = { crest: crestRadii.slice(), trough: troughRadii.slice() };
    };
    /* spherical waves in the Surface view: the plane z = 0 lifted by Re psi(r), a surface of revolution on a fine polar mesh */
    api.setRevolution = function (re, rmax, dr, scale) {     /* re(r): Re psi at radius r; rings every dr out to rmax */
        api.scale = scale || 1;
        const nr = Math.floor(rmax / dr) + 1, nt = 192, N = nr * nt;
        let g = surf.geometry;
        if (!g.attributes.position || g.attributes.position.count !== N || !g.userData.polar) {
            g.dispose(); g = new THREE.BufferGeometry(); g.userData.polar = true;
            g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(N * 3), 3)); g.setAttribute('color', new THREE.BufferAttribute(new Float32Array(N * 3), 3));
            const idx = []; for (let i = 0; i < nr - 1; i++) for (let j = 0; j < nt; j++) { const a = i * nt + j, b = a + nt, a1 = i * nt + (j + 1) % nt, b1 = a1 + nt; idx.push(a, b, a1, a1, b, b1); }
            g.setIndex(idx); surf.geometry = g;
        }
        const pos = g.attributes.position.array, col = g.attributes.color.array;
        for (let i = 0; i < nr; i++) {
            const r = i * dr, v = re(r) / api.scale, c = surfaceColour(v).convertSRGBToLinear();
            for (let j = 0; j < nt; j++) { const q = i * nt + j, th = 2 * Math.PI * j / nt; pos[3 * q] = r * Math.cos(th); pos[3 * q + 1] = v * api.height; pos[3 * q + 2] = r * Math.sin(th); col[3 * q] = c.r; col[3 * q + 1] = c.g; col[3 * q + 2] = c.b; }
        }
        g.attributes.position.needsUpdate = true; g.attributes.color.needsUpdate = true; g.computeVertexNormals();
        api.lastPlane = { radial: true };
    };
    /* o: { nx, ny, x0, y0, h: the grid of the sheet (physics x = x0 + i h, y = y0 + j h); H[i * ny + j]: its height (physics z, in a);
            T[i * ny + j]: its colour, 0 (trough slate) through 0.5 (paper) to 1 (crest wine); every: a mesh line on every every-th grid line; outline: polylines
            [x0, y0, x1, y1, ...] in the plane, drawn on the sheet; key: a new key rebuilds the grid } */
    api.setMesh = function (o) {
        const nx = o.nx, ny = o.ny, N = nx * ny, h = o.h, H = o.H, T = o.T;
        let g = sheet.geometry;
        if (!g.attributes.position || g.userData.key !== o.key) {
            g.dispose(); g = new THREE.BufferGeometry(); g.userData = { key: o.key };
            const pos = new THREE.BufferAttribute(new Float32Array(N * 3), 3); pos.setUsage(THREE.DynamicDrawUsage);
            g.setAttribute('position', pos); g.setAttribute('normal', new THREE.BufferAttribute(new Float32Array(N * 3), 3)); g.setAttribute('color', new THREE.BufferAttribute(new Float32Array(N * 3), 3));
            const idx = new Uint32Array((nx - 1) * (ny - 1) * 6); let k = 0;
            for (let i = 0; i < nx - 1; i++) for (let j = 0; j < ny - 1; j++) { const a = i * ny + j, b = a + ny; idx[k++] = a; idx[k++] = a + 1; idx[k++] = b; idx[k++] = b; idx[k++] = a + 1; idx[k++] = b + 1; }
            g.setIndex(new THREE.BufferAttribute(idx, 1)); sheet.geometry = g;
            const li = [], ev = o.every;
            for (let i = 0; i < nx; i += ev) for (let j = 0; j < ny - 1; j++) li.push(i * ny + j, i * ny + j + 1);
            for (let j = 0; j < ny; j += ev) for (let i = 0; i < nx - 1; i++) li.push(i * ny + j, (i + 1) * ny + j);
            const wg = new THREE.BufferGeometry(); wg.setAttribute('position', pos); wg.setIndex(li); wire.geometry.dispose(); wire.geometry = wg;
        }
        const pos = g.attributes.position.array, nor = g.attributes.normal.array, col = g.attributes.color.array;
        for (let i = 0; i < nx; i++) {
            const i0 = i > 0 ? i - 1 : 0, i1 = i < nx - 1 ? i + 1 : nx - 1;
            for (let j = 0; j < ny; j++) {
                const q = i * ny + j, j0 = j > 0 ? j - 1 : 0, j1 = j < ny - 1 ? j + 1 : ny - 1;
                pos[3 * q] = o.x0 + i * h; pos[3 * q + 1] = H[q]; pos[3 * q + 2] = o.y0 + j * h;     /* physics (x, y, z) -> three (x, z, y) */
                const hx = (H[i1 * ny + j] - H[i0 * ny + j]) / ((i1 - i0) * h), hy = (H[i * ny + j1] - H[i * ny + j0]) / ((j1 - j0) * h), m = 1 / Math.sqrt(1 + hx * hx + hy * hy);
                nor[3 * q] = -hx * m; nor[3 * q + 1] = m; nor[3 * q + 2] = -hy * m;
                const t = T[q], u = Math.round(1024 * (t < 0 ? 0 : t > 1 ? 1 : t)) * 3; col[3 * q] = LUT[u]; col[3 * q + 1] = LUT[u + 1]; col[3 * q + 2] = LUT[u + 2];
            }
        }
        g.attributes.position.needsUpdate = true; g.attributes.normal.needsUpdate = true; g.attributes.color.needsUpdate = true; g.computeBoundingSphere();
        while (outline.children.length) { const c = outline.children.pop(); c.geometry.dispose(); }
        const at = (x, y) => {                          /* the sheet's height at (x, y), bilinear between its grid points */
            const u = Math.max(0, Math.min(nx - 1.0001, (x - o.x0) / h)), v = Math.max(0, Math.min(ny - 1.0001, (y - o.y0) / h)), i = Math.floor(u), j = Math.floor(v), a = u - i, b = v - j;
            return (1 - a) * ((1 - b) * H[i * ny + j] + b * H[i * ny + j + 1]) + a * ((1 - b) * H[(i + 1) * ny + j] + b * H[(i + 1) * ny + j + 1]);
        };
        (o.outline || []).forEach((pl) => {
            const pts = []; for (let k = 0; k < pl.length; k += 2) pts.push(new THREE.Vector3(pl[k], at(pl[k], pl[k + 1]) + 0.06, pl[k + 1]));
            const ln = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), outMat); ln.frustumCulled = false; outline.add(ln);
        });
        api.lastMesh = o; api.heightAt = at;
    };
    api.meshVertex = function (k) { const a = sheet.geometry.attributes.position; return a ? [a.array[3 * k], a.array[3 * k + 2], a.array[3 * k + 1]] : null; };   /* the drawn sheet's own vertex k, in physics (x, y, z) */
    api.setMeshView = function (span) { api.meshCam.dist = 1.34 * span; };   /* the sheet's width in a: the camera stands back to see all of it */
    api.setRoom = function (floorY, dist) {   /* spherical waves fill a larger space: a lower floor and a farther camera */
        floor.position.y = floorY; grid.position.y = floorY + 0.01; api.dist = dist;
        Object.assign(sun.shadow.camera, { left: -60, right: 60, top: 60, bottom: -60, far: 220 }); sun.shadow.camera.updateProjectionMatrix();
    };
    api.clear = function () { setGeo(crest, { pos: new Float32Array(0), nor: new Float32Array(0) }); setGeo(trough, { pos: new Float32Array(0), nor: new Float32Array(0) }); api.lastField = null; };

    function applyMode() {
        const mesh = api.mode === 'mesh', sheets = api.mode === 'sheets' || api.mode === 'cutaway', clip = api.mode === 'cutaway' ? cut : [];
        crest.visible = trough.visible = sheets; surf.visible = api.mode === 'surface';
        sheet.visible = wire.visible = outline.visible = mesh; barrier.visible = floor.visible = grid.visible = axisLine.visible = arrow.visible = !mesh;
        scene.fog = mesh ? null : roomFog;
        /* the sheet is lit by white light only (its colours are read back by the pixel check); the room keeps its warm light */
        hemi.color.set(mesh ? 0xffffff : 0xfffaf3); hemi.groundColor.set(mesh ? 0x8a8a8a : 0xb8aea4); hemi.intensity = mesh ? 1.55 : 1.6;
        sun.intensity = mesh ? 1.9 : 2.2;   /* a level patch of the sheet then shows its own colour: (1.55 + 1.9 cos 35°) / pi = 1.0 */ sun.castShadow = !mesh; fill.intensity = mesh ? 0 : 0.9;
        crestMat.clippingPlanes = troughMat.clippingPlanes = clip;
        barrier.children.forEach((m) => { m.material.clippingPlanes = clip; m.material.needsUpdate = true; });
        crestMat.needsUpdate = troughMat.needsUpdate = true;
    }
    api.setMode = function (m) { api.mode = m; applyMode(); };

    /* ---------- camera, rendering, projection ---------- */
    const camOf = () => api.mode === 'mesh' ? api.meshCam : api;   /* the meshed sheet keeps its own camera */
    function place() {
        const C = camOf(), cp = Math.cos(C.pitch), w = canvas.clientWidth || canvas.width, hh = canvas.clientHeight || canvas.height;
        cam.aspect = w / hh; cam.fov = cam.aspect < 1 ? 34 / Math.max(0.62, cam.aspect) : 34; cam.updateProjectionMatrix();
        cam.position.set(C.dist * cp * Math.sin(C.yaw), C.dist * Math.sin(C.pitch), C.dist * cp * Math.cos(C.yaw));
        if (api.mode === 'mesh') cam.lookAt(0, 0, 0); else cam.lookAt(1, -2, 0);
    }
    api.resize = function (w, h, dpr) { r.setPixelRatio(dpr || 1); r.setSize(w, h, false); };
    api.render = function () { place(); r.render(scene, cam); };
    api.project = function (p) {        /* physics point -> CSS pixels on the canvas */
        place(); const v = P(p[0], p[1], p[2]).project(cam), w = canvas.clientWidth, hh = canvas.clientHeight;
        return { x: (v.x + 1) / 2 * w, y: (1 - v.y) / 2 * hh, inFront: v.z < 1 };
    };
    api.pickPlane = function (cx, cy) {   /* CSS pixel -> the physics point where its ray meets the plane z = 0 through the axis */
        place(); const w = canvas.clientWidth, hh = canvas.clientHeight, rc = new THREE.Raycaster(), hit = new THREE.Vector3();
        rc.setFromCamera(new THREE.Vector2(cx / w * 2 - 1, 1 - cy / hh * 2), cam);
        if (api.mode === 'mesh') { const hits = rc.intersectObject(sheet, false); if (hits.length) { const p = hits[0].point; return [p.x, p.z, p.y]; } return null; }   /* the meshed sheet: where the ray first meets it */
        return rc.ray.intersectPlane(new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), hit) ? [hit.x, hit.z, hit.y] : null;
    };
    api.readPixel = function (cx, cy) {   /* the drawn picture at CSS pixel (cx, cy): [r, g, b, a] */
        const gl = r.getContext(), dpr = r.getPixelRatio(), px = new Uint8Array(4);
        gl.readPixels(Math.round(cx * dpr), Math.round(gl.drawingBufferHeight - 1 - cy * dpr), 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
        return Array.from(px);
    };

    /* ---------- turning: press and drag ---------- */
    let drag = null;
    canvas.addEventListener('pointerdown', (e) => { if (opt.canTurn && !opt.canTurn()) return; const C = camOf(); drag = { x: e.clientX, y: e.clientY, yaw: C.yaw, pitch: C.pitch, C }; canvas.setPointerCapture(e.pointerId); });
    canvas.addEventListener('pointermove', (e) => { if (!drag) return; drag.C.yaw = drag.yaw - (e.clientX - drag.x) * 0.008; drag.C.pitch = Math.max(-0.2, Math.min(1.35, drag.pitch + (e.clientY - drag.y) * 0.008)); if (opt.onTurn) opt.onTurn(); });
    const up = () => { drag = null; }; canvas.addEventListener('pointerup', up); canvas.addEventListener('pointercancel', up);
    applyMode();
    return api;
}

window.Wave3D = { create, marching, surfaceColour, meshColour, meshV, MESH_ZERO, MESH_CREST, MESH_TROUGH };
window.dispatchEvent(new Event('wave3d-ready'));
