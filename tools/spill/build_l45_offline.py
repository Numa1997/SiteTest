"""Build the Kaggle notebook text for test 4.5 Part C (step4-slosh-head-offline): internet OFF, code embedded (zlib + base64)
at a pinned commit, env STEP45=1 SUBRUN=full DX=0.0015. Checks every embedded file byte-identical to `git show COMMIT:file`.
Usage (repo root): python3 tools/spill/build_l45_offline.py OUT.py [COMMIT=5acb718]"""
import base64, hashlib, subprocess, sys, zlib
out = sys.argv[1]; C = sys.argv[2] if len(sys.argv) > 2 else "5acb718"
files = ["tools/fig12/kaggle/stout_jax.py", "tools/spill/rest_variants.py", "tools/fig12/kaggle/run_b.py", "public/scripts/guinness-glass.js"]
raw = {f: subprocess.check_output(["git", "show", f"{C}:{f}"]) for f in files}
emb = {f: base64.b64encode(zlib.compress(b, 9)).decode() for f, b in raw.items()}
full = subprocess.check_output(["git", "rev-parse", C]).decode().strip()
src = f'''# step4-slosh-head-offline: test 4.5 Part C (free slosh, EVP head, wall-friction fix 8375a2f). Internet OFF, no downloads, no pip.
# Code embedded at commit {full} (zlib + base64). Env: STEP45=1, SUBRUN=full, DX=0.0015.
import os, sys, zlib, base64, hashlib, subprocess, time
FILES = {emb!r}
ROOT = "/kaggle/working/repo"
for p, b in FILES.items():
    fp = os.path.join(ROOT, p); os.makedirs(os.path.dirname(fp), exist_ok=True)
    d = zlib.decompress(base64.b64decode(b)); open(fp, "wb").write(d)
    print(p, len(d), hashlib.sha256(d).hexdigest(), flush=True)
env = dict(os.environ, STEP45="1", SUBRUN="full", DX="0.0015")
os.makedirs("/kaggle/working/step4", exist_ok=True)
print("start", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), "UTC", flush=True)
log = open("/kaggle/working/step4/slosh_head.log", "w")
pr = subprocess.Popen([sys.executable, os.path.join(ROOT, "tools/spill/rest_variants.py"), "/kaggle/working"], cwd=ROOT, env=env,
                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
for line in pr.stdout:
    log.write(line); log.flush(); print(line, end="", flush=True)
rc = pr.wait(); log.close()
subprocess.run(["rm", "-rf", ROOT])
print("end", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), "UTC rc", rc, flush=True)
if rc: raise SystemExit(rc)
'''
back = eval(src.split("FILES = ", 1)[1].split("\nROOT =")[0])
for f in files:
    d = zlib.decompress(base64.b64decode(back[f]))
    assert d == raw[f], f
    print(f, "byte-identical", len(d), hashlib.sha256(d).hexdigest()[:16])
open(out, "w").write(src); print(out, len(src.encode()), "bytes")
