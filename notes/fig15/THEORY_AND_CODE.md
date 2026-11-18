# Fig. 15 correction: the theory, derived, and its one-to-one map onto the code

Scope: everything the correction session (14–15 Nov 2026) computed: the exact wall runs, the axisymmetric (x, rho) disc and shell
runs, the comparison with the stored runs, and the checks. For each piece the physical picture comes first, then the derivation, then a
table mapping each equation to the file, function and line that implements it. Line numbers refer to branch `claude/fig15-correction`
at commit 10bd476. Where the code departs from the theory, or the theory was applied wrongly, it says so in a box marked **Defect**.

Units throughout: ħ = m = 1, lengths in the grid unit a. Energy unit ħ²/(m a²), time unit m a²/ħ. Example only (not the site's
choice): an electron with a = 1 nm gives an energy unit of 76.2 meV and a time unit of 8.64 fs.

Contents
1. The problem and the stored solver
2. Walls: separation of variables
3. Walls: the 1D problem solved by stationary scattering states
4. Walls: the observables (T, regions, fluxes, the 3D frames)
5. Walls: the batched GPU implementation
6. Discs and shells: reduction to (x, rho)
7. Discs and shells: the split-step scheme with the Hankel transform
8. Discs and shells: potential, borders, observables, T
9. Precision, convergence and the smoke tests
10. Comparison with the stored runs (gate, T_far, classification)
11. The file format (RT3C) and what the page reads
12. Defects found, in one list

---------------------------------------------------------------------------------------------------------------------------
## 1. The problem and the stored solver

**Picture.** A ripple of electron wave, a Gaussian packet about 3 a wide, runs along x into a row of thin, hard barriers, like a ball
of light into a stack of half-silvered mirrors. Most of it bounces back. But at certain energies the wave fits a whole number of
half-wavelengths between two barriers. It then rings in the gap like a struck glass, builds up, and leaks through in a slow trickle.
That is resonant tunnelling. The figure shows this in 3D for three kinds of obstacle: walls (barriers across the whole cross-section),
discs (barriers of finite radius on the axis) and shells (spherical barriers around the origin).

**Equation.** The time-dependent Schrödinger equation

$$ i\,\partial_t \psi(\mathbf r,t) = \Big[-\tfrac12\nabla^2 + V(\mathbf r)\Big]\psi(\mathbf r,t), \qquad (1.1)$$

with the start packet (product of three Gaussians, centred at x₀, wave number k₀ = √(2E) along x)

$$ \psi_0 = \chi_0(x)\,g(y)\,g(z),\quad \chi_0(x) = (2\pi s_x^2)^{-1/4} e^{-(x-x_0)^2/(4 s_x^2) + i k_0 x},\quad
g(y) = (2\pi s_\perp^2)^{-1/4} e^{-y^2/(4 s_\perp^2)}. \qquad (1.2)$$

Barriers of height V₀ and thickness D, N of them at pitch P; x₀ = (first face) − max(14, 4 s_x). A bias B adds a linear drop across
the structure: V → V − B (x − x_l)/(x_r − x_l) for x_l ≤ x ≤ x_r, and −B beyond x_r.

**The stored solver** (`tools/kaggle/resonant-tunnelling/rt3d2.py`, generation 2): 3D Strang split-step on a 0.5 a grid, dt = 0.01,
complex64, mask sin^(1/8) on the outer tenth of each axis (rt3d2.py:24–28). Its defects, measured before this session (brief §3):
D1 a barrier of thickness 1 a is 2 grid points, so the barrier is drawn wrong and resonances move; D2 the side mask eats the
trapped wave; D4 norm lost from t = 0; D5 the mask reflects, more for smaller dt (see §8.3). The correction replaces this solver by
methods that do not sample the barrier on a 0.5 a grid at all (walls) or sample it 8–16 times finer and exactly in cell averages
(discs, shells).

## 2. Walls: separation of variables

**Picture.** A wall is uniform across y and z, like a pane of glass that fills the whole corridor. Nothing in the problem then pushes the
wave sideways. Sideways, the packet spreads exactly as it would in empty space, and all the interesting physics happens along x.

