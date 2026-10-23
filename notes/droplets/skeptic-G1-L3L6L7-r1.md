# Skeptic G1, round 1: contracts L3, L6, L7

Blind Gate-1 review, 23 October 2026. Read: the three contracts whole, `physics.cjs` (`vBeard`, `weber`, `eCoal`, `ayalaFactor`,
`pairEfficiency`), `tools/run_cold.cjs`, `data/cold.json`. Not read: status, dossiers, other skeptic files.

Recomputation: `check.py` (Python, every constant retyped: 10 °C, 850 hPa, ideal-gas air, Sutherland viscosity with the thesis
constants, σ = 0.07422 N/m, ρ_w = 1000, g = 9.81, Beard 1976 retyped) and `cold_probe.cjs` (re-runs the cold case with the model's own
collision efficiencies, to get the energy spread, the riming geometry and the effect of other readings of the Phillips coefficients).
Both are in the session scratchpad: `/tmp/claude-0/-home-user-SiteTest/de75440b-f270-5344-8ae7-923c4f178e24/scratchpad/g1/`.

Sources opened for this review. Firecrawl was out of credits and Exa was rate-limited, so I used WebSearch, the OpenAlex API for
abstracts, and direct PDF downloads from Copernicus:
- Korolev and Leisner 2020 (ACP 20, 11767), Tables 1 and 2 and the text around them, read in full.
- Sotiropoulou et al. 2021 (ACP 21, 755), Appendix B: the Phillips et al. 2017 breakup law with its coefficients.
- Georgakaki et al. 2022 (ACP 22, 1965), section 2: the same coefficients, a second independent copy.
- Grzegorczyk et al. 2023 (ACP 23, 13505), eq. 2.
- Abstracts only: Beard and Ochs 1984; Beard and Ochs 1995 (Part II); Beard et al. 2002 (JAS 59, 233); Wang et al. 2008 (NJP 10,
  075013); Ayala et al. 2008, Parts 1 and 2; Wang and Grabowski 2009; Grabowski and Wang 2013.
- Not obtained: Phillips et al. 2017 itself, the full text of Ayala et al. 2008 Part 2 (IOP blocked the download), and Straub et al. 2010.

Air at 10 °C and 850 hPa: ρ = 1.04579 kg/m³, μ = 1.77107 × 10⁻⁵ Pa s, ν = 1.69352 × 10⁻⁵ m²/s. The IAPWS formula gives
σ = 0.07422 N/m, the same as the brief.

---

## L3: coalescence efficiency, exp(−1.15 We). Verdict: PASS with fixes

All the numbers are right. The problems are in what the picture describes and in how far the claim "E_coal = 1 for cloud droplets"
reaches.

### Objections

