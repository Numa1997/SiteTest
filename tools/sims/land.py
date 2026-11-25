"""Step 7 of the simulations pipeline: put the new data (and the run's status file) on main without clashing with what was merged
meanwhile.

Why: a Kaggle run takes minutes to hours, and other work is merged into main while it runs. On 23 November 2026 the data of the
double pendulum was computed and checked, but the save failed at "git pull --rebase": both the data commit and a merge from another
session had rewritten docs/files.md, a generated list, and git stopped at the clash (run 45254099718). Nothing was saved.

What it does instead, for the simulations named on the command line and the code commit they were computed from:
  1. keeps aside what pipeline.py wrote: each new generation's folder (public/data/sims/<sim>/<run>/ for an "r2" run,
     public/data/sims/<sim>/<date>/ for a "repo" or "release" run) and its entry in generations.json;
  2. checks out the newest main in a separate git worktree (git worktree add once, then reset to the newest main for each push), so
     neither what was merged meanwhile nor the run's own working tree is touched;
  3. puts the kept folders in, adds the kept entries to main's own generations.json (an entry for the same simulation and run, or
     for a "repo" entry the same simulation and date, is replaced; every other entry stays), and generates docs/files.md again with
     tools/inventory.py instead of merging it;
  4. commits as the workflow's identity, then sets the run's status file public/data/sims/status/<sim>.json to "saved" with the
     data commit, and pushes both; if main moved again in between, starts over from 2 (five tries).
push_status() does steps 2 to 4 for the status file alone; pipeline.py and verify_live.py call it while a run goes on.
Usage: python3 tools/sims/land.py "<sim> [<sim> ...]" <commit>"""
import datetime, json, os, shutil, subprocess, sys, tempfile, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GEN_REL = "public/data/sims/generations.json"
GEN = os.path.join(ROOT, GEN_REL)
BOT = ["-c", "user.name=github-actions[bot]", "-c", "user.email=41898282+github-actions[bot]@users.noreply.github.com"]

def git(*a, cwd=ROOT, check=True):
    r = subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True)
    if check and r.returncode: sys.exit(f"git {' '.join(a)} failed: {r.stderr.strip()[-800:]}")
    return r

def folder(e):
    """The repository folder of a generation: its run address for an "r2" run, its date otherwise."""
    return os.path.join("public/data/sims", e["sim"], e.get("run") or e["date"])

def same(q, e):
    if q["sim"] != e["sim"]: return False
    return q.get("run") == e["run"] if e.get("run") else (not q.get("run") and q["date"] == e["date"])

def write_json(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(d, open(p, "w"), indent=1, ensure_ascii=False); open(p, "a").write("\n")

def worktree():
    """A checkout of the newest main beside the run's own checkout (git worktree), made once per runner and reset for each push:
    a fresh checkout of this repository takes most of a minute, a reset only rewrites what changed."""
    import hashlib
    wt = os.path.join(tempfile.gettempdir(), "sims-land-" + hashlib.sha1(ROOT.encode()).hexdigest()[:10])
    git("fetch", "-q", "origin", "main")
    if os.path.isdir(wt) and git("rev-parse", "--git-dir", cwd=wt, check=False).returncode == 0:
        git("reset", "-q", "--hard", "origin/main", cwd=wt); git("clean", "-q", "-fd", cwd=wt)
    else:
        shutil.rmtree(wt, ignore_errors=True); git("worktree", "prune")
        git("worktree", "add", "-q", "--detach", wt, "origin/main")
    return wt

def push_to_main(steps, tries=5):
    """steps: a list of (message, writer); each writer(worktree) changes files there and becomes one commit (a writer may also take
    the commit made just before it, as writer(worktree, previous sha)). All commits go to main in one push; on a moved main, start
    over on the newest main. Returns the last commit, or None when nothing changed."""
    for attempt in range(1, tries + 1):
        wt = worktree()
        prev = None; made = 0
        for msg, writer in steps:
            writer(wt, prev) if writer.__code__.co_argcount == 2 else writer(wt)
            r = subprocess.run([sys.executable, "tools/inventory.py"], cwd=wt, capture_output=True, text=True)
            if r.returncode: sys.exit("tools/inventory.py failed: " + (r.stdout + r.stderr)[-800:])
            git("add", "-A", "public/data/sims", "docs/files.md", cwd=wt)
            if git("diff", "--cached", "--quiet", cwd=wt, check=False).returncode == 0: continue
            git(*BOT, "commit", "-q", "-m", msg, cwd=wt); prev = git("rev-parse", "HEAD", cwd=wt).stdout.strip(); made += 1
        if not made: print("nothing new"); return None
        if git("push", "-q", "origin", "HEAD:main", cwd=wt, check=False).returncode == 0:
            print(f"on main (try {attempt}): {prev}"); return prev
        print(f"main moved during try {attempt}; starting again from the newest main")
        time.sleep(float(os.environ.get("LAND_WAIT", 10)))
    sys.exit("could not push to main after five tries")

def push_status(sim, d):
    """Put the status file of one simulation on main (state changes during a run)."""
    rel = f"public/data/sims/status/{sim}.json"
    return push_to_main([(f"Simulation status: {sim} {d['state']}", lambda wt: write_json(os.path.join(wt, rel), d))])

def main():
    sims, sha = sys.argv[1].split(), sys.argv[2]
    mine = [e for e in json.load(open(GEN))["generations"] if e["sim"] in sims and e["commit"] == sha]
    mine = [e for e in mine if os.path.isdir(os.path.join(ROOT, folder(e)))]
    if not mine: print("nothing new to land"); return
    keep = tempfile.mkdtemp(prefix="land-")
    for e in mine: shutil.copytree(os.path.join(ROOT, folder(e)), os.path.join(keep, folder(e)))
    status = {}
    for s in sims:
        p = os.path.join(ROOT, "public/data/sims/status", s + ".json")
        if os.path.exists(p): status[s] = json.load(open(p))

    def data(wt):
        g = json.load(open(os.path.join(wt, GEN_REL)))
        for e in mine:
            dest = os.path.join(wt, folder(e))
            if os.path.exists(dest): shutil.rmtree(dest)
            shutil.copytree(os.path.join(keep, folder(e)), dest)
            g["generations"] = [q for q in g["generations"] if not same(q, e)] + [e]
        write_json(os.path.join(wt, GEN_REL), g)

    def saved(wt, data_commit):
        for s, d in status.items():
            d.update(state="saved", data_commit=data_commit, failure=None,
                     ended_at=d.get("ended_at") or datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))
            write_json(os.path.join(wt, "public/data/sims/status", s + ".json"), d)

    msg = f"Simulation data from Kaggle: {' '.join(sims)} (notebook numakoudsie/phyein-usul-simulations, code {sha[:7]})"
    steps = [(msg, data)] + ([(f"Simulation status: {' '.join(status)} saved", saved)] if status else [])
    top = push_to_main(steps)
    print(f"landed on main: {top}" if top else "nothing new")

if __name__ == "__main__":
    main()
