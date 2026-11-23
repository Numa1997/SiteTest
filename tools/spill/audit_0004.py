"""Instruction 0004 (23 Nov 2026): the energy-closure audit of test 4.5, measurement only. Kaggle CPU. Run from the repository's root:
    python3 tools/spill/audit_0004.py OUTDIR      (env SUBRUN = "smoke" or "full"; DX default 0.003; ONLY e.g. "rot,slab,ident,slosh")
Blocks, each guarded, results to OUTDIR/audit_0004/:
  rot    the rigid-rotation check: one particle, C = Omega (rotation about z, D = 0), Omega 30 rad/s, dt 7.67e-4 s, 1000 steps from
         be = I, through stout_jax.evp_return_map: max s and E_plastic per unit volume (V = 1 m^3).
  slab   test (a): tools/spill/step4_slab.py, 4.3 case C1 (h 0.018 m, dx 1.5 mm, tau_b 1.5 tau_y, no vertical jitter, 2.0 s) with
         EAUDIT=1 (window 1.0-2.0 s).
  ident  the default path is unchanged: N_IDENT steps of the 4.5 set-up at DX with stout_jax at 5acb718 (tools/fig12/kaggle/
         stout_jax_5acb718.py, embedded by the launcher) and with the current stout_jax, audit off: every state array compared bit for bit.
  slosh  tests (b), (c), (d)-ledger: the 4.5 set-up (Fig. 16 deck, model "wall", head_mode "evp", gamma 0, side visibility, solid
         extension, wall guard, lip 1.25 mm) at DX, the same push (3.4 m/s^2 half-sine 0.15 s from 0.05 s), dt = min(2e-3, 0.8 dx / vmax,
         0.40 dx / c_s), never cut, to the first step with t >= 1.0 s, with S.audit = True (stout_jax.Stout._audit_evp); per-step JSONL."""
import json, os, sys, time, math, datetime, subprocess, traceback, importlib.util, hashlib
import numpy as np
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
KDIR = os.path.join(ROOT, "tools", "fig12", "kaggle"); sys.path.insert(0, KDIR)
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import stout_jax as SJ  # noqa: E402
SUB = os.environ.get("SUBRUN", "smoke"); DXA = float(os.environ.get("DX", "0.003")); ONLY = os.environ.get("ONLY", "rot,slab,ident,slosh").split(",")
VOUT = os.path.join(OUT, "audit_0004"); os.makedirs(VOUT, exist_ok=True)
T0 = time.time()
js = open(os.path.join(ROOT, "public", "scripts", "guinness-glass.js")).read()
RG = np.array([float(v) for v in js.split("R: [")[1].split("]")[0].split(",")]); DZP, FILL = 0.0005, 0.125; F16 = (0.155, 0.062, -0.030)


def say(m):
    line = f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')} UTC | +{time.time() - T0:7.1f} s] {m}"
    print(line, flush=True); open(os.path.join(VOUT, f"progress_{SUB}.log"), "a").write(line + "\n")


def dump(name, obj):
    json.dump(obj, open(os.path.join(VOUT, name), "w"), indent=1, default=str)


def setup(mod, dxd, audit):
    G = mod.Geometry(RG, DZP, FILL, dxd, body=F16, top=0.08, lip=0.00125)
    S = mod.Stout(G, model="wall", K_frac=1.0, M_drops=4096, head_mode="evp"); S.gamma = 0.0
    S.enable_side_vis(); info = S.enable_ls_extend(); S.wall_guard = True
    if audit: S.audit = True; S.diag_g2p = True
    s = S.init_state()
    if audit: s = dict(s, be_cell=jnp.tile(jnp.asarray([1, 1, 1, 0, 0, 0], jnp.float32), (S.N, 1)))
    return G, S, s, info


say(f"start {SUB}: DX {DXA}, blocks {ONLY}, device {jax.devices()[0]}, jax {jax.__version__}")

