// Figure collision check of the built page, in Chromium (the preinstalled Playwright).
//
//   node portfolios-src/electron-beam/checks/check_figures.cjs                    every figure and simulation of the page
//   node ... --chapters ch00,ch01,ch02                                            only those chapters (by the enclosing section.chapter id)
//   node ... --only fig-scales,sim-ch00,eb-tip                                    only figures / simulations / canvases with these ids
//   node ... --widths 360,1440   --quick (default state only, no slider sweep)   --shots DIR (element screenshots, default state)
//   node ... --url http://127.0.0.1:8765/portfolios/electron-beam/index.html     a page already served (default: serves public/ itself)
//   node ... --json FILE                                                         every finding as JSON
//
// What it tests, at widths 360, 390, 1024 and 1440 px:
//   SVG figures (every visible <svg> inside a figure.pfig): each <text> is cut into its lines (runs of characters on one baseline,
//   from getExtentOfChar / getStartPositionOfChar) and each line gets an ink box, baseline - 0.74 em to baseline + 0.18 em, mapped
//   to the screen with getScreenCTM (so rotated labels are rotated boxes). Every path, line, polyline, polygon, rect, circle and
//   ellipse is sampled every 1.5 screen px along getTotalLength()/getPointAtLength(), clipped by any clip-path rectangle on it or
//   an ancestor. Reported: text on text, a stroke or shape outline through a text box (widened by half the stroke width), a text
//   box outside the viewBox, and text smaller than the minimum size (10.5 CSS px below 600 px width, 9.5 px above).
//   Canvas simulations (every canvas inside .eb-sim, .ebsim or [data-figcheck-sim]): before any page script runs, the
//   CanvasRenderingContext2D methods are wrapped. fillText/strokeText record the ink box from measureText (actualBoundingBox*,
//   which already holds textAlign and textBaseline) under the current transform; moveTo/lineTo/bezierCurveTo/quadraticCurveTo/
//   arc/arcTo/ellipse/rect/closePath record the path under the current transform, stroke() and fill() commit it, strokeRect and
//   fillRect commit rectangles. A clearRect or fillRect over the whole canvas, or a change of its width or height, starts a new
//   picture; what is tested is the last picture. Same four tests, in the canvas's CSS px. Each simulation is tested at its default,
//   at the minimum and the maximum of every range input, at every option of every select, with every checkbox flipped and after
//   each preset button (button[data-eb-preset], button[data-preset], [data-figcheck-click]), each from the default state.
//
// Allow-list (things meant to touch):
//   SVG:    data-nocollide on an element (or any ancestor) takes it out of every test: put it on grid lines and the plot frame that
//           tick labels sit on, and on a leader line that ends at its label. On a <text> it excludes that text entirely.
//   Canvas: set ctx.__nocollide = true while drawing the grid, the frame or a leader, and false afterwards; strokes, fills and texts
//           drawn while it is true are not tested. (It is a plain property, not part of save()/restore().)
//   Background: an SVG rect or a canvas fillRect covering at least 98 % of the figure is the ground, never tested.
//
// Exit status 0 when nothing is found, 1 otherwise. Tolerance: overlaps of 0.5 CSS px or less are not counted.
'use strict';
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..', '..', '..');
const arg = n => (process.argv.includes(n) ? process.argv[process.argv.indexOf(n) + 1] : null);
const flag = n => process.argv.includes(n);
const WIDTHS = (arg('--widths') || '360,390,1024,1440').split(',').map(Number);
const ONLY = arg('--only') ? arg('--only').split(',') : null;
const CHAPTERS = arg('--chapters') ? arg('--chapters').split(',') : null;
const SHOTS = arg('--shots') ? path.resolve(arg('--shots')) : null;
const SETTLE = Number(arg('--settle') || 450);
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.json': 'application/json', '.png': 'image/png', '.webp': 'image/webp' };

function serve() {
  const pub = path.join(ROOT, 'public');
  return new Promise(res => {
    const s = http.createServer((q, r) => {
      let f = path.join(pub, decodeURIComponent(q.url.split('?')[0]));
      if (!f.startsWith(pub)) { r.writeHead(403); return r.end(); }
      if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
      if (!fs.existsSync(f)) { r.writeHead(404); return r.end('not found'); }
      r.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' });
      fs.createReadStream(f).pipe(r);
    }).listen(0, '127.0.0.1', () => res(s));
  });
}

