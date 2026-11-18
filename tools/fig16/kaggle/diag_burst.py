"""Fig. 16 on Kaggle's CPU: the burst in seed 1 of the controlled kerb (audit M3). Reads the packed ride (public/data/fig16/<DATE>/
<RIDE>.json from the repository at COMMIT), decodes the stored surface as StoutRide does (base64, deflate, int16 differences summed),
recomputes the two level probes exactly as stout_jax.Stout.probes reads them (bilinear over the columns with a surface, extended
straight from r1 = R - 2.5 dx and r2 = r1 - 1.5 dx to the wall), compares with the stored probe reading yq, and lists, for every
frame where yq jumps by more than JUMP_MM, which of the probes' 16 columns changed and by how much. Writes diag_burst.log.
Environment: COMMIT, RIDE (default kerb_full), DATE (default 2026-11-15), JUMP_MM (default 0.25)."""
import base64, json, os, urllib.request, zlib
import numpy as np

C = os.environ["COMMIT"]; RIDE = os.environ.get("RIDE", "kerb_full"); DATE = os.environ.get("DATE", "2026-11-15")
JUMP = float(os.environ.get("JUMP_MM", "0.25")) * 1e-3
LOG = open("/kaggle/working/diag_burst.log", "w")
def log(m): print(m, flush=True); LOG.write(m + "\n")

D = json.loads(urllib.request.urlopen(f"https://raw.githubusercontent.com/Numa1997/SiteTest/{C}/public/data/fig16/{DATE}/{RIDE}.json").read())
js = urllib.request.urlopen(f"https://raw.githubusercontent.com/Numa1997/SiteTest/{C}/public/scripts/guinness-glass.js").read().decode()
import re
R = np.array(json.loads(re.search(r"R:\s*(\[[^\]]*\])", js).group(1))); DZP = 0.0005
n, nf, dx, x0, fill, qH = D["n"], D["frames"], D["dx"], D["x0"], D["fill"], D["qH"]
Hd = np.frombuffer(zlib.decompress(base64.b64decode(D["H"])), np.int16).reshape(nf, n, n).astype(np.int32)
H = np.empty_like(Hd)
H[0] = Hd[0]
for k in range(1, nf): H[k] = ((Hd[k] + H[k - 1]) + 32768) % 65536 - 32768      # the running sum in int16, as StoutRide
Hm = np.where(H == -32768, np.nan, H * qH)                                       # m; NaN where the column stored no surface
Rfill = float(np.interp(fill / DZP, np.arange(len(R)), R))
r = Rfill; r1 = r - 2.5 * dx; r2 = r1 - 1.5 * dx


def bil(Hk, x, y):
    fx = (x - x0) / dx - 0.5; fy = (y - x0) / dx - 0.5
    i = int(np.clip(np.floor(fx), 0, n - 2)); j = int(np.clip(np.floor(fy), 0, n - 2)); tx, ty = fx - i, fy - j
    cols = [((1 - tx) * (1 - ty), i, j), (tx * (1 - ty), i + 1, j), ((1 - tx) * ty, i, j + 1), (tx * ty, i + 1, j + 1)]
    num = sum(w * Hk[a, b] for w, a, b in cols if np.isfinite(Hk[a, b])); den = sum(w for w, a, b in cols if np.isfinite(Hk[a, b]))
    return (num / den if den > 1e-9 else np.nan), [(a, b, w) for w, a, b in cols]


def probe(Hk):
    out, cols = [], []
    for s in (1.0, -1.0):
        h1, c1 = bil(Hk, s * r1, 0.0); h2, c2 = bil(Hk, s * r2, 0.0); out.append(h1 + (r - r1) * (h1 - h2) / (r1 - r2)); cols += c1 + c2
    return 0.5 * (out[0] - out[1]), cols


t = np.array(D["t"]); yq = np.array(D["yq"]); rec = np.array([probe(Hm[k])[0] for k in range(nf)])
log(f"{RIDE}: {nf} frames, dx {dx * 1e3:.2f} mm, R(fill) {Rfill * 1e3:.2f} mm, r1 {r1 * 1e3:.2f} mm, r2 {r2 * 1e3:.2f} mm")
log(f"stored yq vs recomputed from the stored (rounded, trusted) columns: rms {np.sqrt(np.nanmean((yq - rec) ** 2)) * 1e3:.3f} mm, "
    f"max {np.nanmax(np.abs(yq - rec)) * 1e3:.3f} mm")
_, cols = probe(Hm[0]); cols = sorted({(a, b) for a, b, w in cols})
for k in range(1, nf):
    if abs(yq[k] - yq[k - 1]) > JUMP:
        ch = [(a, b, (Hm[k, a, b] - Hm[k - 1, a, b]) * 1e3) for a, b in cols]
        big = sorted(ch, key=lambda c: -abs(np.nan_to_num(c[2], nan=99)))[:4]
        nans = [(a, b) for a, b in cols if np.isnan(Hm[k, a, b]) != np.isnan(Hm[k - 1, a, b])]
        log(f"t {t[k]:.3f} s: yq {yq[k - 1] * 1e3:+.3f} -> {yq[k] * 1e3:+.3f} mm (recomputed {rec[k - 1] * 1e3:+.3f} -> {rec[k] * 1e3:+.3f}); "
            f"largest column changes (i, j, mm): {[(a, b, round(float(c), 3)) for a, b, c in big]}; columns gaining or losing a surface: {nans}")
# the surface's own motion at the probes for scale: first-mode height at the wall from the ring, per frame
log("done")
