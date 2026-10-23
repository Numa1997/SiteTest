# Contract L7: ice, and what collisions can add

Gate 1. Source: `dossier-ice.md` (Korolev and Leisner 2020 read whole; Phillips, Yano and Khain 2017 prose read, coefficients second-hand
through Sotiropoulou et al. 2021 and Grzegorczyk et al. 2023; Hallett and Mossop 1974, Takahashi et al. 1995, Vardiman 1978 only second-hand).
Code: `tools/run_cold.cjs` → `data/cold.json`.

## 1. Question and observable

The thesis asks whether collisions involving ice multiply the number of ice particles. Observable 3: new ice particles per cm³ per
minute from each mechanism, at the start of the thesis's cold case (−10 °C, 600 hPa; the warm cloud's two modes split bin by bin with
the thesis's supercooled liquid fraction, 44.55 % at −10 °C: 134.1 cm⁻³ liquid droplets and 166.9 cm⁻³ ice spheres of density 900 kg/m³).

## 2. Picture and mechanism

Picture: shake ice cubes in a glass and small chips break off; drip water onto a cold window and some drops freeze with a crack and
spit splinters. Each chip is new ice made from old ice: the number of pieces rises, the mass of ice does not. Mechanism: new particles
per volume and time = (fragments per event) × (events per volume and time). The event rates come from the kernel (L1–L3, each phase with
its density; liquid freezes on contact with ice; E_coal = 1 for pairs with ice); the fragments per event come only from measurements.

## 3. Model

Rates at t = 0 (production rates need no time evolution). Three measured channels, each with its source and range:
1. **Rime splintering (Hallett–Mossop)**: measured only between −8 and −3 °C (Korolev and Leisner, Table 2): zero at −10 °C.
2. **Shattering of freezing drops**: measured at −10 °C for drops of 50 µm diameter and more; 1–37 % of drops shatter, with at most
   3–12 fragments (Korolev and Leisner, Table 1): 0.03–1.7 fragments per freezing drop (dossier's bracket). Applied to liquid drops of
   radius ≥ 25 µm captured by ice, an assumption: the data are for drops that freeze alone, not on contact with ice.
3. **Ice–ice breakup**: Phillips et al.'s law N = αA[1 − exp(−(C K₀/(αA))^γ)] with type-I coefficients at −10 °C (A = 1.44 × 10⁶ m⁻²,
   γ = 0.3, C between 2.2 × 10⁴ and 6.3 × 10⁶ J⁻¹), K₀ = ½ μ_red Δv², α = π D² of the smaller sphere: fitted to collisions of 0.5 mm–2 cm
   particles at 10⁻⁴–10⁻² J, applied here to collisions of 10⁻¹² to 10⁻⁹ J, an extrapolation over 4 to 9 orders of magnitude, so an upper
   bound at best.
For comparison, the old study's rule: a fraction λ = 0.001 of the larger particle's mass per ice–ice collision, as 5 µm fragments, with
no measurement behind it.

## 4. Rejected alternatives

A time-dependent two-phase SCE (the old study): the production rates at t = 0 answer observable 3 directly, and a long run would only
propagate rates that are uncertain by orders of magnitude; it is left out at lecture-note scale. Vardiman's (1978) crystal law: for
dendrites and plates against a plate, not spheres.

## 5. Results (computed after this contract was drafted; `data/cold.json`)

| Mechanism | New ice, cm⁻³ min⁻¹ |
|---|---|
| Rime splintering | 0 (outside its temperature window) |
| Shattering of captured drops ≥ 25 µm (2.80 such events cm⁻³ min⁻¹) | 0.084 to 4.8 (if captured drops shatter like free ones) |
| Ice–ice breakup (5.27 riming and 2.88 ice–ice events cm⁻³ min⁻¹ in all) | 7.0 × 10⁻⁵ to 3.7 × 10⁻⁴ |
| The old rule, λ = 0.001 | 2.6 |

## 6. Prediction that could come out wrong

Ice–ice breakup of the thesis's small ice spheres produces at least a thousand times less new ice than the old rule assumed.
(Outcome: 7 × 10³ to 4 × 10⁴ times less.)

## 7. Derived, cited, chosen, price

Derived: the rate formula, the collision energies. Cited: every yield. Chosen: ice spheres of 900 kg/m³, the thesis's liquid fraction,
E_coal = 1 with ice, the application of free-drop shattering data to captured drops. Price: the only channel that could matter at
−10 °C rests on an unmeasured geometry, so the study can bound observable 3 but not pin it down; the page says so.
