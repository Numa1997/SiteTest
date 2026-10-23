# Contract L8: drops with positions in a random turbulent flow

Gate 1 of physics-model-loop, round 1. Numbers: `portfolios-src/droplets/derive/L8_scales.cjs`. Air 10 °C, 850 hPa (ν = 1.69 × 10⁻⁵ m²/s).
Context: L0–L7 treat the cloud as a well-mixed box; drops have sizes but no positions, and turbulence enters only through
Ayala et al.'s (2008) mean relative speed, switched off outside its range (size ratio above 0.6, radii above 60 µm, Stokes number
above 1). Chapter 7 says plainly that no number was found for the near-equal collector pairs that make the first drizzle.
This level is the first step towards Numa's request for a stochastic velocity field instead of a "cylinder fall".

## 1. Question and observable

Does turbulence change how often drops meet, for the pairs that matter? Observable: the enhancement Γ = K_turb/K_grav of the
geometric collision kernel (rate of contacts per unit concentration of each partner, no hydrodynamic interaction), for three pairs
and two dissipation rates:

- 40/8 µm, the capture pair of observable 1 (where Ayala's formula applies: Γ = 1.056 at ε = 10⁻² m²/s³, 1.281 at 4 × 10⁻²);
- 60/50 µm, a near-equal collector pair of the kind that makes the first drizzle (chapter 6), outside Ayala's range;
- 20/18 µm, small near-equal droplets (Wang et al. 2008 report enhancements of about 2 and 7 at 100 and 400 cm²/s³ for 18/20 µm,
  including the change of collision efficiency, which this level does not compute).

ε = 10⁻² and 4 × 10⁻² m²/s³ (100 and 400 cm²/s³). Then, as a consequence: the measured Γ for near-equal collector pairs, put into
the exact stochastic runs of L5, gives the turbulent first-drizzle time in 100 and 1000 cm³, the number chapter 7 says is missing.

## 2. Picture and formal mechanism

Picture: dust in a sunbeam. The specks drift together in slow swirls; neighbours a hair apart move almost as one, and only the
heavier specks slide out of the swirls. A cloud drop's neighbours at contact are a few tens of micrometres away, far inside the
smallest swirl (the Kolmogorov length, 0.8 mm at ε = 10⁻² m²/s³), so the air carries both almost alike.

Mechanism (computed, `L8_scales.cjs`): at contact the separation a = R + r is 0.03 to 0.19 Kolmogorov lengths η. In that smooth
region the air's velocity differs across a by about a/τ_K (τ_K = √(ν/ε) the Kolmogorov time): 0.3 to 5 mm/s for our pairs, against
gravitational relative speeds of 170 mm/s (40/8), 89 mm/s (60/50) and 9 mm/s (20/18). Saffman and Turner's (1956) shear kernel is
0.1 % to 8 % of the gravitational one. Turbulence can therefore change the rate only through the drops' inertia: drops of Stokes
number St = τ_p/τ_K near 1 are flung out of eddies and gather in their edges (clustering), and fast drops can cross each other's
paths with velocities set far away ("sling" or caustics). For near-equal pairs gravity's speed difference is small, so these
effects can dominate. The level measures them instead of assuming a formula.

## 3. Model

- **Air:** a kinematic simulation (Fung et al. 1992): a sum of N_k random Fourier modes, u(x, t) = Σₙ [aₙ cos(kₙ·x + ωₙt) +
  bₙ sin(kₙ·x + ωₙt)] with aₙ, bₙ ⊥ kₙ (divergence-free by construction), mode amplitudes from the model spectrum
  E(k) = 1.5 ε^{2/3} k^{−5/3} exp(−1.5 β (kη)^{4/3}) between k_L = 2π/L and about 2/η (Kolmogorov inertial range with a dissipation
  cut-off), frequencies ωₙ = λ √(k³E(k)) (unsteadiness parameter λ ≈ 0.5). The flow is periodic in a cube of side L = 1 cm (12 η at
  ε = 10⁻²). The velocity gradient statistics are checked against ⟨(∂u/∂x)²⟩ = ε/(15ν) before any drop is added.
- **Drops:** each moves by dv/dt = [u(x, t) − v]/τ − g* e_z, dx/dt = v, with τ = v_T/g* (the drag-corrected response time of L2,
  so that in still air each drop falls at its Beard speed). Linear drag is used up to St ≈ 2 (drop Reynolds number below 2 here).
  The step uses the exact solution of the linear equation over Δt with u frozen during the step (Δt = τ_K/20).
- **Contacts:** ghost collisions (drops pass through each other, so concentrations stay steady). A contact is counted when the
  closest approach of two drops within a step, computed from their straight-line motion over the step, is below R + r. A cell list
  limits pair checks to neighbours. K = (contacts per s)/(n₁n₂V).
- **Size of the job:** 1 cm³, 1000 drops of each size (concentrations 10⁹ m⁻³, so ~10³ contacts per simulated second for 40/8), a few
  simulated seconds per run, ten independent flow realisations per case: standard errors of a few per cent.

## 4. Rejected alternatives

1. **An independent random velocity for each drop** (what I proposed first): two drops a few tens of µm apart would get independent
   air velocities of order the Kolmogorov speed u_K = 20 mm/s, where the real difference is about a/τ_K ≈ 1 mm/s. It would invent
   collisions by a factor of about 20. Rejected as wrong physics.
2. **Direct numerical simulation of the Navier–Stokes equations** (Ayala et al., Wang et al.): the reference method, beyond this
   study's means in a browser or a Node run of minutes.
3. **A stochastic model of the pair's relative velocity** (Langevin equation for the separation vector): cheaper, but it needs a
   closure for exactly the inertial effects the level wants to measure, and it gives no picture of drops in a flow.
4. **Ayala's formula extended outside its range:** its weak-inertia expansion is invalid at St ≈ 1 and for near-equal sizes.

## 5. Assumptions and their numbers

| Assumption | Number | Where it fails |
|---|---|---|
| Kinematic simulation represents the small-scale velocity gradients | gradients checked against ε/(15ν) | it has no sweeping of small eddies by large ones and wrong Lagrangian time correlations; it is known in the literature to misjudge clustering against DNS (scout to quantify) |
| Box of 1 cm, periodic | L = 12 η at 10⁻², 17 η at 4 × 10⁻²; integral scale of a real cloud ~ 10–100 m | large eddies missing: they sweep pairs together without changing their relative velocity at contact, so the kernel needs only the small scales; the absolute dispersion of drops is not modelled |
| Ghost collisions, no hydrodynamic interaction | geometric kernel | overcounts contacts; Γ is a ratio of geometric kernels, and the change of collision efficiency by turbulence (part of Wang et al.'s factor) is not computed |
| Linear drag | drop Re ≤ 1.5 for r ≤ 60 µm | larger drops |
| Gravity along z, drops in a frozen-frame periodic box | drops fall 0.18 m/s × 1 s = 18 box lengths per second | the falling drops sample the field along a line; recirculation in the periodic box repeats the field every L/v_T = 0.06 s: the flow's own time variation (ωₙ) must decorrelate it, checked by doubling L |

## 6. Exact results it must reproduce

1. ε → 0: Γ = 1 for every pair, the counting algorithm against the analytic gravitational kernel π(R + r)²|v_R − v_r| within 2 %.
2. No gravity, zero inertia (τ → 0): the Saffman–Turner kernel √(8π/15)(R + r)³/τ_K within 10 %.
3. Single drops: mean fall speed in the flow against the still-air speed, reported (KS may produce spurious fast sweeping).
4. 40/8 µm: compared with Ayala's Γ = 1.056 (10⁻²) and 1.281 (4 × 10⁻²); agreement within the statistical error is not required (the
   formula is an expansion), but a disagreement beyond a factor 2 in Γ − 1 is investigated before anything else is believed.

## 7. Prediction that could come out wrong (written before any code)

For the near-equal collector pair 60/50 µm at ε = 10⁻² m²/s³, Γ < 1.2: the shear difference at contact (2.7 mm/s) is 3 % of the
gravitational speed difference (89 mm/s) and the two drops' inertia nearly matches (St 0.86 and 0.64). If Γ ≥ 1.5, inertial
effects not captured by the speed ratio dominate, and chapter 6's first-drizzle times must carry the measured factor. At
4 × 10⁻² (St 1.7 and 1.3) no prediction is made.

## 8. Derived, cited, chosen, and the price

Derived here: the scale comparison of section 2, the gravitational and shear kernels, the exact linear-drag step, the closest-approach
test. Cited: the kinematic simulation method (Fung et al. 1992), the model spectrum (Pope 2000, chapter 6), Saffman and Turner
(1956), Ayala et al. (2008), Wang et al. (2008). Chosen: the cube size, N_k, λ, β, ghost collisions, linear drag. Price: Γ measured in a
kinematic flow is a model result, not a DNS result; the study states that and compares with DNS where DNS exists.
