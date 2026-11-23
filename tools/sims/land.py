"""Step 7 of the simulations pipeline: put the new data on main without clashing with what was merged meanwhile.

Why: a Kaggle run takes minutes to hours, and other work is merged into main while it runs. On 23 November 2026 the data of the
double pendulum was computed and checked, but the save failed at "git pull --rebase": both the data commit and a merge from another
session had rewritten docs/files.md, a generated list, and git stopped at the clash (run 45254099718). Nothing was saved.

What it does instead, for the simulations named on the command line and the code commit they were computed from:
  1. keeps aside what pipeline.py wrote: each new generation's folder public/data/sims/<sim>/<date>/ and its entry in generations.json;
  2. takes the newest main as it is (git fetch, git reset --hard origin/main), so nothing merged meanwhile is touched;
  3. puts the kept folders back, adds the kept entries to main's own generations.json (an entry for the same simulation and date is
     replaced, every other entry stays), and generates docs/files.md again with tools/inventory.py instead of merging it;
  4. commits as the workflow's identity and pushes; if main moved again in between, starts over from 2 (five tries).
Usage: python3 tools/sims/land.py "<sim> [<sim> ...]" <commit>"""
import json, os, shutil, subprocess, sys, tempfile, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GEN = os.path.join(ROOT, "public/data/sims/generations.json")

def git(*a, check=True):
    r = subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode: sys.exit(f"git {' '.join(a)} failed: {r.stderr.strip()[-800:]}")
    return r

def main():
    sims, sha = sys.argv[1].split(), sys.argv[2]
    mine = [e for e in json.load(open(GEN))["generations"] if e["sim"] in sims and e["commit"] == sha]
    if not mine: print("nothing new to land"); return
    keep = tempfile.mkdtemp(prefix="land-")
    for e in mine: shutil.copytree(os.path.join(ROOT, "public/data/sims", e["sim"], e["date"]), os.path.join(keep, e["sim"], e["date"]))
    msg = f"Simulation data from Kaggle: {' '.join(sims)}(notebook numakoudsie/phyein-usul-simulations, code {sha[:7]})"
    for attempt in range(1, 6):
        git("fetch", "-q", "origin", "main"); git("reset", "-q", "--hard", "origin/main")
        g = json.load(open(GEN))
        for e in mine:
            dest = os.path.join(ROOT, "public/data/sims", e["sim"], e["date"])
            if os.path.exists(dest): shutil.rmtree(dest)
            shutil.copytree(os.path.join(keep, e["sim"], e["date"]), dest)
            g["generations"] = [q for q in g["generations"] if not (q["sim"] == e["sim"] and q["date"] == e["date"])] + [e]
        json.dump(g, open(GEN, "w"), indent=1, ensure_ascii=False); open(GEN, "a").write("\n")
        r = subprocess.run([sys.executable, "tools/inventory.py"], cwd=ROOT, capture_output=True, text=True)
        if r.returncode: sys.exit("tools/inventory.py failed: " + (r.stdout + r.stderr)[-800:])
        git("add", "public/data/sims", "docs/files.md")
        if git("diff", "--cached", "--quiet", check=False).returncode == 0: print("nothing new"); return
        git("commit", "-q", "-m", msg)
        if git("push", "origin", "HEAD:main", check=False).returncode == 0:
            print(f"landed on main (try {attempt}): {git('rev-parse', 'HEAD').stdout.strip()}"); return
        print(f"main moved during try {attempt}; starting again from the newest main"); time.sleep(10)
    sys.exit("could not land the data after five tries")

if __name__ == "__main__":
    main()
