"""Step B1 of Fig. 15: read the single-barrier amplitudes t(k) and r(k) off the stored flat-wall runs of Fig. 14.

Parent data: public/data/schrodinger-sphere/2026-11-12/flat/e{i}_v{j}_a{k}.bin ('SPHC', written by
tools/kaggle/schrodinger-shapes/build_flat.py from flat.py). A file holds the cut psi(x, rho) = chi(x, t) g(rho, t) g(0, t) on
128 x 64 points 0.5 a apart (x = -32 ... 31.5, rho = 0 ... 31.5), 48 frames, as 8-bit levels: |psi| in 255 levels of the first
frame's peak, arg psi in levels of 2 pi / 255 (set to 0 where the amplitude level is below 3).

The rule used (exact for a packet that starts wholly left of the barrier and has no k < 0 part): for x right of the barrier
    chi(x, t) = (2 pi)^-1/2 Int phi(k) t(k) exp(i k x - i k^2 t / 2) dk,
and left of it the incident packet plus (2 pi)^-1/2 Int phi(k) r(k) exp(-i k x - i k^2 t / 2) dk. Once the transmitted and
reflected packets lie inside the stored window, a Fourier sum over x > a/2 (or x < -a/2) gives phi t e^{-i k^2 t/2}
(or phi r e^{-i k^2 t/2} at -k); dividing by the known phi(k) and the free phase gives t(k) and r(k).

Conventions: hbar = m = 1, slab V0 for |x| < a/2, t and r referred to x = 0 (incoming e^{ikx}, transmitted t e^{ikx},
reflected r e^{-ikx}).
"""
import json, struct, zlib, os, sys
import numpy as np

S0, X0 = 3.0, -14.0                       # the packet of Fig. 14: sigma0, start centre
N0 = (2 * np.pi * S0**2) ** -0.25         # chi(x, 0) = N0 exp(-(x - x0)^2 / (4 s0^2) + i k0 x)


def read_sphc(path):
    b = open(path, "rb").read()
    assert b[:4] == b"SPHC"
    H = struct.unpack("<I", b[4:8])[0]
    h = json.loads(b[8:8 + H]); curves = np.array(h.pop("curves"))
    raw = np.frombuffer(zlib.decompress(b[8 + H:]), np.uint8)
    n, nx, nr = h["n"], h["nx"], h["nr"]
    qa = raw[:n * nx * nr].reshape(n, nx, nr); qp = raw[n * nx * nr:].reshape(n, nx, nr)
    return h, curves, qa, qp


def g0(rho, t):
    """The free Gaussian of flat.py, g(y, t) for sigma0 = 3."""
    c = 1 + 1j * t / (2 * S0**2)
    return (2 * np.pi * S0**2) ** -0.25 * c ** -0.5 * np.exp(-rho**2 / (4 * S0**2 * c))


def phi(k, k0):
    """Fourier transform (2 pi)^-1/2 Int chi(x, 0) e^{-ikx} dx of the start packet."""
    return N0 * np.sqrt(2) * S0 * np.exp(-S0**2 * (k - k0)**2) * np.exp(-1j * (k - k0) * X0)


def exact_tr(k, V0, a):
    """t and r of the slab, by solving the four matching equations at x = -a/2 and x = +a/2 directly (no formula used).
    Left: e^{ikx} + r e^{-ikx}; inside: F e^{iqx} + G e^{-iqx}, q = sqrt(k^2 - 2 V0) (complex below the top); right: t e^{ikx}."""
    k = np.atleast_1d(np.asarray(k, float)); t = np.empty(k.size, complex); r = np.empty(k.size, complex)
    for n, kk in enumerate(k):
        E_ = kk**2 / 2
        if abs(E_ - V0) < 1e-9: E_ = V0 * (1 + 1e-9) + 1e-12      # avoid q = 0, where the two inside solutions coincide
        q = np.sqrt(complex(2 * (E_ - V0))); L, R = -a / 2, a / 2
        e = lambda s, x: np.exp(1j * s * x)
        # unknowns (r, F, G, t)
        A = np.array([[e(-kk, L), -e(q, L), -e(-q, L), 0],
                      [-1j * kk * e(-kk, L), -1j * q * e(q, L), 1j * q * e(-q, L), 0],
                      [0, e(q, R), e(-q, R), -e(kk, R)],
                      [0, 1j * q * e(q, R), -1j * q * e(-q, R), -1j * kk * e(kk, R)]])
        rhs = np.array([-e(kk, L), -1j * kk * e(kk, L), 0, 0])
        r[n], _, _, t[n] = np.linalg.solve(A, rhs)
    return t, r


def chi_from_cut(amp, ph, t, rho, use_rho="axis"):
    """chi(x, t) from one stored frame. amp, ph: (nx, nr) complex parts already decoded. 'axis' uses rho = 0 only;
    'all' takes the least-squares combination of every rho column whose level is >= 3 (each column is chi g(rho) g(0))."""
    psi = amp * np.exp(1j * ph)
    G = g0(rho, t) * g0(0.0, t)                        # (nr,)
    if use_rho == "axis":
        return psi[:, 0] / G[0]
    good = amp > 0                                     # set by the caller: False where the level was below 3
    W = good * np.abs(G)[None, :]**2
    return (psi * np.conj(G)[None, :] * good).sum(1) / np.maximum(W.sum(1), 1e-300)


