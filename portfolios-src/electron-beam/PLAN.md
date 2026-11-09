# Project 07 · The Electron Beam, from Tip to Measurement — plan and brief for every session

Every session working on this project reads this whole file first, then `CLAUDE.md`, `AGENTS.md`, `notes/STANDARD.md`,
`docs/pages.md`, `docs/portfolios.md` and `docs/styles.md`. This file is the single source of truth for scope, aim, file
ownership and the hand-over contract. Written 9 November 2026 by the planning session (branch `ccr-cc3b1649-gefitf`).

## 1. Final aim (read this first)

Numa Koudsie (physics B.Sc., Leipzig) is applying to Applied Materials, Heimstetten near Munich, for two roles:
"Electron Optics & Multiphysics Simulation Physicist / Engineer (m/f/d)", job ID R2631003
(<https://jobs.appliedmaterials.com/job/heimstetten/electron-optics-and-multiphysics-simulation-physicist-engineer-m-f-d/95/102714041664>),
and "Physicist / Engineer (m/f/d) Particle Beam Technology / Semiconductor Control", job ID R2628679
(<https://jobs.appliedmaterials.com/job/heimstetten/physicist-engineer-m-f-d-particle-beam-technology-semiconductor-control/95/101388475328>).
This project is attached to that application as his portfolio. A hiring engineer who builds electron-beam columns will read it.
It must be correct, honest and self-explanatory, and show that Numa can build a charged-particle system from first principles,
check it against theory and published data, and say how sensitive it is to each parameter.

What R2631003 asks for (the project should visibly answer it): simulate e-beam columns and electron-optical components (their
tools: Opera, CST, COMSOL, Ansys, custom Python); analyse and optimise electron-optical performance from theory; tolerance,
sensitivity and process-window analysis; design for manufacturability; Python simulation and analysis tools; correlate models
with experiment; present results as clear conclusions. R2628679: define system requirements and specifications; collect and
analyse data, statistically valid experiments; electron optics, SEM, UHV and high voltage.

Never claim any affiliation with Applied Materials, never use its logos, never claim to model its actual tools. Cite its public
statements as sources only. The cover letters are done (Google Docs in Numa's Drive); no session edits CV or cover letters.

## 2. Where it goes and how it is built

- A **project** on the Projects page `public/portfolios.html`, number **07** (entries 01 to 06 exist; nothing on the site
  simulates charged particles yet). Not a simulation figure.
- Source: `portfolios-src/electron-beam/` (not served). Generated output: `public/portfolios/electron-beam/index.html`
  (one page, lecture notes in chapters, simulations running in the browser, figures as inline SVG, maths typeset at build time
  with KaTeX 0.16.11), plates in `public/portfolios/electron-beam/fig/`.
- Pattern to copy: Iron, Cotton and the Head (`portfolios-src/impact/build.py --site`: template + text + physics between
  markers + datahooks; the site's security policy and referrer tag after the charset line; site fonts; back link to Projects).
  Build-time KaTeX and the "every quoted number is computed" check from Droplet Collection
  (`portfolios-src/droplets/tools/katex_render.cjs`, `checks/check_numbers.cjs`). Fonts via `portfolios-src/site_fonts.py`.
  No Google Fonts, no outside requests.
- Registration: one `<article class="proj" id="electron-beam">` in `portfolios.html` with `proj__num` 07, band, title,
  abstract, buttons, `proj__tally`, parts, four plates; a section in `docs/portfolios.md`; then `python3 tools/inventory.py`,
  `python3 tools/redirects.py`, `python3 tools/i18n/build.py --check` (the Projects page has German and Arabic copies, so the
  entry needs translation tables in `i18n/<lang>/`; the project page itself may stay English-only).
- Data panel: follow `docs/scripts/dataset.md` and the skill `phyein-usul-data-panel` if the page carries a store; a
  simulation writes each number into the store at the line that computes it; the display only reads.

**Files that may change:** `portfolios-src/electron-beam/` (new), `public/portfolios/electron-beam/` (generated),
`public/portfolios.html` and its plates, `docs/portfolios.md`, `docs/files.md` (via `tools/inventory.py`, plus rules in
`tools/inventory.py` for the new files), `public/_redirects` (via `tools/redirects.py`), the home page project list if projects
are listed there, translation tables only for the Projects page entry. Touch no other project or figure. Never touch the
out-of-bounds apps named in AGENTS.md.

## 3. The question the project answers, on its first screen, in plain words

Why does anyone build an electron beam, and what must the machine deliver? Chips have features a few nanometres wide and one
defect can kill a chip, so every step is inspected and measured. Light cannot resolve such features (diffraction limit about
λ/2NA) and averages over many of them; the electron wavelength is picometres at kilovolt energies. The beam is a probe scanned
over the wafer; what comes back (secondary and backscattered electrons) gives edge position, height and material. The machine
must deliver at once: a spot thinner than the feature, enough current for a clean picture (shot noise), a beam gentle enough
for fragile resist but able to reach buried layers, and speed. These demands trade against each other: a smaller spot means
less current. Cold field emission gives a very bright narrow source, at the price of extreme vacuum and a cleaning cycle,
because one stray atom changes the emission. The project is a chain of chapters that exposes these trade-offs.

Applied's public statements, verified 9 November 2026 (cite as public claims only):
- PROVision 10 page <https://www.appliedmaterials.com/us/en/product-library/provision-10-ebeam-metrology.html>: cold field
  emission column, "up to 100 million accurate, actionable measurements per hour", Elluminator "captures 95% of back-scattered
  electrons", high-energy modes "hundreds of nanometers deep", low-energy modes for EUV resist.
- Press release of 14 December 2022 (Semiconductor Digest,
  <https://www.semiconductor-digest.com/applied-materials-breakthrough-in-electron-beam-imaging-technology-accelerates-development-of-the-worlds-most-advanced-computer-chips/>):
  TFE runs above 1500 °C; CFE narrower beam, 10× imaging speed; vacuum "well below 1×10⁻¹¹ millibar" (= 10⁻⁹ Pa), two to
  three orders better than TFE; "a single atom" on the tip can partially block emission; cyclical self-cleaning.
- Also to read: the SEMVision H20 and G7C pages on appliedmaterials.com.

## 4. The chapters (each: everyday picture, physical setup with drawn parts, full derivation, simulation with tunable symbols, hand-over to the next)

0. **The goal.** The question above, with a drawn comparison of feature size, optical wavelength and electron wavelength.
   Plus a short **reading guide for the reviewer** at the very top (no jargon): what the project shows, what it models, what it
   leaves out (no field solver, no aberration-corrected optics, no proprietary detail), where each number comes from.
1. **A free electron in fields.** Thomson's cathode-ray tube, parabola in E, circle in B, crossed fields, e/m, helix in an
   axial B. Lagrangian L = −mc²/γ − qφ + q v·A (q = −e), Euler–Lagrange → Lorentz force, canonical momentum p = γmv + qA,
   Hamiltonian, energy conservation in static fields, why B does no work, the non-relativistic limit and the size of the
   correction. Integrators: Boris pusher (derive the rotation, why it keeps energy and gyroradius), RK4 order and error, both
   against the exact helix. Overlay: Thomson 1897 e/m against CODATA.
2. **The source.** Thermionic (Richardson–Dushman), Schottky, cold field emission. Schottky–Nordheim barrier (triangular with
   image charge), WKB transmission, supply function, Fowler–Nordheim formula with every symbol (Forbes' v(f) approximation),
   tip field F = V/(k r), FN plot, energy spread and reduced brightness of each source. Vacuum and contamination:
   Hertz–Knudsen flux, coverage rate equation with sticking and desorption, time-to-monolayer against pressure, emission as a
   function of coverage (a stated model assumption), the cleaning cycle. Overlay: a published FN data set for a tungsten tip
   (e.g. Dyke & Dolan 1956; find and read it).
3. **Acceleration, current, brightness, energy spread, relativistic correction.** λ(V) relativistic, V* = V(1 + eV/2mc²),
   brightness and reduced brightness, Liouville. Overlay: CODATA constants; published B_r of CFE/Schottky sources.
4. **The lens.** From the helix to a magnetic lens. Static Maxwell, axial expansion B_r = −(r/2)B′(z) + … from div B = 0 and
   curl B = 0; Busch's theorem from canonical angular momentum; paraxial ray equation r″ + (e/(8mV*))B²r = 0 in the rotating
   frame; Glaser bell field B(z) = B₀/(1 + (z/a)²) with its exact solution; focal length, image rotation, thin-lens limit, lens
   matrix, Lagrange invariant, brightness conservation. Electrostatic lens and plates by Laplace with fringe fields. Ray tracing
   through source, condenser and objective.
5. **The spot.** Spherical ½C_sα³ (state the convention), chromatic C_cα(ΔE/E), diffraction from the Airy pattern, geometric
   source image; quadrature sum and its known weakness (Barth & Kruit 1996), optimum aperture in closed form, minimum spot;
   Scherzer's theorem stated with its assumptions; cold-field versus thermal (Schottky) source.
6. **Scan and hit.** Deflectors; Monte Carlo of scattering in resist and silicon (screened Rutherford or Mott, mean free path,
   Bethe stopping power, continuous slowing down), range (Kanaya–Okayama, converted to SI), interaction volume, SE and BSE
   yields against energy and material, why edges look bright, landing energy; charging and resist shrinkage named as effects.
   Overlay: measured ranges and yields (e.g. Joy's database of electron–solid interactions).
7. **Detect and measure.** Synthetic line-and-space and fin-like profile, edge brightening, Poisson shot noise, SNR against
   dose, edge detection on a noisy profile, CD extraction and its uncertainty (error propagation and Monte Carlo, the 1/√N law),
   throughput relation, collection fraction η as a tunable symbol (Applied's 95 % quoted as a public claim only).
8. **The whole machine.** All chapters connected, all parameters as sliders, live readout of spot size, current, dose, CD
   uncertainty, measurements per hour; sensitivity table (Jacobian, normalised sensitivities); tolerance Monte Carlo over tip
   radius, lens current, pressure, alignment; process-window plot.
9. **What an interviewer for this role will probe**, as prose (deriving the paraxial equation, what limits resolution, how a
   simulation is checked against measurement, which parameter matters most), each pointing to the chapter that answers it.

**Gaps the text must close, inside the running text where they arise (never as Q&A):** why electrons and not X-rays or ions;
how a magnetic field can focus at all (Busch's twist turned into an inward push ∝ r, like a glass lens); why a round static
lens can never be perfect (Scherzer); why the cold tip is bright but fragile; what the beam actually sees (SE from the top
nanometres, edge brightening, BSE from deeper layers); how a width is read from a blurred noisy profile and how precise that
is; charging and damage, why low landing energy matters; why speed and statistics over the whole wafer matter to a fab;
where quantum mechanics enters (wavelength, tunnelling, shot noise).

**Correlate with experiment** in at least three chapters (1, 2, 6 at least), label the source, say plainly where model and
data differ.

**Python reference:** `portfolios-src/electron-beam/ref/` holds a readable NumPy reference solver for chapters 1, 2, 4, 5,
6 and 7. The project shows that its numbers and the browser simulations agree, and links the code.

## 5. How to write (Numa's rules)

Start from the physical setup (what each part is, how it connects, how things move with and without the input), then derive
every term step by step from where it comes from, backed by real sources or worked examples. Never skip a step or bring in a
term from nowhere; Numa counts skipped steps as lying. Keep every physical parameter as a symbol in the derivations and
tunable in the simulations. SI units only. Draw the mechanical parts (tube, plates, coils, tip, lens, deflectors, detector,
wafer). Lecture notes in the house format (Latin Modern, KaTeX, numbered equations and figures), Taylor's way of teaching
(`notes/STANDARD.md`, verdict of 21 October 2026): patient "we", every step with its reason, "Key result" boxes, numbered
worked examples, ★ for skippable heavy maths with results restated. No Q&A, no AI tells. Design only as `docs/styles.md`
allows, no new fonts. Check every derived formula with SymPy (or Wolfram) and numerically, and show the check on the page.
Cite a source for every formula; from a book, give book and chapter and re-derive the steps.

**Books** (Numa's permission, read-only; never edit, move, share or trash): Google Drive folders EP4
(`1Vn7gUpaKlPakuiV-Gd-sIc-XUGokF0oE`, `19LyJVyYGVF8fj__C2edOj0FKRRI0-Z6h`) and Oldenburg (`1I2vlAk6M0gOxu-PX1HfeqyrqVXE_AmU_`;
subfolders seen 9 November: Electrodynamics `1E4o4bETZcK8MbeSE8GFE88AxxIvVecTl`, Q.M lecture `1BPyfeGPVK4qszxeCfFjoYToa3L4nUiv6`,
Numerics `1JXygIKx-MKvu2Dl4_iBxZkF_RyzHMI5z`, LabProject, Matlab; more on later pages). Known: Haken & Wolf, *The Physics of
Atoms and Quanta*; *atoms, molecules and photons*; Griffiths, *Introduction to Quantum Mechanics*; *Concepts in Thermal
Physics*. If the Drive connector is unavailable in a session, use open sources and say so. Standard electron-optics texts to
find: Reimer, *Scanning Electron Microscopy*; Hawkes & Kasper, *Principles of Electron Optics*; Orloff (ed.), *Handbook of
Charged Particle Optics*; Szilagyi, *Electron and Ion Optics*.

## 6. The hand-over contract (written by the scaffold session first; every chapter codes against it)

`portfolios-src/electron-beam/contract.json` fixes symbol names, SI units and the interface of each stage:

| Stage | In | Out |
|---|---|---|
| ch2 source | tip radius r_t, extraction voltage V_ex, work function φ, temperature T, pressure p, time since cleaning | emission current I_e, reduced brightness B_r, energy spread ΔE, virtual source size d_v |
| ch3 gun | acceleration voltage V_acc (landing V_land) | E₀, λ, γ, V* |
| ch4 lenses | coil excitation NI, half-width a, distances | magnification M, f, C_s, C_c, image rotation |
| ch5 spot | the above, aperture half-angle α | probe diameter d_p (with convention), probe current I_p |
| ch6 sample | E_land, material (Z, A, ρ, J) | δ_SE, η_BSE, range R, interaction volume, signal spread |
| ch7 measure | d_p, I_p, dwell t_d, pixels, collection η_c, profile | SNR, σ_CD, measurements per hour |

Shared physics core: `physics/core.js` (constants CODATA 2018, units), owned by the scaffold. Each chapter's solver is
`physics/chNN.js`, a pure module that runs in the page and in Node; the Python reference `ref/chNN.py` mirrors it.

## 7. Sessions, ownership and order

12 sessions in all, at most 5 at once: 1 coordinator and 11 workers in three rounds. Round 1 (chapters 0–2), round 2 (3–5) and
round 3 (6–9) are each finished, tested and published before the next round's chapter work is merged.

| Session | Round | Owns (writes only these) | Branch |
|---|---|---|---|
| Coordinator | all | integration, `public/portfolios.html` entry, `docs/portfolios.md`, inventory/redirects/i18n, merges, live check, final editor pass for one voice | `ccr-cc3b1649-gefitf` |
| S1 Scaffold | 1 | `build.py`, `template.html`, `contract.json`, `physics/core.js`, `checks/` harness (parity, numbers, Playwright), `README.md`, inventory rules | `eb/scaffold` |
| S2 Librarian | 1 (stays) | `sources/` (bibliography.md with book+chapter+page, Drive files read, published data digitised into `data/` with provenance) | `eb/librarian` |
| S3 Chapters 0+1 | 1 | `text/ch00.py`, `text/ch01.py`, `physics/ch01.js`, `ref/ch01.py`, `derive/ch01.py`, `data/ch01/` | `eb/ch01` |
| S4 Chapter 2 | 1 | same pattern, ch02 | `eb/ch02` |
| S5 Chapter 3 | 2 | ch03 | `eb/ch03` |
| S6 Chapter 4 | 2 | ch04 | `eb/ch04` |
| S7 Chapter 5 | 2 | ch05 | `eb/ch05` |
| S8 Chapter 6 | 3 | ch06 (Monte Carlo; may run stored runs if the browser is too slow, and say so) | `eb/ch06` |
| S9 Chapter 7 | 3 | ch07 | `eb/ch07` |
| S10 Chapter 8 | 3 | ch08 (whole machine, Jacobian, tolerance MC, process window) | `eb/ch08` |
| S11 Chapter 9 + reading guide | 3 | `text/ch09.py`, the reading guide text | `eb/ch09` |

A worker never edits a file it does not own. If it needs a change in a shared file (template, core, contract), it writes the
request in `notes/electron-beam/requests.md` on its branch and tells the coordinator. Workers push their own branch only; the
coordinator merges. Chapter workers may start before the scaffold lands by coding against section 6; they rebase on the
scaffold when it is merged.

## 8. Definition of done (each chapter, each round)

1. Every formula derived step by step, cited, checked by SymPy (`derive/chNN.py` output shown on the page).
2. Browser solver equals Python reference within a stated tolerance (float32/float64 gaps named as such).
3. Every number in the text is computed (`checks/check_numbers`), every unit SI, at least one limiting case checked in text.
4. Published data overlaid where the chapter calls for it, with source and the gap stated.
5. Playwright at 360, 390, 1024, 1440 px: 0 KaTeX errors, 0 page errors, no sideways scroll, no request outside the site;
   screenshots kept in `notes/electron-beam/shots/`.
6. Coordinator per round: build (`npm run build`), browser test of the served page, docs updated, inventory, redirects,
   i18n --check, merge into `main` (Numa's rule since 3 November 2026: finished, checked against other sessions' work on
   `main`, tested in a real browser → merge and publish without asking), verify <https://phyeinusul.com/portfolios/electron-beam/>.
7. At the end the coordinator sends Numa the link, a short plain list of what the project shows and what it leaves out, and
   three honest sentences he can put in his application.

## 9. Constraints every session keeps

Commit messages end with the attribution lines the session is given; no model names in commits or files. Never push to
`main` except the coordinator's merges. Never touch other projects or figures. Never claim Applied affiliation. Ask Numa only
when readings differ materially, one question at a time; otherwise decide and report. Report in plain short sentences,
marking facts (with a handle), inferences and opinions.