| # | Severity | Claim (quoted) | Why it is wrong or unclear | Fix I would accept |
|---|---|---|---|---|
| 1 | must-fix | Picture: "the air between them must drain before the surfaces touch, and a hard hit can deform them so much that they bounce apart or tear apart again." | The picture describes two mechanisms, and the model contains only one. Straub et al.'s exp(−1.15 We) is fitted to simulations of raindrops that touch, merge for a moment and then stretch apart again (filament, sheet and disk breakup). The air film and bouncing are not in it; the contract itself says "the energy laws know nothing of a bouncing air film". Bouncing also comes from a film that does not drain in time, not from a "hard hit": for small drops it happens at modest Weber numbers. A student will think the formula covers the puddle picture. | Keep the puddle for motivation. Then say plainly that two things can stop a merger: (a) the air film does not drain, so the drops bounce, and this is not in (L3.2); (b) the merged drop has too much energy of relative motion and tears apart, which is what (L3.2) describes. Fix "a hard hit … bounce". |
| 2 | must-fix | "No measurement of coalescence for cloud droplets this small was found in the sources read" and "a choice that is harmless only because any energy law gives the same there" | (i) The dossier holds the Beard and Ochs 1984 abstract. It says rebound cuts the time-averaged collection efficiency by 50 % for collectors growing from 50 to 500 µm by accreting 30 µm droplets, and gives a maximum collection efficiency of only 71 % (115 µm on 12 µm). That is evidence of E_coal well below 1 for drizzle-sized collectors catching cloud droplets. (ii) Beard and Ochs 1995, which the contract calls "the right law for our sizes", depends on We and the size ratio p and describes bouncing. The 40/8 µm pair (diameters 80/16 µm) lies inside its 14–800 µm range, so "any energy law gives the same" has not been shown. (iii) There is a direct measurement in favour of the contract for near-equal pairs: Beard et al. 2002 (JAS 59, 233) found E_coal "certainly greater than 91 % and likely greater than 95 %" for cloud drops of 55–105 µm radius at ratios 0.5–1. | State the evidence in both directions. Near-equal 55–105 µm pairs: measured E_coal > 0.91 (Beard et al. 2002), which supports E_coal ≈ 1 for the collector–collector pairs. Small droplets on collectors of 100 µm and more: rebound measured (Beard and Ochs 1984), so E_coal = 1 there is an assumption the law cannot test. Write "(L3.2) gives 1 to 4 parts in 10⁴", not "E_coal = 1". |
| 3 | must-fix | Low and List rejected because 0.54 at 8/40 µm is "against every energy argument" | Bouncing at low energy does not go against energy arguments; it is a different mechanism (film drainage). Low and List should be rejected because it is far outside its measured range, and because it contradicts the 2002 measurement: my recomputation gives Low and List = 0.23 for 60/50 µm, where Beard et al. 2002 measured > 0.91. | Reject it for those two reasons. |
| 4 | minor | "For every pair that decides observable 1 the collision energy is 10⁻⁵ to 10⁻⁴ of the surface energy" | The table's own 60/50 µm row has We = 2.9 × 10⁻⁴. | "2 × 10⁻⁵ to 3 × 10⁻⁴". |
| 5 | minor | Prediction 1: replacing (L3.2) by E_coal = 1 changes t₅₀, t₉₀ by less than 0.1 % | This follows directly from the table, where every relevant E ≥ 0.994, so it cannot fail in an interesting way. The prediction that could fail is the bouncing uncertainty of objection 2. | Label it a consistency check, or add a sensitivity run with E_coal = 0.8 for collectors ≥ 100 µm catching droplets ≤ 15 µm, in the spirit of Beard and Ochs 1984. |
| 6 | minor | "with Stokes speeds it switches mergers off above about 200 µm" | At 200/100 µm with Stokes speeds E is still 0.49; it reaches about 0 at 500/250. "200 µm" does not say radius or diameter. | "above about 300 µm radius (E = 0.49 at 200/100, ≈ 0 at 500/250)". |
| 7 | minor | The Price: "the two available laws differ by up to 0.2 (0.55 against 0.34 at 500/250 µm)" | I checked the other raindrop rows: 0.148 against 0.181 at 1000/500, and 0.034 against 0.000 at 2000/1000. "Up to 0.2" holds for these rows. | Show the three rows in the table. |

### Numbers recomputed (Beard speeds from my own Beard 1976 code; Stokes in brackets)

| Pair (µm) | Δv Beard (Stokes), m/s | We | E (L3.2) Beard (Stokes) | freed surface / CKE | Low and List (Beard Δv) |
|---|---|---|---|---|---|
| 40/8 | 0.169 (0.189) | 2.03 × 10⁻⁵ | 0.99998 (0.99997) | 1.7 × 10³ | 0.540 |
| 60/8 | 0.340 (0.435) | 3.67 × 10⁻⁵ | 0.99996 (0.9999) | 440 | 0.606 |
| 60/50 | 0.089 (0.135) | 2.86 × 10⁻⁴ | 0.99967 (0.9992) | 873 | 0.231 |
| 100/50 | 0.468 (0.922) | 5.06 × 10⁻³ | 0.99420 (0.9777) | 30.7 | 0.346 |
| 200/100 | 0.946 (3.689) | 0.0413 | 0.95365 (0.4858) | 3.77 | 0.346 |
| 500/250 | 2.123 (23.06) | 0.520 | 0.54998 (2 × 10⁻³¹) | 0.299 | 0.338 |
| 1000/500 | 2.685 (92.22) | 1.66 | 0.14776 (0) | 0.0936 | 0.181 |
| 2000/1000 | 2.529 (368.9) | 2.95 | 0.03364 (0) | 0.0528 | 0.000 |

Every row of the contract's table is reproduced to the digits quoted. The Low and List prefactor at 8/40 is 0.540, as quoted.

---

## L6: turbulence, decided by a number. Verdict: PASS with fixes

The numbers are right: Stokes numbers 0.14, 0.44, 0.88, and kernel factors +0.4, +5.6, +28 %. The conclusion "turbulence stays a
stated check for observable 1" is stronger than the method allows. The method switches turbulence off wherever the formula does not
apply, and it leaves out the larger turbulent effect on collision efficiency. So the result is a lower bound, and the page must say so.

