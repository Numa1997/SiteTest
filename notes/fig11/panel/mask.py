#!/usr/bin/env python3
"""Mask the new English strings for DeepL: maths, symbols, markup, identifiers and equation numbers become ⟦n⟧.
   mask.py todo.json out.json   ->  out.json = [{"en": ..., "masked": ..., "map": {"⟦0⟧": ...}}]"""
import json, re, sys
todo = json.load(open(sys.argv[1]))['strings']
PAT = [
    r"rgb\(\d+, \d+, \d+\)",
    r"\((?:\d+[a-z]?)\)(?:–\((?:\d+[a-z]?)\))?",                     # (16b), (25)–(26)
    r"\([^()]*[θẋ][^()]*\)",                                         # (x, θ₁, θ₂, ẋ, θ̇₁, θ̇₂)
    r"[^\s,;:()]*=[^,;]*",                                           # a formula from an = sign to the next comma
    r"[A-Za-zΦΓθσλρ|]*<su[bp]>[^<]*</su[bp]>[^\s,;)]*",             # x<sub>cart</sub>
    r"\b[A-Za-z]+_[A-Za-z0-9]+\b",                                    # T_s, x_c, u_max
    r"\|λ\| ≥ 1|\|λ\||±π|0\.9 c\*|Φ − ΓK|Φ, Γ|\bK\b|\bP\b|[ρΦΓσ]|ẍ|θ̈₁|θ̈₂|θ₁|θ₂|u Δx|\bj\(k\)|\bRK4\b|\d+(?:\.\d+)? ?(?:px|ms|N|s|m|kg|%)\b|m/s²|rad/s²",
    r"\b(?:kg m²|kg m|kg)\b",
]
out = []
for en in todo:
    m, k = {}, 0
    s = en
    for p in PAT:
        def sub(mo):
            global_k = len(m); t = '⟦%d⟧' % global_k; m[t] = mo.group(0); return t
        s = re.sub(p, sub, s)
    out.append({'en': en, 'masked': s, 'map': m})
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
for o in out: print(o['masked'])
