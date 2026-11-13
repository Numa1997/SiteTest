# Verification of the research note (guinness-materials.md), and the model taken from it

Done by the session "Guinness cart page rebuild", 13 November 2026, before any computation with these numbers.

## What was read

All of it:
- the note (471 lines), and its last commit ab9e6b2, which adds the composites table and the boundary-condition table;
- the three Wolfram files and their outputs, and the two SymPy checks and their outputs;
- all 40 source extracts;
- the research session's own messages.

## Independent checks (Wolfram, this session)

1. **Wall damping of mode (1,1)** in the pint (R = 39.1 mm, H = 125 mm, ν = 2.06e-3/1007 m²/s), recomputed from Bongarzone &
   Gallaire 2022 eq. 17 (the formula is in sources/bongarzone-gallaire2022-arxiv2207.06907.txt, p.4):
   - side wall 0.110121 1/s, bulk 0.009072 1/s, bottom 3.4e-6 1/s, inextensible surface 0.110394 1/s;
   - ζ = 0.00555 for a clean surface (e-folding 8.4 s), and 0.0107 with a protein skin or a lid (4.4 s).

   Same as the note's wolfram/01 (0.110121 1/s). **Confirmed.**
2. **The wall-friction law of foam, falsification test.**
   - The test: Cantat 2013's law, σ = Z (γ/r_b) ξ Ca^(2/3) per unit wall area (mobile surfaces, ξ = 4.94), with Z = 0.18. Z is
     Cantat's own fit at liquid fraction 0.25 to Marze et al.'s data, not to Viola's. It was put into the modal equation of mode
     (1,1) to predict Viola et al. 2016's measured coefficient α, with nothing fitted to Viola's data.
   - Viola's setup: cylinder R = 37.05 mm, 0.25 mm bubbles, 25 % liquid, γ = 31.5 mN/m, water.
   - Predicted 0.0111, 0.0146, 0.0177, 0.0222, 0.0288 against measured 0.010, 0.013, 0.016, 0.023, 0.030 for foam 2.5, 3.3, 4,
     5 and 6.5 mm thick. **Within 4-11 %. The law passes.** (With Cantat's theoretical Z = 0.094 it gives half, so the fitted Z is the
     one to use.)
3. **The same law for the Guinness head** (stiff protein surfaces, ξ = 6.82, plus the 0.94 (l/r_m) Ca^(1/3) term with Cantat's
   l/r_m fits; the foam's sliding speed decays upward over ℓ = 1/k = 21.2 mm, as Sauret measured, 16.8 mm against L/π = 22 mm in
   their cell; head 19 mm):
   - Viola-form α = 0.13-1.7 for R = 25-100 µm and φ_l = 0.10-0.25, against 0.030 for Viola's thickest soap foam.
   - Inference: a sliding Guinness head would arrest a free slosh within about one period.
4. **Head thickness, 18-20 mm.** Read by this session in Nature Reviews Physics 5, 197 (2023), the editorial "The physics of fizz":
   "For a pint of Guinness, the head should be 18–20 mm". **Confirmed** (the research session could not reach it).
5. **Stout viscosity.**
   - Zhang & Xu 2008 measured Guinness at 1.40 times water (temperature not stated). Water at 6 °C is about 1.47 mPa s, so this
     gives about 2.06 mPa s, consistent with Benilov's measured value.
   - Inference: a consistency check, not a proof, because the temperature is unknown.

## Corrections and cautions found while reading

- The yield stress is smaller than the wall stress. At slosh speeds (0.01-0.1 m/s) the sliding stress is 18-170 Pa, while
  τ_y = 6-23 Pa at φ_l = 0.2 (note, sec. 2.3).
  - Inference: the foam cannot pass more than its own strength to the glass. So the wall stress is the smaller of two stresses:
    - the sliding law;
    - the foam's yield stress plus its Herschel–Bulkley flow stress (Tcholakova 2008) in a layer one bubble diameter thick.
  - This cap adds no parameter: it uses the same R, φ_l and γ.
- Costa's thesis assigns Ca^(1/2) to mobile and Ca^(2/3) to rigid surfaces, the reverse of Cantat and Denkov. The research session
  flagged this. Cantat's assignment is the one used, and it is the one validated in check 2.
- R and φ_l of a real head are **not measured anywhere found**. They are the two inputs without a measurement. Values used:
  - R = 50 µm (range 25-100). Stout bubbles are 27-61 µm in radius; nitrogen beer foam starts near 100 µm (Ronteltap).
  - φ_l = 0.20 (range 0.05-0.4). Ronteltap calls 0.4 realistic for fresh beer foam; Lee et al. use 0.2.
  - Both are inferences, stated on the page.
- The bubbly body: a settled pint (over 2 min) has α < 10⁻³, so the stout is single-phase Newtonian (note, sec. 1.3). Accepted.
- Cling (lacing) thickness is not measured, so cling is left out of the volume balance. Stated on the page.
- Drainage and collapse (about 650 s) are left out of a 20 s ride: about 0.6 mm of head. Stated.

## The model taken into the solver (tools/fig12/kaggle/stout_jax.py, model "full")

1. **The stout:** single-phase, incompressible Navier–Stokes; ρ = 1007 kg/m³, ν = 2.05e-6 m²/s.
2. **Stout on glass:** the Stokes-layer wall stress ρ√(νω/2) u_slip, ω = 2π × 3.42 Hz (target ζ_wall = 0.0051).
3. **Surface skin and lid:**
   - Under the head, and on bare stout where the head has gone, the surface does not stretch. It behaves as a no-slip lid.
   - The horizontal velocity of the surface cells is braked by the same Stokes-layer stress (target +0.0051).
   - The head itself is held still in the horizontal by its friction on the glass (check 3), so the lid's velocity is zero
     relative to the glass.
4. **The head's weight:** p = ρ_f h_f |g_eff| on the stout surface, ρ_f = φ_l ρ. Set in the pressure solve by the ghost-fluid rule.
5. **The head on the glass:**
   - As the stout's edge moves up and down the glass, the head's edge slides with it.
   - Wall stress: τ_w = min[Z (γ/R)(6.82 Ca^(2/3) + 0.94 (l/r_m) Ca^(1/3)), τ_y + τ_HB(v/2R)], with Ca = μv/γ.
   - It acts over the effective height h_eff = (3ℓ/5)(1 − e^(−5h_f/3ℓ)).
   - The update is clamped, so it can stop the motion but never reverse it: a finite-time arrest.
6. **The head spilling:** where the head's top stands above the rim by e, the part above the rim breaks away as a lump once its
   own weight and outward inertia overcome its strength, ρ_f(|g_eff| e/2 + a_out e) ≥ τ_y. The lump then flies freely, like the
   drops of stout.
7. **The head's mass** rides with the glass in the cart's equation, and leaves it with each lump.

Free inputs: R and φ_l (no measurement). Everything else is measured or derived from them.
