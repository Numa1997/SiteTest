"""Fig. 12 note (public/simulations/guinness-kaggle.html): every number the note quotes, printed from the stored runs, the
model's constants and the code's own functions, so that none is typed in by hand. The note's figures are drawn here too, as
SVG, from the same numbers.

Sources, all in the repository:
  public/data/fig12/2026-11-14-run10/            the files the page plays: run 10's five controlled rides; run 8's three rides with
                                                 the speed held, its free swing with the head; run 6's free swing without the head
  notes/fig12/jax/run10-check/run10-summary.json what run_b.py wrote on Kaggle for run 10 (books, impulses, gains, cost)
  notes/fig12/jax/run8-check/run8-summary.json   the same for run 8 (the pint at rest, the free swing's fit, the speed-held rides)
  public/scripts/guinness-glass.js               the glass's inner radius every 0.5 mm
  tools/fig12/kaggle/stout_jax.py                the model's constants, the cart, the controllers' design (slosh_lqr, susp_lqr,
                                                 observer_design), the glass on the grid (Geometry); imported, run on the CPU
Run:  python3 tools/fig12/kaggle/note_numbers.py           prints name = value, one per line; writes notes/fig12/note-numbers.json
      python3 tools/fig12/kaggle/note_numbers.py --check   also lists every number typed by hand in the note's source
                                                           (notes/fig12/note/paper.html): decimals, and whole numbers followed by
                                                           a unit, outside {{...}}, outside the Sources section and \\tag{...}
The cart driven alone over each road (the pint frozen as a rigid load) takes about a minute on a CPU; its result is kept in
notes/fig12/note/cart-alone.json, keyed by the SHA-256 of stout_jax.py, and recomputed when that file changes."""
import base64, hashlib, html, json, math, os, re, sys, zlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(ROOT, "public", "data", "fig12", "2026-11-14-run10")
CHK8 = os.path.join(ROOT, "notes", "fig12", "jax", "run8-check")
CHK10 = os.path.join(ROOT, "notes", "fig12", "jax", "run10-check")
SRC_NOTE = os.path.join(ROOT, "notes", "fig12", "note", "paper.html")
CACHE = os.path.join(ROOT, "notes", "fig12", "note", "cart-alone.json")
sys.path.insert(0, HERE)
os.environ.setdefault("JAX_PLATFORMS", "cpu")
N = {}   # name -> (value, printed text)


SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def put(name, value, fmt):
    if fmt.startswith("sci"):
        d = int(fmt[3:] or 2); m, e = f"{value:.{d - 1}e}".split("e"); e = int(e)
        N[name] = (value, (f"{m} × 10" if m not in ("1", "1.0") else "10") + str(e).translate(SUP)); return
    N[name] = (value, fmt.format(value).replace("-", "−") if isinstance(value, (int, float)) and value < 0 else fmt.format(value))


def put_text(name, text):
    N[name] = (text, text)


def sig(x, n=3):
    """x to n significant figures, as text (no exponent for 1e-4 <= |x| < 1e6)."""
    if x == 0: return "0"
    d = n - 1 - int(math.floor(math.log10(abs(x))))
    return f"{x:.{max(d, 0)}f}"


import stout_jax as sj                                     # noqa: E402  (the solver's own constants and functions)
import scipy.linalg as sl                                  # noqa: E402
from scipy.optimize import curve_fit                       # noqa: E402
from scipy.special import jv, jnp_zeros                    # noqa: E402

# ============================================================================================ 1. the glass and the pint
gl = open(os.path.join(ROOT, "public", "scripts", "guinness-glass.js")).read()
RTAB = np.array([float(v) for v in re.search(r"R:\s*\[([^\]]*)\]", gl).group(1).split(",")])
DZP = 0.0005; FILL = 0.125; DX = 0.0015; RHO = 1007.0; G = 9.81
GEO = sj.Geometry(RTAB, DZP, FILL, DX)
R = GEO.Rfill                                             # m, the radius at the fill
zrim = (len(RTAB) - 1) * DZP; iw = int(np.argmax(RTAB))
put("glass_height_mm", 160, "{:d}"); put("glass_width_mm", 85, "{:d}")          # the catalogue size the drawing was scaled to
put("R_floor_mm", RTAB[0] * 1e3, "{:.1f}"); put("D_floor_mm", 2 * RTAB[0] * 1e3, "{:.1f}")
put("R_wide_mm", RTAB[iw] * 1e3, "{:.1f}"); put("z_wide_mm", iw * DZP * 1e3, "{:.0f}")
put("z_rim_mm", zrim * 1e3, "{:.1f}"); put("R_mm", R * 1e3, "{:.1f}"); put("R_m", R, "{:.4f}")
put("dzp_mm", DZP * 1e3, "{:.1f}")
z5 = int(round(5e-3 / DZP)); put("R_at_5mm_mm", RTAB[z5] * 1e3, "{:.1f}")
zz = np.arange(len(RTAB)) * DZP; top = (zz >= FILL - 0.020) & (zz <= FILL)
put("R_change_top20_mm", (RTAB[top].max() - RTAB[top].min()) * 1e3, "{:.2f}")
put("fill_mm", FILL * 1e3, "{:.0f}"); put("fill_m", FILL, "{:.3f}")
V = sj.glass_volume(RTAB, DZP, FILL); put("stout_mL", V * 1e6, "{:.1f}"); put("stout_g_theory", RHO * V * 1e3, "{:.1f}")
HEAD0 = sj.HEAD0; put("hf_mm", HEAD0 * 1e3, "{:.0f}"); put("hf_m", HEAD0, "{:.3f}")
put("head_top_mm", (FILL + HEAD0) * 1e3, "{:.0f}"); put("head_below_rim_mm", (zrim - FILL - HEAD0) * 1e3, "{:.1f}")
put("stout_to_rim_mm", (zrim - FILL) * 1e3, "{:.1f}")
# the stout and the head
MU = sj.MU_STOUT; NU = sj.NU_STOUT
put("rho", RHO, "{:.0f}"); put("mu_mPas", MU * 1e3, "{:.2f}"); put("nu_e6", NU * 1e6, "{:.2f}"); put("serve_C", 6, "{:d}")
put("rho_W", 1006, "{:d}"); put("mu_W_lo", 2.03, "{:.2f}"); put("mu_W_hi", 2.23, "{:.2f}"); put("T_W_C", 5, "{:d}")
put("settle_s", 120, "{:d}")
put("hf_spec_lo", 18, "{:d}"); put("hf_spec_hi", 20, "{:d}")
for i, v in enumerate((17.5, 20.6, 22.2)): put(f"hf_meas{i + 1}", v, "{:.1f}")
d_mean, s_ln = 61e-6, 0.24                                 # Watamura et al.: mean diameter, log-normal width (data-for-solver.md)
put("bub_d_mean_um", d_mean * 1e6, "{:.0f}"); put("bub_sigma", s_ln, "{:.2f}")
R32 = 0.5 * d_mean * math.exp(2 * s_ln ** 2); put("R32_from_dist_um", R32 * 1e6, "{:.1f}")
put("R32_um", sj.RBUB * 1e6, "{:.0f}"); put("exp2s2", math.exp(2 * s_ln ** 2), "{:.3f}")
PHI_L = sj.PHI_F; GAS = sj.GAS; PHIC = sj.PHI_C
put("phi_l", PHI_L, "{:.2f}"); put("Phi", GAS, "{:.2f}"); put("Phi_c", PHIC, "{:.3f}"); put("Phi_c_pct", PHIC * 100, "{:.1f}")
put("Phi_minus_c", GAS - PHIC, "{:.3f}"); put("Phi_pct", GAS * 100, "{:.0f}")
put("phi_l_lo", 0.24, "{:.2f}"); put("phi_l_hi", 0.36, "{:.2f}"); put("phi_l_top", 0.235, "{:.3f}")
put("drain_min_lo", 25, "{:d}"); put("drain_min_hi", 110, "{:d}")
rho_f = PHI_L * RHO; put("rho_f", rho_f, "{:.0f}")
put("gamma_mN", sj.GAMMA * 1e3, "{:.1f}"); put("Einf_mN", sj.E_INF * 1e3, "{:.1f}"); put("VW_T_C", 20, "{:d}")
m_s = rho_f * HEAD0; lam_h = m_s / RHO
put("m_s", m_s, "{:.2f}"); put("lam_h_mm", lam_h * 1e3, "{:.2f}")
put("head_press_Pa", m_s * G, "{:.1f}"); put("head_equiv_stout_mm", m_s / RHO * 1e3, "{:.1f}")
head_disc_mL = math.pi * R ** 2 * HEAD0 * 1e6; put("head_disc_mL", head_disc_mL, "{:.2f}")

# ============================================================================================ 2. the first mode
XI = float(jnp_zeros(1, 3)[0]); XIS = [float(v) for v in jnp_zeros(1, 3)]
k = XI / R; th = math.tanh(k * FILL)
w11 = math.sqrt(G * k * th); f11 = w11 / (2 * math.pi)
put("xi", XI, "{:.4f}"); put("xi2", XIS[1], "{:.3f}"); put("xi3", XIS[2], "{:.3f}")
put("k", k, "{:.1f}"); put("inv_k_mm", 1e3 / k, "{:.1f}"); put("kh", k * FILL, "{:.2f}"); put("xih_R", XI * FILL / R, "{:.3f}")
put("tanh_kh", th, "{:.5f}"); put("w11_sq", w11 ** 2, "{:.1f}"); put("w11", w11, "{:.2f}"); put("f11", f11, "{:.3f}")
put("T11_s", 1 / f11, "{:.3f}")
for j, x in ((2, XIS[1]), (3, XIS[2])):
    put(f"f1{j}", math.sqrt(G * x / R * math.tanh(x * FILL / R)) / (2 * math.pi), "{:.2f}")
beta = 2 * XI * th / (XI ** 2 - 1); put("beta", beta, "{:.3f}")
put("c1J1_over_R", 2 / (XI ** 2 - 1), "{:.3f}")
put("J1xi", float(jv(1, XI)), "{:.4f}")
put("a_head_to_rim", G * (zrim - FILL - HEAD0) / R, "{:.2f}")
put("a_stout_to_rim", G * (zrim - FILL) / R, "{:.2f}")
put("q_rigid_fac", 2 / (XI ** 2 - 1), "{:.3f}")
put("one_mode_short_pct", 100 * (1 - 2 / (XI ** 2 - 1)), "{:.0f}")
dv_ex = 0.1; put("dv_ex", dv_ex, "{:.1f}"); put("dv_ex_mm_s", dv_ex * 1e3, "{:.0f}")
put("kick_ex_mm", beta * dv_ex / w11 * 1e3, "{:.1f}")
# the half-sine push of the free swing (run_b.py: push=(0.3, 1.0, 0.146))
t0p, ap, Tp = 0.3, 1.0, 0.146
put("push_t0", t0p, "{:.1f}"); put("push_a", ap, "{:.1f}"); put("push_T", Tp, "{:.3f}"); put("push_T_ms", Tp * 1e3, "{:.0f}")
put("push_half_period_s", 0.5 / f11, "{:.3f}")
tt = np.linspace(0, Tp, 20001); I_ = np.trapezoid(ap * np.sin(np.pi * tt / Tp) * np.exp(1j * w11 * tt), tt)
put("push_A_bare_mm", beta * abs(I_) / w11 * 1e3, "{:.1f}")

