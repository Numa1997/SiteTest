"""Store a generation of Fig. 12 rides computed on Kaggle in public/data/fig12/<date>/: rides.json as Kaggle wrote it, and
index.json (notebook, version, machine, code commit, measured times, SHA-256 and size of each file).
Run: python3 tools/fig12/kaggle/store_rides.py <rides.json> <timing.json> <date> <notebook version> <code commit>"""
import hashlib, json, os, shutil, sys
src, timing_path, date, version, commit = sys.argv[1:6]
here = os.path.dirname(os.path.abspath(__file__)); out = os.path.normpath(os.path.join(here, "..", "..", "..", "public", "data", "fig12", date))
os.makedirs(out, exist_ok=True); dst = os.path.join(out, "rides.json"); shutil.copyfile(src, dst)
D = json.load(open(dst)); T = json.load(open(timing_path)); b = open(dst, "rb").read()
idx = dict(about=f"Fig. 12 computed on Kaggle: stored rides of the pint on the one-wheel cart, played back by public/simulations/guinness-kaggle.html. Generated on Kaggle on {date}.",
           generated=date,
           kaggle=dict(notebook="numakoudsie/guinness-on-a-cart-stout-sloshing", url="https://www.kaggle.com/code/numakoudsie/guinness-on-a-cart-stout-sloshing",
                       version=int(version), machine="Tesla T4 GPU", output_file="rides.json"),
           code=f"Solver v2 (tools/fig12/kaggle/solver.py at SiteTest commit {commit}): Taichi 1.7.4 APIC on a 1.5 mm grid, ghost-fluid free surface, "
                f"free-slip glass faces on the grid, the Fig. 12 note's wall (Stokes layer) and foam (Sauret et al. 2015) friction; model {json.dumps(D.get('model'))}",
           rides=[dict(road=r["road"], v0=r["v0"], frames=r["n"], seconds=round((r["n"] - 1) / D["fps"], 3)) for r in D["rides"]],
           measured=dict(minutes_per_ride=[round(t["measured_min"], 1) for t in T], steps_per_ride=[t["steps"] for t in T],
                         ms_per_step=[round(t["wall_s"] / t["steps"] * 1e3) for t in T], cg_iterations_per_step=[round(t["cg_iterations"] / t["steps"]) for t in T]),
           files=[dict(path="rides.json", bytes=len(b), sha256=hashlib.sha256(b).hexdigest())])
json.dump(idx, open(os.path.join(out, "index.json"), "w"), indent=1)
print(out, len(b), idx["files"][0]["sha256"])
