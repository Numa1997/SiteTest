"""First measurement of Step B1 on three stored flat-wall runs, with the error split into its sources.

  A  solver + method: the same solver (flat.py) rerun here, unquantized, on its own fine grid (dx = 0.05) over the whole line
  B  + the stored window (x = -32 ... 31.5) and its 0.5 a spacing: the rerun sampled at the stored points
  C  + the 8-bit levels: the stored file itself, axis rho = 0 only
  D  the stored file, every rho column combined (least squares; chi = psi / (g(rho) g(0)) in each column)
Reference: exact t(k), r(k) from the four matching equations (exact_tr). Band: |phi(k)|^2 >= 1 % of its peak.
Also: the rerun, quantized as build_flat.py does, compared level by level with the stored file (reproducibility).
Usage: python3 b1_first.py [out.json]
"""
import json, sys, os, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, "tools/kaggle/schrodinger-shapes"))
from extract_t import read_sphc, exact_tr, extract, chi_from_cut, decode, phi, g0, S0
from flat import run

FLAT = os.path.join(ROOT, "public/data/schrodinger-sphere/2026-11-12/flat/")
CASES = [("e1_v8_a1.bin", "running example: E = 1, V0 = 3, a = 1"),
         ("e3_v8_a1.bin", "E = 2, V0 = 3, a = 1"),
         ("e7_v7_a3.bin", "E = 4 above V0 = 2, a = 3")]


def stats(te, tx, re, rx):
    d2 = np.abs(te)**2 - np.abs(tx)**2
    dph = np.angle(te / tx)
    dr2 = np.abs(re)**2 - np.abs(rx)**2
    dphr = np.angle(re / rx)
    return dict(T_abs_max=float(np.max(np.abs(d2))), T_abs_rms=float(np.sqrt(np.mean(d2**2))),
                T_rel_max=float(np.max(np.abs(d2) / np.abs(tx)**2)),
                phase_t_max=float(np.max(np.abs(dph))), phase_t_rms=float(np.sqrt(np.mean(dph**2))),
                R_abs_max=float(np.max(np.abs(dr2))), phase_r_max=float(np.max(np.abs(dphr))))


out = []
for name, what in CASES:
    h, curves, qa, qp = read_sphc(FLAT + name)
    E, V0, a = h["E"], h["V0"], h["a"]; k0 = np.sqrt(2 * E)
    f = h["n"] - 1; t = curves[f, 0]
    k = np.linspace(k0 - 0.506, k0 + 0.506, 81)        # |phi|^2 >= 1 % of peak
    tx, rx = exact_tr(k, V0, a)
    T0 = time.time(); R = run(E, V0, a); wall = time.time() - T0
    # A: fine grid, whole line, unquantized
    x = R["x"]; tA, rA = extract(x, R["chi_end"], t, k, k0, a, R["dx"])
    # B: the rerun at the stored points (x = -32 + 0.5 i), unquantized, axis rho = 0
    xv = -32.0 + 0.5 * np.arange(128); rho = 0.5 * np.arange(64)
    chiB = R["plane"][f][:, 0] / (g0(0.0, t) * g0(0.0, t))
    tB, rB = extract(xv, chiB, t, k, k0, a, 0.5)
    # reproducibility: quantize the rerun as build_flat.py does and compare with the stored levels
    pl = R["plane"]; amp = np.abs(pl); ph = np.angle(pl); a0r = amp[0].max()
    qa2 = np.clip(np.round(255 * amp / a0r), 0, 255).astype(np.uint8)
    qp2 = (np.round((ph + np.pi) / (2 * np.pi) * 255) % 256).astype(np.uint8); qp2[qa2 < 3] = 0
    same_a = float(np.mean(qa2 == qa)); same_p = float(np.mean(qp2 == qp))
    dqa = int(np.max(np.abs(qa2.astype(int) - qa)));
    # C, D: the stored file
    ampS, phS, ampM, a0 = decode(qa, qp, f, E)
    chiC = chi_from_cut(ampS, phS, t, rho, "axis")
    tC, rC = extract(xv, chiC, t, k, k0, a, 0.5)
    chiD = chi_from_cut(ampM, phS, t, rho, "all")
    tD, rD = extract(xv, chiD, t, k, k0, a, 0.5)
    # how much of the transmitted / reflected packet is inside the stored window at this frame (from the fine rerun)
    p = np.abs(R["chi_end"])**2; dxf = R["dx"]
    inT = p[(x > a / 2) & (x < 31.75)].sum() * dxf / p[x > a / 2].sum() / dxf
    inR = p[(x < -a / 2) & (x >= -32.25)].sum() * dxf / max(p[x < -a / 2].sum() * dxf, 1e-300)
    row = dict(file=name, what=what, E=E, V0=V0, a=a, frame=f, t=t, a0_header_free=a0, a0_rerun=float(a0r),
               levels_identical_amp=same_a, levels_identical_phase=same_p, largest_amp_level_diff=dqa,
               rerun_seconds=round(wall, 1), window_holds_T=float(inT), window_holds_R=float(inR),
               T_k0_exact=float(np.abs(exact_tr(k0, V0, a)[0][0])**2),
               A=stats(tA, tx, rA, rx), B=stats(tB, tx, rB, rx), C=stats(tC, tx, rC, rx), D=stats(tD, tx, rD, rx),
               curve=dict(k=k.tolist(), T_exact=(np.abs(tx)**2).tolist(), T_C=(np.abs(tC)**2).tolist(), T_D=(np.abs(tD)**2).tolist(),
                          dphase_C=np.angle(tC / tx).tolist(), dphase_D=np.angle(tD / tx).tolist()))
    out.append(row)
    print(f"\n{name} ({what}); frame {f}, t = {t}; rerun {wall:.1f} s; window holds {inT:.5f} of T, {inR:.5f} of R")
    print(f"  stored levels reproduced: amplitude {same_a*100:.3f} % identical (largest diff {dqa}), phase {same_p*100:.3f} %; "
          f"a0 assumed {a0:.6g}, rerun {a0r:.6g}")
    print(f"  |t(k0)|^2 exact {row['T_k0_exact']:.5f}")
    for key in "ABCD":
        s = row[key]
        print(f"  {key}: |t|^2 err max {s['T_abs_max']:.2e} (rel {s['T_rel_max']:.2e}), rms {s['T_abs_rms']:.2e}; "
              f"phase t max {s['phase_t_max']:.2e} rad; |r|^2 err max {s['R_abs_max']:.2e}; phase r max {s['phase_r_max']:.2e}")
if len(sys.argv) > 1:
    json.dump(out, open(sys.argv[1], "w"), indent=1)
