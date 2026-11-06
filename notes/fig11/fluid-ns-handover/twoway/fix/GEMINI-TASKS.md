# Tasks for Gemini (paste each one as it stands; bring back the full answer)

## G1: the force on the body in a cut-cell solver (the open decision)
In a 2D cut-cell incompressible flow solver (MAC grid, Batty-style fluid fractions w at each velocity face, explicit viscosity with a
ghost-fluid no-slip link at the body), the viscous flux between two neighbouring faces is nu*(u_q - u_c)/dx^2, applied unweighted. So the
weighted momentum sum(w*u) is not conserved where neighbouring faces have different w. Two ways to define the force on the body:
(A) the body's viscous force is the total change sum(w*du) that the viscous step makes in the fluid, less what the channel walls and ends take
("momentum ledger"); (B) the body's viscous force is only the flux through the ghost links at the body surface.
Which one do published cut-cell or immersed-boundary papers use, and why? Cite only papers you actually opened, with equation numbers (for
example Uhlmann 2005; Nangia et al. 2017; Kempe & Froehlich 2012; Ng, Min & Gibou 2009). Does either rule have a known error of order dx^0
in the force?

## G2: an independent check of my benchmark finding
Schaefer & Turek 1996 benchmark 2D-1 (channel 2.2 x 0.41 m, cylinder D = 0.1 at (0.2, 0.2), parabolic inflow U_max = 0.3, nu = 1e-3).
I found that a zero-gradient condition for the transverse velocity v at the inlet, in place of v = 0, makes c_D about 5 %, the recirculation
length La about 6 % and the pressure drop about 12 % too low at every grid resolution, because the inlet is only 1.5 D ahead of the cylinder.
Is this sensitivity to the inlet's v condition reported anywhere? What do other codes impose for v at this inlet? Estimate, with reasoning,
whether a 5-10 % effect is plausible with the inlet 1.5 D upstream.

## G3: an exact reference for the open test
Derive the force on a fixed circular cylinder, radius a, in a 2D stream oscillating as U(t) = U0 sin(omega t), in unsteady Stokes flow.
Give the part in phase with dU/dt and the part in phase with U, as multiples of rho*pi*a^2*U0*omega, as functions of k*a with
k = sqrt(omega/nu). Show the derivation and evaluate both parts at a = 0.05 m, nu = 1e-3 m^2/s, omega = pi 1/s.
(I have 3.020 in phase and 1.249 in quadrature from Wolfram; I want an independent derivation and number.)
