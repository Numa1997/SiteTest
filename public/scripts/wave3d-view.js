/* Wave3D: the lit 3D views of Fig. 14 (three.js 0.170, vendored in vendor/three/). Three ways to draw the same stored wave:
     'sheets'  - the surfaces Re psi = +c (crests, wine) and Re psi = -c (troughs, slate), lit and shaded, in a room with a floor;
     'cutaway' - the same sheets with the quarter y > 0, z > 0 cut away, so the inside of the wave and of the barrier shows;
     'surface' - the plane z = 0 through the flight axis, lifted by Re psi: a height map, coloured by the sign of Re psi.
   The page hands over numbers it read from Kaggle's files; this module only draws them: a 3D field of Re psi on a grid (for the
   sheets, found by marching cubes), or a 2D plane of Re psi (for the surface). Physics axes: x along the flight, z up on screen.
   Turning: press and drag on the canvas (never a mere pass of the pointer). Docs: docs/scripts/wave3d-view.md. */
import * as THREE from '../vendor/three/three.module.min.js';
import { edgeTable, triTable } from '../vendor/three/MarchingCubes.js';

const PAPER = 0xf5f1ea, CARD = 0xfbf6ee, WINE = 0xa3303f, SLATE = 0x55607a, ROSE = 0xe2a2aa, TAN = 0xd9b56b;
const P = (x, y, z) => new THREE.Vector3(x, z, y);          /* physics (x, y, z) -> three (x, y = up, z) */

/* ---------- marching cubes on a rectangular grid: field[(i * ny + j) * nz + k] at (x0 + i h, y0 + j h, z0 + k h) ---------- */
/* corners as in vendor/three/MarchingCubes.js (Bourke): bit b of the cube index is set when corner b is below the level */
const CORNER = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]];
const EDGE = [[0, 1], [1, 2], [3, 2], [0, 3], [4, 5], [5, 6], [7, 6], [4, 7], [0, 4], [1, 5], [2, 6], [3, 7]];
export function marching(field, nx, ny, nz, level, sign, x0, y0, z0, h) {
    const pos = [], nor = [], vx = new Float32Array(12 * 3), vn = new Float32Array(12 * 3);
    const at = (i, j, k) => sign * field[(i * ny + j) * nz + k];
    const grad = (i, j, k, out, o) => {         /* -grad of (sign * field): points from the crest out into lower values */
        const i0 = Math.max(0, i - 1), i1 = Math.min(nx - 1, i + 1), j0 = Math.max(0, j - 1), j1 = Math.min(ny - 1, j + 1), k0 = Math.max(0, k - 1), k1 = Math.min(nz - 1, k + 1);
        out[o] = -(at(i1, j, k) - at(i0, j, k)) / (i1 - i0); out[o + 1] = -(at(i, j1, k) - at(i, j0, k)) / (j1 - j0); out[o + 2] = -(at(i, j, k1) - at(i, j, k0)) / (k1 - k0);
    };
    const g0 = new Float32Array(3), g1 = new Float32Array(3), val = new Float32Array(8);
    for (let i = 0; i < nx - 1; i++) for (let j = 0; j < ny - 1; j++) for (let k = 0; k < nz - 1; k++) {
        let ci = 0;
        for (let c = 0; c < 8; c++) { const v = at(i + CORNER[c][0], j + CORNER[c][1], k + CORNER[c][2]); val[c] = v; if (v < level) ci |= 1 << c; }
        const bits = edgeTable[ci]; if (!bits) continue;
        for (let e = 0; e < 12; e++) {
            if (!(bits & (1 << e))) continue;
            const a = EDGE[e][0], b = EDGE[e][1], A = CORNER[a], B = CORNER[b];
            const t = (level - val[a]) / (val[b] - val[a]);
            vx[3 * e] = x0 + h * (i + A[0] + t * (B[0] - A[0])); vx[3 * e + 1] = y0 + h * (j + A[1] + t * (B[1] - A[1])); vx[3 * e + 2] = z0 + h * (k + A[2] + t * (B[2] - A[2]));
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
            for (const e of [e0, e1, e2]) { pos.push(vx[3 * e], vx[3 * e + 2], vx[3 * e + 1]); nor.push(vn[3 * e], vn[3 * e + 2], vn[3 * e + 1]); }   /* to three's axes */
        }
    }
    return { pos: new Float32Array(pos), nor: new Float32Array(nor) };
}

