# Self-induced velocity in two-way point-force / actuator-line models: literature dossier

Scout run 6 Nov 2026. Question: how do published methods estimate and remove the self-induced
(self-disturbance) velocity, so that a drag law calibrated for the UNDISTURBED velocity is fed the
undisturbed velocity? Our case: 2D incompressible NS, MAC grid, cell D = 2.5 cm, rods as lines of
point forces, Peskin 4-point kernel (read and spread), drag = resistive-force theory + quadratic
pressure drag, measured drag deficit 3 to 7 percent (glycerol 0.959, honey 0.931, water 0.967),
growing slightly as D is halved. Re per rod diameter: honey ~1, glycerol 10-20, water ~1e4.

## Opening status (what I could and could not read)

| Source | Status |
|---|---|
| Horwitz & Mani 2016 (arXiv 1509.07542) | Opened, full text (PDF to text). Read Secs 1-5 and key equations. |
| Horwitz & Mani 2017 nonlinear drag (arXiv 1703.06966) | Opened, read Secs 1-3 (method, Schiller-Naumann, Re range). |
| Esmaily & Horwitz 2018 (arXiv 1711.08084) | Opened, read Sec 1-2 and Appendix A. |
| Pakseresht, Esmaily & Apte 2020 (arXiv 2004.05311) | Opened, read intro and Kc fit; not the full wall part. |
| Pakseresht & Apte CTR 2022 note | Not opened (TLS fetch failed). |
| Martinez-Tossas & Meneveau 2019 JFM 863 (NSF copy par.nsf.gov/servlets/purl/10106934) | Opened, read Secs 1-3 headlines and equation list only. Not read whole. |
| Martinez-Tossas et al. 2017 (optimal width) | NOT opened. Known only through the 2019 paper's description (eps_opt ~ c/4 for a lifting section, Gaussian). |
| Balachandar, Liu & Lakhote 2019 JCP 376:160 | NOT opened (paywalled). Abstract only (ADS) plus how Balachandar & Liu 2022 (IJMF 104316, text via search highlights) describes it. NB the third author is Lakhote, not "Lakhani". |
| Ireland & Desjardins 2017 | NOT opened. Described by Pakseresht 2020 and Balachandar & Liu 2022 only. |
| Gualtieri, Picano, Sardina, Casciola 2015 | NOT opened. Described by the same secondary sources only. |
| Dag & Sorensen 2020 | NOT opened (no time). |
| arXiv 2503.03467 (steady undisturbed correction near walls, Wendland/Gaussian) | Opened as HTML, math partly stripped; used only for the Oseen-factor validity statement. |

Roads tried: WebFetch (arXiv API, arXiv PDFs saved then pdftotext), WebSearch, Exa web_search_exa,
curl with the agent CA bundle. Not used: Firecrawl, TinyFish, Nimble, Tavily, Consensus (call budget).
I derived and computed the numbers marked DERIVED / COMPUTED below myself; they are not from any paper.

## 1. The shared idea

A point-force model applies force F = F(u_read - v) and spreads -F to the grid. The fluid then
carries a disturbance u_s(x) = response of the flow to the regularised force. What the kernel reads
is u_read = u_inf + u_s. Every method estimates u_s (or a map from u_read to u_inf) and uses
u_inf = u_read - u_s. They differ in how u_s is obtained:

1. Analytic response to a regularised force (Gaussian): Stokes (Ireland & Desjardins; Gualtieri)
   or Oseen (Balachandar et al.).
2. Reverse-engineered grid stencil: u_inf = u + C D^2 laplacian(u) (Horwitz & Mani).
3. Cell-as-a-solid-body ODE, or its algebraic limit (Esmaily & Horwitz; Pakseresht et al.).
4. Filtered lifting-line theory for lift-dominated actuator lines (Martinez-Tossas & Meneveau).

## 2. Source notes

