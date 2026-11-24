NEON REQUEST N-1: the ten cloud genera, built in 3D and seen from the ground, in the forest's sky and in a cloud-atlas scene

GOAL (plain words, and why)
The website Phyein Usul (repository Numa1997/SiteTest, branch `sky-and-wind`, made from main at commit 5b09422) draws small
"living scenes" on its pages with one script, public/scripts/bg-scenes.js (attached whole below). The home page's forest scene
(`S.forest`) has a sky in the two top corners of the page. Its clouds are now all one kind, a cumulus: round puffs on a flat base at
1000 m, built in 3D and projected into the eye of someone standing on the ground (functions proj, cloud, seen, join, paint inside
S.forest). The user finds them not good enough and asks for every kind of cloud, "the very large, the very long, the thin",
according to shape and form, included in the animations. So:
1. Write a new file public/scripts/bg-sky.js: a small cloud atlas. It builds each of the ten WMO cloud genera as a 3D object at its
   true height and draws it, seen from the ground, through the same pinhole camera the forest uses.
2. Change S.forest in bg-scenes.js so its sky holds a mix of genera that follows the seasons and the forest's water, using bg-sky.js.
3. Add one new scene, `atlas`, to bg-scenes.js: the ten genera side by side at their heights, each labelled, for the scenes page.
4. Add the atlas as section S13 to public/scenes.html and rewrite the forest's text there (S1) to describe the new sky.

THE TEN GENERA (WMO International Cloud Atlas, 2017; levels for temperate latitudes, table 6 of the Atlas: low from the ground to
2 km, middle 2 to 7 km, high 5 to 13 km). Each is a generator of a 3D object in metres, in its own frame, then projected. Shape and
form, which is what the drawing must show:
- Cumulus (Cu), low, base 0.6–1.5 km: detached heaps, flat dark base, domed top of rounded puffs ("cauliflower"); 0.3–1.5 km wide,
  about as tall as wide. (The current generator; keep its look: opaque puffs pale where light falls, flat underside seen from below.)
- Cumulonimbus (Cb), low base ~1 km, top up to 10–12 km: the very large one. A tower of puffs several km wide, widening upward,
  topped by a flat anvil (incus) spreading sideways at its top, dark ragged base with a rain shaft (or snow) falling from it.
  Rare; in the forest it grows out of a cumulus that has gathered much water, in summer.
- Stratocumulus (Sc), low 0.5–2 km: the very long one. Grey-white patches, rolls or rounded masses joined into rows that run for
  many km, with gaps of sky between rolls; the rolls are flattened lumps (wider than tall), lined up in long parallel bands.
- Stratus (St), low 0.1–0.5 km: a flat, featureless grey layer with a fairly uniform base, ragged at its edges (fractus pieces).
- Nimbostratus (Ns), base ~0.5–2 km, several km thick: a dark grey, diffuse layer, its base blurred by falling rain or snow that
  reaches the ground. Cold season.
- Altocumulus (Ac), middle 2–6 km: a field of many small rounded masses or rolls ("sheep"), each about 100–300 m, in rows or a loose
  grid with gaps, shaded on one side. In perspective the field shrinks toward the horizon: this is where the 3D shows best.
- Altostratus (As), middle 3–6 km: a uniform grey-bluish sheet, fibrous or striated, covering much of the sky, thin enough that the
  sun shows as through ground glass (no halo).
- Cirrus (Ci), high 6–12 km: the thin one. Detached white filaments: fibres, hooks ("mares' tails", uncinus) and strands, silky;
  drawn as thin curved strokes, each a hook: a long straight fall streak bending at one end.
- Cirrocumulus (Cc), high 6–12 km: a thin layer of very small grains or ripples, regular rows ("mackerel sky"), each element
  appearing less than 1° wide.
- Cirrostratus (Cs), high 6–12 km: a transparent whitish veil, fibrous or smooth, covering much of the sky; it may show a halo of
  22° around the sun (optional: a faint ring).

