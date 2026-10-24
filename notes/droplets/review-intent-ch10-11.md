# Review: Part IV (chapters 10 and 11, panels 4 and 5, problems 6 and 7) against Numa's intent

Reviewer: independent, 23 October 2026. I read the rendered page at 1280 px and 390 px, ran both panels in headless Chromium,
and re-ran parts of the chapter 11 model to test claims. I did not read the author's plans in `notes/droplets/`.

Evidence folder (screenshots, scripts, measurements):
`/tmp/claude-0/-home-user-SiteTest/de75440b-f270-5344-8ae7-923c4f178e24/scratchpad/review_intent/` (called `S/` below).

## Verdict

| criterion | verdict | one line |
|---|---|---|
| Delivers Numa's intent | **FAIL** | His one sentence (energy and entropy decide the shares and the diets, *depending on where we sit*) became two chapters that never meet. The energy idea is tested only in its weakest form. Picture data is postponed. The shapes are drawn by hand, not made by a random process. |
| Motivated | PASS | Both openings are everyday pictures that really are the mechanism (rain on a window; a smoke plume). |
| Readable for the student | **FAIL** | Chapter 10 is 2282 words, twice any earlier chapter. One table counts mergers while the figure beside it counts water, and the text does not say so. Symbols are reused. One section is a question with its answer. The panel 4 labels are 5.7 px at 390 px. |
| Honest | **FAIL** | The cloud's outline is fixed in space while the mean wind blows through it. With the eddies off, 22.5 % of the water still leaves through the sides of the cumulus (measured), yet the text says the eddies carry the drops out. One table row changes two things and does not say so. |
| Figures and panels | **FAIL** | No figure or panel shows the velocity field or the path of a single drop, which is the thing Numa asked for. Panel 5 has one button and nothing to set. The pointer behaviour passes: nothing reacts to a passing pointer (measured). |
| Coherent with chapters 1–9 | **FAIL** | Chapter 11 adds five effects in one step: space, a mean cell, a stochastic element, evaporation and super-droplets, plus shapes. The ladder's rule is one effect per level. |

## Point-by-point intent

| Numa asked for | status | evidence |
|---|---|---|
| Competition by Monte Carlo or by gradient descent that minimises energy and maximises entropy | **Built partly, then argued down** | 10.3 builds a Metropolis rule (10.5) and a steepest descent ("largest pair first"), and Fig. 10.2 and panel 5 compare them with the real kernel. Both are used only as contrasts, and the chapter concludes "energy fixes that end; it cannot choose among paths". The physics is right, but the idea is tested only where it is bound to lose: direct acceptance of a merger. Two stronger forms are missing. The free energy E − TS is never written. Vapour exchange through drop curvature (Kelvin), the one channel where surface energy really chooses which drop grows, is never mentioned (objection 2). |
| "each proportion of each population and what it eats" | **Built, in the box only** | 10.4 ledger, Figs. 10.3 and 10.4, and the merger table. The shares and diets are set by the kernel, not by energy. The ledger does not exist in the chapter 11 code (`physics.cjs` `makeCloud` keeps no channel ledger). |
| "will eventually minimise energy, maximise entropy" | **Explained away** | In a closed box, "eventually" is one drop (10.6), so the question has only a trivial answer. No open, steady cloud is built where "eventually" could mean something. Maximum entropy is tested only in the closed box with N and M as constraints (Fig. 10.6). |
| "depending on where we sit in the field" | **Built partly** | Fig. 11.4: 90.2 % of the 100 µm passages happen in the updraft core. The panel 4 probe gives the local wind, σ, T_L, water and largest drop. There are no shares, diets, energy or entropy by place, and no "fate by starting place". |
| Velocity field with a stochastic element, "not a random velocity field" | **Built; it is what he meant, but it is not shown** | (11.1) is mean cell + Ornstein–Uhlenbeck u′ − fall speed, with Kolmogorov scaling and Thomson's drift. That is a deterministic field with a stochastic element, as he said. But u′ is drawn separately for each drop, not as a field. Two drops in the same cell get unrelated eddies, so there are no "puffs" as in the chapter's own chimney picture. No figure draws the field or a single drop's path. |
| Not a cylinder fall | **Built** | A 2 km × 1.5 km slice, an overturning cell, fall-out through the base. |
| "any geometric beautiful shape a stochastic process … might give us" | **Built partly** | Four fixed hand-made shapes (`SHAPE_BOX`, five discs and a slab for the cumulus). None comes from a random process. The outline never changes in time. The code takes any `inside(x,z)` mask, but the reader cannot use that. |
| Picture data from clouds | **Missing (postponed)** | Ch. 11 callout: "a field measured from pictures of real clouds … is the next study, not done here." |
| Simple models first, then scale up | **Partly** | Chapter 10 stays in the box (good). Chapter 11 jumps (objection 6). |
| "think thrice before committing bullshit physics … an honest model" | **Partly** | The limits callout is good. Several prices are not named (objections 3–5). |

