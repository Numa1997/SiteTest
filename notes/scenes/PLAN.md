# The living scenes: from a running decoration to a documented study

Asked on 20 November 2026, 19:58: "similar to some of the work we have on the website, I would like these animations be specified
and analysed and documented on the site as well as their data be generated using Kaggle, brought to GitHub, then animated ...
sometimes process tediousness is important."

Today every scene in `public/scripts/bg-scenes.js` computes itself in the browser with a quick step (semi-implicit Euler, made-up
pixel units, no record). The goal is the same pipeline as the figures (docs/kaggle-pipeline.md):

1. **Specify.** One reference model per scene in `tools/scenes/<scene>.py`, in SI units, every parameter a named symbol at the top,
   the equations in its docstring, integrated accurately (SciPy DOP853 or an exact method), with its own checks written into the
   output (periodicity, tolerance, conservation, a known limit).
2. **Generate on Kaggle, once per scene.** The GitHub Actions workflow "Scenes on Kaggle" ([docs/scenes-pipeline.md](../../docs/scenes-pipeline.md)),
   started by itself when a scene's model is added or changed on `main` (or by hand), pushes the private CPU notebook `numakoudsie/scenes-living-backgrounds`, waits, checks the
   output by SHA-256 and commits it. A scene that should differ on every visit is generated once as a set of runs from random starts
   (seeds recorded); the page picks one at random. No timer; an unchanged model never reruns (owner, 20 November 2026).
   Its output, named by the date of generation, also goes into a dataset `numakoudsie/scenes-living-backgrounds` once there is
   more than one scene.
3. **Stored in GitHub by the workflow.** `public/data/scenes/<YYYY-MM-DD>/` (the data files and `index-<scene>.json` with the notebook, version,
   commit, sizes and SHA-256), and `public/data/scenes/generations.json` listing the generations.
4. **Animate from the data.** The scene reads its stored file and plays it; the browser computes nothing the model computed. Where
   a scene is endless by design (the forest), the stored run is long enough that a visitor never meets the repeat, and the page
   says what is stored and what is drawn.
5. **Document on the site.** A page of lecture notes, one section per scene in figure order (picture from everyday life, model,
   derivation, the numbers of the stored run, what the drawing changes), plus `docs/scripts/bg-scenes.md` for the code.

A stored loop repeats. For a periodic system (Barton's pendulums) the model is made exactly periodic, so the loop has no seam.
For the stochastic scenes (forest, spinners, mixing) the choice between "stored and repeating" and "live and never repeating"
is the user's; it will be asked when those scenes come up.

## Order

| # | Scene | Where | Physics the model specifies | State |
|---|---|---|---|---|
| 1 | Barton's pendulums (`rails`, right) | home, right margin | pendulums on a moving support, driver with a swept length | model, pipeline A and the player (pipeline B) written and tested with a stand-in for Kaggle; first real run when the secret `KAGGLE_API_TOKEN` is in GitHub |
| 2 | spinners (`spin`) | home, strip | phase oscillators locked by a rotating field (Adler / Kuramoto) | |
| 3 | harmonica (`harp`) | Simulations, foot | reed tones as travelling pressure fronts | |
| 4 | iron powder (`powder`) | Simulations, beside title | dipole and wire fields, filings aligning | |
| 5 | mixing (`mix`) | Portfolios, foot | hard-disc gas of three species, entropy of mixing | |
| 6 | chip (`chip`) | Portfolios, beside title | routing and step-and-repeat exposure | |
| 7 | roots (`rails`, left) | home, left margin | space colonisation, Murray's law | |
| 8 | forest (`forest`) | home, top | growth, seasons, droplet collection | |
| 9 | motes (`motes`) | Lucretius, beside title | Ornstein-Uhlenbeck (Brownian) motion | |
| 10 | swerve, seeds, shores | Lucretius, home foot | to be specified | |

## Step 1, Barton's pendulums (20 November 2026)

`tools/scenes/barton.py`. Local run: sweep period T_s = 64.98 s (75 driver turns per sweep, rounded so the loop closes), 1949
frames at 30 fps, file 40 kB; periodicity residual 4.3e-11 rad, tolerance check 6.1e-10 rad, against a storage step of 1e-4 rad.
Largest swings 0.99 rad (shortest, 0.10 m) down to 0.28 rad (longest, 0.34 m): the short pendulums answer more because the
bar's push enters as ẍ_b / L. Each pendulum swings widest a little after the driver's length has passed its own, while the driver
is shortening: the response lags the sweep.