# ------------------------------------------------------------------------------------------------ rot
if "rot" in ONLY:
    try:
        Om, dt, n = 30.0, 7.67e-4, 1000
        C = jnp.asarray([[[0.0, -Om, 0.0], [Om, 0.0, 0.0], [0.0, 0.0, 0.0]]], jnp.float32)
        be = jnp.asarray([[1, 1, 1, 0, 0, 0]], jnp.float32); rm = jax.jit(lambda b: SJ.evp_return_map(b, C, dt))
        smax = 0.0; epl = 0.0; first_yield = None; rows = []
        for k in range(1, n + 1):
            be, y, gp, s_new, det, res = rm(be)
            sv = float(s_new[0]); smax = max(smax, sv); e = float(y[0]) * sv * float(gp[0]) * dt; epl += e
            if bool(y[0]) and first_yield is None: first_yield = k
            if k % 50 == 0 or k <= 3: rows.append(dict(step=k, s=sv, yielded=bool(y[0]), gp=float(gp[0]), E_plastic_cum=epl, det=float(det[0])))
        pred = SJ.G_HEAD * (Om * dt) ** 2 / math.sqrt(3.0)
        out = dict(Omega=Om, dt=dt, steps=n, V_p_m3=1.0, max_s_rot_Pa=smax, E_plastic_rot_J_per_m3=epl, first_yield_step=first_yield, tau_y=SJ.TAU_Y,
                   predicted_s_increment_per_step_Pa=pred, rows=rows,
                   pass_marks=dict(max_s_rot_lt_0p05_tau_y=bool(smax < 0.05 * SJ.TAU_Y), E_plastic_rot_eq_0=bool(epl == 0.0)))
        dump("rotation_check.json", out); say(f"rot: max_s {smax:.4f} Pa, E_plastic {epl:.4e} J/m^3, first yield step {first_yield}")
    except Exception as ex:
        say(f"rot FAILED: {ex!r}"); traceback.print_exc(); dump("rotation_check.json", dict(error=repr(ex)))

# ------------------------------------------------------------------------------------------------ slab (test a)
if "slab" in ONLY:
    try:
        env = dict(os.environ, JAX_PLATFORMS="cpu", SUBRUN=SUB, ONLY="4.3", HH="0.018", JITZ="0", T43="2.0", DX="0.0015", FRAC43="1.5", EAUDIT="1")
        if SUB == "smoke": env.update(EAUD_T0="0.005", EAUD_T1="0.012")
        say(f"slab: step4_slab.py C1 with EAUDIT=1 ({SUB})")
        r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "spill", "step4_slab.py"), VOUT], env=env, capture_output=True, text=True)
        open(os.path.join(VOUT, f"slab_{SUB}.log"), "w").write(r.stdout + r.stderr); say(f"slab rc {r.returncode}")
    except Exception as ex:
        say(f"slab FAILED: {ex!r}"); traceback.print_exc()

# ------------------------------------------------------------------------------------------------ ident (default path unchanged)
if "ident" in ONLY:
    try:
        p_old = os.path.join(KDIR, "stout_jax_5acb718.py")
        spec = importlib.util.spec_from_file_location("stout_jax_5acb718", p_old); SO = importlib.util.module_from_spec(spec); spec.loader.exec_module(SO)
        nid = int(os.environ.get("N_IDENT", "3")); hashes = {}
        for tag, mod, au_ in (("old_5acb718", SO, False), ("new_audit_off", SJ, False), ("new_audit_on", SJ, True)):
            G, S, s, _ = setup(mod, DXA, au_)
            prep = jax.jit(S.prepare); step = jax.jit(lambda s, pr, dt, gx: S.step(s, dt, gx, -9.81, prep=pr))
            cs = math.sqrt(mod.G_HEAD / mod.RHO_HEAD); dt_el = 0.40 * DXA / cs; t = 0.0; vmax = 0.0
            for k in range(nid):
                dt = min(2e-3, dt_el, 0.8 * DXA / max(vmax, 1e-12)); s, d = step(s, prep(s), dt, 0.0); t += dt; vmax = float(d["vmax"])
            hashes[tag] = {kk: hashlib.sha256(np.ascontiguousarray(np.asarray(v)).tobytes()).hexdigest() for kk, v in sorted(s.items())}
            say(f"ident {tag}: {nid} steps, t {t:.6f}")
        same = {kk: hashes["old_5acb718"][kk] == hashes["new_audit_off"].get(kk) for kk in hashes["old_5acb718"]}
        mot = ("xp", "vp", "C", "be", "act", "p", "wh")
        out_on = {kk: hashes["old_5acb718"][kk] == hashes["new_audit_on"].get(kk) for kk in mot}
        out = dict(audit_on_motion_identical=out_on, steps=nid, dx=DXA, old_sha256_of_file=hashlib.sha256(open(p_old, "rb").read()).hexdigest(), keys=same, all_identical=all(same.values()),
                   extra_keys_new=sorted(set(hashes["new_audit_off"]) - set(hashes["old_5acb718"])))
        dump("default_path_identity.json", out); say(f"ident: all identical {out['all_identical']}")
    except Exception as ex:
        say(f"ident FAILED: {ex!r}"); traceback.print_exc(); dump("default_path_identity.json", dict(error=repr(ex)))

