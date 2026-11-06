# Handover 2: fix every remaining error of project 05's solved fluid (6 November 2026)

Read this whole file first, then `HANDOVER.md` (section 0 and 1), `twoway/research/ROOTCAUSE.md`, the three dossiers in
`twoway/research/`, `CLAUDE.md`, `AGENTS.md`, `notes/STANDARD.md`, `docs/scripts/twoway.md`, and lecture-note section 13.6 of
`public/simulations/double-inverted-pendulum.html`.

## 1. The aim (Numa's words, kept)
The double inverted pendulum on a cart (project 05, phyeinusul.com) moves through a real fluid: a velocity field acting on
every point of every body, the bodies pushing back (two-way, Newton's third law), wakes, the cart moving, live in a browser on
a CPU (no GPU, no Colab). "The right way, physically; nothing sketchy." Numa now asks: fix ALL remaining errors, known and
unknown; check everything that is unchecked, with Wolfram; root cause first, then resolution.

## 2. What is live (PR #102, #104; `main`)
`public/scripts/twoway.js`: 2D MAC Navier–Stokes in a tank as deep as the cart (b = 0.2 m, 4 × 2.8 m, Δ 2.5 cm, fluid
step 20 ms); cart resolved, Batty 2007 pressure coupling with exact area fractions, ghost-fluid no-slip, implicit added mass
(m_a = −K_x Δt carried by the cart, G = Q0 + K_x ẋ0 held); rods as actuator lines (Peskin 4-point kernel, the page's law
(33)+(34)+(39), impulses RK4-weighted, delivered one step later); the page's 1 ms RK4 machine steps, controller and logs run
inside (`twCtrl`, `twSub`). Page switch *The fluid: given / solved*; section 13.6 eqs. (41)–(46); data-panel group
*The solved fluid*; German and Arabic. Branch `claude/fluid-rootcause` (this file's branch) adds test options, all off by
default: `incremental`, `advCentral`, `advWeighted`, `noExtrap`, `measureSdf`.

## 3. The errors, with what is known (details and every number: `twoway/research/ROOTCAUSE.md`)
1. **Rods under-dragged 3–7 % (13 % in slow honey). Cause SETTLED:** self-induced (Oseen) velocity. Fast regime: slowing
   = k·f/(2ρbU), k ≈ 0.45 (0.52 at Δ/2), flat across ν and U; slow regime: Stokes-paradox log with Oseen cut-off
   (honey/glycerol ratio predicted 2.9, measured 2.8). Fix to build: subtract u_self (2D Oseen influence for the Peskin
   kernel, or a law joining both regimes), iterate with the nonlinear law; pass ±1 % on held rods across/along/45°, three
   liquids, Δ and Δ/2, and an independent moving-rod case. No published 2D scheme exists (dossier-selfinduced.md).
2. **Benchmark flow weak, does NOT converge with the grid. Cause NOT FOUND.** Schäfer–Turek 2D-1: La 0.0801/0.0785/0.0777,
   Δp 0.1033/0.1041/0.1046 at 10/20/39 cells per D (published 0.0842–0.0852, 0.1172–0.1176); c_D body 5.12/5.21/4.96,
   control volume 5.34/5.32/5.30 (5.57–5.59). Ruled out: run length, advection scheme (central conservative gives the same),
   extrapolation, weighted tracing, time splitting as main cause, incremental projection alone. Shown right: Poiseuille
   with cut walls (0.15 %), unsteady-Stokes oscillating cylinder converging (−6.8 % → −4.1 %). So: steady nonlinear flow
   hitting a curved body. Next suspects: force/momentum ledger identity (fluid + solid weights = 1 per face), Kim–Moin lagged
   φ wall value, the treatment of faces with centre inside but wu > 0 (held at body velocity, pressure-projected), inlet v
   boundary, the Δp/La measurement itself (validate it on a trusted reference: `spectral/ns2.cjs` reproduced La 0.0847).
3. **Momentum uncounted between body and water, 2–6 %.** Measure by an identity test before fixing.
4. **Energy remainder R 17 % (glycerol), 80 % (water).** Advection minor (central: 15.5 %), Δt part about a third (12.5 % at
   5 ms), ~11 % independent of Δt and Δ. Suspect the book: `impose()` overrides inside the viscous substeps change KE; their
   momentum is credited to the cart, their energy is not separated. The `incremental` option's book is invalid (its old-
   pressure work lands in E_diff). Water: 2D cascade, name any subgrid term as a regulariser.
5. **Unknown errors:** audit everything not yet checked (list in section 5).

## 4. Standards (binding)
- Skills to load and follow: anthropic-skills:physics-model-loop, theoretical-fluids-and-pdes, wolfram-physics,
  verification-before-completion, pushback-proof-answers, phyein-usul-physics-content, phyein-usul-data-panel,
  phyein-usul-bookkeeper, phyein-usul-i18n, tune-with-numa (anything judged by eye).
- Wolfram (`mcp__Wolfram__WolframLanguageEvaluator`, and WolframAlpha) for every derivation and every exact reference value;
  two routes per numbered equation; units and one limit for each.
- Measure, never estimate; every exact or published reference opened and read; test each new piece against an exact result
  before use; root cause before fix; a fix is accepted only if it improves the target AND does not break the other tests.
- Code: the page's style (ES5 in the page, comments that state the physics), `twoway.js` works in Node and the browser;
  page edits line-neutral where possible, else remap doc line links by content; walkthrough excerpts identical to page lines;
  `python3 tools/i18n/build.py --check` 0 missing for the page; `tools/inventory.py`, `tools/redirects.py --check`,
  `npm run build` (then delete `package-lock.json`); revert regenerated pages whose only change is the commit stamp.
- Browser: headless Chromium, en/de/ar at 1100 and 390 px: no page errors, no `.katex-error`, no pending, no overflow; look
  at screenshots. Existing `notes/fig11/panel/hon.cjs rest flick wind water stillwater` must stay 5/5.
- Talk to Numa per his constitution: short, Fact/Inference/Opinion, metric, end turns with "Where we are" / "Next, if you say yes".
- CLAUDE.md: when finished and tested, merge to main and verify live (poll for a sentence only the new version has).

## 5. Unchecked items to audit (find more)
Rod Froude–Krylov/added-mass term with grid Du/Dt (39) in two-way form; the one-step lag of rod impulses (energy, stability);
cart viscous force sign and size against an exact Couette/Stokes-layer case; added mass for a cart near the floor/rail;
tank confinement effects; boundaryPower and the open right end (closed-tank option); stability at large flicks and swing-up
in honey; the `tw_res` hook; the vorticity colour scale; speed in Chromium (target ≤ 20 ms per step); the controller's 2D
cart added mass (46) versus the measured −K_x Δt.

## 6. Tests and tools that exist (`notes/fig11/fluid-ns-handover/twoway/`)
t_addedmass, panel_addedmass.py, t_poiseuille, t_cutchannel, t_schaefer, t_st2, t_oscstokes, t_rodheld, t_disc, t_cartdrag,
t_book, t_decomp, t_run, t_its, t_prof. Run from that folder; they load `public/scripts/twoway.js`.
