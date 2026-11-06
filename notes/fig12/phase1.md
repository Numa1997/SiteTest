# Fig. 12, phase 1: measurements before choosing the real-time fluid (6 November 2026)

Nothing on the page changes in phase 1. Each number below has the command that reproduces it. Labels: **Fact** (measured here or
read in a source, with the handle), **Inference** (reasoning from facts), **Opinion**.

## 1. What the 3D solver costs, and where

- **Fact.** `node tools/fig12/same.cjs` still prints `sha256 7747da757ea9d800`; 1 simulated s (200 steps of 5 ms, 4 mm grid,
  20 × 10 × 45 cells, ~22 000 particles) takes 4.6 s on one core of the build machine: 0.22 s simulated per s. The page with 4
  threads reaches 0.31 s/s (docs/simulations/fig12-beer-slosh.md, "Threads").
- **Fact** (`node --cpu-prof tools/fig12/same.cjs`, self time): level set from the particles 32 % (`phiCell` 24 %, bins, dilate,
  particles), particle-to-grid and grid-to-particle transfers 35 % (`transfer` 18 %, g2p 16 %), the pressure solve 16 %
  (`pcg`) plus 3 % assembling it (`project`), the rest under 3 % each.
- **Inference.** An infinitely fast pressure solve alone would lift 0.31 s/s to about 0.38 s/s. Real time needs the particles,
  the level set and the transfers on the GPU too: a port of the whole step, not of the solve.
- **Fact** (inline `node -e` in the session, one thread, 3 simulated s): 5 mm grid 0.45 s/s, 6 mm 0.71 s/s. The first-mode
  frequency read from zero crossings rises to 4.4 Hz and 5.0 Hz (3.42 Hz is the continuum value): the coarse grids are too coarse
  for the swing. Coarsening is not a route.

## 2. A minimal GPU pressure solve on the 4 mm grid

`scratchpad` files, not in the repository: `gpu/dump.cjs` writes one pressure system of the solver (step 100 of the `same.cjs`
run: 3 702 liquid cells, 104 of them closed on all six faces and left out, as MIC(0) leaves them out), `gpu/bench.html` solves it
with one workgroup of 256 threads running Jacobi-preconditioned CG in float32 (no read-back until the end), `gpu/runbench.cjs`
runs it in headless Chromium 153.

- **Fact.** The container's Chromium has WebGPU only on SwiftShader (a CPU emulation of a GPU); no hardware GPU is reachable.
- **Fact.** The GPU answer agrees with the solver's float64 MIC(0)-PCG answer to 4.5·10⁻⁶ (relative max difference) at tolerance
  10⁻⁵, in 106 iterations (MIC(0): 33–35). On SwiftShader one solve takes 116 ms median (CPU MIC(0): about 4–7 ms).
- **Inference.** The SwiftShader time says nothing about a real GPU. The 106 iterations are four reductions each; on a desktop GPU a
  single-workgroup loop of this size is latency-bound, plausibly 0.5–2 ms per solve (not measured). A real number needs the page
  opened on a machine with a GPU.

## 3. The live modes against the 3D solver, from rest

`node tools/fig12/linearity.cjs <modal|3d> A1,A2,…` drives both models with the same glass acceleration from rest, a half-sine
pulse a_x = A sin(πt/0.3 s), a hard forward start (speed gain 0.19 m/s per m/s² of A), no cart. `node tools/fig12/linfit.cjs
notes/fig12/runs/linearity-*.json` fits the free swing after the pulse (a cos + b sin + linear drift, frequency scanned).

| A (m/s²) | peak lean, modes | peak lean, 3D | free swing, modes | free swing, 3D | spill modes / 3D |
|---|---|---|---|---|---|
| 0.5 | 6.0 mm | 5.9 mm | 3.8 mm, 3.420 Hz | 2.1 mm, 3.160 Hz | 0 / 0 |
| 1 | 12.0 | 11.5 | 7.5, 3.420 | 4.4, 3.202 | 0 / 0 |
| 2 | 24.1 | 25.4 | 15.0, 3.420 | 14.7, 3.194 | 0 / 0 |
| 4 | 48.1 | 45.3 | 30.0, 3.420 | 32.7, 3.109 | 0 / 1.6 g |
| 6 | 67.0 | 69.3 | 40.0, 3.418 | 36.9, 3.056 | 5.0 / 12.2 g |

