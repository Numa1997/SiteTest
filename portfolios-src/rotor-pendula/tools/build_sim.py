#!/usr/bin/env python3
"""Finish rotor_sim.html in place; it can be run any number of times.

1. The study's fonts (fonts/fonts-embedded.css, written by tools/build_fonts.py) go between /*FONTS-BEGIN*/ and /*FONTS-END*/.
2. Every <div class="eq tex" data-tex="..."> ... </div><!--/eq--> is typeset again from its data-tex with KaTeX
   (tools/katex_render.js), and KaTeX's stylesheet, with the fonts it needs embedded, goes between /*KATEX-BEGIN*/ and
   /*KATEX-END*/. The page runs no maths library.
3. Numbers: <span data-n="key">...</span> and <tbody data-t="key">...</tbody> are filled from data/sim_solutions.json
   (tools/sim_solutions.js) and data/sim_check.json (tools/check_sim.js). An unknown key stops the build.

Usage: (cd tools && npm install) once; node tools/check_sim.js; node tools/sim_solutions.js; python3 tools/build_sim.py
"""
import base64
import html
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = ROOT / 'tools'
PAGE = ROOT / 'rotor_sim.html'
KATEX = TOOLS / 'node_modules' / 'katex' / 'dist'

def typeset_page(s):
    """Steps 1 and 2 on the text of a page: the fonts, then every equation and KaTeX's stylesheet. Returns (text, equations)."""
    fonts = (ROOT / 'fonts' / 'fonts-embedded.css').read_text().strip()
    s = re.sub(r'/\*FONTS-BEGIN\*/[\s\S]*?/\*FONTS-END\*/', lambda m: '/*FONTS-BEGIN*/\n' + fonts + '\n/*FONTS-END*/', s, count=1)
    texs = [html.unescape(m.group(1)) for m in BLOCK.finditer(s)]
    res = subprocess.run(['node', str(TOOLS / 'katex_render.js')], input=json.dumps([{'tex': t, 'display': True} for t in texs]),
                         capture_output=True, text=True, check=True)
    out = json.loads(res.stdout)
    bad = [(t, r['error']) for t, r in zip(texs, out) if 'error' in r]
    if bad:
        for t, e in bad:
            print('KaTeX error:', e, '\n   in:', t[:160])
        raise SystemExit(1)
    it = iter(zip(texs, out))

    def put(_m):
        t, r = next(it)
        label = html.escape(re.sub(r'\s+', ' ', t), quote=True)
        return f'<div class="eq tex" data-tex="{html.escape(t, quote=True)}" role="img" aria-label="{label}">{r["html"]}</div><!--/eq-->'

    s = BLOCK.sub(put, s)
    css = (KATEX / 'katex.min.css').read_text()
    css = re.sub(r'@font-face\{[^}]*\}', _embed, css)
    s = re.sub(r'/\*KATEX-BEGIN\*/[\s\S]*?/\*KATEX-END\*/', lambda m: '/*KATEX-BEGIN*/\n' + css + '\n/*KATEX-END*/', s, count=1)
    return s, len(texs)


BLOCK = re.compile(r'<div class="eq tex" data-tex="([^"]*)"[^>]*>[\s\S]*?</div><!--/eq-->')
KEEP = ('Main', 'Math', 'AMS', 'Size1', 'Size2', 'Size3', 'Size4')


def _embed(m):
    rule = m.group(0)
    if not re.search(r'font-family:KaTeX_(%s);' % '|'.join(KEEP), rule):
        return ''
    fn = re.search(r'url\(fonts/(KaTeX_[\w-]+)\.woff2\)', rule).group(1)
    data = base64.b64encode((KATEX / 'fonts' / f'{fn}.woff2').read_bytes()).decode()
    return re.sub(r'src:[^;}]*', f'src:url(data:font/woff2;base64,{data}) format("woff2")', rule)


def main():
    s, ntex = typeset_page(PAGE.read_text())
    # 3. numbers and tables
    N, T = {}, {}
    for name in ('sim_solutions.json', 'sim_check.json'):
        d = json.loads((ROOT / 'data' / name).read_text())
        N.update(d.get('n', {}))
        T.update(d.get('t', {}))
    used = set()


    def num(m):
        k = m.group(1)
        if k not in N:
            raise SystemExit(f'unknown number key: {k}')
        used.add(k)
        return f'<span data-n="{k}">{html.escape(N[k], quote=False)}</span>'


    def tab(m):
        k = m.group(1)
        if k not in T:
            raise SystemExit(f'unknown table key: {k}')
        return f'<tbody data-t="{k}">{T[k]}</tbody>'


    s = re.sub(r'<span data-n="([A-Za-z0-9_]+)">[^<]*</span>', num, s)
    s = re.sub(r'<tbody data-t="([A-Za-z0-9_]+)">[\s\S]*?</tbody>', tab, s)
    PAGE.write_text(s)
    print(f'rotor_sim.html: {ntex} equations typeset, {len(used)} numbers and {len(T)} tables filled, {len(s) / 1e6:.2f} MB')


if __name__ == '__main__':
    main()
