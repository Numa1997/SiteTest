# Guinness on a jolted cart: the stout, its head, and the layers between them and the glass

All numbers for the solver in one list: `data-for-solver.md`.

Research note for Fig. 12, written 13 November 2026 on branch `claude/guinness-materials-research`. No fluid simulation was run.
**Report to:** the parent session "Guinness cart page rebuild" (session_01DGmqiq8T8BLo2FkMX6RM1D), which verifies everything here
before any computation. Every number is marked **Fact** (with source file and page),
**Inference** (my reasoning or arithmetic from facts, with the file that holds the arithmetic) or **Opinion**.
Source extracts are in `sources/`, derivations in `wolfram/` (first) and `sympy/` (check).

## Summary: the model in ten lines

1. The stout is a Newtonian liquid, ρ = 1007 kg/m³, μ = 2.06 mPa s. Once the pint has settled (more than about 2 min), treat it as
   bubble-free. Use the bubbly mixture only if the ride starts during the surge.
2. Jolts of 1–10 m/s² change the pressure by at most ρaH = 1.26 kPa (1.2 % of 1 atm). They make no new bubbles. Only splashing that
   traps air does.
3. Free surface without a head: no stress, plus a protein skin that makes the surface close to inextensible. That skin about doubles
   the wall damping.
4. The head is a very soft, very viscous solid made of the stout's own bubbles (Sauter radius R₃₂ = 34 µm). It is wet: liquid
   fraction 0.24–0.36, because a 19 mm column of 34 µm bubbles cannot drain drier and takes 25–110 min even to reach that.
   Yield stress τ_y = 0.51 (γ/R)(Φ − 0.62)² = 1–17 Pa; modulus G₀ = 1.4–1.64 (γ/R) Φ(Φ − 0.64) = 25–240 Pa
   (Φ = 1 − φ_l, the gas fraction; γ the surface tension).
5. Its effective viscosity is 300–10 000 times the stout's (0.65–21 Pa s at 1–30 s⁻¹). A wave of its own would die in 2–120 ms,
   against a slosh period of 292 ms. So the head rides the stout surface as one sheet and makes no waves of its own.
6. On the stout the head acts as a lid with mass ρ_f h_f per unit area. It presses down with ρ_f h_f g_eff, does not slip on the
   liquid, and slides on the glass with Plateau-border friction f = ξ γ Ca^(2/3) per unit border length.
7. It yields (flows) only where the stress beats τ_y. The test is the Bingham number Bi = τ_y/(ρ_f a h_f). At 1 m/s² Bi = 0.2–4:
   it holds its shape at the drier end. At 10 m/s² Bi = 0.02–0.4: it yields at the hardest jolts and then flows like a thick cream.
8. Thrown out, a lump 10 mm across needs 0.16–0.58 s to be pulled apart (time = η_eff L/γ), longer than it flies, so the head leaves
   as lumps. Stout breaks at the capillary scale √(γ/ρa) = 2 mm, so it leaves as drops.
9. Over a 20 s ride the head loses volume only by spilling and by what it leaves on the glass. Its drainage (25–110 min for 34 µm
   bubbles) and nitrogen bubble coarsening (none in 3 min) are far too slow to matter. Stout recedes from glass at a contact angle of
   about 4–6° (Guinness, Hamlett 2015): it leaves a film, 7–140 µm thick depending on speed (Landau–Levich–Derjaguin).
10. Damping of the first mode, ζ = γ_d/ω: wall Stokes layer 0.0051, plus protein skin about 0.0051, plus contact line (up to ×2.4).
    A foam lid adds sub-linear wall friction that stops the slosh in finite time.

### Parameter table (the fewest the physics allows)

| Symbol | Meaning | Value | Range | Source |
|---|---|---|---|---|
| ρ_l | stout density, 5–6 °C | 1007 kg/m³ | 1006–1007 | Fact: benilov2012 p.1; watamura2019-scirep9-5718 SI Table S1 |
| μ_l | stout viscosity, 6 °C | 2.06 mPa s | 2.0–2.23 | Fact: benilov2012 p.1; watamura2019 (2.03–2.21 at 5 °C); robinson2008 |
| γ | surface tension of beer | 0.045 N/m | 0.038–0.048 static; 0.052–0.055 while stretched | Fact: ronteltap1989 Table 4.5 p.38; chatzigiannakis2025 Table I (lagers and ales, not stout) |
| R | bubble (Sauter) radius in the head | 34 µm | 33–36 µm | Inference: the head is made of the stout's own bubbles and N₂ stops them growing; Sauter radius of Watamura's measured log-normal (mean D 61 µm, σ = 0.24 read off SI Fig. S2; wolfram/04). Confirmed by Watamura & Sugiyama 2024: D = 59 ± 15 µm (web-watamura2024-oleoscience-table1.txt) and by the settling time (61 µm clears 125 mm in 126 s, measured ≈ 120 s) |
| φ_l | liquid fraction of the head | 0.27 | 0.24–0.36 | Inference (wolfram/05): equilibrium of a 19 mm column of 34 µm bubbles gives 0.36 at the bottom → 0.24 at the top (K = 3.2; 0.18 for an ordered foam); reaching it takes 25–110 min, so a 2–5 min old head is at least this wet. No weighing of a Guinness head found |
| h_f | head thickness as served | 19 mm | 10–24 mm | Fact: 18–20 mm (brief, Nature Rev. Phys. 5, 197, not re-read here); ESGI "about 1 cm" (power2009 p.177); my read-off of Watamura Movie S1 ≈ 24 ± 4 mm (catalogue below); 17.5–22.2 mm two minutes after three kinds of pour (web-kegworks2019) |
| C | yield-stress prefactor, τ_y = C (γ/R)(Φ − Φ_c)² | 0.51 (Φ_c = 0.62) | 0.51–0.53 | Fact: mason1996-jcis179.txt p.443 (C = 0.51, Φ_c = 0.62, emulsions); saintjalmes-durian1999 (0.53, foam) |
| a | modulus prefactor, G₀ = a (γ/R) Φ(Φ − 0.64) | 1.4 | 1.4–1.64 | Inference from Facts: 0.51/0.365 (dry-foam limit, saintjalmes-durian1999) = 1.40, as costa2012 quotes; 0.6/0.365 (mason1995, which prints no prefactor) = 1.64. The "1.7" of the brief is not printed in any source read |
| Φ_c | gas fraction at jamming | 0.64 | 0.62–0.64 | Fact: saintjalmes-durian1999 (0.635 ± 0.01), mason1996 (0.62 fit) |
| ξ | Plateau-border wall-friction coefficient, stiff surfaces | 6.82 | 4.94–6.82; fits need up to ×4 | Fact: cantat2013 |
| θ, θ_r | contact angle of Guinness on clean glass: static, receding | 28.5° ± 2.0°, 4.2° ± 2.4° | static 19–30° for four beers; receding 4–6° | Fact: Hamlett et al. 2015 J. Am. Soc. Brew. Chem. 73, Table 2 (web-hamlett2015-jasbc-beer-contact-angles.txt), bottled Guinness Original degassed, room temperature, HCl-cleaned glass. Row order of the table to be confirmed against the journal |

