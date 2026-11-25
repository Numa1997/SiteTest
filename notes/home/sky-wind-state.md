# Sky and wind: state of the session (24 November 2026)

Read this first after a compaction.

## The user's asks (24 November 2026, 10:13)
1. The clouds "do not look good": show every kind of cloud, "the very large, the very long, the thin", by shape and form, and use
   them in the animations.
2. Replace the spring-coupled pendulums ("out of place, void of creativity") with "swinging pendula under a velocity wind field,
   the field lines, not arrows, present, guiding their motion next to gravity", the problem the site already solved (the flows and
   the drag law of the double inverted pendulum page, section 13).

## The user's rules for this work
- 25 November 2026, 02:44: "nevermind, you handle all fixes and all enhancements and push": Claude writes the code itself again
  (the Neon requests N-1 and N-2 were never used and are deleted).
- Every model run on Kaggle, never locally; Kaggle runs need no fresh yes; monitor each run.
- Publish without asking once finished, checked against main and tested; the user checks the live site.
- Refer to the user as "the user"; commits as the user, no AI attribution. Times in Berlin time. Clean up after.

## What was built (branch `sky-wind-2`, from main e466e6d)
- `public/scripts/bg-scenes.js`: `mkSky()` (the ten cloud genera in 3D, two canvases, mask), the forest's sky through the year
  (`SEASON`, `NG`, `CB`, winds per level, the thunder cloud), `windDraw()`, the rails' right half, the scenes `wind` and `atlas`.
- `tools/sims/windpend.py` and its registry entry; `coupled` keeps its model and data but has no page.
- `public/scenes.html`: S3 is now the wind, S13 the cloud atlas, S1's text describes the sky.
- `index.html` note: the forest's and the globes' sentences, with German and Arabic.
- Docs: `docs/scripts/bg-scenes.md`, `docs/kaggle-sims.md`.
- Kaggle previews from the branch: notebook numakoudsie/phyein-usul-simulations versions 11 (λ = 4 m) and 12 (λ = 6 m, kept
  parameters); outputs not committed. The site's data comes from the workflow after the merge.

## Measured
- windpend v12: T = 4.69 s; settled in 14 to 17 periods; swings 0.35, 0.27, 0.35 rad; gap 0.78 m; energy residual 1e-11.
- Pages (check.cjs): 7 pages × 4 widths and reduced motion, no errors, no sideways scroll.
- Cost (cost.cjs, headless, 1920 px): forest draw 20 to 30 ms a frame (17 ms before the ten kinds); rails 1.6 ms (1.4 ms before).

## Open
- The user found YEAR = 120 s too long (23 November) but asked to keep it; it is the first number of S.forest.
- The scenes page is English only.
