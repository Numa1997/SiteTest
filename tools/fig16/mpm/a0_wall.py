"""Fig. 16 one-model spill, test A.0: does the 2.5 mm glass wall hold at dx = 1.5 mm? (2-D planar, Kaggle CPU.)

Pass marks, fixed before the run (notes/spill/STATE-one-model.md, owner's corrections of 20 Nov 2026):
  main            the pint at rest (stout to 125 mm, head to 144 mm), outside empty, 2 s, side tags on:
                  zero particles cross the wall at every check (1 ms apart, 2 000 checks): no particle changes side below the rim,
                  and no particle that started inside is ever found outside the outer wall below the rim.
  control_untagged  liquid on both sides of the wall (outside: stout from the outer wall out 15 mm, from the deck up to 60 mm)
                  and a sideways push b_x = 5 m/s^2 for the first 0.2 s, 0.5 s in all, side tags OFF (one velocity per node):
                  crossings > 0 expected. If it shows none, the test does not discriminate: report that and stop.
  control_tagged  the same case with side tags on: zero crossings.
Logged, not judged here: depth into the solid, |J - 1| (density error) per phase, isolated particles, top of the column at the
centre (test A.1 later), largest speed and c / vmax, the number of head particles at the viscosity cap.

Usage (on Kaggle):  python a0_wall.py --profile glass_profile.json --out /kaggle/working/a0 --smoke
                    python a0_wall.py --profile glass_profile.json --out /kaggle/working/a0 --full
--smoke runs 1 000 steps of each case and writes smoke.json with the measured time per step and the full run's estimate.
--full runs the three cases; after each case its results are written (results_<case>.json, snapshots_<case>.npz, <case>.png).
Every line printed carries the clock time (UTC) and the time elapsed since start, for the live monitor.
"""
import argparse, json, os, sys, time, datetime
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mpm2d as M
import jax, jax.numpy as jnp

T0 = time.time()


def say(s):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
    print(f"[{now} UTC | +{time.time() - T0:7.1f} s] {s}", flush=True)


CASES = {
    "main": dict(cpic=True, band=None, push=0.0, T=2.0),
    "control_untagged": dict(cpic=False, band=(0.015, 0.060), push=5.0, T=0.5),
    "control_tagged": dict(cpic=True, band=(0.015, 0.060), push=5.0, T=0.5),
}
T_PUSH = 0.2


def build(name, profile):
    cs = CASES[name]; P = M.default_params(); P["cpic"] = cs["cpic"]
    G = M.Glass2D(profile, P); Gr = M.Grid2D(G, P)
    p = M.seed(G, P, outer_band=cs["band"])
    st = M.to_state(p, P)
    tag0, _ = M.tag_of(G, st["x"][:, 0], st["x"][:, 1])
    g = P["g"]; push = cs["push"]

    def body(t):
        bx = jnp.where(t < T_PUSH, push, 0.0)
        return jnp.stack([bx, -g * jnp.ones_like(bx)]).astype(M.F32)

    step = M.make_step(G, Gr, P)
    return P, G, Gr, st, tag0, step, body


