"""Fig. 1, Wave interference, generation 2: the reference model behind `simulations/Circular Wave Interference Visualization.html`.

Why a second model. The first (`wave_interference.py`) stored a ring for every whole wavelength, 16, 17, ..., 64 px, and every damping
0, 0.05, ..., 0.60, and the page showed the nearest. Measured on 23 November 2026: between two whole wavelengths the picture was off by
up to 0.65 (at lambda = 30.5 px, 89 % of the points a wrong colour), and during a wavelength sweep on the live site 51 % of the frames
still showed an older wavelength while the next file downloaded. This model makes the wavelength and the damping continuous again.

The setup (as in the first model). A still pond seen from above, a field W wide. Floats on one straight line, a height h_s above the
near edge, all bobbing together at one frequency f. Each sends out a ring; where rings meet, their heights add. One ring (note eq. 5),
at distance r from its source:

    psi_s(r, t) = a(r) cos(k r - omega t),   k = 2 pi / lambda,   omega = 2 pi f,   a(r) = exp(-gamma r / R)               (1)
    psi = (1/N) sum_s a(r_s) cos(k r_s - omega t) = C cos(omega t) + S sin(omega t)                                          (2)

Fixed grid (as before): cells DX across and up, source places DX/2 apart, so every distance from a source place to a cell is one entry
r(j, m) of one table, m = |2i + 1 - q|, j counted up from the near edge.

What is new: nodes evenly spaced in k, not in lambda. The angle of a ring, k r, grows in proportion to k. So between two neighbouring
nodes k_n and k_n+1 the angle at any distance is EXACTLY the straight-line blend of the two stored angles,

    k r = (1 - t) k_n r + t k_n+1 r,   t = (k - k_n) / (k_n+1 - k_n),                                                         (3)

provided the two stored angles, each reduced to one turn, can be put back together without doubt: their difference must stay below
half a turn at every distance. With the largest distance r_max on the grid, that asks (k_n+1 - k_n) r_max < pi; the model keeps it
below 0.9 pi, which fixes the number of nodes. The page blends the two stored angles (the difference taken the short way round),
so every wavelength from 16 to 64 px is shown as computed here, up to the rounding of the stored numbers.

The height a = exp(-gamma r / R) is stored at gamma = 0, 0.025, ..., 0.6; between two nodes the page blends the two heights in a
straight line. That is not exact: the largest error is (d gamma)^2 (r/R)^2 / 8 at gamma = 0, measured here and stored with the data.

Units. SI in the parameters below; nothing depends on the absolute scale, only on k r and gamma r / R. The page counts lengths in px of
a field always 800 px wide, so the tables use that unit: 1 px = W / 800 = PX_M m.

Method: closed form, evaluated in float64 by NumPy, then rounded for storage (no integration, so no tolerances):
    angle -> uint16, one count = 2 pi / 65536 rad      height -> uint16, one count = 1 / 65535
    cosine -> int16, one count = 1 / 32767            distance -> float32, px

Files (each: 4 bytes of label b"WIF2", uint32 header length, a JSON header padded with spaces to a multiple of 4 bytes, then the
little-endian array). Every table is split into its bottom half (rows 0 ... 124, file *_lo) and top half (rows 125 ... 249, *_hi):
a wide screen shows only the bottom 113 rows, so it downloads half.
    geometry.bin           header: every parameter, the node lists, the checks; then the cosine table int16 [65536]
    dist_lo.bin, dist_hi.bin                 r(j, m) float32 [125 x 500] px
    ring_k<NNN>_lo.bin, ring_k<NNN>_hi.bin   angle of a ring at node k_NNN, uint16 [125 x 500]
    damp_g<NNN>_lo.bin, damp_g<NNN>_hi.bin   height of a ring at gamma = NNN / 1000, uint16 [125 x 500]
    wave_interference2.json                  the geometry header again, readable

Checks written into the output (geometry header and wave_interference2.json):
  - blend safety: the largest difference between the stored angles of neighbouring nodes, taken the short way round, in turns;
    it must stay below one half;
  - comparison with the exact field: the page's sum (computed here exactly as the page computes it: the blend of (3), the height
    blend, float32 sums) against the float64 sum straight from (1)-(2), for the presets Reset and Line of 16, at every wavelength the
    slider can take (16.0, 16.1, ..., 64.0 px) at a damping node and halfway between two, and at every damping the slider can take
    (0, 0.01, ..., 0.6) at lambda = 30 px; and the colour-table row drawn at 8 instants of one period;
  - a known limit: two sources at gamma = 0, the amplitude must be |cos(k (r_1 - r_2) / 2)|, at every slider wavelength;
  - a conserved quantity: cos^2 + sin^2 = 1 in the stored cosine table;
  - rounding: the largest error of each stored angle and height against its exact value.
Usage: python3 wave_interference2.py [out_dir]"""
import json, math, os, struct, sys, time
import numpy as np