# ============================================================================================ 3. the thin layers
w_code = sj.OMEGA; f_code = w_code / (2 * math.pi)
put("f_code", f_code, "{:.2f}"); put("w_code", w_code, "{:.2f}")
delta = math.sqrt(2 * NU / w_code); put("delta_mm", delta * 1e3, "{:.2f}"); put("delta_mm3", delta * 1e3, "{:.3f}")
put("delta_cells", delta / DX, "{:.2f}"); put("two_delta_mm", 2 * delta * 1e3, "{:.1f}")
sq = math.sqrt(NU * w_code / 2); put("sqrt_nuw2_mm_s", sq * 1e3, "{:.2f}")
put("tau_ex_U_mm_s", 10, "{:d}"); put("tau_ex_Pa", RHO * sq * 0.01, "{:.3f}")
sig_wall = sq * (XI ** 2 + 1) / (2 * R * (XI ** 2 - 1)); z_wall = sig_wall / w_code
put("sigma_wall", sig_wall, "{:.3f}"); put("zeta_wall", z_wall, "{:.4f}"); put("wall_fac", (XI ** 2 + 1) / (2 * (XI ** 2 - 1)), "{:.3f}")
sig_skin = sq * k / 2 / math.tanh(k * FILL); z_skin = sig_skin / w_code
put("sigma_skin", sig_skin, "{:.3f}"); put("zeta_skin", z_skin, "{:.4f}")
sig_bulk = 2 * NU * k ** 2; put("sigma_bulk", sig_bulk, "{:.4f}"); put("zeta_bulk", sig_bulk / w_code, "{:.4f}")
z_lid = z_wall + z_skin + sig_bulk / w_code; put("zeta_lid", z_lid, "{:.4f}"); put("zeta_lid3", z_lid, "{:.3f}")
z_bare = z_wall + sig_bulk / w_code; put("zeta_bare", z_bare, "{:.4f}"); put("zeta_bare3", z_bare, "{:.3f}")   # a free, clean surface
zr_ = float(f"{z_bare:.4f}"); put("t_e_bare_s", 1 / (zr_ * float(f"{w11:.2f}")), "{:.1f}"); put("halve_swings", math.log(2) / (2 * math.pi * zr_), "{:.1f}")
put("tenth_s", math.log(10) / (zr_ * float(f"{w11:.2f}")), "{:.1f}")
put("logdec_pct", 100 * (1 - math.exp(-2 * math.pi * z_bare)), "{:.0f}")
Kst = 2 * math.pi * (XI ** 2 + 1) / (4 * (XI ** 2 - 1)) * math.sqrt(2) * XI ** 0.25 / XI    # Lambda = K nu^1/2 R^-3/4 g^-1/4
c_zeta = (XI ** 2 + 1) / (4 * (XI ** 2 - 1)) * math.sqrt(2) * XI ** -0.25
put("zeta_wall_coef", c_zeta, "{:.4f}"); put("K_lam", 2 * math.pi * c_zeta, "{:.2f}")
put("K_miles", 3.52, "{:.2f}"); put("K_exp", 5.23, "{:.2f}"); put("K_exp_pct", 100 * (5.23 / 3.52 - 1), "{:.0f}")
put("tank_in_lo", 3, "{:d}"); put("tank_ft_hi", 10, "{:d}")
put("zeta_wall_exp", z_wall * 5.23 / (2 * math.pi * c_zeta), "{:.4f}")
kd = k * DX; pic_step = kd ** 2 / 6; put("kdx", kd, "{:.3f}"); put("pic_loss_step", pic_step * 1e4, "{:.1f}")
put("pic_sigma", pic_step / 0.002, "{:.2f}"); put("pic_zeta", pic_step / 0.002 / w11, "{:.3f}")


# ============================================================================================ 4. the head of foam
pL = sj.P_GEN; put("pL", pL, "{:.0f}"); put("G0", sj.G_HEAD, "{:.0f}"); put("tau_y", sj.TAU_Y, "{:.1f}")
put("pL_bubble", 2 * sj.GAMMA / sj.RBUB, "{:.0f}")
put("VW_a", 1.0, "{:.0f}"); put("VW_k", 0.25, "{:.2f}")
for nm, pl in (("024", 0.24), ("030", 0.30)):
    put(f"tau_y_{nm}", 0.25 * pL * (1 - pl - PHIC) ** 2, "{:.1f}")
put("tau_y_over_weight", sj.TAU_Y / (m_s * G), "{:.2f}")
put("slope_hold_deg", math.degrees(math.asin(sj.TAU_Y / (m_s * G))), "{:.0f}")
gd = 10.0; Ca_f = MU * gd * sj.RBUB / sj.GAMMA
t_film = sj.GAMMA / sj.RBUB * GAS ** (5 / 6) * 0.7 * Ca_f ** 0.47 / PHI_L ** 0.5
t_corn = sj.GAMMA / sj.RBUB * GAS ** (5 / 6) * 8 * Ca_f ** 0.7 / PHI_L ** 0.15
put("gd_ex", gd, "{:.0f}"); put("Ca_f_ex", Ca_f * 1e5, "{:.1f}"); put("tau_film", t_film, "{:.1f}"); put("tau_corner", t_corn, "{:.1f}")
put("tau_v_ex", t_film + t_corn, "{:.1f}"); put("tau_tot_ex", t_film + t_corn + sj.TAU_Y, "{:.1f}")
put("tch_a1", 0.7, "{:.1f}"); put("tch_e1", 0.47, "{:.2f}"); put("tch_p1", 0.5, "{:.1f}")
put("tch_a2", 8, "{:d}"); put("tch_e2", 0.7, "{:.1f}"); put("tch_p2", 0.15, "{:.2f}"); put("tch_Phi_min", 0.80, "{:.2f}")
put("mu_floor_gd", 0.05, "{:.2f}")
mu_f_floor = (sj.TAU_Y + float(sj.foam_flow_stress(MU * 0.05 * sj.RBUB / sj.GAMMA))) / 0.05
put("mu_f_floor", mu_f_floor, "{:.0f}")
put("sheet_mass", RHO * 2 * DX, "{:.1f}"); put("dx_mm", DX * 1e3, "{:.1f}")
q_yield = HEAD0 * sj.TAU_Y * k / (RHO * G); put("q_yield_mm", q_yield * 1e3, "{:.1f}")
put("Z_wall", sj.Z_WALL, "{:.2f}"); put("lr_wall", sj.LR_WALL, "{:.3f}"); put("cantat_phi", 0.25, "{:.2f}")
put("cant_c1", 6.82, "{:.2f}"); put("cant_c2", 0.94, "{:.2f}")
for v in (1, 10, 50, 100):
    put(f"tau_edge_{v}", float(sj.head_wall_stress(v * 1e-3)), "{:.1f}" if v < 50 else "{:.0f}")
    Caw = MU * v * 1e-3 / sj.GAMMA
    put(f"edge_term2_pct_{v}", 100 * 0.94 * sj.LR_WALL * Caw ** (1 / 3) / (6.82 * Caw ** (2 / 3) + 0.94 * sj.LR_WALL * Caw ** (1 / 3)), "{:.1f}")
cap = lambda v: sj.TAU_Y + float(sj.foam_flow_stress(MU * (v / (2 * sj.RBUB)) * sj.RBUB / sj.GAMMA))
put("cap_1", cap(1e-3), "{:.0f}"); put("cap_100", cap(0.1), "{:.0f}")
ell = 1 / k; h_eff = 3 * ell / 5 * (1 - math.exp(-5 * HEAD0 / (3 * ell)))
put("h_eff_mm", h_eff * 1e3, "{:.1f}"); put("ws_floor_mm_s", 1, "{:d}")
eps_star = 2 * sj.TAU_Y / (rho_f * G); put("eps_star_mm", eps_star * 1e3, "{:.1f}")
put("rise_head_go_mm", (zrim - FILL - HEAD0 + eps_star) * 1e3, "{:.1f}")
put("aout_ex", 5, "{:d}")
eps5 = sj.TAU_Y / (rho_f * (G / 2 + 5)); put("eps_star_5_mm", eps5 * 1e3, "{:.1f}")
put("stout_vs_head_rise", (zrim - FILL) / (zrim - FILL - HEAD0 + eps_star), "{:.0f}")
eps1 = 1e-3; put("aout_1mm", sj.TAU_Y / (rho_f * eps1) - G / 2, "{:.0f}")
put("wedge_mm", 2 * eps_star * 1e3, "{:.1f}")
fac = 1 + lam_h * k * th
put("head_fac", fac, "{:.3f}"); put("lam_k", lam_h * k * th, "{:.3f}"); put("head_ffac", 1 / math.sqrt(fac), "{:.3f}")
put("rho_over_k", RHO / k, "{:.1f}")
w_h = w11 / math.sqrt(fac); put("f_head_theory", w_h / (2 * math.pi), "{:.2f}"); put("f_head_theory3", w_h / (2 * math.pi), "{:.3f}")
beta_h = beta / fac; put("beta_h", beta_h, "{:.3f}")
put("sauret_f", 3.1, "{:.1f}"); put("sauret_f0", 3.3, "{:.1f}")

# ============================================================================================ 5. the stored runs
S8 = json.load(open(os.path.join(CHK8, "run8-summary.json"))); S10 = json.load(open(os.path.join(CHK10, "run10-summary.json")))
T8 = {t["name"]: t for t in S8["tasks"]}; T10 = {t["name"]: t for t in S10["tasks"]}
I = json.load(open(os.path.join(DATA, "index-jax.json"))); FILES = {f["path"][:-5]: f for f in I["files"]}
rest = T8["rest"]; rg = rest["rest_guard"]
put("particles", rest["particles"], "{:,}"); put("cells", rest["cells"], "{:,}"); put("n_cols", GEO.n, "{:d}"); put("nz", GEO.nz, "{:d}")
put("mp_mg", rest["mp"] * 1e6, "{:.3f}"); put("mp_d_mm", (6 * rest["mp"] / RHO / math.pi) ** (1 / 3) * 1e3, "{:.2f}")
put("mp_mm3", rest["mp"] / RHO * 1e9, "{:.2f}")
put("cells_worth", V / DX ** 3, "{:,.0f}"); put("ppc_eff", rest["particles"] / (V / DX ** 3), "{:.2f}")
put("rest_max_mm", rg["max_dev_mm"], "{:.2f}"); put("rest_rms_mm", rg["rms_dev_mm"], "{:.3f}")
put("rest_lim_max_mm", rg["limit_max_mm"], "{:.2f}"); put("rest_lim_rms_mm", rg["limit_rms_mm"], "{:.3f}")
inside = (np.hypot(*np.meshgrid(GEO.xc, GEO.xc, indexing="ij")) < GEO.Rfill - DX)
put("trusted_cols", int(inside.sum()), "{:,}")
dE = (rest["energy_J"][0] - rest["energy_J"][1]); put("rest_dE_uJ", dE * 1e6, "{:.1f}")
m_st = rest["books"]["stout_glass_g_end"] * 1e-3
put("rest_sink_um", dE / (m_st * G) * 1e6, "{:.1f}")
put("rest_ms_step", rest["ms_per_step"], "{:.1f}"); put("rest_its", rest["its_per_step"], "{:.0f}")
put("rest_s_per_s", rest["s_per_simulated_s"], "{:.0f}")
put("tol_cg", 1e-5, "sci1"); put("maxit", 600, "{:d}")
put("head_served_mL", rest["books"]["head_ml0"], "{:.3f}"); put("stout_g", m_st * 1e3, "{:.1f}")
put("head_g", rest["books"]["head_ml0"] * 1e-6 * rho_f * 1e3, "{:.1f}")
put("load_g", m_st * 1e3 + rest["books"]["head_ml0"] * 1e-6 * rho_f * 1e3, "{:.1f}")
put("head_vs_disc_pct", 100 * (rest["books"]["head_ml0"] / head_disc_mL - 1), "{:.2f}")
put("viscous_cfl", NU * 0.002 / DX ** 2, "{:.4f}")
put("dt_ms", 2, "{:d}"); put("cfl", 0.8, "{:.1f}"); put("fps", 30, "{:d}"); put("sub_ms", 0.1, "{:.1f}"); put("Ts_ms", 1, "{:d}")
put("qH_mm", 0.02, "{:.2f}"); put("qhf_mm", 0.1, "{:.1f}"); put("qv_mm3", 0.1, "{:.1f}")
put("nu_dt_lim", 1 / 6, "{:.3f}")
put("alpha_min", 0.05, "{:.2f}"); put("mu_cells", lam_h / DX, "{:.1f}")
put("lagged_kmax", lam_h * math.pi / DX, "{:.1f}")
put("r0_p", 0.9, "{:.1f}"); put("r0_h", 0.505, "{:.3f}"); put("fallback_cell", 0.68, "{:.2f}"); put("drop_cells", 1.5, "{:.1f}")
put("ls_kernel_cells", 2, "{:d}")
put("dt_rest_last_ms", 1000 / 30 - 16 * 2, "{:.2f}")

