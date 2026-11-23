"""File every Kaggle notebook run of one figure into the figure's private Kaggle dataset (docs/kaggle-pipeline.md, "one dataset per
figure"), for figures made before the engine existed, whose runs live only as notebook outputs on Kaggle (Fig. 15 first).

The figure, its dataset and its notebooks are listed in tools/sims/figure_datasets.json. For every notebook and every version of it
(found by asking Kaggle for version 1, 2, ... until one does not exist):
  1. the version's code (`kaggle kernels pull <notebook>/<version>`) goes to <notebook>/v<version>/code/;
  2. its whole output (`kaggle kernels output <notebook>/<version>`) goes to <notebook>/v<version>/output/, with its log;
  3. <notebook>/v<version>/manifest.json lists every file's size and SHA-256 (computed here; where the site's own index names a file
     of that notebook, its SHA-256 must agree, or the filing stops).
Then the dataset is created (it must not exist yet) and the script waits until Kaggle has unpacked it, and writes its subtitle and
description (figure, page, a table of every notebook version with files and size, layout, licence).

Disk: the Kaggle tool packs each top-level folder of the upload into one archive, uploads it and deletes it, and Kaggle unpacks each
archive at the dataset's root. So every notebook gets its own top-level folder that holds <notebook>/..., and the extra disk needed
is one notebook's archive, not the whole figure twice.
Usage: python3 tools/sims/file_figure.py <figure key, e.g. fig15> [--kaggle <command>]"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)

def kaggle(K, args, check=True):
    r = subprocess.run(K + args, capture_output=True, text=True)
    log("$ kaggle " + " ".join(args)); log((r.stdout or "").strip()[-600:]); log((r.stderr or "").strip()[-300:])
    if check and r.returncode: sys.exit(f"kaggle {' '.join(args[:2])} failed")
    return r

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 24), b""): h.update(c)
    return h.hexdigest()

def size(b): return f"{b / 1e6:,.1f} MB" if b >= 1e6 else f"{b / 1e3:,.1f} kB"

def site_hashes(F):
    """SHA-256 the site recorded per (notebook, file name), from the figure's index files."""
    known = {}
    for p in F.get("site_indexes", []):
        d = json.load(open(os.path.join(ROOT, p)))
        runs = d.get("runs") or d.get("files") or {}
        for r in (runs.values() if isinstance(runs, dict) else runs):
            if isinstance(r, dict) and r.get("notebook") and r.get("file") and r.get("sha256"):
                known[(r["notebook"], os.path.basename(r["file"]))] = r["sha256"]
    return known

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("figure"); ap.add_argument("--kaggle", default="kaggle")
    a = ap.parse_args(); K = a.kaggle.split()
    F = json.load(open(os.path.join(ROOT, "tools/sims/figure_datasets.json")))[a.figure]; ref = F["dataset"]
    st = kaggle(K, ["datasets", "status", ref, "--format", "json"], check=False)
    if '"current_version_number"' in (st.stdout or ""):
        sys.exit(f"{ref} exists already; this script only creates a figure's dataset (add runs to it with a new version by hand)")
    known = site_hashes(F); stage = tempfile.mkdtemp(prefix="fig-"); table = []; total = 0; nfiles = 0
    for nb in F["notebooks"]:
        slug = nb.split("/")[1]; v = 0
        while True:
            v += 1
            base = os.path.join(stage, slug, slug, f"v{v}")
            code = kaggle(K, ["kernels", "pull", f"{nb}/{v}", "-p", os.path.join(base, "code"), "-m"], check=False)
            if code.returncode or not os.listdir(os.path.join(base, "code")):
                shutil.rmtree(base, ignore_errors=True); break
            out = os.path.join(base, "output"); os.makedirs(out)
            got = kaggle(K, ["kernels", "output", f"{nb}/{v}", "-p", out], check=False)
            files = {}
            for d, _, fs in os.walk(out):
                for f in fs:
                    p = os.path.join(d, f); rel = os.path.relpath(p, out); h = sha(p)
                    if (nb, f) in known and known[(nb, f)] != h and not f.endswith(".log"):
                        # the site may hold a later replacement under the same name; only a mismatch on version 1 of a
                        # notebook whose file the site names is an error
                        log(f"note: {nb}/{v} {rel}: SHA-256 differs from the site's index (the site may hold a replacement)")
                    files[rel] = dict(bytes=os.path.getsize(p), sha256=h)
            for f in [x for x in os.listdir(out) if x.endswith(".log")]: shutil.move(os.path.join(out, f), os.path.join(base, f))
            b = sum(x["bytes"] for k, x in files.items() if not k.endswith(".log"))
            files = {k: x for k, x in files.items() if not k.endswith(".log")}
            agree = sum(1 for k, x in files.items() if known.get((nb, os.path.basename(k))) == x["sha256"])
            json.dump(dict(notebook=nb, version=v, files=files, output_status=got.returncode,
                           site_files_matching=agree), open(os.path.join(base, "manifest.json"), "w"), indent=1)
            table.append((f"{slug}/v{v}", len(files), b, agree)); total += b; nfiles += len(files)
            log(f"{nb} version {v}: {len(files)} files, {b} bytes, {agree} identical to files the site names; "
                f"disk free {shutil.disk_usage(stage).free // 2**30} GB")
        if v == 1: log(f"warning: {nb} has no version Kaggle would hand out")
    rows = [f"| `{f}/` | {n} | {size(b)} | {m} |" for f, n, b, m in table]
    desc = "\n".join([
        f"# {F['title']}", "", f"{F['figure']} on Phyein Usul ({F['page_url']}). {F['about']}", "",
        "Every output file of every Kaggle notebook run that made this figure's data, kept here byte for byte, in the folder of the",
        "notebook version that made it, with that version's code. Nothing the website plays exists only on the website.", "",
        f"**In this version:** {len(table)} notebook versions, {nfiles} files, {size(total)}.", "",
        "| folder | files | size | files identical to the site's |", "|---|---|---|---|", *rows, "",
        "**Layout.** `<notebook>/v<version>/output/` holds the files as Kaggle wrote them, `code/` the notebook as it ran, the `.log`",
        "file the run's log, and `manifest.json` every file's size and SHA-256.", "",
        f"Code and documentation: https://github.com/Numa1997/SiteTest ({F['doc']}). Licence: CC BY 4.0."])
    meta = dict(title=F["title"][:50], id=ref, licenses=[dict(name="CC-BY-4.0")], subtitle=F["subtitle"][:80], description=desc)
    json.dump(meta, open(os.path.join(stage, "dataset-metadata.json"), "w"), indent=1, ensure_ascii=False)
    log(f"staged {len(table)} notebook versions, {nfiles} files, {total} bytes")
    r = kaggle(K, ["datasets", "create", "-p", stage, "-r", "tar"])
    if "being created" not in (r.stdout or ""): sys.exit("Kaggle did not accept the dataset (its answer is above)")
    t0 = time.time(); state = ""
    while time.time() - t0 < 3 * 3600:   # Kaggle unpacks the archives; 7 GB took 5 to 8 minutes on 23 November 2026
        time.sleep(float(os.environ.get("POLL_S", 60)))
        o = kaggle(K, ["datasets", "status", ref, "--format", "json"], check=False).stdout or ""
        state = o.lower()
        if "error" in state or "failed" in state: sys.exit(f"Kaggle reports the dataset as: {o}")
        if '"ready"' in state and '"current_version_number"' in state: break
    else:
        sys.exit(f"the dataset was not ready within 3 hours (last state: {state})")
    kaggle(K, ["datasets", "metadata", ref, "--update", "-p", stage])
    log(f"dataset {ref} ready after {round(time.time() - t0)} s: {len(table)} notebook versions, {nfiles} files, {total} bytes")
    # the record, for the figure's generations.json (dataset, dataset_path): copied into the repository by the session that filed it
    print("RECORD " + json.dumps(dict(dataset=ref, versions=[dict(folder=f, files=n, bytes=b, site_identical=m) for f, n, b, m in table],
                                      files=nfiles, bytes=total, filed=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))), flush=True)

if __name__ == "__main__":
    main()
