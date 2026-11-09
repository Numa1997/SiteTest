# data/ch02: published data used by chapter 2

## ayari2023_w111_iv.csv

Field-emission current–voltage data of one tungsten ⟨111⟩ tip in ultra-high vacuum.

- **Source:** A. Ayari, P. Vincent, S. Perisanu, P. Poncharal, S. T. Purcell, "All field emission experiments are noisy, … are any meaningful ?",
  arXiv:2301.13578 (31 January 2023), section III. Data set on Zenodo, <https://doi.org/10.5281/zenodo.7215660>
  (the file list I downloaded sits under record 10876708, `Fowler-Nordheim_analysis3.zip`, folder `Zenodo3/Data/`, ten text files `IV1u … IV5d`).
- **Licence:** Creative Commons Attribution 4.0 (`cc-by-4.0` in the Zenodo record metadata, read 9 November 2026).
- **What was measured (paper, section III.A):** tip made by electrochemical etching of a 125 µm tungsten wire, initial radius about 15 nm,
  heated several times for 30 s at 1700 K; base pressure 3×10⁻¹⁰ Torr (= 4×10⁻⁸ Pa); AC 1 V rms at 33 Hz on a DC voltage; current collected
  by a microchannel plate and phosphor screen; five voltage sweeps, each up (`u`) and down (`d`), 1300 V to 1630 V in steps of 10 V (33 points per sweep).
- **Columns:** `V_V` DC voltage on the tip in volt; `I_nA` DC current in nanoampere (units read from the authors' analysis notebook,
  `Idc = np.zeros(n0) #nA`); `dIdV_nA_per_V` lock-in derivative in nA/V. Values are the authors' numbers, rewritten as CSV, nothing else changed.
- **Authors' own fit (their Fig. 2, run 4 down):** FN slope 41339 ± 73 V, intercept 4.57 ± 0.05 (natural log, I in nA, V in volt), R² = 0.999903,
  standard deviation of the current about the fit 1.82 %, maximum deviation about 6 %; current drift about 8 % per hour.

## Not obtained

Dyke & Trolan, Phys. Rev. 89, 799 (1953), emitter X89, the classical tungsten data set (Forbes 2013 uses it as the reference for the physically
reasonable range 0.20 < f < 0.34). The page <https://link.aps.org/doi/10.1103/PhysRev.89.799> gives the abstract only; the PDF could not be opened from
this environment (HTTP 403), so no number from that paper is used anywhere in the chapter.

## source_properties_williams_carter.csv  (data item c, first part)
- **Source**: D. B. Williams, C. B. Carter, *Transmission Electron Microscopy*, chapter 5 "Electron Sources", Table 5.1
  "Characteristics of the Principal Electron Sources" (book page 74). Copy used:
  <https://iubemcenter.indiana.edu/doc/williams-and-carter/transmission-electron-microscopy-chapter-05.pdf>, PDF page 2.
- **How digitised**: read from a 250 dpi image of the table (the PDF text layer dropped every exponent, so the text could not be used).
  Values are **as printed**; the book gives them at 100 kV.
- **Units**: converted to SI where needed: the book already uses A m⁻², A m⁻² sr⁻¹, eV, K, Pa, nm, h. The column
  `reduced_brightness_computed_A_per_m2_sr_V` is **computed here** as brightness divided by 10⁵ V (the 100 kV of the table); it is
  not in the book. It ignores the relativistic correction V* = V(1 + eV/2mc²), which is 5 % at 100 kV.
- **Uncertainty**: none given in the book; the values are round, typical numbers (one or two digits). Treat each as good to a factor of about 2.
- **Known problems in the printed table (checked, not repaired)**:
  1. Richardson constants printed as 6×10⁹ (tungsten) and 4×10⁹ A m⁻² K⁻² (LaB₆). Demtröder Table 2.3 (p. 37) gives tungsten
     (1.5 to 15)×10⁵. With A = 6×10⁹ the Richardson law gives J = 1.7×10⁸ A m⁻² at 2700 K and 4.5 eV, far above the table's own
     current-density row, so the printed exponent is wrong; with A = 6×10⁵ it gives 1.7×10⁴ A m⁻², and with 1.5×10⁵ to 15×10⁵ it gives
     4.4×10³ to 4.4×10⁴ A m⁻².
  2. The tungsten current density is printed as "5" with no exponent; the LaB₆ value 10² A m⁻² is about 900 times below the Richardson
     value for 1700 K, 2.4 eV and A = 4×10⁵ (8.9×10⁴ A m⁻²). Do not overlay the current-density row on a Richardson curve.
  3. Richardson constants for the two field-emission guns are blank in the table.