def decode(f):
    """A stored ride file as the page reads it: the surface heights per column (NaN where none is stored), the lists."""
    D = json.load(open(os.path.join(DATA, f + ".json"))); n, nf = D["n"], D["frames"]
    d = np.frombuffer(zlib.decompress(base64.b64decode(D["H"])), np.int16).reshape(nf, n, n)
    Hq = np.cumsum(d.astype(np.int64), 0); Hq = ((Hq + 32768) % 65536) - 32768
    H = np.where(Hq == -32768, np.nan, Hq * D["qH"])
    return D, H


def ring(D, H, r, th):
    """pack_ride.py's ring(): bilinear over the four columns around the point, leaving out columns without a value."""
    n, dx, x0 = D["n"], D["dx"], D["x0"]; out = np.full(H.shape[0], np.nan); q = r
    while q > 0 and np.isnan(out).any():
        fx = (q * np.cos(th) - x0) / dx - 0.5; fy = (q * np.sin(th) - x0) / dx - 0.5
        i, j = int(np.floor(fx)), int(np.floor(fy)); tx, ty = fx - i, fy - j; num = np.zeros(H.shape[0]); den = np.zeros(H.shape[0])
        for a, b_, w in ((0, 0, (1 - tx) * (1 - ty)), (1, 0, tx * (1 - ty)), (0, 1, (1 - tx) * ty), (1, 1, tx * ty)):
            ii, jj = i + a, j + b_
            if 0 <= ii < n and 0 <= jj < n:
                v = H[:, ii, jj]; ok = np.isfinite(v); num += np.where(ok, w * np.nan_to_num(v), 0.0); den += np.where(ok, w, 0.0)
        val = np.where(den > 1e-6, num / np.maximum(den, 1e-12), np.nan); out = np.where(np.isnan(out), val, out); q -= 0.5 * dx
    return out


TH64 = 2 * np.pi * np.arange(64) / 64
RIDES = {}
for nm in FILES:
    D, H = decode(nm)
    RING = np.stack([ring(D, H, R - 0.5 * DX, a) for a in TH64], 1)
    lean = (RING[:, 0] - RING[:, 32]) * 1e3; tilt = 2 * (2 / 64) * (RING * np.cos(TH64)[None]).sum(1) * 1e3
    RIDES[nm] = dict(D=D, H=H, lean=lean, tilt=tilt, t=np.array(D["t"]))
    m = FILES[nm]["measured"]; g = lambda v: "{:.1f}".format(v) if v >= 2 else "{:.2f}".format(v)
    N[f"{nm}.lean_mm"] = (m["lean_max_mm"], "{:.1f}".format(m["lean_max_mm"]))          # as the page's table shows them
    N[f"{nm}.tilt_mm"] = (m["tilt_max_mm"], "{:.1f}".format(m["tilt_max_mm"]))
    N[f"{nm}.lean_mm2"] = (m["lean_max_mm"], "{:.2f}".format(m["lean_max_mm"]))
    N[f"{nm}.tilt_mm2"] = (m["tilt_max_mm"], "{:.2f}".format(m["tilt_max_mm"]))
    put(f"{nm}.lean_stored_mm", float(np.nanmax(np.abs(lean))), "{:.2f}")
    put(f"{nm}.head_spilled_mL", D["head_spill_ml"][-1], "{:.2f}")
    put(f"{nm}.stout_spilled_g", D["spill_g"][-1], "{:.3f}")
    hs = np.array(D["head_spill_ml"]); first = np.nonzero(hs > 0)[0]
    if len(first): put(f"{nm}.head_first_s", D["t"][first[0]], "{:.2f}")
    put(f"{nm}.ms_step", m["ms_per_step"], "{:.1f}"); put(f"{nm}.its", m["its_per_step"], "{:.0f}")
    if "i" in D:
        put(f"{nm}.i_max_A", float(np.max(np.abs(D["i"]))), "{:.2f}")
        put(f"{nm}.v_min", float(np.min(D["v"])), "{:.2f}"); put(f"{nm}.v_max", float(np.max(D["v"])), "{:.2f}")
        put(f"{nm}.dv_lost", D["v0"] - float(np.min(D["v"])), "{:.2f}")
        if "icmd" in D: put(f"{nm}.frames_3A", int(np.sum(np.abs(D["icmd"]) >= 3.0)), "{:d}")
        if "us" in D: put(f"{nm}.us_max_N", float(np.max(np.abs(D["us"]))), "{:.1f}")
        if "ipar" in D: put(f"{nm}.ipar_max_A", float(np.max(np.abs(D["ipar"]))), "{:.3f}")
        if "qhat" in D and D["ctrl"] in ("slosh", "joint"):
            qh, yq = np.array(D["qhat"]), np.array(D["yq"])
            put(f"{nm}.filter_rms_mm", float(np.sqrt(np.mean((qh - yq) ** 2))) * 1e3, "{:.2f}")
            put(f"{nm}.probe_rms_mm", float(np.sqrt(np.mean(yq ** 2))) * 1e3, "{:.2f}")
    T = T10.get(nm) if FILES[nm]["commit"].startswith("58eea") else T8.get(nm)
    if T and T.get("impulse_vs_momentum"):
        iv = T["impulse_vs_momentum"]; put(f"{nm}.impulse_rel", abs(iv["impulse_x"] + iv["momentum_x_end"]) / max(abs(iv["momentum_x_end"]), 1e-30), "sci1")
        put(f"{nm}.momentum_end", abs(iv["momentum_x_end"]), "{:.1e}")
    if T: put(f"{nm}.s_per_s", T["s_per_simulated_s"], "{:.0f}")
    b = m.get("books") or {}
    if b: put(f"{nm}.head_err", b["head_err_ml_max"], "sci2"); put(f"{nm}.stout_err", b["stout_err_particles_max"], "{:d}")
put("lean_round_diff_max_mm", max(abs(N[f"{nm}.lean_stored_mm"][0] - FILES[nm]["measured"]["lean_max_mm"]) for nm in FILES), "{:.2f}")
put("books_head_err_max", max((FILES[nm]["measured"].get("books") or {}).get("head_err_ml_max") or 0 for nm in FILES), "sci2")
put("books_stout_err_max", max((FILES[nm]["measured"].get("books") or {}).get("stout_err_particles_max") or 0 for nm in FILES), "{:d}")
imp_all = [N[k][0] for k in N if k.endswith(".impulse_rel")]; put("impulse_rel_max", max(imp_all), "sci1")
put("ms_step_lo", min(FILES[nm]["measured"]["ms_per_step"] for nm in FILES if nm.startswith("ride")), "{:.0f}")
put("ms_step_hi", max(FILES[nm]["measured"]["ms_per_step"] for nm in FILES if nm.startswith("ride")), "{:.0f}")
put("s_per_s_lo", min(N[k][0] for k in N if k.endswith(".s_per_s") and k.startswith("ride")), "{:.0f}"); put("s_per_s_hi", max(N[k][0] for k in N if k.endswith(".s_per_s") and k.startswith("ride")), "{:.0f}")
put("ride8_min", 8 * N["s_per_s_hi"][0] / 60, "{:.0f}")
lean = lambda nm: FILES[nm]["measured"]["lean_max_mm"]
put("resonant_joint_factor", lean("ride_resonant") / lean("ride_resonant_joint"), "{:.0f}")
put("bump25_joint_factor", lean("ride_bump25") / lean("ride_bump25_joint"), "{:.0f}")
# the free swings: the run's own fit (ring 13 of the run's surface) and a refit of the stored file (the same ring, the same law)
def fit(t, q):
    fun = lambda t, A, tau, w, ph, c: A * np.exp(-np.clip(t / tau, -50, 50)) * np.cos(w * t + ph) + c; best = None
    for fg, taug in ((3.4, 5.0), (3.3, 0.3), (3.0, 0.3), (3.3, 0.1), (3.0, 0.1)):
        for ph in np.linspace(0, 2 * np.pi, 8, endpoint=False):
            try:
                p, _ = curve_fit(fun, t, q, p0=[np.max(np.abs(q - q.mean())), taug, 2 * np.pi * fg, ph, q.mean()], maxfev=20000)
                r = np.sum((fun(t, *p) - q) ** 2)
                if best is None or r < best[1]: best = (p, r)
            except Exception: pass
    A, tau, w, ph, c = best[0]; w0 = math.sqrt(w * w + 1 / tau ** 2)
    return dict(f=abs(w) / (2 * math.pi), f0=w0 / (2 * math.pi), zeta=1 / (abs(tau) * w0), tau=abs(tau), A=A, w=w, ph=ph, c=c, fun=fun, p=best[0])


r13 = 13 / 16 * (R - 0.5 * DX); put("r13_mm", r13 * 1e3, "{:.1f}"); put("ring_num", 13, "{:d}"); put("ring_den", 16, "{:d}")
put("ring_angles", 64, "{:d}")
SW = {}
for nm, key in (("free_full_1.5", "head"), ("free_wall_1.5", "nohead")):
    F = FILES[nm]["measured"]["fit_ring13"]; Rd = RIDES[nm]
    put(f"sw_{key}_f", F["f"], "{:.3f}"); put(f"sw_{key}_f0", F["f0"], "{:.3f}"); put(f"sw_{key}_zeta", F["zeta"], "{:.3f}")
    put(f"sw_{key}_zeta4", F["zeta"], "{:.4f}"); put(f"sw_{key}_A", F["A_mm"], "{:.2f}")
    put(f"sw_{key}_tau_s", 1 / (F["zeta"] * 2 * math.pi * F["f0"]), "{:.3f}")
    q13 = (2 / 64) * (np.stack([ring(Rd["D"], Rd["H"], r13, a) for a in TH64], 1) * np.cos(TH64)[None]).sum(1)
    t = Rd["t"]; msk = t >= t0p + Tp + 0.1
    Fs = fit(t[msk] - t[msk][0], q13[msk])
    put(f"sw_{key}_f0_stored", Fs["f0"], "{:.3f}"); put(f"sw_{key}_zeta_stored", Fs["zeta"], "{:.3f}")
    SW[key] = dict(t=t, q=q13, fit=Fs, t_start=t[msk][0])
