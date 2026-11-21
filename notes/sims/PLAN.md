# Moving every simulation to data computed once on Kaggle

Asked on 20 November 2026, 19:58: "similar to some of the work we have on the website, I would like these animations be specified
and analysed and documented on the site as well as their data be generated using Kaggle, brought to GitHub, then animated ...
sometimes process tediousness is important."

Today every scene in `public/scripts/bg-scenes.js` computes itself in the browser with a quick step (semi-implicit Euler, made-up
pixel units, no record). The goal is the same pipeline as the figures (docs/kaggle-pipeline.md):

1. **Specify.** One reference model per scene in `tools/sims/<scene>.py`, in SI units, every parameter a named symbol at the top,
   the equations in its docstring, integrated accurately (SciPy DOP853 or an exact method), with its own checks written into the
   output (periodicity, tolerance, conservation, a known limit).
2. **Generate on Kaggle, once per scene.** The GitHub Actions workflow "Simulations on Kaggle" ([docs/kaggle-sims.md](../../docs/kaggle-sims.md)),
   started by itself when a scene's model is added or changed on `main` (or by hand), pushes the private CPU notebook `numakoudsie/phyein-usul-simulations`, waits, checks the
   output by SHA-256 and commits it. A scene that should differ on every visit is generated once as a set of runs from random starts
   (seeds recorded); the page picks one at random. No timer; an unchanged model never reruns (owner, 20 November 2026).
   Its output, named by the date of generation, also goes into a dataset `numakoudsie/phyein-usul-simulations` once there is
   more than one scene.
3. **Stored in GitHub by the workflow.** `public/data/sims/<YYYY-MM-DD>/` (the data files and `index-<scene>.json` with the notebook, version,
   commit, sizes and SHA-256), and `public/data/sims/generations.json` listing the generations.
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

`tools/sims/barton.py`. Local run: sweep period T_s = 64.98 s (75 driver turns per sweep, rounded so the loop closes), 1949
frames at 30 fps, file 40 kB; periodicity residual 4.3e-11 rad, tolerance check 6.1e-10 rad, against a storage step of 1e-4 rad.
Largest swings 0.99 rad (shortest, 0.10 m) down to 0.28 rad (longest, 0.34 m): the short pendulums answer more because the
bar's push enters as ẍ_b / L. Each pendulum swings widest a little after the driver's length has passed its own, while the driver
is shortening: the response lags the sweep.

## All simulations, in figure order (owner, 21 November 2026: "we start from the first one")

Every simulation that still computes in the visitor's browser goes through the same line, one per pull request, starting with
Fig. 1. "Live" means the page computes its physics in the browser today.

| Order | Simulation | Page | Today |
|---|---|---|---|
| 1 | Fig. 1 Wave interference | `public/simulations/Circular Wave Interference Visualization.html` | live |
| 2 | Fig. 2 Double pendulum chaos | `public/simulations/Double Pendulum.html` | live |
| 3 | Fig. 3 Double-slit interference | `public/simulations/Interactive Double-Slit Experiment Visualization.html` | live |
| 4 | Fig. 4 Transverse and longitudinal waves | `public/simulations/Transverse and longitudinal waves.html` | live |
| 5 | Fig. 5 Circular water waves | `public/simulations/water-wave.html` | live |
| 6 | Fig. 6 Wave interference simulator | `public/simulations/wave-interference.html` | live |
| 7 | Fig. 7 Phasor sums | `public/simulations/phasor-sums.html` | live |
| 8 | Fig. 8 Draw and decompose | `public/simulations/draw-decompose.html` | live |
| 9 | Fig. 10 Wind turbine control | `public/simulations/wind-turbine.html` | live |
| 10 | Driven oscillator | `public/simulations/driven-oscillator.html` | live |
| 11 | Fig. 11 Double pendulum under control | `public/simulations/pendulum-control.html` | live |
| 12 | Balancing two rods on a cart; in a liquid | `double-inverted-pendulum.html`, `rods-in-liquid.html` | live |
| 13 | Fig. 12 Guinness on a cart built to carry it | `public/simulations/guinness-cart-control.html` | live |
| 14 | Fig. 12 Guinness on a one-wheel cart | `public/simulations/guinness-kaggle.html` | Kaggle data, carried by hand in the past |
| 15 | Fig. 13 pages (catch, dashboard, periodic orbits, spirographs) | `public/simulations/butterfly-*.html`, `flower-hunt.html`, `momentum-spirographs.html` | mostly live |
| 16 | Fig. 14 Wave packet meets a sphere | `public/simulations/schrodinger-sphere.html` | Kaggle data, carried by hand |
| 17 | Fig. 15 Resonant tunnelling | `public/simulations/resonant-tunnelling.html` | Kaggle data in R2, carried by hand |
| 18 | The projects (droplets, rotor pendula, hydraulics, impact, electron beam) | `public/portfolios/*` | live, to be inventoried |
| 19 | The background scenes (forest, roots, spinners, shores, powder, harmonica, chip, mixing, motes, swerve, seeds) | `public/scripts/bg-scenes.js` | live |

Each page is read first: what it integrates or randomises, what its sliders change (the stored data must cover their whole range),
and how large the stored data would be. Pages already computed on Kaggle (14, 16, 17) move to the automated line so nobody carries
their data by hand again.
