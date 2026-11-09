/* The Electron Beam, from Tip to Measurement · app.js
   The page's own script. It binds each simulation slot (.eb-sim[data-module]) to its physics module (EB.chNN, physics/chNN.js):
   a slider or menu per contract symbol (data-symbol), readouts (data-out), a canvas the module draws on. It computes nothing itself:
   module.compute(p) gives the numbers, module.draw(ctx, w, h, p, out) paints them. Also the contents list's "you are here" mark.
   window.EB.sims[id] = { p, out, set(symbol, value) } is how the browser checks drive a slider. */
(function () {
  'use strict';
  var EB = window.EB, core = EB.core;
  var CONTRACT = JSON.parse(document.getElementById('eb-contract').textContent);
  EB.contract = CONTRACT; EB.sims = {};

  function unitText(s, v) {
    var u = s.display_unit || s.unit, x = v * (s.display_scale || 1);
    return core.fmt(x, 3) + (u === '1' || u === '' ? '' : ' ' + u);
  }
  function fromSlider(s, t) {
    var lo = s.min, hi = s.max, v = s.scale === 'log' ? lo * Math.pow(hi / lo, t) : lo + t * (hi - lo);
    return s.type === 'integer' ? Math.round(v) : v;
  }
  function toSlider(s, v) {
    var lo = s.min, hi = s.max;
    return core.clamp(s.scale === 'log' ? Math.log(v / lo) / Math.log(hi / lo) : (v - lo) / (hi - lo), 0, 1);
  }

  function mount(el) {
    var id = el.getAttribute('data-module'), mod = EB[id];
    if (!mod) return;
    var p = {}, out = null, pending = false, err = el.querySelector('.eb-sim__err');
    mod.inputs.forEach(function (k) { p[k] = CONTRACT.symbols[k].default; });
    var cv = el.querySelector('canvas'), ctx = cv.getContext('2d');

    function show() {
      pending = false;
      try {
        out = mod.compute(p); err.hidden = true;
        EB.sims[id].out = out;
        el.querySelectorAll('[data-out]').forEach(function (d) {
          var k = d.getAttribute('data-out'), v = k in out ? out[k] : p[k];
          d.textContent = unitText(CONTRACT.symbols[k], v);
        });
        el.querySelectorAll('[data-for]').forEach(function (o) { var k = o.getAttribute('data-for'); o.textContent = unitText(CONTRACT.symbols[k], p[k]); });
        if (mod.draw) {
          var dpr = window.devicePixelRatio || 1, w = cv.clientWidth, h = cv.clientHeight;
          if (cv.width !== Math.round(w * dpr) || cv.height !== Math.round(h * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); }
          ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
          mod.draw(ctx, w, h, p, out);
        }
      } catch (e) { err.textContent = 'This simulation stopped: ' + (e && e.message || e); err.hidden = false; }
    }
    function later() { if (!pending) { pending = true; requestAnimationFrame(show); } }

    EB.sims[id] = { p: p, out: null, set: function (k, v) { p[k] = v; sync(k); later(); }, redraw: show };
    function sync(k) {
      var inp = el.querySelector('[data-symbol="' + k + '"]'); if (!inp) return;
      if (inp.tagName === 'SELECT') { inp.value = p[k]; return; }
      var t = toSlider(CONTRACT.symbols[k], p[k]); inp.value = Math.round(t * 1000); inp.style.setProperty('--p', (t * 100) + '%');
    }
    el.querySelectorAll('[data-symbol]').forEach(function (inp) {
      var k = inp.getAttribute('data-symbol'), s = CONTRACT.symbols[k];
      sync(k);
      inp.addEventListener('input', function () {
        if (inp.tagName === 'SELECT') p[k] = inp.value;
        else { var t = inp.value / 1000; p[k] = fromSlider(s, t); inp.style.setProperty('--p', (t * 100) + '%'); }
        later();
      });
    });
    if (window.ResizeObserver) new ResizeObserver(later).observe(cv);
    show();
  }

  function toc() {
    var links = Array.prototype.slice.call(document.querySelectorAll('.paper__toc a[data-ch]'));
    if (!window.IntersectionObserver || !links.length) return;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (a) { var on = a.getAttribute('data-ch') === e.target.id; a.classList.toggle('is-here', on); a.parentNode.classList.toggle('is-open', on); });
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    document.querySelectorAll('.chapter').forEach(function (c) { io.observe(c); });
  }

  document.querySelectorAll('.eb-sim[data-module]').forEach(mount);
  toc();
})();
