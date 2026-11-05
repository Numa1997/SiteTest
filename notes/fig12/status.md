# Fig. 12 · A Pint of Stout, Carried — status (5 November 2026)

## Done, with evidence
- Glass geometry from a photograph, rebuilt in Blender 5.2.3 (bpy): brim 603.7 mL (integral) vs 603.3 mL (Blender mesh, 96 sides, factor 0.99929); 568 mL at 151.9 mm, 8.1 mm below the rim; widest 84.1 mm vs published 85 mm. `tools/fig12/glass.py`.
- FEM mode solver gated against the exact cylinder: 9 eigenvalues within 2.4e-4 (λ11 within 3e-7); Q equals 2R/((ξ²−1)J1(ξ)) = 0.057528 m; damping integrals equal Wolfram's exact Bessel integrals to 7e-5. `python3 tools/fig12/check_cylinder.py` → PASS.
- Wolfram Language: ξ11 = 1.841183781, β = 0.05752775 m, f1 = 3.3816 Hz for R = 40 mm, h = 99.5 mm (the brief's 3.382 Hz confirmed).
- Live RK4 gated against SciPy DOP853: 5e-8 (sideways resonance) and 7e-7 (Faraday) of the largest amplitude. `notes/fig12/gate.cjs` + `tools/fig12/check_dynamics.py` → PASS.
- Note numbers: 53/53 quoted numbers match the computation. `tools/fig12/check_note_numbers.py` → PASS.
- Browser (headless Chromium, SwiftShader WebGL), 1440 and 390 px: 0 page errors, 0 KaTeX errors, no sideways scroll, 38/38 data-panel checks identical (English, German, Arabic), both read-backs find ink, scripted drag moves the glass. `notes/fig12/test.cjs`.
- Walkthrough: 38/38 quoted lines found. `node notes/walkcheck.cjs`.
- Phone cost: physics 0.3 ms per frame at 4× CPU slowdown; the page's own JS is a few percent of the frame (the rest is software WebGL in headless Chromium).

## Findings worth telling Numa
- The brief's β, f1 = 3.382 Hz and the modal equation are right (two routes each).
- The brief's "bulk damping negligible" is right only for the slowest mode: 2 % of its damping, growing as λ² for higher modes.
- The NASA empirical decrement 4.98 ν^½ a^−¾ g^−¼ is 1.42 × the clean-wall theory (3.50): real tanks lose more than clean walls, as Miles 1967 reports.
- The head is the largest damping term (47 % of the slowest mode's damping); the pint settles to 5 % in 6.0 s with the head, 11.1 s without.
- The tulip's inward-leaning wall above its widest point raises f1 against a straight glass (3.37 vs 3.30 Hz at 590 mL); below it, the outward lean lowers it (3.14 vs 3.25 Hz at 300 mL).

## Uncertain values (said on the page)
- Head liquid fraction 0.15 (no source); foam friction transferred from Sauret et al.'s slot to a round glass (factor 3); contact-line rate 0.05 1/s; Guinness surface tension (beers 41–48 mN/m).

## Second version (5 November 2026, later): two review loops and the waiter
- Two rounds of referee and code review, one review of the waiter; every finding fixed or answered (`referee-r*.md`, `code-review-r*.md`, `waiter-review.md`). `node notes/fig12/regress.cjs` → PASS.
- The waiter (note section 10): LQR gains equal SciPy's to 3e-10; a 20 cm carry peaks at 2.6 mm at the wall (8.0 mm by hand on the same path), arrives in 1.45 s; it calms an existing 5 mm slosh tenfold in 1.0 s against 4.6 s with the glass held still. `node notes/fig12/gate-waiter.cjs` → as offline.
- A jerk-free (third-order) path alone, with no feedback, already holds the slosh to 2.3 mm: the planning does half the work; the feedback is what calms a slosh that is already there.
- German and Arabic updated (181 pieces each), with four English fixes the translators found (Figure 4 "nearest" tie, the 60 cm × 6 cm tank, the hand hint contradicting section 6, the unexplained 46.02 in Example 4.1), and one Arabic bidi fix in the live readout.
