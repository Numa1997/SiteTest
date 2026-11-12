"""Turns Kaggle's run files (runs/e{i}_v{j}_r{k}.json + index.json from the notebook full.ipynb) into the files the
website serves: one binary file per run and one index.

Usage: python3 to_site.py <kaggle-output-folder> <project-data-folder> <generation-date> [notebook-ref] [version] [commit] [--phase]

Every generation of data lives in its own folder named by the date Kaggle computed it, <project-data-folder>/<YYYY-MM-DD>/,
with its own index.json; <project-data-folder>/generations.json lists the generations (docs/kaggle-pipeline.md, "Storage").
The website keeps the amplitude only (the phase picture doubles the size and no number on the page comes from it); --phase
keeps it too. The full output, phase included, stays with the Kaggle notebook as its output.

Run file e{i}_v{j}_r{k}.bin, little-endian:
  bytes 0-3   'SPH1'
  bytes 4-7   uint32 H, length of the header
  next H      UTF-8 JSON header: E, V0, R, i, j, k, n (frames), out (points per side), steps, dt, wall (s on Kaggle),
              device, curves [[t, norm, behind, ahead, sigma_y] per frame]
  the rest    one zlib stream; inflated it is n*out*out bytes of |psi| levels (followed, with --phase, by n*out*out bytes
              of arg-psi levels), frame-major, then x-major, then y (index f*out*out + x*out + y); header field "phase" says which
index.json: the grid (Es, Vs, Rs), the numerical constants, and per run its file, size, SHA-256 and end probabilities.
Standard library only, plus the Kaggle files."""
import base64, hashlib, json, os, struct, sys, zlib
args = [a for a in sys.argv[1:] if not a.startswith("--")]; PHASE = "--phase" in sys.argv
src, proj, date = args[0], args[1], args[2]
ref = args[3] if len(args) > 3 else ""
ver = args[4] if len(args) > 4 else ""
commit = args[5] if len(args) > 5 else ""
dst = os.path.join(proj, date)
os.makedirs(dst, exist_ok=True)
idx = json.load(open(os.path.join(src, "index.json")))
out_runs = []
for r in idx["runs"]:
    d = json.load(open(os.path.join(src, "runs", r["file"])))
    amp = zlib.decompress(base64.b64decode(d["amp"])); ph = zlib.decompress(base64.b64decode(d["ph"]))
    n, o = d["n"], idx["out"]
    assert len(amp) == len(ph) == n * o * o, r["file"]
    head = dict(E=d["E"], V0=d["V0"], R=d["R"], i=d["i"], j=d["j"], k=d["k"], n=n, out=o, steps=d["steps"], dt=idx["dt"],
                wall=d["wall"], device=d["device"], phase=PHASE, curves=d["c"])
    hb = json.dumps(head, separators=(",", ":")).encode()
    body = b"SPH1" + struct.pack("<I", len(hb)) + hb + zlib.compress(amp + ph if PHASE else amp, 9)
    name = r["file"].replace(".json", ".bin")
    open(os.path.join(dst, name), "wb").write(body)
    out_runs.append(dict(file=name, i=d["i"], j=d["j"], k=d["k"], E=d["E"], V0=d["V0"], R=d["R"], bytes=len(body),
                         sha256=hashlib.sha256(body).hexdigest(), behind=r["behind"], ahead=r["ahead"], norm_end=r["norm_end"],
                         steps=d["steps"], wall=d["wall"]))
meta = {k: idx[k] for k in ("Es", "Vs", "Rs", "N", "L", "dt", "out", "nframes", "sigma0", "device", "gpus", "sweep_s")}
meta.update(generated=date, x0=-14.0, travel=30.0, units="hbar = m = 1, lengths in the grid unit a", phase=PHASE,
            source=dict(kaggle=ref, version=ver, commit=commit, solver="tools/kaggle/schrodinger-sphere/solver.py",
                        kaggle_output="the notebook's output, version " + ver + ": runs/e{i}_v{j}_r{k}.json with phase"),
            runs=out_runs)
json.dump(meta, open(os.path.join(dst, "index.json"), "w"), separators=(",", ":"))
gp = os.path.join(proj, "generations.json")
gens = json.load(open(gp)) if os.path.exists(gp) else []
gens = [g for g in gens if g["date"] != date] + [dict(date=date, index=date + "/index.json", runs=len(out_runs), kaggle=ref, version=ver, commit=commit)]
json.dump(sorted(gens, key=lambda g: g["date"]), open(gp, "w"), indent=1)
tot = sum(r["bytes"] for r in out_runs)
print(f"{len(out_runs)} runs, {tot/1e6:.1f} MB, largest {max(r['bytes'] for r in out_runs)/1e3:.0f} kB")
