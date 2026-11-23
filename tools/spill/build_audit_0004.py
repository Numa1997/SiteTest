"""Build the Kaggle CPU notebook text for instruction 0004 (step4-energy-audit-cpu): internet OFF, GPU OFF, code embedded (zlib +
base64) at a pinned commit, plus stout_jax.py at 5acb718 as stout_jax_5acb718.py for the default-path identity check. Checks every
embedded file byte-identical to git. Usage: python3 tools/spill/build_audit_0004.py OUT.py COMMIT SUBRUN [ONLY]"""
import base64, subprocess, sys, zlib
out, C, sub = sys.argv[1], sys.argv[2], sys.argv[3]; only = sys.argv[4] if len(sys.argv) > 4 else "rot,slab,ident,slosh"
files = {p: (C, p) for p in ["tools/fig12/kaggle/stout_jax.py", "tools/spill/audit_0004.py", "tools/spill/step4_slab.py", "public/scripts/guinness-glass.js"]}
files["tools/fig12/kaggle/stout_jax_5acb718.py"] = ("5acb718", "tools/fig12/kaggle/stout_jax.py")
raw = {p: subprocess.check_output(["git", "show", f"{c}:{f}"]) for p, (c, f) in files.items()}
emb = {p: base64.b64encode(zlib.compress(b, 9)).decode() for p, b in raw.items()}
full = subprocess.check_output(["git", "rev-parse", C]).decode().strip()
src = f'''# step4-energy-audit-cpu: instruction 0004 (energy-closure audit of test 4.5), measurement only. CPU, internet OFF, no pip.
# Code embedded at commit {full} (zlib + base64); stout_jax_5acb718.py = stout_jax.py at 5acb718. SUBRUN={sub}, ONLY={only}.
import os, sys, zlib, base64, hashlib, subprocess, time
FILES = {emb!r}
ROOT = "/kaggle/working/repo"
for p, b in FILES.items():
    fp = os.path.join(ROOT, p); os.makedirs(os.path.dirname(fp), exist_ok=True)
    d = zlib.decompress(base64.b64decode(b)); open(fp, "wb").write(d); print(p, len(d), hashlib.sha256(d).hexdigest(), flush=True)
env = dict(os.environ, SUBRUN="{sub}", ONLY="{only}", DX="0.003", IDENT_DX="0.0015", JAX_PLATFORMS="cpu")
pr = subprocess.Popen([sys.executable, os.path.join(ROOT, "tools/spill/audit_0004.py"), "/kaggle/working"], cwd=ROOT, env=env,
                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
for line in pr.stdout: print(line, end="", flush=True)
rc = pr.wait(); subprocess.run(["rm", "-rf", ROOT]); print("end rc", rc, flush=True)
if rc: raise SystemExit(rc)
'''
back = eval(src.split("FILES = ", 1)[1].split("\nROOT =")[0])
for p in files:
    assert zlib.decompress(base64.b64decode(back[p])) == raw[p], p
    print(p, "byte-identical", len(raw[p]))
open(out, "w").write(src); print(out, len(src.encode()), "bytes")
