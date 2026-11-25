"""Local end-to-end test of the engine on R2 (docs/kaggle-sims.md): every step of a run, with nothing real touched.

It builds, in one temporary folder that it removes at the end:
  - a bare git repository as "origin" (main = this repository's HEAD plus the engine files as they stand in the working tree), and
    for each case a fresh clone of it, the "runner's checkout", in which the engine runs as it would on GitHub's runner;
  - a local S3 server (moto) standing in for Cloudflare R2, with the bucket phyein-usul-runs;
  - a stand-in for the Kaggle tool: "kernels push" keeps the notebook and answers a new version number, "kernels status" answers a
    scripted sequence, "kernels output" runs the pushed notebook text on this machine (against the local origin) and hands out its
    output, kept per version as Kaggle keeps it; dataset commands are refused, so the dataset filing fails and is recorded;
  - a local web server for verify_live.py: public/ of the landed main, and /r2/<key> from the S3 server with byte ranges.
Twelve cases, each printing "PASS <name>" or "FAIL <name>: <why>", then "<passed> passed, <failed> failed"; exit 0 only if none failed.
Usage: python3 tools/sims/test_engine_r2.py [case numbers, e.g. 1 5 12]"""
import datetime, http.server, json, os, shutil, socket, subprocess, sys, tempfile, threading, time, traceback

SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PARTS = ["tools", "docs", "public/data/sims", "public/scripts", "notes/sims", ".github", "AGENTS.md", "CLAUDE.md", ".gitignore",
         "public/*.html"]   # tools/inventory.py reads the pages for their walkthrough keys
BUCKET = "phyein-usul-runs"
PY = sys.executable

def need(mod, pkg):
    try: __import__(mod)
    except ImportError: subprocess.run([PY, "-m", "pip", "install", "-q", pkg], check=True)

need("boto3", "boto3==1.40.70"); need("moto", "moto[server]==5.1.16"); need("flask_cors", "moto[server]==5.1.16"); need("numpy", "numpy")
import boto3
from moto.server import ThreadedMotoServer

def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p

def sh(*a, cwd=None, env=None, check=True):
    r = subprocess.run(list(a), cwd=cwd, env=env, capture_output=True, text=True)
    if check and r.returncode: raise RuntimeError(f"{' '.join(a)} failed ({r.returncode}): {(r.stdout + r.stderr)[-1500:]}")
    return r

FAKE = r'''
import json, os, shutil, subprocess, sys
D = os.environ["FAKE_KAGGLE"]; REF = "numakoudsie/phyein-usul-simulations"
cfg_p = os.path.join(D, "config.json"); cfg = json.load(open(cfg_p)) if os.path.exists(cfg_p) else {}
def save(): json.dump(cfg, open(cfg_p, "w"))
a = sys.argv[1:]
if a[:2] == ["kernels", "push"]:
    n_p = os.path.join(D, "counter"); n = int(open(n_p).read()) + 1 if os.path.exists(n_p) else 1; open(n_p, "w").write(str(n))
    shutil.copytree(a[a.index("-p") + 1], os.path.join(D, "pushed", str(n)))
    open(os.path.join(D, "latest"), "w").write(str(n))
    print(f"Kernel version {n} successfully pushed.  Please check progress at https://www.kaggle.com/code/{REF}")
elif a[:2] == ["kernels", "status"]:
    if cfg.get("hook"): subprocess.run(cfg.pop("hook"), shell=True, check=True); save()
    seq = cfg.get("status", [])
    s = seq.pop(0) if seq else "complete"; cfg["status"] = seq; save()
    if s == "error": print("500 Server Error: Internal Server Error"); sys.exit(1)
    print(f'{REF} has status "KernelWorkerStatus.{s.upper()}"')
elif a[:2] == ["kernels", "output"]:
    ref = a[2]; v = ref.split("/")[2] if ref.count("/") == 2 else open(os.path.join(D, "latest")).read().strip()
    cache = os.path.join(D, "outputs", v)
    if not os.path.isdir(cache):   # Kaggle keeps each version's output; the stand-in computes it once, on first request
        work = os.path.join(D, "work-" + v); os.makedirs(work)
        env = dict(os.environ, KAGGLE_WORKING_DIR=work, SIMS_REPO_URL=os.environ["FAKE_ORIGIN"])
        r = subprocess.run([sys.executable, os.path.join(D, "pushed", v, "kaggle_sims.py")], cwd=work, env=env, capture_output=True, text=True)
        open(os.path.join(work, "phyein-usul-simulations.log"), "w").write(r.stdout + r.stderr)
        if r.returncode: print("the notebook failed:", (r.stdout + r.stderr)[-2000:]); sys.exit(1)
        shutil.copytree(work, cache); shutil.rmtree(work)
    dest = a[a.index("-p") + 1]; shutil.copytree(cache, dest, dirs_exist_ok=True)
    if cfg.get("alter"):   # a file changed after the notebook wrote its index
        for d, _, fs in os.walk(dest):
            for f in fs:
                if f == cfg["alter"]:
                    b = bytearray(open(os.path.join(d, f), "rb").read()); b[0] ^= 0xFF; open(os.path.join(d, f), "wb").write(bytes(b))
    print("Output file downloaded to", dest)
elif a[:1] == ["datasets"]:
    print("403 Client Error: Forbidden (the stand-in files no datasets)"); sys.exit(1)
else:
    print("the stand-in does not know:", a); sys.exit(2)
'''

