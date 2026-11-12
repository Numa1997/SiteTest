"""Packs Kaggle's stored cuts into the website's files for the 3D view by rotational symmetry (no new computation).

The packet flies along x through the centre of the sphere, so psi does not depend on the angle around the x axis: the whole
3D field is psi(x, rho, t) with rho = sqrt(y^2 + z^2). Kaggle stored the cut z = 0 (|psi| and arg psi, 128 x 128 points,
0.5 a apart); its half y >= 0 is psi(x, rho) for rho = 0 ... 31.5 a. This script keeps that half-plane, as Kaggle stored it.

Usage: python3 to_site_axisym.py <kaggle-output-folder> <project-data-folder> <generation-date> [notebook-ref] [version] [commit]
Run file e{i}_v{j}_r{k}.bin (little-endian): 'SPHC', uint32 header length H, H bytes JSON header (E, V0, R, i, j, k, n,
nx, nr, x0, step, steps, dt, wall, device, curves [[t, norm, behind, ahead, sigma_y] per frame]), then one zlib stream:
n*nx*nr bytes of |psi| levels (0..255 of the first frame's peak in the plane) then as many arg-psi levels (0..255 for
-pi..pi, 0 where |psi| < 3 levels); index f*nx*nr + i*nr + r, x = x0 + i*step, rho = r*step."""
import base64, hashlib, json, os, sys, zlib, struct
import numpy as np
src, proj, date = sys.argv[1], sys.argv[2], sys.argv[3]
ref = sys.argv[4] if len(sys.argv) > 4 else ""; ver = sys.argv[5] if len(sys.argv) > 5 else ""; commit = sys.argv[6] if len(sys.argv) > 6 else ""
dst = os.path.join(proj, date); os.makedirs(dst, exist_ok=True)
for f in os.listdir(dst):
    if f.endswith(".bin"): os.remove(os.path.join(dst, f))
idx = json.load(open(os.path.join(src, "index.json"))); out = idx["out"]; L = idx["L"]; step = L / out
runs = []; mirror = 0
for r in idx["runs"]:
    d = json.load(open(os.path.join(src, "runs", r["file"])))
    n = d["n"]
    amp = np.frombuffer(zlib.decompress(base64.b64decode(d["amp"])), np.uint8).reshape(n, out, out)
    ph = np.frombuffer(zlib.decompress(base64.b64decode(d["ph"])), np.uint8).reshape(n, out, out)
    # mirror check: the y < 0 half must equal the y >= 0 half (rows 63 - r against 64 + r is y = -(r + 0.5)... the grid is
    # x = (i - 64) step, so y = 0 is row 64; row 64 + r and row 64 - r are mirror images)
    a_up = amp[:, :, 65:128].astype(int); a_dn = amp[:, :, 63:0:-1].astype(int)
    mirror = max(mirror, int(np.abs(a_up - a_dn).max()))
    A = np.ascontiguousarray(amp[:, :, 64:128]); P = np.ascontiguousarray(ph[:, :, 64:128])
    head = dict(E=d["E"], V0=d["V0"], R=d["R"], i=d["i"], j=d["j"], k=d["k"], n=n, nx=out, nr=out // 2, x0=-L / 2, step=step,
                steps=d["steps"], dt=idx["dt"], wall=d["wall"], device=d["device"], curves=d["c"])
    hb = json.dumps(head, separators=(",", ":")).encode()
    body = b"SPHC" + struct.pack("<I", len(hb)) + hb + zlib.compress(A.tobytes() + P.tobytes(), 9)
    name = r["file"].replace(".json", ".bin"); open(os.path.join(dst, name), "wb").write(body)
    runs.append(dict(file=name, i=d["i"], j=d["j"], k=d["k"], E=d["E"], V0=d["V0"], R=d["R"], bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                     behind=r["behind"], ahead=r["ahead"], norm_end=r["norm_end"], steps=d["steps"], wall=d["wall"]))
meta = {k: idx[k] for k in ("Es", "Vs", "Rs", "N", "L", "dt", "nframes", "sigma0", "device", "gpus", "sweep_s")}
meta.update(generated=date, kind="axisym", x0=-14.0, travel=30.0, units="hbar = m = 1, lengths in the grid unit a",
            mirror_check=dict(largest_level_difference=mirror, what="|psi| levels of rows y and -y of every stored cut"),
            source=dict(kaggle=ref, version=ver, commit=commit, solver="tools/kaggle/schrodinger-sphere/solver.py",
                        kaggle_output="the notebook's output, version " + ver + ": runs/e{i}_v{j}_r{k}.json, the full cut z = 0 with phase"),
            runs=runs)
json.dump(meta, open(os.path.join(dst, "index.json"), "w"), separators=(",", ":"))
gp = os.path.join(proj, "generations.json"); gens = json.load(open(gp)) if os.path.exists(gp) else []
gens = [g for g in gens if g["date"] != date] + [dict(date=date, index=date + "/index.json", kind="axisym", runs=len(runs), kaggle=ref, version=ver, commit=commit)]
json.dump(sorted(gens, key=lambda g: g["date"]), open(gp, "w"), indent=1)
print(f"{len(runs)} runs, {sum(r['bytes'] for r in runs)/1e6:.1f} MB, largest {max(r['bytes'] for r in runs)/1e3:.0f} kB; mirror check: largest |psi| level difference {mirror}")
