/* VolumeView: draws a stored 3D cloud (a cube of n^3 uint8 levels) as coloured fog by ray marching in WebGL2, with a sphere
   drawn as a glass shell, seen by a camera the reader turns by dragging. Used by Fig. 14 (docs/simulations/fig14-schrodinger-sphere.md).
   The picture and the store are tied: expected(x, y) repeats the shader's sums on the CPU from the same stored levels, so the
   data panel can compare a screen pixel with the colour the stored cloud must give there; pick(x, y) returns the stored cell of
   highest level along the ray under a point.
   Geometry: the cube spans [-1, 1]^3 in view units (one view unit = L/2 of the physics box); x to the right, y up, z towards
   the reader at the starting view. Density shown d = (q / 255)^2, the stored level squared (the level is the root-mean-square
   |psi| of the cell in units of the first frame's peak cell, so d is the cell's mean probability density in those units).
   opt.offset shifts the cube's texture by a fraction of its side: Fig. 14's cells of 2 grid points are centred 0.25 a off the
   cell centres a cube from -L/2 to L/2 would have, so it passes 0.25/64. */
(function () {
    'use strict';
    var STEPS = 192, KAPPA = 30.0;                       /* march steps through the cube; opacity per unit density and view length */
    var PAPER = [245 / 255, 241 / 255, 234 / 255], WINE = [122 / 255, 31 / 255, 43 / 255], DEEP = [77 / 255, 15 / 255, 24 / 255];
    var VS = '#version 300 es\nin vec2 p; out vec2 uv; void main(){ uv = p; gl_Position = vec4(p, 0.0, 1.0); }';
    var FS = '#version 300 es\nprecision highp float; precision highp sampler3D;\n' +
        'in vec2 uv; out vec4 o; uniform sampler3D vol; uniform mat3 rot; uniform float dist, fov, aspect, sph, kappa, has; uniform vec3 paper, wine, deep; uniform float off;\n' +
        'const int STEPS = ' + STEPS + ';\n' +
        'bool box(vec3 ro, vec3 rd, out float t0, out float t1){ vec3 a = (-1.0 - ro) / rd, b = (1.0 - ro) / rd; vec3 lo = min(a, b), hi = max(a, b); t0 = max(max(lo.x, lo.y), lo.z); t1 = min(min(hi.x, hi.y), hi.z); return t1 > max(t0, 0.0); }\n' +
        'void main(){\n' +
        '  vec3 ro = rot * vec3(0.0, 0.0, dist); vec3 rd = normalize(rot * vec3(uv.x * aspect * fov, uv.y * fov, -1.0));\n' +
        '  vec3 col = vec3(0.0); float T = 1.0; float t0, t1;\n' +
        '  /* the sphere: entry and exit of the ray */\n' +
        '  float bq = dot(ro, rd), cq = dot(ro, ro) - sph * sph, disc = bq * bq - cq; float s0 = 1e9, s1 = 1e9; if (disc > 0.0) { s0 = -bq - sqrt(disc); s1 = -bq + sqrt(disc); }\n' +
        '  bool hit0 = s0 > 0.0 && s0 < 1e8, hit1 = s1 > 0.0 && s1 < 1e8;\n' +
        '  if (has > 0.5 && box(ro, rd, t0, t1)) {\n' +
        '    t0 = max(t0, 0.0); float dt = (t1 - t0) / float(STEPS);\n' +
        '    for (int i = 0; i < STEPS; i++) {\n' +
        '      float t = t0 + (float(i) + 0.5) * dt;\n' +
        '      if (hit0 && t >= s0 && t - dt < s0) { float f = abs(dot(normalize(ro + rd * s0), rd)); float a = 0.10 + 0.30 * pow(1.0 - f, 3.0); col += T * a * vec3(0.11, 0.08, 0.09); T *= 1.0 - a; hit0 = false; }\n' +
        '      if (hit1 && t >= s1 && t - dt < s1) { float f = abs(dot(normalize(ro + rd * s1), rd)); float a = 0.05 + 0.20 * pow(1.0 - f, 3.0); col += T * a * vec3(0.11, 0.08, 0.09); T *= 1.0 - a; hit1 = false; }\n' +
        '      vec3 pos = ro + rd * t; float q = texture(vol, pos * 0.5 + 0.5 - off).r; float d = q * q;\n' +
        '      float a = 1.0 - exp(-kappa * d * dt); vec3 c = mix(wine, deep, clamp(d * 1.5, 0.0, 1.0));\n' +
        '      col += T * a * c; T *= 1.0 - a; if (T < 0.004) break;\n' +
        '    }\n' +
        '  }\n' +
        '  if (hit0) { float f = abs(dot(normalize(ro + rd * s0), rd)); float a = 0.10 + 0.30 * pow(1.0 - f, 3.0); col += T * a * vec3(0.11, 0.08, 0.09); T *= 1.0 - a; }\n' +
        '  if (hit1) { float f = abs(dot(normalize(ro + rd * s1), rd)); float a = 0.05 + 0.20 * pow(1.0 - f, 3.0); col += T * a * vec3(0.11, 0.08, 0.09); T *= 1.0 - a; }\n' +
        '  o = vec4(col + T * paper, 1.0);\n' +
        '}';

    function rotation(yaw, pitch) {   /* camera frame: columns right, up, back */
        var cy = Math.cos(yaw), sy = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
        return [cy, 0, -sy, -sy * sp, cp, -cy * sp, sy * cp, sp, cy * cp];   /* column-major mat3 */
    }
    function mulRot(m, v) { return [m[0] * v[0] + m[3] * v[1] + m[6] * v[2], m[1] * v[0] + m[4] * v[1] + m[7] * v[2], m[2] * v[0] + m[5] * v[1] + m[8] * v[2]]; }

    window.VolumeView = function (canvas, opt) {
        opt = opt || {};
        var gl = canvas.getContext('webgl2', { preserveDrawingBuffer: true, antialias: false });
        var api = { ok: !!gl, yaw: opt.yaw == null ? -0.65 : opt.yaw, pitch: opt.pitch == null ? 0.42 : opt.pitch, dist: 2.15, fov: 0.46, sphere: 0, n: 0, data: null, kappa: KAPPA, offset: opt.offset || 0 };
        if (!gl) return api;
        function sh(type, src) { var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; }
        var prog = gl.createProgram(); gl.attachShader(prog, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(prog);
        if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
        var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
        var loc = gl.getAttribLocation(prog, 'p'), U = {};
        ['vol', 'rot', 'dist', 'fov', 'aspect', 'sph', 'kappa', 'has', 'paper', 'wine', 'deep', 'off'].forEach(function (k) { U[k] = gl.getUniformLocation(prog, k); });
        var tex = gl.createTexture();
        gl.bindTexture(gl.TEXTURE_3D, tex);
        gl.texParameteri(gl.TEXTURE_3D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_3D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
        ['TEXTURE_WRAP_S', 'TEXTURE_WRAP_T', 'TEXTURE_WRAP_R'].forEach(function (w) { gl.texParameteri(gl.TEXTURE_3D, gl[w], gl.CLAMP_TO_EDGE); });
        gl.pixelStorei(gl.UNPACK_ALIGNMENT, 1);
        var perm = null;
        /* the stored order is [x][y][z] (x slowest); a 3D texture wants z slowest: s = x, t = y, r = z */
        api.setVolume = function (data, n) {
            if (!perm || perm.length !== n * n * n) perm = new Uint8Array(n * n * n);
            for (var x = 0; x < n; x++) for (var y = 0; y < n; y++) { var src = (x * n + y) * n; for (var z = 0; z < n; z++) perm[(z * n + y) * n + x] = data[src + z]; }
            gl.bindTexture(gl.TEXTURE_3D, tex);
            gl.texImage3D(gl.TEXTURE_3D, 0, gl.R8, n, n, n, 0, gl.RED, gl.UNSIGNED_BYTE, perm);
            api.n = n; api.data = data;
        };
        api.clear = function () { api.data = null; };
        api.render = function () {
            var w = canvas.width, h = canvas.height; gl.viewport(0, 0, w, h);
            gl.useProgram(prog); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
            gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_3D, tex); gl.uniform1i(U.vol, 0);
            gl.uniformMatrix3fv(U.rot, false, rotation(api.yaw, api.pitch));
            gl.uniform1f(U.dist, api.dist); gl.uniform1f(U.fov, api.fov); gl.uniform1f(U.aspect, w / h); gl.uniform1f(U.sph, api.sphere);
            gl.uniform1f(U.kappa, api.kappa); gl.uniform1f(U.has, api.data ? 1 : 0);
            gl.uniform1f(U.off, api.offset); gl.uniform3fv(U.paper, PAPER); gl.uniform3fv(U.wine, WINE); gl.uniform3fv(U.deep, DEEP);
            gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
        };
        /* the ray through a point of the canvas, in css px from the top left */
        function ray(px, py, cw, ch) {
            var u = 2 * px / cw - 1, v = 1 - 2 * py / ch, R = rotation(api.yaw, api.pitch);
            var ro = mulRot(R, [0, 0, api.dist]), d = mulRot(R, [u * (cw / ch) * api.fov, v * api.fov, -1]), l = Math.hypot(d[0], d[1], d[2]);
            return { ro: ro, rd: [d[0] / l, d[1] / l, d[2] / l] };
        }
        function boxHit(ro, rd) {
            var t0 = -Infinity, t1 = Infinity;
            for (var k = 0; k < 3; k++) { var a = (-1 - ro[k]) / rd[k], b = (1 - ro[k]) / rd[k]; t0 = Math.max(t0, Math.min(a, b)); t1 = Math.min(t1, Math.max(a, b)); }
            return t1 > Math.max(t0, 0) ? [Math.max(t0, 0), t1] : null;
        }
        /* the stored level at a point of the cube, trilinear between cell centres as the texture unit does (clamped at the edges) */
        function level(p) {
            var n = api.n, D = api.data, f = [0, 0, 0], i0 = [0, 0, 0], w = [0, 0, 0];
            for (var k = 0; k < 3; k++) { var c = (p[k] * 0.5 + 0.5 - api.offset) * n - 0.5; c = Math.max(0, Math.min(n - 1, c)); i0[k] = Math.min(n - 2, Math.floor(c)); w[k] = c - i0[k]; }
            var s = 0;
            for (var a = 0; a < 2; a++) for (var b = 0; b < 2; b++) for (var c2 = 0; c2 < 2; c2++) {
                var x = i0[0] + a, y = i0[1] + b, z = i0[2] + c2, wt = (a ? w[0] : 1 - w[0]) * (b ? w[1] : 1 - w[1]) * (c2 ? w[2] : 1 - w[2]);
                s += wt * D[(x * n + y) * n + z];
            }
            return s / 255;
        }
        api.levelAt = level;
        /* the colour the shader must give at a canvas point, recomputed from the stored levels (sphere shell included) */
        api.expected = function (px, py, cw, ch) {
            var r = ray(px, py, cw, ch), ro = r.ro, rd = r.rd, col = [0, 0, 0], T = 1, R = api.sphere;
            var bq = ro[0] * rd[0] + ro[1] * rd[1] + ro[2] * rd[2], cq = ro[0] * ro[0] + ro[1] * ro[1] + ro[2] * ro[2] - R * R, disc = bq * bq - cq, s0 = 1e9, s1 = 1e9;
            if (disc > 0) { s0 = -bq - Math.sqrt(disc); s1 = -bq + Math.sqrt(disc); }
            var hit = [s0 > 0 && s0 < 1e8, s1 > 0 && s1 < 1e8];
            function shell(s, k) { var q = [ro[0] + rd[0] * s, ro[1] + rd[1] * s, ro[2] + rd[2] * s], l = Math.hypot(q[0], q[1], q[2]), f = Math.abs((q[0] * rd[0] + q[1] * rd[1] + q[2] * rd[2]) / l), a = (k ? 0.05 : 0.10) + (k ? 0.20 : 0.30) * Math.pow(1 - f, 3); col[0] += T * a * 0.11; col[1] += T * a * 0.08; col[2] += T * a * 0.09; T *= 1 - a; }
            var bh = api.data ? boxHit(ro, rd) : null;
            if (bh) {
                var dt = (bh[1] - bh[0]) / STEPS;
                for (var i = 0; i < STEPS; i++) {
                    var t = bh[0] + (i + 0.5) * dt;
                    if (hit[0] && t >= s0 && t - dt < s0) { shell(s0, 0); hit[0] = false; }
                    if (hit[1] && t >= s1 && t - dt < s1) { shell(s1, 1); hit[1] = false; }
                    var q = level([ro[0] + rd[0] * t, ro[1] + rd[1] * t, ro[2] + rd[2] * t]), d = q * q, a = 1 - Math.exp(-api.kappa * d * dt), m = Math.max(0, Math.min(1, d * 1.5));
                    for (var k = 0; k < 3; k++) col[k] += T * a * (WINE[k] + (DEEP[k] - WINE[k]) * m);
                    T *= 1 - a; if (T < 0.004) break;
                }
            }
            if (hit[0]) shell(s0, 0); if (hit[1]) shell(s1, 1);
            return [0, 1, 2].map(function (k) { return Math.round(255 * Math.min(1, col[k] + T * PAPER[k])); });
        };
        /* the stored cell of highest level along the ray under a canvas point */
        api.pick = function (px, py, cw, ch) {
            if (!api.data) return null;
            var r = ray(px, py, cw, ch), bh = boxHit(r.ro, r.rd); if (!bh) return null;
            var n = api.n, best = null, bl = -1, dt = (bh[1] - bh[0]) / STEPS;
            for (var i = 0; i < STEPS; i++) {
                var t = bh[0] + (i + 0.5) * dt, p = [r.ro[0] + r.rd[0] * t, r.ro[1] + r.rd[1] * t, r.ro[2] + r.rd[2] * t];
                var o = api.offset, ix = Math.max(0, Math.min(n - 1, Math.floor((p[0] * 0.5 + 0.5 - o) * n))), iy = Math.max(0, Math.min(n - 1, Math.floor((p[1] * 0.5 + 0.5 - o) * n))), iz = Math.max(0, Math.min(n - 1, Math.floor((p[2] * 0.5 + 0.5 - o) * n)));
                var q = api.data[(ix * n + iy) * n + iz]; if (q > bl) { bl = q; best = { ix: ix, iy: iy, iz: iz, q: q, p: p }; }
            }
            return best;
        };
        /* where a point of the cube lands on the canvas (css px), for the data panel's markers */
        api.project = function (p, cw, ch) {
            var R = rotation(api.yaw, api.pitch), ro = mulRot(R, [0, 0, api.dist]), v = [p[0] - ro[0], p[1] - ro[1], p[2] - ro[2]];
            var x = v[0] * R[0] + v[1] * R[1] + v[2] * R[2], y = v[0] * R[3] + v[1] * R[4] + v[2] * R[5], z = -(v[0] * R[6] + v[1] * R[7] + v[2] * R[8]);
            return { x: (x / (z * api.fov * cw / ch) + 1) * cw / 2, y: (1 - y / (z * api.fov)) * ch / 2 };
        };
        /* turning: drag on the canvas (a press-and-move, never a mere pass of the pointer) */
        var drag = null;
        canvas.addEventListener('pointerdown', function (e) { if (opt.canTurn && !opt.canTurn()) return; drag = { x: e.clientX, y: e.clientY, yaw: api.yaw, pitch: api.pitch }; canvas.setPointerCapture(e.pointerId); });
        canvas.addEventListener('pointermove', function (e) { if (!drag) return; api.yaw = drag.yaw - (e.clientX - drag.x) * 0.008; api.pitch = Math.max(-1.4, Math.min(1.4, drag.pitch + (e.clientY - drag.y) * 0.008)); if (opt.onTurn) opt.onTurn(); });
        function up() { drag = null; } canvas.addEventListener('pointerup', up); canvas.addEventListener('pointercancel', up);
        return api;
    };
})();
