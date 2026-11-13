"""Reads Fig. 15's 3D run files ('RT3C', written by rt3d_run.py on Kaggle) and prints the checks of each run.
Usage: python3 read_rt3d.py <file.bin | folder | rt3d.tar> ..."""
import json, struct, zlib, sys, os, tarfile, io
import numpy as np


def read(blob):
    assert blob[:4] == b"RT3C", "not an RT3C file"
    H = struct.unpack("<I", blob[4:8])[0]
    h = json.loads(blob[8:8 + H])
    raw = zlib.decompress(blob[8 + H:])
    n, nxs, nr, nx = h["n"], h["nxs"], h["nr"], h["prof_nx"]
    a = n * nxs * nr
    amp = np.frombuffer(raw, np.uint8, a, 0).reshape(n, nxs, nr)
    phase = np.frombuffer(raw, np.uint8, a, a).reshape(n, nxs, nr)
    prof = np.frombuffer(raw, np.float32, n * nx, 2 * a).reshape(n, nx)
    prof1d = np.frombuffer(raw, np.float32, n * nx, 2 * a + 4 * n * nx).reshape(n, nx) if h.get("has_1d") else None
    return h, amp, phase, prof, prof1d


def blobs(paths):
    for p in paths:
        if p.endswith(".tar"):
            with tarfile.open(p) as tf:
                for m in tf.getmembers():
                    if m.name.endswith(".bin"): yield m.name, tf.extractfile(m).read()
        elif os.path.isdir(p):
            for f in sorted(os.listdir(p)):
                if f.endswith(".bin"): yield f, open(os.path.join(p, f), "rb").read()
        else:
            yield os.path.basename(p), open(p, "rb").read()


if __name__ == "__main__":
    for name, b in blobs(sys.argv[1:]):
        h, amp, ph, prof, p1 = read(b)
        c = dict(zip(h["curve_names"], h["curves"][-1]))
        ns = h["wall"] / h["steps"] / np.prod(h["box"]) * 1e9
        line = (f"{name}: {h['steps']} steps, {h['wall']:.1f} s on {h['device']} ({ns:.2f} ns per cell-step); start in barrier "
                f"{h['start_in_barrier']:.1e}, in border {h['start_in_border']:.1e}; end {json.dumps({k: round(v, 5) for k, v in c.items()})}")
        if p1 is not None:
            line += (f"; 3D vs 1D twin {h['sep_check_max']:.1e}; transmitted: 1D split-step {h['T_1d_splitstep']:.4f}, "
                     f"exact {h['T_packet_exact']:.4f}")
        print(line)
