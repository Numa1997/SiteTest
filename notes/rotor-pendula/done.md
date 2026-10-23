# Rotor Pendula: definition of done

Written once on 23 October 2026 from the brief "enhance the two portfolios (droplets and wind turbines)" and the skill
physics-model-loop. Only Numa may change it.

- [ ] 1. The study lives as source in `portfolios-src/rotor-pendula/` (model, pages, theory sources, build script, checks, README), and the
      served copy `public/portfolios/rotor-pendula/` is generated from it by the build script, never edited by hand. The address of
      the served copy does not change.
- [ ] 2. Nothing correct in the old version (`notes/rotor-pendula/baseline/`, recovered from the deployed bundle) is lost: each of its
      headline numbers is reproduced by the new model, or the change is explained on the page.
- [ ] 3. Complexity ladder: every level k has `contract-L<k>.md` that passed Gate 1 (blind skeptic, every objection answered in
      the contract) and `check-L<k>.md` from Gate 2 with no "wrong" row left. Each level adds one physical effect, justified by a
      computed dimensionless number, and the page shows how much it changes the observable.
- [ ] 4. Gate 3: the blind skeptic's final report on the rendered pages passes all six thresholds (motivated, honest, derived,
      checked, sourced, readable).
- [ ] 5. A number script finds every number quoted in the text computed by the model: PASS.
- [ ] 6. Independent physics checks (constants retyped, not imported; SymPy/SciPy or Wolfram): PASS.
- [ ] 7. Browser check at 360, 390, 1024 and 1440 px: 0 KaTeX errors, 0 page errors, no sideways scroll; screenshots shown.
- [ ] 8. `public/portfolios.html`, `docs/portfolios.md` and the other docs describe the new version; `python3 tools/inventory.py --check` passes.
- [ ] 9. Committed and pushed to `claude/awesome-ritchie-qiy1zo`; a pull request into `main` is open and NOT merged.
