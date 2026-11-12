"""Turns Kaggle's run files (runs/e{i}_v{j}_r{k}.json + index.json from the notebook full.ipynb) into the files the
website serves: one binary file per run and one index.

Usage: python3 to_site.py <kaggle-output-folder> <site-data-folder> [notebook-ref] [version] [commit]

Run file e{i}_v{j}_r{k}.bin, little-endian:
  bytes 0-3   'SPH1'
  bytes 4-7   uint32 H, length of the header
  next H      UTF-8 JSON header: E, V0, R, i, j, k, n (frames), out (points per side), steps, dt, wall (s on Kaggle),
              device, curves [[t, norm, behind, ahead, sigma_y] per frame]
  the rest    one zlib stream; inflated it is n*out*out bytes of |psi| levels followed by n*out*out bytes of arg-psi
              levels, frame-major, then x-major, then y (index f*out*out + x*out + y)
index.json: the grid (Es, Vs, Rs), the numerical constants, and per run its file, size, SHA-256 and end probabilities.
Standard library only, plus the Kaggle files."""
import base64, hashlib, json, os, struct, sys, zlib
src, dst = sys.argv[1], sys.argv[2]
ref = sys.argv[3] if len(sys.argv) > 3 else ""
ver = sys.argv[4] if len(sys.argv) > 4 else ""
commit = sys.argv[5] if len(sys.argv) > 5 else ""
os.makedirs(dst, exist_ok=True)
idx = json.load(open(os.path.join(src, "index.json")))
out_runs = []
for r in idx["runs"]:
    d = json.load(open(os.path.join(src, "runs", r["file"])))
    amp = zlib.decompress(base64.b64decode(d["amp"])); ph = zlib.decompress(base64.b64decode(d["ph"]))
    n, o = d["n"], idx["out"]
    assert len(amp) == len(ph) == n * o * o, r["file"]
    head = dict(E=d["E"], V0=d["V0"], R=d["R"], i=d["i"], j=d["j"], k=d["k"], n=n, out=o, steps=d["steps"], dt=idx["dt"],
                wall=d["wall"], device=d["device"], curves=d["c"])
    hb = json.dumps(head, separators=(",", ":")).encode()
    body = b"SPH1" + struct.pack("<I", len(hb)) + hb + zlib.compress(amp + ph, 9)
    name = r["file"].replace(".json", ".bin")
    open(os.path.join(dst, name), "wb").write(body)
    out_runs.append(dict(file=name, i=d["i"], j=d["j"], k=d["k"], E=d["E"], V0=d["V0"], R=d["R"], bytes=len(body),
                         sha256=hashlib.sha256(body).hexdigest(), behind=r["behind"], ahead=r["ahead"], norm_end=r["norm_end"],
                         steps=d["steps"], wall=d["wall"]))
meta = {k: idx[k] for k in ("Es", "Vs", "Rs", "N", "L", "dt", "out", "nframes", "sigma0", "device", "gpus", "sweep_s")}
meta.update(x0=-14.0, travel=30.0, units="hbar = m = 1, lengths in the grid unit a",
            source=dict(kaggle=ref, version=ver, commit=commit, solver="tools/kaggle/schrodinger-sphere/solver.py"),
            runs=out_runs)
json.dump(meta, open(os.path.join(dst, "index.json"), "w"), separators=(",", ":"))
tot = sum(r["bytes"] for r in out_runs)
print(f"{len(out_runs)} runs, {tot/1e6:.1f} MB, largest {max(r['bytes'] for r in out_runs)/1e3:.0f} kB")