Derived, not free: ρ_f = φ_l ρ_l; G₀ and τ_y from (R, φ_l, γ); bubble slip from (R, μ, ρ); the damping of each layer from (ν, ω, R).

### The two composite materials, in numbers

| | Stout (a bubbly liquid) | Head (a foam) |
|---|---|---|
| What it is | liquid with rigid gas spheres, mean diameter 59–61 µm (radius ≈ 30 µm), log-normal σ ≈ 0.24 | packed bubbles of the same population, Sauter radius 34 µm |
| Gas fraction | 0.08–0.097 canned bulk; ≈ 0.1 pub draught; 0.02 served; < 10⁻³ settled (> 2 min) | Φ = 0.64–0.76 (φ_l 0.24–0.36), mean ≈ 0.73 |
| Density | ρ_m = (1 − α) 1007: 987 at α = 0.02, 957 at α = 0.05 kg/m³ | ρ_f = φ_l ρ_l = 240–360 kg/m³ (272 at φ_l = 0.27) |
| Viscosity or stiffness | μ_m = 2.06 mPa s × (1 + 2.5α): 2.16 at 0.02, 2.32 at 0.05 | G₀ 25–240 Pa (122–143 at φ_l = 0.27); τ_y 1–17 Pa (8 at 0.27); effective viscosity 0.65–21 Pa s at 1–30 s⁻¹ |
| Slip or drift | bubble slip (2a²ρ/9μ)(Du/Dt − g_eff): 1.0 mm/s at 1 g for 61 µm | drainage 1.2–2.1 µm/s by gravity; 25–110 min to equilibrium |
| Lifetime | settles in ≈ 120 s | drains over 25–110 min; no coarsening in 180 s; head 17.5–22 mm two minutes after the pour (web-kegworks2019) |
| Rheology | Newtonian (beer, 92–921 s⁻¹, r² ≥ 0.99) | Herschel–Bulkley (yield stress + Ca^0.47) |

### Every boundary layer as a boundary condition (details in 3.3)

| Interface | Condition | Numbers |
|---|---|---|
| Stout on glass | no slip; Stokes layer δ = √(2ν/ω) | δ = 0.436 mm; ζ = 0.0051, γ_d = 0.110–0.119 s⁻¹ for mode (1,1) |
| Stout contact line on glass | Coulomb friction: the line holds until γ(cos θ − cos θ_s) exceeds the hysteresis; it recedes at θ_r ≈ 4° and leaves a film h = 0.946 ℓ_c Ca^(2/3) (×2.5 for rigid surfaces) | θ_s = 28.5°, θ_r = 4.2° (Hamlett 2015, Guinness); Δcos θ = cos 4.2° − cos 28.5° = 0.12; film 7–140 µm at 1 mm/s–0.1 m/s; ×1.5–2.4 on the wall damping |
| Head on glass | sliding with Plateau-border friction τ_w ≈ (ξγ/R)Ca^(2/3), ξ = 6.82 | 18–36 Pa at 0.01 m/s, 85–170 Pa at 0.1 m/s; finite-time stop (Viola α = 0.010–0.030) |
| Head on stout | the head is a lid with no slip: u_t(stout) = u_f; normal stress p = ρ_f h_f (g_eff·n) | ρ_f h_f ≈ 3.8 kg/m² (1–7.6); foam velocity decays upward over 16.8 mm (Sauret); adds ζ ≈ 0.0051 |
| Bare stout surface (after a spill) | p = −γκ; protein skin close to inextensible (tangential no slip on the surface) | γ = 0.045 N/m (0.038–0.055); dilatational modulus 5–25 mN/m; adds ζ ≈ 0.0051 |

---

## Part 1. The body: the stout

### 1.1 Facts

- **Density and viscosity.** Fact: "ρ = 1007 kg m⁻³ … μ = 2.06 × 10⁻³ Pa s" at 6 °C (benilov2012-arxiv1205.5233.txt, p.1).
  Watamura et al. measured 1006 kg/m³ and 2.03–2.21 mPa s at 5 °C. Their viscosity was measured above 10 °C and extrapolated
  (watamura2019-scirep9-5718.txt, lines 13–22). Robinson et al. give about 2 mPa s at about 5 °C and specific gravity 1.007, from
  Diageo (robinson2008-physfluids20-067101.txt, p.067101-8). Inference: about −2.3 %/K near 6 °C, from Severa & Los on a dark
  lager, not on stout (severa-los2008-acta56-303-dark-beer-viscosity.txt).
- **Newtonian.** Fact: beer on a Bohlin rheometer at 92–921 s⁻¹ and 5 °C gave a linear stress–rate curve with r² ≥ 0.99
  (jin2004-jinstbrew110-104-beer-viscosity-newtonian.txt, Methods). These were beers rebuilt from concentrate. Nobody has done a
  shear-rate sweep on Guinness. Inference: at 2 % sugars and 4 % ethanol there is nothing to make it non-Newtonian. A sweep from
  1 to 1000 s⁻¹ on a cone-and-plate rheometer at 6 °C would settle it in an afternoon.
- **Dissolved gas.** Fact: the can equilibrates at 3.8 bar at 8 °C with 79 % N₂ / 21 % CO₂. That gives CO₂ ≈ 2 g/L (0.8 bar) and
  N₂ ≈ 0.072 g/L (power2009-esgi70-initiation-of-guinness.txt, pp.143–144, 176–177). Fact: the Guinness widget patent gives N₂ at
  1.5–3.5 % v/v and CO₂ at 0.8–1.8 vol/vol, i.e. 1.46–3.29 g/L
  (patent-US4832968-GB2183592-forage-byrne-widget.txt). Fact: Henry constants at 8 °C are CO₂ 2.50 and N₂ 0.0241 g L⁻¹ bar⁻¹ (ESGI
  Table 8). Inference: at 6 °C in water, CO₂ 2.5–2.7 and N₂ 0.024–0.025 g L⁻¹ bar⁻¹ (sander2015-acp15-4399-henry.txt with its
  temperature terms). No beer-specific values were found. Fact: Guinness supersaturation is about 2.8 (ESGI p.147).
- **The gas mix, settled.** Fact: 60/40 and 70/30 are CO₂/N₂ blends for ordinary lagers and ales. Stout gas ("G-Mix") is 25/75 to
  30/70 CO₂/N₂ (ba-draught-beer-quality-manual-2011-gas-blends.txt, p.30). So the brief's "70 % N₂ / 30 % CO₂" is right for the
  dispense gas, and a web source's "60/40" is the ale blend. The sealed can is a different equilibrium, 79/21 N₂/CO₂ (ESGI). No
  public Diageo specification was found.
- **Bubbles.** The measured sizes disagree by a factor of two.
  - Fact: mean diameter 54–68 µm, log-normal, at least 3000 bubbles per run, unchanged over 15–45 s, gas fraction 8 % in canned
    Guinness within 10 s of opening (watamura2019-scirep9-5718.txt, SI Table S1).
  - Fact: Robinson et al. give diameters 94–122 µm (robinson2008).
  - Fact: Benilov's 122 µm is a diameter taken from Robinson, not his own measurement (benilov2012 p.2).
  - Fact: draught in a pub carries about 0.1 gas fraction, and about 0.02 once served after the two-part pour (benilov2012 p.2).
    Near the wall early in settling it is 0.23–0.32 (robinson2008 p.067101-9).
  - Fact: settling takes about 120 s measured, against 43 s computed for 122 µm bubbles (benilov2012 p.2). Inference: a 61 µm
    bubble rising 125 mm by Stokes' law takes 126 s, which matches the 120 s.
