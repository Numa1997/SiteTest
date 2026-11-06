# Two-way Navier–Stokes for project 05: research and prototype (5 November 2026)

Scratchpad only; nothing in the repository was changed.

## Sources read whole (in `src/`)
- Kolomenskiy & Schneider 2009, J. Comput. Phys. 228, 5687 (`ks_jcp2009final.txt`): penalized NS (4), forces as volume integrals (6)-(7),
  vorticity form (8), AB2 + exact viscous factor (16)-(17), stability dt < eta (App. B), smooth mask needed for moving bodies (sec. 4.2, App. A),
  free fall coupling (54)-(56), first-order coupling.
- Engels, Kolomenskiy, Schneider & Sesterhenn 2013, Comput. Struct. (`ekss_cas_2013_proof.txt`): force (4) = int chi/eps (u-us) + d/dt int us;
  vorticity sponge (sec. 3.1.2); erf mask (sec. 3.1.4); explicit staggered coupling fails for light bodies (artificial added mass), sec. 3.3.
- Schäfer & Turek 1996 (`dfg_benchmark_results.txt`): 2D-1 cD in [5.57, 5.59], La in [0.0842, 0.0852]; 2D-2 cDmax [3.22, 3.24], cLmax [0.99, 1.01], St [0.295, 0.305].
- LilyPad source (`src/lilypad/BDIM.pde`, `Body.pde`): BDIM mixing u = del*F + (1-del)*u_b; FSI via pressure force and a lagged added mass in `react()`.
- LilyPad wiki: "the Reynolds number set in the code will not be reflected in the results if the flow is under-resolved".

## Solver (`ns2.cjs`)
2D incompressible NS, vorticity state, Fourier pseudo-spectral, 2/3 dealiasing, SSP-RK3 with exact viscous integrating factor,
then implicit (backward-Euler) Brinkman penalization and velocity sponge, projected through the curl. Forces: Engels (4).

## Tests
| Test | Result | Script / log |
|---|---|---|
| Taylor–Green, N = 64…1024 | max error 1.2–2.0e-15 | `t_tg.cjs` |
| Speed, 3 FFT/step (Node, 1 core) | 256²: 17 ms, 512²: 87 ms, 1024²: 433 ms | `t_tg.cjs` |
| Speed, full step 512×128 / 1024×256 | 77–80 ms / 336–385 ms | `st1_*.log` |
| Unsteady Stokes, oscillating cylinder (Wolfram) | F = -rho pi a² [1 + 4K1(ka)/(ka K0(ka))] dU/dt | Wolfram call, this session |
| Oscillating cylinder, mixing, 20 / 40 cells per D | cos +18.7 % / +9.9 %, sin +8.7 % / -3.2 % | `osc_256_mix.log`, `osc_512_mix.log` |
| Interior-fluid identity E[T_in] = rho b int a·dr/dq | difference 0 (slab rod on cart) | Wolfram call, this session |
| WebGL2 in headless Chromium | SwiftShader (CPU), float render targets yes | `gl.cjs` |

### Schäfer–Turek 2D-1 (Re 20), cD and La
| Immersion, mask | 10 /D | 20 /D | 40 /D |
|---|---|---|---|
| implicit penalty, erfc 1 cell | – | 6.838, 0.0999 | – |
| mixing, erfc 1 cell (CFL 0.6) | 6.528 | 5.652, 0.0864 | 5.387, 0.0810 |
| mixing, erfc 1 cell, CFL 0.3 / 0.15 | – | 5.863 / ≈6.07 | – |
| mixing, erfc ½ cell / 1.5 cells | – | 5.260 / 6.196 | – |
| penalty, ramp (CFL 0.6 / 0.3) | 5.867 | 5.215 / 5.270 | 5.263 |
| penalty, ramp, no dealiasing of the correction | 5.757 | 5.202 | – |
| penalty, ramp, full-strength inlet (dt ≈ 5.7 / 2.9 / 1.5 ms at 20 /D) | 6.020 | 5.361 / 5.418 / 5.473, La 0.0829–0.0833 | 5.408, La 0.0832 (dt 2.9 ms) |
| same, exact exponential penalization | 6.034 | 5.370 / 5.428 | – |
| reference band | | 5.57–5.59, 0.0842–0.0852 | |