- **Cross-checks (EXCERPT only, not digitised)**: Tsujino, *J. Vac. Sci. Technol. B* **40**, 030801 (2022) says space charge limits the
  reduced brightness of a field emitter to about 10⁸ A m⁻² sr⁻¹ V⁻¹, "the maximum B ... about 10¹³ A m⁻² sr⁻¹" at about 100 keV; this
  agrees with the cold-FEG row here (10¹³ and, computed, 10⁸). A JEOL table (<https://www.jeolusa.com/RESOURCES/Electron-Optics/Documents-Downloads/choose-the-right-sem-analysis-edition>) gives
  brightness 10⁵ A cm⁻² sr⁻¹ (= 10⁹ A m⁻² sr⁻¹) for thermionic W and 10⁷ to 10⁸ A cm⁻² sr⁻¹ for Schottky, energy spread 1 to 3 eV and
  0.5 to 0.6 eV, at an unstated voltage: the same order as here once the voltage is allowed for.
- **Still missing for data item c**: a measured value with an uncertainty for each source, from a primary paper (Bronsgeest et al. 2008 is
  located, not read). This table is a textbook summary, not a measurement.

## fn_tungsten_nanotip_li2025.csv  (data item b: a measured Fowler–Nordheim I–V set for a tungsten tip)
- **Source**: Y. Li, L. Xia, N. Li, S. Tang, Y. Ge, J. Wang, B. Xiao, Y. Cheng, L. K. Ang, G. Meng, "Uncovering a widely applicable empirical
  formula for field emission characteristics of metallic nanotips in nanogaps", *Nature Communications* **16**, 5583 (2025),
  doi 10.1038/s41467-025-60607-6. Figure 2a,b: measured I_m–V_m curves of one tungsten nanotip of apex radius 4 nm (from TEM images) against a gold plate,
  at gaps d = 5, 10, 15, 20, 25, 30, 50, 80 nm. In-situ TEM holder; the paper states a current resolution of 0.1 nA, gap adjustment to 0.04 nm
  and voltages up to 150 V (excerpt of its Methods).
- **How obtained (not digitised from a picture)**: the authors' own Source Data, `Source Data/Figure 2 a-b.xlsx` in
  <https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-025-60607-6/MediaObjects/41467_2025_60607_MOESM3_ESM.rar>. I took only the
  measured columns `Vm` and `Im(d=…nm)` of each block (771 points). The authors' theoretical Murphy–Good columns in the same sheet are **not** copied.
- **Units**: V in volts. The sheet has no unit for I. I take **nA**: the maximum is 101.7 in every block, and the paper's text speaks of currents of "2 nA",
  "10, 50 and 100 nA". `I_measured_A` is I × 10⁻⁹. `ln_I_over_V2…` and `one_over_V` are computed here, only where I > 0 and V > 0.
- **Uncertainty**: current resolution 0.1 nA (paper); the noise floor shows in the data (negative currents down to −0.28 nA at low voltage, 9 points).
  No uncertainty on V is stated.
- **Check done here (reproduce with `numpy.polyfit` on rows with I ≥ 2 nA)**: for each gap the plot of ln(I/V²) against 1/V is straight (rms residual 0.10 to 0.24).
  With φ = 4.5 eV, b = 6.83089×10⁹ V m⁻¹ eV⁻³ᐟ² (Forbes Eq. 18, recomputed), c_S² = 1.43996×10⁻⁹ eV² m V⁻¹ and v(f) ≈ 1 − f + (f ln f)/6 (Forbes Eq. 40), solving
  slope = −b φ³ᐟ² v(f)/β self-consistently gives, at the mid-range voltage of the fit:

  | gap d (nm) | fit range (V) | slope (V) | β = F/V (10⁷ m⁻¹) | apex field F (V/nm) | f | k = 1/(βR), R = 4 nm |
  |---|---|---|---|---|---|---|
  | 5 | 25.6–33.1 | −359 | 12.4 | 3.64 | 0.26 | 2.0 |
  | 10 | 30.4–39.2 | −391 | 11.1 | 3.86 | 0.27 | 2.3 |
  | 20 | 37.2–48.0 | −511 | 8.66 | 3.69 | 0.26 | 2.9 |
  | 30 | 42.0–53.8 | −659 | 6.98 | 3.34 | 0.24 | 3.6 |
  | 50 | 46.2–58.8 | −725 | 6.35 | 3.34 | 0.24 | 3.9 |
  | 80 | 51.5–66.0 | −729 | 6.13 | 3.60 | 0.26 | 4.1 |

  So the data are consistent with the Schottky–Nordheim theory of ch. 2 for polycrystalline tungsten (4.5 eV): the apex field at emission is 3.3 to 3.9 V/nm and
  f ≈ 0.25, and the tip-field relation F = V/(kR) holds with k between 2 and 4, rising as the anode moves away. The sharp 4 nm tip is the weak point: assumptions are
  φ = 4.5 eV, a constant emitting area, and the pre-exponential factor left free (only the slope is used).
- **What this is not**: it is not Dyke and Dolan (1956), which I could not open, and not an SEM-gun tip (radius about 100 nm, kilovolts). It is a modern
  measured tungsten I–V set that tests the same exponent.
- **Licence warning (decide before publishing)**: the paper is open access under **CC BY-NC-ND 4.0**, and I could not see a separate licence on the Source Data file.
  NC-ND does not allow adapted material. Numbers are facts and a plotted overlay with a citation is normal scientific use, but the coordinator should not
  copy the sheet itself onto the site without checking, and may prefer to keep the CSV in the repository only (not served).
- **Other open tungsten-tip papers found, with I–V only as figures** (not digitised: needs the page image, which this session could not fetch): M. A. Madanat,
  M. S. Mousa, A. N. Al-Rabadi, A. Fischer, *Jordan J. Phys.* **8**(2), 79–85 (2015), Table 1 gives apex radii (SEM 93 to 220 nm; extracted from the FN slope 108 to 288 nm; the
  paper's relation r_FEM = 1.35 r_SEM − 20 nm) — a ready model-versus-data check of the radius extraction; E. C. Reeves, Hamline University honors thesis (2014),
  <https://digitalcommons.hamline.edu/dhp/15>, Figure 22 (I–V of 11 etched tips, radii about 20 to 100 nm).
