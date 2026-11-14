"""Fig. 15 correction, walls: the exact 3D field of a stored wall run, with no time grid and no barrier sampling.

Separation. V depends on x alone and the start packet is a product, so for all time
    psi(x, y, z, t) = chi(x, t) h(y, t) h(z, t),
h the free Gaussian of width sp:  h(y, t) = (2 pi sp^2)^(-1/4) (1 + i t / (2 sp^2))^(-1/2) exp(-y^2 / (4 sp^2 (1 + i t / (2 sp^2)))).

chi by superposition of stationary scattering states (hbar = m = 1, E = k^2 / 2, k the wave number on the left):
    chi(x, t) = Int dk / (2 pi) [ c+(k) psi+_k(x) + (k / kR) c-(k) psi-_k(x) ] e^{-i k^2 t / 2},
    psi+_k : e^{ikx} + r e^{-ikx} on the left,  t e^{i kR x} on the right            (incident from the left),
    psi-_k : t' e^{-ikx} on the left,  e^{-i kR x} + r' e^{i kR x} on the right      (incident from the right),
    kR = sqrt(k^2 + 2 bias),  c+- = <psi+-_k | chi0>  (the exact projections; normalisation <psi+_k|psi+_k'> = 2 pi delta(k - k'),
    <psi-_k|psi-_k'> = 2 pi (kR / k) delta(k - k')).
The two families with E > 0 are complete for a packet that starts on the left, up to right-incident states with -bias < E < 0,
which are evanescent on the left; their share is bounded by the start packet's share right of the first face (start_in_barrier).
Inside the structure psi is carried face to face by the exact flat-segment propagator; a bias ramp is cut into flat slices whose
convergence is measured (nslice).

Time enters only as e^{-iEt}: there is no time step and no grid in x, so neither the barrier sampling (D1) nor the side border
(D2) can arise. The k sum is a trapezoid on a uniform grid dk: it equals the exact integral periodised in x with period
2 pi / dk, so dk is chosen with 2 pi / dk far longer than the distance any part of the wave travels in the run.

Regions over the whole line: P_left(t) = P_left(0) - Int_0^t j(xl), P_right(t) = Int_0^t j(xr) (j the flux at the outer faces),
P_struct(t) from |chi|^2 on a fine grid between the faces; P_left + P_struct + P_right = 1 is checked, not imposed.
"""
import os, sys, json
import numpy as np
from math import erfc, sqrt, pi

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))


def centres(sp):
    """Barrier centres as in rt3d2.centres (faces on odd multiples of 0.25)."""
    N, P, D = sp["N"], sp["P"], sp["D"]
    for c in (0.0, 0.25):
        cs = [c + (k - (N - 1) / 2) * P for k in range(N)]
        faces = [f for ck in cs for f in (ck - D / 2, ck + D / 2)]
        if all(abs((f - 0.25) / 0.5 - round((f - 0.25) / 0.5)) < 1e-9 for f in faces): return cs
    raise ValueError("no grid-aligned placement")


def x0_of(sp):
    cs = centres(sp); return cs[0] - sp["D"] / 2 - max(14.0, 4 * sp["sx"])


def segments(sp, nslice=2000):
    """Flat segments (a, b, V) tiling [xl, xr]. Unbiased walls are exact; a bias ramp is sliced, about nslice slices in all."""
    cs = centres(sp); D, V0, b = sp["D"], sp["V0"], sp.get("bias", 0.0) or 0.0
    xl, xr = cs[0] - D / 2, cs[-1] + D / 2
    faces = sorted({round(f, 12) for c in cs for f in (c - D / 2, c + D / 2)})
    segs = []
    for a, bb in zip(faces[:-1], faces[1:]):
        m = 0.5 * (a + bb); Vb = V0 if any(abs(m - c) < D / 2 for c in cs) else 0.0
        if not b: segs.append((a, bb, Vb)); continue
        n = max(4, int(np.ceil(nslice * (bb - a) / (xr - xl)))); xg = np.linspace(a, bb, n + 1)
        for u, v in zip(xg[:-1], xg[1:]): segs.append((u, v, Vb - b * (0.5 * (u + v) - xl) / (xr - xl)))
    return segs, xl, xr


