"""The simulations pipeline: Kaggle computes, the engine checks and stores, Cloudflare serves. Run by .github/workflows/sims-kaggle.yml.

For one simulation (a model file tools/sims/<sim>.py with a run function, listed in tools/sims/registry.json) it:
  1. writes the notebook folder: kernel-metadata.json and the script tools/sims/kaggle_sims.py with JOB = <sim>, COMMIT = the
     commit being run, GPU, SHARD, SHARDS and FORMAT filled in, so Kaggle computes exactly the code in git;
  2. pushes it as a new version of the private notebook numakoudsie/phyein-usul-simulations (`kaggle kernels push`);
  3. polls `kaggle kernels status` until the run is complete. An unreadable answer is tried again for up to 10 minutes; only a real
     "error" or "cancel" state stops the run. The time limit (registry "timeout_s") counts from the first poll that reports the run
     as running, because time spent waiting in Kaggle's queue is not the model's fault;
  4. downloads that version's output (`kaggle kernels output <notebook>/<version>`), finds index-<sim>.json, and checks every
     listed file's size and SHA-256 against it;
  5. stores the data. Where depends on the registry entry's "store":
     - "r2" (from 25 November 2026): every file goes to the Cloudflare R2 bucket phyein-usul-runs under
       sims/<sim>/<run>/[shard-<i>-of-<n>/]<file>, each upload read back and compared (tools/sims/r2.py). <run> = <date>-v<version>,
       so a rerun on the same day gets a new address and never touches the old one. The repository keeps only the combined index
       public/data/sims/<sim>/<run>/index-<sim>.json and the small files the entry names in "repo_files". A run refuses to store
       anything when the model's own checks failed (checks_passed false in its index).
       A large model can be cut into "shards": n parts, each one Kaggle notebook version, computed one after another; the runner
       holds one shard at a time (push, wait, download, check, upload, file, delete, next), so no run needs more than one shard's
       room on its disk or on Kaggle's working folder (about 20 GB).
     - "repo" (or no "store"): the files are copied to public/data/sims/<sim>/<date>/ (as before 25 November 2026).
     - "release": the files matching "release_files" go to the GitHub release sims-<sim>-<date> (as from 23 November 2026).
  6. adds the generation to public/data/sims/generations.json, and files every run's whole output as a version of the
     simulation's private Kaggle dataset (tools/sims/dataset.py); a filing failure is recorded in the entry and loses no data;
  7. writes the run's state to public/data/sims/status/<sim>.json on main as it goes (queued, running, each shard stored, failed;
     tools/sims/land.py writes "saved", tools/sims/verify_live.py "live_ok"), so anyone can see where a run stands.
Collect mode (--collect <version>[,<version>...] --shard <first>) does steps 4 to 7 for notebook versions that already ran, without
computing again: for a run whose download or upload failed, or a sharded run that stopped part way.

Authentication: the official Kaggle tool reads KAGGLE_API_TOKEN; R2 needs R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY.
Kaggle's `kernels push` exits with status 0 even when Kaggle refuses the push, so its printed answer is read and checked.

Usage: python3 tools/sims/pipeline.py <sim> <commit> [--kaggle <command>] [--timeout <s>] [--gh <command>]
                                     [--collect <versions>] [--shard <first shard>]
Exit status 0 only when every check passed; anything else stops the workflow before a commit."""
import argparse, datetime, fnmatch, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OWNER, SLUG, TITLE = "numakoudsie", "phyein-usul-simulations", "Phyein Usul simulations"
REF = f"{OWNER}/{SLUG}"
GP = os.path.join(ROOT, "public/data/sims/generations.json")

def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)
def now(): return datetime.datetime.now(datetime.timezone.utc)
def iso(t): return t.isoformat(timespec="seconds") if t else None

class Failed(Exception):
    pass

def kaggle(cmd, args):
    r = subprocess.run(cmd + args, capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    log("$ kaggle " + " ".join(args)); log(out.strip()[-1500:])
    return r.returncode, out

def sha_file(p):
    h = hashlib.sha256(); n = 0
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 24), b""): h.update(chunk); n += len(chunk)
    return n, h.hexdigest()

# ---------------------------------------------------------------- the run's status file (step 7)

