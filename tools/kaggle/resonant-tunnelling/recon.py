"""Fig. 15, Step B3: the time-dependent wave at two barriers without a time-dependent solve.

For V >= 0 there are no bound states, and the scattering states psi_k (incident e^{ikx} from the left, k > 0) together with
those incident from the right are complete. A packet that starts wholly left of the barriers and has no k < 0 part is
    psi(x, t) = (2 pi)^-1/2 Int phi(k) psi_k(x) e^{-i k^2 t / 2} dk,     phi(k) = Fourier transform of psi(x, 0),
exactly; the neglected pieces (the start packet's tail inside the barriers, its k < 0 part) are measured and stored.
psi_k comes from the transfer matrices of tm.py. hbar = m = 1.

Writes one run file per (gap, packet, energy) and a JSON summary. File 'RTF1' (little-endian):
  'RTF1', uint32 H, H bytes JSON header (padded with spaces to an even length), then nf * nx float16 Re psi, nf * nx float16
  Im psi on the stored window, then nf * zoom_nx float16 Re psi and Im psi on the magnified stretch around the pair.
Usage: python3 recon.py OUTDIR [--quick]
"""
import json, struct, sys, os, time, hashlib
import numpy as np
from scipy.integrate import simpson
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tm import solve, psi_x, double

V0, D = 3.0, 1.0                         # the running example: height 3, width 1
GAPS = [2.343, 3.454, 6.0]               # centre-to-centre: resonant at E = 1, antiresonant at E = 1, a wider well
PACKETS = {3.0: dict(win=50.0, nf=240), 12.0: dict(win=120.0, nf=200)}
DX = 0.25
DXL = 0.05                               # spacing of the long line used for the probabilities
EGRID = [round(0.5 + 0.1 * i, 2) for i in range(21)]


def phi(k, k0, s0, x0):
    N = (2 * np.pi * s0**2) ** -0.25
    return N * np.sqrt(2) * s0 * np.exp(-s0**2 * (k - k0)**2) * np.exp(-1j * (k - k0) * x0)


def T_of_E(Es, segs):
    return np.array([abs(solve(E, segs)[0])**2 for E in Es])


def resonances(segs, Emin=0.05, Emax=3.0, n=6000):
    """Peaks of T(E) with T > 0.5: energy, peak T, full width at half maximum (bisection on both sides)."""
    Es = np.linspace(Emin, Emax, n); T = T_of_E(Es, segs); out = []
    for i in range(1, n - 1):
        if T[i] > T[i - 1] and T[i] >= T[i + 1] and T[i] > 0.5:
            # refine the peak by golden section on [Es[i-1], Es[i+1]]
            a, b = Es[i - 1], Es[i + 1]; g = (np.sqrt(5) - 1) / 2
            for _ in range(80):
                c1 = b - g * (b - a); c2 = a + g * (b - a)
                if abs(solve(c1, segs)[0]) > abs(solve(c2, segs)[0]): b = c2
                else: a = c1
            Ep = (a + b) / 2; Tp = abs(solve(Ep, segs)[0])**2
            def half(lo, hi):
                flo = abs(solve(lo, segs)[0])**2 - Tp / 2
                for _ in range(80):
                    m = (lo + hi) / 2; fm = abs(solve(m, segs)[0])**2 - Tp / 2
                    if np.sign(fm) == np.sign(flo): lo, flo = m, fm
                    else: hi = m
                return (lo + hi) / 2
            w = Es[1] - Es[0]; lo = Ep;
            while abs(solve(lo, segs)[0])**2 > Tp / 2 and lo > Emin: lo -= w
            hi = Ep
            while abs(solve(hi, segs)[0])**2 > Tp / 2 and hi < Emax + 1: hi += w
            El = half(lo, Ep); Er = half(Ep, hi)
            out.append(dict(E=Ep, T=Tp, Gamma=Er - El, tau=1 / (Er - El), El=El, Er=Er))
    return out


