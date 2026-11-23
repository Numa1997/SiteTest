"""Fig. 1, Wave interference: the reference model behind the page `simulations/Circular Wave Interference Visualization.html`.

The setup. A still pond seen from above, a field W wide. A row of small floats sits on one straight line, a height h_s above the
near edge; a motor makes them all bob up and down together, at one frequency f. Each float sends out a ring of ripples. Where rings
meet, their heights add (superposition). The page colours the height of the water at every point.

One ring (note eq. 5), at distance r from its source s:

    psi_s(r, t) = a(r) cos(k r - omega t),    k = 2 pi / lambda,    omega = 2 pi f,    a(r) = exp(-gamma r / R)          (1)

All rings added and divided by their number N (note eq. 6), split exactly into space times time (note eq. 18):

    psi = (1/N) sum_s a(r_s) cos(k r_s - omega t) = C cos(omega t) + S sin(omega t),
    C = (1/N) sum_s a(r_s) cos(k r_s),   S = (1/N) sum_s a(r_s) sin(k r_s)                                                (2)

What is stored, and why. The finished field C, S cannot be stored for every choice of the reader: the sources may be placed
anywhere by clicking, so their combinations have no end. But (2) is a sum of rings, and a ring depends only on its distance r. On a
common lattice (cells every DX across and up, source places every DX/2 along the source line) the distance from cell (i, j) to the
source at place q depends only on m = |2i + 1 - q| and on j, so ONE table r(j, m) holds every distance that can occur. The model
stores, for every wavelength node lambda, the angle k r(j, m) of a ring, reduced to one turn; for every damping node gamma its height
a(r(j, m)); and a table of cos(2 pi n / 65536). The page then adds the rings of the sources the reader chose, with no cos, sin, exp
or sqrt of its own: it reads the angle, looks its cosine and sine up in the stored table, multiplies by the stored height and adds.

Units. SI in the parameters below. Nothing in (1) and (2) depends on the absolute scale: the picture depends only on k r and gamma r/R.
The page counts lengths in px of a field that is always 800 px wide, so the stored tables use that unit: 1 px = W / 800 = PX_M m.
The scale W is a choice (a ripple tank 0.40 m wide), stated so that every length has a value in metres.

Method: closed form, evaluated in float64 by NumPy; no integration, so there are no tolerances. Then rounded for storage:
    angle  -> uint16, one count = 2 pi / 65536 rad          height -> uint16, one count = 1 / 65535
    cosine -> int16,  one count = 1 / 32767                 distance r -> float32, px

Files (each: 4 bytes of label b"WIF1", uint32 header length, a JSON header padded with spaces to a multiple of 4 bytes, then the
little-endian array, row j (counted up from the near edge) by column m):
    geometry.bin       r(j, m) float32 [NJ x NM] px, then the cosine table int16 [65536]; the header holds every parameter,
                       the node lists and the checks
    ring_l<NNN>.bin    angle k r(j, m) reduced to one turn, uint16 [NJ x NM], one file per wavelength node lambda = NNN px
    damp_g<NNN>.bin    height a(r(j, m)), uint16 [NJ x NM], one file per damping node gamma = NNN / 100
    wave_interference.json   the geometry header again, readable (parameters, nodes, checks, file list)

Checks written into the output (geometry header and wave_interference.json):
  - comparison with today's browser result: the page's sum from the stored tables (computed here exactly as the page computes it,
    float32 sums) against the float64 sum straight from (1)-(2), which is what the browser computed live, for the presets Reset
    and Line of 16 at every node pair; and the colour-table row drawn at 32 instants of one period;
  - a known limit: two sources at gamma = 0, the amplitude must be |cos(k (r_1 - r_2) / 2)|;
  - a conserved quantity: a stored ring keeps the length of its arrow, cos^2 + sin^2 = 1, in the stored cosine table;
  - rounding: the largest error of each stored angle and height against its exact value.
Usage: python3 wave_interference.py [out_dir]"""
import json, os, struct, sys, time
import numpy as np

# ---- parameters (SI) ----
W = 0.40                 # m, width of the field (a ripple tank); the page draws it 800 px wide
PX_M = W / 800           # m per px of the field: 0.5 mm
R = 300 * PX_M           # m, damping length: a ring loses gamma factors of e over R (note eq. 5); 300 px
H_S = 10 * PX_M          # m, height of the source line above the near edge; 10 px
DX = 3.2 * PX_M          # m, size of a grid cell, across and up: 1.6 mm, 3.2 px
NI = 250                 # cells across: NI * DX = W
NJ = 250                 # cells up, counted from the near edge: NJ * DX = W, the square field of a phone
NQ = 501                 # source places x_q = q DX / 2, q = 0 ... 500, along the source line
NM = 500                 # values of m = |2i + 1 - q|, 0 ... 499
LAMBDA_PX = list(range(16, 65))                          # wavelength nodes, px: 16, 17, ..., 64 (8 mm ... 32 mm)
GAMMA = [round(0.05 * n, 2) for n in range(13)]          # damping nodes: 0, 0.05, ..., 0.60
F_RANGE_HZ = (0.2, 2.0)  # Hz, the frequency slider; f only sets how fast the stored period is played, so it needs no data
MAX_SOURCES = 24         # the page keeps the newest 24 sources
N_ANGLE, N_HEIGHT, N_COS = 65536, 65535, 32767           # counts per turn, per unit height, per unit cosine
N_INSTANTS = 32          # instants of one period in the colour-row check

