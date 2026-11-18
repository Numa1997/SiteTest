# Fig. 15 before the correction: theory and its one-to-one map onto the earlier sessions' code

Companion to `THEORY_AND_CODE.md` (the correction). This file covers the code the earlier sessions (13–14 Nov) wrote in
`tools/kaggle/resonant-tunnelling/`, the physics each file implements, and what in it later proved wrong. Line numbers refer to branch
`claude/fig15-correction` at commit d5f9f1c. Nothing was run to write this file. Fact / Inference / Opinion as before.

Units: ħ = m = 1, lengths in a, energies in E_u = ħ²/(m a²). The site's real-units panel (`real_units.py`) anchors V₀ = 3 to the GaAs/AlGaAs
band offset 0.30 eV, so E_u = 0.10 eV with m* = 0.067 m_e; then a = ħ/√(m* E_u) ≈ 3.37 nm (Inference: my arithmetic from those two numbers).
Generation 2 uses V₀ = 2, so the same anchor would give 0.20 eV barriers.

The order in which the methods appeared (Fact, `HISTORY_COMMITS.txt`):
1. Step B1: read the single-barrier t(k), r(k) off Fig. 14's stored runs (`extract_t.py`, `b1_first.py`, `b1_survey.py`).
2. Step B3: generation 0, a 1D reconstruction by scattering states (`recon.py`, file format RTF1, `pack.py`); later replaced.
3. Step B4: an independent Crank–Nicolson solve to check B3 (`cn.py`, `check_cn.py`), and the diode current (`iv.py`).
4. Generation 1: 115 3D runs on Kaggle (`rt3d.py`, `rt3d_run.py`, `file_rt3d.py`), checked against `exact1d.py`.
5. Generation 2: 3,697 3D runs (`rt3d2.py`, `rt3d2_run.py`, `file_rt3d2.py`), live on the page since 14 Nov 10:04 UTC.

---------------------------------------------------------------------------------------------------------------------------
## 1. Transfer matrices for flat steps (`tm.py`)

**Picture.** Cut the barrier landscape into flat slabs. In each slab the wave is a sum of a right-mover and a left-mover. At each edge
the wave and its slope must join smoothly, like two ropes spliced without a kink. Those joining rules are 2 × 2 matrices; multiplying them
across the structure carries the wave from one side to the other.

**Derivation.** In region j (potential V_j on [x_j, x_{j+1})), ψ = A_j e^{iq_j(x−x_j)} + B_j e^{−iq_j(x−x_j)}, q_j = √(2(E − V_j)), imaginary
below the step. Continuity of ψ and ψ' at an edge between q₁ (left) and q₂ (right), in local coordinates at the edge:

$$ \begin{pmatrix}1&1\\q_1&-q_1\end{pmatrix}\begin{pmatrix}A_1\\B_1\end{pmatrix} = \begin{pmatrix}1&1\\q_2&-q_2\end{pmatrix}\begin{pmatrix}A_2\\B_2\end{pmatrix}
\;\Rightarrow\; \begin{pmatrix}A_1\\B_1\end{pmatrix} = \frac12\begin{pmatrix}1+q_2/q_1 & 1-q_2/q_1\\ 1-q_2/q_1 & 1+q_2/q_1\end{pmatrix}\begin{pmatrix}A_2\\B_2\end{pmatrix}. \qquad (1.1)$$

Moving the reference point back across a flat stretch L: (A, B) → (A e^{−iqL}, B e^{iqL}). Starting with (1, 0) in the last region
(outgoing only) and stepping left gives the left amplitudes; t = e^{−ikx_N}/A, r = B/A with the global phase convention that refers t
and r to x = 0. When E = V exactly the code nudges E − V to 1e-12 so the edge matrix stays finite.

| Item | Code (`tm.py`) |
|---|---|
| q_j, nudge at E = V | `q_of` :7–12 |
| (1.1) edge matrix | `edge` :14–16 |
| flight across L | `flight` :18–20 |
| regions covering the line | `layers` :22–30 |
| t, r, all region amplitudes | `solve` :32–49 |
| ψ_k(x) on points | `psi_x` :51–61 |
| a symmetric double barrier | `double` :63–65 |