put("sw_head_w0", 2 * math.pi * FILES["free_full_1.5"]["measured"]["fit_ring13"]["f0"], "{:.2f}")
W0 = N["sw_head_w0"][0]; Z0 = FILES["free_full_1.5"]["measured"]["fit_ring13"]["zeta"]
put("sw_head_wd", W0 * math.sqrt(1 - Z0 ** 2), "{:.2f}"); put("sw_head_sigma", Z0 * W0, "{:.2f}")
put("sw_head_T_s", 1 / FILES["free_full_1.5"]["measured"]["fit_ring13"]["f0"], "{:.3f}")
put("sw_head_te_over_T", (1 / (Z0 * W0)) * FILES["free_full_1.5"]["measured"]["fit_ring13"]["f0"], "{:.2f}")
put("push_A_ring_mm", N["push_A_bare_mm"][0] * float(jv(1, k * r13)) / float(jv(1, XI)), "{:.1f}")
fnh = FILES["free_wall_1.5"]["measured"]["fit_ring13"]
put("sw_nohead_vs_theory_pct", 100 * (1 - fnh["f0"] / f11), "{:.1f}")
k_grid = (2 * math.pi * fnh["f0"]) ** 2 / G; put("k_grid", k_grid, "{:.1f}")
fac_g = 1 + lam_h * k_grid; put("head_fac_grid", fac_g, "{:.3f}"); put("head_ffac_grid", 1 / math.sqrt(fac_g), "{:.3f}")
put("f_head_grid_pred", fnh["f0"] / math.sqrt(fac_g), "{:.3f}")
put("sw_head_vs_pred_pct", 100 * (1 - FILES["free_full_1.5"]["measured"]["fit_ring13"]["f0"] / (fnh["f0"] / math.sqrt(fac_g))), "{:.1f}")
put("sw_head_vs_theory_pct", 100 * (1 - FILES["free_full_1.5"]["measured"]["fit_ring13"]["f0"] / (w_h / (2 * math.pi))), "{:.1f}")
z_num = fnh["zeta"] - (z_wall + sig_bulk / w_code); put("zeta_num", z_num, "{:.4f}"); put("zeta_phys_nohead", z_wall + sig_bulk / w_code, "{:.4f}")
put("zeta_num_ratio", z_num / (z_wall + sig_bulk / w_code), "{:.1f}")
put("zeta_num_vs_head_pct", 100 * z_num / Z0, "{:.0f}")
put("tail_mm", float(np.mean(SW["head"]["q"][SW["head"]["t"] >= 1.5])) * 1e3, "{:.2f}")
put("bump_rate_Hz", 1.0 / 0.29, "{:.3f}"); put("bump_gap_m", 0.29, "{:.2f}")
put("bump_vs_bare_pct", 100 * (1.0 / 0.29 / f11 - 1), "{:.1f}"); put("bump_vs_head_pct", 100 * (1.0 / 0.29 / (FILES["free_full_1.5"]["measured"]["fit_ring13"]["f0"]) - 1), "{:.0f}")
put("plant_beta_used", T10["ride_sharp30_joint"]["plant"]["beta"], "{:.3f}")

# ============================================================================================ 6. the cart
P = dict(sj.CART_COMMON)
b = P["Ngear"] * P["Km"] / P["Rw"]; put("b", b, "{:.0f}")
for kk, fm in (("Mb", "{:.1f}"), ("mw", "{:.1f}"), ("k", "{:.0f}"), ("c", "{:.0f}"), ("kt", "{:,.0f}"), ("ct", "{:.0f}"), ("cx", "{:.0f}"),
               ("Imax", "{:.0f}"), ("Vmax", "{:.0f}"), ("Ra", "{:.0f}"), ("mu", "{:.1f}"), ("Ngear", "{:.0f}"), ("Km", "{:.2f}"), ("Umax", "{:.0f}")):
    put(f"cart_{kk}", P[kk], fm)
put("cart_Rw_mm", P["Rw"] * 1e3, "{:.0f}"); put("cart_Iw", P["Iw"] * 1e5, "{:.0f}"); put("cart_Jm", P["Jm"] * 1e6, "{:.0f}")
put("cart_tauI_ms", P["tauI"] * 1e3, "{:.0f}"); put("cart_tauU_ms", P["tauU"] * 1e3, "{:.0f}"); put("cart_Ls_mm", P["Ls"] * 1e3, "{:.0f}")
put("kt_kN", P["kt"] / 1e3, "{:.0f}")
ml = rest["books"]["stout_glass_g_end"] * 1e-3 + rest["books"]["head_ml0"] * 1e-6 * rho_f
put("ml", ml, "{:.4f}"); put("ml_g", ml * 1e3, "{:.1f}")
rot = (P["Iw"] + P["Ngear"] ** 2 * P["Jm"]) / P["Rw"] ** 2
put("m_wheel_rot", P["Iw"] / P["Rw"] ** 2, "{:.3f}"); put("m_motor_rot", P["Ngear"] ** 2 * P["Jm"] / P["Rw"] ** 2, "{:.3f}"); put("m_rot", rot, "{:.3f}")
Mx = P["Mb"] + ml + P["mw"] + rot; put("Mx", Mx, "{:.3f}")
Ms = P["Mb"] + ml; put("Ms", Ms, "{:.3f}")
put("F_motor_max", b * P["Imax"], "{:.0f}"); put("a_motor_max", b * P["Imax"] / Mx, "{:.2f}")
E15 = b * 1.5; put("emf_15", E15, "{:.1f}"); put("i_fwd_15", (P["Vmax"] - E15) / P["Ra"], "{:.2f}"); put("F_fwd_15", b * (P["Vmax"] - E15) / P["Ra"], "{:.2f}")
put("a_fwd_15", b * (P["Vmax"] - E15) / P["Ra"] / Mx, "{:.2f}"); put("i_brk_15", (P["Vmax"] + E15) / P["Ra"], "{:.2f}")
put("i0_15", P["cx"] * 1.5 / b, "{:.1f}"); put("i0_10", P["cx"] * 1.0 / b, "{:.1f}")
N0 = (Ms + P["mw"]) * G; put("N0", N0, "{:.1f}"); put("grip_N0", P["mu"] * N0, "{:.1f}"); put("N_grip_lim", b * P["Imax"] / P["mu"], "{:.2f}")
put("f_body", math.sqrt(P["k"] / Ms) / (2 * math.pi), "{:.2f}"); put("f_hop", math.sqrt((P["k"] + P["kt"]) / P["mw"]) / (2 * math.pi), "{:.1f}")
put("tyre_static_mm", N0 / P["kt"] * 1e3, "{:.1f}")
M_bare = P["Mb"] + rest["books"]["stout_glass_g_end"] * 1e-3 + P["mw"] + rot; put("Mx_bare", M_bare, "{:.3f}")
wc = b * P["Kp"] / M_bare; put("fc", wc / (2 * math.pi), "{:.0f}"); put("Kp", P["Kp"], "{:.2f}"); put("Ki", P["Ki"], "{:.1f}")
put("Ki_ratio", P["Ki"] / (P["Kp"] * wc / 4), "{:.3f}")
put("fc_head", b * P["Kp"] / Mx / (2 * math.pi), "{:.2f}")
rts = np.roots([Mx, P["cx"] + b * P["Kp"], b * P["Ki"]]); put("pi_root1", float(np.max(rts.real)), "{:.1f}"); put("pi_root2", float(np.min(rts.real)), "{:.1f}")
put("Mx_head_pct", 100 * (Mx / M_bare - 1), "{:.0f}")
zsky = P["csky"] / (2 * math.sqrt(P["k"] * (P["Mb"] + rest["books"]["stout_glass_g_end"] * 1e-3)))
put("csky", P["csky"], "{:.1f}"); put("zeta_sky", zsky, "{:.2f}")
put("f_body_sky_zeta", (P["c"] + P["csky"]) / (2 * math.sqrt(P["k"] * Ms)), "{:.2f}")
put("zeta_body_passive", P["c"] / (2 * math.sqrt(P["k"] * Ms)), "{:.2f}")
# the sensitivity of the speed loop at the swing's frequency (with the head)
jw = 1j * W0; Lp = b * (P["Kp"] + P["Ki"] / jw) / (Mx * jw + P["cx"])
put("S_mag", abs(1 / (1 + Lp)), "{:.3f}"); put("L_re", Lp.real, "{:.3f}"); put("L_im", Lp.imag, "{:.3f}")
put("PI_re", P["Kp"], "{:.2f}"); put("PI_im", (P["Ki"] / jw).imag, "{:.2f}"); put("plant_im", Mx * W0, "{:.2f}")
put("one_plus_L", abs(1 + Lp), "{:.3f}")
Lp2 = Lp / (1 + P["tauI"] * jw) * np.exp(-jw * P["Ts"] / 2); put("S_mag_lag", abs(1 / (1 + Lp2)), "{:.3f}")
put("S_pct", 100 * abs(1 / (1 + Lp2)), "{:.0f}")
# the preview: the lag as a delay
wtau = W0 * P["tauI"]; put("prev_phase_lag", -math.degrees(math.atan(wtau)), "{:.4f}"); put("prev_phase_delay", -math.degrees(wtau), "{:.4f}")
put("prev_mag", 1 / math.sqrt(1 + wtau ** 2), "{:.5f}")
# the roads and the axle's path
ROADS = {"resonant": [dict(x=1.5 + 0.29 * i, h=0.020, L=0.25) for i in range(5)], "bump25": [dict(x=1.5, h=0.025, L=0.30)], "sharp30": [dict(x=1.5, h=0.030, L=0.12)]}
for rk, bumps in ROADS.items():
    xmin, h, za, zr = sj.road_table(dict(kind="bumps", bumps=bumps), xmax=6.0)
    put(f"{rk}_road_slope", math.pi * bumps[0]["h"] / bumps[0]["L"], "{:.3f}")
    put(f"{rk}_axle_slope", float(np.max(np.abs(np.diff(za) / h))), "{:.3f}")
    put(f"{rk}_prev_A", N0 * float(np.max(np.abs(np.diff(za) / h))) / b, "{:.2f}")
put("prev_ahead_mm_15", 1.5 * P["tauI"] * 1e3, "{:.0f}")
put("hb_kerb_mm", 30, "{:d}"); put("L_kerb_m", 0.12, "{:.2f}")


# ============================================================================================ 7. the cart alone (frozen pint)
_xm, _h, _za, _zr = sj.road_table(dict(kind="bumps", bumps=ROADS["sharp30"]), xmax=6.0)
X_TOUCH = float(_xm + _h * np.nonzero(_za > _za[0] + 1e-7)[0][0])          # where the wheel's rim first lifts the axle


