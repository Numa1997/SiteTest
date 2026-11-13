def energies(S):
    """Kinetic energy (velocity relative to the glass) and potential energy of the stout's particles, and its momentum."""
    a = S.act.to_numpy() == 1; v = S.vp.to_numpy()[a].astype(np.float64); z = S.xp.to_numpy()[a][:, 2].astype(np.float64)
    return 0.5 * S.mp * float((v ** 2).sum()), S.mp * 9.81 * float(z.sum()), S.mp * float(v[:, 0].sum())


def free_swing(dx, model):
    model, o = run_opts(model); tag = model + ''.join(f'@{k}={v:g}' for k, v in o.items() if (k, v) not in (('dt', 0.002), ('seed', 1), ('a', PUSH_A_DEFAULT)))
    PUSH_A = o['a']
    S = Stout(R, DZP, FILL, RHO, dx, PPC, model=MODELS[model], seed=int(o['seed']))
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
        dt = min(o['dt'], 0.8 * dx / max(vmax, 1e-6), end - t)
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
    rec.update(dx=dx, model=tag, opts=o, physics=S.model, cells=S.ncells, particles=S.N, mp=S.mp, steps=nsteps, wall_s=wall, cg_per_step=its / max(nsteps, 1),
               wall_check=S.wall_check, frames=base64.b64encode(zlib.compress(np.stack(surf).tobytes(), 9)).decode())
    return rec

import base64, zlib
results = []
for g, m in RUNS:
    results.append(free_swing(g, m))
    json.dump(dict(generated=STAMP, solver="v2", test="free swing: glass held still, one half-sine push along x", fill=FILL, rho=RHO,
                   settle=SETTLE, push_a=PUSH_A_DEFAULT, push_t=PUSH_T, free=FREE, fps=FPS, nr=NR, nth=NTH, q=0.0002, runs=results),
              open(WORK / "free_swing_v2.json", "w"))
log(f"all runs done; wrote {WORK / 'free_swing_v2.json'} ({(WORK / 'free_swing_v2.json').stat().st_size / 1e6:.1f} MB)")