- **The surge.** Fact: the cascade shows best where the wall leans 5–20° from vertical, and moves down at about 35 mm/s
  (watamura2019). Fact: the ultrasonic surger runs at 20–80 kHz, example 40 kHz (patent-US7520212-diageo-surger.txt), while the ESGI
  model used 125 kHz (power2009 p.147).
- **Nucleation by a knock.** Fact: tapping a bottle sends a pressure pulse of about 100 kPa lasting 0.24 ms. That breaks up existing
  bubbles and nucleates more (rodriguez2014-arxiv1403.2678-beer-tapping.txt, p.3). Fact: homogeneous nucleation needs a
  supersaturation of several hundred, against Guinness's 2.8 (ESGI pp.147, 150). Fact: air trapped by "banging a glass down",
  shaking or swirling is the route that works (ESGI p.151).

### 1.2 Equations

**Mixture form (drift-flux).** Let α be the gas volume fraction and u the volume-averaged velocity. The bubbles are rigid spheres
because surfactants coat them. The 1/2 is the added-mass coefficient of a sphere. Neglecting the bubble's own mass, the force
balance on one bubble is

0 = ρ_l V (Du/Dt − g_eff) + ½ ρ_l V (Du/Dt − dv/dt) + 6πμ a (u − v),   g_eff = g − a_glass.

Its steady solution is the slip velocity (wolfram/02, checked in sympy/01_02)

**v − u = (2a²ρ_l/9μ)(Du/Dt − g_eff)**,

with relaxation time τ_b = ρ_l a²/(9μ) = 0.11–0.20 ms. That is 10³ times shorter than anything on the cart, so the slip is
always at its local equilibrium. The equations a GPU grid can carry are:

- ∂α/∂t + ∇·[α(u + v_s)] = 0,   v_s = (2a²ρ_l/9μ)(1 − α)^n (Du/Dt − g_eff),   n ≈ 4.5–5.6 (brzinski-durian2018);
- ρ_m(Du/Dt) = −∇p + ∇·[2μ_m D] + ρ_m g_eff,   ρ_m = (1 − α)ρ_l,   μ_m = μ_l(1 + 5α/2),   ∇·u = −∇·(α v_s) ≈ 0.

Einstein's μ(1 + 2.5α) is the rigid-sphere value; the second-order term 7.6α² adds less than 2 %. I read it in
gerard-varet-hillairet2020, not in Einstein's own papers.

**Regime numbers for a 20 s ride** (wolfram/02):

| Number | Value | Meaning |
|---|---|---|
| Stokes rise U_b (a = 27–61 µm) | 0.7–4.0 mm/s | bubbles drift 14–80 mm in 20 s, slower than the slosh (≈ 0.1 m/s) by 25–140× |
| Slip under a jolt | U_b × \|g − a\|/g, between 0 and 2 U_b | a 10 m/s² upward jolt doubles the slip; free fall stops it |
| Einstein correction at α = 0.02 / 0.05 | +5 % / +12.5 % in μ | changes the wall damping by √(1.05) = 2.5 % |
| Density change at α = 0.02 / 0.05 | 987 / 957 kg/m³ | changes nothing that is uniform; only gradients of α act |
| Buoyancy frequency of a clearing front (Δα = 0.02 over 50 mm) | N = 2.0 rad/s | N/ω = 0.09: internal waves are 11× slower than the slosh and do not couple |
| Pressure swing ρaH at 10 m/s² | 1.26 kPa = 1.2 % atm | far below the 100 kPa of a tapped bottle |
| Acoustic transit H/c | 84 µs | jolts last ≥ 10 ms ≫ 84 µs, so the stout stays incompressible, with no water hammer |
| Water hammer ρcΔv for a hard knock (Δv = 0.1 m/s stopped in < 0.1 ms) | 149 kPa | a knock on a table can nucleate; the cart's suspension cannot deliver one |
| Reynolds number of the slosh (U = 0.1 m/s, L = R) | 1.9 × 10³ | laminar bulk, thin boundary layers |
| R√(ω/ν) (Womersley) | 127 | the boundary layers are thin compared with the glass |

### 1.3 Conclusion for the body

- Inference: in a settled pint (more than 2 min) α < 10⁻³. Use a single-phase Newtonian liquid with ρ = 1007 kg/m³ and
  μ = 2.06 mPa s, which means ν = 2.05 × 10⁻⁶ m²/s, not water's 10⁻⁶ that the solver uses today
  (docs/simulations/fig12-beer-slosh.md, "The model").
- Inference: carry α only if the ride starts within 2 min of the pour. Then add α with the slip above (one scalar field, one
  parameter a), with the Boussinesq buoyancy term −α ρ_l g_eff.
- Inference: the cart makes no new bubbles. Splash-entrained air does: a drop or sheet that falls back traps air, which then rises
  as the surge does.

### 1.4 Uncertain, and how to measure it

- Bubble size in a served pint: 54–68 µm (Watamura) against 94–122 µm (Robinson). A macro photograph through the wall with a
  calibrated scale would decide it.
- Void fraction against time after a two-part pour: no time series exists. Light transmission through the pint, logged against
  time, would give one.
- A shear-rate sweep of Guinness itself.

---

## Part 2. The head: the foam

### 2.1 Facts

- **No measurement of a stout head exists** for bubble size, liquid fraction, surface tension or collapse rate. Searched: Ronteltap,
  ESGI, Lee & Devereux, Benilov, Watamura, Bamforth (paywalled). Roads are listed at the end.
- **Surface tension.** Fact: beer 38.0–47.4 mN/m at rest and 52–55 mN/m while its surface is stretched (ronteltap1989-thesis.txt,
  Table 4.5, p.38). Fact: lagers and Belgian ales 40.8–48.1 mN/m (chatzigiannakis2025-pof37.txt, Table I). Fact: surface pressure of
  24 lagers 25–30 mN/m, dilatational modulus 5–25 mN/m (wierenga2023-acis312-102845.txt, pp.4–5).
- **Nitrogen keeps the bubbles as they are.** Fact: in nitrogen foam made from beer, the mean radius starts near 100 µm, and after
  3 minutes no bubble had shrunk. CO₂ foam coarsens visibly (ronteltap1989 pp.114–115). Fact: nitrogen foams were too stable for the
  modified NIBEM collapse test (p.107). Rudin drainage times were 633–757 s for N₂ against 142–293 s for CO₂ (Table 8.1).
- **How beer foam dies.** Fact: mainly by drainage and gas loss through the top, not by bubbles merging. Small bubbles stick to the
  glass more strongly than to each other, and the head collapses faster near the wall (ronteltap1989 abstract, pp.85, 90).
