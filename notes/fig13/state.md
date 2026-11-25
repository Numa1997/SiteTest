# Fig. 13 (Spirographs in Momentum Space): state of the work

Kept current by the chat that builds Fig. 13. Reread after a compaction before anything else.

## Aim
Fig. 13 at https://phyeinusul.com/simulations/momentum-spirographs.html: the momentum sheet with its chaos map ("the eye"), the butterfly,
the flower hunt, the catch (a motor at the top pin brings a chaotic double pendulum onto any of 14 closed orbits, on request), the films.

## Live (25 November 2026)
- `#eye` "How the eye is built": `public/scripts/fig13-eye.js`. Animation in five steps (one strike and its twin, every strike, energy
  ellipses and pupil, iris, fold lines = lashes) with Play, step buttons and a time slider; graph of the chaotic share against strike
  energy from the map image; tap the graph to pin an energy (its ellipse is drawn on the eye).
- Card picture on the simulations list: `public/images/sims/momentum-spirographs.webp`, drawn by `tools/fig13/eye_thumb.py`.
- The catch: `tools/fig13/gift/catch.html` and `pendulum.js` (published by `gift/publish_films.py`); 14 targets; measured with
  `node tools/fig13/catch_targets.cjs 60 300`. Numbers in `docs/simulations/fig13-momentum-spirographs.md`.
- Display work on the stations and films was done by a separate session (20 November 2026), merged to main.

## Left
- The labels under the catch picture are small on a phone (check whether the display session fixed them).
- The butterflies are slower to catch than the flowers (median 8 to 35 s); their first catch slips about four times in ten.

## Rules for this work
- Publish finished, browser-tested work to `main` without asking, then check the live site at phone size.
- House fonts only (Instrument Serif titles, IBM Plex Sans text, IBM Plex Mono labels; Instrument Sans in the films).
- No file over 24 MB under `public/`. Never merge branch `fig13-study-bundle`.
- Docs that describe a changed file must say what it now does; run `tools/inventory.py`, `tools/i18n/build.py`, `npm run build`.
- Never write a description of the site owner as a person, never copy chat text, never put keys in the repository.
- Displays only read stored values; show the proof (stored value, recomputed value, pixel) where they meet.
