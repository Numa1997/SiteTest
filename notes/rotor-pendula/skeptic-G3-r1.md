# Rotor Pendula: Gate 3 skeptic review, round 1

Reviewer: blind adversarial reader (did not open notes/rotor-pendula/). Date: 2026-10-23.
I served `public/` on port 8790 and opened `portfolios/rotor-pendula/index.html` in headless Chromium
(Playwright, chromium_headless_shell-1194). I read the lecture notes in full from the rendered frame. The KaTeX
here is HTML only, with no MathML annotations, so I took the TeX from the rendered glyphs and from
`theory/*.src.html` where needed. I used the simulation by hand and by script. I recomputed numbers on my own in
Python (SciPy Radau, written from the equations on the page) and ran every check listed in the source README.

## What I ran

| check | result |
|---|---|
| `python3 tools/check_numbers.py` | PASS: 322 numbers read, 206 computed |
| `python3 -I check_physics.py` | ALL PASS: 17 checks (SymPy derivations, SciPy re-integration to about 1e-8, geared runs to about 2e-5) |
| `node tools/check_sim.js` | PASS: worst 1.3e-8 on Sol's 36 runs; geared load 3.3e-3 %, paid 2.3e-3 %. **This rewrites the tracked `data/sim_check.json`. I restored it with `git checkout`; see minor m9.** |
| `node tools/check_sim_browser.js <scratch>` | ALL PASS at 360/390/1024/1440 (hover text and pixels unchanged, strip at 3.8 to 4 per second) |
| `python3 tools/check_combined.py http://127.0.0.1:8790/...` | ALL PASS (both tabs, 0 KaTeX errors, links switch tabs, sol.html renders, no sideways scroll) |
| My own Playwright probes | layout at 390 and 1440; hover, click-to-pin and readout rate; six simulation solves |
| My own Python (`indep.py`, g = 9.80665) | 20 numbers recomputed from the formulas on the page (see threshold 4) |
| maxon product page 339152 (fetched with curl) | Rc 1.53 Ω, kt 20.8 mN m/A, 460 rpm/V, I0 40.2 mA at 10 900 rpm, J 14.7 g cm², rated torque 30.4 mN m: **all match the notes**. The page also says **"Graphite Brushes"** (see major M3). |
| NREL/TP-500-38060 PDF | could not be fetched (proxy 502). J = 4.38e7 kg m² and the 8.98 rpm kink (871 generator rpm / 97) agree with my knowledge of the report. |

## Verdicts

