# Status of the ten notes

Updated by the lead after every agent returns. Rule in force: judge first, change only what needs it (notes/STANDARD.md,
"Numa's verdicts").

| Fig. | Page | Teacher | Sections judged clear / needing work | Check | Referee | Walk | Rounds | Open |
|---|---|---|---|---|---|---|---|---|
| 1 | Circular Wave Interference Visualization.html | running | | | | | 0 | |
| 2 | Double Pendulum.html | running | | | | | 0 | |
| 3 | Interactive Double-Slit Experiment Visualization.html | done; 6 repairs, lead accepted all | 7 clear / 4 needing work (§5 θ undefined and cross term unwritten, §7 closed-slit claim and "animation", §10 polarisation, references) | running | running | running | 1 | known: "Animate wavelets" ticked while clock may start paused |
| 4 | Transverse and longitudinal waves.html | done; 8 repairs, lead accepted all | 4 clear / 6 needing work (A_L before definition, Ex. 3.1 false for lower row, B = γp and K + 4G/3 asserted, ρ 1.2041 → 1.2043, 26 % span asserted, tilt energy asserted, 214 → 215 points, references) | running | running | running | 1 | known: tl.js:85 mark in note; redraw while paused |
| 5 | water-wave.html | done; 4 repairs, lead accepted all | 8 clear / 4 needing work (§02 symbols before definition, §05 c_g asserted, §08 "stored" claim, references) | running | running | running | 1 | code: `cg` stored as c/2 with dispersion off (L663), report only |
| 6 | wave-interference.html | done; 4 repairs, lead accepted all | 6 clear / 4 needing work (§3 sign of the second derivative, §4.1 group velocity "narrow envelope", §6 string energy asserted, references) | running | running | running | 1 | Phase slider stops at 6.25 (note says "about 2π") |
| 7 | phasor-sums.html | done; 5 repairs, lead accepted all | 7 clear / 4 needing work (§5 gcd defined after unrelated text, §6 readout position, §8 dot size and Record timing, references) | running | running | running | 1 | known: replay does not wrap phases (L1205); new: Record snapshots 58 ms apart, not 50 (L1189) |
| 8 | draw-decompose.html | done; 6 repairs, lead accepted all | 6 clear / 5 needing work (§2 pointer, §4.1 inverse DFT step, Fig. 3 caption, §6.1 corner reason and a rounding slip, references) | running | running | running | 1 | design choice in `resamp()` (closed shapes sample the start point twice), report only |
| 9 | driven-oscillator.html | done; 8 repairs, lead accepted all | 4 clear / 7 needing work (§3.1 complex division, §3.2 roots and constants, §4 Ω_r derived as (6a), §5 pole sign, Ex. 6.1 wrong, §7 mean power step, §9 window chart, references) | queued | queued | queued | 1 | known: redraw while paused; new: time-tick label can overlap "t (s)" (L783); page +3 lines, 5 links in docs/scripts shifted by the lead |
| 10 | wind-turbine.html | done; ~16 repairs, lead accepted all | 2 clear / 9 needing work (ω, R, ρ undefined; Betz Bernoulli step; λ-only argument; ω*, τ0, PI step; "without ringing" false; Δv; share numbers; RK4 step error; P_aero curve unnamed; references) | queued | queued | queued | 1 | known: redraw while paused; new: Play after 120 s does nothing (L962); walkthrough step 4 still says "without ringing" |

Baseline before any change (20 October 2026, headless Chromium, 1440 × 900 and 390 × 844, all folds open): all ten pages
0 console errors, 0 KaTeX errors, 0 px sideways scroll; 37 references in all, none with a link.
