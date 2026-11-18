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
// colours as seen in photographs of a real pint (notes/realism/STATE.md, photos 1, 2, 4): near-black stout, ivory-cream head
const STOUT = 0x070302, CREAM = 0xf0e4c8;
// The stout's colour by transmission is Beer-Lambert, I = I0 exp(-alpha d), with the measured average beer spectrum
// (deLange, J. Am. Soc. Brew. Chem. 66(3) 143-150, 2008; formula in en.wikipedia.org/wiki/Standard_Reference_Method):
//   A(lambda) per cm = SRM/12.7 (0.018747 exp(-(lambda-430)/13.374) + 0.98226 exp(-(lambda-430)/80.514)),  alpha = ln10 A.
// SRM 40 (stouts are 35-70 SRM; Guinness's own value not found), read at 610, 550, 465 nm for red, green, blue:
// alpha = 76, 160, 462 per m. So 10 mm of stout passes 47 %, 20 %, 1 % (dark ruby), 70 mm passes 0.5 % of red only (black).
const SRM = 40, alphaAt = (l) => Math.log(10) * SRM / 12.7 * (0.018747 * Math.exp(-(l - 430) / 13.374) + 0.98226 * Math.exp(-(l - 430) / 80.514)) * 100;
const ALPHA = [alphaAt(610), alphaAt(550), alphaAt(465)];
// the light behind the glass that shines through the stout (linear RGB): a warm, dim room (drawing assumption)
const BACKLIGHT = [1.6, 1.15, 0.7];

function envTexture(renderer) {
  // a warm, dim room seen in the glass: dark wooden walls, a pale ceiling band and a row of warm lamps, and a window on one side,
  // painted on the inside of a sphere and prefiltered for reflections (drawing only; it gives the glass its highlights)
  const W = 512, H = 256, c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d');
  const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, '#3b2a20'); gr.addColorStop(0.3, '#5a4434'); gr.addColorStop(0.5, '#2a1d16'); gr.addColorStop(0.6, '#24170f'); gr.addColorStop(1, '#120b08');
  g.fillStyle = gr; g.fillRect(0, 0, W, H);
  for (let i = 0; i < 6; i++) { const x = (i + 0.5) * W / 6, y = H * 0.18, rg = g.createRadialGradient(x, y, 0, x, y, 18); rg.addColorStop(0, '#fff3d6'); rg.addColorStop(0.35, '#ffcf80'); rg.addColorStop(1, 'rgba(255,190,110,0)'); g.fillStyle = rg; g.fillRect(x - 20, y - 20, 40, 40); }
  // a tall window behind and to the side, and a narrower one in front: they make the narrow vertical highlights on a real glass
  g.fillStyle = "#f4f7fa"; g.fillRect(W * 0.70, H * 0.12, W * 0.06, H * 0.4); g.fillStyle = "#dfe7ec"; g.fillRect(W * 0.78, H * 0.12, W * 0.03, H * 0.4);
  g.fillStyle = "#fff6e8"; g.fillRect(W * 0.20, H * 0.15, W * 0.025, H * 0.34);
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const sc = new THREE.Scene(); sc.add(new THREE.Mesh(new THREE.SphereGeometry(10, 64, 32), new THREE.MeshBasicMaterial({ map: tex, side: THREE.BackSide })));
  const pm = new THREE.PMREMGenerator(renderer); const env = pm.fromScene(sc, 0.01).texture; pm.dispose();
  const bg = new THREE.CanvasTexture(c); bg.colorSpace = THREE.SRGBColorSpace; bg.mapping = THREE.EquirectangularReflectionMapping;
  return { env: env, bg: bg };
}