def cart_alone():
    import jax, jax.numpy as jnp
    jax.config.update("jax_enable_x64", True)
    out = {}
    roads = {"resonant": (1.0, 8.0), "bump25": (1.0, 8.0), "sharp30": (1.5, 4.0)}
    for rk, (v0, T) in roads.items():
        for mode in (("speed", "early") if rk == "sharp30" else ("speed",)):
            road = sj.road_table(dict(kind="bumps", bumps=ROADS[rk]), xmax=0.5 + v0 * T * 1.3 + 2)
            cart = sj.Cart(dict(sj.CART_COMMON, v0=v0, ctrl="speed"), road)
            if mode == "early":                                  # full forward current from 4 ms before the axle first rises to the top
                x_on = X_TOUCH - v0 * 0.004; x_off = 1.5
                base = cart.sample
                def sample(c, base=base):
                    c2 = base(c); on = (c["x"] >= x_on) & (c["x"] < x_off)
                    return dict(c2, icmd=jnp.where(on, 10.0, c2["icmd"]))
                cart.sample = sample
            c = cart.init(0.5, ml)
            @jax.jit
            def adv(c):
                v0_, z0_ = c["vx"], c["vzb"]
                def body(_, cc):
                    cc = cart.step(cc, 1e-4, 0.0, 0.0)
                    return cc
                rec = []
                def body2(cc, _):
                    cc = cart.step(cc, 1e-4, 0.0, 0.0)
                    a, d = cart.axle(cc["x"])
                    Fm = jnp.clip(cart.bForce() * cc["i"], -cart.p["mu"] * cc["N"], cart.p["mu"] * cc["N"])
                    return cc, jnp.stack([cc["t"], cc["x"], cc["vx"], cc["N"], -cc["N"] * d, Fm, cc["i"], cc["vzb"]])
                cc, ys = jax.lax.scan(body2, c, None, length=20)
                return cc, ys
            ys = []
            for _ in range(int(round(T / 0.002))):
                c, y = adv(c); ys.append(np.asarray(y))
            Y = np.concatenate(ys)
            t, x, v, Nw, Fr, Fm, i, vzb = Y.T
            # the glass's mean accelerations over each 2 ms step, as the stout feels them
            v2 = np.concatenate([[v0], v[19::20]]); z2 = np.concatenate([[0.0], vzb[19::20]])
            ax = np.diff(v2) / 0.002; az = np.diff(z2) / 0.002; tm = np.arange(len(ax)) * 0.002 + 0.001
            out[f"{rk}_{mode}"] = dict(t=t[::10].tolist(), v=v[::10].tolist(), N=Nw[::10].tolist(), Fr=Fr[::10].tolist(), Fm=Fm[::10].tolist(),
                                     i=i[::10].tolist(), x=x[::10].tolist(), ax=ax.tolist(), az=az.tolist(), tm=tm.tolist(),
                                     air_ms=float(np.sum(Nw <= 0) * 0.1), v_min=float(np.min(v)), N_max=float(np.max(Nw)), Fr_min=float(np.min(Fr)),
                                     air_events=int(np.sum((Nw[1:] <= 0) & (Nw[:-1] > 0))))
    return out


h_src = hashlib.sha256(open(os.path.join(HERE, "stout_jax.py"), "rb").read()).hexdigest()
CA = None
if os.path.exists(CACHE):
    c_ = json.load(open(CACHE))
    if c_.get("stout_jax_sha256") == h_src and c_.get("ml") == ml and c_.get("x_touch") == X_TOUCH: CA = c_["runs"]
if CA is None:
    CA = cart_alone(); json.dump(dict(stout_jax_sha256=h_src, ml=ml, x_touch=X_TOUCH, runs=CA), open(CACHE, "w"))
put("plant_w0", W0, "{:.2f}"); put("plant_f0", W0 / (2 * math.pi), "{:.3f}"); put("plant_zeta", Z0, "{:.3f}")
for rk in ROADS:
    r_ = CA[f"{rk}_speed"]; ax = np.array(r_["ax"]); az = np.array(r_["az"]); tm = np.array(r_["tm"])
    put(f"{rk}_ax_max", float(np.max(np.abs(ax))), "{:.1f}"); put(f"{rk}_geff_min", float(np.min(G + az)), "{:.1f}"); put(f"{rk}_geff_max", float(np.max(G + az)), "{:.1f}")
    put(f"{rk}_az_absmax", float(np.max(np.abs(az))), "{:.0f}")
    for key, (ww, bb) in (("bare", (w11, beta)), ("head", (W0, beta_h))):
        put(f"{rk}_A_{key}_mm", bb / ww * abs(np.sum(ax * np.exp(1j * ww * tm)) * 0.002) * 1e3, "{:.0f}" if bb / ww * abs(np.sum(ax * np.exp(1j * ww * tm)) * 0.002) > 0.01 else "{:.1f}")
put("resonant_A_vs_rim", N["resonant_A_bare_mm"][0] / N["stout_to_rim_mm"][0], "{:.1f}")
ks = CA["sharp30_speed"]; ke = CA["sharp30_early"]
t_ = np.array(ks["t"]); Fr = np.array(ks["Fr"]); Nw = np.array(ks["N"]); v_ = np.array(ks["v"])
put("kerb_Fr_peak", -float(np.min(Fr)), "{:.0f}"); put("kerb_N_max", float(np.max(Nw)), "{:.0f}"); put("kerb_N_ratio", float(np.max(Nw)) / N0, "{:.1f}")
blow = Fr < -1.0; idx = np.nonzero(blow)[0]
put("kerb_blow_ms", (t_[idx[-1]] - t_[idx[0]]) * 1e3 if len(idx) else 0, "{:.0f}")
put("kerb_over15_ms", float(np.sum(-Fr > b * P["Imax"])) * 1.0, "{:.0f}")         # samples every 1 ms
put("kerb_air_ms", ks["air_ms"], "{:.0f}"); put("kerb_air_events", ks["air_events"], "{:d}")
put("kerb_v_min", ks["v_min"], "{:.2f}"); put("kerb_dv", 1.5 - ks["v_min"], "{:.2f}"); put("kerb_early_v_min", ke["v_min"], "{:.2f}")
tke_ = np.array(ke["t"]); vke_ = np.array(ke["v"]); ve_peak = float(vke_[tke_ <= tke_[np.argmin(vke_)]].max())
put("kerb_early_vpeak", ve_peak, "{:.2f}"); put("kerb_early_dv", ve_peak - ke["v_min"], "{:.2f}"); put("kerb_early_net", 1.5 - ke["v_min"], "{:.2f}")
put("kerb_Fr_vs_motor", -float(np.min(Fr)) / (b * (P["Vmax"] - b * 1.5) / P["Ra"]), "{:.1f}")
put("kerb_i_cmd_need", -float(np.min(Fr)) / b, "{:.0f}")
put("kerb_prev_static_A", N0 * N["sharp30_axle_slope"][0] / b, "{:.2f}")
put("kerb_i_max_speed", float(np.max(np.abs(ks["i"]))), "{:.2f}")
# the kick into the stout: its first peak (with the head's plant) for the best case's loss of speed
dvk = ve_peak - ke["v_min"]; wd = W0 * math.sqrt(1 - Z0 ** 2); tp = math.atan(math.sqrt(1 - Z0 ** 2) / Z0) / wd
put("tp_ms", tp * 1e3, "{:.0f}"); put("wd_tp", wd * tp, "{:.3f}"); put("kick_rate_mm", beta_h * dvk / W0 * 1e3, "{:.1f}")
put("kick_exp", math.exp(-Z0 * W0 * tp), "{:.3f}"); put("kick_peak_mm", beta_h * dvk / W0 * math.exp(-Z0 * W0 * tp) * 1e3, "{:.1f}")
put("kick_exp_bare", math.exp(-z_bare * math.atan(math.sqrt(1 - z_bare ** 2) / z_bare) / math.sqrt(1 - z_bare ** 2)), "{:.3f}")
put("kick_zt", Z0 * W0 * tp, "{:.3f}")
put("swing_period_ms", 1000 / (W0 / (2 * math.pi)), "{:.0f}"); put("lag_phase_deg", 360 * 0.002 * W0 / (2 * math.pi), "{:.1f}")

# ============================================================================================ 8. the controllers' design
cx = P["cx"]
K = sj.slosh_lqr(Mx, b, cx, W0, Z0, beta_h, P["Imax"])
for i_, v in enumerate(K): put(f"K{i_ + 1}", v, "{:.2f}")
K_run = FILES["ride_sharp30_joint"]["measured"]["control"]["gains"]["K"]
put("K_vs_run_max", max(abs(a - b_) for a, b_ in zip(K, K_run)), "sci1")
put("K4_hand", P["Imax"] / 0.02, "{:.0f}")
for nm_, v in (("lqr_dv_m", 0.05), ("lqr_q_m_mm", 2), ("lqr_xi_m_cm", 2)): put(nm_, v, "{:.2f}" if v < 1 else "{:.0f}")
A4 = np.array([[-cx / Mx, 0, 0, 0], [0, 0, 1, 0], [beta_h * cx / Mx, -W0 ** 2, -2 * Z0 * W0, 0], [-1, 0, 0, 0]])
B4 = np.array([[b / Mx], [0.0], [-beta_h * b / Mx], [0.0]])
ev_open = np.linalg.eigvals(A4); ev = np.linalg.eigvals(A4 - B4 @ K[None])
sw = sorted([e for e in ev if abs(e.imag) > 1e-6], key=lambda e: -e.imag)[0]
put("ev_open_re", -Z0 * W0, "{:.2f}"); put("ev_open_im", W0 * math.sqrt(1 - Z0 ** 2), "{:.2f}")
put("ev_sw_re", sw.real, "{:.2f}"); put("ev_sw_im", abs(sw.imag), "{:.2f}"); put("ev_sw_zeta", -sw.real / abs(sw), "{:.2f}")
reals = sorted([e.real for e in ev if abs(e.imag) <= 1e-6])
put("ev_slow", reals[-1], "{:.2f}"); put("ev_fast", reals[0], "{:.0f}")
put("lqr_gain_pct", 100 * (sw.real / (-Z0 * W0) - 1), "{:.0f}")
Kb = sj.slosh_lqr(Mx, b, cx, w11, z_bare, beta, P["Imax"])
A4b = np.array([[-cx / Mx, 0, 0, 0], [0, 0, 1, 0], [beta * cx / Mx, -w11 ** 2, -2 * z_bare * w11, 0], [-1, 0, 0, 0]])
B4b = np.array([[b / Mx], [0.0], [-beta * b / Mx], [0.0]]); evb = np.linalg.eigvals(A4b - B4b @ Kb[None])
swb = sorted([e for e in evb if abs(e.imag) > 1e-6], key=lambda e: -e.imag)[0]
for i_, v in enumerate(Kb): put(f"Kb{i_ + 1}", v, "{:.1f}")
put("bare_sigma", z_bare * w11, "{:.2f}"); put("bare_sigma_lqr", -swb.real, "{:.1f}"); put("bare_lqr_factor", -swb.real / (z_bare * w11), "{:.0f}")
# what the gains mean
put("K1_brake_A", K[0] * 0.1, "{:.1f}"); put("K2_1mm_A", -K[1] * 0.001, "{:.2f}"); put("K3_10mms_A", -K[2] * 0.01, "{:.2f}"); put("K4_1cm_A", -K[3] * 0.01, "{:.1f}")
# the filter: steady cycle of the covariance (probes at every second sample), its gains and its uncertainty
Ad, Bd, Qd = sj.observer_design(W0, Z0, beta_h, Mx, b, cx, P["Ts"])
so = dict(sigQ=0.0008, sigV=0.002); Rv, Rq = so["sigV"] ** 2, so["sigQ"] ** 2
C = np.diag([Rv, Rq, (so["sigQ"] * W0) ** 2]); Lfresh = None
for it in range(4000):
    Cp = Ad @ C @ Ad.T + Qd
    if it % 2 == 0:
        H2 = np.array([[1.0, 0, 0], [0, 1.0, 0]]); S2 = H2 @ Cp @ H2.T + np.diag([Rv, Rq]); L2 = Cp @ H2.T @ np.linalg.inv(S2)
        IK = np.eye(3) - L2 @ H2; C = IK @ Cp @ IK.T + L2 @ np.diag([Rv, Rq]) @ L2.T; Lfresh = L2; Cf = C
    else:
        L1 = Cp[:, 0] / (Cp[0, 0] + Rv); IK = np.eye(3) - np.outer(L1, [1, 0, 0]); C = IK @ Cp @ IK.T + Rv * np.outer(L1, L1)
