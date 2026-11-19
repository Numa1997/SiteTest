# Findings of the independent review, 19 November 2026 (Guinness on a cart, the spill)

For the Claude Code session that holds the work (branch `claude/guinness-open-problems`). This file is the whole result of the
review of `notes/spill/PROMPT-argon.md`. It replaces the earlier file `PROMPT-rest-drift-fix.md` from the same review, which is
withdrawn (section 3). Refer to the person you work for as "the owner"; never write a name.

Each statement is marked: FACT (read or counted, with where), INFERENCE (reasoning from facts), OPINION, or NOT CHECKED.

## 0. Where things stand, in five lines

1. The continuous model's pint at rest sinks because cut cells in the glass's bowl-shaped base are read as air (section 1). FACT for
   their existence at t = 0; INFERENCE that they are the drift.
2. A one-line change that removes them was proposed and then withdrawn: it is a fourth patch on three overlapping devices (section 3).
3. Published solvers do this job with one rule: the liquid's level set is continued into the solid (section 4).
4. The owner's decision after that (19 Nov, about 02:20): **no ride is recomputed on the GPU.** The spill outside the glass is to be
   derived from the stored rides by a cheap second computation (section 6).
5. A CPU notebook that measures whether the stored data allows this exists on Kaggle but has not yet read the data (section 7).

## 1. Why the continuous model's pint at rest drifts

Code read at commit 0c51864, `tools/fig12/kaggle/stout_jax.py`.

FACT. A pint at rest is an exact solution of the discrete equations: gravity's kick `-g dt` on each open face is cancelled by the
hydrostatic pressure difference, `w = w* - (dt/rho)(p_above - p_below)/dx = -g dt + g dt = 0`. This holds only if every neighbour of
a liquid cell, through an open face, is liquid or air at the true surface.

FACT. Three lines break that at the bottom of the glass:
- line 530: a cell with no particle that is not in `near` gets `ph = +2 dx` (air);
- line 542: such a cell becomes liquid again only if it is in `wallcut` and touches liquid through an open face;
- line 162: for the continuous model `wallcut` has an outer bound, `r < R(z) + dx/2`, measured along the radius; the old model has none.

FACT. The glass's base is a shallow bowl: R = 16.31 mm at z = 0, 28.0 mm at z = 4 mm (`public/scripts/guinness-glass.js`), so
dR/dz is about 4 and the wall lies about 14 degrees from the horizontal. A cell centre a depth d below the glass's surface is 4 d
outside R(z) along the radius. The bound 4 d < dx/2 keeps only d < dx/8; a cut cell still has an open corner for d up to about dx/2.

FACT (count at t = 0, Fig. 16 deck body, seed 1, ppc 2; cells with no particle, an open face to a cell with particles, more than
2 dx below the fill, not in `near`, not in `wallcut`):

| dx | grid | particles | such cells | open area to stout | with the old `wallcut` |
|---|---|---|---|---|---|
| 2.0 mm | 159 x 66 x 108 | 420 216 | 4 (z = 1.0 mm) | 6.0 faces = 24 mm^2 | 0 |
| 1.5 mm | 211 x 87 x 143 | 1 001 952 | 36 (z = 0.75 to 2.25 mm) | 38.5 faces = 87 mm^2 | 0 |

All are on the cavity's side (`G.side` True). The count was made by the reviewer in numpy, outside Kaggle, from `Geometry` and
`seed_particles` only, with particle occupancy standing in for the level set. It is not a run and breaks the owner's rule "every
computation on Kaggle"; reproduce it on Kaggle before relying on it.

INFERENCE. For a liquid cell with pressure p_c beside an air cell, the ghost-fluid rule (lines 815-821) gives the face
`u = u* + (dt/rho) p_c / (theta dx)`. With p_c = rho g H = 1007 x 9.81 x 0.123 = 1215 Pa, dt = 2 ms, dx = 1.5 mm: u = 1.6/theta m/s
into the glass, at most about 7 mm^3 per open face per step (an upper bound). The air cell has no divergence equation, so the
grid loses that volume; `_g2p_cont` puts the particles back on the wall, so none leaves while the cloud is compacted at the bottom.
- Fits v8 (1.5 mm, 1 s): 0 outside the cavity, mean particle height 72.69 -> 67.74 mm (D), 67.96 mm (F), surface 120.49 / 120.63 mm.
- Size: 4.5 mm x 4803 mm^2 = 21 600 mm^3 in 500 steps = 43 mm^3 per step, against a bound of 38.5 x 7 = 270.
- Grid: 3.6 times more open area at 1.5 mm than at 2 mm; drift about 1 mm/s (v5) against about 4.5 mm/s (v8).

