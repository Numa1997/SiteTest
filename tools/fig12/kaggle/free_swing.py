def polar_surface_fixed(S, fill):
    """The surface on the 17 x 64 polar grid, each column's height from its OPEN length: the column (dx by dx, vertical)
    is open where its centre lies inside the glass, R(z) > r_c, which for the tulip can be in two pieces (below and above
    the waist). The liquid height is where the open length below it, times dx^2, equals the column's count x V_p.
    Columns within 1.5 dx of the wall are left out; rings beyond r1 = R - 3.5 dx are extended linearly along the radius."""
    n, dx = S.n, S.dx
    cnt = np.zeros((n, n), np.int32); S.col_counts(cnt)
    c = S.x0 + (np.arange(n) + 0.5) * dx
    X, Y = np.meshgrid(c, c, indexing="ij"); rc = np.hypot(X, Y)
    if not hasattr(S, "_openL"):
        zz = np.arange(len(S.R)) * S.dzp
        openm = rc[:, :, None] < np.asarray(S.R)[None, None, :]
        S._openL = np.concatenate([np.zeros((n, n, 1)), np.cumsum(openm[:, :, 1:] * S.dzp, 2)], 2)
        S._zz = zz
    Vp = S.V / S.N; L = cnt * Vp / dx ** 2
    OL = S._openL; zz = S._zz
    idx = np.clip((OL < L[:, :, None]).sum(2), 1, len(zz) - 1)
    i0 = idx - 1; L0 = np.take_along_axis(OL, i0[:, :, None], 2)[:, :, 0]; L1 = np.take_along_axis(OL, idx[:, :, None], 2)[:, :, 0]
    Hc = zz[i0] + np.where(L1 > L0, (L - L0) / np.maximum(L1 - L0, 1e-12), 0) * S.dzp
    Hc = np.where(OL[:, :, -1] > 0, Hc, np.nan)
    Rh = float(np.interp(fill / S.dzp, np.arange(len(S.R)), S.R))
    ok = np.isfinite(Hc) & (rc < Rh - 1.5 * dx) & (cnt > 0)
    Hz = np.where(ok, Hc, 0.0); W = ok.astype(float)
    Hs = sum(np.roll(np.roll(Hz, a, 0), b, 1) for a in (-1, 0, 1) for b in (-1, 0, 1))
    Ws = sum(np.roll(np.roll(W, a, 0), b, 1) for a in (-1, 0, 1) for b in (-1, 0, 1))
    Hc = np.where(ok, Hs / np.maximum(Ws, 1), Hc)
    r1 = Rh - 3.5 * dx; r2 = r1 - 3.5 * dx
    Hf = np.where(np.isfinite(Hc), Hc, fill)
    def bil(x, y):
        fx = (x - S.x0) / dx - 0.5; fy = (y - S.x0) / dx - 0.5
        i = np.clip(np.floor(fx).astype(int), 0, n - 2); j = np.clip(np.floor(fy).astype(int), 0, n - 2); tx = fx - i; ty = fy - j
        return (1 - tx) * (1 - ty) * Hf[i, j] + tx * (1 - ty) * Hf[i + 1, j] + (1 - tx) * ty * Hf[i, j + 1] + tx * ty * Hf[i + 1, j + 1]
    th = 2 * np.pi * np.arange(NTH) / NTH; out = np.zeros((NR + 1, NTH))
    for ir in range(NR + 1):
        r = Rh * ir / NR
        if r <= r1: out[ir] = bil(r * np.cos(th), r * np.sin(th))
        else:
            h1 = bil(r1 * np.cos(th), r1 * np.sin(th)); h2 = bil(r2 * np.cos(th), r2 * np.sin(th))
            out[ir] = h1 + (r - r1) * (h1 - h2) / (r1 - r2)
    return out


def energies(S):
    """Kinetic energy (velocity relative to the glass) and potential energy of the stout's particles, and its momentum."""
    a = S.act.to_numpy() == 1; v = S.vp.to_numpy()[a].astype(np.float64); z = S.xp.to_numpy()[a][:, 2].astype(np.float64)
    return 0.5 * S.mp * float((v ** 2).sum()), S.mp * 9.81 * float(z.sum()), S.mp * float(v[:, 0].sum())


