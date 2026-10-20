# Fig. 5 lecture note: derivation check

Checked: `public/simulations/water-wave.html`, the note between `<article class="paper" id="paper">` and `</article>`.
File sha256 `3802f40b513c5caecacc78c36740ea99ae3134e77205b1ec4a7ab36382bf76e0`, identical to HEAD `468c139` (working tree clean for
this file). Against the base `db1a24b` it has 12 changed lines, all checked: the §2 warning paragraph, the Figure 1 caption (twice:
ak = 0.59 sentence kept, labels (4) and (9) added), §4.2 (gz becomes gη), §5.3 (two-wave group), §07 (sin²θ half of the drift picture),
§08 (W_field defined; what is stored and what is only drawn), and the four references. The page changed once while this check ran
(15:32 UTC); every browser measurement below was rerun on the final file.

How: SymPy 1.14 for every numbered equation (re-derived, not just substituted), a dimension table for each, NumPy for the numbers,
my own RK4 for Figure 4, and the page's own code run in headless Chromium 1194 (Playwright) from a private build
(`APPDEPLOY_VITE_OUT_DIR=/tmp/fig05-check-dist npm run build`, served by a small Node static server). In the browser I read the
readouts, the slider outputs and the data store (`Sim.data.ds`) at the defaults and after moving sliders, counted canvas path
vertices and arc radii by wrapping `CanvasRenderingContext2D`, recomputed all 90 stored parcels from stored inputs, and read back the
pixel under each stored parcel (alpha first). Viewports: 1280 and 1600 px wide (canvas 770 × 366 and 630 × 299 css px, wide field)
and 390 px (canvas 356 × 338, narrow field). No console or page errors; 337 KaTeX formulas, 0 KaTeX errors; tags (1)…(23) in order.
I did not read `notes/fig05/plan.md`, the referee report or any other teacher file.

Verdicts: **verified**, **wrong, because …** (with the correct result), **unverifiable, because …**.

## A. Numbered equations

