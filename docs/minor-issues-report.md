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
