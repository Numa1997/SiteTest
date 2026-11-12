# Fig. 14 · A wave packet meets a sphere · plan

Page `public/simulations/schrodinger-sphere.html`. Until now the note is a placeholder (L116–119: "The lecture note for this
figure is being written."), so the whole note is new. Written to Numa's verdict of 21 October 2026 (notes/STANDARD.md): a
chapter of a bachelor's textbook in the manner of J. R. Taylor, *Classical Mechanics*: a patient "we", every step shown, every
symbol defined where it first appears, "Key result" boxes, numbered worked examples with the page's numbers, Problems at the
end, ★ on the heavier passages with their results restated unstarred. No walkthrough exists (`data-walk` absent), so nothing to
keep in step there. The page's script and controls are being edited by another session at the same time: the note is put in
by one exact replacement of the placeholder article, nothing else in the page is touched. The doc
`docs/simulations/fig14-schrodinger-sphere.md` is written by another agent in parallel; the caller said not to edit it, so the
line anchors of the article are reported back instead.

## The chapter, section by section

| § | Title | What it does |
|---|---|---|
| head | Abstract | What the figure is, what the note does, how ★ works. |
| 1 | A ball, a wall and a pillar | Everyday pictures first: a ball thrown at a wall comes back; a swell in a harbour bends round a pillar and fills its shadow. A quantum particle does both. What the figure shows. Figure 1: the geometry (packet, sphere, the three slabs behind / inside / ahead, the absorbing border), drawn to the page's scale. |
| 2 | The model | Wave function, Born rule, the Schrödinger equation, the potential of the sphere, units ħ = m = 1 and what one grid unit means for an electron (a = 0.1 nm). The starting packet, its four numbers. Table: the page's parameters and the dimensionless numbers k₀σ₀, k₀R, R/σ₀, E/V₀, κR. |
| 3 | A free packet | Plane waves, ω = k²/2, phase and group velocity, the Gaussian packet as a sum of plane waves, momentum width 1/(2σ₀), mean energy E + 3/(8σ₀²). ★ the spreading law σ(t) = σ₀√(1 + (t/2σ₀²)²) derived by Fourier transform. Key result boxes. Example 3.1: the default packet (E = 2.5): k₀, λ, speed, flight time, width at the end, against the stored V₀ = 0 run. |
| 4 | A wall in one dimension | Step and slab. Inside, E < V₀: the evanescent wave e^{−κx}, decay length 1/κ. ★ The slab transmission T(E) by matching at both faces (transfer of amplitudes), both branches. Key result. Example 4.1: the default numbers (T ≈ 4 × 10⁻⁷) and the largest T on the page's grid for E < V₀. Over the barrier: resonances 2R·k′ = nπ. |
| 5 | A ball in three dimensions | Why the sphere is not a slab: the packet is as wide as the sphere, part misses it, part is reflected sideways, the wave bends into the shadow, and a packet carries a spread of energies so a fraction flies over the top. Classical estimates (fraction of the beam aimed at the disc, fraction with energy above V₀, a classical ensemble with the packet's own spread) against the stored quantum runs. Figure 2: the four probabilities against time for the default run, from the stored file. Figure 3: probability ahead at the end against V₀ for E = 2.5 and R = 2, 4, 6, from index.json, with the classical ensemble. |
| 6 | Solving it: the split-step Fourier method | The grid and the FFT; the kinetic step is a multiplication in k-space, the potential step in x-space; Strang's symmetric splitting. Key result: each factor is unitary, so the norm is kept exactly (measured without the border). ★ The error: BCH, local O(Δt³) from [T, V], global O(Δt²); a sharp sphere makes [T, V] large at the surface. Measured convergence in Δt. Resolution: k_max = π/Δx against the packet's largest k; phase per step. 32-bit against 64-bit. |
| 7 | The border and what "lost" means | Periodic box, the sin^{1/8} mask in the outer W = 12 cells, what it removes and when. Lost = 1 − ∫|ψ|². The free-packet check and the norm in the first quarter of every run. |
| 8 | Kaggle and the live preview | 405 runs, timing, file sizes; the live preview on 64³ (box shrink rule, Δt), and how far it is from Kaggle, measured. |
| 9 | From equation to screen | Which drawn thing is which symbol: |ψ| in z = 0 in 256 levels of the first frame's peak (clipping where interference exceeds it, measured), phase colours, the dashed circle, the scale bar, the curves panel, the readouts (slabs, not the sphere), the 1D guide; the frame shown is the stored one at or before the playback time; spatial smoothing of the 128 × 128 picture. |
| 10 | What the model leaves out | Spin, relativity, smooth potentials, real scatterers, measurement; the next model: stationary scattering theory, partial waves, cross sections. Problems box. Further reading. |

## The numbers, and how each is measured

All scripts in `notes/fig14/`; nothing estimated.

1. `runs.py` (NumPy): decodes the stored run files (`SPH1` header + zlib) and `index.json`: curves of the default run
   (E = 2.5, V₀ = 3, R = 4) and the cases quoted; the largest |∫|ψ|² − 1| over frames 0–12 of all 405 runs; σ_y against the
   free law for all V₀ = 0 runs; clipped pixels (level 255) after frame 0; total sweep time and bytes.
2. `reproduce.py` (JAX on this workspace's CPU, the page's own `solver.py` imported unchanged): the run E = 2, V₀ = 3, R = 4
   in 32-bit and 64-bit; Δt = 0.02, 0.01, 0.005, 0.0025 for the order of the time error; the free packet without the sphere;
   the norm without the absorbing mask (unitarity), 32-bit and 64-bit; the stored default run reproduced.
3. `derive.py` (SymPy): the spreading law from the Fourier integral; ⟨k²⟩ of the packet; the slab transmission by matching
   (both branches, checked against a direct linear solve); the symmetric BCH term of Strang splitting (and a matrix check).
4. `classical.py` (NumPy): a classical ensemble drawn from the packet's position and momentum spreads, moving in straight
   lines, refracted or reflected at the sphere's surface by energy and tangential-momentum conservation; probabilities in the
   three slabs at the run's end time; fraction of the beam aimed at the disc; fraction with k²/2 > V₀.
5. `live.cjs` (Node): `public/scripts/schrodinger-live-worker.js` run unchanged with a stub `postMessage`, for the three
   comparison cases and its run time.
6. `page.cjs` (Playwright + headless Chromium on `npm run build` output, served locally): the store with the defaults at the
   last frame (behind, ahead, inside, lost, σ_y, σ_free, T1D, t, steps, wall, sha_ok), the frame times, canvas size and scale,
   KaTeX errors, equation tags, console errors, horizontal overflow at 1440 × 900 and 390 × 844, folds.

## Sources to open before citing

Griffiths & Schroeter, *Introduction to Quantum Mechanics* (3rd ed.), ch. 2 (free particle, finite well/barrier, Problem on
the rectangular barrier); Sakurai & Napolitano, *Modern Quantum Mechanics*, ch. 2 (time evolution, wave packets); Feit, Fleck &
Steiger, J. Comput. Phys. 47, 412 (1982); Strang, SIAM J. Numer. Anal. 5, 506 (1968); an open source on absorbing boundaries
(Kosloff & Kosloff 1986) and on splitting error (Jahnke & Lubich 2000) if they open. Each one only if opened in this session.
