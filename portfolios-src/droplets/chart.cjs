/* House-style SVG line charts: white plate, clipped plot, IBM Plex Mono ticks. Used at build time by tools/figs.cjs and inlined
   into the page (between CHART-BEGIN and CHART-END) for the live charts. No DOM access: returns SVG markup as a string. */
/*CHART-BEGIN*/
var CHART = (function () {
  'use strict';
  var COL = ['#7d1d2f', '#33627f', '#3c6a46', '#c9783f', '#6f665e', '#9a5b8f', '#23160f'];
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function niceTicks(lo, hi, n) {
    var span = hi - lo, step = Math.pow(10, Math.floor(Math.log10(span / n))), err = span / n / step;
    if (err >= 7.5) step *= 10; else if (err >= 3.5) step *= 5; else if (err >= 1.5) step *= 2;
    var t = [], v = Math.ceil(lo / step - 1e-9) * step;
    for (; v <= hi + step * 1e-9; v += step) t.push(+v.toPrecision(12));
    return t;
  }
  function logTicks(lo, hi) {
    var t = [], e, decades = Math.log10(hi / lo) > 4;     // wide ranges: powers of ten only
    for (e = Math.floor(Math.log10(lo)); e <= Math.ceil(Math.log10(hi)); e++) {
      (decades ? [1] : [1, 2, 5]).forEach(function (m) { var v = m * Math.pow(10, e); if (v >= lo * 0.999 && v <= hi * 1.001) t.push(v); });
    }
    return t;
  }
  function fmt(v) {
    if (v === 0) return '0';
    var a = Math.abs(v);
    if (a >= 1e4 || a < 1e-3) { var e = Math.floor(Math.log10(a)), m = v / Math.pow(10, e); return (Math.abs(m - 1) < 1e-9 ? '' : +m.toPrecision(2) + '×') + '10' + sup(e); }
    return String(+v.toPrecision(4));
  }
  function sup(e) { var d = { '-': '⁻', '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹' }; return String(e).split('').map(function (c) { return d[c]; }).join(''); }
  // o: { w, h, xlabel, ylabel, xlog, ylog, xmin, xmax, ymin, ymax, series: [{x, y, label, color, dash, width, dots}], legend, title,
  //      vlines: [{x, label}], hlines: [{y, label}], id }
  function line(o) {
    var W = o.w || 560, H = o.h || 320, L = 62, R = 14, T = 16, B = 46;
    var pw = W - L - R, ph = H - T - B, s = o.series || [];
    // legend below the plot (the default): it never covers a curve. 'right', 'bottom', 'bottomright' place it inside.
    var legItems = o.legend === false ? [] : s.filter(function (q) { return q.label; });
    var below = !o.legendAt || o.legendAt === 'below', legRows = below ? Math.ceil(legItems.length / 2) : 0, H0 = H;
    H = H0 + (legRows ? legRows * 17 + 6 : 0);
    var xs = [], ys = [];
    s.forEach(function (q) { q.x.forEach(function (v, i) { var y = q.y[i]; if (isFinite(v) && isFinite(y) && (!o.xlog || v > 0) && (!o.ylog || y > 0)) { xs.push(v); ys.push(y); } }); });
    var xmin = o.xmin !== undefined ? o.xmin : Math.min.apply(null, xs), xmax = o.xmax !== undefined ? o.xmax : Math.max.apply(null, xs);
    var ymin = o.ymin !== undefined ? o.ymin : Math.min.apply(null, ys), ymax = o.ymax !== undefined ? o.ymax : Math.max.apply(null, ys);
    if (xmax === xmin) xmax = xmin + 1; if (ymax === ymin) ymax = ymin + 1;
    var fx = o.xlog ? function (v) { return L + pw * (Math.log(v / xmin) / Math.log(xmax / xmin)); } : function (v) { return L + pw * (v - xmin) / (xmax - xmin); };
    var fy = o.ylog ? function (v) { return T + ph * (1 - Math.log(v / ymin) / Math.log(ymax / ymin)); } : function (v) { return T + ph * (1 - (v - ymin) / (ymax - ymin)); };
    var id = o.id || ('c' + Math.random().toString(36).slice(2, 8));
    var out = ['<svg class="chart" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc(o.title || o.ylabel || 'chart') + '" xmlns="http://www.w3.org/2000/svg">',
      '<defs><clipPath id="' + id + '"><rect x="' + L + '" y="' + T + '" width="' + pw + '" height="' + ph + '"/></clipPath></defs>',
      '<rect x="0" y="0" width="' + W + '" height="' + H + '" fill="#fff"/>'];
    var xt = o.xlog ? logTicks(xmin, xmax) : niceTicks(xmin, xmax, o.xticks || 6), yt = o.ylog ? logTicks(ymin, ymax) : niceTicks(ymin, ymax, o.yticks || 5);
    xt.forEach(function (v) { var X = fx(v).toFixed(1); out.push('<line x1="' + X + '" x2="' + X + '" y1="' + T + '" y2="' + (T + ph) + '" stroke="#ece3d2" stroke-width="1"/><text x="' + X + '" y="' + (T + ph + 16) + '" text-anchor="middle" class="tick">' + fmt(v) + '</text>'); });
    yt.forEach(function (v) { var Y = fy(v).toFixed(1); out.push('<line x1="' + L + '" x2="' + (L + pw) + '" y1="' + Y + '" y2="' + Y + '" stroke="#ece3d2" stroke-width="1"/><text x="' + (L - 6) + '" y="' + (+Y + 4) + '" text-anchor="end" class="tick">' + fmt(v) + '</text>'); });
    out.push('<rect x="' + L + '" y="' + T + '" width="' + pw + '" height="' + ph + '" fill="none" stroke="#3f2c23" stroke-width="1"/>');
    (o.vlines || []).forEach(function (q) { var X = fx(q.x).toFixed(1); out.push('<line x1="' + X + '" x2="' + X + '" y1="' + T + '" y2="' + (T + ph) + '" stroke="#6f665e" stroke-dasharray="3 3"/>' + (q.label ? '<text x="' + (+X + 4) + '" y="' + (T + 12) + '" class="tick">' + esc(q.label) + '</text>' : '')); });
    (o.hlines || []).forEach(function (q) { var Y = fy(q.y).toFixed(1); out.push('<line x1="' + L + '" x2="' + (L + pw) + '" y1="' + Y + '" y2="' + Y + '" stroke="#6f665e" stroke-dasharray="3 3"/>' + (q.label ? '<text x="' + (L + pw - 4) + '" y="' + (+Y - 4) + '" text-anchor="end" class="tick">' + esc(q.label) + '</text>' : '')); });
    out.push('<g clip-path="url(#' + id + ')">');
    s.forEach(function (q, k) {
      var c = q.color || COL[k % COL.length], pts = [];
      q.x.forEach(function (v, i) { var y = q.y[i]; if (isFinite(v) && isFinite(y) && (!o.xlog || v > 0) && (!o.ylog || y > 0)) pts.push(fx(v).toFixed(1) + ',' + fy(y).toFixed(1)); });
      if (q.dots) pts.forEach(function (pt) { var a = pt.split(','); out.push('<circle cx="' + a[0] + '" cy="' + a[1] + '" r="' + (q.r || 3) + '" fill="' + c + '"/>'); });
      else if (pts.length) out.push('<polyline fill="none" stroke="' + c + '" stroke-width="' + (q.width || 2) + '"' + (q.dash ? ' stroke-dasharray="' + q.dash + '"' : '') + ' points="' + pts.join(' ') + '"/>');
    });
    out.push('</g>');
    if (o.xlabel) out.push('<text x="' + (L + pw / 2) + '" y="' + (H0 - 8) + '" text-anchor="middle" class="axl">' + esc(o.xlabel) + '</text>');
    if (o.ylabel) out.push('<text transform="translate(14 ' + (T + ph / 2) + ') rotate(-90)" text-anchor="middle" class="axl">' + esc(o.ylabel) + '</text>');
    if (below && legItems.length) {
      legItems.forEach(function (q, k) {
        var c = q.color || COL[s.indexOf(q) % COL.length], lx = L + (k % 2) * (pw / 2), y = H0 + 10 + 17 * Math.floor(k / 2);
        out.push('<line x1="' + lx + '" x2="' + (lx + 18) + '" y1="' + (y - 4) + '" y2="' + (y - 4) + '" stroke="' + c + '" stroke-width="2.5"' + (q.dash ? ' stroke-dasharray="' + q.dash + '"' : '') + '/><text x="' + (lx + 24) + '" y="' + y + '" class="leg">' + esc(q.label) + '</text>');
      });
    } else if (o.legend !== false) {
      var lx = L + 10, ly = T + 14, items = legItems;
      if (o.legendAt === 'right') { lx = L + pw - 200; }
      if (o.legendAt === 'bottom') { ly = T + ph - 14 * items.length; }
      if (o.legendAt === 'bottomright') { lx = L + pw - 182; ly = T + ph - 15 * items.length; }
      items.forEach(function (q, k) {
        var c = q.color || COL[s.indexOf(q) % COL.length], y = ly + 15 * k;
        out.push('<line x1="' + lx + '" x2="' + (lx + 18) + '" y1="' + (y - 4) + '" y2="' + (y - 4) + '" stroke="' + c + '" stroke-width="2.5"' + (q.dash ? ' stroke-dasharray="' + q.dash + '"' : '') + '/><text x="' + (lx + 24) + '" y="' + y + '" class="leg">' + esc(q.label) + '</text>');
      });
    }
    out.push('</svg>');
    return out.join('');
  }
  return { line: line, COL: COL, fmt: fmt };
})();
/*CHART-END*/
if (typeof module !== 'undefined') module.exports = CHART;
