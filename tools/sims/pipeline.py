"""The simulations pipeline: Kaggle computes, GitHub stores, Cloudflare serves. Run by .github/workflows/sims-kaggle.yml.

For one simulation (a model file tools/sims/<sim>.py with a run(out_dir) function, listed in tools/sims/registry.json) it:
  1. writes the notebook folder: kernel-metadata.json and the script tools/sims/kaggle_sims.py with JOB = <sim> and
     COMMIT = the commit being run, so Kaggle computes exactly the code in git;
  2. pushes it as a new version of the private CPU notebook numakoudsie/phyein-usul-simulations (`kaggle kernels push`);
  3. polls `kaggle kernels status` every 20 s until the run is complete (or fails, or the time limit passes);
  4. downloads the run's output (`kaggle kernels output`), finds index-<sim>.json, and checks every listed file's size and
     SHA-256 against it;
  5. copies the files to public/data/sims/<sim>/<date of generation>/ and adds the generation to public/data/sims/generations.json.
     Large data (registry "store": "release", 23 November 2026): the files matching the entry's "release_files" patterns are not
     put in the repository but attached to the GitHub release sims-<sim>-<date> (gh, with the workflow's own token), their sizes
     checked against the release afterwards; only the other files (the index, the summary with every fingerprint) are committed,
     and the generation records the release and its files. The site's Worker serves those files under /rel/<tag>/<file>.
A registry entry may also ask for the GPU ("gpu": true) and a longer wait ("timeout_s").
The workflow then puts the data on main (tools/sims/land.py); Cloudflare Workers Builds publishes the site.

Authentication: the official Kaggle tool reads the environment variable KAGGLE_API_TOKEN (a repository secret of the same name).
Kaggle's `kernels push` exits with status 0 even when Kaggle refuses the push, so its printed answer is read and checked.

Usage: python3 tools/sims/pipeline.py <sim> <commit> [--kaggle <command>] [--timeout <s>] [--gh <command>]
Exit status 0 only when every check passed; anything else stops the workflow before a commit."""
import argparse, datetime, fnmatch, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OWNER, SLUG, TITLE = "numakoudsie", "phyein-usul-simulations", "Phyein Usul simulations"
REF = f"{OWNER}/{SLUG}"

def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)

