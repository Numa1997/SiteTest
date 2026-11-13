"""Merges version 2 of the 3D runs (numakoudsie/schrodinger-shapes-3d, version 2, on the GPUs: the 243 runs whose start
wave was wrong in version 1; the same runs were also started on four CPU notebooks ...-v2-a to -d, whose output is not used) into the website's 3D generation: unpacks each part, checks every SHA-256, replaces the run files and
their index entries (marked v = 2), sets the shell constants of version 2 and records the source.
Usage: python3 merge_v2.py <public/data/schrodinger-sphere/<date>/shapes3d> <commit> <part-folder> [<part-folder> ...]"""
import hashlib, json, os, sys, tarfile
dst, commit, parts = sys.argv[1], sys.argv[2], sys.argv[3:]
ix = json.load(open(os.path.join(dst, "index.json"))); by = {r["file"]: n for n, r in enumerate(ix["runs"])}
done = 0; walls = 0.0
for part in parts:
    px = json.load(open(os.path.join(part, "index.json")))
    assert not px["failed"] and not px["not_started"], (part, px["failed"], px["not_started"])
    for sh in px["groups"]:
        t = os.path.join(part, sh + ".tar")
        if os.path.exists(t):
            with tarfile.open(t) as tf:
                for m in tf.getmembers():
                    if m.isfile() and m.name.startswith(sh + "/") and ".." not in m.name: tf.extract(m, dst, filter="data")
    for r in px["runs"]:
        for f, h in ((r["file"], r["sha256"]), (r.get("wave_file"), r.get("wave_sha256"))):
            if f: assert hashlib.sha256(open(os.path.join(dst, f), "rb").read()).hexdigest() == h, f
        r["v"] = 2; ix["runs"][by[r["file"]]] = r; done += 1; walls += r["wall"]
    ix["shell"] = px["shell"]
ix["version2"] = dict(runs=done, what="hard walls: start wave zero inside; spherical wave from the side: source at -17, r0 = 5, starts outside the barrier",
                      kaggle="numakoudsie/schrodinger-shapes-3d", version="2", commit=commit, device="2 x Tesla T4", gpu_seconds=round(walls, 1))
json.dump(ix, open(os.path.join(dst, "index.json"), "w"), separators=(",", ":"))
print(f"{done} runs replaced, all SHA-256 checked; {walls/3600:.2f} device hours of runs")
