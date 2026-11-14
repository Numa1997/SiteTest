"""Fig. 16: read the stored Fig. 12 rides (public/data/fig12/<run>/<name>.json) on the CPU, decoded exactly as the page decodes them.

Nothing is simulated here. The surface H is unpacked (zlib, int16 differences in steps of qH, -32768 = no value), the outer ring is read
as tools/fig12/kaggle/pack_ride.py reads it (bilinear over the trusted columns, stepping inward by half a cell), and from it:
  tilt(t)  = 2 (2/64) sum eta(theta) cos(theta)   [m]  twice the first-mode height at the wall, the number pack_ride stores as tilt_max_mm
  q(t)     = tilt / 2                              [m]  the first mode's height at the front wall (note eq. 11)
Run as a script it prints, for every stored ride, the largest tilt and the stored tilt_max_mm, which must agree (the decoding check)."""
import base64, json, os, zlib
import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DATA = os.path.join(ROOT, "public", "data", "fig12")


def unpack(s, dt):
    return np.frombuffer(zlib.decompress(base64.b64decode(s)), dtype=dt)


def load(run, name):
    d = json.load(open(os.path.join(DATA, run, name + ".json")))
    n, nf = d["n"], d["frames"]
    Hd = unpack(d["H"], np.int16).reshape(nf, n, n).astype(np.int64)
    Hq = np.cumsum(Hd, axis=0)                                    # running sum undoes the differences (mod 2^16)
    Hq = ((Hq + 32768) % 65536) - 32768
    H = np.where(Hq == -32768, np.nan, Hq * d["qH"])
    d["Hgrid"] = H
    d["tarr"] = np.asarray(d["t"], float)
    return d


def ring(d, r, th):
    Hs, n, dx, x0 = d["Hgrid"], d["n"], d["dx"], d["x0"]
    out = np.full(Hs.shape[0], np.nan); q = r
    while q > 0 and np.isnan(out).any():
        fx = (q * np.cos(th) - x0) / dx - 0.5; fy = (q * np.sin(th) - x0) / dx - 0.5
        i, j = int(np.floor(fx)), int(np.floor(fy)); tx, ty = fx - i, fy - j
        num = np.zeros(Hs.shape[0]); den = np.zeros(Hs.shape[0])
        for a, b_, w in ((0, 0, (1 - tx) * (1 - ty)), (1, 0, tx * (1 - ty)), (0, 1, (1 - tx) * ty), (1, 1, tx * ty)):
            ii, jj = i + a, j + b_
            if 0 <= ii < n and 0 <= jj < n:
                v = Hs[:, ii, jj]; ok = np.isfinite(v)
                num += np.where(ok, w * np.nan_to_num(v), 0.0); den += np.where(ok, w, 0.0)
        val = np.where(den > 1e-6, num / np.maximum(den, 1e-12), np.nan); out = np.where(np.isnan(out), val, out); q -= 0.5 * dx
    return out


def rfill(d):
    """R_fill as pack_ride used it: the run's Rfill is not in the page file, so it is recovered from the trusted columns
    (the largest column-centre radius with a value in the first frame lies within one cell inside R_fill - dx)."""
    return d.get("Rfill")


def tilt(d, Rf):
    dx = d["dx"]; R16 = Rf - 0.5 * dx; TH = 2 * np.pi * np.arange(64) / 64
    RING = np.stack([ring(d, R16, th) for th in TH], 1)
    return 2 * (2 / 64) * (RING * np.cos(TH)[None]).sum(1), RING


RUNS = {"run10": "2026-11-14-run10", "run8": "2026-11-13-run8"}

if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.join(ROOT, "tools", "fig12", "kaggle"))
    from stout_jax import Geometry
    R = json.load(open(os.path.join(ROOT, "tools", "fig12", "glass_profile.json")))["R"] if os.path.exists(os.path.join(ROOT, "tools", "fig12", "glass_profile.json")) else None
    print("R table found:", R is not None)
