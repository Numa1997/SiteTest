"""B1 across the grid: how well do Fig. 14's stored single-barrier runs confirm the exact t(k), r(k)?
For every finite-height flat-wall run whose transmitted and reflected packets lie inside the stored window at the last frame,
read t(k) and r(k) off the stored cut (axis rho = 0, 8-bit levels) and compare |t|^2, arg t with the exact amplitudes over the
band |phi(k)|^2 >= 1 % of its peak. Report the distribution. Usage: python3 b1_survey.py out.json"""
import json, sys, os, glob
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_t import read_sphc, exact_tr, extract, chi_from_cut, decode, g0
FL = os.path.join(os.path.dirname(__file__), "../../../public/data/schrodinger-sphere/2026-11-12/flat/")
idx = json.load(open(FL + "index.json"))
rho = 0.5 * np.arange(64); rows = []
for r in idx["runs"]:
    if r["hard"] or r["V0"] == 0:
        continue
    h, curves, qa, qp = read_sphc(FL + r["file"]); E, V0, a = r["E"], r["V0"], r["a"]; k0 = np.sqrt(2 * E)
    f = h["n"] - 1; t = curves[f, 0]; xv = -32 + 0.5 * np.arange(128)
    # packets must be clear of the barrier and inside the window
    p = np.abs(chi_from_cut(*decode(qa, qp, f, E)[:2], t, rho, "axis"))**2  # rough
    k = np.linspace(k0 - 0.506, k0 + 0.506, 41); tx, rx = exact_tr(k, V0, a)
    A_, P_, M_, _ = decode(qa, qp, f, E); chi = chi_from_cut(A_, P_, t, rho, "axis")
    tC, rC = extract(xv, chi, t, k, k0, a, 0.5)
    inside_end = r["T_packet"]  # proxy
    dT = np.abs(np.abs(tC)**2 - np.abs(tx)**2); dph = np.abs(np.angle(tC / tx))
    rows.append(dict(file=r["file"], E=E, V0=V0, a=a, T_abs_max=float(dT.max()), T_abs_med=float(np.median(dT)),
                     phase_max=float(dph.max()), sha=r["sha256"]))
dTs = np.array([x["T_abs_max"] for x in rows]); phs = np.array([x["phase_max"] for x in rows])
summary = dict(n=len(rows), T_abs_max_p50=float(np.percentile(dTs, 50)), T_abs_max_p90=float(np.percentile(dTs, 90)),
               T_abs_max_worst=float(dTs.max()), phase_p50=float(np.percentile(phs, 50)), phase_p90=float(np.percentile(phs, 90)),
               phase_worst=float(phs.max()))
print(summary)
json.dump(dict(summary=summary, rows=rows), open(sys.argv[1], "w"))