Respect for the energy and entropy idea: the tone is respectful ("the gap … is the most instructive part"), and Problem 6 is a fair test of the idea. But the chapter does not steel-man the idea. It never writes E − TS. It never gives the drops' own entropy, which I estimate below at about 10² k_B per drop against about 10¹⁰ k_B released per merger. It never shows the vapour channel, where curvature energy really does pick winners. Without these, a reader like Numa will read 10.3 as "your idea, built so it fails". Nothing he asked for was quietly swapped for something easier, except two things. The stochastic *field* became a stochastic velocity carried by each drop. The shapes made by a random process became four drawn shapes.

## Objections

**1. Fatal. Energy, entropy and place never meet.** Numa's sentence joins three things: competition (shares and diets), an energy/entropy principle, and place. Chapter 10 has the first two in a box with no place ("Everything so far happened in a box with no place in it"). Chapter 11 has place but no ledger, no energy and no entropy. Fig. 11.4 (birthplace of 100 µm drops) is the only place-resolved result.
*Fix required:* in the chapter 11 run, keep the 10.4 ledger by region: updraft core, flanks, a band 100 m inside the outline, and below the base. Report, for each region, the population shares, the diet (who ate whose water), the surface energy released, and the spectrum error against the local maximum-entropy gamma (the Fig. 10.6 measure). Add a map of each 50 m cell's starting water by fate: rained, evaporated, still aloft. Then write one section, "11.5 Energy, entropy and place", that answers his sentence with these numbers.

**2. Major. The energy idea is not given its strongest form.** (a) "Minimise energy, maximise entropy" is, in physics, "minimise the free energy F = E − TS". 10.2 and 10.3 treat E and S apart and never write F. The drops' own entropy (where they are in the volume) favours many drops by about 104 k_B per drop. I estimate this from the thermal de Broglie length of an 8 µm drop at 283 K and 3×10⁸ drops per m³. A merger releases about 10¹⁰ k_B. One paragraph with these two numbers would settle the idea fairly and in his words. (b) Surface energy does choose winners in real clouds, through vapour. A curved surface holds its water less tightly (the Kelvin effect), so in a closed volume large drops grow at the expense of small ones. With the model's own σ and G (11.3), in air saturated over flat water, a pure-water 8 µm droplet would lose its water by curvature alone in about 39 min (my estimate: a = 2σ/(ρ_w R_v T) = 1.14 nm, dr²/dt = −2Ga/r). The dissolved salt opposes this. This is an hour-scale, place-dependent, energy-driven competition, and it is exactly his picture. The notes never name it (no hit for Kelvin, Ostwald or ripening in `text/`). Literature exists (Wood, Irons and Jonas 2002, J. Atmos. Sci. 59, 2681, "spectral ripening"; I confirmed the metadata only, I did not read it).
*Fix required:* a short section in chapter 10 that writes F = E − TS, gives the per-drop entropy number, and names the vapour channel with its size from the model's G and σ. Mark it as the energy-driven competition the closed collision box cannot show.

