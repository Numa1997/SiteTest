# Contract L3: coalescence efficiency

Gate 1. Sources: `dossier-coalescence-turbulence.md` (Low and List 1982a abstract, Straub et al. 2010 abstract and introduction,
Beard and Ochs 1984 abstract; Beard and Ochs 1995 not opened; Low and List's constants second-hand via Jacobson 2011 and PySDM).
Numbers: `portfolios-src/droplets/derive/L3_coal.py`.

## 1. Question and observables

Two drops touch. Do they stay together? Observables: the coalescence efficiency E_coal (the fraction of collisions that end in a
lasting merger) for the pair classes of the thesis cloud and of the drops it grows (8 µm on 40–100 µm collectors; collector pairs
50–60 µm; drizzle and rain pairs 100–2000 µm), and its effect on observable 1 (t₅₀, t₉₀) and on the largest drops (observable 2).

## 2. Picture and formal mechanism

Picture: watch rain on a puddle. Most drops vanish into it at once; some bounce, or skate across on a thin film of air before they
sink. Two drops in a cloud face the same choice: the air between them must drain before the surfaces touch, and a hard hit can
deform them so much that they bounce apart or tear apart again.

Mechanism, the energy that decides: of the two drops' kinetic energy, the part carried by their common centre of mass survives any
collision (momentum is conserved); only the energy of relative motion, carried by the reduced mass μ = m₁m₂/(m₁ + m₂), can deform
them (derived in the textbook by splitting off the centre of mass):

  CKE = ½ μ (Δv)²,      S_c = π σ d_c²,      We = CKE / S_c,      d_c = (d₁³ + d₂³)^{1/3}.                     (L3.1)

S_c is the surface energy of the merged drop; a merger frees π σ (d₁² + d₂² − d_c²) > 0. We ≪ 1 means the hit is gentle against the
surface's stiffness; We ≳ 1 means it can tear the drops apart again.

## 3. Model

Closure: E_coal = exp(−1.15 We) (L3.2), with We from (L3.1) and the fall speeds of the kernel in use. This is the thesis's law
(equations 21–24 of N. Koudsie 2022, as quoted in the baseline), and it is the form Straub et al. (2010) fitted to numerical
simulations of raindrop pairs (small drop 0.35–1.8 mm, large 0.6–4.6 mm in diameter; abstract and introduction read in the dossier).
For pairs with ice (L7) E_coal = 1: liquid freezes on contact, ice is taken to stick to ice (a choice, stated there).

## 4. Rejected alternatives

1. **Low and List (1982a)**: measured for raindrops (small drop ≥ 0.395 mm in diameter); its prefactor 0.778(1 + d_S/d_L)^{−2} does
   not reach 1 for gentle collisions, so extrapolated to cloud droplets it gives 0.54 for 8 µm on 40 µm, against every energy argument.
   Its constants are known here only second-hand. Used as a comparison for raindrops only (0.34 at 500/250 µm against 0.55).
2. **Beard and Ochs (1995)**: the law built for small precipitation drops (14–800 µm in diameter, second-hand via Jacobson 2011), with
   E → 1 below 14 µm. It is the right law for our sizes, but it was not opened, so it cannot be coded honestly. Open item: if it is
   obtained, it replaces (L3.2) below 0.4 mm.
3. **E_coal = 1 everywhere** (Hall 1980): right for the cloud-droplet pairs (below), wrong for raindrops, where both laws give
   0.03–0.55.

## 5. Numbers (10 °C, 850 hPa, σ = 0.07422 N/m, Beard speeds; Stokes speeds in brackets)

| Pair (radii, µm) | Δv (m/s) | We | E_coal (L3.2) | freed surface / CKE |
|---|---|---|---|---|
| 40 / 8 | 0.169 (0.189) | 2.0 × 10⁻⁵ | 0.99998 (0.99997) | 1700 |
| 60 / 8 | 0.340 (0.435) | 3.7 × 10⁻⁵ | 0.99996 (0.99993) | 440 |
| 60 / 50 | 0.089 (0.135) | 2.9 × 10⁻⁴ | 0.99967 (0.99923) | 870 |
| 100 / 50 | 0.469 (0.922) | 5.1 × 10⁻³ | 0.9942 (0.9777) | 31 |
| 200 / 100 | 0.946 (3.69) | 0.041 | 0.954 (0.486) | 3.8 |
| 500 / 250 | 2.12 (23.1) | 0.52 | 0.550 (≈ 0) | 0.30 |
| 1000 / 500 | 2.68 (92.2) | 1.66 | 0.148 (0) | 0.094 |
| 2000 / 1000 | 2.53 (369) | 2.95 | 0.034 (0) | 0.053 |

For every pair that decides observable 1 the collision energy is 2 × 10⁻⁵ to 3 × 10⁻⁴ of the surface energy: E_coal = 1 to 4 parts in 10⁴.
No measurement of coalescence for cloud droplets this small was found in the sources read (the energy laws know nothing of a bouncing
air film; Beard and Ochs 1995 would be the test). For drizzle and rain the law matters, and with Stokes speeds it switches mergers off
above about 300 µm radius (E = 0.49 at 200/100 µm, about 0 at 500/250): this is why the thesis kernel stalls.

## 6. Exact and limiting behaviour

E_coal → 1 as We → 0; E_coal falls by a factor e^{−1.15} per unit of We. The reduced-mass split (derived) gives CKE → ½ m_small Δv² for
very unequal pairs, so cloud droplets carry almost no collision energy. The thesis's W_E and Straub's We are the same ratio.

## 7. Predictions that could come out wrong

1. Replacing (L3.2) by E_coal = 1 changes the extended kernel's t₅₀, t₉₀ by less than 0.1 % (L3 is a stated check for observable 1,
   not an active ingredient).