### Objections

| # | Severity | Claim (quoted) | Why it is wrong or unclear | Fix I would accept |
|---|---|---|---|---|
| 1 | must-fix | "the SCE's t₉₀ shortens by 1.7 % at 100 cm²/s³ and 1.1 % at 400 cm²/s³ … Turbulence therefore stays a stated check for observable 1" | Two reasons make this a lower bound. (a) The enhancement is set to 1 for collectors above 60 µm and wherever St > 1. Observable 1 is built by collectors of 40–100 µm, so a large share of the mass flux gets no turbulence by construction. (b) Only the *geometric* kernel is enhanced. Wang et al. 2008 (abstract) find that turbulence also raises the *collision efficiency*: ×1.6 and ×4 for 18/20 µm, and an overall enhancement "typically below 2" for size ratios 0.2–0.8 (40/8 is at 0.2). That is still a factor of up to about 2, against the 1.056 used here. Wang and Grabowski 2009, and Grabowski and Wang 2013 (whose abstract is in the dossier), report that turbulence "can significantly reduce the time for warm rain initiation". A student will read the −1.7 % as contradicting them. | Say: "The part of the turbulent effect this study can compute (geometric kernel, pairs inside the formula's range) shortens t₉₀ by 1.7 %. It is a lower bound. The efficiency enhancement and the out-of-range pairs are missing, and studies with the full kernel find a significant speed-up." Keep turbulence as a stated check only with that sentence, and make observable 1 an upper bound on the time, as is already done for observable 2. |
| 2 | must-fix | t₉₀ shortens by 1.7 % at 100 cm²/s³ but only 1.1 % at 400 | This is an artefact of the range cut, not physics. At ε = 4 × 10⁻² m²/s³ the cut St ≤ 1 (τ = v/g) removes every collector above 43.1 µm (my bisection). At 10⁻² the cut falls at 66 µm, so the 60 µm radius cut is the binding one. Stronger turbulence switches the enhancement off for more collectors, so the effect shrinks. | Say why the 400 cm²/s³ number is smaller, or drop it. Never present it as a turbulence result. |
| 3 | must-fix | "Threshold chosen from the literature before computing: X = 10 % (Ayala et al.'s formula gives +5.6 % on the governing pair at 100 cm²/s³)" | The justification for a threshold "chosen before computing" quotes the result of the computation. A reader cannot tell what was fixed in advance. | Give the literature reason for 10 % (for example the efficiency band, 13.5 against 11.4 min, which is about 17 %), and move +5.6 % to the results. |
| 4 | minor | "+28 % at 400 cm²/s³" | St = 0.88 there, at the edge of a weak-inertia expansion (St ≪ 1). | Say it is at the edge of the formula's range. |
| 5 | minor | "g₁₂ = 1 (they find clustering negligible for size ratios above 1.3)" | I could not check the number 1.3. Part 1's abstract speaks of "a moderate level" of clustering for bidisperse pairs. | Give where in Ayala et al. this is stated. |
| 6 | minor | "below the efficiency band (13.5 against 11.4 min)" | Unclear: band of what, from which runs? | One clause defining it. |
| 7 | minor | Ayala weak-inertia formula | My recomputation implements the same four terms as `ayalaFactor`: shear R²ε/15ν, acceleration (τ₁−τ₂)² a₀ ε^{3/2} ν^{−1/2}, gravity–shear coupling (v₁τ₁−v₂τ₂)² 2ε/15ν, and π/8 (τ₁−τ₂)² g². So it checks the arithmetic, not the coefficients. I could not open Part 2. The limit is right: with no turbulence it reduces to ½Δv. | Quote the equation number from Ayala et al. Part 2 next to (L6.x). |

### Numbers recomputed

| ε (m²/s³) | τ_K (s) | St of 40 µm, τ = v/g (τ Stokes) | St of 8 µm | Ayala factor, 40/8 µm | Term sizes (m²/s²): shear / acceleration / gravity–shear / gravity |
|---|---|---|---|---|---|
| 10⁻³ | 0.1301 | 0.139 (0.154) | 0.0062 | 1.0043 | 9.1e−9 / 1.6e−5 / 8.0e−5 / 1.12e−2 |
| 10⁻² | 0.0412 | 0.439 (0.488) | 0.0197 | 1.0564 | 9.1e−8 / 5.0e−4 / 8.0e−4 / 1.12e−2 |
| 4 × 10⁻² | 0.0206 | 0.877 (0.976) | 0.0394 | 1.2814 | 3.6e−7 / 4.0e−3 / 3.2e−3 / 1.12e−2 |

