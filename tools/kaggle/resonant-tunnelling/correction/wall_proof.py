"""Fig. 15 correction, walls: rebuild a few wall runs exactly and prove each rebuilt file three ways (not filed).

For each run:
  stored   : the numbers written into the rebuilt RT3C file (header T_ref; curves; 8-bit levels with each frame's peak);
  recomputed from stored inputs : T from the coordinator's independent transfer-matrix code (mytm.packet_T, spectrum |G|^2) and
             from the file's own curves at the last frame (P_right + P_well / 2, whole line); |psi| at the brightest point of three
             frames recomputed from the spec alone (exact_wall, a fresh instance at that one point);
  read back: the level at that point decoded as the page's worker decodes it (level / 255 * peak_f * peak0).
Usage: python3 wall_proof.py <out dir> <file> ...
"""
import os, sys, json, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "notes", "fig15", "coordinator"))
import read_rt3d, exact_wall as ew, rebuild_wall as rw, mytm
from wall_curves import fetch, BY


def main(outdir, names):
    os.makedirs(outdir, exist_ok=True); rep = []
    for name in names:
        parent = fetch(name); h, amp, ph, prof, p1 = read_rt3d.read(parent)
        slab, pr, pr1, curves, cn, X, extra = rw.from_exact(h)
        head = dict(method="exact: psi = chi(x,t) h(y,t) h(z,t); chi by superposition of the stationary scattering states "
                    "(tools/kaggle/resonant-tunnelling/correction/exact_wall.py); no time grid, no barrier sampling",
                    parent=dict(file=name, sha256=BY[name]["sha256"]), T_ref=X.T_inf, carried=X.carried,
                    regions="left, right: inside the box |x| <= box half-length (norm = what is in the box); "
                            "left_line, right_line: whole line", device="cpu (exact)", wall=None,
                    closure_max=float(np.abs(extra["closure"] - 1).max()),
                    extra_curves=dict(left_line=np.round(extra["left_line"], 7).tolist(), right_line=np.round(extra["right_line"], 7).tolist()))
        blob, A, P, peaks = rw.write(h, slab, pr, pr1, curves, cn, head)
        open(os.path.join(outdir, name), "wb").write(blob)
        H, a2, p2, pf2, q2 = read_rt3d.read(blob)                       # read the file back as written
        c = np.array(H["curves"]); C = {n: c[:, i] for i, n in enumerate(H["curve_names"])}
        well_end = C["well"][-1] if "well" in C else 0.0
        T_curves = H["extra_curves"]["right_line"][-1] + 0.5 * well_end
        sp = H["spec"]; t = np.arange(H["n"]) * H["frame_dt"]
        pts = []
        for f in (H["n"] // 5, H["n"] // 2, H["n"] - 1):
            i, j = np.unravel_index(np.argmax(a2[f]), a2[f].shape)
            xpt = H["x_first"] + i * H["step"]; ypt = j * H["step"]
            Y = ew.Exact(sp, np.array([xpt]))
            chi = Y.chi(np.array([t[f]]))[0, 0]
            hy = ew.h_free(np.array([ypt, 0.0]), np.array([t[f]]), sp["sp"])[:, 0]
            exact_abs = abs(chi * hy[0] * hy[1])
            readback = a2[f, i, j] / 255 * H["peaks"][f] * H["peak0"]
            pts.append(dict(frame=f, t=round(float(t[f]), 3), x=xpt, y=ypt, level=int(a2[f, i, j]), readback=readback,
                            recomputed=exact_abs, rel=readback / exact_abs - 1))
        r = dict(file=name, sha256_rebuilt=hashlib.sha256(blob).hexdigest(), bytes=len(blob),
                 T_stored=H["T_ref"], T_mytm=mytm.packet_T(sp, nk=80001), T_from_curves=T_curves,
                 T_far_old=BY[name]["T_far"]["value"], T_twin_old=BY[name]["twin"]["T"], closure_max=H["closure_max"], points=pts)
        rep.append(r); print(json.dumps(r))
    json.dump(rep, open(os.path.join(outdir, "proof.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