def _prop(q, L):
    """cos(qL), sin(qL)/q, -q sin(qL) for complex q (q -> 0 limit handled)."""
    c = np.cos(q * L); small = np.abs(q) < 1e-9
    s = np.where(small, L, np.sin(q * L) / np.where(small, 1, q))
    return c, s, -q * q * s


class Scatter:
    """Both scattering families at the wave numbers k (left lead), and their values at given interior points."""

    def __init__(self, sp, k, xin, nslice=2000):
        self.sp = sp; self.k = k = np.asarray(k, float); bias = sp.get("bias", 0.0) or 0.0
        segs, xl, xr = segments(sp, nslice); self.xl, self.xr = xl, xr
        E = 0.5 * k * k; self.E = E; kR = np.sqrt(k * k + 2 * bias); self.kR = kR
        xin = np.asarray(xin, float); order = np.argsort(xin); xs = xin[order]
        # fundamental solutions u1: (psi, psi')(xl) = (1, 0), u2: (0, 1), carried right face by face
        p1, d1 = np.ones_like(k, complex), np.zeros_like(k, complex)
        p2, d2 = np.zeros_like(k, complex), np.ones_like(k, complex)
        U1 = np.zeros((len(xs), len(k)), complex); U2 = np.zeros_like(U1)
        j = 0
        for (a, b, V) in segs:
            q = np.sqrt(2 * (E - V) + 0j)
            while j < len(xs) and xs[j] < b:
                if xs[j] >= a:
                    c, s, _ = _prop(q, xs[j] - a); U1[j] = c * p1 + s * d1; U2[j] = c * p2 + s * d2
                j += 1
            c, s, m = _prop(q, b - a)
            p1, d1 = c * p1 + s * d1, m * p1 + c * d1
            p2, d2 = c * p2 + s * d2, m * p2 + c * d2
        inv = np.empty(len(xs), int); inv[order] = np.arange(len(xs))
        U1, U2 = U1[inv], U2[inv]
        # left-lead values of e^{ikx} (a) and e^{-ikx} (b) at xl
        ea, eb = np.exp(1j * k * xl), np.exp(-1j * k * xl)
        A = (ea, 1j * k * ea); B = (eb, -1j * k * eb)
        def at_r(v):            # (psi, psi')(xl) -> (psi, psi')(xr)
            return v[0] * p1 + v[1] * p2, v[0] * d1 + v[1] * d2
        def split(w):           # (psi, psi')(xr) -> amplitudes of e^{i kR x}, e^{-i kR x}
            ps, dp = w
            return 0.5 * (ps + dp / (1j * kR)) * np.exp(-1j * kR * xr), 0.5 * (ps - dp / (1j * kR)) * np.exp(1j * kR * xr)
        aR, bR = split(at_r(A)); aRb, bRb = split(at_r(B))
        r = -bR / bRb; t = aR + r * aRb                        # psi+: B_R = 0
        tp = 1 / bRb; rp = aRb / bRb                           # psi-: unit incoming e^{-i kR x}
        self.r, self.t, self.tp, self.rp = r, t, tp, rp
        # interior values of both families
        self.inP = (A[0] + r * B[0]) * U1 + (A[1] + r * B[1]) * U2
        self.inM = tp * (B[0] * U1 + B[1] * U2)
        self.T = (kR / k) * np.abs(t)**2; self.R = np.abs(r)**2

    def values(self, x, inside_idx=None):
        """psi+ and psi- on points x: analytic outside [xl, xr]; inside, from the precomputed interior table (inside_idx maps
        each interior point to its row)."""
        k, kR = self.k, self.kR; x = np.asarray(x, float)
        Pp = np.empty((len(x), len(k)), complex); Pm = np.empty_like(Pp)
        L = x < self.xl; Rr = x > self.xr; I = ~(L | Rr)
        if L.any():
            e = np.exp(1j * np.outer(x[L], k)); Pp[L] = e + self.r / e; Pm[L] = self.tp / e
        if Rr.any():
            e = np.exp(1j * np.outer(x[Rr], kR)); Pp[Rr] = self.t * e; Pm[Rr] = 1 / e + self.rp * e
        if I.any():
            Pp[I] = self.inP[inside_idx[I]]; Pm[I] = self.inM[inside_idx[I]]
        return Pp, Pm


