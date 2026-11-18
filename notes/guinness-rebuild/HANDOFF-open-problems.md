# Handoff: the open problems of the Guinness rebuild (Fig. 12 and Fig. 16)

Written 18 November 2026 by the rebuild chat (session_01DGmqimP4q3W5e6LtQwSTNe) for a new session that closes them.
Read first: `CLAUDE.md`, `AGENTS.md`, `notes/STANDARD.md`, `notes/guinness-rebuild/STATE.md`, `notes/guinness-rebuild/audit.md`
(items A-M), `notes/fig16/STATE.md` (section "Session finished"), `docs/simulations/fig16-guinness-cart-control.md`,
`docs/simulations/fig12-beer-slosh.md`, `docs/kaggle-pipeline.md`.

## The owner's binding rules (verbatim where quoted)
- 15 Nov 2026: "No referee or checker. No tests to be run. Read the code and validate it by reading, not by running anything.
  Any tests that you run, you run on my Kaggle. Absolutely nothing in your environment anymore, zero."
  So in the container: read, edit, git, curl downloads, Kaggle MCP calls. No python, node, npm, browsers, agents.
  Packing, builds, browser checks run in a Kaggle notebook (CPU unless a GPU is needed); download outputs, commit them.
- "No need to ask for permissions ... they are granted." Compute on Kaggle without asking; report the GPU bill.
- 18 Nov (via the inventory session): no new runs beyond what finishing needs; if a further GPU run is needed, state it to the
  owner in one line with its cost before starting it.
- CLAUDE.md: finished, tested work is merged to main and published without asking (Cloudflare deploys main); verify live.
  Never touch the Cloudflare Workers, R2, public/de/, public/ar/, scripts/i18n/, *.rtl.css. No model names in commits.
- Owner: BSc physics; metric units; define terms; Fact (with handle) / Inference / Opinion; mechanism in one line; short turns;
  end each turn with "Where we are:" and "Next, if you say yes:".

## How Kaggle work is done here (proven pattern)
- GPU notebook `numakoudsie/fig-16-guinness-cart-with-control` (Fig. 16), `numakoudsie/guinness-on-a-cart-stout-in-jax` (Fig. 12).
- CPU notebook `numakoudsie/fig-16-cart-diagnostics-cpu` (latest version 8): a script that fetches the repository at a pinned commit
  (codeload tarball) and runs a tool, e.g. `tools/fig16/kaggle/publish16.py` (env COMMIT, RUN_VERSION, RIDES, DATE, SRC_URLS).
  Save with `save_notebook` (kernelType script, enableInternet true, SaveAndRunAll), poll `get_notebook_session_status`,
  list outputs with `list_notebook_session_output`, curl the signed URLs, extract into the repo, review the diff, commit.
- A codeload tarball has no `.git`: tools that call git (tools/inventory.py) must `git clone` the repository in the notebook instead.

## Open problems, in the order to close them
1. **inventory check and docs/files.md.** `tools/inventory.py` now describes `tools/fig16/kaggle/diag_burst.py`, but
   `python3 tools/inventory.py --check` has not been run (CPU v8 failed: no .git in the tarball). On the Kaggle CPU: `git clone`
   at main, run `--check`; if it fails, run it without `--check` to regenerate `docs/files.md`, download and commit it. Any other
   file without a description (e.g. `tools/fig12/kaggle/damping_grid.py`, `tools/fig16/check_pint3d.cjs`) gets one.
2. **Fig. 16 data panel with the three-way proof** (CLAUDE.md "A data table is a pipeline"; skill `phyein-usul-data-panel`).
   The page `public/simulations/guinness-cart-control.html` (built from `notes/fig16/page/guinness-cart-control.src.html` by
   `tools/fig16/build_page.py`, which runs on Kaggle) plays stored rides (`public/data/fig16/2026-11-14/`, `2026-11-15/`) via
   `public/scripts/guinness16-play.js`, `cart16-view.js`, `pint3d-view.js`. Needed: a panel that shows the stored values of the
   current picture (tilt, pitch, actuator forces, head spilled, ...), the same recomputed from stored inputs, and the pixel read
   back from the canvas; a data cursor that is switched on, never hover (CLAUDE.md rules). Prove it in headless Chromium on
   Kaggle (pip install playwright + chromium there), screenshots downloaded and shown to the owner. Model on Fig. 12's panel,
   if one exists (`public/simulations/guinness-kaggle.html`, `docs/simulations/fig12-beer-slosh.md`).
3. **Fig. 16's own Kaggle dataset** (layout rule in `docs/kaggle-pipeline.md`; Fig. 12 and Fig. 14 already have one): one
   dataset holding the GPU outputs the page uses: version 2 (resonant_full, bump25_full), version 8 (kerb_off, resonant_off,
   bump25_off), version 9 (kerb_full, kerb_full_seed2, summary.json), with a README naming notebook, version and commit.
   The inventory session that planned this is finished; do it here. Copy, delete nothing.
4. **3D close-up smoothness on a real GPU** (`public/scripts/pint3d-view.js`): measure frame times in headless Chromium on a
   Kaggle GPU machine (WebGL via ANGLE/SwiftShader or the T4), for both pages; report ms per frame; fix only if it misses 60 fps.
5. **Fig. 12's bare swing at 1.0 mm (optional).** Numerical damping ζ = 0.0152 at 1.5 mm, 0.0090 at 1.0 mm
   (`notes/fig12/damping-grid.json`, audit F); real stout 0.0055. A rerun of the bare swing at 1.0 mm costs about 10 GPU-minutes:
   ask the owner first (one line, with the cost), per the 18 Nov rule.
6. **Fig. 12 lecture note to STANDARD.md.** Fig. 16's note was rewritten (physics-teacher agent, nine sections). Fig. 12's note
   (`public/simulations/guinness-kaggle.html`, `beer-slosh.html`) was only corrected. Rewrite only if the owner wants it; the
   owner forbade referee/checker agents.

Known design limits, stated in the note, not to "fix": the rear tyres' grip (19 N) and the actuators' 50 N at the kerb (audit M2).

## Where things stand (18 Nov 2026, 01:05 UTC)
main at 34f7ef0, live on https://phyeinusul.com (checked with curl). Branch of the rebuild chat: claude/compassionate-pascal-kk3d8g.
Kaggle GPU quota: weekly 30 h, resets 21 November 00:00 UTC; this week much is used (check get_accelerator_quota).