class Site(http.server.BaseHTTPRequestHandler):
    root = None; s3 = None
    def log_message(self, *a): pass
    def do_GET(self):
        path = self.path.split("?")[0]
        if path.startswith("/r2/"):
            key = path[4:]; rng = self.headers.get("Range")
            try:
                o = self.s3.get_object(Bucket=BUCKET, Key=key, **({"Range": rng} if rng else {}))
            except Exception:
                self.send_response(404); self.end_headers(); return
            body = o["Body"].read()
            self.send_response(206 if rng else 200)
            if rng: self.send_header("Content-Range", o["ContentRange"])
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body); return
        p = os.path.join(self.root, path.lstrip("/"))
        if not os.path.isfile(p): self.send_response(404); self.end_headers(); return
        b = open(p, "rb").read(); self.send_response(200); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

class T:
    def setup(self):
        self.tmp = tempfile.mkdtemp(prefix="engine-test-")
        self.origin = os.path.join(self.tmp, "origin.git")
        # The origin holds the parts of the repository the engine reads and writes, as they stand in the working tree; a full checkout
        # of the repository (about 1.8 GB) would make every case's clone take most of a minute.
        sh("git", "init", "-q", "--bare", "-b", "main", self.origin)
        seed = os.path.join(self.tmp, "seed"); os.makedirs(seed)
        files = sh("git", "ls-files", "--cached", "--others", "--exclude-standard", *PARTS, cwd=SRC).stdout.split("\n")
        for f in filter(None, files):
            if os.path.isfile(os.path.join(SRC, f)):
                os.makedirs(os.path.dirname(os.path.join(seed, f)) or seed, exist_ok=True); shutil.copy2(os.path.join(SRC, f), os.path.join(seed, f))
        sh("git", "init", "-q", "-b", "main", cwd=seed)
        sh(PY, "tools/inventory.py", cwd=seed)
        sh("git", "add", "-A", cwd=seed)
        sh("git", "-c", "user.name=test", "-c", "user.email=test@example.invalid", "commit", "-q", "-m", "test: the engine's parts of the working tree", cwd=seed)
        sh("git", "remote", "add", "origin", self.origin, cwd=seed); sh("git", "push", "-q", "origin", "main", cwd=seed); shutil.rmtree(seed)
        self.port = free_port(); self.moto = ThreadedMotoServer(ip_address="127.0.0.1", port=self.port, verbose=False); self.moto.start()
        self.env = dict(os.environ, R2_ENDPOINT=f"http://127.0.0.1:{self.port}", R2_ACCESS_KEY_ID="test", R2_SECRET_ACCESS_KEY="test",
                        R2_BUCKET=BUCKET, POLL_S="0.2", LAND_WAIT="1", R2_WAIT_SCALE="0.01", FAKE_ORIGIN=self.origin,
                        TMPDIR=os.path.join(self.tmp, "t"))   # the engine's own temporary folders and landing worktrees stay inside the test's folder
        os.makedirs(self.env["TMPDIR"])
        for k in ("R2_ACCOUNT_ID", "GITHUB_OUTPUT", "GITHUB_STEP_SUMMARY", "SIMS_SMOKE_FAIL"): self.env.pop(k, None)
        self.s3 = boto3.client("s3", endpoint_url=self.env["R2_ENDPOINT"], region_name="us-east-1", aws_access_key_id="test", aws_secret_access_key="test")
        self.s3.create_bucket(Bucket=BUCKET)
        self.fake_dir = os.path.join(self.tmp, "kaggle"); os.makedirs(self.fake_dir)
        self.fake = os.path.join(self.tmp, "fakekaggle.py"); open(self.fake, "w").write(FAKE)
        self.env["FAKE_KAGGLE"] = self.fake_dir
        self.site_dir = os.path.join(self.tmp, "site"); self.n = 0
        Site.s3 = self.s3; Site.root = os.path.join(self.site_dir, "public")
        self.web = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Site); threading.Thread(target=self.web.serve_forever, daemon=True).start()
        self.site = f"http://127.0.0.1:{self.web.server_address[1]}"
        self.runs = {}

    def teardown(self):
        try:
            if getattr(self, "web", None): self.web.shutdown()
            if getattr(self, "moto", None): self.moto.stop()
        finally:
            shutil.rmtree(self.tmp, ignore_errors=True)

    def clone(self, name):
        d = os.path.join(self.tmp, name); shutil.rmtree(d, ignore_errors=True)
        sh("git", "clone", "-q", "-b", "main", self.origin, d); return d

    def config(self, **c): json.dump(c, open(os.path.join(self.fake_dir, "config.json"), "w"))
    def counter(self):
        p = os.path.join(self.fake_dir, "counter"); return int(open(p).read()) if os.path.exists(p) else 0

    def engine(self, sim, *extra, registry=None, env=None):
        """One workflow run: a fresh checkout of main, pipeline.py, and (if it passed) land.py. Returns (ok, log, checkout, commit)."""
        self.n += 1; w = self.clone(f"run{self.n}")
        if registry:
            rp = os.path.join(w, "tools/sims/registry.json"); r = json.load(open(rp)); r["sims"][sim].update(registry); json.dump(r, open(rp, "w"), indent=1)
        commit = sh("git", "rev-parse", "HEAD", cwd=w).stdout.strip()
        e = dict(self.env, **(env or {}))
        p = sh(PY, "tools/sims/pipeline.py", sim, commit, "--kaggle", f"{PY} {self.fake}", *extra, cwd=w, env=e, check=False)
        log = p.stdout + p.stderr
        if p.returncode: return False, log, w, commit
        gen = json.load(open(os.path.join(w, "public/data/sims/generations.json")))["generations"]
        land_commit = next((q["commit"] for q in reversed(gen) if q["sim"] == sim), commit)
        l = sh(PY, "tools/sims/land.py", sim, land_commit, cwd=w, env=e, check=False)
        log += l.stdout + l.stderr
        return l.returncode == 0, log, w, commit

    def main_file(self, path):
        r = sh("git", "--git-dir", self.origin, "show", f"main:{path}", check=False)
        return r.stdout if r.returncode == 0 else None
    def main_json(self, path):
        t = self.main_file(path); return json.loads(t) if t is not None else None
    def gens(self): return self.main_json("public/data/sims/generations.json")["generations"]
    def status(self, sim="sims_smoke"): return self.main_json(f"public/data/sims/status/{sim}.json")
    def objects(self, prefix=""):
        out = {}
        for page in self.s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
            for o in page.get("Contents", []):
                h = self.s3.head_object(Bucket=BUCKET, Key=o["Key"]); out[o["Key"]] = (o["Size"], o["ETag"], (h.get("Metadata") or {}).get("sha256"))
        return out
    def today(self): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    # ------------------------------------------------------------------ the cases
    def c1_r2_one_shard(self):
        self.config(status=["queued", "running", "complete"])
        ok, log, w, commit = self.engine("sims_smoke")
        assert ok, "the run failed: " + log[-2000:]
        v = self.counter(); run = f"{self.today()}-v{v}"; self.runs["c1"] = (run, commit, v)
        objs = self.objects(f"sims/sims_smoke/{run}/")
        assert set(objs) == {f"sims/sims_smoke/{run}/a.bin", f"sims/sims_smoke/{run}/b.json"}, f"objects: {sorted(objs)}"
        idx = self.main_json(f"public/data/sims/sims_smoke/{run}/index-sims_smoke.json"); assert idx, "no combined index on main"
        for f, m in idx["files"].items():
            assert objs[f"sims/sims_smoke/{run}/{f}"][0] == m["bytes"] and objs[f"sims/sims_smoke/{run}/{f}"][2] == m["sha256"], f"{f}: object differs from the index"
        assert log.count("stored and read back") == 2, "read-back not reported for both files"
        e = [q for q in self.gens() if q["sim"] == "sims_smoke" and q.get("run") == run]
        assert len(e) == 1 and e[0]["store"] == "r2" and e[0]["format"] == 1 and set(e[0]["files"]) == {"a.bin", "b.json"}, f"entry: {e}"
        assert all("bytes" in m and "sha256" in m for m in e[0]["files"].values()), "entry files lack bytes or sha256"
        tree = sh("git", "--git-dir", self.origin, "ls-tree", "-r", "--name-only", "main", "public/data/sims/sims_smoke/").stdout.split()
        assert tree == [f"public/data/sims/sims_smoke/{run}/index-sims_smoke.json"], f"committed: {tree}"
        st = self.status(); assert st["state"] == "saved" and st["run"] == run and st["data_commit"], f"status: {st}"
        assert "dataset_error" in e[0], "the refused dataset filing was not recorded"

    def c2_three_shards(self):
        self.config(); before = self.counter()
        ok, log, w, commit = self.engine("sims_smoke", registry={"shards": 3})
        assert ok, "the run failed: " + log[-2000:]
        vs = [before + 1, before + 2, before + 3]; assert self.counter() == before + 3, f"pushes: {self.counter() - before}"
        for i, v in enumerate(vs, start=1):
            t = open(os.path.join(self.fake_dir, "pushed", str(v), "kaggle_sims.py")).read()
            assert f"\nSHARD = {i} " in t and "\nSHARDS = 3 " in t, f"version {v} was not pushed as shard {i} of 3"
        run = f"{self.today()}-v{vs[0]}"
        objs = self.objects(f"sims/sims_smoke/{run}/")
        for i in (1, 2, 3):
            for f in ("a.bin", "b.json", "index-sims_smoke.json"): assert f"sims/sims_smoke/{run}/shard-{i}-of-3/{f}" in objs, f"missing shard {i} {f}"
        idx = self.main_json(f"public/data/sims/sims_smoke/{run}/index-sims_smoke.json")
        assert len(idx["files"]) == 6 and sorted(m["shard"] for m in idx["files"].values()) == [1, 1, 2, 2, 3, 3], f"index files: {idx['files']}"
        assert idx["versions"] == vs, f"versions {idx['versions']} != {vs}"

    def c3_same_day_rerun(self):
        run1, _, _ = self.runs["c1"]
        before = self.objects(f"sims/sims_smoke/{run1}/"); idx_before = self.main_file(f"public/data/sims/sims_smoke/{run1}/index-sims_smoke.json")
        self.config(); ok, log, w, commit = self.engine("sims_smoke")
        assert ok, "the rerun failed: " + log[-2000:]
        run2 = f"{self.today()}-v{self.counter()}"; assert run2 != run1
        assert len(self.objects(f"sims/sims_smoke/{run2}/")) == 2, "the rerun's objects are missing"
        assert self.objects(f"sims/sims_smoke/{run1}/") == before, "the first run's objects changed"
        assert self.main_file(f"public/data/sims/sims_smoke/{run1}/index-sims_smoke.json") == idx_before, "the first run's index changed"
        runs = [q.get("run") for q in self.gens() if q["sim"] == "sims_smoke"]; assert run1 in runs and run2 in runs, f"entries: {runs}"

    def c4_altered_file(self):
        n_obj = len(self.objects()); gens = self.gens(); self.config(alter="a.bin")
        ok, log, w, commit = self.engine("sims_smoke")
        assert not ok, "a run with an altered file was accepted"
        assert len(self.objects()) == n_obj, "something was uploaded"
        assert self.gens() == gens, "generations.json on main changed"
        st = self.status(); assert st["state"] == "failed" and "a.bin" in (st["failure"] or ""), f"status: {st}"

    def c5_never_overwrite(self):
        sys.path.insert(0, os.path.join(SRC, "tools/sims")); os.environ.update({k: self.env[k] for k in ("R2_ENDPOINT", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET", "R2_WAIT_SCALE")})
        import hashlib, r2
        r2._client = None; r2.BUCKET = BUCKET
        key = "sims/test/2026-01-01-v1/x.bin"; old = b"old bytes" * 100
        self.s3.put_object(Bucket=BUCKET, Key=key, Body=old, Metadata={"sha256": hashlib.sha256(old).hexdigest()})
        p = os.path.join(self.tmp, "new.bin"); new = b"new bytes" * 100; open(p, "wb").write(new)
        try:
            r2.put(p, key, hashlib.sha256(new).hexdigest(), len(new)); raise AssertionError("other bytes were accepted at an existing key")
        except r2.R2Error as ex:
            assert "never overwritten" in str(ex), str(ex)
        assert self.s3.get_object(Bucket=BUCKET, Key=key)["Body"].read() == old, "the object changed"
        open(p, "wb").write(old)
        assert r2.put(p, key, hashlib.sha256(old).hexdigest(), len(old)) == "already stored", "the same bytes were not skipped"
        assert r2.head(key) == (len(old), hashlib.sha256(old).hexdigest()) and r2.head("sims/test/none") is None

    def c6_checks_failed(self):
        n_obj = len(self.objects()); self.config()
        ok, log, w, commit = self.engine("sims_smoke", env={"SIMS_SMOKE_FAIL": "1"})
        assert not ok, "a run whose checks failed was accepted"
        assert len(self.objects()) == n_obj, "something was uploaded"
        st = self.status(); assert st["state"] == "failed" and "checks_passed" in (st["failure"] or ""), f"status: {st}"

    def c7_collect(self):
        run, _, v = self.runs["c1"]
        objs = self.objects(f"sims/sims_smoke/{run}/"); e0 = next(q for q in self.gens() if q.get("run") == run)
        i0 = self.main_json(f"public/data/sims/sims_smoke/{run}/index-sims_smoke.json"); pushes = self.counter(); self.config()
        ok, log, w, commit = self.engine("sims_smoke", "--collect", str(v), "--shard", "1")
        assert ok, "collect failed: " + log[-2000:]
        assert self.counter() == pushes, "collect mode pushed a notebook"
        assert self.objects(f"sims/sims_smoke/{run}/") == objs and log.count("already stored") == 2, "objects not skipped as already stored"
        e1 = [q for q in self.gens() if q.get("run") == run]; assert len(e1) == 1, f"{len(e1)} entries for {run}"
        drop = lambda d: {k: x for k, x in d.items() if k != "collected"}
        assert drop(e1[0]) == drop(e0), f"entry differs: {drop(e1[0])} vs {drop(e0)}"
        i1 = self.main_json(f"public/data/sims/sims_smoke/{run}/index-sims_smoke.json"); assert drop(i1) == drop(i0), "index differs"

    def c8_status_errors(self):
        self.config(status=["error", "error", "running", "complete"])
        ok, log, w, commit = self.engine("sims_smoke"); assert ok, "the run failed: " + log[-2000:]
        assert self.status()["state"] == "saved"

    def c9_long_queue(self):
        self.config(status=["queued"] * 15 + ["running", "complete"])
        ok, log, w, commit = self.engine("sims_smoke", "--timeout", "2"); assert ok, "the run failed: " + log[-2000:]
        st = self.status(); assert st["state"] == "saved" and st["queue_s"] is not None and st["queue_s"] >= 2, f"status: {st}"

    def c10_main_moves(self):
        other = os.path.join(self.tmp, "other")
        hook = (f"rm -rf {other} && git clone -q {self.origin} {other} && echo 'line from another session' >> {other}/notes/sims/engine/state.md && "
                f"git -C {other} -c user.name=other -c user.email=o@example.invalid commit -qam 'another session' && git -C {other} push -q origin HEAD:main")
        self.config(status=["running", "complete"], hook=hook)
        ok, log, w, commit = self.engine("sims_smoke"); assert ok, "the run failed: " + log[-2000:]
        theirs = sh("git", "-C", other, "rev-parse", "HEAD").stdout.strip()
        assert sh("git", "--git-dir", self.origin, "merge-base", "--is-ancestor", theirs, "main", check=False).returncode == 0, "the other commit was lost"
        assert "line from another session" in self.main_file("notes/sims/engine/state.md"), "the other session's line is gone"
        run = f"{self.today()}-v{self.counter()}"; assert any(q.get("run") == run for q in self.gens()), "the run was not landed"

    def c11_repo_store(self):
        self.config()
        ok, log, w, commit = self.engine("barton"); assert ok, "barton failed: " + log[-3000:]
        d = self.today()
        tree = sh("git", "--git-dir", self.origin, "ls-tree", "-r", "--name-only", "main", f"public/data/sims/barton/{d}/").stdout.split()
        assert f"public/data/sims/barton/{d}/barton.bin" in tree and f"public/data/sims/barton/{d}/index-barton.json" in tree, f"tree: {tree}"
        e = [q for q in self.gens() if q["sim"] == "barton" and q["date"] == d and q["commit"] == commit]
        assert len(e) == 1 and "run" not in e[0] and "barton.bin" in e[0]["files"], f"entry: {e}"

    def c12_verify_live(self):
        # the status file describes the newest run; check that one (an older run is checked too, but its status is left alone)
        run = self.status()["run"] or self.runs["c1"][0]
        commit = next(q["commit"] for q in self.gens() if q.get("run") == run)
        site = self.clone("site")
        vl = lambda: sh(PY, "tools/sims/verify_live.py", "sims_smoke", commit, "--site", self.site, "--run", run, "--timeout", "10", cwd=site, env=self.env, check=False)
        r = vl(); assert r.returncode == 0, "verify_live failed on a good run: " + (r.stdout + r.stderr)[-1500:]
        assert self.status()["state"] == "live_ok", f"status after a good check: {self.status()['state']}"
        key = f"sims/sims_smoke/{run}/a.bin"; o = self.s3.head_object(Bucket=BUCKET, Key=key)
        self.s3.put_object(Bucket=BUCKET, Key=key, Body=b"x" * o["ContentLength"], Metadata=o.get("Metadata") or {})
        sh("git", "pull", "-q", cwd=site)
        r = vl(); assert r.returncode != 0, "verify_live passed with a replaced object"
        assert "a.bin" in (r.stdout + r.stderr), "the failure does not name the file"
        st = self.status(); assert st["state"] == "failed" and "a.bin" in (st["failure"] or ""), f"status after a failed check: {st}"

CASES = ["c1_r2_one_shard", "c2_three_shards", "c3_same_day_rerun", "c4_altered_file", "c5_never_overwrite", "c6_checks_failed",
         "c7_collect", "c8_status_errors", "c9_long_queue", "c10_main_moves", "c11_repo_store", "c12_verify_live"]

def main():
    pick = {int(x) for x in sys.argv[1:]} or set(range(1, 13))
    t = T(); passed = failed = 0
    try:
        t.setup()
        for i, name in enumerate(CASES, start=1):
            if i not in pick and not (name == "c1_r2_one_shard" and pick & {3, 7, 12}): continue
            t0 = time.time()
            try:
                getattr(t, name)(); print(f"PASS {name} ({round(time.time() - t0, 1)} s)", flush=True); passed += 1
            except Exception as ex:
                print(f"FAIL {name}: {ex}", flush=True); failed += 1
                if os.environ.get("TEST_TRACE"): traceback.print_exc()
    finally:
        t.teardown()
    print(f"{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 and passed else 1)

if __name__ == "__main__":
    main()