- **Make-up.** Fact: "realistic" fresh beer foam is 60 % gas and 40 % liquid (ronteltap1989 p.82). A gas fraction of 0.80 is used as
  a model input (lee2018-ajp86.txt). Fact: the ESGI report gives the observed head as "about 1 cm" (power2009-esgi70-guinness.txt,
  p.177).
- **Rheology of wet foam.** Fact, as quoted by costa2012-thesis.txt from Höhler & Cohen-Addad (2005), with Φ the gas fraction and
  Φ_c = 0.64:
  - **G₀ = 1.4 (γ/R₃₂) Φ(Φ − Φ_c)**;
  - **τ_y = a_y (γ/R)(Φ − Φ_c)²**, with a_y = 0.5–1.

  Fact: one measured check, 5 % liquid and R = 24 µm, gave G₀ = 206 Pa, below the formula (besson2008-hal.txt). So the prefactor is
  uncertain by a factor of a few. Later read in the originals (mason1995-prl75.txt, mason1996-jcis179.txt, saintjalmes-durian1999-jrheol43.txt): Mason 1995 prints no modulus prefactor (its dry limit 0.6 σ/r implies 1.64); the yield law is τ_y = 0.51 (σ/a)(φ − 0.62)² (Mason 1996 p.443); the "1.7" of the brief is printed nowhere.
- **Flow beyond yield.** Fact: for 1–20 % liquid (tcholakova2008-pre78.txt), stresses in units of γ/R with Ca = μγ̇R/γ:
  - films only: τ ≈ 1.162 Ca^0.47 Φ^(5/6) (Φ − 0.74)^0.1 (1 − Φ)^(−1/2);
  - films and menisci: τ ≈ 0.7 Ca^0.47 Φ^(5/6)/(1 − Φ)^0.5 + 8 Ca^0.7 Φ^(5/6)/(1 − Φ)^0.15.

  So the head is a Herschel–Bulkley material: a yield stress, then a stress that grows about as γ̇^0.5.
- **Foam on sloshing liquid.**
  - Fact (sauret2015-pof27.txt, read whole): five layers of 3 mm bubbles cut the forced amplitude tenfold and barely move the
    frequency (3.1 Hz against 3.3 Hz predicted). The damping law is 1/τ = 1/τ_l + (1/τ_f∞)(1 − e^(−ξ/ξ_c)), with
    1/τ_f∞ = 9 ± 3 s⁻¹ and ξ_c = 5 ± 2 layers. The loss is the bubbles' liquid edges sliding on the walls, f = Kγ Ca^(2/3) for
    Ca < 10⁻². The bubble speed in the foam falls off upward as exp(−z/16.8 mm).
  - Fact (viola2016-pof28.txt, read whole), a cylinder of radius 37.05 mm at 3.50 Hz, close to the pint:
    - frequency unchanged by the foam;
    - model X'' + ω₀²X = −2σω₀X' − α ω₀^(4/3) R^(1/3) X'|X'|^(−1/3), with ω₀ = 22.00 rad/s and σ = 9.8 × 10⁻³;
    - α = 0.010–0.030 for layers 2.5–6.5 mm thick, rising with thickness, expected to level off in thick foam;
    - their foam: bubbles 0.25 mm, 25 % liquid, γ = 31.5 mN/m;
    - the waves stop in finite time, 5–12 s from 5 mm.
- **Wall friction** (cantat2013-pof25.txt). Fact:
  - f = ξγCa^(2/3) + ζγ(l/r_m)Ca^(1/3) per unit length of Plateau border, with (ξ, ζ) = (4.94, 0) for mobile, (6.82, 0.94) for
    sliding and (6.22, 0) for rolling surfaces;
  - measured speed exponents are 0.28–0.66 at 10–25 % liquid;
  - Denkov's Ca^(1/2) law does not apply to foam against a wall.

  Fact: beer surfaces are stiff, with Boussinesq number Bq ≫ 1 (chatzigiannakis2025), so the sliding branch applies.
- **Foam ejected as a lump, or spilling over a rim:** no published study found (searched as listed at the end).

### 2.2 Why the head is thick, makes no waves, and leaves as lumps

The picture: tilt a jelly on a plate, and it leans as one piece. It does not ripple, because ripples would have to bend it, and
bending costs elastic energy that the jelly stores at a stiffness far above what the slow tilt supplies. The head is that jelly.
It is a dense pack of 50–100 µm bubbles held in shape by surface tension, with a stiffness of order γ/R ≈ 450–900 Pa.

1. **Thick.** The head is thick because it does not collapse. Nitrogen dissolves 66 times less than CO₂ (molar ratio, sander2015),
   so small bubbles cannot empty into big ones. Ronteltap saw no coarsening in 3 min. The bubbles stay small, the films between
   them stay thick, and drainage takes 10–13 min (Fact, Table 8.1). A CO₂ head of the same height coarsens and drains in 2–5 min.
2. **No waves of its own.** The head's natural shear wave crosses its 19 mm thickness in h/√(G₀/ρ_f) = 7–65 ms (wolfram/03), against
   a slosh period of 292 ms. Inference: the head therefore moves quasi-statically with the stout surface beneath it. A gravity wave
   on the head's own upper surface would need the head to flow, and it cannot flow below its yield stress. Inference: a thin
   elastic plate on water stiffens the mode. That estimate changes f₁₁ by −10 % to +11 % over the parameter range (wolfram/03).
   Sauret and Viola both measured no change, so the head as a bending plate overstates it. Opinion: model it as a mass-loaded lid
   that follows the surface, not as a plate.
3. **Leaves as lumps.**
   - The stout is a liquid. A sheet of it thrown off at acceleration a breaks where surface tension can no longer hold it, at the
     capillary length √(γ/ρa) = 2.1 mm at 10 m/s². So it leaves as drops.
   - The head is a yield-stress solid. A piece of it holds together as long as its own inertial stress ρ_f a L stays below τ_y. So
     the largest piece that survives is **L\* = τ_y/(ρ_f a)**, which is 3–170 mm at 10 m/s² (wolfram/03), as big as or bigger than
     the head is thick.

   Inference: so a bump throws the head out as lumps of the head's own size, never as spray.
4. **Walking fast and bumping into things.** The liquid underneath sloshes like any liquid. The head on top behaves as a lid
   with three effects:
   - its mass lowers nothing measurably;
   - its no-slip underside adds a second Stokes layer, which doubles the damping (Part 3);
   - its sub-linear wall friction stops small motions dead, in finite time, instead of letting them ring down slowly.

   Inference: this is why a pint does not behave as you would expect a plain liquid or an ordinary (CO₂, coarsening, mobile)
   foam to.

### 2.3 Equations: the head as a state on a grid

The head stays a thin layer on the stout surface. Its state, per surface cell:

- **h_f(x, y, t):** thickness, 19 mm at the start.
- **φ_l:** liquid fraction. Held constant over a ride, since drainage takes 633–757 s.
- **R:** bubble radius. Held constant: no coarsening in 3 min.
- **u_f:** in-plane velocity of the foam sheet.
- **m_lost:** mass lost to the glass and to spills.

**Boundary condition on the stout's free surface under the head** (Inference: the head is a lid that does not slip on the liquid
beneath it):