| # | Eq. | Re-derivation, units, limits | Verdict |
|---|---|---|---|
| A1 | (1) continuity | SymPy: net outflow of a δx × δz box to first order is (∂u/∂x + ∂w/∂z) δx δz. Both terms 1/s. | verified |
| A2 | (2) no spin | Vorticity ∂u/∂z − ∂w/∂x is the y-component of curl u, twice the angular velocity; SymPy: it vanishes identically for u = ∇φ. Units 1/s. | verified |
| A3 | (3) potential | Follows (2) automatically; φ in m²/s. | verified |
| A4 | (4) Laplace | (3) into (1), SymPy identical. Units 1/s. | verified |
| A5 | (5) kinematic condition | Exact form correct. SymPy ratios for the dropped terms at the solution: (u ∂η/∂x)/(∂η/∂t) = −ak cos θ and (η ∂w/∂z)/w = ak cos θ, both order ak as stated. Units m/s. | verified |
| A6 | (6) linear kinematic | SymPy: satisfied exactly by (10) with (12). Units m/s. | verified |
| A7 | (7) unsteady Bernoulli | SymPy, componentwise: Euler with constant ρ, gravity −g ẑ and (u·∇)u = ∇(½\|u\|²) for u = ∇φ equals ∇[φ_t + ½\|∇φ\|² + p/ρ + gz]. Each term m²/s². | verified |
| A8 | (8) dynamic condition | Dropped term: (½\|∇φ\|²)/(aω²/k) = ak/2 at z = 0, order ak. gz at z = η gives gη (the new §4.2 remark). m²/s². | verified |
| A9 | (9) deep water | ∇φ ∝ e^{kz} → 0 as z → −∞. | verified |
| A10 | (10) travelling wave | Crest at kx − ωt = 0 moves at ω/k. kx, ωt dimensionless. | verified |
| A11 | (11) Z(z) | SymPy dsolve of Z'' = k²Z: C1 e^{−kz} + C2 e^{kz}. | verified |
| A12 | (12) φ | Kinematic condition gives A = aω/k (SymPy solve); φ of (12) satisfies (4). m²/s. | verified |
| A13 | (13) ω² = gk | SymPy: (8) reduces to (g − ω²/k) a cos(kx − ωt) = 0; ∂φ/∂t at z = 0 is −(aω²/k) cos, as written. Units 1/s². Limit: ω² = gk tanh kh → gk as h → ∞. | verified |
| A14 | (14) c and T | SymPy: ω/k = √(g/k) = √(gλ/2π); 2π/ω = √(2πλ/g). m/s and s. | verified |
| A15 | (15) c_g | SymPy: dω/dk = ½√(g/k) = c/2. | verified |
| A16 | (16) velocity | ∇ of (12), SymPy identical. m/s. | verified |
| A17 | (17) parcel paths | SymPy: d/dt of (17) equals (16) at (x0, z0); the two quoted derivative identities hold. | verified |
| A18 | (18) r = a e^{kz0} | SymPy: (x−x0)² + (z−z0)² = a²e^{2kz0}; speed constant rω; (x−x0)ż − (z−z0)ẋ = −a²ω e^{2kz0} < 0, so clockwise with x right and z up; under a crest top and moving forward, under a trough bottom and moving back, a quarter wavelength ahead of a crest rising. Limit z0 → −∞: r → 0. | verified |
| A19 | (19) surface | z0 = 0 in (17). SymPy: dx/dx0 = 1 − ak cos θ; as ak → 0 the curve becomes the sine (10). | verified |
| A20 | (20) expansion | SymPy: ∂u/∂x = −aωk e^{kz0} sin θ, ∂u/∂z = aωk e^{kz0} cos θ at the rest position; the two products are a²ωk e^{2kz0} sin²θ and a²ωk e^{2kz0} cos²θ. Units m/s. | verified |
| A21 | (21) Stokes drift | SymPy period average: a²ωk e^{2kz0} = c(ak)² e^{2kz0}; ⟨u at rest position⟩ = 0; U_S T = (ak)² e^{2kz0} λ. m/s. Confirmed numerically by C47–C49. | verified |
| A22 | (22) phase update | Matches the code: `omegaT += 2 * Math.PI * f() * dt`, `f()` = `Math.sqrt(G * k() * PX_PER_M) / (2 * Math.PI)`; k_m = 100 k (rad/px × px/m). Measured: Δ(ωt)/Δt = 2πf to 1 part in 10¹⁴ over 1 s of play. (For the wording of Δt see D2.) | verified |
| A23 | (23) metres to pixels | Matches the code: `s = w / WORLD_W`, `ys = Math.max(A * s + 34, h * 0.28)`, `cy = ys - z0 * s` with z0 = −56 j, `px = (X0 - r sin th) * s`, `py = cy - r cos th * s`. Measured: all 90 stored px, py equal the formula from stored inputs (max difference 1.1 × 10⁻¹³ px); the canvas pixel at every stored position is opaque and dark (90/90, alpha checked first). | verified |

## B. Unnumbered steps and statements (all changed lines included)