def kaggle(cmd, args):
    r = subprocess.run(cmd + args, capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    log("$ kaggle " + " ".join(args)); log(out.strip()[-1500:])
    return r.returncode, out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("sim"); ap.add_argument("commit")
    ap.add_argument("--kaggle", default="kaggle"); ap.add_argument("--timeout", type=int, default=None); ap.add_argument("--gh", default="gh")
    a = ap.parse_args(); K = a.kaggle.split()
    reg = json.load(open(os.path.join(ROOT, "tools/sims/registry.json")))["sims"]
    if a.sim not in reg or not os.path.exists(os.path.join(ROOT, reg[a.sim]["model"])):
        sys.exit(f"{a.sim} is not a simulation in tools/sims/registry.json (or its model file is missing)")
    sc = reg[a.sim]; gpu = bool(sc.get("gpu")); timeout = a.timeout or int(sc.get("timeout_s", 1800))
    big = lambda f: sc.get("store") == "release" and any(fnmatch.fnmatch(f, p) for p in sc.get("release_files", []))
    if not re.fullmatch(r"[0-9a-f]{40}", a.commit): sys.exit("commit must be a full 40-character hash")
    # 1. the notebook folder
    nb = tempfile.mkdtemp(prefix="nb-")
    src = open(os.path.join(ROOT, "tools/sims/kaggle_sims.py")).read()
    src = re.sub(r'^JOB = "[^"]*"', f'JOB = "{a.sim}"', src, count=1, flags=re.M)
    src = src.replace("__COMMIT__", a.commit)
    assert f'JOB = "{a.sim}"' in src and a.commit in src
    open(os.path.join(nb, "kaggle_sims.py"), "w").write(src)
    json.dump(dict(id=REF, title=TITLE, code_file="kaggle_sims.py", language="python", kernel_type="script", is_private=True,
                   enable_gpu=gpu, enable_tpu=False, enable_internet=True, dataset_sources=[], competition_sources=[],
                   kernel_sources=[], model_sources=[]), open(os.path.join(nb, "kernel-metadata.json"), "w"), indent=1)
    # 2. push
    rc, out = kaggle(K, ["kernels", "push", "-p", nb])
    m = re.search(r"version\s+(\d+)\s+successfully pushed", out, re.I)
    if rc or not m: sys.exit("Kaggle did not accept the push (its answer is above)")
    version = int(m.group(1)); log("pushed version", version)
    # 3. wait
    t0 = time.time(); state = ""
    while time.time() - t0 < timeout:
        time.sleep(float(os.environ.get("POLL_S", 20)))
        rc, out = kaggle(K, ["kernels", "status", REF])
        mm = re.search(r'status\s+"?([A-Za-z_.]+)"?', out)
        state = (mm.group(1) if mm else out).lower()
        if "complete" in state: break
        if any(w in state for w in ("error", "cancel")): sys.exit(f"the Kaggle run ended in state {state}")
    else:
        sys.exit(f"no result within {timeout} s (last state: {state})")
    log("run complete after", round(time.time() - t0), "s")
    # 4. download and check
    dl = tempfile.mkdtemp(prefix="out-")
    rc, out = kaggle(K, ["kernels", "output", REF, "-p", dl])
    if rc: sys.exit("download failed")
    idx = [os.path.join(d, f) for d, _, fs in os.walk(dl) for f in fs if f == f"index-{a.sim}.json"]
    if len(idx) != 1: sys.exit(f"expected one index-{a.sim}.json in the output, found {len(idx)}")
    index = json.load(open(idx[0])); here = os.path.dirname(idx[0])
    if index.get("job") != a.sim or index["source"]["commit"] != a.commit: sys.exit("the output index names another simulation or commit")
    for f, meta in index["files"].items():
        b = open(os.path.join(here, f), "rb").read()
        if len(b) != meta["bytes"] or hashlib.sha256(b).hexdigest() != meta["sha256"]: sys.exit(f"{f}: size or SHA-256 differs from the index")
    log("all", len(index["files"]), "files match their SHA-256")
    day = index["date"]; tag = None
    large = {f: m for f, m in index["files"].items() if big(f)}
    if large:   # 5a. large data into the GitHub release sims-<sim>-<date>; a rerun on the same day replaces it
        tag = f"sims-{a.sim}-{day}"; G = a.gh.split()
        subprocess.run(G + ["release", "delete", tag, "--yes", "--cleanup-tag"], capture_output=True)
        r = subprocess.run(G + ["release", "create", tag, "--title", f"Simulation data: {a.sim}, {day}",
                                "--notes", f"Computed on Kaggle ({REF}, version {version}) from commit {a.commit}. Fingerprints: public/data/sims/{a.sim}/{day}/index-{a.sim}.json. Served by the site under /rel/{tag}/."]
                           + [os.path.join(here, f) for f in sorted(large)], capture_output=True, text=True)
        log(r.stdout[-1500:], r.stderr[-1500:])
        if r.returncode: sys.exit("the GitHub release could not be made (its answer is above)")
        r = subprocess.run(G + ["release", "view", tag, "--json", "assets"], capture_output=True, text=True)
        got = {x["name"]: x["size"] for x in json.loads(r.stdout or "{}").get("assets", [])}
        for f, m in large.items():
            if got.get(f) != m["bytes"]: sys.exit(f"{f}: the release holds {got.get(f)} bytes, the index says {m['bytes']}")
        log("release", tag, "holds", len(large), "files,", sum(m["bytes"] for m in large.values()), "bytes, sizes match")
    # 5. into the site
    dest = os.path.join(ROOT, "public/data/sims", a.sim, day); os.makedirs(dest, exist_ok=True)
    for f in [f for f in index["files"] if f not in large] + [f"index-{a.sim}.json"]: shutil.copy2(os.path.join(here, f), os.path.join(dest, f))
    gp = os.path.join(ROOT, "public/data/sims/generations.json")
    g = json.load(open(gp)) if os.path.exists(gp) else dict(about="Data of the site's simulations, computed once on Kaggle by the notebook "
        f"{REF} and carried here by .github/workflows/sims-kaggle.yml. One entry per simulation and date; a page plays the newest entry of its simulation.", generations=[])
    g["generations"] = [q for q in g["generations"] if not (q["sim"] == a.sim and q["date"] == day)]   # one entry per simulation and day: a rerun the same day replaces it
    g["generations"].append(dict(sim=a.sim, date=day, notebook=REF, version=version, commit=a.commit,
                                 index=f"{a.sim}/{day}/index-{a.sim}.json", files={f: v for f, v in index["files"].items() if f not in large},
                                 **(dict(release=tag, release_files=large, gpu=gpu) if large else {}),
                                 wall_s=round(index.get("wall_s", 0), 1), collected=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")))
    json.dump(g, open(gp, "w"), indent=1, ensure_ascii=False); open(gp, "a").write("\n")
    log(f"stored under public/data/sims/{a.sim}/{day}/, generations.json updated")
    if os.environ.get("GITHUB_OUTPUT"):
        open(os.environ["GITHUB_OUTPUT"], "a").write(f"version={version}\nday={day}\n")

if __name__ == "__main__":
    main()