Mixing is not time-consistent (cD rises ~0.21 per halving of dt). Penalty + ramp + corrected inlet: grid-converged at fixed dt
(5.418 at 20 /D vs 5.408 at 40 /D, both dt 2.9 ms), -3.0 % in cD, -1.3 % in La; but cD still drifts +0.056 per halving of dt
(splitting error of advect / penalize / project). Open: put the penalization inside the time integrator.

## 6 November: penalization inside the integrator, and the cart-and-rods demo
- `ns2.cjs` option `inRhs`: the Brinkman term and the sponge are part of the RK3 right-hand side (K&S eq. 8), dt ≤ 2η, force = ∫χ/η(u − u_s) at the first stage + d/dt∫χu_s.
- Re 20 benchmark with it, η = 2e-4 (dt 4e-4), corrected inlet, ramp mask: 20 /D: **cD 5.621, La 0.0847** (band 5.57–5.59, 0.0842–0.0852); 10 /D: 6.71 (η 2e-4), 6.81 (η 1e-4). Logs `b512_inrhs.log`, `b256_inrhs*.log`.
- The split scheme's booked force on moving bodies is not convergent in dt (glycerol demo: 1209 / 692 / 1572 N at CFL 0.6 / 0.3 / 0.15, `dtprobe.cjs`).
- Demo `play_bundle.html` (self-contained; `shoot.cjs` renders frames). Air at real ν blows up on 0.6 cm cells (Re 3.6e4): `frames_512/t1.00.png`.
- Glycerol (ρ 1261, μ 1.412), breeze 1.5 m/s, 256×128 over 3.0×1.6 m, inRhs η 2e-4 (`isoprobe.cjs`, `frames_cart_*`):
  still cart alone 0.249 → 63 N (2D wall ½·2·0.12·1.5² → 68 N; page law 48 N with the 3D box C_D 1.28);
  moving cart alone at t = 1 s (v = −0.61 m/s) 0.539 → 136 N (2D wall at 2.1 m/s → 133 N);
  with the swinging rods: cart 7.3 (×30), rods 28–45 per unit → 1000 N each, max fluid speed 12 m/s in a jet under the rail (`whereprobe.cjs`):
  the in-plane rods are 50 cm paddles sweeping a 1.6 m box; the displaced fluid returns through the 11 cm slot under the cart. Artefact of the 2D world, not of the scheme (both schemes agree).

## Cart alone at rest in a breeze (`cartfield.cjs`, logs `cf2_*.log`, fields `cf2_*/field.json`)
256×128 over 3.0×1.6 m (1.17 cm cells), inRhs η 2e-4, cart centred vertically (yc 0.8; at 0.25 the bottom sponge gave a spurious mean lift of 77 N),
seed vortex 0.5 /s behind the cart (without it the flow stays mirror-symmetric and never sheds), 6 s, means over the last 2 s; depth 0.2 m.

| medium | U m/s | Re_h | solved drag N | page law N (cc U² + cl U) | ratio | lift amplitude (sd) N | St = f h/U |
|---|---|---|---|---|---|---|---|
| glycerol | 0.5 | 54 | 7.2 | 6.4 | 1.14 | 0 | – |
| glycerol | 2 | 214 | 79.9 | 83.5 | 0.96 | 25.9 | 0.161 |
| glycerol | 4 | 429 | 327.5 | 322.0 | 1.02 | 145.6 | 0.185 |
| honey | 0.5 | 12 | 17.4 | 12.9 | 1.34 | 0 | – |
| honey | 2 | 49 | 131.3 | 117.2 | 1.12 | 0 | – |
| honey | 4 | 97 | 391.9 | 408.8 | 0.96 | 15.2 | 0.119 |

Preview: `site/simulations/preview.html` (a copy of the page + `solved.js`, symlinked assets), shots in `preview_shots/`.
Overlay hides |ω| < 12 % of the colour scale (Gibbs ringing of the cart's sharp mask) and the sponge layers.

## Blade added mass (`t_blade.cjs`)
Rod as a 2D blade, chord 0.5 m, 2 cm thick, oscillating across itself, nu = 1e-5, 1 cm cells: m_a = 0.169 per unit density and depth,
0.86 of rho pi (c/2)^2 = 0.196. In water at 2 cm depth: 3.4 kg on a 0.5 kg rod.