**3. Major (honesty). The cloud's outline is fixed in space, and the mean wind blows through it.** The overturning cell fills the shape's bounding box (`SHAPE_BOX`), not the shape. For the cumulus and the disc, the cell's streamlines cross the outline. Air that is saturated on one side of the line is treated as 80 % humid the moment it crosses. I measured this with the model's code (a copy that logs where evaporation happens, `S/evap_where.cjs`, output in `S/evap_where.txt`; one seed, 32 super-droplets per cell). With the stochastic element **off**, 22.5 % of the cumulus water and 20.9 % of the disc water evaporate through the sides and top. For the box and the tower the figure is 0.0 %, because there the cell fits the shape. The text says the opposite: "The stochastic element is what carries drops across the edge". The shape comparison in 11.3 (and the chapter 9 summary "the more edge … the more of its water evaporates") therefore mixes two things: the edge, and how well the cell fits the shape. Without eddies the ranking even reverses: tower 49.1 % rained, cumulus 45.6 %, disc 42.7 %, box 37.9 %. Two more prices go unnamed. The cell has zero vertical wind at the cloud base, whereas a cumulus is fed by an updraft through its base. And evaporated water simply vanishes: the clear air never gets moister.
*Fix required:* either make the mean flow follow the shape (stream function zero on the outline), or say plainly that the outline is a fixed line the mean wind crosses. Then give the share lost that way for each shape and rewrite the 11.3 reading and the chapter 9 item. Add the base-updraft and lost-vapour prices to the "does not do" callout.

**4. Major (honesty). The row "cumulus, eddies strongest in the core" changes two things and the text never discusses it.** In `tools/run_cloud.cjs` this case is `{peaked: true, eps: 4e-2, epsOut: 1e-3, kernelEps: true}`. It sets ε to 4×10⁻² in the core (not 10⁻²) **and** switches on the turbulent collision factor of chapter 7 (`ayalaFactor`). The table label names neither. This also contradicts the callout "the stochastic element … does not change how fast two drops in one cell approach each other".
*Fix required:* split it into two rows (ε profile alone; then plus the chapter 7 collision factor), label them as such, and give each one sentence in 11.3. Otherwise remove the row.

**5. Major. The stochastic element is carried by each drop, not by a field, and the reader never sees it.** In (11.2) every drop has its own u′, unrelated to its neighbours'. That is a standard Lagrangian model (Thomson 1987), and it is honest as far as it goes. But it cannot fold an edge into puffs, as the chimney picture promises, and it is not the "velocity vector field … modelled stochastically" that Numa asked for. No figure in chapter 11 draws the field or one drop's path. In panel 4 the mean-wind arrows are faint, hidden under the dots, and drawn as bare ">" heads where the wind is zero (screenshot `S/shape_1280.png`, 33 of the 63 arrow points lie outside the cell, where the wind is zero).
*Fix required:* (a) Add Fig. 11.0: the mean cell's streamlines with three drop paths from one start, with the stochastic element on and off. (b) Name the price in the callout: neighbouring drops feel unrelated eddies, so the model spreads drops but makes no puffs. (c) In panel 4, draw no arrow where the wind is zero, and add a "trace one drop" option that leaves a short trail behind one chosen super-droplet. The trail is drawn every frame, with no reaction to the pointer.

**6. Major (coherence). Chapter 11 breaks "one effect per level".** In one step it adds a domain with space, fall-out to the ground, a mean cell, an OU stochastic element with Thomson's drift, evaporation outside the outline, the super-droplet method, and four shapes. The ablation table helps, but the text introduces everything together.
*Fix required:* order 11.1–11.4 as rungs, each with its own number. (i) Super-droplets in the box: the check that is already there. (ii) A still, saturated column with fall-out only: how much rains. (iii) Add evaporation below the base. (iv) Add the mean cell. (v) Add the stochastic element. (vi) Change the shape. Most of the numbers already exist in the ablation runs.