### 2.1 Horwitz & Mani 2016, J. Comput. Phys. 318:85-109
arXiv https://arxiv.org/abs/1509.07542 (preprint "Accurate calculation of Stokes drag for point-particle
tracking in two-way coupled flows").
- Where: Sec 3 (error estimate), Sec 4 eqs (6)-(10), Table 1, Sec 5 (settling tests).
- Establishes: a stationary point particle in uniform flow, Stokes drag evaluated with the disturbed
  velocity underpredicts the force, error O(Lambda), Lambda = dp/dx, "relatively insensitive to Reynolds
  number in the low-Re limit", and Gaussian spreading reduces the error only a little (Fig 3). So
  "convergence of the Gaussian width does not imply convergence of F_d" (their statement, paraphrased).
  Higher-order interpolation (Lagrange-4, splines) is WORSE than trilinear when used with the same
  weights for spreading, because the weights concentrate force near the particle (Sec 5, Fig 14).
- Formula (eq 7, 10a, 10b): u_inf ~ u_p + C(Lambda, x) dx^2 lap(u_p). 3D stencil:
  u_inf = (1-6C) u_p + C (sum of the six neighbours). The 2D stencil is shown "only for illustration":
  u_inf = (1-4C) u_p + C (u_n+u_s+u_e+u_w). C is found by reverse engineering: hold a particle fixed,
  F = 3 pi mu dp u_BC, C = (u_BC - u_p)/(dx^2 lap u_p) (eq 8). Example: C = 0.2477 for Lambda = 1 on
  a face-centred particle (Table 1). C depends on Lambda and the position in the cell, tabulated and
  interpolated (the "C-field").
- Conditions: Stokes drag, Re_p up to about 0.5 in their tests, trilinear kernel, isotropic 3D grid,
  Lambda in [0.01, 1], quasi-steady (large Stokes number; correction tuned to steady state, undershoots at St = 0.25).
  Residual steady error about 5 percent at Lambda = 1.
- Does not establish: anything 2D; any kernel other than trilinear (our Peskin 4-point would need a new C
  table); drag-law nonlinearity beyond Stokes (see 2.2); extended bodies (lines of forces).

### 2.2 Horwitz & Mani 2017, nonlinear drag
arXiv https://arxiv.org/abs/1703.06966 "Correction scheme for point-particle two-way coupling applied
to nonlinear drag law".
- Where: Sec 2.1 eqs 2.1-2.3 (Schiller-Naumann F = (m/tau)(u~ - v)(1 + 0.15 Re^0.687)); Sec 3 results.
- Establishes: using the SAME C coefficients (no retuning) with a nonlinear drag law gives reasonable
  settling prediction for Re_p up to about 10; max steady error about 9 percent at Re_p = 5; at least
  70 percent reduction of velocity error versus trilinear. Explanation offered: Batchelor 1967 point-force
  jet solution has a free parameter alpha = (16/3)/Re_p (low Re) that varies slowly.
- Does not establish: Re_p above 10, Re_p ~ 1e4 (our water), 2D.
- Our case: the drag law enters through u~ only, so the implicit evaluation F = F(u_read - u_s(F)) is
  the logical extension (see Recommendation).

### 2.3 Esmaily & Horwitz 2018, J. Comput. Phys. 375:560
arXiv https://arxiv.org/abs/1711.08084 "A correction scheme for two-way coupled point-particle
simulations on anisotropic grids".
- Where: Sec 2, eqs (4), (5), (7), (8), (13); Appendix A eqs (A.1)-(A.3).
- Formulas: u_f = u_d - u_c (eq 4). The cell velocity obeys (3/2) m_c du_c/dt = -3 pi mu d_c K_t u_c - F
  (eq 5), d_c = diameter of the sphere with the cell volume. Steady limit: u_c = -F/(3 pi mu d_c K_t)
  (A.1). With Stokes drag this gives F = 3 pi mu dp K (u_d - u_p), K = [1 - dp/(d_c K_t)]^-1 (A.2, A.3).
  Crudest isotropic form: divide the Stokes drag by 1 - 0.75 Lambda. K_t = K_c C_r /(K_p C_t) collects:
  K_c cell shape (0.516 for a cube, eq 8 fit), K_p interpolation/spreading (depends on the kernel,
  measured numerically, eq 13), C_r finite cell Reynolds number, C_t exposure time.
  The simple form diverges when d_c K_t -> dp (needs grid about twice the particle).
- Conditions: 3D, Stokes sphere, any interpolation function (K_p is measured per kernel), anisotropic grids.
- Does not establish: 2D (no cell-sphere analogy: 2D Stokes paradox, see section 3); line bodies;
  an explicit Re dependence beyond the factor C_r (given only through a fitted correlation I did not read in full).