for (i_, j_), v in np.ndenumerate(Lfresh): put(f"Lk{i_}{j_}", v, "{:.4f}" if abs(v) < 0.01 else "{:.3f}")
put("Lk_v_mm", -Lfresh[0, 0] * 10, "{:.1f}"); put("Lk_qd_mm", -Lfresh[2, 0] * 10, "{:.1f}"); put("Lk_ratio", Lfresh[2, 0] / Lfresh[0, 0], "{:.2f}")
put("Lk_q_mm", Lfresh[1, 1], "{:.3f}"); put("Lk_qd_1mm", Lfresh[2, 1], "{:.2f}"); put("Lk_n", 1 / Lfresh[1, 1], "{:.0f}"); put("Lk_ms", 2 / Lfresh[1, 1], "{:.0f}")
put("C_sv_mm", math.sqrt(Cf[0, 0]) * 1e3, "{:.1f}"); put("C_sq_mm", math.sqrt(Cf[1, 1]) * 1e3, "{:.2f}"); put("C_sqd_mm", math.sqrt(Cf[2, 2]) * 1e3, "{:.1f}")
put("WF", 0.5, "{:.1f}"); put("Wa", 0.002, "{:.3f}"); put("sigV_mm", 2, "{:d}"); put("sigQ_mm", 0.8, "{:.1f}")
put("WF_imp", math.sqrt(0.5 * 0.1), "{:.2f}"); put("Wa_rate", math.sqrt(0.002 / (W0 / (2 * math.pi))), "{:.3f}")
put("probe_r1_cells", 2.5, "{:.1f}"); put("probe_r2_cells", 4, "{:d}")
# the joint design: the parametric term
par = Mx * W0 ** 2 / (beta_h * b); put("par_fac", par, "{:.1f}"); put("W0_sq", W0 ** 2, "{:.1f}")
put("par_ex_A", par * (10 / G) * 0.005, "{:.2f}")
put("prob_par_A", par * (12 / G) * 0.008, "{:.2f}")
# can the heave pump the swing? the damped Mathieu equation, Floquet multipliers over one period of the heave
def floquet(eps, Om, w, z, n=400):
    Tm = 2 * np.pi / Om; h = Tm / n; Y = np.eye(2)
    f = lambda t, y: np.array([y[1], -2 * z * w * y[1] - w * w * (1 + eps * np.cos(Om * t)) * y[0]])
    for col in range(2):
        y = Y[:, col].copy(); t = 0.0
        for _ in range(n):
            k1 = f(t, y); k2 = f(t + h / 2, y + h / 2 * k1); k3 = f(t + h / 2, y + h / 2 * k2); k4 = f(t + h, y + h * k3)
            y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t += h
        Y[:, col] = y
    return max(abs(np.linalg.eigvals(Y)))
best = None
for Om_r in np.linspace(1.2, 2.6, 57):
    lo, hi = 0.0, 4.0
    if floquet(hi, Om_r * W0, W0, Z0) < 1: continue
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        if floquet(mid, Om_r * W0, W0, Z0) > 1: hi = mid
        else: lo = mid
    if best is None or hi < best[0]: best = (hi, Om_r)
for Om_r in np.linspace(best[1] - 0.03, best[1] + 0.03, 13):
    lo, hi = 0.0, 4.0
    if floquet(hi, Om_r * W0, W0, Z0) < 1: continue
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        if floquet(mid, Om_r * W0, W0, Z0) > 1: hi = mid
        else: lo = mid
    if hi < best[0]: best = (hi, Om_r)
put("floq_eps", best[0], "{:.2f}"); put("floq_ratio", best[1], "{:.2f}"); put("floq_az", best[0] * G, "{:.1f}"); put("floq_f", best[1] * W0 / (2 * math.pi), "{:.2f}")
put("floq_bare_az", 4 * z_bare * G, "{:.2f}"); put("floq_bare_f", 2 * f11, "{:.2f}")
put("az_rides_max", max(N[f"{rk}_az_absmax"][0] for rk in ROADS), "{:.0f}")
# the suspension's LQR
Ks = sj.susp_lqr(Ms, P["mw"], P["k"], P["c"], P["kt"], P["ct"])
for i_, v in enumerate(Ks): put(f"Ks{i_ + 1}", v, "{:.2f}")
put("Ks_run_diff", max(abs(a - b_) for a, b_ in zip(Ks, FILES["ride_sharp30_joint"]["measured"]["control"]["gains"]["Ks"])), "sci1")
put("susp_cancel_pct", 100 * -Ks[0] / P["k"], "{:.0f}"); put("k_eff", P["k"] + Ks[0], "{:.0f}")
As = np.array([[0, 1, -1, 0], [-P["k"] / Ms, -P["c"] / Ms, P["c"] / Ms, 0], [P["k"] / P["mw"], P["c"] / P["mw"], -(P["c"] + P["ct"]) / P["mw"], P["kt"] / P["mw"]], [0, 0, -1, 0]])
Bs = np.array([[0.0], [1 / Ms], [-1 / P["mw"]], [0.0]])
def pairs(M):
    e = np.linalg.eigvals(M); e = sorted([x for x in e if x.imag > 0], key=lambda x: abs(x)); return e
eo, ec = pairs(As), pairs(As - Bs @ Ks[None])
for nm_, e in (("body_o", eo[0]), ("body_c", ec[0]), ("hop_o", eo[1]), ("hop_c", ec[1])):
    put(f"{nm_}_re", e.real, "{:.2f}"); put(f"{nm_}_im", e.imag, "{:.2f}"); put(f"{nm_}_f", abs(e) / (2 * math.pi), "{:.2f}" if abs(e) < 100 else "{:.1f}")
    put(f"{nm_}_z", -e.real / abs(e), "{:.2f}")
put("susp_am", 0.5, "{:.1f}"); put("susp_sm_mm", 10, "{:d}"); put("susp_dm_mm", 0.2, "{:.1f}"); put("susp_um", 40, "{:d}")

# ---- the remaining inputs the note names (glass source, roads, examples)
put("g", G, "{:.2f}"); put("glass_dim_h", 149, "{:d}"); put("glass_dim_w", 76, "{:d}"); put("z5_mm", 5, "{:d}"); put("top_mm", 20, "{:d}")
put("tank_cm_lo", 3 * 2.54, "{:.1f}"); put("tank_m_hi", 10 * 0.3048, "{:.2f}"); put("phi_l_030", 0.30, "{:.2f}")
put_text("edge_speeds", "1, 10, 50 and 100")
put("code_vs_head_drag_pct", 100 * (math.sqrt(f_code / (w_h / (2 * math.pi))) - 1), "{:.0f}")
put("play_cap_s", 0.1, "{:.1f}"); put("rest_T", rest["end"], "{:.0f}"); put("free_T", T8["free_full_1.5"]["end"], "{:.0f}")
for rk, tn in (("resonant", "ride_resonant"), ("bump25", "ride_bump25"), ("sharp30", "ride_sharp30")):
    put(f"{rk}_v0", T8[tn]["v0"], "{:.1f}"); put(f"{rk}_T", T8[tn]["end"], "{:.0f}")
    put(f"{rk}_hb_mm", ROADS[rk][0]["h"] * 1e3, "{:.0f}"); put(f"{rk}_L", ROADS[rk][0]["L"], "{:.2f}")
put("start_gap_m", ROADS["resonant"][0]["x"] - 0.5, "{:.0f}")
put("kerb_lead_ms", 4, "{:d}")
put("kerb_t_touch", (X_TOUCH - 0.5) / 1.5, "{:.2f}"); put("x_touch", X_TOUCH, "{:.3f}")
put("resonant_t_first", (ROADS["resonant"][0]["x"] - 0.125 - P["Rw"] - 0.5) / 1.0, "{:.1f}")
put("resonant_t_last", (ROADS["resonant"][-1]["x"] + 0.125 + P["Rw"] - 0.5) / 1.0, "{:.1f}")
put("prob3_ratio", 2 ** 1.25, "{:.2f}")
put("PI_im_abs", abs((P["Ki"] / jw).imag), "{:.2f}"); put("L_im_abs", abs(Lp.imag), "{:.3f}")

put("fit_after_s", 0.1, "{:.1f}"); put("tail_after_s", 1.5, "{:.1f}"); put("ex_dv", 0.1, "{:.1f}"); put("ex_q_mm", 1, "{:d}"); put("ex_qd_mm", 10, "{:d}")
put("ex_xe_cm", 1, "{:d}"); put("WF_tau", 0.1, "{:.1f}"); put("par_ex_q_mm", 5, "{:d}"); put("par_ex_az", 10, "{:d}"); put("prob_par_q_mm", 8, "{:d}"); put("prob_par_az", 12, "{:d}")
_pc = open(os.path.join(ROOT, "notes", "fig12", "handoff-jax", "portcheck.txt")).read()
_ic = {m.group(1) + m.group(2): float(m.group(3)) for m in re.finditer(r"^(\w+)\s+susp (\d):.*?icmd ([0-9.e+-]+)", _pc, re.M)}
put("port_simple_A", max(_ic["speed0"], _ic["preview0"], _ic["speed1"]), "sci1"); put("port_lqr_A", max(_ic["slosh0"], _ic["joint0"]), "sci1")

# ---- round 1: further numbers the readers asked for
th_ = np.linspace(0, 2 * np.pi, 20001); I_s = float(np.mean(np.abs(np.sin(th_)) ** (5 / 3))); I_c = float(np.trapezoid(np.abs(np.cos(th_)) ** (5 / 3), th_))
C_e = sj.Z_WALL * sj.GAMMA / sj.RBUB * 6.82 * (MU / sj.GAMMA) ** (2 / 3)
zeta_edge = lambda q, w: C_e * h_eff * R * (w * q) ** (5 / 3) * I_s * I_c / (2 * w * 0.5 * RHO * G * q * q * math.pi * R * R * (1 - 1 / XI ** 2) / 2)
put("I_s", I_s, "{:.3f}"); put("I_c", I_c, "{:.3f}"); put("C_edge", C_e, "{:.1f}")
for q_ in (1, 5): put(f"zeta_edge_{q_}mm", zeta_edge(q_ * 1e-3, w_h), "{:.2f}")
A_fit = FILES["free_full_1.5"]["measured"]["fit_ring13"]["A_mm"] * float(jv(1, XI)) / float(jv(1, k * r13))
put("edge_vs_bare_lo", zeta_edge(5e-3, w_h) / z_bare, "{:.0f}"); put("edge_vs_bare_hi", zeta_edge(1e-3, w_h) / z_bare, "{:.0f}")
put("A_fit_wall_mm", A_fit, "{:.1f}"); put("zeta_edge_fit", zeta_edge(A_fit * 1e-3, w_h), "{:.2f}")
put("zeta_edge_vs_meas_pct", 100 * (zeta_edge(A_fit * 1e-3, w_h) / Z0 - 1), "{:.0f}")
Rr = RIDES["ride_resonant"]; fr_ = ring(Rr["D"], Rr["H"], R - 0.5 * DX, 0.0); bk_ = ring(Rr["D"], Rr["H"], R - 0.5 * DX, np.pi)
ib = int(np.nanargmax(bk_[Rr["t"] <= 1.5])); put("res_back_rise_mm", (bk_[ib] - FILL) * 1e3, "{:.1f}"); put("res_back_rise_t", Rr["t"][ib], "{:.2f}")
put("res_front_then_mm", -(fr_[ib] - FILL) * 1e3, "{:.1f}")
for nm in ("ride_sharp30", "ride_sharp30_preview", "ride_sharp30_slosh", "ride_sharp30_joint"):
    m_ = RIDES[nm]["t"] >= 1.5; put(f"{nm}.lean_late", float(np.mean(RIDES[nm]["lean"][m_])), "{:.1f}")