**7. Major (teaching). The merger table and the diet figure count different things, and the text does not reconcile them.** The 10.4 table counts *mergers*: collectors eat collectors in 0.36 % of them. Fig. 10.4 counts *water*: there the same channel moves about 15 % of all the water (dashed ochre line, `S/fig-10-4_1280.png`). The text says "Collector–collector mergers are rare, a third of a percent", but "what it eats" is a question about water. Fig. 10.4 also shows six curves on a log axis from 10⁻⁶ to 1, and the channels that matter sit crowded between 0.1 and 1.
*Fix required:* give the table a water column, or make it water only. Add one sentence: "rare as events, large in water". Draw Fig. 10.4 on a linear axis, or as stacked shares.

**8. Major (teaching). Chapter 10 is too long and too dense for one chapter.** At 2282 words with 7 equations, 6 figures and 5 "In our cloud" boxes, it is about twice chapters 5 and 6. The 10.1 box alone holds seven numbers, including a Jensen's-inequality aside the student has never met. The table gives "50.95 ± 0.15 %" where "51 %" teaches the same thing.
*Fix required:* split chapter 10 into "Energy and entropy of merging" (10.1, 10.2, 10.6) and "Three rules and who eats whom" (10.3, 10.4, 10.5), or cut it to about 1400 words. Round the box numbers to two digits. Remove the Jensen aside, or explain it in one plain sentence.

**9. Major (panels). Panel 5 gives the reader nothing to do.** One button replays the chapter's result for new random drops (about 0.9 s). It has no control and no view of the drops themselves. The energy-only idea becomes tangible only if the reader can see *what* each rule builds and can push on the idea.
*Fix required:* add a size spectrum for each rule at the moment half the drops have merged. Add a temperature control for the Metropolis rule (283 K up to 10¹³ K), so the reader sees splits start to happen only near Problem 6's 2.8×10¹² K. Add a volume choice (10 or 100 cm³) so the panel matches Fig. 10.2.

**10. Major (390 px). The panel 4 canvas text cannot be read on a phone.** The 600 px canvas is shown 310 px wide, so its 11–12 px labels ("t = … min", "ground: rain is counted here") come out at 5.7–6.2 px, and the 1.2 px blue droplets disappear (`S/panel4_running_probe_390.png`).
*Fix required:* draw the canvas at its displayed size (scaled by devicePixelRatio), or move the time and ground labels outside the canvas into HTML. Keep the dots at least 2 px.

**11. Minor. A section is a question with its answer.** "10.5 Does the cloud maximise entropy?", then "Is the cloud's distribution this one? … the answer is yes". The house rule is no question-and-answer format.
*Fix:* "10.5 The distribution of greatest entropy", and state the result directly.

**12. Minor. Symbols are reused.** σ is surface tension (ch. 10), the eddy speed (ch. 11) and σ_g (ch. 5). ξ is a normal random number in (11.2) and the multiplicity in (11.4), in the same section. ε is the dissipation rate and also the spectrum error in Fig. 10.6.
*Fix:* use γ for surface tension or σ_u for the eddy speed, ζ for the random number, and "spectrum error D" in Fig. 10.6.

**13. Minor. Process talk on the student's page.** The callout bullet "Not yet reviewed. Chapters 10 and 11 … have not yet been read by an independent reviewer" is status, not physics.
*Fix:* remove it once this review is dealt with.

**14. Minor. The well-mixed check misstates its number.** "The scatter of their counts per region is 0.79 times the scatter of pure chance". The 0.79 in `data/cloud.json` (`mix.chi`) is χ² per degree of freedom, a ratio of *variances*. The ratio of scatters (standard deviations) is 0.89.
*Fix:* say "the variance … is 0.79 times", or give 0.89.

**15. Minor. Fig. 10.6 reads backwards, with crowded ticks.** Time runs right to left (N/N₀ falls to the left), and the labels "10⁻⁴ 2×10⁻⁴ 5×10⁻⁴ 0.001 0.002" touch (`S/clean_fig-10-6.png`).
*Fix:* plot against 1 − N/N₀ or against N₀/N on the right-going axis, with one tick per decade.

