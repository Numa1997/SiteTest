# Skeptic review, Gate 1, contract L1 (round 3, last round)

Reviewed 23 October 2026. Object: `notes/droplets/contract-L1.md` (round 3). Read: that file, `skeptic-G1-L1-r1.md`, `skeptic-G1-L1-r2.md`,
`portfolios-src/droplets/derive/L1_r2.py` and `L1_beard.py` (both run with python3), and `dossier-fallspeed-efficiency.md` for citations. Nothing else
in the repository was read. I listed two paths to see whether they exist and read no content: `notes/droplets/baseline/theory.html` exists, and
`portfolios-src/droplets/text/` does not exist yet, as the contract says ("written after Gate 2").

My own code does not import the study's scripts:
- `/tmp/claude-0/-home-user-SiteTest/de75440b-f270-5344-8ae7-923c4f178e24/scratchpad/sk1r3_indep.py`: Beard's coefficients typed from the dossier; growth
  times by ODE with stop events, not by the script's quadrature; unprinted numbers, side effects, Gunn and Kinzer with two water densities.
- `/tmp/claude-0/-home-user-SiteTest/de75440b-f270-5344-8ae7-923c4f178e24/scratchpad/sk1r3_sce.py` and `sk1r3_sce2.py` (same folder): a minimal
  mass- and number-conserving bin model of the SCE, E = 1, coalescence = 1. I used it only to test whether the §7 prediction is open. It is
  not the study's L4.

Abstracts I read myself (Exa search tool, from the AMS, AIP, Wiley and ADS pages; the bare AMS pages return only a shell): Beard (1976), LeClair,
Hamielec and Pruppacher (1970), Beard and Pruppacher (1969), Pruppacher and Steinberger (1968), Pruppacher and Beard (1970), Gunn and Kinzer
(1949). I opened no full texts.

## 1. Round-2 objections: answered or not

