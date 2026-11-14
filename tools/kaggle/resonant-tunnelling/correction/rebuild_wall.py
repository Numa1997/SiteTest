"""Fig. 15 correction, walls: write a wall run's RT3C file from a given chi(x, t), in exactly the stored file's layout and frames.

Two sources of chi:
  'exact' : exact_wall.Exact (stationary-state superposition; the true 3D field psi = chi(x,t) h(y,t) h(z,t));
  'twin'  : the solver's own grid scheme in 1D (rt3d2.run1d: Strang split-step, 0.5 a, dt 0.01, sin^(1/8) border) for chi and the
            same scheme with V = 0 for h on the 128-point cross axis. The 3D scheme of rt3d2 separates exactly (V(x) alone, a product
            mask, a separable kinetic factor), so the twin must reproduce the stored file to its 8-bit steps: the writer check.
What the file holds, as rt3d2.run writes it: |psi| and arg psi on z = 0, y >= 0 over the box interior, 8-bit levels of each frame's
own peak; the x-profile (integral over y, z); region curves; for walls the 1D profile.
Usage: python3 rebuild_wall.py <stored file.bin> [exact|twin] [out.bin]
"""
import os, sys, json, struct, zlib, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import read_rt3d, exact_wall as ew


def quantize(sl, ph):
    """The solver's own rule (rt3d2.run): levels of the frame's peak; phase levels; phase zeroed where the amplitude is < 3 levels."""
    sl = np.nan_to_num(sl); pk = float(sl.max()) or 1.0
    qa = np.clip(np.round(255 * sl / pk), 0, 255).astype(np.uint8)
    qp = (np.round((np.nan_to_num(ph) + np.pi) / (2 * np.pi) * 255) % 256).astype(np.uint8); qp[qa < 3] = 0
    return qa, qp, pk