## 2. Step B1: reading t(k), r(k) from stored runs (`extract_t.py`, `b1_first.py`, `b1_survey.py`)

**Picture.** Once the transmitted packet has left the barrier, it is just the incoming chord with each tone multiplied by t(k). Take
its Fourier transform, divide by the known incoming spectrum and the free phase, and t(k) falls out.

**Derivation.** For a packet starting left of a slab, right of the slab
χ(x,t) = (2π)^{−1/2} ∫ φ(k) t(k) e^{ikx − ik²t/2} dk; so FT_{x > a/2}[χ](k) = φ(k) t(k) e^{−ik²t/2}, and t(k) = FT / (φ e^{−ik²t/2}).
Left of the slab, the same at −k gives r(k). The reference is the exact slab solution from the four matching equations.

| Item | Code (`extract_t.py`) |
|---|---|
| read Fig. 14's SPHC files | `read_sphc` :24 |
| exact t, r of a slab (4 × 4 linear solve) | `exact_tr` :46–63 |
| χ from the stored cut ψ = χ g(ρ) g(0) | `chi_from_cut` :65 |
| Fourier division | `extract` :82; least-squares variant `extract_ls` :112 |
| error split into solver, window, 8-bit levels | `b1_first.py` (docstring A–D) |
| survey over all stored flat runs | `b1_survey.py` |

## 3. Generation 0: the 1D reconstruction (`recon.py`, `pack.py`)

**Picture and derivation.** The same stationary-state superposition as the correction's walls (`THEORY_AND_CODE.md` §3), but with one
family only. With V ≥ 0 there are no bound states, and a packet that starts wholly left of the barriers and has no k < 0 part is

$$ \psi(x,t) = (2\pi)^{-1/2}\int_0^\infty \varphi(k)\,\psi_k(x)\,e^{-ik^2t/2}\,dk,\qquad
\varphi(k) = (2\pi s_0^2)^{-1/4}\sqrt2\,s_0\,e^{-s_0^2(k-k_0)^2}e^{-i(k-k_0)x_0}. \qquad (3.1)$$

It neglects the start packet's tail inside the barriers and its k < 0 part; both were measured and stored. ψ_k comes from `tm.py`.
Fact (`pack.py` docstring): these runs used V₀ = 3 and were later replaced on the page by generation 1, because the figure was to be
3D. The derived exact 1D numbers survive as checks.

| Item | Code |
|---|---|
| (3.1) φ(k) | `recon.py:28` `phi` |
| T(E), resonances | `recon.py:33` `T_of_E`, `:37` `resonances` |
| one run (frames on the stored window and zoom) | `recon.py:65` `run` |
| packing into the site tree with parents | `pack.py` |

## 4. Step B4: the Crank–Nicolson check (`cn.py`, `check_cn.py`)

**Picture.** A completely different machine for the same motion: step the wave forward in small time steps on a fine grid. If the two
machines agree frame by frame, both are right.

**Derivation.** Crank–Nicolson: (1 + iHdt/2) ψ^{n+1} = (1 − iHdt/2) ψ^n. The Cayley form (1 + iHdt/2)^{−1}(1 − iHdt/2) is exactly
unitary for Hermitian H, and second order in dt. H = −½∂²_x + V with the fourth-order stencil (−1, 16, −30, 16, −1)/(12 dx²). The faces do
not lie on grid points, so each point carries V averaged over its cell [x − dx/2, x + dx/2], second order in the face position. Box far
larger than the flight, ψ = 0 beyond.

| Item | Code (`cn.py`) |
|---|---|
| cell-averaged V | `cell_potential` :12–18 |
| box, start packet, cell-averaged V | `run` :20–27 |
| fourth-order stencil into a banded H, plus V | :28–32 |
| A = 1 + iHdt/2, B = 1 − iHdt/2 | :33–34 |
| banded solve per step | `solve_banded` (later in `run`) |
| frame-by-frame L2 comparison with recon | `check_cn.py` |

## 5. The diode under bias (`iv.py`, `real_units.py`)

