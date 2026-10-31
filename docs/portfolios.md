# The four research projects: `public/portfolios/`

The Portfolios page ([`public/portfolios.html`](../public/portfolios.html), described in [pages.md](pages.md)) presents four
research projects; the fourth, Iron, Cotton and the Head, is described [at the end](#iron-cotton-and-the-head-impact). Droplet Collection ([below](#droplet-collection-droplet-collection-since-23-october-2026)) and Rotor Pendula ([below](#rotor-pendula-rotor-pendula)) are, since 23 October 2026, generated from their sources in this repository; the third, the Hydraulic Press
Study, is generated from its source in this repository too, `portfolios-src/hydraulics/` (moved here from the repository
`Numa1997/Gergi-s-vision` on 21 October 2026; [below](#the-hydraulic-press-study-hydraulics)). The site serves the
**generated pages**, never edited by hand:

| Folder | Generated from | What it is |
|---|---|---|
| [`public/portfolios/droplet-collection/`](../public/portfolios/droplet-collection/) | its source in [`portfolios-src/droplets/`](../portfolios-src/droplets/) | Numa's Bachelor thesis (Leipzig) on how cloud droplets grow into rain, rebuilt as lecture notes: thirteen chapters from one drop to ice, energy and entropy, who eats whom, and a cloud with a shape, five simulations running in the browser, worked problems and checks. One self-contained page ([below](#droplet-collection-droplet-collection-since-23-october-2026)). |
| [`public/portfolios/rotor-pendula/`](../public/portfolios/rotor-pendula/) | its source in [`portfolios-src/rotor-pendula/`](../portfolios-src/rotor-pendula/) | A second blade hinged at the tip of a wind-turbine blade as a sensor's power supply, told as a double pendulum whose first arm the wind holds: lecture notes in nine chapters, a simulation page and an animated turbulent-wind page, one generated page. |
| [`public/portfolios/hydraulics/`](../public/portfolios/hydraulics/) | its source in [`portfolios-src/hydraulics/`](../portfolios-src/hydraulics/) (not an app) | A servo-hydraulic press under digital control, from first principles: the animated press with its PID controller, loop analysis (Bode, Nyquist, z-plane), Pascal's ideal press, and a 23-chapter text deriving every equation. One page, with the site's font files beside it. |

Every project here is generated from its source in this repository.

## Files in each project folder

### `droplet-collection/`

The page is generated from [`portfolios-src/droplets/`](../portfolios-src/droplets/); see
[below](#droplet-collection-droplet-collection-since-23-october-2026). What sits in the folder:

| Path | What it is |
|---|---|
| `index.html` | The whole project in one file, written by `portfolios-src/droplets/tools/build.py --site`: the lecture notes (maths typeset at build time with KaTeX 0.16.11), the model, the five simulations, the figures as inline SVG. It loads the site's `fonts/instrument-plex.css` and `vendor/katex/katex.min.css`. |
| `fig/plate-fallspeed.svg`, `fig/plate-efficiency.svg`, `fig/plate-warm.svg`, `fig/plate-first.svg` | The four plates of the Portfolios page article, written by the same build from the same figures as the notes. |
| `fig/c1_ice.svg`, `fig/ecoll_map.svg`, `fig/fallspeed_gk.svg`, `fig/golovin.svg`, `fig/w2_rain.svg`, `fig/w2_spectra.svg` | Older plates of the study. No page links them (checked 29 October 2026: `grep -rl c1_ice public index.html` finds nothing). |

### `rotor-pendula/`

| Path | What it is |
|---|---|
| `index.html` | **Generated** by `portfolios-src/rotor-pendula/tools/build_combined.py --site` (4.16 MB, 31 October 2026): a tab bar with the lecture notes (`#notes`), the simulation (`#sim`) and the wind (`#wind`), each embedded unchanged in its own frame; described [below](#rotor-pendula-rotor-pendula). |
| `LICENSE-fonts.txt` | Licences of the fonts the page uses (written by the build). |


## The Hydraulic Press Study: `hydraulics/`

This project was never a Vite build of an app. It is one HTML page (with German and Arabic versions) that needs only the site's
font files beside it, generated from its
source, which lives in this repository in [`portfolios-src/hydraulics/`](../portfolios-src/hydraulics/) (its
[`README.md`](../portfolios-src/hydraulics/README.md) describes it). Vite neither builds nor serves that folder. The study was
written in the repository `Numa1997/Gergi-s-vision` and moved here on 21 October 2026, so that the whole site has one
repository.

**What the reader gets.** A tab bar with three tabs: the servo-hydraulic press (pump, four-way servo valve, two metres of hose,
differential cylinder and specimen under a PID controller sampled every 1 ms, animated, every setting recomputable, with
time traces, Bode, Nyquist and z-plane plots and nine worked solutions), Pascal's ideal press, and *Hydraulics from First
Principles*, a 23-chapter text with 63 numbered equations. `index.html#servo`, `#ideal` and `#theory` open a tab directly;
the Portfolios page links to those three addresses.

**How the page works.** Picture three finished pages packed into one envelope. Each of the three pages is stored inside
`index.html` unchanged, as a JSON string, and shown in its own frame (`<iframe srcdoc>`; for a host that refuses `srcdoc` frames, a `blob:` frame replaces it after 8 s, but
only then: a frame that is merely slow is left to finish, since 31 October 2026, and on the site the security policy would block a
`blob:` frame anyway, [performance.md](performance.md)),
so their styles, element ids and scripts cannot collide. A small script added to each embedded page turns the links between
them into tab switches. The scripts and styles are inline; the text's maths is typeset when the page is generated, so no KaTeX
runs in the browser. The fonts are the site's own files: the study's sources embed them as `data:` addresses so that a standalone
copy works anywhere, and the site build (`--site`) replaces each one by a link to the byte-identical file in `public/fonts/` or
`public/vendor/katex/fonts/` ([`portfolios-src/site_fonts.py`](../portfolios-src/site_fonts.py), since 31 October 2026). A phone
then fetches each font once and keeps it for every tab and page, instead of receiving the same 59 fonts (1.3 MB of base64, about
two thirds of the compressed page) inside the page on every visit; measured before and after in [performance.md](performance.md).
The page loads `../../fonts/instrument-plex.css` for its tab bar and those font files, and makes no request outside the site.

**Its security policy has two additions.** The page carries the website's policy and referrer rule after its charset line,
taken from the root `index.html`, as every page does. The servo press runs its solver in a Web Worker that it builds from text
at run time, so this one page adds `'unsafe-eval'` to `script-src` (for `new Function`) and `blob:` to `worker-src` (the worker
is started from a `blob:` address). A policy in a `meta` tag governs only the page that carries it, and the frames inherit
it, so no other page of the site is affected. The response headers of [`public/_headers`](../public/_headers) apply as to
every page; `X-Frame-Options: SAMEORIGIN` does not stop the page's own frames, which are same-origin.

**Files.**

| Path | What it is |
|---|---|
| `index.html` | The whole study, 3.79 MB (31 October 2026): the tab bar and the three embedded pages. |
| `de.html`, `ar.html` | The study in German and Arabic, written by `tools/i18n/hydraulics.py` from `index.html` and the tables in `i18n/<lang>/` ([i18n.md](i18n.md)); never edited by hand. |
| `LICENSE-fonts.txt` | The licences of the fonts the study uses (SIL Open Font License 1.1 for IBM Plex and Instrument Serif; MIT for KaTeX's fonts). |
| `fig/01_press.webp` … `fig/04_map.webp` | The four plates of the Portfolios page (part 3.3), screenshots of the study at 600 px height: the press mid-cycle, the six time traces, Bode and Nyquist, and the block map of chapter 0. |

**How to update it.** Change the study in `portfolios-src/hydraulics/`, then, from that folder:

~~~bash
(cd tools && npm ci)                       # KaTeX 0.16.11 for the theory page, once
python3 tools/build_theory.py              # only if theory/*.src.html changed
python3 tools/build_combined.py --site     # writes ../../public/portfolios/hydraulics/index.html and LICENSE-fonts.txt
python3 check_physics.py && python3 check_control.py                          # the physics against independent Python models
node tools/check_theory_numbers.js ../../public/portfolios/hydraulics/index.html   # 52 numbers in the text against the models
~~~

The folder has its own `package.json` only to say `"type": "commonjs"`: the site's root `package.json` declares ES modules,
and the study's Node scripts are CommonJS. Then build this site, serve `dist/` (for example `python3 -m http.server` in it)
and run, from that folder, `python3 tools/check_combined.py http://localhost:<port>/portfolios/hydraulics/index.html` (33 checks in a real browser:
each tab complete, Play and the sliders working, links switching tabs, no script error, nothing scrolling sideways at 360 to
1440 px). `--site` takes the policy from this repository's `index.html`, the tab icon from `portfolios.html` and the fonts from
`public/fonts/instrument-plex.css`, so a change to those reaches the study on its next generation. The plates are not
regenerated automatically; retake them when the pictures change.

**Verified on 21 October 2026**, with the copy served from this repository's build under its own policy: 33 of 33 browser
checks, 52 of 52 theory numbers, no request outside the site, the tab bar in the site's own Instrument Serif and IBM Plex Sans.

### The data panel of the two simulations (since 23 October 2026)

The ideal press and the servo press each carry the site's data panel ([scripts/datalog.md](scripts/datalog.md)), the same one as
the eleven simulations and Iron, Cotton and the Head. Each page is its own source, so the store and the panel's hooks are written into
it, after the page's user-interface code: `declareStore()`, `storeRun()` (and on the servo page `storeAnalysis()`), `setNow()` and
`Sim.data`.

**Loading the shared files from inside a frame.** Each page sits in an `iframe srcdoc`, whose address for relative links is the
study's own (`portfolios/hydraulics/index.html`), so `../../scripts/…` reaches the site's `sim.js`, `dataset.js`, `datalog.js` and
`../../styles/…` its `paper.css` and `data.css`. A three-line loader in each page chooses the folder: two levels up when the
address ends in `/portfolios/hydraulics/…`, `../../public/` when the page is opened from `portfolios-src/hydraulics/` on disk, and
nothing elsewhere (the `blob:` fallback frame), where the page runs as before without a panel. The scripts are written into the page
with `document.write` while it is being read, so they keep their order: `sim.js`, `dataset.js`, the page, `datalog.js`. `sim.js`
loads a walkthrough only for an element that names one in `data-walk`, so the ideal press's chart `canvas#walk` (the pressure walk)
no longer makes it request `walk/null.js`.

**What is stored.** Ideal press (92 variables): the seven sliders, the eleven constants of `CONST`, ten numbers of `makeModel()`
(areas, the lever $r$, $F_{1,\min}$, the level stiffness $k$, $\mu'$, $\mu(0)$), the run's results (outcome, departure, stroke stop,
impact speed and lost energy, highest and lowest pressure, the two self-tests), the 18 recorded series over one sample per 1 ms plus
$x_2 = r x$, $F_2 = p_2 A_2$ and Pascal's $F_1/r$, the sample on screen, and the drawing (scale, origin, piston rows, dial radius,
centres, full scales and the five needle angles). Servo press: the sixteen sliders, the constants of `C0`, thirteen numbers of
`makePlant()`, the cycle's results, the 28 recorded series per controller sample plus the two summed losses shown in the tiles, and for
each loop the margins, the operating point, the frequency response (500 frequencies: $|L|$, dB, phase, Nyquist real and imaginary
parts) and the open- and closed-loop poles with their frequencies and damping ratios, the sample on screen and the drawing (scale,
dial centres, radius, full scales, the five needle angles).

**What reads it.** The scene, the dials, the plots, the readouts, the status lines and chips, and on the servo page the Bode and Nyquist
plots and the tables of margins and poles read the store's arrays and values (the z-plane plot draws the same closed-loop poles from
the analysis result the store was filled from); the arithmetic left in the drawing turns metres, pascals and
newtons into pixels and display units. The servo page's nine worked solutions compute their own small figures when opened; those
numbers are not in the store, and the panel's paragraph says so.

**Check.** A slider value against the slider; a constant against the code; a derived value from its formula with the stored inputs;
every recorded series and every result by running `simulate()` again from the stored parameters (ideal press: a few milliseconds;
servo press: the whole cycle and both analyses on this page, 1.6 s in Node, cached by the parameters); the drawing numbers from the
layout formula and the stored inputs. **Read-back:** the five needles of each dial strip (a dark pixel 0.45 r from the hub along the
stored angle) and, on the ideal press, the lower edges of both pistons at their stored rows. **Read values:** a click on a dial pins
its value and needle angle, on a piston (ideal) or the ram and platen (servo) pins the motion, pressures and forces of the sample on
screen, on the oil (ideal) pins the pressure there and its parts. **One round** is one run (ideal) or one press cycle (servo), from
$t = 0$; Record plays it from the start.

**The ideal press's pressure probe now needs a click.** It used to follow the mouse across the running figure, against the site's rule
that nothing on a running figure reacts to a pointer merely crossing it; a click or tap places it, a click outside the oil removes it.

## Rotor Pendula: `rotor-pendula/`

Since 23 October 2026 the page at `portfolios/rotor-pendula/index.html` is generated, like the Hydraulic Press Study, from its
source in [`portfolios-src/rotor-pendula/`](../portfolios-src/rotor-pendula/) (its [`README.md`](../portfolios-src/rotor-pendula/README.md)
gives the commands and checks); the models, model runs and review record are in `notes/rotor-pendula/`.

**What the reader gets.** Three tabs. *Lecture notes* (`#notes`): *A Second Blade on a Turning Blade*, nine chapters in three parts,
52 numbered equations and twenty-six figures, rewritten on 28 October 2026 as one story whose spine is the double pendulum (the earlier
version, chapters 0–9 patched section by section, is in the git history). All nine chapters were then rewritten again in a denser
style (about 15 % fewer words, 82 displayed equations instead of 55), and then read once more for readability (sentences written out
in full, a plain sentence between derivation steps, long result boxes split from their explanation, no rhetorical questions; about 2 % more
words, the same physics and numbers). On 30 October 2026 a revision for a reader with a bachelor's in physics filled the steps such a reader would stop at (record and diagnosis: `notes/rotor-pendula/revision.md`; every added step checked by SymPy in `notes/rotor-pendula/derive/R_revision.py`; a blind reader's report and its fixes are recorded there), added three figures (the drive chain, the steady lean, the bent tip); a second pass derived what was still only stated (the adiabatic invariant, Kolmogorov's −5/3 from dimensions, the vibration model's equations in section 8.2); a third pass, after a second blind reader, added the phase plane (Figure 6), the torque law (Figure 21, from `notes/rotor-pendula/derive/L2_torque_curve.py`) rotational sampling (Figure 24), the once-per-turn pushes as turning arrows (Figure 23) and the shaking's power spectrum (Figure 26, from `notes/rotor-pendula/derive/L3_response.py`), an estimate of the best tip-speed ratio from swirl and drag losses, and the vibration model's Lagrangian; every equation number was kept, because the simulation and wind pages cite them: derivations shown line by line, and each new idea in a card
(`.idea` in `tools/theory_template.html`, twenty of them) that says it four ways: what it feels like, what happens physically, how it
is measured, and its mathematics. Figures are numbered at build time: a caption starts `Figure {{fig:key}}.` and the text refers to
`Figure {{fig:key}}`; `tools/build_theory.py` numbers them in order of appearance and stops on an unknown or doubled label, and
`tools/make_numbers.py` refuses a figure key defined twice. Part I, *A double pendulum held by the wind*: chapter 1
opens with the desk double pendulum, introduces the machine (a second, lighter blade, a thin uniform rod of m = 1 kg and l = 1 m,
hinged at the 63 m tip of the NREL 5 MW blade and braked by a generator in the hinge; Figures 1–3) and the sensor it would power,
writes the free double pendulum's Lagrangian for a rigid first arm (1.1)–(1.5), holds the first arm to a steady turning and shows
term by term how the second arm's equation becomes (1.6) while the first arm's equation becomes the torque the rotor must supply,
with the brake's generalized force, the energy balance (1.7) derived from the energy function, and the dimensionless form (1.8); then chaos, free and held (Figure 4, from
`tools/double_pendulum.js`, which copies `deriv()`/`rk4()` out of the site's Fig. 2 page and runs them unchanged: the free pendulum
from 120°, 150° has Λ = 1.44 /s over 3000 s; held, equal arms sit at resonance R = 1 and stay chaotic from some starts at every Γ; the second
blade, R = 94.5, is regular in its bowl and chaotic only near the hilltop unbraked, and with the best brake every exponent is
negative, Table 1); then why the held blade is calm (section 1.5): the landscape (1.10) whose hilltop rises and falls once per turn
(Figure 5), the adiabatic invariant, the separatrix action (1.11) and the predicted chaotic band (1.12), checked against once-per-turn
snapshots, a Poincaré section, of equal arms and of the rod at 6 m/s (Figure 7, also from `tools/double_pendulum.js`; the band's
predicted edges lie within about 5 % of the computed ones). Chapter 2 reads (1.6) from the turning blade (the car pendulum; the turning frame's acceleration derived and the
centrifugal, Coriolis, Euler and gravity torques about the hinge integrated and summed back to (1.6); the apparent gravity and its largest tilt arcsin(1/Γ), Figure 8;
the bowl that rocks, Figure 9; the work of a push that comes round; the energy balance in the turning frame, where gravity pays; the generator as a brake). Chapter 3: the best brake κ* = R − 1 and P* = mg²l/[8Ω(r_p − 2l/3)] (the torques as turning arrows closing a right triangle on Thales' circle, whose area is the power, Figure 10; Figures 11, 12;
Table 2). Chapter 4: stiffness and the stable step, the Radau IIA method (stages, order, stability function), the full equation, the trail that is the bill with the shaft torque derived
exactly (Figure 13), where the mass sits. Chapter 5: the real geared generator (the drive chain, Figure 14; maxon RE 25 + GP 32 C, ratio 492; the describing
function of friction, (5.6) as Pythagoras on the torque triangle; where the rotor's payment goes, Figure 16, the coil's share
computed as the load's times R_c/R_L; Tables 3–5). Part II, *The real wind*: chapter 6 builds the wind (its power, the Betz limit by momentum, energy and Bernoulli with its stream tube, Figure 17; blades as wings and why
λ* = 7.55, Figure 18; the turbulent field of section 6.4 with the Kaimal spectrum against forty synthesised records, Figure 19, and
the field, Figure 20; what the rotor makes of it, with the torque law and why it is stable, the 7.91 rpm at 6 m/s and (6.9) derived); chapter 7 the air on the second blade (the steady lean, Figure 22), estimated and then solved in time in the gusty field; chapter 8 the
blade's sag and the tilt of the stator (Figure 25), its vibration, and the ceiling for white-noise shaking with the double-pendulum Monte Carlo. Part III: chapter 9, the
ceiling inequality, the answer, and the double pendulum once more. Warm-up and guess-first boxes were folded into the prose; worked
examples, checks, "What to remember" boxes and problems with folded answers remain.
Every number is computed by the study's models (`tools/make_numbers.py`) or listed with its reason (`tools/typed_numbers.py`).
The teaching research behind earlier versions and blind readers' reports are in `notes/rotor-pendula/teaching/`. *Simulation* (`#sim`): the same machine;
choose a steady wind (6, 8 or 10 m/s), the brake and an ideal brake or the geared generator; the page solves the full equations
with a Radau IIA integrator in a Web Worker built from its physics block, then plays the last turns back. The scene draws the
three NREL blades from the chord table to one scale and the tip close up to a second, named scale; no angle is magnified. The close-up
draws the second blade slender, as the physics treats it, and a green line at the bottom of its potential bowl, θ_b = atan2(−cos φ, Γ − sin φ),
which the second blade chases; θ_b is stored (`thb_now`), checked from the stored φ, Ω, r_p, g, and read back from the picture. Six
worked solutions (`tools/sim_solutions.js`, numbers from the page's own physics block): the best brake at 8 m/s, the trail as the
bill at 6 m/s, the three winds, how hard the generator must brake and hold, which gear ratio, and where the power goes.
Reading a value is a tool: "Read values" on, a click pins a point, and the values show in a strip outside the plots.

**How the page works.** As for the Hydraulic Press Study: each page is embedded as a JSON string and shown in its own `iframe srcdoc`;
a small script turns links between the three pages into tab switches and opens other links outside the frame.
The page carries the site's security policy with `'unsafe-eval'` in `script-src` and `blob:` in `worker-src` (the simulation's worker).

**The data panel** (since 24 October 2026). The simulation tab carries the site's data panel: the Data tab on the right, Read values
under the scene, Check, Record one round and Save. The page links the shared files (`styles/data.css`, `scripts/sim.js`,
`scripts/dataset.js`, `scripts/datalog.js`) by their path from the source folder, `../../public/…`; `tools/build_combined.py --site`
rewrites that to `../../…`, which the frame resolves against `portfolios/rotor-pendula/index.html` (an `iframe srcdoc` takes its
parent's address). Opened on its own from `portfolios-src/rotor-pendula/`, the page finds the same files; in a build without them
(`--artifact`) the store script returns at once and the page works without a panel. `rotor_sim.html` adds the panel's colour tokens
in its own colours and lays the panel's marker canvas over the scene. The page now also redraws when the box of the scene or
the plots changes size without a window resize (a `ResizeObserver`): before, opening or closing the panel while paused left the
canvases stretched by CSS, so the picture no longer matched the stored positions (and the blade view's two labels overlapped).
Read values works in `#stage`'s coordinates; the scene canvas sits inside it, so `probe` and `inspect` shift by its offset.

- *Physics block.* The second blade obeys $I\ddot\theta + (ml/2)[\Omega^2 r_p\sin\theta + g\cos(\varphi+\theta)] + c\dot\theta = 0$ with
  $I = ml^2/3$ about the hinge and $r_p = 63$ m (notes (1.3)), so $R = 3r_p/(2l)$,
  $G = 3g/(2l\Omega^2)$, $\kappa = c/(I\Omega)$. The rotor's work $W_\text{in}$ is integrated as the last state of every run, with
  $\dot W_\text{in} = \Omega\,\tau_\text{rot}$ and $\tau_\text{rot} = (ml/2)r_p[\ddot\theta\cos\theta - (\Omega+\dot\theta)^2\sin\theta] + mgr_p\cos\varphi - c\dot\theta$
  from Lagrange's equation for $\varphi$ (checked in SymPy); with the generator the gravity term is $G_p = mgr_p/(I\Omega^2)$, which is
  $\tfrac43 GR$ for the rigid blade, not $GR$. `bladeEnergy()` gives $T = \tfrac12 I(\Omega+\dot\theta)^2 + \tfrac12 m r_p^2\Omega^2 + (ml/2) r_p\Omega(\Omega+\dot\theta)\cos\theta$
  and $V = mg[r_p\sin\varphi + (l/2)\sin(\varphi+\theta)]$. Because $d(T+V)/dt = \dot W_\text{in} - c\dot\theta^2$ exactly, the energy book
  $W_\text{in} = \Delta E_\text{kin} + \Delta E_\text{pot} + E_\text{paid}$ closes to the integrator's error: measured residual $2\times10^{-9}$ J
  on runs where $W_\text{in}$ swings by about $\pm mgr_p \approx \pm 6200$ J ($3\times10^{-13}$ of it). The swing of $W_\text{in}$ is the rotor lifting the
  whole second blade through $2r_p$ each turn and letting it down. The double pendulum was removed on 24 October 2026.
- *Store* (the script before the page script): 125 variables in eight groups. What you set (wind, generator, brake, gear ratio,
  load); fixed constants ($g$, $m$, $l$, $r_\text{rot}$, $\lambda^*$); what follows ($\Omega = \lambda^* v/r_\text{rot}$, $n$, $T$, $v_\text{tip}$, $r_p$,
  $I$, $ml/2$, $R$, $G$, $G_p$, $\omega_n = \Omega\sqrt R$, $\kappa^*$, $c$, $\kappa$, $P^* = mg^2l/[8\Omega(r_p - 2l/3)]$, the peak brake torque
  $\tau^* = (ml/2)g/\sqrt2$, and the generator's $c_\text{sc}$, $c_e$, $R_L$, $j = (J+J_g)N^2/I$, $\eta$, share kept, jammed); the state now;
  what the solve found (mean powers, swing, trail, the bill $-(ml/2)r_p\Omega^3\langle\sin\theta\rangle$, the lag, the rotor's mean power);
  the stored record (13 arrays over the frames `k` of the last four turns, the very arrays the page draws); the solver; the drawing
  (both scales: `sc` for the rotor view, `sc2` for the close-up, and their ratio `zoom`; hinge, centre-of-mass and length on screen in
  each view; plot axes; the 161-point curve of the third plot). Power is in watts throughout. The page calls the hooks `D.solved`,
  `D.put`, `D.scene`, `D.plot`, `D.curve` and `D.frame` at the lines where it computes or draws a number; the hooks store what they
  are given and compute nothing.
- *Check* recomputes from stored values only: the derived constants by their formulas from the stored $m$, $l$, $I$ and $ml/2$, the
  record by rerunning the same `simulate()` in the page from the stored settings (cached), the power by $c\dot\theta^2$, the
  energies by the formulas above from the stored angles and rates, the lag by the first-harmonic sum, the axis ends and the
  positions on screen from the stored series and scales. *Read back* (the canvas is opaque, and the tests still check alpha first):
  the wine second blade three quarters along its length in the close-up, from the stored hinge, $\theta$ and $l\,s_2$; for $\varphi$,
  the hinge in the rotor view, placed from the stored hub, $r_p$, $s$ and $\varphi$ (there the 1 m second blade, about 2.6 px, lies under the
  hinge mark, so the blade itself cannot be read); the green bowl-bottom line beyond the second blade's tip, from the stored $\theta_b$; the hinge's dark centre; the wine curves of the
  three plots; the playhead ring; the tiles' numbers (scientific notation included). A curve point under a marker reports "not in
  the picture now".
- *The ledger* ([`scripts/ledger/rotor-pendula.js`](../public/scripts/ledger/rotor-pendula.js), loaded between the page's scripts and
  `datalog.js`): six headline numbers, θ, θ̇, the harvested power p, the rotor's work $W_\text{in}$, the energy lifted $\Delta E_\text{pot}$
  beside it (the two nearly cancel, which explains the rotor's large work), and the harvest $E_h$; eight sections in causal order;
  one book, *Energy*: rows $\Delta E_\text{kin}$, $\Delta E_\text{pot}$, $\Delta E_\text{spin}$, $E_h$, $E_\text{fric}$ and $E_\text{other}$ (winding and gear
  losses), closing line $W_\text{in}$, residual `book_res` stored by the page, tolerance $10^{-9}$ of the flows. Angular momentum has no
  book: the shaft's torque holds Ω fixed. The ledger's new words still need German and Arabic entries.
- *Read values* pins the second blade (either view), the hinge (either view) or the hub; *a round* is one turn of the record
  ($t$ = `t_now`), blocked when fewer than one turn is left before the playback loops.

Measured on 24 October 2026 in headless Chromium on the source page, at 1440 and 390 px with the ideal brake and at 1440 px with
the generator (ratio 51, the formula's load), 8 m/s: no page errors; 135 values (every scalar, and the first, middle and last element
of every array) agree with their Check, the largest gap $2.8\times10^{-16}$ relative; every read-back finds its ink; shifting the stored
$\theta$ by 0.3 rad or $\varphi$ by 0.2 rad makes the blade read-backs fail, as they must; the ledger's text changes 3.7 to 4.0 times a
second while playing; with the panel closed `__dataPanel.running()` is false; Record keeps one turn and Save gives a zip that `zipfile.testzip()` accepts and
`numpy.load` reads (`q1`, `Win`, `Ek` of shape (961,), `kap` of (161,)), with $m$, $l$, $I$, $ml/2$, $P^*$, $\tau^*$ and `zoom` and their units in
`dataset.json`; the book recomputed from the saved arrays closes to $3\times10^{-9}$ J against $|W_\text{in}|$ up to 6600 J.

**The Wind tab** (`#wind`, source `portfolios-src/rotor-pendula/rotor_wind.html`, since 28 October 2026). A turbulent wind over the
rotor, synthesised in the browser in about half a second: the IEC 61400-1 ed. 3 Kaimal spectra for u, v, w (class A, B, C or none;
σ_u = I_ref(0.75U + 5.6 m/s)), the power-law shear (exponent 0.2), the IEC coherence for u and TurbSim's smooth-model default
exp(−0.75 f r) for v and w, on an 11 × 11 grid 12.6 m apart, by Veers' method (a Cholesky factor per frequency, 255 frequencies,
a 256 s record every 0.5 s that repeats); the random numbers are mulberry32 + Box–Muller, so the page's field equals the Python
reference `notes/rotor-pendula/derive/L6_wind.py` to 2·10⁻¹⁴ m/s. The physics block sits between `/*WIND-BEGIN*/` and `/*WIND-END*/`
in the page. The rotor turns in the disc-averaged wind with the NREL torque law and C_p(λ) from the ROSCO table; the second blade
obeys (1.6) of the notes with the Euler torque, the brake set to the best brake at the steady speed of the mean wind, and the air of
chapter 7 at its middle (no air, streamlined with C_L = 2π(γ − γ_0), or a small wing with C_L = 1 + 2π(γ − γ_0): both aerofoils' lift
follows the inflow angle, as in `L5_air.py`), from the local wind of the field; it
starts on the small-swing solution (3.2). Integrated while the reader watches (RK4, h = 5 ms, at 1×, 2×, 5× or 10×). Two views:
the disc from upwind (colour = the gust along the shaft, a 96 × 96 bilinear raster; arrows = the wind across the disc, 3 m per m/s;
the tip magnified in a circle, the second blade at its true θ) and the side view (the column through the hub, the air upstream
by Taylor's frozen turbulence, arrows 1.6 m per m/s, the mean profile dashed). Traces of the last 90 s: hub wind and disc average,
rotor speed, θ, power with its running mean and P*. The store (about 95 variables, the whole synthesised record included, and a
900-sample history ring) and the ledger [`scripts/ledger/rotor-wind.js`](../public/scripts/ledger/rotor-wind.js): six headline
numbers (disc wind, rotor speed, wind at the tip, θ, power, mean power), ten sections, and one book, the second blade's energy:
the rotor's work from Newton's law for its centre of mass (hinge force times hinge velocity, less the brake torque times Ω) plus
the air's work equals the change of its ground-frame energy plus the harvest, tolerance 10⁻⁵ of the flows (measured 4·10⁻¹¹ after
20 s; 7·10⁻⁷ over a whole record in `tools/check_wind.js`). Read values pins the second blade, the hinge, the hub, any grid point
of the disc or any arrow of the side view; measured on 28 October 2026 in headless Chromium at 1440 px: no errors, the strip
rewritten 3.7 times a second, nothing shown by a pointer sweep with Read values off; the figure re-lays itself when the panel
opens (a `ResizeObserver`, deferred to the next frame). `tools/build_wind.py` copies the simulation page's layout stylesheet into
it and typesets its four equations (it imports `typeset_page` from `build_sim.py`). Results quoted in chapters 6 and 7 come from
the Python reference (`L6_wind.json`): at 8 m/s, class A, record 1, the rotor's speed wanders by 11.8 % and the second blade gives
200 mW against 205 mW in steady sheared wind; streamlined 199 mW in steady wind and 212 mW in the gusts; the small wing 287 mW in
steady wind (formula (7.2): +44 %) and 420 mW in the gusts.

**Checks** (from `portfolios-src/rotor-pendula/`): `python3 tools/check_numbers.py` (every number computed or explained),
`python3 -I check_physics.py` (independent SymPy and SciPy checks with retyped constants: the rod's Lagrangian, the uneven-rotor
term, κ*, the 45° lag, P*, τ*, the trail identity, the nine stored runs re-integrated, the generator's circuit and two geared runs),
`node tools/check_sim.js` (the simulation's physics block reproduces the Python engine's nine reference runs, and the geared
settings of `data/L4_check_2000.json`), `node tools/check_newton.js` (Newton's cap and the step: the geared powers change by
at most 8e-12 and 3e-4), `node tools/check_sim_browser.js` (360–1440 px: no errors, no sideways scroll, a hover
sweep changes nothing, Read values pins and rewrites at most four times a second, every "Try it" button solves) and, with
`public/` served, `python3 tools/check_combined.py <url>` (all three tabs complete, 0 KaTeX errors, solve, the wind tab
synthesises and runs, tab links, no sideways scroll at 360–1440 px), `node tools/check_wind.js` (the Wind tab's physics block
against `L6_wind.py`: the same field to 2e-14, a 60 s run with every term to 3e-14, the energy book over a record) and
`node tools/double_pendulum.js` (chapter 1's free and held double pendulum on the site's own engine, `data/L0_double.json`).

**Boxes and their edges (since 28 October 2026, at Numa's request).** Every box of the study carries an **edge**: a line down its
left side, in the colour of what the box holds, on top of its 1 px outline. It generalises the wine line the equation boxes of the
Simulation and Wind tabs had (`.eq`) and the blue line of the concept cards. One rule, two stylesheets:

| Box | Where | Edge |
|---|---|---|
| numbered equation (`.eqn`) | notes | 4 px wine |
| key result (`.eqn.boxed`, also outlined in wine) | notes | 6 px wine |
| the real model's numbers, "On our blade", worked examples (`.press`) | notes | 4 px wine |
| links to the other tabs (`.links a`), quotations (`blockquote.quote`) | notes | 4 px wine |
| a new idea in four ways: feel, physics, measure, maths (`.idea`) | notes | 4 px blue |
| callouts (`.callout`), guess-first boxes (`.guess`), the contents (`nav.toc`, `details.toc-m`) | notes | 4 px blue |
| checks (`.check`) | notes | 4 px green |
| everyday pictures (`.picture`), warm-ups (`.warm`) | notes | 4 px ochre (`--oil-hi`) |
| what to remember (`.remember`) | notes | 4 px ink (`--line`) |
| problems (`.problems`) | notes | 4 px wine-deep |
| figures (`figure.fig`), tables (`table.mt`) | notes | 4 px steel |
| panels (`.box`) and solution cards (`.sol`) | Simulation, Wind | 4 px wine |
| equations (`.eq`) | Simulation, Wind | 4 px wine (was 3 px) |
| tasks (`.sol .task`) | Simulation, Wind | 3 px blue (unchanged) |
| the Read values strip (`.readout`) | Simulation, Wind | 3 px blue |
| number tiles (`.tile`), folds (`details.more`) | Simulation, Wind | 3 px muted brown |
| plots (`.plot canvas`, `canvas#plots`) | Simulation, Wind | 4 px muted brown |
| the scene (`#stage`) | Simulation, Wind | 4 px muted brown, drawn by `#stage::after` over the canvas |
| warnings (`.stale`) | Simulation, Wind | 3 px wine-deep |
| a picture inside a solution card (`.sol .picture`) | Simulation | 3 px ochre |

The colours say what kind of thing the box holds: wine for mathematics and the model's own numbers, blue for ideas and tools, green
for checks, ochre for everyday pictures, ink for summaries, steel or muted brown for figures, plots and tiles. Three things are not
boxes and have no edge: the chapter panels of the notes, which are frames holding the boxes; pills and buttons (`.chip`, `.mag`,
`.crosslinks a`, the tab bar); and the site-wide data panel (`public/styles/data.css`), which belongs to every simulation, not to
this study. The notes' rule is one block at the end of `tools/theory_template.html`'s stylesheet, using a `--edge` property per
box kind; the tabs' rule is one block at the end of `rotor_sim.html`'s stylesheet, which `tools/build_wind.py` copies into
`rotor_wind.html`. Geometry is kept exact: the scene's edge is a pseudo-element drawn over the canvas, so the canvas keeps its size and
the read-back tests their pixels; the Wind tab's plot now sizes its drawing by `clientWidth`/`clientHeight` (inside the border) rather
than the border box, and the Simulation's plot clicks measure from inside the border (`clientLeft`).

## Notes for maintainers

- The KaTeX fonts: once in `public/vendor/katex/fonts/` (20 woff2 files, 0.26 MB), for the simulation pages and Droplet
  Collection, which link `vendor/katex/katex.min.css`, and, since 31 October 2026, for the Hydraulic Press Study and Rotor
  Pendula too: their sources embed the fonts as `data:` addresses, and `build_combined.py --site` links the same files instead
  (`portfolios-src/site_fonts.py`; the build stops if a study embeds a font the site does not serve).


## Iron, Cotton and the Head: `impact/`

Three pages (English, German, Arabic), generated from [`portfolios-src/impact/`](../portfolios-src/impact/) (its [README](../portfolios-src/impact/README.md)
lists every file) by `python3 portfolios-src/impact/build.py --site`. Never edit the three pages by hand.

| Path | What it is |
|---|---|
| `impact/index.html` | The study in English: two balls of 1 kg, iron and cotton, dropped from 10 m onto a head drawn as a plate on a spring and damper, which is also the scale. A peak-hold force gauge and a digital panel under each ball, force curves, energy books, seven sections of derivations and a table of every parameter. |
| `impact/ar.html` | The same study written in Arabic, right to left, set in Amiri and Noto Naskh Arabic ([assets.md](assets.md#arabic-faces-added-22-october-2026-on-numas-request)). |
| `impact/de.html` | The same study in German (`text_de.py`, since 23 October 2026), house fonts; its sitebar links English · Deutsch · العربية and the German Portfolios page. |
| `impact/fig/01_impact.webp` … `04_weight.webp` | The four plates of the Portfolios entry, screenshots of the English page. The entry shows them as Figures 1–4 in the order `01_impact`, `04_weight`, `02_force`, `03_energy`: the two scenes (818 × 600) share the first row and the two plots (1252 × 600, 1468 × 600) the second, so the two plates of a row are nearly the same height. In file order a tall scene sat beside a short plot in each row, leaving 129 px and 187 px of blank under the plots at 1440 px (measured in headless Chromium, 30 October 2026); now at most 59 px, as in the other entries. |

**How a page works.** The model (`physics.js`, copied into the page between `/*PHYSICS-BEGIN*/` and `/*PHYSICS-END*/`) runs once
when the page opens, in slices of 14 ms so the page stays usable, and stores every particle's position every 1 ms up to 2.5 s and
every 2 ms after that; the animation only plays the stored run back, as Figs. 9 and 10 do. Each page carries the site's security
policy and referrer rule after its charset line, loads only `../../fonts/instrument-plex.css` (and `arabic.css` on the Arabic page),
makes no request outside the site, and links back to `../../portfolios.html`. The pages need no `'unsafe-eval'` and no worker.

**What was checked** (22 October 2026, headless Chromium on the built site, `checks/site_check.cjs`): both pages at 1100 and
390 px, no script errors, no failed or outside requests, no sideways scroll; iron peaks at 638.6 N, cotton at 188.0 N, both
scales settle at 9.81 N; the first touch at 1.428 s equals √(2h/g); the energy books close to 0.21 J (iron) and 0.51 J (cotton) out
of about 98 J (`checks/energy_books.cjs`); halving the time step changes the peaks by 0.0 % (iron) and 1.5 % (cotton)
(`checks/step_size.cjs`).

### The data panel of the study

Since 23 October 2026 the pages carry the site's data panel (all three, measured 29 October 2026), the same one as the eleven simulations
([scripts/datalog.md](scripts/datalog.md)). Picture an assistant beside the drop with a notebook: the run is computed once, and
every number of it is written into one store, a dataset in the sense of [scripts/dataset.md](scripts/dataset.md); the drawing, the
gauges, the readouts, the plots and the energy bars only read that store, and the panel shows it, checks it and saves it.

**What loads.** The pages load the shared files from the site, no copies: `../../styles/paper.css` (for Latin Modern in the
panel's symbols) and `../../styles/data.css` in the head; at the end of the body `../../scripts/sim.js`, `../../scripts/dataset.js`,
the page script, and `../../scripts/datalog.js` last. `sim.js` does no harm here: it defines `window.Sim`, adds an error banner if a
script fails, and would load KaTeX for a figure caption with mathematics; the study's caption has none, and since this change
`sim.js` loads KaTeX on a page without a lecture note only when a caption contains `\(` (measured: the page requests
`paper.css`, `data.css`, `sim.js`, `dataset.js`, `datalog.js` and fonts, nothing else). The study defines the panel's colour and
font tokens in its own palette (`--accent` is the study's wine, `--sans` IBM Plex Sans, also on the Arabic page), and its element
rules for `h2`, `h3`, `p`, `button` and `canvas` are written as `:where(…:not(.dp *))`, so they no longer reach into the panel.

**Where the code is.** The store is declared in `declare()` and filled in `record()` in
[`template.html`](../portfolios-src/impact/template.html); the panel's hooks (`probe`, `inspect`, `locate`, `check`, `drawn`,
`round`, `about`) are in [`datahooks.js`](../portfolios-src/impact/datahooks.js), which `build.py` inserts after the page script.
The canvas sits in `figure.stage > div#stage`, with the caption `figcaption.stage__cap` that receives the Read values switch.

**The store.** Six dimensions: `n` (5751 samples: every 1 ms to 2.5 s, every 2 ms to 9 s), `p_iron` (91 atoms), `p_cot` (612
beads), `b_iron` (240 bonds), `b_cot` (1196 bonds: 594 stretch springs along the fibres, 602 junctions) and `c` (47 checkpoints).
The groups of the panel:

| Group | What it holds |
|---|---|
| Parameters | the 35 constants of `P`, as scalars |
| Derived physics | particles and bonds of each ball, particle mass $M/N$, skin contact $m\omega_c^2$ and $2\zeta_c m\omega_c$, iron's Morse $\alpha = \alpha r_0/a$ and $D = k/2\alpha^2$, the junction's $\alpha_j$ and $D_j$, the zero of height energy, $E_0$, $t^* = \sqrt{2h/g}$, $v^* = \sqrt{2gh}$, $Mg$ |
| Solver | samples, checkpoint spacing, samples computed, frame steps, compute time, done |
| Results | first touch, peak force, weight (mean reading from 4 s to 9 s), its distance from $Mg$, largest gap in the energy books |
| Stored run | per sample: `ts`, `nstep`; for each ball the positions `x`, `y` and speeds `sp` of every particle (float32), plate position `yp` and velocity `vp`, scale reading `F`, peak hold `Fmax`, the six energy terms `KE`, `PE`, `El`, `Eh`, `Qb` (heat in the ball), `Qh` (heat in the head), the bars `Ein` and `Esum`, the gap `books` and the running weight `W` |
| Shape of the balls | bond lists `bi`, `bj`, rest lengths `l0`, cotton's bond kinds and fibre of each bead |
| Checkpoints | every 125 samples, the full state of each ball (positions, velocities, plate, peak hold, heat, first touch, which bonds hold) and the step count |
| Playback | `t_play`, `i_now`, `t_now`, `slow`, `playing`, and for each ball the reading, peak, weight, kitchen-scale masses $F_\text{peak}/g$ and $W/g$, plate position, kinetic energy and books gap of the sample on screen |
| Drawing | canvas size and device pixel ratio, ruler, scene top and bottom, column width and centres, the scale $s$ in px/m, the camera height, the gain $G = 10$ of the plate travel and the extra offset $(G-1)y_p$, the plate's screen row, the gauge radius and centre, the two needle angles, the gauge's full scale |

Every variable has a symbol, units where it has any, a long name, `computed_in` and digits. Positions and speeds are float32: the
cotton ball alone holds $612 \times 5751 \times 3$ of them, 42 MB as float32 and 84 MB as float64; everything else is float64.

**What each Check recomputes.** A constant against `P`; a derived value from its formula with the stored inputs; counts, bond lists,
rest lengths and the zero of height energy from a second build by `makeIron()` or `makeCotton()`. A position, speed, plate state,
peak or energy term at sample $n$ by rerunning the same `step()` on a separately built ball, from the checkpoint before $n$ (never
from $n$ itself) to $n$; the first checkpoint is checked by stepping a fresh build from $t = 0$, so the chain is anchored at the
start. The step counts by adding the sub-steps $\Delta t/5$ again exactly as the model does. The scale reading as
$F = -k_h y_p$ from the stored plate position; the bars as $E_\text{in} = E_0 - V_n$ and $E_\text{now} = K + E_\text{el} +
E_\text{head} + Q_\text{ball} + Q_\text{head}$; the books gap as their difference; the weight as the mean of the stored readings;
every drawing number from the stored drawing inputs. A rerun takes at most 1250 steps (0.67 s for cotton and 0.09 s for iron,
measured in Node).

**What each read-back reads.** The plate: two columns near its ends are scanned row by row for the plate's fill colour, which must
begin half the outline below `plate_px`; the black needle: a dark pixel 0.3 R from the hub along the stored angle; the red peak
needle: its tip, 6.5 px inside the rim, which the black needle never covers; a particle at the sample on screen: the dark atom disc
or the pale bead core at the position worked out from the stored drawing variables; the scale reading of sample $n$: the wine
(iron) or blue (cotton) curve of the whole-run plot. Values not drawn at the moment (another sample, a part outside the scene,
cotton's curve under iron's) give "not in the picture at the moment".

**Read values.** A click on an atom or a bead pins it: sample, time, $x$, $y$, speed (and the fibre of a bead). A click on a gauge,
a digital panel or a plate pins that ball's scale: reading, peak, weight, plate position, needle angle. **One round** is one drop,
$t = 0$ to 9 s of the stored run; Record starts a new drop from $t = 0$ (the first frame of a drop advances nothing, so the round
begins exactly at 0), refuses while a drop is under way, and follows the iron scale unless another point is pinned.

**What differs between store and picture**, said in the panel's paragraph: the plate travel, and the ball resting on it, are drawn
ten times larger than computed; the camera follows the lowest iron atom for both columns; bond colours are worked out at drawing
time from the stored positions; cotton fibres are smooth curves through the beads; the gauges have a square-root dial; the weight
shows from 6.5 s.

**The panel's words are English on the Arabic page too**, set left to right (`lang="en" dir="ltr"` on the panel, the tab, the strip
and the switch, written by `datalog.js`), until the panel gets its string table.

**Measured** (23 October 2026, headless Chromium, built site): English page at 1100 and 1600 px, Arabic page at 390 px
(`portfolios-src/impact/checks/data_panel.cjs`): no script errors, no sideways scroll; 190 variables, each with symbol,
long name, `computed_in` and digits, each in one of nine groups; Check on every scalar and on six indices of every array: 406
identical, 34 agreeing to 7 or 8 figures (the float32 positions and speeds), 18 undefined on both sides (the weight before 4 s),
0 differing, all 458 in 7.1 s; every read-back at the moment of impact (t = 1.452 s) shows its value (atoms, bead, both needles, both
peak needles, both plates, both curves), and cotton's curve, where the iron curve covers it, reads "not in the picture at the
moment"; Read values: a pointer swept across the figure paints 0 overlay pixels with the switch off and on, a click pins an atom, a
bead or a scale, the strip sits directly under the figure (no overlap), its values change 4 times a second (12 batches in 3 s); one
round, 0 to 9 s, records every frame (349 to 486 samples at real speed) with no undefined value at the followed scale; Save gives a
51.6 MB zip that `zipfile.testzip()` accepts and NumPy reads (`x_cot` float32 5751 × 612, `F_iron` float64 5751, 73 members,
units in `dataset.json`); with the panel closed `__dataPanel.running()` is false. The run itself gives the documented numbers: iron
638.6 N, cotton 188.0 N, weights 9.810 N and 9.810 N, first touch 1.428 s, books closed to 0.21 J and 0.51 J. Computing the run
takes 9 % longer than before the store (123 s against 113 s in this container's headless Chromium, which has no GPU).



## Droplet Collection: `droplet-collection/` (since 23 October 2026)

The project was rebuilt from first principles as lecture notes. Source, build and checks are in [`portfolios-src/droplets/README.md`](../portfolios-src/droplets/README.md); the record of
how each model level was argued, attacked by an independent reviewer and checked is in [`notes/droplets/`](../notes/droplets/)
(`status.md` first).

- **One page, four tabs.** `index.html` holds the tabs Simulation (`#sim`), Lecture notes (`#book`), Problems (`#problems`) and
  Checks (`#checks`); any element id also works as an address (`#ch3`, `#fig-5-2`, `#eq-6.1`), opening its tab. The Portfolios
  page links to `#book`, `#sim`, `#problems`, `#checks` and to four figures.
- **The model runs in the page.** The code between `/*PHYSICS-BEGIN*/` and `/*PHYSICS-END*/` of `physics.cjs` is inlined; the
  same code runs in Node for the run tools and the checks. The five panels (collection equation in a box, droplet trajectories,
  an exact random cloud, a cloud with a shape, one energy landscape under three rules) change only on a click, a slider release or a
  button; nothing reacts to the pointer crossing a figure. Panel 4 animates on Start; its probe is pinned by a click and its words
  change about four times a second.
- **Every quoted number is checked.** `checks/check_numbers.cjs` recomputes 235 numbers from the model and finds each in the text
  near its anchor; `checks/check_physics.py` recomputes the physics independently in Python (14 checks); `checks/check_browser.py`
  opens every tab at 360, 390, 1024 and 1440 px and counts KaTeX errors, page errors and horizontal overflow.
- **The ladder.** L0 one collector (chapter 1); L1 fall speed (2); L2 collision efficiency (3); L3 coalescence (4); L4 the
  collection equation (5); L5 the exact random process and the first drizzle (6); L6 turbulence, decided by a number (7); L7 ice (8); L8 energy, entropy, ripening and who eats whom (10, 11);
  L10 a cloud with a shape: fall, mean motion and a stochastic element (12). L9 (turbulence at contact scale) and L11 (a mean motion
  measured from cloud pictures) are open; Part IV had one round of two independent reviews (`notes/droplets/review-*.md`).

### The data panel: the bookkeeper (since 24 October 2026)

Panel 4 (a cloud with a shape) carries the site's data panel ([scripts/datalog.md](scripts/datalog.md)) as a bookkeeper, and the
panel also keeps the exact runs of panel 3 (lucky drops) as an ensemble. `Sim.data.ledger`, at the end of `datahooks.js`, declares:
the headline (share of the water in drizzle drops f₁₀₀, share of the starting drops still in the air N/N₀, cloud time, the first
drizzle drop, the share rained out, the largest drop); seven sections in causal order (set-up, what follows from it, the state now,
super-droplets and cells, the ensemble of panel 3, and the solver and drawing, folded); how each number is obtained (the cloud's
own step is "solver", what `record()` works out from it "formula", panel 3's stored runs "stored run"); the two books; the
dependencies of the derived constants; and which menu sets which input. Drop counts (about 10¹⁶) and the residuals print as
2.1×10⁻⁹ (`sci`); the headline prints plain numbers, so it shows N/N₀ rather than N.

- **One store, written where each number is computed.** `app.js` creates the store (`Sim.dataset`, exposed as `Sim.cloudStore`).
  The set-up and the derived constants (air density and viscosity, fall speeds at 10, 20, 40 and 100 µm, collision efficiencies
  from the stored table, the kernel K(40 µm, 10 µm), the eddy speed and memory, the growth constant, the starting water M₀ and drop
  number N₀) are written when a cloud is made (`newCloud()`). After every frame's model steps, `record()` copies the super-droplets
  out of the model (`sd_x`, `sd_z`, `sd_r` in µm, `sd_xi`, `sd_id`, `sd_cls`), adds them into the 40 × 30 collision cells
  (`cell_lwc`, `cell_n`, `cell_rmax`), stores the census (`cloud.census()`, called once per frame) and the two books. The readouts
  beside the picture and the page's own probe read the store; nothing there is computed again. The stored exact runs of panel 3 are
  summarised once at load (share of runs with a 100 µm drop within their 60 min, mean, standard deviation, 10, 50 and 90 % points of the
  time of the first 100 µm drop, for 1, 10, 100 and 1000 cm³); your own run (`lk_*`, 30 min long) is stored with its rank among them (without a drizzle drop of yours, the stored runs that had one by 30 min count as luckier).
- **The books.** Water: M₀ = M + M_rain + M_evap + δM. Drops: N₀ = N + N_rain + N_evap + N_merge + δN. For the drop book the model
  counts two numbers it did not count before: `N0` (drops at the start) and `evapN` (drops that evaporated completely), added to
  `makeCloud` in `physics.cjs` without changing any line count or any result. Tolerances: 10⁻⁹ of M₀ and 10⁻¹² of N₀ (N is about
  10¹⁶, above 2⁵³, so float64 sums can miss by a drop).
- **The hooks** are `datahooks.js`, inlined by the build after `app.js`, and read only stored variables: `probe` pins the drop
  under the pointer (the largest class within 6 px, then the nearest) or else the 50 m cell; `check` recomputes from stored inputs
  (sums over the stored super-droplets, the stored efficiency table, the model's own formulas called with the stored air); `drawn`
  reads back the dot of a super-droplet (alpha first, then the class colour; a dot covered by a later one says so), the cloud
  background of a region square, the readout words and the picture's size. A round is five cloud-minutes; it is refused in the last
  five minutes before the cloud stops at 45 min. Every word the hooks write goes through `T()`; the study has no German or Arabic
  page.
- **Markup.** The canvas sits in `#stage` with its caption `.stage__cap` (where the Read values switch goes); the template maps the
  site tokens the panel's stylesheet reads onto the study's palette, and `.plot > svg` keeps the charts' full-width rule off the
  panel's icons. The served page loads `sim.js` and `dataset.js` before its inline script and `datalog.js` after it, with
  `paper.css` and `data.css`; the standalone build has none of them and keeps its readouts through a bare stand-in store.
