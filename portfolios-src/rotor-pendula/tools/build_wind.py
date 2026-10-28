#!/usr/bin/env python3
"""Finish rotor_wind.html in place (the Wind tab); it can be run any number of times.

1. The simulation page's layout stylesheet (rotor_sim.html, the <style> after the fonts) is copied between /*SIMCSS-BEGIN*/ and
   /*SIMCSS-END*/, so the two tabs share one look.
2. The study's fonts and KaTeX, as build_sim.py does for rotor_sim.html: fonts/fonts-embedded.css between /*FONTS-BEGIN*/ and
   /*FONTS-END*/; every <div class="eq tex" data-tex="..."></div><!--/eq--> typeset from its data-tex, and KaTeX's stylesheet
   with the fonts it needs between /*KATEX-BEGIN*/ and /*KATEX-END*/.
The physics block (/*WIND-BEGIN*/ ... /*WIND-END*/) is the page's own source; tools/check_wind.js runs it against
notes/rotor-pendula/derive/L6_wind.py.
Usage: python3 tools/build_wind.py   (after python3 tools/build_sim.py)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from build_sim import typeset_page  # noqa: E402

PAGE = ROOT / 'rotor_wind.html'
s = PAGE.read_text()
sim = (ROOT / 'rotor_sim.html').read_text()
a = sim.index('<style>\n/* Layout as the hydraulics')
css = sim[a + len('<style>\n'):sim.index('</style>', a)].rstrip()
s = re.sub(r'/\*SIMCSS-BEGIN\*/[\s\S]*?/\*SIMCSS-END\*/', lambda m: '/*SIMCSS-BEGIN*/\n' + css + '\n/*SIMCSS-END*/', s, count=1)
s, n = typeset_page(s)
PAGE.write_text(s)
print(f'rotor_wind.html: {n} equations typeset, {len(s) / 1e6:.2f} MB')
