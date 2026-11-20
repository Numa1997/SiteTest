"""Fig. 16: build public/simulations/guinness-cart-control.html from its source notes/fig16/page/guinness-cart-control.src.html, filling
every {{key}} with a number read from the stored data: the rides' index (public/data/fig16/2026-11-14/index-16.json), the run's summary
(notes/fig16/run16-v2-summary.json, downloaded from the Kaggle notebook's output), Fig. 12's index (public/data/fig12/2026-11-14-run10/
index-jax.json) and the stored ride files. No number in the page is typed by hand. The navigation is copied from Fig. 12's page with
Fig. 16 added. Run: python3 tools/fig16/build_page.py  (--check: fail if the page on disk differs from what would be built)."""
import json, math, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P = lambda *a: os.path.join(ROOT, *a)
I16 = json.load(open(P("public", "data", "fig16", "2026-11-14", "index-16.json")))
I12 = json.load(open(P("public", "data", "fig12", "2026-11-14-run10", "index-jax.json")))
S = json.load(open(P("notes", "fig16", "run16-v2-summary.json")))
f16 = {f["path"][:-5]: f for f in I16["files"]}; f12 = {f["path"][:-5]: f for f in I12["files"]}
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
    f12_kerb_tilt=f"{f12['ride_sharp30_slosh']['measured']['tilt_max_mm']:.1f}", f12_kerb_head=f"{f12['ride_sharp30_slosh']['measured']['head_spilled_ml']:.2f}",
    f12_res_tilt=f"{f12['ride_resonant_joint']['measured']['tilt_max_mm']:.2f}", f12_res_head=f"{f12['ride_resonant_joint']['measured']['head_spilled_ml']:.2f}",
    f12_b25_tilt=f"{f12['ride_bump25_joint']['measured']['tilt_max_mm']:.2f}", f12_b25_head=f"{f12['ride_bump25_joint']['measured']['head_spilled_ml']:.2f}",
    f16_kerb_tilt=f"{f16['kerb_full']['measured']['tilt_max_mm']:.1f}", f16_kerb_head=f"{f16['kerb_full']['measured']['head_spilled_ml']:.3f}",
    f16_res_tilt=f"{f16['resonant_full']['measured']['tilt_max_mm']:.2f}", f16_res_head=f"{f16['resonant_full']['measured']['head_spilled_ml']:.2f}",
    f16_b25_tilt=f"{f16['bump25_full']['measured']['tilt_max_mm']:.2f}", f16_b25_head=f"{f16['bump25_full']['measured']['head_spilled_ml']:.2f}",
    f16_kerb_pitch=f"{f16['kerb_full']['measured']['pitch_max_deg']:.1f}", f16_kerb_i=f"{f16['kerb_full']['measured']['i_max_A']:.0f}",
    f16_kerb_u=f"{f16['kerb_full']['measured']['u_max_N']:.0f}",
    off_pitch=f"{f16['kerb_off']['measured']['pitch_max_deg']:.0f}", off_end_s=f"{off['t'][-1]:.2f}",
    off_head=f"{f16['kerb_off']['measured']['head_spilled_ml']:.2f}", off_stout=f"{f16['kerb_off']['measured']['spilled_g']:.1f}",
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
