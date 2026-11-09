# data/ch01: Thomson 1897 and CODATA e/m

## thomson1897_em.csv
- **Source**: J. J. Thomson, "Cathode Rays", *Philosophical Magazine*, series 5, vol. 44, no. 269 (October 1897), pp. 293–316,
  doi 10.1080/14786449708621070. Table I (method 1, heating of a collecting cylinder, p. 306) and Table II (method 2, electric
  and magnetic deflection, p. 309).
- **How digitised**: by hand from the OCR text of the paper at <https://www.damtp.cam.ac.uk/user/tong/pp/jj1.pdf> (fetched with
  Exa `web_fetch_exa` on 9 November 2026). I did not see the page images. The OCR lost leading dots and some digits, and
  whole columns (W/Q, I, and the field columns). So only **m/e** (both tables) and **v** (Table II) are given, and only for rows where
  the digits were legible. `ocr_flag` marks the others: `leading-dot-lost` (the value is Thomson's ".35" or ".4" with the dot
  dropped by OCR; the value must lie between 0 and 1 in these units), `digit-uncertain` (Tube 3, first air row, ".9" may be another
  digit), `m/e-lost-in-OCR` (first row of Table II, value missing).
- **Check against the paper**: Thomson states the means on p. 307: tube 1 air .40, hydrogen .42, carbonic acid .4; tube 2 air
  .52, hydrogen .50, carbonic acid .54 (all ×10⁻⁷). My transcribed rows give tube 1 .42, .425, .397 and tube 2 .529, .507, .54. They
  agree to 5 %, which is within the spread of the rows. A reader with the page images should check each row.
- **Units**: Thomson's m/e is in electromagnetic units of the cgs system, grams per EMU of charge. 1 EMU of charge = 10 C and 1 g =
  10⁻³ kg, so m/e [kg/C] = (value ×10⁻⁷) × 10⁻³ / 10 = value × 10⁻¹¹. Example: 0.57×10⁻⁷ g/EMU =
  5.7×10⁻¹² kg/C, e/m = 1.75×10¹¹ C/kg. Check of the unit reading: Thomson compares with 10⁻⁴ for the hydrogen ion in
  electrolysis; Faraday's constant over the hydrogen molar mass gives e/m = 9.65×10⁷ C/kg, which is 1.04×10⁻⁴ g/EMU. So the
  units are right. v is in cm/s in the paper (×10⁹), converted to m/s.
- **Uncertainty**: Thomson gives none. The row-to-row spread is about ±25 % in tube 1 and about ±15 % in tube 2; he says tube 3 (small
  holes) and the second method give larger values (1.1 to 1.5 ×10⁻⁷) and that tubes 1 and 2 probably read too low because of
  conduction in the gas (p. 307). The mean of tubes 1 and 2 is 0.467×10⁻⁷ g/EMU, e/m = 2.1×10¹¹ C/kg, 22 % above CODATA.
  The mean of Table II is 1.28×10⁻⁷, e/m = 0.78×10¹¹ C/kg, 56 % below.

## codata_em.csv
- **CODATA 2018**: e = 1.602 176 634 × 10⁻¹⁹ C (exact) and m_e = 9.109 383 7015(28) × 10⁻³¹ kg, from the NIST wallet card
  *2018 CODATA Recommended Values* (NIST SP 959, June 2019), <https://physics.nist.gov/cuu/pdf/wallet_2018.pdf>. The e/m in the
  file is **computed here** as e/m_e = 1.758 820 011 × 10¹¹ C/kg; I did not read the table entry for e/m itself. Relative
  uncertainty 3.1 × 10⁻¹⁰ (e is exact).
- **CODATA 2022** (read directly): −1.758 820 008 38(55) × 10¹¹ C/kg, the value the live NIST page
  <https://physics.nist.gov/cgi-bin/cuu/Value?esme> now serves; the sign is for the electron. The 2022 value differs from the
  2018 one by 1.4 × 10⁻⁹ in relative terms.
