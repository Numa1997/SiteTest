# Gate 3 skeptic, round 1: Droplet Collection (rendered page, read blind)

Page: `public/portfolios/droplet-collection/index.html`, served at `http://localhost:8771/portfolios/droplet-collection/index.html`.
Method: headless Chromium (Playwright). I pulled the visible text of all four tabs, opened all five problem solutions,
took screenshots of all 9 figures at 1366 px and at 360 px (DPR 2), and ran all three simulation panels. I swept the pointer
across every figure and panel, and recomputed 45 quoted numbers in Python (NumPy, SciPy, SymPy). That included my own
trajectory integration for E(40, 8) and the critical Stokes numbers. I did not read notes/droplets/ or portfolios-src/.

## Verdicts

| # | threshold | verdict | evidence |
|---|---|---|---|
| 1 | Motivated | **PASS** | Every chapter opens with an everyday picture before the model: cardboard in drizzle (1), spoon in honey and water (2), windscreen in rain and mist (3), rain on a puddle (4), a ledger (5), savings (6), tea leaves (7), ice cubes (8). After the picture comes a formal reason: power counting for the blow-up, Buckingham for the drag law, a damped oscillator for St_c, the moment identity (5.2) for conservation. Chapters 4, 7 and 8 have no figure (see objection 24). |
| 2 | Honest | **FAIL** (all fixable) | Prices and limits are named well: the Langmuir weight sweep, one-sided flow, p > 0.6 held, the 3σ cut, the closed box, turbulence as a bound. Four failures. (a) §5.3 says Golovin's solution is "derived on the Checks tab by a Laplace transform", but no such derivation exists. "Laplace" appears once in the whole page. (b) The header claims "Every curve and every number on these pages comes from the model" / "every number computed by the model", yet Fig 2.1 plots Gunn–Kinzer data, Fig 3.2 plots Hall's dots, and ch 4 and ch 8 quote measured yields. (c) The Panel 3 dashed curves contradict the Fig 6.1 caption (obj. 1). (d) The Checks tab reports the efficiencies "8–10 % low at K = 3–3.6, unresolved", and the key 40/8 pair sits exactly there (St = 3.60). Chapter 3 never says so. |
| 3 | Derived | **PASS** | All 22 numbered equations follow on the page or name their source: (4.2) cites Straub, (8.2) cites PYK17 via Sotiropoulou. SymPy confirms dF/dR = R²/((R+r)³(R−r)) and lim F = −1/R for (1.4). Gaps: Golovin's solution (promised, absent), Beard's polynomial and Ayala's formula (cited, not shown). |
| 4 | Checked | **PASS**, with slips | 45 numbers recomputed (table below). The physics core matches to the quoted digits, including my independent trajectory integration: E_creeping = 0.3373, E_potential = 0.8382, St_c(creeping) = 1.21194. Six slips: the ch 0 fall speed (wrong by a factor of 3), the drag-doubling factor 2.44 (should be 2.50), 4.8 (should be 4.7), 20.09 % (19.74 % continuous), 134.1 "droplets" (really 301 drops split), and σ, which is never stated, so We cannot be recomputed from the page. |
| 5 | Sourced | **FAIL** | Nine works cited in the text are missing from the sources list: Beard et al. 2002, Beard and Ochs 1984, Low and List 1982, Hallett and Mossop 1974, Brownscombe and Thorndike 1968, Sotiropoulou et al. 2021, Davis 1972, Jonas 1972, Grabowski and Wang 2013. Golovin 1963 has no journal and Michael and Norey no page. Claims with no source: the condensation rate in ch 9, "the sources disagree" about small drops in ch 2, the energy range (8.2) was fitted to in ch 8, and Smoluchowski. |
| 6 | Readable | **FAIL** | At 360 px every figure label renders at **4.9–5.7 CSS px** (measured: SVG font size × screen CTM, all 9 figures and both Panel plots); at 1366 px they are 11.4–12.9 px. Fig 3.1's header line is clipped ("…air rises past the collecto"). Trajectories cross both label lines in Fig 3.1 and Panel 2. Legends sit on curves in Figs 5.1, 5.2 and 6.2 and in Panels 1 and 3. Questions with their own answers recur (obj. 23), and there are three walls of numbers (obj. 24). **Pointer test PASSES**: sweeping 25 points across every figure and plot produced 0 DOM mutations and identical pixels. No pointermove/mouseover listeners on any figure (CDP getEventListeners). |

