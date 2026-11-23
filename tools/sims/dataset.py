"""Every data set also stays on Kaggle: file one run's whole output as a version of the simulation's private Kaggle dataset.

Why: the site reads its data from the repository, a GitHub release or (later) R2, but a complete copy of every run stays on Kaggle,
where it was made, whatever its size (the user's rule; docs/kaggle-pipeline.md, "one dataset per figure"). Kaggle allows 200 GB per
dataset, 200 GB of private datasets in all and 50 files at the top level (https://www.kaggle.com/docs/datasets).

What it does, for one simulation and one version of the notebook numakoudsie/phyein-usul-simulations:
  1. takes that version's output (already downloaded by pipeline.py, or downloads it: `kaggle kernels output <notebook>/<version>`);
  2. checks every file's size and SHA-256 against the run's index-<sim>.json; any difference stops it;
  3. lays the files out as phyein-usul-simulations-v<version>/ with a manifest.json (size and SHA-256 of every file), so a dataset
     version always says which notebook version made it;
  4. creates the private dataset numakoudsie/phyein-usul-<sim> (hyphens for underscores), or adds a new version to it; a dataset
     version holds only what was uploaded with it, so each run is one dataset version and the older runs stay in the older versions;
  5. waits until Kaggle reports the dataset ready, and writes dataset, dataset_path and dataset_note into the run's entry in
     public/data/sims/generations.json (the workflow then saves it with land.py).
Usage: python3 tools/sims/dataset.py <sim> <notebook version> [--from <folder holding the output>] [--kaggle <command>]"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
NOTEBOOK = "numakoudsie/phyein-usul-simulations"
GEN = os.path.join(ROOT, "public/data/sims/generations.json")

def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)

def kaggle(K, args, check=True):
    r = subprocess.run(K + args, capture_output=True, text=True); out = (r.stdout or "") + (r.stderr or "")
    log("$ kaggle " + " ".join(args)); log(out.strip()[-1200:])
    if check and r.returncode: sys.exit(f"kaggle {args[0]} {args[1]} failed")
    return out

def file_dataset(sim, version, src, K=("kaggle",)):
    K = list(K)
    idx = [os.path.join(d, f) for d, _, fs in os.walk(src) for f in fs if f == f"index-{sim}.json"]
    if len(idx) != 1: sys.exit(f"expected one index-{sim}.json under {src}, found {len(idx)}")
    index = json.load(open(idx[0])); here = os.path.dirname(idx[0])
    folder = f"phyein-usul-simulations-v{version}"
    stage = tempfile.mkdtemp(prefix="ds-"); dst = os.path.join(stage, folder); os.makedirs(dst)
    manifest = {}
    for f, meta in sorted(index["files"].items()):
        p = os.path.join(here, f); h = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 24), b""): h.update(chunk)
        if os.path.getsize(p) != meta["bytes"] or h.hexdigest() != meta["sha256"]: sys.exit(f"{f}: size or SHA-256 differs from the index")
        os.link(p, os.path.join(dst, f)) if os.stat(p).st_dev == os.stat(stage).st_dev else shutil.copy2(p, os.path.join(dst, f))
        manifest[f] = meta
    shutil.copy2(idx[0], os.path.join(dst, f"index-{sim}.json"))
    json.dump(dict(notebook=NOTEBOOK, version=version, sim=sim, date=index.get("date"), commit=index["source"]["commit"], files=manifest),
              open(os.path.join(dst, "manifest.json"), "w"), indent=1)
    total = sum(m["bytes"] for m in manifest.values())
    log(f"{len(manifest)} files, {total} bytes checked against the index; staged as {folder}/")
    slug = "phyein-usul-" + re.sub(r"[^a-z0-9]+", "-", sim.lower()).strip("-"); ref = f"numakoudsie/{slug}"
    json.dump(dict(title=f"Phyein Usul simulation data: {sim}"[:50], id=ref, licenses=[dict(name="CC-BY-4.0")],
                   subtitle=f"Every run of the website's {sim} model, as computed on Kaggle"[:80]),
              open(os.path.join(stage, "dataset-metadata.json"), "w"), indent=1)
    exists = "403" not in (st := kaggle(K, ["datasets", "status", ref], check=False)) and "404" not in st and "not found" not in st.lower() and "error" not in st.lower()
    if exists:
        out = kaggle(K, ["datasets", "version", "-p", stage, "-r", "tar", "-m", f"{NOTEBOOK} version {version}, code {index['source']['commit'][:7]}"])
        if "being created" not in out: sys.exit("Kaggle did not accept the dataset version (its answer is above)")
    else:
        out = kaggle(K, ["datasets", "create", "-p", stage, "-r", "tar"])
        if "being created" not in out: sys.exit("Kaggle did not accept the new dataset (its answer is above)")
    t0 = time.time(); state = ""
    while time.time() - t0 < 3600:   # Kaggle unpacks and indexes the upload; large data takes minutes
        time.sleep(float(os.environ.get("POLL_S", 30)))
        state = kaggle(K, ["datasets", "status", ref], check=False).strip().lower()
        if "ready" in state: break
        if "error" in state or "failed" in state: sys.exit(f"Kaggle reports the dataset as: {state}")
    else:
        sys.exit(f"the dataset was not ready within an hour (last state: {state})")
    shutil.rmtree(stage)
    log(f"dataset {ref} ready with {folder}/ ({total} bytes) after {round(time.time() - t0)} s")
    return ref, folder, total

def record(sim, version, ref, folder, total):
    g = json.load(open(GEN)); hit = [e for e in g["generations"] if e["sim"] == sim and e.get("version") == version]
    if not hit: sys.exit(f"generations.json has no {sim} from notebook version {version}")
    for e in hit:
        e["dataset"] = ref; e["dataset_path"] = folder + "/"
        e["dataset_note"] = f"the whole Kaggle output of {NOTEBOOK} version {version}, {total} bytes, filed as one version of this dataset"
    json.dump(g, open(GEN, "w"), indent=1, ensure_ascii=False); open(GEN, "a").write("\n")
    return hit[-1]["commit"]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("sim"); ap.add_argument("version", type=int)
    ap.add_argument("--from", dest="src", default=None); ap.add_argument("--kaggle", default="kaggle")
    a = ap.parse_args(); K = a.kaggle.split(); src = a.src
    if not src:   # backfill: fetch that version's output again from Kaggle (Kaggle keeps every version's output)
        src = tempfile.mkdtemp(prefix="out-"); kaggle(K, ["kernels", "output", f"{NOTEBOOK}/{a.version}", "-p", src])
    ref, folder, total = file_dataset(a.sim, a.version, src, K)
    commit = record(a.sim, a.version, ref, folder, total)
    if os.environ.get("GITHUB_OUTPUT"): open(os.environ["GITHUB_OUTPUT"], "a").write(f"commit={commit}\n")

if __name__ == "__main__":
    main()
