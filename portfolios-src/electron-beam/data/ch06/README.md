# data/ch06: electron yields and ranges

## bse_coefficient_vs_energy.csv  (data item e, backscattering)
- **Source**: the open database of electron backscattering coefficients, F. Akbari et al., *Medical Physics* (2023),
  doi 10.1002/mp.16604 (author list not verified: the Zenodo record names F. Akbari; a search listing gave a different first author),
  data at doi 10.5281/zenodo.7810951 (published 24 November 2022, **CC BY 4.0**). Files used: `Energy dependence (csv).rar` →
  `Si.csv`, `Cu.csv`, `Au.csv`, `Al.csv`, `Resist.csv` (the last is "Resist (e-beam PMMA)", one data set).
- **How digitised**: not by me. The database authors collected the points from the original papers; I merged five ASCII files and added
  columns. In the files the reference number is given only on the first row of each block of points. I carried it forward to the rows
  below it until the next number (my reading of the layout; `reference_no_in_source_Table_1A` is the database's own numbering).
  I did not open the paper's Table 1A, so I cannot name the original authors of each point.
- **Units**: E in keV as in the source plus `E_J` (E × 10³ × e, J); η in per cent as in the source plus a fraction.
- **Uncertainty**: none given per point. The spread between references is the honest uncertainty: Si at 10 keV is 17.4 and 17.4
  (refs 6 and 14), 18.6 (ref 12), 20 (ref 10) per cent, about ±7 %. Sample preparation matters (the Cu and Au files carry "cleaned
  sample" comments on some points).
- **Conditions**: thickness and angle of incidence are not columns in these files; the database keeps them in separate "Thickness" and
  "Orientation" files, which I did not open. Treat the points as bulk targets at normal incidence only after checking those files.
- **Error in the source**: `Au.csv` is headed "Gold, (Z=74)"; gold is Z = 79 (74 is tungsten). I wrote Z = 79. The database's material
  list also shows "Gold (Z = 74)" (search excerpt of the paper).
- The resist file has 10 points, 0.5 to 10 keV, η 6 to 10.5 %, one reference (38); in the paper's table the same reference also
  covers PETEOS, amorphous Si, an Al interconnect line and COAT725 (a wafer coating), per the excerpt.

## se_yield_lin_joy2005.csv  (data item e, secondary electrons)
- **Source**: Y. Lin, D. C. Joy, "A new examination of secondary electron yield data", *Surf. Interface Anal.* **37** (2005) 895–900,
  doi 10.1002/sia.2107, <https://psec.uchicago.edu/Papers/A_new_examination_of_secondary_electron_yield_data.pdf> (read: abstract,
  universal law, Table 1).
- **What the numbers are**: Table 1 is titled "Data for elements from Monte Carlo simulation". These are not raw measurements: the
  paper fits the SE yield compilation of its Ref. 1 with a universal curve and with Monte Carlo, and tabulates δ_max, E_max and δ at 2 and
  20 keV. I copied Al, Si (crystal), Cu and Au.
- **The universal law** (the paper's Eq. 5): δ/δ_max = 1.28 (E/E_max)^(−0.67) [1 − exp(−1.614 (E/E_max)^1.67)].
  The CSV carries δ at 2 and 20 keV from that law, **computed here**, beside the printed Monte Carlo values. They agree for Al and Si
  (ratio 0.96 to 1.05 at 2 keV) and not for Cu (1.25 and 1.69) and Au (1.45 and 2.67): the law is a template, not the same as the
  Monte Carlo output. Say so if the page overlays one of them.
- **Not in this file**: SE yield of a resist (this paper has no resist entry); Joy's compilation itself (<http://www.napchan.com/bse/index.htm>,
  named in the paper) was not reached.
- **Uncertainty**: none printed. The paper discusses a wide spread between authors in the compiled data for the same element.

## Still to do for ch06 (data item d, ranges)
Measured electron ranges (Everhart and Hoff 1971, Kanaya and Okayama 1972) are paywalled and not yet found in an open copy. See
`sources/bibliography.md` section 3.