## Simulation panels, as exercised

- **Panel 1.** Each run takes about 1 s. Default (drag balance, trajectories, energy law, SCE, 4 bins): 5.7 / 13.4 min; the page gives 13.35 at 4 bins, so this is consistent. Thesis kernel SCE: 2.2 / 4.4; GCE: 2.5 / 6.9; extended GCE: 6.7 / 18.3; Hall's E: 4.5 / 11.3; every touch merges: 5.7 / 13.3; E = 1 with drag balance: 2.9 / 7.9. All agree with the ch 5 table to grid accuracy. The spectrum slider works. The legend overlaps the thesis curve near t = 1–2 min.
- **Panel 2.** While the slider is dragged, the label updates but the drawing and the numbers do not (checked mid-drag). On release, both update within 0.01 s, as the note promises. Values match Fig 3.2 and ch 3: 40/8 → 0.344; 50/8 → 0.406 (page: 0.41); 100/8 → 0.550; 20/8 → 0.011. r ≥ R is refused cleanly. At 150/2 it shows "S = 0.000". At p > 0.6 it shows E computed at that p (for 40/30, 0.445), although the model holds E at p = 0.6. The panel does not say so.
- **Panel 3.** 1, 10 and 100 cm³ each run in about 0.5 s. One 1 cm³ run made no 100 µm drop. In 10 cm³, two runs gave 7.9 and 12.5 min; in 100 cm³, 2.5 min. These are consistent with the stored curves. **But the dashed (6.1) curves fall after their peak:** the 10 cm³ curve peaks at 0.32 near 10 min and drops to about 0.05 by 20 min, and the 100 cm³ curve drops from 0.98 to 0.37. Fig 6.1 in the notes uses the running maximum and is monotone. The readout says "first drop of 100 µm at none within 30 min" and "merger(s)".

## Objections

