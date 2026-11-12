# Computing on Kaggle: the Schrödinger test

Started 12 November 2026. Aim: simulation pages that compute nothing in the visitor's browser. Kaggle computes the runs
ahead of time on its GPU, the results are stored once, and the page only plays them back.

## `tools/kaggle/schrodinger-sphere/`

| File | What it does |
|---|---|
| [`solver.py`](../tools/kaggle/schrodinger-sphere/solver.py) | The time-dependent Schrödinger equation in 3D, units ħ = m = 1, by the split-step Fourier method (half a potential step, a full kinetic step in Fourier space, half a potential step) in JAX. A Gaussian packet (width σ₀ = 3, start x = −14) flies along x at a sphere of radius R with potential V₀ inside. The box is periodic (side 64) with an absorbing layer in its outer tenth. Each run stores 48 frames of \|ψ\| and arg ψ in the plane z = 0 (uint8, 128 × 128) and, from the whole 3D ψ, the probability behind (x < −R), ahead (x > R), the total, and the width σ_y. |
| [`pack.py`](../tools/kaggle/schrodinger-sphere/pack.py) | Compresses each run's frames (zlib level 9, base64) and writes them with the curves into the panel. |
| [`panel_template.html`](../tools/kaggle/schrodinger-sphere/panel_template.html) | The animator in the house colours. It computes nothing: it inflates the stored frames in the browser (`DecompressionStream("deflate")`) and plays them. Each slider has a dot under every position: filled when that run is stored, hollow when not; an unstored combination shows "not computed yet". Checks shown: the four probabilities sum to 1 until the packet reaches the border; with V₀ = 0 the measured σ_y(t) beside the free law σ₀√(1 + (t/2σ₀²)²); the 1D slab formula as a guide only. |
| [`build_smoke.py`](../tools/kaggle/schrodinger-sphere/build_smoke.py) | Writes `smoke.ipynb` for a given commit. The notebook downloads the three files above from this repository at that commit, so the code Kaggle runs is the code in git. |
| [`smoke.ipynb`](../tools/kaggle/schrodinger-sphere/smoke.ipynb) | The GPU test: checks the GPU (installs GPU JAX if missing, stops if there is no GPU), times one step on 128³ and 256³ cells in 32-bit and 64-bit, compares 32-bit with 64-bit and Δt with Δt/2 on one barrier run, computes 8 runs and writes `schrodinger_sphere.html`, `timing.json` and `progress.log`. |

Measured before Kaggle (this workspace, 4 CPU cores, 64³ cells): the free packet's width follows the free law to 2 × 10⁻⁶;
one step takes about 2.2 ms (8.4 ns per cell). The GPU numbers go here once measured.
