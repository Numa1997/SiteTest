/* Fig. 16: the four-wheel cart and the road in 3D, physically based materials (three.js 0.170), for the realistic view.
   Every size is Cart16View's (cart16-view.js, G, which takes the wheelbase, wheel radius and hinge depth from the ride's stored
   cart); every motion is the stored pose the player hands over (axle heights, the deck's centre height and pitch, the wheels'
   rolling angle -x/R_w) and the stored road z_r(x). Nothing physical is computed here; the parts' look is drawing only.
   Axes: physics (x along the road, y across, z up) -> three (x, z, -y). The deck's frame: a point (x, y, z) fixed to the deck,
   z up from the deck's underside at its middle, maps to (x cos p - z sin p, y, z_c + x sin p + z cos p), p the stored pitch. */
import * as THREE from '../vendor/three/three.module.min.js';

const V = (x, y, z) => new THREE.Vector3(x, z, -y);              // physics -> three

function noiseTexture(base, spread, seed, n, grain) {
  const N = 256, c = document.createElement('canvas'); c.width = N; c.height = N; const g = c.getContext('2d');
  g.fillStyle = base; g.fillRect(0, 0, N, N); let s = seed; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  for (let i = 0; i < n; i++) { const v = Math.round(spread * (rnd() - 0.5)); g.fillStyle = `rgba(${128 + v},${128 + v},${128 + v},0.18)`; g.fillRect(rnd() * N, rnd() * N, grain * (0.5 + rnd()), grain * (0.5 + rnd())); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; return t;
}

const M = {
  alu: () => new THREE.MeshPhysicalMaterial({ color: 0xc8ccd2, metalness: 1, roughness: 0.32 }),                 // brushed aluminium
  anod: () => new THREE.MeshPhysicalMaterial({ color: 0x2b2c30, metalness: 0.5, roughness: 0.45 }),            // black anodised
  steel: () => new THREE.MeshPhysicalMaterial({ color: 0xd9dde2, metalness: 1, roughness: 0.18 }),               // spring steel, chromed rod
  rubber: () => new THREE.MeshPhysicalMaterial({ color: 0x18181a, metalness: 0, roughness: 0.88 }),             // tyre
  coil: () => new THREE.MeshPhysicalMaterial({ color: 0x6e1b25, metalness: 0.35, roughness: 0.4 }),             // the voice-coil actuator's can
  brass: () => new THREE.MeshPhysicalMaterial({ color: 0xc7a35e, metalness: 1, roughness: 0.3 }),               // load cell, pins
  plastic: () => new THREE.MeshPhysicalMaterial({ color: 0x1f2124, metalness: 0, roughness: 0.55 }),            // boxes
  valve: () => new THREE.MeshPhysicalMaterial({ color: 0xd8b25a, metalness: 1, roughness: 0.25 }),
};

// a cylinder (radius r) whose axis runs from a to b (three vectors)
function rod(mesh, a, b) {
  const d = new THREE.Vector3().subVectors(b, a), L = d.length() || 1e-6;
  mesh.position.copy(a).addScaledVector(d, 0.5); mesh.scale.set(1, L, 1);
  mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.multiplyScalar(1 / L));
}