| # | severity | tab, section | quote | problem | fix I would accept |
|---|---|---|---|---|---|
| 1 | must-fix | Simulation, Panel 3 | dashed "(6.1) from the collection equation" | The share of volumes that have *ever* held a 100 µm drop cannot decrease. The panel uses the instantaneous n100(t), while Fig 6.1 and its caption use "the largest n100 reached so far". Panel and notes contradict each other. | Use the running maximum, as in Fig 6.1. |
| 2 | must-fix | Notes §5.3 / Checks | "derived on the Checks tab by a Laplace transform" | No such derivation exists on Checks or anywhere else. | Add the derivation, or at least the closed-form solution with Golovin's reference, or delete the clause. |
| 3 | must-fix | Notes, Appendix A | "Sources (read whole, or as stated…)" | 9 works cited in the text are missing (listed under threshold 5). Golovin 1963 has no journal; Michael and Norey 1970 has no page. "As stated in the study's notes" points to notes the reader cannot see. | Complete the list and say "abstract only" next to each such entry. |
| 4 | must-fix | All figures and plots at 360 px | n/a | Labels and ticks render at 4.9–5.7 px, which cannot be read on a phone. | Below ~600 px, scale the SVG text up (≥ 10 px rendered), thin the ticks, put the legend below the plot. |
| 5 | must-fix | Notes ch 0 | "droplets are about ten micrometres across, and they sink … at about a centimetre per second" | Stokes speed at r = 5 µm is 0.31 cm/s. One cm/s needs r ≈ 9 µm, and the study's own 8 µm droplets fall at 0.80 cm/s. The first number a reader meets is off by a factor of 3. | "about ten micrometres in radius" or "a few millimetres per second". |
| 6 | must-fix | Notes ch 4 | "We = CKE/(πσd_c²)" | σ is not defined at first use and its value is never given (I needed 0.0742 N/m to reproduce 2.0×10⁻⁵ and 0.52). σ also means σ_g in ch 5. | "σ = 0.0742 N/m, the surface tension of water at 10 °C" at (4.2). |
| 7 | must-fix | Notes ch 3 + Checks | Checks: "8–10 % low at K = 3–3.6, unresolved" | The pair that decides observable 1 has St = 3.60, inside the unresolved band, but "How far to trust it" is silent. Langmuir's K is also never defined on the page. | One sentence in ch 3: the solver matches an independent SciPy integration (and my own: 0.3373); the gap is against Langmuir's 1948 table; define K. |
| 8 | must-fix | Notes Fig 3.1; Simulation Panel 2 | "collector R = 40 µm, … air rises past the collecto" | The header text is clipped at the right edge, and paths run through both label lines. | Put the labels outside the drawing area or give them a background. |
| 9 | minor | Notes ch 2 | "Doubling the speed of a 100 µm drop multiplies its drag by 2.44" | Actually doubling Re on Beard's curve gives **2.50**; 2.44 = 2^1.289, from the local exponent. | "multiplies its drag by 2.5", or "drag grows locally as v^1.29". |
| 10 | minor | Notes §8.3 table | "0 to 4.8" | 2.80 × 0.14 × 12 = 4.70 (rounded 1.7 was used). | 4.7. |
| 11 | minor | Notes §8.1 | "the droplets split … 134.1 liquid droplets and 166.9 ice spheres" | 300 × 0.4455 = 133.65. The 134.1 is 301 × 0.4455, so both modes were split. | "all 301 drops per cm³ (both modes) split…". |
| 12 | minor | Notes §5.1 | "At the start 20.09 % of the water is in drops above 40 µm." | The continuous lognormals give 19.74 %. Four figures for a grid value. | "20.1 % on the grid (19.7 % for the continuous modes)". |
| 13 | minor | Notes §5.3 | "bins i≤j produce C_ij = K_ij N_i N_j Δt mergers" | For i = j there are N_i²/2 pairs, not N_i². | Add the ½ for i = j, or say the code does. |
| 14 | minor | Notes ch 1 | "W = 0.643 g/m³ (300 droplets of 8 µm per cm³)" vs ch 0 "0.805 g/m³" | A student will stall on two different water contents. | One clause: monodisperse vs lognormal (mean r³ larger by a factor of 1.25). |
| 15 | minor | Notes ch 3, 5, 6 | "about ν/U = 2R/Re"; "−τg* e_z"; "ν_k + ν_{k+1}"; "τ = −ln u₁/a₀" | ν is used before it is defined (only in the appendix), and e_z's direction is never stated. Symbol clashes: ν (viscosity vs product count), τ (response time vs waiting time), E (efficiency vs E² operator), a (radius vs air velocity), σ (surface tension vs σ_g). | Define each at first use; rename the clashes. |
| 16 | minor | Problems, P1 | "the growth becomes merely faster than exponential" | dlnv/dlnR from Beard: 1.76 (40 µm), 1.33 (100), 1.04 (300), 0.89 (500). Any power above 1 still blows up in finite time. Growth stays finite because the exponent falls below 1 and v saturates. | "slows to about exponential near 0.3 mm and slower beyond". |
| 17 | minor | Notes ch 2 | "a polynomial in ln N_Da" | The coefficients are not given, so a student cannot reproduce 0.177 m/s. | List b₀…b₆ and the slip factor 1 + 2.51λ/d in an appendix. |
| 18 | minor | Notes §8.2 | "αA = 9.2×10⁻³"; "eight to twelve orders of magnitude below the collisions (8.2) was fitted to" | A and its D-dependence are never given (implied A ≈ 1.14×10⁷ m⁻²). The fitted energy range is neither stated nor sourced. | Give A(D) and C, and the experiments' K₀ range with its source. |
| 19 | minor | Header, all tabs | "Every curve and every number on these pages comes from the model" | Not true for measured data and cited yields (obj. under threshold 2). | "…every number not attributed to a source comes from the model". |
| 20 | minor | Notes ch 7 | "the stronger turbulence seems to do less (−1.1 %)" | The sign is ambiguous next to "shortens by 1.7 %". | "shortens t90 by only 1.1 %". |
| 21 | minor | Notes ch 9 | "condenses 0.06 to 0.25 g/m³ … per minute" | The number is correct (I get 0.062–0.247 from the moist adiabat), but it is neither derived nor sourced. | "(moist-adiabatic lapse rate)". |
| 22 | minor | Figs 5.1, 5.2, 6.2; Panels 1 and 3 | legends | Legends drawn over curves. In Panel 3, "100 cm³" is struck through by a dashed curve. | Move the legends into empty space or outside the plot. |
| 23 | minor | Notes, several chapters | "Why does the radius run away…?", "Which energy can do the tearing?", "How much do these choices matter?", "Which ingredient decides the speed?"; ch 8 title "can collisions make new ice?" | The house rule forbids a question-and-answer format. Many "X, not Y" closers ("a door to a further study, not a flaw hidden in this one"; "what matters is what actually moves") read as AI tells. | State the point directly; cut most of the aphorisms. |
| 24 | minor | Notes ch 3 "How far to trust it", §6.3 "In 10 cm³…", ch 7 | n/a | Walls of numbers; about 20 values in three paragraphs of ch 3. Chapters 4, 7 and 8 have no figure. | A small table: crossover weight → E(40,8) → t90. A figure for E_coal(We) or for the ch 8 yields (log bars). |
| 25 | minor | Notes Fig 6.2 | 1 cm³ curve | It starts at ≈ 0.155, not 0.20, and the text does not say why (one collector, below 40 µm half the time). A student will read the whole gap as slower growth. | One sentence. |
| 26 | minor | Simulation, Panel 3 readout | "first drop of 100 µm at none within 30 min"; "merger(s)" | Ungrammatical machine text. | "no 100 µm drop within 30 min"; proper plural. |
| 27 | minor | Notes Fig 3.2 caption | "…and from Hall's (1980) compiled table…, at 10 °C and 850 hPa" | Reads as if Hall's dots were also computed at 10 °C and 850 hPa. | "lines at 10 °C, 850 hPa". |
| 28 | minor | Checks | "spectrum error 0.051"; "folder portfolios-src/droplets/" | The error norm is undefined, and the folder is named but not linked. | Define the norm; link the folder. |
| 29 | minor | Notes ch 2 | "where the sources disagree among themselves about the small drops"; "wind-tunnel measurements on water drops" | No sources named. Beard and Pruppacher 1969 is in the list but not cited at this point. | Name them. |
| 30 | minor | Notes ch 9 | "always through mergers of collectors with each other" | True for the 230 exact runs. The 1 m³ result is a mean-field estimate that does not track the mechanism. | "in every exact run". |
| 31 | minor | Simulation, Panel 2 | E readout at p > 0.6 | The model holds E at p = 0.6, but the panel shows E at the true p. | Say so under the readout. |
| 32 | minor | Simulation, all sliders | n/a | The range inputs are default browser blue, not the house palette. | Style them (accent-color). |

