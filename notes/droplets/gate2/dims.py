"""Tiny dimension checker: a quantity is a (M, L, T) exponent vector. Used by the Gate 2 scripts."""
import sympy as sp
class D:
    def __init__(s, M=0, L=0, T=0): s.v = (sp.Rational(M), sp.Rational(L), sp.Rational(T))
    def __mul__(s, o): return D(*[a + b for a, b in zip(s.v, o.v)])
    def __truediv__(s, o): return D(*[a - b for a, b in zip(s.v, o.v)])
    def __pow__(s, n): return D(*[a * n for a in s.v])
    def __eq__(s, o): return s.v == o.v
    def __repr__(s):
        names = 'kg m s'.split(); parts = []
        for n, e in zip(names, s.v):
            if e != 0: parts.append(f'{n}^{e}' if e != 1 else n)
        return ' '.join(parts) if parts else '1 (dimensionless)'
ONE = D(); kg = D(1); m = D(0, 1); s = D(0, 0, 1)
mass, length, time = kg, m, s
speed = m / s; accel = m / s ** 2; force = kg * m / s ** 2; energy = force * m
dens = kg / m ** 3; visc = kg / (m * s); sigma = force / m  # N/m
nu = m ** 2 / s; eps = m ** 2 / s ** 3
def same(label, a, b):
    ok = (a == b); print(f'  units  {label}: {a}  vs  {b}  ->  {"OK" if ok else "MISMATCH"}'); return ok
