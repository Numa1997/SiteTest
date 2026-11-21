"""Step 4, the 4.3 plug-flow diagnostic of 21 Nov 2026 (instruction "step4-diag-and-cpu-smoke", Part A). Kaggle CPU only.
Does the seed's layering explain 4.3's -9.4 % (1.5 mm) and +7.7 % (0.75 mm)? The original slab (h = 0.019 m) puts round(h / (dx/2))
layers at spacing h / that number: 25 layers (1.0133 cell volumes per sheared cell) at 1.5 mm, 51 (0.9935) at 0.75 mm. Here h = 0.018 m
(a whole number of layers on both grids) and no vertical jitter. Cases, each 2.0 s: C1 dx 1.5 mm, 1.5 tau_y (exact 1.3424e-3 m/s);
C2 dx 0.75 mm, same load; C3 dx 1.5 mm, 1.6 tau_y (z_y mid-cell, exact 2.1454e-3 m/s). Also the quadrature numbers of the original
h = 0.019 m seeds at both grids. Writes OUTDIR/step4/diag_4p3.json. Run: python3 tools/spill/step4_diag43.py OUTDIR (SUBRUN smoke | full)."""
import json, os, subprocess, sys, datetime, time, glob
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; SUB = os.environ.get("SUBRUN", "smoke")
HERE = os.path.dirname(os.path.abspath(__file__)); VOUT = os.path.join(OUT, "step4"); os.makedirs(VOUT, exist_ok=True)
T0 = time.time()


def say(m):
    print(f"[{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')} UTC | +{time.time() - T0:7.1f} s] {m}", flush=True)


def run(env):
    e = dict(os.environ, JAX_PLATFORMS="cpu", SUBRUN=SUB, **env)
    r = subprocess.run([sys.executable, os.path.join(HERE, "step4_slab.py"), OUT], env=e); return r.returncode


out = dict(sub=SUB, quad_original={}, cases={})
for dx in ("0.0015", "0.00075"):                   # the original h = 0.019 m seeds: numbers only
    try:
        run(dict(QUAD_ONLY="1", DX=dx)); tag = "" if dx == "0.0015" else "_dx0.75mm"
        out["quad_original"][dx] = json.load(open(os.path.join(VOUT, f"quad{tag}.json")))
    except Exception as ex:
        out["quad_original"][dx] = dict(error=repr(ex))
REF = dict(C1=1.3424e-3, C2=1.3424e-3, C3=2.1454e-3)
CASES = dict(C1=dict(DX="0.0015", FRAC43="1.5"), C2=dict(DX="0.00075", FRAC43="1.5"), C3=dict(DX="0.0015", FRAC43="1.6"))
for name, env in CASES.items():
    try:
        env = dict(env, ONLY="4.3", HH="0.018", JITZ="0", T43="2.0"); say(f"{name}: {env}")
        rc = run(env)
        dxtag = "" if env["DX"] == "0.0015" else "_dx0.75mm"; ftag = "" if env["FRAC43"] == "1.5" else f"_f{float(env['FRAC43']):g}"
        f = os.path.join(VOUT, f"slab_4.3{dxtag}_T2s_h18mm_jz0{ftag}_{SUB}_summary.json")
        o = json.load(open(f))
        c = dict(rc=rc, summary_file=os.path.basename(f), v_ref_given=REF[name], v_ref_computed=o.get("v_h_ref"), z_y_ref=o.get("z_y_ref"),
                 v_plug=o.get("v_plug_last0p2"), quadrature=o.get("quadrature"), n_floor_max=o.get("n_floor_max"), steps=o.get("steps"),
                 n_yielded_max=o.get("n_yielded_max"), det_dev_max=o.get("det_dev_max"), v_by_0p1s=o.get("v_h_by_0p1s"))
        if c["v_plug"] is not None: c["err"] = (c["v_plug"] - REF[name]) / REF[name]
        out["cases"][name] = c; say(f"{name}: {json.dumps(c)}")
    except Exception as ex:
        out["cases"][name] = dict(error=repr(ex)); say(f"{name} FAILED: {ex!r}")
    json.dump(out, open(os.path.join(VOUT, f"diag_4p3{'' if SUB == 'full' else '_' + SUB}.json"), "w"), indent=1)
if SUB == "full":
    try:
        C = out["cases"]; e1, e2, e3 = C["C1"]["err"], C["C2"]["err"], C["C3"]["err"]
        q1, q2 = C["C1"]["quadrature"], C["C2"]["quadrature"]
        out["pass_marks"] = dict(C1_err_lt_0p025=abs(e1) < 0.025, C2_err_lt_0p010=abs(e2) < 0.010, C2_lt_half_C1=abs(e2) < 0.5 * abs(e1),
                                 C3_err_lt_0p025=abs(e3) < 0.025,
                                 C1_C2_V_cell0_within_1e3=all(abs(q["V_cell_over_A_dx"][0] - 1) < 1e-3 for q in (q1, q2)),
                                 C1_C2_M_tot_within_1e4=all(abs(q["M_tot_over_rho_A_h"] - 1) < 1e-4 for q in (q1, q2)))
        out["pass_marks_all"] = all(out["pass_marks"].values())
        out["refutation"] = dict(rule="C1 or C2 error >= 0.03 while V_cell_0 within 1e-3 and the mass floor never acted -> quadrature explanation wrong",
                                 triggered=bool(any(abs(C[n]["err"]) >= 0.03 and abs(C[n]["quadrature"]["V_cell_over_A_dx"][0] - 1) < 1e-3 and C[n]["n_floor_max"] == 0
                                                    for n in ("C1", "C2"))))
    except Exception as ex:
        out["pass_marks_error"] = repr(ex)
    json.dump(out, open(os.path.join(VOUT, "diag_4p3.json"), "w"), indent=1)
say(f"done: {json.dumps(out.get('pass_marks'))}")