## Recomputed numbers (Python, from the stated inputs)

Inputs: T = 283.15 K, p = 850 hPa, R_d = 287.05, μ = 1.771×10⁻⁵ (page value; Sutherland 1.458e-6/110.4 gives 1.765×10⁻⁵, 0.3 % lower), ρ_w = 1000, g = 9.81, σ = 0.0742 N/m (my assumption), Beard (1976) coefficients from the paper.

| quantity | page | mine | verdict |
|---|---|---|---|
| ρ_a | 1.0458 | 1.04579 | ok |
| k | 1.2296×10⁸ | 1.22966×10⁸ | ok |
| v_S(40 µm) | 0.197 m/s | 0.19674 | ok |
| swept volume; clearing time | 9.9×10⁻¹⁰ m³/s; 17 min | 9.889×10⁻¹⁰; 16.85 min | ok |
| W (300 × 8 µm) | 0.643 g/m³ | 0.6434 | ok |
| droplet / collector LWC | 0.805 / 0.311 | 0.8050 / 0.3113 | ok |
| t* (blow-up) | 21.1 min | 21.07 | ok |
| (1.3) 40→100 µm | 12.64 min | 12.640 | ok |
| (1.4) 40→100 µm | 9.96 min | 9.9550 (closed form = quad) | ok |
| R_m | 60.15 µm | 60.148 | ok |
| 44 µm starter ends | near 70 µm | 69.7 | ok |
| closed box, Stokes t50 / t90 | 2.93 / 9.19 min | 2.927 / 9.192 | ok |
| Stokes Re = 1 radius | 41.0 µm | 40.99 | ok |
| Stokes 100 µm v, Re | 1.23 m/s, 15 | 1.2297, 14.5 | ok |
| slip correction 8 µm | +1.2 % | +1.19 % | ok |
| v_B(40, 60, 100 µm) | 0.177, 0.348, 0.728 | 0.1771, 0.3478, 0.7277 | ok |
| Stokes excess at 40, 60, 100 | 11, 27, 69 % | 11.1, 27.3, 69.0 % | ok |
| drag factor for doubled speed, 100 µm | 2.44 | **2.50** (2.44 = 2^1.289, local slope) | slip, obj. 9 |
| single collector, Stokes vs drag balance | 9.96 vs 13.02; 1.31; bounds 1.12, 1.70 | 9.955 vs 13.019; 1.308; 1.117, 1.698 | ok |
| closed box factors | 1.14, 1.20 | 1.145, 1.200 | ok |
| St, S, Re (40/8) | 3.60, 0.045, 0.84 | 3.598, 0.0450, 0.837 | ok |
| E creeping / potential (own trajectory code) | 0.337 / 0.838 | 0.3373 / 0.8382 | ok |
| Langmuir blend with 60, 20, 6, 2 | 0.344, 0.358, 0.399, 0.485 | 0.3439, 0.3571, 0.3983, 0.4848 | ok |
| St_c creeping (own axis integration) | 1.21194 | 1.21194 | ok |
| St_c potential | 1/12 | 1/12 (St = 0.09 hits; ≤ 0.083 approaches asymptotically) | ok |
| creeping approach at 1 + p, p = 0.2 | 0.039 | 0.0394 | ok |
| ν/U in collector radii | 2.4 | 2.39 | ok |
| P2 smallest droplet radius | 1.22 / 4.67 µm | 1.225 / 4.672 | ok |
| CKE, We (40/8) | 3.0×10⁻¹⁴ J, 2.0×10⁻⁵ | 3.04×10⁻¹⁴, 2.03×10⁻⁵ | ok |
| We (60/50) | 2.9×10⁻⁴ | 2.86×10⁻⁴ | ok |
| 500/250 µm: Δv, We, E_coal | 2.12 m/s, 0.52, 0.55 | 2.123, 0.520, 0.550 | ok |
| Stokes 500/250: Δv, We | 23.1 m/s, 61 | 23.06, 61.3 | ok |
| Golovin N/N₀ after 1 h | 0.00452 | 0.004517 | ok |
| Golovin mass below grid | −4.58×10⁻⁷ | 4.582×10⁻⁷ (lower bin edge x₀·2^(−1/16)) | ok |
| initial share ≥ 40 µm | 20.09 % | **19.74 %** continuous | grid value, obj. 12 |
| uncut tail > 100 µm | 0.25 per m³ | 0.251 | ok |
| 3σ cut radius | 69 µm | 69.12 | ok |
| captures 69 → 100 µm | 1312 | 1311.5 | ok |
| cloud volume per 100 µm / 1 mm drop | 3.75 cm³ / 3.75 L | 3.752 / 3.752 | ok |
| 10 cm³ water → one drop of | 139 µm | 138.6 | ok |
| 54 % in 155 µm drops per 10 cm³; P(≥1) | 0.39; 32 % | 0.386; 32.1 % | ok |
| Poisson median n100, 1 L / 1 m³ | 693 / 0.69 per m³ | 693.1 / 0.693 | ok |
| τ_K at ε = 10⁻²; τ(8 µm); τ(40 µm); St_K | 41 ms; 0.8 ms; 18 ms; ≈ 0.4 | 41.2; 0.80; 18.1; 0.44 | ok |
| St = 1 radius at 400 cm²/s³ | 43 µm | 43.1 | ok |
| ice v(40), v(8) at −10 °C, 600 hPa | 0.1726, 0.0076 | 0.1729, 0.0076 (my μ) | ok |
| ice K₀; F at C = 6.3×10⁶ | 2.6×10⁻¹⁴ J; 3.4×10⁻⁴ | 2.61×10⁻¹⁴; 3.40×10⁻⁴ | ok |
| old rule, one collision | 0.51 | 0.512 | ok |
| liquid/ice split | 134.1 / 166.9 | 301 × 0.4455 = 134.1 (300 × = 133.65) | wording, obj. 11 |
| shattering maximum | 4.8 | **4.70** | slip, obj. 10 |
| ratios to old rule | 1600, 52 | 1625, 52 | ok |
| condensation at 0.5–2 m/s | 0.06–0.25 g/m³/min | 0.062–0.247 | ok |
| ch 0 fall speed, 10 µm across | ≈ 1 cm/s | **0.31 cm/s** | error, obj. 5 |

Scripts and screenshots: `/tmp/claude-0/-home-user-SiteTest/de75440b-f270-5344-8ae7-923c4f178e24/scratchpad/g3/` (recompute.py, eff.py, stc.py, fontsz.py, hover.py, sim1–3.py, *.png).