class Status:
    """public/data/sims/status/<sim>.json, pushed to main at every change of state. A failed push of the status is logged and does
    not stop the run: the status reports on the data, it is not the data."""
    def __init__(self, sim, sc, commit, shards):
        self.d = dict(sim=sim, state="queued", notebook=REF, run=None, version=None, versions=[], shard=None, shards=shards,
                      card="gpu" if sc.get("gpu") else "cpu", queued_at=None, started_at=None, ended_at=None, queue_s=None, run_s=None,
                      code_commit=commit, data_commit=None, bytes_stored=0, failure=None, expected_s=None, expected_done=None,
                      expected_note=None, log_url=f"https://www.kaggle.com/code/{OWNER}/{SLUG}/log",
                      progress_note="Kaggle does not report progress during a run; watch the notebook's log page.")
        self.expect()
    def expect(self):
        """The expected duration comes only from a measured benchmark (public/data/sims/bench/<sim>.json), never from a guess."""
        p = os.path.join(ROOT, "public/data/sims/bench", self.d["sim"] + ".json")
        if not os.path.exists(p):
            self.d.update(expected_s=None, expected_done=None, expected_note=f"no benchmark file public/data/sims/bench/{self.d['sim']}.json yet"); return
        b = json.load(open(p)).get("full_run_s"); s = b.get(self.d["card"]) if isinstance(b, dict) else b
        if s is None:
            self.d.update(expected_s=None, expected_done=None, expected_note=f"the benchmark has no full_run_s for the card {self.d['card']}"); return
        self.d.update(expected_s=s, expected_note=None)
        start = self.d["started_at"] or self.d["queued_at"]
        if start: self.d["expected_done"] = iso(datetime.datetime.fromisoformat(start) + datetime.timedelta(seconds=float(s)))
    def push(self, **kw):
        self.d.update(kw); self.expect()
        if self.d["queued_at"] and self.d["started_at"]:
            self.d["queue_s"] = round((datetime.datetime.fromisoformat(self.d["started_at"]) - datetime.datetime.fromisoformat(self.d["queued_at"])).total_seconds())
        if self.d["started_at"] and self.d["ended_at"]:
            self.d["run_s"] = round((datetime.datetime.fromisoformat(self.d["ended_at"]) - datetime.datetime.fromisoformat(self.d["started_at"])).total_seconds())
        self.write_local()
        try:
            import land
            land.push_status(self.d["sim"], self.d)
        except BaseException as ex:   # land exits through sys.exit on a git failure; the run goes on
            log("the status file could not be pushed:", ex)
    def write_local(self):
        p = os.path.join(ROOT, "public/data/sims/status", self.d["sim"] + ".json"); os.makedirs(os.path.dirname(p), exist_ok=True)
        json.dump(self.d, open(p, "w"), indent=1, ensure_ascii=False); open(p, "a").write("\n")

# ---------------------------------------------------------------- Kaggle: notebook, push, wait, download (steps 1 to 4)

def notebook(sim, commit, gpu, shard, shards, fmt):
    nb = tempfile.mkdtemp(prefix="nb-")
    src = open(os.path.join(ROOT, "tools/sims/kaggle_sims.py")).read()
    for name, val in (("JOB", f'"{sim}"'), ("GPU", repr(bool(gpu))), ("SHARD", str(int(shard))), ("SHARDS", str(int(shards))), ("FORMAT", str(int(fmt)))):
        src, n = re.subn(rf"^{name} = [^#\n]*", f"{name} = {val}".ljust(36), src, count=1, flags=re.M)   # the comment after it stays in place
        if n != 1: raise Failed(f"tools/sims/kaggle_sims.py has no line '{name} = ...' to fill")
    src = src.replace("__COMMIT__", commit)
    assert f'JOB = "{sim}"' in src and commit in src
    open(os.path.join(nb, "kaggle_sims.py"), "w").write(src)
    json.dump(dict(id=REF, title=TITLE, code_file="kaggle_sims.py", language="python", kernel_type="script", is_private=True,
                   enable_gpu=bool(gpu), enable_tpu=False, enable_internet=True, dataset_sources=[], competition_sources=[],
                   kernel_sources=[], model_sources=[]), open(os.path.join(nb, "kernel-metadata.json"), "w"), indent=1)
    return nb

def push(K, nb):
    rc, out = kaggle(K, ["kernels", "push", "-p", nb])
    m = re.search(r"version\s+(\d+)\s+successfully pushed", out, re.I)
    if rc or not m: raise Failed("Kaggle did not accept the push (its answer is in the log)")
    shutil.rmtree(nb, ignore_errors=True)
    return int(m.group(1))