px = lambda metres: metres / PX_M

def geometry():
    """r(j, m) in px, float64: horizontal gap m DX/2, vertical gap (j + 1/2) DX - H_S."""
    j = np.arange(NJ)[:, None]; m = np.arange(NM)[None, :]
    return np.hypot(m * px(DX) / 2, (j + 0.5) * px(DX) - px(H_S))

def ring_counts(r, lam):
    """angle k r reduced to one turn, in counts of 2 pi / 65536: uint16"""
    return (np.rint(np.mod(r / lam, 1.0) * N_ANGLE).astype(np.int64) % N_ANGLE).astype(np.uint16)

def damp_counts(r, gamma):
    return np.rint(N_HEIGHT * np.exp(-gamma * r / px(R))).astype(np.uint16)

def cos_table():
    return np.rint(N_COS * np.cos(2 * np.pi * np.arange(N_ANGLE) / N_ANGLE)).astype(np.int16)

def write(path, label, hdr, *arrays):
    hb = json.dumps(hdr, separators=(",", ":")).encode()
    hb += b" " * ((-(8 + len(hb))) % 4)                   # so the arrays start on a multiple of 4 bytes
    with open(path, "wb") as f:
        f.write(label); f.write(struct.pack("<I", len(hb))); f.write(hb)
        for a in arrays: f.write(a.tobytes())

def presets():
    return {"reset": [125, 375], "line16": [40 + 28 * n for n in range(16)]}    # x = 200, 600 px; x = 64 + 44.8 n px