### 1. Motivated: PASS
Every chapter opens from everyday experience before the model: a Ferris wheel with a bag (0.1, 1.1), a hand-held
spring and honey (2.1), an AC resistor matched to a coil (2.3), a spoon in honey for stiffness (3.1), a hammer
gripped halfway up (3.3), coffee on a bus (4.1), a metronome on a train (5), a springy ruler (6.1), a bicycle
dynamo (7.1), an egg beater (7.2), a box pushed across a floor (7.3), and a bag of shopping on a rope (8.1). Each
step down in detail is justified where it is made. Section 1.3 says why Lagrange and not Newton. Section 2.1 says
why the parametric term is dropped even though it is not small ("multiplying a swing at frequency 1 by sin φ produces
motion at frequencies 0 and 2"). Section 3.1 says why an implicit solver. Section 3.3 explains the double by locking
its hinge. Section 7.3 says why a describing function. Chapter 4 says why it drops the rotor ("To keep it clean").
The weakest spot is chapter 5. It brings in the IEC wind model, a 40-record Monte Carlo and the full NREL controller
with a single picture (the metronome), and never says why ten-minute records and a disc average are the right level
of detail.

### 2. Honest: FAIL
There is a lot to praise. The study withdraws its own claims and says so: "The tuned rod is an idea these notes have
not shown to work". It gives sensitivity runs for the uncertain catalogue friction and efficiency (7.4), and marks
the fast-rotor numbers with † and ‡ and calls them rough. It says "These notes have not measured the three
separately" (3.1). It calls the chaos grid "a sample, not a boundary". It fails on three points where a summary or
a key input is stated more strongly than the evidence:
- **The summaries hedge the tip vibration on one side only (B2).** Section 6.2 says "How strongly, no source we
  could open says for this blade, so the notes take a range: 5, 20 or 100 mm". So none of the three levels has a
  source. Yet 0.2 and 8.2 treat 5–20 mm as the normal case and only 100 mm as "a level no source we found
  confirms". At 100 mm the short pendulum takes 22.8 mW from shaking, against 8.9 mW from gravity. The closing line
  "the disorder adds little" (8.2), and "It hardly helps" (0.2), are not conditioned on this unknown input, which
  spans a factor of 400 in power.
- **The sensor budget leaves out its own exclusions (M2).** "Needs about 37.6 µW" (0.2) is the denominator of
  "127 times" and "47 times". I reproduced the number exactly: 37.584 µW = ADXL362 1.8 µA × 2.0 V, plus the CC2652R
  (7.0 mA TX + 3.39 mA CPU) × 1 ms × 3.0 V, plus 0.94 µA standby × 3.0 V. But Sol's source note
  (`study/sources/README.md`) says the budget leaves out "Radio/CPU startup, receive/retry windows, peripheral power,
  converter leakage and storage losses" and assumes 1000 bits per second. The notes leave all of that out.
- **The brushes are not modelled (M3).** The motor variant cited (339152) has graphite brushes. The load sees peaks
  of only 130 to 553 mV at 0.13 to 0.33 Hz (7.4). A brush contact drop is not modelled. It appears only as "the brushes
  … also need a test".
Smaller over-statements: m3 (0.68 %) and m4 (the sag rule).

### 3. Derived: PASS (with major gaps)
The equations behind the headline numbers are derived on the page, line by line, and I checked them: (1.3), (1.4),
(1.5), (2.1)–(2.6), (3.1)–(3.4), (4.1)–(4.4), (7.1)–(7.8) and (8.1). I also re-derived (2.7) by hand: the
centrifugal potential of the tilted rod gives the stiffness R cos α − sin²α, and the 1-DOF Coriolis term is a
total derivative. I re-derived the 2Ω²w push of 6.1 from the pivot's acceleration and the centrifugal shift. Both
agree with the notes. check_physics.py confirms the rest in SymPy.

Gaps (each major, none fatal):
- The double pendulum's equations are not in the notes, only on the simulation page (section 4 there).
- The coupled blade-and-pendulum model of 6.2 is described in words, but its equations are never written. A reader
  cannot rebuild 0.057, 0.912 or 22.8 mW.
- Chapter 5 does not name the turbulence spectrum or coherence model (Kaimal? Mann?), or how "the average over its
  disc" is formed. So σΩ = 10.3 % cannot be checked.
- The SymPy routes are named, but no script is linked from the page.

### 4. Checked: PASS
Numbers I recomputed on my own (formula, then my value against the page):
- Table 1, P* (2.5): 400 rpm 30 % 57.09 against 57.09; 20 rpm 60 % 14.49 against 14.49; 8 rpm 30 % 28.91 against
  28.91; 8 rpm 90 % 9.57 against 9.57. Γ range 1.44 to 215 ✓, R 2.01 to 301 ✓, G 0.028 to 69.9 ✓, turbine share
  7.21e-5 ✓.
- The full equation, my own Radau integration at κ*: 20 rpm 60 % 14.48 mW (Table 1: 14.48); 400 rpm 30 % 57.09
  (57.09); 8 rpm 30 % 28.61 mW with mean θ −0.128 rad (3.2 says "full model −0.128"; the simulation's worked
  solution 2 says 28.61).
- Trail (3.2), 8 rpm 30 %: −0.1227 rad, 7.03° ✓.
- Tilted hinge (2.7): α = 43.04° and dk/dα = −2.37 per radian (400 rpm 30 %); α = 89.62° and −300.8 (8 rpm 90 %) ✓.
- **Table 4 (chapter 7)** by (7.6)–(7.7) at the tabulated N and RL: 8 rpm 30 % (51, 7.2 Ω) load 7.98 mW and Θ 0.463
  (table 7.98); 20 rpm 90 % (51, 3.0 Ω) 1.80 (table 1.80); 8 rpm 90 % (51, 2.9 Ω) 1.77 (table 1.77); 400 rpm 30 %
  (33, 8.0 Ω) 41.15 (table 41.15). j = 1.001 at 51 ✓, friction 31 % of mgL ✓, jamming at N = 164.2 (three stages)
  and 140.8 (four stages) ✓, csc = 2.82e-4 N m s ✓, c* 0.168 to 1.005 N m s, so 600 to 3600 times csc and N of 25
  to 60 ✓, 0.1387 N m ✓.
- Margins: 9.55 mW / (2 × 37.58 µW) = 127 ✓; 1.79 mW / 37.58 µW = 47.6 ✓; s²/2 = 0.53 % ✓; 6.2 tuned rod
  L = 1.11 m and G/2R = 9.6 % ✓; 8.1's π/(4√2) = 0.555 ✓.
- **Simulation against the notes:** default 20 rpm 30 % gives 29.28 mW (Table 1: 29.28). 14 rpm 60 % double gives
  10.59 mW (Table 1: 10.59). 400 rpm 30 % gives 57.09 (57.09). 8 rpm 90 % with the RE 25 + GP 32 C at 51 : 1 and
  RL best (2.95 Ω) gives a load of 1.786 mW and a rotor bill of 8.694 mW, friction 38.8 % (Table 4: 1.79, 8.69;
  text "33 to 39 %"). The swing differs a little, 0.148 rad in the simulation against 0.151 in Table 4 (m6).
- The chapter 4 Monte Carlo log (`data/mc_full.log`) matches the quoted 0.22 to 0.65 %.
- Not reproduced: 6.1's "sag only" figures do not follow from the rule the text gives (m4).

### 5. Sourced: FAIL
The notes have **no reference list and no external link** at all. The only links are to the simulation and to Sol's
`report.pdf`.
- **Turbine.** "Jonkman, Butterfield, Musial and Scott 2009, NREL/TP-500-38060", with Table 9-1 for 1.0793 Hz. A
  reader can find this, but there is no URL. "Cp(λ) from NREL's published table" and "the NREL blade's mass and
  stiffness tables" name no table or file.
- **Motor.** "maxon RE 25 … catalogue part 339152". I confirmed this is openable and every value matches. But the
  catalogue year and page are missing; the source script records "RE 25 page 153 / GP 32 C pages 430-431", but the
  page does not show them.
- **Gearhead.** "GP 32 C" with efficiencies 80/75/70/60 %, 0.7 to 1.5 g cm², 1° backlash and 8000 rpm, but no part
  number, page or link.
- **Wind standard.** "IEC 61400-1, turbulence class A", with no edition (σ1 = 0.16 (0.75 v + 5.6) is the NTM of
  edition 3). It is paywalled and no open secondary source is given.
- **Sensor.** "ADXL362" and "CC2652R … typical currents of the two datasheets". No revision, page, current value or
  URL is given. They exist in `study/sources/README.md` (ADXL362 Rev. G pp. 4–5; SWRS207J §8.5–8.6, with URLs and
  SHA-256), but the notes do not point there.
- **Blade vibration level.** Unsourced, and admitted to be.

### 6. Readable: FAIL
The prose is clear and plain, and terms are defined on first use: the Lyapunov exponent, Radau IIA, the Dirac delta,
the describing function, backlash, tip-speed ratio and back-EMF. Neither tab scrolls sideways at 390 or 1440
(measured scrollWidth = clientWidth in the shell and in both frames). It fails on what a phone reader actually sees,
and on a thin set of pictures:
- **The figure labels are unreadable at 390 px (B3).** The SVG text boxes measure 8–9 px high, about a 6 px font,
  against 14–16 px at 1440. Figure 1's θ, rp, L, "centrifugal Ω²r" and "gravity g", and Figure 3's α and hinge
  labels, cannot be read. In Figure 3, "bob at rest" overprints "outward pull" at both widths.
- **Too few figures (M5).** There are 3 figures for 29 equations and nine chapters. There is no drawing of the
  double pendulum's q1 and q2 (3.3), of the bending blade with its turning stator (6.1, the subtlest argument in
  the notes), of the gear train and circuit (7.1–7.2), or of the stick–slip swing (7.4).