NOT CHECKED. That these cells are the whole drift. That the 1496 empty cut cells at 1.5 mm (738 at 2 mm) lying in `near` read as
liquid from particles and mirror images (assumed, their phi was not computed). Whether the cells refill during a run.

Candidates examined and not the located cause:
- Surface tension: excluded by v8 (F against D). FACT.
- Gravity reaching open faces outside the glass through the trilinear stencil (`_corners`, one cell reach): at 1.5 mm only diagonal
  faces, weights near 0.01; at 2 mm faces on the axes, weights up to about 0.15. INFERENCE (estimates, not counts).
- Conjugate gradient on the larger grid: the unknowns are the liquid cells only, the same pint as the old model. INFERENCE.

## 2. Corrections to `notes/spill/PROMPT-argon.md` (FACT)

- The deck grid at 1.5 mm is 211 x 87 x 143 = 2.63 M cells (v8 log, `rest_variants.json`), not 213 x 89 x 151.
- The 1.5 mm particle count is 1 001 952; 420 216 is the 2 mm count.
- "The projection is not keeping the velocity divergence-free": it does; the liquid's domain has holes in its boundary.
- v8 timings: D 233 s, E 62 s, F 215 s for 1 s of rest at 1.5 mm on the T4.

## 3. Withdrawn: the one-line fix

The earlier prompt proposed `wallcut = (Z > 0) & (Z < zrim) & side & ~cav_inner` for `body` set. FACT: counted on the starting
geometry it leaves 0 such cells at both grids and selects 6604 cells (2 mm) / 11 708 cells (1.5 mm), the same cells as the old rule
restricted to the cavity's side. It is withdrawn all the same (the owner rejected it, and the review agrees): the commit history
shows the wall being handled by a rule that changed three times (f885e96 faces closed where the centre-to-centre segment crosses
glass; cc51c2c cut cells keep their fractions; 6aab9eb one side per cell by majority), and three separate devices answer the one
question "is this cell at the glass liquid?": mirror images of particles, the inherit rule with its band, and the shortcut that
calls an empty cell air without computing phi. The hole of section 1 is where those three fail to overlap.

## 4. How published solvers do it (sources read on 19 Nov; relevant only if the continuous model is ever taken up again)

The principle: the pressure solve must never see glass as air. The liquid's level set phi is continued into the solid; the wall is
enforced only by the closed face fractions.
- FACT. Batty's reference solver, github.com/christopherbatty/Fluid3D, `fluidsim.cpp`, `compute_phi`, lines 260-274: every cell
  whose centre lies in the solid and whose particle phi is below dx/2 gets phi = -dx/2 (its comment: "simple, naive").
- FACT. Ando's solver, github.com/ryichando/shiokaze, `src/utility/gridutility3.cpp`, `extrapolate_levelset`: each solid cell takes
  the liquid's phi at the nearest point of the wall, phi(x) = phi(x - psi n), psi the solid's signed distance, n its normal.
- FACT. Lepilliez, Popescu, Gibou, Tanguy, J. Comput. Phys. 321 (2016) 1217: the extension is d(phi)/d(tau) + H(phi_s) n_s . grad phi
  = cos(theta_s) in solid cells (their eq. 21), which also sets the contact angle; curvature is extended the same way (eq. 22);
  capillary time step dt = (1/2) sqrt(rho_l/sigma) dx^(3/2), which is 4.4 ms at 1.5 mm for stout.
- FACT. Weta 2019 notes (wetafx.co.nz, siggraph2019_drips.pdf): extrapolating the fluid into the solid is what a standard FLIP
  implementation does; with a contact angle, fluidSDF = sin(theta) d + cos(theta) solidSDF, d = sqrt(fluidSDF^2 - solidSDF^2).