export class Cart3D {
  constructor(G) {
    this.G = G; const g = this.group = new THREE.Group();
    const mats = this.m = Object.fromEntries(Object.entries(M).map(([k, f]) => [k, f()]));
    // the deck and what is fixed to it (deck frame, see above)
    const deck = this.deck = new THREE.Group(); g.add(deck);
    const box = (x0, x1, y0, y1, z0, z1, mat, parent) => { const m = new THREE.Mesh(new THREE.BoxGeometry(x1 - x0, z1 - z0, y1 - y0), mat); m.position.copy(V((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)); (parent || deck).add(m); return m; };
    box(-G.deckL / 2, G.deckL / 2, -G.deckW / 2, G.deckW / 2, 0, G.deckT, mats.alu);                                   // the deck plate
    box(-0.07, 0.07, -0.038, 0.038, -0.034, -0.002, mats.plastic);                                                     // the battery
    box(-0.146, -0.078, -0.040, 0.040, G.deckT, G.deckT + 0.022, mats.anod);                                           // the controller
    for (let f = 0; f < 6; f++) box(-0.142, -0.082, -0.034 + f * 0.0125, -0.030 + f * 0.0125, G.deckT + 0.022, G.deckT + 0.030, mats.alu);   // its cooling fins
    box(0.232, 0.262, -0.022, 0.022, G.deckT + 0.020, G.deckT + 0.042, mats.plastic);                                 // the road scanner
    { const b = new THREE.Mesh(new THREE.CylinderGeometry(0.0035, 0.0035, 1, 12), mats.alu); deck.add(b); rod(b, V(G.deckL / 2 - 0.004, 0, G.deckT + 0.004), V(0.235, 0, G.deckT + 0.030)); }
    box(0.054, 0.070, 0.022, 0.038, G.deckT, G.deckT + 0.005, mats.coil);                                              // the IMU
    const zSeat = this.zSeat = G.deckT + 0.004;                                                                          // the seat plate and clamp ring
    { const seat = new THREE.Mesh(new THREE.CylinderGeometry(0.050, 0.050, zSeat - G.deckT, 48), mats.anod); seat.position.copy(V(0, 0, (G.deckT + zSeat) / 2)); deck.add(seat);
      const ring = new THREE.Mesh(new THREE.TorusGeometry(0.0395, 0.0028, 12, 64), mats.coil); ring.rotation.x = Math.PI / 2; ring.position.copy(V(0, 0, zSeat + 0.011)); deck.add(ring);
      for (let q = 0; q < 3; q++) { const a = q * 2.094 + 0.6, bolt = new THREE.Mesh(new THREE.CylinderGeometry(0.003, 0.003, 0.014, 10), mats.brass); bolt.position.copy(V(0.043 * Math.cos(a), 0.043 * Math.sin(a), zSeat + 0.007)); deck.add(bolt); } }
    this.mount = new THREE.Group(); this.mount.position.copy(V(0, 0, zSeat)); deck.add(this.mount);   // the glass's foot stands here
    // the four corners: hanger and tower on the deck, swing arm, strut (damper, rod, coil spring, voice coil, load cell), wheel
    this.corners = [];
    for (const sx of [1, -1]) for (const side of [1, -1]) {
      const xa = sx * G.wb / 2, ya = side * G.yArm, yt = ya - side * 0.019, c = { sx, side, xa, ya };
      box(xa + G.armL - 0.012, xa + G.armL + 0.012, ya - 0.007, ya + 0.007, -G.pivDrop - 0.008, 0, mats.anod);       // hanger
      box(xa + 0.018, xa + 0.042, yt - 0.006, yt + 0.006, G.deckT, G.deckT + G.towerH, mats.anod);                    // tower
      const cyl = (r, mat) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 1, 20), mat); g.add(m); return m; };
      c.arm = cyl(0.0055, mats.alu); c.axle = cyl(0.004, mats.steel); c.body = cyl(0.0075, mats.anod); c.rod = cyl(0.0025, mats.steel);
      c.vc = cyl(0.013, mats.coil); c.cell = cyl(0.009, mats.brass); c.pin = cyl(0.003, mats.brass);
      // the coil spring: 7 turns of 1.6 mm wire on a 12 mm radius, built along +y with unit length and stretched to the strut
      { const pts = []; for (let q = 0; q <= 7 * 32; q++) { const t = q / (7 * 32), a = 2 * Math.PI * 7 * t; pts.push(new THREE.Vector3(0.012 * Math.cos(a), t - 0.5, 0.012 * Math.sin(a))); }
        c.spring = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 7 * 32, 0.0016, 8, false), mats.steel); g.add(c.spring); }
      // the wheel: a tyre (torus) on a rim with five spokes and a hub; one brass valve, so a whole turn is the only repeat
      const w = c.wheel = new THREE.Group(); g.add(w);
      const R = G.Rw, tyre = new THREE.Mesh(new THREE.TorusGeometry(R - 0.008, 0.008, 16, 64), mats.rubber); w.add(tyre);
      const rim = new THREE.Mesh(new THREE.CylinderGeometry(R - 0.014, R - 0.014, 2 * G.hw - 0.004, 48, 1, true), mats.alu); rim.rotation.x = Math.PI / 2; w.add(rim);
      for (let k = 0; k < 5; k++) { const sp = new THREE.Mesh(new THREE.BoxGeometry(R - 0.016, 0.005, 0.004), mats.alu); const a = k * 2 * Math.PI / 5; sp.position.set(0.5 * (R - 0.016) * Math.cos(a), 0.5 * (R - 0.016) * Math.sin(a), side * 0.004); sp.rotation.z = a; w.add(sp); }
      const hub = new THREE.Mesh(new THREE.CylinderGeometry(sx < 0 ? 0.018 : 0.008, sx < 0 ? 0.018 : 0.008, 2 * G.hw, 24), sx < 0 ? mats.coil : mats.anod); hub.rotation.x = Math.PI / 2; w.add(hub);   // rear: hub motor
      const valve = new THREE.Mesh(new THREE.CylinderGeometry(0.0018, 0.0018, 0.006, 8), mats.valve); valve.position.set(R - 0.017, 0, side * 0.006); valve.rotation.z = Math.PI / 2; w.add(valve);
      this.corners.push(c);
    }
    // the road: an asphalt ribbon 0.30 m wide on the stored profile z_r, with pavement either side; its texture scrolls with x
    const NX = 240; this.NX = NX; this.span = 0.9;
    const strip = (y0, y1, tex, rough, rep) => { const geo = new THREE.PlaneGeometry(1, 1, NX - 1, 1), m = new THREE.Mesh(geo, new THREE.MeshPhysicalMaterial({ map: tex, roughness: rough, metalness: 0 }));
      m.userData = { y0, y1, rep }; m.frustumCulled = false; g.add(m); return m; };
    this.asphalt = strip(-0.15, 0.15, noiseTexture('#3b3a39', 120, 3, 9000, 2.2), 0.92, 6);
    this.paveN = strip(0.15, 0.6, noiseTexture('#9b968e', 60, 5, 6000, 3), 0.85, 3);
    this.paveF = strip(-0.6, -0.15, noiseTexture('#9b968e', 60, 9, 6000, 3), 0.85, 3);
    this.line = strip(0.135, 0.145, noiseTexture('#e9e6dc', 20, 13, 500, 2), 0.6, 1);
  }
  // pose as Cart16View.pose: zwF, zwR (axle heights), zc (deck), pitch, wheelAng; road(x) = z_r at x relative to the cart; x the cart
  update(pose, road, x) {
    const G = this.G, cp = Math.cos(pose.pitch), sp = Math.sin(pose.pitch);
    const T = (p) => V(p[0] * cp - p[2] * sp, p[1], pose.zc + p[0] * sp + p[2] * cp);
    this.deck.position.set(0, pose.zc, 0); this.deck.rotation.set(0, 0, pose.pitch);
    for (const c of this.corners) {
      const zw = c.sx > 0 ? pose.zwF : pose.zwR, ax = V(c.xa, c.ya, zw);
      const piv = T([c.xa + G.armL, c.ya, -G.pivDrop]), pv = new THREE.Vector3(piv.x, piv.y, piv.z);
      rod(c.arm, pv, ax); rod(c.axle, ax, V(c.xa, c.side * (G.yw - G.hw), zw));
      const pivP = [piv.x, -piv.z, piv.y];
      const lo = V(c.xa + 0.014 + (pivP[0] - c.xa) * 0.12, c.ya, zw + 0.012 + (pivP[2] - zw) * 0.12), hi = T([c.xa + 0.030, c.ya, G.deckT + G.towerH - 0.006]);
      const L = (t) => new THREE.Vector3().lerpVectors(lo, hi, t);
      rod(c.body, L(0), L(0.46)); rod(c.rod, L(0.46), L(0.74)); rod(c.vc, L(0.72), L(0.90)); rod(c.cell, L(0.90), L(0.97));
      rod(c.pin, T([c.xa + 0.030, c.ya - c.side * 0.019, G.deckT + G.towerH - 0.006]), hi);
      rod(c.spring, L(0.06), L(0.70));
      c.wheel.position.copy(V(c.xa, c.side * G.yw, zw)); c.wheel.rotation.set(0, 0, pose.wheelAng);
    }
    // the road under the cart: x from -span to +span about the cart, heights z_r, texture coordinates fixed to the road (x + cart x)
    for (const m of [this.asphalt, this.paveN, this.paveF, this.line]) {
      const P = m.geometry.attributes.position, U = m.geometry.attributes.uv, { y0, y1, rep } = m.userData;
      for (let i = 0; i < this.NX; i++) {
        const xr = -this.span + 2 * this.span * i / (this.NX - 1), z = road(xr) - 0.0005;
        for (const [row, y] of [[0, y1], [1, y0]]) { const j = row * this.NX + i; P.setXYZ(j, xr, z, -y); U.setXY(j, (xr + x) * rep, row * (y1 - y0) * rep); }
      }
      P.needsUpdate = true; U.needsUpdate = true; m.geometry.computeVertexNormals();
    }
  }
}
