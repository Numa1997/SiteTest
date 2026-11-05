# Fig. 12 · A Pint of Stout on a Suspension — status (5 November 2026, cart version)

## Done, with evidence
- Glass from the dimensioned drawing (dimensions.com, vector outline) scaled to 160 × 85 mm, with the two sculpted panels of the 2010 glass (photographs): brim 576.2 mL (quadrature) vs 575.3 mL (Blender mesh, 64 sides, polygon factor 0.9984); 568 mL at 158.2 mm, 1.8 mm below the rim, as a brim-measure pint glass should; the photograph profile of the first version was 6 % too big. `tools/fig12/geom.py`, `glass.py`.
- Three-dimensional FEM (27-node hexahedra, curved to the real wall) gated against the exact cylinder: λ11 within 6e-6, kept modes within 1.2e-4, Q11 within 1.5e-6, wall integral within 5e-6; against the 2D solver on the round glass within 1.6e-4. `python3 tools/fig12/check_modes3d.py` → PASS.
- The panels change the frequencies by 0.003 % at 500 mL and 0.1 % at 300 mL: real in the geometry, irrelevant to the slosh. Stated in the note.
- Plant from a Lagrangian: hand assembly = SymPy Hessians exactly; modal row = boundary-value modal equation with tilt and Stokes–Joukowski terms. `python3 tools/fig12/check_plant.py` → PASS.
- Controller: LQR in suspension coordinates; the page's gains = SciPy's to 6e-12; τ_cl identical; bump peaks identical page vs offline (61.13 / 15.01 / 3.76 mm). `node notes/fig12/gate-ctl3.cjs`, `python3 tools/fig12/gate_ctl3.py` → PASS.
- Note numbers: 71/71 match. `python3 tools/fig12/check_note_numbers.py` → PASS.
- Browser (headless Chromium, SwiftShader WebGL), 1440 px: 0 errors, 0 KaTeX errors, no sideways scroll, 44/44 checks, both read-backs find ink, the scripted push works (53 N held, 0 after release), bump ordering passive > skyhook > LQR. `notes/fig12/test.cjs`. Regressions: `notes/fig12/regress.cjs` → PASS.
- Walkthrough: 55/55 quoted lines found. `node notes/walkcheck.cjs`.
- Physics cost 0.05 ms per 1 ms step (5 % of real time on this CPU).

## Findings worth telling Numa
- The pitch frequency of the default cart (3.39 Hz) sits 5 % from the slosh (3.23 Hz): the passive cart is a resonator for the pint. That, not the bump itself, is why it spills.
- The LQR's first design (wheel heights as states) pushed the wheel down on the bump and tilted the glass; in suspension coordinates (deflections) it holds the pint. The marginal mode (road slope) made the Riccati equation unsolvable with ψ as a state.
- The LQR tilts the glass more than the skyhook on the bump (1.4° vs 1.3°) and spills less: it levels the stout, not the body.
- The stout's turn coupling Q_r/Q = 103 mm against Z_s = 144 mm: the liquid is swung 71 % as hard as a frozen block.
- Without the parametric (Faraday) term the offline and page runs differed by 10 %; with it, identical.

## Uncertain values (said on the page)
- Panel depth 2 mm (photographs); head liquid fraction 0.15; dome limit 8 mm; foam friction transfer (factor 3); contact-line rate 0.05 1/s; Guinness surface tension (41–48 mN/m); the cart's numbers are a choice.

## Open at the time of writing
- The production-mesh mode data (`build_modes3d.py`, running) replaces the quick-mesh data; numbers re-checked after the swap. German and Arabic translations; merge with main.