- **Wide tables at 390 px.** Tables 1 and 4 (766 and 797 px) scroll inside a 290 px box. The first column (the
  mounting) is not sticky, so after scrolling the reader loses which row is which, and nothing hints that the table
  scrolls (m1). Four display equations also scroll in their boxes; (4.3) is 421 px in 302.
- **Undefined in 6.2:** "modal mass", "rms", "spectrum … flat near 1.08 Hz", "first edgewise mode".
- **A duplicated sentence at the end of 4.2** (m2).

### Interaction rule on the simulation: PASS
- With playback paused, I swept the pointer across the scene and all three plots, with Read values off and then on
  (no click). Canvas pixels were unchanged and there were 0 DOM mutations. With playback running, the DOM mutation
  rate was the same with and without a sweep (66.7 and 66.4 per second, all from playback), and the readout
  changed at 4.0 and 3.87 per second.
- Read values is a toggle (aria-pressed). A click pins a point: "pinned turn 1.546 (rotor angle 196°) · θ = 0.1668
  rad · p = 12.26 mW". The values appear in the strip `#readout` under the plots, outside every figure. While
  playing, the strip text changed 24 times in 6 s, with a median gap of 250 ms and the shortest 237 ms. The θ plot
  redraws 61 times per second (marker every frame). Clicking the κ plot pins "κ = 30.54 = 0.781 κ* · small-swing
  power 28.48 mW". Switching Read values off clears the pin.
