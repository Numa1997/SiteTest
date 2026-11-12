"""Fig. 12: write one self-contained Kaggle notebook that runs one OpenFOAM case of the stout in the tulip.

    python3 tools/fig12/kaggle/make_notebook.py <case name> [--commit SHA] [--np N] [--set key=value ...] [--out FILE]

The case is looked up by name in notes/fig12/of-request.json, then in notes/fig12/of-runs/<name>/case.json (the
record of a case already run on GitHub), with the same fields the GitHub workflow takes:
    {"name", "level", "forcing", "fill", "end", "write", "wall", "sigma", "nu", "rho", "maxco", "maxdt", "ride"}
--set overrides one field (for a short test: --set end=0.05). --commit is the full commit of this repository the
notebook clones (default: HEAD, which must already be pushed). The notebook goes to tools/fig12/kaggle/notebooks/.

The notebook does on Kaggle what .github/workflows/fig12-openfoam.yml does on a GitHub runner, and stores the same
files in the same layout as notes/fig12/of-runs/<name>/, under /kaggle/working/<name>/:
  1 environment   cores, memory, OS, disk
  2 install       OpenFOAM 13 from dl.openfoam.org (the workflow's commands; Kaggle is Ubuntu 24.04 "noble"), Node if
                  missing (the mesh reads public/scripts/guinness-glass.js through node), and the user "foam":
                  OpenFOAM refuses to compile the case's coded monitor as root
  3 code          a sparse clone of this repository at the pinned commit (tools/fig12, public/scripts only)
  4 case          tools/fig12/of/make_case.py with the case's parameters; params.json, case.json
  5 run           tools/fig12/of/run.sh on all cores; progress.log every PROGRESS_S seconds with the simulated time
                  reached; the monitors are copied to the output during the run, so a timeout still leaves data
  6 outputs       stoutMonitor.dat.gz, cartMonitor.dat.gz (cart rides), log.foamRun.tail.gz, walltime, case.json,
                  surface/ (the mesh and alpha.stout at every written time: the free surface for playback),
                  params.json, timing.json (cores, OS, OpenFOAM version, wall times), SHA256SUMS.txt; the notebook
                  ends with an error if the solver failed or the monitor stops before the end time
Kaggle's save_notebook drops attached data sources (Kaggle/kaggle-cli issue #1140), so everything is fetched here.
"""
import argparse, json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REPO = "https://github.com/Numa1997/SiteTest"
FIELDS = ("name", "level", "forcing", "fill", "end", "write", "wall", "sigma", "nu", "rho", "maxco", "maxdt", "ride")


def find_case(name):
    req = ROOT / "notes/fig12/of-request.json"
    for c in json.loads(req.read_text()):
        if c.get("name") == name:
            return c, str(req.relative_to(ROOT))
    rec = ROOT / "notes/fig12/of-runs" / name / "case.json"
    if rec.exists():
        return json.loads(rec.read_text()), str(rec.relative_to(ROOT))
    sys.exit(f"no case '{name}' in notes/fig12/of-request.json or notes/fig12/of-runs/{name}/case.json")


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip("\n")}


def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": text.strip("\n")}


