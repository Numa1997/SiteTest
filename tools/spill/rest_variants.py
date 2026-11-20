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
DRAIN = os.environ.get("DRAIN") == "1"; STEP2 = os.environ.get("STEP2") == "1"
for key, case in (() if (DRAIN or STEP2) else CASES.items()):
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
if not (DRAIN or STEP2): json.dump(rep, open(os.path.join(OUT, "rest_variants.json"), "w"), indent=1, default=str)


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