**Picture.** A voltage tilts the landscape. Electrons pour in from a sea filled up to the Fermi energy on the left; the current is how many
of them find the resonance window open as the tilt slides the resonance down past the sea.

**Derivation.** Under bias V_b the potential is the barriers plus a linear drop across the device (emitter 0, collector −V_b). The ramp is cut
into n_per flat cells per piece (barrier, well, barrier), keeping the four faces as exact edges, and composed with (1.1). With unequal leads the
current-conserving transmission is

$$ T = \frac{\mathrm{Re}\,q_R}{q_L}\,|t|^2. \qquad (5.1)$$

Tsu & Esaki (Appl. Phys. Lett. 22, 562 (1973)) current per area:

$$ J(V) = \frac{e\,m^*k_BT}{2\pi^2\hbar^3}\int_0^\infty T(E_x,V)\,N(E_x,V)\,dE_x,\qquad
N = \ln\frac{1+e^{(E_F-E_x)/k_BT}}{1+e^{(E_F-E_x-eV)/k_BT}}. \qquad (5.2)$$

Assumptions (stated in the code): coherent transport, linear drop (no charge build-up), parabolic bands, thermal Fermi seas.

| Item | Code (`iv.py`) |
|---|---|
| staircased ramp, composed transfer matrices, (5.1) | `T_biased` :24–47 |
| vectorised | `T_biased_vec` :49 |
| (5.2) supply function N | `supply` :77–79 |
| J(V) curve | `iv_curve` :82 |
| prefactor and real units | `real_units.py` |

## 6. The exact 1D reference numbers (`exact1d.py`)

For walls the 3D wave separates (`THEORY_AND_CODE.md` §2), so the 1D transfer-matrix numbers are exact for 3D walls up to the grid.
`exact1d.py` writes T(E) of the pair and of one barrier, the packet average T̄(E) = ∫|φ|²T dk / ∫|φ|² (σ_k = 1/(2σ₀)), the resonances
(E_r; Γ from the full width at half height; τ = 1/Γ), the diode curve and the real-units block.

| Item | Code (`exact1d.py`) |
|---|---|
| T(E) | `T_of` :24 |
| T̄(E) | `tbar` :28 |
| resonances, Γ, τ | `resonances` :37 |
| output file | `main` :55 |

## 7. Generations 1 and 2: the 3D split-step solver (`rt3d.py`, `rt3d2.py`)

**Picture.** The 3D wave lives on a lattice of points 0.5 a apart. Each tick, it is pushed half a tick by the potential (a phase twist at
each point), a full tick by free flight (done exactly in Fourier space), and another half tick by the potential. Near the box walls a soft
mask dims the wave so that it does not come back.

**Derivation.** Strang splitting, as in `THEORY_AND_CODE.md` (7.1), here with the 3D FFT for the kinetic step:

$$ \psi \leftarrow e^{-iVdt/2}\,\mathrm{IFFT}_3\big[e^{-i(k_x^2+k_y^2+k_z^2)dt/2}\,\mathrm{FFT}_3\,(e^{-iVdt/2}\psi)\big],\quad
\psi \leftarrow m(x)m(y)m(z)\,\psi, \qquad (7.1)$$

m = sin^{1/8}(πe/(2W)) on the outer W = max(4, n/10) points of each axis. V = V₀ on the points strictly inside a barrier, plus the bias ramp.
Barrier centres are placed so every face lies on an odd multiple of 0.25 a (a cell boundary of the 0.5 a grid). Run length: the trailing
edge's flight to 20 a past the last face plus three lifetimes of the longest-lived resonance in the packet's window (from the 1D T(E)).
Storage: the plane z = 0, y ≥ 0, |ψ| and arg ψ as 8-bit levels of each frame's own peak; the x-profile; region probabilities.

The walls also carry a 1D twin: the same scheme in 1D (complex128) on the same x axis and mask. Its "transmitted" and "reflected" add the
mask's absorption, split at x = 0.

