"""Fig. 16: build public/simulations/guinness-cart-control.html from its source notes/fig16/page/guinness-cart-control.src.html, filling
every {{key}} with a number read from the stored data: the rides' index (public/data/fig16/2026-11-14/index-16.json), the run's summary
(notes/fig16/run16-v2-summary.json, downloaded from the Kaggle notebook's output), Fig. 12's index (public/data/fig12/2026-11-14-run10/
index-jax.json), the stored ride files, and the lecture note's derived numbers (notes/fig16/note-numbers.json, measured by
notes/fig16/note_numbers.py). No number in the page is typed by hand. The navigation is copied from Fig. 12's page with
Fig. 16 added. Run: python3 tools/fig16/build_page.py  (--check: fail if the page on disk differs from what would be built)."""
import json, math, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P = lambda *a: os.path.join(ROOT, *a)
I16 = json.load(open(P("public", "data", "fig16", "2026-11-14", "index-16.json")))
I12 = json.load(open(P("public", "data", "fig12", "2026-11-14-run10", "index-jax.json")))
S = json.load(open(P("notes", "fig16", "run16-v2-summary.json")))
f16 = {f["path"][:-5]: f for f in I16["files"]}
# run 3 and run 4b (15 November 2026: the turning deck's forces, 60 stored pictures a second, control off on every road, the volume
# correction for the uncontrolled rides): where a ride was computed again, the new one is used
I16B = json.load(open(P("public", "data", "fig16", "2026-11-15", "index-16.json"))); f16.update({f["path"][:-5]: f for f in I16B["files"]}); f12 = {f["path"][:-5]: f for f in I12["files"]}
task = {t["name"]: t for t in S["tasks"]}
C = S["cart"]; pl = S["plant"]
off = json.load(open(P("public", "data", "fig16", "2026-11-14", "kerb_off.json")))
kerb = json.load(open(P("public", "data", "fig16", "2026-11-14", "kerb_full.json")))
ml = kerb["books"]["stout_glass_g_end"] + kerb["books"]["head_ml0"] * 0.272 if "stout_glass_g_end" in kerb["books"] else kerb["stout_g"][0] + kerb["books"]["head_ml0"] * 0.272
rides = [t for t in S["tasks"] if t["kind"] == "ride"]
V = dict(
    Md=f"{C['Md']:.1f}", ml_g=f"{ml:.0f}", Rw_mm=f"{C['Rw'] * 1e3:.0f}", wb_mm=f"{(C['af'] + C['ar']) * 1e3:.0f}", k=f"{C['k']:.0f}", c=f"{C['c']:.0f}",
    f_bounce=f"{math.sqrt(C['k'] / ((C['Md'] + ml / 1e3) / 2)) / (2 * math.pi):.1f}", Umax=f"{C['Umax']:.0f}", b=f"{C['b']:.0f}", Imax=f"{C['Imax']:.0f}",
    Vmax=f"{C['Vmax']:.0f}", preview_s=f"{C['Np'] * C['Ts']:.2f}", Np=f"{C['Np']}", Ts_ms=f"{C['Ts'] * 1e3:.0f}", hg_mm=f"{C['hg'] * 1e3:.0f}",
    f0=f"{pl['f0']:.3f}", zeta=f"{pl['zeta']:.3f}", beta=f"{pl['beta']:.3f}",
    q_mm=f"{S['design']['chosen'].get('q', 0.0005) * 1e3:.2f}", th_deg=f"{math.degrees(S['design']['chosen'].get('th', 0.08)):.1f}",
    stroke_mm=f"{S['design']['chosen'].get('stroke', 0.020) * 1e3:.0f}", ncand=f"{len(S['design']['candidates'])}",
    nb_version=f"{I16['kaggle']['version']}", device=S["device"], rest_max_mm=f"{task['rest']['rest_guard']['max_dev_mm']:.2f}",
    head_err=f"{max(t['books']['head_err_ml_max'] for t in S['tasks']):.0e}".replace("e-0", " × 10⁻").replace("e-", " × 10⁻"),
    ms_step=f"{sum(t['ms_per_step'] for t in rides) / len(rides):.0f}",
    gpu_min=f"{sum(t['run_s'] + t['compile_s'] for t in S['tasks']) / 60:.0f}",
    f12_kerb_tilt=f"{f12['ride_sharp30_slosh']['measured']['tilt_max_mm']:.2f}", f12_kerb_head=f"{f12['ride_sharp30_slosh']['measured']['head_spilled_ml']:.2f}",
    f12_res_tilt=f"{f12['ride_resonant_joint']['measured']['tilt_max_mm']:.2f}", f12_res_head=f"{f12['ride_resonant_joint']['measured']['head_spilled_ml']:.2f}",
    f12_b25_tilt=f"{f12['ride_bump25_joint']['measured']['tilt_max_mm']:.2f}", f12_b25_head=f"{f12['ride_bump25_joint']['measured']['head_spilled_ml']:.2f}",
    f16_kerb_tilt=f"{f16['kerb_full']['measured']['tilt_max_mm']:.2f}", f16_kerb_head=f"{f16['kerb_full']['measured']['head_spilled_ml']:.3f}",
    f16_res_tilt=f"{f16['resonant_full']['measured']['tilt_max_mm']:.2f}", f16_res_head=f"{f16['resonant_full']['measured']['head_spilled_ml']:.2f}",
    f16_b25_tilt=f"{f16['bump25_full']['measured']['tilt_max_mm']:.2f}", f16_b25_head=f"{f16['bump25_full']['measured']['head_spilled_ml']:.2f}",
    f16_kerb_pitch=f"{f16['kerb_full']['measured']['pitch_max_deg']:.1f}", f16_kerb_i=f"{f16['kerb_full']['measured']['i_max_A']:.0f}",
    f16_kerb_u=f"{f16['kerb_full']['measured']['u_max_N']:.1f}",
    off_pitch=f"{f16['kerb_off']['measured']['pitch_max_deg']:.0f}",
    off_head=f"{f16['kerb_off']['measured']['head_spilled_ml']:.1f}", off_stout=f"{f16['kerb_off']['measured']['spilled_g']:.0f}",
    off_res_head=f"{f16['resonant_off']['measured']['head_spilled_ml']:.1f}", off_res_stout=f"{f16['resonant_off']['measured']['spilled_g']:.0f}",
    off_res_pitch=f"{f16['resonant_off']['measured']['pitch_max_deg']:.0f}", off_b25_head=f"{f16['bump25_off']['measured']['head_spilled_ml']:.1f}",
    off_b25_stout=f"{f16['bump25_off']['measured']['spilled_g']:.0f}", off_b25_pitch=f"{f16['bump25_off']['measured']['pitch_max_deg']:.0f}",
    seed2_tilt=f"{f16['kerb_full_seed2']['measured']['tilt_max_mm']:.2f}", seed2_head=f"{f16['kerb_full_seed2']['measured']['head_spilled_ml']:.3f}",
    head0_ml=f"{json.load(open(P('public', 'data', 'fig16', '2026-11-15', 'kerb_off.json')))['books']['head_ml0']:.0f}",
)
# the lecture note's derived numbers (15 November 2026): measured by notes/fig16/note_numbers.py from cart4.py, the glass profile and
# the stored rides, written to notes/fig16/note-numbers.json; here they are only formatted
NN = {k: v["value"] for k, v in json.load(open(P("notes", "fig16", "note-numbers.json"))).items()}
src4 = open(P("tools", "fig16", "kaggle", "cart4.py")).read(); src16 = open(P("tools", "fig16", "kaggle", "run16.py")).read()
srcb = open(P("tools", "fig12", "kaggle", "run_b.py")).read(); srcs = open(P("tools", "fig12", "kaggle", "stout_jax.py")).read()
num = lambda pat, s: float(re.search(pat, s, re.M).group(1))
Wa, sq = (float(x) for x in re.search(r"Wa, sq = ([0-9.e-]+), ([0-9.e-]+)", src4).groups())
f1 = lambda x, k=1: f"{x:.{k}f}"
R_ = {n: NN["ride_" + n] for n in ("kerb_full", "kerb_full_seed2", "kerb_off", "resonant_off", "bump25_off")}
M_ = NN["modes_here"]; M16 = NN["modes16"]
heave_fn = M_[1]["f_nat"]
# Table 3: the design step's candidates, as stored in the index
def cand_label(w):
    if not w: return f"nothing (the values of section 5.1 with a swing of {num(r'q=([0-9.]+), qd=', src4) * 1e3:.2f} mm)"
    names = dict(q=("swing", 1e3, "mm", 2), th=("pitch", 180 / math.pi, "°", 1), stroke=("strokes", 1e3, "mm", 0), u=("actuator forces", 1, "N", 0))
    return ", ".join(f"{names[k][0]} {v * names[k][1]:.{names[k][3]}f} {names[k][2]}".replace(" °", "°") for k, v in w.items())