| # | Round-2 objection | Verdict | Evidence |
|---|---|---|---|
| N1, #11 | Script does not print every number | **partly** | The round-3 block now prints 16 of the earlier gaps. Seven computed numbers in the contract are still not printed by `L1_r2.py` or the `L1_beard.py` it imports. (1) F_c(0) = 0.294 (§1). (2) "about 1.06" (§4.2). (3) "saturated air is 0.55 % lighter" (§5): the script computes the moist density but prints only the speed change. (4) "Slip changes Δv at 40 µm by +0.19 %" (§5). (5) "differs from Gunn and Kinzer's 27 cm/s by 5 %" (§6, also §8). (6) v_S(8 µm) = 0.00787 and v_B = 0.00796 m/s (§7): printed only as 0.0079 and 0.0080. (7) "growth times are 2–4 % too long" (§6), an estimate that is not computed. My code gives all seven correctly: 0.2941; 1.0608; −0.548 %; +0.193 %; 5.2 % or 5.5 % depending on the base; 0.007869 and 0.007963; and −2.50 % and −3.96 % in time for speeds +2.5 % and +4 %. §10 also says "except the honey Re range (printed too)", which contradicts itself. See new row A. |
| N2, #3 | Measurements in the study's range missed | **partly** | Answered as honesty. §3 and §6 now name the measurements, say that the agreement is the authors' statement, and state the Gunn and Kinzer conflict. I checked each quotation against the abstracts and they are faithful ("close agreement", "agreed quite closely", Re 0.001–10, Re 0.2–200, water-saturated air). Not done: reading B&P 1969 and P&S 1968 whole and giving Beard minus measured at a = 40–100 µm. The contract says the full texts are "blocked to this session", but CLAUDE.md asks for the roads that were tried, and it does not name them. Two new wording faults in the same paragraph (rows C and D). |
| N3 | Prediction 2 cannot fail | answered | Dropped. §7 says plainly that L1 makes no new prediction against nature, and why. |
| N4 | Prediction 1 cannot fail | answered | The SCE prediction is genuinely open: the box bound does not decide it, because in the SCE the time ratio is no longer a weighted mean of ΔV_S/ΔV_B. My rough bin SCE gives 1.62–1.90 for t₉₀ (outside [1.117, 1.262]) for mode widths 1.02–1.4 and separating radii 20 and 30 µm. So the prediction can fail, and in my rough model it does. Minor residual: the SCE setup is not pinned (row H). |
| N5 | "Halfway"; honey; wording; group count | answered, with a residual | Drag exponents 1.088 and 1.289 and multipliers 2.125 and 2.444 reproduced. Honey Re 0.010–0.070 reproduced (honey density 1400 kg/m³, in the script but not stated). Groups now counted correctly. Residual: "a quarter of the way" holds at 100 µm, not at 40 µm (row E). |
| N6, #21 | Dry vs 50 % RH | answered | With 50 % RH my code gives an in-sample maximum of 0.49 %. It stays inside ±0.5 % with ρ_w = 998.2 kg/m³ as well (0.45 %). Out of sample: −1.94, −1.94, −1.90, −1.01, −0.34, −0.21, −0.56, −0.37 %. ρ_w = 1000 is in fact the right choice here, because Gunn and Kinzer defined the diameter with 1 g/cm³ (dossier §1). |
| N7 | Moist viscosity | partly | The number is now "not computed". The reason given ("both act on Stokes and Beard alike and cannot move the time ratios") is wrong, although the conclusion holds (row B). |
| N8 | Bound statement loose | answered | Weight f/ΔV_S and both droplet speeds are written. I checked on 2001 points that ΔV_S/ΔV_B rises monotonically: 1.11670 → 1.69755. |
| N9 | F_c undefined | answered | Defined in §1 (collector water over all water, 0.294 at t = 0). |
| N10 | Seven terms' condition | answered | −3.19, 5.81, −0.05, −0.20, −0.68, 0.59, −0.13 at ln N_Da = 5.854, printed. |
| N11, #16 | 1.12 from the asymptote | partly | 1.12 and 1.06 are both given. But 1.06 uses Langmuir's C_D at Re = 1000 (18.62 × 24/1000 = 0.4469, dossier §5), while a rigid sphere at 3 mm falls at Re ≈ 1700–1790 (mine). The excess lies between the two, nearer 1.09 (row F). The measured shapes are a fair substitute for Beard's axis ratio. |
| N12 | Deformation as physics | answered | Matches the Pruppacher and Beard (1970) abstract word for word ("no detectable deformation" below a₀ = 140 µm; "slightly deformed into an oblate spheroid" for 140–500 µm; equatorial surface speed "about 1/100" of the fall speed). |
| N13 | No section 9 | answered | Added. Its claim needs scoping (row I). |
| N14 | Kajikawa a search excerpt | answered | Said so. |
| N15 | Davies attribution, μ₀ | answered | 2.51 = 2 × 1.257 attributed correctly; μ₀, p₀, T₀ as in dossier §2.2. |
| N16 | Spacing in collector radii | answered | 1.494 mm = 37 and 15 collector radii; Oseen length 95.6 µm (mine). |
| N17 | Charge, turbulence without numbers | partly | Turbulence deferred to L6: acceptable. Charge is still "not quantified here", although the dossier already holds a usable fact: Gunn and Kinzer's drops carried a charge, and "the charge was tested and did not change the speed" (dossier §1). Minor. |
| N18 | Rate exponent | answered | 1.47, 1.44, 1.32, 1.23 reproduced, all above 1. |
| N19 | Oseen uncited | partly | §6 says "Oseen's law, cited" but names no source. No source read by the study states Re(1 + 3Re/16) = N_Da/24. LeClair's abstract says that at the lowest Re its results agree best with Proudman and Pearson, whose expansion contains Oseen's term. Minor. |
| #12 | Textbook location | answered | The baseline file exists (I did not read its content, outside my boundary). The textbook folder does not exist yet, as stated. |
| #13 | Gunn and Kinzer body sentence | answered as far as possible | The abstract quotation "better than 0.7 per cent" is exact (checked on the AMS and ADS pages). The mass limit is attributed to the scout's OCR reading. |

Summary: 15 answered, 6 partly (N1, N2, N7, N11, N17, N19), 0 not answered. None of the "partly" items involves a wrong physics number.

## 2. New objections