(Lean = front − back wall height, so the wall amplitude is half of it. The 3D reading noise is about 1–2 mm, the fit's misfit.)

- **Fact.** During the push the two agree within 10 % at every amplitude: the forced, quasi-static tilt is what linear theory gets
  right. After it, the 3D swing slows as it grows: 3.20 Hz at 4 mm, 3.06 Hz at 37 mm, −4.5 %. The modes keep one frequency (they
  cannot do otherwise) and it is the continuum's 3.42 Hz, while the 4 mm grid's linear frequency is 3.21 Hz (known grid error).
- **Fact.** The 25 mm bump in open loop through the whole cart (`MODAL=1 node tools/fig12/study.cjs 25 off 0`): modes 73.9 mm lean,
  9.9 g spilled; 3D 60.7 mm, 11.9 g (docs table). The modes overshoot the 3D lean by 22 %.
- **Fact** (computed from the model's constants): R_s = 39.1 mm, kh = ξ₁₁h/R = 5.89 (deep: tanh kh = 1.0000), f₁₁ = 3.421 Hz,
  ζ₁ = 0.0053. A planar wave breaks when the crest's downward acceleration aω² reaches g, a = g/ω² = R/ξ₁₁ = 21.2 mm at the wall
  (Taylor 1953, quoted by Royon-Lebeaud, Hopfinger & Cartellier, JFM 577 (2007) §2.2, hal-00265298). A 74 mm lean is a 37 mm wall
  amplitude, 1.7 times the breaking amplitude: no linear, and no weakly nonlinear, theory holds there.
- **Fact** (Royon-Lebeaud et al. 2007, §2.2): for h/R ≫ 1 planar waves soften, ω/ω₁ = 1 − ½A⟨η²⟩/ℓ² with A = 1.11; swirl
  stiffens (A + B = −0.42). The 3D solver's softening is the right sign. **Inference:** a quantitative check against this formula
  needs ℓ and ⟨η²⟩ defined as in Miles (paywalled) and is left for phase 2.
- **Fact** (code, `stout-cart.js:122`): the 3D solver computes half the glass with a mirror plane at y = 0 (v = 0 there). It cannot
  swirl. Swirl (Miles 1984) is a broken y → −y symmetry; near resonance between the bifurcation points U and H the planar wave is
  unstable and real stout would swirl (Faltinsen, Lukovsky & Timokha, JFM 804 (2016) §4). Any "real fluid" route must drop the
  mirror or it misses the most visible nonlinear effect.
- **Inference** (vertical motion): a vertical acceleration a_z(t) enters only as g → g + a_z, i.e. ω² → ω²(1 + a_z/g), a Mathieu
  equation. With damping ζ, the first mode is pumped (Faraday) when the vertical acceleration at 2f₁₁ = 6.84 Hz exceeds 4ζg =
  0.21 m/s². At 1 m/s that is a road wavelength of 14.6 cm, the size of a cobble sett; the slosh frequency itself is a 29.2 cm
  wavelength. A cobbled road at walking speed sits on the parametric resonance.

## 4. The contact model on a rough road

- **Fact** (`stout-cart.js:1343–1344`): the tyre force is N = k_t(z_a − z_w) + c_t(ż_a − ż_w), clamped at N ≥ 0; the wheel can
  leave the road and fly (the axle then follows −F_s − m_w g). The road enters through the rigid-wheel envelope z_a (`Road.build`,
  0.5 mm table), which bridges gaps narrower than the wheel, as a rigid wheel does.
- **Fact** (`stout-cart.js:1346`): the drive force F = b i acts whatever N is. In the air the motor still pushes the cart. A rough
  road needs traction limited to |F| ≤ μN (and the wheel's spin as its own state when it slips). Not yet a problem on the present
  bumps (smallest tyre load 4.4 N), certain to be one on cobbles.

## 5. The routes to a real fluid in real time

- **(A) The 3D solver on the GPU.** Whole step in WGSL: particles, level set, transfers (float atomics do not exist in WGSL:
  fixed-point integer atomics or a gather by cell bins), the solve (§2). Float32, so the `same.cjs` fingerprint becomes a
  statistical comparison with the CPU solver, not identity. The mirror plane would be dropped (full glass, 2× cells) to allow swirl.
  Cost (inference): the largest of the three, about 1 500 lines of JS rewritten as compute shaders. Risk: only measurable on real
  GPUs; phones and the build machine have none or weak ones; a CPU fallback stays at 0.3 s/s.
- **(B) Nonlinear multimodal ODEs** (Narimanov–Moiseev third order for the upright cylinder, Faltinsen, Lukovsky & Timokha 2016
  eqs. 2.17–2.20, or Lukovsky's 5 ODEs eq. 2.23). Valid for h/R ≳ 1.05–1.5 (here 3.2), small forcing near f₁₁, wall amplitude below
  breaking (21 mm here); it has planar waves, swirl and chaos, and the coefficients tend to constants for deep liquid (Marcotte,
  Gallaire & Bongarzone, arXiv:2302.02443, Table 1). Cost: tens of ODEs, microseconds a step. Risk: it is still a model of the
  fluid, not the fluid; beyond 21 mm it is as wrong as the linear modes, only differently; the tulip is not a cylinder.
- **(C) Shallow water or Boussinesq on the disc.** **Inference: wrong for this glass.** kh = 5.89; shallow water needs kh ≪ 1 and
  the usual Boussinesq extensions reach kh ≈ 3 at best. Rejected on physics, not on cost.
- **Literature** (agent's report, sources read): no paper found that runs a nonlinear 3D free-surface fluid in real time *inside*
  a feedback loop. Real-time slosh control uses pendulum or modal models (Sato, Nagai & Sakai 2014: camera at 15 Hz, identified LTI
  model); a learned reduced model reached real time on a real cup from a depth camera (Moya et al., arXiv:2106.13301), prediction
  only. Browser GPU FLIP solvers run 50 000 cells at 33 fps on a 2013 GPU (austinEng WebGL PIC/FLIP README).

The sensors and the observer are the same in every route: wall level probes are point samples of η at the wall, η(R, θ_k, t); the
observer estimates (q, q̇) of the slosh modes from them (Kalman), the LQR or MPC acts on the estimate. In (A) the probes read the
solver's level set, so the loop closes on the fluid, not on a model of it.

## 6. Real roads (sources read by the session's research agent; downloads kept outside the repository)

- **Fact.** ISO 8608 displacement PSD G_d(n) = G_d(n₀)(n/n₀)^(−w), n₀ = 0.1 cycles/m, w = 2; class geometric means
  G_d(n₀) = 16, 64, 256, 1 024, 4 096, 16 384, 65 536, 262 144 ×10⁻⁶ m³ for A–H, bounds a factor 2 either side (Agostinacchio,
  Ciampa & Olita, Eur. Transp. Res. Rev. 6, 267 (2014), Table 1). Paved roads "hardly belong to classes worse than D"; a 2017 sample
  of real roads: A 18 %, B 58 %, C 23 %, D 1 %, and the measured w averaged 3.16 ± 0.17, not 2 (Loprencipe & Zoccali, J. Mod.
  Transport. 25, 24 (2017), Tables 1–2).
- **Fact.** Synthesis: z(x) = Σᵢ √(2 Δn G_d(nᵢ)) cos(2π nᵢ x + φᵢ), φᵢ uniform on [0, 2π), Δn = 1/L (Agostinacchio et al. eq. 8).
  ISO 8608:2016 (preview, §5.1.1.5): the band is the user's; the tyre's enveloping is a low-pass filter, upper limit 10 cycles/m
  recommended. One paper (arXiv:2605.05235 eq. 13) drops the √2 and halves the variance; another (arXiv:2605.09175 Table 1) mislabels
  G_d(Ω₀) as G_d(n₀). Neither is to be copied.
- **Fact.** Washboard: lab ripples 50–500 mm long, a few mm to 50 mm high, onset speed ≈ 1.5 m/s, λ/L = f(Fr) with L = v²/g
  (Taberlet, Morris & McElwaine, PRL 99, 068003 (2007), arXiv:0711.3872); λ = 195 mm at 1.1 m/s (Percier et al., arXiv:1209.5560).
  Real gravel roads: 300–1 000 mm, depth up to 50 mm (review in Erasanayagam et al., Road Mater. Pavement Des. 2025, §1); a drone
  profile in Ecuador, 20.6 mm mean peak-to-peak.
- **Fact.** Measured Belgian block: OpenCRG `belgian_block.crg` (Apache-2.0, DaimlerChrysler 2005; 10 m × 3.4 m on a 10 mm grid).
  The agent's own reading of it: centre line 17.4 mm RMS, 78 mm peak to peak; 8.5 mm RMS once waves over 0.6 m are removed; PSD
  12 ×10⁻⁶ m³ at 2 cycles/m, 0.4 ×10⁻⁶ at 10 cycles/m. Proving-ground cobbles: stones 70–350 mm, heights 20–120 mm, PSD in classes
  D–F (Han et al., Math. Probl. Eng. 2018, 7246503, CC BY, Table 2). Street setts 15 × 15 cm with 12–30 mm joints (Majer et al.,
  Sustainability 16, 6040 (2024)). Paris–Roubaix: no measured sett data found.
- **Fact** (inline `node -e`, w = 2, 0.011–10 cycles/m): RMS height 3.8, 7.6, 15.3, 30.5 mm for classes A–D; the raw road vertical
  acceleration in the band 6.5–7.2 Hz at 1 m/s, (2πf)⁴G_d(f/v)/v integrated, is 0.09, 0.18, 0.36, 0.72 m/s² RMS.
- **Inference.** Against the Faraday threshold 0.21 m/s² (§3), a class C road and worse at walking speed pumps the swing
  parametrically, before the wheel's envelope and the suspension filter it. The page should show that, and the cart's own
  filtering decides whether it survives to the glass.
