# Fig. 17 · Living Scenes

Page: `public/simulations/living-scenes.html` (English only, `ENGLISH_ONLY` in `tools/i18n/build.py`), served at
<https://phyeinusul.com/simulations/living-scenes>. Added 26 November 2026, at the user's request: one simulation page for all the
small moving pictures behind the site's pages, their physics computed on Kaggle, with lecture notes.

## What the page does, in plain words

The page has one picture frame (the stage) and a panel under it. The stage holds all thirteen scenes of `scripts/bg-scenes.js`, one
holder each, but shows only one at a time. The chips at the top of the panel choose the scene; the page then shows that holder,
tells `bg-scenes.js` to size it (`__bgSize()`), and fills the panel for it:

- **What you see**: one sentence about the scene, and a note saying whether it is computed on Kaggle, still drawn in the browser, or a
  drawing.
- **Numbers to change**: built from the scene's own table `K` (the same table the scenes page uses). A slider for a drawing number; a
  row of buttons where the table lists stored values, because the physics was computed on Kaggle only for those.
- **Start again**: restarts the scene.
- **Readouts** and **Where these numbers come from**: for a stored scene, the numbers of the file being played, read from its header
  and its stored columns, rewritten about four times a second; nothing is recomputed. For the spinners: time in the run, K₀, κ, and the
  stored share of rotors near the field's centre that turn with it. For the paper globes: the wind and thread numbers. For the other
  scenes, a sentence saying they are not stored yet, or are drawings.

The address can name a scene (`living-scenes.html#wind`); the page opens on it.

With reduced motion asked for in the system settings, the background scenes of other pages stay off, but these holders carry
`data-bg-motion="allow"`: the reader came to this page to see them.

## The lecture note

Section 1 says which scenes are physics and which are drawings, and the rule they follow (computed once on Kaggle, stored with a
SHA-256 fingerprint, only played back). Section 2 is the spinners: the torque balance of a small magnet in oil, Adler's equation in
the frame turning with the field, the locking condition and slip period (derived, with the ★ integral), the locking radius, what the
moving field and the neighbours change (Table 1, from the stored runs), how the runs were computed and checked, how each drawn thing
maps to a symbol, the model's limits, problems and three sources. Its three figures are SVG plotted from the formulas and, in
Figure 2, from the stored single-rotor checks (`notes/scenes17/figs.py` writes them from `spinners.json`). Each further physics scene
gets its own section when it moves to Kaggle; the order is in `notes/scenes17/state.md`.

## Files

- `public/simulations/living-scenes.html`: the page, its note and its small script (chips, knobs, readouts).
- `public/scripts/bg-scenes.js`: the scenes; `S.spin` plays `data/sims/spinners/<date>/spin-K<K₀>-k<κ>.bin`
  ([../scripts/bg-scenes.md](../scripts/bg-scenes.md)).
- `tools/sims/spinners.py`: the spinners model, run on Kaggle by the workflow "Simulations on Kaggle"
  ([../kaggle-sims.md](../kaggle-sims.md)); `tools/sims/registry.json`, entry `spinners`.
- `public/scripts/catalog.js`: the catalog entry, Fig. 17; thumbnail `public/images/sims/living-scenes.webp`.
- `notes/scenes17/`: the state file of this work, the figure script and the browser check (`page.cjs`).