def run(E, s, s0, dk=0.001, quick=False):
    segs = double(V0, D, s); pk = PACKETS[s0]
    xl = -s / 2 - D / 2; xr = s / 2 + D / 2                     # outer edges of the pair
    k0 = np.sqrt(2 * E); sk = 1 / (2 * s0)
    x0 = round(xl - 6 * s0 - 2, 2)                              # start: 6 sigma0 + 2 left of the first edge
    win = pk["win"]; nf = pk["nf"]
    xv = np.arange(-win, win + DX / 2, DX)
    t_end = 1.3 * (win - x0) / k0
    dtf = max(1, round(t_end / (nf - 1) / 0.005)) * 0.005       # frame interval: a whole number of the check solver's steps
    times = dtf * np.arange(nf)
    ks = np.arange(max(k0 - 8 * sk, 0.01), k0 + 8 * sk, dk)
    ph = phi(ks, k0, s0, x0) * dk / np.sqrt(2 * np.pi)         # quadrature weights (midpoint-equivalent on a fine grid)
    # stationary states on the stored points and on a long line for the probabilities
    L = 60 * s0 + 400
    xa = np.linspace(-L, xl, int(round((xl + L) / DXL)) + 1)      # left of the pair, ending exactly on its edge
    xb = np.linspace(xr, L, int(round((L - xr) / DXL)) + 1)       # right of the pair, starting exactly on its edge
    xl_long = np.concatenate([xa, xb])
    xin = np.linspace(xl, xr, 801)                              # barriers and well, fine
    Psi_v = np.empty((ks.size, xv.size), complex); Psi_L = np.empty((ks.size, xl_long.size), complex)
    Psi_in = np.empty((ks.size, xin.size), complex)
    for n, k in enumerate(ks):
        E_ = k * k / 2
        Psi_v[n] = psi_x(E_, segs, xv)[0]; Psi_L[n] = psi_x(E_, segs, xl_long)[0]; Psi_in[n] = psi_x(E_, segs, xin)[0]
    # the pair magnified: from 2 left of the first barrier to 2 right of the second, 0.05 apart
    xz = np.round(np.arange(round(xl - 2, 2), xr + 2 + 1e-9, 0.05), 6)
    Psi_z = np.array([psi_x(k * k / 2, segs, xz)[0] for k in ks])
    W = ph[None, :] * np.exp(-1j * np.outer(times, ks**2 / 2))   # (nf, nk)
    frames = W @ Psi_v                                          # (nf, nx)
    zoom = W @ Psi_z
    # what the page's blend between stored frames f and f+1 misses: the exact wave half-way, against
    # e^{-iE tau} [(1 - h) psi_f + h e^{iE dt} psi_f+1] at h = 1/2 (E = k0^2 / 2, the packet's mean energy)
    tm_ = times[:-1] + (times[1] - times[0]) / 2
    Wm = ph[None, :] * np.exp(-1j * np.outer(tm_, ks**2 / 2))
    mid = Wm @ Psi_v; dtf_ = times[1] - times[0]
    blend = np.exp(-1j * E * dtf_ / 2) * 0.5 * (frames[:-1] + np.exp(1j * E * dtf_) * frames[1:])
    interp_err = float(np.abs(mid - blend).max() / np.abs(frames).max())
    long = W @ Psi_L
    inner = W @ Psi_in
    pl = np.abs(long)**2; na = xa.size
    P_left = simpson(pl[:, :na], x=xa, axis=1)        # Simpson: error O(dx^4)
    P_right = simpson(pl[:, na:], x=xb, axis=1)
    P_in = simpson(np.abs(inner)**2, x=xin, axis=1)
    norm = P_left + P_in + P_right
    # the start packet against the reconstruction at t = 0
    N0 = (2 * np.pi * s0**2) ** -0.25
    start = N0 * np.exp(-(xl_long - x0)**2 / (4 * s0**2) + 1j * k0 * xl_long)
    start_err = float(np.sqrt(np.trapezoid(np.abs(long[0, :na] - start[:na])**2, xa) + np.trapezoid(np.abs(long[0, na:] - start[na:])**2, xb)))
    sx = N0 * np.exp(-(xin - x0)**2 / (4 * s0**2))
    tail_in = float(np.trapezoid(np.abs(start[na:])**2, xb) + np.trapezoid(sx**2, xin))
    kneg = float(0.5 * (1 - __import__("math").erf(np.sqrt(2) * s0 * k0)))     # probability with k < 0 in |phi|^2
    T_packet = float(np.sum(np.abs(phi(ks, k0, s0, x0))**2 * np.array([abs(solve(k * k / 2, segs)[0])**2 for k in ks])) * dk)
    # lifetime: fit P_in(t) = A e^{-t/tau} once the incident packet has passed the pair (its centre 4 sigma beyond the far edge)
    t_pass = (xr - x0 + 4 * s0 * np.sqrt(1 + 0)) / k0
    m = (times > t_pass) & (P_in > 1e-7)
    fit = None
    if m.sum() >= 8:
        cf = np.polyfit(times[m], np.log(P_in[m]), 1)
        resid = np.log(P_in[m]) - np.polyval(cf, times[m])
        fit = dict(tau=float(-1 / cf[0]) if cf[0] < 0 else None, A=float(np.exp(cf[1])), t_from=float(times[m][0]),
                   t_to=float(times[m][-1]), points=int(m.sum()), log_rms=float(np.sqrt(np.mean(resid**2))))
    head = dict(E=E, k0=float(k0), V0=V0, d=D, s=s, sigma0=s0, x0=x0, barriers=[list(b) for b in segs], x_first=float(xv[0]),
                dx=DX, nx=int(xv.size), nf=nf, t=[round(float(t), 6) for t in times], dk=dk, k_min=float(ks[0]), k_max=float(ks[-1]),
                nk=int(ks.size), P_left=np.round(P_left, 7).tolist(), P_in=np.round(P_in, 7).tolist(), P_right=np.round(P_right, 7).tolist(),
                norm_min=float(norm.min()), norm_max=float(norm.max()), start_error=start_err, start_tail_in_barriers=tail_in,
                k_negative=kneg, T_packet=T_packet, T_k0=float(abs(solve(E, segs)[0])**2), fit=fit, peak=float(np.abs(frames).max()),
                zoom_first=float(xz[0]), zoom_dx=0.05, zoom_nx=int(xz.size), zoom_peak=float(np.abs(zoom).max()),
                interp_err_max=interp_err, frame_dt=float(times[1] - times[0]),
                fp16_max_rel=None, method="transfer-matrix superposition (tools/kaggle/resonant-tunnelling/recon.py)")
    re = frames.real.astype(np.float16); im = frames.imag.astype(np.float16)
    zr = zoom.real.astype(np.float16); zi = zoom.imag.astype(np.float16)
    err = np.abs(re.astype(float) + 1j * im.astype(float) - frames)
    head["fp16_max_abs"] = float(err.max()); head["fp16_max_rel"] = float(err.max() / np.abs(frames).max())
    hb = json.dumps(head, separators=(",", ":")).encode()
    hb += b" " * ((-len(hb) - 8) % 2)                           # the float16 arrays start on an even byte
    body = b"RTF1" + struct.pack("<I", len(hb)) + hb + re.tobytes() + im.tobytes() + zr.tobytes() + zi.tobytes()
    return head, body, frames, xv, times


