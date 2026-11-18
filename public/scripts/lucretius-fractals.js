/* Lucretius page: a small generative background (18 November 2026). Documented in docs/pages.md, "Background".

   One canvas fixed behind the page. Famous fractals appear one after another at random places, mostly in the margins: each grows
   (its points or its curve are revealed in order), holds still for a moment, then a slow fluid takes hold of it and carries it off
   like ink in water while it fades; the next one has already begun. At most four are alive at once.

   The fluid is divergence-free: velocity (u, v) = (dψ/dy, −dψ/dx) from a stream function ψ(x, y, t), a sum of five slowly drifting
   sine waves, plus a slight fall downwards and a tiny random swerve per point (Lucretius' clinamen). Divergence-free means the ink
   is stirred and stretched but never piles up or thins out from nothing.

   Cost: at most about 13 000 points drawn per frame, 30 frames a second, each fractal drawn as one path; the loop stops while the tab
   is hidden, and under prefers-reduced-motion two fractals are drawn once and nothing moves. */
(function () {
  var cv = document.querySelector('.lp-fx');
  if (!cv || !cv.getContext || document.documentElement.dataset.bg) return;
  var ctx = cv.getContext('2d'), W = 0, H = 0, dpr = Math.min(1.5, window.devicePixelRatio || 1);
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var R = Math.random, PI = Math.PI;
  function size() { W = innerWidth; H = innerHeight; cv.width = W * dpr | 0; cv.height = H * dpr | 0; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
  size(); addEventListener('resize', size);

  /* ---- the fractals: each returns raw points [x0, y0, x1, y1, ...]; NaN lifts the pen ---- */
  function lsys(axiom, rules, ang, n, draw) {              // L-system and turtle
    var s = axiom;
    for (var i = 0; i < n; i++) { var t = ''; for (var j = 0; j < s.length; j++) t += rules[s[j]] || s[j]; s = t; }
    var x = 0, y = 0, a = 0, out = [0, 0], st = [], r = ang * PI / 180;
    for (var k = 0; k < s.length; k++) {
      var c = s[k];
      if (draw.indexOf(c) >= 0) { x += Math.cos(a); y += Math.sin(a); out.push(x, y); }
      else if (c === '+') a += r; else if (c === '-') a -= r;
      else if (c === '[') st.push(x, y, a); else if (c === ']') { a = st.pop(); y = st.pop(); x = st.pop(); out.push(NaN, NaN, x, y); }
    }
    return out;
  }
  function ifs(n, maps) {                                     // chaos game for an iterated function system
    var out = [], x = 0, y = 0;
    for (var i = 0; i < n + 20; i++) {
      var r = R(), m = maps[maps.length - 1];
      for (var j = 0; j < maps.length; j++) { if (r < maps[j][0]) { m = maps[j]; break; } r -= maps[j][0]; }
      var nx = m[1] * x + m[2] * y + m[5], ny = m[3] * x + m[4] * y + m[6]; x = nx; y = ny;
      if (i >= 20) out.push(x, -y);
    }
    return out;
  }
  var G = [
    ['Barnsley fern', 0, function () { return ifs(2600, [[.01, 0, 0, 0, .16, 0, 0], [.85, .85, .04, -.04, .85, 0, 1.6], [.07, .2, -.26, .23, .22, 0, 1.6], [.07, -.15, .28, .26, .24, 0, .44]]); }],
    ['Sierpinski triangle', 0, function () { return ifs(2600, [[1 / 3, .5, 0, 0, .5, 0, 0], [1 / 3, .5, 0, 0, .5, .5, 0], [1 / 3, .5, 0, 0, .5, .25, .433]]); }],
    ['Heighway dragon', 1, function () {
      var out = [0, 0], x = 0, y = 0, a = 0;
      for (var i = 1; i <= 4096; i++) { a += (((i & -i) << 1) & i) ? -PI / 2 : PI / 2; x += Math.cos(a); y += Math.sin(a); out.push(x, y); }
      return out; }],
    ['Lévy C curve', 1, function () { return lsys('F', { F: '+F--F+' }, 45, 11, 'F'); }],
    ['Koch snowflake', 1, function () { return lsys('F--F--F', { F: 'F+F--F+F' }, 60, 5, 'F'); }],
    ['Gosper flowsnake', 1, function () { return lsys('A', { A: 'A-B--B+A++AA+B-', B: '+A-BB--B-A++A+B' }, 60, 4, 'AB'); }],
    ['Hilbert curve', 1, function () { return lsys('A', { A: '+BF-AFA-FB+', B: '-AF+BFB+FA-' }, 90, 5, 'F'); }],
    ['Sierpinski arrowhead', 1, function () { return lsys('A', { A: 'B-A-B', B: 'A+B+A' }, 60, 7, 'AB'); }],
    ['Fractal plant', 1, function () { return lsys('X', { X: 'F+[[X]-X]-F[-FX]+X', F: 'FF' }, 25, 5, 'F'); }],
    ['Binary tree', 1, function () {                          // grown breadth first, so it rises from the trunk
      var out = [], q = [[0, 0, -PI / 2, 1, 0]], da = (18 + R() * 20) * PI / 180, f = .66 + R() * .08;
      while (q.length) { var b = q.shift(), x2 = b[0] + b[3] * Math.cos(b[2]), y2 = b[1] + b[3] * Math.sin(b[2]);
        out.push(b[0], b[1], x2, y2, NaN, NaN);
        if (b[4] < 10) { q.push([x2, y2, b[2] - da + (R() - .5) * .2, b[3] * f, b[4] + 1]); q.push([x2, y2, b[2] + da + (R() - .5) * .2, b[3] * f, b[4] + 1]); } }
      return out; }],
    ['Golden-angle sunflower', 0, function () {
      var out = []; for (var i = 1; i < 1400; i++) { var r = Math.sqrt(i), a = i * 2.39996323; out.push(r * Math.cos(a), r * Math.sin(a)); } return out; }],
    ['Golden spiral', 1, function () {
      var out = [], b = Math.log(1.6180339887) / (PI / 2);
      for (var t = 0; t < 7 * PI; t += .02) { var r = Math.exp(b * t); out.push(r * Math.cos(t), r * Math.sin(t)); } return out; }],
    ['Lorenz attractor', 1, function () {
      var out = [], x = .1, y = 0, z = 0, dt = .007;
      for (var i = 0; i < 4200; i++) { var dx = 10 * (y - x), dy = x * (28 - z) - y, dz = x * y - 8 / 3 * z; x += dx * dt; y += dy * dt; z += dz * dt; if (i > 100) out.push(x, -z); }
      return out; }],
    ['Julia set', 0, function () {                            // inverse iteration: z -> ±sqrt(z - c)
      var C = [[-.8, .156], [-.4, .6], [.285, .01], [-.70176, -.3842], [-.835, -.2321], [.355, .355], [-.123, .745]][R() * 7 | 0];
      var out = [], x = 1, y = 0;
      for (var i = 0; i < 3200; i++) { var a = x - C[0], b = y - C[1], m = Math.sqrt(Math.sqrt(a * a + b * b)), t = Math.atan2(b, a) / 2;
        x = m * Math.cos(t); y = m * Math.sin(t); if (R() < .5) { x = -x; y = -y; } if (i > 40) out.push(x, y); }
      return out; }],
    ['Clifford attractor', 0, function () {
      var P = [[-1.4, 1.6, 1, .7], [1.7, 1.7, .6, 1.2], [-1.7, 1.3, -.1, -1.2], [-1.8, -2, -.5, -.9]][R() * 4 | 0], out = [], x = .1, y = .1;
      for (var i = 0; i < 3200; i++) { var nx = Math.sin(P[0] * y) + P[2] * Math.cos(P[0] * x), ny = Math.sin(P[1] * x) + P[3] * Math.cos(P[1] * y); x = nx; y = ny; if (i > 20) out.push(x, y); }
      return out; }],
    ['Peter de Jong attractor', 0, function () {
      var P = [[1.4, -2.3, 2.4, -2.1], [2.01, -2.53, 1.61, -.33], [-2.7, -.09, -.86, -2.2]][R() * 3 | 0], out = [], x = .1, y = .1;
      for (var i = 0; i < 3200; i++) { var nx = Math.sin(P[0] * y) - Math.cos(P[1] * x), ny = Math.sin(P[2] * x) - Math.cos(P[3] * y); x = nx; y = ny; if (i > 20) out.push(x, y); }
      return out; }]
  ];
  var COLS = ['122,31,43', '163,52,63', '92,22,32', '140,40,52'];

  /* ---- one living fractal ---- */
  function region() {                                         // mostly the margins beside the 1240 px text block
    var side = (W - 1240) / 2, s, x;
    if (side > 120 && R() < .8) { s = Math.min(Math.max(side * 1.25, 230), 360) * (.75 + R() * .4); x = R() < .5 ? side / 2 : W - side / 2; x += (R() - .5) * side * .3; }
    else { s = Math.min(W, H) * (.25 + R() * .2); x = R() * W; }
    return [x, s, s * .55 + R() * (H - s * 1.1)];
  }
  function born(now) {
    var g = G[R() * G.length | 0], raw = g[2](), n = raw.length / 2;
    var mx = 1e9, Mx = -1e9, my = 1e9, My = -1e9;
    for (var i = 0; i < raw.length; i += 2) if (raw[i] === raw[i]) { mx = Math.min(mx, raw[i]); Mx = Math.max(Mx, raw[i]); my = Math.min(my, raw[i + 1]); My = Math.max(My, raw[i + 1]); }
    var rg = region(), sc = rg[1] / Math.max(Mx - mx, My - my), rot = (R() - .5) * (g[1] ? 2 * PI : .6), c = Math.cos(rot), s = Math.sin(rot);
    var p = new Float32Array(raw.length), sw = new Float32Array(n);
    for (i = 0; i < n; i++) {
      var x = (raw[2 * i] - (mx + Mx) / 2) * sc, y = (raw[2 * i + 1] - (my + My) / 2) * sc;
      p[2 * i] = rg[0] + c * x - s * y; p[2 * i + 1] = rg[2] + s * x + c * y; sw[i] = (R() - .5) * 14;
    }
    return { p: p, sw: sw, n: n, line: g[1], col: COLS[R() * COLS.length | 0], t0: now, tg: 3.5 + R() * 3, th: 2 + R() * 2.5, tf: 8 + R() * 4 };
  }

  /* ---- the fluid ---- */
  var K = []; for (var k = 0; k < 5; k++) { var th = R() * 2 * PI, kk = (.002 + R() * .006); K.push([kk * Math.cos(th), kk * Math.sin(th), .1 + R() * .3, R() * 2 * PI, (8 + R() * 14) / kk / 400]); }
  function stir(f, t, dt) {                                   // velocity = curl of ψ, plus a slow fall and each point's swerve
    var p = f.p;
    for (var i = 0; i < p.length; i += 2) {
      var x = p[i], y = p[i + 1]; if (x !== x) continue;
      var u = 0, v = 0;
      for (var j = 0; j < 5; j++) { var q = K[j], cs = Math.cos(q[0] * x + q[1] * y + q[2] * t + q[3]) * q[4]; u += q[1] * cs * 400; v -= q[0] * cs * 400; }
      p[i] = x + (u + f.sw[i >> 1]) * dt; p[i + 1] = y + (v + 9) * dt;
    }
  }

  function draw(f, t) {
    var age = t - f.t0, upto = f.n, a = .5;
    if (age < f.tg) { upto = Math.max(2, f.n * (1 - Math.pow(1 - age / f.tg, 2)) | 0); }
    else if (age > f.tg + f.th) { var k = (age - f.tg - f.th) / f.tf; a = .5 * (1 - k) * (1 - k); }
    ctx.beginPath(); var p = f.p;
    if (f.line) {
      var pen = false;
      for (var i = 0; i < upto; i++) { var x = p[2 * i], y = p[2 * i + 1];
        if (x !== x) { pen = false; continue; }
        if (pen && Math.abs(x - p[2 * i - 2]) + Math.abs(y - p[2 * i - 1]) < 40) ctx.lineTo(x, y); else ctx.moveTo(x, y); pen = true; }
      ctx.strokeStyle = 'rgba(' + f.col + ',' + a + ')'; ctx.lineWidth = .8; ctx.stroke();
    } else {
      for (i = 0; i < upto; i++) ctx.rect(p[2 * i], p[2 * i + 1], 1.3, 1.3);
      ctx.fillStyle = 'rgba(' + f.col + ',' + (a * 1.2) + ')'; ctx.fill();
    }
  }

  var live = [], last = 0, nextAt = 0, raf = 0;
  if (reduce) { var t0 = performance.now() / 1000; live.push(born(t0 - 30), born(t0 - 30)); live.forEach(function (f) { f.th = 1e9; draw(f, t0); }); return; }
  function frame(ms) {
    raf = requestAnimationFrame(frame);
    var t = ms / 1000; if (t - last < 1 / 30) return;
    var dt = Math.min(.05, t - last); last = t;
    if (t > nextAt && live.length < 4) { live.push(born(t)); nextAt = t + 2.5 + R() * 3; }
    ctx.clearRect(0, 0, W, H);
    for (var i = live.length - 1; i >= 0; i--) {
      var f = live[i], age = t - f.t0;
      if (age > f.tg + f.th + f.tf) { live.splice(i, 1); continue; }
      if (age > f.tg + f.th) stir(f, t, dt);
      draw(f, t);
    }
  }
  function go() { cancelAnimationFrame(raf); if (!document.hidden) { last = performance.now() / 1000; raf = requestAnimationFrame(frame); } }
  document.addEventListener('visibilitychange', go); go();
  window.__lpFx = { live: function () { return live.length; }, names: G.map(function (g) { return g[0]; }), gen: function (i) { return G[i][2](); } };
})();