def page_sum(q_list, RC, DC, TC):
    """C, S exactly as the page adds them: float32 maps, one source after another, term = height * cosine * (1/N) / (65535 * 32767)."""
    i = np.arange(NI)
    C = np.zeros((NJ, NI), np.float32); S = np.zeros((NJ, NI), np.float32); w = (1 / len(q_list)) / (N_HEIGHT * N_COS)
    for q in q_list:
        m = np.abs(2 * i + 1 - q)
        n = RC[:, m].astype(np.int64); a = DC[:, m].astype(np.float64)
        C = (C.astype(np.float64) + a * TC[n] * w).astype(np.float32)
        S = (S.astype(np.float64) + a * TC[(n - N_ANGLE // 4) % N_ANGLE] * w).astype(np.float32)
    return C, S

def exact_sum(q_list, lam, gamma):
    """C, S straight from (1)-(2) in float64: what the browser computed live on this grid."""
    x = (np.arange(NI) + 0.5) * px(DX); y = (np.arange(NJ) + 0.5) * px(DX) - px(H_S)
    C = np.zeros((NJ, NI)); S = np.zeros((NJ, NI))
    for q in q_list:
        r = np.hypot(x[None, :] - q * px(DX) / 2, y[:, None]); a = np.exp(-gamma * r / px(R)) / len(q_list)
        C += a * np.cos(2 * np.pi * r / lam); S += a * np.sin(2 * np.pi * r / lam)
    return C, S

def row(psi):
    return np.rint(np.clip(psi, -1, 1) * 127.5 + 127.5)

def run(out_dir="."):
    t0 = time.time(); os.makedirs(out_dir, exist_ok=True)
    r = geometry(); TC = cos_table()
    RCs = {lam: ring_counts(r, lam) for lam in LAMBDA_PX}; DCs = {g: damp_counts(r, g) for g in GAMMA}
    # ---- checks ----
    err_angle = max(float(np.max(np.abs(np.angle(np.exp(1j * (2 * np.pi * RCs[l] / N_ANGLE - 2 * np.pi * r / l)))))) for l in LAMBDA_PX)
    err_height = max(float(np.max(np.abs(DCs[g] / N_HEIGHT - np.exp(-g * r / px(R))))) for g in GAMMA)
    c = TC / N_COS; s = np.roll(TC, N_ANGLE // 4) / N_COS                       # s[n] = TC[n - 16384] = sin(2 pi n / 65536)
    arrow = float(np.max(np.abs(c * c + s * s - 1)))
    err_cos = float(np.max(np.abs(c - np.cos(2 * np.pi * np.arange(N_ANGLE) / N_ANGLE))))
    wt = 2 * np.pi * np.arange(N_INSTANTS) / N_INSTANTS
    cmp = dict(); worst = dict(C=0.0, S=0.0, psi=0.0); rows_differ = 0; cells = 0; row_diff_max = 0
    for name, ql in presets().items():
        for lam in LAMBDA_PX:
            for g in GAMMA:
                Cp, Sp = page_sum(ql, RCs[lam], DCs[g], TC); Ce, Se = exact_sum(ql, lam, g)
                worst["C"] = max(worst["C"], float(np.max(np.abs(Cp - Ce)))); worst["S"] = max(worst["S"], float(np.max(np.abs(Sp - Se))))
                Pp = Cp[None].astype(np.float64) * np.cos(wt)[:, None, None] + Sp[None] * np.sin(wt)[:, None, None]
                Pe = Ce[None] * np.cos(wt)[:, None, None] + Se[None] * np.sin(wt)[:, None, None]
                worst["psi"] = max(worst["psi"], float(np.max(np.abs(Pp - Pe))))
                d = np.abs(row(Pp) - row(Pe)); rows_differ += int(np.count_nonzero(d)); row_diff_max = max(row_diff_max, int(d.max())); cells += d.size
        cmp[name] = ql
    # known limit: two sources (Reset) at gamma = 0, amplitude = |cos(k (r1 - r2) / 2)|
    x = (np.arange(NI) + 0.5) * px(DX); y = (np.arange(NJ) + 0.5) * px(DX) - px(H_S)
    r1 = np.hypot(x[None, :] - 200, y[:, None]); r2 = np.hypot(x[None, :] - 600, y[:, None])
    limit = 0.0
    for lam in LAMBDA_PX:
        Cp, Sp = page_sum([125, 375], RCs[lam], DCs[0.0], TC)
        limit = max(limit, float(np.max(np.abs(np.hypot(Cp, Sp) - np.abs(np.cos(np.pi * (r1 - r2) / lam))))))
    checks = dict(
        compared_presets=cmp, node_pairs=len(LAMBDA_PX) * len(GAMMA), instants=N_INSTANTS,
        max_diff_C=worst["C"], max_diff_S=worst["S"], max_diff_psi=worst["psi"],
        colour_row_cell_instants=cells, colour_row_differ=rows_differ, colour_row_max_diff=row_diff_max,
        two_source_limit_max_diff=limit, arrow_length_max_diff=arrow, cos_table_max_err=err_cos,
        angle_max_err_rad=err_angle, height_max_err=err_height,
        rounding=dict(angle_rad=np.pi / N_ANGLE, height=0.5 / N_HEIGHT, cosine=0.5 / N_COS))
    # ---- files ----
    P = dict(W_m=W, px_m=PX_M, R_m=R, R_px=px(R), H_S_m=H_S, source_lift_px=px(H_S), DX_m=DX, DX_px=px(DX), pitch_px=px(DX) / 2,
             NI=NI, NJ=NJ, NQ=NQ, NM=NM, f_range_Hz=F_RANGE_HZ, max_sources=MAX_SOURCES, angle_counts=N_ANGLE, height_counts=N_HEIGHT,
             cos_counts=N_COS)
    files = {}
    for lam in LAMBDA_PX:
        fn = "ring_l%03d.bin" % lam
        write(os.path.join(out_dir, fn), b"WIF1", dict(model="wave_interference", version=1, kind="ring", lambda_px=lam, lambda_m=lam * PX_M,
              k_rad_per_px=2 * np.pi / lam, shape=[NJ, NM], dtype="uint16", unit="2 pi / 65536 rad", formula="round(65536 frac(r / lambda)) mod 65536"),
              RCs[lam].astype("<u2"))
        files[fn] = dict(lambda_px=lam)
    for g in GAMMA:
        fn = "damp_g%03d.bin" % round(100 * g)
        write(os.path.join(out_dir, fn), b"WIF1", dict(model="wave_interference", version=1, kind="damp", gamma=g, g_per_px=g / px(R),
              shape=[NJ, NM], dtype="uint16", unit="1 / 65535", formula="round(65535 exp(-gamma r / R))"), DCs[g].astype("<u2"))
        files[fn] = dict(gamma=g)
    hdr = dict(model="wave_interference", version=1, kind="geometry", params=P, lambda_px=LAMBDA_PX, gamma=GAMMA,
               arrays=[dict(name="r", shape=[NJ, NM], dtype="float32", unit="px", formula="hypot(m DX/2, (j + 1/2) DX - H_S)"),
                       dict(name="cos", shape=[N_ANGLE], dtype="int16", unit="1 / 32767", formula="round(32767 cos(2 pi n / 65536))")],
               layout="row j counted up from the near edge, column m = |2i + 1 - q|", checks=checks, wall_s=round(time.time() - t0, 1))
    write(os.path.join(out_dir, "geometry.bin"), b"WIF1", hdr, r.astype("<f4"), TC.astype("<i2"))
    hdr["files"] = sorted(files) + ["geometry.bin"]
    json.dump(hdr, open(os.path.join(out_dir, "wave_interference.json"), "w"), indent=1)
    total = sum(os.path.getsize(os.path.join(out_dir, f)) for f in os.listdir(out_dir))
    print(json.dumps(dict(files=len(os.listdir(out_dir)), bytes=total, wall_s=round(time.time() - t0, 1), checks=checks), indent=1))
    return hdr

if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else ".")
