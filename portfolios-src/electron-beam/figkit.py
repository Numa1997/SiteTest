"""The Electron Beam, from Tip to Measurement · figkit.py · layout helpers for the inline SVG figures of the chapters.

Why: a figure is drawn once in user units and scaled to its plate, so a 760-unit-wide drawing shows its 11-unit labels at 4.5 CSS px on a
360 px phone, and labels placed by hand land on curves. Three helpers, used by text/ch00.py to ch02.py and open to every chapter:

  width(markup, cls)      advance width of a label in user units, from the house fonts' own advance widths (measured with canvas
                          measureText in Chromium on the built page, 11 November 2026: IBM Plex Sans 400 and 600, IBM Plex Mono, Latin
                          Modern Roman italic and upright); it understands the tspans the figures use (class m, mu, font-size).
  Layout(W, H)            the obstacles of one drawing (curve points, shapes, placed labels) on a hashed grid. place() puts a label at
                          the free spot nearest to where it is wanted, inside a region, with a short leader line when it had to move
                          away; the leader carries data-nocollide, the allow-list of checks/check_figures.cjs.
  dual(wide, narrow)      one figure as two drawings: the wide one from 700 px of window width up, the narrow one (300 units wide, so
                          an 11-unit label shows at 11 CSS px on a 360 px phone) below. A <style> in the wide drawing switches them; the
                          hidden one takes no room and is out of the accessibility tree.

A label's ink box here is the one the checker tests: from 0.74 em above the baseline to 0.18 em below it.
"""
import math
import re