- FACT. Thin walls: Azevedo, Batty, Oliveira (SIGGRAPH 2016) give each cut piece of a cell its own pressure, but for single-phase
  flow only; free surfaces are named as a possible extension, not implemented. Guendelman, Selle, Losasso, Fedkiw (SIGGRAPH 2005):
  stencils use only points visible from the reference point; a face whose centre-to-centre ray crosses the solid gets no flow
  (the rule of commit f885e96).
- NOT READ: Wang et al. 2005; Ng, Min, Gibou 2009; Batty et al. 2007 beyond a summary of its sections.

Time step for surface tension: three values are on the table and they disagree. The brief: sqrt(rho dx^3 / (2 pi gamma)) = 3.5 ms.
A second review: 1/omega at k = pi/dx = 1.57 ms (its first draft: 1.87 ms). Lepilliez et al.: 4.4 ms. NOT CHECKED which bound
applies to this scheme; a capillary-wave test decides.

## 5. A second review ("Neon"), checked against the code

- Its three conditions for exact rest are right and are the ones used in section 1.
- "Submerged wall cells become p = 0 drains": the right kind of fault, the wrong place (it puts them along the upright wall).
  Wrong details: a tie goes to the outside, not the cavity (line 149, `nin > nout`); mirror images do reach wall cells (lines
  517-526); "the cell can never fill" is not shown.
- "Stencil through the wall", called primary: the transfer is trilinear (lines 456-464), not quadratic; see section 1.
- Surface tension: excluded as the drift's cause by v8, which it did not have.
- Its sections 2 to 4 are NOT CHECKED, and some numbers contradict the repository: 420 000 particles (the 2 mm count); 40 um
  bubbles, jamming at 0.64 and a 4.3 Pa yield stress where `stout_jax.py` has 34 um, 0.635 and 5.4 Pa with sources; contact
  angles of 25 and 70 degrees with no source (`notes/spill/STATE.md` records that no measured stout-on-glass angle was found).
  Its claim that Basilisk combines embedded solids, volume-of-fluid contact angles and Bingham rheology out of the box was not
  checked against Basilisk's documentation.

## 6. The owner's direction now: derive the spill from the stored rides, no GPU

The owner's words (19 Nov): no recomputing on the GPU; "we will derive the new data, using the old ones".

INFERENCE (why this is legitimate). Liquid that has crossed the rim never returns, so the flow inside the glass does not depend
on what the spilled liquid does afterwards. Inside the glass the old model is the verified one (it holds the pint at rest). The
stored rides are therefore a valid source term for a second computation of the liquid outside the glass. One approximation: the
spilled stout's weight on the deck acts back on the cart; at most 76 g against a deck of 2.40 kg plus axles 1.60 kg
(`cart4.py` CART4: Md, mf, mr), about 2 %.

OPINION. The flying part of the stored data is right to first order. A parcel in the air has atmospheric pressure all round it,
so `Dv/Dt = -grad p / rho + g` reduces to `Dv/Dt = g`: free flight is the same equation with its pressure term gone, valid when
inertia beats surface tension. For a sheet 3 mm thick leaving at 1 m/s (guessed values, not measured), rho U^2 h / gamma =
1007 x 1 x 0.003 / 0.0442 = 68. What the stored flight lacks: air drag, and the slow overflow that clings to the glass.

FACT (what is wrong in the stored data). A drop that lands is frozen where it hits, and the old model's landing plane is Fig. 12's
body (`BODY_TOP` = -14 mm, `BODY_HALF` = 110 x 60 mm, hard-coded in `g2p`), not Fig. 16's deck (310 x 124 mm, top at -30 mm).

The book model for the deck (from memory of de Gennes, Brochard-Wyart, Quere, "Capillarity and Wetting Phenomena", section 2.2
"Drops and Puddles in the Partial Wetting Regime", 2.2.3 heavy drops; the contents were confirmed, the formula was NOT CHECKED
against the page): a puddle has a thickness set by gravity against surface tension,
e = 2 kappa^-1 sin(theta/2), kappa^-1 = sqrt(gamma / (rho g)) = sqrt(0.0442 / (1007 x 9.81)) = 2.1 mm, theta the contact angle.
Deck free area: 310 x 124 mm minus the glass's foot (radius R(8 mm) + 2.5 mm = 31.2 mm) = about 35 400 mm^2.

