# Sky and wind: state of the session (24 November 2026)

Read this first after a compaction.

## The user's asks (24 November 2026, 10:13)
1. The clouds "do not look good": show every kind of cloud, "the very large, the very long, the thin", by shape and form, and use
   them in the animations.
2. Replace the spring-coupled pendulums ("out of place, void of creativity") with "swinging pendula under a velocity wind field,
   the field lines, not arrows, present, guiding their motion next to gravity", the problem the site already solved (the flows and
   the drag law of the double inverted pendulum page, section 13).

## The user's rules for this work
- No code by Claude, not one line: every code file comes from Neon (Gemini) through the user (notes/sims/ENGINE-PROMPT.md, "HOW YOU
  WORK"). Claude writes the requests, applies the answers byte for byte, tests, commits, reports.
- Every model run on Kaggle, never locally; Kaggle runs need no fresh yes; monitor each run.
- Publish without asking once finished, checked against main and tested; the user checks the live site.
- Refer to the user as "the user"; commits as the user, no AI attribution. Times in Berlin time. Clean up after.

## Decisions
- Clouds: the ten WMO genera (International Cloud Atlas; temperate levels: low to 2 km, middle 2–7 km, high 5–13 km), each a 3D
  generator in bg-sky.js, seen through the forest's existing ground camera; the season picks the mix; cumulus keep the water
  bookkeeping and can grow into a cumulonimbus; a cloud-atlas scene S13 on scenes.html.
- Pendulums: a wind blowing down the margin with a Kármán vortex street in its wake. Chosen because the field is a travelling
  pattern, v(η, ξ − c t): it repeats with T = λ / c, and a pendulum lower by Δξ sees the same wind Δξ / c later, so one settled orbit
  per position across the strip serves every beam, exactly. Light balsa rods with polystyrene balls, so the air's push is a fair part
  of their weight. Drag as on the site: resistive force theory (33) plus quadratic drag (34); sphere drag for the ball. Field lines =
  contours of the stored stream function, shifted by c t on the page.

## Requests to Neon
- N-1 (notes/home/neon/N-1-request.md): bg-sky.js (new), bg-scenes.js, scenes.html. Status: sent to the user, waiting.
- N-2 (notes/home/neon/N-2-request.md): tools/sims/windpend.py (new), registry.json. Status: sent to the user, waiting.
- N-3 (after N-1 is applied and N-2 has run on Kaggle): the player in bg-scenes.js (rails right half, and the pairs scene on the
  scenes page becomes the wind pendulums), with the field lines.

## Branch
- `sky-and-wind` from main 5b09422.