def chi0(sp, x):
    s = sp["sx"]; k0 = sqrt(2 * sp["E"]); x0 = x0_of(sp)
    return (2 * pi * s * s) ** -0.25 * np.exp(-(x - x0)**2 / (4 * s * s) + 1j * k0 * x)


def G(sp, k):
    """Int e^{-ikx} chi0(x) dx over the whole line (closed form)."""
    s = sp["sx"]; k0 = sqrt(2 * sp["E"]); x0 = x0_of(sp)
    return (2 * pi * s * s) ** -0.25 * 2 * s * sqrt(pi) * np.exp(-s * s * (k - k0)**2 - 1j * (k - k0) * x0)


def kgrid(sp, dk=5e-4, nsig=8.5):
    k0 = sqrt(2 * sp["E"]); sk = 1 / (2 * sp["sx"])
    lo = max(dk, k0 - nsig * sk); hi = k0 + nsig * sk
    n = int(np.ceil((hi - lo) / dk)) + 1
    k = np.linspace(lo, hi, n); w = np.full(n, (hi - lo) / (n - 1)); w[0] *= 0.5; w[-1] *= 0.5
    return k, w


def simpson_w(n, h):
    if n % 2 == 0: raise ValueError("odd n")
    w = np.ones(n); w[1:-1:2] = 4; w[2:-1:2] = 2; return w * h / 3