| theta | e | most the deck holds at rest |
|---|---|---|
| 30 deg | 1.1 mm | 39 mL |
| 70 deg | 2.4 mm | 86 mL |
| 90 deg | 3.0 mm | 106 mL |

The kerb ride with control off spills 76 g, about 75 mL: the same size as what the deck can hold, so the contact angle and the
deck's shaking decide whether it stays or pours off. No measured angle for stout on the deck exists in the repository; the owner
must give one or have it measured.

Proposed derivation (OPINION; not built): the puddle on the accelerating, pitching deck as a thin layer h(x, y, t) with mean
velocity (shallow water; Landau and Lifshitz, "Fluid Mechanics", long gravity waves, from memory, NOT CHECKED), fed by the landing
drops, driven by the stored effective gravity of the deck's frame, leaving over the deck's edge, held back by the puddle
thickness above. About 38 000 cells at 1 mm: seconds on a CPU.

FACT (what a stored ride holds; `run16.py` lines 169-208, `Stout.observe`). Per picture, 60 a second: `drops` (positions of up to
16 384 drops, float16, glass frame; an even subsample when the true count is larger), `ndrops`, `nfly`, `nlanded`, `nstuck`,
`nact`, `H`, `hf`, `lumps`, `lumpvol`, `foam_spill`, the cart's state (`x`, `v`, `th`, `om`, `al`, ...), and `gx`, `gz`, the
effective gravity of the glass's frame; plus `N`, `mp`. Not stored: the drops' velocities, and which drop is which from one
picture to the next (the solver re-sorts its particles by cell after every picture). So the mass over the rim per picture is
exact; velocities must be recovered, for instance by the free-flight relation x(t+dt) - 2 x(t) + x(t-dt) = a dt^2.

## 7. What exists on Kaggle from this review

- FACT. Notebook `numakoudsie/fig16-spill-derived`, private, CPU, version 1 (kernel id 145889083). Its header documents the idea
  and six questions: the arrays and books; whether the drop list is complete; whether a list slot is a drop; whether velocities
  can be recovered by free-flight matching (residual and uniqueness); the speed and Weber number at the rim and the landing
  points on Fig. 16's true deck; how hard the deck shakes. It writes REPORT.md, report.json, params.json and three figures.
- FACT. Version 1 failed after 10 s: `/kaggle/input` was empty (the connector's save call dropped the dataset attachment, the
  bug the Kaggle skill already records) and the `kagglehub` download inside the run also failed; its error text was not read.
  Nothing was measured. No GPU time was used.
- To run it: attach `numakoudsie/fig16-guinness-cart-control` in the notebook's editor (Add Input, Your Datasets) and save with
  "Save & Run All"; the code looks under `/kaggle/input/**/fig-16-guinness-cart-with-control/v8/output/2026-11-15/kerb_off.npz`
  first. The notebook's code has never run past the loading step, so its later sections are untested.
- FACT. GPU quota read at about 02:05: 96 279 s used of 108 000 s (about 195 T4-minutes left), refresh 21 November 00:00 UTC.
- FACT. `continuous-spill-fig16-gpu` is at version 8, complete. Nothing else was created, changed or deleted on Kaggle.

## 8. What the review did not touch

Nothing was written to the repository, the site, or any dataset. `main` was at 12c2e3a1, the branch at 0c51864. The live pages
`guinness-kaggle.html` (Fig. 12) and `guinness-cart-control.html` (Fig. 16) play stored rides only and were read, not changed.

## 9. Open, in the order the review would take them (OPINION)

1. Get the measuring notebook to read one ride, and read its report: can velocities be recovered, how much lands on the deck.
2. The owner's value for the contact angle of stout on the deck.
3. Only then design the derived computation (flight with drag, landing, puddle, run-off) and its checks.
4. The continuous model on the GPU stays parked. If it is ever resumed, start from section 4, not from another band or rule.