- normal stress: p_surface = ρ_f h_f (g_eff · n), with ρ_f = φ_l ρ_l, where g_eff · n is the component of g_eff along the surface
  normal. This is the head's weight. At a 10 m/s² upward jolt it rises to 2 g;
- tangential velocity: u_tangential(stout surface) = u_f, no slip. Sauret's speed profile decays only over 16.8 mm, so the foam's
  base moves with the liquid;
- at the glass, the sheet slides with stress τ_w ≈ (ξγ/R) Ca^(2/3) per unit contact area, Ca = μ|u_f|/γ, ξ = 6.82
  (cantat2013). Wolfram/03 gives 18–36 Pa at 0.01 m/s and 85–170 Pa at 0.1 m/s.

**Motion of the sheet** (depth-averaged, Inference). The sheet is a membrane with a yield stress (a Bingham plate):

ρ_f h_f Du_f/Dt = ∇_s·(h_f T) + τ_base + ρ_f h_f g_eff,t,

- τ_base: the shear stress the stout's surface layer exerts on the foam;
- T: the in-plane stress. Elastic, T = G₀ε, while |T| < τ_y. Regularised Herschel–Bulkley (formulas above) once |T| ≥ τ_y.
- g_eff,t: the tangential part of g_eff, the cart's jolt as felt in the glass frame.

In a GPU solver the cheapest correct choice is a regularised Bingham viscosity in the foam cells,

μ_f = μ_∞ + τ_y/(|γ̇| + ε),   ε = τ_y/μ_max.

Its parameters (τ_y, ρ_f, μ_∞) all follow from (R, φ_l, γ, μ_l). Opinion: the depth-averaged sheet is enough while the head is
intact. A 3D foam phase (level-set material flag, same Bingham law) is needed only for lumps that leave.

**Volume balance**, dV_f/dt = −Q_spill − Q_cling − Q_drain − Q_collapse:

- Q_spill: foam carried over the rim. Advect h_f with u_f; what crosses the rim leaves as a lump of size L*.
- Q_cling: a film of foam left on the glass where the head's edge recedes. Its thickness is not measured (see 2.5).
- Q_drain, Q_collapse: about h_f/650 s ≈ 0.03 mm/s. Inference: about 0.6 mm in a 20 s ride, so they can be left out.

**Regime numbers at the cart's accelerations** (wolfram/03, checked in sympy/03; R = 50/100 µm, a_y = 0.5–1). Superseded by 2.5, which fixes R = 34 µm and φ_l = 0.24–0.36 from physics; kept for the record:

| φ_l | G₀ Pa | τ_y Pa | Bi at 10 m/s² | Bi at 1 m/s² | L* at 10 m/s², mm |
|---|---|---|---|---|---|
| 0.05 | 186–371 | 22–87 | 2.3–9.0 | 23–90 | 43–172 |
| 0.10 | 147–295 | 15–61 | 0.8–3.2 | 8–32 | 15–60 |
| 0.20 | 81–161 | 6–23 | 0.15–0.6 | 1.5–6 | 3–11 |
| 0.30 | 26–53 | 0.8–3.2 | 0.01–0.06 | 0.1–0.6 | 0.3–1.1 |

Reading it (Inference):
- Bi > 1 means the head stays a solid plug.
- At 1 m/s² the head is solid unless it is very wet (φ_l ≳ 0.3).
- At the hardest jolts (10 m/s²) a 10–20 % liquid head is close to yielding: it holds together with Bi ≈ 0.2–3.
- The wall stress at slosh speeds (18–170 Pa) is as large as τ_y or larger. Opinion: so the head both slides at the wall and
  shears near it, and only a measurement of φ_l and R will say which wins.

### 2.4 Parameter table for the head

| Quantity | Value | Range | Status |
|---|---|---|---|
| γ | 0.045 N/m | 0.038–0.055 | Fact for beer (ronteltap1989, chatzigiannakis2025) |
| R₃₂ | 34 µm | 33–36 µm | Inference from measured distributions (2.5) |
| φ_l | 0.27 | 0.24–0.36 | Inference from the column equilibrium and drainage time (2.5) |
| ρ_f = φ_l ρ_l | 272 kg/m³ | 240–360 | derived |
| G₀ | 122–143 Pa | 25–240 | derived (prefactor 1.4–1.64) |
| τ_y | 8 Pa | 1–17 | derived (C = 0.51, Φ_c = 0.62) |
| effective viscosity | 2 Pa s at 10 s⁻¹ | 0.65–21 Pa s at 1–30 s⁻¹ | derived (Tcholakova 2008 + τ_y) |
| h_f | 19 mm | 10–24 | Fact / read-off |
| ξ (wall friction) | 6.82 | 4.94–27 | Fact (cantat2013, fits up to ×4) |

### 2.5 Worked out from the bubble size (added 13 November 2026, after review)

The first version left the head's bubble size and liquid fraction as guesses (25–100 µm, 0.05–0.4). Both follow from physics and
from measurements of the stout:

1. **Bubble size.** The head is built from the bubbles that rise out of the stout; nitrogen bubbles do not coarsen in minutes
   (ronteltap1989 pp.114–115). So the head's bubbles are the stout's. Watamura's measured distribution (≥ 3000 bubbles, microscope
   lens, log-normal, mean D = 61 µm) read off their SI Fig. S2 has half-heights near 47 and 82 µm, so σ = 0.24 ± 0.05 and the Sauter
   diameter D₃₂ = 68 µm: **R₃₂ = 34 µm (33–36)** (wolfram/04, sympy/04). Two checks: Watamura & Sugiyama 2024 measured
   59 ± 15 µm; and 61 µm bubbles clear a 125 mm column in 126 s by Stokes' law, against the measured ≈ 120 s, while Robinson's
   122 µm would clear it in 32 s. Robinson counted at the wall without a microscope; their 94–122 µm sit in the tail of Watamura's
   distribution (marked as arrows in SI Fig. S2).
2. **Liquid fraction.** A foam column is held by surface tension against its weight: the osmotic pressure Π = K (γ/R)(ε_c − ε)²/√ε
   (forel2016, quoting Maestro 2013; K = 3.2, ε_c = 0.36 disordered) rises with height as dΠ/dz = ρg(1 − ε). With R = 34 µm the
   capillary pressure γ/R = 1324 Pa is ten times the weight of the head (131 Pa), so the head cannot drain dry: at equilibrium
   ε = 0.36 at its base, 0.27 at 10 mm, **0.235 at the top of 19 mm** (0.18 for an ordered foam). Reaching that equilibrium takes
   25–95 min by capillary diffusion and hours by gravity (permeability k = R²ε²/300, rigid protein surfaces); Ronteltap's measured
   N₂ foam drainage, 633–757 s at R ≈ 100 µm, scaled by R² gives 91–109 min. So **a 2–5 min old head has ε between 0.24 and 0.36**
   (wolfram/05, sympy/05). Gemini's unsourced "0.05–0.15 drained" is ruled out.
