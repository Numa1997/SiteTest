"""Fig. 12 note (public/simulations/guinness-kaggle.html): every number the note quotes, printed from the stored runs and the
model's parameters, so that none is typed in by hand.

Sources, all in the repository:
  public/data/fig12/2026-11-13-run8/index-jax.json and its ride files   the rides the page plays (runs 8 and 9, run 6's free_wall)
  notes/fig12/jax/run8-check/run8-summary.json, run9-summary.json       what run_b.py wrote on Kaggle (fits, books, times, gains)
  tools/fig12/kaggle/stout_jax.py                                       the model's constants (head, glass, cart)
Run:  python3 tools/fig12/kaggle/note_numbers.py            prints name = value, one per line, and writes notes/fig12/note-numbers.json
      python3 tools/fig12/kaggle/note_numbers.py --check    also lists every number in the note's text that no entry prints
                                                            (a number of the note must either appear here or be a label, a year,
                                                            an equation or section number, or a source's page)"""
import json, math, os, re, sys, html

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
DATA = os.path.join(ROOT, "public", "data", "fig12", "2026-11-13-run8")
CHK = os.path.join(ROOT, "notes", "fig12", "jax", "run8-check")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("GLASS_JSON", "")
N = {}   # name -> (value, printed text)


def put(name, value, fmt):
    N[name] = (value, fmt.format(value))


# ---- the model's constants (stout_jax.py) -------------------------------------------------------------------------------
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "stout_jax.py")).read()
const = lambda nm: float(re.search(r"^%s\s*=\s*([0-9.eE+-]+)" % nm, src, re.M).group(1))
PHI_F, HEAD0 = const("PHI_F"), const("HEAD0")
RHO, G, FILL = 1007.0, 9.81, 0.125
XI1, R_S = 1.8412, 0.0391                      # first zero of J1' and the surface's radius at the fill (run_b.py)
k = XI1 / R_S; th = math.tanh(k * FILL)
w_bare = math.sqrt(G * k * th)
put("k_theory_per_m", k, "{:.1f}")
put("f_bare_Hz", w_bare / (2 * math.pi), "{:.3f}")
mu = PHI_F * HEAD0
put("head_mass_per_area_kg_m2", PHI_F * RHO * HEAD0, "{:.2f}")
put("head_density_kg_m3", PHI_F * RHO, "{:.0f}")
put("head_thickness_mm", HEAD0 * 1e3, "{:.0f}")
put("mu_mm", mu * 1e3, "{:.2f}")
fac = 1 + mu * k * th
put("head_mass_factor_inertia", fac, "{:.3f}")
put("head_mass_factor_freq", 1 / math.sqrt(fac), "{:.3f}")
put("f_with_head_mass_theory_Hz", w_bare / (2 * math.pi) / math.sqrt(fac), "{:.3f}")
beta = 2 * XI1 * math.tanh(XI1 * FILL / R_S) / (XI1 ** 2 - 1)
put("beta_bare", beta, "{:.3f}")
put("beta_with_head", beta / fac, "{:.3f}")

# ---- the run's own record ------------------------------------------------------------------------------------------------
S8 = json.load(open(os.path.join(CHK, "run8-summary.json"))); S9 = json.load(open(os.path.join(CHK, "run9-summary.json")))
T = {t["name"]: t for t in S8["tasks"] + S9["tasks"]}
F = T["free_full_1.5"]["fit_ring13"]
put("swing_f0_Hz", F["f0"], "{:.3f}"); put("swing_fd_Hz", F["f"], "{:.3f}"); put("swing_zeta", F["zeta"], "{:.3f}")
put("swing_f0_vs_theory_pct", 100 * (F["f0"] / (w_bare / (2 * math.pi) / math.sqrt(fac)) - 1), "{:.1f}")
put("swing_omega_rad_s", 2 * math.pi * F["f0"], "{:.2f}")
put("run8_task_seconds", sum(t["run_s"] for t in S8["tasks"]), "{:.0f}")
put("run9_task_seconds", S9["tasks"][0]["run_s"], "{:.0f}")
put("particles", T["rest"]["particles"], "{:,}")
put("cells", T["rest"]["cells"], "{:,}")
for nm, t in T.items():
    if "ms_per_step" in t: put(f"{nm}.ms_per_step", t["ms_per_step"], "{:.1f}")
K = T["ride_sharp30_joint"].get("K") or T["ride_sharp30_joint"].get("control", {}).get("gains", {}).get("K")

# ---- the stored rides (what the page plays) --------------------------------------------------------------------------------
I = json.load(open(os.path.join(DATA, "index-jax.json")))
herr, perr = 0.0, 0
for f in I["files"]:
    nm = f["path"][:-5]; m = f["measured"]
    put(f"{nm}.lean_mm", m["lean_max_mm"], "{:.1f}" if m["lean_max_mm"] >= 2 else "{:.2f}")
    put(f"{nm}.tilt_mm", m["tilt_max_mm"], "{:.1f}" if m["tilt_max_mm"] >= 2 else "{:.2f}")
    put(f"{nm}.head_spilled_mL", m["head_spilled_ml"], "{:.2f}")
    put(f"{nm}.stout_spilled_g", m["spilled_g"], "{:.3f}")
    if m.get("i_max_stored_A") is not None: put(f"{nm}.i_max_A", m["i_max_stored_A"], "{:.2f}")
    b = m.get("books") or {}
    if b:
        herr = max(herr, b.get("head_err_ml_max") or 0.0); perr = max(perr, b.get("stout_err_particles_max") or 0)
        put("head_served_mL", b["head_ml0"], "{:.3f}"); put("stout_g", b["stout_glass_g_end"] + b["stout_out_g_end"], "{:.3f}")
    g = (m.get("control") or {}).get("gains")
    if g and nm == "ride_sharp30_joint": K = g["K"]
put("books_head_err_mL_max", herr, "{:.1e}"); put("books_stout_err_particles_max", perr, "{:d}")
for i, v in enumerate(K or []): put(f"K{i + 1}", v, "{:.3f}")
lean = lambda nm: N[nm + ".lean_mm"][0]
put("resonant_joint_lean_cut_pct", 100 * (1 - lean("ride_resonant_joint") / lean("ride_resonant")), "{:.0f}")
put("bump25_joint_lean_cut_pct", 100 * (1 - lean("ride_bump25_joint") / lean("ride_bump25")), "{:.0f}")

if __name__ == "__main__":
    for nm, (v, s) in N.items(): print(f"{nm} = {s}")
    out = os.path.join(ROOT, "notes", "fig12", "note-numbers.json")
    json.dump({nm: dict(value=v, text=s) for nm, (v, s) in N.items()}, open(out, "w"), indent=1)
    if "--check" in sys.argv:
        page = open(os.path.join(ROOT, "public", "simulations", "guinness-kaggle.html")).read()
        a = page.index('<article class="paper" id="paper"'); b = page.index("</article>", a)
        text = html.unescape(re.sub(r"<[^>]+>", " ", page[a:b]))
        known = {s.replace(",", "") for _, s in N.values()}
        found = re.findall(r"(?<![\w.])\d{1,3}(?:,\d{3})*(?:\.\d+)?(?![\w.]\d)", text)
        miss = sorted({x for x in found if ("." in x or "," in x) and x.replace(",", "") not in known}, key=lambda x: float(x.replace(",", "")))
        print(f"\n{len(miss)} decimal numbers in the note that no entry prints:\n" + " ".join(miss))