**Derivation.** If V = V(x) only, the Hamiltonian splits: H = H_x + H_y + H_z with H_y = −½∂²_y. A product start ψ₀ = χ₀ g g stays a
product for all time, because e^{−iHt} = e^{−iH_x t} e^{−iH_y t} e^{−iH_z t} (the three parts commute):

$$ \psi(x,y,z,t) = \chi(x,t)\,h(y,t)\,h(z,t). \qquad (2.1)$$

h is the free evolution of the Gaussian g (solve i∂_t h = −½h'' with h(y,0) = g(y); Fourier transform, multiply by e^{−ik²t/2},
transform back):

$$ h(y,t) = (2\pi s_\perp^2)^{-1/4}\,a^{-1/2}\exp\!\Big(-\frac{y^2}{4 s_\perp^2 a}\Big),\qquad a = 1 + \frac{i t}{2 s_\perp^2}. \qquad (2.2)$$

∫|h|²dy = 1 at all t, so every probability of the 3D problem is the matching probability of χ. The whole 3D wall problem is the 1D
problem i∂_tχ = [−½∂²_x + V(x)]χ, χ(x,0) = χ₀.

| Eq. | Code |
|---|---|
| (2.2) h(y,t) | `exact_wall.py:264` `h_free(y, t, s)` |
| (2.1) the 3D field on the stored slice z = 0, y ≥ 0 | `wall_gpu_run.py:67–68` `Hy = h_free(0.5·[0..63], t, s⊥)`; `slab = chi[x] · Hy[y] · Hy[z=0]` |

## 3. Walls: the 1D problem solved by stationary scattering states

**Picture.** A packet is a chord of many pure tones (plane waves of different k). Each pure tone meets the barriers and splits for ever
in the same way: a fixed share bounces, a fixed share goes through, and a standing pattern sits inside. If we know, for every tone,
the full stationary wave across the structure, the packet at any time is just these tones added up, each with its own clock e^{−iEt}.
There is no time step and no grid, so neither the barrier sampling (D1) nor a border (D2, D5) can enter.

### 3.1 The two scattering families
For E = k²/2 > 0 (k the wave number on the left; on the right, under bias B, k_R = √(k² + 2B)) two independent stationary solutions:

$$ \psi^+_k(x) = \begin{cases} e^{ikx} + r\,e^{-ikx} & x<x_l\\ t\,e^{ik_Rx} & x>x_r\end{cases}\qquad
\psi^-_k(x) = \begin{cases} t'\,e^{-ikx} & x<x_l\\ e^{-ik_Rx} + r'\,e^{ik_Rx} & x>x_r\end{cases} \qquad (3.1)$$

(ψ⁺ comes in from the left, ψ⁻ from the right.) Normalisation: ⟨ψ⁺_k|ψ⁺_{k'}⟩ = 2π δ(k−k'), ⟨ψ⁻_k|ψ⁻_{k'}⟩ = 2π (k_R/k) δ(k−k').