# ---- parameters (SI) ----
W = 0.40                 # m, width of the field (a ripple tank); the page draws it 800 px wide
PX_M = W / 800           # m per px of the field: 0.5 mm
R = 300 * PX_M           # m, damping length: a ring loses gamma factors of e over R (note eq. 5); 300 px
H_S = 10 * PX_M          # m, height of the source line above the near edge; 10 px
DX = 3.2 * PX_M          # m, size of a grid cell, across and up: 1.6 mm, 3.2 px
NI, NJ, NM, NQ = 250, 250, 500, 501      # cells across, cells up, values of m = |2i + 1 - q|, source places
HALF = 125               # rows in each half file
LAMBDA_MIN_PX, LAMBDA_MAX_PX, LAMBDA_STEP_PX = 16.0, 64.0, 0.1         # the wavelength slider
GAMMA_MAX, GAMMA_STEP, GAMMA_NODE = 0.6, 0.01, 0.025                     # the damping slider and the stored damping nodes
BLEND_BOUND = 0.9 * math.pi                                              # largest angle gap between neighbouring k nodes, rad
N_ANGLE, N_HEIGHT, N_COS = 65536, 65535, 32767
N_INSTANTS = 8           # instants of one period in the colour-row check

px = lambda metres: metres / PX_M

def geometry():
    j = np.arange(NJ)[:, None]; m = np.arange(NM)[None, :]
    return np.hypot(m * px(DX) / 2, (j + 0.5) * px(DX) - px(H_S))

def k_nodes(rmax):
    kmin, kmax = 2 * np.pi / LAMBDA_MAX_PX, 2 * np.pi / LAMBDA_MIN_PX
    n = int(math.ceil((kmax - kmin) * rmax / BLEND_BOUND)) + 1
    return [float(x) for x in np.linspace(kmin, kmax, n)]

def gamma_nodes():
    return [round(GAMMA_NODE * i, 3) for i in range(int(round(GAMMA_MAX / GAMMA_NODE)) + 1)]

def ring_counts(r, k):
    return (np.floor(np.mod(k * r / (2 * np.pi), 1.0) * N_ANGLE + 0.5).astype(np.int64) % N_ANGLE).astype(np.uint16)

def damp_counts(r, gamma):
    return np.floor(N_HEIGHT * np.exp(-gamma * r / px(R)) + 0.5).astype(np.uint16)

def cos_table():
    return np.floor(N_COS * np.cos(2 * np.pi * np.arange(N_ANGLE) / N_ANGLE) + 0.5).astype(np.int16)

def write(path, hdr, *arrays):
    hb = json.dumps(hdr, separators=(",", ":")).encode()
    hb += b" " * ((-(8 + len(hb))) % 4)
    with open(path, "wb") as f:
        f.write(b"WIF2"); f.write(struct.pack("<I", len(hb))); f.write(hb)
        for a in arrays: f.write(a.tobytes())

def presets():
    return {"reset": [125, 375], "line16": [40 + 28 * n for n in range(16)]}

# ---- the page's arithmetic, written out exactly as the page's JavaScript does it (float64, round = floor(x + 0.5), float32 sums) ----
def page_weights(lam, gamma, K, G):
    k = 2 * math.pi / lam; dk = K[1] - K[0]
    n = min(len(K) - 2, max(0, int(math.floor((k - K[0]) / dk + 1e-9)))); t = (k - K[n]) / dk
    g = min(len(G) - 2, max(0, int(math.floor(gamma / GAMMA_NODE + 1e-9)))); u = (gamma - G[g]) / GAMMA_NODE
    return n, t, g, u

def page_sum(q_list, A0, A1, t, H0, H1, u, TC):
    i = np.arange(NI)
    C = np.zeros((NJ, NI), np.float32); S = np.zeros((NJ, NI), np.float32); w = (1 / max(1, len(q_list))) / (N_HEIGHT * N_COS)
    for q in q_list:
        m = np.abs(2 * i + 1 - q)
        n0 = A0[:, m].astype(np.int64); d = ((A1[:, m].astype(np.int64) - n0 + 32768) & 65535) - 32768
        na = (n0 + np.floor(t * d + 0.5).astype(np.int64)) & 65535
        h0 = H0[:, m].astype(np.float64); h = h0 + u * (H1[:, m].astype(np.float64) - h0)
        C = (C.astype(np.float64) + h * TC[na] * w).astype(np.float32)
        S = (S.astype(np.float64) + h * TC[(na - 16384) & 65535] * w).astype(np.float32)
    return C, S