function foamTexture() {
  // the head's fine bubbles: pits of 0.2-1 mm as a bump map (drawing only)
  const N = 256, c = document.createElement('canvas'); c.width = N; c.height = N; const g = c.getContext('2d');
  g.fillStyle = '#808080'; g.fillRect(0, 0, N, N);
  let s = 7; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  for (let i = 0; i < 1400; i++) { const x = rnd() * N, y = rnd() * N, r = 0.6 + 2.2 * rnd() * rnd(); g.fillStyle = `rgba(40,40,40,${0.25 + 0.4 * rnd()})`; g.beginPath(); g.arc(x, y, r, 0, 2 * Math.PI); g.fill(); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(6, 3); return t;
}

class Pint3D {
  constructor(canvas, glass) {
    this.cv = canvas; this.G = glass;
    this.zRim = (glass.R.length - 1) * glass.dz;
    this.Rz = (z) => { const f = Math.max(0, Math.min(z, this.zRim - 1e-6)) / glass.dz, i = Math.min(Math.floor(f), glass.R.length - 2); return glass.R[i] + (f - i) * (glass.R[i + 1] - glass.R[i]); };
    const r = this.renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: false });
    r.setPixelRatio(Math.min(1.5, window.devicePixelRatio || 1)); r.outputColorSpace = THREE.SRGBColorSpace; r.toneMapping = THREE.AgXToneMapping; r.toneMappingExposure = 1.25;
    const s = this.scene = new THREE.Scene(); const E = envTexture(r); s.environment = E.env;
    s.background = E.bg; s.backgroundBlurriness = 0.35; s.backgroundIntensity = 0.9;   // the room behind, out of focus as in a photograph
    s.add(new THREE.HemisphereLight(0xfff0dc, 0x3a2a20, 0.9));
    const key = new THREE.DirectionalLight(0xffe2b8, 2.4); key.position.set(-0.25, 0.55, 0.35); s.add(key);   // a warm lamp above, in front
    const rim = new THREE.DirectionalLight(0xdfe8ff, 1.2); rim.position.set(0.35, 0.25, -0.45); s.add(rim);  // the window behind, to one side
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
    // the stout: a liquid surface (n = 1.34, so it reflects about 2 % head-on and more at grazing angles), near-black body
    const stoutTop = new THREE.MeshPhysicalMaterial({ color: STOUT, roughness: 0.05, metalness: 0, ior: 1.34, specularIntensity: 1, envMapIntensity: 1.4 });
    const stoutSide = new THREE.MeshPhysicalMaterial({ color: STOUT, roughness: 0.08, metalness: 0, ior: 1.34, side: THREE.DoubleSide, envMapIntensity: 1.2 });
    // the light from behind that crosses the stout near its edge (Beer-Lambert, ALPHA above), added on its side: see render()
    const ruby = new THREE.MeshBasicMaterial({ vertexColors: true, blending: THREE.AdditiveBlending, transparent: true, depthWrite: false, side: THREE.FrontSide, toneMapped: true });
    // the head: dense foam, matt with a soft sheen, ivory-cream, with fine bubble pits
    const foam = foamTexture();
    const cream = new THREE.MeshPhysicalMaterial({ color: CREAM, roughness: 0.92, sheen: 0.6, sheenRoughness: 0.8, sheenColor: 0xfff4de, bumpMap: foam, bumpScale: 0.6, side: THREE.DoubleSide });
    this.surf = new THREE.Mesh(grid(), stoutTop); this.headTop = new THREE.Mesh(grid(), cream);
    this.side = new THREE.Mesh(band(), stoutSide); this.headSide = new THREE.Mesh(band(), cream);
    this.rubySide = new THREE.Mesh(band(), ruby); this.rubySide.geometry.setAttribute('color', new THREE.BufferAttribute(new Float32Array((this.NZ + 1) * NTH * 3), 3));
    // texture coordinates: the head's top as a disc, the bands by angle and height
    { const uv = new Float32Array((1 + NR * NTH) * 2); uv[0] = uv[1] = 0.5;
      for (let ir = 1; ir <= NR; ir++) for (let it = 0; it < NTH; it++) { const j = 1 + (ir - 1) * NTH + it, a = 2 * Math.PI * it / NTH; uv[2 * j] = 0.5 + 0.5 * ir / NR * Math.cos(a); uv[2 * j + 1] = 0.5 + 0.5 * ir / NR * Math.sin(a); }
      this.headTop.geometry.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
      const ub = new Float32Array((this.NZ + 1) * NTH * 2); for (let q = 0; q <= this.NZ; q++) for (let it = 0; it < NTH; it++) { const j = q * NTH + it; ub[2 * j] = it / NTH; ub[2 * j + 1] = q / this.NZ * 0.15; }
      this.headSide.geometry.setAttribute('uv', new THREE.BufferAttribute(ub, 2)); }
    [this.surf, this.headTop, this.side, this.headSide, this.rubySide].forEach((m) => { m.frustumCulled = false; s.add(m); });
    this.rubySide.renderOrder = 3;
    // the glass: one solid body of revolution (outer wall 2.5 mm out, a rounded lip, the inner wall, a 14 mm solid foot), a clear
    // dielectric (n = 1.52): three.js refracts what lies behind it and reflects the room by Fresnel's law
    const prof = []; const W0 = 0.0025, FOOT = 0.014, Rout = (z) => this.Rz(Math.max(0.008, z)) + W0;
    prof.push(new THREE.Vector2(0, -FOOT), new THREE.Vector2(Rout(0) - 0.002, -FOOT), new THREE.Vector2(Rout(0), -FOOT + 0.002));
    for (let z = -FOOT + 0.004; z < this.zRim; z += 0.002) prof.push(new THREE.Vector2(Rout(z), z));
    prof.push(new THREE.Vector2(this.Rz(this.zRim) + W0, this.zRim), new THREE.Vector2(this.Rz(this.zRim) + 0.5 * W0, this.zRim + 0.0012), new THREE.Vector2(this.Rz(this.zRim), this.zRim));
    for (let z = this.zRim - 0.002; z > 0; z -= 0.002) prof.push(new THREE.Vector2(this.Rz(z), z));
    prof.push(new THREE.Vector2(this.Rz(0) - 0.003, 0), new THREE.Vector2(0, 0));
    prof.reverse();   // LatheGeometry faces outward when the profile runs from the top down on the outside
    const gm = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.02, metalness: 0, transmission: 1, ior: 1.52, thickness: 0.004,
      specularIntensity: 1, envMapIntensity: 1.3, side: THREE.DoubleSide });
    const gl = new THREE.Mesh(new THREE.LatheGeometry(prof, 128), gm); gl.renderOrder = 2; s.add(gl);
    // a varnished wooden bar top under the foot, so the glass has something to stand on, to refract and to reflect in (drawing only)
    { const N = 512, c = document.createElement('canvas'); c.width = N; c.height = N; const g = c.getContext('2d');
      g.fillStyle = '#3a1c0e'; g.fillRect(0, 0, N, N); let sd = 11; const rnd = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
      for (let i = 0; i < 160; i++) { const y = rnd() * N, a = 0.05 + 0.12 * rnd(); g.strokeStyle = rnd() < 0.5 ? `rgba(90,45,20,${a})` : `rgba(20,8,4,${a})`; g.lineWidth = 1 + 4 * rnd();
        g.beginPath(); g.moveTo(0, y); for (let x = 0; x <= N; x += 16) g.lineTo(x, y + 6 * Math.sin(x / 60 + i) + 3 * Math.sin(x / 13 + 2 * i)); g.stroke(); }
      const wood = new THREE.CanvasTexture(c); wood.colorSpace = THREE.SRGBColorSpace; wood.wrapS = wood.wrapT = THREE.RepeatWrapping; wood.repeat.set(2, 2);
      const top = new THREE.Mesh(new THREE.CircleGeometry(0.6, 64), new THREE.MeshPhysicalMaterial({ map: wood, roughness: 0.3, clearcoat: 0.8, clearcoatRoughness: 0.15 }));
      top.rotation.x = -Math.PI / 2; top.position.y = -FOOT - 0.0002; s.add(top); this.table = top; }
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
    // the light from behind that crosses the stout and leaves through its near side toward the camera: Beer-Lambert over the
    // chord of the horizontal circle of radius r along the view ray, d = 2 r cos(beta), beta the angle between the ray and the
    // wall's normal (the vertical part of the path and the refraction at the glass are left out: drawing approximation)
    const br = this.rubySide.geometry.attributes.position, bc = this.rubySide.geometry.attributes.color, C = this.camera.position;
    for (let it = 0; it < NTH; it++) {
      const th = 2 * Math.PI * it / NTH, c = Math.cos(th), s = Math.sin(th), H = edge[it][1];
      for (let q = 0; q <= NZ; q++) {
        const z1 = H * q / NZ, r1 = Rz(z1) - 0.0003, j = q * NTH + it, X = r1 * c, Z = -r1 * s;
        br.setXYZ(j, X, z1, Z);
        let vx = X - C.x, vz = Z - C.z; const vl = Math.hypot(vx, vz) || 1; vx /= vl; vz /= vl;
        const cb = -(c * vx + (-s) * vz), d = cb > 0 ? 2 * r1 * cb : 0, fade = Math.min(1, (H - z1) / 0.004);   // near side only
        const tf = cb > 0 ? 1 - (0.02 + 0.98 * Math.pow(1 - cb, 5)) : 0;                     // Fresnel (Schlick), out of the stout and the glass
        for (let ch = 0; ch < 3; ch++) bc.array[3 * j + ch] = BACKLIGHT[ch] * Math.exp(-ALPHA[ch] * d) * tf * tf * fade;
      }
    }
    br.needsUpdate = true; bc.needsUpdate = true;
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
