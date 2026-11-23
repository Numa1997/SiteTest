"""Continuous spill: which difference makes the pint at rest sink on Fig. 16's set-up (19 Nov 2026, GPU checks 2 and 3: the read
surface fell 9.6 mm in 0.3 s while no stout was lost; the 2 mm smoke test with Fig. 12's body and the "wall" model had held it).
Runs the pint at rest for REST seconds (default 0.3) with the glass held still, gx = 0, gz = -9.81, dt = 2 ms (as smoke_cpu.py), for:
  A  Fig. 12's body (0.11, 0.06, -0.014), model "wall"   (the set-up that passed, now on the rectangular grid)
  B  Fig. 12's body, model "full" (head, skin)
  C  Fig. 16's deck (0.155, 0.062, -0.030), model "wall"
  D  Fig. 16's deck, model "full"
  E  old model (no body), model "full"                    (the baseline every stored ride used)
  F  as D with the surface tension off
and prints, at the end: the median read surface, its range, the particles' mean height (at the start and end), particles below the
cavity floor and outside the cavity, active particles. Kaggle (GPU or CPU); nothing runs outside Kaggle.
Run from the repository's root:  python3 tools/spill/rest_variants.py OUTDIR   (env DX default 0.002, REST default 0.3, ONLY e.g. "A,D")"""
import json, os, sys, time
import numpy as np
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; os.makedirs(OUT, exist_ok=True)
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "fig12", "kaggle"))
import jax  # noqa: E402
import stout_jax as SJ  # noqa: E402
js = open(os.path.join(ROOT, "public", "scripts", "guinness-glass.js")).read()
R = np.array([float(v) for v in js.split("R: [")[1].split("]")[0].split(",")])
DZP, FILL = 0.0005, 0.125
dx = float(os.environ.get("DX", "0.002")); REST = float(os.environ.get("REST", "0.3"))
F12 = (SJ.BODY_HALF[0], SJ.BODY_HALF[1], SJ.BODY_TOP); F16 = (0.155, 0.062, -0.030)
CASES = dict(A=(F12, "wall"), B=(F12, "full"), C=(F16, "wall"), D=(F16, "full"), E=(None, "full"),
             F=(F16, "full", "no tension"))      # F: D with the surface tension switched off (19 Nov 2026: is it what settles the pint?)
only = os.environ.get("ONLY"); rep = {"dx_mm": dx * 1e3, "rest_s": REST, "device": str(jax.devices()[0])}
DRAIN = os.environ.get("DRAIN") == "1"; STEP2 = os.environ.get("STEP2") == "1"; STEP3 = os.environ.get("STEP3") == "1"
STEP3V = os.environ.get("STEP3_VERIFY") == "1"; STEP4 = os.environ.get("STEP4") == "1"; STEP45 = os.environ.get("STEP45") == "1"; AUDIT45 = os.environ.get("STEP45_AUDIT") == "1"
for key, case in (() if (DRAIN or STEP2 or STEP3 or STEP3V or STEP4 or STEP45 or AUDIT45) else CASES.items()):
    body, model = case[0], case[1]
    if only and key not in only.split(","): continue
    t0 = time.time()
    G = SJ.Geometry(R, DZP, FILL, dx, body=body)
    S = SJ.Stout(G, model=model, K_frac=1.0 if body else 0.62, M_drops=4096); S.gamma = 0.0 if len(case) > 2 else S.gamma; s = S.init_state(); N = S.N
    step = jax.jit(lambda s, dt, gx, gz: S.step(s, dt, gx, gz))
    z0 = float(np.asarray(s["xp"])[:, 2].mean()); t = 0.0; dt = 0.002
    while t < REST - 1e-9: s, d = step(s, dt, 0.0, -9.81); t += dt
    o = S.observe(s); H = np.asarray(o["H"]); Hc = H[np.isfinite(H)]
    X = np.asarray(s["xp"]); act = np.asarray(s["act"]); rr = np.hypot(X[:, 0], X[:, 1])
    Rr = np.interp(np.clip(X[:, 2], 0, G.zrim) / DZP, np.arange(len(R)), R)
    r = dict(body=body, model=model, grid=[G.nx, G.ny, G.nz], particles=N, active=int(act.sum()),
             surface_median_mm=round(float(np.median(Hc)) * 1e3, 2), surface_range_mm=[round(float(Hc.min()) * 1e3, 2), round(float(Hc.max()) * 1e3, 2)],
             mean_z_mm=[round(z0 * 1e3, 2), round(float(X[act, 2].mean()) * 1e3, 2)], below_floor=int((act & (X[:, 2] < 0)).sum()),
             outside_cavity=int((act & ~((X[:, 2] > 0) & (rr < Rr))).sum()), wall_s=round(time.time() - t0, 1))
    rep[key] = r; print(key, json.dumps(r), flush=True)
if not (DRAIN or STEP2 or STEP3 or STEP3V or STEP4 or STEP45 or AUDIT45): json.dump(rep, open(os.path.join(OUT, "rest_variants.json"), "w"), indent=1, default=str)


