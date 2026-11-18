/* Phyein Usul: living scenes (18 November 2026). Documented in docs/scripts/bg-scenes.md.

   Every element that carries data-bg="<scene>" gets its own canvas and its own scene; a page places different scenes in different
   spots (behind the top of the page, in a band at its foot, behind the hero, fixed in the side margins); styles/bg-scenes.css
   holds the placement classes. No scene runs twice, and none covers a whole page with everything at once.
     data-bg-mask   how the canvas fades: "down" (strong at the top), "up", "both" (default for bands), "sides" (strong in the side
                    margins, faint behind the 1240 px text column), "soft" (the same, gentler), "softdown" (soft and down together), "none"
     data-bg-alpha  overall strength, 0 to 1 (default 1)
   A scene only runs while its element is on screen (IntersectionObserver) and the tab is visible; thirty frames a second at
   most; canvas pixels are CSS pixels (not doubled on dense screens). Nothing is mounted when the reader asks for reduced motion.

   The ten scenes (each an object with init() and draw(dt); all sizes come from the element, W x H):
     letters  loose letters drift, then assemble into a word and scatter again         (Lucretius I 196-197)
     seeds    a seed falls, a stem grows slowly into a rose, an ear of wheat or grapes  (I 174-175)
     swerve   atoms fall in parallel; one tilts; a cascade of collisions                (II 216-293)
     shores   motes rise through a slow waterline and brighten: the shores of light     (I 170, 179)
     forest   a tree's fallen leaves feed neighbouring seedlings, each with its own habit; generations
     powder   iron powder gathers on the field lines of two drifting magnets and of a wire whose current comes and goes
     harp     a ten-hole harmonica; each note travels outward through the air as rings of pressure
     spin     spinners turning at random; a wandering rotating field pulls those in reach into step
     mix      three species, three shapes, three temperatures; walls lift; collisions mix and equalise them
     chip     blocks are traced, wires routed block to block, then the die is stamped across a wafer */