- The contract's 0.14, 0.44, 0.88 use τ = v/g, the drag-corrected time. That is fine; say so.
- The enhancement comes almost entirely from fluid acceleration and gravity–shear coupling; shear is negligible. This fits the
  tea-leaf picture.
- The St = 1 cut falls at a collector radius of 66.1 µm at 10⁻² and 43.1 µm at 4 × 10⁻².
- The Saffman–Turner shear kernel at 0.1 m²/s³ is 0.90 % of gravity for 40/8 µm. The contract's "under 1 %" holds, narrowly.
- Wang et al. 2008 abstract checked: "factor of 7 and 2 at 400 and 100 cm²/s³" for 18/20 µm, as the contract quotes.

---

## L7: ice production rates at −10 °C. Verdict: PASS with fixes

The rates reproduce, and the prediction survives under the reading the cited sources recommend. But five statements of fact are wrong:
1. the asperity density A does not match either secondary source;
2. the collision energies are 100 to 10 000 times below the stated range;
3. the Hallett–Mossop window is misdescribed;
4. the shattering data were taken in largely the geometry the contract calls unmeasured;
5. the "measured at −10 °C" bracket is built from maxima taken at other temperatures.

### Objections

| # | Severity | Claim (quoted) | Why it is wrong or unclear | Fix I would accept |
|---|---|---|---|---|
| 1 | must-fix | "type-I coefficients at −10 °C (A = 1.44 × 10⁶ m⁻²…)"; code: `A = 0.428*3.78e4*(1 + 0.0079*Math.pow(500,1.5))` | Both secondary copies I opened write a₀ = 3.78 × 10⁴ (1 + 0.0079 / D^1.5), with D in metres the diameter of the smaller particle: Sotiropoulou et al. 2021 App. B, and Georgakaki et al. 2022 §2. The code multiplies instead of dividing, with D = 500 (µm). The temperature factor 0.428 is right. Sotiropoulou adds that the law was fitted for 500 µm < D < 5 mm, and that outside this range D is set to the nearest limit. Clamped to 500 µm: A = 1.14 × 10⁷ m⁻², 7.9 times the contract's value. With the true D (16–80 µm): A = 2 × 10⁹ to 1.8 × 10⁸ m⁻². | Use the published form with D clamped to 500 µm, and say so. Quote A = 1.1 × 10⁷ m⁻². State that taking the true D instead raises the rate about 30-fold more (see the numbers). |
| 2 | must-fix | Prediction: "at least a thousand times less new ice than the old rule (Outcome: 7 × 10³ to 4 × 10⁴ times less)" | With objection 1 fixed, the upper end becomes 1.6 × 10⁻³ cm⁻³ min⁻¹, 1.6 × 10³ times below the old rule. The prediction survives, but only by a factor of 1.6. Without the clamp it is 5.0 × 10⁻² cm⁻³ min⁻¹, only 52 times below, and the prediction fails. | Report the new ratio. Say the prediction holds only if D is clamped to the law's fitted range, which is the recommended use. |
| 3 | must-fix | "applied here to collisions of 10⁻¹² to 10⁻⁹ J, an extrapolation over 4 to 9 orders of magnitude" | The event-weighted collision energies in this very run are 1.3 × 10⁻¹⁴ J (5 %), 5.4 × 10⁻¹⁴ J (median) and 2.3 × 10⁻¹³ J (95 %), with a maximum of 3.7 × 10⁻¹¹ J. A 40/8 µm ice pair has K₀ = 2.6 × 10⁻¹⁴ J. Against the fitted 10⁻⁴ to 10⁻² J this is 8 to 12 orders of magnitude, not 4 to 9. | "about 10⁻¹⁴ to 10⁻¹³ J, 8 to 12 orders of magnitude below the fit". |
| 4 | must-fix | "Rime splintering (Hallett–Mossop): measured only between −8 and −3 °C (Korolev and Leisner, Table 2): zero at −10 °C" | Table 2 lists measurements from −2 to −16 °C. Hallett and Mossop 1974 cover −2 to −16 °C and Mossop et al. 1974 measured at −8 and −10 °C. What lies between −3 and −8 °C is the *active* window, and HM found production stops outside it. So zero at −10 °C is a measured result, not an extrapolation. Note too that Latham and Mason 1961 report splintering peaking between −8 and −18 °C (Table 2), which disagrees. | "Splinter production is measured to stop below about −8 °C (Hallett and Mossop 1974; Mossop et al. 1974 at −10 °C); one older study (Latham and Mason 1961) disagrees; we take zero." Besides, only 0.004 of the 2.80 cm⁻³ min⁻¹ events with drops ≥ 25 µm are in the riming geometry (objection 5), so this channel cannot matter anyway. |
| 5 | must-fix | "Applied to liquid drops of radius ≥ 25 µm captured by ice, an assumption: the data are for drops that freeze alone, not on contact with ice" and Price: "the only channel that could matter at −10 °C rests on an unmeasured geometry" | Both halves are wrong. (a) In this run 2.799 of the 2.803 events cm⁻³ min⁻¹ have the liquid drop *larger* than the ice particle. A big supercooled drop sweeps up a small ice sphere and freezes whole. It is not "captured by ice". (b) In Korolev and Leisner's Table 1, most of the free-fall shattering experiments nucleated their drops with "tiny ice crystals": Brownscombe and Thorndike 1968 (50–90 µm, −5/−10/−15 °C, free fall), Takahashi and Yamashita 1970, Takahashi 1975, Lauber et al. 2018, Keinert et al. 2020. That is the same geometry as (a). So the channel rests on a *measured* geometry. The real uncertainties are drop size (50 µm diameter is the bottom of the measured range, and Wildeman et al. 2017 argue that drops below 50 µm cannot shatter) and the scatter between laboratories. | Rewrite the picture: "a large supercooled drop collects a small ice sphere and freezes, as in the laboratory experiments". Rewrite the Price around drop size and the scatter between laboratories. This makes the channel *more* credible, and the page should say so. |
| 6 | must-fix | "measured at −10 °C for drops of 50 µm diameter and more; 1–37 % of drops shatter, with at most 3–12 fragments … 0.03–1.7 fragments per freezing drop" | Table 1 gives the *maximum* shattering frequency and the *maximum* number of fragments over each study's whole temperature range. Most of those maxima are at −15 °C, not −10 °C; the 37 % is Takahashi and Yamashita 1970, peaking at −15 °C. 0.37 × 12 = 4.4, not 1.7. The bracket is evidently 0.14 × 12 (Brownscombe and Thorndike) and 0.01 × 3 (Keinert), but this is not shown. Each end is a product of two maxima, so 0.03 is not a lower bound: Hobbs and Alkezweeny saw no shattering at 20–50 µm. | Name the pairing: "0.14 × 12 = 1.7 (Brownscombe and Thorndike 1968, 50–90 µm, maxima over −5 to −15 °C); 0.01 × 3 = 0.03 (Keinert et al. 2020, 300 µm drops)". Say both are upper-leaning and that the true value for 50–60 µm drops at −10 °C may be near zero. Write "0 to 4.8 cm⁻³ min⁻¹". |
| 7 | must-fix | The cold case: "134.1 cm⁻³ liquid droplets and 166.9 cm⁻³ ice spheres" | 167 cm⁻³ of ice at −10 °C is several orders of magnitude above the ice concentrations observed in mixed-phase clouds at that temperature (order 1 L⁻¹ = 10⁻³ cm⁻³). The channels also scale differently: ice–ice events go as N_ice², shattering as N_ice × N_liq. So the *ranking* of channels, and not only their size, depends on this construction. (The comparison with the old rule does not, since both use the same ice–ice events.) | One sentence: "This is the thesis's starting state, far more glaciated than observed clouds; at realistic ice numbers ice–ice breakup drops as the square of N_ice and shattering only linearly, so breakup matters even less." |
| 8 | minor | Picture: "Each chip is new ice made from old ice: the number of pieces rises, the mass of ice does not." | True for ice–ice breakup. For a freezing drop that shatters, the ice mass does rise (liquid becomes ice). | Limit the sentence to breakup. |
| 9 | minor | "C between 2.2 × 10⁴ and 6.3 × 10⁶ J⁻¹" | It is C = 6.3 × 10⁶ ψ, with ψ = 3.5 × 10⁻³ (Sotiropoulou's sublimation correction, after Vardiman 1978) or ψ = 1. The reader cannot see where the range comes from. | Say what ψ is. |
| 10 | minor | Table row "Ice–ice breakup (5.27 riming and 2.88 ice–ice events cm⁻³ min⁻¹ in all)" | The riming count belongs to the shattering row. | Move it. |
| 11 | minor | Old rule: "as 5 µm fragments" | In the code these are 5 µm in *radius*, ice density 900. | Say "5 µm radius". |
| 12 | minor | "type-I" | The sources I read call this set graupel–graupel. The thesis's ice spheres are frozen drops of 8–80 µm, not graupel. | "the graupel–graupel coefficients (Phillips type I), the nearest category to dense ice spheres". |

### Numbers recomputed

- Liquid fraction at −10 °C from the polynomial: 44.550 %. Liquid 134.1 cm⁻³, ice 166.9 cm⁻³. ✓
- Phillips temperature factor: 1/3 + max(2/3 − |263.15 − 258|/9, 0) = 0.4278. ✓ (0.428 in the code)
- A as coded: 1.445 × 10⁶ m⁻². As published, D clamped to 500 µm: 1.14 × 10⁷. With the true D: 2.0 × 10⁹ at 16 µm, 1.8 × 10⁸ at 80 µm.
- A 40/8 µm ice pair at −10 °C and 600 hPa: v = 0.1726 and 0.00763 m/s, K₀ = 2.6 × 10⁻¹⁴ J. Fragments per event at C = 6.3 × 10⁶:
  7.9 × 10⁻⁵ (contract A), 3.4 × 10⁻⁴ (clamped), 1.3 × 10⁻² (true D).
- Order of magnitude of the ice–ice rate, by hand: the 40 µm ice mode (0.55 cm⁻³) sweeping up the 8 µm ice (166 cm⁻³) gives
  6.6 cm⁻³ min⁻¹ × E with the geometric kernel. The model gives 2.88 in all, so E ≈ 0.4. Consistent. ✓
- Old rule for one 40 µm event: 0.001 × (40/5)³ = 0.51 fragments. The model gives an average of 2.61 / 2.88 = 0.9 per event. Consistent. ✓
- Shattering: 2.80 × 0.03 = 0.084 and 2.80 × 1.7 = 4.8 cm⁻³ min⁻¹. ✓ (the arithmetic; see objection 6 for the inputs)
- Re-run with the model's collision efficiencies (`cold_probe.cjs`):

| Quantity | Value |
|---|---|
| Ice–ice events | 2.878 cm⁻³ min⁻¹ |
| K₀, event-weighted, 5 / 50 / 95 % | 1.3 × 10⁻¹⁴ / 5.4 × 10⁻¹⁴ / 2.3 × 10⁻¹³ J (max 3.7 × 10⁻¹¹) |
| Breakup (upper C), contract A / clamped / true D | 3.70 × 10⁻⁴ / 1.61 × 10⁻³ / 4.99 × 10⁻² cm⁻³ min⁻¹ |
| Old rule ÷ breakup | 7.0 × 10³ / 1.6 × 10³ / 52 |
| Events with liquid ≥ 25 µm: drop larger than ice / riming geometry | 2.799 / 0.004 cm⁻³ min⁻¹ |

---

## Summary

- L3, PASS with fixes. Every number reproduces. The picture (air film, bouncing) describes a mechanism the exp(−1.15 We) law does not
  contain. "E_coal = 1 for cloud droplets" must be stated as a property of the law. Cite the measurement that supports it for
  55–105 µm pairs (Beard et al. 2002, > 0.91) and the one that questions it for drizzle collectors (Beard and Ochs 1984, rebound).
- L6, PASS with fixes. The Stokes numbers and the +0.4 / +5.6 / +28 % reproduce. The −1.7 % in t₉₀ is a lower bound: it covers the
  geometric kernel only, with turbulence switched off for collectors above 60 µm (above 43 µm at 400 cm²/s³). The smaller effect at
  400 cm²/s³ is an artefact of that cut. The "chosen before computing" threshold quotes the computed result.
- L7, PASS with fixes. The rates reproduce. A in the code does not match the published form: corrected, A is 7.9 times larger, the
  breakup rate rises 4.3 times, and the "1000×" prediction survives only by a factor of 1.6. The collision energies are
  10⁻¹⁴–10⁻¹³ J, not 10⁻¹²–10⁻⁹ J. The Hallett–Mossop window is misdescribed. The shattering events are big drops collecting small
  ice, which is the laboratory geometry, so the channel is better grounded than the contract says. The 0.03–1.7 bracket is built
  from maxima.