| # | Where | Statement | Check | Verdict |
|---|---|---|---|---|
| B1 | §2 warning (changed) | First-order circles: swings a quarter cycle apart, radius a e^{kz0}, z0 the calm-water height, negative below | From (17): ξ = −r sin θ, ζ = r cos θ. | verified |
| B2 | §2 warning (changed) | Cross-references: Section 06 derives the circles, Section 07 the drift, Section 6.2 Gerstner | Read: §06 (17)–(18), §07 (20)–(21), §6.2 last paragraph. | verified |
| B3 | Fig. 1 caption (changed) | "The two labels in the water are Laplace's equation (4) and the deep-water condition (9), met in Sections 03 and 04" | SVG text: "∇²φ = 0 / in the water" and "∇φ → 0 as z → −∞"; (4) is in §03, (9) in §4.3. | verified |
| B4 | §4.2 (changed) | The bracket is taken at the surface, so gz becomes gη | z = η at the surface; with p = p_air absorbed, (7) gives φ_t + gη = 0 there, then moved to z = 0. | verified |
| B5 | §5.3 (changed) | Two waves k ± δk, ω ± δω add to 2a cos(δk x − δω t) cos(kx − ωt) | SymPy: identity holds exactly. | verified |
| B6 | §5.3 (changed) | Crests run at ω/k, envelope at δω/δk, which becomes dω/dk | SymPy: zeros of each factor move at those speeds; [ω(k+δk) − ω(k−δk)]/2δk → ½√(g/k). (For two waves on the curve ω(k) their mean frequency differs from ω(k) only at order δk², which does not change the limit.) | verified |
| B7 | §07 (changed) | Top-and-bottom picture is the cos²θ half of (20) | SymPy: ζ ∂u/∂z averages to exactly ½ U_S. | verified |
| B8 | §07 (changed) | sin²θ half: at the side of its circle, while rising or sinking, the parcel is shifted towards the nearest crest, where the flow also runs forward | SymPy: at θ = π/2, ξ = −r (towards the crest a quarter wavelength behind), w = +rω (rising), u at the shifted point = aω e^{kz0} sin(kr) > 0; at θ = −π/2 the mirror image (ξ = +r towards the crest ahead, sinking, u > 0). | verified |
| B9 | §5.2 | Horizontal push per kg at the surface is g × slope, at most g ak; equating to aω² gives (13) | SymPy: −(1/ρ)∂p/∂x at z = 0 equals −g ∂η/∂x = g ak sin(kx − ωt). | verified |
| B10 | §3 | Pressure on a parcel of uniform density acts through its centre of mass; Kelvin's theorem for constant density, no viscosity, potential force | For a linear pressure field the torque about the centroid, −∫ r × ∇p dV, vanishes when ∫ r dV = 0; Kelvin's conditions stated correctly. | verified |
| B11 | §3 | Harmonic φ equals its average on any circle inside the water | Mean-value property of Laplace's equation. | verified |
| B12 | §6.2, §07 | Gerstner's wave: exact, trochoidal surface, exactly circular orbits, water spins, closed orbits and no drift | SymPy on the Lagrangian Gerstner map: Jacobian 1 − e^{2kβ} (time-independent, so incompressible), orbit radius e^{kβ}/k, vorticity 2ck e^{2kβ}/(e^{2kβ} − 1) ≠ 0, mean drift over a period 0. | verified |
| B13 | §6.2 | Crests sharper, troughs flatter; agree with the sine as ak → 0 | dx/dx0 = 1 − ak cos θ is smallest at the crest (parcels crowd) and largest at the trough. | verified |

## C. Numbers

All values recomputed in Python and, where the page shows them, read from the page's readouts or data store in Chromium.

