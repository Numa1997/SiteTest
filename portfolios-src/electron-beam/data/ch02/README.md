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