# ------------------------------------------------------------------------------------------------ slosh (tests b, c, d-ledger)
if "slosh" in ONLY:
    rows = []
    try:
        PA, PT, P0, T = 3.4, 0.15, 0.05, 1.0
        G, S, s, info = setup(SJ, DXA, True)
        cs = math.sqrt(SJ.G_HEAD / SJ.RHO_HEAD); dt_el = 0.40 * DXA / cs
        say(f"slosh: grid {G.nx} x {G.ny} x {G.nz}, N {S.N} (stout {S.N_stout}, head {S.N_head}), m_stout0 {S.m_stout0:.6f} kg, m_head0 {S.m_head0:.6f} kg, "
            f"V_head {S.V_head:.4e} m^3, m_floor {S.m_floor:.4e} kg, dt_el {dt_el:.4e} s")
        prep = jax.jit(S.prepare); step = jax.jit(lambda s, pr, dt, gx: S.step(s, dt, gx, -9.81, prep=pr))
        f6 = lambda v: float(v)
        KE0 = 0.5 * float(jnp.sum(s["pmass"].astype(jnp.float64) * jnp.sum(s["vp"].astype(jnp.float64) ** 2, 1)))
        PE00 = 9.81 * float(jnp.sum(s["pmass"].astype(jnp.float64) * s["xp"][:, 2].astype(jnp.float64)))
        rows.append(dict(step=0, t=0.0, KE_p=KE0, PE=PE00, U_el=0.0))
        fh = open(os.path.join(VOUT, f"slosh_audit_{SUB}.jsonl"), "w"); fh.write(json.dumps(rows[0]) + "\n")
        t = 0.0; k = 0; vmax = 0.0; nmax = 5 if SUB == "smoke" else 10 ** 9; tc = time.time()
        keys = ("dE_P2G", "dE_visc", "dE_wall", "dE_dev", "dE_grav_proj", "dE_G2P_coll", "dE_mech", "W_sg_mfloor", "E_drop", "W_trial",
                "E_pl_mfloor", "E_pl_wall", "E_pl_interior", "E_pl_cellD")
        while t < T - 1e-12 and k < nmax:
            dt = min(2e-3, dt_el, 0.8 * DXA / max(vmax, 1e-12))
            tm = t + 0.5 * dt; gx = PA * math.sin(math.pi * (tm - P0) / PT) if P0 <= tm < P0 + PT else 0.0
            s, d = step(s, prep(s), dt, gx); t += dt; k += 1; vmax = float(d["vmax"])
            row = dict(step=k, t=t, dt=dt, gx=gx, it=int(d["it"]), res=f6(d["res"]), conv=bool(d["conv"]), KE_p=f6(d["aud_KE_p"]), PE=f6(d["aud_PE"]),
                       U_el=f6(d["aud_U_el"]), e_plastic=f6(d["e_plastic"]), e_wall_foam=f6(d["e_wall_foam"]), e_wall_stout=f6(d["e_wall_stout"]),
                       **{k_: f6(d["aud_" + k_]) for k_ in keys}, n_yielded=int(d["n_yielded"]), ny_mfloor=int(d["aud_ny_mfloor"]), ny_wall=int(d["aud_ny_wall"]),
                       ny_interior=int(d["aud_ny_interior"]), ny_cellD=int(d["aud_ny_cellD"]), n_head_mfloor=int(d["aud_n_head_mfloor"]),
                       n_head_wall=int(d["aud_n_head_wall"]), n_floor=int(d["n_floor"]), s_max=f6(d["s_max"]), s_max_cellD=f6(d["aud_s_max_cellD"]),
                       det_min=f6(d["det_min"]), det_max=f6(d["det_max"]), n_gone=int(d["aud_n_gone"]), vmax=vmax, wall_s=round(time.time() - tc, 2))
            rows.append(row); fh.write(json.dumps(row) + "\n"); fh.flush()
            if k < 3 or k % 50 == 0: say(f"slosh: step {k}  t {t:.4f}  gx {gx:.3f}  it {row['it']}  KE {row['KE_p']:.4e}  U_el {row['U_el']:.4e}  "
                                         f"yielded {row['n_yielded']}  ({row['wall_s']:.0f} s)")
        fh.close(); say(f"slosh: {k} steps to t {t:.5f} in {time.time() - tc:.0f} s")
    except Exception as ex:
        say(f"slosh FAILED at step {len(rows)}: {ex!r}"); traceback.print_exc()
    try:   # the window's numbers (Neon section 5) and the marks (STATE-projection-fix.md, "0004 step 5")
        ta, tb = (0.2, 1.0) if SUB == "full" else (rows[2]["t"], rows[-1]["t"])
        ia = next(i for i, r in enumerate(rows) if r["t"] >= ta - 1e-12); ib = next(i for i, r in enumerate(rows) if r["t"] >= tb - 1e-12)
        W = lambda key: sum(r[key] for r in rows[ia + 1:ib + 1]); A, B = rows[ia], rows[ib]
        dKE = B["KE_p"] - A["KE_p"]; dPE = B["PE"] - A["PE"]; dU = B["U_el"] - A["U_el"]; dEm = dKE + dPE; dEt = dEm + dU
        Ep, Ewf, Ews = W("e_plastic"), W("e_wall_foam"), W("e_wall_stout"); Ev = -W("dE_visc"); Wsg = -W("dE_dev"); Wc = dU + Ep
        sinks = Ep + Ewf + Ews; sinks_all = sinks + Ev; led = sum(W(k_) for k_ in ("dE_P2G", "dE_visc", "dE_wall", "dE_dev", "dE_grav_proj", "dE_G2P_coll"))
        r_ = lambda x, y: x / y if y else float("nan")
        tab = dict(t_a=A["t"], t_b=B["t"], step_a=A["step"], step_b=B["step"], minus_dKE=-dKE, minus_dPE=-dPE, minus_dU_el=-dU, minus_dE_mech=-dEm, minus_dE_tot=-dEt,
                   PE_drift_tb_minus_0=B["PE"] - rows[0]["PE"], U_el_a=A["U_el"], U_el_b=B["U_el"], U_el_min=min(r["U_el"] for r in rows),
                   E_plastic=Ep, E_drop=W("E_drop"), W_trial=W("W_trial"), E_wall_foam=Ewf, E_wall_stout=Ews, E_visc_stout=Ev, W_stress_grid=Wsg,
                   W_stress_grid_on_mfloor_faces=W("W_sg_mfloor"), W_constit=Wc, W_constit_over_W_stress_grid=r_(Wc, max(Wsg, 1e-12)),
                   E_plastic_mfloor=W("E_pl_mfloor"), E_plastic_wall=W("E_pl_wall"), E_plastic_interior=W("E_pl_interior"), E_plastic_cellD=W("E_pl_cellD"),
                   E_plastic_minus_cellD=Ep - W("E_pl_cellD"), E_num=-dEt - sinks_all, sinks_logged=sinks, sinks_all=sinks_all,
                   sinks_over_minus_dE_mech=r_(sinks, -dEm), r_tot=r_(sinks, -dEt), closure_all_over_minus_dE_tot=r_(sinks_all, -dEt),
                   ledger=dict(dE_P2G=W("dE_P2G"), dE_visc=W("dE_visc"), dE_wall=W("dE_wall"), dE_dev=W("dE_dev"), dE_grav_proj=W("dE_grav_proj"),
                               dE_G2P_coll=W("dE_G2P_coll"), sum=led, dE_mech_stores=dEm, dE_mech_steps=W("dE_mech")),
                   n_floor_max_window=max(r["n_floor"] for r in rows[ia + 1:ib + 1]), n_gone_total=sum(r.get("n_gone", 0) for r in rows))
        pm = dict(b_U_el_min_ge_m1e12=bool(tab["U_el_min"] >= -1.0e-12), b_U_el_a_gt_b=bool(A["U_el"] > B["U_el"]),
                  b_alone_explains=bool(tab["sinks_over_minus_dE_mech"] > 1.25 and tab["r_tot"] <= 1.02 and abs(tab["r_tot"] - 1.0) < 0.25),
                  b_partial_only_r_tot_gt_1p05=bool(tab["r_tot"] > 1.05),
                  c_adjoint_within_5pct=bool(abs(Wc / max(Wsg, 1.0e-12) - 1.0) < 0.05), c_proved_ratio_gt_1p15=bool(Wc / max(Wsg, 1.0e-12) > 1.15),
                  d_telescoping_lt_1e7=bool(abs(led - dEm) < 1.0e-7), d_wall_logger_within_2pct=bool(abs(r_(-W("dE_wall"), Ewf + Ews) - 1.0) < 0.02),
                  d_grav_proj_le_2pct=bool(W("dE_grav_proj") <= 0.02 * (-dEm)), d_G2P_coll_le_2pct=bool(W("dE_G2P_coll") <= 0.02 * (-dEm)))
        tab["telescoping_abs_J"] = abs(led - dEm); tab["wall_logger_ratio"] = r_(-W("dE_wall"), Ewf + Ews)
        dump(f"slosh_audit_{SUB}_summary.json", dict(sub=SUB, dx=DXA, steps=len(rows) - 1, window_requested=[ta, tb], table=tab, pass_marks=pm))
        say(f"slosh window: {json.dumps(tab)}"); say(f"slosh marks: {json.dumps(pm)}")
    except Exception as ex:
        say(f"slosh summary FAILED: {ex!r}"); traceback.print_exc()
say("all done")
