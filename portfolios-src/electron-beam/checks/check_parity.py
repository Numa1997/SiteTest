#!/usr/bin/env python3
"""Parity of the browser physics and the Python reference.

    python3 portfolios-src/electron-beam/checks/check_parity.py

1. Constants: every value of physics/core.js (C, D, U) against ref/core.py, relative difference at most 1e-15.
2. The number formatter: core.js fmt against ref/core.py fmt on a fixed list, identical strings.
3. Each physics/chNN.js against ref/chNN.py on the module's own `cases` (missing inputs take the contract defaults), every output
   within the module's stated `tolerance` {rel, abs}: |js - py| <= abs + rel * max(|js|, |py|). Arrays are compared element by element.
   Chapters 1, 2, 4, 5, 6 and 7 must have a reference (PLAN.md section 4); chapters 3 and 8 may not and are reported as such.
Both sides run in float64. A gap larger than rounding is a bug in one of the two; a gap that is a deliberate model difference
(float32 arrays, a different quadrature) must be named in the module's `tolerance.note` and stated on the page.
"""
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import eb_lib as L  # noqa: E402
from ref import core as rc  # noqa: E402

REQUIRED_REF = {'ch01', 'ch02', 'ch04', 'ch05', 'ch06', 'ch07'}
FMT_VALUES = [1, 3.14159, 0.001, 0.00099999, 12345.6, 99999.5, 123456, 9.999e-4, 3.70144e-12, 6.02214076e23, 1.0e-9, 0.5, 100, 99.95, 2.5e-11, -4.55, 7.2898e-19]
ok = True


def say(good, msg):
    global ok
    ok &= good
    print(('PASS ' if good else 'FAIL ') + msg)


def close(a, b, tol):
    return abs(a - b) <= tol.get('abs', 0) + tol.get('rel', 0) * max(abs(a), abs(b))


# 1. constants
js = L.node('core')
worst = 0.0
bad = []
for group, py in (('C', rc.C), ('D', rc.D), ('U', rc.U)):
    for k, v in js[group].items():
        if k not in py:
            bad.append('%s.%s missing in ref/core.py' % (group, k))
            continue
        d = abs(v - py[k]) / abs(v)
        worst = max(worst, d)
        if d > 1e-15:
            bad.append('%s.%s: js %r, py %r' % (group, k, v, py[k]))
    for k in py:
        if k not in js[group]:
            bad.append('%s.%s missing in core.js' % (group, k))
say(not bad, 'constants core.js = ref/core.py, %d values, largest relative difference %.1e %s' % (sum(len(js[g]) for g in js), worst, '; '.join(bad)))

# 2. formatter
jf = L.node('fmt', [[x, s] for x in FMT_VALUES for s in (2, 3, 4)])
pf = [rc.fmt(x, s) for x in FMT_VALUES for s in (2, 3, 4)]
diff = [(a, b) for a, b in zip(jf, pf) if a != b]
say(not diff, 'number formatter core.js = ref/core.py on %d cases %s' % (len(pf), diff[:3]))

# 3. modules
modules = L.node('modules')
contract = L.load_contract()
bad_contract = L.check_contract(contract, modules)
say(not bad_contract, 'contract agrees with %d physics module(s) %s' % (len(modules), bad_contract[:3]))
import importlib  # noqa: E402
for m in modules:
    mid = m['id']
    try:
        ref = importlib.import_module('ref.' + mid)
    except ModuleNotFoundError:
        say(mid not in REQUIRED_REF, '%s: no ref/%s.py%s' % (mid, mid, ' (required)' if mid in REQUIRED_REF else ' (not required for this chapter)'))
        continue
    tol = m.get('tolerance')
    if not tol:
        say(False, '%s: the physics module states no tolerance' % mid)
        continue
    cases = m['cases'] or [{}]
    res = L.node('compute', [{'module': mid, 'inputs': c} for c in cases])
    worst, msgs = 0.0, []
    for c, r in zip(cases, res):
        if 'error' in r:
            msgs.append('js error %s' % r['error'])
            continue
        p = r['inputs']
        py = ref.compute(p)
        if sorted(py) != sorted(m['outputs']) or sorted(r['outputs']) != sorted(m['outputs']):
            msgs.append('output names differ: js %s, py %s, declared %s' % (sorted(r['outputs']), sorted(py), sorted(m['outputs'])))
            continue
        for k in m['outputs']:
            a, b = r['outputs'][k], py[k]
            pairs = list(zip(a, b)) if isinstance(a, list) else [(a, b)]
            if isinstance(a, list) and len(a) != len(b):
                msgs.append('%s: length %d vs %d' % (k, len(a), len(b)))
                continue
            for x, y in pairs:
                if not close(x, y, tol):
                    msgs.append('%s on %s: js %r, py %r' % (k, c, x, y))
                    break
                if max(abs(x), abs(y)) > 0:
                    worst = max(worst, abs(x - y) / max(abs(x), abs(y)))
    say(not msgs, '%s: js = py on %d case(s), %d outputs, largest relative difference %.1e (stated tolerance rel %g, abs %g)%s %s' % (
        mid, len(cases), len(m['outputs']), worst, tol.get('rel', 0), tol.get('abs', 0), (' note: ' + tol['note']) if tol.get('note') else '', '; '.join(msgs[:3])))
print('PARITY CHECK', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