# advance widths in hundredths of an em: font -> (characters, widths)
_TABLE = {
    'sans': ('0123456789 !"#$%&\'()*+,-./:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~§°±²³µ·¹½×áèöøΔΦΩαδεηθκλπστφρζνμγβωψχΓΛΣΠΘ–—’…‴‹›⁗⁰⁴⁵⁶⁷⁸⁹⁻₀₁₂₃₉ₛ−∥≈●★≤≥→←↑↓∞√∝∂∇',
           [60,60,60,60,60,60,60,60,60,60,24,28,42,71,60,93,69,24,33,33,45,60,27,40,27,38,29,29,60,60,60,48,89,64,65,62,67,58,56,69,71,40,51,63,50,81,71,71,61,71,64,58,57,68,61,89,61,59,58,32,38,32,60,56,60,53,58,50,58,55,32,53,57,25,25,53,27,87,57,56,58,58,37,49,35,57,49,77,51,50,46,34,31,34,60,59,47,60,35,35,57,33,36,87,60,53,55,56,57,64,85,72,64,56,52,57,56,53,51,62,58,48,71,55,43,51,58,50,58,74,73,50,50,63,57,69,71,59,78,27,80,42,30,30,88,46,35,35,35,35,35,35,43,35,35,35,35,35,39,60,50,55,60,104,55,55,100,100,82,82,71,55,71,49,67]),
    'sans600': ('0123456789 !"#$%&\'()*+,-./:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~§°±²³µ·¹½×áèöøΔΦΩαδεηθκλπστφρζνμγβωψχΓΛΣΠΘ–—’…‴‹›⁗⁰⁴⁵⁶⁷⁸⁹⁻₀₁₂₃₉ₛ−∥≈●★≤≥→←↑↓∞√∝∂∇',
           [60,60,60,60,60,60,60,60,60,60,24,31,47,66,60,96,71,26,34,34,56,60,30,40,30,44,32,32,60,60,60,49,90,67,66,64,69,60,58,71,72,42,54,68,52,82,72,71,64,71,66,61,58,69,64,95,65,63,60,33,44,33,60,56,60,56,60,51,60,56,35,54,59,27,27,56,29,89,59,56,60,60,39,50,37,59,52,82,54,52,50,36,38,36,60,57,47,60,35,34,59,35,35,86,60,56,56,56,57,67,85,71,66,56,52,60,57,56,53,64,58,49,76,57,43,53,60,53,60,76,75,53,51,66,60,70,72,59,78,29,87,55,31,31,88,46,30,30,30,30,30,30,43,30,30,30,30,30,39,60,50,55,60,104,55,55,100,100,88,88,71,55,71,49,67]),
    'mono': ('0123456789 !"#$%&\'()*+,-./:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~§°±²³µ·¹½×áèöøΔΦΩαδεηθκλπστφρζνμγβωψχΓΛΣΠΘ–—’…‴‹›⁗⁰⁴⁵⁶⁷⁸⁹⁻₀₁₂₃₉ₛ−∥≈●★≤≥→←↑↓∞√∝∂∇',
           [60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,64,73,74,52,47,42,52,48,50,48,50,54,40,58,50,41,45,54,44,51,66,63,44,58,73,58,72,72,60,60,60,60,42,60,60,88,46,35,35,35,35,35,35,43,35,35,35,35,35,39,60,50,55,60,104,55,55,100,100,60,60,71,55,71,49,67]),
    'tex': ('0123456789 !"#$%&\'()*+,-./:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~§°±²³µ·¹½×áèöøΔΦΩαδεηθκλπστφρζνμγβωψχΓΛΣΠΘ–—’…‴‹›⁗⁰⁴⁵⁶⁷⁸⁹⁻₀₁₂₃₉ₛ−∥≈●★≤≥→←↑↓∞√∝∂∇',
           [51,51,51,51,51,51,51,51,51,51,36,31,40,82,50,82,77,31,41,41,51,77,31,36,31,51,31,31,78,77,78,51,77,74,70,72,75,68,65,77,74,39,52,77,63,90,74,77,68,77,73,56,72,74,74,100,74,74,61,31,50,31,56,74,51,51,46,46,51,46,31,46,51,31,31,46,26,82,56,51,51,46,42,41,33,54,46,66,46,49,41,50,28,50,56,49,38,77,39,36,51,77,37,81,77,51,46,51,51,59,76,72,52,46,39,50,49,48,43,50,49,36,55,48,40,44,50,39,50,71,62,44,57,60,59,72,72,51,102,31,68,42,36,36,88,46,35,35,35,35,35,35,43,35,35,35,35,35,39,77,50,55,60,104,55,55,97,97,51,51,92,46,71,49,67]),
    'texr': ('0123456789 !"#$%&\'()*+,-./:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~§°±²³µ·¹½×áèöøΔΦΩαδεηθκλπστφρζνμγβωψχΓΛΣΠΘ–—’…‴‹›⁗⁰⁴⁵⁶⁷⁸⁹⁻₀₁₂₃₉ₛ−∥≈●★≤≥→←↑↓∞√∝∂∇',
           [50,50,50,50,50,50,50,50,50,50,33,28,37,83,50,83,78,28,39,39,50,78,28,33,28,50,28,28,78,78,78,47,78,75,71,72,76,68,65,78,75,36,51,78,62,92,75,78,68,78,74,56,72,75,75,103,75,75,61,28,50,28,56,75,50,50,56,44,56,44,31,50,56,28,31,53,28,83,56,50,56,53,39,39,39,56,53,72,53,53,44,50,28,50,56,48,37,78,36,36,56,78,37,82,78,50,44,50,50,64,73,74,52,47,42,52,48,50,48,50,54,40,58,50,41,45,54,44,51,66,63,44,58,73,58,72,72,50,100,28,67,42,39,39,88,46,35,35,35,35,35,35,43,35,35,35,35,35,39,78,50,55,60,104,55,55,100,100,50,50,100,47,71,49,67]),
}
_W = {k: dict(zip(c, w)) for k, (c, w) in _TABLE.items()}
# class -> (font, size in user units), as public/styles/paper.css sets them for .pfig svg
CLS = {'tick': ('mono', 11.0), 'lbl': ('sans', 12.5), 'm': ('tex', 17.0), 'mu': ('texr', 16.0), None: ('sans', 13.0)}
ENT = {'&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'", '&nbsp;': ' '}
NARROW_W = 300          # user units of a narrow drawing


def _plain(s):
    for k, v in ENT.items():
        s = s.replace(k, v)
    return s


def seg_width(txt, font='sans', size=12.5, bold=False):
    tab = _W['sans600' if (bold and font == 'sans') else font]
    txt = re.sub(r'\s+', ' ', _plain(txt))
    return sum(tab.get(c, 60) for c in txt) / 100.0 * size


def _segments(markup, cls='lbl', size=None, bold=False):
    """(text, font, size, bold) pieces of a label; a tspan with class m / mu or a font-size changes font and size."""
    font, sz = CLS.get(cls, CLS[None])
    sz = size or sz
    out, pos = [], 0
    for m in re.finditer(r'<tspan([^>]*)>(.*?)</tspan>', markup):
        if m.start() > pos:
            out.append((re.sub(r'<[^>]+>', '', markup[pos:m.start()]), font, sz, bold))
        attrs = m.group(1)
        c = re.search(r'class="([^"]*)"', attrs)
        f2, s2 = CLS.get(c.group(1), (font, sz)) if c else (font, sz)
        fs = re.search(r'font-size="([\d.]+)"', attrs)
        if fs:
            s2 = float(fs.group(1))
        out.append((re.sub(r'<[^>]+>', '', m.group(2)), f2, s2, bold))
        pos = m.end()
    if pos < len(markup):
        out.append((re.sub(r'<[^>]+>', '', markup[pos:]), font, sz, bold))
    return out


def width(markup, cls='lbl', size=None, bold=False):
    return sum(seg_width(t, f, s, b) for t, f, s, b in _segments(markup, cls, size, bold))


def em(cls='lbl', size=None):
    return size or CLS.get(cls, CLS[None])[1]


LEAD = 1.3              # line height of a label of several lines, in em


def text_box(x, y, markup, cls='lbl', anchor='start', size=None, bold=False):
    """Ink box of a label; a list of strings is a label of several lines, the first baseline at y."""
    lines = markup if isinstance(markup, (list, tuple)) else [markup]
    w, e = max(width(t, cls, size, bold) for t in lines), em(cls, size)
    top = max(sz for t in lines[:1] for _, _, sz, _ in _segments(t, cls, size, bold))       # a larger tspan (a symbol) reaches higher
    x0 = x - (w if anchor == 'end' else w / 2 if anchor == 'middle' else 0)
    return (x0, y - 0.74 * top, x0 + w, y + (len(lines) - 1) * LEAD * e + 0.18 * e)


def text(x, y, markup, cls='lbl', anchor='start', extra='', size=None):
    lines = markup if isinstance(markup, (list, tuple)) else [markup]
    e = em(cls, size)
    return ''.join('<text class="%s" x="%.1f" y="%.1f" text-anchor="%s"%s>%s</text>' % (cls, x, y + i * LEAD * e, anchor, (' ' + extra) if extra else '', t)
                   for i, t in enumerate(lines))


def wrap(words, maxw, cls='lbl', size=None):
    """Split a plain label into lines no wider than maxw."""
    lines, cur = [], ''
    for wd in words.split(' '):
        t = (cur + ' ' + wd).strip()
        if cur and width(t, cls, size) > maxw:
            lines.append(cur)
            cur = wd
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def overlap(a, b, m=0.0):
    return a[0] < b[2] + m and b[0] < a[2] + m and a[1] < b[3] + m and b[1] < a[3] + m


class Layout:
    """Obstacles of one drawing, in its user units. Points sit in a hashed grid of `cell` units."""

    def __init__(s, W, H, cell=8.0):
        s.W, s.H, s.cell = W, H, cell
        s.grid = {}
        s.boxes = []

    def point(s, x, y, hw=1.0):
        s.grid.setdefault((int(x // s.cell), int(y // s.cell)), []).append((x, y, hw))

    def line(s, pts, hw=1.0, step=2.0):
        pts = [p for p in pts if p is not None]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
            for k in range(n):
                s.point(x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n, hw)
        if pts:
            s.point(pts[-1][0], pts[-1][1], hw)

    def rect(s, x, y, w, h, hw=0.6):
        s.line([(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], hw)

    def circle(s, cx, cy, r, hw=0.6):
        n = max(8, int(2 * math.pi * r / 2))
        s.line([(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n + 1)], hw)

    def box(s, b):
        s.boxes.append(b)

    def hits(s, b, m=2.5, region=None):
        r = region or (0, 0, s.W, s.H)
        if b[0] < r[0] or b[1] < r[1] or b[2] > r[2] or b[3] > r[3]:
            return True
        if any(overlap(b, o, m) for o in s.boxes):
            return True
        c = s.cell
        for i in range(int((b[0] - m - 4) // c), int((b[2] + m + 4) // c) + 1):
            for j in range(int((b[1] - m - 4) // c), int((b[3] + m + 4) // c) + 1):
                for x, y, hw in s.grid.get((i, j), ()):
                    if b[0] - m - hw < x < b[2] + m + hw and b[1] - m - hw < y < b[3] + m + hw:
                        return True
        return False

    def place(s, markup, x, y, cls='lbl', anchor='start', region=None, radius=90, step=3, extra='', leader=True, size=None,
              anchors=None, prefer=None, lead_to=None, m=2.5, force=True):
        """Put a label at (x, y), or at the nearest free spot within `radius`; returns its SVG (the text, and a leader line to
        `lead_to` (default (x, y)) when it moved more than 16 units). anchors: text-anchor values to try at each spot.
        prefer: a direction (dx, dy) whose spots count as nearer. With force, a label that finds no free spot stays where asked
        (the checker will report it); without, None is returned."""
        cands = []
        R = int(radius // step)
        pl = math.hypot(*prefer) if prefer else 1
        for i in range(-R, R + 1):
            for j in range(-R, R + 1):
                dx, dy = i * step, j * step
                d = math.hypot(dx, dy)
                if d > radius:
                    continue
                if prefer:
                    d -= 0.35 * (dx * prefer[0] + dy * prefer[1]) / pl
                cands.append((d, dx, dy))
        cands.sort()
        best = None
        for d, dx, dy in cands:
            for an in (anchors or [anchor]):
                b = text_box(x + dx, y + dy, markup, cls, an, size)
                if not s.hits(b, m, region):
                    best = (x + dx, y + dy, an, b, math.hypot(dx, dy))
                    break
            if best:
                break
        if best is None:
            if not force:
                return None
            best = (x, y, anchor, text_box(x, y, markup, cls, anchor, size), 0)
        px, py, an, b, dist = best
        s.box(b)
        out = text(px, py, markup, cls, an, extra, size)
        if leader and dist > 16:
            ax, ay = lead_to or (x, y)
            ex, ey = min(max(ax, b[0] - 1), b[2] + 1), min(max(ay, b[1] - 1), b[3] + 1)
            if math.hypot(ex - ax, ey - ay) > 4:
                out = ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#b5aaa0" stroke-width="0.8" data-nocollide=""/>' % (ax, ay, ex, ey)) + out
        return out


STYLE = ('<style>.pfig__plate svg.fk-n{display:none}@media (max-width:699.98px){.pfig__plate svg.fk-w{display:none}'
         '.pfig__plate svg.fk-n{display:block;max-width:440px;margin:0 auto}}</style>')


def dual(wide, narrow):
    """The wide drawing (carrying the switch) followed by the narrow one; both are complete <svg> elements with a viewBox."""
    wide = wide.strip().replace('<svg ', '<svg class="fk-w" ', 1)
    i = wide.index('>') + 1
    wide = wide[:i] + STYLE + wide[i:]
    narrow = narrow.strip().replace('<svg ', '<svg class="fk-n" ', 1)
    return wide + narrow