### 3.2 Crossing the structure: the flat-segment propagator
On a segment [a, b] with constant V, write q = √(2(E − V)) (complex if E < V). The pair (ψ, ψ') is carried by

$$ \begin{pmatrix}\psi\\ \psi'\end{pmatrix}_b = \begin{pmatrix}\cos qL & \dfrac{\sin qL}{q}\\[4pt] -q\sin qL & \cos qL\end{pmatrix}
\begin{pmatrix}\psi\\ \psi'\end{pmatrix}_a,\qquad L = b-a, \qquad (3.2)$$

which is exact (ψ'' = −q²ψ on the segment), with the q → 0 limit sin(qL)/q → L. Chaining (3.2) over all segments from x_l to x_r gives
the two fundamental solutions u₁ (ψ, ψ')(x_l) = (1, 0) and u₂ = (0, 1). Under bias the ramp is cut into ≈ 2,000 flat slices; slicing
2,000 → 8,000 changed T by 8e-9 (measured, `CORRECTION_STATE.md`).

### 3.3 Reading r, t, t', r'
Start at x_l with the left-lead form of e^{ikx} (A = (e^{ikx_l}, ik e^{ikx_l})) and of e^{−ikx} (B), carry to x_r, and split the result
into right-moving and left-moving waves e^{±ik_Rx}:

$$ a_R = \tfrac12\Big(\psi + \frac{\psi'}{ik_R}\Big)e^{-ik_Rx_r},\quad b_R = \tfrac12\Big(\psi - \frac{\psi'}{ik_R}\Big)e^{ik_Rx_r}. \qquad (3.3)$$

ψ⁺ = (e^{ikx} + r e^{−ikx}) on the left must have no incoming wave on the right: b_R(A) + r b_R(B) = 0, so

$$ r = -\frac{b_R(A)}{b_R(B)},\qquad t = a_R(A) + r\,a_R(B). \qquad (3.4)$$

ψ⁻ = t' e^{−ikx} on the left must have unit incoming e^{−ik_Rx} on the right: t' b_R(B) = 1, so t' = 1/b_R(B), r' = a_R(B)/b_R(B).
The stationary transmission is T(k) = (k_R/k)|t|² (flux ratio).

### 3.4 Expanding the start packet
The families (3.1), with E > 0, are complete for a packet that starts on the left (closure relation)

$$ \int\frac{dk}{2\pi}\Big[\psi^+_k(x)\psi^{+*}_k(x') + \frac{k}{k_R}\psi^-_k(x)\psi^{-*}_k(x')\Big] = \delta(x-x'), \qquad (3.5)$$

up to the right-incident states with −B < E < 0, which are evanescent on the left; their share is bounded by the start packet's
share right of the first face (`start_in_barrier`, ≈ 1e-6). Hence

$$ \chi(x,t) = \int\frac{dk}{2\pi}\Big[c_+(k)\psi^+_k(x) + \frac{k}{k_R}c_-(k)\psi^-_k(x)\Big]e^{-ik^2t/2},\qquad c_\pm = \langle\psi^\pm_k|\chi_0\rangle. \qquad (3.6)$$

**The projections.** Split ψ^± into its left-lead form L^± (the x < x_l formula, used everywhere) and the difference ψ^± − L^±, which
is non-zero only for x ≥ x_l:

$$ c_+ = \underbrace{G(k) + r^* G(-k)}_{\int L^{+*}\chi_0\ \text{closed form}} + \int_{x_l}^{\infty}(\psi^{+*}-L^{+*})\chi_0\,dx,\quad
c_- = t'^* G(-k) + \int_{x_l}^{\infty}(\psi^{-*}-L^{-*})\chi_0\,dx, \qquad (3.7)$$

$$ G(k) = \int e^{-ikx}\chi_0\,dx = (2\pi s_x^2)^{-1/4}\,2 s_x\sqrt\pi\;e^{-s_x^2(k-k_0)^2 - i(k-k_0)x_0}. \qquad (3.8)$$

The correction integral is over the Gaussian tail of χ₀ that reaches the structure (Simpson, step 0.02 a, up to where |χ₀|² < 1e-16 of
its peak).

**The k grid.** Trapezoid in k from max(dk, k₀ − 8.5 σ_k) to k₀ + 8.5 σ_k, σ_k = 1/(2s_x), dk = 5e-4. A trapezoid sum in k is the exact
integral made periodic in x with period 2π/dk ≈ 12,600 a, far longer than any distance travelled. Convergence: dk 5e-4 → 2.5e-4
changes T by ≤ 3e-6 (measured).

| Eq. | Reference code (`exact_wall.py`) | GPU code (`exact_wall_jax.py`; batched `wall_gpu_run.py`) |
|---|---|---|
| (3.2) segment propagator | `_prop` :61; chained in `Scatter.__init__` :78–89 | `_prop` :17; `step` + `lax.scan` :34–39; batched `core.step` :143–147 |
| segments, bias slices | `segments` :47 | same function (imported) |
| (3.3) split into a_R, b_R | `Scatter.__init__` `at_r`, `split` :94–100 | `split` :43–46; `wall_gpu_run.py:150–154` |
| (3.4) r, t, t', r' | :101–102 | :47; `wall_gpu_run.py:155` |
| T(k) = (k_R/k)|t|² | :107 | :74 |
| ψ^± inside the structure | `Scatter` interior table :83–86, :105–106 | `values` :82–100 (gather of face values + (3.2) to the point) |
| (3.8) G(k) | `G` :129 | same (imported) |
| (3.7) projections | :176–183 | :61–68; `wall_gpu_run.py:167–172` |
| k grid | `kgrid` :135 | same; padded to multiples of 1024 with zero weights :26–28 (sum unchanged) |
| (3.6) amplitudes a_± = w/2π · c_± (· k/k_R) | :185 | :70; `wall_gpu_run.py:173` |
| (3.6) χ(x,t) = Σ_k B(x,k) e^{−iE_k t} | `_basis` :199, `chi` :203 | `basis` :102, `chi` :105; `wall_gpu_run.py:178–181` |
| completeness check ("carried") | :187 | :71; `wall_gpu_run.py:174` |

> **Defect (not a physics error, a difference between two codes):** the reference `Exact` projects over x_l … x_l + 10 s_x
> (exact_wall.py:164–166); the GPU `ExactJ` and the batched code over x_l … max(x_r + 1, x₀ + 8.6 s_x) (exact_wall_jax.py:59–60). The
> GPU range covers the whole tail; the two agree to T ± 1e-11 on the runs compared, and the batched code equals `ExactJ` exactly
> (§5).

## 4. Walls: the observables

### 4.1 Transmission at infinite time
As t → ∞ the part of χ right of the structure becomes ∫dk/2π A(k) e^{ik_Rx} e^{−iEt} with A = c₊ t + (k/k_R) c₋ r'. Its norm:

$$ \int|\chi_R|^2dx = \iint\frac{dk\,dk'}{(2\pi)^2}AA'^*\,2\pi\,\delta(k_R-k_R') = \int\frac{dk}{2\pi}\,|A|^2\,\frac{k_R}{k}, \qquad (4.1)$$

using δ(k_R − k_R') = (k_R/k) δ(k − k'). This is T_ref for walls.

A second number, the spectrum-weighted transmission T_w = ∫|G|²T(k)dk / ∫|G|²dk (stationary T averaged over the packet's spectrum,
ignoring the tail correction).

| Eq. | Code |
|---|---|
| (4.1) T_ref | `exact_wall.py:189–190`; `exact_wall_jax.py:72–73`; `wall_gpu_run.py:175–176` |
| T_w | `exact_wall.py:191`; `exact_wall_jax.py:74–75`; `wall_gpu_run.py:177` |

### 4.2 Probability in regions, by flux
Probability current j = Im(χ* ∂_xχ). Conservation ∂_t|χ|² + ∂_x j = 0 integrated over x < x_l and x > x_r:

$$ P_L(t) = P_L(0) - \int_0^t j(x_l,t')dt',\qquad P_R(t) = \int_0^t j(x_r,t')dt',\qquad P_L(0) = 1 - \tfrac12\mathrm{erfc}\Big(\frac{x_l-x_0}{\sqrt2 s_x}\Big). \qquad (4.2)$$

χ and χ' at a point are Σ_k (value or slope coefficient) e^{−iEt}; the code builds e^{−iE t} on a time grid of 0.02 by recurrence
(one exp table per chunk, multiplied by e^{−iE·chunk·h}), takes j, and integrates by Simpson. P_struct = ∫_{x_l}^{x_r}|χ|² on a fine
Simpson grid (0.01 a, separate per segment between true faces), P_well the same restricted to the gaps. The closure
P_L + P_struct + P_R = 1 is **checked, not imposed**: all 1,088 walls satisfy it to ≤ 2.6e-5.

### 4.3 Inside the stored box
The stored files show probabilities inside the stored box |x| ≤ half-box. The parts beyond the box edges x_lo, x_hi:

$$ \text{lo}(t) = \tfrac12\mathrm{erfc}\Big(\frac{x_0-x_{lo}}{\sqrt2 s_x}\Big) - \int_0^t j(x_{lo}),\quad
\text{hi}(t) = \tfrac12\mathrm{erfc}\Big(\frac{x_{hi}-x_0}{\sqrt2 s_x}\Big) + \int_0^t j(x_{hi}), \qquad (4.3)$$

so norm(box) = 1 − lo − hi, left(box) = P_L − lo, right(box) = P_R − hi.

| Eq. | Code |
|---|---|
| j and its time integral | `exact_wall.py:208` `_flux_cum`; `exact_wall_jax.py:117`; batched: same function on the vmap outputs (`wall_gpu_run.py:214`) |
| face coefficients (ψ, ψ') at x_l, x_r | `exact_wall.py:195–197` `fl, fr`; `exact_wall_jax.py:78–80`; `wall_gpu_run.py:184–186` |
| (4.2) P_L(0) | `exact_wall.py:192`; `wall_gpu_run.py:126` |
| P_struct, P_well (fine grid) | `exact_wall.py:155–162`, `regions_and_tails` :247; `wall_gpu_run.py:114–121, 182–183` |
| (4.3) box tails | `lead_pair` :233, `regions_and_tails` :251–253; `wall_gpu_run.py:134, 187, 217` |
| curves t, norm, left, right, well | `wall_gpu_run.py:70` |
| closure | `wall_gpu_run.py:218` (sum) and `:76` (header `closure_max`) |

## 5. Walls: the batched GPU implementation

**Picture.** Walls that share a geometry (same barriers, same box, same packet width) differ only in energy and height. They can be
computed side by side like identical sums done in parallel columns.

**Method.** Group key (Nx, N, D, P, s_x, biased?) (`wall_gpu_run.py:98`). Inside a group the segment faces, the projection points, the
fine grid and the output points are identical; this is asserted per wall, not assumed (:107–112). The k grids are padded to the
group's largest length with zero weights (:197–199); a zero weight removes a term from every sum in §3–4, so nothing changes. A
pure function `core` (:141–188) does §3.2–4.2 for one wall; `jax.jit(jax.vmap(core))` runs B walls per call (:190). Memory estimate
16 bytes × K × (8 n_t + 4 n_f + 4 n_out + 600 + 5 S + 40), batch B = min(8, 6 GB / estimate) (:191–194).

**Check, built in.** The first wall of every group is also computed by the verified one-wall path `ExactJ`; the group is kept batched
only if |ΔT| ≤ 1e-9 and no amplitude level differs by more than 1 (:269–276). Result (Fact, `walls_summary.json`): 13/13 groups,
ΔT = 0 or ≤ 3.5e-18, Δlevel = 0. And T_ref equals the earlier CPU reference to 6.8e-7 (`CORRECTION_LOG.md` §3.1).

## 6. Discs and shells: reduction to (x, rho)

**Picture.** A disc on the flight axis, or a shell centred on it, looks the same from every side around the axis, like a lamp shade
seen along its stem. The packet also starts on the axis. Nothing then can make the wave swirl around the axis, so the 3D wave
depends only on x and on the distance ρ from the axis.

**Derivation.** In cylinder coordinates (x, ρ, φ), ∇² = ∂²_x + ∂²_ρ + (1/ρ)∂_ρ + (1/ρ²)∂²_φ. V and ψ₀ are independent of φ, so ψ is
too (angular momentum m = 0 is conserved) and

$$ i\partial_t\psi = -\tfrac12\Big(\partial_x^2 + \partial_\rho^2 + \tfrac1\rho\partial_\rho\Big)\psi + V(x,\rho)\psi,\qquad
\int|\psi|^2\,2\pi\rho\,d\rho\,dx = 1. \qquad (6.1)$$

This is the 3D problem exactly, on a 2D grid. The start packet (1.2) is g(y)g(z) ∝ exp(−ρ²/(4s⊥²)).

| Eq. | Code |
|---|---|
| (6.1) start packet on the (x, ρ) grid | `axisym.py:146`; `axisym_jax.py:43–44` (normalised by the discrete norm, :44) |
| geometry: barrier centres, extent, x₀ | `axisym.py:44–60` |

## 7. Discs and shells: the split-step scheme with the Hankel transform

### 7.1 Strang splitting
With H = K + V, one step

$$ e^{-iH\,dt} = e^{-iV dt/2}\,e^{-iK dt}\,e^{-iV dt/2} + O(dt^3), \qquad (7.1)$$

second order globally. K = −½(∂²_x + ∂²_ρ + ρ⁻¹∂_ρ) is diagonal in (k_x, k_ρ): e^{−iKdt} = e^{−ik_x²dt/2} e^{−ik_ρ²dt/2}. Along x a
discrete Fourier transform makes ∂²_x diagonal (periodic box, then masked). Along ρ the transform that diagonalises the m = 0 radial
Laplacian is the zero-order Hankel transform: ψ(ρ) = ∫_0^∞ Ψ(k) J₀(kρ) k dk.

### 7.2 The quasi-discrete Hankel transform (QDHT)
Guizar-Sicairos & Gutiérrez-Vega, J. Opt. Soc. Am. A 21, 53 (2004). With j_n the zeros of J₀, S = j_{N+1}, nodes ρ_n = j_n R_max/S and
wave numbers k_n = j_n/R_max, the matrix

$$ T_{mn} = \frac{2\,J_0(j_m j_n/S)}{S\,|J_1(j_m)|\,|J_1(j_n)|} \qquad (7.2)$$

acts on the scaled field u_n = ψ(ρ_n)/|J₁(j_n)| and is (nearly) its own inverse, T² ≈ 1. The code makes it exactly orthogonal by
T → T (T²)^{−1/2} (symmetrised), so the radial free step

$$ M = T\,\mathrm{diag}(e^{-ik_n^2dt/2})\,T \qquad (7.3)$$

is exactly unitary. The norm weight follows from the discrete Parseval relation of the QDHT:

$$ \int|\psi|^2\,2\pi\rho\,d\rho\,dx \;\approx\; \frac{4\pi R_{max}^2}{S^2}\,h_x\sum|u|^2 . \qquad (7.4)$$

### 7.3 The step as coded
u ← e^{−iVdt/2}u; u ← IFFT_x[e^{−ik_x²dt/2} FFT_x u]·M; u ← e^{−iVdt/2}u; then the absorbing mask (§8.3).

| Eq. | Code |
|---|---|
| (7.2) T, nodes, k_n, J₁ | `axisym.py:28–37` `qdht` |
| orthogonalisation | `axisym.py:31–32` |
| (7.4) wq | `axisym.py:34` |
| (7.3) M | `axisym.py:153`; `axisym_jax.py:48` |
| e^{−ik_x²dt/2} | `axisym.py:154`; `axisym_jax.py:49` |
| e^{−iVdt/2} | `axisym.py:152`; `axisym_jax.py:47` |
| (7.1) one step | `axisym.py:162–164`; `axisym_jax.py:60` (inside `chunk`, a `fori_loop` over the steps between frames, :57–65) |

## 8. Discs and shells: potential, borders, observables, T

### 8.1 The potential as cell averages
On the grid each x cell is [x − h_x/2, x + h_x/2] and each ρ cell lies between midpoints of nodes. V is V₀ times the share of the cell
inside a barrier:
- along x: overlap length of the cell with each barrier / h_x;
- disc along ρ: area share of the annulus cell inside radius R, (min(e_hi, R)² − e_lo²)/(e_hi² − e_lo²) (area ∝ ρ²);
- shell: sub-sampling 8 × 8 per cell, weighted by ρ (area), testing |r − R_c| < D/2 with r = √(x² + ρ²).
Bias: V − B·clip((x − x_l)/(x_r − x_l), 0, 1).
A cell-averaged barrier is a consistent discretisation: as h_x → 0 it converges to the true barrier, unlike rt3d2's point sampling (D1).

| Item | Code |
|---|---|
| x overlap | `axisym.py:63` `overlap`, :83–85 |
| disc ρ area share | `axisym.py:88` |
| shell sub-sampling | `axisym.py:103–114` |
| bias | `axisym.py:115–116` |
| regions (left, right, well; core, gap, out) and sides L, M, R | `axisym.py:117–133` |
| rt3d2's drawing (for test C only) | `axisym.py:68` `staircase_disc_profile`, :81–83, :87, :92–99 |

### 8.2 The production grid
Discs: h_x = 0.0625 a, N_ρ = 256, R_max = 64 a, ρ border 12 a, dt = 0.01, x box 2 × the stored one. Shells: N_ρ = 640, R_max = 160 a,
ρ border 24 a (radial step kept at 0.25 a). Why the x box is doubled: §8.3.

### 8.3 The absorbing mask and why it reflects
Multiplying by m(x) ∈ (0, 1] every step is the same as adding an imaginary potential −iW with e^{−W dt} = m, i.e.
W = −ln m / dt. A complex absorbing potential reflects part of the wave, more when it rises steeply relative to the wavelength. Here
its height grows like 1/dt: halving dt doubles W, steepening the absorber, so reflection grows as dt shrinks. That is the measured D5
(2D wall test, exact T 0.196820: box 96 a, dt 0.01 → 0.200847; dt 0.0025 → 0.210937; box 192 a, dt 0.01 → 0.196889). Doubling the box
sends the reflected part back after the read time. What the mask removes is booked by side: x < x_l (reflected), x > x_r
(transmitted), between (undecided).

| Item | Code |
|---|---|
| sin^(1/8) mask, x and ρ | `axisym.py:40` `border`; `axisym_jax.py:37–40` |
| absorbed probability by side | `axisym.py:165–168`; `axisym_jax.py:61–63` |

### 8.4 T, its uncertainty, and the drift

$$ T_{ref} = P(x>x_r) + A_R + \tfrac12\big(P(x_l\le x\le x_r) + A_M\big),\qquad T_{unc} = \tfrac12\big(P_M + A_M\big), \qquad (8.1)$$

at the end of the run, A the absorbed shares by side. "Between" (M) is everything with x_l ≤ x ≤ x_r **at any ρ**, so a wave scattered
sideways and swallowed by the ρ border while its x is still between the faces counts half to each side. That is why the shells needed a
wide ρ range (§9.2).

Norm drift: max over frames |Σ|u|²wq + A_L + A_R + A_M − 1|. A unitary step conserves it exactly; what remains is rounding.

| Eq. | Code |
|---|---|
| (8.1) T, T_unc | `axisym.py:175–177`; `axisym_jax.py:95, 97` |
| drift | `axisym_jax.py:96` |

### 8.5 The stored-layout output
Frames: ψ on the stored points x ∈ 0.5 a grid, ρ = 0, 0.5, …, 31.5 a (shown as the half-plane z = 0, y = ρ ≥ 0). From the nodes ρ_n to the
output radii by the Bessel series of a field band-limited to k_n: ψ(ρ) = Σ_m a_m J₀(k_m ρ), with a solved from the node values
(`bessel_rows`, `axisym_jax.py:19–26`). x-profile p(x) = ∫|ψ|² 2πρ dρ = Σ_ρ |u|² wq / h_x (`axisym_jax.py:88`). Levels and phases
are written as in the stored files (`rt2d_run.py:49–54` quantize, `:56–82` `one`).

## 9. Precision, convergence and the smoke tests

### 9.1 complex64 against complex128
complex64 carries 7 significant digits. Over ~10⁴ steps the rounding errors of the FFT and the matrix product accumulate like a random
walk and show up as a slow loss or gain of norm. Measured (`kaggle_outputs/2d-smoke/smoke__smoke.jsonl`): complex64 drift 2–4e-3,
complex128 drift 1e-11. On T itself the two agree to ≤ 6e-4 on discs and 0.0012 on one shell (N2 R3 E0.75 at R_max 160:
0.627703 vs 0.628891). complex128 costs 7.5–14× the step time on a T4, whose double-precision rate is 1/32 of single.

### 9.2 Grid convergence
Discs (R6 N2 E0.75; R12 N10 E0.9): every refinement (h_x halved or doubled, N_ρ 384, dt 0.005, box 3×, R_max 96) changes T by ≤ 0.0019.
Shells: R_max is the slow variable, because of (8.1). T at R_max 64/96/128/160/192 a (`2d-shellconv`): N2R3E0.75
0.6122/0.6220/0.6251/0.6277/0.6285; N2R5E0.30 0.5070/0.5190/0.5225/0.5245/0.5248; N1R3E1.50 0.8376/0.8401/0.8409/0.8417/0.8421;
N1R5E0.75 0.6348/0.6422/0.6447/0.6467/0.6474. Chosen: 160 a (the step to 192 a is ≤ 0.0008).

### 9.3 Wall limit
A disc wider than the ρ range is a wall; its T must equal the exact wall T of §4.1. complex64: 0.196539 vs 0.196820 (N2 E0.75), 0.167971
vs 0.166225 (N10 E0.9), 0.039134 vs 0.039048 (bias 2.125 E0.5).

| Test | Code |
|---|---|
| smoke tests A–C and step times | `rt2d_smoke.py` |
| shell R_max convergence | `rt2d_shellconv.py` |
| production runner (shards, tracker, ETA) | `rt2d_run.py:86–131` |

## 10. Comparison with the stored runs

### 10.1 The stored number T_far
`file_rt3d2.py:48–62`: find the last frame before 1e-3 of the wave reaches the end borders (|x| > inner half-box); there

$$ T_{far} = \frac{P_{right} + \tfrac12 P_{well}}{P_{box}}. \qquad (10.1)$$

Dividing by P_box removes what the side border took (D2).

### 10.2 The gate and the classification
Gate: |T_old − T_ref| ≤ max(0.005, 0.01 T_ref) (`classify_2d.py:35`). Because the new disc T is itself uncertain by up to 0.002 (§9),
a run is kept only if it clears the gate by 0.002 (`classify_2d.py:46`); otherwise it is marked for a complex128 recompute.
Results: walls, 918 of 1,088 stored fail (exact T_ref); discs, 1,582 of 2,327 stored fail; 545 kept with margin.

> **Defect (my error):** for shells the stored index has no transmission number. I defined T_old = P_out / P_box at the T_far frame
> (`file_corrected.py:56–61`), where "out" is outside the outer sphere. That includes the reflected wave, so T_old ≈ 0.998 against
> T_ref ≈ 0.86, and the "282 of 282 fail" is meaningless. A correct definition would be the share beyond the last face in x, which the
> stored shell curves do not carry.

## 11. The file format (RT3C) and what the page reads

`b'RT3C'`, uint32 header length, JSON header, zlib body: n × n_xs × 64 uint8 amplitude levels (of each frame's own peak), the same for
arg ψ (zeroed where the level < 3), n × N_x float32 x-profile, [n × N_x float32 1D profile]. Reader `read_rt3d.py:7–18`; writer
`rebuild_wall.py:89–100`; 2D writer `rt2d_run.py:56–82`. The wall header adds T_ref, T_spectrum_weighted, carried, closure_max,
parent {file, sha256}, extra_curves {left_line, right_line} (`wall_gpu_run.py:72–81`); the 2D header adds T_ref, T_unc, drift, grid,
parent (`rt2d_run.py:70–78`).

## 12. Defects found, in one list

| # | Where | What | Effect | State |
|---|---|---|---|---|
| 1 | `rt3d2.py` (gen 2) | barrier sampled at 0.5 a points (D1) | resonances misplaced; 918 walls, 1,582 discs fail | the reason for the correction |
| 2 | `rt3d2.py` | side mask absorbs trapped wave (D2) | lifetimes short | replaced |
| 3 | `rt3d2.py` | norm lost from t = 0 (D4) | curves low by ≤ 2.4e-3 | cause unknown |
| 4 | masks everywhere | absorber reflection ∝ 1/dt (D5, §8.3) | +0.004 … +0.014 on T at box 96 a | box doubled |
| 5 | `axisym_jax.py` | carry dtype promoted after a c128 run | crash (smoke v1) | fixed 17ffd02 |
| 6 | `rt2d_run.py` | default grid overwrote the loader's | 141 shells at R_max 64 | fixed 07ac9bf, rerun |
| 7 | `file_corrected.py` | default user agent → HTTP 403 | classify v1 failed | fixed a7cf734 |
| 8 | `classify_2d.py` | status unset for unreadable files | would crash | fixed b9ccf3a |
| 9 | `file_corrected.shell_T_old` | wrong quantity for stored shells (§10.2) | shell comparison meaningless | **open** |
| 10 | discs and shells | complex64 drift 2–4e-3 > 1e-3 | brief's rule broken; T within 6e-4 (discs), 0.0012 (one shell) | **open** |
| 11 | `exact_wall.py` vs `exact_wall_jax.py` | different projection ranges (§3) | none measurable (≤ 1e-11) | noted |