CELL_ENV = r'''
import os, sys, json, time, platform, subprocess, hashlib, gzip, shutil, datetime
from pathlib import Path

CASE = __CASE__                      # the case, exactly as the GitHub workflow takes it
COMMIT = "__COMMIT__"                # this repository at this commit is what runs
REPO = "__REPO__"
NP = int(os.environ.get("NB_NP", "__NP__") or os.cpu_count())   # processes for the run (empty = all cores)
PROGRESS_S = 180                     # a progress line every this many seconds
WORK = Path(os.environ.get("NB_WORK", "/kaggle/working")) / CASE["name"]   # kept as the notebook's output
FOAM = "foam"                                                               # the ordinary user OpenFOAM runs as
SRC = Path(f"/home/{FOAM}/src")                                             # the code (not kept as output)
RUN = Path(f"/home/{FOAM}/run") / CASE["name"]                              # the case (not kept as output)
if WORK.exists():
    shutil.rmtree(WORK)
WORK.mkdir(parents=True)
T0 = time.time(); TIMES = {}


def log(msg):
    line = f"{datetime.datetime.now(datetime.timezone.utc):%Y-%m-%dT%H:%M:%SZ}  {time.time() - T0:9.1f} s  {msg}"
    print(line, flush=True)
    with open(WORK / "progress.log", "a") as f:
        f.write(line + "\n")


def sh(cmd, user=None, check=True):
    """Run a bash command (as `user` if given) with pipefail; return its stdout."""
    full = ["bash", "-c", "set -o pipefail; " + cmd]
    if user:
        full = ["runuser", "-u", user, "--"] + full
    r = subprocess.run(full, capture_output=True, text=True)
    if check and r.returncode:
        print(r.stdout[-3000:], r.stderr[-3000:])
        raise RuntimeError(f"command failed ({r.returncode}): {cmd}")
    return r.stdout.strip()


def meminfo_gb(key):
    for line in open("/proc/meminfo"):
        if line.startswith(key + ":"):
            return round(int(line.split()[1]) / 2**20, 2)


osr = dict(l.strip().split("=", 1) for l in open("/etc/os-release") if "=" in l)
ENV = dict(
    started_utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    on_kaggle=bool(os.environ.get("KAGGLE_KERNEL_RUN_TYPE")),
    os=osr.get("PRETTY_NAME", "").strip('"'), os_codename=osr.get("VERSION_CODENAME"),
    kernel=platform.release(), python=platform.python_version(),
    cpu_model=next((l.split(":", 1)[1].strip() for l in open("/proc/cpuinfo") if l.startswith("model name")), None),
    nproc=os.cpu_count(), cpus_usable=len(os.sched_getaffinity(0)), processes_used=NP,
    ram_total_gb=meminfo_gb("MemTotal"), ram_available_gb=meminfo_gb("MemAvailable"),
    disk_free_gb=round(shutil.disk_usage("/").free / 2**30, 1),
)
for k, v in ENV.items():
    print(f"{k:18s} {v}")
if os.geteuid() != 0:
    raise RuntimeError("this notebook installs OpenFOAM with apt and needs root (as on Kaggle)")
log(f"environment checked; case {CASE['name']}")
'''

CELL_INSTALL = r'''
t = time.time()
if not Path("/opt/openfoam13/etc/bashrc").exists():
    # the GitHub workflow's own commands (.github/workflows/fig12-openfoam.yml); OpenFOAM 13 is built for Ubuntu 24.04
    if ENV["os_codename"] != "noble":
        raise RuntimeError(f"OpenFOAM 13's packages are for Ubuntu noble; this machine is {ENV['os']}")
    sh("wget -q -O - https://dl.openfoam.org/gpg.key > /etc/apt/trusted.gpg.d/openfoam.asc")
    sh('echo "deb [arch=amd64] http://dl.openfoam.org/ubuntu noble main" > /etc/apt/sources.list.d/openfoam.list')
    sh("apt-get update -qq")
    sh("DEBIAN_FRONTEND=noninteractive apt-get install -y -qq openfoam13 bc > /dev/null")
if shutil.which("node") is None:
    sh("DEBIAN_FRONTEND=noninteractive apt-get install -y -qq nodejs > /dev/null")
if shutil.which("bc") is None:
    sh("DEBIAN_FRONTEND=noninteractive apt-get install -y -qq bc > /dev/null")
if subprocess.run(["id", FOAM], capture_output=True).returncode:
    sh(f"useradd -m {FOAM}")
TIMES["install_s"] = round(time.time() - t, 1)
ENV["openfoam"] = sh("source /opt/openfoam13/etc/bashrc > /dev/null 2>&1; echo $WM_PROJECT_VERSION", user=FOAM)
ENV["openfoam_package"] = sh("dpkg-query -W -f='${Version}' openfoam13")
ENV["node"] = sh("node --version")
log(f"OpenFOAM {ENV['openfoam']} (package {ENV['openfoam_package']}), node {ENV['node']}; install {TIMES['install_s']} s")
'''

