# Guinness on a jolted cart: every number for the solver, in one place (13 November 2026)

For the parent session "Guinness cart page rebuild". The derivations are in `guinness-materials.md`, `wolfram/` and `sympy/`; the
sources are in `sources/`. Each number carries one status:

- **M**: measured by someone; we read the source (file named).
- **M-G**: measured by someone; the owner's Gemini search quoted it with a link, but we have not opened that page.
- **D**: derived by us in Wolfram and checked in SymPy (file named).
- **X**: checked and rejected.

## 1. The stout (a bubbly liquid)

| Quantity | Value | Status, source |
|---|---|---|
| Density, degassed, 5–6 °C | 1007 kg/m³ (1006–1007) | M: benilov2012 p.1; watamura2019 SI (U-tube meter) |
| Dynamic viscosity, 6 °C | 2.06 mPa s (2.03–2.23); ν = 2.05 × 10⁻⁶ m²/s, not water's 10⁻⁶ | M: benilov2012; watamura2019 (rolling-ball viscometer) |
| Newtonian? | yes for beer, linear 92–921 s⁻¹, r² ≥ 0.99; no sweep of Guinness itself exists | M: jin2004 |
| Surface tension, degassed Guinness, 20 °C | 44.2 mN/m (pendant drop) | M-G: Völp & Willenbacher 2021 Soft Matter 17, 3937, Table 2 (we read the paper and its Table 1 entry "Guinness stout beer, degassed, 20 °C"; the 44.2 is Gemini's quote of Table 2) |
| Surface dilatational elasticity, Guinness | 18.7 mN/m (high-frequency, pendant drop) | M-G: same Table 2 |
| Surface tension, beers generally | 38–47 mN/m; lager 41.55 ± 1.39 mN/m at 25 °C | M: ronteltap1989 Table 4.5; M-G: "dancing peanuts" R. Soc. Open Sci. 10, 230376 (2023) |
| Gas in the sealed can | 3.8 bar at 8 °C, 79 % N₂ / 21 % CO₂; CO₂ ≈ 2 g/L, N₂ ≈ 0.072 g/L; supersaturation ≈ 2.8 | M: power2009-esgi70 pp.143–147 |
| Dispense gas | 25/75 to 30/70 CO₂/N₂ | M: Brewers Association manual 2011 p.30 |
| Bubble diameter | mean 61 µm (log-normal, σ ≈ 0.24, at least 3000 bubbles); 59 ± 15 µm (N = 301) | M: watamura2019 SI Fig. S2; watamura2024 Oleoscience Table 1; M-G: Watamura PRE 103, 063103 (2021) |
| Robinson's 94–122 µm | rejected: those bubbles would clear the glass in 32 s against a measured 120 s | X, D: wolfram/04 |
| Gas fraction | 8 % canned bulk (weighed); 9.7 %; ≈ 10 % pub draught; ≈ 2 % served | M: watamura2019 SI; watamura2024; benilov2012 |
| Settling time | ≈ 120 s; 61 µm bubbles by Stokes' law: 126 s | M: benilov2012; D: wolfram/04 |
| Settled pint (> 2 min) | gas fraction < 10⁻³: treat as single-phase | D |
| Bubble slip, if the ride starts during the surge | v − u = (2a²ρ/9μ)(Du/Dt − g_eff): 1.0 mm/s at 1 g; relaxes in 0.1–0.2 ms | D: wolfram/02 |
| Mixture density and viscosity | ρ_m = (1 − α)ρ; μ_m = μ(1 + 2.5α) | M (Einstein, rigid spheres): gerard-varet-hillairet2020 |
| New bubbles from jolts? | no: ρaH = 1.26 kPa at 10 m/s², against a 100 kPa / 0.24 ms tap needed | D: wolfram/02; M: rodriguez2014 |
| Cascade | forms only where the wall leans 5–20°; moves down at ≈ 35 mm/s | M: watamura2019 |

## 2. The head (a foam)

| Quantity | Value | Status, source |
|---|---|---|
| Thickness 2 min after pouring | 17.5 mm (two-part), 20.6 mm (Irish), 22.2 mm (one-shot); specification 18–20 mm | M: kegworks2019 (hobbyist, one pour each) |
| Thickness against time, can into pint | 14 mm at 5 s, 22 mm at 60 s, 21 mm at 115 s | D: pixel read-out of watamura2019 Fig. 3 (mm axes) |
| Bubble Sauter radius R₃₂ | 34 µm (33–36): the stout's own bubbles, which nitrogen does not let grow | D: wolfram/04 from watamura2019 SI |
| Liquid fraction ε | 0.24–0.36, about 0.27 mean | D: wolfram/05. At equilibrium a 19 mm column of 34 µm bubbles holds ε = 0.36 at its base and 0.235 at its top; reaching that takes 25–110 min, so a 2–5 min old head is at least this wet |
| Density | 240–360 kg/m³ (272 at ε = 0.27) | D |
| Shear modulus G₀, from Guinness's own surface (γ + 2E∞)/R₃₂ = 2400 Pa | 228 / 166 / 109 / 40 Pa at ε = 0.24 / 0.27 / 0.30 / 0.34 | D: wolfram/06, law of Völp & Willenbacher 2021 (G₀ = 1·(γ+2E∞)/R₃₂·Φ(Φ − 0.635)) |
| Same from Mason-type laws (cross-check) | 122–143 Pa at ε = 0.27 | D: wolfram/05 |
| Yield stress τ_y, Guinness surface law | 9.4 / 5.4 / 2.5 / 0.4 Pa at ε = 0.24 / 0.27 / 0.30 / 0.34 | D: wolfram/06 (τ_y = 0.25·(γ+2E∞)/R₃₂·(Φ − 0.635)²) |
| Same from Mason 1996 (cross-check) | 17 / 8.2 / 4.3 / 1.1 Pa at ε = 0.22 / 0.27 / 0.30 / 0.34 | D: wolfram/05; M: mason1996 p.443 (C = 0.51, Φ_c = 0.62) |
| Bingham number τ_y/(ρ_f a h_f) | 1 m/s²: 2.0 / 1.0 / 0.44 / 0.06; 10 m/s²: 0.20 / 0.10 / 0.04 / 0.006 | D: wolfram/06. The head holds its shape when moved gently and yields under hard jolts |
| Effective viscosity | 0.65–21 Pa s at 1–30 s⁻¹ (300–10 000 × stout) | D: wolfram/05 (Tcholakova 2008 flow law plus τ_y) |
| Its own waves | damped in 2–120 ms against the 292 ms slosh period, so it makes none | D: wolfram/05 |
| A thrown lump | a 10 mm lump takes 0.16–0.58 s to pull apart, so it stays a lump; stout breaks into 2 mm drops | D: wolfram/03, 05 |
| Drainage, coarsening | 25–110 min; no coarsening in 3 min; negligible over a 20 s ride | D: wolfram/05; M: ronteltap1989 |
| Rudin head retention | stouts 102–120 s (lagers 85–100.5 s) | M: mohan1993 (abstract) |
| NIBEM | Guinness Foreign Extra Stout 260 s at 20 °C; commercial range 211–359 s including stouts | M-G: Beninese brewery study (ResearchGate 349055897); Australian Rudin–NIBEM comparison (ResearchGate 259159112) |
| Foam on sloshing liquid | 5 bubble layers cut the slosh tenfold; frequency 3.1 against 3.3 Hz; 1/τ_f∞ = 9 ± 3 s⁻¹ | M: sauret2015 |
| Same in a 37 mm cylinder at 3.5 Hz | friction coefficient α = 0.010–0.030; motion stops in 5–12 s; frequency unchanged | M: viola2016 |
| Dish-soap foam (not beer) | decay time 1.81 s without foam, 0.63 s with 6 mm of foam, 0.37 s with 20 mm | M: cappello2015 |
| "Drained" liquid fraction 0.05–0.15 | rejected by the column equilibrium above | X (Gemini, no source) |
| Head bubble radius 50–60 µm | rejected: conflicts with the measured distributions | X (Gemini) |

## 3. Every boundary layer, as a boundary condition

| Interface | Condition | Numbers | Status |
|---|---|---|---|
| Stout on glass | no slip; Stokes layer δ = √(2ν/ω) | δ = 0.436 mm; side-wall decay 0.110 s⁻¹, ζ = 0.0051; with the bulk term 0.119 s⁻¹ | D: wolfram/01, sympy/01_02; agrees with bongarzone-gallaire2022 eq. 17 |
| Handbook check | log decrement 4.98–5.23 ν^½ R^(−¾) g^(−¼) | 1.4–1.5 × the theory above | M: nasa-sp106 pp.109–111 |
| Stout contact line on glass | static 28.5 ± 2.0°, receding 4.2 ± 2.4°; Δcos θ = 0.12; Coulomb friction until the hysteresis is overcome | adds ×1.5–2.4 to the wall damping | M: hamlett2015 Table 2 (Guinness Original, degassed; the table's row order still to be confirmed); M: viola2016 thesis p.174; M-G: lager on glass 23.2 ± 2.8° (dancing-peanuts paper, 2023) |
| Film left on the glass (lacing) | h = 0.946 ℓ_c Ca^(2/3) × 2.5 for rigid surfaces, ℓ_c = 2.13 mm | 6.5 / 19 / 48 / 140 µm at 1 mm/s / 5 mm/s / 2 cm/s / 0.1 m/s | D: wolfram/04; M: snoeijer2008, rio-boulogne2017 |
| Head on glass | slides with Plateau-border friction f = ξγCa^(2/3) per unit border length, ξ = 6.82 | wall stress ≈ 18–36 Pa at 0.01 m/s, 85–170 Pa at 0.1 m/s | M: cantat2013; D: wolfram/03 |
| Head on stout | the head is a lid: no slip, u_t = u_foam; normal stress p = ρ_f h_f (g_eff·n) | ρ_f h_f ≈ 5.2 kg/m² (272 × 0.019); adds ζ ≈ 0.0051 | D: wolfram/01; M: sauret2015 (foam speed decays upward over 16.8 mm) |
| Bare stout surface (after a spill) | p = −γκ; the protein skin is close to inextensible, so tangential no slip on the surface | γ = 0.0442 N/m, E∞ = 18.7 mN/m; adds ζ ≈ 0.0051 | M-G: γ, E∞; D: wolfram/01 |

**Mode (1,1) totals**, D:
- f₁₁ = 3.42 Hz.
- ζ = 0.0051 for the wall alone, plus 0.0051 for the skin or the head, giving 0.010.
- The contact line adds up to ×1.5–2.4.
- The head's sub-linear wall friction stops small motions in finite time.

## 4. Still not measured by anyone found

- A weighing of a Guinness head, to confirm ε = 0.24–0.36.
- A slosh or ringdown of a real pint, with or without its head.
- The published row order of Hamlett's Table 2.
- The Table 2 values of Völp & Willenbacher, read by us directly (the 44.2 and 18.7 are Gemini's quote).