| Item | Code (`rt3d2.py`; generation 1 has the same structure in `rt3d.py`) |
|---|---|
| grid 0.5 a, k grids, masks, K² | `setup` :19–29 (mask :23–24) |
| face-aligned barrier centres | `centres` :32–39 |
| extent, x₀ | `extent` :42–47, `x0_of` :50–51 |
| bias ramp | `vbias` :59–62 |
| barrier and region masks (walls, discs, shells) | `geometry` :65–81 |
| resonance lifetime for the run length | `tau_est` :84–98, `t_end_of` :101–105 |
| start packet, normalised on the grid | `run` :111–113 |
| V on points | :114–117 |
| (7.1) half-V, kinetic, half-V, mask | :120–122, step :129–131 |
| probability, x-profile, regions, slice | `measure` :134–140 |
| 8-bit levels | :147–149 |
| the 1D twin | `run1d` :159–178 (losses split at x = 0 :174–175, T and R :177–178) |
| job list, groups A–G | `rt3d2_run.py:37–66` `jobs` |
| loader notebooks | `build_rt3d2.py`, `rt3d2_*.ipynb` |

## 8. The numbers the page reads (`file_rt3d.py`, `file_rt3d2.py`)

T_far (`file_rt3d2.py:48–62`): at the last frame before 1e-3 of the wave reaches the end borders,
T_far = (P_right + P_well/2)/P_box; half of what is trapped counts as leaving forwards; dividing by P_box removes what the side border took.
τ: slope of a straight-line fit of ln P_in(t) where P_in has fallen from 60 % to 5 % of its peak (`fit_tau` :36–45).
Diode: J(V) = ∫ T N dE by the trapezoid rule over the 25 stored energies, with T the 1D twin for walls and T_far for discs (`:120–134`).
Exact 1D curves for every unbiased wall structure, T and T̄ (`:136–149`).

## 9. What was wrong in this code, and why (Fact where measured, Inference where explained)

| # | Where | What | Physics of the failure | Measured |
|---|---|---|---|---|
| 1 | `rt3d2.py:117` (and `run1d` :164) | V₀ only on points strictly inside a barrier, 0.5 a apart (D1) | Inference: a 1 a barrier is 2 points. Under the barrier the wave decays like e^{−κx}, κ = √(2(V₀ − E)) ≈ 1.7 /a at V₀ = 2, E = 0.5, so it falls by e^{−0.87} per point; two points cannot hold that decay, and the barrier the scheme feels is not the intended one. Resonances, which depend on the phase picked up between the barriers, shift. | Fact: 918 / 1,088 walls and 1,582 / 2,327 discs fail the gate; median wall error 0.0136, largest 0.435 |
| 2 | `rt3d2.py:23–28` side masks | the side border absorbs the trapped wave (D2) | the trapped wave spreads sideways while it rings; the mask eats it, so P_in decays faster than by leaking | lifetimes too short (brief §3) |
| 3 | `rt3d2.py` whole run, complex64 | norm lost from t = 0 (D4) | cause not found; the kinetic factor's rounding explains 1/140 of it | 0.46 % by t = 90 |
| 4 | masks | reflection from the mask grows as 1/dt (D5) | the mask is an imaginary potential −ln(m)/dt; a taller, steeper absorber reflects more | 2D wall test: +0.004 (dt 0.01), +0.014 (dt 0.0025) at box 96 a |
| 5 | `rt3d.py` version 1 (13 Nov) | single wall and disc centred at x = 0 | `|x| < D/2` held one grid point: half the intended thickness | Fact (`file_rt3d.py` docstring): those runs were not filed; `fig15-rt3d-singles-v2` replaced them |
| 6 | `file_rt3d2.py` T_far under bias | T_far reads low under bias | the faster transmitted wave reaches the end border while some is still trapped | Fact (docstring :19–20); the diode used the 1D twin for walls |
| 7 | `file_rt3d2.py` shells | no transmission number for shells | only "core, gap, out" regions are stored; "out" includes the reflected wave | the correction could not judge stored shells (`THEORY_AND_CODE.md` §10.2) |

What held up (Fact, from the correction): the stationary-state method of generation 0 (`recon.py`) is the same method the correction used for
the walls, and the correction's exact walls agree with `tm.py` transfer matrices to 3e-7. The transfer matrices, the Tsu–Esaki formula and the
exact 1D numbers are not in question; the 3D split-step runs (generations 1 and 2) are.
