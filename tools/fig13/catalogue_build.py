"""Fig. 13: write public/scripts/fig13-catalogue-data.js, the catalogue of closed drawings.

Inputs: the orbits pinned by closed_pin.py (JSON: strike, period, turns, closure error) and the 14 orbits of the flower hunt
(public/scripts/fig13-hunt-data.js). Kept: closure error below 1e-3 after one lap; one of each mirror pair (the mirror drawing has
the strike and both turn numbers reversed, so it is turned to n1 > 0, or n2 > 0 when n1 = 0); distinct (n1, n2, period to 0.01 s).
Added to each: total energy and the stability index s = trace of the lap's monodromy - 2 (closed_stability.index; |s| < 2 stable).

Usage: python3 tools/fig13/catalogue_build.py PINNED.json
"""
import sys, os, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import closed_stability as st

pinned = json.load(open(sys.argv[1]))
t = open(os.path.join(HERE, '../../public/scripts/fig13-hunt-data.js')).read(); hunt = json.loads(t[t.index('{'):t.rindex('}') + 1])['garden']
seen, out = set(), []


def add(p1, p2, T, n1, n2, src):
    if n1 < 0 or (n1 == 0 and n2 < 0):
        p1, p2, n1, n2 = -p1, -p2, -n1, -n2
    key = (n1, n2, round(T, 2))
    if key in seen:
        return
    seen.add(key)
    s = float(st.index(p1, p2, T, st.A, st.B, st.C, st.U1, st.U2))
    E = (st.B * p1 * p1 - 2 * st.C * p1 * p2 + st.A * p2 * p2) / (2 * (st.A * st.B - st.C * st.C)) - st.U1 - st.U2
    out.append([round(p1, 10), round(p2, 10), round(T, 9), n1, n2, round(E, 2), round(s, 4), 1 if src == 'hunt' else 0])


for h in hunt:
    q = st.flow(np.array([0., 0., h['p1'], h['p2']]), h['period'], st.A, st.B, st.C, st.U1, st.U2)
    add(h['p1'], h['p2'], h['period'], round(q[0] / (2 * math.pi)), round(q[1] / (2 * math.pi)), 'hunt')
for g in pinned:
    if g['err'] < 1e-3:
        add(g['p1'], g['p2'], g['T'], g['n1'], g['n2'], 'map')
out.sort(key=lambda o: o[5])
dest = os.path.join(HERE, '../../public/scripts/fig13-catalogue-data.js')
open(dest, 'w').write(
    "// Fig. 13: the catalogue of closed drawings. Written by tools/fig13/catalogue_build.py; do not edit by hand.\n"
    "// Each row: strike p1, p2 (kg m^2/s, from hanging still), period T (s), turns per lap of the upper and lower rod n1, n2,\n"
    "// total energy E (J; hanging still is -19.6), stability index s = trace of the lap's monodromy - 2 (|s| < 2 stable), 1 if from the flower hunt.\n"
    "window.FIG13_CATALOGUE = " + json.dumps(out, separators=(',', ':')) + ";\n")
print('wrote', dest, len(out), 'orbits')
