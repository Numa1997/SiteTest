# S3 report: chapters 0 and 1 (branch eb/ch01, based on eb/scaffold)

Files: `text/ch00.py`, `text/ch01.py`, `physics/ch01.js`, `ref/ch01.py`, `derive/ch01.py`, `data/ch01/thomson1897.json`, `notes/electron-beam/ch01/`.
**Needs one coordinator action:** apply `notes/electron-beam/ch01/contract-ch01.patch` to `contract.json` (see `requests.md`). I did not edit shared files.

## What is derived (all on the page, each step shown, each checked by SymPy: 24 identities PASS, `derive/ch01.py`)
Abbe limit from the grating equation; relativistic Lagrangian with q = -e from proper time; canonical momentum; Euler-Lagrange to the Lorentz force
(component by component); Hamiltonian and its form in p; energy conservation, gamma = 1 + eV/mc^2; why B does no work; non-relativistic limit
with the size of the correction (v/v_NR = 1 - 3 eps/4 + 23 eps^2/32; 4.4 % at 30 kV); wavelength; Helmholtz pair; exact helix and Busch-type focus
L = 2 pi v_par/Omega; RK4 stability function (|R|^2 = 1 - th^6/72 + th^8/576, phase th^5/120); Boris rotation = exact turn by 2 arctan(Omega h/2), phase
error th^3/12, polygon radius r_L sqrt(1+(Omega h/2)^2).

## What is checked, and how
- `check_parity.py`: PASS. ch01 JS = NumPy on 8 cases (E, B, helix, relativistic, both integrators); positions, angle, r_g agree to ~1e-16; only energy_drift
  (a difference of nearly equal numbers) differs, by up to 1e-13 absolute, covered by the stated absolute floor 1e-12 (named in the module).
- `check_numbers.py`: PASS. 425 declared numbers, browser string = Python string for every one; no uncomputed numeral (quoted values listed with sources).
  The Boris energy entries are rounding noise that differs between JS and Python, so the table says "noise" instead of printing them.
- `checks/selftest.py`: PASS. `check_page.cjs` (Chromium 360, 390, 1024, 1440): PASS, 0 KaTeX errors, no overflow, no outside request, both sliders-sims draw and move.
- Measured results: Thomson method on the simulated tube returns e/m to 0.62 %; the deficit is exactly gamma (0.9961) times arctan(y)/y (0.9977), product within 3e-6.
  Integrator slopes: Boris position -2.00, RK4 position -3.98, RK4 energy -5.00; RK4 at 16 steps/turn loses half its energy in 867 turns.
- Data: Thomson 1897 (all 26 + 7 rows, all columns) from C. J. Giunta's transcription; cross-checked row by row against S2's independent OCR digitisation
  (`check_thomson_vs_librarian.py`: 0 differences in m/e). Against CODATA 2018: method 1 gives 0.57-1.78x (tubes 1,2: 1.26x; tube 3: 0.67x), method 2 gives 0.45x.
  One printed W/Q (hydrogen, tube 1) disagrees by 10x with its own m/e and v: flagged on the page as a probable misprint.
- Applied's public statements were re-read on 9 November 2026 (WebFetch got 403; Exa answered) and quoted word for word, as public claims only.

## Open issues
- Textbook formulas (Jackson, Landau-Lifshitz, Griffiths, Hairer-Norsett-Wanner, Boris 1970, Qin 2013, Abbe 1873) are cited by book and chapter but were not
  re-opened this session; the derivations on the page are self-contained and SymPy-checked. The page says so under "Sources".
- Screenshots are in `notes/electron-beam/shots/` (git-ignored by the scaffold).
- The reading guide at the top of chapter 0 is S11's (slot left to the build).
- The plate fringe fields (d/l = 0.3) are the largest simplification of the model tube; the page says so and defers to chapter 4.
