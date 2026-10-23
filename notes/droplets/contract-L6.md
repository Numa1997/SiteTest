# Contract L6: turbulence, decided by a number

Gate 1. Source: `dossier-coalescence-turbulence.md` (Ayala, Rosa and Wang 2008 Part 2 read whole; Saffman and Turner 1956 read; Wang
et al. 2008 and Grabowski and Wang 2013 abstracts). Code: `physics.cjs` (`ayalaFactor`); numbers `derive/L6_ayala.py`, SCE runs logged
in `status.md`.

## 1. Question

Does the turbulence of a cloud change observable 1 or 2 by more than their uncertainty? Typical dissipation rates: ε = 10⁻³ to
10⁻¹ m²/s³ (10–1000 cm²/s³; Ayala et al. quote 100–650 cm²/s³ for cumulus).

## 2. Picture and mechanism

Picture: stir a cup of tea with tea leaves in it. The leaves are carried by the swirls, but the heavier ones lag behind the flow and
bump into the lighter ones. Turbulence adds two such effects to gravity: the air's shear moves neighbours past each other, and drops of
different inertia respond differently to the air's accelerations. Mechanism: the turbulent kernel is 2πR²⟨|w_r|⟩ g₁₂, with ⟨|w_r|⟩ the
mean radial relative speed at contact and g₁₂ the clustering factor (Ayala et al.). For a collector of 40 µm and a droplet of 8 µm,
the relevant scale is the collector's Stokes number τ_p/τ_K: 0.14, 0.44, 0.88 at ε = 10⁻³, 10⁻², 4 × 10⁻² m²/s³.

## 3. Model and the decision

Ayala et al.'s weak-inertia formula for ⟨|w_r|⟩ (shear, fluid acceleration and a gravity–shear coupling), g₁₂ = 1 (they find clustering
negligible for size ratios above 1.3), applied only inside its range: r/R ≤ 0.6, radii ≤ 60 µm, Stokes number ≤ 1; elsewhere gravity
alone. Threshold chosen from the literature before computing: X = 10 % (Ayala et al.'s formula gives +5.6 % on the governing pair
at 100 cm²/s³). Result (computed after): the kernel of 40/8 µm rises by +0.4, +5.6, +28 % at 10, 100, 400 cm²/s³; the SCE's t₉₀
shortens by 1.7 % at 100 cm²/s³ and 1.1 % at 400 cm²/s³, below X and below the efficiency band (13.5 against 11.4 min). Turbulence
therefore stays a stated check for observable 1. For observable 2 the route is collector–collector mergers of near-equal drops,
exactly where the formula does not apply and where DNS finds the largest enhancement (×2 at 100 cm²/s³ and ×7 at 400 for 18/20 µm,
Wang et al. 2008 abstract); the page says that turbulence would make the first drizzle earlier by an amount this study cannot compute.

## 4. Rejected alternatives

Saffman and Turner's shear kernel alone (it is under 1 % of gravity for 40/8 µm up to 1000 cm²/s³ and misses the inertial terms);
DNS-based efficiency enhancement tables (not obtained).

## 5. Prediction that could come out wrong

At 100 cm²/s³ observable 1 changes by less than X = 10 %. (Outcome, computed after this contract: −1.7 % in t₉₀, −4.4 % in t₅₀.)

## 6. Derived, cited, chosen, price

Cited: Ayala et al.'s formula and its range. Chosen: R_λ = 2 × 10⁴, the range cut. Price: the near-equal pairs that make the first
drizzle are left without turbulence, so observable 2 is an upper bound on the time in a turbulent cloud.
