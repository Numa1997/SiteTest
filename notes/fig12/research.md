# Fig. 12: use cases and open teaching material on slosh, foam and liquid rendering (6 November 2026)

Read for the page by a research agent of the session (primary sources opened; downloads kept outside the repository).
Licences as stated by each source. Opinions are marked.

## Real-world use cases
- **Food-serving robot**: Choi et al., Robotics and Autonomous Systems 179, 104728 (2024) (abstract and preview read): exponential
  reference-shaping filter, LQ tracking holding the body level, disturbance observer; no slosh model. Code: github.com/superchd/anti-sloshing-robot (no licence; learn only).
- **Robot arm carrying water**: Moriello, Biagiotti et al., ICRA 2017: spherical pendulum tuned to the first mode, exponential FIR
  trajectory filter; added delay 0.644 s (1 L), 0.515 s (2 L).
- **Packaging (Tetra Pak)**: Grundelius, PhD thesis, Lund 2001: minimum-energy acceleration profile on a 2nd-order slosh model plus
  iterative learning; 7.4 % shorter moves in production; tilting the package ~20 % shorter for the same peak surface.
- **Transport track**: B&R SuperTrak anti-sloshing profiles (press release 2017, no numbers); Rothenbuchner, TU Wien diploma thesis
  (2023): flatness-based feedforward, "virtual tray" pendulum, slosh angles up to 38° handled on an ACOPOS 6D shuttle.
- **Molten-metal ladle**: Noda, Yano, Terashima, J. Robotics Soc. Japan 24, 94 (2006): frequency tracked by short-time FFT as the
  ladle tilts, notch filters.
- **Lab rig**: Pridgen, Bai, Singhose (Georgia Tech), "Slosh suppression by robust input shaping": ω = 12.5 rad/s, ζ = 0.008;
  peak transient slosh vs unshaped (simulation): ZV 50 %, ZVD 25 %, SI 19 %.
- **Rocket**: Falcon 1 Demo Flight 2 (2007), SmallSat paper SSC07-III-6: LOX slosh coupled with steering ~90 s into the second-stage
  burn, roll, engine shutdown; fix: baffles and control changes.
- **Handbook**: NASA SP-106 (Abramson 1966, public domain), ch. 4 damping (floating lids), ch. 6 mechanical models, ch. 7 control.
- **3D printers**: Klipper input shapers, `klippy/extras/shaper_defs.py` (GPL-3.0): ZV, ZVD, MZV, EI.

## Open code to learn from
| Repository | Licence | What |
|---|---|---|
| DocVaughan/CRAWLAB-Code-Snippets (`Input Shaping in C/`, `basic_InputShaping.py`) | BSD-style (Licenses/LICENSE.md) | real-time ring-buffer ZV, EI shapers |
| zabertech/zaber-examples `motion_input_shaping` | MIT | ZV, ZVD, EI shapers with an explanatory article |
| Klipper3d/klipper `shaper_defs.py` | GPL-3.0 | shaper definitions |
| learnsyslab/upright ("Keep It Upright") | MIT | MPC for the waiter's problem (ROS/OCS2) |
| LGST-LAB/slosh_ml | GPL-3.0 | pendulum-model parameters for any tank shape |
| evanw/webgl-water | MIT (file headers) | height-field water, Fresnel, refraction, caustics |
| matthias-research/pages, Ten Minute Physics 17, 18 | MIT (file headers) | 2D fluid, FLIP with particles |
| three.js Water2, dli/fluid, WebGPU-Ocean | MIT | browser water rendering |

## Open teaching material
- **Amer, Zentgraf, Ober, "Damping of Sloshing in a Moving Container"**, AALE 2026, doi:10.33968/2026.19, **CC BY 4.0**: an
  Arduino rig, modes 2.8 and 5.2 Hz, fitted G(s) = −26.2 s²/(s² + 0.703 s + 317); unshaped 24° peak, ZV 14° residual, two-mode ZVD
  to the noise floor. The best bachelor-level worked example found.
- SwRI, "Mechanical Analogs for Fluid Slosh Dynamics" (2024), derivations of the spring-mass and pendulum models.
- Vaughan, MCHE485 Mechanical Vibrations notebooks (BSD), and CRAWLAB input-shaping slides.

## Foam
- **Sauret, Boulogne, Cappello, Dressaire, Stone**, arXiv:1411.6542 (CC BY 3.0) = Phys. Fluids 27, 022103 (2015): cells 70 × 92 mm,
  3–19 mm wide, 4 cm of water–glycerol–detergent, 3 mm bubbles in layers; f₁ unchanged (3.1–3.3 Hz); 1/τ = 1/τ_ℓ +
  (1/τ_f∞)(1 − e^(−ξ/ξ_c)), 1/τ_ℓ ≈ 2 s⁻¹, 1/τ_f∞ = 9 ± 3 s⁻¹, ξ_c = 5 ± 2 (3 mm cell). Mechanism: Plateau borders sliding on the
  walls, 1/τ_f ∝ 1/w. The authors say true 3D is untested.
  Estimate by the research agent (not the paper's): in a pint, w ≈ 8 cm, the foam would add only 0.2–0.4 s⁻¹, comparable to the
  liquid's own damping.
- **Stout foam**: Watamura et al., Sci. Rep. 9, 5718 (2019), CC BY 4.0: Guinness bubbles ~50–61 µm, gas fraction 8 %, the cascade a
  roll-wave instability of the film on the tilted wall. Lee & Devereux, arXiv:1105.2263: N₂ ~50× less soluble than CO₂, small
  bubbles, long-lasting head. Bishop et al., J. Inst. Brew. (1975): N₂ or air foam half-life ~330–430 s, CO₂ foam ~4× faster.

## Walking with coffee
Mayer & Krechetnikov, Phys. Rev. E 85, 046117 (2012): f₁₁ ≈ 3.65 Hz for R = 3.5 cm, H = 10 cm (same formula as the note's (16));
cups 2.6–4.3 Hz; walking shakes at 1–2.5 Hz; the early peak acceleration sets the slosh; spills after 7–10 steps; focused walking
delays it by less high-frequency noise; anti-spill: flexible cups, ring baffles.

## Recommendations for the page (opinion)
1. A ZV/ZVD input shaper on the speed set-point and on the reader's push, tuned to the measured swing; state its cost (T/2, T).
2. Feedforward from the road ahead, and a slosh-state feedback, side by side with the PI loop.
3. Foam as extra damping only where the data support it; say that the measured cells were 3–19 mm wide and a pint is 80 mm.
4. Height-field shading with a Fresnel term; Beer–Lambert for the stout; spilled particles drawn as a stream.
5. Open the note with walking with coffee, then Falcon 1, then the packaging line; Amer et al. (CC BY) as the worked example.