/* the colour of the height surface for a value v of Re psi (fraction of the first frame's peak): paper at 0, towards wine (v > 0)
   or slate (v < 0), full at |v| = 0.5. Exported so that the page's data panel can state the rule it checks pixels against. */
export function surfaceColour(v) {
    const a = Math.min(1, Math.abs(v) / 0.5), c = new THREE.Color(CARD), t = new THREE.Color(v > 0 ? WINE : SLATE);
    return c.lerp(t, a);
}

export function create(canvas, opt) {
    opt = opt || {};
    const r = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, alpha: false });
    r.setClearColor(PAPER); r.shadowMap.enabled = true; r.shadowMap.type = THREE.PCFSoftShadowMap; r.localClippingEnabled = true;
    r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = 1.15;
    const scene = new THREE.Scene(); scene.fog = new THREE.Fog(PAPER, 80, 160);
    const cam = new THREE.PerspectiveCamera(34, 1, 0.5, 400);
    scene.add(new THREE.HemisphereLight(0xfffaf3, 0xb8aea4, 1.6));
    const sun = new THREE.DirectionalLight(0xffffff, 2.2); sun.position.set(-18, 40, 22); sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -36, right: 36, top: 30, bottom: -30, near: 1, far: 140 });
    sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.06; scene.add(sun);
    const fill = new THREE.DirectionalLight(0xffeedd, 0.9); fill.position.set(-40, 5, 30); scene.add(fill);
    const FLOOR = -17.5;
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(72, 48), new THREE.MeshStandardMaterial({ color: CARD, roughness: 1 }));
    floor.rotation.x = -Math.PI / 2; floor.position.y = FLOOR; floor.receiveShadow = true; scene.add(floor);
    const grid = new THREE.GridHelper(72, 36, 0xd9d0c2, 0xe6dfd2); grid.scale.z = 48 / 72; grid.position.y = FLOOR + 0.01; scene.add(grid);
    const axisLine = new THREE.Line(new THREE.BufferGeometry().setFromPoints([P(-26, 0, 0), P(26, 0, 0)]), new THREE.LineDashedMaterial({ color: 0x8b8079, dashSize: 0.8, gapSize: 0.5 }));
    axisLine.computeLineDistances(); scene.add(axisLine);
    scene.add(new THREE.ArrowHelper(new THREE.Vector3(1, 0, 0), P(-27, 0, 0), 5, 0x1c1518, 1.1, 0.55));
    /* the cutaway removes the quarter y > 0 and z > 0 (physics): three's z > 0 and y > 0; an object is clipped only where both planes clip */
    const cut = [new THREE.Plane(new THREE.Vector3(0, 0, -1), 0), new THREE.Plane(new THREE.Vector3(0, -1, 0), 0)];
    const matSheet = (color) => new THREE.MeshPhysicalMaterial({ color, roughness: 0.32, metalness: 0, clearcoat: 0.6, clearcoatRoughness: 0.3, side: THREE.DoubleSide, clipIntersection: true });
    const crestMat = matSheet(WINE), troughMat = matSheet(SLATE);
    const crest = new THREE.Mesh(new THREE.BufferGeometry(), crestMat), trough = new THREE.Mesh(new THREE.BufferGeometry(), troughMat);
    for (const m of [crest, trough]) { m.castShadow = true; m.receiveShadow = true; m.frustumCulled = false; scene.add(m); }
    const surfMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.55, side: THREE.DoubleSide });
    const surf = new THREE.Mesh(new THREE.BufferGeometry(), surfMat); surf.castShadow = true; surf.receiveShadow = false;   /* no self-shadow: a lifted sheet shadowing itself shows moiré */ surf.frustumCulled = false; scene.add(surf);
    const barrier = new THREE.Group(); scene.add(barrier);
    const api = { yaw: -0.62, pitch: 0.42, dist: 64, mode: 'sheets', level: 0.25, height: 6, ok: true, renderer: r, THREE };

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
    api.setField = function (field, nx, ny, nz, x0, y0, z0, h, level) {
        if (level != null) api.level = level;
        const c = marching(field, nx, ny, nz, api.level, 1, x0, y0, z0, h), t = marching(field, nx, ny, nz, api.level, -1, x0, y0, z0, h);
        setGeo(crest, c); setGeo(trough, t);
        api.lastField = { field, nx, ny, nz, x0, y0, z0, h }; api.triangles = (c.pos.length + t.pos.length) / 9;
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
    api.clear = function () { setGeo(crest, { pos: new Float32Array(0), nor: new Float32Array(0) }); setGeo(trough, { pos: new Float32Array(0), nor: new Float32Array(0) }); api.lastField = null; };

    function applyMode() {
        const sheets = api.mode !== 'surface', clip = api.mode === 'cutaway' ? cut : [];
        crest.visible = trough.visible = sheets; surf.visible = !sheets;
        crestMat.clippingPlanes = troughMat.clippingPlanes = clip;
        barrier.children.forEach((m) => { m.material.clippingPlanes = clip; m.material.needsUpdate = true; });
        crestMat.needsUpdate = troughMat.needsUpdate = true;
    }
    api.setMode = function (m) { api.mode = m; applyMode(); };

    /* ---------- camera, rendering, projection ---------- */
    function place() {
        const cp = Math.cos(api.pitch), w = canvas.clientWidth || canvas.width, hh = canvas.clientHeight || canvas.height;
        cam.aspect = w / hh; cam.fov = cam.aspect < 1 ? 34 / Math.max(0.62, cam.aspect) : 34; cam.updateProjectionMatrix();
        cam.position.set(api.dist * cp * Math.sin(api.yaw), api.dist * Math.sin(api.pitch), api.dist * cp * Math.cos(api.yaw));
        cam.lookAt(1, -2, 0);
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
        return rc.ray.intersectPlane(new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), hit) ? [hit.x, hit.z, hit.y] : null;
    };
    api.readPixel = function (cx, cy) {   /* the drawn picture at CSS pixel (cx, cy): [r, g, b, a] */
        const gl = r.getContext(), dpr = r.getPixelRatio(), px = new Uint8Array(4);
        gl.readPixels(Math.round(cx * dpr), Math.round(gl.drawingBufferHeight - 1 - cy * dpr), 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
        return Array.from(px);
    };

    /* ---------- turning: press and drag ---------- */
    let drag = null;
    canvas.addEventListener('pointerdown', (e) => { if (opt.canTurn && !opt.canTurn()) return; drag = { x: e.clientX, y: e.clientY, yaw: api.yaw, pitch: api.pitch }; canvas.setPointerCapture(e.pointerId); });
    canvas.addEventListener('pointermove', (e) => { if (!drag) return; api.yaw = drag.yaw - (e.clientX - drag.x) * 0.008; api.pitch = Math.max(-0.2, Math.min(1.35, drag.pitch + (e.clientY - drag.y) * 0.008)); if (opt.onTurn) opt.onTurn(); });
    const up = () => { drag = null; }; canvas.addEventListener('pointerup', up); canvas.addEventListener('pointercancel', up);
    applyMode();
    return api;
}

window.Wave3D = { create, marching, surfaceColour };
window.dispatchEvent(new Event('wave3d-ready'));