CELL_CLONE = r'''
t = time.time()
if SRC.exists():
    shutil.rmtree(SRC)
SRC.mkdir(parents=True)
# only what the case needs: tools/fig12 (mesh, case, cart) and public/scripts (glass profile, cart model).
# Cloned as root (whose network settings apply), then handed to the user OpenFOAM runs as.
sh(f"cd {SRC} && git init -q && git remote add origin {REPO} && git sparse-checkout set tools/fig12 public/scripts"
   f" && git fetch -q --depth 1 --filter=blob:none origin {COMMIT} && git checkout -q FETCH_HEAD")
head = sh(f"cd {SRC} && git rev-parse HEAD")
sh(f"chown -R {FOAM}: {SRC}")
if head != COMMIT:
    raise RuntimeError(f"checked out {head}, expected {COMMIT}")
TIMES["clone_s"] = round(time.time() - t, 1)
log(f"code at {REPO} commit {head} ({TIMES['clone_s']} s)")
'''

CELL_CASE = r'''
t = time.time()
args = ["--level", CASE["level"], "--forcing", CASE["forcing"], "--fill", CASE["fill"], "--end", CASE["end"],
        "--write", CASE["write"], "--wall", CASE["wall"], "--sigma", CASE["sigma"], "--nu", CASE["nu"],
        "--rho", CASE["rho"], "--maxco", CASE["maxco"], "--maxdt", CASE.get("maxdt", 0.001)]
if CASE.get("ride") is not None:
    args += ["--ride", json.dumps(CASE["ride"]) if not isinstance(CASE["ride"], str) else CASE["ride"]]
RUN.parent.mkdir(parents=True, exist_ok=True); sh(f"chown -R {FOAM}: {RUN.parent}")
quoted = " ".join("'" + str(a).replace("'", "'\\''") + "'" for a in args)
print(sh(f"cd {SRC} && python3 tools/fig12/of/make_case.py {RUN} {quoted}", user=FOAM))
json.dump(CASE, open(WORK / "case.json", "w"), indent=1)
json.dump(dict(case=CASE, make_case_args=[str(a) for a in args], processes=NP, source=dict(repo=REPO, commit=COMMIT)),
          open(WORK / "params.json", "w"), indent=1)
TIMES["case_s"] = round(time.time() - t, 1)
note = sh(f"grep -a -m1 -o 'nCells: *[0-9]*' {RUN}/constant/polyMesh/owner || true")
ENV["mesh_cells"] = int(note.split(":")[1]) if note.split(":")[-1].strip() else None
log(f"case built in {TIMES['case_s']} s; {ENV['mesh_cells']} cells")
'''