- The cursor is a crosshair over the plots, a static style that is not a reaction.

## Problems, ranked

### Blocking
- **B1. No sources a reader can open (Sourced).** Location: the whole notes; 0.2, 0.3, 5, 6.1, 6.2, 7.1, 7.2.
  Fix: add a numbered reference list at the end of the notes, with a URL and the table or page for each item: the
  NREL/TP-500-38060 PDF (Table 9-1; the Cp(λ) table actually used, with its file or table name; the blade
  structural table); the maxon catalogue edition with RE 25 p. 153 and the product page for 339152; the GP 32 C
  part numbers for 14/33/51/111/190 : 1 and catalogue pp. 430–431; IEC 61400-1 edition 3 (2005) clause 6.3.1.3 plus
  an open secondary source for the NTM and the spectrum used; ADXL362 Rev. G pp. 4–5 and CC2652R SWRS207J §8.5–8.6
  with their URLs, and the current values themselves. Or link `study/sources/README.md`. Cite each where it is used.
- **B2. The summaries over-state "the disorder adds little" (Honest).** Location: 0.2 ("It hardly helps … a level no
  source we found confirms") and 8.2 (third bullet and the last paragraph). Fix: say that no tip-vibration level is
  sourced, that 5, 20 and 100 mm are assumptions, and that the shaking's share runs from 0.6 % to 260 % of gravity's
  harvest across that range. Make the closing sentence conditional ("unless the blade vibrates at tens of mm rms, which
  no source we found gives either way").
- **B3. Figure labels unreadable at 390 px (Readable).** Location: Figures 1 and 3 (and Figure 2's axis labels).
  Fix: set the SVG text in CSS px so it does not scale below about 12 px, or give phone widths a separate viewBox
  with larger labels. Move "outward pull" in Figure 3 off "bob at rest".

### Major
- **M1. The chapter 5 wind model is not named or checkable (Derived).** Fix: state the spectrum (Kaimal per IEC
  61400-1 Annex B, or Mann), the length scale, the coherence or disc-averaging method, the record length and the seed
  handling, and give the single equation that turns the wind into Ω(t).
- **M2. The sensor budget's exclusions are not stated (Honest).** Location: 0.2 and the 47× and 127× margins. Fix: one
  sentence listing what the 37.6 µW leaves out (radio and CPU start-up, receive and ACK windows, peripherals,
  converter leakage, storage) and the 1000-bit-per-second assumption, plus an estimate of how much these could add.
- **M3. Graphite-brush contact drop at 0.13–0.55 V is not modelled (Honest/Checked).** Location: 7.1 and 7.4. The
  cited variant 339152 has graphite brushes. For small currents, a brush contact drop (nonlinear and not in the
  1.53 Ω) is likely a substantial part of a few hundred mV. Fix: either pick a precious-metal-brush RE 25 variant and
  redo Table 4, or model a brush drop of 0.1 to 0.3 V and show the load power. At minimum, flag it beside the
  1.8–9.0 mW headline in 0.2 and 8.2.
- **M4. The 6.2 model equations and the double pendulum's equations are missing from the notes (Derived).** Fix:
  write the two-DOF linear system (modal oscillator plus pendulum, with the coupling terms 0.82 and 27.8 mrad/m), the
  formula for mean power from the transfer function, and the double's two equations (copy them from the simulation
  page's section 4), each with a numbered equation.
- **M5. Too few figures (Readable).** Fix: add at least a double-pendulum geometry figure (3.3), a bending-blade
  figure showing the pivot's sideways move w and the stator's turn β (6.1), a gear-train and circuit figure (7.1–7.2),
  and a θ(φ) plot showing the friction stops (7.4). The simulation's plots could be reused as static figures.

### Minor
- **m1.** Tables 1 and 4 at 390 px: make the first column `position: sticky; left: 0`, and add a fade or "scroll →"
  cue. Or split Table 4 into "setting" and "power" halves on phones.
- **m2.** 4.2, last paragraph: "These notes give no value of S for a real blade, because a real blade does not shake
  as white noise. A real blade, though, does not shake as white noise: …". The same clause appears twice; delete the
  first sentence's reason or the second's opening.
- **m3.** 2.4: "The closed form (2.5) is within 0.68 % of the full model everywhere". At the two ¹ mountings this
  compares with the full model at Sol's searched brake. At κ* itself, 8 rpm 30 % gives 28.61 against 28.91 (1.0 %;
  the simulation's worked solution 2 shows 28.61). The notes give "28.72–29.28" for the large rotors; the simulation
  gives "28.61 to 29.28". Fix: say "within 0.68 % at Sol's brake settings, 1.0 % at κ*", and use one range in both
  tabs.
- **m4.** 6.1: "the pivot's motion adds 2Ω²w to gravity's push … 1.0 %, 6.0 % and 14.5 %". With w = 31.5, 165.3 and
  384.4 mm (`data/L3_sag.json`) and Ω = 0.9494 rad/s, (1 + 2Ω²w/g)² − 1 gives 1.16 %, 6.17 % and 14.63 %. Something
  else enters the model (perhaps a slope term). Also name the rotor speed used in chapter 6 (9.07 rpm?). Fix: give
  the full push expression, or quote the numbers that follow from the stated rule.
- **m5.** 7.2–7.4: Coulomb friction with static equal to kinetic. With the rod stopped for 25 to 29 % of each turn,
  breakaway (static) friction of the backdriven gearhead would lengthen the stops. Add it to the list of things the
  bench test must measure.
- **m6.** Table 4's swing at 8 rpm 90 % is 0.151 rad. The simulation at the same setting (51 : 1, RL 2.95 Ω) shows
  0.148 rad, while its load (1.786 mW) and bill (8.694 mW) match. Say whether the two use different step counts
  (2000 against 1200 per turn) or definitions.
- **m7.** Simulation page, section 5: "(version 3 of the derivations)"; section 6: "exactly as the Python engine of
  the notes", "tools/check_sim.js", "L4_check_2000.json". These are workshop references that mean nothing to a
  reader. Fix: rewrite in reader terms, or link the scripts.
- **m8.** The notes' body text is set in IBM Plex Sans. The house rule (CLAUDE.md) says lecture notes are set like
  a LaTeX document in Latin Modern. Either follow it or record the exception.
- **m9.** Reproducibility: the committed `data/sim_check.json` has `"geared": null` and `chk_geared_sentence: "."`,
  but the served `rotor_sim.html` contains the geared-check sentence ("3.3·10⁻³ %"). Rebuilding from the committed
  data would silently drop that sentence. Running `node tools/check_sim.js` (a README "check") rewrites the tracked
  file. Fix: commit the current `sim_check.json`, and note in the README that this check writes it.
- **m10.** 6.2: define "modal mass", "rms" and "a spectrum flat near 1.08 Hz" in a clause each, for the school
  readers the opening promises.
- **m11.** 0.2: the ADXL362 is budgeted at 2.0 V and the CC2652R at 3.0 V. On a single 3.0 V rail the accelerometer
  draws slightly more. Say which rail is assumed.

## Answers (23 October 2026)

- B1 Sourced: section 8.3 "Sources" lists every outside source with a link a reader can open (Sol's report and his sources
  file with the datasheets, Jonkman et al. 2009, the OpenFAST blade file, the ROSCO C_p table, the TurbSim guide for IEC
  61400-1, the maxon motor and gearhead pages, the ADXL362 and CC2652R datasheets).
- B2 Honest: §0.2 and §8.2 now say that whether the blade's shaking helps depends on a shaking level no source states; at
  100 mm it gives more than gravity. The last sentence of §8.2 carries the same condition.
- B3 Readable: each figure sits in a scroll box with a minimum width of 520 px on phones, so its labels stay at their size;
  the overlapping label of Figure 3 moved. No sideways scroll of the page at 360 and 390 px; check_combined.py ALL PASS.
- M1: chapter 5 names the Kaimal spectrum, the IEC coherence and the disc average (TurbSim guide). M2: §0.2 says what the
  sensor budget leaves out. M3: §7.4 names the brushes' contact voltage drop as unmodelled.
- Open: M4 (the equations of the §6.2 shaking model and of the double pendulum are described and named, not printed),
  M5 (more figures).