def axis(n, dx=0.5):
    x = (np.arange(n) - n // 2) * dx; k = 2 * np.pi * np.fft.fftfreq(n, dx)
    W = max(4, n // 10); m = np.ones(n); e = np.arange(W); m[:W] = np.sin(0.5 * np.pi * e / W) ** 0.125; m[-W:] = m[:W][::-1]
    return x, k, m


def twin_fields(h):
    """chi_d(x, t_f) on the box grid and h_d(y, t_f) on the cross grid, by the stored run's own discrete scheme (complex128)."""
    sp = h["spec"]; dt = h["dt"]; per = int(round(h["frame_dt"] / dt)); n = h["n"]
    x, kx, mx = axis(sp["Nx"]); y, ky, my = axis(128)
    cs = h["centres"]; xl, xr = h["extent"]
    V = np.zeros_like(x)
    for c in cs: V += np.where(np.abs(x - c) < sp["D"] / 2, sp["V0"], 0.0)
    if sp.get("bias"): V += -sp["bias"] * np.clip((x - xl) / (xr - xl), 0, 1)
    k0 = np.sqrt(2 * sp["E"]); x0 = h["x0"]
    chi = np.exp(-(x - x0)**2 / (4 * sp["sx"]**2) + 1j * k0 * x); chi /= np.sqrt((abs(chi)**2).sum() * 0.5)
    g = np.exp(-y**2 / (4 * sp["sp"]**2)).astype(complex); g /= np.sqrt((abs(g)**2).sum() * 0.5)
    hv = np.exp(-0.5j * V * dt); kin = np.exp(-0.5j * kx**2 * dt); kiny = np.exp(-0.5j * ky**2 * dt)
    C = np.empty((n, len(x)), complex); H = np.empty((n, len(y)), complex)
    for f in range(n):
        if f:
            for _ in range(per):
                chi = hv * np.fft.ifft(kin * np.fft.fft(hv * chi)) * mx
                g = np.fft.ifft(kiny * np.fft.fft(g)) * my
        C[f] = chi; H[f] = g
    return x, C, y, H


def from_twin(h):
    x, C, y, H = twin_fields(h)
    sp = h["spec"]; i0 = int(round((h["x_first"] - x[0]) / 0.5)); nxs = h["nxs"]; j0 = 64
    S = (np.abs(H)**2).sum(1) * 0.5                       # transverse survival per axis
    slab = C[:, i0:i0 + nxs, None] * H[:, None, j0:] * H[:, j0, None, None]
    prof = np.abs(C)**2 * (S**2)[:, None]
    xl, xr = h["extent"]; cs = h["centres"]; D = sp["D"]
    inb = np.zeros_like(x, bool)
    for c in cs: inb |= np.abs(x - c) < D / 2
    reg = dict(left=x < xl, right=x > xr)
    if len(cs) > 1: reg["well"] = (x > cs[0] + D / 2) & (x < cs[-1] - D / 2) & ~inb
    t = np.arange(h["n"]) * h["frame_dt"]
    curves = [t, (np.abs(C)**2).sum(1) * 0.5 * S**2] + [(np.abs(C[:, m])**2).sum(1) * 0.5 * S**2 for _, m in sorted(reg.items())]
    return slab, prof, np.abs(C)**2, np.array(curves).T, ["t", "norm"] + sorted(reg)


def from_exact(h, dk=5e-4, nslice=2000):
    sp = dict(h["spec"]); xs = h["prof_x_first"] + np.arange(h["prof_nx"]) * h["step"]
    X = ew.Exact(sp, xs, dk=dk, nslice=nslice)
    t = np.arange(h["n"]) * h["frame_dt"]
    chi = X.chi(t).T                                         # (n, nx)
    i0 = int(round((h["x_first"] - xs[0]) / h["step"])); nxs = h["nxs"]
    yy = np.arange(64) * h["step"]; Hy = ew.h_free(yy, t, sp["sp"]).T      # (n, 64); h(0, t) = Hy[:, 0]
    slab = chi[:, i0:i0 + nxs, None] * Hy[:, None, :] * Hy[:, 0, None, None]
    prof = np.abs(chi)**2                                    # the transverse factor has norm 1 on the whole plane
    half = 0.5 * h["prof_nx"] * h["step"]
    R, lo, hi = X.regions_and_tails(t, -half, half)
    # the same regions as the stored file, counted over the box (|x| <= box half-length) so that "total in box" keeps its meaning;
    # the whole-line values are kept beside them
    curves = [t, 1 - lo - hi, R["left"] - lo, R["right"] - hi] + ([R["well"]] if h["spec"]["N"] > 1 else [])
    names = ["t", "norm", "left", "right"] + (["well"] if h["spec"]["N"] > 1 else [])
    extra = dict(left_line=R["left"], right_line=R["right"], struct=R["struct"], closure=R["closure"])
    return slab, prof, prof, np.array(curves).T, names, X, extra


def write(h, slab, prof, prof1d, curves, names, extra_head):
    A, P, peaks = [], [], []
    for f in range(len(slab)):
        qa, qp, pk = quantize(np.abs(slab[f]), np.angle(slab[f])); A.append(qa); P.append(qp); peaks.append(pk)
    head = dict(h)
    head.update(peaks=[round(p / peaks[0], 6) for p in peaks], peak0=peaks[0], curve_names=names,
                curves=np.round(curves, 7).tolist())
    head.update(extra_head)
    body = np.array(A).tobytes() + np.array(P).tobytes() + np.asarray(prof, np.float32).tobytes()
    if prof1d is not None: body += np.asarray(prof1d, np.float32).tobytes()
    hb = json.dumps(head, separators=(",", ":")).encode()
    return b"RT3C" + struct.pack("<I", len(hb)) + hb + zlib.compress(body, 6), np.array(A), np.array(P), peaks


def level_diff(a, b, phase=False):
    d = np.abs(a.astype(int) - b.astype(int))
    if phase: d = np.minimum(d, 256 - d)
    return d


if __name__ == "__main__":
    src = sys.argv[1]; mode = sys.argv[2] if len(sys.argv) > 2 else "exact"
    blob = open(src, "rb").read(); h, amp, ph, prof, p1 = read_rt3d.read(blob)
    if mode == "twin":
        slab, pr, pr1, curves, names = from_twin(h)
        out, A, P, peaks = write(h, slab, pr, pr1, curves, names, {})
        da = level_diff(A, amp); dp = level_diff(P, ph, True); live = (amp >= 3) | (A >= 3)
        c = np.array(h["curves"])
        print(json.dumps(dict(file=os.path.basename(src), amp_max_level_diff=int(da.max()), amp_frac_diff=float((da > 0).mean()),
                              phase_max_level_diff_where_amp_ge3=int(dp[live].max()), phase_frac_diff=float((dp[live] > 0).mean()),
                              peak_rel_max=float(np.max(np.abs(np.array(peaks) / h["peak0"] / np.array(h["peaks"]) - 1))),
                              prof_rel_max=float(np.abs(pr - prof).max() / prof.max()),
                              curves_abs_max=float(np.abs(curves - c).max()))))
    else:
        slab, pr, pr1, curves, names, X, extra = from_exact(h)
        out, A, P, peaks = write(h, slab, pr, pr1, curves, names, {})
        print(len(out), X.T_inf)