// ---------------------------------------------------------------------------------------------- runs in the page before its scripts
function instrument() {
  const P = CanvasRenderingContext2D.prototype;
  const rec = cv => cv.__fig || (cv.__fig = { texts: [], strokes: [], n: 0 });
  const fresh = cv => { cv.__fig = { texts: [], strokes: [], n: ((cv.__fig && cv.__fig.n) || 0) + 1 }; };
  const T = (g, x, y) => { const m = g.getTransform(); return [m.a * x + m.c * y + m.e, m.b * x + m.d * y + m.f]; };
  const scl = g => { const m = g.getTransform(); return Math.sqrt(Math.abs(m.a * m.d - m.b * m.c)); };
  const path = g => g.__path || (g.__path = { subs: [], cur: null, last: null });
  const add = (g, x, y) => { const p = path(g), q = T(g, x, y); if (!p.cur) { p.cur = [q]; p.subs.push(p.cur); } else p.cur.push(q); p.last = [x, y]; };
  const wrap = (name, fn) => { const o = P[name]; P[name] = function () { fn.apply(this, arguments); return o.apply(this, arguments); }; };
  const wrapAfter = (name, fn) => { const o = P[name]; P[name] = function () { const r = o.apply(this, arguments); fn.apply(this, arguments); return r; }; };
  const desc = g => (typeof g.strokeStyle === 'string' ? g.strokeStyle : 'pattern');
  wrap('beginPath', function () { this.__path = { subs: [], cur: null, last: null }; });
  wrap('moveTo', function (x, y) { const p = path(this); p.cur = null; add(this, x, y); });
  wrap('lineTo', function (x, y) { add(this, x, y); });
  wrap('closePath', function () { const p = path(this); if (p.cur && p.cur.length) { p.cur.push(p.cur[0].slice()); } });
  wrap('bezierCurveTo', function (a, b, c, d, x, y) {
    const p = path(this), s = p.last || [a, b];
    for (let i = 1; i <= 24; i++) { const t = i / 24, u = 1 - t; add(this, u * u * u * s[0] + 3 * u * u * t * a + 3 * u * t * t * c + t * t * t * x, u * u * u * s[1] + 3 * u * u * t * b + 3 * u * t * t * d + t * t * t * y); }
  });
  wrap('quadraticCurveTo', function (a, b, x, y) {
    const p = path(this), s = p.last || [a, b];
    for (let i = 1; i <= 16; i++) { const t = i / 16, u = 1 - t; add(this, u * u * s[0] + 2 * u * t * a + t * t * x, u * u * s[1] + 2 * u * t * b + t * t * y); }
  });
  const arcPts = (g, cx, cy, rx, ry, rot, a0, a1, ccw) => {
    let d = a1 - a0;
    if (!ccw && d < 0) d = d % (2 * Math.PI) + 2 * Math.PI; if (ccw && d > 0) d = d % (2 * Math.PI) - 2 * Math.PI;
    if (Math.abs(a1 - a0) >= 2 * Math.PI) d = ccw ? -2 * Math.PI : 2 * Math.PI;
    const n = Math.max(8, Math.ceil(Math.abs(d) * Math.max(rx, ry) * scl(g) / 2)), cr = Math.cos(rot), sr = Math.sin(rot);
    for (let i = 0; i <= Math.min(n, 400); i++) { const a = a0 + d * i / Math.min(n, 400), ex = rx * Math.cos(a), ey = ry * Math.sin(a); add(g, cx + ex * cr - ey * sr, cy + ex * sr + ey * cr); }
  };
  wrap('arc', function (x, y, r, a0, a1, ccw) { arcPts(this, x, y, r, r, 0, a0, a1, !!ccw); });
  wrap('ellipse', function (x, y, rx, ry, rot, a0, a1, ccw) { arcPts(this, x, y, rx, ry, rot, a0, a1, !!ccw); });
  wrap('arcTo', function (x1, y1) { add(this, x1, y1); });
  wrap('rect', function (x, y, w, h) { const p = path(this); p.cur = null; add(this, x, y); add(this, x + w, y); add(this, x + w, y + h); add(this, x, y + h); add(this, x, y); p.cur = null; });
  const full = (g, x, y, w, h) => { const a = T(g, x, y), b = T(g, x + w, y + h), cv = g.canvas; return Math.min(a[0], b[0]) <= 1 && Math.min(a[1], b[1]) <= 1 && Math.max(a[0], b[0]) >= cv.width - 1 && Math.max(a[1], b[1]) >= cv.height - 1; };
  const commit = (g, subs, kind, hw) => {
    if (!subs.length) return; const r = rec(g.canvas);
    r.strokes.push({ subs: subs.map(s => s.map(q => q.slice())), kind, hw, nocollide: !!g.__nocollide, desc: kind + ' ' + (kind === 'fill' ? (typeof g.fillStyle === 'string' ? g.fillStyle : 'pattern') : desc(g)) + (kind === 'fill' ? '' : ' lw ' + g.lineWidth) });
  };
  wrap('stroke', function (p2) { if (p2) return; commit(this, path(this).subs, 'stroke', this.lineWidth * scl(this) / 2); });
  wrap('fill', function (p2) { if (p2 && typeof p2 !== 'string') return; commit(this, path(this).subs, 'fill', 0); });
  const rectSub = (g, x, y, w, h) => [[T(g, x, y), T(g, x + w, y), T(g, x + w, y + h), T(g, x, y + h), T(g, x, y)]];
  wrap('strokeRect', function (x, y, w, h) { commit(this, rectSub(this, x, y, w, h), 'stroke', this.lineWidth * scl(this) / 2); });
  wrap('fillRect', function (x, y, w, h) { if (full(this, x, y, w, h)) fresh(this.canvas); else commit(this, rectSub(this, x, y, w, h), 'fill', 0); });
  wrap('clearRect', function (x, y, w, h) { if (full(this, x, y, w, h)) fresh(this.canvas); });
  const text = function (s, x, y) {
    const m = this.measureText(s), l = m.actualBoundingBoxLeft, r = m.actualBoundingBoxRight, a = m.actualBoundingBoxAscent, d = m.actualBoundingBoxDescent;
    if (!(r + l > 0)) return;
    const fs = parseFloat((/(\d+(?:\.\d+)?)px/.exec(this.font) || [0, 10])[1]) * scl(this);
    rec(this.canvas).texts.push({ s: String(s), quad: [T(this, x - l, y - a), T(this, x + r, y - a), T(this, x + r, y + d), T(this, x - l, y + d)], fs, nocollide: !!this.__nocollide });
  };
  wrap('fillText', text); wrap('strokeText', text);
  for (const k of ['width', 'height']) {
    const d = Object.getOwnPropertyDescriptor(HTMLCanvasElement.prototype, k);
    Object.defineProperty(HTMLCanvasElement.prototype, k, { get: d.get, set: function (v) { fresh(this); d.set.call(this, v); }, configurable: true });
  }
}