**16. Minor. Names differ for the same thing.** "gravity's kernel (the cloud)" (Fig. 10.2 legend), "kernel of chapters 1–4" (table, caption), "kernel of chapters 1–4 (one hour)" (panel 5). Also "every pair alike (energy only)" against "(Metropolis)".
*Fix:* one name each, everywhere.

**17. Minor. There is no problem for chapter 11.** Problems 6 and 7 cover chapter 10 only.
*Fix:* add one, for example: "How far does a puff spread in ten minutes at ε = 10⁻³, and does a 150 µm drop survive the 300 m fall below the base?" Both answers follow from (11.2) and (11.3).

**18. Minor. Panel 4 runs too fast to watch.** 45 cloud-minutes pass in about 23 s of wall time (`S/panels.json`: 11 min at 6 s). The first drizzle appears about 1 s after Start.
*Fix:* add a speed choice (real ×30 or ×120), or run at half the current speed.

## Measurements (pointer rule and panels)

- Pointer sweeps (40 positions) over the panel 4 canvas, static or paused: pixel hash of the whole panel unchanged, **0 DOM mutations** (`S/mut.py`).
- Panel 4 running with a pinned probe: readout and probe text change **4 times per second**, the same with or without a pointer sweep (8+8 in 2 s still; 11+11 during a 2.7 s sweep). The marker is redrawn every frame. Click to pin, values in a box below the figure. **Passes the house rule.**
- Pointer sweeps over Figs. 10.1–10.6, 11.1–11.4 and the panel 5 chart: screenshots identical at 1280 and 390 px. No console errors.
- No horizontal page scroll at 390 px. The figures need a sideways swipe at 390 px; a caption hint says so. Smallest figure text after scaling: 9.9–10.3 px.
- Panel 4 probe example: "x = 1025 m, z = 775 m (inside the cloud), mean wind −0.01 / 0.98 m/s, σ = 0.79 m/s, T_L = 21 s, 20 super-droplets, 0.215 g/m³, largest drop 166 µm". End state of one run: 32.9 % rained, 64.3 % evaporated, close to the chapter's 32.6 / 64.4.
- Rechecked and correct: (10.2) and its expansion 1 − ⅔(r/R) + ⅑(r/R)⁴; 5.17×10⁻¹¹ J and 3.04×10⁻¹⁴ J; Lamb's time 0.25 ms; 4.6×10⁻⁵ K; 1.32×10¹⁰ k_B; σ = 0.79 m/s and T_L = 21 s; 126 m in 10 min; 2.6 s and 257 s evaporation; 4×10¹¹ and 4×10⁹ drops per super-droplet; Problem 6 (3.85×10⁻¹¹ J, 2.79×10¹² K); Problem 7's algebra; the chapter 11 table against `data/cloud.json`.

## What works well

- The window-in-the-rain opening of chapter 10 is the mechanism itself: drops merge only on touching, and gravity orders the meals. It is one of the best pictures in the notes.
- 10.1 is a clean, correct result. Surface energy is a Lyapunov function merger by merger, so it holds along every exact Monte Carlo history and not just on average. The check box (20.6 % for equal drops, almost all of the small drop's surface for a big one) is good teaching.
- 10.2 makes irreversibility concrete: e^(−1.32×10¹⁰) for a split.
- 10.5 is honest that maximum entropy depends on the variable chosen (mass versus radius) and calls it "a hypothesis about shape". Problem 7 lets the student prove that the constant kernel keeps the exponential.
- The ledger is a pure observer ("reproduces chapter 5 bit for bit").
- Chapter 11's stochastic element is what Numa said: a mean field plus a random element, with its size and memory taken from ε through Kolmogorov scaling, and Thomson's drift tested by a well-mixed check. Super-droplets are checked against the collection equation (5.807 against 5.873 min).
- The ablation table (eddies off, still air) is the right instinct. Most of the numbers needed for a proper ladder already exist.
- The "What this chapter does not do" callout names the main prices: no condensation, lumping, one cell, the constants.
- Panel 4 obeys the probe rule exactly (measured above). Its readouts are short and plain.