### 2.4 Pakseresht, Esmaily & Apte 2020
arXiv https://arxiv.org/abs/2004.05311 "A general velocity correction scheme for two-way coupled
point-particle simulations".
- Establishes (intro): the model handles arbitrary interpolation and distribution functions and
  anisotropic grids, adds wall corrections (K_c,w, eqs 11-15). Summary of literature ranges given there:
  Pan & Banerjee 1996 and Maxey & Patel 2001 limited to Re_p < O(0.1); Horwitz & Mani to Re_p < 10 and
  Lambda = O(1) (their reading); Ireland & Desjardins unbounded and small Re_p; Balachandar et al. 2019
  Re_p < 200 (their reading, not verified by me).
- Does not establish: 2D.

### 2.5 Balachandar, Liu & Lakhote 2019, J. Comput. Phys. 376:160-185 (abstract only)
doi 10.1016/j.jcp.2018.09.033. Abstract (ADS): exact solution of Oseen's equation for steady Gaussian
feedback force plus finite-Re simulation gives a steady model for u_s; the unsteady problem solved at
zero Re, extended to finite Re by simulation; two parameters, Re_sigma (Reynolds number on Gaussian width)
and a non-dimensional force; quasi-steady and unsteady versions tested on a settling particle.
- Via Balachandar & Liu 2022 (IJMF 104316): the correction is implicit (iterate three to four times),
  the unsteady part is a convolution over force history with a kernel function of delay time and Re_sigma,
  unsteady correction needed only for rapid force variation, resolution needed D <= sigma/2 for 2nd-order
  finite differences (D <= sigma spectral), generalises to other spreading functions by re-deriving the
  Oseen response (analytic or numerical "Oseenlet", their Algorithm 2a). Vector form handles forces not
  aligned with the relative velocity.
- I did NOT read the formulas. In 3D Stokes limit the Gaussian result is (DERIVED by me, matches the
  known force-coupling result): u_s = F/(6 pi^(3/2) mu sigma), so with Stokes drag u_inf = u_read/(1 - dp/(2 sqrt(pi) sigma)).
- Does not establish (as far as I can tell from the abstract): 2D.

### 2.6 Ireland & Desjardins 2017; Gualtieri et al. 2015 (not opened)
Per Pakseresht 2020 and Balachandar & Liu 2022: Ireland & Desjardins use the steady Stokes solution of a
Gaussian feedback force (unbounded, small Re_p, includes particle volume displacement); Gualtieri et al.
("exact regularised point particle") solve the unsteady Stokes equation with a Gaussian, including walls,
and need a large precomputed stencil. Both are Stokes (Re -> 0) and 3D. I cannot give formulas from them.

### 2.7 Martinez-Tossas & Meneveau 2019, J. Fluid Mech. 863:269-292
https://par.nsf.gov/servlets/purl/10106934 (author copy). doi 10.1017/jfm.2018.994.
- Where: eq 2.2 (3D Gaussian kernel eta_eps = exp(-r^2/eps^2)/(pi^(3/2) eps^3)), Sec 3 (3.5 to 3.10
  filtered induced velocity), eq 4.x (eps_opt ~ 0.25 chord).
- Establishes: for LIFT forces on a wing, Gaussian-filtering the lifting line reduces the induced
  velocity at the blade; the missing part is an integral of the spanwise circulation gradient with a
  smoothing function that depends on eps (3.9, 3.10); correct it by adding the difference between the
  unfiltered and filtered induced velocity (a "regularisation correction"), so the optimal eps ~ c/4 is
  no longer needed. The velocity is inviscid, from vorticity transport and Biot-Savart.
- Does not establish: drag forces, viscous or finite-thickness bodies, 2D, Peskin kernels. The approach
  removes the regularisation-specific part of the 3D tip-vortex induction, not the model's total
  self-velocity. Its idea (subtract the regularised-minus-singular induced velocity) is the
  conceptual cousin of the Stokes/Oseen approaches.
- Dag & Sorensen 2020 and Martinez-Tossas 2017: not opened. Say so in any citation.

## 3. Applicability to our three constraints

