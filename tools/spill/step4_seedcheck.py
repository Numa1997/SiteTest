"""Step 4, Part 1 of instruction "step4-seed-fix-gpu-smoke" (21 Nov 2026): the head's seed alone, no time stepping. Kaggle CPU only.
Logs: the volume of particles in the cells inside the head over dx^3 (each cell, and averaged per layer of cells), the top layer's
particle count and volume, V_head (particles) against the glass's volume between FILL and FILL + HEAD0, and m_head0. Also the same with
no vertical jitter, and the stout's interior cell volume, for comparison. Writes OUTDIR/step4/seedcheck.json.
Marks: abs(V_cell / dx^3 - 1) < 1e-3 in interior foam cells; abs(V_head / V_glass - 1) < 1e-6."""
import json, math, os, sys
import numpy as np
OUT = sys.argv[1] if len(sys.argv) > 1 else "/kaggle/working"; VOUT = os.path.join(OUT, "step4"); os.makedirs(VOUT, exist_ok=True)
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "fig12", "kaggle"))
import stout_jax as SJ  # noqa: E402
js = open(os.path.join(ROOT, "public", "scripts", "guinness-glass.js")).read()
R = np.array([float(v) for v in js.split("R: [")[1].split("]")[0].split(",")])
DZP, FILL, DX = 0.0005, 0.125, float(os.environ.get("DX", "0.0015")); F16 = (0.155, 0.062, -0.030)
G = SJ.Geometry(R, DZP, FILL, DX, body=F16, top=0.08, lip=0.00125)
hl = DX / 2; n_full = int(math.floor(SJ.HEAD0 / hl + 1e-9)); t_top = SJ.HEAD0 - n_full * hl


def cells(P, vol, zlo, zhi, margin=2.0):
    """Particle volume per grid cell over dx^3, for cells whose z range lies inside [zlo, zhi] and whose centre is more than margin dx
    inside the glass's wall at that height."""
    i = np.floor((P[:, 0] - G.x0) / DX).astype(int); j = np.floor((P[:, 1] - G.y0) / DX).astype(int); k = np.floor((P[:, 2] - G.z0) / DX).astype(int)
    V = np.zeros((G.nx, G.ny, G.nz)); np.add.at(V, (i, j, k), vol); V /= DX ** 3
    Xc, Yc, Zc = np.meshgrid(G.xc, G.yc, G.zc, indexing="ij")
    inner = (Zc - 0.5 * DX >= zlo) & (Zc + 0.5 * DX <= zhi) & (np.hypot(Xc, Yc) < G.Rz(Zc) - margin * DX)
    v = V[inner]; layers = sorted(set(np.nonzero(inner)[2].tolist()))
    lay = [float(V[:, :, kk][inner[:, :, kk]].mean()) for kk in layers]
    return dict(n_cells=int(inner.sum()), mean=float(v.mean()), min=float(v.min()), max=float(v.max()), std=float(v.std()),
                max_abs_dev=float(np.abs(v - 1).max()), layer_means=lay, layer_max_abs_dev=float(np.max(np.abs(np.array(lay) - 1))))


out = dict(dx=DX, HEAD0=SJ.HEAD0, hl=hl, n_full=n_full, t_top=t_top, fill=FILL)
for jz in (0.3, 0.0):
    try:
        P, Vg, vol = SJ.seed_head(G, 2, 2, jitter_z=jz)
        top = np.isclose(vol, hl * hl * t_top) if t_top > 0 else np.zeros(len(vol), bool)
        r = dict(N_head=len(P), top_count=int(top.sum()), top_volume_m3=float(vol[top].sum()), V_head_particles_m3=float(vol.sum()),
                 V_glass_m3=Vg, V_ratio=float(vol.sum() / Vg), m_head0_kg=float(SJ.RHO_HEAD * vol.sum()),
                 interior=cells(P, vol, FILL, FILL + n_full * hl))
        r["marks"] = dict(V_cell_within_1e3_each_cell=r["interior"]["max_abs_dev"] < 1e-3, V_cell_within_1e3_layer_means=r["interior"]["layer_max_abs_dev"] < 1e-3,
                          V_head_within_1e6=abs(r["V_ratio"] - 1) < 1e-6)
        out[f"head_jitter_{jz:g}"] = r; print("head", jz, json.dumps({k: v for k, v in r.items() if k != "interior"}), json.dumps({k: v for k, v in r["interior"].items() if k != "layer_means"}), flush=True)
    except Exception as ex:
        out[f"head_jitter_{jz:g}"] = dict(error=repr(ex)); print("FAILED", jz, repr(ex), flush=True)
try:   # the stout, as Steps 1-3 seed it (unchanged): uniform particle volume V / N
    Ps = SJ.seed_particles(G, 2, 1); Vs = SJ.glass_volume(G.R, G.dzp, G.fill); vs = np.full(len(Ps), Vs / len(Ps))
    hz_s = FILL / round(FILL / hl)
    out["stout"] = dict(N=len(Ps), V_glass_m3=Vs, Vp_m3=Vs / len(Ps), Vp_over_hl2_hz=float(Vs / len(Ps) / (hl * hl * hz_s)), hz_m=hz_s,
                        layering_ratio_2hz_over_dx=2 * hz_s / DX, interior=cells(Ps, vs, 0.01, FILL - 0.005))
    print("stout", json.dumps({k: v for k, v in out["stout"].items() if k != "interior"}), json.dumps({k: v for k, v in out["stout"]["interior"].items() if k != "layer_means"}), flush=True)
except Exception as ex:
    out["stout"] = dict(error=repr(ex)); print("FAILED stout", repr(ex), flush=True)
json.dump(out, open(os.path.join(VOUT, "seedcheck.json"), "w"), indent=1)
print("done", flush=True)