class Exact:
    """The exact chi of one wall run. xs_out: the points where chi is wanted (the box's 0.5 a grid)."""

    def __init__(self, sp, xs_out, dk=5e-4, nslice=2000, hfine=0.01):
        self.sp = sp; k, w = kgrid(sp, dk); self.k, self.w = k, w
        segs, xl, xr = segments(sp, nslice)
        # fine grid over the structure (Simpson, per segment between true faces), for P_struct and the well
        cs = centres(sp); D = sp["D"]
        faces = sorted({round(f, 12) for c in cs for f in (c - D / 2, c + D / 2)})
        fine, fw, fwell = [], [], []
        for a, b in zip(faces[:-1], faces[1:]):
            n = int(np.ceil((b - a) / hfine)); n += (n % 2 == 1); n += 1
            xx = np.linspace(a, b, n); fine.append(xx); fw.append(simpson_w(n, (b - a) / (n - 1)))
            m = 0.5 * (a + b); fwell.append(np.full(n, not any(abs(m - c) < D / 2 for c in cs)))
        self.xf = np.concatenate(fine); self.wf = np.concatenate(fw); self.well = np.concatenate(fwell)
        # projection grid: chi0 right of xl (its tail), where psi differs from the left-lead form
        s = sp["sx"]; xt_hi = xl + 10 * s
        nt = int(np.ceil((xt_hi - xl) / hfine)); nt += (nt % 2 == 1); nt += 1
        self.xt = np.linspace(xl, xt_hi, nt); self.wt = simpson_w(nt, (xt_hi - xl) / (nt - 1))
        xs_out = np.asarray(xs_out, float); self.xs_out = xs_out
        inside = np.concatenate([self.xf, self.xt[(self.xt >= xl) & (self.xt <= xr)], xs_out[(xs_out >= xl) & (xs_out <= xr)]])
        S = Scatter(sp, k, inside, nslice); self.S = S
        nf = len(self.xf); nt_in = int(((self.xt >= xl) & (self.xt <= xr)).sum())
        idx_f = np.arange(nf)
        idx_t = np.full(len(self.xt), -1); idx_t[(self.xt >= xl) & (self.xt <= xr)] = nf + np.arange(nt_in)
        idx_o = np.full(len(xs_out), -1); io = (xs_out >= xl) & (xs_out <= xr); idx_o[io] = nf + nt_in + np.arange(io.sum())
        # projections c+ = <psi+|chi0>, c- = <psi-|chi0>: closed form for the left-lead form over the whole line, plus the
        # exact correction where chi0's tail meets the structure and beyond
        Gk, Gmk = G(sp, k), G(sp, -k)
        cP = Gk + np.conj(S.r) * Gmk
        cM = np.conj(S.tp) * Gmk
        Pp, Pm = S.values(self.xt, idx_t)
        e = np.exp(1j * np.outer(self.xt, k)); Lp = e + S.r / e; Lm = S.tp / e
        c0 = chi0(sp, self.xt) * self.wt
        cP = cP + ((np.conj(Pp) - np.conj(Lp)) * c0[:, None]).sum(0)
        cM = cM + ((np.conj(Pm) - np.conj(Lm)) * c0[:, None]).sum(0)
        self.cP, self.cM = cP, cM
        self.aP = w / (2 * pi) * cP; self.aM = w / (2 * pi) * (k / S.kR) * cM
        # completeness: the share of chi0 the two families carry (1 up to the evanescent right-incident states and k-range cut)
        self.carried = float((w / (2 * pi) * (np.abs(cP)**2 + (k / S.kR) * np.abs(cM)**2)).sum())
        # the share that ends on the right: outgoing right amplitude per k is c+ t + (k/kR) c- r'
        out = cP * S.t + (k / S.kR) * cM * S.rp
        self.T_inf = float((w / (2 * pi) * np.abs(out)**2 * (S.kR / k)).sum())
        self.T_packet_weights = float((w * np.abs(Gk)**2 * S.T).sum() / (w * np.abs(Gk)**2).sum())
        self.PL0 = 1 - 0.5 * erfc((xl - x0_of(sp)) / (sqrt(2) * s))   # Int_{-inf}^{xl} |chi0|^2
        # tables of psi on the output points and the fine structure grid, and at the two outer faces (value and slope)
        self.Bo = self._basis(xs_out, idx_o); self.Bf = self._basis(self.xf, idx_f)
        kk, kR = k, S.kR; el, er = np.exp(1j * kk * xl), np.exp(1j * kR * xr)
        self.fl = (self.aP * (el + S.r / el) + self.aM * (S.tp / el), self.aP * 1j * kk * (el - S.r / el) + self.aM * (-1j * kk) * S.tp / el)
        self.fr = (self.aP * S.t * er + self.aM * (1 / er + S.rp * er), self.aP * 1j * kR * S.t * er + self.aM * 1j * kR * (-1 / er + S.rp * er))

    def _basis(self, x, idx):
        Pp, Pm = self.S.values(x, idx)
        return Pp * self.aP + Pm * self.aM            # sum over k of this row times e^{-iEt} gives chi(x, t)

    def chi(self, times, which="out"):
        B = self.Bo if which == "out" else self.Bf
        ph = np.exp(-1j * np.outer(self.S.E, times))  # (nk, nt)
        return B @ ph                                  # (nx, nt)

    def flux_integrals(self, times, dt=0.02):
        """P_left(t), P_right(t) at the given times by integrating the flux at xl and xr in time (Simpson on a fine time grid)."""
        tmax = float(np.max(times)); n = int(np.ceil(tmax / dt)); n += (n % 2 == 1); n = max(n, 2)
        tt = np.linspace(0, tmax, n + 1); h = tmax / n
        jl = np.empty(len(tt)); jr = np.empty(len(tt))
        for a in range(0, len(tt), 2000):
            ph = np.exp(-1j * np.outer(tt[a:a + 2000], self.S.E))
            pl, dl = ph @ self.fl[0], ph @ self.fl[1]; pr, dr = ph @ self.fr[0], ph @ self.fr[1]
            jl[a:a + 2000] = np.imag(np.conj(pl) * dl); jr[a:a + 2000] = np.imag(np.conj(pr) * dr)
        # cumulative Simpson at even nodes, linear (trapezoid) blend at odd nodes
        cl = np.zeros(len(tt)); cr = np.zeros(len(tt))
        cl[2::2] = np.cumsum(h / 3 * (jl[0:-2:2] + 4 * jl[1:-1:2] + jl[2::2]))
        cr[2::2] = np.cumsum(h / 3 * (jr[0:-2:2] + 4 * jr[1:-1:2] + jr[2::2]))
        cl[1::2] = cl[0:-1:2] + 0.5 * h * (jl[0:-1:2] + jl[1::2]); cr[1::2] = cr[0:-1:2] + 0.5 * h * (jr[0:-1:2] + jr[1::2])
        return self.PL0 - np.interp(times, tt, cl), np.interp(times, tt, cr)

    def box_tails(self, times, xlo, xhi, dt=0.02):
        """Int_{-inf}^{xlo} |chi|^2 and Int_{xhi}^{inf} |chi|^2 at the given times: the start packet's share there minus (plus) the
        time integral of the flux through xlo (xhi). xlo < xl and xhi > xr (lead regions, analytic psi)."""
        k, kR, S = self.k, self.S.kR, self.S
        el, eh = np.exp(1j * k * xlo), np.exp(1j * kR * xhi)
        fl = (self.aP * (el + S.r / el) + self.aM * (S.tp / el), self.aP * 1j * k * (el - S.r / el) - self.aM * 1j * k * S.tp / el)
        fh = (self.aP * S.t * eh + self.aM * (1 / eh + S.rp * eh), self.aP * 1j * kR * S.t * eh + self.aM * 1j * kR * (-1 / eh + S.rp * eh))
        tmax = float(np.max(times)); n = int(np.ceil(tmax / dt)); n += (n % 2 == 1); n = max(n, 2)
        tt = np.linspace(0, tmax, n + 1); h = tmax / n; jl = np.empty(len(tt)); jh = np.empty(len(tt))
        for a in range(0, len(tt), 2000):
            ph = np.exp(-1j * np.outer(tt[a:a + 2000], self.S.E))
            jl[a:a + 2000] = np.imag(np.conj(ph @ fl[0]) * (ph @ fl[1])); jh[a:a + 2000] = np.imag(np.conj(ph @ fh[0]) * (ph @ fh[1]))
        def cum(j):
            c = np.zeros(len(tt)); c[2::2] = np.cumsum(h / 3 * (j[0:-2:2] + 4 * j[1:-1:2] + j[2::2]))
            c[1::2] = c[0:-1:2] + 0.5 * h * (j[0:-1:2] + j[1::2]); return np.interp(times, tt, c)
        s = self.sp["sx"]; x0 = x0_of(self.sp)
        lo0 = 0.5 * erfc((x0 - xlo) / (sqrt(2) * s)); hi0 = 0.5 * erfc((xhi - x0) / (sqrt(2) * s))
        return lo0 - cum(jl), hi0 + cum(jh)

    def regions(self, times):
        cf = self.chi(times, "fine"); rho = np.abs(cf)**2
        Pst = (self.wf[:, None] * rho).sum(0); Pw = (self.wf[self.well][:, None] * rho[self.well]).sum(0)
        PL, PR = self.flux_integrals(times)
        return dict(left=PL, right=PR, well=Pw, struct=Pst, closure=PL + PR + Pst)


def h_free(y, t, s):
    a = 1 + 1j * t / (2 * s * s)
    return (2 * pi * s * s) ** -0.25 * a ** -0.5 * np.exp(-np.asarray(y)[:, None] ** 2 / (4 * s * s * a))
