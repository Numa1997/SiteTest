# S4 report · chapter 2, the source · branch `eb/ch02` · 9 November 2026

Marks: **Fact** (a handle to check it), **Inference** (my reasoning), **Opinion** (my judgment).

## What is on the branch

| File | What it is |
|---|---|
| `portfolios-src/electron-beam/text/ch02.py` | the chapter, 13 sections, about 8 700 words, 534 formulas, 8 figures and the live figure; `build()` |
| `physics/ch02.js` | solver, runs in the page and in Node; `physics/ch02_ui.js` the canvases and controls |
| `ref/ch02.py` | NumPy reference, written separately from the JS |
| `derive/ch02.py` | 19 checks (SymPy identities, mpmath, quadrature, a Runge–Kutta trajectory); writes `data/ch02/derive_results.json` |
| `data/ch02/` | published tungsten-tip data (CC BY 4.0), README with provenance, derive output |
| `notes/electron-beam/ch02/` | `check_parity.py`, `check_browser.cjs`, `build_preview.py`, `serve.py`, `render_math.cjs` (a preview harness, because the scaffold had not landed) |
| `notes/electron-beam/shots/` | screenshots at 360 and 1440 px |
| `notes/electron-beam/requests.md` | what the shared files need |

## Results of the checks (all run on this branch)

- **Fact.** `python3 portfolios-src/electron-beam/derive/ch02.py` → 19 of 19 pass.
- **Fact.** `python3 notes/electron-beam/ch02/check_parity.py` → browser solver against NumPy reference, worst relative difference 1.1×10⁻⁹ over 7 emission cases, v/t, tip current, hand-over, flux, coverage, cycle.
- **Fact.** `node notes/electron-beam/ch02/check_browser.cjs` → at 360, 390, 1024, 1440 px: 0 KaTeX errors (534 formulas), 0 page and console errors, no sideways scroll, no request outside the site, all four canvases drawn (alpha counted before colour). The page's stored I_e, B_r, d_v equal the NumPy values to 10⁻¹⁴; ΔE on screen differs by 7×10⁻⁴ (display grid).
- **Not run:** the scaffold's own harness (it did not exist: no `eb/scaffold` branch when I worked), `npm run build`, i18n, inventory, redirects. Not done by me by design (coordinator).

## What the chapter does, in plain words

Derives, every step written: image-charge barrier and its roots, WKB transmission, supply function, Fowler–Nordheim with Forbes' v(f) and t(f), temperature factor, FN plot and its slope, Richardson and Schottky from the same integral, energy distribution and ΔE, reduced brightness, virtual source, Hertz–Knudsen flux, rate equation, emission against coverage (marked as an assumption in a box), flash cleaning. "Why the cold tip is bright but fragile" is closed in section 2.11 with computed numbers (J ∝ F^17.5, J ∝ φ^−26.6). Hand-over: I_e, B_r, ΔE, d_v for two presets, both in the text and live on the figure.

## Correlation with experiment

1. **Ayari et al. 2023, tungsten ⟨111⟩ tip, UHV (data on Zenodo, CC BY 4.0).** **Fact:** a plain FN line through the CSV gives slope −41 339 V and intercept 4.578, the authors' own numbers, so the unit reading is right. The model fit (φ = 4.5 eV, 300 K) gives ζ = 657.5 nm, rms ln I = 1.85 %, largest 5.8 %; the authors' own analysis has 653 nm. **Fact:** the fit is equally good for φ = 4.0 to 5.5 eV; only ζ moves (788 to 484 nm). **Inference:** the data cannot test φ; the radius from a slope inherits φ and k.
2. **Cho 2014, W(310), current decay against pressure (read in full).** **Fact:** p·τ₉₀ = 3.0, 2.6, 3.2 ×10⁻⁷ Pa·min at three pressures over a factor 29 (±9 %). The rate equation with Hertz–Knudsen flux predicts p·τ constant. **Inference:** this confirms the 1/p scaling; the single number κs ≈ 0.53 is fitted, so the absolute level is not an independent test, and I say so on the page.
3. **Hitachi High-Tech vendor page (read in full):** CFE ΔE 0.2–0.3 eV, Schottky 0.6–1.1 eV; virtual source 2.5–5 nm and 15–30 nm. **Fact:** my cold ΔE is 0.215 eV (not fitted); Schottky preset 0.43 eV (below the range); d_v 1.3 nm and 8.8 nm (below both ranges). **Inference:** the model has no electron–electron interaction, no extractor lens, no emitting-area spread; it is a lower bound.

## What I could not do, and what I assumed

- **Dyke & Trolan 1953 was not obtained** (the APS PDF returns 403 from this environment; the planning brief named it). No number from it is used. The Zenodo data set above replaces it, with its provenance.
- **The books in Google Drive were not consulted.** I did not search Drive. Textbook sources are not cited; sources listed are those I opened (listed on the page, with what I read). Forbes 2006 (Appl. Phys. Lett.) I cite through two papers that quote it, and say I did not open it.
- **The TU Delft Bronsgeest thesis and the NUS tungsten-life-cycle paper could not be fetched** (proxy errors). The Schottky work function 2.9 eV is an assumed value, stated as such on the page.
- **Applied's public statements** (1×10⁻¹¹ mbar, a single atom, cyclical self-cleaning) are quoted as public claims from PLAN.md; I did not re-open the press release.
- **Assumed, not measured (each is a control):** k (5 for the tip), φ = 4.5 eV, Schottky φ = 2.9 eV and apex field 0.5 V/nm, E_d = 1.9 eV, ν₀ = 10¹³ s⁻¹, Δφ_ads = 1.0 eV, N_s = 10¹⁹ m⁻², flash 5 s at 1000 K, threshold 0.7.
- **Model limit I did not hide:** a single adsorbed atom changes the current of a 50 nm tip by 1.2×10⁻⁴ (one of 8 200 emitting sites). The model does not reproduce Applied's "single atom" statement for a tip this size. It would for an emitting area of a few atoms.

## Two findings worth knowing

- **Fact.** The first version of the cap integral stopped at 25 % of the apex field and lost 2.4 to 6 % of the Schottky current. I now integrate the whole cap with 24 nodes (checked to better than 10⁻⁴ against 96 nodes).
- **Fact.** A slider cannot hold 1000 V exactly; 0.4 % of V is 7 % of the current (J ∝ F^17). The page keeps the exact value of each control in a variable and uses the slider only to change it.

## For Numa and the coordinator

- **Opinion.** The chapter is long (about 8 700 words). Sections 2.5 and 2.10 carry most of the weight; the ★ parts can be skipped. I did not run the referee or derivation-checker agents, and I did not tune layout by eye with Numa.
- **Fact.** Not committed: `notes/electron-beam/ch02/preview/` (generated, 0.8 MB; `python3 notes/electron-beam/ch02/build_preview.py` makes it; `python3 notes/electron-beam/ch02/serve.py` serves it at `/__preview/index.html`).
- Details for the scaffold are in `notes/electron-beam/requests.md`.