// ---------------------------------------------------------------------------------------------- geometry, shared by both kinds (page)
function geometryLib() {
  // a text box is a quad [p0 p1 p2 p3] (p0->p1 along the baseline, p1->p2 down); tests in its own frame
  const frame = q => {
    const ux = q[1][0] - q[0][0], uy = q[1][1] - q[0][1], L = Math.hypot(ux, uy) || 1e-9, vx = q[3][0] - q[0][0], vy = q[3][1] - q[0][1], H = Math.hypot(vx, vy) || 1e-9;
    return { o: q[0], u: [ux / L, uy / L], v: [vx / H, vy / H], L, H };
  };
  const inside = (f, p, m) => { const dx = p[0] - f.o[0], dy = p[1] - f.o[1], a = dx * f.u[0] + dy * f.u[1], b = dx * f.v[0] + dy * f.v[1]; return a > -m && a < f.L + m && b > -m && b < f.H + m; };
  const axes = q => [[q[1][0] - q[0][0], q[1][1] - q[0][1]], [q[3][0] - q[0][0], q[3][1] - q[0][1]]].map(a => { const l = Math.hypot(a[0], a[1]) || 1; return [a[0] / l, a[1] / l]; });
  const overlap = (A, B, tol) => {      // separating axis test; true when the quads overlap by more than tol on every axis
    for (const ax of [...axes(A), ...axes(B)]) {
      const pa = A.map(p => p[0] * ax[0] + p[1] * ax[1]), pb = B.map(p => p[0] * ax[0] + p[1] * ax[1]);
      if (Math.min(Math.max(...pa), Math.max(...pb)) - Math.max(Math.min(...pa), Math.min(...pb)) <= tol) return false;
    }
    return true;
  };
  const densify = (subs, step) => {
    const out = [];
    for (const s of subs) for (let i = 0; i < s.length; i++) {
      out.push(s[i]);
      if (i + 1 < s.length) { const d = Math.hypot(s[i + 1][0] - s[i][0], s[i + 1][1] - s[i][1]), n = Math.min(400, Math.floor(d / step)); for (let k = 1; k < n; k++) out.push([s[i][0] + (s[i + 1][0] - s[i][0]) * k / n, s[i][1] + (s[i + 1][1] - s[i][1]) * k / n]); }
    }
    return out;
  };
  // texts: [{s, quad, fs (CSS px), group}], strokes: [{pts, hw, desc}], box: [x0, y0, x1, y1]; all CSS px
  function analyse(texts, strokes, box, minFont, tol) {
    const out = [];
    texts.forEach(t => { t.f = frame(t.quad); });
    for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i], b = texts[j];
      if (a.group !== undefined && a.group === b.group) continue;
      if (overlap(a.quad, b.quad, tol)) out.push({ type: 'text-text', a: a.s, b: b.s });
    }
    for (const t of texts) for (const s of strokes) {
      const m = Math.max(0, s.hw - tol);
      if (s.pts.some(p => inside(t.f, p, m))) out.push({ type: 'text-line', a: t.s, b: s.desc });
    }
    for (const t of texts) {
      const out1 = t.quad.some(p => p[0] < box[0] - tol || p[1] < box[1] - tol || p[0] > box[2] + tol || p[1] > box[3] + tol);
      if (out1) out.push({ type: 'text-edge', a: t.s, b: 'edge ' + box.map(v => Math.round(v)).join(',') + ' text ' + t.quad.map(p => p.map(v => Math.round(v)).join(',')).join(' ') });
      if (t.fs < minFont) out.push({ type: 'text-small', a: t.s, b: t.fs.toFixed(1) + ' px < ' + minFont });
    }
    // one text with one line is one finding
    const seen = new Set();
    return out.filter(o => { const k = o.type + '|' + o.a + '|' + o.b; if (seen.has(k)) return false; seen.add(k); return true; });
  }
  return { analyse, densify };
}