CELL_RUN = r'''
def monitor_path(name):
    for p in (RUN / name, RUN / "processor0" / name):
        if p.exists():
            return p


def last_time(p):
    try:
        with open(p, "rb") as f:
            f.seek(max(0, os.path.getsize(p) - 4000))
            rows = [l.split() for l in f.read().decode(errors="ignore").splitlines() if l.strip() and not l.startswith("#")]
        return float(rows[-1][0]) if rows else None
    except (OSError, ValueError, IndexError):
        return None


def save_monitors():
    for name in ("stoutMonitor.dat", "cartMonitor.dat"):
        p = monitor_path(name)
        if p:
            with open(p, "rb") as fi, gzip.open(WORK / (name + ".gz"), "wb", compresslevel=9) as fo:
                shutil.copyfileobj(fi, fo)


t = time.time()
proc = subprocess.Popen(["runuser", "-u", FOAM, "--", "bash", str(SRC / "tools/fig12/of/run.sh"), str(RUN), str(NP)])
log(f"run started on {NP} processes, to t = {CASE['end']} s of stout")
while True:
    try:
        rc = proc.wait(timeout=PROGRESS_S); break
    except subprocess.TimeoutExpired:
        p = monitor_path("stoutMonitor.dat"); ts = last_time(p) if p else None
        el = time.time() - t
        if ts:
            log(f"t = {ts:.3f} of {CASE['end']} s; {el:.0f} s elapsed; {el / ts:.0f} s per simulated s; "
                f"about {el / ts * (float(CASE['end']) - ts) / 60:.0f} min to go")
        else:
            log(f"{el:.0f} s elapsed; no monitor line yet")
        save_monitors()
TIMES["run_s"] = round(time.time() - t, 1)
save_monitors()
log(f"run ended with exit code {rc} after {TIMES['run_s']} s")
'''

CELL_OUT = r'''
for f in ("log.foamRun",):
    p = RUN / f
    if p.exists():
        with open(p, "rb") as fi:
            fi.seek(max(0, p.stat().st_size - 200000)); tail = fi.read()
        with gzip.open(WORK / (f + ".tail.gz"), "wb", compresslevel=9) as fo:
            fo.write(tail)
if (RUN / "walltime").exists():
    shutil.copy(RUN / "walltime", WORK / "walltime")

# the free surface for playback: the mesh once, and the stout's volume fraction at every written time
surf = WORK / "surface"; surf.mkdir()
for f in ("points", "faces", "owner", "neighbour", "boundary"):
    p = RUN / "constant/polyMesh" / f
    if p.exists():
        with open(p, "rb") as fi, gzip.open(surf / ("polyMesh." + f + ".gz"), "wb", compresslevel=9) as fo:
            shutil.copyfileobj(fi, fo)
written = sorted((d for d in RUN.iterdir() if d.is_dir() and d.name != "0" and (d / "alpha.stout").exists()),
                 key=lambda d: float(d.name))
for d in written:
    with open(d / "alpha.stout", "rb") as fi, gzip.open(surf / f"alpha.stout.t{d.name}.gz", "wb", compresslevel=9) as fo:
        shutil.copyfileobj(fi, fo)

mon = WORK / "stoutMonitor.dat.gz"
t_end = None
if mon.exists():
    rows = [l.split() for l in gzip.open(mon, "rt") if l.strip() and not l.startswith("#")]
    t_end = float(rows[-1][0]) if rows else None
done = rc == 0 and t_end is not None and t_end >= float(CASE["end"]) - 1e-6
wall = float((RUN / "walltime").read_text()) if (RUN / "walltime").exists() else None
TIMES["total_s"] = round(time.time() - T0, 1)
json.dump(dict(case=CASE["name"], done=done, exit_code=rc, simulated_s=t_end, end_s=float(CASE["end"]),
               solver_wall_s=wall, written_times=[d.name for d in written], stages_s=TIMES, machine=ENV),
          open(WORK / "timing.json", "w"), indent=1)

files = sorted(p for p in WORK.rglob("*") if p.is_file() and p.name != "SHA256SUMS.txt")
with open(WORK / "SHA256SUMS.txt", "w") as f:
    for p in files:
        f.write(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(WORK)}\n")
for p in files:
    print(f"{p.stat().st_size:>12,d} B  {p.relative_to(WORK)}")
log(f"outputs written; solver wall time {wall} s; simulated to {t_end} s of {CASE['end']}")
if not done:
    raise RuntimeError("the case did not finish: the solver failed or the monitor stops before the end time (log in the output)")
'''


