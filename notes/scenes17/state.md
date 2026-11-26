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
| 1 | spinners (`spin`) | overdamped rotors, Adler / Kuramoto, rotating field | model, page, note §2 done 26 Nov; publishing (PR from fig17-scenes) |
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

## Progress (26 November 2026, Berlin time)
- 03:58 Kaggle preview v16 (commit 0e64e23): all checks good. Adler slip period to 7.7e-9, locked rate to 3.7e-9 rad/s; still field:
  108 predicted, 115 measured, the 7 extra have slip periods 114 to 736 s (> 60 s window); rerun at 1e-11 within 0.038 rad. 62 s wall.
  v14 failed (uint8 overflow), v15 had a meaningless relative error and a bad end-of-run comparison; both replaced.
- After v16 the quantisation was changed from floor to nearest (error π/256); the data on main comes from the workflow run at merge.
- Built: `public/simulations/living-scenes.html` (stage with all 13 holders, chips, knobs from K with stored-value buttons, readouts,
  note §1 + §2 with 3 SVG figures from `figs.py`), catalog entry + thumbnail, "17" in every English nav, ENGLISH_ONLY, DE/AR strings
  for the catalog, scenes.html knob buttons + data-bg-fit for S4, docs (bg-scenes.md, kaggle-sims.md, fig17-living-scenes.md), inventory.
- Tested locally with the v16 file K10-k1 staged in dist only (page.cjs: all scenes drawn, no errors except the expected 404s of
  unstaged runs).

## Next
- Merge, watch the workflow (Kaggle run, land, verify_live), check the live page.
- Then motes (Ornstein–Uhlenbeck): model, run, section 3 of the note.