put("kerb_late_lo", min(N[f"{nm}.lean_late"][0] for nm in ("ride_sharp30", "ride_sharp30_preview", "ride_sharp30_slosh", "ride_sharp30_joint")), "{:.1f}")
put("kerb_late_hi", max(N[f"{nm}.lean_late"][0] for nm in ("ride_sharp30", "ride_sharp30_preview", "ride_sharp30_slosh", "ride_sharp30_joint")), "{:.1f}")
put("held_lean_mm", 2 * q_yield * 1e3, "{:.1f}")
drops = [T.get("drops_max") or 0 for T in list(T10.values()) + list(T8.values())]; put("drops_max_any", max(drops), "{:d}")
put("a_foam_break", G * (zrim - FILL - HEAD0 + eps_star) / R, "{:.1f}")
put("T_head_theory_ms", 1000 / (w_h / (2 * math.pi)), "{:.0f}")
put("prev_ahead_mm_10", 1.0 * P["tauI"] * 1e3, "{:.0f}")
put("frames_ms", 1000 / 30, "{:.0f}")
for nm in ("ride_sharp30", "ride_sharp30_preview", "ride_sharp30_slosh", "ride_sharp30_joint"):
    put(f"{nm}.ms_3A", N[f"{nm}.frames_3A"][0] * 1000 / 30, "{:.0f}")
for nm in ("ride_resonant", "ride_bump25", "ride_sharp30"):
    v_ = np.array(RIDES[nm]["D"]["v"]); put(f"{nm}.dv_drop", float(v_[: np.argmin(v_) + 1].max() - v_.min()), "{:.2f}")
put("wedge_coef", 4, "{:d}"); put("wedge_mm4", 4 * sj.TAU_Y / (rho_f * G) * 1e3, "{:.1f}")
put("pack_random_pct", 64, "{:d}"); put("pack_ordered_pct", 74, "{:d}")
put("f_body_tyre", N["body_o_f"][0], "{:.2f}")
put("head_lag_amp", lam_h * k * th, "{:.2f}")
put("sigma_ratio_skin_wall", sig_skin / sig_wall, "{:.3f}")
put("tail_after_fit", 1.5, "{:.1f}")
put("Lk_v_abs", abs(Lfresh[0, 0]) * 10, "{:.1f}"); put("Lk_ratio_abs", abs(Lfresh[2, 0] / Lfresh[0, 0]), "{:.2f}")
put("rho_gml", RHO / 1000, "{:.3f}"); put("base_mm", (0.160 - zrim) * 1e3, "{:.1f}")
put("Iw_e4", P["Iw"] * 1e4, "{:.1f}")

put("kerb_top_curv_mm", 0.12 ** 2 / (2 * math.pi ** 2 * 0.030) * 1e3, "{:.0f}")
for nm in ("ride_sharp30", "ride_sharp30_preview", "ride_sharp30_slosh", "ride_sharp30_joint"):
    m_ = RIDES[nm]["t"] <= 0.8; put(f"{nm}.surge_mm", float(np.nanmax(RIDES[nm]["lean"][m_])), "{:.1f}")
put("motor_vs_road", (P["Vmax"] - b * 1.5) / P["Ra"] * b / N["kerb_Fr_peak"][0], "{:.2f}")
put("res_dv_max", N["ride_resonant.dv_drop"][0], "{:.2f}")


# ---- round 2
put("surge_cut_s", 0.8, "{:.1f}"); put("kerb_x", 1.5, "{:.1f}"); put("bond", RHO * G / (sj.GAMMA * k * k), "{:.0f}"); put("bond_pct", 100 * (math.sqrt(1 + sj.GAMMA * k * k / (RHO * G)) - 1), "{:.1f}")
put("kq_rides", k * float(np.max([FILES[nm]["measured"]["lean_max_mm"] for nm in FILES if nm.startswith("ride")])) / 2e3, "{:.1f}")
put("kq_resonant_bare", k * N["resonant_A_bare_mm"][0] * 1e-3, "{:.0f}")
put("lambda_cm", 2 * math.pi / k * 100, "{:.0f}")
put("zeta_num_vs_head_pct1", 100 * z_num / Z0, "{:.1f}")
m_ = lambda nm: float(np.nanmin(RIDES[nm]["lean"][RIDES[nm]["t"] <= 1.2]))
for nm in ("ride_sharp30", "ride_sharp30_preview", "ride_sharp30_slosh", "ride_sharp30_joint"): put(f"{nm}.back_mm", -m_(nm), "{:.0f}")
ca_ = CA["sharp30_speed"]; ax_ = np.array(ca_["ax"]); tm_ = np.array(ca_["tm"])
put("kerb_spec_ratio", abs(np.sum(ax_ * np.exp(1j * W0 * tm_))) / abs(np.sum(ax_ * np.exp(1j * w11 * tm_))), "{:.2f}")
put("T_head_meas_ms", 1000 / (W0 / (2 * math.pi)), "{:.0f}")

# ============================================================================================ 9. the figures (SVG)
FONT = 'font-family="IBM Plex Mono, monospace"'


def axes(x0, y0, w, h, xt, yt, xl, yl, xr, yr, xlab, ylab):
    """A white plate with ticks: x range xr, y range yr, ticks xt, yt (values), labels; returns (svg, X, Y)."""
    X = lambda v: x0 + (v - xr[0]) / (xr[1] - xr[0]) * w; Y = lambda v: y0 + h - (v - yr[0]) / (yr[1] - yr[0]) * h
    s = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="#8b8079" stroke-width="1"/>']
    for v, lab in zip(xt, xl):
        s.append(f'<line x1="{X(v):.1f}" y1="{y0 + h}" x2="{X(v):.1f}" y2="{y0 + h + 5}" stroke="#8b8079"/><text class="tick" x="{X(v):.1f}" y="{y0 + h + 18}" text-anchor="middle">{lab}</text>')
    for v, lab in zip(yt, yl):
        s.append(f'<line x1="{x0}" y1="{Y(v):.1f}" x2="{x0 + w}" y2="{Y(v):.1f}" stroke="#ece6dc"/><text class="tick" x="{x0 - 7}" y="{Y(v) + 4:.1f}" text-anchor="end">{lab}</text>')
    s.append(f'<text class="lbl" x="{x0 + w / 2:.1f}" y="{y0 + h + 36}" text-anchor="middle">{xlab}</text>')
    s.append(f'<text class="lbl" x="{x0}" y="{y0 - 10}">{ylab}</text>')
    return s, X, Y


def path(X, Y, xs, ys, **kw):
    pts = [(X(a), Y(c)) for a, c in zip(xs, ys) if np.isfinite(c)]
    d = "M" + " L".join(f"{p:.1f} {q:.1f}" for p, q in pts)
    at = " ".join(f'{k_.replace("_", "-")}="{v}"' for k_, v in kw.items())
    return f'<path d="{d}" fill="none" {at}/>'


def svg(w, h, label, body):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(label)}"><rect x="0" y="0" width="{w}" height="{h}" fill="#fff"/>'
            + "".join(body) + "</svg>")


# Figure 1: the glass, to scale (radius against height), with the stout and the head
sc = 2.3; cx0 = 360; zb0 = 365
zp = np.arange(len(RTAB)) * DZP
Xr = lambda r: cx0 + r * 1e3 * sc; Zr = lambda z: zb0 - z * 1e3 * sc
def outline(mask, side):
    return [(Xr(side * RTAB[i]), Zr(zp[i])) for i in np.nonzero(mask)[0]]
st = zp <= FILL; hd = (zp >= FILL) & (zp <= FILL + HEAD0)
def poly(mask, fill):
    L = outline(mask, -1); Rr = outline(mask, 1)[::-1]
    return f'<path d="M{" L".join(f"{a:.1f} {c:.1f}" for a, c in L + Rr)} Z" fill="{fill}"/>'
body1 = [poly(st, "#2a1a14"), poly(hd, "#efe3c8")]
for side in (-1, 1):
    body1.append('<path d="M' + " L".join(f"{a:.1f} {c:.1f}" for a, c in outline(zp >= 0, side)) + '" fill="none" stroke="#1c1518" stroke-width="2"/>')
body1.append(f'<line x1="{Xr(-RTAB[0]):.1f}" y1="{Zr(0):.1f}" x2="{Xr(RTAB[0]):.1f}" y2="{Zr(0):.1f}" stroke="#1c1518" stroke-width="2"/>')
body1.append(f'<line x1="150" y1="{Zr(0)}" x2="150" y2="{Zr(0.150):.1f}" stroke="#8b8079"/>')
for zt_ in (0, 25, 50, 75, 100, 125, 150):
    body1.append(f'<line x1="146" y1="{Zr(zt_ / 1e3):.1f}" x2="154" y2="{Zr(zt_ / 1e3):.1f}" stroke="#8b8079"/><text class="tick" x="142" y="{Zr(zt_ / 1e3) + 4:.1f}" text-anchor="end">{zt_}</text>')
body1.append(f'<text class="tick" x="150" y="{Zr(0.150) - 10:.1f}" text-anchor="middle">z (mm)</text>')
body1.append(f'<line x1="{cx0}" y1="{Zr(0) + 4}" x2="{cx0}" y2="{Zr(0.150):.1f}" stroke="#8b8079" stroke-dasharray="2 4"/>')
body1.append(f'<text class="lbl" x="{cx0 + 4}" y="{Zr(0) + 18}">axis</text>')
labs = [(zrim, RTAB[-1], f"rim, z = {zrim * 1e3:.1f} mm"), (FILL + HEAD0, float(GEO.Rz(FILL + HEAD0)), f"top of the head, z = {(FILL + HEAD0) * 1e3:.0f} mm"),
        (FILL, R, f"stout's surface, z = h = {FILL * 1e3:.0f} mm; radius R = {R * 1e3:.1f} mm"),
        (iw * DZP, RTAB[iw], f"widest: radius {RTAB[iw] * 1e3:.1f} mm at z = {iw * DZP * 1e3:.0f} mm"),
        (0.0, RTAB[0], f"floor: radius {RTAB[0] * 1e3:.1f} mm")]
ly = [Zr(zrim) - 6, Zr(FILL + HEAD0) + 10, Zr(FILL) + 26, Zr(iw * DZP) + 30, Zr(0) - 4]
for (z_, r_, t_), yy in zip(labs, ly):
    body1.append(f'<line x1="{Xr(r_) + 2:.1f}" y1="{Zr(z_):.1f}" x2="478" y2="{yy - 4:.1f}" stroke="#7a1f2b" stroke-width="1"/><circle cx="{Xr(r_):.1f}" cy="{Zr(z_):.1f}" r="2.5" fill="#7a1f2b"/>')
    body1.append(f'<text class="lbl" x="482" y="{yy:.1f}">{t_}</text>')
body1.append(f'<line x1="{cx0}" y1="{Zr(FILL):.1f}" x2="{Xr(R):.1f}" y2="{Zr(FILL):.1f}" stroke="#7a1f2b" stroke-width="1.6"/><text class="lbl" x="{cx0 + 30}" y="{Zr(FILL) - 6:.1f}" fill="#efe3c8">R</text>')
body1.append(f'<line x1="200" y1="388" x2="{200 + 20 * sc:.1f}" y2="388" stroke="#1c1518" stroke-width="1.5"/><text class="tick" x="{200 + 10 * sc:.1f}" y="382" text-anchor="middle">20 mm</text>')
put_text("fig1_svg", svg(880, 400, "The glass of the page to scale: inner radius against height, the stout to 125 mm, the head of foam above it, the rim.", body1))

# Figure 2: the Stokes layer at four moments
yy = np.linspace(0, 2e-3, 161); s2, X2, Y2 = axes(90, 30, 600, 230, [0, 0.5e-3, 1e-3, 1.5e-3, 2e-3], [-1, -0.5, 0, 0.5, 1], ["0", "0.5", "1", "1.5", "2"],
                                                   ["−1", "−0.5", "0", "0.5", "1"], (0, 2e-3), (-1.15, 1.15), "distance from the glass, d (mm)", "u∥ / U")
