# Fig. 15 of Phyein Usul: resonant tunnelling, built on the stored solutions of Fig. 14

Brief written on 13 November 2026 by the session that built Fig. 14, on the owner's instruction, for the session that builds Fig. 15.

You are taking on a research project, the way a professor hands one to a postdoc. Read all of this before you touch anything. It is
long because every part of it matters to the owner of this website, a physicist (BSc, computational and theoretical physics). Over the
last day the owner has been badly let down by sloppy work: skipped steps, claims quoted from memory, untracked jobs, broken
animations. Your job is to do this one properly, top to bottom, and to be honest at every step.

## 0. Where you are

- **The site:** Phyein Usul, https://phyeinusul.com, built from this repository's `main`. Cloudflare deploys every push to `main`
  by itself. GitHub Pages mirrors it.
- **Read these first, whole, before any work:**
  - `CLAUDE.md` (method: persist, read primary sources whole, measure, build when the request is clear, plain words);
  - `AGENTS.md` (layout, ownership, data panel, folds, i18n, inventory);
  - `docs/kaggle-pipeline.md` (how runs are computed on Kaggle and stored, "Storage: on the website and with the notebook, named
    by the date of generation");
  - `notes/STANDARD.md` (the standard for lecture notes);
  - `docs/styles.md` (house design);
  - `docs/simulations/fig14-schrodinger-sphere.md` (the previous figure, its data, and every mistake made and fixed on it).
- **The previous figure, Fig. 14** (`public/simulations/schrodinger-sphere.html`) shows an electron wave packet meeting barriers in
  3D. Its stored Kaggle runs are in `public/data/schrodinger-sphere/`:
  - `generations.json` lists the dated generations;
  - each generation has an `index.json` with every file's SHA-256 and the Kaggle notebook, version and commit.
- **Do not edit Fig. 14's files.** Another session (its "mother session") owns them and is now fixing how the barriers are drawn.
  You only *read* its data.
- **Skills to load and follow** (Skill tool), each when its moment comes:
  - `anthropic-skills:phyein-usul-physics-content`
  - `anthropic-skills:phyein-usul-data-panel`
  - `anthropic-skills:phyein-usul-bookkeeper`
  - `anthropic-skills:kaggle-gpu-run`
  - `anthropic-skills:phyein-usul-i18n`
  - `anthropic-skills:phyein-usul-smooth-site`
  - `anthropic-skills:wolfram-language` (use the Wolfram MCP tools: `WolframLanguageEvaluator`, `WolframContext`, `WolframAlpha`)
  - `anthropic-skills:sympy`
  - `anthropic-skills:theoretical-physicist`
  - `anthropic-skills:physics-model-loop`
  - `anthropic-skills:verification-before-completion`
  - `anthropic-skills:pushback-proof-answers`
  - `anthropic-skills:web-tool-ladder`
  - `anthropic-skills:unslop`
  - `anthropic-skills:feynman-technique` (for the lecture note)
- **Agents** (`.claude/agents`): `physics-teacher`, `referee`, `derivation-checker`, `walkthrough-keeper`. Use them for the blind
  review of the note at the end, as Fig. 14's note was reviewed.

## 1. The physics question, and why it is the right one

The Schrödinger equation is linear. A solution computed once is a basis to build on, so we should not pay for a new full simulation
every time we want a new system. The owner's demand: **generate new physics from the data we already have, by applying exact rules
to it, and say clearly where that derived data lives and how it was made.**

The cleanest exact rule of this kind is the composition of one-dimensional scattering by transfer matrices:
- one barrier is fully described, at each energy, by its transmission and reflection amplitudes, or equivalently by a 2 × 2 matrix;
- several barriers that don't overlap are the product of their matrices and of free-flight phase matrices between them.

Two barriers a few nanometres apart make a **resonant tunnelling diode** (RTD), a device in use today:
- the fastest solid-state electronic oscillators, over 1 THz (TU Wien reported 1.46 THz in 2014; find newer records yourself);
- the negative differential resistance studied by Tsu and Esaki (1973) and Chang, Esaki and Tsu (1974), and Sollner et al. (1983);
- the injector of quantum cascade lasers;
- many barriers form superlattices with minibands.

This figure must lead the reader, top to bottom, from the equation to that device: its transmission peaks, the lifetime of the
trapped state, and its current-voltage curve with the region of negative slope.

**The primary source for the method:** D. J. Griffiths and C. A. Steinke, "Waves in locally periodic media", Am. J. Phys. 69, 137
(2001). Free copy: https://physics.csuchico.edu/ayars/427/handouts/Griffiths2001.pdf. Read Section II whole, and Section V (the Dirac
case) at least once. Their equation numbers are your spine.