3. **What follows.** At ε = 0.22 / 0.27 / 0.30 / 0.34: G₀ = 202–237 / 122–143 / 78–91 / 24–29 Pa; τ_y = 17 / 8.2 / 4.3 / 1.1 Pa;
   Bi at 1 m/s² = 4.1 / 1.6 / 0.75 / 0.17; at 10 m/s² = 0.41 / 0.16 / 0.075 / 0.017; effective viscosity at 10 s⁻¹ = 3.1 / 2.0 / 1.5 /
   1.1 Pa s (500–1500 × stout); damping time of a wave of its own (k = 47 m⁻¹) 0.016–0.07 s at 10 s⁻¹; breakup time of a 10 mm
   lump 0.58 / 0.35 / 0.25 / 0.16 s.
4. **Reading it.** The head is not a stiff plug: it is a soft solid (τ_y of a few pascals) with an enormous viscosity. It keeps its
   shape under its own weight and gentle motion, yields under the hard jolts, and when it flows it flows like thick cream. Its own
   waves are overdamped, and a thrown piece does not have time to fragment: lumps, not spray.
5. **The film left on the glass** (lacing). Guinness recedes from clean glass at θ_r = 4.2° (Hamlett 2015), so the contact line
   does not pull back cleanly: it leaves a film. Landau–Levich–Derjaguin (snoeijer2008, rio-boulogne2017): h = 0.946 ℓ_c Ca^(2/3),
   ℓ_c = √(γ/ρg) = 2.13 mm, ×4^(2/3) = 2.5 for rigid protein surfaces: 6.5 µm at 1 mm/s, 19 µm at 5 mm/s, 48 µm at 2 cm/s,
   140 µm at 0.1 m/s (wolfram/04). Valid for Ca < 10⁻² (here 5 × 10⁻⁵ to 5 × 10⁻³).
6. **Contact angle from a photograph** (for a later check): the meniscus climbs h = ℓ_c √(2(1 − sin θ)) up a vertical wall:
   2.13 mm at 30°, 1.80 mm at 40° (wolfram/04).

### 2.6 Measured by others (web, 13 November 2026), with how they were measured

| Quantity | Value | Who, how | File |
|---|---|---|---|
| Contact angle, Guinness on HCl-cleaned glass | static 28.5 ± 2.0°; other rows 22.3 ± 2.1°, 4.2 ± 2.4° | Hamlett et al. 2015, Krüss DSA10 sessile drop, bottled Guinness Original degassed 72 h, room temperature | web-hamlett2015-jasbc-beer-contact-angles.txt |
| Same on hydrophobised glass | 109.2° static | same | same |
| Bubble diameter, Guinness | 59 ± 15 µm at 9.7 % gas | Watamura & Sugiyama 2024, Oleoscience Table 1 | web-watamura2024-oleoscience-table1.txt |
| Bubble diameter, canned Guinness | 40–120 µm | Alexander & Zare, Stanford, 750 frames per second | web-zare-stanford-guinness-filming.txt |
| Head 2 min after pouring, tap Guinness | 17.5 mm (two-part), 20.6 mm (Irish), 22.2 mm (one-shot) | KegWorks 2019, one pour each | web-kegworks2019-guinness-head-height.txt |
| Head thickness, can into pint | ≈ 14 mm at 5 s, 22 at 60 s, 21 at 115 s | pixel read-out of Watamura 2019 Fig. 3 (mm axes) | web-watamura2019-scirep-fig3-supplement.txt |
| Rudin head retention, stouts | 102–120 s (lagers 85–100.5 s) | Mohan et al. 1993, J. Inst. Brew. (abstract) | web-mohan1993-jib-hrv-stouts.txt |
| Foam density of poured CO₂ beers | 0.14–0.24 g/mL at 1 min | Constant 1992 (abstract) | web-foam-density-constant1992-klopper1954.txt |
| Surface tension, lagers 25–27 °C | 33.8–43.9 mN/m | KINO company note 2020 | web-kino-surface-tension-table.txt |
| Head bubble size, Diageo design value | ≈ 55 µm, "may be closer to 100 µm", packing 0.64 assumed | patent US9604775B2 | web-diageo-patent-US9604775.txt |
| Slosh decay with dish-soap foam (not beer) | 1.81 s no foam, 0.63 s with 6 mm, 0.37 s with 20 mm | Cappello, Sauret et al. 2015 | web-cappello2015-jvis-sloshing-and-press.txt |

Not found anywhere: a surface-tension measurement on stout itself, a weighing of a Guinness head, a measurement of a tilted or
sloshed pint.

### 2.7 Uncertain, and how to measure it

- **φ_l of a real head** (computed 0.24–0.36): weigh a known volume of the head, scooped with a syringe barrel (ρ_f = φ_l ρ_l).
- **R of the head** (computed 34 µm): a macro photograph of the head against the glass wall with a scale.
- **τ_y.** Tilt a glass slowly and read the tilt at which the head starts to flow over itself: τ_y ≈ ρ_f g h_f sin θ.
- **Lacing thickness:** not measured anywhere I found. Weigh the glass before and after a known area of cling.
- **The prefactor of G₀ and τ_y** for stiff-surface beer foam: no source found. Ronteltap's rheometer chapter may have it, not
  checked.

---

## Part 3. The boundary layers

### 3.1 Facts

- **Viscous wall damping**, Fact, as printed in bongarzone-gallaire2022-arxiv2207.06907.txt, eq. 17, p.4. Lengths are in units of R
  and times in units of √(R/g), with Re = √(gR³)/ν:

  σ = 2k²/Re + √(ω/2Re)·k/sinh 2kH + √(ω/2Re)·[½(1 + (m/k)²)/(1 − (m/k)²) − kH/sinh 2kH].

  The terms are the bulk, the bottom and the side wall. ζ = σ/ω.
- **The handbook's empirical damping.** Fact, from nasa-sp106-abramson1966-ch4.txt pp.109–111, read from the page images: log
  decrement δ = 4.98 ν^½ R^(−3/4) g^(−1/4) (eq. 4.8b) or 5.23 ν^½ R^(−3/4) g^(−1/4) (eq. 4.10b). Divided by 2π, these are the 0.79
  and 0.83 coefficients.
- **The contact line.** Fact: water in a cylinder with R = 37.05 mm at 3.50 Hz had measured ζ = 0.0098, about twice the
  Case–Parkinson value; the author puts the difference down to the moving contact line (viola2016-thesis-epfl7276.txt, p.174). Fact:
  hysteresis acts as Coulomb friction (same thesis, eqs. 8.10, 8.43–8.51):
  - θ − θ_s = αCa ∂_tη + (Δ/2) sgn(∂_tη);
  - the amplitude obeys dA/dT + ζA + χ sgn A = 0;
  - motion stops at t* = ζ⁻¹ ln(1 + A₀ζ/χ);
  - measured slip coefficients for water: α ≈ 58 advancing, 108 receding.
- **Wetting.** Fact: beer-like solutions (3 % ethanol) on acid-cleaned glass have a static angle of 29–46°, and 47–72° on silanised
  glass (wang2017-lund-beer-lacing.txt p.10). Fact: water on clean glass, advancing 51.3° and receding 46.6°, so Δcos θ = 0.06; on
  protein-coated glass Δcos θ = 0.27–0.68 (acuna-nelson2020-jnanomater-8640818-bsa-glass.txt). No measurement for stout.
