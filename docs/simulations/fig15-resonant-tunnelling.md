# Fig. 15 · Resonant Tunnelling

| | |
|---|---|
| Page | [public/simulations/resonant-tunnelling.html](../../public/simulations/resonant-tunnelling.html) (English only, listed in `ENGLISH_ONLY` of [tools/i18n/build.py](../../tools/i18n/build.py)) |
| Lecture note | [public/scripts/resonant-note.js](../../public/scripts/resonant-note.js) (the whole study, injected into the page's `<article>` and typeset by `sim.js`) |
| Data | [public/data/resonant-tunnelling/](../../public/data/resonant-tunnelling/): `generations.json`, and the generation of 2026-11-13: `derived/index.json` (72 runs, with parents), `derived/runs/*.bin`, `curves.json` |
| Reconstruction & checks | [tools/kaggle/resonant-tunnelling/](../../tools/kaggle/resonant-tunnelling/) |
| Equation checks | [notes/fig15/derive.py](../../notes/fig15/derive.py), [notes/fig15/derive.md](../../notes/fig15/derive.md) (SymPy + NumPy, 24/24) |
| Brief & lessons | [notes/fig15/BRIEF.md](../../notes/fig15/BRIEF.md), [notes/fig15/LESSONS.md](../../notes/fig15/LESSONS.md) |
| Catalog entry | [public/scripts/catalog.js](../../public/scripts/catalog.js) (`id: 'resonant-tunnelling'`, `fig: 15`, `field: 'quantum'`) |

Two thin barriers a few nanometres apart. A single barrier passes a slow quantum particle about 6 % of the time; the pair,
at one special energy, passes it with certainty. **The page plays frames built from the exact rules of one-dimensional
scattering applied to data already computed; it computes nothing.** It shows the resonant transmission peaks, the trapped
state that leaks out with lifetime `τ = ħ/Γ`, and the current–voltage curve of the resonant-tunnelling diode with its
region of negative differential resistance.

This is the first **derived-data** figure: its frames are generated from the stored solutions of Fig. 14, not from a new
full simulation. See [kaggle-pipeline.md](../kaggle-pipeline.md), "Derived data: generated from stored runs".

## What the reader sees and sets

- **The main figure** (Fig. 15): a wave packet, drawn as `|ψ|²` (or `Re ψ`) riding on the energy line `E`, meeting two
  **static solid barriers** that rise to `V₀ = 3`. A **Space–time** view draws `|ψ(x,t)|²` over the `(x, t)` plane (paper →
  wine), where the trapped state shows as a bright column between the barriers.
- **Fig. 15b**: transmission `T(E)` for the chosen geometry (wine) and for one barrier (dashed), with the resonance peaks
  marked and the packet's mean energy and packet-average `T̄` shown.
- **Fig. 15c**: the probability reflected, trapped and transmitted against time, with the exponential fit of the trapped
  state and its measured lifetime `τ`.
- **Fig. 15d**: the current–voltage curve `J(V)` (Tsu–Esaki), with the peak, valley and the backward-sloping region shaded.
- **A real-units panel**: the same device in GaAs/AlGaAs (nanometres, meV, fs, kA/cm²).
- **Controls**: the barrier spacing (resonant pair `s = 2.343`, detuned pair `s = 3.454`, wide double well `s = 6`); the
  pulse length (short `σ₀ = 3`, broad in energy; long `σ₀ = 12`, sharp in energy, stored at the resonance energies only);
  the packet energy across the stored grid; a time slider; Play / Pause / From the start.

## How the data is made (and why it is honest)

The Schrödinger equation is linear, so a solution computed once is a basis. The exact **plane-wave scattering states** of the
two barriers come from transfer matrices ([tm.py](../../tools/kaggle/resonant-tunnelling/tm.py), Griffiths & Steinke 2001). A
moving packet is their superposition,

    ψ(x, t) = ∫ φ(k) ψ_k(x) exp(−i E_k t) dk,

exact for `V ≥ 0` when the packet starts wholly left of the barriers (the start-overlap error is below 10⁻⁵ of the peak and
is stored per run). [recon.py](../../tools/kaggle/resonant-tunnelling/recon.py) evaluates this and stores the frames (`RTF1`:
a JSON header, then float16 `Re ψ` and `Im ψ` on the stored window and on a magnified stretch around the pair). The page
plays the stored frames, interpolating between them in the frame that turns at the packet energy, and computes nothing. The
barriers are drawn as static solids.

Three checks (all in `curves.json`, `derived/index.json` and the scripts):

1. **Against Fig. 14.** The single-barrier amplitudes everything is built from were read off Fig. 14's stored flat-wall runs
   ([extract_t.py](../../tools/kaggle/resonant-tunnelling/extract_t.py), [b1_survey.py](../../tools/kaggle/resonant-tunnelling/b1_survey.py)).
   On the 0.5 a / 8-bit stored grid the extraction confirms the exact `|t|²` to a few percent (median 3 %, worse in the tail)
   — enough to trust the exact amplitudes, too coarse to use directly, so the exact ones are used. This is the brief's
   anticipated outcome.
2. **An independent solve.** [cn.py](../../tools/kaggle/resonant-tunnelling/cn.py) solves the double barrier with
   Crank–Nicolson (the scheme of Fig. 14's `flat.py`) and agrees with the reconstruction frame by frame to **0.6 % of the
   peak** ([check_cn.py](../../tools/kaggle/resonant-tunnelling/check_cn.py)).
3. **Probability.** The stored total probability stays `1.000` (worst deviation ~3×10⁻⁶; Simpson quadrature).

Storage error (float16) is below 0.04 % of the peak; the between-frame interpolation misses the exact wave by below 0.1 % of
the peak (both measured in `recon.py`).

**Provenance.** [pack.py](../../tools/kaggle/resonant-tunnelling/pack.py) writes each derived file with its SHA-256 and names
its **parents** — the 45 Fig. 14 flat-wall runs of the same barrier (`V₀ = 3`), by generation, file name and SHA-256 — in
`derived/index.json`, together with the script and commit that built it.

## The device

[iv.py](../../tools/kaggle/resonant-tunnelling/iv.py) computes `T(E, V)` for the biased (tilted) barriers as a staircase of
transfer matrices (convergence checked; the zero-bias case matches the exact solver to 10⁻⁸) and integrates the Tsu–Esaki
supply function. For the resonant pair the curve peaks at `V ≈ 1.1`, falls to a valley at `V ≈ 2.3`, with a peak-to-valley
ratio ≈ 6.9. [real_units.py](../../tools/kaggle/resonant-tunnelling/real_units.py) anchors `V₀ = 3` to the AlGaAs
conduction-band offset (0.30 eV) with `m* = 0.067 mₑ`, giving a length unit `a = 3.37 nm`: barriers 3.37 nm, well 4.53 nm,
resonance 100 meV, `Γ = 4 meV`, `τ = 166 fs`, peak current ≈ 4.7×10² kA/cm² at 110 mV.

## The store and the data panel

Every number shown is written into the page's `Sim.dataset` where it is read, and the panel ([datalog.js](../../public/scripts/datalog.js))
only reads it. The checks: `k₀ = √(2E)`; `∫|ψ|² = P_ref + P_in + P_tr` from the stored per-frame probabilities; and Read
values pins a point of the wave and reports `Re ψ`, `Im ψ`, `|ψ|²` there, with the sheet's own vertex read back from the
picture.

## Measured (headless Chromium, 2026-11-13)

- The resonant pair at `E = 1` loads, its SHA-256 matches, probability stays `1.000`, and it plays at 60 fps (median gap
  16.7 ms, max 23 ms) with no console errors at 1440 × 1000 and 390 × 844; no horizontal overflow.
- Every geometry, pulse length and view (probability, wave, space–time) switches without error.
- The lecture note typesets with 0 KaTeX errors (318 formulas, equations (1)–(16)).
- `τ` from the `T(E)` peak width (`Γ = 0.040 → τ = 25.1`) equals `τ` fitted from the trapped-probability decay (`25.1`).

## Lessons from Fig. 14 followed here

The animation plays stored frames only, interpolated smoothly, with a static solid barrier and no per-frame stalls
(`notes/fig15/LESSONS.md`). No Kaggle GPU was used (this 1D project is cheap and runs locally in minutes). The derivation is
built from the differential equation with no skipped steps and one running example, verified in SymPy/NumPy
(`notes/fig15/derive.py`); Wolfram was requested but its connector was unavailable this session, so the checks are to be
re-run in Wolfram when it is back.
