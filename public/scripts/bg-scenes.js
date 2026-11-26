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
    var key = name + '/' + file; if (STORE[key]) return STORE[key];
    GEN = GEN || fetch(DATA + 'generations.json').then(function (r) { if (!r.ok) throw new Error('no generations.json'); return r.json(); });
    return STORE[key] = GEN.then(function (g) {
      var e = g.generations.filter(function (q) { return q.sim === name; }).pop(); if (!e) throw new Error('no data for ' + name);
      return fetch(DATA + name + '/' + e.date + '/' + file).then(function (r) { if (!r.ok) throw new Error(file + ' ' + r.status); return r.arrayBuffer(); }).then(function (buf) {
        return crypto.subtle.digest('SHA-256', buf).then(function (d) {
          var hex = Array.prototype.map.call(new Uint8Array(d), function (b) { return (b < 16 ? '0' : '') + b.toString(16); }).join('');
          if (hex !== e.files[file].sha256) throw new Error(file + ': SHA-256 differs from generations.json');
          var hl = new DataView(buf).getUint32(4, true), hdr = JSON.parse(new TextDecoder().decode(new Uint8Array(buf, 8, hl)));
          var pay = buf.slice(8 + hl);   /* the numbers after the header: int16 for most models; spinners.py stores bytes (it reads `raw`) */
          return { hdr: hdr, frames: pay.byteLength % 2 ? null : new Int16Array(pay), raw: pay, cols: hdr.columns.length, gen: e, sha_ok: true };
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

  function sstep(u) { u = cl(u, 0, 1); return u * u * (3 - 2 * u); }

  /* ---- the sky: the ten kinds of cloud (the genera of the WMO International Cloud Atlas), each built in 3D and seen from the ground ----
     (25 November 2026: the user asked for every kind of cloud by shape and form, "the very large, the very long, the thin".)
     Clouds are sorted by their form and by the level they live at (temperate latitudes: low, from the ground to 2 km; middle, 2 to
     7 km; high, 5 to 13 km). The ten genera, with the height h (m) each is built at here:
       Ci  Cirrus         high    thin white fibres and hooks ("mares' tails"): ice crystals falling out of a small head and trailing
       Cc  Cirrocumulus   high    a thin sheet of very small grains in ripples ("mackerel sky")
       Cs  Cirrostratus   high    a transparent veil over the whole sky; the sun shines through with a ring (halo) of 22° around it
       Ac  Altocumulus    middle  a field of small rounded masses in rows ("sheep"), shaded underneath
       As  Altostratus    middle  a grey sheet with streaks; the sun shows as through ground glass
       Ns  Nimbostratus   low and thick   a dark, shapeless layer that rains or snows for hours
       Sc  Stratocumulus  low     long rolls of flattened lumps in rows that run for kilometres, with gaps between
       St  Stratus        low     a flat grey layer with a ragged edge, like fog that does not touch the ground
       Cu  Cumulus        low     a single heap: flat base, domed top of round puffs
       Cb  Cumulonimbus   low base, top to 12 km   the thunder cloud: a tower through all levels, spreading into a flat anvil
     The eye stands on the ground; the horizon is the line y = GY. A point X m to the right, Y m up and Z m ahead is seen at
         x = XC + F X / Z,   y = GY − F Y / Z                    (a pinhole camera, proj(); F in px sets how wide it looks:
                                                                 with F = 1.5 GY the top of the picture is 34° above the horizon)
     Every cloud is first built in its own frame, in metres (make()): round puffs for the heaps, flat patches lying in the plane of
     its height for the layers, curved threads for the fibres. Each frame its parts are carried into the eye's frame and
     projected (paint()). A flat patch of radii (rx, rz) at height Y and distance Z is seen as an ellipse F rx / Z wide and
     F rz Y / Z² high: the further away, the more it is seen edge on. So a field of altocumulus crowds and flattens towards the
     horizon, a high cloud must be far away to be seen low, and one wind moves near clouds faster across the picture than far ones.
     Everything is drawn into the sky's own canvas (cv), which the scene then lays on its picture. ---- */
  var GENUS = {
    Ci: { n: 'Cirrus', h: 9000, r: '5–13 km', lv: 2 }, Cc: { n: 'Cirrocumulus', h: 8500, r: '5–13 km', lv: 2 }, Cs: { n: 'Cirrostratus', h: 9500, r: '5–13 km', lv: 2 },
    Ac: { n: 'Altocumulus', h: 4000, r: '2–7 km', lv: 1 }, As: { n: 'Altostratus', h: 4500, r: '2–7 km', lv: 1 },
    Ns: { n: 'Nimbostratus', h: 900, r: 'base below 2 km', lv: 0 }, Sc: { n: 'Stratocumulus', h: 1500, r: 'below 2 km', lv: 0 }, St: { n: 'Stratus', h: 300, r: 'below 2 km', lv: 0 },
    Cu: { n: 'Cumulus', h: 1000, r: 'base below 2 km', lv: 0 }, Cb: { n: 'Cumulonimbus', h: 1000, r: 'top to 12 km', lv: 0 } };
  /* the puffs of a heap, in units of its size s: [across, up (the base is 0), in depth, radius]; far puffs first */
  function cuPuffs() { var P = [], n = 16 + (R() * 10 | 0); for (var i = 0; i < n; i++) { var u = (R() + R() + R() - 1.5) * .8, w = (R() + R() + R() - 1.5) * .5, core = Math.exp(-(u * u + w * w) / .35), rr = .15 + .24 * core * v(.6, 1.1); P.push([u, rr * .5 + .62 * core * R(), w, rr]); }
    P.sort(function (p, q) { return q[2] - p[2]; });
    return { P: P, ax: Math.max.apply(null, P.map(function (q) { return Math.abs(q[0]) + q[3] * .9; })), az: Math.max.apply(null, P.map(function (q) { return Math.abs(q[2]) + q[3] * .9; })) }; }
  /* a thunder cloud's tower: fifteen storeys of six puffs, widening upward (its top is 6.7 sizes above its base) */
  function cbPuffs() { var P = []; for (var j = 0; j < 15; j++) for (var q = 0; q < 6; q++) { var an = R() * 2 * PI, rad = (.55 + .05 * j) * Math.sqrt(R()); P.push([rad * Math.cos(an), .3 + j * .42 + v(-.12, .12), rad * Math.sin(an) * .7, .36 + .014 * j + v(-.07, .07)]); }
    P.sort(function (p, q) { return q[2] - p[2]; }); return { P: P, ax: 1.45, az: 1.15 }; }
  function mkSky(GY, XC, F) {
    /* two canvases: the soft one (layers, lumps, fibres) at half the picture's resolution, which costs a quarter and suits their
       softness; the crisp one, at full resolution, for the heaps drawn in line. RC: the strips of the picture that hold sky. */
    var Q = .5, cvs = document.createElement('canvas'), g = cvs.getContext('2d'), cv2 = document.createElement('canvas'), g2 = cv2.getContext('2d'), SP = {}, RC = [[0, W]];
    cvs.width = Math.max(2, Math.ceil(W * Q)); cvs.height = Math.max(2, Math.ceil(GY * Q)); cv2.width = Math.max(2, Math.ceil(W)); cv2.height = Math.max(2, Math.ceil(GY));
    function proj(X, Y, Z) { var f = F / Z; return [XC + X * f, GY - Y * f, f]; }
    /* a soft round stamp of one tone (paper 0 to wine 1), made once per tone and stretched into every ellipse drawn */
    function sprite(t) { var k = Math.round(t * 20); if (!SP[k]) { var c = document.createElement('canvas'), q = c.getContext('2d'), rg; c.width = c.height = 64; rg = q.createRadialGradient(32, 32, 0, 32, 32, 32); rg.addColorStop(0, mixc(k / 20, 1)); rg.addColorStop(.5, mixc(k / 20, .8)); rg.addColorStop(1, mixc(k / 20, 0)); q.fillStyle = rg; q.fillRect(0, 0, 64, 64); SP[k] = c; } return SP[k]; }
    function ell(px, py, sx, sy, t, a) { if (sx < .3 || a < .004 || px + sx < 0 || px - sx > W || py + sy < 0 || py - sy > GY) return; g.globalAlpha = Math.min(1, a); g.drawImage(sprite(t), px - sx, py - sy, 2 * sx, 2 * sy); }
    /* a flat patch lying in the horizontal plane at height Y, seen from below */
    function flat(X, Y, Z, rx, rz, t, a) { if (Z < 30) return; var p = proj(X, Y, Z); ell(p[0], p[1], rx * p[2], Math.max(.7, rz * p[2] * Y / Z), t, a); }
    /* a rounded mass with thickness th: its pale flank and top above, its darker flat belly below */
    function lump(X, Y, Z, rx, rz, th, a) { if (Z < 30) return; var p = proj(X, Y, Z), sx = rx * p[2], sy = Math.max(.7, rz * p[2] * Y / Z), up = th * p[2]; ell(p[0], p[1] - up * .6, sx * 1.05, sy + up * .6, .2, a); ell(p[0], p[1] + sy * .15, sx * .85, sy * .8, .5, a * .75); }
    /* build a cloud of genus k in its own frame (metres); with o given, rebuild that object (a new cloud drifting in) */
    function make(k, o) {
      o = o || {}; o.k = k; o.E = null; o.B = null; o.Rn = null; o.sk = -1; var i, j, E = [], B = [];
      if (k === 'Cu') { var cu = cuPuffs(); o.P = cu.P; o.ax = cu.ax; o.az = cu.az; o.hb = GENUS.Cu.h; o.s = 500; o.ext = 600; }
      else if (k === 'Cb') { var cb = cbPuffs(); o.P = cb.P; o.ax = cb.ax; o.az = cb.az; o.hb = GENUS.Cb.h; o.s = 1400; o.ext = 5500; o.vg = 1; o.An = []; o.Rn = [];
        for (i = 0; i < 6; i++) o.An.push([v(-1, 2.6), v(-.7, .7), v(1.5, 2.3), v(1.1, 1.5)]);           /* the anvil: flat patches at the top, drawn out downwind */
        for (i = 0; i < 12; i++) o.Rn.push([v(-1, 1), v(-.6, .6)]); }
      else if (k === 'Sc') { var phi = v(-.3, .3), cs = Math.cos(phi), sn = Math.sin(phi);                  /* four long rolls, each a chain of flattened lumps */
        for (i = 0; i < 4; i++) { var off = (i - 1.5) * 950 + v(-80, 80); for (j = -13; j <= 13; j++) { if (R() < .1) continue; var al = j * 340 + v(-60, 60); E.push([al * cs - off * sn, al * sn + off * cs, v(230, 300), v(170, 230), v(140, 220)]); } } o.ext = 4800; }
      else if (k === 'Ac') { for (i = -5; i <= 5; i++) for (j = -4; j <= 4; j++) { if (R() < .22) continue; E.push([i * 300 + v(-60, 60) + (j & 1) * 150, j * 300 + v(-60, 60) + 90 * Math.sin(i * .9), v(95, 140), v(95, 140), v(60, 110)]); } o.ext = 1900; }
      else if (k === 'Cc') { for (i = -11; i <= 11; i++) for (j = -7; j <= 7; j++) { if (R() < .12) continue; E.push([i * 110 + 30 * Math.sin(j * 1.3), j * 110 + 35 * Math.sin(i * .8), v(30, 44)]); } o.ext = 1400; }
      else if (k === 'Ci') { for (i = 0, j = 5 + (R() * 4 | 0); i < j; i++) E.push([v(-1800, 1800), v(-1200, 1200), v(2500, 5200), v(400, 900), v(-500, 500), v(350, 700)]); o.ext = 5200; }   /* threads: [x, z of the head, length, how far it falls, sideways drift, size of the hook] */
      else if (k === 'St') { for (i = 0; i < 5; i++) B.push([v(-700, 700), v(-350, 350), v(500, 800), v(350, 500), .4, .42]); for (i = 0; i < 9; i++) B.push([v(-1500, 1500), v(-500, 500), v(70, 140), v(70, 140), .34, .45]); o.ext = 1600; }
      else if (k === 'Ns') { for (i = 0; i < 6; i++) B.push([v(-2200, 2200), v(-1200, 1200), v(1500, 2400), v(1100, 1600), .58, .18]); o.Rn = []; for (i = 0; i < 16; i++) o.Rn.push([v(-2000, 2000), v(-900, 900)]); o.ext = 4500; }
      else if (k === 'As') { for (i = 0; i < 6; i++) B.push([v(-4000, 4000), v(-2500, 2500), v(3000, 4500), v(2200, 3000), .38, .3]); for (i = 0; i < 12; i++) B.push([v(-5000, 5000), v(-3000, 3000), v(2500, 4500), v(90, 160), .5, .22]); o.ext = 8000; }
      else if (k === 'Cs') { for (i = 0; i < 5; i++) B.push([v(-4000, 4000), v(-2500, 2500), v(3000, 4500), v(2200, 3000), .24, .36]); for (i = 0; i < 14; i++) B.push([v(-5000, 5000), v(-3000, 3000), v(2000, 4000), v(60, 110), .4, .2]); o.ext = 8000; }
      if (E.length) { E.sort(function (p, q) { return q[1] - p[1]; }); o.E = E; } if (B.length) o.B = B;
      return o;
    }
    /* a heap of puffs (cumulus, the tower of a cumulonimbus), drawn as the site draws its trees, with a line around it: one
       outline around the whole heap, its puffs soft pale lumps inside (the cauliflower look), shaded towards the base; nothing
       shows below the far edge of the flat base; then the underside, seen from below, as a darker floor. Each heap is drawn on
       its own small canvas, so the whole heap fades as one. */
    function puffs(o, a) {
      if (a < .01) return; var s = o.s, vg = o.vg === undefined ? 1 : Math.min(1, o.vg / .75), key = s * (1 + vg), p0 = proj(o.X, o.hb, o.Z);
      /* the heap's picture is kept and only drawn again when its size has changed by 2 % (it grows and shrinks with its water) */
      if (!(Math.abs(key - o.sk) <= .02 * key) || Math.abs(o.sZ - o.Z) > 1) {
        var P = o.P, pts = [], i, bx0 = 1e9, bx1 = -1e9, by0 = 1e9, by1 = -1e9; o.sk = key; o.sZ = o.Z; o.sw = 0;
        for (i = 0; i < P.length; i++) { var q = P[i], p = proj(o.X + q[0] * s, o.hb + q[1] * vg * s, o.Z + q[2] * s), rad = q[3] * s * p[2]; pts.push([p[0], p[1], rad]);
          bx0 = Math.min(bx0, p[0] - rad); bx1 = Math.max(bx1, p[0] + rad); by0 = Math.min(by0, p[1] - rad); by1 = Math.max(by1, p[1] + rad); }
        var ring = []; for (i = 0; i < 24; i++) { var an = i / 24 * 2 * PI, pb = proj(o.X + Math.cos(an) * o.ax * s, o.hb, o.Z + Math.sin(an) * o.az * s); ring.push(pb); by1 = Math.max(by1, pb[1]); bx0 = Math.min(bx0, pb[0]); bx1 = Math.max(bx1, pb[0]); }
        var ox = Math.floor(bx0) - 2, oy = Math.floor(by0) - 2, ww = Math.ceil(bx1 - ox) + 4, hh = Math.ceil(by1 - oy) + 4; if (ww < 2 || hh < 2 || ww > 2400 || hh > 2400) return;
        var scr = o.spr || (o.spr = document.createElement('canvas')); scr.width = ww; scr.height = hh;
        var c = scr.getContext('2d'); c.translate(-ox, -oy);
        var low = ring.slice(0, 13); c.beginPath(); c.moveTo(bx0 - 4, by0 - 4); c.lineTo(bx1 + 4, by0 - 4); c.lineTo(bx1 + 4, low[0][1]); low.forEach(function (p) { c.lineTo(p[0], p[1]); }); c.lineTo(bx0 - 4, low[12][1]); c.closePath(); c.clip();
        /* (a) every puff's circle stroked, then (b) all puffs filled flat: the fill hides every stroke inside the heap, so only the
           outline of the whole heap is left; (c) each puff a soft pale lump, lit from the upper left; (d) the heap shaded towards
           its base; (e) below, the floor of the base */
        c.lineWidth = 2; c.strokeStyle = mixc(.8, .6); c.beginPath(); pts.forEach(function (p) { c.moveTo(p[0] + p[2], p[1]); c.arc(p[0], p[1], p[2], 0, 7); }); c.stroke();
        c.fillStyle = mixc(.17, 1); c.beginPath(); pts.forEach(function (p) { c.moveTo(p[0] + p[2], p[1]); c.arc(p[0], p[1], p[2], 0, 7); }); c.fill();
        pts.forEach(function (p) { var rg = c.createRadialGradient(p[0] - p[2] * .22, p[1] - p[2] * .38, p[2] * .05, p[0] - p[2] * .1, p[1] - p[2] * .15, p[2] * .95); rg.addColorStop(0, mixc(.02, .95)); rg.addColorStop(.6, mixc(.08, .55)); rg.addColorStop(1, mixc(.2, 0));
          c.fillStyle = rg; c.beginPath(); c.arc(p[0], p[1], p[2], 0, 7); c.fill(); });
        c.globalCompositeOperation = 'source-atop'; var sh = c.createLinearGradient(0, by0, 0, low[6][1]); sh.addColorStop(0, mixc(.5, 0)); sh.addColorStop(.55, mixc(.5, .06)); sh.addColorStop(1, mixc(.55, .5)); c.fillStyle = sh; c.fillRect(bx0 - 4, by0 - 4, bx1 - bx0 + 8, by1 - by0 + 8); c.globalCompositeOperation = 'source-over';
        var cxr = 0, cyr = 0, rx0 = 1e9, rx1 = -1e9, ry0 = 1e9, ry1 = -1e9; ring.forEach(function (p) { cxr += p[0]; cyr += p[1]; rx0 = Math.min(rx0, p[0]); rx1 = Math.max(rx1, p[0]); ry0 = Math.min(ry0, p[1]); ry1 = Math.max(ry1, p[1]); }); cxr /= 24; cyr /= 24;
        var rx = Math.max(1, (rx1 - rx0) / 2), ry = Math.max(2, (ry1 - ry0) / 2);
        c.translate(cxr, cyr); c.scale(1, ry / rx); var rb = c.createRadialGradient(0, 0, 0, 0, 0, rx * .85); rb.addColorStop(0, mixc(.55, .9)); rb.addColorStop(.6, mixc(.48, .7)); rb.addColorStop(1, mixc(.4, 0)); c.fillStyle = rb; c.beginPath(); c.arc(0, 0, rx * .85, 0, 7); c.fill();
        o.dx = ox - p0[0]; o.dy = oy - p0[1]; o.sw = ww; o.sh = hh;
      }
      if (!o.sw || p0[0] + o.dx > W || p0[0] + o.dx + o.sw < 0) return;
      g2.globalAlpha = Math.min(1, a); g2.drawImage(o.spr, p0[0] + o.dx, p0[1] + o.dy);
    }
    /* rain or snow falling out of a base at height hb: dashed threads that slide down */
    function shafts(o, hb, u, a, T) { g.globalAlpha = Math.min(1, a); g.strokeStyle = mixc(.75, .55); g.lineWidth = 1; g.setLineDash([5, 7]); g.lineDashOffset = -T * 60; g.beginPath();
      for (var i = 0; i < o.Rn.length; i++) { var e = o.Rn[i], p1 = proj(o.X + e[0] * u, hb, o.Z + e[1] * u), p2 = proj(o.X + e[0] * u + .12 * hb, 0, o.Z + e[1] * u); g.moveTo(p1[0], p1[1]); g.lineTo(p2[0], p2[1]); } g.stroke(); g.setLineDash([]); }
    /* the sun behind a high veil (a ring of 22° around it, the halo of ice crystals: its radius in the picture is F tan 22°) or behind
       a grey middle sheet (a bright blur, as through ground glass) */
    function sun(sx, sy, aAs, aCs, rad) {
      if (aCs > .01) { g.globalAlpha = Math.min(1, aCs); g.lineWidth = 2.5; g.strokeStyle = mixc(.5, .4); g.beginPath(); g.arc(sx, sy, rad || .404 * F, 0, 7); g.stroke(); g.lineWidth = 1; g.strokeStyle = mixc(.65, .75); g.beginPath(); g.arc(sx, sy, 6, 0, 7); g.stroke(); }
      if (aAs > .01) { ell(sx, sy, 36, 36, 0, .85 * aAs); ell(sx, sy, 10, 10, 0, aAs); }
    }
    function paint(o, a, T) {
      if (a < .01) return; var k = o.k, h = GENUS[k].h, z = o.sz || 1, E = o.E, i, e, p;
      if (k === 'Cu') { puffs(o, a); return; }
      if (k === 'Cb') { if (o.rain) shafts(o, o.hb, o.s, a * o.rain, T); puffs(o, a); var ag = cl((o.vg - .7) / .3, 0, 1), ht = o.hb + 6.5 * o.s;
        if (ag > 0) { for (i = 0; i < o.An.length; i++) { e = o.An[i]; flat(o.X + e[0] * o.s, ht + .2 * o.s, o.Z + e[1] * o.s, e[2] * o.s * ag * 1.1, e[3] * o.s * ag * 1.1, .2, .9 * a * ag); } for (i = 0; i < o.An.length; i++) { e = o.An[i]; flat(o.X + e[0] * o.s, ht, o.Z + e[1] * o.s, e[2] * o.s * ag * .85, e[3] * o.s * ag * .85, .45, .7 * a * ag); } }
        return; }
      if (o.Rn) shafts(o, h, z, a, T);
      if (o.B) for (i = 0; i < o.B.length; i++) { e = o.B[i]; flat(o.X + e[0] * z, h, o.Z + e[1] * z, e[2] * z, e[3] * z, e[4], e[5] * a); }
      if (k === 'Sc' || k === 'Ac') for (i = 0; i < E.length; i++) { e = E[i]; lump(o.X + e[0] * z, h, o.Z + e[1] * z, e[2] * z, e[3] * z, e[4] * z, a); }
      else if (k === 'Cc') { g.globalAlpha = Math.min(1, a * .8); g.fillStyle = mixc(.38, 1); g.beginPath(); for (i = 0; i < E.length; i++) { e = E[i]; var zz = o.Z + e[1] * z; if (zz < 30) continue; p = proj(o.X + e[0] * z, h, zz); var r = Math.max(.8, e[2] * z * p[2]); if (p[0] < -4 || p[0] > W + 4 || p[1] < -4 || p[1] > GY + 4) continue; g.moveTo(p[0] + r, p[1]); g.ellipse(p[0], p[1], r, Math.max(.6, r * Math.min(1, h / zz * 1.3)), 0, 0, 7); } g.fill(); }
      else if (k === 'Ci') { g.lineCap = 'round'; for (i = 0; i < E.length; i++) { e = E[i]; var pp = null; for (var q = 0; q <= 10; q++) { var s = q / 10, hk = e[5] * Math.pow(Math.max(0, 1 - s / .2), 2), zc = o.Z + (e[1] + e[4] * s * s) * z; if (zc < 30) { pp = null; continue; }
            p = proj(o.X + (e[0] - e[2] * s + hk * .7) * z, h + (hk - e[3] * Math.pow(s, .8)) * z, zc);
            if (pp) { g.globalAlpha = Math.min(1, a * (.9 * (1 - s) + .1)); g.strokeStyle = mixc(.85, 1); g.lineWidth = 3.2 * (1 - s) + .9; g.beginPath(); g.moveTo(pp[0], pp[1]); g.lineTo(p[0], p[1]); g.stroke(); } pp = p; } } g.lineCap = 'butt'; }
      if (o.sun) { p = proj(o.X, h, o.Z); sun(p[0], p[1], k === 'As' ? a : 0, k === 'Cs' ? a : 0, o.halo); }
    }
    return { proj: proj, make: make, paint: paint, puffs: puffs, sun: sun,
      /* begin(strips): clear, and keep all drawing inside the strips [x, width] of the picture that hold sky */
      begin: function (rc) { RC = rc || [[0, W]]; [[g, Q, cvs], [g2, 1, cv2]].forEach(function (a) { var c = a[0]; c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = 1; c.globalCompositeOperation = 'source-over'; c.clearRect(0, 0, a[2].width, a[2].height);
          c.save(); c.setTransform(a[1], 0, 0, a[1], 0, 0); c.beginPath(); RC.forEach(function (r) { c.rect(r[0], 0, r[1], GY); }); c.clip(); }); },
      wash: function (t, a) { if (a < .004) return; g.globalAlpha = 1; g.fillStyle = mixc(t, a); RC.forEach(function (r) { g.fillRect(r[0], 0, r[1], GY); }); },   /* a layer that covers the whole sky */
      /* end(mask): keep of the sky only what the mask lets through */
      end: function (mask) { [g, g2].forEach(function (c) { c.globalAlpha = 1; if (mask) { c.globalCompositeOperation = 'destination-in'; c.drawImage(mask, 0, 0, mask.width, mask.height, 0, 0, W, GY); c.globalCompositeOperation = 'source-over'; } c.restore(); }); },
      /* lay the sky on the scene's picture x: under what is already drawn there (under = true), or over it */
      blit: function (x, a, under) { x.globalAlpha = a; if (under) x.globalCompositeOperation = 'destination-over';
        RC.forEach(function (r) { var soft = function () { x.drawImage(cvs, r[0] * Q, 0, r[1] * Q, Math.floor(GY * Q), r[0], 0, r[1], Math.floor(GY * Q) / Q); }, crisp = function () { x.drawImage(cv2, r[0], 0, r[1], Math.floor(GY), r[0], 0, r[1], Math.floor(GY)); };
          if (under) { crisp(); soft(); } else { soft(); crisp(); } });
        x.globalAlpha = 1; x.globalCompositeOperation = 'source-over'; } };
  }

  /* ---- the wind and its pendulums, drawn from the stored run (tools/sims/windpend.py): used by the right rail of the home page and by
     the scene `wind`. D: the stored data; t: time (s); cx: the strip's centre line (px); top: the y of ξ = 0; wid: the strip's
     width (px); sc: px per metre; beams: the y of each beam below top (px); fd(y): how strongly to draw at that depth.
     Lines: stored row l holds η (mm) of streamline l at ξ − c t = j λ / n. A point y px below top is at ξ = y / sc, so it shows
     the stored point j = ((ξ − c t) mod λ) n / λ. Pendulums: a beam at ξ_b plays the stored frame of the time t − ξ_b / c. ---- */
  function windDraw(D, t, cx, top, wid, sc, beams, fd, y0, y1) {
    var hd = D.hdr, pr = hd.params, dv = hd.derived, F = D.frames, K = hd.columns.length, nf = hd.frames, LI = hd.lines, off = LI.offset_int16, ns = LI.points, lam = pr.lam, c = dv.c, l, y;
    x.lineWidth = .8; x.strokeStyle = col(.2);
    for (l = 0; l < LI.n; l++) { var b0 = off + l * ns; if (Math.abs(F[b0] * .001 * sc) > wid / 2 + 40) continue; x.beginPath();
      for (y = y0 - 6; y <= y1 + 6; y += 6) { var u = ((((y - top) / sc - c * t) / lam) % 1 + 1) % 1 * ns, j = u | 0, e = u - j, px = cx + (F[b0 + j] * (1 - e) + F[b0 + (j + 1) % ns] * e) * .001 * sc; if (y === y0 - 6) x.moveTo(px, y); else x.lineTo(px, y); }
      x.stroke(); }
    /* beyond the stored strip the wind is plain: its lines are straight, at the same spacing (equal steps of the stream function) */
    var dl = pr.WS / (LI.n - 1) * sc; x.beginPath(); for (var px2 = pr.WS / 2 * sc + dl; px2 < wid / 2 + 2; px2 += dl) { x.moveTo(cx + px2, y0); x.lineTo(cx + px2, y1); x.moveTo(cx - px2, y0); x.lineTo(cx - px2, y1); } x.stroke();
    var Lp = pr.L * sc, Rg = pr.R * sc, all = wid >= 2 * pr.a * sc + 2 * (Rg + Lp * .3) + 8;
    beams.forEach(function (by0) { var by = top + by0; if (by < y0 - Lp - Rg - 10 || by > y1 + 10) return; var f = fd(by0), k = (((Math.round((t - by0 / sc / c) / hd.dt) % nf) + nf) % nf) * K;
      x.strokeStyle = col(.5 * f); x.lineWidth = 2.2; ln(cx - Math.min(wid / 2 - 6, pr.a * sc + 30), by, cx + Math.min(wid / 2 - 6, pr.a * sc + 30), by);
      for (var q = 0; q < K; q++) { if (!all && q !== (K - 1) / 2) continue; var th = F[k + q] * 1e-4, px0 = cx + dv.etas[q] * sc, bx = px0 + Lp * Math.sin(th), bb = by + Lp * Math.cos(th);
        x.strokeStyle = col(.55 * f); x.lineWidth = 1; ln(px0, by, bx, bb); dot(px0, by, 1.8, .7 * f);
        /* the globe: thin paper, so the page shows through; an outline, a faint fill and one meridian that turns with the thread */
        x.fillStyle = 'rgba(245,241,234,' + (.85 * f) + ')'; x.beginPath(); x.arc(bx, bb, Rg, 0, 7); x.fill(); x.fillStyle = col(.08 * f); x.fill(); x.strokeStyle = col(.7 * f); x.lineWidth = 1.1; x.stroke();
        x.strokeStyle = col(.3 * f); x.lineWidth = .8; x.beginPath(); x.ellipse(bx, bb, Rg * .45, Rg, -th, 0, 7); x.stroke(); }
    });
  }

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
         TONE       -      how strongly the whole sky is drawn over the paper
         CB         -      water the cumulus clouds must hold together, in early summer, for a thunder cloud (cumulonimbus) to
                           rise: the forest's own vapour feeds it; one a year at most
       The kinds of cloud, how each is built and seen: mkSky() above. Which is in the sky when: SEASON below. */
    K: [['YEAR', 'length of a year', 's', 20, 480, 5], ['GROW', 'light a seedling needs to grow up', 's', 5, 200, 1], ['SEED', 'seeds per grown tree per second of spring and summer', '1/s', 0, .3, .005],
        ['FEED', 'share of rain and rotted leaves that feeds growth', '', 0, 1, .05], ['COND', 'condensation in the clouds', 'px/s', 0, .05, .001], ['RAIN', 'rain from grown droplets', '1/s', 0, 2, .05], ['SOIL', 'vapour from open ground', '1/s per 100 px', 0, 3, .05],
        ['HB', 'height of the cloud base', 'm', 300, 3000, 50, 1], ['SIZE', 'size of a cloud per unit of water', 'm', 30, 250, 5, 1], ['WIND', 'wind', 'm/s', 0, 15, .5], ['NCL', 'open sky per cloud at the start', 'px²', 8000, 80000, 1000, 1], ['EVAP', 'how long a cloud keeps its water', 's', 10, 600, 5], ['CB', 'water in the sky that starts a thunder cloud', '', 0, 40, .5], ['TONE', 'strength of the sky', '', .1, 1, .02]],
    YEAR: 120, GROW: 50, SEED: .04, FEED: .25, START: 3, LIFE: [2.5, 4], FALL: .15, COND: .003, RAIN: .2, SOIL: .6, TONE: .55, EVAP: 60, CB: 4,
    /* when each kind of cloud is in the sky, as parts of the year (0 = the first day of spring, .25 summer, .5 autumn, .75 winter);
       each comes and goes over 4 % of the year. Spring: cumulus, fields of altocumulus, cirrocumulus. Summer: cumulus, cirrus, and
       the thunder cloud. Autumn opens as a warm front does: cirrostratus with its halo, thickening to altostratus, then
       nimbostratus and long rain; then rows of stratocumulus; winter: stratus and snow. */
    SEASON: { Cu: [-.1, .56, .97, 1.1], Ac: [.04, .30], Cc: [.10, .27], Ci: [.18, .52], Cs: [.47, .61], As: [.56, .71], Ns: [.66, .80], Sc: [.76, .92], St: [.86, .99] },
    NG: [['Cs', 2], ['Ci', 5], ['Cc', 4], ['As', 2], ['Ac', 5], ['Ns', 2], ['Sc', 3], ['St', 3]],      /* how many clouds of each layer kind drift through the sky */ OPEN: 240, HB: 1000, SIZE: 80, WIND: 4, NCL: 25000,
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
        CL.push(flo - 30 - 30 >= Math.min(this.OPEN, this.GY * .3) ? { t: 30, b: flo - 30, f: flo < this.GY * .55 ? 0 : 1 } : null); }
      this.CL = CL;
      /* the mask of the sky: one pixel per 16 px column and row, stretched smoothly over the picture when the sky is laid on it.
         Full where a column has open sky; fading out over ten columns (160 px) towards text; below a column's sky it fades over 24 px
         above text, and over 30 % of the ground height where only the trees stand below. So layers and wide clouds never cross
         the text and are never cut by an edge. */
      var mh = Math.ceil(this.GY / 16), mk = this.msk = document.createElement('canvas'), mg, j, dist = [], d0 = 99; mk.width = Math.max(1, n); mk.height = Math.max(1, mh); mg = mk.getContext('2d');
      for (i = 0; i < n; i++) { d0 = CL[i] ? d0 + 1 : 0; dist[i] = d0; } d0 = 99; for (i = n - 1; i >= 0; i--) { d0 = CL[i] ? d0 + 1 : 0; dist[i] = Math.min(dist[i], d0); }
      for (i = 0; i < n; i++) { var c0 = CL[i]; if (!c0) continue; var hf = sstep(dist[i] / 10), fd = c0.f ? this.GY * .3 : 24;
        for (j = 0; j < mh; j++) { var av = hf * cl(1 - (j * 16 + 8 - c0.b) / fd, 0, 1); if (av > 0) { mg.fillStyle = 'rgba(0,0,0,' + av + ')'; mg.fillRect(i, j, 1, 1); } } }
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
    proj: function (X, Y, Z) { var f = this.FF / Z; return [this.XC + X * f, this.GY - Y * f, f]; },
    cloud: function (xs, ys, m) {              /* a new cumulus whose base is seen at (xs, ys), holding the water m */
      var Z = this.FF * this.HB / Math.max(30, this.GY - ys), cu = cuPuffs(), c = { k: 'Cu', X: (xs - this.XC) * Z / this.FF, Z: Z, hb: this.HB, m: m, r: .55, s: this.SIZE * Math.cbrt(m), a: 0, at: 0, P: cu.P, ax: cu.ax, az: cu.az };
      this.Cs.push(c); return c; },
    /* where a cloud is seen: its base centre and its half width on the page */
    seen: function (c) { var p = this.proj(c.X, this.HB, c.Z); c.x = p[0]; c.y = p[1]; c.hw = .95 * c.s * p[2]; return c; },
    join: function (d) {                        /* a parcel of vapour reaching its height joins the cloud there, or starts one */
      var best = null, bd = 1e9, self = this; this.Cs.forEach(function (c) { var dx = Math.abs(c.x - d.x), dy = Math.abs(c.y - 10 - d.y); if (dx < c.hw * 1.2 + 30 && dy < 70 && dx + dy < bd) { bd = dx + dy; best = c; } });
      if (best) best.m += .17; else { var c = this.seen(this.cloud(d.x, d.y + 10, .17)); c.at = 1; }
    },
    paint: function (c) { this.SK.puffs(c, c.a * this.am.Cu); },          /* a cumulus, drawn by the sky (mkSky above) */
    /* put a cloud of one of the layer kinds somewhere in the part of its plane that the sky's window shows, seen at the column sx */
    place: function (o, sx) { o.Z = GENUS[o.k].h * this.FF / (this.GY * v(.3, .97)); o.X = (sx - this.XC) * o.Z / this.FF; },
    band: function (px, CL) { CL = CL || this.CL; return CL ? CL[cl((px / 16) | 0, 0, CL.length - 1)] : null; },
    seed: function (near) { for (var k = 0; k < 14; k++) { var px = near && R() < .65 ? near.x + (R() < .5 ? -1 : 1) * v(near.hw * .6 + 10, near.hw + 240) : v(14, W - 14), t = this.fit(px, KINDS[R() * 5 | 0]()); if (t) { this.A.push(t); return t; } } return null; },
    init: function () {
      this.UN = W > 760 ? (+host.getAttribute('data-bg-under') || 0) : 0; this.Hn = []; this.GY = H - 46 - this.UN; this.Fd = []; this.sc = cl(H / 520, .8, 1.7);
      this.A = []; this.L = []; this.M = []; this.ob = []; this.V = []; this.Cs = []; this.Y = 0; this.sn = new Float32Array(Math.ceil(W / 12) + 1); this.sky = W > 760;
      var self = this, hr = host.getBoundingClientRect(); this.FF = 1.5 * this.GY;   /* the eye's focal length (see mkSky) */
      [host.getAttribute('data-bg-avoid'), host.getAttribute('data-bg-avoid-near')].forEach(function (q) { if (q) document.querySelectorAll(q).forEach(function (e) { var r = e.getBoundingClientRect(); if (r.width && r.height) self.ob.push({ l: r.left - hr.left - 14, r: r.right - hr.left + 14, t: r.top - hr.top - 10, b: r.bottom - hr.top + 10 }); }); });
      var m = null; for (var q = 0; q < 80 && !m; q++) { var g = KINDS[0](); g.len = 64; g.maxd = 6; m = this.fit(q ? v(14, W - 14) : Math.max(46, W * .1), g); }
      if (m) { this.A.push(m); this.ripen(m); m.life = this.LIFE[0] * this.YEAR; }
      /* a few more grown trees of mixed ages, so the land is not bare when the page opens and they do not all die at once */
      for (var s = 1; s < this.START; s++) { var t2 = this.seed(m); if (t2) { this.ripen(t2); t2.age = v(0, .8) * t2.life; } }
      this.XC = W / 2; this.U = 0; this.U2 = 0; this.U3 = 0; this.CL = this.clouds(); this.Cs.forEach(function (c) { self.seen(c); });
      this.SK = mkSky(this.GY, this.XC, this.FF); this.am = {}; this.cb = null; this.cbY = -1; this.Gs = []; this.sun = null;
      /* the runs of open sky: the widest holds the sun (seen only through altostratus and cirrostratus), the next the thunder cloud */
      var runs = [], st = -1; for (var ci = 0; ci <= this.CL.length; ci++) { if (ci < this.CL.length && this.CL[ci]) { if (st < 0) st = ci; } else if (st >= 0) { runs.push([st, ci - 1]); st = -1; } }
      runs.sort(function (p, q) { return (q[1] - q[0]) - (p[1] - p[0]); });
      if (this.sky && runs.length) { var r0 = runs[0], r1 = runs[1] || runs[0], bs = this.CL[(r0[0] + r0[1]) >> 1]; this.sun = [(r0[0] + r0[1] + 1) * 8, bs.t + (bs.b - bs.t) * .45]; this.cbx = (r1[0] + r1[1] + 1) * 8; this.rc = runs.map(function (r) { return [r[0] * 16, Math.min(W, (r[1] + 1) * 16) - r[0] * 16]; });
        this.NG.forEach(function (q) { for (var n2 = 0; n2 < q[1]; n2++) { var o = self.SK.make(q[0]); self.place(o, v(-60, W + 60)); self.Gs.push(o); } }); } },
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
      this.U2 += (-this.U2 / 60 * dt + 2.2 * this.WIND * Math.sqrt(2 / 60 * dt) * (R() + R() + R() - 1.5) * 2); this.U3 += (-this.U3 / 60 * dt + 4 * this.WIND * Math.sqrt(2 / 60 * dt) * (R() + R() + R() - 1.5) * 2);
      /* how much of each kind is in the sky now: its window of the year (SEASON), approached smoothly */
      var SK = this.SK, am = this.am, SE = this.SEASON, kk, drew = !!this.sun, lay = function (k) { self.Gs.forEach(function (o) { if (o.k === k) SK.paint(o, am[k], self.Y); }); };
      for (kk in SE) { var w0 = SE[kk], tg = 0; for (var wi = 0; wi < w0.length; wi += 2) tg = Math.max(tg, sstep((ph - w0[wi]) / .04) * sstep((w0[wi + 1] - ph) / .04)); am[kk] = am[kk] === undefined ? tg : am[kk] + (tg - am[kk]) * Math.min(1, dt / 4); }
      if (drew) { SK.begin(this.rc);
        /* the layer clouds drift with the wind of their level (low, middle, high: higher winds are stronger, and each has a steady
           part); one that leaves the picture comes back in from the other side as a new cloud */
        var wl = [this.U + 3, this.U2 + 7, this.U3 + 14];
        this.Gs.forEach(function (o) { var FF = self.FF, f = FF / o.Z, e = o.ext * f, sx; o.X += wl[GENUS[o.k].lv] * dt; sx = self.XC + o.X * f;
          if (sx - e > W + 40) { SK.make(o.k, o); self.place(o, 0); o.X = (-40 - o.ext * FF / o.Z - self.XC) * o.Z / FF; } else if (sx + e < -40) { SK.make(o.k, o); self.place(o, 0); o.X = (W + 40 + o.ext * FF / o.Z - self.XC) * o.Z / FF; } });
        /* from the highest to the lowest, so the low ones hide the high ones */
        lay('Cs'); SK.wash(.25, .1 * am.Cs); SK.sun(this.sun[0], this.sun[1], 0, am.Cs); lay('Ci'); lay('Cc'); lay('As'); SK.wash(.36, .07 * am.As); SK.sun(this.sun[0], this.sun[1], am.As, 0); lay('Ac');
        /* the thunder cloud: in early summer, when the cumulus hold enough of the forest's water, one tower rises far away (22 km)
           through all the levels (over 9 % of a year), spreads its anvil, rains hard, and fades when autumn comes */
        var cb = this.cb, yr = Math.floor(this.Y / this.YEAR), wsum = 0; Cs.forEach(function (c) { wsum += c.m; });
        if (!cb && ph > .27 && ph < .34 && this.cbY !== yr && wsum > this.CB) { cb = this.cb = SK.make('Cb'); cb.Z = 22000; cb.X = (this.cbx - this.XC) * cb.Z / this.FF; cb.vg = 0; cb.fa = 1; this.cbY = yr; }
        if (cb) { cb.X += this.U * dt; cb.vg = Math.min(1, cb.vg + dt / (.09 * this.YEAR)); if (ph > .5 || ph < .25) cb.fa -= dt / (.05 * this.YEAR);
          if (cb.fa <= 0) this.cb = null; else { SK.paint(cb, cb.fa * Math.min(1, cb.vg * 4), this.Y);
            if (cb.vg > .8 && cb.fa >= 1 && R() < dt * 9) { var cx2 = this.XC + (cb.X + v(-1, 1) * cb.s) * this.FF / cb.Z, bb = this.band(cx2); if (bb) V.push({ x: cx2, y: v(bb.b - 40, bb.b + GY * .1), r: v(1.9, 2.4), q: 1 }); } } }
        lay('Sc'); }
      Cs.sort(function (p, q) { return q.Z - p.Z; });
      Cs.forEach(function (c) {
        c.X += self.U * dt; self.seen(c);
        c.s += (self.SIZE * Math.cbrt(Math.max(c.m, .01)) - c.s) * Math.min(1, dt / 5);
        var ok = 0; for (var k = -2; k <= 2; k++) { var bk = self.band(c.x + k * c.hw * .5); if (bk && c.y < bk.b + 20 && c.x + k * c.hw * .5 > 0 && c.x + k * c.hw * .5 < W) ok++; }
        c.at = ok / 5; c.a += ((ok === 5 ? 1 : 0) - c.a) * Math.min(1, dt / 2.5);   /* fully over open sky, or fading out */ c.m *= Math.exp(-dt / (c.at < .4 || am.Cu < .5 ? 8 : self.EVAP));   /* over text, or out of its season: it thins away */
        if (sea < 3) c.r += self.COND * dt;
        var rate = sea === 3 ? .25 * c.m : self.RAIN * c.m * Math.max(0, c.r - .6);
        if (R() < rate * dt && c.m > .3 && c.a > .3) { var u = v(-.6, .6), w = v(-.4, .4), pb = self.proj(c.X + u * c.s, self.HB, c.Z + w * c.s); c.m -= .15;
          if (sea === 3) V.push({ x: pb[0], y: pb[1], r: .5, q: 1, snow: 1 }); else { V.push({ x: pb[0], y: pb[1], r: v(1.3, 1.7), q: 1 }); c.r = Math.max(.55, c.r - .004); } }
        if (c.a > .01) self.paint(c);
      });
      this.Cs = Cs.filter(function (c) { return c.m > .05 && !(c.a < .01 && c.at === 0); });
      if (drew) { SK.wash(.6, .05 * am.Ns); lay('Ns'); SK.wash(.4, .06 * am.St); lay('St'); SK.end(this.msk);
        /* the sky goes behind everything already drawn (trees, rain, the ground) */
        SK.blit(x, this.TONE, true);
        /* the layers' own weather: long rain from nimbostratus, snow from it and from stratus once winter has come */
        var np = (12 * am.Ns + 5 * am.St) * dt * this.CL.length / 30, cold = ph > .76 || ph < .02;
        for (; np > 0; np -= 1) if (R() < np) { var gj = (R() * this.CL.length) | 0, bj = this.CL[gj]; if (bj) V.push(cold ? { x: gj * 16 + R() * 16, y: v(bj.t, bj.b), r: .5, q: 1, snow: 1 } : { x: gj * 16 + R() * 16, y: v((bj.t + bj.b) / 2, bj.b), r: v(2, 2.5), q: 1 }); } }
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
     up to the trees). Right: paper globes on threads hang from beams in a wind that blows down the margin with a street of
     vortices in it; the wind's lines are drawn, and each passing vortex swings the globes; this half is not computed here but
     played from data computed once on Kaggle (sceneData above, windDraw below). ---- */
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
    /* a beam across the margin, from which the paper globes hang (how many is decided when the stored data is known) */
    bar: function (y) { this.Bs.push({ y: y }); },
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
      /* right: paper globes on threads in a wind that carries a Kármán vortex street, played from the stored run
         (tools/sims/windpend.py, computed on Kaggle; docs/kaggle-sims.md). Nothing is computed here. The wind blows down the margin.
         Its lines (the paths the air follows at this instant) are stored as curves η(ξ − c t): they are drawn shifted down by c t,
         so the vortices are seen sliding down the page. The stored swing is that of a beam at the top; because the whole wind only
         slides, a beam ξ lower sees the same wind ξ / c later, so it plays the same frames with that delay: each vortex pushes
         the globes of every beam as it passes them. */
      var D = this.D; if (!D) { if (!this.asked) { this.asked = 1; sceneData('windpend', 'windpend.bin').then(function (d) { self.D = d; }, function (e) { self.err = String(e.message || e); }); } return; }
      x.save(); x.beginPath(); x.rect(g.r0 - 4, Math.max(0, top), this.rw + 8, Math.min(H, g.bot - sy) - Math.max(0, top)); x.clip();
      windDraw(D, this.t, (g.r0 + g.r1) / 2, top, this.rw, D.hdr.params.scale, this.Bs.map(function (B) { return B.y; }), fade, Math.max(0, top), Math.min(H, g.bot - sy));
      x.restore();
    }
  };
  /* ---- wind: the right rail's paper globes in the wind on their own, in a box (the scenes page, scenes.html). The same stored
     run (tools/sims/windpend.py, computed on Kaggle); nothing is computed here. Two beams, so the delay between them shows:
     the lower globes repeat the upper ones' swing ξ / c later, when the same vortex reaches them. ---- */
  S.wind = {
    K: [],     /* no numbers to change: the stored run is the motion of these globes in this wind, played at real time */
    init: function () { var self = this; this.t = 0; if (!this.asked) { this.asked = 1; sceneData('windpend', 'windpend.bin').then(function (d) { self.D = d; }, function (e) { self.err = String(e.message || e); }); } },
    draw: function (dt) {
      clear(); this.t += dt; var D = this.D; if (!D) return; var pr = D.hdr.params, sc = Math.min(H * .36 / pr.L, W / pr.WS);
      windDraw(D, this.t, W / 2, 0, W, sc, [22, 22 + H * .5], function () { return 1; }, 0, H);
    }
  };
  /* ---- atlas: the ten kinds of cloud side by side, each at its own height and labelled (the scenes page). The same builders and
     the same eye as the forest's sky (mkSky above): the high clouds far away and high in the picture, the middle ones below
     them, the low ones lowest and nearest, and the thunder cloud standing through all three levels. The layer kinds (stratus,
     altostratus, cirrostratus, nimbostratus) cover the whole sky in nature; here a piece of each is shown. ---- */
  S.atlas = {
    TONE: .8, SWAY: 1,
    K: [['TONE', 'strength of the drawing', '', .2, 1, .02], ['SWAY', 'how far the clouds drift to and fro', '×', 0, 4, .1]],
    /* where each kind stands: across the picture (0 to 1), how high its base is seen (share of the height above the horizon), and
       the half width it is shown at (px, at a picture 1100 px wide) */
    AT: [['Ci', .13, .80, 95], ['Cc', .37, .86, 70], ['Cs', .62, .80, 105], ['Ac', .22, .53, 95], ['As', .47, .56, 105], ['St', .075, .24, 80], ['Ns', .245, .26, 85], ['Sc', .50, .31, 175], ['Cu', .76, .21, 62], ['Cb', .92, .075, 0]],
    init: function () {
      var self = this, GY = this.GY = H - 20, F = this.F = 1.5 * GY, kx = Math.min(1, W / 1100); this.SK = mkSky(GY, W / 2, F); this.t = 0;
      this.O = this.AT.map(function (a) { var o = self.SK.make(a[0]), hb = GENUS[a[0]].h; o.Z = hb * F / (a[2] * GY); o.X0 = o.X = (a[1] * W - W / 2) * o.Z / F; o.fx = a[1]; o.ph = R() * 6;
        if (a[0] === 'Cu') { o.s = a[3] * kx * o.Z / F / o.ax; } else if (a[0] === 'Cb') { o.rain = 1; o.s = Math.min(1400, .13 * W * o.Z / F / 4.2); } else o.sz = a[3] * kx * o.Z / F / o.ext;
        if (a[0] === 'As' || a[0] === 'Cs') { o.sun = 1; o.halo = a[0] === 'Cs' ? Math.min(.404 * F, 70 * kx) : 0; }
        return o; });
      this.O.sort(function (p, q) { return q.Z - p.Z; });
    },
    draw: function (dt) {
      clear(); this.t += dt; var self = this, SK = this.SK, GY = this.GY, F = this.F, small = W < 720;
      x.strokeStyle = col(.3); x.lineWidth = 1; ln(0, GY, W, GY);
      SK.begin(); this.O.forEach(function (o) { o.X = o.X0 + self.SWAY * 14 * (o.Z / 1000) * Math.sin(self.t / 11 + o.ph); SK.paint(o, 1, self.t); }); SK.end(null); SK.blit(x, this.TONE, false);
      /* the names: abbreviation, genus and where it lives, under each cloud; the three levels at the left edge */
      x.font = (small ? 9 : 10.5) + 'px "IBM Plex Mono", ui-monospace, monospace'; x.textAlign = 'center'; x.textBaseline = 'top';
      this.O.forEach(function (o) { var G = GENUS[o.k], p = SK.proj(o.X, G.h, o.Z), ly = o.k === 'Cb' ? p[1] - GY * .86 : p[1] + (o.k === 'Cu' ? 14 : G.lv === 2 ? 30 : 34) * Math.min(1, W / 1100) + 6;
        x.fillStyle = col(.85); x.fillText(o.k + ' · ' + G.n, cl(p[0], 60, W - 60), ly); if (!small) { x.fillStyle = col(.5); x.fillText(G.r, cl(p[0], 60, W - 60), ly + 13); } });
      if (!small) { x.textAlign = 'left'; x.fillStyle = col(.4); [['HIGH · 5–13 km', .97], ['MIDDLE · 2–7 km', .64], ['LOW · below 2 km', .36]].forEach(function (q) { x.fillText(q[0], 8, GY * (1 - q[1])); }); }
      x.textAlign = 'left'; x.textBaseline = 'alphabetic';
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
  /* ---- spin: rotors in oil, each turning at its own rate; a rotating field wandering over them brings those it passes into step.
     Played from runs computed once on Kaggle (tools/sims/spinners.py; Fig. 17, section S4); nothing is computed here.
     The model: θ_i' = ω_i + K(r_i, t) sin(Ωt − θ_i) + κ Σ_nb sin(θ_j − θ_i), K = K₀ exp(−|r − s(t)|² / 2σ²) (Adler, Kuramoto).
     Stored: 12 runs, K₀ ∈ {0, 4, 10, 20} rad/s × κ ∈ {0, 1, 3} rad/s, a lattice of 72 × 9 rotors over 80 s at 15 frames a second
     (angles in steps of 2π/256) with the field's centre, its direction and the share of rotors locked near it. The band shows the
     middle of the lattice, 28 px per lattice spacing. Between two stored frames each rotor is turned the short way. The run is
     looped: over its last second the end is cross-faded into its start (the field's path closes; the rotors that slip do not).
     A rotor is drawn bright when its rate, read from the stored frames, is within 0.6 rad/s of the field's rate Ω. ---- */
  S.spin = {
    FIELD: 10, NEIGH: 1,
    K: [['FIELD', 'pull of the rotating field at its centre, K₀ (stored values)', 'rad/s', 0, 20, [0, 4, 10, 20]], ['NEIGH', 'pull between neighbours, κ (stored values)', 'rad/s', 0, 3, [0, 1, 3]]],
    init: function () { this.t = 0; this.nc = Math.min(72, Math.floor(W / 28)); this.nr = Math.min(9, Math.max(1, Math.floor(H / 29.5))); this.load(); },
    load: function () { var self = this, f = 'spin-K' + this.FIELD + '-k' + this.NEIGH + '.bin'; if (this.want === f) return; this.want = f;
      sceneData('spinners', f).then(function (d) { if (self.want === f) { self.D = d; self.A = new Uint8Array(d.raw, 0, d.hdr.frames * d.hdr.N); self.F = new Float32Array(d.raw.slice(d.hdr.frames * d.hdr.N)); } }, function (e) { self.err = String(e.message || e); }); },
    /* one moment τ (s) of the stored run: the rotors at alpha a */
    paint: function (tau, a) {
      var hd = this.D.hdr, N = hd.N, Nc = hd.N_c, fps = hd.fps, nf = hd.frames, u = tau * fps, f = Math.min(nf - 2, Math.floor(u)), e = u - f, A = this.A, Fd = this.F, TW = 2 * PI / 256,
        c0 = Math.floor((Nc - this.nc) / 2), r0 = Math.floor((hd.N_r - this.nr) / 2), ox = (W - (this.nc - 1) * 28) / 2, oy = (H - (this.nr - 1) * 29.5) / 2, Om = Fd[f * 4 + 2 + 4] - Fd[f * 4 + 2], i, j, k;
      var phi = Fd[f * 4 + 2] * (1 - e) + Fd[f * 4 + 6] * e, sx = Fd[f * 4] * (1 - e) + Fd[f * 4 + 4] * e, sy = Fd[f * 4 + 1] * (1 - e) + Fd[f * 4 + 5] * e, px = ox + (sx - c0) * 28, py = oy + (sy - r0) * 29.5;
      x.globalAlpha = a; x.strokeStyle = col(.12); x.lineWidth = 1; x.beginPath(); x.arc(px, py, 4 * 28, 0, 7); x.stroke(); x.lineWidth = 8; x.lineCap = 'round'; ln(px - 40 * Math.cos(phi), py - 40 * Math.sin(phi), px + 40 * Math.cos(phi), py + 40 * Math.sin(phi)); x.lineCap = 'butt';
      for (j = 0; j < this.nr; j++) for (i = 0; i < this.nc; i++) {
        var n = (r0 + j) * Nc + c0 + i, a0 = A[f * N + n] * TW, a1 = A[(f + 1) * N + n] * TW, d = a1 - a0; d -= 2 * PI * Math.round(d / (2 * PI));
        var th = a0 + d * e, lock = Math.abs(d - Om) < .6 / fps ? 1 : 0, al = .3 + .6 * lock, cx = ox + i * 28, cy = oy + j * 29.5;
        x.strokeStyle = col(al); x.lineWidth = 1.3; x.beginPath(); for (k = 0; k < 3; k++) { var an = th + k * 2.094; x.moveTo(cx, cy); x.lineTo(cx + 10 * Math.cos(an), cy + 10 * Math.sin(an)); } x.stroke(); dot(cx + 10 * Math.cos(th), cy + 10 * Math.sin(th), 2.4, Math.min(1, al + .2));
      }
      x.globalAlpha = 1;
    },
    draw: function (dt) {
      clear(); this.t += dt; this.load(); if (!this.D) return; var T = this.D.hdr.frames / this.D.hdr.fps, L = T - 1, tau = this.t % L;
      this.tau = tau;
      if (tau < 1) { this.paint(tau + L, 1 - tau); this.paint(tau, tau); } else this.paint(tau, 1);
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