def build(case, commit, np_, source):
    title = f"Fig. 12 OpenFOAM: {case['name']}"
    head = md(f"""
# {title}

> **Work in progress: not yet verified.** This is one of the solver-proof (Phase 1) cases of Fig. 12, a pint of
> Guinness on a one-wheel cart. The solver has not yet passed its gates, so these numbers are not results of the figure.

What it computes: the stout in the real Guinness tulip glass, incompressible Navier–Stokes with a free surface
(OpenFOAM 13, `incompressibleVoF`, volume of fluid), stout and air, on the `{case['level']}` mesh; forcing
`{case['forcing']}`, walls `{case['wall']}`, fill {case['fill']} m, {case['end']} s of stout. The same case and the
same code run on GitHub's free runners through `.github/workflows/fig12-openfoam.yml`; this notebook repeats them
on a Kaggle CPU session and stores the same files.

Live page: <https://phyeinusul.com/simulations/beer-slosh> (it does not show these runs yet).

Code: <{REPO}> at commit `{commit[:7]}` (`tools/fig12/of/`); case taken from `{source}`.

**Computed results; this page is not interactive. Press Copy & Edit to run it yourself.**
""")
    sub = {"__CASE__": json.dumps(case), "__COMMIT__": commit, "__REPO__": REPO, "__NP__": "" if np_ is None else str(np_)}

    def fill(s):
        for k, v in sub.items():
            s = s.replace(k, v)
        return s
    cells = [head,
             md("## 1. The machine"), code(fill(CELL_ENV)),
             md("## 2. OpenFOAM 13\n\nInstalled from the publisher's repository, with the same commands as the GitHub workflow. "
                "OpenFOAM refuses to compile the case's coded monitor as root, so the case runs as the ordinary user `foam`."),
             code(CELL_INSTALL),
             md("## 3. The code\n\nA sparse clone of the website repository at the pinned commit: only `tools/fig12` and "
                "`public/scripts` (the glass profile and the cart model the mesh and the case read)."),
             code(CELL_CLONE),
             md("## 4. The case\n\n`tools/fig12/of/make_case.py` builds the mesh and the case from the parameters above "
                "(`CASE`); they are stored in `params.json` and `case.json`."),
             code(CELL_CASE),
             md("## 5. The run\n\n`tools/fig12/of/run.sh` on all cores. A progress line every few minutes; the monitors are "
                "copied to the output as the run goes, so a timeout still leaves what was computed."),
             code(CELL_RUN),
             md("## 6. Outputs\n\nThe layout of `notes/fig12/of-runs/<case>/` in the repository, plus the free surface "
                "(`surface/`), `timing.json`, `progress.log` and `SHA256SUMS.txt`."),
             code(CELL_OUT)]
    for i, c in enumerate(cells):
        c["id"] = f"{case['name']}-{i:02d}"
    nb = {"cells": cells,
          "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                       "language_info": {"name": "python"},
                       "fig12": {"case": case, "commit": commit, "source": source}},
          "nbformat": 4, "nbformat_minor": 5}
    return json.dumps(nb, ensure_ascii=False, separators=(",", ":"))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("name"); ap.add_argument("--commit"); ap.add_argument("--np", type=int)
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE")
    ap.add_argument("--out")
    a = ap.parse_args()
    case, source = find_case(a.name)
    case = {k: case[k] for k in FIELDS if k in case}
    for kv in a.set:
        k, v = kv.split("=", 1)
        if k not in FIELDS:
            sys.exit(f"unknown field {k}")
        try:
            case[k] = json.loads(v)
        except json.JSONDecodeError:
            case[k] = v
    commit = a.commit or subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    if len(commit) != 40:
        sys.exit("--commit must be a full 40-character commit hash")
    out = Path(a.out) if a.out else Path(__file__).parent / "notebooks" / f"{case['name']}.ipynb"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(case, commit, a.np, source))
    print(f"wrote {out} ({out.stat().st_size} bytes): case {case['name']}, commit {commit[:12]}")


if __name__ == "__main__":
    main()
