/* Fig. 12: drawing the GPU solver's stout on the graphics chip (screen-space fluid rendering).
 *
 * The particles never leave the chip: each is drawn as a small sphere through the same pinhole camera as stout-view.js,
 * (1) its nearest depth into a depth image, (2) the depth image smoothed by a bilateral filter (it averages only depths
 * that are close, so the surface becomes smooth without blurring the stout into the air), (3) the thickness of stout along
 * each ray, the spheres' chords added up, (4) one pass that shades each pixel: the normal from the smoothed depth, one
 * light, and the colour of the light that crosses the thickness ℓ of stout, Beer–Lambert, T = e^{−κℓ}: ruby where thin,
 * black where thick. The head is DRAWN, not simulated: the top h_head of the stout (measured from the surface the solver's
 * column heights give, World.readProbes' surface) is painted cream. Steps after Green (NVIDIA GDC 2010) and the WebGPU code of
 * matsuoka-601 (Splash, WebGPU-Ocean, MIT licence), rewritten for this camera. The result is a canvas that StoutView.drawGlass
 * lays inside the glass. Nothing physical is computed here.
 */
(function (root) {
  'use strict';
  const CAM = /* wgsl */`
struct Cam {
  d: vec4f, r: vec4f, u: vec4f, cp: vec4f,          // the camera's axes and position (world: x along the road from the axle, y across, z up from the road)
  f: f32, cx: f32, cy: f32, W: f32,                  // focal length and centre in device px, canvas width
  H: f32, zG: f32, rd: f32, kappa: f32,              // canvas height, the glass floor's height, the drawn sphere radius, Beer–Lambert κ
  headH: f32, hsR: f32, hsN: f32, near: f32,         // head thickness, surface map half width and points, depth range
  far: f32, nLive: f32, thickScale: f32, p3: f32,
  L: vec4f, Hh: vec4f,                               // the light's direction, the half vector (light + eye)
};
@group(0) @binding(0) var<uniform> cam: Cam;
fn toScreen(w: vec3f) -> vec3f {
  let v = w - cam.cp.xyz; let dep = dot(v, cam.d.xyz);
  return vec3f(cam.cx + cam.f * dot(v, cam.r.xyz) / dep, cam.cy - cam.f * dot(v, cam.u.xyz) / dep, dep);
}
fn worldAt(X: f32, Y: f32, dep: f32) -> vec3f {
  return cam.cp.xyz + dep * (cam.d.xyz + ((X - cam.cx) / cam.f) * cam.r.xyz - ((Y - cam.cy) / cam.f) * cam.u.xyz);
}
struct VO { @builtin(position) pos: vec4f, @location(0) uv: vec2f, @location(1) dep: f32 };
`;
  const SPHERES = CAM + /* wgsl */`
@group(0) @binding(1) var<storage, read> pos: array<vec4f>;
@vertex fn vs(@builtin(vertex_index) vi: u32, @builtin(instance_index) ii: u32) -> VO {
  var c = array(vec2f(-1, -1), vec2f(1, -1), vec2f(-1, 1), vec2f(-1, 1), vec2f(1, -1), vec2f(1, 1));
  let p = pos[ii]; var o: VO;
  if (p.w < 0.0 || f32(ii) >= cam.nLive) { o.pos = vec4f(2.0, 2.0, 2.0, 1.0); o.uv = vec2f(0.0); o.dep = 0.0; return o; }
  let s = toScreen(vec3f(p.x, p.y, cam.zG + p.z)); let rp = cam.f * cam.rd / s.z;
  let X = s.x + c[vi].x * rp; let Y = s.y - c[vi].y * rp;
  o.pos = vec4f(X / cam.W * 2.0 - 1.0, 1.0 - Y / cam.H * 2.0, clamp((s.z - cam.near) / (cam.far - cam.near), 0.0, 1.0), 1.0);
  o.uv = c[vi]; o.dep = s.z; return o;
}
struct DO { @location(0) depth: f32, @builtin(frag_depth) fd: f32 };
@fragment fn fsDepth(i: VO) -> DO {
  let r2 = dot(i.uv, i.uv); if (r2 > 1.0) { discard; }
  let z = i.dep - cam.rd * sqrt(1.0 - r2); var o: DO; o.depth = z; o.fd = clamp((z - cam.near) / (cam.far - cam.near), 0.0, 1.0); return o;
}
@fragment fn fsThick(i: VO) -> @location(0) vec4f {
  let r2 = dot(i.uv, i.uv); if (r2 > 1.0) { discard; }
  return vec4f(cam.thickScale * 2.0 * cam.rd * sqrt(1.0 - r2), 0.0, 0.0, 1.0);
}
`;
  const FULL = CAM + /* wgsl */`
@vertex fn vsFull(@builtin(vertex_index) vi: u32) -> VO {
  var c = array(vec2f(-1, -1), vec2f(3, -1), vec2f(-1, 3)); var o: VO; o.pos = vec4f(c[vi], 0.0, 1.0); o.uv = c[vi]; o.dep = 0.0; return o;
}
`;
  // separable bilateral filter of the depth: Gaussian in screen distance (about one drawn particle across) and in depth
  // difference (a fraction of the particle radius), so steps between the stout and the air stay sharp
  const FILTER = FULL + /* wgsl */`
@group(0) @binding(1) var src: texture_2d<f32>;
@group(0) @binding(2) var<uniform> dir: vec4f;
@fragment fn fs(i: VO) -> @location(0) vec4f {
  let p = vec2i(i.pos.xy); let z0 = textureLoad(src, p, 0).r;
  if (z0 > 1e4) { return vec4f(z0, 0.0, 0.0, 1.0); }
  let rp = cam.f * cam.rd / z0; let n = i32(clamp(4.0 * rp, 1.0, 24.0)); let sig = max(1.0, 2.0 * rp);
  let sz = 1.5 * cam.rd; var s = 0.0; var w = 0.0;
  let dims = vec2i(textureDimensions(src));
  for (var k = -n; k <= n; k++) {
    let q = clamp(p + vec2i(dir.xy * f32(k)), vec2i(0), dims - 1);
    let z = textureLoad(src, q, 0).r; if (z > 1e4) { continue; }
    let dz = (z - z0) / sz; let wt = exp(-f32(k * k) / (2.0 * sig * sig) - dz * dz);
    s += wt * z; w += wt;
  }
  return vec4f(s / w, 0.0, 0.0, 1.0);
}
`;
  const SHADE = FULL + /* wgsl */`
@group(0) @binding(1) var depthT: texture_2d<f32>;
@group(0) @binding(2) var thickT: texture_2d<f32>;
@group(0) @binding(3) var<storage, read> hs: array<f32>;       // the surface's height (glass frame) on an hsN x hsN grid over [-hsR, hsR]^2
fn surf(x: f32, y: f32) -> f32 {
  let n = i32(cam.hsN); let g = (vec2f(x, y) + cam.hsR) / (2.0 * cam.hsR) * f32(n - 1);
  let i = clamp(i32(floor(g.x)), 0, n - 2); let j = clamp(i32(floor(g.y)), 0, n - 2); let t = clamp(g - vec2f(f32(i), f32(j)), vec2f(0.0), vec2f(1.0));
  let a = hs[i + n * j]; let b = hs[i + 1 + n * j]; let c = hs[i + n * (j + 1)]; let d = hs[i + 1 + n * (j + 1)];
  return mix(mix(a, b, t.x), mix(c, d, t.x), t.y);
}
fn P(p: vec2i) -> vec3f { let z = textureLoad(depthT, p, 0).r; return worldAt(f32(p.x) + 0.5, f32(p.y) + 0.5, z); }
@fragment fn fs(i: VO) -> @location(0) vec4f {
  let p = vec2i(i.pos.xy); let z = textureLoad(depthT, p, 0).r;
  if (z > 1e4) { return vec4f(0.0); }
  let dims = vec2i(textureDimensions(depthT));
  let c = P(p);
  // the normal from the neighbours on the side whose depth is closer (no normal across an edge)
  let zl = textureLoad(depthT, clamp(p - vec2i(1, 0), vec2i(0), dims - 1), 0).r; let zr = textureLoad(depthT, clamp(p + vec2i(1, 0), vec2i(0), dims - 1), 0).r;
  let zu = textureLoad(depthT, clamp(p - vec2i(0, 1), vec2i(0), dims - 1), 0).r; let zd = textureLoad(depthT, clamp(p + vec2i(0, 1), vec2i(0), dims - 1), 0).r;
  var ddx = P(clamp(p + vec2i(1, 0), vec2i(0), dims - 1)) - c; if (abs(zl - z) < abs(zr - z)) { ddx = c - P(clamp(p - vec2i(1, 0), vec2i(0), dims - 1)); }
  var ddy = P(clamp(p + vec2i(0, 1), vec2i(0), dims - 1)) - c; if (abs(zu - z) < abs(zd - z)) { ddy = c - P(clamp(p - vec2i(0, 1), vec2i(0), dims - 1)); }
  var n = normalize(cross(ddy, ddx)); if (dot(n, cam.cp.xyz - c) < 0.0) { n = -n; }
  let lam = max(0.0, dot(n, cam.L.xyz)); let spec = pow(max(0.0, dot(n, normalize(cam.Hh.xyz))), 48.0);
  let thick = textureLoad(thickT, p / 2, 0).r;   // the thickness image is drawn at half size
  let T = exp(-cam.kappa * thick);
  let dark = vec3f(14.0, 8.0, 7.0) / 255.0; let ruby = vec3f(96.0, 22.0, 16.0) / 255.0;
  var body = mix(dark, ruby, T) * (0.85 + 0.3 * lam) + vec3f(0.35) * spec;
  // the head: the top headH of the stout below the computed surface, drawn cream (lit as the CPU view lights its sheet)
  let zg = c.z - cam.zG; let top = surf(c.x, c.y);
  let headC = mix(vec3f(196.0, 178.0, 146.0) / 255.0, vec3f(236.0, 225.0, 201.0) / 255.0, min(1.0, 0.3 + 0.8 * lam));
  let hcol = mix(headC, vec3f(253.0, 250.0, 242.0) / 255.0, 0.45 * spec);
  let inHead = smoothstep(top - cam.headH - 0.0015, top - cam.headH + 0.0015, zg);
  let col = mix(body, hcol, inHead);
  return vec4f(col, 1.0);
}
`;

  function GpuView(fluid, canvas2d) {
    this.fluid = fluid; this.dev = fluid.device; this.main = canvas2d;
    this.cv = (typeof OffscreenCanvas !== 'undefined') ? new OffscreenCanvas(8, 8) : document.createElement('canvas');
    this.ctx = this.cv.getContext('webgpu');
    this.format = navigator.gpu.getPreferredCanvasFormat();
    this.ctx.configure({ device: this.dev, format: this.format, alphaMode: 'premultiplied' });
    this.rd = 0.0022;            // drawn sphere radius, m (particles are 2 mm apart)
    this.hsN = 48;               // the surface map for the head: 48 x 48 points
    this.headH = 0.012;
    const d = this.dev, mod = (c, l) => d.createShaderModule({ label: l, code: c });
    const M = { sph: mod(SPHERES, 'spheres'), filt: mod(FILTER, 'filter'), shade: mod(SHADE, 'shade') };
    this.camBuf = d.createBuffer({ size: 256, usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST });
    this.dirX = d.createBuffer({ size: 16, usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST }); d.queue.writeBuffer(this.dirX, 0, new Float32Array([1, 0, 0, 0]));
    this.dirY = d.createBuffer({ size: 16, usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST }); d.queue.writeBuffer(this.dirY, 0, new Float32Array([0, 1, 0, 0]));
    this.hsBuf = d.createBuffer({ size: 4 * this.hsN * this.hsN, usage: GPUBufferUsage.STORAGE | GPUBufferUsage.COPY_DST });
    this.pDepth = d.createRenderPipeline({ layout: 'auto', vertex: { module: M.sph, entryPoint: 'vs' }, fragment: { module: M.sph, entryPoint: 'fsDepth', targets: [{ format: 'r32float' }] },
      primitive: { topology: 'triangle-list' }, depthStencil: { format: 'depth32float', depthWriteEnabled: true, depthCompare: 'less' } });
    this.pThick = d.createRenderPipeline({ layout: 'auto', vertex: { module: M.sph, entryPoint: 'vs' }, fragment: { module: M.sph, entryPoint: 'fsThick', targets: [{ format: 'r16float', blend: { color: { operation: 'add', srcFactor: 'one', dstFactor: 'one' }, alpha: { operation: 'add', srcFactor: 'one', dstFactor: 'one' } } }] },
      primitive: { topology: 'triangle-list' } });
    this.pFilt = d.createRenderPipeline({ layout: 'auto', vertex: { module: M.filt, entryPoint: 'vsFull' }, fragment: { module: M.filt, entryPoint: 'fs', targets: [{ format: 'r32float' }] }, primitive: { topology: 'triangle-list' } });
    this.pShade = d.createRenderPipeline({ layout: 'auto', vertex: { module: M.shade, entryPoint: 'vsFull' }, fragment: { module: M.shade, entryPoint: 'fs', targets: [{ format: this.format }] }, primitive: { topology: 'triangle-list' } });
    this.W = 0; this.H = 0;
  }
  GpuView.prototype.resize = function (W, H) {
    if (W === this.W && H === this.H) return;
    const d = this.dev; this.W = W; this.H = H; this.cv.width = W; this.cv.height = H;
    const tex = (w, h, f, u) => d.createTexture({ size: [Math.max(1, w), Math.max(1, h)], format: f, usage: u || (GPUTextureUsage.RENDER_ATTACHMENT | GPUTextureUsage.TEXTURE_BINDING) });
    this.tDepth = tex(W, H, 'r32float'); this.tTmp = tex(W, H, 'r32float'); this.tZ = tex(W, H, 'depth32float', GPUTextureUsage.RENDER_ATTACHMENT);
    this.tThick = tex(Math.ceil(W / 2), Math.ceil(H / 2), 'r16float'); this.tZh = tex(Math.ceil(W / 2), Math.ceil(H / 2), 'depth32float', GPUTextureUsage.RENDER_ATTACHMENT);
    this.bgCache = {};
  };
  // the bind groups for the particle buffer `posBuf` (the solver's current set)
  GpuView.prototype.groups = function (posBuf, key) {
    if (this.bgCache[key]) return this.bgCache[key];
    const d = this.dev, B = (p, e) => d.createBindGroup({ layout: p.getBindGroupLayout(0), entries: e });
    const g = {
      depth: B(this.pDepth, [{ binding: 0, resource: { buffer: this.camBuf } }, { binding: 1, resource: { buffer: posBuf } }]),
      thick: B(this.pThick, [{ binding: 0, resource: { buffer: this.camBuf } }, { binding: 1, resource: { buffer: posBuf } }]),
      fx: B(this.pFilt, [{ binding: 0, resource: { buffer: this.camBuf } }, { binding: 1, resource: this.tDepth.createView() }, { binding: 2, resource: { buffer: this.dirX } }]),
      fy: B(this.pFilt, [{ binding: 0, resource: { buffer: this.camBuf } }, { binding: 1, resource: this.tTmp.createView() }, { binding: 2, resource: { buffer: this.dirY } }]),
      shade: B(this.pShade, [{ binding: 0, resource: { buffer: this.camBuf } }, { binding: 1, resource: this.tDepth.createView() }, { binding: 2, resource: this.tThick.createView() }, { binding: 3, resource: { buffer: this.hsBuf } }])
    };
    return (this.bgCache[key] = g);
  };
  // draw the stout for the camera `cam` (StoutView.camera, device px), with the glass's floor zG above the road; hs: the
  // surface heights (glass frame) on the hsN x hsN grid over [-hsR, hsR]^2
  GpuView.prototype.render = function (cam, W, H, zG, hs, hsR, light) {
    this.resize(W, H);
    const d = this.dev, f = this.fluid, posBuf = f.side === 0 ? f.B.posA : f.B.posB;
    const E = [-cam.d[0], -cam.d[1], -cam.d[2]], Hv = [light[0] + E[0], light[1] + E[1], light[2] + E[2]];
    const u = new Float32Array(64);
    u.set(cam.d, 0); u.set(cam.r, 4); u.set(cam.u, 8); u.set(cam.Cp, 12);
    // the spheres overlap: their chords add up to (sphere volume / volume per particle) times the true path; thickScale undoes it
    const sp = f.dx / f.ppcSide, thickScale = sp * sp * sp / (4 / 3 * Math.PI * this.rd * this.rd * this.rd);
    u.set([cam.f, cam.cx, cam.cy, W, H, zG, this.rd, Math.log(2) / 0.006, this.headH, hsR, this.hsN, 1.2, 3.6, f.slots, thickScale, 0], 16);
    u.set(light, 32); u.set(Hv, 36);
    d.queue.writeBuffer(this.camBuf, 0, u);
    d.queue.writeBuffer(this.hsBuf, 0, hs);
    const g = this.groups(posBuf, f.side), enc = d.createCommandEncoder();
    const color = (view, clear) => ({ view, clearValue: clear, loadOp: 'clear', storeOp: 'store' });
    let pass = enc.beginRenderPass({ colorAttachments: [color(this.tDepth.createView(), { r: 1e6, g: 0, b: 0, a: 1 })], depthStencilAttachment: { view: this.tZ.createView(), depthClearValue: 1, depthLoadOp: 'clear', depthStoreOp: 'store' } });
    pass.setPipeline(this.pDepth); pass.setBindGroup(0, g.depth); pass.draw(6, f.slots); pass.end();
    for (let k = 0; k < 4; k++) {
      pass = enc.beginRenderPass({ colorAttachments: [color(this.tTmp.createView(), { r: 1e6, g: 0, b: 0, a: 1 })] }); pass.setPipeline(this.pFilt); pass.setBindGroup(0, g.fx); pass.draw(3); pass.end();
      pass = enc.beginRenderPass({ colorAttachments: [color(this.tDepth.createView(), { r: 1e6, g: 0, b: 0, a: 1 })] }); pass.setPipeline(this.pFilt); pass.setBindGroup(0, g.fy); pass.draw(3); pass.end();
    }
    // the thickness at half size: the sphere pass again, additive, with the projection scaled by 1/2
    const uh = u.slice(); uh[16] = cam.f / 2; uh[17] = cam.cx / 2; uh[18] = cam.cy / 2; uh[19] = Math.ceil(W / 2); uh[20] = Math.ceil(H / 2);
    // the queue runs writes and submissions in order: the depth passes see u, the thickness pass uh, the shading u again
    d.queue.submit([enc.finish()]);
    d.queue.writeBuffer(this.camBuf, 0, uh);
    const enc2 = d.createCommandEncoder();
    pass = enc2.beginRenderPass({ colorAttachments: [color(this.tThick.createView(), { r: 0, g: 0, b: 0, a: 1 })] });
    pass.setPipeline(this.pThick); pass.setBindGroup(0, g.thick); pass.draw(6, f.slots); pass.end();
    d.queue.submit([enc2.finish()]);
    d.queue.writeBuffer(this.camBuf, 0, u);
    const enc3 = d.createCommandEncoder();
    pass = enc3.beginRenderPass({ colorAttachments: [color(this.ctx.getCurrentTexture().createView(), { r: 0, g: 0, b: 0, a: 0 })] });
    pass.setPipeline(this.pShade); pass.setBindGroup(0, g.shade); pass.draw(3); pass.end();
    d.queue.submit([enc3.finish()]);
    return this.cv;
  };
  root.StoutGpuView = GpuView;
})(typeof self !== 'undefined' ? self : this);