cands = I16B["design"]["candidates"]; chosen = I16B["design"]["chosen"]
cand_rows = "\n                            ".join(
    f"<tr><td>{cand_label(c['weights'])}{' (kept)' if c['weights'] == chosen else ''}</td><td>{c['wall_mm']:.2f} mm</td><td>{c['tilt_mm']:.2f} mm</td><td>{c['pitch_deg']:.1f}°</td></tr>" for c in cands)
cand_chosen = next(c for c in cands if c["weights"] == chosen)
sw = NN["swelling"]; Wt = NN["weights"]; ms_on = NN["ms_step_on"]; ms_off = NN["ms_step_off"]
head_err_all = max(f["measured"]["books"]["head_err_ml_max"] for I in (I16, I16B) for f in I["files"])
ex_th, ex_ax, ex_al, ex_brake = 0.01, 0.2, 1.0, 2.0     # inputs of the worked check of eq. (6) and of Problem 9.3 (the same as note_numbers.py)
late = NN["late_seed1"]
SUB = num(r"dt / ([0-9.e-]+)\)", src16); DTMAX = num(r"dtmax=([0-9.]+)", src16); CFL = num(r"cfl=([0-9.]+)", src16)
REST = num(r'name="rest", kind="free", end=end_\(([0-9.]+)\)', src16); GATE = num(r'swelling\(liq, s\["act"\]\) - ([0-9.]+)\)', srcs)
V.update(
    F12_max=f1(NN["F12_max"], 2), J0=f"{C['J0']:.4f}", af_mm=f"{C['af'] * 1e3:.0f}", ar_mm=f"{C['ar'] * 1e3:.0f}", hs_mm=f"{C['hs'] * 1e3:.0f}",
    d_mm=f"{C['d'] * 1e3:.0f}", mf=f"{C['mf']:.2f}", mr=f"{C['mr']:.2f}", Iw=f"{C['Iw']:.4f}", smax_mm=f"{C['smax'] * 1e3:.0f}", kt=f"{C['kt']:,.0f}",
    ct=f"{C['ct']:.0f}", tauU_ms=f"{C['tauU'] * 1e3:.0f}", nm=f"{C['nm']}", Ra=f"{C['Ra']:.1f}", tauI_ms=f"{C['tauI'] * 1e3:.0f}", mu=f"{C['mu']:.1f}",
    cx=f"{C['cx']:.0f}", Ms=f"{NN['st_Ms']:.3f}", Mx=f"{NN['st_Mx']:.3f}", J=f"{NN['st_J']:.4f}", Wf=f"{NN['st_Wf']:.2f}", sag_mm=f"{NN['static_sag_mm']:.1f}",
    k2=f"{2 * C['k']:.0f}", f_bounce1=f"{NN['f_bounce1']:.2f}", zeta_bounce1=f"{NN['zeta_bounce1']:.2f}", heave_fnat=f"{heave_fn:.2f}",
    heave_zeta=f"{M_[1]['zeta']:.2f}", heave_err_pct=f"{abs(NN['f_bounce1'] / heave_fn - 1) * 100:.0f}", k_theta=f"{NN['k_theta']:.2f}",
    f_pitch1=f"{NN['f_pitch1']:.2f}", g=f"{NN['g']:.2f}", zS_mm=f"{NN['zS_mm']:.0f}",
    check_aS_exact=f"{NN['check_aS']['exact']:.0e}".replace("e-0", " × 10⁻").replace("e-", " × 10⁻"), check_aS_code=f"{NN['check_aS']['code']:.2f}",
    gz_err_on=f"{NN['gz_err_kerb_full']:.2f}", gz_err_on_pct=f"{NN['gz_err_kerb_full'] / NN['g'] * 100:.0f}", gz_err_off=f"{NN['gz_err_kerb_off']:.1f}",
    a_min_off_abs=f"{-R_['kerb_off']['a_min']:.2f}", lean_off_deg=f"{R_['kerb_off']['lean_needed_deg']:.0f}", smax2_mm=f"{2 * C['smax'] * 1e3:.0f}",
    pitch_geom_deg=f"{NN['pitch_geom_deg']:.1f}", a_min_on_abs=f"{-R_['kerb_full']['a_min']:.2f}", lean_on_deg=f"{R_['kerb_full']['lean_needed_deg']:.0f}",
    g1deg=f"{NN['g'] * math.sin(math.radians(1)):.3f}", lin_exact=f"{NN['check_lin']['exact']:.5f}", lin_lin=f"{NN['check_lin']['lin']:.5f}",
    lin_th=f"{ex_th}", lin_ax=f"{ex_ax}", lin_al=f"{ex_al:.0f}",
    fill_mm=f"{num(r'^FILL, RHO = ([0-9.]+)', src16) * 1e3:.0f}", rho=f"{num(r'^FILL, RHO = [0-9.]+, ([0-9.]+)', src16):.0f}",
    head0_mm=f"{NN['head0_mm']:.0f}", zrim_mm=f"{NN['zrim_mm']:.1f}", freeboard_mm=f"{NN['freeboard_mm']:.1f}", R_fill_mm=f"{NN['R_fill_mm']:.1f}",
    tilt_head_deg=f"{NN['tilt_head_deg']:.1f}", tau_y=f"{NN['tau_y']:.2f}", e_break_mm=f"{NN['e_break_mm']:.2f}", phi_f=f"{NN['phi_f']:.2f}",
    tilt_break_deg=f"{math.degrees(math.atan((NN['freeboard_mm'] + NN['e_break_mm']) / NN['R_fill_mm'])):.1f}",
    rmax_mm=f"{NN['rmax_mm']:.0f}", om_on=f"{R_['kerb_full']['om_max']:.2f}", centr_on=f"{R_['kerb_full']['centr_rmax']:.2f}",
    om_off=f"{R_['kerb_off']['om_max']:.1f}", centr_off=f"{R_['kerb_off']['centr_rmax']:.1f}", al_on=f"{R_['kerb_full']['al_max']:.0f}",
    al_off=f"{R_['kerb_off']['al_max']:.0f}", omdot_on=f"{NN['omdot_fd_kerb_full']:.0f}", omdot_off=f"{NN['omdot_fd_kerb_off']:.0f}",
    check_rot=f"{NN['check_rot']:.0e}".replace("e-", " × 10⁻"), run3_run2_rms=f"{NN['run3_run2_rms']:.2f}", run3_run2_max=f"{NN['run3_run2_max']:.2f}",
    seed_rms30=f"{NN['seed_rms30']:.2f}", n_pics_30=f"{R_['kerb_full']['frames'] // 2 + 1}", kstop=f"{C['kstop']:,.0f}",
    **{f"m{i + 1}_fn": f"{M_[i]['f_nat']:.2f}" for i in range(5)}, **{f"m{i + 1}_f": f"{M_[i]['f']:.2f}" for i in range(5)},
    **{f"m{i + 1}_z": f"{M_[i]['zeta']:.2f}" for i in range(5)},
    m1_q=f"{M16[0]['share']['q']:.2f}", m2_zc=f"{M16[1]['share']['zc']:.2f}", m3_th=f"{M16[2]['share']['th']:.2f}", m3_q=f"{M16[2]['share']['q']:.2f}",
    m4_zr=f"{M16[3]['share']['zr']:.2f}", m5_zf=f"{M16[4]['share']['zf']:.2f}", f_hop_r1=f"{NN['f_hop_r1']:.1f}", f_hop_f1=f"{NN['f_hop_f1']:.1f}",
    five_f=f"{NN['five_f']:.2f}", wb_m=f"{(C['af'] + C['ar']):.2f}", five_pitch_drive=f"{NN['five_pitch_drive']:.2f}", five_heave_drive=f"{NN['five_heave_drive']:.2f}",
    m3_fpeak=f"{M_[2]['f_peak']:.2f}", five_ratio_pct=f"{NN['five_f'] / M_[2]['f_nat'] * 100:.0f}",
    bump_dx=f"{[b['x'] for b in eval(srcb[srcb.index('ROADS = {') + 8:srcb.index(chr(10) + '}' + chr(10), srcb.index('ROADS = {')) + 2])['five 20 mm bumps in step with the swing']['bumps']][1] - 1.5:.2f}",
    w_q_mm=f"{Wt['q'] * 1e3:.2f}", w_qd_mm=f"{Wt['qd'] * 1e3:.1f}", w_th_deg=f"{math.degrees(Wt['th']):.1f}", w_om=f"{Wt['om']:.1f}", w_zc_mm=f"{Wt['zc'] * 1e3:.0f}",
    w_vzc=f"{Wt['vzc']:.1f}", w_zw_mm=f"{Wt['zw'] * 1e3:.0f}", w_vzw=f"{Wt['vzw']:.0f}", w_stroke_mm=f"{Wt['stroke'] * 1e3:.0f}", w_dv=f"{Wt['dv']:.2f}",
    w_xi_mm=f"{Wt['xi'] * 1e3:.0f}", w_Fd=f"{Wt['Fd']:.0f}", w_u=f"{Wt['u']:.0f}",
    slowest=f"{NN['slowest_k']:.5f}", tau_slow=f"{NN['tau_slow_k']:.2f}", cl_f=f"{NN['cl_least_damped_k']['f']:.1f}", cl_z=f"{NN['cl_least_damped_k']['zeta']:.2f}",
    prev_opt=f"{NN['check_preview']['u_opt']:.6f}".replace("-", "−"), prev_formula=f"{NN['check_preview']['u_formula']:.6f}".replace("-", "−"),
    Kp100=f"{NN['Kp_norm_k']['ratio100']:.2f}", Kp249=f"{NN['Kp_norm_k']['ratio249']:.3f}", Wa=f"{Wa:.0f}", sq_mm=f"{sq * 1e3:.1f}",
    L1=f"{NN['Lk_k'][0]:.3f}", L2=f"{NN['Lk_k'][1]:.1f}", oneminusL1=f"{1 - NN['Lk_k'][0]:.3f}", dt_fluid_ms=f"{NN['dt_fluid_ms']:.2f}",
    kal_tau_ms=f"{NN['kal_tau_ms']:.1f}", T0_ms=f"{1e3 / NN['f0']:.0f}", E16=f"{NN['E16']:.1f}", i_volt16=f"{NN['i_volt16']:.1f}", F16_max=f"{NN['F16_max']:.0f}",
    Nr0=f"{NN['st_Nr0']:.2f}", grip_r=f"{NN['grip_r']:.1f}", air_rear=f"{NN['airborne']['rear']}", air_t0=f"{NN['airborne']['rear_t_first']:.2f}",
    air_t1=f"{NN['airborne']['rear_t_last']:.2f}", cand_rows=cand_rows, cand_tilt_chosen=f"{cand_chosen['tilt_mm']:.2f}",
    particles=f"{f16['kerb_full']['measured']['books']['stout_particles']:,}", dx_mm=f"{kerb['dx'] * 1e3:.1f}",
    substep_ms=f"{SUB * 1e3:.1f}", dtmax_ms=f"{DTMAX * 1e3:.0f}", cfl=f"{CFL:.1f}", rest_s=f"{REST:.0f}", gate_pct=f"{GATE * 100:.0f}",
    fps_old=f"{I12['files'][0].get('fps', 30) if 'fps' in I12['files'][0] else 30}", fps_new=f"{f16['kerb_full']['fps']}",
    v_kerb=f"{f16['kerb_full']['v0']:.1f}", v_res=f"{f16['resonant_off']['v0']:.1f}",
    head_err=f"{head_err_all:.1e}".replace("e-0", " × 10⁻").replace("e-", " × 10⁻"),
    ms_on=f"{sum(ms_on) / len(ms_on):.0f}", ms_off=f"{sum(ms_off) / len(ms_off):.0f}", lost_kerb_pct=f"{sw['kerb_off']['lost_frac'] * 100:.0f}",
    sw_off_kerb=f"{(sw['kerb_off']['ratio'] - 1) * 100:.1f}", sw_off_res=f"{(sw['resonant_off']['ratio'] - 1) * 100:.1f}",
    sw_off_b25=f"{(sw['bump25_off']['ratio'] - 1) * 100:.1f}", sw_on_kerb=f"{(sw['kerb_full']['ratio'] - 1) * 100:.2f}",
    seed_rms_mm=f"{NN['seed_rms_mm']:.2f}", n_pics_60=f"{R_['kerb_full']['frames']}", seed_max_mm=f"{NN['seed_max_mm']:.2f}",
    seed_head_a=f"{R_['kerb_full']['head_spill']:.3f}", seed_head_b=f"{R_['kerb_full_seed2']['head_spill']:.3f}",
    zeta_num=f"{NN['zeta_num']:.4f}", zeta_num_pct=f"{NN['zeta_num_share'] * 100:.1f}",
    stroke_f_min=f"{-NN['strokes_mm']['f_min']:.1f}", stroke_r_min=f"{-NN['strokes_mm']['r_min']:.1f}", t_tilt=f"{R_['kerb_full']['t_tilt_max']:.2f}",
    every2_even=f"{R_['kerb_full']['tilt_every2_even']:.2f}", every2_odd=f"{R_['kerb_full']['tilt_every2_odd']:.2f}",
    stout0_g=f"{R_['kerb_full']['stout0_g']:.0f}", off_kerb_tilt=f"{f16['kerb_off']['measured']['tilt_max_mm']:.0f}",
    off_res_tilt=f"{f16['resonant_off']['measured']['tilt_max_mm']:.0f}", off_b25_tilt=f"{f16['bump25_off']['measured']['tilt_max_mm']:.0f}",
    drops_page=f"{max(max(json.load(open(P('public', 'data', 'fig16', '2026-11-15', f['path'])))['nd']) for f in I16B['files']):,}",
    late_t=f"{late['yq_jump_t']:.1f}", late_yq_min=f"{late['yq_min']:.2f}".replace("-", "−"), late_yq_max=f"{late['yq_max']:.2f}", late_du=f"{late['du_max']:.1f}",
    late_du_before=f"{late['du_before']:.1f}", late_al=f"{late['al_max']:.0f}", late_om=f"{late['om_max']:.1f}", late_tilt=f"{late['tilt_max']:.1f}",
    late_du2=f"{NN['late_seed2']['du_max']:.1f}", brake=f"{ex_brake:.0f}",
    p93_deg=f"{math.degrees(math.atan(ex_brake / NN['g'])):.1f}", p93_q_mm=f"{NN['beta0'] * ex_brake / NN['w0'] ** 2 * 1e3:.1f}",
    v4=f"{f16['kerb_full']['kaggle_version']}", v7=f"{f16['kerb_off']['kaggle_version']}",
)
nav12 = re.search(r'<nav class="sim-nav" aria-label="Simulations">\s*(.*?)\s*</nav>', open(P("public", "simulations", "guinness-kaggle.html")).read(), re.S).group(1)
nav12 = re.sub(r'\s*<a href="guinness-cart-control\.html"[^>]*>16</a>', "", nav12)
V["NAV"] = nav12 + ' <a href="guinness-cart-control.html" aria-current="page">16</a>'
src = open(P("notes", "fig16", "page", "guinness-cart-control.src.html")).read()
missing = sorted(set(re.findall(r"\{\{(\w+)\}\}", src)) - set(V))
if missing: sys.exit("no value for: " + ", ".join(missing))
out = re.sub(r"\{\{(\w+)\}\}", lambda m: V[m.group(1)], src)
dst = P("public", "simulations", "guinness-cart-control.html")
if "--check" in sys.argv:
    sys.exit(0 if open(dst).read() == out else "the page differs from its source and data: run tools/fig16/build_page.py")
open(dst, "w").write(out); print(dst, len(out), "bytes;", len(V), "values filled")
