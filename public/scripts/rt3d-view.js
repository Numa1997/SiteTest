/* Fig. 15 (Resonant Tunnelling): the 3D view. three.js 0.170, vendored in vendor/three/.
   What it draws, and only that:
     - the meshed height sheet in Fig. 14's look: the plane z = 0 through the flight axis, lifted by a number the page hands
       over (Re psi or |psi|^2, over one fixed scale for the whole run), a smooth surface with a thin wire mesh, coloured in the
       house colours (paper at zero, wine on the crests, slate in the troughs);
     - the barriers as static, lit 3D solids at their true place in physical space (walls, discs, spherical shells), with the
       line where each meets the plane z = 0. They never move with the sheet: the sheet passes through them.
   Axes: physics x along the flight, y across, z up; on screen three's (x, y, z) = physics (x, z, y), so the sheet's height
   (the lifted value) runs along physics z, the same direction as the barriers' true height.
   Turning: press and drag on the canvas (never a mere pass of the pointer). Docs: docs/simulations/fig15-resonant-tunnelling.md. */
import * as THREE from '../vendor/three/three.module.min.js';

const PAPER = 0xf5f1ea, INK = 0x1c1518, GLASS = 0x8b8079;
export const ZERO = [0xfb, 0xf6, 0xee], CREST = [0xa3, 0x30, 0x3f], TROUGH = [0x55, 0x60, 0x7a];

/* the sheet's colour for v in [-1, 1]: card paper at 0, towards wine (v > 0) or slate (v < 0), full at |v| = 1, mixed in sRGB.
   The mix grows as sqrt|v| (since 25 November 2026; it was |v|), so a crest at a quarter of the run's largest value is already
   half coloured: most of a run lies well under its largest value and was drawn almost white. The height stays linear in v. */
export function colour(v) {
    v = Math.max(-1, Math.min(1, v)); const e = v >= 0 ? CREST : TROUGH, a = Math.sqrt(Math.abs(v));
    return [ZERO[0] + a * (e[0] - ZERO[0]), ZERO[1] + a * (e[1] - ZERO[1]), ZERO[2] + a * (e[2] - ZERO[2])];
}
/* the inverse used by the pixel check: white light scales the three linear components by one factor, which leaves the ratios of
   the sRGB components nearly unchanged. Towards wine g / r falls from 246/251 to 48/163; towards slate r / b falls from 251/238
   to 85/122. Each ratio is solved for |v|; a pixel with more blue against red than the paper has is on the slate side. */
export function colourV(px) {
    const r = px[0], g = px[1], b = px[2]; if (r <= 0 || b <= 0) return NaN;
    const Z = ZERO, C = CREST, T = TROUGH, q1 = g / r, q2 = r / b;
    const vw = (Z[1] - q1 * Z[0]) / ((Z[1] - C[1]) - q1 * (Z[0] - C[0]));
    const vs = (Z[0] - q2 * Z[2]) / ((Z[0] - T[0]) - q2 * (Z[2] - T[2]));
    return q2 < Z[0] / Z[2] ? -vs * Math.abs(vs) : vw * Math.abs(vw);   /* the mix a was sqrt|v|: undo it */
}