def free_swing(dx, model):
    S = Stout(R, DZP, FILL, RHO, dx, PPC, model=MODELS[model])
    log(f"grid {dx * 1e3:.1f} mm, {model}: {S.n} x {S.n} x {S.nz} = {S.ncells:,} cells, {S.N:,} particles; stout {S.rho * S.V * 1e3:.1f} g; "
        f"glass area in the cells {S.wall_check['area_cells'] * 1e4:.1f} cm^2 (profile {S.wall_check['area_profile_below_rim'] * 1e4:.1f}); "
        f"wall rate {S.gs:.2e} m/s, foam Lambda0 {S.lam0:.3f} kg/(m s)")
    th = 2 * np.pi * np.arange(NTH) / NTH
    keys = ("t", "ax", "KE", "PE", "Px", "q16", "q13", "lean", "ewall", "efoam", "nliq", "max_speed", "nact", "cg")
    rec = {k: [] for k in keys}; surf = []
    S.vp.fill(0); S.cpx.fill(0); S.cpy.fill(0); S.cpz.fill(0)
    t = 0.0; end = SETTLE + PUSH_T + FREE; next_frame = 0.0; nsteps = 0; its = 0; T1 = time.time(); tlast = T1; cg_last = 0
    def record(tf, ax):
        Pf = polar_surface_fixed(S, FILL); KE, PE, Px = energies(S)
        rec["t"].append(round(tf, 5)); rec["ax"].append(ax); rec["KE"].append(KE); rec["PE"].append(PE); rec["Px"].append(Px)
        rec["q16"].append(float(2 / NTH * (Pf[NR] * np.cos(th)).sum() * 1e3)); rec["q13"].append(float(2 / NTH * (Pf[13] * np.cos(th)).sum() * 1e3))
        rec["lean"].append(float((Pf[NR, 0] - Pf[NR, NTH // 2]) * 1e3))
        rec["ewall"].append(float(S.ewall[None])); rec["efoam"].append(float(S.efoam[None]))
        rec["nliq"].append(int(S.liq.to_numpy().sum())); rec["max_speed"].append(S.max_speed()); rec["nact"].append(int(S.nact[None])); rec["cg"].append(cg_last)
        surf.append(np.clip(np.round((Pf - FILL) / 0.0002) + 128, 0, 255).astype(np.uint8))
    vmax = 0.0
    while t < end - 1e-9:
        ax = PUSH_A * math.sin(math.pi * (t - SETTLE) / PUSH_T) if SETTLE <= t < SETTLE + PUSH_T else 0.0
        if t >= next_frame - 1e-9: record(next_frame, ax); next_frame += 1.0 / FPS
        vmax = S.max_speed() if nsteps % 10 == 0 else vmax
        dt = min(0.002, 0.8 * dx / max(vmax, 1e-6), end - t)
        ax = PUSH_A * math.sin(math.pi * (t + 0.5 * dt - SETTLE) / PUSH_T) if SETTLE <= t + 0.5 * dt < SETTLE + PUSH_T else 0.0
        cg_last = S.step(dt, -ax, -9.81); its += cg_last
        t += dt; nsteps += 1
        if not np.isfinite(vmax) or vmax > 5: log(f"STOP: speed {vmax} m/s at t = {t:.3f} s"); break
        if time.time() - tlast > 60:
            tlast = time.time(); el = tlast - T1
            log(f"grid {dx * 1e3:.1f} mm, {model}: {t:.2f} of {end:.2f} s; {nsteps:,} steps; {(el / nsteps) * 1e3:.0f} ms a step; {its / nsteps:.0f} pressure iterations a step; about {el / t * (end - t) / 60:.1f} min left")
    if t >= next_frame - 1e-9: record(next_frame, 0.0)
    wall = time.time() - T1
    log(f"grid {dx * 1e3:.1f} mm, {model} done: {nsteps:,} steps in {wall / 60:.1f} min ({wall / nsteps * 1e3:.0f} ms a step), {its / nsteps:.0f} pressure iterations a step; "
        f"spilled {int(S.spilled[None])} particles; wall took {S.ewall[None] * 1e3:.3f} mJ, foam {S.efoam[None] * 1e3:.3f} mJ")
    rec.update(dx=dx, model=model, physics=S.model, cells=S.ncells, particles=S.N, mp=S.mp, steps=nsteps, wall_s=wall, cg_per_step=its / max(nsteps, 1),
               wall_check=S.wall_check, frames=base64.b64encode(zlib.compress(np.stack(surf).tobytes(), 9)).decode())
    return rec

import base64, zlib
results = []
for g, m in RUNS:
    results.append(free_swing(g, m))
    json.dump(dict(generated=STAMP, solver="v2", test="free swing: glass held still, one half-sine push along x", fill=FILL, rho=RHO,
                   settle=SETTLE, push_a=PUSH_A, push_t=PUSH_T, free=FREE, fps=FPS, nr=NR, nth=NTH, q=0.0002, runs=results),
              open(WORK / "free_swing_v2.json", "w"))
log(f"all runs done; wrote {WORK / 'free_swing_v2.json'} ({(WORK / 'free_swing_v2.json').stat().st_size / 1e6:.1f} MB)")
