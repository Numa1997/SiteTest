"""Files the output of numakoudsie/schrodinger-shapes-3d into the website: unpacks the tar of each shape, checks the SHA-256 of
every file against the notebook's index.json, writes the index with its source, and adds the generation to generations.json.
Usage: python3 to_site_shapes3d.py <downloaded-output-folder (holds index.json and <shape>.tar)> <public/data/schrodinger-sphere> <date> <version> <commit>"""
import hashlib, json, os, sys, tarfile
src, proj, date, ver, commit = sys.argv[1:6]
dst = os.path.join(proj, date, "shapes3d"); os.makedirs(dst, exist_ok=True)
ix = json.load(open(os.path.join(src, "index.json")))
for sh in ix["groups"]:
    t = os.path.join(src, sh + ".tar")
    if os.path.exists(t):
        with tarfile.open(t) as tf:
            for m in tf.getmembers():
                if m.isfile() and m.name.startswith(sh + "/") and ".." not in m.name: tf.extract(m, dst, filter="data")
    elif os.path.isdir(os.path.join(src, sh)):
        os.makedirs(os.path.join(dst, sh), exist_ok=True)
        for f in os.listdir(os.path.join(src, sh)): os.replace(os.path.join(src, sh, f), os.path.join(dst, sh, f))
bad = []
for r in ix["runs"]:
    for f, h in ((r["file"], r["sha256"]), (r.get("wave_file"), r.get("wave_sha256"))):
        if not f: continue
        p = os.path.join(dst, f)
        if not os.path.exists(p) or hashlib.sha256(open(p, "rb").read()).hexdigest() != h: bad.append(f)
assert not bad, f"{len(bad)} files missing or with a wrong SHA-256, e.g. {bad[:5]}"
ix["source"] = dict(kaggle="numakoudsie/schrodinger-shapes-3d", version=ver, commit=commit, solver="tools/kaggle/schrodinger-shapes/solver3d.py",
                    run="tools/kaggle/schrodinger-shapes/shapes3d_run.py", builder="tools/kaggle/schrodinger-shapes/build_shapes3d.py")
json.dump(ix, open(os.path.join(dst, "index.json"), "w"), separators=(",", ":"))
gp = os.path.join(proj, "generations.json"); gens = json.load(open(gp))
gens = [g for g in gens if g["index"] != f"{date}/shapes3d/index.json"] + [dict(date=date, index=f"{date}/shapes3d/index.json", kind="shapes3d",
        shape="coin, tube, sphere wells and hard ball, spherical wave from the side", runs=len(ix["runs"]), kaggle="numakoudsie/schrodinger-shapes-3d", version=ver, commit=commit)]
json.dump(gens, open(gp, "w"), indent=1)
size = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(dst) for f in fs)
print(f"{len(ix['runs'])} runs, all SHA-256 checked, {size/1e6:.0f} MB in {dst}; failed on Kaggle {len(ix['failed'])}, not started {len(ix['not_started'])}")
