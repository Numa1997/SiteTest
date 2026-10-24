#!/usr/bin/env python3
"""Number check of the lecture note: every number in theory/*.src.html is either filled in by tools/make_numbers.py
({{n:key}}, {{table:key}}) or listed, with its reason, in tools/typed_numbers.py; derived numbers listed there are
recomputed and compared.  Also checks that every placeholder has a value in numbers.json.

Usage: python3 tools/check_numbers.py      (exit 1 on any unexplained number, failed recomputation or missing key)
"""
import json, math, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from typed_numbers import TYPED, ENV
D = ROOT / 'data'
NUM = json.load(open(ROOT / 'numbers.json'))
bad = 0; seen = 0
for p in sorted((ROOT / 'theory').glob('*.src.html')):
    s = p.read_text(); tag = p.name[:2]; allow = TYPED.get(tag, {})
    for kind, key in re.findall(r'\{\{(n|table):([A-Za-z0-9_]+)\}\}', s):
        if key not in NUM['n' if kind == 'n' else 'table']:
            print(f'{p.name}: missing {kind} key {key}'); bad += 1
    s = re.sub(r'\{\{(n|table):[A-Za-z0-9_]+\}\}', '#', s)
    s = re.sub(r'<h[23][^>]*>.*?</h[23]>', ' ', s, flags=re.S)
    s = re.sub(r'<ol class="refs">.*?</ol>', ' ', s, flags=re.S)          # the list of sources: bibliographic numbers
    s = re.sub(r'\\tag\{[\d.]+\}', '', s)
    s = re.sub(r'<[^>]+>', ' ', s); s = re.sub(r'\s+', ' ', s)
    # cross-references: (2.3), section 3.1, chapters 4 to 6, Table 2, Figure 1
    s = re.sub(r'\((\d+\.\d+)\)', '(ref)', s)
    s = re.sub(r'\b(section|sections|chapter|chapters|table|figure|equation)\s+\d+(\.\d+)?', r'\1 ref', s, flags=re.I)
    s = re.sub(r'\bref (and|to|or) \d+(\.\d+)?', r'ref \1 ref', s)
    for m in re.finditer(r'(?<![A-Za-z0-9.\\{_^])(\d[\d ]*\d|\d)(\.\d+)?(?![\d]*[A-Za-z_]*\})', s):
        num = (m.group(1) + (m.group(2) or '')).strip()
        if not re.search(r'\d', num):
            continue
        seen += 1
        if '.' not in num and ' ' not in num and int(num) <= 10:
            continue
        why = allow.get(num)
        ctx = s[max(0, m.start() - 40):m.end() + 20]
        if why is None:
            print(f'{p.name}: unexplained number {num!r} | {ctx}'); bad += 1
        elif isinstance(why, tuple):
            _, expr, tol, _ = why
            val = eval(expr, {**ENV, 'math': math, 'json': json, 'D': D, 'N': NUM['n']})
            typed = float(num.replace(' ', ''))
            if abs(val - typed) > tol*abs(val):
                print(f'{p.name}: {num} does not match {expr} = {val:.6g} (tolerance {tol}) | {ctx}'); bad += 1
print(f'{seen} numbers read in the sources; {len(NUM["n"])} computed values; {"PASS" if bad == 0 else f"{bad} FAIL"}')
sys.exit(1 if bad else 0)