(a) 2D. None of the sources treats 2D. The Stokes/Gaussian formulas are 3D (u_s ~ F/(mu sigma)). In 2D
Stokes the isolated point force gives u_s = (F/(4 pi mu))(ln(L/sigma) + c), log divergent with domain size
(Stokes paradox). The Oseen cut-off l_O = nu/U cures it: ln(L/sigma) is replaced by ln(l_O/sigma) + const,
so the self-velocity depends on nu/(U sigma). This is the same cut-off that makes the physical drag of a
2D cylinder finite (Lamb: F = 4 pi mu U/(1/2 - gamma - ln(Re_a/8)), Re_a = U a/nu). Reasoning only (not
computed here, not from a source): the free-stream-referenced drag and the point-force self-velocity share
the same logarithm, so their difference should depend on kernel width over body radius, not on Re.
(b) Drag-dominated bodies. Horwitz & Mani, Esmaily, Balachandar are all drag (Stokes + finite-Re
correlation) models, so they fit. Filtered lifting line is for lift. Balachandar & Liu 2022 added lift
and added mass through a vector form.
(c) Compact kernel. Esmaily/Pakseresht (K_p measured per kernel) and Balachandar (Oseenlet re-derived or
measured numerically) are explicitly kernel-agnostic. Horwitz & Mani's C table is for trilinear only.

## 4. COMPUTED: linearised 2D Oseen self-velocity for our kernel (not from a paper)

Model: steady linearised Oseen about uniform U, density rho, viscosity nu, 2D force F per unit depth
along the stream, spread and read with the same Peskin 4-point kernel g(x,y) = phi(x/D) phi(y/D)/D^2,
continuous kernel, no grid operators. Fourier solution (e^{ik.x}):
  u_hat = F g_hat (1 - kx^2/k^2) / (rho (nu k^2 + i U kx)),
  u_read = integral d^2k/(2 pi)^2 |g_hat|^2 (1 - kx^2/k^2) F nu k^2 / (rho (nu^2 k^4 + U^2 kx^2)).
Script: scratchpad/os2.py (not committed). Checks passed: int phi dr = 1, int phi^2 dr = 3/8 exactly
(the Peskin sum-of-squares property); the high-Re limit equals 3/16 (below).

Isolated point force, Re_D = U D/nu. Table gives u_read/U per unit F~ = F/(rho U^2 D):

| Re_D | 0.1 | 1 | 3 | 10 | 30 | 100 | 1000 | 12500 |
|---|---|---|---|---|---|---|---|---|
| u_s/U per F~ | 0.028 | 0.108 | 0.151 | 0.175 | 0.183 | 0.186 | 0.1874 | 0.1875 |

High-Re closed form (DERIVED, checked by the table): drop viscosity and pressure, rho U du/dx = F g, then
u_read = (F/(rho U)) (1/2) integral g_y^2 dy = (3/16) F/(rho U D). So u_s/U = (3/16) F/(rho U^2 D)
= (3/16) F~. This is the plume/wake effect: the fluid passing the kernel gains the momentum deficit.
Scaling with 1/D explains the deficit rising when D is halved.

Line of forces (rod), continuous line load f per length, rod length L = 24 D (0.6 m), read at the rod centre,
u_c/U per f~ = f/(rho U^2) (in D units, per unit depth):

| Re_D | 1 | 10 | 100 | 12500 |
|---|---|---|---|---|
| rod ACROSS the stream | 0.4995 | 0.500 | 0.500 | 0.500 |
| rod ALONG the stream | 1.54 | 3.27 | 4.29 | 4.50 |

Across the stream the result is the 2D actuator-disc one: the load is a pressure jump, and the rod's own
induction is f/(2 rho U) = Delta p/(2 rho U), independent of kernel and of nu. So for a rod across the
flow the self-induced velocity is set by the ROD LOAD, not by the kernel width. Along the stream it
grows with L (numbers are for L = 24 D). Caveats: unit depth ambiguity (f in N/m needs the depth h the
solver uses: Delta p = f/h); linear theory (u_s << U); no discrete operators; Peskin read at the centre point only.

Honest limit: I have not reproduced the measured 0.959/0.931/0.967. That needs f, h, rod orientation
from the lead's code. If the across-flow disc formula gives u_s/U = f/(2 rho U^2 h) with the rod's actual
drag, it should land in the 3-7 percent range; if it does, the deficit is mostly the physical blockage of
the modelled rod, and the question becomes whether that part SHOULD be removed (see Open questions).

