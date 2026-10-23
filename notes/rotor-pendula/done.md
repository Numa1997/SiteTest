# Rotor Pendula: definition of done

Rewritten on 23 October 2026 from section 3 of the brief "Rotor Pendula: chaos against chaotic wind" (`brief.md`), which replaces
the earlier brief "enhance the two portfolios". Every item of the earlier version is kept; none is weakened. Only Numa may change
this file.

- [ ] 1. The study lives as source in `portfolios-src/rotor-pendula/` (model, pages, theory sources, build script, checks, README).
      The served copy `public/portfolios/rotor-pendula/` is generated from it by the build script, never edited by hand, at the
      same address (`portfolios/rotor-pendula/index.html`). Sol's report (word for word) and his delivery (`study/`) are kept.
      The old bundle stays served until the new one passes every gate.
- [ ] 2. Sol's headline numbers are reproduced by the new model, or the change is explained on the page: the linear optimum
      κ = |R − 1| with P* = M L g² / (4 Ω |r_p − L|); the 18 mountings giving 9.55–57.1 mW; the double-to-single ratio
      0.64–0.74 at equal mass and reach; the rotor's share ≤ 7.2 × 10⁻⁵.
- [ ] 3. Complexity ladder L0–L4: every level has `contract-L<k>.md` that passed Gate 1 (blind skeptic, every objection answered
      inside the contract) and `check-L<k>.md` from Gate 2 with no "wrong" row left. Each level adds one physical effect,
      justified by a computed dimensionless number, and the page shows how much it changes the observable. No level is skipped;
      a level below the observables' uncertainty stays as a stated check.
- [ ] 4. Gate 3: the blind skeptic's final report on the rendered pages passes all six thresholds of physics-model-loop 7.3
      (motivated, honest, derived, checked, sourced, readable).
- [ ] 5. The number script finds every number quoted in the text computed by the model: PASS.
- [ ] 6. Independent physics checks (constants retyped, not imported; SymPy derivations, SciPy re-integration): PASS.
- [ ] 7. Browser check at 360, 390, 1024 and 1440 px: 0 KaTeX errors, 0 page errors, no sideways scroll; screenshots shown.
- [ ] 8. `public/portfolios.html` (the `rotor-pendula` article only), `docs/portfolios.md` (rotor parts only) and the other docs
      that describe the changed files say what the code now does; `python3 tools/inventory.py --check` passes.
- [ ] 9. Committed and pushed to the session branch `claude/dazzling-heisenberg-esnqek`; a pull request into `main` is open and
      NOT merged.