THE CAMERA (keep exactly as now; it is in S.forest): the eye stands on the ground at the holder's horizontal middle XC = W/2; the
horizon is the ground line GY (px from the holder's top). A point X m to the right, Y m up, Z m in front of the eye is seen at
x = XC + F X / Z, y = GY − F Y / Z, with F = GY (px). Layers (St, As, Cs, Ns, Sc fields) are horizontal planes at their height; their
elements are laid on the plane and projected, so they crowd and shrink toward the horizon. Use depths Z from about 0.5 to 40 km so
high clouds and layers reach down near the horizon; anything that projects below the forest's open sky is not drawn.

WHERE THE SKY IS: the forest computes its open sky (this.CL, band(px): for each 16 px column the rows from b.t to b.b where clouds may
be; null where text stands). Today a cloud is faded out over text. With layers and wide clouds, use a mask instead: draw the whole
sky into an offscreen canvas, then lay it on the page through a soft mask made from the open-sky columns (each column's band, its edges
feathered over about 40 px, horizontally and vertically), so nothing is drawn over text and edges are soft, never cut.

HOW THE FOREST'S SKY BEHAVES (the physics stays as documented in docs/scripts/bg-scenes.md, "Clouds in 3D"):
- Low heaps (Cu) keep today's water bookkeeping: vapour from the leaves and the ground joins a cloud or starts one; a cloud's size
  follows its water (s = SIZE ∛m, settling over 5 s); condensation grows its mean droplet radius; grown droplets fall as rain from
  under its base (Stokes, speed 9 r² − updraft); evaporation EVAP; winter snow. A cumulus whose water passes a threshold CB (new
  named parameter) in summer grows over about 30 s into a cumulonimbus: its tower rises, its anvil spreads, it rains hard, then it
  decays. At most one at a time on a page.
- The other genera are the weather of the season, not fed by the forest: spring: Cu with Ac and some Ci; summer: Cu, now and then a
  Cb, Ci; autumn: As thickening to Ns with long rain, Sc rows; winter: St and Ns with snow, Cs. Each genus fades in and out over
  10–20 s as the season turns, so the sky changes smoothly. Use a table in the code (season × genus → how much), named at the top.
- Wind: one wind per level (low, middle, high), each wandering slowly (as this.U now); higher winds stronger (named parameters).
  Clouds drift with their level's wind; perspective gives parallax by itself. When a cloud drifts out of the sky it is replaced by a
  new one entering from the side it left, so the sky never empties.
- Everything is smooth: sizes, positions and opacity change continuously; no cloud pops in or out.
- The drawing stays in the house palette: wine (C = '122,31,43') on paper (245,241,234), with the helpers col(a) and mixc(t, a) that
  bg-scenes.js already has (pass them to bg-sky.js or copy them). Clouds are pale paper-wine, bases and rain deeper. No other colours.

THE ATLAS SCENE (new, `S.atlas` in bg-scenes.js, only on the scenes page): a sky box seen from the ground with the ten genera at their
heights, low ones lower and nearer, high ones higher; each labelled in IBM Plex Mono 10 px with its abbreviation, name and height
range (for example "Ci · Cirrus · 6–12 km"); all drifting slowly with their winds; on the left edge a small height ruler (0, 2, 7,
13 km) drawn as thin lines, so the three levels read at a glance. A knob table K as the other scenes have (for example the wind of
each level, the camera's tilt if you add one), and the scene restarts on restart knobs. The forest's sky and the atlas use the same
generators from bg-sky.js.

LOADING bg-sky.js: bg-scenes.js loads it itself the first time a forest or atlas holder mounts (a <script src> next to its own
script's src, deferred until loaded; the scenes wait for it). No HTML page needs another script tag. The page's Content-Security-Policy
is script-src 'self' 'unsafe-inline', so a same-origin script element is allowed.

RULES THAT BIND THE CODE
- ES5 style as in bg-scenes.js (var, function, no modules, no build step); one IIFE; no libraries; no other fonts (IBM Plex Mono for
  labels only); no console errors; works from 390 px to 2560 px wide.
- Keep every existing interface: mount(), the K tables and properties of every scene, host.__bgScene, host.__bgRestart, sceneData(),
  the rails, pairs and roots scenes, the reduced-motion rule (with prefers-reduced-motion: reduce nothing mounts), the
  IntersectionObserver that runs only visible scenes, data-bg-* attributes. Do not change other scenes.
- Every number of the sky named at the top of S.forest (or of bg-sky.js) with a comment saying what it is and its unit, like the
  existing ones (YEAR, GROW, ... HB, SIZE, WIND, NCL, EVAP, TONE); add K rows for the new ones a reader would want to play with.
- Comments explain the physics and the drawing in plain words (the file's comments are read as documentation by non-programmers).
- Speed: the forest with its sky must keep 60 frames per second on a laptop at 1920 × 1080; draw layers and fields cheaply (for
  example render each layer to its own offscreen canvas only when it moves by a pixel, or draw elements as small sprites).

THE TESTS I WILL RUN ON YOUR ANSWER
1. node -e "require('vm').createScript(require('fs').readFileSync('public/scripts/bg-scenes.js','utf8'))" and the same for
   public/scripts/bg-sky.js (syntax).
2. npm run build (Vite copies public/ to dist/).
3. notes/home/scenes/film.cjs: the home page in headless Chromium at 1920, 1600 and 1100 px for 180 s, screenshots at 3, 30, 60, 90,
   120, 150 and 180 s (all four seasons pass, a year is 120 s); I look at every one: all genera appear over the year, nothing over text,
   no hard edges, smooth.
4. notes/home/scenes/check.cjs: home (English, German, Arabic), scenes, simulations, Portfolios and Lucretius pages at 1920, 1600,
   1100 and 390 px, and with reduced motion: no page errors, no sideways scroll, nothing mounted under reduced motion.
5. notes/home/scenes/each.cjs: every scene of scenes.html after 8 s in view, including S13 atlas: all ten genera visible and labelled.
6. Frames per second of the home page at 1920 × 1080 in headless Chromium over 10 s (counting requestAnimationFrame callbacks): at
   least 50.

ANSWER FORMAT
For each file, one fenced block whose first line is "FILE: <path>" followed by the complete new file (not a diff, not a fragment);
nothing else inside the blocks. The files: public/scripts/bg-sky.js (new), public/scripts/bg-scenes.js (whole), public/scenes.html
(whole). After the blocks, a short list of what changed.

THE FILES (whole, as they stand on the branch)

----- public/scripts/bg-scenes.js -----
```
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

  /* ---- stored simulation data (docs/kaggle-sims.md): computed once on Kaggle, kept under data/sims/<name>/<date>/ on this site. A scene asks
     for its data by name; the newest generation of that scene is downloaded, its SHA-256 is checked against generations.json, and
     only then is it handed over. The file: 4 bytes of label, a uint32 header length, a JSON header, then int16 frames. ---- */
  var DATA = new URL('../data/sims/', (document.currentScript || {}).src || location.href).href, GEN = null, STORE = {};
  function sceneData(name, file) {
    if (STORE[name]) return STORE[name];
    GEN = GEN || fetch(DATA + 'generations.json').then(function (r) { if (!r.ok) throw new Error('no generations.json'); return r.json(); });
    return STORE[name] = GEN.then(function (g) {
      var e = g.generations.filter(function (q) { return q.sim === name; }).pop(); if (!e) throw new Error('no data for ' + name);
      return fetch(DATA + name + '/' + e.date + '/' + file).then(function (r) { if (!r.ok) throw new Error(file + ' ' + r.status); return r.arrayBuffer(); }).then(function (buf) {
        return crypto.subtle.digest('SHA-256', buf).then(function (d) {
          var hex = Array.prototype.map.call(new Uint8Array(d), function (b) { return (b < 16 ? '0' : '') + b.toString(16); }).join('');
          if (hex !== e.files[file].sha256) throw new Error(file + ': SHA-256 differs from generations.json');
          var hl = new DataView(buf).getUint32(4, true), hdr = JSON.parse(new TextDecoder().decode(new Uint8Array(buf, 8, hl)));
          return { hdr: hdr, frames: new Int16Array(buf.slice(8 + hl)), cols: hdr.columns.length, gen: e, sha_ok: true };
        });
      });
    });
  }

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
  function mixc(t, a) { return 'rgba(' + Math.round(245 - 123 * t) + ',' + Math.round(241 - 210 * t) + ',' + Math.round(234 - 191 * t) + ',' + a + ')'; }   /* paper (t = 0) to wine (t = 1), opaque by a */
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
    DRAG: 2.2, KICK: 46, BEAM: 64,
    K: [['DRAG', 'drag γ', '1/s', .3, 8, .1], ['KICK', 'kick strength σ (for a 1 px mote)', 'px/s^1.5', 0, 140, 1], ['BEAM', 'width of the sunbeam', 'px', 20, 160, 1, 1]],
    init: function () {
      this.ax = W * .92; this.ay = -30; this.bx = W * .12; this.by = H + 30; var L = Math.hypot(this.bx - this.ax, this.by - this.ay);
      this.ux = (this.bx - this.ax) / L; this.uy = (this.by - this.ay) / L; this.bw = Math.min(this.BEAM, W * .16);
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
        var gm = self.DRAG, sg = self.KICK / p.r; p.vx += -gm * p.vx * dt + sg * sd * (R() + R() + R() - 1.5) * 2; p.vy += -gm * p.vy * dt + sg * sd * (R() + R() + R() - 1.5) * 2 + 1.5 * dt;
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
    FALL: 130, EVERY: .7, LIFE: 17,
    K: [['FALL', 'speed of a falling seed', 'px/s', 30, 300, 1], ['EVERY', 'time between seeds', 's', .2, 4, .1], ['LIFE', 'life of a plant', 's', 6, 60, 1]],
    init: function () { this.S = []; this.Pl = []; this.tm = 0; },
    draw: function (dt) {
      clear(); var G = H - 12, self = this, k = W / 680; this.tm += dt;
      if (this.tm > this.EVERY / k && this.Pl.length < 26 * k) { this.tm = 0; this.S.push({ x: v(20, W - 20), y: -5, type: R() * 3 | 0 }); }
      x.strokeStyle = col(.25); x.lineWidth = 1; ln(0, G, W, G);
      this.S = this.S.filter(function (s) { s.y += self.FALL * dt; dot(s.x, s.y, 2, .8); if (s.y >= G) { self.Pl.push({ x: s.x, type: s.type, age: 0, h: v(.22, .62) * H, sw: R() * 6, life: self.LIFE }); return false; } return true; });
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
    FALL: 90, EVERY: 2.6,
    K: [['FALL', 'speed of the falling atoms', 'px/s', 20, 240, 1, 1], ['EVERY', 'time between swerves', 's', .3, 10, .1]],
    init: function () { clear(); this.A = []; var per = Math.ceil(H / 67); for (var c = 0; c * 20 + 10 < W; c++) for (var i = 0; i < per; i++) { var x0 = 10 + c * 20; this.A.push({ x0: x0, x: x0, y: R() * H, vx: 0, vy: this.FALL, hot: 0, cd: 0 }); } this.tm = 1.5; },
    draw: function (dt) {
      fade(.13); this.tm += dt; var A = this.A, n = A.length, i, j, self = this;
      if (this.tm > this.EVERY / Math.max(1, area() / 2)) { this.tm = 0; var a0 = A[R() * n | 0]; a0.vx = (R() < .5 ? -1 : 1) * v(18, 44); a0.hot = 1; }
      for (i = 0; i < n; i++) {
        var a = A[i]; a.cd -= dt; if (!a.hot || a.cd > 0) continue;
        for (j = 0; j < n; j++) { var b = A[j]; if (j === i || b.cd > 0) continue; var dx = a.x - b.x, dy = a.y - b.y; if (dx * dx + dy * dy < 40) { var s = dx >= 0 ? 1 : -1; a.vx += s * v(15, 45); b.vx -= s * v(15, 45); a.vy = self.FALL + v(-25, 25); b.vy = self.FALL + v(-25, 25); b.hot = 1; a.cd = b.cd = .35; break; } }
      }
      for (i = 0; i < n; i++) { a = A[i]; a.x += a.vx * dt; a.y += a.vy * dt; if (a.x < 0) a.x += W; if (a.x > W) a.x -= W; if (a.y > H + 5) { a.y = -5; a.x = a.x0; a.vx = 0; a.vy = self.FALL; a.hot = 0; } dot(a.x, a.y, a.hot ? 2.3 : 1.2, a.hot ? .9 : .35); }
    }
  };

  /* ---- shores of light ---- */
  S.shores = {
    DENS: 120, RISE: 1,
    K: [['DENS', 'motes per 680 × 400 px', '', 20, 400, 1, 1], ['RISE', 'speed of rising (× 12 to 32 px/s)', '×', 0, 4, .05]],
    init: function () { this.M = []; var n = Math.min(520, this.DENS * area()); for (var i = 0; i < n; i++) this.M.push({ x: R() * W, y: R() * H, v: v(12, 32), ph: R() * 6 }); this.t = 0; },
    draw: function (dt) {
      clear(); this.t += dt; var t = this.t, y0 = H * .58, q;
      function ys(q) { return y0 + 10 * Math.sin(q * .012 + t * .5) + 6 * Math.sin(q * .031 - t * .8); }
      x.beginPath(); x.moveTo(0, H); for (q = 0; q <= W; q += 8) x.lineTo(q, ys(q)); x.lineTo(W, H); x.closePath(); x.fillStyle = col(.10); x.fill();
      [0, 14, 30, 50].forEach(function (o, i) { x.beginPath(); for (var q = 0; q <= W; q += 8) { var yy = ys(q + o * 3) + o; if (q) x.lineTo(q, yy); else x.moveTo(q, yy); } x.strokeStyle = col(.55 - .13 * i); x.lineWidth = 1; x.stroke(); });
      var rise = this.RISE; this.M.forEach(function (m) { m.y -= m.v * rise * dt; m.x += Math.sin(t + m.ph) * 8 * dt; if (m.y < -5) { m.y = H + 5; m.x = R() * W; } var s = ys(m.x), a = .18, r = 1; if (m.y < s) { var k = Math.min(1, (s - m.y) / 60); a = (.2 + .7 * k) * Math.min(1, m.y / 60); r = 1 + 1.6 * k; } dot(m.x, m.y, r, a); });
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
    /* a forest that starts from a few trees and spreads slowly over the land until no room is left; four seasons a year; its
       leaves breathe vapour in spring and summer, the vapour rises into the open sky of the two top corners (where no text stands)
       and gathers there into clouds of droplets that collide and merge; the big ones fall back as rain that feeds the young trees;
       in winter the clouds snow.
       The pace (23 November 2026, the user: the trees shot up, the land filled in 80 s). Every number of the pace is here:
         YEAR       s      one year: spring, summer, autumn, winter, a quarter each (was 40 s)
         GROW       s      light a seedling needs to become a grown tree; it grows only in spring and summer, so with YEAR 120 a
                           tree takes about one growing season, a minute of the reader's time (was 6 s)
         SEED       1/s    seeds thrown by each grown tree per second of spring and summer (was 0.25); with YEAR 120 that is about
                           2.4 a season, most of which find no room; the land fills in four to six years, 8 to 12 minutes
         FEED       -      share of the extra food (rain, rotted leaves, sugar through the fungus) that counts towards growth (was 1)
         START      -      grown trees standing when the page opens, so the land is never bare
         LIFE       years  a grown tree's life span, drawn at random between the two
         FALL       1/s    in autumn, chance per second that a leaf lets go (scaled with YEAR: 0.45 at YEAR 40)
       The weather in the corners (23 and 24 November 2026; documented in docs/scripts/bg-scenes.md, "Clouds in 3D"):
         COND       px/s   growth of a cloud's mean droplet radius by condensation
         RAIN       1/s    rain from a cloud: raindrops per second per unit of water, times how far the mean droplet radius has
                           grown past 0.6 px (collision and coalescence need grown droplets)
         SOIL       1/s    vapour from the bare ground under open sky in spring and summer, per 100 px of it
         OPEN       px     least height of open sky a 16 px column needs to hold clouds (at most 30 % of the ground height)
         HB         m      height of the cloud base above the ground (all clouds share it, as a real cloud field does)
         SIZE       m      size of a cloud holding one unit of water; a cloud's size grows as the cube root of its water
         WIND       m/s    spread of the slowly wandering wind that carries the clouds
         NCL        px²    open sky per cloud when the page opens
         EVAP       s      a cloud loses its water to the dry air around it with this time constant, so supply and loss settle
                           into a sky that is neither clear nor overcast (water ≈ supply × EVAP)
         TONE       -      how strongly a whole cloud is drawn over the paper (its body is opaque inside, then faded as one) */
    K: [['YEAR', 'length of a year', 's', 20, 480, 5], ['GROW', 'light a seedling needs to grow up', 's', 5, 200, 1], ['SEED', 'seeds per grown tree per second of spring and summer', '1/s', 0, .3, .005],
        ['FEED', 'share of rain and rotted leaves that feeds growth', '', 0, 1, .05], ['COND', 'condensation in the clouds', 'px/s', 0, .05, .001], ['RAIN', 'rain from grown droplets', '1/s', 0, 2, .05], ['SOIL', 'vapour from open ground', '1/s per 100 px', 0, 3, .05],
        ['HB', 'height of the cloud base', 'm', 300, 3000, 50, 1], ['SIZE', 'size of a cloud per unit of water', 'm', 30, 250, 5, 1], ['WIND', 'wind', 'm/s', 0, 15, .5], ['NCL', 'open sky per cloud at the start', 'px²', 8000, 80000, 1000, 1], ['EVAP', 'how long a cloud keeps its water', 's', 10, 600, 5]],
    YEAR: 120, GROW: 50, SEED: .04, FEED: .25, START: 3, LIFE: [2.5, 4], FALL: .15, COND: .003, RAIN: .08, SOIL: .6, TONE: .42, EVAP: 90, OPEN: 240, HB: 1000, SIZE: 95, WIND: 4, NCL: 25000,
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
    ripen: function (t) { var o = { S: [], T: [] }; grow(t.G, t.x, this.GY, 1, o); t.S = o.S; t.T = o.T.map(function (q) { return { x: q.x, y: q.y, a: q.a, s: 1, rg: 0 }; }); t.mat = 1; t.age = 0; t.life = v(this.LIFE[0], this.LIFE[1]) * this.YEAR; },
    /* the open sky: for every 16 px column, from 30 px below the top of the page down to 30 px above the first text or card
       in that column (or to 55 % of the ground height); a column with less than OPEN px of open sky has no clouds. On a wide
       screen this leaves the two top corners: left of the hero text and right of the poem and the Fig. 0 card. */
    clouds: function () {
      var CL = [], n = Math.ceil(W / 16), self = this, i, k;
      for (i = 0; i < n; i++) { var xl = i * 16, xr = xl + 16, flo = this.GY * .55;
        for (k = 0; k < this.ob.length; k++) { var o = this.ob[k]; if (o.r > xl && o.l < xr) flo = Math.min(flo, o.t); }
        CL.push(flo - 30 - 30 >= Math.min(this.OPEN, this.GY * .3) ? { t: 30, b: flo - 30 } : null); }
      this.CL = CL;
      if (this.sky) { var cols = []; CL.forEach(function (c, i) { if (c) cols.push(i); });
        /* clouds already in the sky when the page opens, about one per NCL px² of open sky, spread evenly over it */
        var nT = Math.round(cols.reduce(function (s, i) { return s + 16 * (CL[i].b - CL[i].t); }, 0) / this.NCL);
        for (k = 0; k < nT && cols.length; k++) { var cx0 = cols[Math.min(cols.length - 1, ((k + R()) / nT * cols.length) | 0)] * 16 + 8, c = CL[(cx0 / 16) | 0];
          var cc = this.cloud(cx0, v(c.t + 60, c.b), v(1.5, 6)); cc.r = v(.55, .8); cc.a = cc.at = 1; } }
      return CL;
    },
    /* ---- clouds in 3D, seen from the ground (24 November 2026) ----
       The eye stands on the ground at the horizontal middle of the holder; the horizon is the ground line GY. A point at height Y
       above the ground, at distance Z in front of the eye and X to its right, is seen at
           x = XC + F X / Z,   y = GY − F Y / Z            (a pinhole camera; F = GY px, so the picture keeps its proportions)
       Every cloud is built once, in its own frame, as 8 to 16 round puffs (spheres) standing on a flat base at height HB: a
       cumulus. Then, every frame, its puffs and the ring of its base are carried into the eye's frame (X + u s, HB + v s, Z + w s,
       s the cloud's size) and projected. So a near cloud is high on the page and large, a far one small and low near the horizon;
       the base, a flat floor above the eye, is seen from below as a darker band under the puffs; and the wind, the same in
       metres per second for every cloud, carries near clouds faster across the page than far ones (parallax). */
    proj: function (X, Y, Z) { var f = this.GY / Z; return [this.XC + X * f, this.GY - Y * f, f]; },
    cloud: function (xs, ys, m) {              /* a new cloud whose base is seen at (xs, ys), holding the water m */
      var Z = this.GY * this.HB / Math.max(30, this.GY - ys), c = { X: (xs - this.XC) * Z / this.GY, Z: Z, m: m, r: .55, s: this.SIZE * Math.cbrt(m), a: 0, at: 0, P: [] }, n = 8 + (R() * 9 | 0);
      for (var i = 0; i < n; i++) { var u = (R() + R() + R() - 1.5) * .75, w = (R() + R() + R() - 1.5) * .5, core = Math.exp(-(u * u + w * w) / .35), rr = .22 + .32 * core * v(.6, 1.1);
        c.P.push([u, rr * .55 + .5 * core * R(), w, rr]); }       /* puff: across u, up v (the base is v = 0), in depth w, radius; all in units of s */
      c.P.sort(function (p, q) { return q[2] - p[2]; });              /* far puffs first, so near ones are drawn over them */
      c.ax = Math.max.apply(null, c.P.map(function (q) { return Math.abs(q[0]) + q[3] * .9; })); c.az = Math.max.apply(null, c.P.map(function (q) { return Math.abs(q[2]) + q[3] * .9; }));   /* the base ellipse reaches under every puff */
      this.Cs.push(c); return c; },
    /* where a cloud is seen: its base centre and its half width on the page */
    seen: function (c) { var p = this.proj(c.X, this.HB, c.Z); c.x = p[0]; c.y = p[1]; c.hw = .95 * c.s * p[2]; return c; },
    join: function (d) {                        /* a parcel of vapour reaching its height joins the cloud there, or starts one */
      var best = null, bd = 1e9, self = this; this.Cs.forEach(function (c) { var dx = Math.abs(c.x - d.x), dy = Math.abs(c.y - 10 - d.y); if (dx < c.hw * 1.2 + 30 && dy < 70 && dx + dy < bd) { bd = dx + dy; best = c; } });
      if (best) best.m += .17; else { var c = this.seen(this.cloud(d.x, d.y + 10, .17)); c.at = 1; }
    },
    /* draw one cloud: its puffs (shaded, lit from above), then its base seen from below; through a scratch canvas, so the
       overlapping puffs make one body and the whole cloud fades as one */
    paint: function (c) {
      var self = this, s = c.s, P = c.P, pts = [], i, bx0 = 1e9, bx1 = -1e9, by0 = 1e9, by1 = -1e9;
      for (i = 0; i < P.length; i++) { var q = P[i], p = this.proj(c.X + q[0] * s, this.HB + q[1] * s, c.Z + q[2] * s), rad = q[3] * s * p[2]; pts.push([p[0], p[1], rad, q[1] / (q[3] + .01)]);
        bx0 = Math.min(bx0, p[0] - rad); bx1 = Math.max(bx1, p[0] + rad); by0 = Math.min(by0, p[1] - rad); by1 = Math.max(by1, p[1] + rad); }
      var ring = []; for (i = 0; i < 24; i++) { var an = i / 24 * 2 * PI, pb = this.proj(c.X + Math.cos(an) * c.ax * s, this.HB, c.Z + Math.sin(an) * c.az * s); ring.push(pb); by1 = Math.max(by1, pb[1]); bx0 = Math.min(bx0, pb[0]); bx1 = Math.max(bx1, pb[0]); }
      var ox = Math.floor(bx0) - 2, oy = Math.floor(by0) - 2, ww = Math.ceil(bx1 - ox) + 4, hh = Math.ceil(by1 - oy) + 4; if (ww < 2 || hh < 2 || ww > 2000 || hh > 2000) return;
      var sc = this.scr || (this.scr = document.createElement('canvas')); if (sc.width < ww) sc.width = ww; if (sc.height < hh) sc.height = hh;
      var g = sc.getContext('2d'); g.clearRect(0, 0, ww, hh); g.save(); g.translate(-ox, -oy);
      /* the base is flat: nothing of the cloud shows below the far edge of its base ring */
      var low = ring.slice(0, 13); g.beginPath(); g.moveTo(bx0 - 4, by0 - 4); g.lineTo(bx1 + 4, by0 - 4); g.lineTo(bx1 + 4, low[0][1]); low.forEach(function (p) { g.lineTo(p[0], p[1]); }); g.lineTo(bx0 - 4, low[12][1]); g.closePath(); g.clip();
      /* each puff opaque, a mix of paper and wine: pale where the light from above falls, deeper towards its lower rim; only the
         outermost rim fades, so puffs that overlap hide each other (as in a real cloud) instead of piling up darker */
      pts.forEach(function (p) { var rg = g.createRadialGradient(p[0] - p[2] * .25, p[1] - p[2] * .45, p[2] * .05, p[0], p[1], p[2]);
        rg.addColorStop(0, mixc(.10, 1)); rg.addColorStop(.8, mixc(.30, 1)); rg.addColorStop(.93, mixc(.34, .9)); rg.addColorStop(1, mixc(.34, 0)); g.fillStyle = rg; g.beginPath(); g.arc(p[0], p[1], p[2], 0, 7); g.fill(); });
      /* the underside, seen from below: a darker floor, its edge soft */
      var cxr = 0, cyr = 0; ring.forEach(function (p) { cxr += p[0]; cyr += p[1]; }); cxr /= ring.length; cyr /= ring.length;
      var rxs = ring.map(function (p) { return p[0]; }), rx = (Math.max.apply(null, rxs) - Math.min.apply(null, rxs)) / 2, ry = Math.max(2, (Math.max.apply(null, ring.map(function (p) { return p[1]; })) - Math.min.apply(null, ring.map(function (p) { return p[1]; }))) / 2);
      g.save(); g.translate(cxr, cyr); g.scale(1, ry / rx); var rb = g.createRadialGradient(0, 0, 0, 0, 0, rx * .85); rb.addColorStop(0, mixc(.55, .9)); rb.addColorStop(.6, mixc(.48, .7)); rb.addColorStop(1, mixc(.4, 0)); g.fillStyle = rb; g.beginPath(); g.arc(0, 0, rx * .85, 0, 7); g.fill(); g.restore();
      g.restore(); x.globalAlpha = c.a * self.TONE; x.drawImage(sc, 0, 0, ww, hh, ox, oy, ww, hh); x.globalAlpha = 1;
    },
    band: function (px, CL) { CL = CL || this.CL; return CL ? CL[cl((px / 16) | 0, 0, CL.length - 1)] : null; },
    seed: function (near) { for (var k = 0; k < 14; k++) { var px = near && R() < .65 ? near.x + (R() < .5 ? -1 : 1) * v(near.hw * .6 + 10, near.hw + 240) : v(14, W - 14), t = this.fit(px, KINDS[R() * 5 | 0]()); if (t) { this.A.push(t); return t; } } return null; },
    init: function () {
      this.UN = W > 760 ? (+host.getAttribute('data-bg-under') || 0) : 0; this.Hn = []; this.GY = H - 46 - this.UN; this.Fd = []; this.sc = cl(H / 520, .8, 1.7);
      this.A = []; this.L = []; this.M = []; this.ob = []; this.V = []; this.Cs = []; this.Y = 0; this.sn = new Float32Array(Math.ceil(W / 12) + 1); this.sky = W > 760;
      var self = this, hr = host.getBoundingClientRect();
      [host.getAttribute('data-bg-avoid'), host.getAttribute('data-bg-avoid-near')].forEach(function (q) { if (q) document.querySelectorAll(q).forEach(function (e) { var r = e.getBoundingClientRect(); if (r.width && r.height) self.ob.push({ l: r.left - hr.left - 14, r: r.right - hr.left + 14, t: r.top - hr.top - 10, b: r.bottom - hr.top + 10 }); }); });
      var m = null; for (var q = 0; q < 80 && !m; q++) { var g = KINDS[0](); g.len = 64; g.maxd = 6; m = this.fit(q ? v(14, W - 14) : Math.max(46, W * .1), g); }
      if (m) { this.A.push(m); this.ripen(m); m.life = this.LIFE[0] * this.YEAR; }
      /* a few more grown trees of mixed ages, so the land is not bare when the page opens and they do not all die at once */
      for (var s = 1; s < this.START; s++) { var t2 = this.seed(m); if (t2) { this.ripen(t2); t2.age = v(0, .8) * t2.life; } }
      this.XC = W / 2; this.U = 0; this.CL = this.clouds(); this.Cs.forEach(function (c) { self.seen(c); }); },
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
            if (sea === 2) { if (tp.s >= 1 && R() < dt * self.FALL) { tp.s = 0; tp.rg = null; self.L.push({ x: tp.x, y: tp.y, ph: R() * 6, t: 0, w: v(-26, 34) }); } }
            else if (sea === 0 || sea === 1) { if (tp.rg === null) tp.rg = v(0, 5); if (tp.s < 1) { if (tp.rg > 0) tp.rg -= dt; else tp.s = Math.min(1, tp.s + dt / 1.2); }
              else if (sea === 1 && R() < dt * .012) { tp.s = 0; tp.rg = v(1, 4); self.L.push({ x: tp.x, y: tp.y, ph: R() * 6, t: 0, w: v(-26, 34) }); } }
            if (tp.s > 0) { leaf(tp.x, tp.y, tp.a, tp.s * t.ls, sea === 2 ? .38 : .6); if (tp.s >= 1) leaves++; }
            if (sea < 2 && tp.s >= 1 && self.sky && t.h > 90 && R() < dt * .14) { var bv = self.band(tp.x); if (bv && bv.b < tp.y - 40) self.V.push({ x: tp.x, y: tp.y, r: .5, q: 0, h: v(bv.t, bv.b) }); }
          });
          if (sea < 2 && R() < dt * self.SEED && self.A.length < 90) self.seed(t);
          if (t.age > t.life) { t.dead = 1; if (self.UN) self.Fd.push({ Rs: t.Rs, a: 1 }); t.S.forEach(function (s, i) { if (i % 2 === 0) self.L.push({ x: (s[0] + s[2]) / 2, y: (s[1] + s[3]) / 2, ph: R() * 6, t: 0, w: v(-10, 10) }); }); }
        } else { if (sea < 2) t.fed += dt * t.G.need / self.GROW; var g = Math.min(1, t.fed / t.G.need); if (g <= 0) dot(t.x, GY, 1.5, .5); else grow(t.G, t.x, GY, g, null); if (g >= 1) self.ripen(t); }
      });
      this.A = this.A.filter(function (t) { return !t.dead; }); if (!this.A.length) this.seed(null);
      this.L = this.L.filter(function (l) { l.t += dt; l.y += 32 * dt; var w = l.ph + l.t * 2.4; l.x += (l.w + Math.cos(w) * 34) * dt; if (self.inOb(l.x, l.y, 4) || l.x < -10 || l.x > W + 10) return false; if (l.y >= GY - 2) { for (var k = 0; k < 4; k++) self.M.push({ x: l.x + v(-4, 4), y: GY, ty: GY + 6 + R() * (self.UN ? (self.UN - 40) * R() : 22) }); return false; } leaf(l.x, l.y, w, 1, .45); return true; });
      /* the sky: vapour rises from the leaves into the open sky above the trees, the two top corners of the page beside the
         hero text and beside the pendulum card (band(), set by clouds()); there it condenses into droplets that wander, collide
         and merge (volume is kept, r = cube root of r1^3 + r2^3); each cloud droplet is drawn with a faint halo, so many of them
         together read as a cloud. The speed of fall grows as r squared (Stokes), so only merged drops beat the updraft and fall,
         sweeping up small ones on the way, and the rain feeds the young trees. In winter the clouds give their water up as snow,
         so the corners clear in winter and fill again in spring: the corners hold this forest's own weather. */
      var V = this.V, Cs = this.Cs, up = sea === 1 ? 7 : sea === 0 ? 4 : 2;
      if (sea < 2 && this.sky && V.length < 450) for (var gi = 0; gi < this.CL.length; gi++) { var bg = this.CL[gi]; if (bg && R() < dt * this.SOIL * 16 / 100) V.push({ x: gi * 16 + R() * 16, y: GY - 2, r: .5, q: 0, h: v(bg.t + 60, bg.b) }); }
      /* the wind: one speed for the whole sky, wandering slowly (a random walk pulled back to zero, about a minute's memory) */
      this.U += (-this.U / 60 * dt + this.WIND * Math.sqrt(2 / 60 * dt) * (R() + R() + R() - 1.5) * 2);
      /* each cloud: carried by the wind; its size follows its water smoothly (cube root, settling over 5 s); it fades in where it is
         over open sky and out where it drifts over text or off the page; its droplets grow by condensation, and grown droplets
         collide, merge and fall as rain (or, in winter, as snow) from under its base */
      Cs.sort(function (p, q) { return q.Z - p.Z; });
      Cs.forEach(function (c) {
        c.X += self.U * dt; self.seen(c);
        c.s += (self.SIZE * Math.cbrt(Math.max(c.m, .01)) - c.s) * Math.min(1, dt / 5);
        var ok = 0; for (var k = -2; k <= 2; k++) { var bk = self.band(c.x + k * c.hw * .5); if (bk && c.y < bk.b + 20 && c.x + k * c.hw * .5 > 0 && c.x + k * c.hw * .5 < W) ok++; }
        c.at = ok / 5; c.a += ((ok === 5 ? 1 : 0) - c.a) * Math.min(1, dt / 2.5);   /* fully over open sky, or fading out */ c.m *= Math.exp(-dt / (c.at < .4 ? 8 : self.EVAP));   /* over text: it thins away */
        if (sea < 3) c.r += self.COND * dt;
        var rate = sea === 3 ? .25 * c.m : self.RAIN * c.m * Math.max(0, c.r - .6);
        if (R() < rate * dt && c.m > .3 && c.a > .3) { var u = v(-.6, .6), w = v(-.4, .4), pb = self.proj(c.X + u * c.s, self.HB, c.Z + w * c.s); c.m -= .15;
          if (sea === 3) V.push({ x: pb[0], y: pb[1], r: .5, q: 1, snow: 1 }); else { V.push({ x: pb[0], y: pb[1], r: v(1.3, 1.7), q: 1 }); c.r = Math.max(.55, c.r - .004); } }
        if (c.a > .01) self.paint(c);
      });
      this.Cs = Cs.filter(function (c) { return c.m > .05 && !(c.a < .01 && c.at === 0); });
      for (var a = 0; a < V.length; a++) { var d = V[a]; if (d.dead) continue; var bd0 = self.band(d.x);
        if (!d.q) { d.y -= 90 * dt; d.x += (R() - .5) * 10 * dt; if (!bd0) { d.dead = 1; continue; } if (d.y < d.h) { d.dead = 1; self.join(d); } else dot(d.x, d.y, .6, .22); continue; }
        var snow = d.snow, vt = snow ? 60 : 9 * d.r * d.r - up, nx = d.x + ((R() - .5) * 8) * dt + (snow ? Math.sin(self.Y * 2 + a) * 8 * dt : 0), ny = d.y + vt * dt;
        if (self.inOb(nx, ny, 6) || nx < 2 || nx > W - 2) { d.x -= (nx - d.x) * 2; } else { d.x = nx; } d.y = ny;
        if (d.y >= GY) { d.dead = 1; if (snow) sn[(cl(d.x, 0, W - 1) / 12) | 0] = Math.min(5, sn[(cl(d.x, 0, W - 1) / 12) | 0] + .6);
          else self.A.forEach(function (t) { if (!t.mat && Math.abs(t.x - d.x) < 70) t.fed += 2 * d.r * self.FEED; }); continue; }
        if (snow) { x.strokeStyle = col(.4); x.lineWidth = .8; ln(d.x - 2, d.y, d.x + 2, d.y); ln(d.x - 1, d.y - 1.7, d.x + 1, d.y + 1.7); ln(d.x - 1, d.y + 1.7, d.x + 1, d.y - 1.7); continue; }
        x.strokeStyle = col(.45); x.lineWidth = d.r * .8; ln(d.x, d.y - 6, d.x, d.y);
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
          h.D = h.D.filter(function (o) { o.u += o.d * 26 * dt; if (o.u < 0 || o.u > 60) { var to = o.d > 0 ? h.b : h.a; if (!to.mat) to.fed += 3 * self.FEED; return false; } var q = o.u | 0, e = o.u - q, A = h.P[q], B = h.P[Math.min(60, q + 1)]; dot(A[0] + (B[0] - A[0]) * e, A[1] + (B[1] - A[1]) * e, 1.3, .75 * h.f); return true; });
          return true; });
        this.M = this.M.filter(function (m) {
        var bp = null, bk = null, bd = 120 * 120;
        for (var j = 0; j < self.A.length; j++) { var k = self.A[j]; if (k.mat) continue; for (var q = 0; q < k.Rt.length; q++) { var p = k.Rt[q], dx = p.x - m.x, dy = p.y - m.y, d = dx * dx + dy * dy; if (d < bd) { bd = d; bp = p; bk = k; } } }
        m.age = (m.age || 0) + dt; if (m.y < m.ty - 1) m.y += (m.ty - m.y) * dt * .8;
        else if (bp) { var dd = Math.sqrt(bd); if (dd < 5) { bk.fed += self.FEED; return false; } m.x += (bp.x - m.x) / dd * 16 * dt; m.y += (bp.y - m.y) / dd * 16 * dt; }
        var fa = cl((70 - m.age) / 20, 0, 1); if (fa <= 0) return false;
        dot(m.x, m.y, 1.1, fa * .55 * (1 - .6 * cl((m.y - GY) / U, 0, 1))); return true; }); return; }
      this.M = this.M.filter(function (m) { var b = null; self.A.forEach(function (k) { if (!k.mat && (!b || Math.abs(k.x - m.x) < Math.abs(b.x - m.x))) b = k; }); m.y += (m.ty - m.y) * dt * 1.5; if (b) { var d = b.x - m.x; if (Math.abs(d) < 3) { b.fed += self.FEED; return false; } m.x += (d > 0 ? 1 : -1) * 26 * dt; } dot(m.x, m.y, 1.4, .85); return true; });
    }
  };


  /* ---- powder: iron powder over magnets under a sheet, and a wire with a current ---- */
  S.powder = {
    DENS: 3000, CYCLE: 18, LINES: 22,
    K: [['DENS', 'grains per 680 × 400 px', '', 300, 7000, 100, 1], ['CYCLE', 'the wire current: one on-and-off cycle', 's', 3, 60, 1], ['LINES', 'how many field lines the grains gather on', '', 6, 40, 1]],
    init: function () { this.t = 0; this.n = Math.min(7000, Math.round(this.DENS * area())); this.px = new Float32Array(this.n); this.py = new Float32Array(this.n); for (var i = 0; i < this.n; i++) { this.px[i] = R() * W; this.py[i] = R() * H; } this.G = [{ bx: W * .3, by: H * .45, a: .3, w: .1, ph: 0 }, { bx: W * .7, by: H * .56, a: 2.6, w: -.07, ph: 2.5 }]; this.L = cl(Math.min(W, H) * .1, 34, 70); },
    draw: function (dt) {
      clear(); this.t += dt; var t = this.t, P = [], I = 1.6 * cl(Math.sin(2 * PI * t / this.CYCLE) * 1.6, 0, 1), wx = W / 2 + W * .09 * Math.sin(t * .09), wy = H / 2 + H * .1 * Math.cos(t * .07), L = this.L, i, k;
      this.G.forEach(function (g) { g.a += g.w * dt; var cx = g.bx + 30 * Math.sin(t * .13 + g.ph), cy = g.by + 22 * Math.cos(t * .11 + g.ph), dx = L * Math.cos(g.a), dy = L * Math.sin(g.a); P.push([cx + dx, cy + dy, 1], [cx - dx, cy - dy, -1]); x.strokeStyle = col(.14); x.lineWidth = 20; x.lineCap = 'butt'; ln(cx + dx, cy + dy, cx - dx, cy - dy); });
      x.lineWidth = 1.5; x.strokeStyle = col(.25 + .5 * I / 1.6); x.beginPath(); x.arc(wx, wy, 8, 0, 7); x.stroke(); dot(wx, wy, 2.5 * I / 1.6 + .5, .9);
      var tp = t % 3.5, tap = tp < .25 ? 5 * (1 - tp / .25) : 0, N = this.LINES; x.strokeStyle = col(.8); x.lineWidth = 1.3; x.lineCap = 'round'; x.beginPath();
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
    seq: [[3], [4], [5], [3, 4, 5], [6], [], [4], [0, 1, 2], [7], [3, 5], [], [1, 2, 3], [8], [6, 7, 8]], HN: 1024, C: 140,
    K: [['C', 'speed of sound (drawn)', 'px/s', 40, 400, 5]],
    init: function () { this.t = 0; this.a = new Float32Array(10); this.hs = []; this.last = []; for (var i = 0; i < 10; i++) { this.hs.push(new Float32Array(this.HN)); this.last.push(-99); } this.li = 0; this.Q = []; var s = Math.max(9, Math.sqrt(W * H / 8000)); for (var y = s / 2; y < H; y += s * .9) for (var q = s / 2; q < W; q += s) this.Q.push([q + v(-.3, .3) * s, y + v(-.3, .3) * s]); this.x0 = W / 2 - 105; this.y0 = H - 30; },
    draw: function (dt) {
      clear(); this.t += dt; var t = this.t, on = this.seq[Math.floor(t / 2.2) % this.seq.length], idx = Math.floor(t * 40), i, k, HN = this.HN, x0 = this.x0, y0 = this.y0, act = [];
      for (i = 0; i < 10; i++) { var tg = on.indexOf(i) >= 0 ? 1 : 0; this.a[i] += (tg - this.a[i]) * Math.min(1, dt * 5); for (k = this.li + 1; k <= idx; k++) this.hs[i][k % HN] = this.a[i]; if (this.a[i] > .03) this.last[i] = t; if (t - this.last[i] < 24) act.push(i); }
      this.li = idx; x.fillStyle = col(.62); x.beginPath();
      for (var n = 0; n < this.Q.length; n++) {
        var q = this.Q[n], ox = 0, oy = 0;
        for (k = 0; k < act.length; k++) { i = act[k]; var dx = q[0] - (x0 + i * 23.3), dy = q[1] - y0, r = Math.hypot(dx, dy) + 1, id = Math.floor((t - r / this.C) * 40); if (id < 0 || idx - id > HN - 4) continue; var am = this.hs[i][id % HN]; if (am < .03) continue; var kk = 2 * PI / (70 - i * 4.5), d = am * 6 * Math.sin(kk * r - kk * this.C * t) / (1 + r / 260); ox += dx / r * d; oy += dy / r * d; }
        if (q[1] + oy < y0 - 20) x.rect(q[0] + ox, q[1] + oy, 1.6, 1.6);
      }
      x.fill(); x.strokeStyle = col(.85); x.lineWidth = 1.5; x.strokeRect(x0 - 19, y0 - 14, 248, 30);
      for (i = 0; i < 10; i++) { var hx = x0 - 9 + i * 23.3; x.strokeStyle = col(.5); x.lineWidth = 1; x.strokeRect(hx, y0 - 9, 18, 20); var o = this.a[i] * 3.5 * Math.sin(2 * PI / (70 - i * 4.5) * this.C * t); x.strokeStyle = col(.95); x.lineWidth = 1.6; x.beginPath(); x.moveTo(hx + 3, y0 + 8); x.quadraticCurveTo(hx + 9 + o, y0, hx + 15 + o * 1.6, y0 - 6); x.stroke(); }
    }
  };

  /* ---- rails: the two side margins of the home page below the hero, fixed to the window but drawn in page coordinates, so
     they scroll with the page. Left: the forest's roots go on growing down the page (space colonisation: each tip grows towards
     the scattered water it can sense; thickness by Murray's law, r^3 of a parent = sum of r^3 of its children; sap climbs back
     up to the trees). Right: pairs of pendulums tied by a weak spring hang from beams; the swing drains from one bob into the
     other and back (beats); this half is not computed here but played from data computed once on Kaggle (sceneData above). ---- */
  S.rails = {
    geo: function () {
      var lay = document.querySelector(host.getAttribute('data-bg-around') || 'main'), fo = document.querySelector('[data-bg=forest]'), end = document.querySelector(host.getAttribute('data-bg-until') || 'footer');
      if (!lay) return null; var r = lay.getBoundingClientRect(), sy = scrollY, top = fo ? fo.getBoundingClientRect().bottom + sy - 46 : r.top + sy;
      var bot = end ? end.getBoundingClientRect().top + sy - 30 : r.bottom + sy;
      return { l0: 12, l1: r.left - 18, r0: r.right + 18, r1: W - 12, top: top, bot: Math.max(top + 200, bot) };
    },
    init: function () {
      var self = this; this.g = this.geo(); this.N = []; this.At = []; this.grid = {}; this.flow = []; this.Bs = []; this.t = 0; this.gt = 0; this.mt = 0; this.ok = false;
      var g = this.g; if (!g || g.l1 - g.l0 < 90 || g.r1 - g.r0 < 90) return; this.ok = true;
      this.lw = g.l1 - g.l0; this.rw = g.r1 - g.r0; this.yLen = 0;
      var fo = document.querySelector('[data-bg=forest]'), F = fo && fo.__bgScene, xs = [];
      if (F && F.A) F.A.forEach(function (t) { var px = t.x - g.l0; if (px > 8 && px < self.lw - 8 && xs.every(function (q) { return Math.abs(q - px) > 30; })) xs.push(px); });
      if (!xs.length) xs = [this.lw * .35, this.lw * .75]; xs.slice(0, 3).forEach(function (px) { self.add(px, 0, -1); });
      this.extend();
    },
    /* scatter water over any new length of page, and hang new bars of pendulums there */
    extend: function () {
      var g = this.g, L = g.bot - g.top; if (L <= this.yLen + 20) return; var y0 = this.yLen, n = Math.round(this.lw * (L - y0) / 1100);
      for (var i = 0; i < n; i++) { var u = R(); this.At.push({ x: 6 + (this.lw - 12) * (R() < .5 ? u * u : 1 - u * u), y: v(y0 + 8, L - 10), on: 1 }); }
      var G = 250; for (var y = Math.max(40, Math.ceil((y0 - 40) / G) * G + 40); y < L - 170; y += G) this.bar(y);
      this.yLen = L;
    },
    /* a beam of coupled pendulums: as many pairs as the margin holds side by side (a pair takes the pivot spacing, its swing and 30 px),
       each starting at its own random moment of the stored loop, so no two pairs and no two visits look alike */
    bar: function (y) {
      var off = []; for (var i = 0; i < 4; i++) off.push(R()); this.Bs.push({ y: y, off: off });   /* how many pairs are hung is decided when the data (spacing d) is known */
    },
    add: function (px, py, par) { var i = this.N.length; this.N.push({ x: px, y: py, p: par, c: 1, k: 0 }); var key = ((px / 32) | 0) + ',' + ((py / 32) | 0); (this.grid[key] = this.grid[key] || []).push(i); return i; },
    near: function (px, py, D) { var best = -1, bd = D * D, cx = (px / 32) | 0, cy = (py / 32) | 0, m = Math.ceil(D / 32); for (var a = -m; a <= m; a++) for (var b = -m; b <= m; b++) { var c = this.grid[(cx + a) + ',' + (cy + b)]; if (!c) continue; for (var k = 0; k < c.length; k++) { var q = this.N[c[k]], dx = q.x - px, dy = q.y - py, d = dx * dx + dy * dy; if (d < bd) { bd = d; best = c[k]; } } } return [best, bd]; },
    growStep: function () {
      var N = this.N, my = 0, acc = {}, i; for (i = 0; i < N.length; i++) if (N[i].y > my) my = N[i].y;
      for (i = 0; i < this.At.length; i++) { var a = this.At[i]; if (!a.on || a.y > my + 120) continue; var r = this.near(a.x, a.y, 120); if (r[0] < 0) continue;
        if (r[1] < 64) { a.on = 0; continue; } var q = N[r[0]], d = Math.sqrt(r[1]), s = acc[r[0]] || (acc[r[0]] = [0, 0]); s[0] += (a.x - q.x) / d; s[1] += (a.y - q.y) / d; }
      for (var k in acc) { var q2 = N[k], s2 = acc[k], dx = s2[0] + (R() - .5) * .6, dy = s2[1] + .15, dl = Math.hypot(dx, dy) || 1, nx = q2.x + dx / dl * 6, ny = q2.y + dy / dl * 6;
        if (this.near(nx, ny, 3)[0] < 0) this.add(cl(nx, 2, this.lw - 2), ny, +k); }
      this.At = this.At.filter(function (a) { return a.on; });
    },
    murray: function () { var N = this.N, i; for (i = 0; i < N.length; i++) N[i].k = 0; for (i = N.length - 1; i >= 0; i--) { var q = N[i]; q.c = Math.max(1, q.k); if (q.p >= 0) N[q.p].k += q.c; } },
    draw: function (dt) {
      clear(); if (!this.ok) return; var self = this, g = this.g, sy = scrollY, N = this.N; this.t += dt; this.gt += dt; this.mt += dt;
      if (this.mt > 1) { this.mt = 0; var g2 = this.geo(); if (g2 && Math.abs(g2.bot - g.bot) > 4) { g.bot = g2.bot; this.extend(); } this.murray(); }
      while (this.gt > .05) { this.gt -= .05; this.growStep(); }
      var top = g.top - sy, fade = function (py) { return cl(py / 80, 0, 1) * cl((g.bot - g.top - py) / 80, 0, 1); };
      if (top > H || g.bot - sy < 0) return;
      /* left: roots */
      x.save(); x.beginPath(); x.rect(g.l0 - 4, 0, this.lw + 8, H); x.clip(); x.lineCap = 'round';
      for (var i = 0; i < N.length; i++) { var q = N[i]; if (q.p < 0) continue; var sY = top + q.y; if (sY < -10 || sY > H + 10) continue; var pq = N[q.p], f = fade(q.y);
        x.strokeStyle = col((.2 + .05 * Math.min(4, Math.cbrt(q.c))) * f); x.lineWidth = Math.min(2, .5 + .25 * Math.cbrt(q.c)); ln(g.l0 + pq.x, top + pq.y, g.l0 + q.x, sY); }
      if (R() < dt * 4 && N.length > 10) { var tp = N[(R() * N.length) | 0]; if (tp.c === 1 && tp.p >= 0) this.flow.push({ i: tp.p, f: 0, x: tp.x, y: tp.y }); }
      this.flow = this.flow.filter(function (o) { var tq = N[o.i]; if (!tq) return false; var dx = tq.x - o.x, dy = tq.y - o.y, d = Math.hypot(dx, dy), st = 34 * dt;
        if (d <= st) { o.x = tq.x; o.y = tq.y; if (tq.p < 0) return false; o.i = tq.p; } else { o.x += dx / d * st; o.y += dy / d * st; }
        var s = top + o.y; if (s > -5 && s < H + 5) dot(g.l0 + o.x, s, 1.1, .45 * fade(o.y)); return true; });
      if (this.flow.length > 160) this.flow.splice(0, this.flow.length - 160);
      x.restore();
      /* right: pairs of pendulums tied by a weak spring, played from the stored run (tools/sims/coupled.py, computed on Kaggle).
         Nothing is computed here: each stored frame gives the two angles, the frame nearest in time is drawn. The swing drains from
         one bob into the other through the spring and comes back, a beat of about 27 s (docs/kaggle-sims.md). */
      var D = this.D; if (!D) { if (!this.asked) { this.asked = 1; sceneData('coupled', 'coupled.bin').then(function (d) { self.D = d; }, function (e) { self.err = String(e.message || e); }); } return; }
      var hd = D.hdr, nf = hd.frames, F = D.frames, pr = hd.params, sc = pr.scale, Lp = pr.L * sc, ap = pr.a * sc, dp = pr.d * sc;
      x.save(); x.beginPath(); x.rect(g.r0 - 4, 0, this.rw + 8, H); x.clip();
      this.Bs.forEach(function (B) {
        var by = top + B.y; if (by < -Lp - 20 || by > H + 10) return; var f = fade(B.y), m = Math.max(1, Math.min(B.off.length, Math.floor((self.rw - 16) / (dp + 2 * Lp * .2 + 30)))), cw = self.rw / m;
        x.strokeStyle = col(.45 * f); x.lineWidth = 2.2; ln(g.r0 + 6, by, g.r1 - 6, by);
        for (var q = 0; q < m; q++) {
          var k = (Math.round(self.t / hd.dt + B.off[q] * nf) % nf) * 2, t1 = F[k] * 1e-4, t2 = F[k + 1] * 1e-4;
          var p1 = g.r0 + cw * (q + .5) - dp / 2, p2 = p1 + dp, b1x = p1 + Lp * Math.sin(t1), b1y = by + Lp * Math.cos(t1), b2x = p2 + Lp * Math.sin(t2), b2y = by + Lp * Math.cos(t2);
          var s1x = p1 + ap * Math.sin(t1), s1y = by + ap * Math.cos(t1), s2x = p2 + ap * Math.sin(t2), s2y = by + ap * Math.cos(t2);
          /* the spring: a zigzag of 9 turns between the two rods */
          var sx = s2x - s1x, sy = s2y - s1y, sl = Math.hypot(sx, sy) || 1, nx = -sy / sl, ny = sx / sl; x.strokeStyle = col(.5 * f); x.lineWidth = 1; x.beginPath(); x.moveTo(s1x, s1y);
          for (var z = 1; z < 19; z++) { var u = z / 19, o = (z % 2 ? 3.2 : -3.2) * (z > 1 && z < 18 ? 1 : .5); x.lineTo(s1x + sx * u + nx * o, s1y + sy * u + ny * o); } x.lineTo(s2x, s2y); x.stroke();
          x.strokeStyle = col(.6 * f); x.lineWidth = 1.3; ln(p1, by, b1x, b1y); ln(p2, by, b2x, b2y);
          dot(p1, by, 2, .7 * f); dot(p2, by, 2, .7 * f);
          dot(b1x, b1y, pr.rb * sc, (.45 + .45 * Math.min(1, Math.abs(t1) * 4)) * f); dot(b2x, b2y, pr.rb * sc, (.45 + .45 * Math.min(1, Math.abs(t2) * 4)) * f);
        }
      });
      x.restore();
    }
  };
  /* ---- pairs: the right rail's coupled pendulums on their own, in a box (the scenes page, scenes.html). The same stored run
     (tools/sims/coupled.py, computed on Kaggle); nothing is computed here. The box shows one large pair and draws, under it, the
     energy of each pendulum over the loop, read from the stored angles: E_i = m g L (1 − cos θ_i) + ½ m L² θ_i'², with θ_i'
     taken from the two neighbouring stored frames. That curve is a reading of the stored motion, not a second simulation. ---- */
  S.pairs = {
    SPEED: 1,   /* always real time: the stored run is the motion of these pendulums, so it has no knob (the handoff of 23 November 2026) */
    K: [],
    init: function () { var self = this; this.t = 0; if (!this.asked) { this.asked = 1; sceneData('coupled', 'coupled.bin').then(function (d) { self.D = d; }, function (e) { self.err = String(e.message || e); }); } },
    draw: function (dt) {
      clear(); this.t += dt * this.SPEED; var D = this.D; if (!D) return; var hd = D.hdr, nf = hd.frames, F = D.frames, pr = hd.params;
      var sc = Math.min((H * .62) / pr.L, (W * .5) / pr.d), Lp = pr.L * sc, ap = pr.a * sc, dp = pr.d * sc, by = 24, cx = W / 2, j = Math.round(this.t / hd.dt) % nf, k = j * 2;
      var t1 = F[k] * 1e-4, t2 = F[k + 1] * 1e-4, p1 = cx - dp / 2, p2 = cx + dp / 2;
      x.strokeStyle = col(.6); x.lineWidth = 3; ln(p1 - 40, by, p2 + 40, by);
      var s1x = p1 + ap * Math.sin(t1), s1y = by + ap * Math.cos(t1), s2x = p2 + ap * Math.sin(t2), s2y = by + ap * Math.cos(t2), sx = s2x - s1x, sy = s2y - s1y, sl = Math.hypot(sx, sy) || 1, nx = -sy / sl, ny = sx / sl;
      x.strokeStyle = col(.7); x.lineWidth = 1.3; x.beginPath(); x.moveTo(s1x, s1y); for (var z = 1; z < 23; z++) { var o = (z % 2 ? 6 : -6) * (z > 1 && z < 22 ? 1 : .5); x.lineTo(s1x + sx * z / 23 + nx * o, s1y + sy * z / 23 + ny * o); } x.lineTo(s2x, s2y); x.stroke();
      x.strokeStyle = col(.8); x.lineWidth = 1.8; ln(p1, by, p1 + Lp * Math.sin(t1), by + Lp * Math.cos(t1)); ln(p2, by, p2 + Lp * Math.sin(t2), by + Lp * Math.cos(t2));
      dot(p1 + Lp * Math.sin(t1), by + Lp * Math.cos(t1), pr.rb * sc, .9); dot(p2 + Lp * Math.sin(t2), by + Lp * Math.cos(t2), pr.rb * sc, .9);
      /* the energy of each pendulum over one loop, and where we are in it */
      if (!this.E) { var E = this.E = [new Float32Array(nf), new Float32Array(nf)], g0 = pr.g, mx = 0; for (var f = 0; f < nf; f++) for (var q = 0; q < 2; q++) {
          var th = F[f * 2 + q] * 1e-4, w = (F[((f + 1) % nf) * 2 + q] - F[((f - 1 + nf) % nf) * 2 + q]) * 1e-4 / (2 * hd.dt); E[q][f] = pr.m * g0 * pr.L * (1 - Math.cos(th)) + .5 * pr.m * pr.L * pr.L * w * w; mx = Math.max(mx, E[q][f]); } this.Emax = mx; }
      var gx = 20, gw = W - 40, gh = H * .22, gy = H - 14;
      x.strokeStyle = col(.25); x.lineWidth = 1; ln(gx, gy, gx + gw, gy);
      for (q = 0; q < 2; q++) { x.strokeStyle = col(q ? .45 : .9); x.setLineDash(q ? [5, 3] : []); x.lineWidth = 1.4; x.beginPath(); for (f = 0; f < nf; f += 2) { var px = gx + gw * f / nf, py = gy - gh * this.E[q][f] / this.Emax; if (f) x.lineTo(px, py); else x.moveTo(px, py); } x.stroke(); }
      x.setLineDash([]); x.strokeStyle = col(.8); ln(gx + gw * j / nf, gy, gx + gw * j / nf, gy - gh - 6);
      this.now = { t: j * hd.dt, theta1: t1, theta2: t2, E1: this.E[0][j], E2: this.E[1][j] };
    }
  };
  /* ---- roots: the left rail's roots on their own, in a box (scenes.html). Space colonisation, as in the rail: water is scattered
     over the box; every water drop within SENSE pulls its nearest root tip towards it; each tip grows STEP px per step in the mean
     direction of its pulls (plus a slight pull downwards and a little noise); a drop that a root reaches is used up; thickness by
     Murray's law (r³ of a parent = the sum of r³ of its children); sap dots climb from the tips back to the surface. ---- */
  S.roots = {
    WATER: 1100, SENSE: 120, STEP: 6, DOWN: .15,
    K: [['WATER', 'area per drop of water (fewer drops: sparser roots)', 'px²', 300, 4000, 50, 1], ['SENSE', 'how far a root tip senses water', 'px', 20, 300, 5, 1], ['STEP', 'growth per step', 'px', 2, 16, 1, 1], ['DOWN', 'pull downwards (gravitropism)', '', 0, 1, .05, 1]],
    init: function () { this.N = []; this.At = []; this.grid = {}; this.gt = 0; this.mt = 0; this.flow = [];
      var n = Math.round(W * H / this.WATER), i; for (i = 0; i < n; i++) this.At.push({ x: v(6, W - 6), y: v(20, H - 6), on: 1 });
      for (i = 0; i < 3; i++) this.add(W * (i + .5) / 3 + v(-20, 20), 0, -1); },
    add: function (px, py, par) { var i = this.N.length; this.N.push({ x: px, y: py, p: par, c: 1, k: 0 }); var key = ((px / 32) | 0) + ',' + ((py / 32) | 0); (this.grid[key] = this.grid[key] || []).push(i); },
    near: function (px, py, D) { var best = -1, bd = D * D, cx = (px / 32) | 0, cy = (py / 32) | 0, m = Math.ceil(D / 32); for (var a = -m; a <= m; a++) for (var b = -m; b <= m; b++) { var c = this.grid[(cx + a) + ',' + (cy + b)]; if (!c) continue; for (var k = 0; k < c.length; k++) { var q = this.N[c[k]], dx = q.x - px, dy = q.y - py, d = dx * dx + dy * dy; if (d < bd) { bd = d; best = c[k]; } } } return [best, bd]; },
    step: function () { var N = this.N, acc = {}, i, self = this; for (i = 0; i < this.At.length; i++) { var a = this.At[i]; if (!a.on) continue; var r = this.near(a.x, a.y, this.SENSE); if (r[0] < 0) continue;
        if (r[1] < 64) { a.on = 0; continue; } var q = N[r[0]], d = Math.sqrt(r[1]), s = acc[r[0]] || (acc[r[0]] = [0, 0]); s[0] += (a.x - q.x) / d; s[1] += (a.y - q.y) / d; }
      for (var k in acc) { var q2 = N[k], s2 = acc[k], dx = s2[0] + (R() - .5) * .6, dy = s2[1] + this.DOWN, dl = Math.hypot(dx, dy) || 1, nx = q2.x + dx / dl * this.STEP, ny = q2.y + dy / dl * this.STEP;
        if (this.near(nx, ny, 3)[0] < 0 && ny < H) this.add(cl(nx, 2, W - 2), ny, +k); }
      this.At = this.At.filter(function (a) { return a.on; }); },
    draw: function (dt) { clear(); this.gt += dt; this.mt += dt; var N = this.N, i;
      while (this.gt > .05) { this.gt -= .05; this.step(); }
      if (this.mt > .5) { this.mt = 0; for (i = 0; i < N.length; i++) N[i].k = 0; for (i = N.length - 1; i >= 0; i--) { var q = N[i]; q.c = Math.max(1, q.k); if (q.p >= 0) N[q.p].k += q.c; } }
      x.fillStyle = col(.18); this.At.forEach(function (a) { x.fillRect(a.x - .6, a.y - .6, 1.2, 1.2); });
      x.lineCap = 'round'; for (i = 0; i < N.length; i++) { q = N[i]; if (q.p < 0) continue; var pq = N[q.p]; x.strokeStyle = col(.3 + .08 * Math.min(4, Math.cbrt(q.c))); x.lineWidth = Math.min(3, .6 + .35 * Math.cbrt(q.c)); ln(pq.x, pq.y, q.x, q.y); }
      if (R() < dt * 6 && N.length > 10) { var tp = N[(R() * N.length) | 0]; if (tp.c === 1 && tp.p >= 0) this.flow.push({ i: tp.p, x: tp.x, y: tp.y }); }
      this.flow = this.flow.filter(function (o) { var tq = N[o.i]; if (!tq) return false; var dx = tq.x - o.x, dy = tq.y - o.y, d = Math.hypot(dx, dy), st = 34 * dt;
        if (d <= st) { o.x = tq.x; o.y = tq.y; if (tq.p < 0) return false; o.i = tq.p; } else { o.x += dx / d * st; o.y += dy / d * st; } dot(o.x, o.y, 1.3, .6); return true; });
      x.lineCap = 'butt'; }
  };
  /* ---- spin: spinners at random; a wandering rotating field brings those in reach into step ---- */
  S.spin = {
    FIELD: 16, NEIGH: .9, TURN: 3,
    K: [['FIELD', 'pull of the rotating field', '1/s', 0, 40, .5], ['NEIGH', 'pull between neighbours', '1/s', 0, 4, .05], ['TURN', 'turning rate of the field', 'rad/s', 0, 8, .1]],
    init: function () { this.t = 0; this.O = []; this.nc = Math.floor(W / 28); this.nr = Math.floor(H / 29.5); var ox = (W - (this.nc - 1) * 28) / 2, oy = (H - (this.nr - 1) * 29.5) / 2; for (var j = 0; j < this.nr; j++) for (var i = 0; i < this.nc; i++) this.O.push({ x: ox + i * 28, y: oy + j * 29.5, th: R() * 2 * PI, w: (R() < .5 ? -1 : 1) * v(1.5, 5) }); this.sg = cl(Math.min(W, H) * .33, 110, 300); },
    draw: function (dt) {
      clear(); this.t += dt; var t = this.t, phi = this.TURN * t, sx = W / 2 + W * .37 * Math.sin(t * .21), sy = H / 2 + H * .33 * Math.sin(t * .33 + 1), O = this.O, nc = this.nc, N = O.length, s2 = 2 * this.sg * this.sg, n, k;
      x.strokeStyle = col(.12); x.lineWidth = 1; x.beginPath(); x.arc(sx, sy, this.sg, 0, 7); x.stroke(); x.lineWidth = 8; x.lineCap = 'round'; ln(sx - 40 * Math.cos(phi), sy - 40 * Math.sin(phi), sx + 40 * Math.cos(phi), sy + 40 * Math.sin(phi)); x.lineCap = 'butt';
      for (n = 0; n < N; n++) { var o = O[n], dx = o.x - sx, dy = o.y - sy, K = this.FIELD * Math.exp(-(dx * dx + dy * dy) / s2), c = 0, i = n % nc; if (i > 0) c += Math.sin(O[n - 1].th - o.th); if (i < nc - 1) c += Math.sin(O[n + 1].th - o.th); if (n >= nc) c += Math.sin(O[n - nc].th - o.th); if (n < N - nc) c += Math.sin(O[n + nc].th - o.th); o.d = o.w + K * Math.sin(phi - o.th) + this.NEIGH * c; o.K = K; }
      for (n = 0; n < N; n++) { o = O[n]; o.th += o.d * dt; var lock = Math.pow(Math.max(0, Math.cos(o.th - phi)), 4) * Math.min(1, o.K / 5), a = .3 + .65 * lock; x.strokeStyle = col(a); x.lineWidth = 1.3; x.beginPath(); for (k = 0; k < 3; k++) { var an = o.th + k * 2.094; x.moveTo(o.x, o.y); x.lineTo(o.x + 10 * Math.cos(an), o.y + 10 * Math.sin(an)); } x.stroke(); dot(o.x + 10 * Math.cos(o.th), o.y + 10 * Math.sin(o.th), 2.4, Math.min(1, a + .2)); }
    }
  };

  /* ---- mix: three species in three chambers across the whole window; walls lift; entropy rises, temperatures meet ---- */
  S.mix = {
    HOT: 150, MID: 75, COLD: 28,
    K: [['HOT', 'speed of the triangles', 'px/s', 5, 300, 1, 1], ['MID', 'speed of the rings', 'px/s', 5, 300, 1, 1], ['COLD', 'speed of the squares', 'px/s', 5, 300, 1, 1]],
    init: function () { this.t = 0; this.P = []; this.n = cl(Math.round(80 * area() / 3) * 3, 150, 540); var per = this.n / 3; for (var i = 0; i < this.n; i++) { var k = i / per | 0, a = R() * 2 * PI, s = [this.HOT, this.MID, this.COLD][k] * v(.7, 1.3); this.P.push({ k: k, x: (k + v(.04, .96)) * W / 3, y: v(8, H - 8), vx: s * Math.cos(a), vy: s * Math.sin(a), r: R() * 6, w: v(-2, 2) }); } this.E = []; this.et = 0; },
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
    ROUTE: 150,
    K: [['ROUTE', 'speed of routing a wire', 'px/s', 20, 600, 5]],
    init: function () {
      this.B = []; this.RT = []; this.T = 0; this.ph = 0; this.ft = 0; var i, j, k, n;
      var mg = margin(); if (/\bscn__stage\b/.test(host.className)) { this.s = Math.min(.9, (H - 40) / 400); this.cx = W / 2; this.cy = H / 2; } else if (W >= 1240) { this.s = Math.min(.78, (H - 120) / 400); this.cx = W / 2 + (document.documentElement.dir === 'rtl' ? -1 : 1) * Math.min(320, W * .2); this.cy = 96 + 200 * this.s; } else if (W > 760) { this.s = .55; this.cx = W - 118; this.cy = H * .66; } else { this.s = .45; this.cx = W - 96; this.cy = H - 104; }
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
      var RS = this.ROUTE; this.RT.forEach(function (r) { var l = (T - r.t0) * RS; if (l <= 0) { done = 0; return; } x.strokeStyle = col(.5); x.lineWidth = 1; var hd = part(r.p, Math.min(l, r.L)); x.fillStyle = col(.95); x.fillRect(r.p[0][0] - 1.8, r.p[0][1] - 1.8, 3.6, 3.6); if (l < r.L) { done = 0; dot(hd[0], hd[1], 2.2, .95); } else x.fillRect(r.p[4][0] - 1.8, r.p[4][1] - 1.8, 3.6, 3.6); });
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
  host.__bgRestart = function () { if (W) { clear(); cur.init(); } };   /* the scenes page's "start again" (scenes.html) */
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

```

----- public/scenes.html -----
```
<!doctype html>
<html lang="en" class="no-js">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self'; connect-src 'self'; worker-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; upgrade-insecure-requests" />
    <meta name="referrer" content="strict-origin-when-cross-origin" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Living scenes · Numa Koudsie</title>
    <meta name="description" content="The small moving pictures behind the pages of Phyein Usul, each on its own: what it shows, the physics that drives it, and its numbers to change." />
    <meta name="author" content="Numa Koudsie" />
    <meta name="theme-color" content="#f5f1ea" />
    <link rel="stylesheet" href="styles/site.css" />
    <link rel="stylesheet" href="styles/catalog.css" />
    <link rel="stylesheet" href="styles/bg-scenes.css" />
    <link
      rel="icon"
      href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%237a1f2b'/%3E%3Ctext x='32' y='45' text-anchor='middle' font-family='Georgia,serif' font-size='34' font-weight='700' fill='%23fff'%3ENK%3C/text%3E%3C/svg%3E"
    />
    <script>document.documentElement.className = 'js';</script>
  </head>

  <body>
    <a class="skip-link" href="#scenes">Skip to the scenes</a>
    <header class="cat-top">
      <span style="display:inline-flex;align-items:center;gap:14px"><a href="index.html" aria-label="Phyein Usul, home page" style="display:inline-block;line-height:0"><img src="images/phyein-usul-mark.svg" alt="Phyein Usul" width="87" height="48" /></a><a href="index.html">← Numa Koudsie</a></span>
      <nav aria-label="Site">
        <a href="simulations.html">Simulations</a>
        <a href="portfolios.html">Projects</a>
        <a href="lucretius.html">Lucretius</a>
      </nav>
    </header>

    <main class="cat">
      <div class="cat__head">
        <div>
          <p class="cat__kicker">Behind the pages · twelve small pictures</p>
          <h1>Living scenes<span class="dot">.</span></h1>
          <p class="cat__lede">
            Behind and between the pages of this site, small pictures move: a forest, roots, pendulums, iron powder, a harmonica.
            Each is a little physics story. Here every one runs on its own, with what it shows, what drives it, and its numbers to change.
            They are pictures drawn for the eye, not the site's measured simulations; the pendulums are the exception, played from a
            run computed once on Kaggle.
          </p>
        </div>
      </div>
      <p class="scn-rm">You asked your system for reduced motion, so the scenes do not move here. The text of each stays below.</p>

      <div class="scn-list" id="scenes">

        <section class="scn" id="forest">
          <h2><span class="scn__n">S1</span> The forest</h2>
          <div class="scn__stage scn__stage--tall" data-bg="forest" data-bg-mask="none" data-bg-under="90"></div>
          <div class="scn__text">
            <p class="scn__where">Home page, the land under the title.</p>
            <p><b>What you see.</b> A few trees throw seeds; a seed that finds room grows into a tree in about one spring and summer, and over
            several years of two minutes each the land fills. Leaves fall in autumn, rot in the soil and are taken up by the roots of the young trees.</p>
            <p><b>What drives it.</b> The leaves breathe vapour that rises into the open sky and gathers into clouds. Each cloud is built
            in 3D, round puffs on a flat base 1000 m up, and drawn as seen by someone standing on the ground: near clouds high and
            large, far ones small by the horizon, their flat undersides seen from below, and the same wind carrying near clouds across
            faster than far ones. A cloud's droplets grow by condensation until collisions merge them into raindrops heavy enough to beat
            the updraft (their speed grows as r², Stokes' law); the rain feeds the seedlings, and in winter the clouds snow. On the home
            page the sky is open only in the two top corners, beside the title and beside the poem, so that is where the clouds gather.</p>
          </div>
          <div class="scn__knobs" data-for="forest"></div>
        </section>

        <section class="scn" id="roots">
          <h2><span class="scn__n">S2</span> Roots</h2>
          <div class="scn__stage" data-bg="roots" data-bg-mask="none"></div>
          <div class="scn__text">
            <p class="scn__where">Home page, the left margin, below the forest.</p>
            <p><b>What you see.</b> Roots grow down from the surface, branching like leaf veins or river beds; dots of sap climb back up.</p>
            <p><b>What drives it.</b> Space colonisation: water lies scattered in the soil, every drop pulls the nearest root tip within reach
            towards it, and a reached drop is used up. A root is as thick as the cube root of the number of tips it feeds (Murray's law: the
            cube of a parent's radius is the sum of its children's cubes), the rule that also sets the widths of blood vessels.</p>
          </div>
          <div class="scn__knobs" data-for="roots"></div>
        </section>

        <section class="scn" id="pairs">
          <h2><span class="scn__n">S3</span> Two pendulums and a spring</h2>
          <div class="scn__stage scn__stage--tall" data-bg="pairs" data-bg-mask="none"></div>
          <div class="scn__text">
            <p class="scn__where">Home page, the right margin, a pair on every beam.</p>
            <p><b>What you see.</b> Two pendulums, 1.5 m long with 10 kg steel bobs, joined by a weak spring. The left one starts swinging; within about 13.5 s its
            swing has drained completely into the right one, and after 27 s it is back. The curves under them are each pendulum's energy over
            one loop; the line marks the moment on show.</p>
            <p><b>What drives it.</b> Swinging together, the spring idles and both keep the pendulum's own frequency ω₁ = √(g/L); swinging
            against each other, the spring works and they go a little faster, ω₂ = √(ω₁² + 2ka²/(mL²)). Starting one pendulum starts both
            motions at once, and their beat carries the swing across and back with period 2π/(ω₂ − ω₁).
            The motion is not computed here: <code>tools/sims/coupled.py</code> integrated the full equations once on Kaggle, with the
            energy kept to a few parts in 10¹³, and this page plays that stored run.</p>
            <p class="scn__stored" data-stored="coupled"></p>
          </div>
          <div class="scn__knobs" data-for="pairs"></div>
        </section>

        <section class="scn" id="spin">
          <h2><span class="scn__n">S4</span> Spinners locking into step</h2>
          <div class="scn__stage" data-bg="spin" data-bg-mask="none"></div>
          <div class="scn__text">
            <p class="scn__where">Home page, the band before the simulations.</p>
            <p><b>What you see.</b> Little three-armed spinners turn at their own random speeds. A rotating field wanders over them, and those it
            passes turn in step with it, brighter while they are locked.</p>
            <p><b>What drives it.</b> Each spinner's angle obeys θ' = ω + K sin(φ − θ) + (pull of its neighbours), the Kuramoto and Adler picture of
            phase locking: when the field's pull K is stronger than the spinner's own mistuning, the spinner is captured.</p>
          </div>
          <div class="scn__knobs" data-for="spin"></div>
        </section>

        <section class="scn" id="shores">
          <h2><span class="scn__n">S5</span> The shores of light</h2>
          <div class="scn__stage" data-bg="shores" data-bg-mask="none"></div>
          <div class="scn__text">
            <p class="scn__where">Home page, the band above the footer.</p>
            <p><b>What you see.</b> Motes rise out of a slow dark tide and brighten as they cross its surface into the light.</p>
            <p><b>What drives it.</b> A picture of Lucretius (I 170, 179): things come into "the shores of light" from what was unseen.
            The surface is two waves added; brightness grows with the height above it.</p>
          </div>
          <div class="scn__knobs" data-for="shores"></div>
        </section>

        <section class="scn" id="powder">
          <h2><span class="scn__n">S6</span> Iron powder</h2>
          <div class="scn__stage" data-bg="powder" data-bg-mask="none"></div>
          <div class="scn__text">
            <p class="scn__where">Simulations page, beside the title.</p>
            <p><b>What you see.</b> Iron filings on a sheet line up along the field of two slowly turning bar magnets; a wire through the sheet
            switches its current on and off, and the filings around it curl into rings.</p>
            <p><b>What drives it.</b> Each grain turns along the local field and drifts sideways towards the nearest field line, as real filings
            do when the sheet is tapped (the tap is the shiver every 3.5 s).</p>
          </div>
          <div class="scn__knobs" data-for="powder"></div>
        </section>

        <section class="scn" id="harp">
          <h2><span class="scn__n">S7</span> A harmonica</h2>
          <div class="scn__stage" data-bg="harp" data-bg-mask="none"></div>
          <div class="scn__text">
            <p class="scn__where">Simulations page, the band above the footer.</p>
            <p><b>What you see.</b> A ten-hole harmonica plays; each note travels out through the air as rings that push the dots of air back
            and forth, and a dot far away moves only when the ring reaches it.</p>
            <p><b>What drives it.</b> Each hole's reed sends a wave of its own wavelength; the displacement at distance r is the reed's motion
            from the time r/c ago, so sound takes time to arrive (drawn here at a speed far below the real 343 m/s).</p>
          </div>
          <div class="scn__knobs" data-for="harp"></div>
        </section>

        <section class="scn" id="chip">
          <h2><span class="scn__n">S8</span> A chip</h2>
          <div class="scn__stage" data-bg="chip" data-bg-mask="none"></div>
          <div class="scn__text">
            <p class="scn__where">Portfolios page, beside the title.</p>
            <p><b>What you see.</b> The blocks of a chip are traced, wires are routed between them one by one, and the finished die is
            stamped again and again across a round wafer.</p>
            <p><b>What drives it.</b> Not physics but the order of chip making: design, routing, then photolithography repeats one mask over the wafer.</p>
          </div>
          <div class="scn__knobs" data-for="chip"></div>
        </section>

        <section class="scn" id="mix">
          <h2><span class="scn__n">S9</span> Mixing</h2>
          <div class="scn__stage" data-bg="mix" data-bg-mask="none"></div>
          <div class="scn__text">
            <p class="scn__where">Portfolios page, the band above the footer.</p>
            <p><b>What you see.</b> Three gases, hot triangles, warm rings and cold squares, wait in three chambers; the walls lift, the gases mix,
            and the curves show the mixing (solid) rise and the difference of temperature (dashed) fall.</p>
            <p><b>What drives it.</b> Elastic collisions between equal discs: each collision swaps the velocity components along the line between
            them, so energy spreads until every species moves alike, the second law in a box.</p>
          </div>
          <div class="scn__knobs" data-for="mix"></div>
        </section>

        <section class="scn" id="motes">
          <h2><span class="scn__n">S10</span> Dust in a sunbeam</h2>
          <div class="scn__stage" data-bg="motes" data-bg-mask="none"></div>
          <div class="scn__text">
            <p class="scn__where">Lucretius page, beside the title.</p>
            <p><b>What you see.</b> Dust trembles in a slanting beam of light, lit only inside the beam.</p>
            <p><b>What drives it.</b> Lucretius' own picture (II 112–141) of Brownian motion: each mote is slowed by drag and kicked at random by
            molecules nobody sees, dv = −γ v dt + σ dW, small motes trembling more.</p>
          </div>
          <div class="scn__knobs" data-for="motes"></div>
        </section>

        <section class="scn" id="swerve">
          <h2><span class="scn__n">S11</span> The swerve</h2>
          <div class="scn__stage" data-bg="swerve" data-bg-mask="none"></div>
          <div class="scn__text">
            <p class="scn__where">Lucretius page, the side margins.</p>
            <p><b>What you see.</b> Atoms fall side by side and never meet, until one tilts a little; it strikes a neighbour, and a cascade of collisions follows.</p>
            <p><b>What drives it.</b> Lucretius' clinamen (II 216–293): without the swerve the atoms would fall forever in parallel and nothing would form.</p>
          </div>
          <div class="scn__knobs" data-for="swerve"></div>
        </section>

        <section class="scn" id="seeds">
          <h2><span class="scn__n">S12</span> Seeds</h2>
          <div class="scn__stage" data-bg="seeds" data-bg-mask="none"></div>
          <div class="scn__text">
            <p class="scn__where">Lucretius page, the band above the footer.</p>
            <p><b>What you see.</b> Seeds fall and grow into a rose, an ear of wheat or a bunch of grapes, each from its own seed, then wither.</p>
            <p><b>What drives it.</b> Lucretius I 174–175: every thing comes from its own seed, at its own time.</p>
          </div>
          <div class="scn__knobs" data-for="seeds"></div>
        </section>
      </div>
    </main>

    <footer>
      <span>© 2026 Numa Koudsie</span>
      <span><a href="index.html">Home</a></span>
    </footer>

    <script src="scripts/bg-scenes.js" defer></script>
    <script>
      /* the controls of every scene, built from the scene's own table K: [property, meaning, unit, min, max, step, restart]
         (scripts/bg-scenes.js). A slider writes the property of the running scene; one marked restart starts the scene again. */
      document.addEventListener('DOMContentLoaded', function () {
        Array.prototype.forEach.call(document.querySelectorAll('.scn__knobs'), function (box) {
          var host = box.parentNode.querySelector('[data-bg]'), sc = host && host.__bgScene; if (!sc) { box.remove(); return; }
          var K = sc.K || [], html = '';
          K.forEach(function (k, i) {
            var id = host.getAttribute('data-bg') + '-' + k[0];
            html += '<label class="scn__k" for="' + id + '"><span>' + k[1] + (k[6] ? ' <i>(starts again)</i>' : '') + '</span>' +
              '<input type="range" id="' + id + '" min="' + k[3] + '" max="' + k[4] + '" step="' + k[5] + '" value="' + sc[k[0]] + '" data-i="' + i + '" />' +
              '<output>' + sc[k[0]] + (k[2] ? ' ' + k[2] : '') + '</output></label>';
          });
          box.innerHTML = '<p class="scn__kh">Numbers to change</p>' + html + '<button type="button" class="scn__again">Start again</button>';
          box.addEventListener('input', function (e) { var t = e.target, k = K[+t.getAttribute('data-i')]; if (!k) return; sc[k[0]] = +t.value;
            t.nextSibling.textContent = t.value + (k[2] ? ' ' + k[2] : ''); if (k[6]) host.__bgRestart(); });
          box.querySelector('.scn__again').addEventListener('click', function () { host.__bgRestart(); });
        });
        /* the stored pendulum run: its parameters and checks, read from the header of the file the page plays */
        var pe = document.querySelector('[data-stored=coupled]'), ph = document.querySelector('[data-bg=pairs]'), tries = 0;
        (function wait() { var s = ph && ph.__bgScene; if (s && s.D) { var h = s.D.hdr, p = h.params, d = h.derived, c = h.checks;
            pe.textContent = 'Stored run: L = ' + p.L + ' m, m = ' + p.m + ' kg, spring at a = ' + p.a + ' m, pivots d = ' + p.d + ' m apart, k = ' + d.k_N_per_m.toFixed(3) +
              ' N/m, start θ₀ = ' + p.theta0 + ' rad; one loop ' + d.loop_s.toFixed(2) + ' s; the swing has crossed at ' + c.crossed_at_s.toFixed(2) +
              ' s (2π/(ω₂ − ω₁) ÷ 2 = ' + c.half_beat_linear_s.toFixed(2) + ' s for small swings); energy kept to ' + c.energy_rel_drift.toExponential(1) +
              '; computed ' + s.D.gen.date + ' from commit ' + String(s.D.gen.commit).slice(0, 7) + ', SHA-256 checked.'; }
          else if (s && s.err) pe.textContent = 'The stored run could not be loaded: ' + s.err; else if (tries++ < 100) setTimeout(wait, 200); })();
      });
    </script>
  </body>
</html>

```
