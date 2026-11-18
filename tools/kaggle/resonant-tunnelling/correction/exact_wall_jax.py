"""Fig. 15 correction, walls: exact_wall.py vectorised in JAX for the GPU (complex128). The same mathematics, line for line
(read exact_wall.py's docstring); only the arrays live on the device:
  - the fundamental solutions are carried face to face by lax.scan over the segments, all wave numbers at once;
  - every point value is one gather and one fused elementwise expression over (points x wave numbers);
  - chi at the frame times is one matrix product; the flux integrals use one exp table built by recurrence.
"""
import numpy as np
from math import erfc, sqrt, pi
import jax, jax.numpy as jnp
import os
jax.config.update("jax_enable_x64", os.environ.get("EXACT_X64", "1") == "1")
import exact_wall as ew          # the geometry helpers and the reference implementation

c128 = jnp.complex128 if jax.config.jax_enable_x64 else jnp.complex64


def _prop(q, L):
    c = jnp.cos(q * L); small = jnp.abs(q) < 1e-9
    s = jnp.where(small, L, jnp.sin(q * L) / jnp.where(small, 1.0, q))
    return c, s, -q * q * s


class ExactJ:
    def __init__(self, sp, xs_out, dk=5e-4, nslice=2000, hfine=0.01):
        self.sp = sp; k_np, w_np = ew.kgrid(sp, dk); bias = sp.get("bias", 0.0) or 0.0
        NB = 1024; npad = (-len(k_np)) % NB                    # zero-weight padding: the sums are unchanged
        if npad:
            k_np = np.r_[k_np, k_np[-1] + dk * np.arange(1, npad + 1)]; w_np = np.r_[w_np, np.zeros(npad)]
        segs, xl, xr = ew.segments(sp, nslice); self.xl, self.xr = xl, xr
        k = jnp.asarray(k_np); w = jnp.asarray(w_np); E = 0.5 * k * k; kR = jnp.sqrt(k * k + 2 * bias)
        self.k, self.w, self.E, self.kR = k, w, E, kR
        sa = np.array([s[0] for s in segs]); sb = np.array([s[1] for s in segs]); sV = np.array([s[2] for s in segs])
        # fundamental solutions at every left face (scan over segments)
        def step(c, seg):
            a, b, V = seg; q = jnp.sqrt(2 * (E - V) + 0j); cc, ss, mm = _prop(q, b - a)
            p1, d1, p2, d2 = c
            return (cc * p1 + ss * d1, mm * p1 + cc * d1, cc * p2 + ss * d2, mm * p2 + cc * d2), c
        one = jnp.ones_like(k, dtype=c128); zero = jnp.zeros_like(k, dtype=c128)
        (P1, D1, P2, D2), faces = jax.lax.scan(step, (one, zero, zero, one), (jnp.asarray(sa), jnp.asarray(sb), jnp.asarray(sV)))
        self.faces = faces; self.seg = (sa, sb, sV)
        ea, eb = jnp.exp(1j * k * xl), jnp.exp(-1j * k * xl)
        A = (ea, 1j * k * ea); B = (eb, -1j * k * eb)
        def split(v):
            ps = v[0] * P1 + v[1] * P2; dp = v[0] * D1 + v[1] * D2
            return 0.5 * (ps + dp / (1j * kR)) * jnp.exp(-1j * kR * xr), 0.5 * (ps - dp / (1j * kR)) * jnp.exp(1j * kR * xr)
        aR, bR = split(A); aRb, bRb = split(B)
        r = -bR / bRb; t = aR + r * aRb; tp = 1 / bRb; rp = aRb / bRb
        self.r, self.t, self.tp, self.rp = r, t, tp, rp
        self.alphaP = (A[0] + r * B[0], A[1] + r * B[1]); self.alphaM = (tp * B[0], tp * B[1])
        # fine structure grid (Simpson per segment between true faces)
        cs = ew.centres(sp); D = sp["D"]
        fa = sorted({round(f, 12) for c in cs for f in (c - D / 2, c + D / 2)})
        fine, fw, fwell = [], [], []
        for a, b in zip(fa[:-1], fa[1:]):
            n = int(np.ceil((b - a) / hfine)); n += (n % 2 == 1); n += 1
            xx = np.linspace(a, b, n); fine.append(xx); fw.append(ew.simpson_w(n, (b - a) / (n - 1)))
            m = 0.5 * (a + b); fwell.append(np.full(n, not any(abs(m - c) < D / 2 for c in cs)))
        self.xf = np.concatenate(fine); self.wf = jnp.asarray(np.concatenate(fw)); self.well = np.concatenate(fwell)
        s = sp["sx"]; xt_hi = max(xr + 1.0, ew.x0_of(sp) + 8.6 * s)      # |chi0|^2 < 1e-16 of its peak beyond 8.6 sigma
        ht = 0.02; nt = int(np.ceil((xt_hi - xl) / ht)); nt = -(-nt // 512) * 512 + 1; xt_hi = xl + ht * (nt - 1)
        xt = np.linspace(xl, xt_hi, nt); wt = ew.simpson_w(nt, (xt_hi - xl) / (nt - 1))
        # projections: closed form + exact correction where chi0's tail meets the structure and beyond
        Gk = jnp.asarray(ew.G(sp, k_np)); Gmk = jnp.asarray(ew.G(sp, -k_np))
        Pp, Pm = self.values(xt)
        e = jnp.exp(1j * jnp.outer(jnp.asarray(xt), k)); Lp = e + r / e; Lm = tp / e
        c0 = jnp.asarray(ew.chi0(sp, xt) * wt)
        cP = Gk + jnp.conj(r) * Gmk + ((jnp.conj(Pp) - jnp.conj(Lp)) * c0[:, None]).sum(0)
        cM = jnp.conj(tp) * Gmk + ((jnp.conj(Pm) - jnp.conj(Lm)) * c0[:, None]).sum(0)
        del Pp, Pm, e, Lp, Lm
        self.aP = w / (2 * pi) * cP; self.aM = w / (2 * pi) * (k / kR) * cM
        self.carried = float((w / (2 * pi) * (jnp.abs(cP)**2 + (k / kR) * jnp.abs(cM)**2)).sum())
        out = cP * t + (k / kR) * cM * rp
        self.T_inf = float((w / (2 * pi) * jnp.abs(out)**2 * (kR / k)).sum())
        T = (kR / k) * jnp.abs(t)**2; g2 = w * jnp.abs(Gk)**2
        self.T_packet_weights = float((g2 * T).sum() / g2.sum())
        self.PL0 = 1 - 0.5 * erfc((xl - ew.x0_of(sp)) / (sqrt(2) * s))
        self.Bo = self.basis(np.asarray(xs_out, float)); self.Bf = self.basis(self.xf)
        el, er = jnp.exp(1j * k * xl), jnp.exp(1j * kR * xr)
        self.fl = (self.aP * (el + r / el) + self.aM * (tp / el), self.aP * 1j * k * (el - r / el) - self.aM * 1j * k * tp / el)
        self.fr = (self.aP * t * er + self.aM * (1 / er + rp * er), self.aP * 1j * kR * t * er + self.aM * 1j * kR * (-1 / er + rp * er))

    def values(self, x):
        """psi+ and psi- on the sorted points x (numpy), as (len(x), nk) device arrays: closed forms left and right of the
        structure, the face-to-face propagator only inside it."""
        k, kR = self.k, self.kR; x = np.asarray(x, float)
        assert np.all(np.diff(x) >= 0), "points must be sorted"
        nL = int((x < self.xl).sum()); nR = int((x > self.xr).sum()); xi = x[nL:len(x) - nR]
        parts_p, parts_m = [], []
        if nL:
            eL = jnp.exp(1j * jnp.asarray(x[:nL])[:, None] * k); parts_p.append(eL + self.r / eL); parts_m.append(self.tp / eL)
        if len(xi):
            sa, sb, sV = self.seg
            si = np.clip(np.searchsorted(sa, xi, side="right") - 1, 0, len(sa) - 1); idx = jnp.asarray(si); F = self.faces
            q = jnp.sqrt(2 * (self.E[None, :] - jnp.asarray(sV[si])[:, None]) + 0j)
            c, s_, _ = _prop(q, jnp.asarray(xi - sa[si])[:, None])
            U1 = c * F[0][idx] + s_ * F[1][idx]; U2 = c * F[2][idx] + s_ * F[3][idx]
            parts_p.append(self.alphaP[0] * U1 + self.alphaP[1] * U2); parts_m.append(self.alphaM[0] * U1 + self.alphaM[1] * U2)
        if nR:
            eR = jnp.exp(1j * jnp.asarray(x[len(x) - nR:])[:, None] * kR); parts_p.append(self.t * eR); parts_m.append(1 / eR + self.rp * eR)
        return jnp.concatenate(parts_p, 0), jnp.concatenate(parts_m, 0)

    def basis(self, x):
        Pp, Pm = self.values(x); return Pp * self.aP + Pm * self.aM

    def chi(self, times, which="out"):
        B = self.Bo if which == "out" else self.Bf
        return B @ jnp.exp(-1j * jnp.outer(self.E, jnp.asarray(times)))

    def lead_pair(self, x0):
        k, kR = self.k, self.kR
        if x0 < self.xl:
            e = jnp.exp(1j * k * x0)
            return (self.aP * (e + self.r / e) + self.aM * (self.tp / e), self.aP * 1j * k * (e - self.r / e) - self.aM * 1j * k * self.tp / e)
        e = jnp.exp(1j * kR * x0)
        return (self.aP * self.t * e + self.aM * (1 / e + self.rp * e), self.aP * 1j * kR * self.t * e + self.aM * 1j * kR * (-1 / e + self.rp * e))

    def _flux_cum(self, times, pairs, dt=0.02, chunk=4000):
        tmax = float(np.max(times)); n = int(np.ceil(tmax / dt)); n += (n % 2 == 1); n = max(n, 2)
        tt = np.linspace(0, tmax, n + 1); h = tmax / n
        F = jnp.stack([c for pr in pairs for c in pr], 1)
        base = jnp.exp(-1j * jnp.outer(jnp.arange(chunk) * h, self.E)); step = jnp.exp(-1j * self.E * chunk * h)
        cur = jnp.ones_like(self.E, dtype=c128); Js = []
        for a in range(0, len(tt), chunk):
            m = min(chunk, len(tt) - a); V = (base * cur) @ F
            Js.append(jnp.stack([jnp.imag(jnp.conj(V[:, 2 * q]) * V[:, 2 * q + 1]) for q in range(len(pairs))], 1)[:m])
            cur = cur * step
        J = np.asarray(jnp.concatenate(Js, 0)); out = []
        for q in range(len(pairs)):
            j = J[:, q]; c = np.zeros(len(tt)); c[2::2] = np.cumsum(h / 3 * (j[0:-2:2] + 4 * j[1:-1:2] + j[2::2]))
            c[1::2] = c[0:-1:2] + 0.5 * h * (j[0:-1:2] + j[1::2]); out.append(np.interp(times, tt, c))
        return out

    def regions_and_tails(self, times, xlo, xhi, dt=0.02):
        rho = jnp.abs(self.chi(times, "fine"))**2
        Pst = np.asarray((self.wf[:, None] * rho).sum(0))
        wm = jnp.asarray(self.well)[:, None]
        Pw = np.asarray((self.wf[:, None] * rho * wm).sum(0))
        cl, cr, clo, chi_ = self._flux_cum(times, [self.fl, self.fr, self.lead_pair(xlo), self.lead_pair(xhi)], dt)
        PL, PR = self.PL0 - cl, cr
        s = self.sp["sx"]; x0 = ew.x0_of(self.sp)
        lo = 0.5 * erfc((x0 - xlo) / (sqrt(2) * s)) - clo; hi = 0.5 * erfc((xhi - x0) / (sqrt(2) * s)) + chi_
        return dict(left=PL, right=PR, well=Pw, struct=Pst, closure=PL + PR + Pst), lo, hi
