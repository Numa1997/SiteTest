# data/ch05: aberration coefficients and a probe-size check

## objective_lens_cs_cc.csv  (data item f)
- **What it is not**: the brief asked for "typical Cs, Cc of SEM objective lenses from a textbook". I did **not** find them in a textbook I could open (Reimer and Goldstein et al.
  are named in search results, not opened). This file holds the values I could read in open papers and a vendor white paper. Eleven rows, all in mm in the
  source; SI columns added. `how_read`: `ABSTRACT` = read the abstract (open), `EXCERPT` = read a search excerpt of the page, not the whole paper: open the source before quoting.
- **Kinds of number**: "assumed typical" (Joy), "stated for an uncorrected system" (CEOS), "calculated" (Tsuno et al.; the immersion-lens paper; the manufacturer's calculated values for the
  LVEM microscopes), and one **requirement**, not a lens: Cs below 100 µm and Cc below 84 µm for a probe under 1 nm at 1 keV (Zach, as quoted).
- **Uncertainty**: none given. The rows span a factor of 50 in Cs (0.1 to 5 mm) because they describe different lens types and conditions; the order "Cs and Cc of the
  order of the working distance, in mm" is Joy's rule of thumb, and Bačovský states C_c ≈ f for magnetic lenses (excerpt).
- **Scherzer's theorem** (CEOS white paper, excerpt): "in 1936 Otto Scherzer proved that chromatic aberration (Cc) and spherical aberration (Cs) for rotational symmetric, charge free and static lenses
  are always positive and that they cannot be compensated completely". The white paper cites it as its Ref. [1]; I did not see that reference line. The original (Z. Phys. 101, 593 (1936), from memory) is NOT OPENED.

## Probe-size check against a published worked example (computed here)
Joy (2006) gives the three terms d_Chr = Cc α ΔE/E, d_Diff = 0.61 λ/α, d_Sph = ½ Cs α³ and an example: Cs = Cc = 5 mm, E = 1 keV, ΔE = 0.7 eV (Schottky), "optimum" α of
4 to 5 mrad giving "a spot size of about 18 nm", terms added in quadrature (excerpt of the paper).
My computation (λ = h/√(2meE) with relativistic correction = 0.03876 nm):

| α (mrad) | d_Chr (nm) | d_Diff (nm) | d_Sph (nm) | quadrature sum (nm) |
|---|---|---|---|---|
| 2.6 (minimum) | 9.1 | 9.1 | 0.04 | 12.9 |
| 4 | | | | 15.2 |
| 5 | | | | 18.1 |

So the published "about 18 nm" is the quadrature sum at **5 mrad**, the upper end of the range he calls optimum. It is not the minimum probe size (12.9 nm at 2.6 mrad); Joy
chooses a larger α for more current (beam current ∝ α²: 2.6 mrad has 27 % of the current of 5 mrad). A linear sum of the three terms has its minimum, 18.2 nm, at 2.6 mrad.
Small typo in the excerpt: the constant in λ[nm] = 1.26/√E is printed 1.26; h/√(2me) is 1.2264 nm V^½ (E in eV here), a 3 % difference that moves the sum by under 2 %.
The quadrature sum itself is the thing Barth and Kruit (1996, abstract only read) call approximate; no source in this directory gives its error.