def run(name, profile, out, smoke):
    cs = CASES[name]
    P, G, Gr, st, tag0, step, body = build(name, profile)
    spc = int(round(1e-3 / P["dt"]))                     # 84 steps per 1 ms check
    chunk = M.make_chunk(step, spc, body)
    N = int(st["x"].shape[0])
    say(f"{name}: N = {N} particles, grid {Gr.nx} x {Gr.nz}, dt = {P['dt']:.3e} s, {spc} steps per check, cpic = {P['cpic']}")
    d0 = M.diagnostics(G, Gr, P, st, tag0)
    say(f"{name}: start {json.dumps(d0)}")
    if smoke:
        nchk = int(np.ceil(1000 / spc))
        st1, _, _ = chunk(st, jnp.float32(0.0)); jax.block_until_ready(st1["x"])        # compile
        tc = time.time()
        s = st
        for k in range(nchk):
            s, cr, cp = chunk(s, jnp.float32(k * spc * P["dt"]))
        jax.block_until_ready(s["x"]); el = time.time() - tc
        ms = 1e3 * el / (nchk * spc)
        full_s = ms * 1e-3 * cs["T"] / P["dt"]
        d1 = M.diagnostics(G, Gr, P, s, tag0)
        say(f"{name}: smoke {nchk * spc} steps in {el:.1f} s = {ms:.3f} ms/step; full {cs['T']} s needs about {full_s / 60:.1f} min; {json.dumps(d1)}")
        return dict(case=name, N=N, steps=nchk * spc, ms_per_step=ms, full_estimate_min=full_s / 60, end=d1, finite=bool(np.isfinite(np.asarray(s["x"])).all()))
    nchk = int(round(cs["T"] / 1e-3))
    ever = np.zeros(N, bool); rows = []; snaps = {}; t_snap = {0, nchk // 4, nchk // 2, nchk}
    snaps["x_0"] = np.asarray(st["x"]); snaps["phi"] = np.asarray(st["phi"])
    s = st; tc = time.time(); maxcap = 0
    for k in range(nchk):
        s, cr, cp = chunk(s, jnp.float32(k * spc * P["dt"]))
        cr = np.asarray(cr); ever |= cr; maxcap = max(maxcap, int(cp))
        if True:                                 # every 1 ms check: side changes are recorded at every step inside the chunk
            d = M.diagnostics(G, Gr, P, s, tag0)
            d.update(t=(k + 1) * 1e-3, crossed_in_window=int(cr.sum()), crossed_ever=int(ever.sum()), capped_max=maxcap)
            rows.append(d)
            if (k + 1) % 100 == 0 or k == nchk - 1:
                say(f"{name}: t = {(k + 1) * 1e-3:.3f} s  crossed {int(ever.sum())}  out_from_in {d['outside_from_inside']}  "
                    f"in_solid {d['n_in_solid']}  |J-1| {d['J_err_stout']:.2e}/{d['J_err_head']:.2e}  iso {d['isolated']}  "
                    f"vmax {d['vmax']:.3f}  ({time.time() - tc:.0f} s)")
        if (k + 1) in t_snap:
            snaps[f"x_{k + 1}"] = np.asarray(s["x"])
    if not np.isfinite(np.asarray(s["x"])).all():
        say(f"{name}: NaN in positions")
    crossed = int(ever.sum()); out_from_in = max(r["outside_from_inside"] for r in rows)
    if name == "control_untagged":
        verdict = "LEAKS (control discriminates)" if crossed > 0 else "NO LEAK: the test does not discriminate"
    else:
        verdict = "PASS" if (crossed == 0 and (out_from_in == 0 or name != "main")) else "FAIL"
    res = dict(case=name, params={k: (v if not isinstance(v, float) or np.isfinite(v) else "inf") for k, v in P.items()},
               N=N, T=cs["T"], push=cs["push"], t_push=T_PUSH, band=cs["band"], checks=nchk,
               crossed_ever=crossed, outside_from_inside_max=out_from_in, verdict=verdict,
               J_err_stout_max=max(r["J_err_stout"] for r in rows), J_err_head_max=max(r["J_err_head"] for r in rows),
               min_sdf_mm=min(r["min_sdf_mm"] for r in rows), isolated_max=max(r["isolated"] for r in rows),
               vmax_max=max(r["vmax"] for r in rows), c_over_vmax=P["c"] / max(1e-9, max(r["vmax"] for r in rows)),
               capped_max=maxcap, mass_start=d0["mass"], mass_end=rows[-1]["mass"], N_end=rows[-1]["N"],
               wall_time_s=time.time() - tc, rows=rows)
    json.dump(res, open(os.path.join(out, f"results_{name}.json"), "w"), indent=1)
    np.savez_compressed(os.path.join(out, f"snapshots_{name}.npz"), **snaps)
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        ks = sorted(int(k[2:]) for k in snaps if k.startswith("x_"))
        fig, ax = plt.subplots(1, len(ks), figsize=(4 * len(ks), 5), sharey=True)
        T = Gr.np_true
        for a, kk in zip(np.atleast_1d(ax), ks):
            a.contourf(Gr.X * 1e3, Gr.Z * 1e3, T, levels=[-1, 0], colors=["0.75"])
            xx = snaps[f"x_{kk}"]; hd = snaps["phi"] >= M.PHI_JAM
            a.scatter(xx[~hd, 0] * 1e3, xx[~hd, 1] * 1e3, s=0.2, c="#2b1a12"); a.scatter(xx[hd, 0] * 1e3, xx[hd, 1] * 1e3, s=0.2, c="#d9c8a0")
            a.set_title(f"{name}  t = {kk * 1e-3:.2f} s"); a.set_aspect("equal"); a.set_xlim(-100, 100); a.set_ylim(-40, 160); a.set_xlabel("x [mm]")
        np.atleast_1d(ax)[0].set_ylabel("z [mm]")
        fig.tight_layout(); fig.savefig(os.path.join(out, f"{name}.png"), dpi=110); plt.close(fig)
    except Exception as e:                       # the picture is a convenience; the verdict is in the json
        say(f"{name}: picture failed: {e}")
    say(f"{name}: {verdict}; crossed {crossed}, out_from_in {out_from_in}, |J-1| max {res['J_err_stout_max']:.2e} (stout) "
        f"{res['J_err_head_max']:.2e} (head), deepest {res['min_sdf_mm']:.3f} mm, isolated max {res['isolated_max']}, c/vmax {res['c_over_vmax']:.0f}")
    return res


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--profile", required=True); ap.add_argument("--out", required=True)
    g = ap.add_mutually_exclusive_group(required=True); g.add_argument("--smoke", action="store_true"); g.add_argument("--full", action="store_true")
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    say(f"A.0 start; jax {jax.__version__} on {jax.devices()[0].device_kind}")
    if a.smoke:
        res = [run(n, a.profile, a.out, True) for n in CASES]
        tot = sum(r["full_estimate_min"] for r in res)
        json.dump(dict(cases=res, full_total_estimate_min=tot), open(os.path.join(a.out, "smoke.json"), "w"), indent=1)
        say(f"smoke done; full A.0 estimate {tot:.1f} min of stepping (plus compile)")
        return
    order = ["control_untagged", "control_tagged", "main"]
    summary = {}
    for n in order:
        r = run(n, a.profile, a.out, False); summary[n] = r["verdict"]
        json.dump(summary, open(os.path.join(a.out, "summary.json"), "w"), indent=1)
        if n == "control_untagged" and r["crossed_ever"] == 0:
            say("control_untagged did not leak: A.0 is not discriminating as built. Stopping.")
            break
    say(f"A.0 done: {json.dumps(summary)}")


if __name__ == "__main__":
    main()
