"""Fig. 15 correction, walls on the GPU: the exact rebuild of the wall runs listed in walls_left.json (exact_wall_jax.ExactJ),
written as RT3C files in the stored layout at the stored frame times, exactly as rebuild_walls_all.py does on the CPU.
One thread per GPU; one progress line per run in progress.log; at the end a tar of the files and runs.jsonl.
Globals a loader may set: OUTROOT, CPU (test without a GPU), LIMIT, JOBS."""
import os, sys, json, time, hashlib, threading, queue, tarfile, traceback, subprocess
import numpy as np
T0 = time.time()
ROOT = globals().get("OUTROOT", "/kaggle/working"); os.makedirs(ROOT, exist_ok=True)
LOG = open(ROOT + "/progress.log", "a")
def say(*a):
    s = f"[{time.time()-T0:7.1f} s] " + " ".join(str(x) for x in a); print(s, flush=True); LOG.write(s + "\n"); LOG.flush()
sys.path.insert(0, ".")
if not globals().get("CPU"):
    r = subprocess.run([sys.executable, "-c", "import jax; print(jax.default_backend())"], capture_output=True, text=True)
    if (r.stdout.strip().splitlines() or ["none"])[-1] != "gpu":
        say("installing jax[cuda12]"); subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "jax[cuda12]"], check=True)
import jax
if not globals().get("CPU"): assert any(d.platform == "gpu" for d in jax.devices()), "NO GPU: stopping"
import exact_wall as ew, exact_wall_jax as ej, rebuild_wall as rw


def layout(Nx):
    x = (np.arange(Nx) - Nx // 2) * 0.5; inner = (Nx // 2 - max(4, Nx // 10)) * 0.5
    return x, int(np.searchsorted(x, -inner)), int(np.searchsorted(x, inner))


def header(j):
    sp = j["spec"]; x, i0, i1 = layout(sp["Nx"])
    return dict(spec=sp, group=j["group"], shape=sp["shape"], E=sp["E"], V0=sp["V0"], D=sp["D"], P=sp["P"], N=sp["N"], size=sp["R"],
                bias=sp["bias"], sigma_x=sp["sx"], sigma_perp=sp["sp"], x0=ew.x0_of(sp), centres=ew.centres(sp),
                extent=[ew.centres(sp)[0] - sp["D"] / 2, ew.centres(sp)[-1] + sp["D"] / 2], n=j["n"], nxs=i1 - i0, nr=64,
                x_first=float(x[i0]), step=0.5, prof_x_first=float(x[0]), prof_nx=sp["Nx"], steps=j["steps"], dt=0.01, t_end=j["t_end"],
                frame_dt=j["frame_dt"], start_in_barrier=j["start_in_barrier"], start_in_border=None, box=[sp["Nx"], 128, 128])


def one(j, dev):
    t0 = time.time(); h = header(j); sp = h["spec"]
    xs = h["prof_x_first"] + np.arange(h["prof_nx"]) * 0.5; t = np.arange(h["n"]) * h["frame_dt"]
    X = ej.ExactJ(sp, xs)
    chi = np.asarray(X.chi(t)).T
    i0 = int(round((h["x_first"] - xs[0]) / 0.5)); nxs = h["nxs"]
    Hy = ew.h_free(np.arange(64) * 0.5, t, sp["sp"]).T
    slab = chi[:, i0:i0 + nxs, None] * Hy[:, None, :] * Hy[:, 0, None, None]
    prof = np.abs(chi)**2
    half = 0.5 * h["prof_nx"] * 0.5
    R, lo, hi = X.regions_and_tails(t, -half, half)
    curves = [t, 1 - lo - hi, R["left"] - lo, R["right"] - hi] + ([R["well"]] if sp["N"] > 1 else [])
    names = ["t", "norm", "left", "right"] + (["well"] if sp["N"] > 1 else [])
    head = dict(method="exact: psi = chi(x,t) h(y,t) h(z,t); chi by superposition of the stationary scattering states "
                "(tools/kaggle/resonant-tunnelling/correction/exact_wall.py, exact_wall_jax.py on the GPU); no time grid, no barrier sampling",
                parent=dict(file=j["file"], sha256=j["sha256"]), T_ref=X.T_inf, T_spectrum_weighted=X.T_packet_weights,
                carried=X.carried, closure_max=float(np.abs(R["closure"] - 1).max()),
                regions="left, right, norm: inside the box |x| <= box half-length; left_line, right_line: whole line",
                extra_curves=dict(left_line=np.round(R["left"], 7).tolist(), right_line=np.round(R["right"], 7).tolist()),
                device=str(dev) + " (exact)", wall=None, has_1d=True, sep_check_max=0.0, T_1d_splitstep=None, R_1d_splitstep=None,
                T_packet_exact=X.T_packet_weights)
    blob, A, P, peaks = rw.write(h, slab, prof, prof, np.array(curves).T, names, head)
    return blob, dict(file=j["file"], spec=sp, T_ref=X.T_inf, T_w=X.T_packet_weights, carried=X.carried,
                      closure_max=head["closure_max"], sha256_rebuilt=hashlib.sha256(blob).hexdigest(), bytes=len(blob),
                      s=round(time.time() - t0, 2), device=str(dev))


if globals().get("RUN"):
    J = json.load(open(globals().get("JOBS", "walls_left.json")))
    if globals().get("LIMIT"): J = J[:LIMIT]
    OUTD = ROOT + "/walls"; os.makedirs(OUTD, exist_ok=True)
    Q = queue.Queue(); [Q.put(j) for j in J]; LOCK = threading.Lock(); CNT = [0]; ERR = []
    JL = open(OUTD + "/runs.jsonl", "a")
    say("devices", jax.devices(), len(J), "walls")
    def worker(dev):
        with jax.default_device(dev):
            while True:
                try: j = Q.get_nowait()
                except queue.Empty: return
                try:
                    blob, rec = one(j, dev); open(f"{OUTD}/{j['file']}", "wb").write(blob)
                    with LOCK:
                        CNT[0] += 1; JL.write(json.dumps(rec) + "\n"); JL.flush()
                        say(f"{CNT[0]}/{len(J)} {j['file']} {dev}: T_ref {rec['T_ref']:.6f} closure {rec['closure_max']:.1e} {rec['s']} s")
                except Exception as e:
                    with LOCK: ERR.append(dict(file=j["file"], error=repr(e)[:400]))
                    say("FAILED", j["file"], repr(e)[:300]); say(traceback.format_exc()[-600:])
    devs = [d for d in jax.devices() if d.platform == "gpu"] or [jax.devices()[0]]
    th = [threading.Thread(target=worker, args=(d,)) for d in devs]; [x.start() for x in th]; [x.join() for x in th]
    JL.close()
    with tarfile.open(OUTD + "/walls.tar", "w") as tf:
        for f in sorted(os.listdir(OUTD)):
            if f.endswith(".bin"): tf.add(f"{OUTD}/{f}", arcname=f)
    for f in os.listdir(OUTD):
        if f.endswith(".bin"): os.remove(f"{OUTD}/{f}")
    json.dump(dict(done=CNT[0], failed=ERR, total_s=round(time.time() - T0, 1)), open(OUTD + "/summary.json", "w"))
    say(f"done {CNT[0]}, failed {len(ERR)}, tar {os.path.getsize(OUTD + '/walls.tar')/1e6:.0f} MB")
