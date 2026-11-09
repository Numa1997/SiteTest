# Requests for shared files (from session S4, chapter 2, branch eb/ch02)

Written 9 November 2026. S4 edits none of these files; each line is something the owner may want.

1. **`physics/core.js` (scaffold).** `physics/ch02.js` carries its own CODATA 2018 constants (`K`) because core.js had not landed (no `eb/scaffold`
   branch existed when S4 worked). When core.js exists, `K` should be read from it; the names used are e, h, hbar, me, eps0, kB, u, c.
2. **Module format.** The repository is `"type": "module"`, so a `.js` file is ESM in Node. `physics/ch02.js` is a classic UMD file: it sets
   `module.exports` under CommonJS and `globalThis.EB_CH02` otherwise (Node: `await import(path)` then `globalThis.EB_CH02`; page: `<script>`).
   If the scaffold prefers `.cjs` copies (as `portfolios-src/impact/physics.cjs` does) or ES exports, say so; the file is pure.
3. **A slot for the interactive code.** The browser part of the figure (canvases, controls) is `physics/ch02_ui.js` (S4's file, same pattern);
   the markup and style are strings in `text/ch02.py` (`sim_html`, `SIM_CSS`). `build()` returns `{html, css, ui_js, physics_js, numbers}`.
   The scaffold's template needs: the site stylesheets (`styles/sim.css` brings paper.css and KaTeX css), the chapter `css` in a `<style>`,
   `physics_js` then `ui_js` as scripts, and maths typeset at build time (`\( \)` and `\[ \]` with `\tag{2.n}`; `notes/electron-beam/ch02/render_math.cjs` shows how, with the site's KaTeX 0.16.11).
4. **Data panel.** The figure writes every number into `window.EB_CH02_STORE` (groups `inputs`, `apex`, `handover`, `timeline`; each entry `{value, unit, how}`)
   at the line that computes it and only reads from it for display. It does not use `Sim.dataset()`; the coordinator may map the store to `scripts/dataset.js`
   (docs/scripts/dataset.md). The three-way proof (stored value, formula recomputed, pixel) is done only for the first two so far
   (`notes/electron-beam/ch02/check_browser.cjs`: the store against the NumPy reference, canvases tested for drawn pixels with alpha first).
5. **Contract names.** contract.json was not available. Chapter 2 returns `handover()` = `{I_e (A), B_r (A m^-2 sr^-1 V^-1), dE (J) and dE_eV, d_v (m), F0, f, J0, meanEt_eV, regime}`.
   If contract.json fixes other names, a rename in `handover()` of both implementations is the whole change.
6. **Checks harness.** The scaffold's `check_numbers` was not available. Every number in the text is produced by `ref/ch02.py` or `derive/ch02.py` through `text/ch02.py`
   (unresolved tokens raise), but a text-versus-computation check in the scaffold's format has not been run.
7. **Registration (coordinator).** Nothing was added to `public/portfolios.html`, `docs/`, `tools/inventory.py`, redirects or i18n tables.
8. **Librarian.** `data/ch02/` was written by S4 because `eb/librarian` did not exist: `ayari2023_w111_iv.csv`, its README with provenance and licence, and `derive_results.json` (output of `derive/ch02.py`).
   Dyke & Trolan 1953 (the classical data set) was not obtainable; a librarian with access could add its Fig. 2 (emitter X89) and the chapter could overlay it.


## From S3 (branch eb/ch01): contract change for chapter 1, and two remarks

1. **contract.json, stage ch01 (needed for the chapter to build).** The stage as proposed (E, B, v_0, theta_0, dt, integrator in; r_g,
   omega_c, energy_drift, trajectory out) is the right physics: one electron in uniform E (+y) and B (+z). A quoted number must be a
   scalar module output, so the chapter needs a run time and the end of the path: new input `t_run`; new outputs `x_end`, `y_end`,
   `z_end`, `theta_end`. Ready patch: `notes/electron-beam/ch01/contract-ch01.patch` (`git apply` it to portfolios-src/electron-beam/contract.json).
   I tested everything with it applied locally and did not commit contract.json. Without it `build.py` stops with a contract disagreement.
2. **contract.json, symbol d_opt (ch00).** Its meaning says "smallest half-pitch light can resolve, lambda/(2 NA)". Abbe's lambda/(2 NA) is the
   smallest *period* (pitch); the half-pitch is lambda/(4 NA) (derived in chapter 0). Please reword "half-pitch" to "period". The number is unchanged.
3. **Live integrator figure.** The generic simulation slot takes one module per chapter. Chapter 1's second live figure (Boris and RK4 error
   against the exact helix, log-log) is therefore a static picture drawn from ref/ch01.py; a second slot per chapter would make it live.
4. **tools/inventory.py** needs rules for `notes/electron-beam/ch01/check_thomson_vs_librarian.py` and `notes/electron-beam/ch01/contract-ch01.patch` (`--check` reports them undescribed), and for `docs/files.md` to be regenerated.
