# data/ch02: properties of electron sources

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
