# Dossier: generator at the pendulum pivot (small DC motor + planetary gearhead)

Scout run 2026-10-23. Requirement: resist peak torque about 0.14 N m at the output shaft, shaft swinging at 0.4 to 0.8 rad/s amplitude.
All numbers below were read from manufacturers' own PDF datasheets, downloaded to
`/tmp/claude-0/-home-user-SiteTest/8b34d6df-5462-5589-b418-3710ebaaeab4/scratchpad/sources/gen/` and converted with pdftotext. Line numbers ("line n") are the row numbers printed in the maxon tables; Faulhaber tables have no line numbers, so the row label is quoted.

## Sources (full reference, URL, local file)

S1. maxon motor ag, "RE 25 ∅25 mm, graphite brushes, 20 watt", maxon DC motor catalogue page 153, April 2022 edition (footer: "April 2022 edition / subject to change ... maxon DC motor 153").
URL: https://www.maxongroup.com/medias/sys_master/root/8992314032158/EN-22-153.pdf (linked from the maxon product page https://www.maxongroup.com/maxon/view/product/339152). Local: EN-22-153.pdf.

S2. maxon motor ag, "Planetary Gearhead GP 32 C ∅32 mm, 1.0-6.0 Nm, Ceramic Version", catalogue pages 430-431, "© 2025 maxon. All rights reserved. March edition."
URL: https://www.maxongroup.com/medias/sys_master/root/9406824710174/GP-32-C.pdf. Local: GP-32-C.pdf.
(Cross-check, Japanese, older: "maxon gear 384", GP 32 A, 0.75-4.5 Nm, 2020-10 edition, https://www.maxongroup.com/medias/sys_master/root/8860215738398/2020-JP-384-385.pdf. Same ratios. I did not use its numbers; GP 32 A has lower torque and the same efficiencies.)

S3. Dr. Fritz Faulhaber GmbH & Co. KG, "DC-Micromotors, Precious Metal Commutation, Series 2232 ... SR", datasheet, "Edition 2026 Jul. 28".
URL: https://www.faulhaber.com/fileadmin/Import/Media/EN_2232_SR_DFF.pdf. Local: EN_2232_SR_DFF.pdf.
(Also fetched, only for comparison: Series 2224 ... SR, https://www.faulhaber.com/fileadmin/Import/Media/EN_2224_SR_DFF.pdf, same edition.)

S4. Dr. Fritz Faulhaber GmbH & Co. KG, "Planetary Gearheads, Series 22E" (22E, 22EC, 22EK), "Edition 2026 Jul. 28".
URL: https://www.faulhaber.com/fileadmin/Import/Media/EN_22E_DFF.pdf. Local: f_EN_22E_DFF.pdf, text 22E.txt.

Not obtained: the Faulhaber 22/7 (metal) gearhead datasheet. The file names I guessed (EN_22_7_FDF, EN_22_7_DFF, EN_22GPT_DFF and variants) all returned 404; web search only found reseller pages (im-tek.com), which I did not use. The 2232 SR sheet lists 22/7 as a compatible gearhead (S3, "Product combination").

## Candidate A: maxon RE 25 (graphite brushes, 20 W) + maxon GP 32 C

### Motor, S1 (page "maxon DC motor 153"), part 339152 (24 V winding) and 339150 (12 V winding)

| Quantity | 339152 (24 V) | 339150 (12 V) | S1 line |
|---|---|---|---|
| Nominal voltage | 24 V | 12 V | 1 |
| Terminal resistance R | 1.53 ohm | 0.517 ohm | 10 |
| Terminal inductance | 0.186 mH | 0.057 mH | 11 |
| Torque constant k_t | 20.8 mNm/A = 0.0208 N m/A | 11.5 mNm/A = 0.0115 N m/A | 12 |
| Speed constant | 460 rpm/V | 828 rpm/V | 13 |
| Back-EMF constant k_e = 60/(2 pi x speed const.) | 60/(2 pi x 460) = 0.02076 V s/rad | 60/(2 pi x 828) = 0.01153 V s/rad | derived |
| Rotor inertia J | 14.7 g cm^2 = 14.7e-7 kg m^2 = 1.47e-6 kg m^2 | 14.5 g cm^2 = 1.45e-6 kg m^2 | 16 |
| No-load current | 40.2 mA | 68.1 mA | 3 |
| No-load speed | 10 900 rpm | 9620 rpm | 2 |
| Max. efficiency | 88 % | 84 % | 9 |
| Stall torque / current | 325 mNm / 15.6 A | 268 mNm / 23.2 A | 7, 8 |
| Nominal torque / current | 30.4 mNm / 1.5 A | 27.5 mNm / 2.45 A | 5, 6 |
| Mechanical time constant | 5.24 ms | 5.62 ms | 15 |
| Mass | 115 g | 115 g | 31 |
| Max. speed | 14 000 rpm | | 23 |

Check: k_t and k_e agree (20.8 mNm/A vs 0.02076 V s/rad; 11.5 vs 11.53) as they must in SI units.
The sheet gives no separate friction torque. A friction estimate from the no-load current is k_t x I0 = 0.0208 x 0.0402 = 0.84 mN m (24 V) and 0.0115 x 0.0681 = 0.78 mN m (12 V). This is at no-load speed (about 10 000 rpm) and includes iron and viscous losses; at the slow speeds of the pendulum the true friction is probably lower, which the sheet does not say.
Winding-to-housing 5.1 K/W, housing-ambient 14.4 K/W (lines 17, 18). Magnets/brush type: graphite brushes; 11 commutator segments, 1 pole pair (lines 29, 30).

### Gearhead GP 32 C, S2 (page 430), one row per column of the table

Common data: planetary, straight teeth, stainless output shaft, ball bearing, radial play max 0.14 mm at 5 mm from flange, axial play max 0.4 mm, max. continuous input speed 8000 rpm, temperature -40 to +100 C, "Direction of rotation, drive to output: =".
Stage data as printed (row numbers 1-11 of the sheet): reduction, stages, max. continuous torque, max. intermittent torque, max. efficiency, weight, average backlash at no load, mass inertia, length L1.

| Reduction (nearby the 100-500 range) | Stages | Cont. torque | Interm. torque | Max. efficiency | Weight | Backlash | Inertia (see note) | Length |
|---|---|---|---|---|---|---|---|---|
| 111 : 1 (also 123, 132, 159 and 190 : 1 are 3 or 4 stages, see next rows) | 3 | 6 Nm | 7.5 Nm | 70 % | 194 g | 1.0 deg | 0.7 g cm^2 | 43.1 mm |
| 246 : 1 (also 295, 318, 411, 456 : 1) | 4 | 6 Nm | 7.5 Nm | 60 % | 226 g | 1.0 deg | 0.7 g cm^2 | 49.8 mm |
| 492 : 1 (also 531, 589, 636, 706 : 1) | 4 | 6 Nm | 7.5 Nm | 60 % | 226 g | 1.0 deg | 0.7 g cm^2 | 49.8 mm |
| 33 : 1, 14 : 1 | 2 | 3 Nm | 3.75 Nm | 75 % | 162 g | 0.8 deg | 0.8 g cm^2 | 36.4 mm |
| 3.7 : 1 | 1 | 1 Nm | 1.25 Nm | 80 % | 118 g | 0.7 deg | 1.5 g cm^2 | 26.5 mm |

Part numbers: 166930 (3.7:1), 166933 (14:1), 166938 (33:1), 166939 (51:1), 166944 (111:1), 166949 (246:1), 166954 (492:1), 166959 (762:1); the other ratios have their own numbers in the "Part numbers" rows (S2 page 430).
Stage grouping, read from column alignment of the printed table (check against the PDF): 2 stages 14 to 28 and 33 to 103 : 1 (columns "14" and "33"); 3 stages 51, 66, 79, 86, 103 and 111, 123, 132, 159, 190 : 1; 4 stages 246, 295, 318, 411, 456 and 492, 531, 589, 636, 706 : 1 (also 762 to 913 ...). Efficiency and torque follow the stage count: 3 stages 70 %, 4 stages 60 %.
Mass inertia is given in the sheet "Mass inertia ... g cm^2" and is, by maxon's convention, referred to the input (motor) shaft; the sheet does not say so in the lines I read, so confirm before using it: 0.7 g cm^2 = 0.7e-7 kg m^2.
Modular-system table (S2 page 431 area): RE 25 (and RE 25 20 W) is listed as combinable with GP 32 C; overall length RE 25, 20 W + 4-stage gearhead 92.9 mm.

### Datasheet warning about efficiency
Neither S1 nor S2 contains a warning about low load or backdriving. S2 gives only "Max. efficiency" per column and the note "Direction of rotation, drive to output: =". The sheet says nothing about efficiency when the gearhead is driven from the output side. The 50 to 80 % values are for forward drive at the right load, so they are an upper bound only.

### First-pass numbers (my arithmetic, to be checked by the model)
Take RE 25 24 V + GP 32 C 246 : 1 (4 stages, 60 %). Output swing 0.4 to 0.8 rad/s gives motor speed 98 to 197 rad/s (940 to 1880 rpm), back-EMF k_e x omega_motor = 0.02076 x 98 = 2.0 V to 0.02076 x 197 = 4.1 V.
Motor torque for 0.14 N m output: 0.14/246 = 0.57 mN m ideal; /0.6 = 0.95 mN m with the max. efficiency (as a generator the factor may apply the other way: 0.57 x 0.6 = 0.34 mN m, depending on how the efficiency is defined for backdriving, not established). Current I = T/k_t = 0.95e-3/0.0208 = 0.046 A. So the electrical power is only about 0.1 to 0.2 W, and the coil resistance (1.53 ohm) dissipates R I^2 = 3 mW.
Important point: the motor's own no-load friction (0.84 mN m, see above) is of the same size as the torque the generator must supply. So the generator is not "stiff" at 0.14 N m output unless a ratio of about 100 (111:1, 70 %: 0.14/(111 x 0.7) = 1.8 mN m) is used. Whether the ratio 111 or 246 is better depends on the model's need for a damping coefficient c = k_t k_e N^2 / (R_total) (not computed here).
Pure electrical damping at the output for 246:1 and 1.53 ohm (short circuit, no load resistor): c = k_t k_e N^2 / R = 0.0208 x 0.02076 x 246^2 / 1.53 = 17.1 N m s/rad. The peak torque at 0.8 rad/s would then be 13.7 N m, far above 0.14 N m, so a load resistor (or a higher R) is needed: for 0.14 N m at 0.8 rad/s, c = 0.175 N m s/rad, total resistance about 1.53 x 17.1/0.175 = 150 ohm. (Gear efficiency, motor friction and inertia ignored.)

## Candidate B: Faulhaber 2232 ... SR (precious metal commutation) + Faulhaber 22E

### Motor, S3 (table "Series 2232 ... SR", values at 22 C and nominal voltage)

| Quantity | 2232 U 012 SR | 2232 U 024 SR |
|---|---|---|
| Nominal voltage | 12 V | 24 V |
| Terminal resistance R | 4.09 ohm | 16.4 ohm |
| Rotor inductance | 178 uH | 710 uH |
| Torque constant k_M | 16 mNm/A = 0.016 N m/A | 32 mNm/A = 0.032 N m/A |
| Speed constant k_n | 597 min^-1/V | 299 min^-1/V |
| Back-EMF constant k_e | 60/(2 pi x 597) = 0.01600 V s/rad | 60/(2 pi x 299) = 0.03194 V s/rad |
| Rotor inertia J | 3.8 g cm^2 = 3.8e-7 kg m^2 | 3.8 g cm^2 = 3.8e-7 kg m^2 |
| No-load current I0 (typ.) | 17.6 mA | 8.8 mA |
| Friction torque M_R | 0.28 mNm | 0.28 mNm |
| Max. efficiency | 85 % | 85 % |
| Stall torque | 46.7 mNm | 46.5 mNm |
| Rated torque / current / speed | 10 mNm / 0.694 A / 5430 min^-1 | 10 mNm / 0.347 A / 5420 min^-1 |
| Slope of n-M curve | 153 min^-1/mNm | 153 min^-1/mNm |

Common: mass 62 g; shaft diameter 2 mm; ball-bearing version has preloaded bearings (option 277); radial shaft play 0.015 mm (ball bearings) or 0.03 mm (sintered); max speed 8000 min^-1; 1 pole pair; Rth1 6.9 K/W; Rth2 19 K/W (plastic flange) or 1.8 K/W (metal flange).
Check: friction from I0 = 0.016 x 0.0176 = 0.28 mN m, which equals the printed M_R of 0.28 mNm. So the I0 is dominated by friction here (consistent). That is a clean value for the model: friction 0.28 mN m, independent of voltage version.
The 2224 SR sheet (smaller, 2224 012 SR: R 8.77 ohm, k_M 14.6 mNm/A, k_n 655 min^-1/V, J 2.7 g cm^2, M_R 0.2 mNm, I0 13.8 mA) is the lighter option; its 22E rated torque is the same.

### Gearhead 22E, S4 (all data as printed)

Housing and geartrain plastic; recommended max. input speed 5000 min^-1 continuous; backlash at no-load <= 3 deg; output bearings: sintered (22E), ceramic (22EC), ball (22EK); radial shaft load <= 3 / 15 / 50 N; operating range -30 to +65 C (22E), -20 to +85 (22EC), -30 to +85 (22EK); "Direction of rotation, drive to output: =". Gearheads are "available only with motors mounted". Listed motor: 2232A/B...SR (L1 = 59.3 mm for 2 stages).

| Stages | 2 | 3 | 3 | 4 | 4 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|---|
| Continuous torque (mNm) | 200 | 300 | 400 | 400 | 500 | 600 | 600 | 600 |
| Intermittent torque (mNm) | 400 | 600 | 800 | 800 | 1000 | 1000 | 1000 | 1000 |
| Mass without motor (g) | 17 | 19 | 19 | 20 | 20 | 20 | 22 | 24 |
| Max. efficiency (%) | 78 | 69 | 67 | 62 | 61 | 60 | 55 | 49 |

Reduction ratios (rounded), as printed: code B 19, 69, 249, 896, 3225; code A 28, 102, 152, 369, 546, 809, 1327, 1966, 2913, 4315, 4778, 7078, 10486, 15534, 23014. The text extraction puts these ratios in columns without clear alignment to the stage columns, so the exact link between stage count and ratio must be read from the PDF page. The stage/efficiency row above is as printed. In the 100 to 500 range the sheet offers 102, 152, 249, 369 (and 546 slightly above).
Torque requirement: 0.14 N m output is below the lowest continuous rating (200 mNm), so any 22E version holds it, with a margin of 1.4 at 2 stages; for 3 or more stages the margin is >= 2.1. This is a plastic gear train, so the model should treat it as noisy with up to 3 deg backlash (relevant to a swing amplitude of 0.4 to 0.8 rad/s over a small angle).

First-pass numbers: 2232 012 SR + 22E 249 : 1 (4 stages, about 62 %): motor speed at 0.8 rad/s output = 199 rad/s (1900 rpm), back-EMF 0.016 x 199 = 3.2 V; motor torque for 0.14 N m out = 0.14/249 = 0.56 mN m ideal, 0.9 mN m at 62 %; friction 0.28 mN m is 30 to 50 % of this. Current = 0.9e-3/0.016 = 0.056 A.
Short-circuit damping c = k_t k_e N^2 / R = 0.016 x 0.016 x 249^2 / 4.09 = 3.88 N m s/rad.

### Datasheet warning
No warning about low-load efficiency or backdriving in S3 or S4. S4 says only "Direction of rotation, drive to output: =" and "Efficiency, max."

## What the sources do not establish
- Efficiency in reverse (output driving the motor) and at small loads: no figure in any sheet. The "max. efficiency" is the best value, probably at rated load and speed, forward drive.
- Gearhead breakaway / no-load torque (starting torque) is not given by maxon GP 32 C or Faulhaber 22E. For a 4-stage planetary gearhead this friction referred to the output could be a large share of 0.14 N m. This is the main open number.
- The gearhead mass inertia reference shaft (input or output) is not stated in the lines I read for S2; S4 gives no inertia at all.
- S1 gives no friction torque; only no-load current.
- Brush friction and cogging at 1000 to 2000 rpm are not described. For slow back-driving, graphite brushes (RE 25) may show more stick-slip than precious metal (Faulhaber 2232); this is a general expectation, not from a sheet.
- No brushless motor was read, for lack of calls. A coreless BLDC would have no brush friction but cogging; not covered.
- Which exact Faulhaber part is combinable: the 22E sheet lists "2232A/B...SR", the motor sheet lists "2232 U ... SR"; I did not find the definition of A/B versus U in the files read.

## Final table of numbers

| Item | RE 25 339152 + GP 32 C | RE 25 339150 + GP 32 C | Faulhaber 2232 012 SR + 22E |
|---|---|---|---|
| k_t (N m/A) | 0.0208 | 0.0115 | 0.0160 |
| Speed const. (rpm/V) | 460 | 828 | 597 |
| k_e (V s/rad) = 60/(2 pi n) | 0.02076 | 0.01153 | 0.01600 |
| R (ohm) | 1.53 | 0.517 | 4.09 |
| J (g cm^2 / kg m^2) | 14.7 / 1.47e-6 | 14.5 / 1.45e-6 | 3.8 / 3.8e-7 |
| No-load current | 40.2 mA | 68.1 mA | 17.6 mA |
| Friction torque | not given; k_t I0 = 0.84 mN m | not given; k_t I0 = 0.78 mN m | 0.28 mN m (printed) |
| Max. motor efficiency | 88 % | 84 % | 85 % |
| Gear ratios in 100-500 range | 111, 123, 132, 159, 190, 246, 295, 318, 411, 456 | same | 102, 152, 249, 369 (22E, per sheet) |
| Gear max. efficiency (3 or 4 stages) | 70 % (3 st), 60 % (4 st) | same | 69 to 62 % (3 to 4 st) |
| Gear max. continuous / intermittent torque | 6 / 7.5 Nm (3 or 4 st) | same | 0.3-0.6 / 0.6-1.0 Nm (3 to 4 st) |
| Stages | 3 or 4 | 3 or 4 | 2 to 4 |
| Backlash (no load) | 1.0 deg avg | 1.0 deg avg | <= 3 deg |
| Gearhead mass | 194 g (3 st), 226 g (4 st) | same | 19-20 g |
| Motor mass | 115 g | 115 g | 62 g |
| Gearhead inertia | 0.7 g cm^2 | 0.7 g cm^2 | not given |
| Back-EMF at 0.8 rad/s, ratio 246 (or 249) | 4.1 V | 2.3 V | 3.2 V |
| Short-circuit damping c = k_t k_e N^2/R | 17.1 N m s/rad | 21.6 N m s/rad (0.0115x0.01153x246^2/0.517) | 3.88 N m s/rad |

## Open questions
1. Gearhead breakaway/no-load torque at the output of GP 32 C and 22E: must be measured or asked of maxon / Faulhaber; it decides whether a 0.14 N m peak torque is clean.
2. How should the model treat efficiency when backdriven? A simple choice for the lecture note: take eta from the sheet as a bound, show the result for eta = 1 and eta = sheet value.
3. Is a 4-stage 246:1 (60 %) or a 3-stage 111:1 (70 %) better? The first needs less motor torque but suffers more friction; with the RE 25, 111:1 needs 1.8 mN m motor torque, 2 times its friction.
4. A load resistor of order 100 to 200 ohm in the RE 25 case (see arithmetic above) is a design choice, not a datasheet value.
5. The Faulhaber 22/7 (metal, 0.7 Nm cont., per reseller pages only) datasheet is still to be found if a metal gearhead is wanted; the sheet URL pattern was not discovered.
6. A brushless candidate (maxon EC-i 30 or Faulhaber BX4 with 22/7) was not read.
