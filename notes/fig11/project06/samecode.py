#!/usr/bin/env python3
"""Projects 05 and 06 run one script: compare every inline <script> of the two pages except the settings block #dipc-page.
python3 notes/fig11/project06/samecode.py ; exit 1 on any difference."""
import re, sys, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../public/simulations/')
def scripts(f):
    s = open(R + f, encoding='utf-8').read()
    return [m.group(2) for m in re.finditer(r'<script(\s[^>]*)?>(.*?)</script>', s, re.S) if 'dipc-page' not in (m.group(1) or '') and m.group(2).strip()]
a, b = scripts('double-inverted-pendulum.html'), scripts('rods-in-liquid.html')
same = len(a) == len(b) and all(x == y for x, y in zip(a, b))
print(f'{len(a)} and {len(b)} inline scripts, {sum(map(len, a))} and {sum(map(len, b))} characters:', 'identical' if same else 'DIFFERENT')
sys.exit(0 if same else 1)