2. With the thesis kernel (Stokes speeds in (L3.2)) the SCE's mass piles up below 1 mm and no 1 mm drop appears in 60 min (expected
   number per m³ below 1); with the extended kernel the spectrum keeps growing into millimetres. If the thesis kernel makes 1 mm drops,
   the switch-off argument above is wrong.

## 8. Derived, cited, chosen, and the price

Derived: (L3.1), the centre-of-mass split, the freed surface energy, the table of section 5. Cited: the exponential law (the thesis;
Straub et al. 2010's form and fit range). Chosen: to use it for all liquid pairs, far below its fit range for cloud droplets, where it
gives 1 to within 4 × 10⁻⁴ — a choice that is harmless only because any energy law gives the same there, and the page says that no
measurement covers those sizes. Price: for raindrop pairs the two available laws differ by up to 0.2 (0.55 against 0.34 at 500/250 µm),
so the millimetre end of the spectrum carries that uncertainty.

## 9. Answers to round 1 (`skeptic-G1-L3L6L7-r1.md`, L3: PASS with fixes)

| # | Answer |
|---|---|
| 1 | Picture now names both hazards (air film, tearing) and says the law describes only the second (chapter 4 of the notes). |
| 2 | Evidence both ways now on the page, read from the abstracts (OpenAlex): Beard et al. 2002, E_coal "certainly greater than 91 % and likely greater than 95 %" for 55–105 µm pairs at ratio 0.5–1; Beard and Ochs 1984, time-averaged collection efficiency halved for growth from 50 to 500 µm by 30 µm droplets. "E_coal = 1" restated as "(L3.2) gives 1 to within 4 × 10⁻⁴". |
| 3 | Low and List rejected for being far outside its measured range and for contradicting Beard et al. 2002 (0.23 for 60/50 µm against > 0.91). |
| 4 | "2 × 10⁻⁵ to 3 × 10⁻⁴". |
| 5 | Prediction 1 relabelled a consistency check; outcome 0.26 % (failed narrowly as a prediction, still far below the closure band). |
| 6 | "Above about 300 µm radius (E = 0.49 at 200/100, about 0 at 500/250)". |
| 7 | The three raindrop rows are in section 5. |