| # | Where | Note says | Recomputed / measured | Verdict |
|---|---|---|---|---|
| C1 | §2 | λ = 260 px = 2.6 m, 100 px = 1 m | Slider default 260; `PX_PER_M = 100`; store λ_m = 2.6 | verified |
| C2 | §2 | k = 2.42 rad/m | 2.416610 (store k_m) | verified |
| C3 | §2 | a = 24 px = 0.24 m | Slider default 24; store a = 24 (cap 0.9/k = 37.24 not active) | verified |
| C4 | §2 | g = 9.81 m/s² | `G = 9.81` | verified |
| C5 | §2 warning (changed) | default ak = 0.58 | 0.579986; readout "0.58" | verified |
| C6 | Fig. 1 | four columns a quarter wavelength apart, three depths | SVG columns x = 210, 285, 360, 435 with λ = 300 (crest to crest 210 → 510); depths 130, 180, 230 | verified |
| C7 | Fig. 1 | step λ/6 in depth shrinks circles by e^{π/3} = 2.85 | 50 = 300/6; e^{π/3} = 2.8497; SVG radii 28, 9.83, 3.45 = 28 e^{−πj/3} | verified |
| C8 | Fig. 1 | surface drawn as the page draws it, ak = 0.59 | 28 × 2π/300 = 0.5864; all 323 path vertices lie within 0.06 px of the trochoid (19) with a = 28, λ = 300 | verified |
| C9 | Fig. 1 | dots and arrows: forward under crest, back under trough, up ahead, down behind | Dot positions match (17) at θ = 0, π/2, π, 3π/2 for all 12 dots to 0.1 px; arrow directions match (16) | verified |
| C10 | §5.2 box | ω = 4.87 rad/s, f = 0.775 Hz | 4.868977, 0.774922 (store) | verified |
| C11 | §5.2 | surface water accelerates at 0.58 g | aω² = g·ak = 0.580 g | verified |
| C12 | §5.3 | default c = 2.01 m/s, T = 1.29 s | 2.014797, 1.290453; readouts "2.01 m/s", "1.29 s" | verified |
| C13 | §5.3 | 100 m swell: 12.5 m/s, 8.0 s | 12.495, 8.003 | verified |
| C14 | §5.3 | 16 s swell: λ = 400 m, c_g = 12.5 m/s, about 44 h from 2000 km | λ = gT²/2π = 399.7 m; c_g = gT/4π = 12.49 m/s; 44.5 h | verified |
| C15 | §5.3 | 8 s swell: λ = 100 m, 6.25 m/s, about 89 h | 99.9 m; 6.245 m/s; 88.96 h | verified |
| C16 | table | page, shortest: 1.2, 0.88, 1.37, 0.68 | T 0.8767, c 1.3688, c_g 0.6844 | verified |
| C17 | table | page, default: 2.6, 1.29, 2.01, 1.01 | 1.2905, 2.0148, 1.0074 | verified |
| C18 | table | page, longest: 4.0, 1.60, 2.50, 1.25 | 1.6006, 2.4990, 1.2495 | verified |
| C19 | table | wind waves: 10, 2.53, 3.95, 1.98 | 2.5308, 3.9513, 1.9757 | verified |
| C20 | table | ocean swell: 100, 8.00, 12.5, 6.25 | 8.0030, 12.495, 6.2476 | verified |
| C21 | table | long swell: 400, 16.0, 25.0, 12.5 | 16.006, 24.990, 12.495 | verified |
| C22 | Fig. 2 | 400 wavelengths from 0.02 to 4.6 m, g = 9.81; dashed lines at 1.2 and 4.0 m; labels 2.01 and 1.01 m/s | Both paths have 400 vertices, λ = 0.0203…4.6009 m on the axis scale; every vertex within 0.17 px of √(gλ/2π) and half of it; dashed lines at 1.2003 and 4.0007 m; default dots read 2.015 and 1.008 m/s | verified |
| C23 | Fig. 2 | four times the wavelength, twice the speed | c ∝ √λ | verified |
| C24 | Ex. 5.1 | 120 → 400 px is 1.2 → 4.0 m; c readout 1.37 → 2.50 m/s; factor 1.83 = √(400/120) | Readouts measured "1.37 m/s" and "2.50 m/s"; exact ratio 1.8257 | verified |
| C25 | Ex. 5.1 | T 0.88 → 1.60 s by the same factor; frequency slider follows | Readouts "0.88 s", "1.60 s"; exact ratio 1.8257; slider moved by itself to 1.14 and 0.62 Hz | verified |
| C26 | Ex. 5.1 | dispersion off, 260 px, f = 0.50 Hz: wave runs at 1.30 m/s | Readout "1.30 m/s" | verified |
| C27 | Ex. 5.1 | a 2.6 m deep-water wave must oscillate at 0.77 Hz | 0.7749 Hz | verified |
| C28 | §06 | aω = 1.17 m/s against c = 2.01 m/s | 1.1686, 2.0148 | verified |
| C29 | §6.1 | e^{−π} = 4.3 %, e^{−2π} = 0.19 %, one part in 535 | 4.32 %, 0.187 %, e^{2π} = 535.49 | verified |
| C30 | Fig. 3 | 400 depths, 0 to 2.5 m; k = 5.24, 2.42, 1.57 rad/m | 3 paths × 400 vertices, depth 0…2.5003 m, every vertex within 0.12 px of 100 e^{−kd}; k = 5.236, 2.417, 1.571 | verified |
| C31 | Fig. 3 | dots 100, 25.8, 6.7, 1.7, 0.45 % | 100, 25.84, 6.68, 1.73, 0.446; SVG dots read 25.83, 6.69, 1.71, 0.45 | verified |
| C32 | §6.1 | layers 56 px = 0.56 m apart; factor e^{−k·0.56 m} = 0.258; radii 24, 6.2, 1.6, 0.41, 0.11 px | 0.25839; store r_z = 24, 6.201, 1.602, 0.414, 0.107 | verified |
| C33 | §6.1 | fifth layer 2.24 m down: 0.45 %; readout rounds to 0.4 % | 0.4457 %; readout measured "0.4 % of a" | verified |
| C34 | §6.1 | 5 m under 10 m waves: z0/λ = −0.5, 4.3 % | e^{−π} = 4.32 % | verified |
| C35 | §6.1 | 5 m under a 100 m swell: 73 %; 50 m down for 4.3 % | e^{−0.1π} = 73.0 %; λ/2 = 50 m | verified |
| C36 | Ex. 6.1 | 400 px: deepest layer at 3.0 % of a | 2.964 %; readout measured "3.0 % of a" | verified |
| C37 | Ex. 6.1 | 120 px: readout 0.0 %; e^{−2π·2.24/1.2} = 8 × 10⁻⁶ | 8.06 × 10⁻⁶; readout measured "0.0 % of a" | verified |
| C38 | Ex. 6.1, §9 | circles stop below 1.2 screen pixels | Code `r * s > 1.2`; measured arcs at 1280 px: radii 23.1, 5.97, 1.54 drawn, 0.40 and 0.10 not | verified |
| C39 | §6.2 | crest spans ½ − ak/π = 31.5 % of a wavelength | SymPy fraction ½ − ak/π; 0.31538 | verified |
| C40 | §6.2 | mean surface ½a²k = 7.0 px below the orbit centres | SymPy mean η = −a²k/2; 6.96 px | verified |
| C41 | §6.2 | cusp at ak = 1, where aω = c | dx/dx0 = 0 at the crest when ak = 1; aω/c = ak | verified |
| C42 | §6.2 | cap a = 0.9/k, ak ≤ 0.9 | Code `Math.min(amp.value, 0.9 / k())` | verified |
| C43 | §6.2 | 50 px at 260 px: requested 1.21, held at 37.2 px, readout "0.90 (cap)" | 1.2083; store a = 37.242; readout measured "0.90 (cap)" | verified |
| C44 | §6.2 | steepest wave about 0.14 λ trough to crest, ak = πH/λ ≈ 0.44 | π × 0.14 = 0.440 (Michell's 0.142 gives 0.446) | verified |
| C45 | §07 | ak = 0.2: a = 8.3 cm, U_S = 0.081 m/s, 10.4 cm or 4 % of λ per period | 8.276 cm; 0.08059 m/s; (ak)²λ = 10.40 cm; 4.0 % | verified |
| C46 | Fig. 4 | 3.2 periods; RK4, 2000 steps per period; halving the step changes positions by < 10⁻¹² m; starts at the top of its circle; both axes same scale | My RK4 from (0, a) at t = 0, 2000 steps/period: the 1281 SVG vertices (6400 steps, every 5th kept) lie within 1.1 × 10⁻⁴ m (0.11 px) of it, end point matches; halving the step: 5.6 × 10⁻¹⁴ m; axis scales 1056.8 and 1057.0 px/m | verified |
| C47 | Fig. 4, §07 | loop lasts 1.043 T, ends 11.2 cm on, mean speed 0.0835 m/s, 3.6 % above (21) | 1.04323 T; 11.239 cm; 0.083485 m/s; +3.589 %; SVG dots 11.2 cm apart | verified |
| C48 | §07 | gap 0.93 % at ak = 0.1, 0.24 % at ak = 0.05, about fourfold per halving | 0.926 %, 0.239 %; ratios 3.88 and 3.87 | verified |
| C49 | §07 | z0 = −0.56 m: computed 5.39 mm/s, (21) 5.38 mm/s | 5.394 and 5.381 mm/s | verified |
| C50 | §07 | default U_S = 0.68 m/s, a third of c | Store `stokes` = 0.67775 m/s; (ak)² = 0.336 | verified |
| C51 | §08 (changed) | 90 parcels | Store dims 5 × 18; 90 parcels recomputed | verified |
| C52 | §08 (changed) | surface line 307 points wide, 174 narrow; drawn, not stored | Canvas counted: stroke path 307 vertices (field 800), 174 (field 400); fill path 309 and 176 (+2 corners); no store write in those loops | verified |
| C53 | §08 (changed), §9 | W_field = 800 px = 8 m, or 400 px = 4 m below 560 screen px | Code `box.w < 560 ? 400 : 800`; measured 800 at canvas 770 and 630, 400 at 356 | verified |
| C54 | §9 | calm level at 28 % of H, or lower if crests come within 34 px of the top | Store ys = 102.48 = 0.28 × 366 (a·s + 34 = 57.1 smaller) | verified |
| C55 | §9 | surface point every 3 px of rest position from −60 to W_field + 60 | Code `for (X = -60; X <= WORLD_W + 60; X += 3)` (last point 858 and 459) | verified |
| C56 | §9 | rose tint 36 % at crest height to 5 % at the bottom | Gradient from `ys - A * s` to `h`, alpha 0.36 → 0.05 | verified |
| C57 | §9 | dots 3.8 px at the surface, 3.1 px below; followed column larger | Arcs counted: 17 × 3.8, 68 × 3.1, followed 1 × 6 and 4 × 5 | verified |
| C58 | §9 | followed column i = 8, X0 = 378.2 px (wide) or 190 px (narrow) for 18 parcels | Store follow = 8; X0[8] = 378.235 and 190 | verified |
| C59 | §10 | tanh π = 0.9963; 0.19 % slower at h = λ/2 | 0.99627; 1 − √0.99627 = 0.187 % | verified |
| C60 | §10 | σ = 0.0728 N/m for clean water at 20 °C | IAPWS Revised Release on Surface Tension of Ordinary Water Substance: 72.74 ± 0.36 mN/m at 20 °C; 0.0728 is within the uncertainty | verified |
| C61 | §10 | capillary below λ = 2π√(σ/ρg) = 1.71 cm; no wave slower than 0.231 m/s | 1.712 cm; c_min = (4gσ/ρ)^{1/4} = 0.2312 m/s (ρ = 1000; with 998.2: 1.713 cm, 0.2313); both terms equal there (SymPy). This is the phase speed; the group speed dips lower, to 0.178 m/s near 4.4 cm, which the sentence does not claim otherwise. | verified |
| C62 | §10 | speed × (1 + ½(ak)²), 2 % at ak = 0.2 | Stokes third-order deep-water result; ½ × 0.04 = 0.02 | verified |
| C63 | §10 | ν = 1.0 × 10⁻⁶ m²/s; amplitude e-folds in 24 h for the 2.6 m wave | 1/(2νk²) = 85 616 s = 23.8 h | verified |

## D. The numerical method against the code, line by line

| # | Note says | Code | Verdict |
|---|---|---|---|
| D1 | §08: positions in closed form, never a differential equation stepped; each frame evaluates the formulas afresh; only the phase is accumulated | `draw()` evaluates (17) for every parcel each frame; the only accumulator is `omegaT` | verified |
| D2 | §08: the phase is accumulated "from the time Δt between frames" | `scripts/sim.js`, `clock()`: `dt = last ? Math.min((ts - last) / 1000, 0.05) : 0` | **wrong, because** Δt is the time between frames capped at 0.05 s, not the time between frames. Measured: a 500 ms main-thread stall advanced ωt by 0.324 rad = 2πf (0.05 s + one 16.6 ms frame), not the 2.43 rad of the real gap. Correct: "from the time Δt between frames, capped at 0.05 s so that a stalled or hidden tab does not make the wave jump; after a long pause between frames the picture lags the clock." |
| D3 | §08: dispersion on, f from (13) at full precision, slider only displays it rounded to 0.01 Hz; off, f is the slider value | `f()` returns `Math.sqrt(G * k() * PX_PER_M) / (2 * Math.PI)` or `freq.value`; `couple()` sets the slider. Measured: store f = 0.7749218, slider value 0.77, output "0.77 Hz"; off: f = slider value | verified |
| D4 | §08: summing the phase keeps the motion smooth when f changes | θ = kX0 − ωt with ωt continuous; a clock-based ωt would jump when f changes | verified |
| D5 | §08 list: X0 = 30 + (W_field − 60) i/(N − 1), z0 = −56 j, r = a e^{kz0}, θ = kX0 − ωt, ξ = −r sin θ, ζ = r cos θ, u = rω cos θ, w = rω sin θ | `var X0 = 30 + i * (WORLD_W - 60) / (N - 1)`, `z0 = -j * DZ`, `r = A * Math.exp(kk * z0)`, `th = kk * X0 - omegaT`, `xiM[q] = -r * Math.sin(th)`, `zeM[q] = r * Math.cos(th)`, `uM[q] = r * om * Math.cos(th)`, `wM[q] = r * om * Math.sin(th)`. Stored arrays recomputed from stored inputs: max difference 1.8 × 10⁻¹⁵ to 1.1 × 10⁻¹³ | verified |
| D6 | §08 (changed): every parcel number written into the store at the line that computes it; the panel reads from there | Same line of `draw()` writes `X0A, thM, xiM, zeM, uM, wM, pxM, pyM`; `rL, zL, cyL` per layer | verified |
| D7 | §08: nothing integrated, so nothing accumulates error; positions exact up to double rounding however long the page runs | Positions are recomputed each frame. Note: the phase sum itself gathers rounding (at most about one ulp of ωt per frame, ~10⁻⁴ rad after a day at 60 fps), which shifts the timing but never moves a parcel off its exact circle | verified |
| D8 | §08: a = min(A, 0.9/k) | `function a() { return Math.min(amp.value, 0.9 / k()); }` | verified |
| D9 | §9: dashed line at the calm level, the centres of the surface orbits | `ctx.setLineDash([5, 6])`, line at `ys` | verified |
| D10 | §9: orbits dotted, solid for the followed column, only while radius > 1.2 screen px | `setLineDash(isF ? [] : [2, 3])`, `r * s > 1.2`; measured 17 dashed + 1 solid per drawn layer | verified |
| D11 | §9: the surface line passes through points every 3 px that are not stored parcels | See C52, C55 | verified |
| D12 | §9: "the canvas rounds every position to its own pixel grid" | Canvas 2D in Chromium antialiases; it does not round coordinates | **wrong, because** positions are not rounded. Measured in the same Chromium: a filled disc of radius 3.1 at x = 10.0, 10.25 and 10.5 px gives edge alphas 14/252 … 253/11, 0/200 … 255/72 and 0/136 … 255/136, so a quarter-pixel shift survives as partial coverage of the edge pixels. Correct: "the canvas paints on its own pixel grid, spreading a position that falls between pixels over the edge pixels (antialiasing)". The data panel's `about` text, outside the note, has the same wording. |
| D13 | §9: layers below the bottom of the canvas are computed and stored but not drawn | `var visible = cy <= h - 8;` the loop stores before `if (!visible) continue;` | verified (true as written; the exact test also skips a layer whose centre lies within 8 px of the bottom; at the tested sizes all 5 layers are drawn) |
| D14 | §5: c_g appears in the data panel as a prediction; with dispersion off c_g = c/2 no longer applies | `ds.set('cg', c / 2)`; still written as c/2 when dispersion is off (measured 0.65 m/s at f = 0.50 Hz), which the sentence correctly calls inapplicable | verified |
| D15 | §07: the panel stores U_S from (21) as theory, not as motion | `ds.set('stokes', om * kk * PX_PER_M * am * am)`; nothing in `draw()` uses it | verified |

## E. References (§10.1, changed lines)

Road: curl with a browser user agent first; where curl got 403/202 (bot screens, not proof of a dead link), the Firecrawl scraper.

| # | Reference and link | Opens? | Cited part exists? | Verdict |
|---|---|---|---|---|
| E1 | Feynman, Leighton, Sands, Vol. I, ch. 51, §51-4 "Surface waves"; https://www.feynmanlectures.caltech.edu/I_51.html | curl: 403, body is Cloudflare's "Attention Required" bot page. Firecrawl: 200, the chapter page | Page shows "51 Waves", sections 51-1 Bow waves, 51-2 Shock waves, 51-3 Waves in solids, 51-4 Surface waves (deep-water circles, √(gλ/2π), group velocity one half). | verified |
| E2 | Acheson, OUP 1990, ch. 3 (waves): water waves, dispersion, group velocity, opening with a group crossing a pond; publisher's page and chapter abstract | Publisher's page: curl 202 (bot screen), Firecrawl 200, contents "3. Waves", paperback 9 August 1990. Chapter abstract: curl 403, Firecrawl 200 (redirects to chapter-abstract), title "Waves", DOI …0198596608.003.0003 | Abstract: "When a group of waves moves across the surface of a pond, each particular wavecrest travels faster than the group as a whole…". Section list (KTH SG2221 reading list, which reproduces the book's contents, read whole): 3.2 Surface waves on deep water, 3.3 Dispersion: group velocity, 3.4 capillary waves. | verified |
| E3 | Kundu, Cohen, Dowling, 6th ed., Academic Press 2016, ch. 8 (gravity waves): surface tension, group velocity, nonlinear waves; ScienceDirect chapter page | curl: 403; Firecrawl: 200 | "Chapter 8 - Gravity Waves", Fluid Mechanics (Sixth Edition), 2016, pp. 349–407, Academic Press; keywords include capillary waves, group velocity, nonlinear waves, standing waves. | verified |
| E4 | Landau and Lifshitz, 2nd ed., Pergamon 1987, §12 and §25; Elsevier page | curl: 200; Firecrawl: 200 | Contents list "§12 Gravity Waves" and "§25 Damping of Gravity Waves". The page dates the 2nd edition's e-book 2013; the printed 2nd edition (this ISBN) is Pergamon 1987, as cited. | verified |

## Summary

118 rows (23 equations, 13 unnumbered steps, 63 numbers, 15 method lines, 4 references): 116 verified, 2 wrong (D2: Δt is capped at 0.05 s; D12: the canvas antialiases, it does not round positions), 0 unverifiable.
All 23 numbered equations, every number in the text, table and figures, and every changed line check out.
