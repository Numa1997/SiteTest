/* Fig. 12 and Fig. 16: a close-up of the pint in 3D, riding with the glass (three.js 0.170, vendored in vendor/three/).
   It draws the stored fields of one stored picture (StoutRide, stout-view2.js), and only those:
     - the stout's surface: the stored column heights, sampled on rings and angles exactly as StoutView2 samples them
       (StoutRide.atInward), as a lit, glossy 3D mesh; the outer ring meets the glass at the surface's own height there;
     - the stout's side against the glass, from the floor to that height;
     - the head of foam: a second surface at the stored height plus the stored thickness, and its band against the glass;
     - the drops of stout and the lumps of head in the air, where they were stored, as small spheres.
   The camera rides with the glass, so the view shows the stout as the glass sees it; the cart is drawn beside it in 2D.
   Nothing physical is computed here. The light, the gloss and the glass's tint are drawing only.
   Axes: physics (x along the road, y across, z up from the glass's inner floor) -> three (x, z, -y). */
import * as THREE from '../vendor/three/three.module.min.js';

const NR = 24, NTH = 96;
const STOUT = 0x0d0605, STOUT_EDGE = 0x120605, CREAM = 0xeee2c4, GLASSC = 0xdfe8ec;

function envTexture(renderer) {
  // a soft studio: a bright ceiling and a warm floor, as a gradient on the inside of a sphere, prefiltered for reflections
  const c = document.createElement('canvas'); c.width = 4; c.height = 256; const g = c.getContext('2d');
  const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, '#ffffff'); gr.addColorStop(0.45, '#d9d2c6'); gr.addColorStop(0.55, '#8e8478'); gr.addColorStop(1, '#3a312c');
  g.fillStyle = gr; g.fillRect(0, 0, 4, 256);
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const sc = new THREE.Scene(); sc.add(new THREE.Mesh(new THREE.SphereGeometry(10, 32, 16), new THREE.MeshBasicMaterial({ map: tex, side: THREE.BackSide })));
  const pm = new THREE.PMREMGenerator(renderer); const env = pm.fromScene(sc, 0.02).texture; pm.dispose(); return env;
}