_R = {}
def exact_sum(q_list, lam, gamma):
    """C, S straight from (1)-(2) in float64, on the same grid: the field the page should show."""
    x = (np.arange(NI) + 0.5) * px(DX); y = (np.arange(NJ) + 0.5) * px(DX) - px(H_S)
    C = np.zeros((NJ, NI)); S = np.zeros((NJ, NI))
    for q in q_list:
        if q not in _R: _R[q] = np.hypot(x[None, :] - q * px(DX) / 2, y[:, None])
        r = _R[q]; a = np.exp(-gamma * r / px(R)) / len(q_list); ph = 2 * np.pi * r / lam
        C += a * np.cos(ph); S += a * np.sin(ph)
    return C, S

def row(psi):
    return np.floor(np.clip(psi, -1, 1) * 127.5 + 127.5 + 0.5)

def run(out_dir="."):
    t0 = time.time(); os.makedirs(out_dir, exist_ok=True)
    r = geometry(); rmax = float(r.max()); K = k_nodes(rmax); G = gamma_nodes(); TC = cos_table()
    RC = [ring_counts(r, k) for k in K]; DC = {g: damp_counts(r, g) for g in G}
    # ---- checks ----
    gap = max(int(np.max(np.abs(((RC[n + 1].astype(np.int64) - RC[n] + 32768) & 65535) - 32768))) for n in range(len(K) - 1)) / N_ANGLE
    err_angle = max(float(np.max(np.abs(np.angle(np.exp(1j * (2 * np.pi * RC[n] / N_ANGLE - K[n] * r)))))) for n in range(len(K)))
    err_height = max(float(np.max(np.abs(DC[g] / N_HEIGHT - np.exp(-g * r / px(R))))) for g in G)
    c = TC / N_COS; s = np.roll(TC, N_ANGLE // 4) / N_COS
    arrow = float(np.max(np.abs(c * c + s * s - 1)))
    wt = 2 * np.pi * np.arange(N_INSTANTS) / N_INSTANTS
    lams = [round(LAMBDA_MIN_PX + LAMBDA_STEP_PX * i, 1) for i in range(int(round((LAMBDA_MAX_PX - LAMBDA_MIN_PX) / LAMBDA_STEP_PX)) + 1)]
    gams = [round(GAMMA_STEP * i, 2) for i in range(int(round(GAMMA_MAX / GAMMA_STEP)) + 1)]
    cases = [(lam, 0.15) for lam in lams] + [(lam, 0.1625) for lam in lams] + [(30.0, g) for g in gams]
    worst = dict(C=0.0, S=0.0, psi=0.0); worst_at = {}; rows_differ = 0; cells = 0; row_diff_max = 0
    for name, ql in presets().items():
        for lam, g in cases:
            n, t, gi, u = page_weights(lam, g, K, G)
            Cp, Sp = page_sum(ql, RC[n], RC[n + 1], t, DC[G[gi]], DC[G[gi + 1]], u, TC); Ce, Se = exact_sum(ql, lam, g)
            dC, dS = float(np.max(np.abs(Cp - Ce))), float(np.max(np.abs(Sp - Se)))
            if dC > worst["C"]: worst["C"] = dC; worst_at["C"] = [name, lam, g]
            if dS > worst["S"]: worst["S"] = dS; worst_at["S"] = [name, lam, g]
            Pp = Cp[None].astype(np.float64) * np.cos(wt)[:, None, None] + Sp[None] * np.sin(wt)[:, None, None]
            Pe = Ce[None] * np.cos(wt)[:, None, None] + Se[None] * np.sin(wt)[:, None, None]
            worst["psi"] = max(worst["psi"], float(np.max(np.abs(Pp - Pe))))
            d = np.abs(row(Pp) - row(Pe)); rows_differ += int(np.count_nonzero(d)); row_diff_max = max(row_diff_max, int(d.max())); cells += d.size
    x = (np.arange(NI) + 0.5) * px(DX); y = (np.arange(NJ) + 0.5) * px(DX) - px(H_S)
    r1 = np.hypot(x[None, :] - 200, y[:, None]); r2 = np.hypot(x[None, :] - 600, y[:, None])
    limit = 0.0
    for lam in lams:
        n, t, gi, u = page_weights(lam, 0.0, K, G)
        Cp, Sp = page_sum([125, 375], RC[n], RC[n + 1], t, DC[G[gi]], DC[G[gi + 1]], u, TC)
        limit = max(limit, float(np.max(np.abs(np.hypot(Cp, Sp) - np.abs(np.cos(np.pi * (r1 - r2) / lam))))))
    xr = (r / px(R)); blend_bound = float(np.max(GAMMA_NODE ** 2 * xr ** 2 / 8))
    checks = dict(
        blend_largest_gap_turns=gap, blend_safe=gap < 0.5,
        compared_presets=presets(), slider_wavelengths=len(lams), slider_dampings=len(gams), cases_per_preset=len(cases), instants=N_INSTANTS,
        max_diff_C=worst["C"], max_diff_S=worst["S"], max_diff_psi=worst["psi"], worst_case=worst_at,
        colour_row_cell_instants=cells, colour_row_differ=rows_differ, colour_row_max_diff=row_diff_max,
        two_source_limit_max_diff=limit, arrow_length_max_diff=arrow, angle_max_err_rad=err_angle, height_max_err=err_height,
        height_blend_bound=blend_bound,
        rounding=dict(angle_rad=np.pi / N_ANGLE, height=0.5 / N_HEIGHT, cosine=0.5 / N_COS))
    # ---- files ----
    P = dict(W_m=W, px_m=PX_M, R_m=R, R_px=px(R), H_S_m=H_S, source_lift_px=px(H_S), DX_m=DX, DX_px=px(DX), pitch_px=px(DX) / 2,
             NI=NI, NJ=NJ, NQ=NQ, NM=NM, HALF=HALF, r_max_px=rmax, blend_bound_rad=BLEND_BOUND,
             lambda_slider_px=[LAMBDA_MIN_PX, LAMBDA_MAX_PX, LAMBDA_STEP_PX], gamma_slider=[0.0, GAMMA_MAX, GAMMA_STEP], gamma_node_step=GAMMA_NODE,
             angle_counts=N_ANGLE, height_counts=N_HEIGHT, cos_counts=N_COS)
    files = []
    def halves(stem, hdr, arr, dtype):
        for part, sl in (("lo", slice(0, HALF)), ("hi", slice(HALF, NJ))):
            fn = "%s_%s.bin" % (stem, part); h = dict(hdr, part=part, rows=[sl.start, sl.stop], shape=[HALF, NM], dtype=dtype)
            write(os.path.join(out_dir, fn), h, np.ascontiguousarray(arr[sl]).astype({"uint16": "<u2", "float32": "<f4"}[dtype])); files.append(fn)
    halves("dist", dict(model="wave_interference2", version=1, kind="dist", unit="px", formula="hypot(m DX/2, (j + 1/2) DX - H_S)"), r, "float32")
    for n, k in enumerate(K):
        halves("ring_k%03d" % n, dict(model="wave_interference2", version=1, kind="ring", node=n, k_rad_per_px=k, lambda_px=2 * np.pi / k,
               unit="2 pi / 65536 rad", formula="round(65536 frac(k r / 2 pi)) mod 65536"), RC[n], "uint16")
    for g in G:
        halves("damp_g%03d" % round(1000 * g), dict(model="wave_interference2", version=1, kind="damp", gamma=g, g_per_px=g / px(R),
               unit="1 / 65535", formula="round(65535 exp(-gamma r / R))"), DC[g], "uint16")
    hdr = dict(model="wave_interference2", version=1, kind="geometry", params=P, k_nodes=K, gamma_nodes=G,
               arrays=[dict(name="cos", shape=[N_ANGLE], dtype="int16", unit="1 / 32767", formula="round(32767 cos(2 pi n / 65536))")],
               layout="row j counted up from the near edge (bottom half rows 0-124 in *_lo, top half rows 125-249 in *_hi), column m = |2i + 1 - q|",
               checks=checks, wall_s=round(time.time() - t0, 1))
    write(os.path.join(out_dir, "geometry.bin"), hdr, TC.astype("<i2")); files.append("geometry.bin")
    hdr["files"] = sorted(files)
    json.dump(hdr, open(os.path.join(out_dir, "wave_interference2.json"), "w"), indent=1)
    total = sum(os.path.getsize(os.path.join(out_dir, f)) for f in os.listdir(out_dir))
    print(json.dumps(dict(files=len(os.listdir(out_dir)), bytes=total, k_nodes=len(K), gamma_nodes=len(G), wall_s=round(time.time() - t0, 1), checks=checks), indent=1))
    return hdr

if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else ".")