// ---------------------------------------------------------------------------------------------- SVG figures (page)
function svgFigures(opts) {
  const G = eval('(' + opts.lib + ')')();
  const res = [];
  const noc = el => !!el.closest('[data-nocollide]');
  const chap = el => { const c = el.closest('section.chapter'); return c ? c.id : ''; };
  for (const fig of document.querySelectorAll('figure.pfig')) {
    if (opts.chapters && !opts.chapters.includes(chap(fig))) continue;
    if (opts.only && !opts.only.includes(fig.id)) continue;
    const svgs = [...fig.querySelectorAll('svg')].filter(s => !s.parentElement.closest('svg') && s.getBoundingClientRect().width > 0);
    svgs.forEach((svg, si) => {
      const vb = svg.viewBox.baseVal, M = svg.getScreenCTM(), sc = Math.sqrt(Math.abs(M.a * M.d - M.b * M.c));
      const P = (m, x, y) => [m.a * x + m.c * y + m.e, m.b * x + m.d * y + m.f];
      const corners = [P(M, vb.x, vb.y), P(M, vb.x + vb.width, vb.y + vb.height)];
      const box = [Math.min(corners[0][0], corners[1][0]), Math.min(corners[0][1], corners[1][1]), Math.max(corners[0][0], corners[1][0]), Math.max(corners[0][1], corners[1][1])];
      const texts = [];
      [...svg.querySelectorAll('text')].forEach((t, ti) => {
        if (noc(t) || t.closest('defs') || t.getBoundingClientRect().width === 0) return;
        const n = t.getNumberOfChars(); if (!n) return;
        const m = t.getScreenCTM(), fs0 = parseFloat(getComputedStyle(t).fontSize);
        const ch = [];
        for (let i = 0; i < n; i++) { const e = t.getExtentOfChar(i), s = t.getStartPositionOfChar(i); ch.push({ x0: e.x, x1: e.x + e.width, y: s.y, h: e.height }); }
        const k = ch.map(c => c.h / fs0).sort((a, b) => a - b)[Math.floor(n / 2)] || 1.3;
        const runs = []; let cur = null;
        for (const c of ch) {
          if (!cur || Math.abs(c.y - cur.y) > 0.5 || c.x0 < cur.x1 - 0.5 - 0.6 * fs0 || c.x0 > cur.x1 + 1.2 * fs0) { cur = { x0: c.x0, x1: c.x1, y: c.y, top: c.y, bot: c.y }; runs.push(cur); }
          const fs = c.h / k; cur.x0 = Math.min(cur.x0, c.x0); cur.x1 = Math.max(cur.x1, c.x1); cur.top = Math.min(cur.top, c.y - 0.74 * fs); cur.bot = Math.max(cur.bot, c.y + 0.18 * fs);
        }
        const label = (t.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 40);
        runs.forEach(r => texts.push({ s: label, group: 'svgtext' + ti, quad: [P(m, r.x0, r.top), P(m, r.x1, r.top), P(m, r.x1, r.bot), P(m, r.x0, r.bot)], fs: fs0 * Math.sqrt(Math.abs(m.a * m.d - m.b * m.c)) }));
      });
      const strokes = [];
      const clipRects = el => {      // clip-path rectangles on the element and its ancestors, each with the matrix to its user space
        const out = [];
        for (let a = el; a && a !== svg.parentElement; a = a.parentElement) {
          const cp = a.getAttribute && a.getAttribute('clip-path'); if (!cp) continue;
          const id = (/url\(#([^)]+)\)/.exec(cp) || [])[1], c = id && svg.ownerDocument.getElementById(id); if (!c) continue;
          const r = c.querySelector('rect'); if (!r) continue;
          out.push({ inv: a.getScreenCTM().inverse(), x: r.x.baseVal.value, y: r.y.baseVal.value, w: r.width.baseVal.value, h: r.height.baseVal.value });
        }
        return out;
      };
      for (const el of svg.querySelectorAll('path, line, polyline, polygon, rect, circle, ellipse')) {
        if (noc(el) || el.closest('defs, clipPath, marker, mask, pattern') || el.getBoundingClientRect().width + el.getBoundingClientRect().height === 0) continue;
        const cs = getComputedStyle(el);
        if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) continue;
        const stroked = cs.stroke !== 'none' && +cs.strokeOpacity > 0 && parseFloat(cs.strokeWidth) > 0, filled = cs.fill !== 'none' && +cs.fillOpacity > 0;
        if (!stroked && !filled) continue;
        if (el.tagName === 'rect') { const b = el.getBBox(); if (b.width * b.height >= 0.98 * vb.width * vb.height) continue; }
        const m = el.getScreenCTM(), esc = Math.sqrt(Math.abs(m.a * m.d - m.b * m.c)), L = el.getTotalLength();
        const n = Math.min(4000, Math.max(2, Math.ceil(L * esc / 1.5))), clips = clipRects(el), pts = [];
        for (let i = 0; i <= n; i++) {
          const q = el.getPointAtLength(L * i / n), p = P(m, q.x, q.y);
          if (clips.every(c => { const u = P(c.inv, p[0], p[1]); return u[0] >= c.x - 0.5 && u[0] <= c.x + c.w + 0.5 && u[1] >= c.y - 0.5 && u[1] <= c.y + c.h + 0.5; })) pts.push(p);
        }
        if (!pts.length) continue;
        const a = el.getAttribute.bind(el), what = el.tagName + (el.id ? '#' + el.id : '') + (a('class') ? '.' + a('class') : '') + ' ' + (stroked ? 'stroke ' + cs.stroke : 'fill ' + cs.fill) +
          (el.tagName === 'line' ? ' (' + ['x1', 'y1', 'x2', 'y2'].map(a).join(',') + ')' : el.tagName === 'path' ? ' d=' + (a('d') || '').slice(0, 30) : el.tagName === 'circle' ? ' (' + a('cx') + ',' + a('cy') + ')' : el.tagName === 'rect' ? ' (' + ['x', 'y', 'width', 'height'].map(a).join(',') + ')' : '');
        strokes.push({ pts, hw: stroked ? parseFloat(cs.strokeWidth) * esc / 2 : 0, desc: what });
      }
      const found = G.analyse(texts, strokes, box, opts.minFont, 0.5);
      res.push({ id: fig.id + (svgs.length > 1 ? '[' + si + ']' : ''), n_text: texts.length, n_lines: strokes.length, found });
    });
  }
  return res;
}

// ---------------------------------------------------------------------------------------------- canvases (page)
function canvasReport(opts) {
  const G = eval('(' + opts.lib + ')')();
  const res = [];
  for (const root of document.querySelectorAll(opts.rootSel)) {
    const cvs = [...root.querySelectorAll('canvas')];
    cvs.forEach((cv, i) => {
      const id = cv.id || root.id + (cvs.length > 1 ? '#' + i : '');
      if (opts.only && !opts.only.includes(id) && !opts.only.includes(root.id)) return;
      const r = cv.__fig, s = cv.width ? cv.clientWidth / cv.width : 1;
      if (!r || !cv.clientWidth) { res.push({ id, n_text: 0, n_lines: 0, found: [{ type: 'nothing-drawn', a: '', b: '' }] }); return; }
      const texts = r.texts.filter(t => !t.nocollide).map(t => ({ s: t.s, fs: t.fs * s, quad: t.quad.map(p => [p[0] * s, p[1] * s]) }));
      const strokes = r.strokes.filter(t => !t.nocollide).map(t => ({ hw: t.hw * s, desc: t.desc, pts: G.densify(t.subs.map(sb => sb.map(p => [p[0] * s, p[1] * s])), 1.5) }));
      res.push({ id, n_text: texts.length, n_lines: strokes.length, found: G.analyse(texts, strokes, [0, 0, cv.clientWidth, cv.clientHeight], opts.minFont, 0.5) });
    });
  }
  return res;
}

// ---------------------------------------------------------------------------------------------- driver
(async () => {
  let srv = null, url = arg('--url');
  if (!url) { srv = await serve(); url = 'http://127.0.0.1:' + srv.address().port + '/portfolios/electron-beam/index.html'; }
  if (SHOTS) fs.mkdirSync(SHOTS, { recursive: true });
  const browser = await chromium.launch();
  const lib = geometryLib.toString();
  const all = [];
  const ROOTSEL = '.eb-sim[data-module], .ebsim, [data-figcheck-sim]';
  for (const w of WIDTHS) {
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 2, bypassCSP: true });
    await ctx.addInitScript(instrument);
    const pg = await ctx.newPage();
    pg.on('pageerror', e => console.log('pageerror at ' + w + ': ' + e.message));
    await pg.goto(url, { waitUntil: 'networkidle' });
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(300);
    const minFont = w < 600 ? 10.5 : 9.5;
    // SVG figures
    const figs = await pg.evaluate(svgFigures, { lib, only: ONLY, chapters: CHAPTERS, minFont });
    figs.forEach(f => all.push({ ...f, w, state: 'static' }));
    if (SHOTS) for (const f of figs) { const id = f.id.replace(/\[\d+\]$/, ''); const el = pg.locator('#' + id); if (await el.count()) { await el.scrollIntoViewIfNeeded(); await pg.waitForTimeout(120); await el.screenshot({ path: path.join(SHOTS, `${id}-${w}.png`) }); } }
    // simulations
    const roots = await pg.evaluate(({ sel, chapters }) => [...document.querySelectorAll(sel)].filter(r => { const c = r.closest('section.chapter'); return !chapters || (c && chapters.includes(c.id)); }).map((r, i) => { if (!r.id) r.id = 'figcheck-root-' + i; return r.id; }), { sel: ROOTSEL, chapters: CHAPTERS });
    for (const rid of roots) {
      const ids = await pg.evaluate(rid => [rid, ...[...document.getElementById(rid).querySelectorAll('canvas')].map(c => c.id)], rid);
      if (ONLY && !ids.some(x => ONLY.includes(x))) continue;
      const root = pg.locator('#' + rid);
      await root.scrollIntoViewIfNeeded();
      await pg.waitForTimeout(SETTLE);
      const snap = async state => {
        const rep = await pg.evaluate(canvasReport, { lib, only: ONLY, minFont, rootSel: '#' + rid });
        rep.forEach(r => all.push({ ...r, w, state }));
      };
      await snap('default');
      if (SHOTS) await root.screenshot({ path: path.join(SHOTS, `${rid}-${w}.png`) });
      if (flag('--quick')) continue;
      // every control: remember the default, try its extremes, put it back
      const ctls = await pg.evaluate(rid => {
        const r = document.getElementById(rid), out = [];
        r.querySelectorAll('input[type=range]').forEach((e, i) => out.push({ kind: 'range', i, name: e.dataset.symbol || e.id || 'range' + i, v: e.value, min: e.min || '0', max: e.max || '100' }));
        r.querySelectorAll('select').forEach((e, i) => out.push({ kind: 'select', i, name: e.dataset.symbol || e.id || 'select' + i, v: e.value, opts: [...e.options].map(o => o.value) }));
        r.querySelectorAll('input[type=checkbox]').forEach((e, i) => out.push({ kind: 'check', i, name: e.id || 'check' + i, v: e.checked }));
        r.querySelectorAll('button[data-eb-preset], button[data-preset], [data-figcheck-click]').forEach((e, i) => out.push({ kind: 'click', i, name: (e.dataset.ebPreset || e.dataset.preset || e.textContent.trim()).slice(0, 30) }));
        return out;
      }, rid);
      const setCtl = (c, v) => pg.evaluate(({ rid, c, v }) => {
        const r = document.getElementById(rid);
        if (c.kind === 'range') { const e = r.querySelectorAll('input[type=range]')[c.i]; e.value = v; e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); }
        if (c.kind === 'select') { const e = r.querySelectorAll('select')[c.i]; e.value = v; e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); }
        if (c.kind === 'check') { const e = r.querySelectorAll('input[type=checkbox]')[c.i]; if (e.checked !== v) e.click(); }
        if (c.kind === 'click') r.querySelectorAll('button[data-eb-preset], button[data-preset], [data-figcheck-click]')[c.i].click();
      }, { rid, c, v });
      const presets = ctls.filter(c => c.kind === 'click');
      for (const c of ctls) {
        const tries = c.kind === 'range' ? [['min', c.min], ['max', c.max]] : c.kind === 'select' ? c.opts.filter(o => o !== c.v).map(o => [o, o]) : c.kind === 'check' ? [[String(!c.v), !c.v]] : [['click', null]];
        for (const [lab, v] of tries) {
          await setCtl(c, v); await pg.waitForTimeout(SETTLE);
          await snap(c.name + '=' + lab);
        }
        if (c.kind === 'click') continue;
        await setCtl(c, c.v); await pg.waitForTimeout(c.kind === 'range' ? 30 : SETTLE);
      }
      // back to the first preset (the default of a chapter-own panel) so that later roots start clean
      if (presets.length) { await setCtl(presets[0], null); await pg.waitForTimeout(SETTLE); }
    }
    await ctx.close();
  }
  await browser.close(); if (srv) srv.close();
  // report
  let n = 0; const per = {};
  for (const r of all) {
    per[r.id] = per[r.id] || { states: 0, found: 0, items: 0 };
    per[r.id].states++; per[r.id].items = Math.max(per[r.id].items, r.n_text);
    for (const f of r.found) { n++; per[r.id].found++; console.log(`${r.id}  w=${r.w}  ${r.state}  ${f.type}: "${f.a}"  x  ${f.b}`); }
  }
  console.log('\nper figure (snapshots, findings):');
  for (const [id, v] of Object.entries(per)) console.log(`  ${(v.found ? 'FAIL ' : 'ok   ') + id.padEnd(22)} ${String(v.states).padStart(4)} snapshots  ${String(v.found).padStart(4)} findings`);
  if (arg('--json')) fs.writeFileSync(arg('--json'), JSON.stringify(all, null, 1));
  console.log('FIGURE CHECK ' + (n ? 'FAIL: ' + n + ' findings' : 'PASS'));
  process.exit(n ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