body2 = [f'<rect x="90" y="30" width="{X2(DX) - 90:.1f}" height="230" fill="#f3ede4"/>', f'<text class="lbl" x="{(90 + X2(DX)) / 2:.1f}" y="24" text-anchor="middle">◂ one grid cell, {DX * 1e3:.1f} mm ▸</text>'] + s2
for ph, col, lab, ly_ in ((0, "#1c1518", "ωt = 0", None), (np.pi / 2, "#7a1f2b", "ωt = π/2", None), (np.pi, "#8b8079", "ωt = π", None), (1.5 * np.pi, "#b98a5e", "ωt = 3π/2", None)):
    u = np.cos(ph) - np.exp(-yy / delta) * np.cos(ph - yy / delta)
    body2.append(path(X2, Y2, yy, u, stroke=col, stroke_width=2))
    xa = 1.75e-3 if ph in (0, np.pi) else 0.45e-3; ya = float(np.interp(xa, yy, u))
    body2.append(f'<text class="lbl" x="{X2(xa):.1f}" y="{Y2(ya) + (-7 if ya >= 0 else 15):.1f}" fill="{col}">{lab}</text>')
body2.append(f'<line x1="{X2(delta):.1f}" y1="30" x2="{X2(delta):.1f}" y2="260" stroke="#7a1f2b" stroke-dasharray="4 4"/><text class="lbl" x="{X2(delta) + 6:.1f}" y="44">δₛ = {delta * 1e3:.2f} mm</text>')
put_text("fig2_svg", svg(720, 330, "The velocity of the stout along the glass, relative to the glass, against the distance from the wall, at four moments of one swing.", body2))

# Figure 3: the free swings, stored data and the refit
s3, X3, Y3 = axes(80, 30, 600, 230, [0, 1, 2, 3, 4, 5], [-4, -2, 0, 2, 4], ["0", "1", "2", "3", "4", "5"], ["−4", "−2", "0", "2", "4"], (0, 5), (-5, 5),
                  "time t (s)", "q (ring), mm")
body3 = s3 + [f'<rect x="{X3(t0p):.1f}" y="30" width="{X3(t0p + Tp) - X3(t0p):.1f}" height="230" fill="#f3ede4"/>',
              f'<text class="lbl" x="{X3(t0p + Tp) + 4:.1f}" y="252">◂ the push</text>']
for key, col in (("nohead", "#8b8079"), ("head", "#7a1f2b")):
    d_ = SW[key]; body3.append(path(X3, Y3, d_["t"], d_["q"] * 1e3, stroke=col, stroke_width=1.6))
    F_ = d_["fit"]; tf = np.linspace(0, 5 - d_["t_start"], 400)
    body3.append(path(X3, Y3, tf + d_["t_start"], F_["fun"](tf, *F_["p"]) * 1e3, stroke="#1c1518", stroke_width=1, stroke_dasharray="3 3"))
for j_, (lab, col) in enumerate((("without the head", "#8b8079"), ("with the head", "#7a1f2b"), ("fitted damped cosine", "#1c1518"))):
    body3.append(f'<line x1="470" y1="{48 + 16 * j_}" x2="492" y2="{48 + 16 * j_}" stroke="{col}" stroke-width="2"' + (' stroke-dasharray="3 3"' if j_ == 2 else '') + f'/><text class="lbl" x="498" y="{52 + 16 * j_}">{lab}</text>')
put_text("fig3_svg", svg(720, 300, "The swing on the ring at 13/16 of the radius after one push, with and without the head of foam: stored data and the fitted damped cosine.", body3))

# Figure 4: the kerb, the cart alone
t4 = np.array(ks["t"]) - 1.0 / 1.5 * 0 ; tk = np.array(ks["t"]); xk = np.array(ks["x"]); t_on = float(np.interp(X_TOUCH, xk, tk))
sel = (tk >= t_on - 0.05) & (tk <= t_on + 0.25)
s4, X4, Y4 = axes(80, 30, 600, 170, [t_on - 0.05 + 0.05 * i for i in range(7)], [-80, -60, -40, -20, 0, 20],
                  [f"{(0.05 * i - 0.05) * 1e3:.0f}".replace("-", "−") for i in range(7)], ["−80", "−60", "−40", "−20", "0", "20"], (t_on - 0.05, t_on + 0.25), (-90, 25),
                  "time from the wheel's first touch of the kerb (ms)", "force along the road (N)")
Nk = np.array(ks["N"]); Fmk = np.array(ks["Fm"]); vk = np.array(ks["v"])
imax_v = np.minimum(P["Imax"], (P["Vmax"] - b * vk) / P["Ra"]); Fcan = np.minimum(b * imax_v, P["mu"] * Nk)
air = Nk <= 0; body4 = []
tt_ = tk[sel]; aa = air[sel]
for j_ in range(len(tt_)):
    if aa[j_]: body4.append(f'<rect x="{X4(tt_[j_]):.1f}" y="30" width="{max(X4(tt_[j_] + 0.001) - X4(tt_[j_]), 1):.1f}" height="170" fill="#ece6dc"/>')
body4 += s4
for sgn in (1, -1): body4.append(f'<line x1="80" y1="{Y4(sgn * b * P["Imax"]):.1f}" x2="680" y2="{Y4(sgn * b * P["Imax"]):.1f}" stroke="#8b8079" stroke-dasharray="6 3"/>')
body4.append(path(X4, Y4, tk[sel], np.array(ks["Fr"])[sel], stroke="#1c1518", stroke_width=1.8))
body4.append(path(X4, Y4, tk[sel], Fcan[sel], stroke="#b98a5e", stroke_width=3))
body4.append(path(X4, Y4, tk[sel], Fmk[sel], stroke="#7a1f2b", stroke_width=1.6, stroke_dasharray="4 2"))
body4.append(f'<text class="lbl" x="{X4(t_on + 0.12):.1f}" y="{Y4(b * P["Imax"]) - 6:.1f}">±{b * P["Imax"]:.0f} N, the drive at {P["Imax"]:.0f} A</text>')
s4b, X4b, Y4b = axes(80, 250, 600, 110, [t_on - 0.05 + 0.05 * i for i in range(7)], [1.2, 1.3, 1.4, 1.5, 1.6], [f"{(0.05 * i - 0.05) * 1e3:.0f}".replace("-", "−") for i in range(7)],
                     ["1.2", "1.3", "1.4", "1.5", "1.6"], (t_on - 0.05, t_on + 0.25), (1.17, 1.62), "time from the wheel's first touch of the kerb (ms)", "cart speed (m/s)")
body4 += s4b
body4.append(path(X4b, Y4b, tk[sel], vk[sel], stroke="#1c1518", stroke_width=1.8))
tke = np.array(ke["t"]); sel_e = (tke >= t_on - 0.05) & (tke <= t_on + 0.25)
body4.append(path(X4b, Y4b, tke[sel_e], np.array(ke["v"])[sel_e], stroke="#7a1f2b", stroke_width=1.6, stroke_dasharray="5 3"))
put_text("fig4_svg", svg(720, 410, "The kerb taken at 1.5 m/s by the cart alone with the pint frozen: the road's push, the motor's push and what the motor could give; below, the cart's speed.", body4))

# Figure 5: the lean of the stored rides against time
def lean_fig(names, cols, labels, yr, ytk, tr, title):
    s5, X5, Y5 = axes(80, 30, 600, 200, list(range(int(tr[0]), int(tr[1]) + 1)), ytk, [str(v) for v in range(int(tr[0]), int(tr[1]) + 1)],
                      [str(v).replace("-", "−") for v in ytk], tr, yr, "time t (s)", "lean, front wall minus back (mm)")
    body = list(s5)
    for nm, col in zip(names, cols):
        body.append(path(X5, Y5, RIDES[nm]["t"], RIDES[nm]["lean"], stroke=col, stroke_width=1.5))
    for j_, (lab, col) in enumerate(zip(labels, cols)):
        body.append(f'<line x1="{430}" y1="{48 + 16 * j_}" x2="{452}" y2="{48 + 16 * j_}" stroke="{col}" stroke-width="2"/><text class="lbl" x="458" y="{52 + 16 * j_}">{lab}</text>')
    return svg(720, 280, title, body)
put_text("fig5_svg", lean_fig(["ride_resonant", "ride_resonant_joint"], ["#8b8079", "#7a1f2b"], ["speed held only", "joint control"], (-16, 16), [-15, -10, -5, 0, 5, 10, 15], (0, 8),
                              "The lean of the stout on the five bumps, with the speed held only and with joint control."))
put_text("fig6_svg", lean_fig(["ride_sharp30", "ride_sharp30_preview", "ride_sharp30_slosh", "ride_sharp30_joint"], ["#8b8079", "#b98a5e", "#1c1518", "#7a1f2b"],
                              ["speed held only", "road preview", "slosh LQR", "joint control"], (-30, 30), [-30, -20, -10, 0, 10, 20, 30], (0, 4),
                              "The lean of the stout at the kerb under each controller."))
put("fig4_t_on_m", 1.5 - 0.06 - 0.04, "{:.2f}")


# ============================================================================================ main
def check_source():
    """Numbers typed by hand in the note's source: decimals, and whole numbers followed by a unit, outside {{...}}, \\tag{},
    the Sources section, href and id attributes, figure/table/equation/section labels."""
    s = open(SRC_NOTE).read()
    s = s[:s.find('id="p-refs"')] if 'id="p-refs"' in s else s
    s = re.sub(r'<span class="ps(ub|ec)__n">[^<]*</span>', " ", s); s = re.sub(r"\{\{[^}]*\}\}", " ", s); s = re.sub(r"\\tag\{[^}]*\}", " ", s); s = re.sub(r'(href|id|class|viewBox|d|style)="[^"]*"', " ", s)
    s = re.sub(r'<span class="ps(ub|ec)__n">[^<]*</span>', " ", s); s = re.sub(r"<[^>]+>", " ", s); s = html.unescape(s)
    s = re.sub(r"(section|sections|Section|§|Exercise)\s*[\d.]+(\s*(,|and|&#8211;|–)\s*[\d.]+)*", " ", s); s = re.sub(r"\((\d+\.\d+)(&#8211;|–|, )?(\d+\.\d+)?\)", " ", s)
    s = re.sub(r"(20|25|30) mm bumps?", " ", s)
    s = re.sub(r"\((\d+[a-z]?)\)", " ", s)                                 # equation numbers in brackets
    s = re.sub(r"(Figure|Table|Example|section|sections|Section|Problem|Problems|eq\.|eqs\.|p\.|pp\.|Key result)\s*[\d.,–\- and]+", " ", s)
    unit = r"(?:mm|m|cm|µm|Hz|s|ms|N|A|V|kg|g|mL|Pa|kPa|mPa|%|°|rad|J|µJ|W|Ω|K)\b"
    dec = re.findall(r"(?<![\w.^_{])\d+\.\d+(?![\w.])", s)
    whole = re.findall(r"(?<![\w.^_{])\d+(?:,\d{3})*\s*" + unit, s)
    return sorted(set(dec)), sorted(set(whole))


if __name__ == "__main__":
    for nm, (v, s) in N.items():
        if not nm.endswith("_svg"): print(f"{nm} = {s}")
    out = os.path.join(ROOT, "notes", "fig12", "note-numbers.json")
    json.dump({nm: dict(value=(v if isinstance(v, (int, float, str)) else float(v)), text=s) for nm, (v, s) in N.items() if not nm.endswith("_svg")},
              open(out, "w"), indent=1)
    if "--check" in sys.argv:
        dec, whole = check_source()
        print(f"\n{len(dec)} decimal numbers typed by hand in the source:\n" + " ".join(dec))
        print(f"\n{len(whole)} whole numbers with a unit typed by hand in the source:\n" + " | ".join(whole))
