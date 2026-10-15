# Minor issues · verification report

Batch A was reproduced locally, deployed once, then checked live. Stored version: `1792048596599`.
Viewport checks: 1440 × 900 and 390 × 844; the hidden-layer case also uses 960 × 900.
Commit: `:/^Batch A: fix simulation and recording faults; verify in Chromium$`.
This is Git’s unique-subject revision syntax; it avoids putting a commit’s own hash inside its contents.

| Issue | Status | Proof |
|---|---|---|
| A1 · stale fringe orders | fixed | b = 40 px, λ = 20 px: sin θ₁ = 0.5, θ₁ = 30°, m = 1 label present. |
| A2 · hidden water layers | fixed | Five layers stored, three drawn at 960 × 900; final depth 2.24 m; checked parcel values identical. |
| A3 · empty-bench arrays | fixed | No waves: y_sum = 0, py_sum = mid1 and X spans 0–800. |
| A4 · exact wave repeat | fixed | ν = (1, 0.9975) Hz gives the 20 s cap, previously 1 s. |
| A5 · recording at Speed 0 | fixed | Start is refused with a reason; an active round waits explicitly and completes after Speed is raised. |
| A6 · twin locator | fixed | Four coordinates equal recomputation; pixels are rgb(226, 162, 170), with alpha checked first. |
| A7 · saved turbine target | fixed | All 27 target settings from 8 to 21 turns per minute recompute identically from the stored input. |
| A8 · archive README filenames | fixed | Both READMEs name the actual downloads; CRC and NumPy shape checks pass. |
| A9 · final sample | fixed | At 60 Hz: 600 samples from 601 frames, ending at 10.000000000000776 s; previously 9.983333333334107 s. |
| A10 · transverse endpoint | fixed | The drawing path has 215 points and ends at X = 640 with zero horizontal gap. |

The remaining batches are in progress. Numa’s decision items remain unchanged.


| Issue | Status | Proof |
|---|---|---|
| B1: oscillator log-axis labels | fixed | Ratios 0.1, 0.32, 1, 3.2, 10; endpoint gains 1.01005 and 0.0101005. |
| B2: turbine subscripts | fixed | Four SVG subscript spans render p / opt without underscores. |
| B3: wave-source grid counts | fixed | 1280, 1440, 1600 px: 360 × 162 = 58 320; 390 px: 324 × 324 = 104 976. |
| B4: inaccurate note numbers | fixed | Signed drift −2.416 × 10⁻⁸; 46-step upper bound; 4–17 px bob clamp; slit gap ≤1.4 × 10⁻¹³ px and plot width 500; water widths 800/400; spectrum 0–6 Hz; phase 25.346°; solver 9.5–12.4 ms; measured layout fractions; turbine K 0.5, airflow 5 px/m, dashes 16/22 px. |
| B5: phasor SVG clipping | fixed | Four unique active clip paths; phone image identical, desktop changes only 28 edge pixels. |
| B6: obsolete thumbnail | fixed | New 800 × 500 WebP from the current stage at device scale 2; current TeX axes and scale visible. |
| B7: portfolio image ratios | fixed | Attribute ratios exactly match all four SVG viewBoxes. |
| B8: layout gaps | fixed | 970 px home margin 104 → 48 px; empty catalog margin 28 → 0 px and display none. |

Proposed replacement for the stale CLAUDE.md sentence (file unchanged): “In a 1280–1600 px desktop window, Fig. 1 computes a 360 × 162 = 58 320-point grid; on a 390 px phone it computes 324 × 324 = 104 976 points. At λ = 16 field px these give 7.2 and 6.48 samples per wavelength. Rebuilding Line of 16 on desktop uses 1 866 240 sine and cosine calls.”


| Issue | Status | Proof |
|---|---|---|
| C: transverse, water, bench and turbine excerpts | fixed | Complete quoted lines match source; omitted water caption is marked with an ellipsis. |
| C: pendulum equation references | fixed | References now point to equations (6)–(8). |
| C: phasor sampling and multiplier names | fixed | Every-sample scan documented; multiplier named live[i].mul. |
| C: effective morph alpha | fixed | Smoothing off: stored alpha 1, Now 0.08 → 1.00 at both sizes. |
| C: DFT completeness | fixed | 120 coefficients of 256; K = 120 heart error 0.000491411444. |
| C: damping notation | fixed | γ is the slider; g = γ/R is attenuation per pixel. |
| C: Fourier c_max, L, step and local ds | fixed | Rank-0 maximum labelled correctly; storage site documented; renamed arcDistances leaves all sample/coefficient arrays byte-identical. |
| C: pendulum updates, phasor ang and water frames metadata | fixed | Once-per-frame diagnostics, current draw-loop angle calculation, and playing-only frame count documented. |
| C: scalar types and panel contract | fixed | uint8 and all four omitted contract keys documented. |
| C: catalog extension comment | fixed | New course years explicitly require STAGES, validation and wording updates. |