def wait(K, timeout, queue_limit, on_running):
    """Poll until complete. Returns the moment the run was first seen running (or None if it was never seen running)."""
    poll = float(os.environ.get("POLL_S", 20)); t_push = time.time(); started = None; err_since = None; k = 0; state = ""
    while True:
        time.sleep(poll)
        rc, out = kaggle(K, ["kernels", "status", REF])
        mm = re.search(r'status\s+"?([A-Za-z_.]+)"?', out)
        if rc or not mm:
            # an error answer or one that cannot be read is Kaggle's or the network's trouble, not the run's: try again, waiting longer
            err_since = err_since or time.time(); k += 1
            if time.time() - err_since > 600: raise Failed(f"Kaggle's status could not be read for 10 minutes (last answer: {out.strip()[-300:]})")
            time.sleep(min(60.0, poll * 2 ** k)); continue
        err_since = None; k = 0; state = mm.group(1).lower()
        if "complete" in state: return started
        if any(w in state for w in ("error", "cancel")): raise Failed(f"the Kaggle run ended in state {state}")
        if "running" in state and started is None:
            started = time.time(); on_running()
        if started is not None and time.time() - started > timeout:
            raise Failed(f"no result within {timeout} s of running (last state: {state})")
        if started is None and time.time() - t_push > queue_limit:
            raise Failed(f"still waiting in Kaggle's queue after {queue_limit} s (last state: {state})")

def download(K, sim, version, expect_commit, shard, shards):
    """Download one version's output and check it file by file. Returns (folder holding the files, index, download folder)."""
    dl = tempfile.mkdtemp(prefix="out-")
    rc, out = kaggle(K, ["kernels", "output", f"{REF}/{version}", "-p", dl])
    if rc: raise Failed(f"the download of version {version} failed")
    idx = [os.path.join(d, f) for d, _, fs in os.walk(dl) for f in fs if f == f"index-{sim}.json"]
    if len(idx) != 1: raise Failed(f"expected one index-{sim}.json in the output of version {version}, found {len(idx)}")
    index = json.load(open(idx[0])); here = os.path.dirname(idx[0])
    if index.get("job") != sim: raise Failed(f"the output index of version {version} names another simulation ({index.get('job')})")
    if expect_commit and index["source"]["commit"] != expect_commit: raise Failed(f"the output of version {version} was computed from {index['source']['commit'][:7]}, not {expect_commit[:7]}")
    if (index.get("shard", 1), index.get("shards", 1)) != (shard, shards): raise Failed(f"version {version} computed shard {index.get('shard', 1)} of {index.get('shards', 1)}, expected {shard} of {shards}")
    for f, meta in index["files"].items():
        p = os.path.join(here, f)
        if not os.path.isfile(p): raise Failed(f"{f}: listed in the index but missing from the output")
        if sha_file(p) != (meta["bytes"], meta["sha256"]): raise Failed(f"{f}: size or SHA-256 differs from the index")
    log(f"version {version}: all {len(index['files'])} files match their SHA-256")
    return here, index, dl

def load_gen():
    return json.load(open(GP)) if os.path.exists(GP) else dict(about="Data of the site's simulations, computed once on Kaggle by the notebook "
        f"{REF} and carried here by .github/workflows/sims-kaggle.yml. One entry per simulation and run; a page plays the newest entry of its simulation.", generations=[])

def save_gen(g):
    json.dump(g, open(GP, "w"), indent=1, ensure_ascii=False); open(GP, "a").write("\n")

def out(**kw):
    if os.environ.get("GITHUB_OUTPUT"): open(os.environ["GITHUB_OUTPUT"], "a").write("".join(f"{k}={v}\n" for k, v in kw.items()))

# ---------------------------------------------------------------- store "r2"

def shard_index_from_r2(sim, run, i, n):
    """The index of a shard stored by an earlier workflow run (collect mode finishing a sharded run)."""
    import r2
    key = f"sims/{sim}/{run}/shard-{i}-of-{n}/index-{sim}.json"
    try: body = r2.call(f"GET {key}", lambda: r2.client().get_object(Bucket=r2.BUCKET, Key=key)["Body"].read())
    except Exception as ex: raise Failed(f"shard {i} of run {run} is not in R2 ({key}: {ex})")
    return json.loads(body)

