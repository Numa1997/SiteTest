# Fig. 13 (Spirographs in Momentum Space): state of the work

Kept current by the chat that builds Fig. 13. Reread after a compaction before anything else.

## Aim
Fig. 13 at https://phyeinusul.com/simulations/momentum-spirographs.html: the momentum sheet with its chaos map ("the eye"), the butterfly,
the flower hunt, the catch (a motor at the top pin brings a chaotic double pendulum onto any of 14 closed orbits, on request), the films.

## Live (26 November 2026)
- `#eye` "How the eye is built": `public/scripts/fig13-eye.js`. Animation in five steps (one strike and its twin, every strike, energy
  ellipses and pupil, iris, fold lines = lashes) with Play, step buttons and a time slider; graph of the chaotic share against strike
  energy from the map image; tap the graph to pin an energy (its ellipse is drawn on the eye).
- `#catalogue` "The catalogue of closed drawings": `public/scripts/fig13-catalogue.js` and `fig13-catalogue-data.js` (228 orbits; built by
  `tools/fig13/closed_map.py` → `closed_pin.py` → `catalogue_build.py`, stability by `closed_stability.py`).
- `#straight` "The eye, straightened": `public/scripts/fig13-straight.js`, pictures eye-struck, eye-spin-fold, eye-unrolled written by
  `tools/fig13/spin_fold.py SHEET.npy EYE.npy public/images/fig13 web`. Spin X = (p1+p2)/sqrt(2 Is), fold Y = sqrt(mu/2)(w2-w1), K = X^2+Y^2;
  streaks at +-60 degrees (If/Is = 1/4).
  Below the figure: the exact matrix, inverse and shear (S = [[1,-3/2],[0,1]], amount C/B), and five sources read in full and quoted
  (Heyl 2008, Rafat et al. arXiv:0812.0393, Dullin 1994, Haham & Kol arXiv:2608.20276, Shapiro notes). Symbolic check: `tools/fig13/spin_fold_check.wl`.
- `#families` "Where the repeating motions live" and `#zoom-title` "Into the border between order and chaos":
  `public/scripts/fig13-families.js` with ten pictures in `public/images/fig13/` (families-petals, families-stability, chaos-sheet-fine,
  chaos-eye-fine, chaos-zoom0..5). Four views with legend and plain explanation each, magnify, tap to pin, run the nearest catalogue orbit;
  seven-picture zoom with frames. Numbers from `tools/fig13/families_ground.py`.
- Card picture on the simulations list: `public/images/sims/momentum-spirographs.webp`, drawn by `tools/fig13/eye_thumb.py`.
- The catch: `tools/fig13/gift/catch.html` and `pendulum.js` (published by `gift/publish_films.py`); 14 targets; measured with
  `node tools/fig13/catch_targets.cjs 60 300`. Numbers in `docs/simulations/fig13-momentum-spirographs.md`.
- Display work on the stations and films was done by a separate session (20 November 2026), merged to main.

## Left
- The arrays behind the fine maps and the stability colouring are not in the repository (Kaggle notebook output, scratch files).
- The labels under the catch picture are small on a phone (check whether the display session fixed them).
- The butterflies are slower to catch than the flowers (median 8 to 35 s); their first catch slips about four times in ten.

## Rules for this work
- Publish finished, browser-tested work to `main` without asking, then check the live site at phone size.
- House fonts only (Instrument Serif titles, IBM Plex Sans text, IBM Plex Mono labels; Instrument Sans in the films).
- No file over 24 MB under `public/`. Never merge branch `fig13-study-bundle`.
- Docs that describe a changed file must say what it now does; run `tools/inventory.py`, `tools/i18n/build.py`, `npm run build`.
- Never write a description of the site owner as a person, never copy chat text, never put keys in the repository.
- Displays only read stored values; show the proof (stored value, recomputed value, pixel) where they meet.
