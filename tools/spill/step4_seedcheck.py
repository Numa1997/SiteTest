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


out = dict(dx=DX, HEAD0=SJ.HEAD0, hl=hl, n_full=n_full, t_top=t_top, fill=FILL, version="v3: option 2 (wall-ring volume), no vertical jitter")
zz = np.linspace(FILL, FILL + SJ.HEAD0, 200001); V_glass_indep = float(np.trapezoid(np.pi * G.Rz(zz) ** 2, zz)) if hasattr(np, "trapezoid") else float(np.trapz(np.pi * G.Rz(zz) ** 2, zz))
for jz in (0.0, 0.3):   # 0.0 = the seed as used (marks); 0.3 = with vertical jitter, for comparison only
    try:
        P, Vg, vol, info = SJ.seed_head(G, 2, 2, jitter_z=jz)
        top = np.isclose(vol, hl * hl * t_top, rtol=1e-6, atol=0.0) if t_top > 0 else np.zeros(len(vol), bool)
        facs = [i["ring_factor"] for i in info]
        r = dict(N_head=len(P), top_layer=info[-1], top_count_unscaled=int(top.sum()), V_head_particles_m3=float(vol.sum()), V_glass_seed_m3=Vg,
                 V_glass_independent_m3=V_glass_indep, V_ratio=float(vol.sum() / V_glass_indep), m_head0_kg=float(SJ.RHO_HEAD * vol.sum()),
                 ring_factor_min=float(min(facs)), ring_factor_max=float(max(facs)), ring_count_per_layer=[i["n_ring"] for i in info],
                 layers=info, interior=cells(P, vol, FILL, FILL + n_full * hl))
        r["marks"] = dict(V_cell_within_1e3_interior=r["interior"]["max_abs_dev"] < 1e-3, ring_factor_in_1_1p5=bool(1.0 <= min(facs) and max(facs) <= 1.5),
                          V_head_within_1e4=abs(r["V_ratio"] - 1) < 1e-4)
        r["marks_all"] = all(r["marks"].values())
        out[f"head_jitter_{jz:g}"] = r
        print("head", jz, json.dumps({k: v for k, v in r.items() if k not in ("interior", "layers", "ring_count_per_layer")}),
              json.dumps({k: v for k, v in r["interior"].items() if k != "layer_means"}), flush=True)
    except Exception as ex:
        out[f"head_jitter_{jz:g}"] = dict(error=repr(ex)); print("FAILED", jz, repr(ex), flush=True)
out["marks"] = out.get("head_jitter_0", {}).get("marks"); out["marks_all"] = out.get("head_jitter_0", {}).get("marks_all")
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
