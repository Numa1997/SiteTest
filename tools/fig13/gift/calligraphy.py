"""Outlines of Arabic words in a calligraphic font, as closed polylines, for the phasor (Fourier) drawing in reem.html.

Shaping (the joined letter forms of Arabic) by HarfBuzz (uharfbuzz), outlines by fontTools; curves flattened to straight pieces.
Coordinates in font units, y up, the word's visual left at x = 0.

    from calligraphy import word_contours
    contours = word_contours('Font.ttf', 'ريم')        # list of (n, 2) arrays, each a closed contour
"""
import numpy as np
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen


class FlatPen(BasePen):
    """Records each contour as points; quadratic and cubic pieces flattened into STEPS straight pieces."""
    STEPS = 12

    def __init__(self, glyphset, dx, dy):
        super().__init__(glyphset)
        self.dx, self.dy, self.contours, self.cur = dx, dy, [], []

    def _p(self, p):
        return (p[0] + self.dx, p[1] + self.dy)

    def _moveTo(self, p):
        self.cur = [self._p(p)]

    def _lineTo(self, p):
        self.cur.append(self._p(p))

    def _curveToOne(self, p1, p2, p3):
        p0 = np.array(self.cur[-1]); a, b, c = np.array(self._p(p1)), np.array(self._p(p2)), np.array(self._p(p3))
        for t in np.linspace(0, 1, self.STEPS + 1)[1:]:
            self.cur.append(tuple((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * a + 3 * (1 - t) * t ** 2 * b + t ** 3 * c))

    def _qCurveToOne(self, p1, p2):
        p0 = np.array(self.cur[-1]); a, b = np.array(self._p(p1)), np.array(self._p(p2))
        for t in np.linspace(0, 1, self.STEPS + 1)[1:]:
            self.cur.append(tuple((1 - t) ** 2 * p0 + 2 * (1 - t) * t * a + t ** 2 * b))

    def _closePath(self):
        if len(self.cur) > 2:
            self.contours.append(np.array(self.cur))
        self.cur = []

    _endPath = _closePath


def word_contours(font_path, text):
    blob = hb.Blob.from_file_path(font_path)
    face = hb.Face(blob); font = hb.Font(face)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, {'kern': True, 'liga': True})
    tt = TTFont(font_path); gs = tt.getGlyphSet(); order = tt.getGlyphOrder()
    x, out = 0, []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):          # visual order, left to right
        pen = FlatPen(gs, x + pos.x_offset, pos.y_offset)
        gs[order[info.codepoint]].draw(pen)
        out += pen.contours
        x += pos.x_advance
    assert out, 'no outline: does the font cover ' + text + '?'
    return out
