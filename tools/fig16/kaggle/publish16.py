"""Fig. 16 on Kaggle's CPU (no GPU quota): turn a finished GPU run into the page's files, so that nothing runs outside Kaggle
(owner, 15 November 2026). Steps:
  1. the repository at commit COMMIT (codeload tarball) into /tmp/repo;
  2. the GPU run's output, attached to this notebook as a data source (the notebook fig-16-guinness-cart-with-control), found under
     /kaggle/input by its summary.json;
  3. tools/fig16/kaggle/pack16.py on every ride listed in RIDES, into public/data/fig16/<DATE>/ (format conversion only);
  4. notes/fig16/note_numbers.py (the note's measured numbers) and tools/fig16/build_page.py, then build_page.py --check;
  5. /kaggle/working/publish16.tar.gz with the changed files, and publish16.log.
Environment: COMMIT, RUN_VERSION (the GPU notebook's version), RIDES (comma separated), DATE."""
import glob, io, json, os, subprocess, sys, tarfile, time, urllib.request

COMMIT = os.environ["COMMIT"]; VERSION = os.environ["RUN_VERSION"]; DATE = os.environ.get("DATE", "2026-11-15")
RIDES = os.environ["RIDES"].split(","); WORK = "/kaggle/working"; REPO = "/tmp/repo"
LOG = open(os.path.join(WORK, "publish16.log"), "w")


def log(m):
    print(m, flush=True); LOG.write(m + "\n"); LOG.flush()


def run(args):
    r = subprocess.run([sys.executable] + args, cwd=REPO, capture_output=True, text=True)
    log(f"$ {' '.join(args)}  (exit {r.returncode})\n{r.stdout[-3000:]}{r.stderr[-3000:]}")
    if r.returncode: raise SystemExit(f"failed: {args}")


data = urllib.request.urlopen(f"https://codeload.github.com/Numa1997/SiteTest/tar.gz/{COMMIT}").read()
with tarfile.open(fileobj=io.BytesIO(data)) as t:
    top = t.getnames()[0].split("/")[0]; t.extractall("/tmp")
os.rename(os.path.join("/tmp", top), REPO); log(f"repository at {COMMIT}")
summ = [p for p in glob.glob("/kaggle/input/**/summary.json", recursive=True)]
log("summaries found: " + ", ".join(summ))
summ = [p for p in summ if all(os.path.exists(os.path.join(os.path.dirname(p), r + ".npz")) for r in RIDES)][0]
src = os.path.dirname(summ); log(f"GPU output: {src}")
t0 = time.time()
for r in RIDES:
    run(["tools/fig16/kaggle/pack16.py", os.path.join(src, r + ".npz"), summ, r, DATE, VERSION, COMMIT])
run(["notes/fig16/note_numbers.py"])
run(["tools/fig16/build_page.py"])
run(["tools/fig16/build_page.py", "--check"])
out = [f"public/data/fig16/{DATE}/{r}.json" for r in RIDES] + [f"public/data/fig16/{DATE}/index-16.json", "notes/fig16/note-numbers.json",
       "public/simulations/guinness-cart-control.html"]
with tarfile.open(os.path.join(WORK, "publish16.tar.gz"), "w:gz") as t:
    for f in out: t.add(os.path.join(REPO, f), arcname=f)
log(f"packed {len(out)} files in {time.time() - t0:.0f} s: " + ", ".join(out))
