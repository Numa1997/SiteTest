# Fig. 17 · Living scenes: state of the session (26 November 2026)

Read this first after a compaction.

## The ask (the user, 26 November 2026, 03:45)
"next would be to dedicate a simulation page for all these background simulations, kaggle them that is, and write write write the
lecture notes and whatnot". This is step 5 of notes/sims/PLAN.md ("a page of lecture notes, one section per scene").

## Decisions (made here, per the user's "you judge, you decide")
- One new simulation page, **Fig. 17 "Living scenes"**, `public/simulations/living-scenes.html`, in the catalog; every
  background scene runs in it with its lecture-note section. `scenes.html` stays as the light gallery for now and links to it.
- Every scene with physics gets a reference model `tools/sims/<scene>.py` (SI or stated units, parameters as symbols at the top,
  derivation in the docstring, checks written into the output), run by the engine "Simulations on Kaggle"; the page and the
  background play the stored runs and compute nothing of the physics.
- A knob with physical meaning becomes a choice among values computed on Kaggle (a small grid, stated in the note); a knob of the
  drawing only (tone) stays live. Several random starts (seeds recorded) where the scene is stochastic.
- An endless or stochastic scene stores a run long enough that the seam is rare, and the note says what is stored.
- Chip, seeds, shores and the cloud atlas are drawings with no dynamics to compute: documented as such, not kaggled.
- Notes to notes/STANDARD.md, last verdict (Taylor's Classical Mechanics): patient "we", every step shown, Key result boxes,
  worked examples with the stored numbers, Problems at the end; ★ for heavier passages.

## Order of the scenes
| # | Scene | Model | State |
|---|---|---|---|
| 1 | spinners (`spin`) | overdamped rotors, Adler / Kuramoto, rotating field | in progress |
| 2 | dust in a sunbeam (`motes`) | Ornstein–Uhlenbeck (Langevin) | |
| 3 | mixing (`mix`) | hard-disc gas of three species, event-driven | |
| 4 | the swerve (`swerve`) | falling atoms, collisions | |
| 5 | iron powder (`powder`) | dipole and wire fields, filings | |
| 6 | harmonica (`harp`) | 2D wave equation from reed sources | |
| 7 | roots (`roots`) | space colonisation, Murray's law | |
| 8 | forest and sky (`forest`) | growth, cloud water | |
| – | paper globes (`wind`) | windpend.py, already on Kaggle | done 25 November |

## Rules
- Kaggle runs need no fresh yes; monitor each. Never run models locally.
- Publish when finished, checked against main and tested; the user checks live. Clean up after (branches, scratch, notebooks).
- The user is "the user"; commits as the user.