class Pint3D {
  constructor(canvas, glass) {
    this.cv = canvas; this.G = glass;
    this.zRim = (glass.R.length - 1) * glass.dz;
    this.Rz = (z) => { const f = Math.max(0, Math.min(z, this.zRim - 1e-6)) / glass.dz, i = Math.min(Math.floor(f), glass.R.length - 2); return glass.R[i] + (f - i) * (glass.R[i + 1] - glass.R[i]); };
    const r = this.renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    r.setPixelRatio(Math.min(1.5, window.devicePixelRatio || 1)); r.outputColorSpace = THREE.SRGBColorSpace; r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = 1.05;
    const s = this.scene = new THREE.Scene(); s.environment = envTexture(r);
    s.add(new THREE.HemisphereLight(0xffffff, 0x5a4a40, 0.6));
    const key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(-0.25, 0.5, 0.35); s.add(key);
    const rim = new THREE.DirectionalLight(0xfff1dc, 1.0); rim.position.set(0.3, 0.25, -0.4); s.add(rim);
    this.camera = new THREE.PerspectiveCamera(22, 1, 0.01, 5);
    this.view(-24, 14);
    // the stout's surface and the head's top: NR rings x NTH angles + the centre
    const grid = () => { const g = new THREE.BufferGeometry(), nv = 1 + NR * NTH, idx = [];
      for (let it = 0; it < NTH; it++) { const a = 1 + it, b = 1 + (it + 1) % NTH; idx.push(0, b, a); }
      for (let ir = 0; ir < NR - 1; ir++) for (let it = 0; it < NTH; it++) { const a = 1 + ir * NTH + it, b = 1 + ir * NTH + (it + 1) % NTH, c = a + NTH, d = b + NTH; idx.push(a, b, d, a, d, c); }
      g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(nv * 3), 3)); g.setIndex(idx); return g; };
    // a band against the glass between two heights per angle (NZ rows), following the glass's radius at each height
    this.NZ = 24;
    const band = () => { const g = new THREE.BufferGeometry(), nv = (this.NZ + 1) * NTH, idx = [];
      for (let q = 0; q < this.NZ; q++) for (let it = 0; it < NTH; it++) { const a = q * NTH + it, b = q * NTH + (it + 1) % NTH, c = a + NTH, d = b + NTH; idx.push(a, d, b, a, c, d); }
      g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(nv * 3), 3)); g.setIndex(idx); return g; };
    const stoutTop = new THREE.MeshPhysicalMaterial({ color: STOUT, roughness: 0.12, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.08, envMapIntensity: 1.2 });
    const stoutSide = new THREE.MeshPhysicalMaterial({ color: STOUT_EDGE, roughness: 0.35, emissive: 0x2a0704, emissiveIntensity: 0.35, side: THREE.DoubleSide });
    const cream = new THREE.MeshStandardMaterial({ color: CREAM, roughness: 0.85, side: THREE.DoubleSide });
    this.surf = new THREE.Mesh(grid(), stoutTop); this.headTop = new THREE.Mesh(grid(), cream);
    this.side = new THREE.Mesh(band(), stoutSide); this.headSide = new THREE.Mesh(band(), cream);
    [this.surf, this.headTop, this.side, this.headSide].forEach((m) => { m.frustumCulled = false; s.add(m); });
    // the glass: inner and outer skins of the stored profile, tinted and nearly clear, drawn last
    const prof = (dr) => { const pts = []; for (let z = 0; z <= this.zRim + 1e-9; z += 0.002) pts.push(new THREE.Vector2(this.Rz(z) + dr, z)); return pts; };
    const outer = prof(0.0032); outer.unshift(new THREE.Vector2(0, -0.014), new THREE.Vector2(this.Rz(0) + 0.0032, -0.014));
    const gm = new THREE.MeshStandardMaterial({ color: GLASSC, roughness: 0.05, metalness: 0, transparent: true, opacity: 0.07, depthWrite: false, side: THREE.DoubleSide, envMapIntensity: 1.6 });
    const gOut = new THREE.Mesh(new THREE.LatheGeometry(outer, 96), gm); gOut.renderOrder = 2; s.add(gOut);
    const gIn = new THREE.Mesh(new THREE.LatheGeometry(prof(0), 96), gm); gIn.renderOrder = 2; s.add(gIn);
    // drops of stout and lumps of head in the air
    this.MAXD = 4096; this.MAXL = 512;
    this.drops = new THREE.InstancedMesh(new THREE.SphereGeometry(1, 8, 6), stoutTop, this.MAXD); this.drops.count = 0; this.drops.frustumCulled = false; s.add(this.drops);
    this.lumps = new THREE.InstancedMesh(new THREE.SphereGeometry(1, 10, 8), cream, this.MAXL); this.lumps.count = 0; this.lumps.frustumCulled = false; s.add(this.lumps);
    this.m4 = new THREE.Matrix4();
  }
  view(azimDeg, elevDeg) {   // the camera on a circle about the glass's axis, looking at its middle
    const a = azimDeg * Math.PI / 180, e = elevDeg * Math.PI / 180, d = 0.56, c = new THREE.Vector3(0, 0.095, 0);
    this.camera.position.set(c.x + d * Math.cos(e) * Math.cos(a), c.y + d * Math.sin(e), c.z - d * Math.cos(e) * Math.sin(a)); this.camera.lookAt(c);
  }
  size() {
    const w = this.cv.clientWidth, h = this.cv.clientHeight; if (w < 2 || h < 2) return;
    this.renderer.setSize(w, h, false); this.camera.aspect = w / h; this.camera.updateProjectionMatrix(); this.drawn = null;
  }
  setFrame(ride, k) { this.ride = ride; this.k = Math.max(0, Math.min(ride.frames - 1, k)); }
  // draws only when the stored picture or the size changed; times its two parts (geometry in JavaScript, the draw call) in this.stats
  render() {
    const ride = this.ride; if (!ride || (this.drawn && this.drawn[0] === ride && this.drawn[1] === this.k)) return;
    this.drawn = [ride, this.k]; const t0 = performance.now();
    const k = this.k, Rz = this.Rz, zRim = this.zRim, D = ride.D;
    // rings and angles, as StoutView2: the outer ring is the wall at the surface's own height in that direction
    const edge = [];
    for (let it = 0; it < NTH; it++) {
      const th = 2 * Math.PI * it / NTH; let v = ride.atInward(k, Rz(ride.fill), th);
      const r = Rz(Math.min(v[0], zRim)) - 0.0004; v = ride.atInward(k, r, th); edge.push([r, v[0], v[1]]);
    }
    const ps = this.surf.geometry.attributes.position, ph = this.headTop.geometry.attributes.position;
    const c0 = ride.atInward(k, 0, 0); ps.setXYZ(0, 0, c0[0], 0); ph.setXYZ(0, 0, c0[0] + c0[1], 0);
    for (let ir = 1; ir <= NR; ir++) for (let it = 0; it < NTH; it++) {
      const th = 2 * Math.PI * it / NTH, rr = edge[it][0] * ir / NR, v = ir === NR ? [edge[it][1], edge[it][2]] : ride.atInward(k, rr, th), j = 1 + (ir - 1) * NTH + it;
      const x = rr * Math.cos(th), y = rr * Math.sin(th); ps.setXYZ(j, x, v[0], -y); ph.setXYZ(j, x, v[0] + v[1], -y);
    }
    // the stout's side from the floor to the surface, and the head's band from the surface to its top, against the glass
    const bs = this.side.geometry.attributes.position, bh = this.headSide.geometry.attributes.position, NZ = this.NZ;
    for (let it = 0; it < NTH; it++) {
      const th = 2 * Math.PI * it / NTH, c = Math.cos(th), s = Math.sin(th), H = edge[it][1], F = edge[it][2];
      for (let q = 0; q <= NZ; q++) {
        const z1 = H * q / NZ, r1 = Rz(z1) - 0.0004, z2 = H + F * q / NZ, r2 = Rz(z2) - 0.0004, j = q * NTH + it;
        bs.setXYZ(j, r1 * c, z1, -r1 * s); bh.setXYZ(j, r2 * c, z2, -r2 * s);
      }
    }
    [ps, ph, bs, bh].forEach((a) => { a.needsUpdate = true; });
    [this.surf, this.headTop, this.side, this.headSide].forEach((m) => m.geometry.computeVertexNormals());
    // drops (radius 0.8 mm: about the volume of one particle, 0.43 mm^3, drawn larger to be seen) and lumps (their stored volume)
    const qd = D.qd, d0 = ride.dOff[k], nd = Math.min(this.MAXD, ride.dOff[k + 1] - d0);
    for (let q = 0; q < nd; q++) { const o = 3 * (d0 + q); this.m4.makeScale(0.0008, 0.0008, 0.0008).setPosition(ride.drops[o] * qd, ride.drops[o + 2] * qd, -ride.drops[o + 1] * qd); this.drops.setMatrixAt(q, this.m4); }
    this.drops.count = nd; this.drops.instanceMatrix.needsUpdate = true;
    const l0 = ride.lOff[k], nl = Math.min(this.MAXL, ride.lOff[k + 1] - l0);
    for (let q = 0; q < nl; q++) { const o = 4 * (l0 + q), vol = ride.lumps[o + 3] * D.qv, rad = Math.max(0.0008, Math.cbrt(3 * vol / (4 * Math.PI)));
      this.m4.makeScale(rad, rad, rad).setPosition(ride.lumps[o] * qd, ride.lumps[o + 2] * qd, -ride.lumps[o + 1] * qd); this.lumps.setMatrixAt(q, this.m4); }
    this.lumps.count = nl; this.lumps.instanceMatrix.needsUpdate = true;
    const t1 = performance.now(); this.renderer.render(this.scene, this.camera); const t2 = performance.now();
    const S = this.stats || (this.stats = { n: 0, js: 0, gl: 0 }); S.n++; S.js += t1 - t0; S.gl += t2 - t1; Pint3D.last = this;
  }
}
window.Pint3D = Pint3D;
window.dispatchEvent(new Event('pint3d-ready'));