## 5. Recommended correction for our case (2D, Peskin 4-point, Stokes + quadratic drag)

Do not use the 3D formulas (1 - 0.75 Lambda; 1/(1 - dp/(2 sqrt(pi) sigma))); they have the wrong 2D scaling.
Use the Esmaily/Balachandar logic with a 2D, Peskin-specific Oseen influence:

1. Linear self-influence. For rod points i = 1..N with forces F_i = f_i ds_i (per unit depth), the
   self-induced velocity at point i is u_s,i = sum_j M_ij F_j, where M_ij is the Oseen response of the
   2D flow at x_i to a Peskin-regularised unit force at x_j, read with the same kernel:
     M(x_i - x_j) = integral d^2k/(2 pi)^2 e^{ik.(x_i - x_j)} g_hat(k)^2 [I - k k^T/k^2] / (rho (nu k^2 + i U.k)),
   U = the local undisturbed velocity (iterate). In the isotropic far-field it reduces to the table in
   section 4. Tabulate M once per (Re_D, direction of U) or build M numerically by running the solver
   with a unit force held in uniform flow (Balachandar & Liu "Algorithm 2a"; Esmaily K_p measured). The
   numerical route also captures the MAC grid and discrete operators (the continuous integral does not).
2. Implicit fixed-point iteration each step (Balachandar & Liu: three to four iterations):
     u_inf,i^(k) = u_read,i - sum_j M_ij F_j^(k-1),   F_j^(k) = F_drag( v_j - u_inf,j^(k) ).
   Start from F^(0) = F_drag(v - u_read). Because the drag law is nonlinear (quadratic pressure drag),
   the Newton form is safe: F^(k) = F_drag(w_read) / (1 + A_i) style factors fail when A_i ~ 1.
3. Scalar shortcut for the Stokes part only (Esmaily A.2/A.3 analogue): with F = c w_true, w_true =
   w_read/(1 - c m) where m = M_ii (the diagonal gain, units velocity per force). For an isolated point
   m = 0.1875/(rho U D) at high Re and the table values lower; for a rod include the line sum.
4. Quasi-steady only. Unsteady correction (Balachandar convolution) matters if the force changes
   in less than about a viscous or advective time over the kernel: tau_adv = 4 D/U = 0.2 s at 0.5 m/s;
   rods that sweep faster than that need it.
5. Validation test (three-way, as the house method demands): hold the rod still in a uniform stream,
   compare drag/drag_law before and after the correction; vary D (2.5, 1.25 cm) and orientation (across,
   along, 45 degrees); the corrected ratio must be 1 +/- 1 percent for all three fluids.

## 6. Open questions
1. Should the rod's finite-length blockage (the 2D actuator-disc term f/(2 rho U h)) be removed? A real
   rod of 2 cm thickness also slows the fluid around it, and a free-stream-referenced drag law already
   absorbs the real rod's own near-field; the model's disc-like induction is not the same as the real
   body's. Literature (Esmaily, Balachandar, Martinez-Tossas) removes the regularisation-specific part for
   point or thin bodies; for extended bodies the right reference is unsettled. Test it with a resolved
   2D cylinder or flat plate run (Re ~ 1, 10, 1e3).
2. What is the depth h implied by "force per metre" in the 2D solver? It fixes the amplitude of every number above.
3. MAC-grid discretisation: continuous-kernel numbers (section 4) need a numerical check against the
   solver; second-order central differences need D <= sigma_eff/2 in Balachandar & Liu, and a 4D kernel
   with D = 2.5 cm is borderline.
4. Re ~ 1e4 (water): Oseen linearisation fails when the wake is turbulent or shed; the deficit then
   needs measurement, not theory. Horwitz & Mani show reasonable results only to Re_p ~ 10; Balachandar
   claims Re_p up to a few hundred (unverified).
5. Nonlinearity: with u_s/U of 5-7 percent linear Oseen should be accurate to about 10-20 percent of u_s
   itself; with the iteration this is a second-order error in the drag.
6. Unread sources (Balachandar 2019 formulas, Ireland & Desjardins, Gualtieri, Dag & Sorensen, Martinez-Tossas 2017):
   obtain the PDFs before quoting their numbers.