def run_r2(a, sc, K):
    import r2
    if r2.missing_keys(): sys.exit("the repository secrets " + ", ".join(r2.missing_keys()) + " are missing")
    import dataset as DS
    n = int(sc.get("shards", 1)); fmt = int(sc.get("format", 1)); gpu = bool(sc.get("gpu"))
    timeout = a.timeout or int(sc.get("timeout_s", 1800)); queue_limit = int(sc.get("queue_s", 5 * 3600))
    collect = [int(v) for v in a.collect.split(",")] if a.collect else []
    first = a.shard or 1
    if collect and first + len(collect) - 1 > n: raise SystemExit(f"{len(collect)} versions from shard {first} exceed the {n} shards of {a.sim}")
    last = first + len(collect) - 1 if collect else n
    st = Status(a.sim, sc, a.commit, n)
    run = None; versions = {}; shard_idx = {}; commit = None if collect else a.commit
    if first > 1:
        # finishing a sharded run: its address and the shards already stored come from its status file and from R2
        old = json.load(open(os.path.join(ROOT, "public/data/sims/status", a.sim + ".json")))
        run = old.get("run")
        if not run: raise SystemExit(f"the status file of {a.sim} names no run to finish")
        st.d.update({k: old.get(k) for k in ("run", "queued_at", "started_at", "card", "bytes_stored")})
        for i, v in enumerate(old.get("versions") or [], start=1):
            if i < first: versions[i] = v; shard_idx[i] = shard_index_from_r2(a.sim, run, i, n)
        if len(versions) != first - 1: raise SystemExit(f"the status file of {a.sim} lists {len(versions)} stored shards, shard {first} needs {first - 1}")
    filed, ds_errors = [], []
    try:
        for i in range(first, last + 1):
            # one shard from start to end, so the runner holds at most one shard's data at a time
            if collect:
                v = collect[i - first]; log(f"shard {i} of {n}: collecting notebook version {v}")
            else:
                v = push(K, notebook(a.sim, a.commit, gpu, i, n, fmt)); log(f"shard {i} of {n}: pushed version {v}")
                st.push(state="queued", version=v, versions=[versions[j] for j in sorted(versions)] + [v], shard=i, queued_at=st.d["queued_at"] or iso(now()))
                wait(K, timeout, queue_limit, lambda: st.push(state="running", started_at=st.d["started_at"] or iso(now())))
            here, index, dl = download(K, a.sim, v, commit, i, n)
            commit = commit or index["source"]["commit"]
            if index.get("checks_passed") is False: raise Failed(f"shard {i} (version {v}): the model's own checks failed (checks_passed false); nothing of it is stored")
            if index.get("checks_passed") is None: log(f"shard {i}: the model wrote no checks_passed")
            if run is None: run = f"{index['date']}-v{v}"   # the address: the day shard 1 computed, the version of shard 1
            prefix = f"sims/{a.sim}/{run}/" + (f"shard-{i}-of-{n}/" if n > 1 else "")
            stored = 0
            for f, meta in sorted(index["files"].items()):
                r2.put(os.path.join(here, f), prefix + f, meta["sha256"], meta["bytes"]); stored += meta["bytes"]
            if n > 1:   # each shard's own index goes along, so collect mode can rebuild the combined index later
                ip = os.path.join(here, f"index-{a.sim}.json"); b, h = sha_file(ip); r2.put(ip, prefix + f"index-{a.sim}.json", h, b)
            dest = os.path.join(ROOT, "public/data/sims", a.sim, run)
            for f in index["files"]:
                if any(fnmatch.fnmatch(f, p) for p in sc.get("repo_files", [])):
                    q = os.path.join(dest, (f"shard-{i}-of-{n}/" if n > 1 else "") + f); os.makedirs(os.path.dirname(q), exist_ok=True); shutil.copy2(os.path.join(here, f), q)
            versions[i] = v; shard_idx[i] = index
            try:
                ref, folder, _ = DS.file_dataset(a.sim, v, dl, K); filed.append((ref, folder))
            except SystemExit as ex:
                ds_errors.append(f"shard {i} (version {v}): {ex}"); log("dataset not filed:", ex)
            shutil.rmtree(dl, ignore_errors=True)
            st.push(state="running", run=run, version=versions[min(versions)], versions=[versions[j] for j in sorted(versions)],
                    shard=i, card=index.get("card") or st.d["card"], bytes_stored=(st.d["bytes_stored"] or 0) + stored,
                    started_at=st.d["started_at"] or iso(now()))
            log(f"shard {i} of {n} stored: {len(index['files'])} files, {stored} bytes under {prefix}")
    except (Failed, r2.R2Error) as ex:
        st.push(state="failed", failure=str(ex), ended_at=iso(now()), run=run)
        sys.exit(str(ex))
    if len(versions) < n:
        st.push(state="running", failure=None); log(f"{len(versions)} of {n} shards stored; collect the rest to finish the run"); out(run=run, commit=commit); return
    # the combined index and the generation (step 6)
    one = shard_idx[1]; idxs = [shard_idx[i] for i in range(1, n + 1)]
    cps = [x.get("checks_passed") for x in idxs]
    files = {}
    for i, x in enumerate(idxs, start=1):
        for f, m in x["files"].items(): files[(f"shard-{i}-of-{n}/" if n > 1 else "") + f] = dict(bytes=m["bytes"], sha256=m["sha256"], shard=i)
    collected = iso(now()); vs = [versions[i] for i in range(1, n + 1)]
    combined = dict(project="sims", job=a.sim, sim=a.sim, run=run, date=one["date"], format=one.get("format", fmt), store="r2",
                    source=one["source"], notebook=REF, versions=vs, shards=n, machine=one.get("machine"), card=one.get("card"),
                    libraries=one.get("libraries"), checks_passed=False if False in cps else (None if None in cps else True),
                    grid_parts=[x.get("grid_part") for x in idxs], files=files, wall_s=round(sum(x.get("wall_s", 0) for x in idxs), 1), collected=collected)
    dest = os.path.join(ROOT, "public/data/sims", a.sim, run); os.makedirs(dest, exist_ok=True)
    json.dump(combined, open(os.path.join(dest, f"index-{a.sim}.json"), "w"), indent=1, ensure_ascii=False)
    g = load_gen()
    g["generations"] = [q for q in g["generations"] if not (q["sim"] == a.sim and q.get("run") == run)]   # collecting again replaces the same run
    e = dict(sim=a.sim, date=one["date"], run=run, version=vs[0], versions=vs, notebook=REF, commit=one["source"]["commit"], format=combined["format"],
             store="r2", shards=n, index=f"{a.sim}/{run}/index-{a.sim}.json", files={f: dict(bytes=m["bytes"], sha256=m["sha256"]) for f, m in files.items()},
             gpu=gpu, wall_s=combined["wall_s"], collected=collected)
    if filed: e.update(dataset=filed[0][0], dataset_paths=[f + "/" for _, f in filed])
    if ds_errors: e["dataset_error"] = "; ".join(ds_errors)
    g["generations"].append(e); save_gen(g)
    st.d.update(state="running", run=run, versions=vs, version=vs[0], ended_at=iso(now()), failure=None); st.write_local()   # land.py pushes "saved"
    log(f"run {run}: {len(files)} files, {sum(m['bytes'] for m in files.values())} bytes in R2; index public/data/sims/{a.sim}/{run}/index-{a.sim}.json")
    out(version=vs[0], day=one["date"], run=run, commit=one["source"]["commit"])

