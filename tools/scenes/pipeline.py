"""The scenes pipeline: Kaggle computes, GitHub stores, Cloudflare serves. Run by .github/workflows/scenes-kaggle.yml.

For one scene (a model file tools/scenes/<scene>.py with a run(out_dir) function) it:
  1. writes the notebook folder: kernel-metadata.json and the script tools/scenes/kaggle_scenes.py with JOB = <scene> and
     COMMIT = the commit being run, so Kaggle computes exactly the code in git;
  2. pushes it as a new version of the private CPU notebook numakoudsie/scenes-living-backgrounds (`kaggle kernels push`);
  3. polls `kaggle kernels status` every 20 s until the run is complete (or fails, or the time limit passes);
  4. downloads the run's output (`kaggle kernels output`), finds index-<scene>.json, and checks every listed file's size and
     SHA-256 against it;
  5. copies the files to public/data/scenes/<date of generation>/ and adds the generation to public/data/scenes/generations.json.
The workflow then commits and pushes; Cloudflare Workers Builds publishes the site.

Authentication: the official Kaggle tool reads the environment variable KAGGLE_API_TOKEN (a repository secret of the same name).
Kaggle's `kernels push` exits with status 0 even when Kaggle refuses the push, so its printed answer is read and checked.

Usage: python3 tools/scenes/pipeline.py <scene> <commit> [--kaggle <command>] [--timeout <s>]
Exit status 0 only when every check passed; anything else stops the workflow before a commit."""
import argparse, datetime, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OWNER, SLUG, TITLE = "numakoudsie", "scenes-living-backgrounds", "Scenes living backgrounds"
REF = f"{OWNER}/{SLUG}"

def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)

def kaggle(cmd, args):
    r = subprocess.run(cmd + args, capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    log("$ kaggle " + " ".join(args)); log(out.strip()[-1500:])
    return r.returncode, out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("scene"); ap.add_argument("commit")
    ap.add_argument("--kaggle", default="kaggle"); ap.add_argument("--timeout", type=int, default=1800)
    a = ap.parse_args(); K = a.kaggle.split()
    if not re.fullmatch(r"[a-z0-9_]+", a.scene) or not os.path.exists(os.path.join(ROOT, "tools/scenes", a.scene + ".py")):
        sys.exit(f"no model tools/scenes/{a.scene}.py")
    if not re.fullmatch(r"[0-9a-f]{40}", a.commit): sys.exit("commit must be a full 40-character hash")
    # 1. the notebook folder
    nb = tempfile.mkdtemp(prefix="nb-")
    src = open(os.path.join(ROOT, "tools/scenes/kaggle_scenes.py")).read()
    src = re.sub(r'^JOB = "[^"]*"', f'JOB = "{a.scene}"', src, count=1, flags=re.M)
    src = src.replace("__COMMIT__", a.commit)
    assert f'JOB = "{a.scene}"' in src and a.commit in src
    open(os.path.join(nb, "kaggle_scenes.py"), "w").write(src)
    json.dump(dict(id=REF, title=TITLE, code_file="kaggle_scenes.py", language="python", kernel_type="script", is_private=True,
                   enable_gpu=False, enable_tpu=False, enable_internet=True, dataset_sources=[], competition_sources=[],
                   kernel_sources=[], model_sources=[]), open(os.path.join(nb, "kernel-metadata.json"), "w"), indent=1)
    # 2. push
    rc, out = kaggle(K, ["kernels", "push", "-p", nb])
    m = re.search(r"version\s+(\d+)\s+successfully pushed", out, re.I)
    if rc or not m: sys.exit("Kaggle did not accept the push (its answer is above)")
    version = int(m.group(1)); log("pushed version", version)
    # 3. wait
    t0 = time.time(); state = ""
    while time.time() - t0 < a.timeout:
        time.sleep(float(os.environ.get("POLL_S", 20)))
        rc, out = kaggle(K, ["kernels", "status", REF])
        mm = re.search(r'status\s+"?([A-Za-z_.]+)"?', out)
        state = (mm.group(1) if mm else out).lower()
        if "complete" in state: break
        if any(w in state for w in ("error", "cancel")): sys.exit(f"the Kaggle run ended in state {state}")
    else:
        sys.exit(f"no result within {a.timeout} s (last state: {state})")
    log("run complete after", round(time.time() - t0), "s")
    # 4. download and check
    dl = tempfile.mkdtemp(prefix="out-")
    rc, out = kaggle(K, ["kernels", "output", REF, "-p", dl])
    if rc: sys.exit("download failed")
    idx = [os.path.join(d, f) for d, _, fs in os.walk(dl) for f in fs if f == f"index-{a.scene}.json"]
    if len(idx) != 1: sys.exit(f"expected one index-{a.scene}.json in the output, found {len(idx)}")
    index = json.load(open(idx[0])); here = os.path.dirname(idx[0])
    if index.get("job") != a.scene or index["source"]["commit"] != a.commit: sys.exit("the output index names another scene or commit")
    for f, meta in index["files"].items():
        b = open(os.path.join(here, f), "rb").read()
        if len(b) != meta["bytes"] or hashlib.sha256(b).hexdigest() != meta["sha256"]: sys.exit(f"{f}: size or SHA-256 differs from the index")
    log("all", len(index["files"]), "files match their SHA-256")
    # 5. into the site
    day = index["date"]; dest = os.path.join(ROOT, "public/data/scenes", day); os.makedirs(dest, exist_ok=True)
    for f in list(index["files"]) + [f"index-{a.scene}.json"]: shutil.copy2(os.path.join(here, f), os.path.join(dest, f))
    gp = os.path.join(ROOT, "public/data/scenes/generations.json")
    g = json.load(open(gp)) if os.path.exists(gp) else dict(about="Data of the living scenes (public/scripts/bg-scenes.js), computed on Kaggle by the notebook "
        f"{REF} and carried here by .github/workflows/scenes-kaggle.yml. Newest last; a scene plays its newest entry.", generations=[])
    g["generations"].append(dict(scene=a.scene, date=day, notebook=REF, version=version, commit=a.commit,
                                 index=f"{day}/index-{a.scene}.json", files={f: v for f, v in index["files"].items()},
                                 wall_s=round(index.get("wall_s", 0), 1), collected=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")))
    json.dump(g, open(gp, "w"), indent=1, ensure_ascii=False); open(gp, "a").write("\n")
    log(f"stored under public/data/scenes/{day}/, generations.json updated")
    if os.environ.get("GITHUB_OUTPUT"):
        open(os.environ["GITHUB_OUTPUT"], "a").write(f"version={version}\nday={day}\n")

if __name__ == "__main__":
    main()