| # | Where | What is wrong | Why (number or source) | Severity | What would settle it |
|---|---|---|---|---|---|
| A | Header ("Every number in this contract is printed by…"); §10 N1 | The claim is still false, now for seven numbers. | See the N1 row above. All seven values are right by my code, so no reader is misled about a value, only about where to check it. I rate it minor for that reason, though this is the third round with the same claim. | minor | Print the seven numbers (four lines in `L1_r2.py`), or make the header say "except …". Fix "(printed too)" in §10. |
| B | §5, "Dry air" row | The reason is wrong physics: "both act on Stokes and Beard alike and cannot move the time ratios". | Air density enters Stokes' law only through buoyancy, but enters Beard's law through N_Da. Saturated air changes t₉₀ by −0.0006 % with Stokes and by −0.066 % with Beard, so the ratio moves by −0.066 %. A −0.19 % moist viscosity (round 2's figure) changes t₉₀ by −0.190 % (Stokes) against −0.144 % (Beard): the ratio moves by +0.046 % (mine, ODE). The conclusion "negligible" stands. | minor | "They act differently on the two laws, but move the time ratios by less than 0.1 % (−0.07 % density, about +0.05 % viscosity)." |
| C | §6, first bullet | The Beard and Pruppacher description mixes measured and computed numbers. | Abstract (read): drag was *measured* for Re 0.2–200 in water-saturated air. From the fitted drag formulae, terminal velocities were then *calculated* for radii 10–475 µm at 400, 500, 700 and 1013 mb, with *assumed* temperatures of −16, −8, 14 and 20 °C. The contract lists "radii 10–475 µm … speeds also given for 400–1013 mb" under "wind-tunnel measurements". A reader would take them for measurements aloft, which §3 says do not exist ("no measurement aloft"). The same holds in §3: Beard's "three drag formulas for a rigid sphere" include B&P's water-drop formula. | minor | "Measured drag at Re 0.2–200 in saturated air; from it, computed speeds for radii 10–475 µm at 400–1013 mb (assumed temperatures)." |
| D | §3 and §6, Oseen | Wrong attribution: "the approach to Oseen's drag as Re → 0 is LeClair et al.'s finding". | The LeClair abstract says that the study "confirms the findings of Maxworthy, and Pruppacher and Steinberger, that as the Reynolds number approaches zero the drag … approaches zero via the Oseen drag rather than via the Stokes drag". So the finding is experimental, and LeClair's computation confirms it. | minor | Attribute it to Maxworthy (1965) and P&S (1968), confirmed numerically by LeClair et al., and give Oseen's law a reference (row N19). |
| E | §2, picture | "a quarter of the way" is attached to both sizes. | On the multiplier scale 2 → 4, ×2.125 is 6 % of the way and ×2.444 is 22 %; on the exponent scale 1 → 2, they are 9 % and 29 %. So "a quarter" fits the 100 µm drop only. The 40 µm collector is still almost wholly in the honey world. | minor | "barely past the honey world at 40 µm, a quarter of the way at 100 µm". |
| F | §4.2 | "about 1.06" uses the wrong Reynolds number, and the script does not print it. | A rigid sphere falling 1.06–1.12 × 8.06 m/s at 3 mm has Re = 1695–1791 (mine), not 1000. Langmuir's C_D there is below 0.447, so the excess lies between 1.06 and 1.12. Round 2 suggested "about 1.1". | minor | "between 1.06 (C_D at Re = 1000) and 1.12 (C_D = 0.40); a rigid sphere at Re ≈ 1700 is about 1.1 too fast." |
| G | §6, end of G&K bullet | "If the truth … lies 2–4 % above … below every other uncertainty of observable 1": the range is chosen, not derived, and the comparison is unsupported. | (a) The sources in hand span +2.5 % (B&P at 0.1 mm) to +7.5 % (G&K at 0.1 mm). 2–4 % drops the upper end; with +7.5 %, times shorten by 7.1–7.2 % (mine). (b) "Observable 1" is not defined in this contract. "Every other uncertainty" is literally false, since slip (0.19 %) and moist air (< 0.1 %) are smaller. The intended comparison (with E, turbulence) has no number here. | minor | "2.5–7.5 % above, so times 2.5–7 % too long; small beside the efficiency (L2)". Name the observable. |
| H | §7, prediction | Open and falsifiable (good). But the test is not pinned down. | t₉₀ in an SCE needs a radius that separates "collector water" (F_c as defined in §1 has no meaning for a continuous spectrum). The mode widths and "the coalescence law" (no name, no source) are not given. In my rough SCE the outcome is not sensitive to these: separating radius 20 µm gives 1.653 and 30 µm gives 1.661; widths 1.02–1.4 give 1.62–1.90; resolution s = 6 gives 1.654 and s = 12 gives 1.645. My code is validated against the box: with only collector–droplet pairs allowed it gives 1.150/1.217 (s = 6) and 1.147/1.208 (s = 12), against the contract's 1.145/1.200. So the prediction is genuine and likely to fail, and the stated consequence ("the page's account of where the drag law acts must change") must then be carried out. | minor | Before running L4, write the separating radius, the widths and the coalescence law (with its source) into the prediction, dated. |
| I | §9 | "In growth this is a 14–31 % effect … smaller than the efficiency of L2" is stated as the study's finding, but holds only for the box and the open cloud with a single collector size. | Which ingredient decides the speed is the study's own question. With all pairs acting (E = 1), my rough SCE gives a 62–90 % lengthening of t₉₀, comparable to the efficiency bound round 2 computed for the box (×1.6–2.9). The ranking may survive in L4 or it may not. §7 itself says this is open. | minor | "In the box and the open cloud this is a 14–31 % effect…; whether the drag law or the efficiency weighs more in the full SCE is decided in L4 (§7)." |
| J | Header, sources | The roads tried to the full texts are not named. | CLAUDE.md: "When a tool is blocked, take another road … and say which road you took." The dossier shows that the AMS PDFs were once reachable (Firecrawl PDF reader). Rounds 1 and 2 record curl 403, WebFetch 403, Exa 405, TinyFish unreachable, Firecrawl out of credits. | minor | One line naming the roads tried and when. |

## 3. What I checked and found right (my own code, not the script's)

- Air at 10 °C, 850 hPa: ρ_a = 1.04579 kg/m³, μ = 1.77107 × 10⁻⁵ Pa s. v(8 µm): 0.007869 (Stokes), 0.007963 m/s (Beard with slip). F_c(0) = 0.2941.
- Growth by ODE with stop events: open cloud 597.32 → 781.14 s (1.3077); box F_c = 0.5: R = 47.739 µm, 175.62 → 201.05 s (1.1448); F_c = 0.9: R = 58.072 µm,
  551.52 → 661.76 s (1.1999). Bounds 1.1167 to 1.6975, and the ratio rises monotonically. Every §7 number matches.
- Script output checked line by line against the contract: Re = 1 at 41.0 and 42.7 µm; vS/vB 1.015, 1.111, 1.273, 1.690; Re = 20 at a = 146 µm; ℓ = 0.0756 µm;
  Kn 0.0094; τ_p = 20.08 ms; 1.494 mm, 37, 15 radii; 96 µm; Bo 0.0070, 0.202, 1.617; HR +0.45 % (κ 73.7); slip 1.19 %, 0.237 %; saturated-air +0.045 %, +0.124 %;
  joints −0.165, −0.193, −0.017, +0.003 %; Oseen comparison 0.85/0.77 % and 0.20/0.26 %; 0.996 and 0.83; G&K in 50 % RH air; +2.47 % (saturated) for B&P at 0.1 mm;
  the L0 blow-up at 1264.0 s; the drag exponents; and the growth-rate exponents. All agree with the contract.
- Physics: the Davies number, C_D(Re) for a rigid sphere, the weighted-mean bound and the growth laws are right. The quotations from Beard (1976, "semiempirical
  drag relation for a rigid sphere"), LeClair et al. (1970), B&P (1969), P&S (1968), Pruppacher and Beard (1970) and Gunn and Kinzer (1949) match the abstracts
  I read. "Evaporation of the smallest drops" and "inaccurate below about 0.4 mm" match dossier §1 and §2.4. Beard's 0.09 %/0.6 % fit quality and regime ranges
  match dossier §2.4.
- The B&P point (25.6 cm/s at d = 0.1 mm, Re ≈ 1.7) comes from B&P's own formula for 0.2 ≤ Re ≤ 2, which Beard did not use (he used LeClair below Re = 20).
  So the +2.5 % is a genuine out-of-sample comparison in the study's range, and the contract uses it correctly.

## 4. Thresholds

| Threshold | Verdict | One line |
|---|---|---|
| Motivated | pass | Stokes is 11–69 % too fast across the collector window, and that is computed and right. The spoon picture shows the right mechanism (viscosity against inertia). |
| Honest | pass | The study's range now rests openly on LeClair's computation and on the authors' stated agreement, the G&K conflict is stated, and the prediction is open. The print claim is still false for seven correct numbers (A), and one reason is wrong (B). Both are minor. |
| Derived | pass | The Davies number, the exact weighted-mean bounds and the growth exponents are right, and I re-derived them independently. Only the "2–4 %" range is chosen, not derived (G). |
| Checked | pass | Every number I recomputed matches, by independent ODE code. The §7 prediction is not decided by the contract's own bound, and my rough SCE shows it can fail. |
| Sourced | pass | All quotations match the abstracts I read, and the coefficients match the dossier. Residual wording: B&P speeds aloft are computed, not measured (C); the Oseen finding is attributed to LeClair instead of Maxworthy and P&S (D); Oseen's law has no reference (N19); the roads tried are not named (J). |
| Readable | pass | Short and plain, with defined terms. "A quarter of the way" overreaches at 40 µm (E). |

No fatal item, no must-fix item, 16 minor (6 partial round-2 answers, 10 new: A–J). The minor items should be fixed before the page is written, especially B, C, H and I.

Gate 1 for L1: passed
