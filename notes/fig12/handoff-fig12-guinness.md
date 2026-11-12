# active-memory handoff: Fig. 12 · A pint of Guinness on a one-wheel cart (phyeinusul.com)

**Handoff #1** · 2026-11-11 (state updated 2026-11-12) · Lineage: #1 (2026-11-11): mode model removed; particle solver debugged and retired; OpenFOAM route built (mesh, case, coupled cart); gates waiting on a GitHub Actions outage

## 0. Instructions for Claude (read first)

You are continuing work from a previous chat. That chat is gone; this file is the complete context and the source of truth.

1. Read this whole file before replying.
2. Follow sections 3 (Style), 4 (Hard rules) and 5 (Corrections) in every reply, for the rest of this chat. They override your defaults.
3. Use the values in section 8 exactly. Never round, re-estimate, or "correct" them.
4. Do not suggest anything listed in section 7 (Changed / rejected) again unless the user brings it up.
5. Code word: None active. If the user types /amcodeword, start every reply with the phrase they choose (default "Yes Boss!").
6. Your first reply: at most 5 lines covering the goal, the current state, and the next step (section 11). Mention any files from section 13 that were not attached. Ask the questions in section 12 if there are any. End with "Ready to continue with <next step>?" Then wait for the user's go.

## 1. Mission
- **Goal:** rebuild Fig. 12 (`public/simulations/beer-slosh.html`) so the page shows a pint of Guinness on a one-wheel cart computed by solving the real equations: incompressible Navier–Stokes with a free surface, in the real tulip glass (`public/scripts/guinness-glass.js`), whole glass, with friction, coupled both ways to the cart. All solving ahead of time on GitHub's free runners; the page only plays back computed solutions, identical on every device, and shows the system's phase space.
- **Done looks like (user's words):** "Still liquid stays still; energy is neither created nor lost beyond stated bounds; the proof set is written up; all rides are computed, checked and stored outside the repository's history; the page plays them smoothly on a phone, with phase space; the note is rewritten; the live site shows it."
- **Why it matters:** it is a figure on the user's physics site Phyein Usul, https://phyeinusul.com; "No mode model, no cylinder theory, no reduced model anywhere on the page. The solver is proven correct before any production run. Nothing costs money beyond the user's current plans."

## 2. About the user (as relevant to this work)
- BSc in Physics (computational and theoretical); reads Taylor, Feynman, Landau.
- Owns repository `Numa1997/SiteTest`; the site is built from `main` and served by Cloudflare (Workers Builds deploys every push/merge to `main`); GitHub Pages backup at https://numa1997.github.io/SiteTest/.
- On Cloudflare **Workers Paid**. Wolfram Cloud Basic account (Wolfram MCP evaluator available).
- Refer to the user as "the user"; never use their name.

## 3. Style & communication
- **Language:** English.
- **Tone:** plain, calm, honest; "no jargon without a one-sentence explanation"; physics pictures where they help, formulas only when asked; no flattery, no apology floods; when wrong, say so in one line and fix it.
- **Reply length:** short connected paragraphs; "One short progress line per milestone and an honest time estimate before anything long."
- **Formatting:** **no tables** in replies; metric (SI) units only; mark statements as Fact (with a handle: link, file:line, or command), Inference, or Opinion.
- **Working style:** engineering choices are Claude's; ask only real decisions, one at a time, with 2–3 options (cost and risk each), Claude's pick labelled as opinion, and the strongest case against in one line. During project work end each turn with `Where we are:` (one sentence) and `Next, if you say yes:` (one sentence).
- **Avoid:** long jargon-heavy walls of text; option lists in answer to a clear build request; asking the user to do physical work (filming etc.); computing or deriving from memory.

## 4. Hard rules (word for word)
1. "Do not derive or compute using your literaly training Either python symbols or Wolfram's compuattional abilities."
2. "I DON'T WANT THE IDIOTIC MODES MODEL OR THE CYLINDER STUCK BULLSHIT PROPER FLUID DYNAMICS WITH GRAVITY AND FRICTION INCLUDED"
3. "Drop the fitted-oscillator / mode model completely: no sloshing modes, no cylinder theory, no oscillator fits, no Green's-function compression. Remove that code from the working branch. Nothing of it gets published."
4. "The page only plays back the computed solutions ... It never solves the equations on the visitor's device. Every device shows identical results."
5. "Do not plan production runs on a grid whose own numerical losses rival the real friction."
6. Phase 1 gates: "each step is a gate; do not pass a failed gate". Gate 1.2 target: "numerical loss below one tenth of the real wall friction's loss in the same swing."
7. "Workflows start by hand only, never on every push. Remove any old workflow that still sends failure emails."
8. "Nothing that costs money without an explicit yes, with the amount stated first." Cloudflare R2 "only with the user's explicit yes".
9. "Plain English in short connected paragraphs; no jargon without a one-sentence explanation; no tables."
10. "Never use the user's name; say 'the user'."
11. "When every gate has passed and the page is tested, check against other sessions' work on main, merge into main and publish without asking. Check the live page yourself."
12. "Interpolate between neighbouring solutions only where you have shown the result changes smoothly; otherwise use the nearest computed one and say so on the page."
13. "Store solutions compactly ... Packs stay under 25 MiB each, with checksums." "Plan storage so the repository does not grow by gigabytes."
14. Branch: develop and push only on `ccr-76841c15-le08bl`; never push to another branch; no PR unless asked. Commit messages end with: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` and `Claude-Session: https://claude.ai/code/session_01DGmqimMUbGaehveJ4j5Q7W`; never put a model name in commit messages or code otherwise.
15. Out of bounds for writes: `numa-physics-lab-chatgpt-k0ixwk` and `physik-radar-xvy59b`.
16. CLAUDE.md (repo): data tables are a pipeline (store where computed, display only reads); nothing on a running figure reacts to the pointer merely crossing it; house design (Instrument Serif 400 titles, IBM Plex Sans text, IBM Plex Mono labels, no other font); lecture notes set like LaTeX (Latin Modern, KaTeX, numbered equations), motivate from experience, then model, then maths; no Q&A format; "A change is not done until the docs pages that describe the changed files say what the code now does."
17. After any file change: `python3 tools/inventory.py` then `--check` must pass (every file needs a rule in `tools/inventory.py`); `node tools/fig12/same.cjs` must print `sha256 4db045f0e864ac66` for the particle solver's default.

## 5. Corrections log
| # | Claude did | The user wanted |
|---|---|---|
| 1 | Asked the user to film a video for foam data | "Are you kidding me? Screw that then. Use public data, not necessarily visual or photo based." |
| 2 | Built a modal (finite-element modes + Narimanov–Moiseev) model as the page's stout | Real Navier–Stokes with gravity and friction; modes and cylinder theory removed entirely (rules 2–3) |
| 3 | Derived/quoted results from memory | Compute with sympy/Python or Wolfram only (rule 1) |
| 4 | Long, jargon-heavy explanation of the wall-stress derivation | "Right, dunno what you're on about" → short plain words, then build |
| 5 | Planned production with the particle solver while its numerical losses equalled real friction | Fix the solver first (rule 5) |
| 6 | Costed the half glass and included friction-off rides in production | Cost the whole glass; friction-off only in the convergence proof |
| 7 | Assumed Cloudflare free limit 20,000 files | User is on Workers Paid: 100,000 files per version, 25 MiB each |
| 8 | Said the lean "stayed at 10-12 mm" while energy drained 180 -> 20 uJ | Explain which: energy moved from the swing into a held surface shape and a sinking particle cloud |
| 9 | Used a table in a reply | No tables in replies |

## 6. Decisions
| Decision | Why |
|---|---|
| OpenFOAM 13 interFoam (`incompressibleVoF`) on GitHub runners | User's choice: particle solver's numerical damping (0.002–0.01) rivalled real wall friction (~0.005) |
| Road menu of about 10 roads: single bumps 5, 10, 15, 20, 25 mm, a kerb, a pothole, three periodic rows | User's choice; freehand road impossible to precompute |
| Production: 10 roads × 11 speeds (0.5–1.5 m/s) × 13 fills (80–140 mm) × 3 controllers × suspension on/off = 8,580 rides of 12 s, whole glass, friction on | User's direction |
| Controllers: open loop, speed PI, PI + road preview (slosh-feedback and LQR removed) | They carried a one-mode oscillator (cylinder theory) |
| Data outside git history: GitHub release files (<2 GiB each), fetched by the Cloudflare build, served as static assets | GitHub recommends repos <1 GB; static assets free and unlimited on Workers |
| Gates run on GitHub, started by committing `notes/fig12/of-request.json` | `workflow_dispatch` only works for workflows on `main` |
| Surface tension σ = 0 for now (Claude's choice, to be justified in the note) | σ = 0.045 caused spurious currents 17–27 uJ at rest vs ~2 uJ without; real effect on swing frequency ~1 % |
| Wall-fitted O-grid mesh resolving the 0.44 mm Stokes layer (no wall model) | No-slip friction straight from Navier–Stokes |

## 7. Changed / rejected
- Mode model (TulipModes/TulipNM, ModalFluid/NMFluid, modes_fem.py, nm.json) → removed completely (commit `106daff`).
- Particle (APIC) solver as production solver → retired to tests; OpenFOAM instead.
- Wall-stress model (Stokes-layer kernel, `wallFriction`) in the particle solver → kept as an option only; OpenFOAM resolves the layer.
- Freehand drawn road → road menu.
- `.github/workflows/fig12-3d.yml`, `fig12-modes.yml`, `fig12-validate.yml` (push-triggered) → removed.
- ❌ Cloudflare R2 (reads beyond 10 M/month cost money; not needed).
- ❌ Filming a video for foam data.
- ❌ FLIP, density projection (Kugelstadt 2019), volume correction, larger thetaMin as fixes for the particle solver (tested, none passed both gates).
- ❌ Running the WebGPU solver headless on runners (SwiftShader 329 ms/step at 4 mm; CPU far faster).
- Gate 1.1 fallback "use the largest time step that passes" → moot after the switch to OpenFOAM.

## 8. Data & facts (exact)
- **Guinness at 6 °C** (Benilov, Cummins & Lee, Am. J. Phys. 81, 88 (2013), arXiv:1205.5233, measured by the authors): ρ = 1007 kg/m³, μ = 2.06 × 10⁻³ Pa·s → ν = 2.05 × 10⁻⁶ m²/s. Gate runs used rho 1000; production uses 1007.
- **Glass** (`guinness-glass.js`): profile step dz = 0.0005 m, 296 points, rim at 0.1475 m, R(0) = 0.01631 m, R(rim) = 0.037474 m, Rmax = 0.039299 m; the rounded base widens 16.31 → 28.43 mm in the first 5 mm.
- **Stokes layer** at 3.4114 Hz with ν = 2.05e-6: 0.437 mm (Wolfram).
- **Wall stress** (Wolfram-derived, checked exact): τ(t) = ρ√ν ∫ K(t−t′) U̇(t′) dt′, K = 1/√(πt); Laplace τ̂/Û = ρ√(νs).
- **Old FEM damping predictions at 125 mm (now removed code, for reference only):** ζ_wall 0.00496, ζ_skin 0.00518, f11 3.4114 Hz.
- **Particle solver results:** viscosity-before-gravity fix (`81015f9`): circulation at rest 0–3 µm/s (was +1.0–1.1 / −0.5 mm/s); rest gate passes only at dt = 1.25 ms on 4 mm; quadratic APIC numerical damping 4 mm: 0.0025 (5 ms), 0.0055 (2.5 ms), 0.0095 (1.25 ms); 3 mm 0.0027, 2 mm 0.0011 (5 ms); frequencies 3.216 / 3.258 / 3.303 Hz on 4/3/2 mm.
- **OpenFOAM coarse mesh:** 32,208 cells (cart/gate cases ~32k), max skewness 3.6; levels coarse nq 12, nr 10, dz 0.004, hw 0.0003; medium nq 18, nr 14, dz 0.0027, hw 0.0002; fine nq 26, nr 19, dz 0.0018, hw 0.00014 (m).
- **OpenFOAM speed (local, coarse):** 0.19 s per step on one core; dt reaches 1 ms (maxDeltaT) at rest with max Courant 0.28; 0.5 s of stout in 99 s (1 core); coupled cart ride 0.4 s in 66 s on 2 cores → a 12 s ride ≈ 33 min on 2 cores (inference).
- **OpenFOAM rest (σ = 0, coarse, 0.5 s):** KE ≈ 2 µJ, four wall probes equal to 0.01 mm, mass drift ≈ 2.2 ppm in 0.5 s.
- **Frame sign:** OpenFOAM fvModel `acceleration` adds +ρα dW/dt; measured W rising +x lifted the front surface 3.4 mm in 0.1 s at 1.5 m/s² → table holds −V_glass.
- **First coupled ride** (coarse, bump x 0.75 m, h 0.015 m, L 0.2 m, 1 m/s, speed control): speed dip 0.965 m/s, lean 11.8 mm, stout's push +0.15/−0.12 N; particle solver same ride: 0.964 m/s, 9.5 mm, +0.14/−0.13 N.
- **Cart port check:** C++ vs JS identical to the last digit, 4 s, bumps (1.0 m, 15 mm, 0.3 m) and (2.2 m, 25 mm, 0.25 m), all three controllers with suspension.
- **Storage:** 7 kB per second of ride (3 mm surface, 484 columns, 0.1 mm steps, brotli) → ~100 kB per 12 s ride → ~0.86 GB for 8,580 rides.
- **Limits:** GitHub runners (public repo): 4 vCPU, 16 GB, 6 h per job, 20 jobs at once; GitHub repo ideally <1 GB, strongly <5 GB, push 2 GB, files >100 MB rejected; release assets <2 GiB each, no total limit; Workers Paid static assets 100,000 files/version, 25 MiB each, requests free and unlimited; R2 free 10 GB-month, 10 M class B reads/month.

## 9. People, terms & names
- **People:** the user (site owner; never named).
- **Terms:** "gate" = a pass/fail check in Phase 1 (1.1 rest, 1.2 free-swing energy, 1.3 whole glass + swirl, 1.4 friction incl. foam and cart, 1.5 spill/mass, 1.6 proof set); "ride" = one 12 s computed case; "lean" = front minus back wall surface height; "slip run" = slip walls + ν = 1e-9 (solver's own losses).
- **Names in use:** branch `ccr-76841c15-le08bl`; workflow `.github/workflows/fig12-openfoam.yml` ("Fig. 12 OpenFOAM runs"); request file `notes/fig12/of-request.json`; results `notes/fig12/of-runs/<name>/` (stoutMonitor.dat.gz, log.foamRun.tail.gz, walltime, case.json); OpenFOAM patches `glass`, `spill`, `atmosphere`; phases `stout`, `air`; monitors `stoutMonitor.dat` (t mass KE PE Px Py Pz outVolume h_front h_back h_left h_right) and `cartMonitor.dat` (t x vx zb vzb zw vzw i icmd xi Fx Fz ax az ml N slip za).

## 10. Work state
| Item | Status | Version / location | Notes |
|---|---|---|---|
| Mode model removal | done | `106daff` | page on the branch does not run until playback replaces it; `main` unchanged |
| Particle solver fixes/options | done | `public/scripts/stout-cart.js`, `81015f9` | options: whole, flip, densityProjection, quadratic, wallFriction, colGap |
| OpenFOAM mesh | done | `tools/fig12/of/tulip_mesh.py` | coarse checkMesh OK except none; medium/fine untested by checkMesh |
| OpenFOAM case template + builder | done | `tools/fig12/of/case/`, `make_case.py`, `run.sh` | `--forcing rest|tilt|cart`, `--wall noslip|slip`; must not run as root (use a user, e.g. `foam`) |
| Cart port + coupling | done | `tools/fig12/of/cart/cart.H`, `write_cart.cjs`, `test_cart.cpp`, `case/constant/fvModels.cart` | `3ef38b9` |
| Gate analysis | done | `tools/fig12/of/analyse_swing.py` (`--pair slip noslip`) | `410e59a` |
| Gate batch 1 (8 cases) | done, gates fail | GitHub run 43116028422, `notes/fig12/of-runs/` | 1.1 coarse still; medium mass +3.6e-4 (unexplained). 1.2 fails on all meshes: solver 0.0040/0.0033/0.0012, friction estimate 0.0036/0.0009/0.0067 (pairs had different time steps) |
| Time-step share | measured | local coarse slip 4 s | zeta = 0.0037 + 1.59/s x dt; 0.0016 at 1 ms, 0.0004 at 0.25 ms; the rest is the space grid |
| Gate batch 2 (4 cases) | running | `notes/fig12/of-request.json` | medium + fine, slip/no-slip, fixed 0.25 ms, 6 s; workflow now fails when a case does not reach its end time |
| Foam head, cart friction sources, spill check, swirl | not started | — | Phase 1.4–1.5, 1.3 |
| Pipeline packs/release/Cloudflare fetch | not started | — | Phase 2 |
| Playback page + phase space | not started | — | Phase 3 |
| Lecture note + docs | not started | `docs/simulations/fig12-beer-slosh.md` partly updated | Phase 4 |

Local OpenFOAM install (fresh container): `sudo sh -c "wget -q -O - https://dl.openfoam.org/gpg.key > /etc/apt/trusted.gpg.d/openfoam.asc"; echo "deb [arch=amd64] http://dl.openfoam.org/ubuntu noble main" > /etc/apt/sources.list.d/openfoam.list; apt-get update; apt-get install -y openfoam13 bc; useradd -m foam`.

## 11. Next steps
1. **Next action:** when batch 2 lands in `notes/fig12/of-runs/*-dt025/`, run `python3 tools/fig12/of/analyse_swing.py --pair <slip> <noslip>` for medium and fine. Gate 1.2 needs solver damping below 0.1 x friction (about 0.0005). If fine still fails, the space grid dominates: try a finer surface band or a higher-order time scheme (CrankNicolson), measured the same way.
2. Explain the medium rest run's mass gain (+3.6e-4) and the stout carried out through the top during swings (fraction smeared into the air); gate 1.5.
3. Gates 1.3 (swirl onset vs Royon-Lebeaud, Hopfinger & Cartellier 2007), 1.4 (foam head, cart friction terms with sources), 1.6 (108-ride proof set).
4. Phase 2: measure one 12 s ride on a runner (fine mesh at a fixed small step may exceed the 6 h job limit: split rides into restarts), state total runner hours, pilot release files -> Cloudflare build fetch.
5. Phases 3-5.

## 12. Open questions ⚠️
- Surface tension: keep σ = 0 (stated effect ~1 % on frequency) or include σ ≈ 0.045 N/m (source still needed) at the cost of spurious currents? Engineering choice; justify in the note.
- How to model the foam head's damping in OpenFOAM (not yet designed).
- Whether medium/fine meshes fit the 6 h runner limit for 12 s rides (to be measured).

## 13. Re-attach checklist
Nothing to attach. Everything is committed on branch `ccr-76841c15-le08bl` of `Numa1997/SiteTest` (latest `410e59a`, plus this file).

---
<sub>Audit: 13/13 sections · 17 rules · 9 corrections · 40 data points · secrets removed: none found · generated by active-memory</sub>