export function create(canvas, opt) {
    opt = opt || {};
    const r = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, alpha: false });
    r.setClearColor(PAPER); r.toneMapping = THREE.NoToneMapping;
    const scene = new THREE.Scene();
    const cam = new THREE.PerspectiveCamera(32, 1, 0.5, 600);
    const hemi = new THREE.HemisphereLight(0xffffff, 0x8a8a8a, 1.55); scene.add(hemi);
    const sun = new THREE.DirectionalLight(0xffffff, 1.9); sun.position.set(-20, 40, 26); scene.add(sun);   /* a level patch shows its own colour: (1.55 + 1.9 cos 35°) / π ≈ 1 */

    /* ---------- the sheet ---------- */
    const sheetMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.6, metalness: 0, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 });
    sheetMat.toneMapped = false;
    const sheet = new THREE.Mesh(new THREE.BufferGeometry(), sheetMat); sheet.frustumCulled = false; sheet.renderOrder = 1; scene.add(sheet);
    const wireMat = new THREE.LineBasicMaterial({ color: INK, transparent: true, opacity: 0.13 }); wireMat.toneMapped = false;
    const wire = new THREE.LineSegments(new THREE.BufferGeometry(), wireMat); wire.frustumCulled = false; wire.renderOrder = 1; scene.add(wire);
    const LUT = new Float32Array(1025 * 3);
    for (let q = 0; q <= 1024; q++) { const c = colour(q / 512 - 1), k = new THREE.Color(c[0] / 255, c[1] / 255, c[2] / 255).convertSRGBToLinear(); LUT[3 * q] = k.r; LUT[3 * q + 1] = k.g; LUT[3 * q + 2] = k.b; }

    /* ---------- the flight axis, under the sheet's left edge: where the packet comes from ---------- */
    const arrow = new THREE.ArrowHelper(new THREE.Vector3(1, 0, 0), new THREE.Vector3(-44, 0, 0), 10, INK, 1.8, 0.9); scene.add(arrow);   /* on the flight axis, in front of the sheet's left edge */

    /* ---------- the barriers: the potential energy V(x, y, z = 0) on the plane the sheet shows ----------
       The sheet is the plane z = 0. Up, in this picture, is energy, as in the textbook energy diagram (V(x) drawn as blocks, the
       packet's energy E as a level, the wave drawn on that level): every barrier is drawn as its cut through z = 0 (a wall: a strip
       across the whole plane; a disc of radius R: a strip of length 2R; a spherical shell: an annulus), raised to its potential
       energy V0 (plus the voltage's ramp) on the same energy scale, and the sheet's zero sits at the level E. Where the level E lies
       under a block's top the packet has too little energy to cross classically (tunnelling); where it lies above, it passes over.
       Before 25 November 2026 the barriers were glass solids in physical space, 1 a thick in a 64 a box: from the reading distance
       they looked like pairs of lines, and their height (physical z) shared the up direction with the sheet's lift (ψ). */
    const barrier = new THREE.Group(); scene.add(barrier);
    const api = { yaw: -0.72, pitch: 0.52, dist: 112, renderer: r, THREE, ok: true, base: 0 };
    const STONE = 0xa89f93, LEVEL = 0x7a1f2b;
    const blockMat = () => new THREE.MeshStandardMaterial({ color: STONE, roughness: 0.85, metalness: 0, transparent: true, opacity: 0.62, depthWrite: false, side: THREE.DoubleSide });
    const inkMat = (o) => new THREE.LineBasicMaterial({ color: INK, transparent: true, opacity: o });
    function clearGroup(gr) { while (gr.children.length) { const c = gr.children.pop(); c.traverse((o) => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); }); } }
    /* b: { shape: 'flat' | 'coin' | 'shell' (or generation 1's 'dflat' ... 'sshell'), size (R), D, S (spacing), centres, radii,
            V0, bias, ext: [first face, last face], E (the packet's mean energy), k (screen length per energy unit), x0, x1, w (sheet span) } */
    api.setBarriers = function (b) {
        clearGroup(barrier); if (!b) return;
        const kind = b.shape.replace(/^[ds](?=(flat|coin|shell)$)/, ''), flat = kind === 'flat', coin = kind === 'coin', shell = kind === 'shell';
        const two = b.shape[0] === 'd', k = b.k || 3, V0 = b.V0 == null ? 2 : b.V0, bias = b.bias || 0, ext = b.ext || [-1, 1];
        const x0 = b.x0 == null ? -32 : b.x0, x1 = b.x1 == null ? 32 : b.x1, w = b.w || 63;
        const vb = (x) => -bias * Math.min(1, Math.max(0, (x - ext[0]) / (ext[1] - ext[0])));   /* the voltage's ramp, as rt3d2.py's vbias */
        api.base = (b.E || 0) * k; sheet.position.y = wire.position.y = api.base; arrow.position.y = api.base;
        /* the floor: V = ramp only, a ribbon along the flight under the sheet (flat when there is no voltage) */
        const nf = 129, fx = new Float32Array(nf), fp = new Float32Array(nf * 2 * 3);
        for (let i = 0; i < nf; i++) fx[i] = x0 + (x1 - x0) * i / (nf - 1);
        for (let i = 0; i < nf; i++) for (let s = 0; s < 2; s++) { const q = 3 * (2 * i + s); fp[q] = fx[i]; fp[q + 1] = vb(fx[i]) * k; fp[q + 2] = (s ? 1 : -1) * w / 2; }
        const fi = []; for (let i = 0; i < nf - 1; i++) { const a = 2 * i; fi.push(a, a + 1, a + 2, a + 2, a + 1, a + 3); }
        const fg = new THREE.BufferGeometry(); fg.setAttribute('position', new THREE.BufferAttribute(fp, 3)); fg.setIndex(fi); fg.computeVertexNormals();
        const floor = new THREE.Mesh(fg, new THREE.MeshStandardMaterial({ color: STONE, roughness: 0.95, transparent: true, opacity: 0.22, depthWrite: false, side: THREE.DoubleSide }));
        floor.renderOrder = 0; barrier.add(floor);
        /* the level E: an outline of the sheet's rest plane, in wine */
        const lv = [[x0, -w / 2], [x1, -w / 2], [x1, w / 2], [x0, w / 2], [x0, -w / 2]].map((p) => new THREE.Vector3(p[0], api.base, p[1]));
        const level = new THREE.Line(new THREE.BufferGeometry().setFromPoints(lv), new THREE.LineDashedMaterial({ color: LEVEL, dashSize: 1.2, gapSize: 0.8 }));
        level.computeLineDistances(); level.renderOrder = 2; barrier.add(level);
        /* a block from the floor to V0 above it, over the footprint `shape` (a THREE.Shape in the plane, physics (x, y)) */
        const block = (shapeXY, xc) => {
            const g = new THREE.ExtrudeGeometry(shapeXY, { depth: V0 * k, bevelEnabled: false, curveSegments: 96 });
            g.rotateX(-Math.PI / 2);            /* the shape's (x, y) -> screen (x, -z): flip y so physics y maps to screen z */
            g.scale(1, 1, -1);
            g.translate(0, vb(xc) * k, 0);
            const m = new THREE.Mesh(g, blockMat()); m.renderOrder = 3; barrier.add(m);
            const e = new THREE.LineSegments(new THREE.EdgesGeometry(g, 30), inkMat(0.75)); e.renderOrder = 4; barrier.add(e);
        };
        const rect = (xa, xb, ya, yb) => { const sh = new THREE.Shape(); sh.moveTo(xa, ya); sh.lineTo(xb, ya); sh.lineTo(xb, yb); sh.lineTo(xa, yb); sh.closePath(); return sh; };
        if (flat || coin) {
            const xs = b.centres || (two ? [-b.S / 2, b.S / 2] : [-b.S / 2]), half = flat ? w / 2 : b.size;
            xs.forEach((xc) => block(rect(xc - b.D / 2, xc + b.D / 2, -half, half), xc));
        }
        if (shell) {
            const radii = b.radii || (two ? [b.size, b.size + b.S] : [b.size]);
            radii.forEach((Rc) => {
                const sh = new THREE.Shape(); sh.absarc(0, 0, Rc + b.D / 2, 0, 2 * Math.PI, false);
                const hole = new THREE.Path(); hole.absarc(0, 0, Rc - b.D / 2, 0, 2 * Math.PI, true); sh.holes.push(hole);
                block(sh, 0);                   /* a shell straddles the ramp; drawn on the ramp at its centre */
            });
        }
        api.barrier = b;
    };

    /* o: { nx, ny, x0, y0, h, H (heights, physics z, length nx * ny, index i * ny + j), T (colour 0 slate .. 0.5 paper .. 1 wine), every, key } */
    api.setSheet = function (o) {
        const nx = o.nx, ny = o.ny, N = nx * ny, h = o.h, H = o.H, T = o.T;
        let g = sheet.geometry;
        if (!g.attributes.position || g.userData.key !== o.key) {
            g.dispose(); g = new THREE.BufferGeometry(); g.userData = { key: o.key };
            const pos = new THREE.BufferAttribute(new Float32Array(N * 3), 3); pos.setUsage(THREE.DynamicDrawUsage);
            g.setAttribute('position', pos); g.setAttribute('normal', new THREE.BufferAttribute(new Float32Array(N * 3), 3)); g.setAttribute('color', new THREE.BufferAttribute(new Float32Array(N * 3), 3));
            g.attributes.normal.setUsage(THREE.DynamicDrawUsage); g.attributes.color.setUsage(THREE.DynamicDrawUsage);
            const idx = new Uint32Array((nx - 1) * (ny - 1) * 6); let k = 0;
            for (let i = 0; i < nx - 1; i++) for (let j = 0; j < ny - 1; j++) { const a = i * ny + j, bb = a + ny; idx[k++] = a; idx[k++] = a + 1; idx[k++] = bb; idx[k++] = bb; idx[k++] = a + 1; idx[k++] = bb + 1; }
            g.setIndex(new THREE.BufferAttribute(idx, 1)); sheet.geometry = g;
            const li = [], ev = o.every;
            for (let i = 0; i < nx; i += ev) for (let j = 0; j < ny - 1; j++) li.push(i * ny + j, i * ny + j + 1);
            for (let j = 0; j < ny; j += ev) for (let i = 0; i < nx - 1; i++) li.push(i * ny + j, (i + 1) * ny + j);
            const wg = new THREE.BufferGeometry(); wg.setAttribute('position', pos); wg.setIndex(li); wire.geometry.dispose(); wire.geometry = wg;
            for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++) { const q = i * ny + j; pos.array[3 * q] = o.x0 + i * h; pos.array[3 * q + 2] = o.y0 + j * h; }
        }
        const pos = g.attributes.position.array, nor = g.attributes.normal.array, col = g.attributes.color.array;
        for (let i = 0; i < nx; i++) {
            const i0 = i > 0 ? i - 1 : 0, i1 = i < nx - 1 ? i + 1 : nx - 1;
            for (let j = 0; j < ny; j++) {
                const q = i * ny + j, j0 = j > 0 ? j - 1 : 0, j1 = j < ny - 1 ? j + 1 : ny - 1;
                pos[3 * q + 1] = H[q];
                const hx = (H[i1 * ny + j] - H[i0 * ny + j]) / ((i1 - i0) * h), hy = (H[i * ny + j1] - H[i * ny + j0]) / ((j1 - j0) * h), m = 1 / Math.sqrt(1 + hx * hx + hy * hy);
                nor[3 * q] = -hx * m; nor[3 * q + 1] = m; nor[3 * q + 2] = -hy * m;
                const t = T[q], u = Math.round(1024 * (t < 0 ? 0 : t > 1 ? 1 : t)) * 3; col[3 * q] = LUT[u]; col[3 * q + 1] = LUT[u + 1]; col[3 * q + 2] = LUT[u + 2];
            }
        }
        g.attributes.position.needsUpdate = true; g.attributes.normal.needsUpdate = true; g.attributes.color.needsUpdate = true;
        if (!g.boundingSphere) g.computeBoundingSphere();
        api.last = o;
    };
    api.vertex = function (k) { const a = sheet.geometry.attributes.position; return a ? [a.array[3 * k], a.array[3 * k + 2], a.array[3 * k + 1]] : null; };   /* the drawn vertex k: physics (x, y) and its lift above the level E (the sheet's own height) */

    /* ---------- camera, rendering, picking ---------- */
    function place() {
        const cp = Math.cos(api.pitch), w = canvas.clientWidth || canvas.width, hh = canvas.clientHeight || canvas.height;
        cam.aspect = w / hh; cam.fov = cam.aspect < 1 ? 32 / Math.max(0.6, cam.aspect) : 32; cam.updateProjectionMatrix();
        const d = api.dist * (cam.aspect < 1.2 ? 1.18 / Math.max(0.75, cam.aspect) : 1);   /* a narrow screen stands back to see the whole sheet */
        cam.position.set(d * cp * Math.sin(api.yaw), d * Math.sin(api.pitch), d * cp * Math.cos(api.yaw));
        cam.lookAt(0, api.base * 0.5, 0);
    }
    api.resize = function (w, h, dpr) { r.setPixelRatio(dpr || 1); r.setSize(w, h, false); };
    api.render = function () { place(); r.render(scene, cam); };
    api.project = function (p) {   /* physics point -> CSS pixels on the canvas */
        place(); const v = new THREE.Vector3(p[0], p[2] + api.base, p[1]).project(cam), w = canvas.clientWidth, hh = canvas.clientHeight;
        return { x: (v.x + 1) / 2 * w, y: (1 - v.y) / 2 * hh, inFront: v.z < 1 };
    };
    api.pick = function (cx, cy) {  /* CSS pixel -> the physics point where its ray first meets the sheet */
        place(); const w = canvas.clientWidth, hh = canvas.clientHeight, rc = new THREE.Raycaster();
        rc.setFromCamera(new THREE.Vector2(cx / w * 2 - 1, 1 - cy / hh * 2), cam);
        const hits = rc.intersectObject(sheet, false); if (!hits.length) return null; const p = hits[0].point; return [p.x, p.z, p.y - api.base];
    };
    api.readPixel = function (cx, cy) {
        const gl = r.getContext(), dpr = r.getPixelRatio(), px = new Uint8Array(4);
        gl.readPixels(Math.round(cx * dpr), Math.round(gl.drawingBufferHeight - 1 - cy * dpr), 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
        return Array.from(px);
    };
    api.home = function () { api.yaw = -0.72; api.pitch = 0.52; };
    api.setSpan = function (L) { arrow.position.x = -L / 2 - 12; api.dist = 112 * Math.max(1, L / 77); };   /* the sheet's length along x: the arrow sits before it, the camera stands back to see it */

    let drag = null;
    canvas.addEventListener('pointerdown', (e) => { if (opt.canTurn && !opt.canTurn()) return; drag = { x: e.clientX, y: e.clientY, yaw: api.yaw, pitch: api.pitch }; canvas.setPointerCapture(e.pointerId); });
    canvas.addEventListener('pointermove', (e) => { if (!drag) return; api.yaw = drag.yaw - (e.clientX - drag.x) * 0.008; api.pitch = Math.max(0.05, Math.min(1.45, drag.pitch + (e.clientY - drag.y) * 0.008)); if (opt.onTurn) opt.onTurn(); });
    const up = () => { drag = null; }; canvas.addEventListener('pointerup', up); canvas.addEventListener('pointercancel', up);
    return api;
}

window.RT3DView = { create, colour, colourV, ZERO, CREST, TROUGH };
window.dispatchEvent(new Event('rt3d-view-ready'));
