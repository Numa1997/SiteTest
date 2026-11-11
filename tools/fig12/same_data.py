#!/usr/bin/env python3
"""Do two Fig. 12 data files hold the same numbers? python3 tools/fig12/same_data.py <a.json> <b.json>
Exit 0 if every number agrees within 2e-5 absolute or 1e-5 relative (the files round to 5-8 digits, and a different maths
library can flip the last one), 1 if they differ or one is missing. The pipeline commits a new file only on exit 1."""
import json, sys, os


def leaves(x, path=''):
    if isinstance(x, dict):
        for k in sorted(x): yield from leaves(x[k], path + '/' + k)
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from leaves(v, f'{path}[{i}]')
    else:
        yield path, x


a, b = sys.argv[1:3]
if not (os.path.exists(a) and os.path.exists(b)):
    print('missing file'); sys.exit(1)
A, B = dict(leaves(json.load(open(a)))), dict(leaves(json.load(open(b))))
if A.keys() != B.keys():
    print('different structure:', sorted(set(A) ^ set(B))[:5]); sys.exit(1)
worst, where = 0.0, None
for k, va in A.items():
    vb = B[k]
    if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
        d = abs(va - vb)
        if d > 2e-5 and d > 1e-5 * max(abs(va), abs(vb)):
            print(f'differ at {k}: {va} vs {vb}'); sys.exit(1)
        if d > worst: worst, where = d, k
    elif va != vb:
        print(f'differ at {k}: {va!r} vs {vb!r}'); sys.exit(1)
print(f'same numbers (largest difference {worst:.1e} at {where})')
