# Handover: project 05 (double inverted pendulum on a cart) in a fluid that answers back

Written 6 November 2026 by the previous session for a fresh one. Read this whole file, then `CLAUDE.md` and `AGENTS.md`
at the repository root, before doing anything.

## 1. What Numa wants, in his words and in physics

Page: `public/simulations/double-inverted-pendulum.html` (project 05; live at phyeinusul.com).
The machine: a cart (1.5 kg; 0.36 × 0.12 m, 0.2 m deep) on a rail, driven by a motor (±60 N), with two hinged rods
(0.5 kg, 0.5 m and 0.75 kg, 0.75 m; 2 cm thick), balanced by an LQR controller sampled every 10 ms.

Numa wants the cart and the rods to move through a fluid (air, water, glycerol, honey) where:
- the fluid is a velocity field defined everywhere;
- each body feels, at every point, the fluid's velocity minus its own, integrated over the body: momentum exchange
  ("a shitload of momentum exchange"), force density integrated to forces and torques, then generalized forces on (x, θ1, θ2);
- **the fluid answers back**: the bodies change the flow (two-way coupling, Newton's third law), wakes form;
- **the cart moves** — a frozen, precomputed field around a cart at rest was rejected outright ("not a non moving cart");
- the field may be **2D** ("the velocity field can also be simply 2d… all we care for is the interactions between the
  geometric 2d bodies"); vector field drawn on the page;
- runs **on a CPU, no GPU, no Colab, no external compute** ("I absolutely do not agree that you need a GPU to run such a
  silly example"; "Connecting to colab is not an option").
- the right way, physically; nothing sketchy.

He holds a BSc in physics (computational/theoretical). Read his constitution (system prompt): one step per turn, every
action needs a yes, Fact / Inference / Opinion marked, options with costs and risks, a handle on every claim, metric units,
short plain words, no persuasion, end project turns with "Where we are" / "Next, if you say yes". He is frustrated:
several sessions produced theory and detours. **Stick strictly to physics, and show working results.**

## 2. Skills and memories to follow (load them before working)

From the session skill list: `anthropic-skills:wolfram-physics` (route derivations and reference solutions to Wolfram),
`anthropic-skills:theoretical-fluids-and-pdes`, `anthropic-skills:physics-model-loop`, `anthropic-skills:phyein-usul-first-principles-control`,
`anthropic-skills:phyein-usul-physics-content`, `anthropic-skills:verification-before-completion`, `anthropic-skills:pushback-proof-answers`.
Repository: `notes/STANDARD.md` (lecture-note standard), `notes/skills/phyein-usul-data-panel`, `CLAUDE.md` (method: persist,
read primary sources whole, measure numbers, build when the request is clear, data panel as a pipeline), `AGENTS.md`.
Wolfram MCP (`mcp__Wolfram__WolframLanguageEvaluator`) is available for derivations; use it.

## 3. What exists on the live page now (one-way model, section 13 of the lecture note)

Prescribed analytic 2D fields (12 flows), forces on rods by resistive-force theory plus quadratic drag, buoyancy, added
mass (C_a = 1, from potential flow, Wolfram block 6 in `notes/fig11/fluid/checks.wl`) and Froude–Krylov; cart by Stokes +
quadratic drag and ellipsoid added mass. Checked in Wolfram (`notes/fig11/fluid/README.md`), honesty tests pass.
Numa rejected it as "drag and buoyancy… what are we 15": the bodies do not change the flow.

## 4. What was tried in this session, and what each attempt established (all code in this folder)

| Attempt | Folder | Established (Fact) | Why it was not the answer |
|---|---|---|---|
| Fourier pseudo-spectral 2D NS, Brinkman penalization (Kolomenskiy & Schneider 2009) | `spectral/` | Taylor–Green exact to 2e-15; Schäfer–Turek 2D-1 cD 5.621, La 0.0847 at 20 cells/D once the penalization was put inside RK3 (band 5.57–5.59, 0.0842–0.0852); `RESULTS.md` has every run | explicit penalization forces dt ≤ 2η: ~1/50 of real time; split schemes gave forces that do not converge in dt |
| Same solver, cart + rods as **in-plane** 2D bodies | `spectral/play.html`, `inplane_rods_paddle_jet.png` | cart alone in glycerol: drag within 4 % of the page's law at Re_h ≥ 100, Kármán street, St 0.12–0.19 (`RESULTS.md`, table "Cart alone") | in a 2D plane each 2 cm rod is a 50–75 cm blade (a fence): 12 m/s jet under the cart, ~1000 N per rod in a confined box; blade added mass 3.4 kg vs 0.16 kg for the real rod (`t_blade.cjs`) |
| Precomputed field round a cart **at rest**, overlaid on the page | `spectral/solved_glycerol_2.png` | looks right | rejected: the cart must move |
| 3D WaterLily.jl (GPU, Colab notebook) | `waterlily/` | API checked: force metrics return the force ON THE FLUID (negate); 2D oscillating cylinder vs exact Stokes result: inertia −34 % at 4 cells/radius, −7 % at 32 | needs a GPU and Colab: rejected by Numa |
| **2D MAC grid + Batty–Bertails–Bridson 2007 variational coupling**, CPU | `mac/` | light cylinder (mass 0.1 of displaced fluid) under constant force: stable, added mass 1.037 ρπa² at 8 cells/radius, 1.069 at 4 (exact 1); divergence 1e-4 1/s after a cut-cell fix; the whole machine runs coupled with the page's controller (`t_pend.cjs`) | the rods are again in-plane blades: held in a 0.5 m/s glycerol breeze the upper rod takes ~30 N (cD ≈ 13 vs ~2 for a plate) — confinement (fence 1.25 m in a 2.4 m box) and rods < 2 cells thick (Batty sec. 3.1 needs an interior on the grid); 85–170 ms per step at 256 × 192 on one core |

Primary sources read whole (download them again, they are not committed):
- Kolomenskiy & Schneider, J. Comput. Phys. 228 (2009) 5687 — https://www.i2m.univ-amu.fr/perso/kai.schneider/PDF-FILES/ks_jcp2009final.pdf
- Engels et al., Comput. Struct. (2013) — https://www.i2m.univ-amu.fr/perso/kai.schneider/PDF-FILES/ekss_cas_2013_proof.pdf
- Schäfer & Turek 1996 benchmark — https://karlin.mff.cuni.cz/~hron/NMMO403/dfg_benchmark_results.pdf
- Weymouth, LilyPad, arXiv:1510.06886; source github.com/weymouth/lily-pad (BDIM.pde, Body.pde: FSI via `react()` with a lagged added mass)
- Batty, Bertails & Bridson, ACM TOG 26(3) 100 (2007) — https://cs.uwaterloo.ca/~c2batty/papers/Batty07.pdf
- WaterLily.jl source (Metrics.jl, RigidMap.jl, Body.jl), Weymouth & Font, Comput. Phys. Commun. 315 (2025) 109748

Exact result derived in Wolfram this session (use it as a test): cylinder of radius a oscillating with velocity U e^{−iωt}
in fluid at rest, unsteady Stokes: F = −ρπa² [1 + 4K₁(ka)/(ka K₀(ka))] dU/dt, k = √(−iω/ν), Re k > 0.

## 5. The open physics problem, stated precisely

The rods are slender (2 cm thick, 50–75 cm long) and move in the plane of the screen. In a 2D fluid solved in that plane
they can only be infinitely deep blades, which is a different machine. Resolving them as bodies needs cells ≪ 2 cm over a
box several metres across, which a CPU cannot do live. The cart (36 × 12 cm) is resolved fine on a 1–2.5 cm grid.

Recommended next step (the previous session's pick, not yet approved by Numa — ask him):
**hybrid two-way coupling**: the cart as a resolved body in the 2D grid (Batty coupling, `mac/mac.cjs`), each rod as an
**actuator line** — points along the rod read the local fluid velocity, subtract their own velocity, get a force per metre
from the rod's cross-flow law (drag, added mass), and the opposite force is spread back into the fluid as a body force
(regularised kernel), so the rods leave wakes and the exchange is two-way. This is Numa's own momentum-exchange picture and
the standard treatment of blades too thin for the grid (actuator line: Sørensen & Shen, J. Fluids Eng. 2002 — **not yet read;
read it whole before citing**). With rods off the grid, a 2.5 cm grid (~20 000 cells) should run near real time in JS.
Things to verify: momentum balance (force on rods = minus force on fluid, to round-off); the actuator kernel width vs
grid; the rod law against the page's existing law when the field is uniform; stability with the implicit 3×3 coupling.

Alternatives Numa may prefer: a pure 2D world (rods as blades) in a large box, recorded offline; or keep the one-way page.

## 6. Rules for this work

- Physics first: derive, check limits and units, check against exact solutions (Wolfram), then code. No GPU, no Colab.
- Everything stays in the scratchpad or on this branch until Numa says yes; the live page changes only when he approves.
- Machine constants and controller gains per medium are in `waterlily/pageparams.json` (read from the live page).
- Show results as pictures and numbers (headless Chromium is available; Playwright works from any directory).