# ---------------------------------------------------------------- stores "repo" and "release" (unchanged in what they store)

def run_repo(a, sc, K):
    gpu = bool(sc.get("gpu")); timeout = a.timeout or int(sc.get("timeout_s", 1800)); queue_limit = int(sc.get("queue_s", 5 * 3600))
    big = lambda f: sc.get("store") == "release" and any(fnmatch.fnmatch(f, p) for p in sc.get("release_files", []))
    st = Status(a.sim, sc, a.commit, 1)
    try:
        if a.collect:
            version = int(a.collect.split(",")[0]); commit = None
        else:
            version = push(K, notebook(a.sim, a.commit, gpu, 1, 1, int(sc.get("format", 1)))); log("pushed version", version); commit = a.commit
            st.push(state="queued", version=version, versions=[version], shard=1, queued_at=iso(now()))
            wait(K, timeout, queue_limit, lambda: st.push(state="running", started_at=iso(now())))
        here, index, dl = download(K, a.sim, version, commit, 1, 1)
    except Failed as ex:
        st.push(state="failed", failure=str(ex), ended_at=iso(now())); sys.exit(str(ex))
    commit = index["source"]["commit"]; day = index["date"]; tag = None
    large = {f: m for f, m in index["files"].items() if big(f)}
    if large:   # 5a. large data into the GitHub release sims-<sim>-<date>; a rerun on the same day replaces it
        tag = f"sims-{a.sim}-{day}"; G = a.gh.split()
        subprocess.run(G + ["release", "delete", tag, "--yes", "--cleanup-tag"], capture_output=True)
        r = subprocess.run(G + ["release", "create", tag, "--title", f"Simulation data: {a.sim}, {day}",
                                "--notes", f"Computed on Kaggle ({REF}, version {version}) from commit {commit}. Fingerprints: public/data/sims/{a.sim}/{day}/index-{a.sim}.json. Served by the site under /rel/{tag}/."]
                           + [os.path.join(here, f) for f in sorted(large)], capture_output=True, text=True)
        log(r.stdout[-1500:], r.stderr[-1500:])
        if r.returncode: st.push(state="failed", failure="the GitHub release could not be made", ended_at=iso(now())); sys.exit("the GitHub release could not be made (its answer is above)")
        r = subprocess.run(G + ["release", "view", tag, "--json", "assets"], capture_output=True, text=True)
        got = {x["name"]: x["size"] for x in json.loads(r.stdout or "{}").get("assets", [])}
        for f, m in large.items():
            if got.get(f) != m["bytes"]: st.push(state="failed", failure=f"{f}: the release holds another size", ended_at=iso(now())); sys.exit(f"{f}: the release holds {got.get(f)} bytes, the index says {m['bytes']}")
        log("release", tag, "holds", len(large), "files,", sum(m["bytes"] for m in large.values()), "bytes, sizes match")
    # 5. into the site
    dest = os.path.join(ROOT, "public/data/sims", a.sim, day); os.makedirs(dest, exist_ok=True)
    for f in [f for f in index["files"] if f not in large] + [f"index-{a.sim}.json"]: shutil.copy2(os.path.join(here, f), os.path.join(dest, f))
    g = load_gen()
    # one entry per simulation and day for these stores: a rerun the same day replaces it (an "r2" run of that day is a different entry)
    g["generations"] = [q for q in g["generations"] if not (q["sim"] == a.sim and q["date"] == day and not q.get("run"))]
    g["generations"].append(dict(sim=a.sim, date=day, notebook=REF, version=version, commit=commit,
                                 index=f"{a.sim}/{day}/index-{a.sim}.json", files={f: v for f, v in index["files"].items() if f not in large},
                                 **(dict(release=tag, release_files=large, gpu=gpu) if large else {}),
                                 wall_s=round(index.get("wall_s", 0), 1), collected=iso(now())))
    save_gen(g)
    log(f"stored under public/data/sims/{a.sim}/{day}/, generations.json updated")
    # 6. every data set also stays on Kaggle: the whole output as a version of the simulation's private dataset (tools/sims/dataset.py).
    #    A failure here does not throw the computed data away: the entry records it, and Run workflow with mode = dataset repeats it.
    try:
        import dataset as DS
        DS.record(a.sim, version, *DS.file_dataset(a.sim, version, dl, K))
    except SystemExit as ex:
        g = json.load(open(GP)); [q.update(dataset_error=str(ex)) for q in g["generations"] if q["sim"] == a.sim and q["date"] == day and not q.get("run")]
        save_gen(g); log("dataset not filed:", ex)
    st.d.update(state="running", ended_at=iso(now()), card=index.get("card") or st.d["card"]); st.write_local()
    out(version=version, day=day, commit=commit)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("sim"); ap.add_argument("commit")
    ap.add_argument("--kaggle", default="kaggle"); ap.add_argument("--timeout", type=int, default=None); ap.add_argument("--gh", default="gh")
    ap.add_argument("--collect", default="", help="collect mode: the notebook versions to fetch, comma-separated, in shard order")
    ap.add_argument("--shard", type=int, default=None, help="collect mode: the shard number of the first version")
    a = ap.parse_args(); K = a.kaggle.split()
    reg = json.load(open(os.path.join(ROOT, "tools/sims/registry.json")))["sims"]
    if a.sim not in reg or not os.path.exists(os.path.join(ROOT, reg[a.sim]["model"])):
        sys.exit(f"{a.sim} is not a simulation in tools/sims/registry.json (or its model file is missing)")
    if not re.fullmatch(r"[0-9a-f]{40}", a.commit): sys.exit("commit must be a full 40-character hash")
    if a.collect and not re.fullmatch(r"\d+(,\d+)*", a.collect): sys.exit("--collect takes notebook versions, for example 41 or 41,42,43")
    sc = reg[a.sim]
    try:
        (run_r2 if sc.get("store") == "r2" else run_repo)(a, sc, K)
    except Failed as ex:
        sys.exit(str(ex))

if __name__ == "__main__":
    main()