- **Surfactant skin.** Fact: for an inextensible (contaminated) surface, the extra term is √(ω/2Re)·k cosh²kH/sinh 2kH (Henderson &
  Miles 1990, via bongarzone2023-thesis-epfl10334.txt p.136, eq. 6.13). In deep water it equals the side-wall term. Henderson &
  Miles 1994 found that real contaminated surfaces depart from this theory "significantly" more than clean ones
  (jfm-abstracts-sloshing-damping.txt, abstract only). Fact: beer surfaces are stiff, with dilatational modulus 5–25 mN/m
  (wierenga2023) and Bq ≫ 1 (chatzigiannakis2025).

### 3.2 Derivation (wolfram/01, checked in sympy/01_02)

**The Stokes layer.** The bulk slides past the wall with tangential amplitude U at frequency ω. The wall drags a layer
u = U e^(−y/δ) cos(ωt − y/δ) with it, of thickness δ = √(2ν/ω). Picture a hand moving to and fro in honey: only a skin moves
with the hand. Averaged over a cycle, the dissipation per unit wall area is

D = μU²/(2δ) = (ρU²/2)√(νω/2).

**Mode (1,1) of an upright cylinder** (radius R = 39.1 mm at the fill, depth 125 mm):
- potential φ = A J₁(kr) cos θ cosh k(z + H)/cosh kH, with kR = j′₁₁ = 1.84118;
- ω² = gk tanh kH, so **f₁₁ = 3.42 Hz** and **δ = 0.436 mm**.

The amplitude decays at rate γ_d = (wall dissipation)/(2E). For deep water, with the θ and z integrals in closed form,

**γ_d,side = (1/2)√(νω/2) (1/R)(1 + 1/j²)/(1 − 1/j²) = 0.110 s⁻¹**,

which is **ζ = 0.0051**, or ζ = 0.5575 √(ν/(R^(3/2) g^(1/2))). The 3D quadrature in Wolfram and the closed form in SymPy agree:
0.110121 s⁻¹ at finite depth, 0.110132 s⁻¹ deep. This is Bongarzone & Gallaire's side-wall term in physical units.
- Adding their bulk term 2νk² = 0.009 s⁻¹ gives 0.119 s⁻¹.
- The bottom is 120 mm below the surface wave's e-folding depth: 3 × 10⁻⁶ s⁻¹.
- Inference: the handbook's empirical 0.79–0.83 run 1.4–1.5 times this theory. The excess is the contact line and the surface skin,
  which the clean theory leaves out.

**An inextensible surface (protein skin, or the head as a lid).** The same integral over the top surface gives
**γ_d,top = 0.110 s⁻¹, ζ_top = 0.0051**, the same as the wall, as Henderson & Miles's term says.

**The foam lid's wall friction.** Integrating Viola's oscillator directly (wolfram/03b, their own fitted ω₀, σ and R), starting
at 5 mm:
- no foam: amplitude 2.1 mm at 4 s, below 0.05 mm only after 21.5 s;
- α = 0.010: below 0.05 mm after 7 s;
- α = 0.030: below 0.05 mm after 3 s.

This reproduces their 5–12 s stopping times in order of magnitude.

### 3.3 Boundary conditions for the solver, with numbers

| Interface | Condition | Numbers | Status |
|---|---|---|---|
| Stout on glass | no slip. The 1.5 mm grid cannot resolve δ = 0.44 mm, so either refine near the wall or impose the Stokes-layer wall stress τ_w = μ ∂u/∂n ≈ μ(1 + i)u_slip/δ in the slip form. Target ζ_wall = 0.0051 (γ_d = 0.110–0.119 s⁻¹) for mode (1,1) | δ = 0.436 mm | Fact (formula) and Inference |
| Contact line, stout on glass | Coulomb friction: the line does not move until the contact-angle force per length γ(cos θ − cos θ_s) exceeds γΔcos θ/2, then slides | Δcos θ = 0.27 (0.06–0.68), θ ≈ 30–45°. Extra damping ×1.5–2.4 on the wall value (viola2016 thesis p.174; handbook ×1.4–1.5) | Fact for water and model liquids; Inference for stout |
| Free surface without a head (after a spill) | zero normal stress − γκ; tangential: inextensible protein skin, so no slip relative to a surface that cannot stretch | adds ζ ≈ 0.0051 (γ_d ≈ 0.11 s⁻¹) | Fact (formula), Inference that beer is in this limit |
| Stout under the head | the head is a lid: p = ρ_f h_f (g_eff·n); no slip u_t = u_f | ρ_f h_f ≈ 3.8 kg/m² (1–7.6); adds ζ ≈ 0.0051 like the skin | Inference |
| Head on glass | slides with Plateau-border friction τ_w ≈ (ξγ/R)Ca^(2/3); sub-linear, so small motions stop in finite time | 18–36 Pa at 0.01 m/s, 85–170 Pa at 0.1 m/s; Viola α = 0.010–0.030 for thin layers | Fact (law), Inference (numbers) |
| Lacing (cling) | a film left behind as the head's edge recedes | thickness not measured | unknown |

Total for mode (1,1), Inference: ζ ≈ 0.0051 (wall) + 0.0051 (skin or lid) = 0.010. The contact line adds up to ×1.5–2.4 on top.
That is e-folding in 4–5 s clean-surface with head, against 8.3 s for the side wall alone. The foam's sub-linear friction ends the
last millimetres in finite time.

### 3.4 Uncertain, and how to measure it

- The contact angle and hysteresis of stout on a real pint glass: a sessile drop of stout on a piece of the glass, photographed
  from the side while it is tilted.
- Whether the head pins at the glass or slides: film the head's edge against a mark on the glass during a single slosh.
- The ringdown of a real pint: tap the glass sideways and film the surface for 20 s, then fit ζ. With and without a head, this
  measures the head's contribution directly. Opinion: this is the single most useful experiment for the whole model.

---

## Video catalogue

### Clips held (private Google Drive, folder "Guinness research videos")

Drive folder: <https://drive.google.com/drive/folders/14BjGMr_hyN7_nZa3Q4tiMx-QpLOfivQN> (private, owner only).

