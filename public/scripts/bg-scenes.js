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
     motes    dust trembling in a sunbeam, knocked by unseen atoms (Brownian motion)  (Lucretius II 112-141)
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

  /* ---- motes: dust in a sunbeam, knocked about by atoms nobody sees (Lucretius II 112-141; Brownian motion) ----
     each mote follows dv = -g v dt + s sqrt(dt) xi (an Ornstein-Uhlenbeck walk): the drag g slows it, the random kicks s
     of the unseen air molecules keep it trembling; a mote is only lit while it is inside the slanting beam */
  S.motes = {
    init: function () {
      this.ax = W * .92; this.ay = -30; this.bx = W * .12; this.by = H + 30; var L = Math.hypot(this.bx - this.ax, this.by - this.ay);
      this.ux = (this.bx - this.ax) / L; this.uy = (this.by - this.ay) / L; this.bw = Math.min(64, W * .16);
      this.P = []; var n = Math.round(cl(W * H / 1500, 30, 110));
      for (var i = 0; i < n; i++) this.P.push({ x: v(0, W), y: v(0, H), vx: 0, vy: 0, r: v(.7, 2.1), h: [] });
    },
    lit: function (px, py) { var dx = px - this.ax, dy = py - this.ay, d = dx * this.uy - dy * this.ux; return Math.exp(-d * d / (this.bw * this.bw)); },
    draw: function (dt) {
      clear(); var self = this, nx = this.uy, ny = -this.ux, w = this.bw * 1.8;
      var g = x.createLinearGradient(this.ax - nx * w, this.ay - ny * w, this.ax + nx * w, this.ay + ny * w);
      g.addColorStop(0, col(0)); g.addColorStop(.5, col(.07)); g.addColorStop(1, col(0)); x.fillStyle = g; x.beginPath();
      x.moveTo(this.ax - nx * w, this.ay - ny * w); x.lineTo(this.ax + nx * w, this.ay + ny * w); x.lineTo(this.bx + nx * w, this.by + ny * w); x.lineTo(this.bx - nx * w, this.by - ny * w); x.closePath(); x.fill();
      var sd = Math.sqrt(dt);
      this.P.forEach(function (p) {
        var gm = 2.2, sg = 46 / p.r; p.vx += -gm * p.vx * dt + sg * sd * (R() + R() + R() - 1.5) * 2; p.vy += -gm * p.vy * dt + sg * sd * (R() + R() + R() - 1.5) * 2 + 1.5 * dt;
        p.x += p.vx * dt; p.y += p.vy * dt; if (p.x < -6) p.x += W + 12; if (p.x > W + 6) p.x -= W + 12; if (p.y < -6) p.y += H + 12; if (p.y > H + 6) p.y -= H + 12;
        p.h.push(p.x, p.y); if (p.h.length > 24) p.h.splice(0, 2);
        var I = self.lit(p.x, p.y); if (I < .03) return;
        x.strokeStyle = col(.22 * I); x.lineWidth = .6; x.beginPath(); x.moveTo(p.h[0], p.h[1]); for (var k = 2; k < p.h.length; k += 2) { if (Math.abs(p.h[k] - p.h[k - 2]) > 40 || Math.abs(p.h[k + 1] - p.h[k - 1]) > 40) x.moveTo(p.h[k], p.h[k + 1]); else x.lineTo(p.h[k], p.h[k + 1]); } x.stroke();
        dot(p.x, p.y, p.r, .1 + .75 * I);
      });
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
    /* a forest that starts from one tree and keeps spreading over the land until no room is left; four seasons a year (a year
       lasts 40 s); its leaves breathe vapour in summer, the vapour gathers into droplets above the canopy, droplets collide and
       merge, and the big ones fall back as rain that feeds the young trees; in winter the clouds snow */
    YEAR: 40,
    mk: function (px, G) { G.j = []; for (var i = 0; i < 97; i++) G.j.push(R()); G.len *= this.sc; G.need *= .45; return { x: px, G: G, fed: 0, mat: 0, age: 0, Rs: [], Rt: [{ x: px, y: this.GY, a: PI / 2 + v(-.3, .3), s: 0 }] }; },
    /* what lies over the land: rectangles of the page's text and cards that no crown, leaf, cloud or flake may enter */
    inOb: function (px, py, pad) { for (var i = 0; i < this.ob.length; i++) { var o = this.ob[i]; if (px > o.l - pad && px < o.r + pad && py > o.t - pad && py < o.b + pad) return true; } return false; },
    room: function (xl, xr) { var top = 0; for (var i = 0; i < this.ob.length; i++) { var o = this.ob[i]; if (o.r > xl && o.l < xr && o.t < this.GY) top = Math.max(top, Math.min(o.b, this.GY)); } return this.GY - top - 12; },
    /* a tree as tall as the free space above its spot allows: in the margins a full tree, under the buttons a low shrub */
    fit: function (px, G) {
      if (px < 14 || px > W - 14) return null; var t = this.mk(px, G), hw = 0, h = 0;
      for (var k = 0; k < 3; k++) { var o = { S: [], T: [] }; grow(t.G, px, this.GY, 1, o); var mn = this.GY, a = px, b = px;
        o.S.forEach(function (q) { mn = Math.min(mn, q[3]); a = Math.min(a, q[2]); b = Math.max(b, q[2]); }); h = this.GY - mn + 8; hw = Math.max(px - a, b - px) + 8;
        var rm = this.room(px - hw, px + hw); if (h <= rm) break; t.G.len *= rm / h * .96; }
      if (h > this.room(px - hw, px + hw) + 1 || t.G.len < 4) return null;
      if (!this.A.every(function (q) { return Math.abs(q.x - px) > Math.max(12, (q.hw + hw) * .45); })) return null;
      t.hw = hw; t.h = h; t.ls = cl(h / 140 + .3, .4, 1); return t; },
    /* roots: tips walk down through the soil, bend towards the nearest speck of rotted leaf, fork now and then */
    root: function (t, dt) {
      var top = this.GY, lim = this.GY + this.UN - 26, M = this.M, nt = t.Rt.length;
      if (t.Rs.length > (t.mat ? 170 : 90)) return;
      for (var i = 0; i < nt; i++) {
        var p = t.Rt[i]; if (p.dead) continue; var b = null, bd = 90 * 90, dep = (p.y - top) / (lim - top);
        if (!t.mat) for (var k = 0; k < M.length; k++) { var dx = M[k].x - p.x, dy = M[k].y - p.y, d = dx * dx + dy * dy; if (d < bd) { bd = d; b = M[k]; } }
        var aim = b ? Math.atan2(b.y - p.y, b.x - p.x) : (p.o ? p.home : PI / 2);
        if (dep > .8) aim = p.a < PI / 2 ? .15 : PI - .15;
        var da = Math.atan2(Math.sin(aim - p.a), Math.cos(aim - p.a));
        p.a += da * (b ? 1.4 : .7) * dt + (R() - .5) * 1.8 * dt; p.a = cl(p.a, .08, PI - .08);
        var sp = (t.mat ? 7 : 13) * dt / (1 + .35 * (p.o || 0)), nx = p.x + Math.cos(p.a) * sp, ny = p.y + Math.sin(p.a) * sp; p.s += sp;
        if (ny > lim + 6 || nx < 4 || nx > W - 4 || p.s > 400) { p.dead = 1; continue; }
        if (p.s > 6) { t.Rs.push([p.lx, p.ly, nx, ny, p.o || 0]); p.lx = nx; p.ly = ny; p.s = 0; p.n = (p.n || 0) + 1;
          if (t.Rt.length < 16 && (p.o || 0) < 3 && p.n % 3 === 0 && R() < .7) { var sd = R() < .5 ? -1 : 1; t.Rt.push({ x: nx, y: ny, a: p.a + sd * v(.7, 1.2), home: PI / 2 - sd * v(.6, 1.1), s: 0, lx: nx, ly: ny, o: (p.o || 0) + 1 }); } }
        p.x = nx; p.y = ny;
      }
    },
    roots: function (Rs, a) { var top = this.GY, U = this.UN - 26; for (var i = 0; i < Rs.length; i++) { var r = Rs[i], f = 1 - cl((r[3] - top) / U, 0, 1); x.strokeStyle = col(a * (.6 - Math.min(.3, r[4] * .1)) * (.25 + .75 * f)); x.lineWidth = Math.max(.6, 2.4 - r[4] * .55); ln(r[0], r[1], r[2], r[3]); } },
    ripen: function (t) { var o = { S: [], T: [] }; grow(t.G, t.x, this.GY, 1, o); t.S = o.S; t.T = o.T.map(function (q) { return { x: q.x, y: q.y, a: q.a, s: 1, rg: 0 }; }); t.mat = 1; t.age = 0; t.life = v(2.5, 4) * this.YEAR; },
    seed: function (near) { for (var k = 0; k < 14; k++) { var px = near && R() < .65 ? near.x + (R() < .5 ? -1 : 1) * v(near.hw * .6 + 10, near.hw + 240) : v(14, W - 14), t = this.fit(px, KINDS[R() * 5 | 0]()); if (t) { this.A.push(t); return t; } } return null; },
    init: function () {
      this.UN = W > 760 ? (+host.getAttribute('data-bg-under') || 0) : 0; this.Hn = []; this.GY = H - 46 - this.UN; this.Fd = []; this.sc = cl(H / 520, .8, 1.7);
      this.A = []; this.L = []; this.M = []; this.ob = []; this.V = []; this.Y = 0; this.sn = new Float32Array(Math.ceil(W / 12) + 1); this.sky = W > 760;
      var self = this, hr = host.getBoundingClientRect();
      [host.getAttribute('data-bg-avoid'), host.getAttribute('data-bg-avoid-near')].forEach(function (q) { if (q) document.querySelectorAll(q).forEach(function (e) { var r = e.getBoundingClientRect(); if (r.width && r.height) self.ob.push({ l: r.left - hr.left - 14, r: r.right - hr.left + 14, t: r.top - hr.top - 10, b: r.bottom - hr.top + 10 }); }); });
      var m = null; for (var q = 0; q < 80 && !m; q++) { var g = KINDS[0](); g.len = 64; g.maxd = 6; m = this.fit(q ? v(14, W - 14) : Math.max(46, W * .1), g); }
      if (m) { this.A.push(m); this.ripen(m); m.life = 2.5 * this.YEAR; } },
    draw: function (dt) {
      clear(); var GY = this.GY, self = this; this.Y += dt; var ph = (this.Y / this.YEAR) % 1, sea = ph * 4 | 0;
      x.strokeStyle = col(.25); x.lineWidth = 1; for (var g0 = 0; g0 < W; g0 += 8) if (!this.inOb(g0 + 4, GY, 0)) ln(g0, GY, g0 + 8, GY);
      /* snow lying on the ground, melting in spring */
      var sn = this.sn; x.fillStyle = col(.16); for (var b = 0; b < sn.length; b++) { if (sea === 0 || sea === 1) sn[b] = Math.max(0, sn[b] - dt * .3); if (sn[b] > .3) x.fillRect(b * 12, GY - sn[b], 12, sn[b]); }
      if (this.UN) { this.Fd = this.Fd.filter(function (f) { f.a -= dt / 7; if (f.a > 0) self.roots(f.Rs, f.a); return f.a > 0; }); x.lineCap = 'round'; this.A.forEach(function (t) { self.root(t, dt); self.roots(t.Rs, 1); }); x.lineCap = 'butt'; }
      var leaves = 0;
      this.A.forEach(function (t) {
        x.strokeStyle = col(.6);
        if (t.mat) {
          t.age += dt; t.S.forEach(function (s) { x.lineWidth = Math.max(.6, (3.8 - s[4] * .65) * cl(t.h / 160, .45, 1)); ln(s[0], s[1], s[2], s[3]); });
          if (sea === 3) { x.strokeStyle = col(.18); x.lineWidth = 1.6; t.S.forEach(function (s, i) { if (s[4] > 1 && i % 2 && sn[(s[2] / 12) | 0] > 1) ln(s[0], s[1] - 1.5, s[2], s[3] - 1.5); }); }
          t.T.forEach(function (tp) {
            if (sea === 2) { if (tp.s >= 1 && R() < dt * .45) { tp.s = 0; tp.rg = null; self.L.push({ x: tp.x, y: tp.y, ph: R() * 6, t: 0, w: v(-26, 34) }); } }
            else if (sea === 0 || sea === 1) { if (tp.rg === null) tp.rg = v(0, 5); if (tp.s < 1) { if (tp.rg > 0) tp.rg -= dt; else tp.s = Math.min(1, tp.s + dt / 1.2); }
              else if (sea === 1 && R() < dt * .012) { tp.s = 0; tp.rg = v(1, 4); self.L.push({ x: tp.x, y: tp.y, ph: R() * 6, t: 0, w: v(-26, 34) }); } }
            if (tp.s > 0) { leaf(tp.x, tp.y, tp.a, tp.s * t.ls, sea === 2 ? .38 : .6); if (tp.s >= 1) leaves++; }
            if (sea < 2 && tp.s >= 1 && self.sky && t.h > 90 && self.room(tp.x - 1, tp.x + 1) > GY * .6 && R() < dt * .14) self.V.push({ x: tp.x, y: tp.y, r: .5, q: 0 });
          });
          if (sea < 2 && R() < dt * .25 && self.A.length < 90) self.seed(t);
          if (t.age > t.life) { t.dead = 1; if (self.UN) self.Fd.push({ Rs: t.Rs, a: 1 }); t.S.forEach(function (s, i) { if (i % 2 === 0) self.L.push({ x: (s[0] + s[2]) / 2, y: (s[1] + s[3]) / 2, ph: R() * 6, t: 0, w: v(-10, 10) }); }); }
        } else { if (sea < 2) t.fed += dt * t.G.need / 6; var g = Math.min(1, t.fed / t.G.need); if (g <= 0) dot(t.x, GY, 1.5, .5); else grow(t.G, t.x, GY, g, null); if (g >= 1) self.ripen(t); }
      });
      this.A = this.A.filter(function (t) { return !t.dead; }); if (!this.A.length) this.seed(null);
      this.L = this.L.filter(function (l) { l.t += dt; l.y += 32 * dt; var w = l.ph + l.t * 2.4; l.x += (l.w + Math.cos(w) * 34) * dt; if (self.inOb(l.x, l.y, 4) || l.x < -10 || l.x > W + 10) return false; if (l.y >= GY - 2) { for (var k = 0; k < 4; k++) self.M.push({ x: l.x + v(-4, 4), y: GY, ty: GY + 6 + R() * (self.UN ? (self.UN - 40) * R() : 22) }); return false; } leaf(l.x, l.y, w, 1, .45); return true; });
      /* the sky: vapour rises to the cloud layer; droplets wander, collide and merge (volume is kept, r = cube root); the speed
         of fall grows as r squared (Stokes), so only merged drops beat the updraft and fall, sweeping up small ones on the way */
      var V = this.V, cb = Math.max(70, GY * .16), ct = cb + 60, up = sea === 1 ? 7 : sea === 0 ? 4 : 2;
      for (var a = 0; a < V.length; a++) { var d = V[a]; if (d.dead) continue;
        if (!d.q) { d.y -= 90 * dt; d.x += (R() - .5) * 10 * dt; if (d.y < v(cb, ct)) { d.q = 1; d.r = .7; } if (!d.q) { dot(d.x, d.y, .6, .22); continue; } }
        if (sea === 3 && !d.snow) { if (R() < dt * .8) { V.push({ x: d.x, y: d.y, r: .5, q: 1, snow: 1 }); d.r = Math.cbrt(Math.max(0, d.r * d.r * d.r - .125)); } if (d.r < .55) d.snow = 1; }
        var snow = d.snow, vt = snow ? 60 : 9 * d.r * d.r - up, nx = d.x + (R() - .5) * 8 * dt + (snow ? Math.sin(self.Y * 2 + a) * 8 * dt : 0), ny = d.y + vt * dt;
        if (self.inOb(nx, ny, 6) || nx < 2 || nx > W - 2) { d.x -= (nx - d.x) * 2; } else { d.x = nx; } d.y = Math.max(cb - 20, ny);
        if (d.y >= GY) { d.dead = 1; if (snow) sn[(cl(d.x, 0, W - 1) / 12) | 0] = Math.min(5, sn[(cl(d.x, 0, W - 1) / 12) | 0] + .6);
          else if (d.r > 1.3) self.A.forEach(function (t) { if (!t.mat && Math.abs(t.x - d.x) < 70) t.fed += 2 * d.r; }); continue; }
        if (snow) { x.strokeStyle = col(.4); x.lineWidth = .8; ln(d.x - 2, d.y, d.x + 2, d.y); ln(d.x - 1, d.y - 1.7, d.x + 1, d.y + 1.7); ln(d.x - 1, d.y + 1.7, d.x + 1, d.y - 1.7); continue; }
        for (var b2 = a + 1; b2 < V.length; b2++) { var e = V[b2]; if (e.dead || !e.q || e.snow) continue; var dx = e.x - d.x, dy = e.y - d.y, rr = d.r + e.r + 1.2; if (dx * dx + dy * dy < rr * rr * 4) { d.r = Math.cbrt(d.r * d.r * d.r + e.r * e.r * e.r); e.dead = 1; } }
        if (sea < 3 && d.y < ct + 20) d.r += dt * .06;
        if (vt > 30) { x.strokeStyle = col(.45); x.lineWidth = d.r * .8; ln(d.x, d.y - 6, d.x, d.y); } else dot(d.x, d.y, d.r, .45);
      }
      this.V = V.filter(function (d) { return !d.dead; }); if (this.V.length > 500) this.V.splice(0, this.V.length - 500);
      if (this.M.length > 700) this.M.splice(0, this.M.length - 700);
      if (this.UN) { var U = this.UN, Hn = this.Hn;
        /* the fungal network: threads in the soil tie the root systems of trees far apart; sugar runs along them from grown
           trees to young ones, as in a real wood-wide web, and feeds them */
        this.ht = (this.ht || 0) - dt;
        if (this.ht <= 0 && Hn.length < 9) { this.ht = 1.5; var C = this.A.filter(function (k) { return k.Rs.length >= 8; }), best = null, bd = 0;
          for (var a = 0; a < C.length; a++) for (var b = a + 1; b < C.length; b++) { var d = Math.abs(C[a].x - C[b].x) * v(.6, 1); if (d > bd && !Hn.some(function (h) { return (h.a === C[a] && h.b === C[b]) || (h.a === C[b] && h.b === C[a]); })) { bd = d; best = [C[a], C[b]]; } }
          if (best && bd > 60) { var ra = best[0].Rs[(best[0].Rs.length * v(.3, 1)) | 0], rb = best[1].Rs[(best[1].Rs.length * v(.3, 1)) | 0], P = [], n = 60, sag = v(10, U * .4), ph = R() * 6, w1 = v(2, 5);
            for (var q = 0; q <= n; q++) { var u = q / n; P.push([ra[2] + (rb[2] - ra[2]) * u + 4 * Math.sin(u * 17 + ph), Math.min(GY + U - 28, ra[3] + (rb[3] - ra[3]) * u + sag * Math.sin(PI * u) + 3 * Math.sin(u * w1 * 6 + ph))]); }
            Hn.push({ a: best[0], b: best[1], P: P, g: 0, f: 1, et: v(.5, 2), D: [] }); } }
        x.lineWidth = .7;
        this.Hn = Hn.filter(function (h) {
          if (h.a.dead || h.b.dead) h.f -= dt / 5; else h.g = Math.min(1, h.g + dt / 10); if (h.f <= 0) return false;
          var m = Math.max(1, Math.round(h.g * 60)); x.strokeStyle = col(.22 * h.f); x.beginPath(); x.moveTo(h.P[0][0], h.P[0][1]); for (var q = 1; q <= m; q++) x.lineTo(h.P[q][0], h.P[q][1]); x.stroke();
          if (h.g >= 1 && h.f >= 1) { h.et -= dt; if (h.et <= 0) { h.et = v(1, 2.6); var fw = h.a.mat && !h.b.mat ? 1 : h.b.mat && !h.a.mat ? -1 : (R() < .5 ? 1 : -1); h.D.push({ u: fw > 0 ? 0 : 60, d: fw }); } }
          h.D = h.D.filter(function (o) { o.u += o.d * 26 * dt; if (o.u < 0 || o.u > 60) { var to = o.d > 0 ? h.b : h.a; if (!to.mat) to.fed += 3; return false; } var q = o.u | 0, e = o.u - q, A = h.P[q], B = h.P[Math.min(60, q + 1)]; dot(A[0] + (B[0] - A[0]) * e, A[1] + (B[1] - A[1]) * e, 1.3, .75 * h.f); return true; });
          return true; });
        this.M = this.M.filter(function (m) {
        var bp = null, bk = null, bd = 120 * 120;
        for (var j = 0; j < self.A.length; j++) { var k = self.A[j]; if (k.mat) continue; for (var q = 0; q < k.Rt.length; q++) { var p = k.Rt[q], dx = p.x - m.x, dy = p.y - m.y, d = dx * dx + dy * dy; if (d < bd) { bd = d; bp = p; bk = k; } } }
        m.age = (m.age || 0) + dt; if (m.y < m.ty - 1) m.y += (m.ty - m.y) * dt * .8;
        else if (bp) { var dd = Math.sqrt(bd); if (dd < 5) { bk.fed++; return false; } m.x += (bp.x - m.x) / dd * 16 * dt; m.y += (bp.y - m.y) / dd * 16 * dt; }
        var fa = cl((70 - m.age) / 20, 0, 1); if (fa <= 0) return false;
        dot(m.x, m.y, 1.1, fa * .55 * (1 - .6 * cl((m.y - GY) / U, 0, 1))); return true; }); return; }
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

  var cur = S[name]; if (!cur) { host.removeChild(cv); return; } host.__bgScene = cur;
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
