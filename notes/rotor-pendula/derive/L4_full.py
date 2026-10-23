"""L4: the full equation of the pendulum with a geared generator, shared by L4_check.py, L4_scan.py, L4_resonance.py and
L4_harmonics.py.  Rotor angle tau = Omega t as the time; state per row: theta, theta', E_load, E_paid, E_fric (energies in
units of m L^2 Omega^2, so a power is d/dtau times m L^2 Omega^3).

Motor side (per unit m L^2 Omega^2, motor angle N theta): the torque needed to turn the motor, referred to the pendulum through
an ideal gear, is   x = j theta'' + f0 sgn(theta') + kappa_e theta'
   j = J N^2/(m L^2) (rotor + gearhead input inertia), f0 = N T0/(m L^2 Omega^2) (motor friction), kappa_e = c_e/(m L^2 Omega).
Gearhead (version 3): the loss goes with the power that flows through it, whatever its kind: when power flows from the
pendulum into the motor side (x theta' > 0) the pendulum must supply x/eta; when the motor side gives power back (x theta' < 0,
its rotor slowing down) the pendulum receives eta x.  So the torque on the pendulum is  x k,  k = eta^(-sgn(x theta')).
(Version 2 applied eta to the brake and the friction only, and passed the inertial torque j theta'' without loss: at the
accidental resonance of 400 rpm, 30 %, ratio 51, that let a reactive power of tens of watts flow through the gears for free.)
Pendulum:  theta'' + R sin(theta) + G cos(tau + theta) + k x = 0.
Given theta and theta', h(a) = a + R sin + G cos + k(x(a)) x(a) is increasing in a (k x is increasing in x, x in a; with the
smoothing below, d(kx)/dx >= 1 - |ln eta| max(u sech^2 u) > 0 for eta >= 0.5), so the acceleration is found by bisection followed by Newton steps kept inside the bracket.  sgn is smoothed: sgn(theta') -> tanh(theta'/eps_w),
sgn(x theta') -> tanh(x theta'/eps_p).
"""
import math
import numpy as np

def make_rhs(R, G, j, f0, ke, eta, keep, eps_w, eps_p, nbis=14, nnewt=5):
    """All arguments arrays over rows (or scalars).  keep = 1 - c_e/c_sc (the load's share of the electrical power).
    eta = 1 turns the gear loss off; passing eta_inertia_free=(eta) is not supported: for version 2 use make_rhs_v2."""
    lneta = np.log(eta)
    def F(t, Y):
        th, w = Y[:, 0], Y[:, 1]
        fr = f0*np.tanh(w/eps_w)
        D = R*np.sin(th) + G*np.cos(t + th)
        xr = fr + ke*w                                   # the part of x that does not depend on theta''
        # h(a) rises with slope at least 1 (k x rises with x, x with a), so the root lies within |a| <= |h(0)| <= |D| + |xr|/eta
        B = np.abs(D) + np.abs(xr)/eta + 1e-12
        lo, hi = -B, B
        for _ in range(nbis):                            # narrow the bracket, then Newton steps kept inside it
            mid = 0.5*(lo + hi); x = j*mid + xr
            h = mid + D + x*np.exp(-lneta*np.tanh(x*w/eps_p))
            pos = h > 0
            hi = np.where(pos, mid, hi); lo = np.where(pos, lo, mid)
        a = 0.5*(lo + hi)
        for _ in range(nnewt):
            x = j*a + xr; u = x*w/eps_p; tu = np.tanh(u); k = np.exp(-lneta*tu)
            h = a + D + k*x
            dh = 1 + j*k*(1 - lneta*u*(1 - tu**2))
            a = np.clip(a - h/dh, lo, hi)
        x = j*a + xr
        k = np.exp(-lneta*np.tanh(x*w/eps_p))
        p_paid = k*x*w                                   # power the pendulum gives to the gearhead (in the mean: all losses)
        return np.stack([w, a, ke*keep*w**2, p_paid, fr*w], axis=1)
    return F

def make_rhs_v2(R, G, j, f0, ke, eta, keep, eps_w):
    """Version 2 (for comparison only): gear loss on the brake and the friction, inertia passed without loss."""
    def F(t, Y):
        th, w = Y[:, 0], Y[:, 1]
        fr = f0*np.tanh(w/eps_w)/eta
        a = -((ke/eta)*w + fr + R*np.sin(th) + G*np.cos(t + th))/(1 + j)
        return np.stack([w, a, ke*keep*w**2, (ke/eta)*w**2 + fr*w + j*a*w, fr*w], axis=1)
    return F