| File | Source | Author | Licence | Used | What it shows | Measured |
|---|---|---|---|---|---|---|
| watamura2019_S2_pint_pour_settle_CC-BY.mp4 (Drive id 1zilkZf3bBr4_ofmW8j5iX5-MjUFtjfTg) | Sci. Rep. 9, 5718 (2019), Supplementary Movie S1 (Springer file MOESM2), static-content.springer.com/esm/art%3A10.1038%2Fs41598-019-42094-0/MediaObjects/41598_2019_42094_MOESM2_ESM.mp4 | Watamura, Iwatsubo, Sugiyama, Yamamoto, Kaneda, Ogasawara, Takahira | CC BY 4.0 | whole, 0–80 s (196 × 384 px, 25 fps) | A pint glass filled from a tap. The head forms, the stout darkens from the bottom up as the bubbles clear, and the head grows to its final height. The head stays a flat white band with a sharp lower edge | In the centre column, at 79 s the head spans rows 86–137, i.e. 51 px. The glass's inner height is about 310 px; for 150 mm that is ≈ 0.48 mm/px, so the head is ≈ 24 ± 4 mm. The clearing front (pixels darker than 30) rose from row ≈ 264 at 40 s to ≈ 192 at 60 s to ≈ 150 at 79 s: ≈ 1.7 then 1.1 mm/s. Whether the clip runs in real time is not stated (Inference) |
| watamura2019_S4_tilted_tank_pour_CC-BY.mp4 (Drive id 1tlsEnqUJZ2zBJqCGiJTscvouY-joYE3L) | same paper, Movie S3 (file MOESM4; the paper's tilted-container/Boycott movie) | same | CC BY 4.0 | whole, 0–60 s | A tilted thin tank filled with stout. Large bubbles in the head burst, and the head thins from a coarse foam to a thin white skin. The bulk clears from the bottom, more slowly along the overhanging wall | qualitative: the head on a wide surface coarsens and thins within about 30 s in this tank, where bubbles are large. No scale bar read |
| not uploaded: file MOESM3 (4.1 MB) | same paper, Movie S2 (file MOESM3) | same | CC BY 4.0 | 0–5.1 s, 20 fps, 1188 × 586 | microscope view of bubbles near the wall, with tracked velocity arrows pointing downward | the file is over the connector's 3.1 MB upload limit. It is publicly available at the link |

Springer files MOESM1 and MOESM5 returned HTTP 403. Numbering: the paper's Movie S1 = file MOESM2, S2 = MOESM3, S3 = MOESM4 (the file names on Drive carry the file numbers S2 and S4, not the paper's movie numbers).

### Candidates found but not downloaded

YouTube refused every video page from this container ("Sign in to confirm you're not a bot") on eight player clients. Mirror sites
were refused by the session's permission check, which I did not work around. These were found by title in 44 searches and are not
watched. The full list of about 30 is in the video agent's notes; the best are:

| URL | Title, uploader | Why it matters |
|---|---|---|
| youtube.com/watch?v=yPJKfAGzTbk | "Beer physics: How foam affects sloshing", New Scientist | Sauret et al. 2015 foam damping |
| youtube.com/watch?v=8FwM40HgagM | "Beer inspires anti-sloshing science", 2014 Gallery of Fluid Motion | Stone lab sloshing with and without foam |
| youtube.com/watch?v=tpA5jH04ayU | "Under the Influence of Beer Foam", SciFri | same experiments |
| youtube.com/watch?v=2_V2MRNlZOs | "Experiment: Tilted cylinder/stout flow" | probably Benilov's Limerick experiment |
| youtube.com/watch?v=EEtKZ2wJhNk | Cathal Cummins (MACSI), "Why do bubbles in Guinness sink?" | the cascade |
| youtube.com/watch?v=xH--Ig5TMfg | "High speed camera shooting of Beer Foam Cascades" | the cascade in slow motion |
| youtube.com/watch?v=-vYONSL0sk4, td8KBEFTi_E | Guinness pour in slow motion (400 fps) | surge and settle |
| youtube.com/watch?v=kfDVFx1CJL8, CvuibQ2zM7Q, tkf6h7sIltQ | upside-down pint tricks | the head as a plug: does it hold under −g? |
| youtube.com/watch?v=M3sI9c5EQvg, G1AF294XJ3M | a pint carried up Croagh Patrick, up Mount Fuji | a pint carried while walking |
| youtube.com/watch?v=I--Cg11aruw | "Irish Pint Drop" | a dropped pint |
| youtube.com/watch?v=AqlHvB3TYqE | "Glass of Beer Spilling in slow motion", Science Source | an ordinary beer spill, for contrast |

To get them: a browser-saved copy, or yt-dlp run with the owner's cookies, from a machine the owner controls.

---

## Sources and search roads

**Extracts in `sources/`** (one file per source; verbatim passages with pages). Some papers were read by two agents and appear
twice: lee2011-stoutfoaming / lee-devereux2011, power2009-esgi70-guinness / -initiation-of-guinness, watamura2019-scirep9 /
-5718, lee2018-ajp86 / lee-kaar-obrien2018. Both copies are kept because they quote different passages.

- **Body:** benilov2012, benilov2013, lee-devereux2011, power2009-esgi70 (×2), watamura2019 (×2), robinson2008, lee-kaar-obrien2018,
  zhang-xu2008, rodriguez2014, three patents (US4832968/GB2183592, GB1588624, US7520212), sander2015, ba-draught-beer-quality-manual-2011,
  severa-los2008, jin2004, gerard-varet-hillairet2020, haines-mazzucato2012, hofer-schubert2021, brzinski-durian2018.
- **Head:** ronteltap1989-thesis, costa2012-thesis, besson2008-hal, tcholakova2008-pre78, cantat2013-pof25, sauret2015-pof27,
  viola2016-pof28, chatzigiannakis2025-pof37, lee2011-stoutfoaming, lee2018-ajp86.
- **Boundary layers:** bongarzone-gallaire2022, bongarzone2023-thesis, viola2016-thesis, nasa-sp106-abramson1966-ch4,
  wierenga2023, wang2017-lund-beer-lacing, acuna-nelson2020, jfm-abstracts-sloshing-damping (abstracts only).

**Not read, so not cited for content:**
- Nature Reviews Physics 5, 197 (2023): no match found. The 18–20 mm head is taken from the brief.
- Bamforth 2023 (closed), and Bamforth 1985, Bishop 1975 (bot-blocked).
- Mason–Bibette–Weitz 1995/1996 and Höhler & Cohen-Addad 2005 (closed). Their formulas are used as quoted in costa2012.
- Case & Parkinson 1957, Miles 1967, Keulegan 1959, Hocking 1987, Cocciaro 1993, Henderson & Miles 1994, Henderson 1998 (paywalled).
  The formulas are used as printed in Bongarzone & Gallaire and the Viola thesis.
- Einstein 1906/1911 and Richardson–Zaki 1954 (originals not reached).
- Cantat et al., "Foams" (Oxford 2013): no open copy.

**Roads that answered:** curl to arXiv and its API, NASA NTRS, EPFL Infoscience REST API, HAL API, OpenAlex, Unpaywall, Crossref,
Semantic Scholar (metadata), Google Patents, WebSearch, Exa search and fetch, Consensus, Wageningen (edepot.wur.nl) and Lund
repositories, the Nature/Springer supplementary server (videos), Google Drive (storage).

**Roads that failed:**
- Bot checks: core.ac.uk, Wiley, Royal Society, IOP and ScienceDirect.
- Firecrawl: reached paywall pages, timed out once, and was once refused by the permission check.
- YouTube video pages: bot check.
- Invidious, Piped, Vimeo and Dailymotion through yt-dlp: refused by the permission check.
- Wikimedia Commons API: rate-limited after the first search.
- Springer: Movies 1 and 5 returned 403.
- The Drive connector: 3.1 MB per-file limit, so Movie S3 was not uploaded.

**Not tried:** TinyFish, Nimble and Espacenet on the body questions, and Tavily and Bright Data, because other roads answered.
