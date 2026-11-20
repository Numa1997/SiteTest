"""Fig. 13: the two words of the gift as SVG, from the same outlines the gift film fills (tools/fig13/gift/reem.json, 'fill',
even-odd rule): public/images/fig13/reem.svg (رِيمْ) and public/images/fig13/farashatuki.svg (فَرَاشَتُكِ). The films panel of the
Fig. 13 page shows them as its heading. Colour: currentColor is not available to an <img>, so the wine of the house, #7a1f2b, and
a rose for the dark panel (-night.svg).     python3 tools/fig13/calligraphy_svg.py"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
D = json.loads((ROOT / 'tools/fig13/gift/reem.json').read_text())
for key, name in (('reem', 'reem'), ('butterfly', 'farashatuki')):
    w = D[key]; pts = [p for c in w['fill'] for p in c]
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts); y0, y1 = min(-p[1] for p in pts), max(-p[1] for p in pts)
    pad = 0.02 * (x1 - x0); S = 1000 / (x1 - x0 + 2 * pad)
    d = ''.join('M' + 'L'.join('%.1f %.1f' % ((x - x0 + pad) * S, (-y - y0 + pad) * S) for x, y in c) + 'Z' for c in w['fill'])
    W, H = round((x1 - x0 + 2 * pad) * S), round((y1 - y0 + 2 * pad) * S)
    for suffix, col in (('', '#7a1f2b'), ('-night', '#e2a2aa')):
        (ROOT / f'public/images/fig13/{name}{suffix}.svg').write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{w["text"]}"><path fill="{col}" fill-rule="evenodd" d="{d}"/></svg>\n')
    print(name, W, H)