(function () {
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var INST = [];
  var MASKS = {
    down: 'linear-gradient(to bottom,#000 0,#000 35%,transparent 100%)', up: 'linear-gradient(to top,#000 0,#000 35%,transparent 100%)',
    both: 'linear-gradient(to bottom,transparent 0,#000 22%,#000 78%,transparent 100%)',
    soft: 'linear-gradient(to right,#000 0,#000 calc(50% - 640px),rgba(0,0,0,.3) calc(50% - 430px),rgba(0,0,0,.3) calc(50% + 430px),#000 calc(50% + 640px),#000 100%)',
    round: 'radial-gradient(ellipse closest-side at center,#000 55%,transparent 100%)',
    sides: 'linear-gradient(to right,#000 0,#000 calc(50% - 720px),rgba(0,0,0,.07) calc(50% - 590px),rgba(0,0,0,.07) calc(50% + 590px),#000 calc(50% + 720px),#000 100%)' };

  function mount(host) {
  var name = host.getAttribute('data-bg'), fixed = getComputedStyle(host).position === 'fixed';
  var cv = document.createElement('canvas'), x = cv.getContext('2d'), W = 0, H = 0;
  var mk = host.getAttribute('data-bg-mask') || 'both', MASK = mk === 'softdown' ? MASKS.soft + ',' + MASKS.down : MASKS[mk];
  cv.className = 'bgs'; cv.setAttribute('aria-hidden', 'true');
  if (MASK) { cv.style.webkitMaskImage = MASK; cv.style.maskImage = MASK; if (mk === 'softdown') { cv.style.webkitMaskComposite = 'source-in'; cv.style.maskComposite = 'intersect'; } }
  cv.style.opacity = host.getAttribute('data-bg-alpha') || (mk === 'sides' && innerWidth <= 760 ? '.3' : '1');
  if (!/\bbgs-/.test(host.className)) { if (getComputedStyle(host).position === 'static') host.style.position = 'relative'; host.style.isolation = 'isolate'; cv.style.zIndex = '-1'; }
  host.insertBefore(cv, host.firstChild);

  var C = '122,31,43', R = Math.random, PI = Math.PI;
  function col(a) { return 'rgba(' + C + ',' + a + ')'; }
  function cl(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function v(a, b) { return a + R() * (b - a); }
  function clear() { x.clearRect(0, 0, W, H); }
  function fade(a) { x.globalCompositeOperation = 'destination-out'; x.fillStyle = 'rgba(0,0,0,' + a + ')'; x.fillRect(0, 0, W, H); x.globalCompositeOperation = 'source-over'; }
  function dot(px, py, r, a) { x.fillStyle = col(a); x.beginPath(); x.arc(px, py, r, 0, 7); x.fill(); }
  function ln(a, b, c, d) { x.beginPath(); x.moveTo(a, b); x.lineTo(c, d); x.stroke(); }
  function leaf(px, py, rot, s, a) { x.save(); x.translate(px, py); x.rotate(rot); x.fillStyle = col(a); x.beginPath(); x.ellipse(4 * s, 0, 5 * s, 2.3 * s, 0, 0, 7); x.fill(); x.restore(); }
  function area() { return W * H / 272000; }                       // 1 = the 680 x 400 sketch the scenes were tuned on
  function margin() { return (W - 1240) / 2; }                     // width of one side margin beside the text column

  var S = {};

  /* ---- letters: the same letters, rearranged, make every word ---- */
  S.letters = {
    words: [['SEMINA', 0], ['بذور', 1], ['NATVRA', 0], ['العدم', 1], ['NOTHING', 0], ['طبيعة', 1], ['SAMEN', 0], ['نور', 1], ['NIHIL', 0], ['LVMEN', 0]],
    font: '30px "Instrument Serif", Georgia, "Times New Roman", serif',
    init: function () {
      this.P = []; var k = Math.max(1, Math.round(area() / 2.5));
      for (var r = 0; r < k; r++) for (var w = 0; w < this.words.length; w++) { var ch = Array.from(this.words[w][0]); for (var i = 0; i < ch.length; i++) this.P.push({ ch: ch[i], x: R() * W, y: R() * H, vx: v(-13, 13), vy: v(-13, 13), t: null }); }
      this.T = 0; this.wi = 0; this.cur = null;
    },
    draw: function (dt) {
      clear(); x.font = this.font; x.textBaseline = 'middle'; this.T += dt; var self = this;
      if (!this.cur && this.T > 1.5) {
        var w = this.words[this.wi % this.words.length], chs = Array.from(w[0]), mg = margin(), pos = [], i, tot = 0;
        var cx = mg > 170 ? (R() < .5 ? mg / 2 : W - mg / 2) : W * v(.25, .75), cy = H * v(.15, .85);
        if (w[1]) { var ws = chs.map(function (c) { return x.measureText(c).width + 5; }); ws.forEach(function (q) { tot += q; }); var xr = cx + tot / 2; ws.forEach(function (q) { xr -= q; pos.push(xr); }); }
        else { tot = x.measureText(w[0]).width; chs.forEach(function (c, i) { pos.push(cx - tot / 2 + x.measureText(w[0].slice(0, i)).width); }); }
        chs.forEach(function (c, i) { var best = null, bd = 1e9; self.P.forEach(function (q) { if (q.ch === c && !q.t) { var d = Math.abs(q.x - pos[i]) + Math.abs(q.y - cy); if (d < bd) { bd = d; best = q; } } }); if (best) best.t = [pos[i], cy]; });
        this.cur = { w: w, cx: cx, cy: cy, t0: this.T };
      }
      var k = 0, age = 0;
      if (this.cur) {
        age = this.T - this.cur.t0; if (this.cur.w[1]) k = cl((age - 2.6) / .8, 0, 1) * cl((6.3 - age) / .5, 0, 1);
        if (age > 6.5) { this.P.forEach(function (p) { if (p.t) { p.t = null; p.vx = v(-30, 30); p.vy = v(-30, 30); } }); this.cur = null; this.T = 0; this.wi++; }
      }
      x.textAlign = 'left';
      this.P.forEach(function (p) {
        if (p.t) { var s = Math.min(1, dt * 3); p.x += (p.t[0] - p.x) * s; p.y += (p.t[1] - p.y) * s; }
        else { p.vx = cl(p.vx + (R() - .5) * dt * 30, -30, 30); p.vy = cl(p.vy + (R() - .5) * dt * 30, -30, 30); p.x += p.vx * dt; p.y += p.vy * dt; if (p.x < -20) p.x = W + 10; if (p.x > W + 20) p.x = -10; if (p.y < -20) p.y = H + 10; if (p.y > H + 20) p.y = -10; }
        x.fillStyle = col(p.t ? .9 * (1 - k) : .32); x.fillText(p.ch, p.x, p.y);
      });
      if (this.cur && k > 0) { x.textAlign = 'center'; x.fillStyle = col(.9 * k); x.fillText(this.cur.w[0], this.cur.cx, this.cur.cy); }
    }
  };

  /* ---- seeds: each thing from its own seed, little by little ---- */
  S.seeds = {
    init: function () { this.S = []; this.Pl = []; this.tm = 0; },
    draw: function (dt) {
      clear(); var G = H - 12, self = this, k = W / 680; this.tm += dt;
      if (this.tm > .7 / k && this.Pl.length < 26 * k) { this.tm = 0; this.S.push({ x: v(20, W - 20), y: -5, type: R() * 3 | 0 }); }
      x.strokeStyle = col(.25); x.lineWidth = 1; ln(0, G, W, G);
      this.S = this.S.filter(function (s) { s.y += 130 * dt; dot(s.x, s.y, 2, .8); if (s.y >= G) { self.Pl.push({ x: s.x, type: s.type, age: 0, h: v(.22, .62) * H, sw: R() * 6, life: 17 }); return false; } return true; });
      this.Pl = this.Pl.filter(function (p) {
        p.age += dt; if (p.age > p.life) return false;
        var g0 = Math.min(1, p.age / 7), g = 1 - (1 - g0) * (1 - g0), ht = p.h * g, a = p.age > p.life - 3 ? (p.life - p.age) / 3 : 1, s, i;
        function px(s) { return p.x + Math.sin(s * .02 + p.sw) * 9 * (s / p.h); }
        x.strokeStyle = col(.75 * a); x.lineWidth = 1.1; x.beginPath(); x.moveTo(p.x, G); for (s = 0; s <= ht; s += 5) x.lineTo(px(s), G - s); x.stroke();
        x.beginPath(); for (s = 26, i = 0; s < ht - 10; s += 28, i++) { var d = i % 2 ? 1 : -1, bx = px(s), by = G - s; x.moveTo(bx, by); x.quadraticCurveTo(bx + d * 9, by - 3, bx + d * 13, by - 11); } x.stroke();
        if (g0 > .85) {
          var ha = (g0 - .85) / .15 * a, tx = px(ht), ty = G - ht; x.fillStyle = col(.55 * ha); x.strokeStyle = col(.8 * ha);
          if (p.type === 0) { for (i = 0; i < 6; i++) { x.beginPath(); x.arc(tx + Math.cos(i * 1.047) * 5, ty + Math.sin(i * 1.047) * 5, 4, 0, 7); x.fill(); } x.beginPath(); x.arc(tx, ty, 3, 0, 7); x.fill(); }
          else if (p.type === 1) { x.beginPath(); for (i = 0; i < 6; i++) { var yy = ty + i * 6; x.moveTo(tx, yy); x.lineTo(tx - 6, yy - 8); x.moveTo(tx, yy); x.lineTo(tx + 6, yy - 8); } x.stroke(); }
          else for (var r = 0; r < 4; r++) for (i = 0; i < 4 - r; i++) { x.beginPath(); x.arc(tx + 8 + (i - (3 - r) / 2) * 6.5, ty + 8 + r * 6, 3, 0, 7); x.fill(); }
        }
        return true;
      });
    }
  };

  /* ---- swerve: one atom leaves its straight fall, and a world of collisions follows ---- */
  S.swerve = {
    init: function () { clear(); this.A = []; var per = Math.ceil(H / 67); for (var c = 0; c * 20 + 10 < W; c++) for (var i = 0; i < per; i++) { var x0 = 10 + c * 20; this.A.push({ x0: x0, x: x0, y: R() * H, vx: 0, vy: 90, hot: 0, cd: 0 }); } this.tm = 1.5; },
    draw: function (dt) {
      fade(.13); this.tm += dt; var A = this.A, n = A.length, i, j;
      if (this.tm > 2.6 / Math.max(1, area() / 2)) { this.tm = 0; var a0 = A[R() * n | 0]; a0.vx = (R() < .5 ? -1 : 1) * v(18, 44); a0.hot = 1; }
      for (i = 0; i < n; i++) {
        var a = A[i]; a.cd -= dt; if (!a.hot || a.cd > 0) continue;
        for (j = 0; j < n; j++) { var b = A[j]; if (j === i || b.cd > 0) continue; var dx = a.x - b.x, dy = a.y - b.y; if (dx * dx + dy * dy < 40) { var s = dx >= 0 ? 1 : -1; a.vx += s * v(15, 45); b.vx -= s * v(15, 45); a.vy = 90 + v(-25, 25); b.vy = 90 + v(-25, 25); b.hot = 1; a.cd = b.cd = .35; break; } }
      }
      for (i = 0; i < n; i++) { a = A[i]; a.x += a.vx * dt; a.y += a.vy * dt; if (a.x < 0) a.x += W; if (a.x > W) a.x -= W; if (a.y > H + 5) { a.y = -5; a.x = a.x0; a.vx = 0; a.vy = 90; a.hot = 0; } dot(a.x, a.y, a.hot ? 2.3 : 1.2, a.hot ? .9 : .35); }
    }
  };

  /* ---- shores of light ---- */
  S.shores = {
    init: function () { this.M = []; var n = Math.min(520, 120 * area()); for (var i = 0; i < n; i++) this.M.push({ x: R() * W, y: R() * H, v: v(12, 32), ph: R() * 6 }); this.t = 0; },
    draw: function (dt) {
      clear(); this.t += dt; var t = this.t, y0 = H * .58, q;
      function ys(q) { return y0 + 10 * Math.sin(q * .012 + t * .5) + 6 * Math.sin(q * .031 - t * .8); }
      x.beginPath(); x.moveTo(0, H); for (q = 0; q <= W; q += 8) x.lineTo(q, ys(q)); x.lineTo(W, H); x.closePath(); x.fillStyle = col(.10); x.fill();
      [0, 14, 30, 50].forEach(function (o, i) { x.beginPath(); for (var q = 0; q <= W; q += 8) { var yy = ys(q + o * 3) + o; if (q) x.lineTo(q, yy); else x.moveTo(q, yy); } x.strokeStyle = col(.55 - .13 * i); x.lineWidth = 1; x.stroke(); });
      this.M.forEach(function (m) { m.y -= m.v * dt; m.x += Math.sin(t + m.ph) * 8 * dt; if (m.y < -5) { m.y = H + 5; m.x = R() * W; } var s = ys(m.x), a = .18, r = 1; if (m.y < s) { var k = Math.min(1, (s - m.y) / 60); a = (.2 + .7 * k) * Math.min(1, m.y / 60); r = 1 + 1.6 * k; } dot(m.x, m.y, r, a); });
    }
  };

  /* ---- forest: every tree its own habit; the fall of one feeds the next ---- */
  var KINDS = [
    function () { return { n: 2, spread: v(.45, .65), ratio: v(.68, .76), lean: v(-.2, .2), droop: 0, mono: 0, maxd: 5, len: v(36, 44), need: 150 }; },
    function () { return { n: 3, spread: v(1, 1.25), ratio: .5, lean: 0, droop: v(.2, .4), mono: 1, maxd: 5, len: v(26, 32), need: 130 }; },
    function () { return { n: 3, spread: v(.5, .7), ratio: v(.56, .66), lean: v(-.15, .15), droop: 0, mono: 0, maxd: 4, len: v(30, 38), need: 110 }; },
    function () { return { n: 2, spread: v(.32, .45), ratio: v(.72, .8), lean: (R() < .5 ? -1 : 1) * v(.7, 1.1), droop: 0, mono: 0, maxd: 5, len: v(34, 42), need: 140 }; },
    function () { return { n: 2, spread: v(.65, .85), ratio: v(.66, .74), lean: v(-.1, .1), droop: v(.8, 1.1), mono: 0, maxd: 6, len: v(32, 38), need: 160 }; }];
  function grow(G, px, py, g, out) {
    var md = 1 + Math.floor(g * (G.maxd - 1) + .001), n = 0;
    function j() { return G.j[n++ % 97]; }
    function rec(px, py, a, len, d) {
      a += G.lean * .13 + G.droop * Math.cos(a) * .34; var x2 = px + len * Math.cos(a), y2 = py + len * Math.sin(a);
      if (out) out.S.push([px, py, x2, y2, d]); else { x.lineWidth = Math.max(.7, 3.4 - d * .6); ln(px, py, x2, y2); }
      if (d >= md - 1) { if (out) out.T.push({ x: x2, y: y2, a: a }); return; }
      if (G.mono) { rec(x2, y2, a + (j() - .5) * .16, len * .84, d + 1); var sg = d % 2 ? 1 : -1; rec(x2, y2, a + sg * G.spread * (.85 + .3 * j()), len * .55, d + 1); rec(x2, y2, a - sg * G.spread * (.85 + .3 * j()), len * .5, d + 1); }
      else for (var k = 0; k < G.n; k++) { var f = k / (G.n - 1) * 2 - 1; rec(x2, y2, a + f * G.spread + (j() - .5) * .36, len * G.ratio * (.8 + .4 * j()), d + 1); }
    }
    rec(px, py, -PI / 2, G.len * (.25 + .75 * g), 0);
  }
  S.forest = {
    mk: function (px, G) { G.j = []; for (var i = 0; i < 97; i++) G.j.push(R()); G.len *= this.sc; return { x: px, G: G, fed: 0, mat: 0, age: 0 }; },
    ripen: function (t) { var o = { S: [], T: [] }; grow(t.G, t.x, this.GY, 1, o); t.S = o.S; var sl = Math.max(1, o.T.length / 32); t.T = o.T.map(function (q) { return { x: q.x, y: q.y, a: q.a, s: 1, hold: v(1, 9) * sl, rg: 0, sl: sl }; }); t.mat = 1; t.age = 0; t.life = v(55, 100); },
    spawn: function () { for (var k = 0; k < 30; k++) { var px = v(30, W - 30); if (this.A.every(function (t) { return Math.abs(t.x - px) > 55; })) { this.A.push(this.mk(px, KINDS[R() * 5 | 0]())); return; } } },
    init: function () { this.GY = H - 46; this.sc = cl(H / 520, .8, 1.7); this.max = cl(Math.round(9 * W / 680), 5, 18); this.A = []; this.L = []; this.M = []; var g = KINDS[0](); g.len = 64; g.maxd = 6; var m = this.mk(Math.max(46, W * .1), g); this.ripen(m); m.life = 45; this.A.push(m); for (var k = 0; k < Math.max(3, this.max / 3); k++) this.spawn(); },
    draw: function (dt) {
      clear(); var GY = this.GY, self = this, young = 0; x.strokeStyle = col(.25); x.lineWidth = 1; ln(0, GY, W, GY);
      this.A.forEach(function (t) {
        x.strokeStyle = col(.6);
        if (t.mat) {
          t.age += dt; t.S.forEach(function (s) { x.lineWidth = Math.max(.7, 3.8 - s[4] * .65); ln(s[0], s[1], s[2], s[3]); });
          t.T.forEach(function (tp) {
            if (tp.s >= 1) { tp.hold -= dt; if (tp.hold <= 0) { tp.s = 0; tp.rg = 3; self.L.push({ x: tp.x, y: tp.y, ph: R() * 6, t: 0, w: v(-30, 44) }); } }
            else if (tp.rg > 0) tp.rg -= dt; else { tp.s = Math.min(1, tp.s + dt / 2); if (tp.s >= 1) tp.hold = v(2, 11) * tp.sl; }
            if (tp.s > 0) leaf(tp.x, tp.y, tp.a, tp.s, .6);
          });
          if (t.age > t.life) { t.dead = 1; t.S.forEach(function (s, i) { if (i % 2 === 0) self.L.push({ x: (s[0] + s[2]) / 2, y: (s[1] + s[3]) / 2, ph: R() * 6, t: 0, w: v(-10, 10) }); }); }
        } else { young++; var g = Math.min(1, t.fed / t.G.need); if (g <= 0) dot(t.x, GY, 1.5, .5); else grow(t.G, t.x, GY, g, null); if (g >= 1) self.ripen(t); }
      });
      this.A = this.A.filter(function (t) { return !t.dead; }); if (young < 2 && this.A.length < this.max) this.spawn();
      this.L = this.L.filter(function (l) { l.t += dt; l.y += 32 * dt; var w = l.ph + l.t * 2.4; l.x += (l.w + Math.cos(w) * 34) * dt; if (l.y >= GY - 2) { for (var k = 0; k < 4; k++) self.M.push({ x: l.x + v(-4, 4), y: GY, ty: GY + 6 + R() * 22 }); return false; } leaf(l.x, l.y, Math.sin(w), 1, .75); return true; });
      if (this.M.length > 700) this.M.splice(0, this.M.length - 700);
      this.M = this.M.filter(function (m) { var b = null; self.A.forEach(function (k) { if (!k.mat && (!b || Math.abs(k.x - m.x) < Math.abs(b.x - m.x))) b = k; }); m.y += (m.ty - m.y) * dt * 1.5; if (b) { var d = b.x - m.x; if (Math.abs(d) < 3) { b.fed++; return false; } m.x += (d > 0 ? 1 : -1) * 26 * dt; } dot(m.x, m.y, 1.4, .85); return true; });
    }
  };

  /* ---- powder: iron powder over magnets under a sheet, and a wire with a current ---- */
  S.powder = {
    init: function () { this.t = 0; this.n = Math.min(7000, Math.round(3000 * area())); this.px = new Float32Array(this.n); this.py = new Float32Array(this.n); for (var i = 0; i < this.n; i++) { this.px[i] = R() * W; this.py[i] = R() * H; } this.G = [{ bx: W * .3, by: H * .45, a: .3, w: .1, ph: 0 }, { bx: W * .7, by: H * .56, a: 2.6, w: -.07, ph: 2.5 }]; this.L = cl(Math.min(W, H) * .1, 34, 70); },
    draw: function (dt) {
      clear(); this.t += dt; var t = this.t, P = [], I = 1.6 * cl(Math.sin(2 * PI * t / 18) * 1.6, 0, 1), wx = W / 2 + W * .09 * Math.sin(t * .09), wy = H / 2 + H * .1 * Math.cos(t * .07), L = this.L, i, k;
      this.G.forEach(function (g) { g.a += g.w * dt; var cx = g.bx + 30 * Math.sin(t * .13 + g.ph), cy = g.by + 22 * Math.cos(t * .11 + g.ph), dx = L * Math.cos(g.a), dy = L * Math.sin(g.a); P.push([cx + dx, cy + dy, 1], [cx - dx, cy - dy, -1]); x.strokeStyle = col(.14); x.lineWidth = 20; x.lineCap = 'butt'; ln(cx + dx, cy + dy, cx - dx, cy - dy); });
      x.lineWidth = 1.5; x.strokeStyle = col(.25 + .5 * I / 1.6); x.beginPath(); x.arc(wx, wy, 8, 0, 7); x.stroke(); dot(wx, wy, 2.5 * I / 1.6 + .5, .9);
      var tp = t % 3.5, tap = tp < .25 ? 5 * (1 - tp / .25) : 0, N = 22; x.strokeStyle = col(.8); x.lineWidth = 1.3; x.lineCap = 'round'; x.beginPath();
      for (i = 0; i < this.n; i++) {
        var px = this.px[i], py = this.py[i], bx = 0, by = 0, psi = 0, dx, dy, r2;
        for (k = 0; k < 4; k++) { var p = P[k]; dx = px - p[0]; dy = py - p[1]; r2 = dx * dx + dy * dy + 25; bx += p[2] * dx / r2; by += p[2] * dy / r2; psi += p[2] * Math.atan2(dy, dx); }
        dx = px - wx; dy = py - wy; r2 = dx * dx + dy * dy + 25; bx += -I * dy / r2; by += I * dx / r2; psi -= I * .5 * Math.log(r2);
        var mg = Math.hypot(bx, by) + 1e-9, ux = bx / mg, uy = by / mg, lat = -Math.sin(N * psi) * 1.1, al = (R() - .5) * 1.4;
        px += -uy * lat + ux * al + (R() - .5) * tap; py += ux * lat + uy * al + (R() - .5) * tap;
        if (px < 0 || px > W || py < 0 || py > H || R() < .0006) { px = R() * W; py = R() * H; }
        this.px[i] = px; this.py[i] = py; x.moveTo(px - ux * 1.6, py - uy * 1.6); x.lineTo(px + ux * 1.6, py + uy * 1.6);
      }
      x.stroke(); x.lineCap = 'butt';
    }
  };

  /* ---- harp: a harmonica; every note travels outward at the speed of sound (here 140 px/s) ---- */
  S.harp = {
    seq: [[3], [4], [5], [3, 4, 5], [6], [], [4], [0, 1, 2], [7], [3, 5], [], [1, 2, 3], [8], [6, 7, 8]], HN: 1024,
    init: function () { this.t = 0; this.a = new Float32Array(10); this.hs = []; this.last = []; for (var i = 0; i < 10; i++) { this.hs.push(new Float32Array(this.HN)); this.last.push(-99); } this.li = 0; this.Q = []; var s = Math.max(9, Math.sqrt(W * H / 8000)); for (var y = s / 2; y < H; y += s * .9) for (var q = s / 2; q < W; q += s) this.Q.push([q + v(-.3, .3) * s, y + v(-.3, .3) * s]); this.x0 = W / 2 - 105; this.y0 = H - 30; },
    draw: function (dt) {
      clear(); this.t += dt; var t = this.t, on = this.seq[Math.floor(t / 2.2) % this.seq.length], idx = Math.floor(t * 40), i, k, HN = this.HN, x0 = this.x0, y0 = this.y0, act = [];
      for (i = 0; i < 10; i++) { var tg = on.indexOf(i) >= 0 ? 1 : 0; this.a[i] += (tg - this.a[i]) * Math.min(1, dt * 5); for (k = this.li + 1; k <= idx; k++) this.hs[i][k % HN] = this.a[i]; if (this.a[i] > .03) this.last[i] = t; if (t - this.last[i] < 24) act.push(i); }
      this.li = idx; x.fillStyle = col(.62); x.beginPath();
      for (var n = 0; n < this.Q.length; n++) {
        var q = this.Q[n], ox = 0, oy = 0;
        for (k = 0; k < act.length; k++) { i = act[k]; var dx = q[0] - (x0 + i * 23.3), dy = q[1] - y0, r = Math.hypot(dx, dy) + 1, id = Math.floor((t - r / 140) * 40); if (id < 0 || idx - id > HN - 4) continue; var am = this.hs[i][id % HN]; if (am < .03) continue; var kk = 2 * PI / (70 - i * 4.5), d = am * 6 * Math.sin(kk * r - kk * 140 * t) / (1 + r / 260); ox += dx / r * d; oy += dy / r * d; }
        if (q[1] + oy < y0 - 20) x.rect(q[0] + ox, q[1] + oy, 1.6, 1.6);
      }
      x.fill(); x.strokeStyle = col(.85); x.lineWidth = 1.5; x.strokeRect(x0 - 19, y0 - 14, 248, 30);
      for (i = 0; i < 10; i++) { var hx = x0 - 9 + i * 23.3; x.strokeStyle = col(.5); x.lineWidth = 1; x.strokeRect(hx, y0 - 9, 18, 20); var o = this.a[i] * 3.5 * Math.sin(2 * PI / (70 - i * 4.5) * 140 * t); x.strokeStyle = col(.95); x.lineWidth = 1.6; x.beginPath(); x.moveTo(hx + 3, y0 + 8); x.quadraticCurveTo(hx + 9 + o, y0, hx + 15 + o * 1.6, y0 - 6); x.stroke(); }
    }
  };

  /* ---- spin: spinners at random; a wandering rotating field brings those in reach into step ---- */
  S.spin = {
    init: function () { this.t = 0; this.O = []; this.nc = Math.floor(W / 28); this.nr = Math.floor(H / 29.5); var ox = (W - (this.nc - 1) * 28) / 2, oy = (H - (this.nr - 1) * 29.5) / 2; for (var j = 0; j < this.nr; j++) for (var i = 0; i < this.nc; i++) this.O.push({ x: ox + i * 28, y: oy + j * 29.5, th: R() * 2 * PI, w: (R() < .5 ? -1 : 1) * v(1.5, 5) }); this.sg = cl(Math.min(W, H) * .33, 110, 300); },
    draw: function (dt) {
      clear(); this.t += dt; var t = this.t, phi = 3 * t, sx = W / 2 + W * .37 * Math.sin(t * .21), sy = H / 2 + H * .33 * Math.sin(t * .33 + 1), O = this.O, nc = this.nc, N = O.length, s2 = 2 * this.sg * this.sg, n, k;
      x.strokeStyle = col(.12); x.lineWidth = 1; x.beginPath(); x.arc(sx, sy, this.sg, 0, 7); x.stroke(); x.lineWidth = 8; x.lineCap = 'round'; ln(sx - 40 * Math.cos(phi), sy - 40 * Math.sin(phi), sx + 40 * Math.cos(phi), sy + 40 * Math.sin(phi)); x.lineCap = 'butt';
      for (n = 0; n < N; n++) { var o = O[n], dx = o.x - sx, dy = o.y - sy, K = 16 * Math.exp(-(dx * dx + dy * dy) / s2), c = 0, i = n % nc; if (i > 0) c += Math.sin(O[n - 1].th - o.th); if (i < nc - 1) c += Math.sin(O[n + 1].th - o.th); if (n >= nc) c += Math.sin(O[n - nc].th - o.th); if (n < N - nc) c += Math.sin(O[n + nc].th - o.th); o.d = o.w + K * Math.sin(phi - o.th) + .9 * c; o.K = K; }
      for (n = 0; n < N; n++) { o = O[n]; o.th += o.d * dt; var lock = Math.pow(Math.max(0, Math.cos(o.th - phi)), 4) * Math.min(1, o.K / 5), a = .3 + .65 * lock; x.strokeStyle = col(a); x.lineWidth = 1.3; x.beginPath(); for (k = 0; k < 3; k++) { var an = o.th + k * 2.094; x.moveTo(o.x, o.y); x.lineTo(o.x + 10 * Math.cos(an), o.y + 10 * Math.sin(an)); } x.stroke(); dot(o.x + 10 * Math.cos(o.th), o.y + 10 * Math.sin(o.th), 2.4, Math.min(1, a + .2)); }
    }
  };

  /* ---- mix: three species in three chambers across the whole window; walls lift; entropy rises, temperatures meet ---- */
  S.mix = {
    init: function () { this.t = 0; this.P = []; this.n = cl(Math.round(80 * area() / 3) * 3, 150, 540); var per = this.n / 3; for (var i = 0; i < this.n; i++) { var k = i / per | 0, a = R() * 2 * PI, s = [150, 75, 28][k] * v(.7, 1.3); this.P.push({ k: k, x: (k + v(.04, .96)) * W / 3, y: v(8, H - 8), vx: s * Math.cos(a), vy: s * Math.sin(a), r: R() * 6, w: v(-2, 2) }); } this.E = []; this.et = 0; },
    shape: function (p) {
      x.save(); x.translate(p.x, p.y); x.rotate(p.r);
      if (p.k === 0) { x.fillStyle = col(.85); x.beginPath(); x.moveTo(0, -5.5); x.lineTo(4.8, 3.5); x.lineTo(-4.8, 3.5); x.closePath(); x.fill(); }
      else if (p.k === 1) { x.strokeStyle = col(.8); x.lineWidth = 1.4; x.beginPath(); x.arc(0, 0, 4, 0, 7); x.stroke(); }
      else { x.fillStyle = col(.45); x.fillRect(-3.6, -3.6, 7.2, 7.2); x.strokeStyle = col(.9); x.lineWidth = 1; x.strokeRect(-3.6, -3.6, 7.2, 7.2); }
      x.restore();
    },
    draw: function (dt) {
      clear(); this.t += dt; var t = this.t, P = this.P, n = P.length, w1 = W / 3, w2 = 2 * W / 3, wy = H - cl((t - 3) * H / 6, 0, H), i, j, self = this;
      if (t > 60) { this.init(); return; }
      x.strokeStyle = col(.6); x.lineWidth = 3; if (wy > 0) { ln(w1, 0, w1, wy); ln(w2, 0, w2, wy); }
      for (i = 0; i < n; i++) { var a = P[i]; for (j = i + 1; j < n; j++) { var b = P[j], dx = b.x - a.x, dy = b.y - a.y, d2 = dx * dx + dy * dy; if (d2 < 81 && d2 > 0) { var d = Math.sqrt(d2), nx = dx / d, ny = dy / d, rv = (b.vx - a.vx) * nx + (b.vy - a.vy) * ny; if (rv < 0) { a.vx += rv * nx; a.vy += rv * ny; b.vx -= rv * nx; b.vy -= rv * ny; } } } }
      var c = [[0, 0, 0], [0, 0, 0], [0, 0, 0]], ke = [0, 0, 0];
      P.forEach(function (p) {
        var ox = p.x; p.x += p.vx * dt; p.y += p.vy * dt; p.r += p.w * dt;
        if (p.x < 6) { p.x = 6; p.vx = Math.abs(p.vx); } if (p.x > W - 6) { p.x = W - 6; p.vx = -Math.abs(p.vx); } if (p.y < 6) { p.y = 6; p.vy = Math.abs(p.vy); } if (p.y > H - 6) { p.y = H - 6; p.vy = -Math.abs(p.vy); }
        if (((ox - w1) * (p.x - w1) < 0 || (ox - w2) * (p.x - w2) < 0) && p.y < wy + 5) { p.x = ox; p.vx = -p.vx; }
        c[p.x < w1 ? 0 : p.x < w2 ? 1 : 2][p.k]++; ke[p.k] += p.vx * p.vx + p.vy * p.vy; self.shape(p);
      });
      this.et += dt;
      if (this.et > .25) { this.et = 0; var Sm = 0; c.forEach(function (r) { var tot = r[0] + r[1] + r[2]; r.forEach(function (q) { if (q) Sm -= q * Math.log(q / tot); }); }); var mk = Math.max(ke[0], ke[1], ke[2]), mn = Math.min(ke[0], ke[1], ke[2]); this.E.push([t, Sm / (n * Math.log(3)), (mk - mn) / (mk + mn)]); }
      var gx = 24, gw = Math.min(300, W - 48), gy = H - 24; x.strokeStyle = col(.2); x.lineWidth = 1; ln(gx, gy, gx + gw, gy); ln(gx, gy - 55, gx + gw, gy - 55);
      [1, 2].forEach(function (q) { x.strokeStyle = col(q === 1 ? .85 : .4); x.lineWidth = q === 1 ? 1.4 : 1; x.setLineDash(q === 1 ? [] : [4, 3]); x.beginPath(); self.E.forEach(function (e, i) { var px = gx + e[0] / 60 * gw, py = gy - e[q] * 55; if (i) x.lineTo(px, py); else x.moveTo(px, py); }); x.stroke(); });
      x.setLineDash([]);
    }
  };

  /* ---- chip: blocks traced at once, wires routed one by one, then the die stamped across a wafer ---- */
  var X0 = 160, Y0 = 20, CS = 60;
  function plen(p) { var l = 0; for (var i = 1; i < p.length; i++) l += Math.abs(p[i][0] - p[i - 1][0]) + Math.abs(p[i][1] - p[i - 1][1]); return l; }
  function part(p, len) { x.beginPath(); x.moveTo(p[0][0], p[0][1]); var hx = p[0][0], hy = p[0][1]; for (var i = 1; i < p.length && len > 0; i++) { var dx = p[i][0] - p[i - 1][0], dy = p[i][1] - p[i - 1][1], l = Math.abs(dx) + Math.abs(dy), f = Math.min(1, len / l); hx = p[i - 1][0] + dx * f; hy = p[i - 1][1] + dy * f; x.lineTo(hx, hy); len -= l; } x.stroke(); return [hx, hy]; }
  S.chip = {
    init: function () {
      this.B = []; this.RT = []; this.T = 0; this.ph = 0; this.ft = 0; var i, j, k, n;
      var mg = margin(); if (W >= 1240) { this.s = Math.min(.78, (H - 120) / 400); this.cx = W / 2 + (document.documentElement.dir === 'rtl' ? -1 : 1) * Math.min(320, W * .2); this.cy = 96 + 200 * this.s; } else if (W > 760) { this.s = .55; this.cx = W - 118; this.cy = H * .66; } else { this.s = .45; this.cx = W - 96; this.cy = H - 104; }
      for (j = 0; j < 6; j++) for (i = 0; i < 6; i++) { if (R() < .12) continue; var w = v(26, 44), h = v(26, 44), cx = X0 + CS * (i + .5), cy = Y0 + CS * (j + .5), c = R() * 4 | 0, q = [[cx - w / 2, cy - h / 2], [cx + w / 2, cy - h / 2], [cx + w / 2, cy + h / 2], [cx - w / 2, cy + h / 2]], p = []; for (k = 0; k < 5; k++) p.push(q[(c + k) % 4]); this.B.push({ i: i, j: j, cx: cx, cy: cy, w: w, h: h, p: p, L: 2 * (w + h), t0: R() * 2.6, inner: R() < .5 }); }
      function o() { return ((R() * 5 | 0) - 2) * 3; }
      for (n = 0; n < 48; n++) { var B = this.B, a = B[R() * B.length | 0], b = B[R() * B.length | 0]; if (a === b) continue; var sx = R() < .5 ? -1 : 1, x1 = X0 + CS * (a.i + (sx > 0 ? 1 : 0)) + o(), up = R() < .5, y1 = Y0 + CS * (b.j + (up ? 0 : 1)) + o(), ya = a.cy + o(), xb = b.cx + o(); p = [[a.cx + sx * a.w / 2, ya], [x1, ya], [x1, y1], [xb, y1], [xb, b.cy + (up ? -1 : 1) * b.h / 2]]; this.RT.push({ p: p, L: plen(p), t0: 3.4 + R() * 7 }); }
      if (!this.off) { this.off = document.createElement('canvas'); this.off.width = this.off.height = 376; }
      this.Wf = []; for (j = 0; j < 11; j++) { var row = []; for (i = 0; i < 11; i++) { var px = 340 + (i - 5) * 33, py = 200 + (j - 5) * 33; if (Math.hypot(px - 340, py - 200) < 178) row.push([px, py]); } if (j % 2) row.reverse(); this.Wf = this.Wf.concat(row); }
    },
    die: function () {
      x.strokeStyle = col(.5); x.lineWidth = 1.2; x.strokeRect(X0 - 8, Y0 - 8, 376, 376); x.lineJoin = 'round'; var done = 1, T = this.T;
      this.B.forEach(function (b) {
        var u = (T - b.t0) / 1.3; if (u <= 0) { done = 0; return; } x.strokeStyle = col(.85); x.lineWidth = 1.4; var hd = part(b.p, Math.min(1, u) * b.L);
        if (u < 1) { done = 0; dot(hd[0], hd[1], 2.2, 1); }
        else { x.fillStyle = col(.1); x.fillRect(b.cx - b.w / 2, b.cy - b.h / 2, b.w, b.h); if (b.inner) { x.strokeStyle = col(.35); x.lineWidth = 1; x.beginPath(); for (var k = 1; k < 4; k++) { var yy = b.cy - b.h / 2 + b.h * k / 4; x.moveTo(b.cx - b.w / 2 + 4, yy); x.lineTo(b.cx + b.w / 2 - 4, yy); } x.stroke(); } }
      });
      this.RT.forEach(function (r) { var l = (T - r.t0) * 150; if (l <= 0) { done = 0; return; } x.strokeStyle = col(.5); x.lineWidth = 1; var hd = part(r.p, Math.min(l, r.L)); x.fillStyle = col(.95); x.fillRect(r.p[0][0] - 1.8, r.p[0][1] - 1.8, 3.6, 3.6); if (l < r.L) { done = 0; dot(hd[0], hd[1], 2.2, .95); } else x.fillRect(r.p[4][0] - 1.8, r.p[4][1] - 1.8, 3.6, 3.6); });
      return done;
    },
    draw: function (dt) {
      this.T += dt; clear(); x.save(); x.translate(this.cx, this.cy); x.scale(this.s, this.s); x.translate(-340, -200);
      if (this.ph === 0) {
        if (this.die()) { this.ft += dt; if (this.ft > 2) { var keep = x, o = this.off.getContext('2d'); o.setTransform(1, 0, 0, 1, 0, 0); o.clearRect(0, 0, 376, 376); o.translate(-(X0 - 8), -(Y0 - 8)); x = o; this.die(); x = keep; this.ph = 1; this.ft = 0; } }
      } else {
        this.ft += dt; var Wf = this.Wf, tot = Wf.length * .09, k; x.strokeStyle = col(.6); x.lineWidth = 1.5; x.beginPath(); x.arc(340, 200, 190, .12, PI - .12); x.arc(340, 200, 190, PI, 2 * PI); x.closePath(); x.stroke();
        var n = Math.min(Wf.length, Math.floor(this.ft / .09)); x.globalAlpha = this.ft > tot + 4 ? Math.max(0, 1 - (this.ft - tot - 4) / 1.2) : 1;
        for (k = 0; k < n; k++) x.drawImage(this.off, Wf[k][0] - 15, Wf[k][1] - 15, 30, 30);
        if (n < Wf.length) { x.fillStyle = col(.35); x.fillRect(Wf[n][0] - 16, Wf[n][1] - 16, 32, 32); }
        x.globalAlpha = 1; if (this.ft > tot + 5.4) { x.restore(); this.init(); return; }
      }
      x.restore();
    }
  };

  var cur = S[name]; if (!cur) { host.removeChild(cv); return; }
  var inst = { on: !('IntersectionObserver' in window),
    size: function () { var w = fixed ? innerWidth : host.clientWidth, h = fixed ? innerHeight : host.clientHeight; if (!w || !h) return; if (Math.abs(w - W) < 30 && Math.abs(h - H) < 100 && W) return; W = w; H = h; cv.width = W; cv.height = H; cur.init(); },
    draw: function (dt) { if (W) cur.draw(dt); } };
  inst.size(); INST.push(inst);
  if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { inst.on = e[e.length - 1].isIntersecting; }, { rootMargin: '80px' }).observe(host);
  }

  var hosts = document.querySelectorAll('[data-bg]'), i;
  for (i = 0; i < hosts.length; i++) { try { mount(hosts[i]); } catch (e) { if (window.console) console.error('bg-scenes', e); } }
  var last = 0, raf = 0, rz = 0;
  function frame(ms) { raf = requestAnimationFrame(frame); var t = ms / 1000; if (t - last < 1 / 31) return; var dt = Math.min(.05, t - last); last = t; for (var k = 0; k < INST.length; k++) if (INST[k].on) { try { INST[k].draw(dt); } catch (e) { INST[k].on = false; if (window.console) console.error('bg-scenes', e); } } }
  function go() { cancelAnimationFrame(raf); if (!document.hidden && INST.length) { last = performance.now() / 1000; raf = requestAnimationFrame(frame); } }
  addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { INST.forEach(function (q) { q.size(); }); }, 250); });
  document.addEventListener('visibilitychange', go); go();
  window.__bgScenes = { count: INST.length };
})();
