"""Every data set also stays on Kaggle: file one run's whole output as a version of the simulation's private Kaggle dataset.

Why: the site reads its data from the repository, a GitHub release or (later) R2, but a complete copy of every run stays on Kaggle,
where it was made, whatever its size (the user's rule; docs/kaggle-pipeline.md, "one dataset per figure"). Kaggle allows 200 GB per
dataset, 200 GB of private datasets in all and 50 files at the top level (https://www.kaggle.com/docs/datasets).

What it does, for one simulation and one version of the notebook numakoudsie/phyein-usul-simulations:
  1. takes that version's output (already downloaded by pipeline.py, or downloads it: `kaggle kernels output <notebook>/<version>`);
  2. checks every file's size and SHA-256 against the run's index-<sim>.json; any difference stops it;
  3. lays the files out as phyein-usul-simulations/v<version>/output/, with the run's log and a manifest.json (size and SHA-256 of
     every file, the code's commit) in phyein-usul-simulations/v<version>/, as docs/kaggle-pipeline.md prescribes;
  4. creates the figure's private dataset (registry "dataset", for example numakoudsie/fig2-double-pendulum; without one,
     numakoudsie/phyein-usul-<sim>), or adds a new version to it; a dataset
     version holds only what was uploaded with it, so the runs already in the dataset are downloaded and uploaded again beside the
     new one: the newest dataset version always holds every run;
  5. waits until Kaggle reports the dataset ready, and writes dataset, dataset_path and dataset_note into the run's entry in
     public/data/sims/generations.json (the workflow then saves it with land.py).
Usage: python3 tools/sims/dataset.py <sim> <notebook version> [--from <folder holding the output>] [--kaggle <command>]
       python3 tools/sims/dataset.py "<sim> ..." card   (only rewrites the datasets' subtitle and description from the records)"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
NOTEBOOK = "numakoudsie/phyein-usul-simulations"
GEN = os.path.join(ROOT, "public/data/sims/generations.json")

def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)

def kaggle(K, args, check=True):
    r = subprocess.run(K + args, capture_output=True, text=True); out = (r.stdout or "") + (r.stderr or "")
    # Kaggle's answer is on stdout, its progress bars on stderr: log the answer whole and only the last bar
    log("$ kaggle " + " ".join(args)); log((r.stdout or "").strip()[-1200:]); log((r.stderr or "").strip()[-300:])
    if check and r.returncode: sys.exit(f"kaggle {args[0]} {args[1]} failed")
    return out

def size(b):
    return f"{b / 1e6:,.1f} MB" if b >= 1e6 else f"{b / 1e3:,.1f} kB"

def card(reg, sim, folders):
    """The dataset's subtitle and description, as Kaggle shows them (the user's rule of 24 November 2026: no internal names,
    no empty description). folders: {"phyein-usul-simulations/v<N>": manifest dict}."""
    fig = reg.get("figure") or "Phyein Usul"
    subtitle = reg.get("dataset_subtitle") or f"{fig}: every Kaggle run behind the page on phyeinusul.com"
    page = reg.get("page_url") or "https://phyeinusul.com"
    rows = []; total = 0; nfiles = 0
    for f, m in sorted(folders.items(), key=lambda x: int(x[0].rsplit("v", 1)[1])):
        n = len(m.get("files", {})); b = sum(x["bytes"] for x in m.get("files", {}).values()); total += b; nfiles += n
        c = m.get("commit", "")
        rows.append(f"| `{f}/` | {m.get('sim', '')} | {m.get('date', '')} | {n} | {size(b)} | "
                    f"[{c[:7]}](https://github.com/Numa1997/SiteTest/tree/{c}/tools/sims) |")
    desc = "\n".join([
        f"# {reg.get('dataset_title') or fig}", "",
        f"{fig} on Phyein Usul ({page}). {reg.get('dataset_about', '')}".strip(), "",
        "Every run that made this data was computed on Kaggle by the notebook `numakoudsie/phyein-usul-simulations`. Each run is",
        "kept here byte for byte, in the folder of the notebook version that made it, so nothing the website plays exists only on the",
        "website.", "",
        f"**In this version:** {len(folders)} run{'s' if len(folders) != 1 else ''}, {nfiles} files, {size(total)}.", "",
        "| folder | model | date | files | size | code |", "|---|---|---|---|---|---|", *rows, "",
        "**Layout.** `<notebook>/v<version>/output/` holds the files as Kaggle wrote them; beside it `manifest.json` lists every",
        "file's size and SHA-256 and the commit of the code, and the `.log` file is the run's log. The site checks every file it",
        "plays against the same SHA-256.", "",
        "Code and documentation: https://github.com/Numa1997/SiteTest (tools/sims/, docs/kaggle-sims.md). Licence: CC BY 4.0."])
    return subtitle[:80], desc

def file_dataset(sim, version, src, K=("kaggle",)):
    K = list(K)
    idx = [os.path.join(d, f) for d, _, fs in os.walk(src) for f in fs if f == f"index-{sim}.json"]
    if len(idx) != 1: sys.exit(f"expected one index-{sim}.json under {src}, found {len(idx)}")
    index = json.load(open(idx[0])); here = os.path.dirname(idx[0])
    # the figure's own dataset (docs/kaggle-pipeline.md: one private dataset per figure, numakoudsie/fig<N>-<topic>), named in the
    # registry entry as "dataset" and "dataset_title"; a simulation without a figure gets numakoudsie/phyein-usul-<sim>
    reg = json.load(open(os.path.join(ROOT, "tools/sims/registry.json")))["sims"].get(sim, {})
    ref = reg.get("dataset") or "numakoudsie/phyein-usul-" + re.sub(r"[^a-z0-9]+", "-", sim.lower()).strip("-")
    title = reg.get("dataset_title") or f"Phyein Usul simulation data: {sim}"
    # Layout of docs/kaggle-pipeline.md: <notebook>/v<version>/output/ plus manifest.json. The Kaggle tool packs each top-level folder
    # of the upload into one archive of that folder's contents and Kaggle unpacks it at the dataset's root, so the tree is wrapped
    # in one more folder ("upload") to arrive as phyein-usul-simulations/v<version>/... (seen 23 November 2026: an unwrapped folder
    # arrived flat at the root).
    stage = tempfile.mkdtemp(prefix="ds-"); wrap = os.path.join(stage, "upload")
    folder = f"{NOTEBOOK.split('/')[1]}/v{version}"; dst = os.path.join(wrap, folder, "output"); os.makedirs(dst)
    def put(p, q):
        os.makedirs(os.path.dirname(q), exist_ok=True)
        os.link(p, q) if os.stat(p).st_dev == os.stat(stage).st_dev else shutil.copy2(p, q)
    manifest = {}
    for f, meta in sorted(index["files"].items()):
        p = os.path.join(here, f); h = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 24), b""): h.update(chunk)
        if os.path.getsize(p) != meta["bytes"] or h.hexdigest() != meta["sha256"]: sys.exit(f"{f}: size or SHA-256 differs from the index")
        put(p, os.path.join(dst, f)); manifest[f] = meta
    shutil.copy2(idx[0], os.path.join(dst, f"index-{sim}.json"))
    for f in os.listdir(src):   # the run's log, as Kaggle hands it out with the output
        if f.endswith(".log"): shutil.copy2(os.path.join(src, f), os.path.join(wrap, folder, f))
    folders = {folder: dict(sim=sim, date=index.get("date"), commit=index["source"]["commit"], files=manifest)}
    json.dump(dict(notebook=NOTEBOOK, version=version, sim=sim, date=index.get("date"), commit=index["source"]["commit"],
                   code=f"https://github.com/Numa1997/SiteTest/tree/{index['source']['commit']}/tools/sims", files=manifest),
              open(os.path.join(wrap, folder, "manifest.json"), "w"), indent=1)
    total = sum(m["bytes"] for m in manifest.values())
    log(f"{len(manifest)} files, {total} bytes checked against the index; staged as {folder}/output/")
    def ver():   # the dataset's newest version number, or None if it does not exist
        o = kaggle(K, ["datasets", "status", ref, "--format", "json"], check=False)
        m = re.search(r'"current_version_number"\s*:\s*(\d+)', o); return int(m.group(1)) if m else None
    before = ver(); exists = before is not None
    if exists:
        # A Kaggle dataset version holds only what is uploaded with it. The rule is that the dataset holds every run of the figure,
        # so the runs already in it are downloaded and uploaded again beside the new one. Files outside <notebook>/ (the flat layout
        # of the first filing, 23 November 2026) are left out; they stay in the older dataset versions.
        old = tempfile.mkdtemp(prefix="old-"); kaggle(K, ["datasets", "download", ref, "-p", old, "--unzip"])
        base = os.path.join(old, NOTEBOOK.split("/")[1]); kept = 0
        if os.path.isdir(base):
            for d, _, fs in os.walk(base):
                for f in fs:
                    rel = os.path.relpath(os.path.join(d, f), old)
                    if rel.startswith(folder + "/"): continue   # the same version filed again: the new copy wins
                    put(os.path.join(d, f), os.path.join(wrap, rel)); kept += 1
                    if f == "manifest.json": folders[os.path.dirname(rel)] = json.load(open(os.path.join(d, f)))
        log(f"{kept} files of earlier runs kept beside the new one")
        write_meta(stage, reg, sim, ref, title, folders)
        out = kaggle(K, ["datasets", "version", "-p", stage, "-r", "tar", "-m", f"{NOTEBOOK} version {version}, code {index['source']['commit'][:7]}"])
        if "being created" not in out: sys.exit("Kaggle did not accept the dataset version (its answer is above)")
    else:
        write_meta(stage, reg, sim, ref, title, folders)
        out = kaggle(K, ["datasets", "create", "-p", stage, "-r", "tar"])
        if "being created" not in out: sys.exit("Kaggle did not accept the new dataset (its answer is above)")
    # Wait for THIS version. "ready" alone is not enough: while Kaggle unpacks a new version, the status still reports the previous
    # version as ready (23 November 2026: a 7 GB version was reported ready after 30 s and was not yet there). So wait until the
    # version number has risen and that version is ready.
    t0 = time.time(); state = ""
    while time.time() - t0 < 3 * 3600:   # Kaggle unpacks and indexes the upload; large data takes many minutes
        time.sleep(float(os.environ.get("POLL_S", 60)))
        state = kaggle(K, ["datasets", "status", ref], check=False).strip().lower()
        if "error" in state or "failed" in state: sys.exit(f"Kaggle reports the dataset as: {state}")
        v = ver()
        if "ready" in state and v is not None and (before is None or v > before): break
        log(f"newest version {v} (before the upload: {before}), state {state}: waiting")
    else:
        sys.exit(f"the new dataset version was not there within 3 hours (last state: {state})")
    # "datasets version" does not change the subtitle and description; set them from the same file
    update_card(K, ref, stage)
    shutil.rmtree(stage)
    log(f"dataset {ref} version {v} ready with {folder}/ ({total} bytes) after {round(time.time() - t0)} s")
    return ref, folder, total

def update_card(K, ref, stage):
    """Set the subtitle and description from stage/dataset-metadata.json on an existing dataset. The update refuses the licence
    name the upload takes ("CC-BY-4.0": "You've specified an invalid license", 24 November 2026), so the dataset's own metadata is
    downloaded first and its licence entry kept as Kaggle wrote it."""
    want = json.load(open(os.path.join(stage, "dataset-metadata.json")))
    cur = tempfile.mkdtemp(prefix="meta-"); kaggle(K, ["datasets", "metadata", ref, "-p", cur])
    have = json.load(open(os.path.join(cur, "dataset-metadata.json")))
    info = have.get("info", have)   # the download is {"info": {...}}, and the update reads "info" when it is there
    # isPrivate must be set: the update treats a missing isPrivate as False and would make the dataset public
    info.update(title=want["title"], subtitle=want["subtitle"], description=want["description"], isPrivate=True)
    if not info.get("licenses"): sys.exit(f"{ref}: the downloaded metadata has no licence entry; not updating")
    json.dump(have, open(os.path.join(cur, "dataset-metadata.json"), "w"), indent=1, ensure_ascii=False)
    out = kaggle(K, ["datasets", "metadata", ref, "--update", "-p", cur])
    if "invalid" in out.lower() or "rror" in out: sys.exit("Kaggle did not take the new card (its answer is above)")

def write_meta(stage, reg, sim, ref, title, folders):
    sub, desc = card(reg, sim, folders)
    json.dump(dict(title=title[:50], id=ref, licenses=[dict(name="CC-BY-4.0")], subtitle=sub, description=desc),
              open(os.path.join(stage, "dataset-metadata.json"), "w"), indent=1, ensure_ascii=False)

def record(sim, version, ref, folder, total):
    g = json.load(open(GEN)); hit = [e for e in g["generations"] if e["sim"] == sim and e.get("version") == version]
    if not hit: sys.exit(f"generations.json has no {sim} from notebook version {version}")
    for e in hit:
        e["dataset"] = ref; e["dataset_path"] = folder + "/"
        e["dataset_note"] = f"the whole Kaggle output of {NOTEBOOK} version {version}, {total} bytes, filed as one version of this dataset"
    json.dump(g, open(GEN, "w"), indent=1, ensure_ascii=False); open(GEN, "a").write("\n")
    return hit[-1]["commit"]

def set_card(sim, K):
    """Rewrite the subtitle and description of the simulation's dataset from the records (no upload). The Kaggle connector cannot
    do it (it refuses every licence it is given), so it runs here: Run workflow, mode dataset, version "card"."""
    reg = json.load(open(os.path.join(ROOT, "tools/sims/registry.json")))["sims"][sim]; ref = reg["dataset"]
    folders = {}
    for e in json.load(open(GEN))["generations"]:
        if e.get("dataset") == ref:
            idx = json.load(open(os.path.join(ROOT, "public/data/sims", e["index"])))
            folders[(e.get("dataset_path") or f"phyein-usul-simulations/v{e['version']}/").rstrip("/")] = dict(
                sim=e["sim"], date=e["date"], commit=e["commit"], files=idx["files"])
    if not folders: sys.exit(f"no generation of {sim} is filed in {ref}")
    stage = tempfile.mkdtemp(prefix="card-"); write_meta(stage, reg, sim, ref, reg.get("dataset_title") or ref, folders)
    update_card(K, ref, stage)
    log(f"{ref}: subtitle and description set ({len(folders)} runs)")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("sim"); ap.add_argument("version")
    ap.add_argument("--from", dest="src", default=None); ap.add_argument("--kaggle", default="kaggle")
    a = ap.parse_args(); K = a.kaggle.split(); src = a.src
    if a.version == "card":
        for s in a.sim.split(): set_card(s, K)
        return
    a.version = int(a.version)
    if not src:   # backfill: fetch that version's output again from Kaggle (Kaggle keeps every version's output)
        src = tempfile.mkdtemp(prefix="out-"); kaggle(K, ["kernels", "output", f"{NOTEBOOK}/{a.version}", "-p", src])
    ref, folder, total = file_dataset(a.sim, a.version, src, K)
    commit = record(a.sim, a.version, ref, folder, total)
    if os.environ.get("GITHUB_OUTPUT"): open(os.environ["GITHUB_OUTPUT"], "a").write(f"commit={commit}\n")

if __name__ == "__main__":
    main()