def ft(x, f, k, dx):
    """(2 pi)^-1/2 sum f(x_j) e^{-ikx_j} dx."""
    return (np.exp(-1j * np.outer(k, x)) @ f) * dx / np.sqrt(2 * np.pi)


def extract(x, chi, t, k, k0, a, dx, margin=0.0):
    """t(k), r(k) from chi(x) at time t on the points x (spacing dx)."""
    right = x > a / 2 + margin; left = x < -a / 2 - margin
    T = ft(x[right], chi[right], k, dx) * np.exp(1j * k**2 * t / 2) / phi(k, k0)
    Rr = ft(x[left], chi[left], -k, dx) * np.exp(1j * k**2 * t / 2) / phi(k, k0)
    # the incident packet's own part left of the barrier: the free packet, subtracted with its exact form
    inc = ft(x[left], free_packet(x[left], t, k0), -k, dx) * np.exp(1j * k**2 * t / 2) / phi(k, k0)
    return T, Rr - inc


def free_packet(x, t, k0):
    c = 1 + 1j * t / (2 * S0**2)
    return N0 * c**-0.5 * np.exp(-(x - X0 - k0 * t)**2 / (4 * S0**2 * c) + 1j * k0 * (x - k0 * t / 2))


def decode(qa, qp, f, E):
    a0 = N0 * g0(0.0, 0.0).real**2 * 1.0           # amp[0].max(): the start packet's peak on the axis, at x = x0 (a grid point)
    amp = qa[f].astype(float) / 255 * a0
    ph = qp[f].astype(float) / 255 * 2 * np.pi - np.pi
    amp_masked = np.where(qa[f] >= 3, amp, 0.0)
    return amp, ph, amp_masked, a0


def omega_cn(k, dx=0.05, dt=0.01):
    """The free phase per unit time of flat.py's scheme for a plane wave e^{ikx}: the fourth-order Laplacian's symbol
    (30 - 32 cos k dx + 2 cos 2k dx) / (12 dx^2) halved, then Crank-Nicolson's (2/dt) arctan(dt w / 2)."""
    w = 0.5 * (30 - 32 * np.cos(k * dx) + 2 * np.cos(2 * k * dx)) / (12 * dx**2)
    return 2 / dt * np.arctan(dt * w / 2)


def extract_ls(x, frames, times, k0, a, knots, dk=0.002, lam=1e-6, disp="cn", margin=0.0):
    """t(k), r(k) on the knots by least squares over every frame and every point right (left) of the barrier.
    Model, exact for a packet that starts wholly left: chi(x, t) = (2 pi)^-1/2 Int phi(k) [t(k) e^{ikx}] e^{-i w(k) t} dk for
    x > a/2, and the incident packet + (2 pi)^-1/2 Int phi(k) r(k) e^{-ikx} e^{-i w(k) t} dk for x < -a/2.
    t(k) and r(k) are piecewise linear between the knots. w(k) = k^2/2 ('exact') or the solver's own (omega_cn).
    frames: (nf, nx) complex chi on the points x; times: (nf,). Returns t, r at the knots and the rms residuals."""
    kq = np.arange(knots[0], knots[-1] + dk / 2, dk)
    hat = np.maximum(0, 1 - np.abs(kq[:, None] - knots[None, :]) / (knots[1] - knots[0]))   # (nq, nm)
    w = omega_cn(kq) if disp == "cn" else kq**2 / 2
    ph = phi(kq, k0) * dk / np.sqrt(2 * np.pi)
    out = []
    for side in (+1, -1):
        sel = x > a / 2 + margin if side > 0 else x < -a / 2 - margin
        xs = x[sel]
        rows = []; rhs = []
        for f, t in enumerate(times):
            E = np.exp(1j * side * np.outer(xs, kq) - 1j * w[None, :] * t) * ph[None, :]      # (nx, nq)
            rows.append(E @ hat)
            y = frames[f][sel]
            if side < 0:     # remove the incident packet, propagated with the same phase law
                y = y - E_inc(xs, t, kq, w, ph)
            rhs.append(y)
        A = np.vstack(rows); b = np.concatenate(rhs)
        AhA = A.conj().T @ A; n = AhA.shape[0]
        c = np.linalg.solve(AhA + lam * np.trace(AhA).real / n * np.eye(n), A.conj().T @ b)
        res = float(np.sqrt(np.mean(np.abs(A @ c - b)**2)) / np.sqrt(np.mean(np.abs(b)**2)))
        out.append((c, res))
    (tc, rest), (rc, resr) = out
    return tc, rc, rest, resr


def E_inc(xs, t, kq, w, ph):
    return np.exp(1j * np.outer(xs, kq) - 1j * w[None, :] * t) @ ph