The previous session checked in Wolfram:
- their Eq. 41 (rectangular barrier) against a solution from scratch: difference 0 symbolically;
- their Eqs. 16–18 (det M = 1, M = [[w, z], [z\*, w\*]]);
- their Eqs. 30–32 against a face-by-face solution for N = 1, 2, 3, 5, 10, at energies below and above the barrier: agreement to
  10⁻¹⁶.

Redo these checks yourself; do not take them on trust.

**Literature to find and read** (primary sources, full text where it is reachable; the web-tool-ladder skill lists the roads):
- Tsu & Esaki, Appl. Phys. Lett. 22, 562 (1973);
- Chang, Esaki & Tsu, Appl. Phys. Lett. 24, 593 (1974);
- Sollner et al., Appl. Phys. Lett. 43, 588 (1983);
- a modern review of RTD terahertz oscillators (Asada and Suzuki's group, or TU Wien / Feiginov);
- on factorising the 1D scattering matrix: Aktosun, J. Math. Phys. 33, 3865 (1992), and Aktosun, Klaus & van der Mee, J. Math.
  Phys. 37, 5897 (1996).

Cite only what you have read. If something is unreachable, say so and state the road you tried.

## 2. What to build, part by part

### Part A: the derivation, from the differential equation up. No step skipped.

The owner rejected three previous attempts because they skipped steps and threw symbols at the reader. So:
- Derive from −(ħ²/2m)ψ″ + Vψ = Eψ:
  - why ψ and ψ′ are continuous at a step;
  - the general solution in each flat region, oscillating or decaying, with every symbol defined in words when it first appears;
  - the 2 × 2 matrix of one edge, then of one barrier, by substituting one set of linear equations into the other (say in words that
    this substitution *is* matrix multiplication);
  - reading t and r off the matrix by a stated experiment (incoming 1 from the left, nothing from the right);
  - time-reversal symmetry giving the conjugate pattern, and conservation of probability giving det = 1, each shown on numbers;
  - two barriers as a product, then the same result recovered as a sum over round trips (geometric series): show both and show they
    agree;
  - the resonance condition, the Breit–Wigner (Lorentzian) shape near a peak, the width Γ, and the lifetime τ = ħ/Γ of the trapped
    state (derive it; do not quote it);
  - N barriers via Cayley–Hamilton and Chebyshev polynomials (Griffiths & Steinke Eqs. 24–35), bands and gaps.
- **Carry one running numerical example through the whole note**, the way a good textbook does. The owner liked this one:
  - E = 1, V₀ = 3, width 1, in ħ = m = 1 units;
  - one barrier transmits 6.33 %;
  - two barriers with centres 2.343 apart transmit 100 %; 3.454 apart, 0.107 %;
  - the partial sums over round trips reach 0.4 %, 1.5 %, 10.5 %, 26 %, 56 %, 93 %, 99.7 % after 0, 1, 5, 10, 20, 50, 100 round
    trips.

  Recompute every one of these numbers yourself in Wolfram before using it.
- **Then switch to real units**, GaAs/AlGaAs: effective mass 0.067 mₑ, barrier height from the conduction-band offset (find it in a
  primary or review source), barrier and well widths in nm. Show the same physics there: peak energies in meV, Γ in meV, τ in
  femtoseconds to picoseconds. Every material number gets a cited source.
- **Verify every equation** with Wolfram (symbolic where possible, numeric otherwise) and independently with SymPy or NumPy. The
  `derivation-checker` agent rechecks the note at the end.

### Part B: data generated from data. This is the heart of the project.

**Basis (parent data):** the 585 flat-wall runs of Fig. 14, `public/data/schrodinger-sphere/2026-11-12/flat/`.
- Each file is `SPHC`: a JSON header, then zlib-compressed levels of |ψ| and arg ψ.
- The levels are 8-bit: |ψ| in 255 levels of the first frame's peak, and the phase in 256 levels.
- Each file holds the cut ψ(x, ρ) of the 3D wave on 128 × 64 points, 0.5 a apart, x from −32 to 31.5, 48 frames.
- Physics: ψ = χ(x) g(y) g(z), with χ computed by Crank–Nicolson (Δx = 0.05 over a 200 a line), and g the free Gaussian spread.
  The note of Fig. 14, equations 22–24, and `tools/kaggle/schrodinger-shapes/flat.py` give the exact construction.
- The grid of runs: 9 energies (0.5 … 4.5), 13 heights (wells −4, −2, −1; 0 … 8; hard wall), 5 thicknesses (0.5, 1, 1.5, 2, 3).
  Packet σ₀ = 3, start x₀ = −14.

**Step B1: extract the single-barrier amplitudes t(k) and r(k) from the stored runs.**
- At late times the transmitted and reflected packets are free. Then
  - transmitted part: χ(x, t) ≈ ∫ φ(k) t(k) e^{i(kx − k²t/2)} dk / √(2π);
  - reflected part: the same with r(k) e^{−ikx}.
- So a Fourier transform of the stored late-time cut, beyond the wall and before the wall, divided by the known incoming spectrum
  φ(k) and the known free phase, gives t(k) and r(k) over the band where |φ(k)| is not small.
- Steps you must handle:
  1. Divide out g(0, t) (the cut is at ρ = 0).
  2. Undo the 8-bit levels.
  3. Choose a frame where the packets have left the wall.
  4. Choose the window.
  5. Propagate the error.
- Overlapping energies give overlapping k-bands; stitch them and show the overlaps agree.
- **Compare with the exact single-barrier formula** (`T_plane` in `flat.py`, and Griffiths & Steinke Eq. 41). Report the error in
  |t|² and in the phase of t, band by band.
- **Be honest.** If the 0.5 a grid and 8-bit levels make the extraction too coarse for some bands, say so, quantify it, and use
  those runs as a check on the exact formula rather than as a source of numbers. The owner wants the truth, not a pretty claim.

**Step B2: compose the double barrier from the single-barrier data.**
- t₂(k) = t_A t_B / (1 − r̃_A r_B), with the shift rules for a barrier moved by s (t unchanged, r → r e^{2iks} from the left,
  r̃ → r̃ e^{−2iks} from the right).
- Do this twice and compare: once with the extracted t(k), r(k), once with the exact ones.

**Step B3: the time-dependent animation without a new time-dependent solve.**
- Build the stationary scattering states of the double barrier in all five regions from the transfer matrices.
- Superpose them with the incoming packet's spectrum: ψ(x, t) = ∫ φ(k) ψ_k(x) e^{−iE_k t/ħ} dk.
- This is exact for V ≥ 0, where there are no bound states, as long as the initial packet lies wholly left of the barriers. State
  that condition, and quantify the error from the packet's tail overlapping the barrier at t = 0.
- For wells there are bound states: either restrict to barriers or add the bound states, and say which you did.
- **Fact the note must show:** on resonance, part of the packet is trapped between the walls and leaks out exponentially with
  lifetime τ = ħ/Γ. Measure τ from the animation's data (probability between the walls against time, fitted) and compare with Γ from
  the T(E) peak.

**Step B4: independent check on Kaggle.**
- Solve the double barrier directly with a 1D time-dependent solver (Crank–Nicolson with the fourth-order Laplacian, the same scheme
  as `flat.py`) for a chosen subset of cases.
- Compare ψ(x, t) frame by frame with the reconstruction from B3 (L² error, transmitted and reflected probabilities,
  trapped-probability curve).
- Also run on Kaggle's CPU: the bias sweep for the current-voltage curve. A bias makes the potential a sloped line. Treat it as a fine
  staircase of steps composed by transfer matrices, and check convergence as the staircase gets finer. Airy functions are the exact
  alternative: do both and compare.
- The current comes from the Tsu–Esaki formula: J ∝ ∫ T(E, V) [f_L(E) − f_R(E + eV)] dE, with Fermi functions at a stated
  temperature. Read Tsu & Esaki before you use it; derive the supply function, state every assumption (coherent transport, no
  scattering, no charge build-up) and what it leaves out.

**Where the derived data lives: a distinct, documented place.** The owner's explicit demand: data generated from other data must have
its own place and its own provenance.
- New tree `public/data/resonant-tunnelling/` with its own `generations.json` and dated folders `YYYY-MM-DD/`. Inside each, separate
  subfolders, each with an `index.json`:
  - `derived/` for data computed from the Fig. 14 runs (B1–B3);
  - `kaggle/` for new runs computed on Kaggle (B4).
- Every derived file's index entry names its **parents**: generation, file name and SHA-256 of every Fig. 14 run it was computed
  from, plus the script and commit that computed it.
- Every Kaggle file's entry names its notebook, version and commit, as `docs/kaggle-pipeline.md` requires.
- Add a section **"Derived data: generated from stored runs"** to `docs/kaggle-pipeline.md`, describing this layout as the rule for
  every future figure.
- Scripts go in `tools/kaggle/resonant-tunnelling/`: extraction, composition, reconstruction, the notebook builders, and the packers
  that write `public/data/...`. The page computes nothing it can read from the store.

### Part C: the page

- `public/simulations/<slug>.html` (choose a short slug, e.g. `resonant-tunnelling.html`). Check `public/scripts/catalog.js` for the
  next free figure number; it should be Fig. 15.
- Register it as `AGENTS.md` says: catalog entry, thumbnail, Fig. links on every simulation page, redirects (`tools/redirects.py`),
  inventory (`tools/inventory.py`), German and Arabic pages (`tools/i18n/build.py`, phyein-usul-i18n skill).
- **What the reader sees:**
  1. **The main animation:** the packet meeting two barriers in 1D (|ψ|² and Re ψ, with the potential drawn as a solid, static
     landscape that never moves with the wave), played smoothly. The owner judged Fig. 14's first animation "horrible, glitches and
     slow". On Fig. 14 the fix was to play stored frames with interpolation in the frame turning at the energy E
     (ψ(t₀ + τ) = e^{−iEτ}[(1 − s)ψ₀ + s e^{iEΔt}ψ₁]), with heavy work in Web Workers and no slow-downs. Here, B3 gives ψ at any t
     analytically from stored spectra, so the motion can be exact at every screen frame. Prefer that.
  2. **Controls** for energy, barrier height, barrier width, gap and bias, with stops tied to stored data, as the other Kaggle
     figures do (`scripts/kaggle-flow.js`).
  3. **T(E)** with its resonances marked; **the trapped probability against time** with the exponential fit; **the I–V curve**
     with its negative-slope region; and a **3D height-sheet view** of |ψ(x, t)|² over the (x, t) plane, a space-time picture in the
     meshed-sheet style the owner liked on Fig. 14.
  4. **A real-units panel** for a GaAs/AlGaAs diode: nanometres, meV, femtoseconds, kA/cm².
- **The data panel** (phyein-usul-data-panel and bookkeeper skills): every number shown is written into the store where it is
  computed and only read for display. Prove the pipeline three ways (stored value, formula recomputed from stored inputs, pixel read
  back), as `CLAUDE.md` requires; a read-back test checks alpha before colour.
- **The lecture note** (`<article class="paper" id="paper">`, `notes/STANDARD.md`):
  - motivate from everyday experience first: light in double glazing, an echo between two walls;
  - then the model, then the mathematics, every symbol dissected, with the running example;
  - then the method and the data pipeline, including where the derived data lives and how it was made from Fig. 14's runs;
  - then the device, what the model leaves out, and further reading;
  - numbered equations and figures, inline SVG charts in the house style;
  - no question-and-answer format.
- **A section linking to the Electron Beam project** (`public/portfolios/electron-beam/`, source in `portfolios-src/electron-beam/`).
  Read its chapter 1 (field emission) and chapter 2 (energy spread) whole. Field emission is tunnelling through the surface barrier
  tilted by the applied field (Fowler–Nordheim). Show, with your staircase transfer matrices, the Fowler–Nordheim transmission
  through a triangular barrier, and compare it with the chapter's own formula and numbers. If adsorbates or tip states make resonant
  field emission plausible, find the primary literature and show it as a double-barrier case. Don't edit that project's files; link
  to it.

## 3. Rules learned the hard way on Fig. 14. Follow every one.

1. **Kaggle:**
   - Every GPU launch needs the owner's explicit yes, given in chat for that exact run, with its bill: runs × cells × steps ×
     measured time per cell-step = GPU hours, and its share of the 30 weekly hours (read `get_accelerator_quota` first).
   - CPU notebooks need no GPU hours; prefer them for 1D work, which is all of this project.
   - Before any launch, you must have a progress tracker **you yourself can read while the job runs**. The Kaggle connector returns
     logs only after a session ends. So either split work into short notebooks that finish and report, or find and test another
     road before launching. Never launch something you cannot watch. If you cannot watch it, say so to the owner before launching,
     not after.
   - Write each run's result to disk the moment it finishes. Run pyflakes on the notebook text before sending. Test one tiny case
     end to end on the local machine before sending.
   - Check the **start state** of every run: the packet wholly outside every barrier at t = 0, and nothing left inside a hard wall.
     On Fig. 14, 243 runs had to be recomputed because a start wave began inside a barrier.
2. **Never claim from memory.** Every citation is to something you opened and read; every number comes from a computation you ran;
   mark statements to the owner as Fact (with its source or the command that checks it), Inference or Opinion. If you are unsure,
   say "I don't know" and how to find out.
3. **Measure, don't estimate:** run times, frame times, file sizes, error norms.
4. **Animation quality:**
   - smooth at every screen frame;
   - no stepping between stored frames;
   - no pauses while the page computes (Web Workers);
   - the potential is static and drawn as a proper solid;
   - nothing reacts to the pointer merely passing over it.
5. **Publishing (`CLAUDE.md`):** when a part is finished and tested in a real browser (headless Chromium, screenshots at 390 and
   1440 px that you have looked at), merge to `main` and verify the live page. Work on your own branch; merge `origin/main` first,
   as other sessions push to `main` too. Every change updates the `docs/` pages that describe the changed files.
6. **Talking to the owner:**
   - short plain sentences, metric units;
   - Fact / Inference / Opinion marked;
   - one decision asked at a time;
   - end each turn with "Where we are:" and "Next, if you say yes:";
   - never write the owner's name;
   - no apology floods, no flattery;
   - when you are wrong, say so in one line and fix it.
   The owner reads explanations critically and has rejected anything that skips steps. Explain every symbol where it first appears,
   with a worked example.
7. **Do not message other Claude sessions** unless the owner tells you to.

## 4. Order of work, and first reply

1. Read the files of section 0 and the Griffiths & Steinke paper.
2. Then, before building anything, send the owner one reply with:
   - a one-page plan: the figure's sections; the exact list of derived and new data, with file layout and sizes; which Kaggle
     notebooks (CPU), with run counts and measured or estimated times; how you will track them;
   - Part A's derivation as you intend to present it in the note, every step and symbol shown, the running example in it, verified
     in Wolfram, so the owner can judge its readability first;
   - a first measurement of Step B1 on two or three stored flat-wall runs: does the extraction of t(k) from the stored data work, and
     to what accuracy?
3. Then build, in the order A → B → C, publishing as each part is finished and tested.

Be the physicist the owner expects: careful, complete, honest about every limit, and proud of work that holds up to a hostile reader.