def grid(quick=False):
    """The runs to store. Main sweep: the short packet (sigma0 = 3) across a fine energy grid for every geometry, so the
    reader can drag energy across the resonances. Plus the long packet (sigma0 = 12) at each geometry's resonance energies
    in [0.5, 2.5], to show that a longer pulse (sharper in energy) transmits more fully on resonance."""
    jobs = []
    for gi, s in enumerate(GAPS):
        res = [r for r in resonances(double(V0, D, s)) if 0.5 <= r["E"] <= 2.5]
        Es3 = sorted(set(EGRID) | {round(r["E"], 4) for r in res})
        Es12 = sorted({round(r["E"], 4) for r in res})
        if quick: Es3, Es12 = [1.0], [1.0]
        for E in Es3: jobs.append((gi, s, 3.0, E))
        for E in Es12: jobs.append((gi, s, 12.0, E))
    return jobs


def _one(args):
    gi, s, s0, E = args; t1 = time.time()
    head, body, *_ = run(E, s, s0)
    name = f"s{gi}_p{int(s0)}_E{E:.4f}.bin"
    return name, body, dict(file=name, gap=gi, s=s, sigma0=s0, E=E, bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                            seconds=round(time.time() - t1, 2), T_packet=head["T_packet"], T_k0=head["T_k0"],
                            P_right_end=head["P_right"][-1], P_in_end=head["P_in"][-1], norm_min=head["norm_min"],
                            norm_max=head["norm_max"], start_error=head["start_error"], fit=head["fit"],
                            fp16_max_rel=head["fp16_max_rel"], interp_err_max=head["interp_err_max"], nf=head["nf"],
                            t_end=head["t"][-1], peak=head["peak"], zoom_peak=head["zoom_peak"])


if __name__ == "__main__":
    from multiprocessing import Pool
    out = sys.argv[1]; quick = "--quick" in sys.argv
    os.makedirs(out + "/runs", exist_ok=True)
    ET = np.linspace(0.02, 3.0, 1500)
    geoms = []
    for gi, s in enumerate(GAPS):
        segs = double(V0, D, s)
        geoms.append(dict(s=s, V0=V0, d=D, resonances=resonances(segs),
                          T_E=dict(E=np.round(ET, 5).tolist(), T=np.round(T_of_E(ET, segs), 7).tolist())))
    single = dict(E=np.round(ET, 5).tolist(), T=np.round(T_of_E(ET, [(-D / 2, D / 2, V0)]), 7).tolist())
    jobs = grid(quick); runs = []; T0 = time.time()
    with Pool(min(4, os.cpu_count())) as pool:
        for m, (name, body, rec) in enumerate(pool.imap_unordered(_one, jobs), 1):
            open(f"{out}/runs/{name}", "wb").write(body); runs.append(rec)
            print(f"{m:3d}/{len(jobs)} {name}: {rec['seconds']}s T_packet {rec['T_packet']:.4f} P_right(end) {rec['P_right_end']:.4f} "
                  f"norm {rec['norm_min']:.6f}..{rec['norm_max']:.6f} start {rec['start_error']:.1e} tau {rec['fit'] and rec['fit']['tau']}", flush=True)
    runs.sort(key=lambda r: r["file"])
    json.dump(dict(V0=V0, d=D, gaps=GAPS, packets={str(k): v for k, v in PACKETS.items()}, dx=DX, geometries=geoms, single=single,
                   runs=runs, seconds=round(time.time() - T0, 1), total_bytes=sum(r["bytes"] for r in runs)),
              open(f"{out}/summary.json", "w"), separators=(",", ":"))
    print(f"done {len(runs)} runs, {sum(r['bytes'] for r in runs)/1e6:.1f} MB, {time.time()-T0:.0f} s")