# ====================================================================================================================================
# The bowl-base drain test (20 Nov 2026, notes/spill/STATE-projection-fix.md). Case F (Fig. 16 deck, model "full", no surface tension),
# dx = 1.5 mm, dt = 2 ms, the glass at rest. Run with DRAIN=1 and SUBRUN = "smoke" (3 steps, both codes), "base" (baseline code, 0.2 s)
# or "ext" (the solid-extrapolated level set, S.enable_ls_extend(), 1.0 s). Every step logs: CG iterations it, final residual res,
# n_drain_faces (open faces, theta > 0, joining a liquid and a non-liquid cell below z = 0.11 m, on the level set the pressure step
# used), mean particle height, median read surface, particles outside the cavity. One JSON line per step, flushed, in OUT.
def drain_run():
    import datetime
    import jax.numpy as jnp
    T0 = time.time()
    def say(m):
        print(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')} UTC | +{time.time() - T0:7.1f} s] {m}", flush=True)
    sub = os.environ.get("SUBRUN", "smoke")
    plan = {"smoke": [("base", None, 3), ("ext", None, 3)], "base": [("base", 0.2, None)], "ext": [("ext", 1.0, None)],
            "full": [("base", 0.2, None), ("ext", 1.0, None)]}[sub]
    dxd = float(os.environ.get("DX", "0.0015"))
    G = SJ.Geometry(R, DZP, FILL, dxd, body=F16)
    zf = G.z0 + dxd * np.arange(G.nz + 1); zcc = G.z0 + dxd * (np.arange(G.nz) + 0.5)
    low_c = jnp.asarray(zcc < 0.11); low_f = jnp.asarray(zf < 0.11)
    out_all = {}
    for label, T, nsteps in plan:
        S = SJ.Stout(G, model="full", K_frac=1.0, M_drops=4096); S.gamma = 0.0
        info = S.enable_ls_extend() if label == "ext" else None
        s = S.init_state(); N = S.N; dt = 0.002
        nst = nsteps if nsteps else int(round(T / dt))
        say(f"{sub}/{label}: grid {G.nx} x {G.ny} x {G.nz}, N = {N}, steps {nst}, extension {info}")
        thu, thv, thw = S.th
        def ndrain(liq):
            a = (thu[1:-1] > 0) & (liq[1:] != liq[:-1]) & low_c[None, None, :]
            b = (thv[:, 1:-1] > 0) & (liq[:, 1:] != liq[:, :-1]) & low_c[None, None, :]
            c = (thw[:, :, 1:-1] > 0) & (liq[:, :, 1:] != liq[:, :, :-1]) & low_f[None, None, 1:-1]
            return jnp.sum(a, dtype=jnp.int32) + jnp.sum(b, dtype=jnp.int32) + jnp.sum(c, dtype=jnp.int32)
        # where the drain faces are (logging only): a z histogram per cell layer up to 0.11 m, and how many touch a cell whose centre
        # is in a solid, in the cavity (both cells), or outside the cavity
        Xc, Yc, Zc = np.meshgrid(G.xc, G.yc, G.zc, indexing="ij")
        sol = jnp.asarray(G.solid(Xc, Yc, Zc)); cav = jnp.asarray(G.cavity(Xc, Yc, Zc))
        kz = jnp.asarray(np.arange(G.nz))
        def where_drain(liq):
            out = dict(solid=0, cavity=0, other=0); hist = jnp.zeros(G.nz, jnp.int32)
            for ax, th in ((0, thu), (1, thv), (2, thw)):
                sl = [slice(None)] * 3; sl[ax] = slice(1, -1); a_ = [slice(None)] * 3; a_[ax] = slice(1, None); b_ = [slice(None)] * 3; b_[ax] = slice(None, -1)
                f = (th[tuple(sl)] > 0) & (liq[tuple(a_)] != liq[tuple(b_)])
                low = (low_f[1:-1][None, None, :] if ax == 2 else low_c[None, None, :]); f = f & low
                s1 = sol[tuple(a_)] | sol[tuple(b_)]; c2 = cav[tuple(a_)] & cav[tuple(b_)]
                out["solid"] = out["solid"] + jnp.sum(f & s1); out["cavity"] = out["cavity"] + jnp.sum(f & ~s1 & c2)
                out["other"] = out["other"] + jnp.sum(f & ~s1 & ~c2)
                hz = jnp.sum(f, (0, 1)).astype(jnp.int32)          # per cell layer; a vertical face (nz - 1 of them) counts in the layer below it
                hist = hist + hz if ax != 2 else hist.at[: G.nz - 1].add(hz)
            return out, hist
        wd_j = jax.jit(where_drain)
        def drain_where(liq):
            o, h = wd_j(liq); h = np.asarray(h)
            return dict({k: int(v) for k, v in o.items()}, layers_z_mm_count=[[round(float(G.zc[i]) * 1e3, 2), int(h[i])] for i in np.nonzero(h)[0][:40]])
        prep = jax.jit(S.prepare)
        step = jax.jit(lambda s, pr: S.step(s, dt, 0.0, -9.81, prep=pr))
        obs = jax.jit(S.observe)
        nd_j = jax.jit(ndrain)
        Rd = jnp.asarray(R, jnp.float32)
        def stats(s):
            X = s["xp"]; act = s["act"]; rr = jnp.hypot(X[:, 0], X[:, 1])
            Rr = jnp.interp(jnp.clip(X[:, 2], 0, G.zrim) / DZP, jnp.arange(len(R), dtype=jnp.float32), Rd)
            zmean = jnp.sum(jnp.where(act, X[:, 2], 0.0)) / jnp.maximum(jnp.sum(act), 1)
            outside = jnp.sum(act & ~((X[:, 2] > 0) & (rr < Rr)))
            H = obs(s)["H"]; Hf = jnp.where(jnp.isfinite(H), H, jnp.nan)
            return zmean, outside, jnp.nanmedian(Hf)
        st_j = jax.jit(stats)
        z0, o0, h0 = [float(v) for v in st_j(s)]
        say(f"{sub}/{label}: t = 0  mean height {z0 * 1e3:.3f} mm  median surface {h0 * 1e3:.3f} mm  outside {int(o0)}")
        fn = os.path.join(OUT, f"drain_{sub}_{label}.jsonl"); fh = open(fn, "w")
        rows = []; tc = time.time()
        for k in range(nst):
            pr = prep(s); nd = int(nd_j(pr["liq"]))
            s, d = step(s, pr)
            zm, ou, hm = [float(v) for v in st_j(s)]
            row = dict(step=k + 1, t=round((k + 1) * dt, 4), it=int(d["it"]), res=float(d["res"]), n_drain_faces=nd,
                       mean_z_mm=zm * 1e3, surface_median_mm=hm * 1e3, outside=int(ou), nact=int(d["nact"]), wall_s=round(time.time() - tc, 2))
            if k == 0 or k == nst - 1: row["drain_where"] = drain_where(pr["liq"])
            rows.append(row); fh.write(json.dumps(row) + "\n"); fh.flush()
            if "drain_where" in row: say(f"{sub}/{label}: drain faces by place at step {k + 1}: {json.dumps(row['drain_where'])}")
            if k < 3 or (k + 1) % 25 == 0 or k == nst - 1:
                say(f"{sub}/{label}: step {k + 1}/{nst}  it {row['it']}  res {row['res']:.2e}  drain {nd}  z {row['mean_z_mm']:.3f}  "
                    f"H {row['surface_median_mm']:.3f}  out {row['outside']}  ({row['wall_s']:.0f} s)")
        fh.close()
        summ = dict(label=label, sub=sub, steps=nst, T=nst * dt, N=N, ext=info, mean_z0_mm=z0 * 1e3, mean_z1_mm=rows[-1]["mean_z_mm"],
                    surface0_mm=h0 * 1e3, surface1_mm=rows[-1]["surface_median_mm"], it_max=max(r["it"] for r in rows),
                    res_max=max(r["res"] for r in rows), drain_min=min(r["n_drain_faces"] for r in rows),
                    drain_max=max(r["n_drain_faces"] for r in rows), outside_max=max(r["outside"] for r in rows),
                    ms_per_step=1e3 * (time.time() - tc) / nst, wall_s=time.time() - tc)
        if label == "ext" and sub in ("ext", "full"):
            marks = dict(drain_zero_every_step=summ["drain_max"] == 0, it_lt_600=summ["it_max"] < 600, res_lt_1e5=summ["res_max"] < 1e-5,
                         mean_z_within_0p05mm=abs(summ["mean_z1_mm"] - summ["mean_z0_mm"]) < 0.05,
                         surface_within_0p2mm_of_125=abs(summ["surface1_mm"] - 125.0) < 0.2, zero_outside=summ["outside_max"] == 0)
            summ["pass_marks"] = marks; summ["pass"] = all(marks.values())
        out_all[label] = summ
        json.dump(summ, open(os.path.join(OUT, f"drain_{sub}_{label}_summary.json"), "w"), indent=1, default=str)
        say(f"{sub}/{label}: done {json.dumps(summ, default=str)}")
    say(f"{sub}: all done")


if DRAIN: drain_run()


# ====================================================================================================================================
# Step 2: side visibility (20 Nov 2026, notes/spill/STATE-projection-fix.md). Case F (Fig. 16 deck, model "full", gamma = 0),
# dx = 1.5 mm, dt = 2 ms, enable_ls_extend() on in every case. Run with STEP2=1 and SUBRUN = "smoke" (5 steps per case) or "full":
#   rest_2s        the pint at rest, 2.0 s (1000 steps), the outside empty, side visibility ON
#   push_tagged    the pint plus a band of stout outside the glass (15 mm wide beyond R_out, from the deck z = -0.030 m up to
#                  z = 0.060 m), a sideways body force bx = 5.0 m/s^2 for 0 <= t < 0.2 s, run to 0.5 s (250 steps), side visibility ON
#   push_untagged  the same with side visibility OFF (negative control: must show bleed across the wall or crossings)
# Every step, one JSON line: it, res, n_drain_bowl, n_drain_total, n_phantom_out, n_phantom_hi (outside cells above the band, z_c in
# 0.075 m .. rim), mean height and median surface (of the pint's particles), outside / outside_strict (pint particles), crossings.
def step2_run():
    import datetime
    import jax.numpy as jnp
    T0 = time.time()
    def say(m):
        print(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')} UTC | +{time.time() - T0:7.1f} s] {m}", flush=True)
    sub = os.environ.get("SUBRUN", "smoke")
    cases = [("rest_2s", 2.0, False, True), ("push_tagged", 0.5, True, True), ("push_untagged", 0.5, True, False)]
    sel = os.environ.get("ONLY"); cases = [c for c in cases if not sel or c[0] in sel.split(",")]
    dxd = float(os.environ.get("DX", "0.0015")); dt = 0.002; BX, TPUSH = 5.0, 0.2
    G = SJ.Geometry(R, DZP, FILL, dxd, body=F16)
    zf = G.z0 + dxd * np.arange(G.nz + 1); zcc = G.z0 + dxd * (np.arange(G.nz) + 0.5)
    low_c = jnp.asarray(zcc < 0.11); low_f = jnp.asarray(zf < 0.11)
    hi_c = jnp.asarray((zcc > 0.075) & (zcc < G.zrim))
    def band():   # the stout outside the glass: the pint's lattice (spacing dx/2), 15 mm beyond R_out(z), deck to 0.060 m, jittered
        rng = np.random.default_rng(7); h = dxd / 2; zt = F16[2]
        xs = np.arange(-0.075, 0.075, h) + 0.5 * h; Xb, Yb = np.meshgrid(xs, xs, indexing="ij"); rb = np.hypot(Xb, Yb); pts = []
        for z in np.arange(zt + 0.5 * h, 0.060, h):
            Ro = float(G.Rz(np.clip(z, 0.008, G.zrim - 1e-6))) + G.WALL
            m = (rb > Ro + 0.25 * h) & (rb < Ro + 0.015) & (np.abs(Yb) < -G.y0 - 3 * dxd)
            pts.append(np.stack([Xb[m], Yb[m], np.full(m.sum(), z)], 1))
        P = np.concatenate(pts); P[:, :2] += rng.uniform(-0.3 * h, 0.3 * h, (len(P), 2)); P[:, 2] += rng.uniform(-0.3 * h, 0.3 * h, len(P))
        return P
    stray_fh = open(os.path.join(OUT, f"step2_{sub}_stray.jsonl"), "w")
    Rd = jnp.asarray(R, jnp.float32); out_all = {}
    for label, T, push, sv in cases:
        extra = band() if push else None
        S = SJ.Stout(G, model="full", K_frac=1.0, M_drops=4096, extra=extra); S.gamma = 0.0
        S.build_sides()
        if sv: S.enable_side_vis()
        info = S.enable_ls_extend()
        s = S.init_state(); N = S.N; Np = S.N_pint
        nst = 5 if sub == "smoke" else int(round(T / dt))
        say(f"{sub}/{label}: grid {G.nx} x {G.ny} x {G.nz}, N = {N} (pint {Np}, band {N - Np}), K = {S.K}, steps {nst}, "
            f"side_vis {S.side_vis}, extension {info}")
        thu, thv, thw = S.th; cs = S.cell_side; br = S.below_rim
        def metrics(liq):
            tot = jnp.zeros((), jnp.int32); bowl = jnp.zeros((), jnp.int32)
            for ax, th in ((0, thu), (1, thv), (2, thw)):
                sl = [slice(None)] * 3; sl[ax] = slice(1, -1); a_ = [slice(None)] * 3; a_[ax] = slice(1, None); b_ = [slice(None)] * 3; b_[ax] = slice(None, -1)
                low = (low_f[1:-1][None, None, :] if ax == 2 else low_c[None, None, :])
                f = (th[tuple(sl)] > 0) & (liq[tuple(a_)] != liq[tuple(b_)]) & low
                tot = tot + jnp.sum(f, dtype=jnp.int32); bowl = bowl + jnp.sum(f & (cs[tuple(a_)] | cs[tuple(b_)]), dtype=jnp.int32)
            ph_out = liq & ~cs & br
            return tot, bowl, jnp.sum(ph_out, dtype=jnp.int32), jnp.sum(ph_out & hi_c[None, None, :], dtype=jnp.int32)
        met_j = jax.jit(metrics)
        prep = jax.jit(S.prepare)
        step = jax.jit(lambda s, pr, gx: S.step(s, dt, gx, -9.81, prep=pr))
        obs = jax.jit(S.observe)
        pint = jnp.arange(N) < Np
        def stats(s, side_prev):
            X = s["xp"]; act = s["act"]; rr = jnp.hypot(X[:, 0], X[:, 1])
            Rr = jnp.interp(jnp.clip(X[:, 2], 0, G.zrim) / DZP, jnp.arange(len(R), dtype=jnp.float32), Rd)
            ap = act & pint
            zmean = jnp.sum(jnp.where(ap, X[:, 2], 0.0)) / jnp.maximum(jnp.sum(ap), 1)
            outm = ap & ~((X[:, 2] > 0) & (rr < Rr))
            strict = ap & ~((X[:, 2] > -1e-5) & (rr < Rr + 1e-5))
            H = obs(s)["H"]; Hf = jnp.where(jnp.isfinite(H), H, jnp.nan)
            side = S.p_side(X); below = X[:, 2] < G.zrim
            cross = act & (side != side_prev[0]) & below & side_prev[1]
            wrong = act & below & (side != pint)        # a particle on the other side from where it started, below the rim
            sidx = jnp.nonzero(outm, size=10, fill_value=-1)[0]
            return (zmean, jnp.sum(outm), jnp.sum(strict), jnp.nanmedian(Hf), jnp.sum(cross), jnp.sum(wrong), (side, below), sidx,
                    jnp.max(jnp.where(act & ~pint, X[:, 2], -1.0)))
        st_j = jax.jit(stats)
        side0 = (S.p_side(s["xp"]), s["xp"][:, 2] < G.zrim)
        z0, o0, os0, h0, _, w0, sp, _, zb0 = st_j(s, side0)
        say(f"{sub}/{label}: t = 0  mean height {float(z0) * 1e3:.3f} mm  median surface {float(h0) * 1e3:.3f} mm  outside {int(o0)} "
            f"(strict {int(os0)})  on the other side {int(w0)}  band top {float(zb0) * 1e3:.1f} mm")
        fn = os.path.join(OUT, f"step2_{sub}_{label}.jsonl"); fh = open(fn, "w")
        rows = []; tc = time.time(); ncross = 0
        for k in range(nst):
            t = k * dt; gx = BX if (push and t < TPUSH - 1e-9) else 0.0
            pr = prep(s); tot, bowl, pho, phh = [int(v) for v in met_j(pr["liq"])]
            s, d = step(s, pr, gx)
            zm, ou, ous, hm, cr, wr, sp, sidx, zb = st_j(s, sp)
            ncross += int(cr)
            row = dict(step=k + 1, t=round((k + 1) * dt, 4), gx=gx, it=int(d["it"]), res=float(d["res"]), n_drain_bowl=bowl, n_drain_total=tot,
                       n_phantom_out=pho, n_phantom_hi=phh, mean_z_mm=float(zm) * 1e3, surface_median_mm=float(hm) * 1e3, outside=int(ou),
                       outside_strict=int(ous), crossings=int(cr), crossings_cum=ncross, other_side=int(wr), nact=int(d["nact"]),
                       nsel=int(d["nsel"]), band_top_mm=float(zb) * 1e3, wall_s=round(time.time() - tc, 2))
            if int(d["nsel"]) >= S.K: row["nsel_capped"] = True
            if int(ou) > 0:
                ids = [int(i) for i in np.asarray(sidx) if i >= 0]
                X = np.asarray(s["xp"])[ids]; V = np.asarray(s["vp"])[ids]
                for i, x, v in zip(ids, X, V):
                    r_ = float(np.hypot(x[0], x[1])); Rr_ = float(np.interp(np.clip(x[2], 0, G.zrim) / DZP, np.arange(len(R)), R))
                    Ro_ = float(G.Rz(np.clip(x[2], 0.008, G.zrim - 1e-6))) + G.WALL
                    stray_fh.write(json.dumps(dict(case=label, step=k + 1, t=row["t"], idx=i, x=float(x[0]), y=float(x[1]), z=float(x[2]), r=r_,
                                                   Rr=Rr_, r_minus_Rr=r_ - Rr_, Rout=Ro_, vx=float(v[0]), vy=float(v[1]), vz=float(v[2]))) + "\n")
                stray_fh.flush()
            rows.append(row); fh.write(json.dumps(row) + "\n"); fh.flush()
            if k < 3 or (k + 1) % 25 == 0 or k == nst - 1:
                say(f"{sub}/{label}: step {k + 1}/{nst}  it {row['it']}  res {row['res']:.2e}  bowl {bowl}  total {tot}  phantom {pho}/{phh}  "
                    f"z {row['mean_z_mm']:.4f}  H {row['surface_median_mm']:.4f}  out {row['outside']}/{row['outside_strict']}  "
                    f"cross {ncross}  other {row['other_side']}  nsel {row['nsel']}  ({row['wall_s']:.0f} s)")
        fh.close()
        mx = lambda key: max(r[key] for r in rows)
        summ = dict(label=label, sub=sub, steps=nst, T=nst * dt, N=N, N_pint=Np, K=S.K, side_vis=S.side_vis, ext=info,
                    mean_z0_mm=float(z0) * 1e3, mean_z1_mm=rows[-1]["mean_z_mm"], surface0_mm=float(h0) * 1e3, surface1_mm=rows[-1]["surface_median_mm"],
                    it_max=mx("it"), res_max=mx("res"), n_drain_bowl_max=mx("n_drain_bowl"), n_drain_total_max=mx("n_drain_total"),
                    n_phantom_out_max=mx("n_phantom_out"), n_phantom_hi_max=mx("n_phantom_hi"), outside_max=mx("outside"),
                    outside_strict_max=mx("outside_strict"), crossings_total=ncross, other_side_max=mx("other_side"),
                    other_side_t0=int(w0), nsel_max=mx("nsel"), nsel_capped=any(r.get("nsel_capped") for r in rows), band_top_max_mm=mx("band_top_mm"),
                    ms_per_step=1e3 * (time.time() - tc) / nst, wall_s=time.time() - tc)
        if label == "rest_2s":
            marks = dict(n_drain_bowl_zero=summ["n_drain_bowl_max"] == 0, n_phantom_out_zero=summ["n_phantom_out_max"] == 0,
                         n_drain_total_zero=summ["n_drain_total_max"] == 0, it_lt_600=summ["it_max"] < 600, res_lt_1e5=summ["res_max"] < 1e-5,
                         outside_strict_zero=summ["outside_strict_max"] == 0)
            summ["pass_marks"] = marks; summ["pass_marks_all"] = all(marks.values())
            summ["mean_z_change_mm"] = summ["mean_z1_mm"] - summ["mean_z0_mm"]; summ["surface_minus_125_mm"] = summ["surface1_mm"] - 125.0
            summ["no_threshold_given"] = ["mean_z_change_mm", "surface_minus_125_mm"]
        elif label == "push_tagged":
            summ["pass_marks"] = dict(crossings_zero=ncross == 0); summ["pass_marks_all"] = ncross == 0
        else:
            summ["pass_marks"] = dict(discriminates=(ncross > 0) or (summ["n_phantom_hi_max"] > 0)); summ["pass_marks_all"] = summ["pass_marks"]["discriminates"]
        out_all[label] = summ
        json.dump(summ, open(os.path.join(OUT, f"step2_{sub}_{label}_summary.json"), "w"), indent=1, default=str)
        say(f"{sub}/{label}: done {json.dumps(summ, default=str)}")
        del S, s, pr
    stray_fh.close()
    say(f"{sub}: all done")


if STEP2: step2_run()


# ====================================================================================================================================
# Step 3: taller grid, rounded rim lip, bare stout (20 Nov 2026, notes/spill/STATE-projection-fix.md). Fig. 16 deck, model "wall"
# (viscosity and the glass's boundary layer; no head, no skin), gamma = 0, dx = 1.5 mm, dt = 2 ms; grid top = rim + 0.08 m; lip
# radius 1.25 mm; side visibility, solid extension and the 1e-5 m wall guard on. Run with STEP3=1 and SUBRUN = "smoke" (5 steps per
# case) or "full":
#   slosh     at rest 0.3 s, pushed along x by 1.0 m/s^2 for 0.146 s, then free to 2.5 s (1250 steps); the swing is the cos(theta)
#             part of ring 13 of the stored surface (damping_grid.py's measure), sampled every 5 steps, fitted with run_b.py's fit_swing
#             from 0.1 s after the push; pass: frequency within 3 % of 3.421 Hz (the upright cylinder of R(fill), depth 0.125 m)
#   overflow  pushed along x by 5.0 m/s^2 for 0 <= t < 0.2 s, to 0.6 s (300 steps): the stout goes over the lip; pass: 0 particles
#             within a cell of the grid's top, 0 crossings of the wall below the rim, 0 particles deeper than 1e-5 m in a solid
#             after any step, and some stout over the rim (else the lip was not tested)
def step3_run():
    import datetime
    import jax.numpy as jnp
    T0 = time.time()
    def say(m):
        print(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')} UTC | +{time.time() - T0:7.1f} s] {m}", flush=True)
    sub = os.environ.get("SUBRUN", "smoke")
    _src = open(os.path.join(ROOT, "tools", "fig12", "kaggle", "run_b.py")).read()
    _a = _src.index("def fit_swing"); _b = _src.index("\n\n\n", _a); _ns = {"np": np}; exec(_src[_a:_b], _ns); fit_swing = _ns["fit_swing"]
    cases = [("slosh", 2.5, (0.3, 1.0, 0.146)), ("overflow", 0.6, (0.0, 5.0, 0.2))]
    sel = os.environ.get("ONLY"); cases = [c for c in cases if not sel or c[0] in sel.split(",")]
    dxd = float(os.environ.get("DX", "0.0015")); dt = 0.002; F0 = 3.421
    G = SJ.Geometry(R, DZP, FILL, dxd, body=F16, top=0.08, lip=0.00125)
    topz = G.z0 + G.nz * dxd; hx, hy, zt = F16; lip = G.lip; zcl = G.zlip
    say(f"{sub}: grid {G.nx} x {G.ny} x {G.nz}, top {topz * 1e3:.1f} mm (rim {G.zrim * 1e3:.1f} mm), lip {lip * 1e3:.2f} mm about "
        f"(R_m {G.Rm * 1e3:.3f} mm, z_c {zcl * 1e3:.3f} mm)")
    out_all = {}
    for label, T, (tp0, ax_, tpl) in cases:
        S = SJ.Stout(G, model="wall", K_frac=1.0, M_drops=4096); S.gamma = 0.0
        S.enable_side_vis(); info = S.enable_ls_extend(); S.wall_guard = True
        s = S.init_state(); N = S.N
        nst = 5 if sub == "smoke" else int(round(T / dt))
        say(f"{sub}/{label}: N = {N}, K = {S.K}, steps {nst}, push {ax_} m/s^2 from {tp0} s for {tpl} s, extension {info}")
        prep = jax.jit(S.prepare); step = jax.jit(lambda s, pr, gx: S.step(s, dt, gx, -9.81, prep=pr))
        obs = jax.jit(S.observe); pol = jax.jit(lambda H: S.polar(H))
        def stats(s, side_prev):
            X = s["xp"]; act = s["act"]; r = jnp.hypot(X[:, 0], X[:, 1]); z = X[:, 2]
            Rin = S.Rz(jnp.clip(z, 0.0, G.zrim - 1e-6)); Rout = S.Rz(jnp.clip(z, 0.008, G.zrim - 1e-6)) + G.WALL; e = 1e-5
            in_wall = (z > 0) & (z < zcl) & (r > Rin + e) & (r < Rout - e)
            in_cap = (z >= zcl) & (jnp.sqrt((r - G.Rm) ** 2 + (z - zcl) ** 2) < lip - e)
            in_foot = (z < -e) & (z > zt + e) & (r < Rout - e)
            in_deck = (z < zt - e) & (jnp.abs(X[:, 0]) < hx) & (jnp.abs(X[:, 1]) < hy)
            in_solid = act & (in_wall | in_cap | in_foot | in_deck)
            ceil = act & (z >= topz - dxd)
            side = S.p_side(X); below = z < G.zrim
            cross = act & (side != side_prev[0]) & below & side_prev[1]
            over = act & ~side                                   # on the outside's side (over the rim and beyond the lip's mid-radius)
            above = act & (z >= G.zrim)
            zmean = jnp.sum(jnp.where(act, z, 0.0)) / jnp.maximum(jnp.sum(act), 1)
            return (jnp.sum(in_solid), jnp.sum(ceil), jnp.max(jnp.where(act, z, -1.0)), jnp.sum(cross), jnp.sum(over), jnp.sum(above), zmean,
                    (side, below))
        st_j = jax.jit(stats)
        sp = (S.p_side(s["xp"]), s["xp"][:, 2] < G.zrim)
        isol0, ce0, zmax0, _, ov0, ab0, zm0, sp = st_j(s, sp)
        say(f"{sub}/{label}: t = 0  in solid {int(isol0)}  ceiling {int(ce0)}  z max {float(zmax0) * 1e3:.2f} mm  over {int(ov0)}  mean z {float(zm0) * 1e3:.3f} mm")
        fh = open(os.path.join(OUT, f"step3_{sub}_{label}.jsonl"), "w"); rows = []; tc = time.time(); ncross = 0; ts, q13 = [], []
        for k in range(nst):
            t = k * dt; gx = ax_ if (tp0 - 1e-9 <= t < tp0 + tpl - 1e-9) else 0.0
            pr = prep(s); s, d = step(s, pr, gx)
            isol, ce, zmax, cr, ov, ab, zm, sp = st_j(s, sp); ncross += int(cr)
            row = dict(step=k + 1, t=round((k + 1) * dt, 4), gx=gx, it=int(d["it"]), res=float(d["res"]), in_solid=int(isol), ceiling=int(ce),
                       zmax_mm=float(zmax) * 1e3, crossings=int(cr), crossings_cum=ncross, over=int(ov), above_rim=int(ab), mean_z_mm=float(zm) * 1e3,
                       nact=int(d["nact"]), nsel=int(d["nsel"]), vmax=float(d["vmax"]), wall_s=round(time.time() - tc, 2))
            if (k + 1) % 5 == 0 or sub == "smoke":
                P = np.asarray(pol(obs(s)["H"])); th = 2 * np.pi * np.arange(P.shape[1]) / P.shape[1]
                q = float(2 / len(th) * (P[13] * np.cos(th)).sum()); ts.append(row["t"]); q13.append(q); row["q13_mm"] = q * 1e3
            if int(d["nsel"]) >= S.K: row["nsel_capped"] = True
            rows.append(row); fh.write(json.dumps(row) + "\n"); fh.flush()
            if k < 3 or (k + 1) % 50 == 0 or k == nst - 1:
                say(f"{sub}/{label}: step {k + 1}/{nst}  t {row['t']:.3f}  gx {gx}  it {row['it']}  res {row['res']:.2e}  in solid {row['in_solid']}  "
                    f"ceiling {row['ceiling']}  z max {row['zmax_mm']:.1f}  cross {ncross}  over {row['over']}  above rim {row['above_rim']}  "
                    f"q13 {row.get('q13_mm', float('nan')):.3f} mm  vmax {row['vmax']:.3f}  ({row['wall_s']:.0f} s)")
        fh.close()
        mx = lambda key: max(r[key] for r in rows)
        summ = dict(label=label, sub=sub, steps=nst, T=nst * dt, N=N, K=S.K, grid=[G.nx, G.ny, G.nz], top_mm=topz * 1e3, lip_mm=lip * 1e3,
                    push=[tp0, ax_, tpl], ext=info, it_max=mx("it"), res_max=mx("res"), in_solid_max=mx("in_solid"), ceiling_max=mx("ceiling"),
                    zmax_max_mm=mx("zmax_mm"), crossings_total=ncross, over_max=mx("over"), over_end=rows[-1]["over"], above_rim_max=mx("above_rim"),
                    nact_end=rows[-1]["nact"], nsel_max=mx("nsel"), nsel_capped=any(r.get("nsel_capped") for r in rows),
                    mean_z0_mm=float(zm0) * 1e3, mean_z1_mm=rows[-1]["mean_z_mm"], ms_per_step=1e3 * (time.time() - tc) / nst, wall_s=time.time() - tc)
        if label == "slosh":
            ts_, q_ = np.array(ts), np.array(q13); m = ts_ > tp0 + tpl + 0.1
            F = fit_swing(ts_[m] - ts_[m][0], q_[m]) if m.sum() > 30 else {}
            summ["fit_ring13"] = F; summ["f_target_hz"] = F0
            if F.get("f"):
                summ["f_err_pct"] = 100 * (F["f"] / F0 - 1); summ["f0_err_pct"] = 100 * (F["f0"] / F0 - 1)
            summ["pass_marks"] = dict(f_within_3pct=bool(F.get("f") and abs(F["f"] / F0 - 1) < 0.03), ceiling_zero=summ["ceiling_max"] == 0,
                                      crossings_zero=ncross == 0, in_solid_zero=summ["in_solid_max"] == 0)
        else:
            summ["pass_marks"] = dict(ceiling_zero=summ["ceiling_max"] == 0, crossings_zero=ncross == 0, in_solid_zero=summ["in_solid_max"] == 0,
                                      overflowed=summ["over_max"] > 0)
        summ["pass_marks_all"] = all(summ["pass_marks"].values())
        out_all[label] = summ
        json.dump(summ, open(os.path.join(OUT, f"step3_{sub}_{label}_summary.json"), "w"), indent=1, default=str)
        say(f"{sub}/{label}: done {json.dumps(summ, default=str)}")
        del S, s, pr
    say(f"{sub}: all done")


if STEP3: step3_run()


# ====================================================================================================================================
# Step 3 verify, Task A (20 Nov 2026, notes/spill/STATE-projection-fix.md): diagnostic only, the overflow case of STEP3 exactly (grid
# top rim + 0.08 m, lip 1.25 mm, model "wall", gamma 0, side_vis + extension + wall guard, seed 1, push 5.0 m/s^2 for 0.2 s, dt fixed
# 2 ms, 0.6 s). The old crossing test runs unchanged. In addition, for every particle active before and after a step whose old or new
# position lies within 5 mm of the glass, the glass's signed distance phi_glass (exact distance to the (r, z) section polylines of
# Geometry.section_lines, the lip's arc as 24 chords, 0.7 um from the circle; sign from the analytic test, negative in the glass) at
# 17 points on the straight step from the old to the new position; and hit_g2p (did _g2p_cont move it: its position before the
# collisions differs from the final one). Verdicts: REAL_CROSSING, LIP_CHORD_CLIP, CLEAR, else SHALLOW_OTHER (phi_min in [-6.25e-4, 0)
# but not a lip-chord clip, no side change below the lip). Run with STEP3_VERIFY=1, SUBRUN = "smoke" (5 steps) or "full".
def step3v_run():
    import datetime
    import jax.numpy as jnp
    T0 = time.time()
    def say(m):
        print(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')} UTC | +{time.time() - T0:7.1f} s] {m}", flush=True)
    sub = os.environ.get("SUBRUN", "smoke")
    vout = os.path.join(OUT, "step3_verify"); os.makedirs(vout, exist_ok=True)
    dxd = float(os.environ.get("DX", "0.0015")); dt = 0.002; T = 0.6; tp0, ax_, tpl = 0.0, 5.0, 0.2
    G = SJ.Geometry(R, DZP, FILL, dxd, body=F16, top=0.08, lip=0.00125)
    topz = G.z0 + G.nz * dxd; hx, hy, zt = F16; lip = G.lip; zcl = G.zlip; zrim = G.zrim; Rm = G.Rm; W = G.WALL
    DEEP = 0.5 * lip; NEAR = 5e-3; WIN = 32; CAP = 600000; NS = 17; FCAP = 256
    say(f"{sub}: grid {G.nx} x {G.ny} x {G.nz}, top {topz * 1e3:.1f} mm, lip {lip * 1e3:.2f} mm about (R_m {Rm * 1e3:.4f} mm, z_lip {zcl * 1e3:.3f} mm), "
        f"rim {zrim * 1e3:.3f} mm, dt fixed {dt} s")
    # the glass's section as two polylines (z non-decreasing along each), for a windowed exact distance
    cavl, extl = G.section_lines()
    polys = []
    for P in (cavl, extl):
        A = jnp.asarray(P[:-1], jnp.float32); B = jnp.asarray(P[1:], jnp.float32); zm = jnp.asarray(0.5 * (P[:-1, 1] + P[1:, 1]), jnp.float32)
        assert np.all(np.diff(0.5 * (P[:-1, 1] + P[1:, 1])) >= -1e-12)
        polys.append((A, B, zm))
    offs = jnp.arange(-WIN, WIN)
    Rd = jnp.asarray(R, jnp.float32)
    def RzJ(z):
        f = jnp.clip(z / DZP, 0.0, len(R) - 1.001); i = jnp.floor(f).astype(jnp.int32); return Rd[i] + (f - i) * (Rd[i + 1] - Rd[i])
    def in_glass(r, z):
        Rin = RzJ(jnp.clip(z, 0.0, zrim - 1e-6)); Rout = RzJ(jnp.clip(z, 0.008, zrim - 1e-6)) + W
        wall = (z > 0) & (z < zcl) & (r >= Rin) & (r < Rout)
        cap = (z >= zcl) & ((r - Rm) ** 2 + (z - zcl) ** 2 < lip ** 2)
        foot = (z <= 0) & (z > zt) & (r < Rout)
        return wall | cap | foot
    def phi(r, z):          # r, z: (n,) -> (n,)
        d = jnp.full(r.shape, 1.0, jnp.float32)
        for A, B, zm in polys:
            M = A.shape[0]; i0 = jnp.searchsorted(zm, z); idx = jnp.clip(i0[:, None] + offs[None], 0, M - 1)
            a = A[idx]; b = B[idx]; ab = b - a; p = jnp.stack([r, z], -1)[:, None, :]
            t = jnp.clip(jnp.sum((p - a) * ab, -1) / jnp.maximum(jnp.sum(ab * ab, -1), 1e-30), 0.0, 1.0)
            d = jnp.minimum(d, jnp.sqrt(jnp.min(jnp.sum((p - (a + t[..., None] * ab)) ** 2, -1), -1)))
        return jnp.where(in_glass(r, z), -d, d)
    def phi_chunked(r, z, ch=16384):
        n = r.shape[0]; npad = (-n) % ch
        rp = jnp.pad(r, (0, npad), constant_values=1.0); zp = jnp.pad(z, (0, npad), constant_values=1.0)
        return jax.lax.map(lambda c: phi(c[0], c[1]), (rp.reshape(-1, ch), zp.reshape(-1, ch))).reshape(-1)[:n]
    def side_f(r, z):       # > 0 on the outside's side; the side test of Stout.p_side: r < R_mid(min(z, rim))
        Rin = RzJ(jnp.clip(z, 0.0, zrim - 1e-6)); Rout = RzJ(jnp.clip(z, 0.008, zrim - 1e-6)) + W
        return r - 0.5 * (Rin + Rout)
    S = SJ.Stout(G, model="wall", K_frac=1.0, M_drops=4096); S.gamma = 0.0
    S.enable_side_vis(); info = S.enable_ls_extend(); S.wall_guard = True; S.diag_g2p = True
    s = S.init_state(); N = S.N
    nst = 5 if sub == "smoke" else int(round(T / dt))
    say(f"{sub}: N = {N}, K = {S.K}, steps {nst}, extension {info}")
    prep = jax.jit(S.prepare); step = jax.jit(lambda s, pr, gx: S.step(s, dt, gx, -9.81, prep=pr))
    # the old test, exactly as step3_run's stats (rest_variants.py at 9cecadc, lines 316-342)
    def stats_old(s, side_prev):
        X = s["xp"]; act = s["act"]; r = jnp.hypot(X[:, 0], X[:, 1]); z = X[:, 2]
        Rin = S.Rz(jnp.clip(z, 0.0, G.zrim - 1e-6)); Rout = S.Rz(jnp.clip(z, 0.008, G.zrim - 1e-6)) + G.WALL; e = 1e-5
        in_wall = (z > 0) & (z < zcl) & (r > Rin + e) & (r < Rout - e)
        in_cap = (z >= zcl) & (jnp.sqrt((r - G.Rm) ** 2 + (z - zcl) ** 2) < lip - e)
        in_foot = (z < -e) & (z > zt + e) & (r < Rout - e)
        in_deck = (z < zt - e) & (jnp.abs(X[:, 0]) < hx) & (jnp.abs(X[:, 1]) < hy)
        in_solid = act & (in_wall | in_cap | in_foot | in_deck)
        ceil = act & (z >= topz - dxd)
        side = S.p_side(X); below = z < G.zrim
        cross = act & (side != side_prev[0]) & below & side_prev[1]
        return jnp.sum(in_solid), jnp.sum(ceil), cross, (side, below)
    so_j = jax.jit(stats_old)
    def new_test(Xo, Xn, Xp, act_o, act_n, gglass, cross_old):
        ok = act_o & act_n
        ro = jnp.hypot(Xo[:, 0], Xo[:, 1]); rn = jnp.hypot(Xn[:, 0], Xn[:, 1])
        po = phi_chunked(ro, Xo[:, 2]); pn = phi_chunked(rn, Xn[:, 2])
        ds = jnp.linalg.norm(Xn - Xo, axis=1)
        near = ok & (jnp.minimum(po, pn) < NEAR)
        nnear = jnp.sum(near)
        sel = jnp.nonzero(near, size=CAP, fill_value=0)[0]; valid = jnp.arange(CAP) < nnear
        xo = Xo[sel]; xn = Xn[sel]; sk = jnp.linspace(0.0, 1.0, NS, dtype=jnp.float32)
        q = xo[:, None, :] + sk[None, :, None] * (xn - xo)[:, None, :]                    # (CAP, 17, 3)
        rq = jnp.hypot(q[..., 0], q[..., 1]).reshape(-1); zq = q[..., 2].reshape(-1)
        ph = phi_chunked(rq, zq).reshape(CAP, NS)
        kmin = jnp.argmin(ph, 1); pmin = jnp.min(ph, 1); zmin = jnp.take_along_axis(q[..., 2], kmin[:, None], 1)[:, 0]
        sf = side_f(rq, zq).reshape(CAP, NS)
        so_ = sf[:, 0] > 0; sn_ = sf[:, -1] > 0; chg = so_ != sn_
        flip = (sf[:, :-1] > 0) != (sf[:, 1:] > 0); kf = jnp.argmax(flip, 1)
        f0 = jnp.take_along_axis(sf, kf[:, None], 1)[:, 0]; f1 = jnp.take_along_axis(sf, kf[:, None] + 1, 1)[:, 0]
        z0 = jnp.take_along_axis(q[..., 2], kf[:, None], 1)[:, 0]; z1 = jnp.take_along_axis(q[..., 2], kf[:, None] + 1, 1)[:, 0]
        wq = f0 / jnp.where(f1 != f0, f0 - f1, 1.0); zx = z0 + wq * (z1 - z0)
        zx = jnp.where(chg & jnp.any(flip, 1), zx, jnp.nan)
        hit = jnp.any(jnp.abs(Xp[sel] - xn) > 0.0, 1)
        po_s = po[sel]; pn_s = pn[sel]; zo = xo[:, 2]; zn = xn[:, 2]
        real = valid & ((pmin < -DEEP) | (chg & (zx < zcl)) | (chg & (zo < zrim) & (zn < zrim) & hit))
        clip = valid & ~real & (zo >= zcl) & (zn >= zcl) & (po_s > 0) & (pn_s > 0) & ~hit & (pmin >= -DEEP) & (pmin < 0)
        clear = valid & ~real & (pmin >= 0)
        other = valid & ~real & ~clip & ~clear
        oc = cross_old[sel] & valid
        flag = real | oc
        fsel = jnp.nonzero(flag, size=FCAP, fill_value=-1)[0]
        nflag = jnp.sum(flag)
        dmax = jnp.max(jnp.where(ok, ds, 0.0))
        fl = dict(i=sel[jnp.clip(fsel, 0)], ok=fsel >= 0, oc=oc[jnp.clip(fsel, 0)], real=real[jnp.clip(fsel, 0)], clip=clip[jnp.clip(fsel, 0)],
                  clear=clear[jnp.clip(fsel, 0)], xo=xo[jnp.clip(fsel, 0)], xn=xn[jnp.clip(fsel, 0)], po=po_s[jnp.clip(fsel, 0)],
                  pn=pn_s[jnp.clip(fsel, 0)], pmin=pmin[jnp.clip(fsel, 0)], zmin=zmin[jnp.clip(fsel, 0)], zx=zx[jnp.clip(fsel, 0)],
                  hit=hit[jnp.clip(fsel, 0)], gg=gglass[sel[jnp.clip(fsel, 0)]])
        cnt = dict(near=nnear, real=jnp.sum(real), clip=jnp.sum(clip), clear=jnp.sum(clear), other=jnp.sum(other), old_cross=jnp.sum(cross_old),
                   old_cross_in_near=jnp.sum(oc), nflag=nflag, hit=jnp.sum(valid & hit), phimin=jnp.min(jnp.where(valid, pmin, 1.0)), dsmax=dmax,
                   cross_any_in_near=jnp.sum(valid & chg & (zo < zrim) & (zn < zrim)))
        return cnt, fl
    nt_j = jax.jit(new_test)
    sp = (S.p_side(s["xp"]), s["xp"][:, 2] < G.zrim)
    isol0, ce0, _, sp = so_j(s, sp)
    say(f"{sub}: t = 0  in solid {int(isol0)}  ceiling {int(ce0)}")
    sfx = "" if sub == "full" else f"_{sub}"      # the full run writes the names of the instruction: flagged_particles.jsonl, summary.json
    fh = open(os.path.join(vout, f"steps{sfx}.jsonl"), "w"); ff = open(os.path.join(vout, f"flagged_particles{sfx}.jsonl"), "w")
    rows = []; tc = time.time(); tot = dict(real=0, clip=0, clear=0, other=0, old_cross=0, flagged_logged=0, hit=0)
    ver_old = {}; big_steps = []; cap_hit = False; fcap_hit = False
    for k in range(nst):
        t = k * dt; gx = ax_ if (tp0 - 1e-9 <= t < tp0 + tpl - 1e-9) else 0.0
        try:
            Xo = s["xp"]; act_o = s["act"]
            pr = prep(s); s, d = step(s, pr, gx)
            isol, ce, cross, sp = so_j(s, sp)
            cnt, fl = nt_j(Xo, s["xp"], s["xprop"], act_o, s["act"], s["g2p_glass"], cross)
            cnt = {kk: (float(v) if kk in ("phimin", "dsmax") else int(v)) for kk, v in cnt.items()}
            row = dict(step=k + 1, t=round((k + 1) * dt, 4), dt=dt, gx=gx, it=int(d["it"]), res=float(d["res"]), in_solid=int(isol), ceiling=int(ce),
                       vmax=float(d["vmax"]), ds_max_m=cnt["dsmax"], ds_max_over_dx=cnt["dsmax"] / dxd, **{f"n_{kk}": v for kk, v in cnt.items() if kk not in ("dsmax",)},
                       wall_s=round(time.time() - tc, 2))
            if cnt["near"] >= CAP: row["near_capped"] = True; cap_hit = True
            if cnt["nflag"] > FCAP: row["flag_capped"] = True; fcap_hit = True
            if row["ds_max_over_dx"] > 1.0: big_steps.append([row["step"], round(row["ds_max_over_dx"], 3)])
            for kk in ("real", "clip", "clear", "other", "old_cross", "hit"): tot[kk] += cnt[kk]
            if cnt["nflag"] > 0:
                F = {kk: np.asarray(v) for kk, v in fl.items()}
                for j in np.nonzero(F["ok"])[0]:
                    verdict = "REAL_CROSSING" if F["real"][j] else ("LIP_CHORD_CLIP" if F["clip"][j] else ("CLEAR" if F["clear"][j] else "SHALLOW_OTHER"))
                    xo, xn = F["xo"][j].astype(float), F["xn"][j].astype(float)
                    rec = dict(step=k + 1, t=row["t"], dt=dt, idx=int(F["i"][j]), old_cross=bool(F["oc"][j]), verdict=verdict,
                               x_old=xo[0], y_old=xo[1], z_old=xo[2], r_old=float(np.hypot(xo[0], xo[1])),
                               x_new=xn[0], y_new=xn[1], z_new=xn[2], r_new=float(np.hypot(xn[0], xn[1])),
                               ds=float(np.linalg.norm(xn - xo)), ds_over_dx=float(np.linalg.norm(xn - xo) / dxd),
                               phi_old=float(F["po"][j]), phi_new=float(F["pn"][j]), phi_min=float(F["pmin"][j]), z_min_phi=float(F["zmin"][j]),
                               z_cross=(None if not np.isfinite(F["zx"][j]) else float(F["zx"][j])), hit_g2p=bool(F["hit"][j]), g2p_glass=bool(F["gg"][j]))
                    ff.write(json.dumps(rec) + "\n"); tot["flagged_logged"] += 1
                    if rec["old_cross"]: ver_old[verdict] = ver_old.get(verdict, 0) + 1
                ff.flush()
            rows.append(row); fh.write(json.dumps(row) + "\n"); fh.flush()
            if k < 3 or (k + 1) % 25 == 0 or k == nst - 1 or cnt["old_cross"] or cnt["real"]:
                say(f"{sub}: step {k + 1}/{nst}  t {row['t']:.3f}  it {row['it']}  res {row['res']:.2e}  in solid {row['in_solid']}  old cross {cnt['old_cross']}  "
                    f"near {cnt['near']}  real {cnt['real']}  clip {cnt['clip']}  other {cnt['other']}  phi min {cnt['phimin'] * 1e3:.4f} mm  "
                    f"ds/dx max {row['ds_max_over_dx']:.3f}  ({row['wall_s']:.0f} s)")
        except Exception as ex:
            import traceback; say(f"{sub}: step {k + 1} FAILED: {ex!r}"); traceback.print_exc(); break
    fh.close(); ff.close()
    if rows:
        mx = lambda key: max(r[key] for r in rows)
        oc_steps = [[r["step"], r["n_old_cross"]] for r in rows if r["n_old_cross"] > 0]
        summ = dict(sub=sub, steps_done=len(rows), steps_planned=nst, T=len(rows) * dt, N=N, dt_rule="fixed dt = 2.0e-3 s (as Step 3's overflow; no speed limit)",
                    old_cross_count=tot["old_cross"], old_cross_steps=oc_steps, old_cross_verdicts=ver_old, real_crossing_count=tot["real"],
                    lip_chord_clip_count=tot["clip"], clear_count=tot["clear"], shallow_other_count=tot["other"],
                    counts_are="particle-steps among particles within 5 mm of the glass (old or new position)", hit_g2p_particle_steps=tot["hit"],
                    flagged_logged=tot["flagged_logged"], max_ds_m=mx("ds_max_m"), max_ds_over_dx=mx("ds_max_over_dx"), steps_ds_over_dx_gt_1=big_steps,
                    n_in_solid_max=mx("in_solid"), it_max=mx("it"), res_max=mx("res"), ceiling_max=mx("ceiling"), vmax_max=mx("vmax"),
                    phi_min_overall_m=min(r["n_phimin"] for r in rows), near_capped=cap_hit, flag_capped=fcap_hit,
                    params=dict(deep_m=DEEP, near_m=NEAR, samples=NS, window_segments=2 * WIN, z_lip_m=zcl, z_rim_m=zrim, R_m_m=Rm, lip_m=lip),
                    ms_per_step=1e3 * (time.time() - tc) / len(rows), wall_s=time.time() - tc)
        summ["pass_marks"] = dict(old_cross_10_at_steps_78_99=(tot["old_cross"] == 10 and all(78 <= st <= 99 for st, _ in oc_steps)),
                                  real_crossing_zero=tot["real"] == 0, in_solid_zero=summ["n_in_solid_max"] == 0, it_lt_600=summ["it_max"] < 600,
                                  res_lt_1e5=summ["res_max"] < 1e-5, every_flag_logged=(tot["flagged_logged"] >= tot["old_cross"] and not fcap_hit))
        summ["pass_marks_all"] = all(summ["pass_marks"].values())
        json.dump(summ, open(os.path.join(vout, f"summary{sfx}.json"), "w"), indent=1, default=str)
        say(f"{sub}: summary {json.dumps(summ, default=str)}")
    say(f"{sub}: all done")


if STEP3V: step3v_run()


# ====================================================================================================================================
# Step 4, test 4.4 (21 Nov 2026, notes/spill/STATE-projection-fix.md; instruction B.5): the pint with the head as elasto-viscoplastic
# foam particles (Stout head_mode "evp"), at rest, 1.0 s. Fig. 16 deck, Step 3's grid (top rim + 0.08 m, lip 1.25 mm), model "wall"
# (the stout's viscosity and Stokes layer; the head's Cantat wall stress comes with head_mode "evp"), gamma 0, side visibility,
# solid extension and wall guard on, dt = min(2e-3, 0.8 dx / vmax, 0.40 dx / c_s). Run with STEP4=1, SUBRUN "smoke" (5 steps) or "full".
# Every step one JSON line; summary with the marks of B.5 4.4 (abs( ) notation): n_drain_bowl 0 and n_phantom_out 0 every step;
# it < 600, res < 1e-5; abs(stout mean height drift) < 5e-5 m; abs(head mean height drift) < 1e-4 m; abs(H_top(1 s) - 0.144) < 3e-4 m;
# both mass books < 1e-6 relative every step; 0 real crossings and 0 particles in solids. "Real crossings": a side change below the
# lip (both ends below z_lip) or below the rim with the step longer than the wall (ds > 2.5 mm); at rest the old test (side change
# with both ends below the rim) is also logged.
def step4_run():
    import datetime, math
    import jax.numpy as jnp
    T0 = time.time()
    def say(m):
        print(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')} UTC | +{time.time() - T0:7.1f} s] {m}", flush=True)
    sub = os.environ.get("SUBRUN", "smoke"); vout = os.path.join(OUT, "step4"); os.makedirs(vout, exist_ok=True)
    dxd = float(os.environ.get("DX", "0.0015")); T = 1.0
    G = SJ.Geometry(R, DZP, FILL, dxd, body=F16, top=0.08, lip=0.00125)
    topz = G.z0 + G.nz * dxd; hx, hy, zt = F16; lip = G.lip; zcl = G.zlip
    cs = math.sqrt(SJ.G_HEAD / SJ.RHO_HEAD); dt_el = 0.40 * dxd / cs
    S = SJ.Stout(G, model="wall", K_frac=1.0, M_drops=4096, head_mode="evp"); S.gamma = 0.0
    S.enable_side_vis(); info = S.enable_ls_extend(); S.wall_guard = True
    s = S.init_state(); N = S.N; Ns = S.N_stout; Nh = S.N_head
    say(f"{sub}: grid {G.nx} x {G.ny} x {G.nz}, N {N} (stout {Ns}, head {Nh}), m_p stout {S.mp:.4e} kg, head {S.mp_head:.4e} kg, V_head {S.V_head * 1e6:.3f} cm^3, "
        f"K {S.K}, dt_el {dt_el:.4e} s, extension {info}")
    zf = G.z0 + dxd * np.arange(G.nz + 1); zcc = G.z0 + dxd * (np.arange(G.nz) + 0.5)
    low_c = jnp.asarray(zcc < 0.11); low_f = jnp.asarray(zf < 0.11)
    thu, thv, thw = S.th; cs_ = S.cell_side; br = S.below_rim
    def metrics(liq):
        tot = jnp.zeros((), jnp.int32); bowl = jnp.zeros((), jnp.int32)
        for ax, th in ((0, thu), (1, thv), (2, thw)):
            sl = [slice(None)] * 3; sl[ax] = slice(1, -1); a_ = [slice(None)] * 3; a_[ax] = slice(1, None); b_ = [slice(None)] * 3; b_[ax] = slice(None, -1)
            low = (low_f[1:-1][None, None, :] if ax == 2 else low_c[None, None, :])
            f = (th[tuple(sl)] > 0) & (liq[tuple(a_)] != liq[tuple(b_)]) & low
            tot = tot + jnp.sum(f, dtype=jnp.int32); bowl = bowl + jnp.sum(f & (cs_[tuple(a_)] | cs_[tuple(b_)]), dtype=jnp.int32)
        return tot, bowl, jnp.sum(liq & ~cs_ & br, dtype=jnp.int32)
    met_j = jax.jit(metrics)
    prep = jax.jit(S.prepare); step = jax.jit(lambda s, pr, dt: S.step(s, dt, 0.0, -9.81, prep=pr)); obs = jax.jit(S.observe)
    def stats(s, prev):
        X = s["xp"]; act = s["act"]; hd = s["is_head"]; r = jnp.hypot(X[:, 0], X[:, 1]); z = X[:, 2]
        Rin = S.Rz(jnp.clip(z, 0.0, G.zrim - 1e-6)); Rout = S.Rz(jnp.clip(z, 0.008, G.zrim - 1e-6)) + G.WALL; e = 1e-5
        in_wall = (z > 0) & (z < zcl) & (r > Rin + e) & (r < Rout - e)
        in_cap = (z >= zcl) & (jnp.sqrt((r - G.Rm) ** 2 + (z - zcl) ** 2) < lip - e)
        in_foot = (z < -e) & (z > zt + e) & (r < Rout - e)
        in_deck = (z < zt - e) & (jnp.abs(X[:, 0]) < hx) & (jnp.abs(X[:, 1]) < hy)
        in_solid = act & (in_wall | in_cap | in_foot | in_deck)
        side = S.p_side(X); X0, side0 = prev
        chg = act & (side != side0)
        old_cross = chg & (z < G.zrim) & (X0[:, 2] < G.zrim)
        ds = jnp.linalg.norm(X - X0, axis=1)
        real = chg & (((z < zcl) & (X0[:, 2] < zcl)) | ((z < G.zrim) & (X0[:, 2] < G.zrim) & (ds > G.WALL)))
        st = act & ~hd; ha = act & hd
        zs = jnp.sum(jnp.where(st, z, 0.0).astype(jnp.float64)) / jnp.maximum(jnp.sum(st), 1)
        zh = jnp.sum(jnp.where(ha, z, 0.0).astype(jnp.float64)) / jnp.maximum(jnp.sum(ha), 1)
        H = obs(s)["H"]; Hf = jnp.where(jnp.isfinite(H), H, jnp.nan)
        # mass books: each particle keeps its mass; active plus landed (left the grid) against the start, per material
        pm = s["pmass"].astype(jnp.float64)   # each particle's own mass (the head's top layer is lighter); books weighted by it
        bs = jnp.abs(jnp.sum(jnp.where(st | (s["landed"] & ~hd), pm, 0.0)) - S.m_stout0) / S.m_stout0
        bh = jnp.abs(jnp.sum(jnp.where(ha | (s["landed"] & hd), pm, 0.0)) - S.m_head0) / S.m_head0
        return (jnp.sum(in_solid), jnp.sum(old_cross), jnp.sum(real), zs, zh, jnp.nanmedian(Hf), bs, bh, jnp.max(jnp.where(act, ds, 0.0)),
                jnp.sum(act & (z >= topz - dxd)), (X, side))
    st_j = jax.jit(stats)
    prev = (s["xp"], S.p_side(s["xp"]))
    isol0, _, _, zs0, zh0, H0, bs0, bh0, _, _, prev = st_j(s, prev)
    zs0, zh0, H0 = float(zs0), float(zh0), float(H0)
    say(f"{sub}: t = 0  in solid {int(isol0)}  stout mean height {zs0 * 1e3:.4f} mm  head mean height {zh0 * 1e3:.4f} mm  H_top {H0 * 1e3:.3f} mm")
    sfx = "" if sub == "full" else f"_{sub}"
    CPU = os.environ.get("CPU_SMOKE") == "1" or os.environ.get("GPU_SMOKE") == "1"   # 21 Nov: 5-step smokes with a forced resort at RESORT_AT
    GPUS = os.environ.get("GPU_SMOKE") == "1"
    RESORT_AT = int(os.environ.get("RESORT_AT", "0"))
    base = ("smoke_4p4_gpu" if GPUS else "smoke_4p4_cpu") if CPU else f"pint_head_rest{sfx}"
    fh = open(os.path.join(vout, f"{base}.jsonl"), "w"); rows = []; tc = time.time(); t = 0.0; k = 0; vmax = 0.0
    nmax = 5 if sub == "smoke" else 10 ** 9; resort_info = None
    fin_j = jax.jit(lambda s: jnp.all(jnp.isfinite(s["xp"])) & jnp.all(jnp.isfinite(s["vp"])) & jnp.all(jnp.isfinite(s["be"])))
    while t < T - 1e-12 and k < nmax:
        try:
            dt = min(2e-3, dt_el, 0.8 * dxd / max(vmax, 1e-12))   # never cut to land on T (owner, 22 Nov): the last step ends at t >= T
            pr = prep(s); tot, bowl, pho = [int(v) for v in met_j(pr["liq"])]
            s, d = step(s, pr, dt); t += dt; k += 1
            isol, oc, real, zs, zh, Hm, bs, bh, dsm, ceil, prev = st_j(s, prev)
            vmax = float(d["vmax"]); finite = bool(fin_j(s))
            if RESORT_AT and k == RESORT_AT:   # Part B: reorder the particles in memory; every per-particle array in s must follow
                _, _, _, zs_b, zh_b, _, bs_b, bh_b, _, _, _ = st_j(s, prev)
                s = S.resort(s); prev = (s["xp"], S.p_side(s["xp"]))
                _, _, _, zs_a, zh_a, _, bs_a, bh_a, _, _, _ = st_j(s, prev)
                resort_info = dict(step=k, head_mean_z_before_m=float(zh_b), head_mean_z_after_m=float(zh_a), dz_head_m=float(zh_a) - float(zh_b),
                                   stout_mean_z_before_m=float(zs_b), stout_mean_z_after_m=float(zs_a), books_before=[float(bs_b), float(bh_b)],
                                   books_after=[float(bs_a), float(bh_a)], n_head_after=int(jnp.sum(s["is_head"])), finite_after=bool(fin_j(s)))
                say(f"{sub}: resort at step {k}: {json.dumps(resort_info)}")
            row = dict(step=k, t=t, dt=dt, it=int(d["it"]), res=float(d["res"]), res_abs=float(d["res_abs"]), bnorm=float(d["bnorm"]), conv=bool(d["conv"]), n_drain_bowl=bowl, n_drain_total=tot, n_phantom_out=pho,
                       stout_mean_z_mm=float(zs) * 1e3, head_mean_z_mm=float(zh) * 1e3, H_top_mm=float(Hm) * 1e3, book_stout=float(bs), book_head=float(bh),
                       in_solid=int(isol), old_cross=int(oc), real_cross=int(real), ceiling=int(ceil), ds_max_over_dx=float(dsm) / dxd, vmax=vmax,
                       n_yielded=int(d["n_yielded"]), gp_max=float(d["gp_max"]), s_max=float(d["s_max"]), det_min=float(d["det_min"]), det_max=float(d["det_max"]),
                       rm_res=float(d["rm_res"]), mom_phys=[float(v) for v in np.asarray(d["mom_phys"])], nsel=int(d["nsel"]), nact=int(d["nact"]),
                       finite=finite, n_floor=int(d["n_floor"]), n_floor_head=int(d["n_floor_head"]), wall_s=round(time.time() - tc, 2), step_s=round(time.time() - tc - (rows[-1]["wall_s"] if rows else 0.0), 2))
            rows.append(row); fh.write(json.dumps(row) + "\n"); fh.flush()
            if k < 3 or k % 50 == 0 or t >= T - 1e-12 or k == nmax:
                say(f"{sub}: step {k}  t {t:.4f}  dt {dt:.3e}  it {row['it']}  res {row['res']:.2e}  bowl {bowl}  phantom {pho}  z stout {row['stout_mean_z_mm']:.4f}  "
                    f"z head {row['head_mean_z_mm']:.4f}  H_top {row['H_top_mm']:.3f}  books {bs:.1e}/{bh:.1e}  in solid {row['in_solid']}  real {row['real_cross']}  "
                    f"yielded {row['n_yielded']}  s_max {row['s_max']:.3f}  det {row['det_min']:.6f}..{row['det_max']:.6f}  vmax {vmax:.4f}  ({row['wall_s']:.0f} s)")
        except Exception as ex:
            import traceback; say(f"{sub}: step {k + 1} FAILED: {ex!r}"); traceback.print_exc(); break
    fh.close()
    if rows:
        mx = lambda key: max(r[key] for r in rows); last = rows[-1]
        summ = dict(sub=sub, steps=k, t_end=t, N=N, N_stout=Ns, N_head=Nh, mp_stout=S.mp, mp_head=S.mp_head, V_head_m3=S.V_head, ext=info,
                    dt_rule="dt = min(2e-3, 0.8 dx / vmax, 0.40 dx / c_s)", dt_el=dt_el, stout_mean_z0_mm=zs0 * 1e3, stout_mean_z1_mm=last["stout_mean_z_mm"],
                    head_mean_z0_mm=zh0 * 1e3, head_mean_z1_mm=last["head_mean_z_mm"], H_top0_mm=H0 * 1e3, H_top1_mm=last["H_top_mm"],
                    n_drain_bowl_max=mx("n_drain_bowl"), n_phantom_out_max=mx("n_phantom_out"), it_max=mx("it"), res_max=mx("res"),
                    book_stout_max=mx("book_stout"), book_head_max=mx("book_head"), in_solid_max=mx("in_solid"), old_cross_total=sum(r["old_cross"] for r in rows),
                    real_cross_total=sum(r["real_cross"] for r in rows), ceiling_max=mx("ceiling"), ds_max_over_dx=mx("ds_max_over_dx"), vmax_max=mx("vmax"),
                    n_yielded_max=mx("n_yielded"), s_max=mx("s_max"), det_min=min(r["det_min"] for r in rows), det_max=mx("det_max"), rm_res_max=mx("rm_res"),
                    ms_per_step=1e3 * (time.time() - tc) / k, wall_s=time.time() - tc)
        dzs = (summ["stout_mean_z1_mm"] - summ["stout_mean_z0_mm"]) * 1e-3; dzh = (summ["head_mean_z1_mm"] - summ["head_mean_z0_mm"]) * 1e-3
        summ.update(stout_drift_m=dzs, head_drift_m=dzh, H_top_minus_0p144_m=summ["H_top1_mm"] * 1e-3 - 0.144)
        summ["pass_marks"] = dict(drain_bowl_zero=summ["n_drain_bowl_max"] == 0, phantom_zero=summ["n_phantom_out_max"] == 0, it_lt_600=summ["it_max"] < 600,
                                  res_lt_1e5_or_abs_floor=all(r["conv"] for r in rows), stout_drift_lt_5e5=abs(dzs) < 5e-5, head_drift_lt_1e4=abs(dzh) < 1e-4,
                                  H_top_within_3e4=abs(summ["H_top_minus_0p144_m"]) < 3e-4, books_lt_1e6=max(summ["book_stout_max"], summ["book_head_max"]) < 1e-6,
                                  real_cross_zero=summ["real_cross_total"] == 0, in_solid_zero=summ["in_solid_max"] == 0)
        if CPU:   # Part B's marks (instruction "step4-diag-and-cpu-smoke"), plain text with abs( )
            summ["device"] = str(jax.devices()[0]); summ["resort"] = resort_info; summ["step_s"] = [r["step_s"] for r in rows]
            summ["det_dev_max"] = max(abs(summ["det_min"] - 1.0), abs(summ["det_max"] - 1.0))
            summ["n_floor_max"] = max(r["n_floor"] for r in rows); summ["n_floor_head_max"] = max(r["n_floor_head"] for r in rows)
            summ["m_stout0"] = S.m_stout0; summ["m_head0"] = S.m_head0; summ["V_head_glass_m3"] = S.V_head_glass; summ["V_head_particles_m3"] = S.V_head
            summ["step_s_no_compile_mean"] = float(np.mean([r["step_s"] for r in rows[1:]])) if len(rows) > 1 else None
            summ["pass_marks"] = dict(all_finite=all(r["finite"] for r in rows), it_lt_600=summ["it_max"] < 600, res_lt_1e5_or_abs_floor=all(r["conv"] for r in rows),
                                      drain_bowl_zero=summ["n_drain_bowl_max"] == 0, phantom_zero=summ["n_phantom_out_max"] == 0, in_solid_zero=summ["in_solid_max"] == 0,
                                      det_dev_lt_1e5=summ["det_dev_max"] < 1e-5, books_lt_1e6=max(summ["book_stout_max"], summ["book_head_max"]) < 1e-6,
                                      books_across_resort=bool(resort_info and max(resort_info["books_after"]) < 1e-6),
                                      head_height_across_resort_lt_1e5=bool(resort_info and abs(resort_info["dz_head_m"]) < 1e-5))
            if GPUS:   # parity with the CPU smoke (committed notes/spill/step4/smoke_4p4_cpu.json; that run used the v1 head seed)
                try:
                    cpu = json.load(open(os.path.join(ROOT, "notes", "spill", "step4", "smoke_4p4_cpu.json")))
                    dzs_p = (summ["stout_mean_z1_mm"] - cpu["stout_mean_z1_mm"]) * 1e-3; dzh_p = (summ["head_mean_z1_mm"] - cpu["head_mean_z1_mm"]) * 1e-3
                    summ["parity"] = dict(stout_gpu_minus_cpu_m=dzs_p, head_gpu_minus_cpu_m=dzh_p, cpu_steps=cpu.get("steps"))
                    summ["pass_marks"]["parity_stout_lt_1e5"] = abs(dzs_p) < 1e-5; summ["pass_marks"]["parity_head_lt_5e4"] = abs(dzh_p) < 5e-4
                except Exception as ex_:
                    summ["parity"] = dict(error=repr(ex_)); summ["pass_marks"]["parity_stout_lt_1e5"] = False; summ["pass_marks"]["parity_head_lt_5e4"] = False
        summ["pass_marks_all"] = all(summ["pass_marks"].values())
        json.dump(summ, open(os.path.join(vout, f"{base}.json" if CPU else f"pint_head_rest{sfx}_summary.json"), "w"), indent=1, default=str)
        say(f"{sub}: summary {json.dumps(summ, default=str)}")
    say(f"{sub}: all done")


if STEP4: step4_run()


# ====================================================================================================================================
# Step 4, test 4.5 (22 Nov 2026; instruction B.5): free slosh of the pint with the head as elasto-viscoplastic foam. Set-up as 4.4
# (Fig. 16 deck, Step 3's grid and lip, model "wall" + head_mode "evp" with the Cantat wall stress, gamma 0, side visibility, solid
# extension, wall guard, seed v3). The glass is pushed along x by a half-sine a(t) = A sin(pi (t - t0) / tau), t0 <= t < t0 + tau
# (A = PUSH_A, default 3.4 m/s^2, tau = PUSH_T, default 0.15 s, t0 = 0.05 s; a(t) at each step's middle, as make_advance), then
# left free to 1.5 s. dt = min(2e-3, 0.8 dx / vmax, 0.40 dx / c_s), never cut to land on an end time. The swing is the cos(theta) part
# of ring 13 of the stored top surface (as Step 3), every step; fitted with run_b.py's fit_swing over the first three half-cycles
# after the push (t0 + tau .. t0 + tau + 0.5 s). Marks (B.5 4.5): f_d in [2.75, 3.15] Hz; zeta in [0.32, 0.52]; both mass books
# < 1e-6 every step; 0 real crossings and 0 particles in solids from step 1. The set-up aims at a peak wall amplitude of 8-12 mm (logged).
# Run with STEP45=1, SUBRUN "smoke" (5 steps; CPU_SMOKE=1 for Kaggle CPU) or "full".
def step45_run():
    import datetime, math
    import jax.numpy as jnp
    T0 = time.time()
    def say(m):
        print(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')} UTC | +{time.time() - T0:7.1f} s] {m}", flush=True)
    sub = os.environ.get("SUBRUN", "smoke"); vout = os.path.join(OUT, "step4"); os.makedirs(vout, exist_ok=True)
    CPU = os.environ.get("CPU_SMOKE") == "1"
    base = "smoke_4p5_cpu" if CPU else ("slosh_head" if sub == "full" else f"slosh_head_{sub}")
    dxd = float(os.environ.get("DX", "0.0015")); T = 1.5
    PA = float(os.environ.get("PUSH_A", "3.4")); PT = float(os.environ.get("PUSH_T", "0.15")); P0 = 0.05
    _src = open(os.path.join(ROOT, "tools", "fig12", "kaggle", "run_b.py")).read()
    _a = _src.index("def fit_swing"); _b = _src.index("\n\n\n", _a); _ns = {"np": np}; exec(_src[_a:_b], _ns); fit_swing = _ns["fit_swing"]
    G = SJ.Geometry(R, DZP, FILL, dxd, body=F16, top=0.08, lip=0.00125)
    topz = G.z0 + G.nz * dxd; hx, hy, zt = F16; lip = G.lip; zcl = G.zlip
    cs = math.sqrt(SJ.G_HEAD / SJ.RHO_HEAD); dt_el = 0.40 * dxd / cs
    S = SJ.Stout(G, model="wall", K_frac=1.0, M_drops=4096, head_mode="evp"); S.gamma = 0.0
    S.enable_side_vis(); info = S.enable_ls_extend(); S.wall_guard = True
    s = S.init_state(); N = S.N; Ns = S.N_stout; Nh = S.N_head
    say(f"{sub}: grid {G.nx} x {G.ny} x {G.nz}, N {N} (stout {Ns}, head {Nh}), m_head0 {S.m_head0:.6f} kg, push {PA} m/s^2 half-sine {PT} s from {P0} s, "
        f"dt_el {dt_el:.4e} s, atol {S.atol:g}, device {jax.devices()[0]}")
    prep = jax.jit(S.prepare); step = jax.jit(lambda s, pr, dt, gx: S.step(s, dt, gx, -9.81, prep=pr)); obs = jax.jit(S.observe)
    pol = jax.jit(lambda H: S.polar(H))
    def stats(s, prev):
        X = s["xp"]; act = s["act"]; hd = s["is_head"]; r = jnp.hypot(X[:, 0], X[:, 1]); z = X[:, 2]
        Rin = S.Rz(jnp.clip(z, 0.0, G.zrim - 1e-6)); Rout = S.Rz(jnp.clip(z, 0.008, G.zrim - 1e-6)) + G.WALL; e = 1e-5
        in_wall = (z > 0) & (z < zcl) & (r > Rin + e) & (r < Rout - e)
        in_cap = (z >= zcl) & (jnp.sqrt((r - G.Rm) ** 2 + (z - zcl) ** 2) < lip - e)
        in_foot = (z < -e) & (z > zt + e) & (r < Rout - e)
        in_deck = (z < zt - e) & (jnp.abs(X[:, 0]) < hx) & (jnp.abs(X[:, 1]) < hy)
        in_solid = act & (in_wall | in_cap | in_foot | in_deck)
        side = S.p_side(X); X0, side0 = prev
        chg = act & (side != side0); ds = jnp.linalg.norm(X - X0, axis=1)
        real = chg & (((z < zcl) & (X0[:, 2] < zcl)) | ((z < G.zrim) & (X0[:, 2] < G.zrim) & (ds > G.WALL)))
        st = act & ~hd; ha = act & hd; pm = s["pmass"].astype(jnp.float64)
        zs = jnp.sum(jnp.where(st, z, 0.0).astype(jnp.float64)) / jnp.maximum(jnp.sum(st), 1)
        zh = jnp.sum(jnp.where(ha, z, 0.0).astype(jnp.float64)) / jnp.maximum(jnp.sum(ha), 1)
        bs = jnp.abs(jnp.sum(jnp.where(st | (s["landed"] & ~hd), pm, 0.0)) - S.m_stout0) / S.m_stout0
        bh = jnp.abs(jnp.sum(jnp.where(ha | (s["landed"] & hd), pm, 0.0)) - S.m_head0) / S.m_head0
        out_h = jnp.sum(ha & ~side)                                   # head particles on the outside's side (over the rim)
        out_s = jnp.sum(st & ~side)
        # mechanical energy (23 Nov, step4-close): kinetic and potential, each particle with its own mass, float64
        v = s["vp"].astype(jnp.float64); KE = 0.5 * jnp.sum(jnp.where(act, pm * jnp.sum(v * v, 1), 0.0))
        PE = 9.81 * jnp.sum(jnp.where(act, pm * z.astype(jnp.float64), 0.0))
        return (jnp.sum(in_solid), jnp.sum(real), zs, zh, bs, bh, jnp.max(jnp.where(act, ds, 0.0)), jnp.sum(act & (z >= topz - dxd)),
                out_h, out_s, KE, PE, (X, side))
    st_j = jax.jit(stats)
    def ring13(s):
        H = obs(s)["H"]; P = pol(H); th = 2 * jnp.pi * jnp.arange(P.shape[1]) / P.shape[1]
        Hf = jnp.where(jnp.isfinite(H), H, jnp.nan)
        return 2.0 / P.shape[1] * jnp.sum(P[13] * jnp.cos(th)), jnp.nanmedian(Hf)
    r13_j = jax.jit(ring13)
    prev = (s["xp"], S.p_side(s["xp"]))
    _, _, zs0, zh0, _, _, _, _, _, _, KE0, PE0, prev = st_j(s, prev); q0, H0 = [float(v) for v in r13_j(s)]
    PE0 = float(PE0); ecum = dict(wall_stout=0.0, wall_foam=0.0, plastic=0.0)
    try:   # the area the fixed friction applies, at t = 0 (smoke mark abs(A_applied_new / A_grid - 1) < 0.02)
        aud0 = wall_audit(S, prep(s)); say(f"{sub}: wall area at t = 0: {json.dumps(aud0)}")
    except Exception as ex:
        aud0 = dict(error=repr(ex))
    say(f"{sub}: t = 0  stout mean z {float(zs0) * 1e3:.4f} mm  head mean z {float(zh0) * 1e3:.4f} mm  H_top {H0 * 1e3:.3f} mm  q13 {q0 * 1e3:.4f} mm")
    fh = open(os.path.join(vout, f"{base}.jsonl"), "w"); rows = []; tc = time.time(); t = 0.0; k = 0; vmax = 0.0
    nmax = 5 if sub == "smoke" else 10 ** 9
    while t < T - 1e-12 and k < nmax:
        try:
            dt = min(2e-3, dt_el, 0.8 * dxd / max(vmax, 1e-12))     # never cut to land on T
            tm = t + 0.5 * dt; gx = PA * math.sin(math.pi * (tm - P0) / PT) if P0 <= tm < P0 + PT else 0.0
            pr = prep(s); s, d = step(s, pr, dt, gx); t += dt; k += 1
            isol, real, zs, zh, bs, bh, dsm, ceil, oh, os_, KE, PE, prev = st_j(s, prev); q, Hm = [float(v) for v in r13_j(s)]
            vmax = float(d["vmax"])
            ecum["wall_stout"] += float(d["e_wall_stout"]); ecum["wall_foam"] += float(d["e_wall_foam"]); ecum["plastic"] += float(d["e_plastic"])
            row = dict(step=k, t=t, dt=dt, gx=gx, it=int(d["it"]), res=float(d["res"]), res_abs=float(d["res_abs"]), conv=bool(d["conv"]), q13_mm=q * 1e3,
                       H_top_mm=Hm * 1e3, stout_mean_z_mm=float(zs) * 1e3, head_mean_z_mm=float(zh) * 1e3, book_stout=float(bs), book_head=float(bh),
                       in_solid=int(isol), real_cross=int(real), ceiling=int(ceil), head_outside=int(oh), stout_outside=int(os_), vmax=vmax,
                       ds_max_over_dx=float(dsm) / dxd, n_yielded=int(d["n_yielded"]), gp_max=float(d["gp_max"]), s_max=float(d["s_max"]),
                       det_min=float(d["det_min"]), det_max=float(d["det_max"]), ewall_J=float(s["ewall"]), n_floor=int(d["n_floor"]),
                       KE_J=float(KE), PE_J=float(PE) - PE0, E_mech_J=float(KE) + float(PE) - PE0, E_wall_stout_cum_J=ecum["wall_stout"],
                       E_wall_foam_cum_J=ecum["wall_foam"], E_plastic_cum_J=ecum["plastic"],
                       nsel=int(d["nsel"]), nact=int(d["nact"]), wall_s=round(time.time() - tc, 2))
            rows.append(row); fh.write(json.dumps(row) + "\n"); fh.flush()
            if k < 3 or k % 100 == 0 or t >= T - 1e-12 or k == nmax:
                say(f"{sub}: step {k}  t {t:.4f}  gx {gx:.3f}  it {row['it']}  res {row['res']:.2e}  q13 {row['q13_mm']:.3f} mm  H_top {row['H_top_mm']:.3f}  "
                    f"books {bs:.1e}/{bh:.1e}  in solid {row['in_solid']}  real {row['real_cross']}  head out {oh}  yielded {row['n_yielded']}  "
                    f"s_max {row['s_max']:.2f}  vmax {vmax:.4f}  ewall {row['ewall_J']:.3e} J  ({row['wall_s']:.0f} s)")
        except Exception as ex:
            import traceback; say(f"{sub}: step {k + 1} FAILED: {ex!r}"); traceback.print_exc(); break
    fh.close()
    if rows:
        mx = lambda key: max(r[key] for r in rows)
        summ = dict(sub=sub, device=str(jax.devices()[0]), steps=k, t_end=t, N=N, N_stout=Ns, N_head=Nh, m_head0=S.m_head0, push=dict(A=PA, tau=PT, t0=P0),
                    dt_rule="dt = min(2e-3, 0.8 dx / vmax, 0.40 dx / c_s), never cut", atol=S.atol, it_max=mx("it"), res_max=mx("res"),
                    all_converged=all(r["conv"] for r in rows), book_stout_max=mx("book_stout"), book_head_max=mx("book_head"),
                    in_solid_max_from_step1=mx("in_solid"), real_cross_total=sum(r["real_cross"] for r in rows), ceiling_max=mx("ceiling"),
                    head_outside_max=mx("head_outside"), stout_outside_max=mx("stout_outside"), vmax_max=mx("vmax"), ds_max_over_dx=mx("ds_max_over_dx"),
                    n_yielded_max=mx("n_yielded"), s_max=mx("s_max"), det_min=min(r["det_min"] for r in rows), det_max=mx("det_max"),
                    ewall_end_J=rows[-1]["ewall_J"], n_floor_max=mx("n_floor"), E_wall_foam_end_J=ecum["wall_foam"], E_wall_stout_end_J=ecum["wall_stout"],
                    E_plastic_end_J=ecum["plastic"], q13_peak_mm=max(abs(r["q13_mm"]) for r in rows), H_top0_mm=H0 * 1e3,
                    step_s=[round(rows[i]["wall_s"] - (rows[i - 1]["wall_s"] if i else 0.0), 3) for i in range(min(len(rows), 10))],
                    ms_per_step=1e3 * (time.time() - tc) / k, wall_s=time.time() - tc)
        if sub == "full":
            try:
                ts = np.array([r["t"] for r in rows]); q = np.array([r["q13_mm"] for r in rows]) * 1e-3
                t1 = P0 + PT
                fitw = lambda a, b: fit_swing(ts[(ts >= a) & (ts <= b)] - ts[(ts >= a) & (ts <= b)][0], q[(ts >= a) & (ts <= b)])
                F = fitw(0.2, 1.2); Fe = fitw(0.2, 0.6); Fl = fitw(0.6, 1.2)
                summ["fit_0p2_1p2"] = F; summ["fit_0p2_0p6"] = Fe; summ["fit_0p6_1p2"] = Fl; summ["fit_first_three_half_cycles"] = fitw(t1, t1 + 0.5)
                zc = np.nonzero(np.diff(np.sign(q[ts >= t1])))[0]; summ["zero_crossings_after_push_s"] = [float(ts[ts >= t1][i]) for i in zc[:8]]
                # energy over 0.2-1.0 s: the mechanical energy lost against the logged sinks (wall: the head's Cantat stress; plastic; the stout's layer)
                at = lambda key, tt: float(np.interp(tt, ts, np.array([r[key] for r in rows])))
                dEm = at("E_mech_J", 1.0) - at("E_mech_J", 0.2)
                Ew = at("E_wall_foam_cum_J", 1.0) - at("E_wall_foam_cum_J", 0.2); Ep = at("E_plastic_cum_J", 1.0) - at("E_plastic_cum_J", 0.2)
                Es = at("E_wall_stout_cum_J", 1.0) - at("E_wall_stout_cum_J", 0.2); sinks = Ew + Ep + Es
                summ["energy_0p2_1p0"] = dict(minus_dE_mech_J=-dEm, E_wall_foam_J=Ew, E_plastic_J=Ep, E_wall_stout_J=Es, sinks_J=sinks,
                                              closure=sinks / max(-dEm, 1e-30) - 1.0)
                summ["zeta_status"] = "provisional: anchored in a first-principles estimate (Neon), not in an experiment for this glass"
                summ["pass_marks"] = dict(f_d_in_2p70_3p15=bool(F.get("f") and 2.70 <= F["f"] <= 3.15),
                                          zeta_0p2_1p2_in_0p13_0p33=bool(F.get("zeta") and 0.13 <= F["zeta"] <= 0.33),
                                          zeta_late_gt_early=bool(Fl.get("zeta") and Fe.get("zeta") and Fl["zeta"] > Fe["zeta"]),
                                          energy_closure_within_0p25=abs(sinks / max(-dEm, 1e-30) - 1.0) < 0.25, sinks_le_loss_within_2pct=sinks <= 1.02 * (-dEm),
                                          books_lt_1e6=max(summ["book_stout_max"], summ["book_head_max"]) < 1e-6, real_cross_zero=summ["real_cross_total"] == 0,
                                          in_solid_zero=summ["in_solid_max_from_step1"] == 0, it_lt_600=summ["it_max"] < 600, converged=summ["all_converged"])
                summ["pass_marks_all"] = all(summ["pass_marks"].values())
                summ["setup_peak_wall_amplitude_in_8_12mm"] = bool(8.0 <= summ["q13_peak_mm"] <= 12.0)
            except Exception as ex:
                summ["fit_error"] = repr(ex)
        else:
            tg = aud0.get("totals_three_components", {}) if isinstance(aud0, dict) else {}
            ratio = tg.get("A_applied_new", float("nan")) / max(tg.get("A_grid", 0.0), 1e-30)
            summ["wall_area_t0"] = aud0; summ["A_applied_new_over_grid"] = ratio
            summ["pass_marks"] = dict(all_finite=bool(np.all(np.isfinite(np.asarray(s["xp"])))), converged=summ["all_converged"], it_lt_600=summ["it_max"] < 600,
                                      A_applied_new_within_2pct=bool(abs(ratio - 1) < 0.02),
                                      books_lt_1e6=max(summ["book_stout_max"], summ["book_head_max"]) < 1e-6, in_solid_zero=summ["in_solid_max_from_step1"] == 0)
        json.dump(summ, open(os.path.join(vout, f"{base}_summary.json" if not CPU else f"{base}.json"), "w"), indent=1, default=str)
        say(f"{sub}: summary {json.dumps(summ, default=str)}")
    say(f"{sub}: all done")



# ====================================================================================================================================
# Step 4 close, Part A (23 Nov 2026, instruction "step4-close"): audit of the wall friction's area, CPU, before any change. At the 4.5
# set-up, at t = 0 (prepare) and after one step: in the foam band 125-143.75 mm, A_geom = integral of 2 pi R(z) ds of the inner wall;
# per velocity component, A_grid = sum of af dx^3 over wall faces (af > 0) and A_applied = sum of af dx^3 x alpha_open, alpha_open =
# M_f / (rho_f dx^3), the area friction_evp effectively applies (its lam divides by rho_f dx^3, not by M_f); alpha_open's mean, min,
# max over wall faces; n_mfloor_wall / n_mfloor_free (occupied faces with M_f < m_floor, af > 0 / af = 0). From the committed
# slosh_head.jsonl: E_mech at the half-cycle extremes of the swing over 0.2-1.2 s (potential energy above rest from the logged mean
# heights; the kinetic energy is near zero there), and the logged ewall per half-cycle. Writes OUTDIR/step4/diag_4p5_energy.json.
def wall_audit(S, pr, z_lo=0.125, z_hi=0.14375):
    import jax.numpy as jnp
    G = S.G; dx = S.dx; ex = pr["ex"]; out = {}
    zf = G.z0 + dx * np.arange(G.nz + 1)
    fz = [np.broadcast_to(G.zc[None, None, :], S.fshape[0]), np.broadcast_to(G.zc[None, None, :], S.fshape[1]), np.broadcast_to(zf[None, None, :], S.fshape[2])]
    tot = dict(A_grid=0.0, A_applied=0.0, A_applied_new=0.0)
    for c, name in enumerate("uvw"):
        af = np.asarray(S.af[c]); M = np.asarray(ex["M"][c]); rf = np.asarray(ex["rho_f"][c]); ws = np.asarray(pr["mass"][c]); th = np.asarray(S.th[c])
        occ = (th > 0) & (ws > 1e-6); band = (fz[c] >= z_lo) & (fz[c] <= z_hi); wall = occ & (af > 0) & band
        alpha = M / (rf * dx ** 3)
        A_grid = float((af * dx ** 3)[wall].sum()); A_app = float((af * dx ** 3 * alpha)[wall].sum())
        A_new = float((af * dx ** 3 * np.minimum(1.0, M / np.maximum(M, S.m_floor)))[wall].sum())
        fl = occ & (M < S.m_floor)
        out[name] = dict(n_wall_faces=int(wall.sum()), A_grid_m2=A_grid, A_applied_m2=A_app, A_applied_over_grid=A_app / max(A_grid, 1e-30),
                         A_applied_new_m2=A_new, alpha_open_mean=float(alpha[wall].mean()), alpha_open_min=float(alpha[wall].min()), alpha_open_max=float(alpha[wall].max()),
                         n_mfloor_wall=int((fl & (af > 0)).sum()), n_mfloor_free=int((fl & (af == 0)).sum()))
        tot["A_grid"] += A_grid; tot["A_applied"] += A_app; tot["A_applied_new"] += A_new
    zz = np.linspace(z_lo, z_hi, 20001); Rr = G.Rz(zz); ds = np.sqrt(np.diff(zz) ** 2 + np.diff(Rr) ** 2)
    out["A_geom_m2"] = float(np.sum(2 * np.pi * 0.5 * (Rr[1:] + Rr[:-1]) * ds)); out["band_m"] = [z_lo, z_hi]; out["totals_three_components"] = tot
    return out


def audit45_run():
    import datetime
    import jax.numpy as jnp
    T0 = time.time()
    def say(m):
        print(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')} UTC | +{time.time() - T0:7.1f} s] {m}", flush=True)
    vout = os.path.join(OUT, "step4"); os.makedirs(vout, exist_ok=True); res = dict(code="as at 045fb72 (before the fix)", device=str(jax.devices()[0]))
    try:
        G = SJ.Geometry(R, DZP, FILL, 0.0015, body=F16, top=0.08, lip=0.00125)
        S = SJ.Stout(G, model="wall", K_frac=1.0, M_drops=4096, head_mode="evp"); S.gamma = 0.0
        S.enable_side_vis(); S.enable_ls_extend(); S.wall_guard = True; s = S.init_state()
        prep = jax.jit(S.prepare); step = jax.jit(lambda s, pr, dt: S.step(s, dt, 0.0, -9.81, prep=pr))
        pr = prep(s); res["t0"] = wall_audit(S, pr); say(f"audit t = 0: {json.dumps(res['t0'])}")
        s, d = step(s, pr, 7.6687e-4); pr = prep(s); res["after_one_step"] = wall_audit(S, pr); say(f"audit after one step: {json.dumps(res['after_one_step'])}")
        res["m_stout0"] = S.m_stout0; res["m_head0"] = S.m_head0
    except Exception as ex:
        import traceback; res["audit_error"] = repr(ex); traceback.print_exc()
    json.dump(res, open(os.path.join(vout, "diag_4p5_energy.json"), "w"), indent=1, default=str)
    try:   # energy at the half-cycle extremes from the committed 4.5 log
        rows = [json.loads(l) for l in open(os.path.join(ROOT, "notes", "spill", "step4", "slosh_head.jsonl"))]
        t = np.array([r["t"] for r in rows]); q = np.array([r["q13_mm"] for r in rows]); ew = np.array([r["ewall_J"] for r in rows])
        zs = np.array([r["stout_mean_z_mm"] for r in rows]) * 1e-3; zh = np.array([r["head_mean_z_mm"] for r in rows]) * 1e-3
        ms, mh = res.get("m_stout0", 0.4296), res.get("m_head0", 0.02407)
        zs0, zh0 = zs[t < 0.05].mean(), zh[t < 0.05].mean()
        PE = 9.81 * (ms * (zs - zs0) + mh * (zh - zh0))
        m = (t >= 0.2) & (t <= 1.2); idx = np.nonzero(m)[0]; ext = []
        for i in idx[1:-1]:
            if abs(q[i]) >= abs(q[i - 1]) and abs(q[i]) > abs(q[i + 1]) and (not ext or np.sign(q[i]) != np.sign(q[ext[-1]])): ext.append(i)
        res["extremes"] = [dict(t=float(t[i]), q13_mm=float(q[i]), E_mech_J=float(PE[i]), ewall_cum_J=float(ew[i])) for i in ext]
        res["per_half_cycle"] = [dict(t0=float(t[a]), t1=float(t[b]), dE_mech_J=float(PE[b] - PE[a]), ewall_logged_J=float(ew[b] - ew[a]))
                                 for a, b in zip(ext[:-1], ext[1:])]
        res["E_mech_note"] = ("potential energy above rest from the logged mean heights (stout mass-weighted; head arithmetic mean over particles, "
                              "the ring and top layer carry other masses: approximate); kinetic energy taken as zero at the extremes")
        say(f"energy: {json.dumps(res['per_half_cycle'])}")
    except Exception as ex:
        res["energy_error"] = repr(ex)
    json.dump(res, open(os.path.join(vout, "diag_4p5_energy.json"), "w"), indent=1, default=str)
    say("all done")


if AUDIT45: audit45_run()


if STEP45: step45_run()   # after wall_audit's definition
