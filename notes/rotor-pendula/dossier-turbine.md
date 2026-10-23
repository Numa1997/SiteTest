# Dossier: the NREL 5-MW reference turbine and the IEC 61400-1 turbulence model

Scout report for the Rotor Pendula study, 23 October 2026.

Rules kept in this file. A number appears only if the scout read it in the named source, with the place it was read. A number the scout had to compute is marked **derived by the scout**, with the arithmetic (Section 6). Quotes are at most one per source and under 15 words. Printed page numbers are the numbers printed on the page, not PDF indices. "text-line N" means line N of the `pdftotext -layout` output kept next to the downloads (`nrel5mw.txt`, `turbsim150.txt`) in `/tmp/claude-0/-home-user-SiteTest/8b34d6df-5462-5589-b418-3710ebaaeab4/scratchpad/sources/s1/`.

## 0. Sources, and what could and could not be opened

| id | document | what the scout did |
|---|---|---|
| S1 | J. Jonkman, S. Butterfield, W. Musial, G. Scott, *Definition of a 5-MW Reference Wind Turbine for Offshore System Development*, NREL/TP-500-38060, February 2009. Fetched from https://www.osti.gov/servlets/purl/947422 (952 922 bytes, PDF, text layer extracted). | Read the body (Sections 1 to 9 and Tables 1-1 to 9-1) and the Appendix A FAST input and the DISCON listing by search. Appendix B airfoil tables not read. |
| S2 | OpenFAST r-test, folder `glue-codes/openfast/`, branch `main`, raw files from https://raw.githubusercontent.com/OpenFAST/r-test/main/glue-codes/openfast/ (commit hash not recorded; fetched 23 Oct 2026). Files: `5MW_Baseline/NRELOffshrBsline5MW_Blade.dat`; `5MW_Land_DLL_WTurb/NRELOffshrBsline5MW_Onshore_ElastoDyn.dat`; `5MW_Land_DLL_WTurb/NRELOffshrBsline5MW_Onshore_ServoDyn.dat`; `5MW_Baseline/ServoData/DISCON/DISCON.F90`; `5MW_Baseline/NRELOffshrBsline5MW_AeroDyn_blade.dat`; `5MW_Baseline/Airfoils/*_A17.dat` and `*_A17_coords.txt`. | Blade, ElastoDyn, ServoDyn read in full (ElastoDyn by key lines). DISCON.F90: parameter block and torque logic read. Airfoil files: headers and coordinates only. |
| S3 | B. J. Jonkman, *TurbSim User's Guide: Version 1.50*, NREL/TP-500-46198, September 2009 (revised 26 Aug 2009). OSTI 965520, DOI 10.2172/965520. Fetched from https://www.osti.gov/servlets/purl/965520 (6.1 MB). | Read the input-parameter text for the IEC models and the sections IECKAI, IECVKM and Spatial Coherence Models. Rest not read. |
| S3b | OSTI record 891594, https://www.osti.gov/servlets/purl/891594, a TurbSim user's guide of 2006 (the scout did not read the cover, so the report number NREL/TP-500-39797 is not confirmed here). | Only the passages near "IECturbc" and the IEC coherence equation were read. |
| S4 | arXiv:1904.07021, "Fatigue design load calculations of the offshore NREL 5MW benchmark turbine using quadrature rule techniques" (authors not recorded by the scout). A paper that restates IEC 61400-1; not the standard. | Read only the paragraph around its Eq. (2.1) (text-lines 118-136). |
| S5 | (a) E. Soto Sagredo et al., 2024, J. Phys.: Conf. Ser. 2767, 052061 (DTU Orbit copy); (b) Wind Energy Science 9, 799-820 (2024), OSTI 2572611. | Search by pattern only; short raw excerpts are printed unreviewed in Section 6b. |

Not opened, and why:
- IEC 61400-1 itself (paywalled). Every IEC statement below is therefore second-hand, through S3, S3b, S4.
- www.nrel.gov (the proxy refuses it), forums.nrel.gov (name resolution failed from this machine), the GitHub API (refused: repository not enabled for the session).
- `DISCON.IN` of the 5-MW controller: raw paths tried and returned 404: `5MW_Baseline/ServoData/DISCON.IN`, `.../DISCON/DISCON.IN`, `.../DISCON/DISCON.in`, `.../DISCON_OC3/DISCON.IN`, `.../DISCON_ITI/DISCON.IN`, `5MW_Land_DLL_WTurb/DISCON.IN`, `5MW_Baseline/DISCON.IN`. The GitHub tree page lists `ServoData/` with three folders (DISCON, DISCON_ITI, DISCON_OC3) and the DISCON folder with `CMakeLists.txt` and `DISCON.F90` (listing may be truncated). The 5-MW controller constants are compiled into `DISCON.F90`.
- `NRELOffshrBsline5MW_AeroDyn15.dat` and `..._AeroDyn15_blade.dat` (404 at the tried paths); the older `NRELOffshrBsline5MW_AeroDyn_blade.dat` exists and was read.
- Bir and Jonkman (Ref. [2] of S1) with isolated-blade and rotating frequencies; any Cp(lambda) table (ROSCO `Cp_Ct_Cq` files were not opened).

## 1. S1: NREL/TP-500-38060 (Jonkman et al. 2009)

**What it establishes.** A land-based and offshore baseline turbine, 3 blades, upwind, variable speed, collective pitch, with the full set of blade, hub, nacelle, drivetrain, tower and controller properties. It builds the blade from the DOWEC 6-MW study, scaled to the REpower 5M prototype. Its baseline controller is described in Section 7. It states one peak of the power coefficient and no Cp surface. Quote (12 words): "the peak power coefficient of 0.482 occurred at a tip-speed ratio of 7.55".

### 1.1 Gross properties (Table 1-1, p. 2, text-lines 388-402; Section 1 text p. 3, text-lines 427-430)
- Rating 5 MW. Rotor diameter 126 m, hub diameter 3 m. Hub height 90 m.
- Cut-in, rated, cut-out wind speed 3, 11.4, 25 m/s. Cut-in, rated rotor speed 6.9 rpm, 12.1 rpm. Rated tip speed 80 m/s.
- Overhang 5 m, shaft tilt 5 deg, precone 2.5 deg. Rotor mass 110 000 kg, nacelle mass 240 000 kg, tower mass 347 460 kg. Overall CM at (-0.2, 0.0, 64.0) m in tower-base coordinates.
- The 126 m ignores precone. The report gives the exact undeflected diameter (126 m) x cos(2.5 deg) = 125.88 m and swept area 12 445.3 m^2 (p. 3).
- Validity: undeflected rotor; the land-based version is the one whose tower is tabulated (Section 6).

### 1.2 Blade structure (Section 2, pp. 4-6; Table 2-1 p. 5, text-lines 505-559; Table 2-2 p. 6, text-lines 596-604)
- Blade length 61.5 m along the preconed axis, measured from the blade root; the root sits 1.5 m from the rotor centre along the pitch axis (p. 5, text-lines 491-494). BlFract = fractional distance from root (0) to tip (1) along the pitch axis.
- Table 2-2: overall (integrated) mass **17 740 kg**; mass scaling factor 4.536 %; second mass moment of inertia about the root **11 776 047 kg m^2**; first mass moment about the root **363 231 kg m**; CM at **20.475 m** from the root along the preconed axis; structural damping ratio, all modes, **0.477465 % of critical** (the report says this equals the 3 % logarithmic decrement of the DOWEC study, text-lines 590-592).
- Table 2-1 lists, per station: Radius (m), BlFract, AeroCent, StrcTwst (deg), BMassDen (kg/m), FlpStff, EdgStff, GJStff (N m^2), EAStff (N), Alpha, FlpIner, EdgIner (kg m), PrecrvRef, PreswpRef, FlpcgOf, EdgcgOf, FlpEAOf, EdgEAOf (m). The report states that the BMassDen values are the DOWEC values and that they were increased by 4.536 % in the model to reach 17 740 kg (text-lines 582-585). The scout spot-checked that rows 1, 3 and 49 of Table 2-1 equal the r-test blade file (BMassDen 678.935, 773.363, 10.319; EdgStff 18113.60E+6, 19558.60E+6, 5.01E+6). Consequence for the modal mass: the tabulated BMassDen must be multiplied by AdjBlMs (S2, Section 2) to reproduce 17 740 kg; Section 6 checks this.
- Edgewise stiffness and inertia are about the principal axes at the structural twist angle (text-lines 564-566). Edgewise CM offset EdgcgOf is tabulated (0.0 to 0.3 m); flapwise CM offset and elastic offsets were set to zero.
- The mode-shape polynomial (BldEdgSh) is not in the body of S1 Section 2; it is in the Appendix A FAST blade file: BldEdgSh(2..6) = 0.3627, 2.5337, -3.5772, 2.3760, -0.6952 (text-lines 2377-2381). These agree with S2 digit for digit.

### 1.3 Blade aerodynamic properties (Section 3, Table 3-1, p. 7, text-lines 650-669)
17 nodes. Columns: node, RNodes (m from rotor centre), AeroTwst (deg), DRNodes (m), Chord (m), airfoil table.

| node | RNodes m | BlFract = (RNodes-1.5)/61.5 (derived) | AeroTwst deg | Chord m | airfoil table |
|---|---|---|---|---|---|
| 1 | 2.8667 | 0.022 | 13.308 | 3.542 | Cylinder1 |
| 2 | 5.6000 | 0.067 | 13.308 | 3.854 | Cylinder1 |
| 3 | 8.3333 | 0.111 | 13.308 | 4.167 | Cylinder2 |
| 4 | 11.7500 | 0.167 | 13.308 | 4.557 | DU40_A17 |
| 5 | 15.8500 | 0.233 | 11.480 | 4.652 | DU35_A17 |
| **6** | **19.9500** | **0.300** | **10.162** | **4.458** | **DU35_A17** |
| 7 | 24.0500 | 0.367 | 9.011 | 4.249 | DU30_A17 |
| 8 | 28.1500 | 0.433 | 7.795 | 4.007 | DU25_A17 |
| 9 | 32.2500 | 0.500 | 6.544 | 3.748 | DU25_A17 |
| **10** | **36.3500** | **0.567** | **5.361** | **3.502** | **DU21_A17** |
| **11** | **40.4500** | **0.633** | **4.188** | **3.256** | **DU21_A17** |
| 12 | 44.5500 | 0.700 | 3.125 | 3.010 | NACA64_A17 |
| 13 | 48.6500 | 0.767 | 2.319 | 2.764 | NACA64_A17 |
| 14 | 52.7500 | 0.833 | 1.526 | 2.518 | NACA64_A17 |
| **15** | **56.1667** | **0.889** | **0.863** | **2.313** | **NACA64_A17** |
| **16** | **58.9000** | **0.933** | **0.370** | **2.086** | **NACA64_A17** |
| 17 | 61.6333 | 0.985 | 0.106 | 1.419 | NACA64_A17 |

- At 30 % of span (r = 19.95 m from the centre): node 6, chord 4.458 m, twist 10.162 deg, DU35 (read).
- At 60 % (r = 1.5 + 0.6 x 61.5 = 38.4 m): the exact midpoint of nodes 10 and 11; chord (3.502 + 3.256)/2 = **3.379 m**, twist **4.77 deg** (4.7745), both DU21 (derived by the scout, linear interpolation).
- At 90 % (r = 56.85 m): one quarter of the way from node 15 to node 16; chord 2.313 + 0.25 x (2.086 - 2.313) = **2.256 m**, twist 0.863 + 0.25 x (0.370 - 0.863) = 0.740 deg, NACA64 (derived by the scout).
- Thickness ratio: S1 gives the airfoil by name only. DU = Delft University airfoil, NACA = National Advisory Committee for Aeronautics, file name NACA64 (p. 8). The percentage thickness is not stated in S1 or in the airfoil input headers read. **Derived by the scout** from the r-test coordinate files by taking the largest upper-minus-lower distance on a 1 % chord grid (one reference row x/c = 0.25, y/c = 0 in each file may disturb the last digit): DU40 0.405, DU35 0.351, DU30 0.300, DU25 0.250, DU21 0.210, NACA64 0.180 of chord. The names agree with these (DU35 = 35 %, DU21 = 21 %).
- Rotor solidity roughly 5.16 % (p. 7). Aerodynamic twist is offset by -0.09182 deg from the DOWEC values so that twist is zero at the tip (p. 7).
- Validity: AeroDyn 17-element discretisation; the airfoil tables are 3-D corrected (Selig and Eggers stall delay, Viterna, aspect ratio 17) (p. 8).

### 1.4 Hub and nacelle (Section 4, text p. 12; Table 4-1 p. 13, text-lines 867-880)
- Hub mass 56 780 kg, CM at the hub centre. **Hub inertia about the low-speed shaft 115 926 kg m^2**, found for a thin spherical shell of radius 1.75 m (text-lines 841-844).
- Elevation of yaw bearing 87.6 m; vertical distance from yaw bearing to shaft 1.96256 m; distance along the shaft from hub centre to yaw axis 5.01910 m; hub centre to main bearing 1.912 m. Nacelle mass 240 000 kg, nacelle inertia about yaw axis 2 607 890 kg m^2, nacelle CM 1.9 m downwind and 1.75 m above the yaw bearing.

### 1.5 Drivetrain (Section 5 text and Table 5-1, p. 14, text-lines 889-926)
- Rated rotor speed 12.1 rpm, rated generator speed 1173.7 rpm, **gearbox ratio 97:1**, electrical generator efficiency 94.4 %. The gearbox has no friction losses (text-line 893).
- **Generator inertia about the high-speed shaft 534.116 kg m^2.** The report says this equals the low-speed-shaft-equivalent 5 025 500 kg m^2 of the DOWEC study (text-lines 897-899). Check, derived by the scout: 534.116 x 97^2 = 5 025 497.4 kg m^2.
- Equivalent drive-shaft torsional spring 867 637 000 N m/rad, damping 6 215 000 N m/(rad/s) (5 % critical, free-free mode of rigid rotor and rigid generator). HSS brake: fully deployed torque 28 116.2 N m, 0.6 s linear ramp.
- Rotor inertia about the shaft and total drivetrain inertia: **not given as numbers in S1**. The nomenclature (text-lines 124-128) and Eq. (7-5) (p. 20) define I_Rotor, I_Gen and I_Drivetrain (drivetrain inertia cast to the low-speed shaft) with I_Drivetrain = I_Rotor + N_Gear^2 I_Gen implied by the left side of Eq. (7-5); the scout found no number for I_Rotor or I_Drivetrain in the body of S1 (searched for kg m^2 values: only blade, hub, nacelle and generator appear). Derived values are in Section 6 (S.3).

### 1.6 Baseline controller (Section 7.2, p. 19, text-lines 1128-1160; Table 7-2, p. 27, text-lines 1592-1618; Fig. 7-2 p. 20 shows the torque curve)
- Five regions: 1 (torque zero), 1 1/2 (linear start-up ramp), 2 (torque proportional to the square of filtered generator speed), 2 1/2 (linear, induction-machine slope), 3 (constant power, torque inversely proportional to speed). Region 1 1/2 sets a lower limit on the operating speed range; Region 2 1/2 limits tip speed at rated power.
- **Region 2 law: generator torque = k x (filtered generator speed)^2, k = 0.0255764 N m/rpm^2, on the high-speed (generator) shaft, with the speed in rpm and the torque in N m.** Text p. 19: it follows from the peak Cp and the 97:1 ratio. Table 7-2 prints the unit "N m/rpm" (superscript lost in the text layer); the text on p. 19 prints N m/rpm^2.
- Peak power coefficient **0.482** at tip-speed ratio **7.55** and rotor-collective blade pitch **0.0 deg** (Table 7-2; text p. 19). Found by FAST with AeroDyn runs at a number of rotor speeds and blade-pitch angles **at a fixed wind speed of 8 m/s**.
- Rated mechanical power 5.296610 MW; rated generator torque 43 093.55 N m (rated electric power 5 MW divided by 94.4 %).
- Boundaries, on the generator shaft: Region 1 to 1 1/2 at **670 rpm**; Region 1 1/2 to 2 at **871 rpm** (30 % above 670); Region 2 1/2 to 3 at **1 161.963 rpm** (99 % of rated 1173.7 rpm); slip in Region 2 1/2 **10 %**. The report ties 670 rpm to the minimum rotor speed of 6.9 rpm of the REpower 5M (text-lines 1158-1160). The Region 2 to 2 1/2 boundary is not tabulated; it follows from the 2 1/2 line (Section 6, S.5).
- Torque limits: maximum 47 402.91 N m (10 % above rated); rate limit 15 000 N m/s. Region-3 torque is also used whenever the previous pitch command is 1 deg or more. Generator-speed low-pass filter corner 0.25 Hz, stated to be one quarter of the blade's first edgewise natural frequency (Section 7.1, text-line 1075), which implies a value near 1 Hz.
- Validity: baseline controller of the land and offshore versions; quasi-steady behaviour (Fig. 9-1 shows rotor speed rising linearly with wind speed in Region 2).

### 1.7 Natural frequencies (Section 9, Table 9-1, p. 30, text-lines 1696-1715)
Full-system frequencies of the land-based turbine, **stationary, high-speed-shaft brake engaged, blades at 0 deg pitch, aerodynamic damping ignored** (text-lines 1692-1695). In Hz, FAST / ADAMS:

| mode | FAST | ADAMS |
|---|---|---|
| 1 1st tower fore-aft | 0.3240 | 0.3195 |
| 2 1st tower side-to-side | 0.3120 | 0.3164 |
| 3 1st drivetrain torsion | 0.6205 | 0.6094 |
| 4 1st blade asymmetric flapwise yaw | 0.6664 | 0.6296 |
| 5 1st blade asymmetric flapwise pitch | 0.6675 | 0.6686 |
| 6 1st blade collective flap | 0.6993 | 0.7019 |
| **7 1st blade asymmetric edgewise pitch** | **1.0793** | **1.0740** |
| **8 1st blade asymmetric edgewise yaw** | **1.0898** | **1.0877** |
| 9 2nd blade asymmetric flapwise yaw | 1.9337 | 1.6507 |
| 10 2nd blade asymmetric flapwise pitch | 1.9223 | 1.8558 |
| 11 2nd blade collective flap | 2.0205 | 1.9601 |
| 12 2nd tower fore-aft | 2.9003 | 2.8590 |
| 13 2nd tower side-to-side | 2.9361 | 2.9408 |

These are full-system values, not isolated-blade values. S1 has **no table of blade-only frequencies** and no collective-edgewise entry. S1 also has no rotating (12.1 rpm) frequencies; it refers to Bir and Jonkman (its Ref. [2]) for those.

### 1.8 FAST input file in S1 Appendix A (v6.10a-jmj; text-lines 2063-2520)
Agrees with S2 where checked: NumBl 3; RotSpeed 12.1 rpm; TipRad 63.0 m; HubRad 1.5 m; OverHang -5.01910 m; ShftTilt -5.0 deg; PreCone -2.5 deg; GenIner 534.116 kg m^2; HubIner 115.926E3 kg m^2; GBRatio 97.0; Twr2Shft 1.96256 m; HH 90.0 m (text-lines 2127-2166, 2518). The DISCON listing in the appendix has the same controller constants as S2 (text-lines 3611-3653).

### 1.9 What S1 does not establish
A Cp(lambda, pitch) table or curve (only the single peak); the air density used for Cp; numeric rotor inertia and total drivetrain inertia; isolated-blade or rotating-blade natural frequencies; the Region 2 to 2 1/2 speed; the thickness ratio as a number; edgewise modal mass; anything about turbulence.

## 2. S2: OpenFAST r-test (files of the same turbine)

**What it establishes.** The model files used by OpenFAST regression tests. Values agree with S1 wherever both state them. The 5-MW controller (DISCON) has its constants compiled in.

### 2.1 ElastoDyn main file, onshore 5-MW (`5MW_Land_DLL_WTurb/NRELOffshrBsline5MW_Onshore_ElastoDyn.dat`; line numbers from `cat -n`)
| line | name | value | unit / note |
|---|---|---|---|
| 8-10 | FlapDOF1, FlapDOF2, EdgeDOF | True | first and second flap mode, first edge mode |
| 13-14 | DrTrDOF, GenDOF | True | drivetrain flexibility, generator DOF |
| 34 | RotSpeed | 12.1 | rpm, initial or fixed rotor speed |
| 45 | NumBl | 3 | |
| 46 | TipRad | 63 | m, apex to blade tip |
| 47 | HubRad | 1.5 | m, apex to blade root |
| 48-50 | PreCone(1..3) | -2.5 | deg |
| 51 | HubCM | 0 | m |
| 55 | OverHang | -5.0191 | m (negative = upwind rotor) |
| 56 | ShftGagL | 1.912 | m |
| 57 | ShftTilt | -5 | deg |
| 58 | NacCMxn | 1.9 | m |
| 64 | Twr2Shft | 1.96256 | m |
| 65 | TowerHt | 87.6 | m |
| 83 | HubMass | 56780 | kg |
| 84 | HubIner | 115926 | kg m^2, about the rotor axis |
| 86 | GenIner | 534.116 | kg m^2, about the HSS |
| 87 | NacMass | 240000 | kg |
| 99-101 | BldFile(1..3) | "../5MW_Baseline/NRELOffshrBsline5MW_Blade.dat" | |
| 123 | GBoxEff | 100 | % |
| 124 | GBRatio | 97 | |

### 2.2 Blade file (`5MW_Baseline/NRELOffshrBsline5MW_Blade.dat`, 82 lines, verbatim in Section 5)
- NBlInpSt = 49 stations (line 4). BldFlDmp(1), BldFlDmp(2), BldEdDmp(1) = 0.477465 % of critical (lines 5-7). FlStTunr(1,2) = 1; **AdjBlMs = 1.04536** (line 11; the file comment says 1.04536 for AD14 and 1.057344 for AeroDyn); AdjFlSt = AdjEdSt = 1.
- **Edgewise mode 1 shape, BldEdgSh(2..6) = 0.3627, 2.5337, -3.5772, 2.376, -0.6952** (lines 77-81), coefficients of x^2 ... x^6 with x = distance from the root over the flexible length (ElastoDyn convention; flexible length = TipRad - HubRad = 61.5 m). The sum of the coefficients is 1.0000 (shape is 1 at the tip; derived by the scout).
- Distributed table: lines 17-65, 49 rows, columns BlFract, StrcTwst (deg), BMassDen (kg/m), FlpStff (N m^2), EdgStff (N m^2). Copied verbatim in Section 5.
- Flap mode shapes BldFl1Sh and BldFl2Sh are in lines 67-76 (also in Section 5).

### 2.3 ServoDyn and DISCON (controller)
- ServoDyn (`5MW_Land_DLL_WTurb/NRELOffshrBsline5MW_Onshore_ServoDyn.dat`): PCMode = 5 and VSContrl = 5 (Bladed-style DLL). The simple-VS entries VS_RtGnSp, VS_RtTq, VS_Rgn2K, VS_SlPc are **placeholders 9999.9, used only when VSContrl = 1** (lines 37-40). So ServoDyn does not carry the Region-2 numbers. GenEff 94.4 % (line 30). HSSBrTqF 28116.2 N m (line 59). DLL_FileName "../5MW_Baseline/ServoData/DISCON.dll", DLL_InFile "DISCON.IN" (lines 86-87). The pitch actuator spring and damper in this file are 7.0e8 N m/rad and 2.3e5 N m/(rad/s) (lines 12-17), which differ from S1 Table 7-2 (971 350 000 and 206 000).
- DISCON (`5MW_Baseline/ServoData/DISCON/DISCON.F90`), parameter block (lines 58, 70-99), SI units, HSS side, **identical to the constants in S1's appendix listing (text-lines 3611-3653)**:

| name | value | unit | line | comment in source |
|---|---|---|---|---|
| CornerFreq | 1.570796 | rad/s | 58 | low-pass corner; the comment says one quarter of the blade edgewise frequency of about 1 Hz |
| VS_CtInSp | 70.16224 | rad/s | 88 | regions 1 to 1 1/2 |
| VS_Rgn2Sp | 91.21091 | rad/s | 93 | regions 1 1/2 to 2 |
| **VS_Rgn2K** | **2.332287** | N m/(rad/s)^2 | 92 | torque constant in Region 2, HSS side |
| VS_RtGnSp | 121.6805 | rad/s | 95 | comment: chosen as 99 % of PC_RefSpd, i.e. the 2 1/2 to 3 transition |
| PC_RefSpd | 122.9096 | rad/s | 77 | rated HSS speed (1173.7 rpm) |
| VS_RtPwr | 5296610.0 | W | 96 | rated power in Region 3, 5 MW / 0.944 |
| VS_SlPc | 10.0 | % | 99 | slip in Region 2 1/2 |
| VS_MaxTq | 47402.91 | N m | 91 | comment: chosen 10 % above rated torque, 43.09355 kN m |
| VS_MaxRat | 15000.0 | N m/s | 90 | |
| VS_Rgn3MP | 0.01745329 | rad | 94 | pitch (1 deg) above which Region 3 torque is used |

- **VS_RtTq is not a parameter of DISCON.F90.** Its value, 43.09355 kN m = 43 093.55 N m, appears in the VS_MaxTq comment (line 91) and in S1 Table 7-2. The rated torque used in Region 3 is VS_RtPwr / generator speed.
- Torque logic (lines 174-180 and 385-394): VS_SySp = VS_RtGnSp / (1 + 0.01 VS_SlPc); VS_Slope15 = VS_Rgn2K VS_Rgn2Sp^2 / (VS_Rgn2Sp - VS_CtInSp); VS_Slope25 = (VS_RtPwr/VS_RtGnSp) / (VS_RtGnSp - VS_SySp); VS_TrGnSp = (VS_Slope25 - sqrt(VS_Slope25 (VS_Slope25 - 4 VS_Rgn2K VS_SySp))) / (2 VS_Rgn2K). Region 3 if filtered speed >= VS_RtGnSp or commanded pitch >= VS_Rgn3MP: torque = VS_RtPwr/speed; Region 1 if speed <= VS_CtInSp: 0; Region 1 1/2 if speed < VS_Rgn2Sp: VS_Slope15 (speed - VS_CtInSp); Region 2 if speed < VS_TrGnSp: VS_Rgn2K speed^2; else Region 2 1/2: VS_Slope25 (speed - VS_SySp); then clipped to VS_MaxTq and rate limited.

### 2.4 Aerodynamic blade file and airfoils
- `5MW_Baseline/NRELOffshrBsline5MW_AeroDyn_blade.dat` (AeroDyn 15 format): 19 nodes, BlSpn measured from the root (0 to 61.5 m), BlTwist, BlChord, BlAFID (airfoil index 1 to 8). Chords and twists equal S1 Table 3-1 at the same nodes (for example BlSpn 18.45 m, twist 10.162 deg, chord 4.458 m; BlSpn 5.46667E+01 m, twist 0.863 deg, chord 2.313 m). The t_c column is 0.0 (not used). The file also holds BlCrvAC/BlSwpAC (prebend and sweep of the aerodynamic centre, up to -0.1157 m and -0.57 m).
- Airfoil files `Airfoils/<name>_A17.dat` do not state a thickness ratio in their headers (the scout read the first lines and searched for "thick" and "t/c": none).

### 2.5 What S2 does not establish
Cp(lambda); numeric rotor inertia; the isolated-blade natural frequencies (ElastoDyn computes them at run time and prints them in its summary file, which is not in the repository folder read); the contents of `DISCON.IN` (not found); the commit hash of the files read.

## 3. S3: TurbSim User's Guide, version 1.50 (IEC passages)

**What it establishes.** How TurbSim implements the IEC 61400-1 Kaimal spectrum, the integral scale parameters, the turbulence scale parameter, the standard-deviation ratios and the longitudinal coherence, for edition 2 and edition 3. It cites IEC 61400-1 3rd ed. as its Ref. [21] and the 2nd ed. as Ref. [24]. Quote (4 words): "assumes neutral atmospheric stability" (the Kaimal model, p. 29). Equation numbers below are those of S3. The text layer flattens stacked fractions, so the forms are read with their dimensions checked.

- **Kaimal spectrum, Eq. (21), p. 29**, for K = u, v, w: S_K(f) = 4 sigma_K^2 (L_K / u_hub) / (1 + 6 f L_K / u_hub)^(5/3), f cyclic frequency, u_hub mean hub-height wind speed. Valid for neutral stability (RICH_NO = 0). Text-line 1543-1549.
- **Integral scale parameter, Eq. (22), p. 30**: L_K = 8.10 Lambda_U for K = u, 2.70 Lambda_U for v, 0.66 Lambda_U for w.
- **Turbulence scale parameter, Eq. (23), p. 30**: Lambda_U = 0.7 min(30 m, HubHt) for edition 2; **Lambda_U = 0.7 min(60 m, HubHt) for edition 3**. So Lambda_1 = 0.7 z up to 60 m and 0.7 x 60 = 42 m above (the 42 m is derived by the scout).
- **Component ratios, Eq. (24), p. 30**: sigma_v = 0.8 sigma_u and sigma_w = 0.5 sigma_u.
- The IEC Kaimal spectra and standard deviations do not vary across the grid: TurbSim uses hub wind speed and hub height for all points (p. 30-31).
- **Coherence, Eq. (47), p. 38** (u-component of the IEC models): Coh_ij = exp( -a [ (f r / u_hub)^2 + (0.12 r / L_c)^2 ]^(1/2) ), with r the distance between the points. **The square root (radical) is not visible in the text layer of S3 or S3b**: the layout shows both terms squared inside a large bracket. The scout rendered the page (Section 6, S.7) so that the root can be confirmed by eye; the square root is the form given in the study brief, and this text layer can neither confirm nor refute it. Edition 2, Eq. (48): a = 8.8, L_c = 2.45 min(30 m, HubHt). **Edition 3, Eq. (49): a = 12, L_c = 5.67 min(60 m, HubHt).** Derived by the scout: 5.67 = 8.1 x 0.7, so L_c = 8.1 Lambda_U exactly, and L_c = 340.2 m for hub height at or above 60 m.
- v and w components: IEC does not specify coherence; TurbSim uses Coh = 1 for i = j and 0 for i not equal to j (Eq. (50), p. 39).
- **Turbulence intensity input, Eq. (6), p. 13**: with IECturbc given in percent, sigma_1 = IECturbc/100 x u_hub. The letters A, B, C select the IEC categories, "A" most turbulent; **Figure 7 (p. 13) plots sigma_1 and TI against V_hub for A, B, C**, but the text does not tabulate I_ref, the 0.75 or the b = 5.6 m/s. (Searched the whole text for "5.6" and "0.75": no IEC hit.)
- **Extreme turbulence model, Eq. (8), p. 14**: sigma_1 = c I_ref [0.072 (V_ave/c + 3)(u_hub/c - 4) + 10], c = 2 m/s default, cited as Eq. 19 in section 6.3.2.3 of IEC 61400-1 3rd ed. I_ref is "the expected value of turbulence intensity", V_ave is 20 % of the reference wind-speed average, both set by the turbine class.
- **Averaging time**: the IEC wind models use the 10-minute average wind speed; the EWM scaling in TurbSim is valid only for 10-minute simulations (p. 13).
- Von Karman (IECVKM, edition 2 only): L = 3.5 Lambda_U, sigma_v = sigma_w = sigma_u (Eqs. 25-28, p. 30). Not needed here.
- Edition handling (p. 12): IECstandard input "1-ED2" or "1-ED3"; without the edition, Kaimal uses edition 3.

**S3b (2006 guide, OSTI 891594)**: says the letters A, B, C correspond to the standard IEC Normal Turbulence Model characteristics; its IEC coherence equation is the same form with decrement b = 12 or 8.8 depending on the edition and again loses the radical in the text layer. No class table of I_ref was seen in the passages read.

**What S3 does not establish.** I_ref for classes A, B, C as numbers; b = 5.6 m/s; the 0.75 factor of the NTM; the 10-minute window for the NTM sigma_1 (only for the EWM and for simulation length); anything about edition 4 (2019).

## 4. S4 and S5: papers that restate the normal turbulence model

- S4 (arXiv:1904.07021, text-lines 120-136): the normal turbulence model gives the standard deviation as the 90 % quantile at the given 10-minute hub-height mean speed: **sigma_1 = I_ref (0.75 V_hub + b), b = 5.6 m/s** (their Eq. 2.1). V_hub is the 10-minute average. The turbulence intensity is sigma_1 / V_hub. **sigma_2 = 0.8 sigma_1, sigma_3 = 0.5 sigma_1** (Kaimal assumed). **I_ref is the expected value of the turbulence intensity at 15 m/s**, and I_ref = 0.16 for the case treated in that paper (the paper does not name the class in the lines read). Not the standard; secondary.
- S5(a) line 157 of the text: sigma_1 = I_ref (0.75 V_hub + 5.6), said to come from the IEC normal turbulence recommendation (the sentence was cut by the scout's search). S5(b) lines 284-307 contain I_ref (0.75 V_hub + 5.6 m/s) as a representative value and distributions. These were found by pattern search; the class table, if any, was **not read** (raw excerpts in Section 6b).
- A search-result summary (not a page the scout opened) said that an NREL forum thread gives I_ref = 0.16, 0.14, 0.12 for classes A, B, C of the 2005 edition and that one DTU paper uses 0.14 for class B. **The scout has not read this and does not count it as established.**

## 5. Verbatim: the OpenFAST blade file (S2), all 82 lines, as fetched

Source: https://raw.githubusercontent.com/OpenFAST/r-test/main/glue-codes/openfast/5MW_Baseline/NRELOffshrBsline5MW_Blade.dat (identical in size, 8049 bytes, to the copy the lead had downloaded). Rows are lines 17-65 (49 rows); mode shapes are lines 67-81.

```
------- ELASTODYN V1.00.* INDIVIDUAL BLADE INPUT FILE --------------------------
NREL 5.0 MW offshore baseline blade input properties.
---------------------- BLADE PARAMETERS ----------------------------------------
         49   NBlInpSt    - Number of blade input stations (-)
   0.477465   BldFlDmp(1) - Blade flap mode #1 structural damping in percent of critical (%)
   0.477465   BldFlDmp(2) - Blade flap mode #2 structural damping in percent of critical (%)
   0.477465   BldEdDmp(1) - Blade edge mode #1 structural damping in percent of critical (%)
---------------------- BLADE ADJUSTMENT FACTORS --------------------------------
          1   FlStTunr(1) - Blade flapwise modal stiffness tuner, 1st mode (-)
          1   FlStTunr(2) - Blade flapwise modal stiffness tuner, 2nd mode (-)
    1.04536   AdjBlMs     - Factor to adjust blade mass density (-)  !bjj: value for AD14=1.04536; value for AeroDyn=1.057344 (it would be nice to enter the requested blade mass instead of a factor here)
          1   AdjFlSt     - Factor to adjust blade flap stiffness (-)
          1   AdjEdSt     - Factor to adjust blade edge stiffness (-)
---------------------- DISTRIBUTED BLADE PROPERTIES ----------------------------
        BlFract               StrcTwst               BMassDen               FlpStff                 EdgStff
          (-)                   (deg)                 (kg/m)                 (Nm^2)                  (Nm^2)
 0.000000000000000E+00  1.330800000000000E+01  6.789349999999999E+02  1.811000000000000E+10  1.811360000000000E+10
 3.250000000000000E-03  1.330800000000000E+01  6.789349999999999E+02  1.811000000000000E+10  1.811360000000000E+10
 1.951000000000000E-02  1.330800000000000E+01  7.733630000000001E+02  1.942490000000000E+10  1.955860000000000E+10
 3.577000000000000E-02  1.330800000000000E+01  7.405500000000000E+02  1.745590000000000E+10  1.949780000000000E+10
 5.203000000000000E-02  1.330800000000000E+01  7.400420000000000E+02  1.528740000000000E+10  1.978880000000000E+10
 6.829000000000000E-02  1.330800000000000E+01  5.924960000000000E+02  1.078240000000000E+10  1.485850000000000E+10
 8.455000000000000E-02  1.330800000000000E+01  4.502750000000000E+02  7.229720000000000E+09  1.022060000000000E+10
 1.008100000000000E-01  1.330800000000000E+01  4.240540000000000E+02  6.309540000000000E+09  9.144700000000000E+09
 1.170700000000000E-01  1.330800000000000E+01  4.006380000000000E+02  5.528360000000000E+09  8.063160000000000E+09
 1.333500000000000E-01  1.330800000000000E+01  3.820620000000000E+02  4.980060000000000E+09  6.884440000000000E+09
 1.495900000000000E-01  1.330800000000000E+01  3.996550000000000E+02  4.936840000000000E+09  7.009180000000000E+09
 1.658500000000000E-01  1.330800000000000E+01  4.263210000000000E+02  4.691660000000000E+09  7.167680000000000E+09
 1.821100000000000E-01  1.318100000000000E+01  4.168200000000000E+02  3.949460000000000E+09  7.271660000000000E+09
 1.983700000000000E-01  1.284800000000000E+01  4.061860000000000E+02  3.386520000000000E+09  7.081700000000000E+09
 2.146500000000000E-01  1.219200000000000E+01  3.814200000000000E+02  2.933740000000000E+09  6.244530000000000E+09
 2.308900000000000E-01  1.156100000000000E+01  3.528220000000000E+02  2.568960000000000E+09  5.048960000000000E+09
 2.471500000000000E-01  1.107200000000000E+01  3.494770000000000E+02  2.388650000000000E+09  4.948490000000000E+09
 2.634100000000000E-01  1.079200000000000E+01  3.465380000000000E+02  2.271990000000000E+09  4.808020000000000E+09
 2.959500000000000E-01  1.023200000000000E+01  3.393330000000000E+02  2.050050000000000E+09  4.501400000000000E+09
 3.284600000000000E-01  9.672000000000001E+00  3.300040000000000E+02  1.828250000000000E+09  4.244070000000000E+09
 3.609800000000000E-01  9.109999999999999E+00  3.219900000000000E+02  1.588710000000000E+09  3.995280000000000E+09
 3.935000000000000E-01  8.534000000000001E+00  3.138200000000000E+02  1.361930000000000E+09  3.750760000000000E+09
 4.260200000000000E-01  7.932000000000000E+00  2.947340000000000E+02  1.102380000000000E+09  3.447140000000000E+09
 4.585500000000000E-01  7.321000000000000E+00  2.871200000000000E+02  8.758000000000000E+08  3.139070000000000E+09
 4.910600000000000E-01  6.711000000000000E+00  2.633430000000000E+02  6.813000000000000E+08  2.734240000000000E+09
 5.235800000000000E-01  6.122000000000000E+00  2.532070000000000E+02  5.347200000000000E+08  2.554870000000000E+09
 5.561000000000000E-01  5.546000000000000E+00  2.416660000000000E+02  4.089000000000000E+08  2.334030000000000E+09
 5.886200000000000E-01  4.971000000000000E+00  2.206380000000000E+02  3.145400000000000E+08  1.828730000000000E+09
 6.211500000000000E-01  4.401000000000000E+00  2.002930000000000E+02  2.386300000000000E+08  1.584100000000000E+09
 6.536600000000000E-01  3.834000000000000E+00  1.794040000000000E+02  1.758800000000000E+08  1.323360000000000E+09
 6.861800000000000E-01  3.332000000000000E+00  1.650940000000000E+02  1.260100000000000E+08  1.183680000000000E+09
 7.187000000000000E-01  2.890000000000000E+00  1.544110000000000E+02  1.072600000000000E+08  1.020160000000000E+09
 7.512200000000000E-01  2.503000000000000E+00  1.389350000000000E+02  9.088000000000000E+07  7.978100000000000E+08
 7.837600000000000E-01  2.116000000000000E+00  1.295550000000000E+02  7.631000000000000E+07  7.096100000000000E+08
 8.162600000000000E-01  1.730000000000000E+00  1.072640000000000E+02  6.105000000000000E+07  5.181900000000000E+08
 8.487800000000000E-01  1.342000000000000E+00  9.877600000000000E+01  4.948000000000000E+07  4.548700000000000E+08
 8.813000000000000E-01  9.540000000000000E-01  9.024800000000000E+01  3.936000000000000E+07  3.951200000000000E+08
 8.975600000000000E-01  7.600000000000000E-01  8.300100000000000E+01  3.467000000000000E+07  3.537200000000000E+08
 9.138200000000000E-01  5.740000000000000E-01  7.290600000000001E+01  3.041000000000000E+07  3.047300000000000E+08
 9.300800000000000E-01  4.040000000000000E-01  6.877200000000001E+01  2.652000000000000E+07  2.814200000000000E+08
 9.382100000000000E-01  3.190000000000000E-01  6.626400000000000E+01  2.384000000000000E+07  2.617100000000000E+08
 9.463600000000000E-01  2.530000000000000E-01  5.934000000000000E+01  1.963000000000000E+07  1.588100000000000E+08
 9.544700000000000E-01  2.160000000000000E-01  5.591400000000000E+01  1.600000000000000E+07  1.378800000000000E+08
 9.626000000000000E-01  1.780000000000000E-01  5.248400000000000E+01  1.283000000000000E+07  1.187900000000000E+08
 9.707300000000000E-01  1.400000000000000E-01  4.911400000000000E+01  1.008000000000000E+07  1.016300000000000E+08
 9.788600000000000E-01  1.010000000000000E-01  4.581800000000000E+01  7.550000000000000E+06  8.507000000000000E+07
 9.869900000000000E-01  6.200000000000000E-02  4.166900000000000E+01  4.600000000000000E+06  6.426000000000000E+07
 9.951200000000000E-01  2.300000000000000E-02  1.145300000000000E+01  2.500000000000000E+05  6.610000000000000E+06
 1.000000000000000E+00  0.000000000000000E+00  1.031900000000000E+01  1.700000000000000E+05  5.010000000000000E+06
---------------------- BLADE MODE SHAPES ---------------------------------------
     0.0622   BldFl1Sh(2) - Flap mode 1, coeff of x^2
     1.7254   BldFl1Sh(3) -            , coeff of x^3
    -3.2452   BldFl1Sh(4) -            , coeff of x^4
     4.7131   BldFl1Sh(5) -            , coeff of x^5
    -2.2555   BldFl1Sh(6) -            , coeff of x^6
    -0.5809   BldFl2Sh(2) - Flap mode 2, coeff of x^2
     1.2067   BldFl2Sh(3) -            , coeff of x^3
   -15.5349   BldFl2Sh(4) -            , coeff of x^4
    29.7347   BldFl2Sh(5) -            , coeff of x^5
   -13.8255   BldFl2Sh(6) -            , coeff of x^6
     0.3627   BldEdgSh(2) - Edge mode 1, coeff of x^2
     2.5337   BldEdgSh(3) -            , coeff of x^3
    -3.5772   BldEdgSh(4) -            , coeff of x^4
      2.376   BldEdgSh(5) -            , coeff of x^5
    -0.6952   BldEdgSh(6) -            , coeff of x^6


```

## 6. Scout arithmetic (everything in this section is derived by the scout)

Computed by plain Python arithmetic in the same command that wrote this file, from numbers in Sections 1 to 5. None of it is a source value. Where a source states the same quantity, both are shown. The scout read this output once, after writing it.

- S.1 Rows of the blade table parsed: 49 (expected 49). Sum of the BldEdgSh coefficients: 1.0000. Integration: piecewise-linear BMassDen and EdgStff between the 49 stations, midpoint rule, 123000 steps over 61.5 m.
- S.2 AdjBlMs = 1: blade mass = 16845 kg; first moment about the root = 345672 kg m; second moment about the root = 11188347 kg m^2.
- S.2 AdjBlMs = 1.04536: blade mass = 17609 kg; first moment about the root = 361352 kg m; second moment about the root = 11695850 kg m^2.
- S.2 AdjBlMs = 1.05734: blade mass = 17811 kg; first moment about the root = 365494 kg m; second moment about the root = 11829931 kg m^2.
  CM from the root = 20.521 m (independent of AdjBlMs). Source values, S1 Table 2-2: 17 740 kg; 363 231 kg m; 11 776 047 kg m^2; 20.475 m.
- S.3 One blade about the rotor axis without cone: I_blade = I_root + 2 r_h S_root + r_h^2 M = 11776047 + 2 x 1.5 x 363231 + 1.5^2 x 17740 = 12905655 kg m^2 (S1 Table 2-2 values; r_h = 1.5 m).
  Three blades with the precone factor cos^2(2.5 deg) = 0.998097, plus the hub 115 926 kg m^2: I_rotor+hub = 38759226 kg m^2.
  N^2 I_gen = 97^2 x 534.116 = 5025497 kg m^2. Rigid-drivetrain total on the low-speed shaft, I_rotor+hub + N^2 I_gen = 43784724 kg m^2.
  Same chain using the integrated table with AdjBlMs 1.04536: I_blade = 12819525, I_rotor+hub = 38501328, total = 43526825 kg m^2.
  Assumptions: precone only shortens the lever arms by cos(2.5 deg); hub inertia 115 926 about the axis; rotor and hub rigid; whether I_Rotor of S1 includes the hub is not stated in S1.
- S.4 AdjBlMs = 1: edgewise modal mass M* = 1355 kg (fraction 0.080 of the blade mass 16845 kg), modal stiffness K* = 6.7129e+04 N/m, f_edge1 = sqrt(K*/M*)/(2 pi) = 1.1204 Hz.
- S.4 AdjBlMs = 1.04536: edgewise modal mass M* = 1416 kg (fraction 0.080 of the blade mass 17609 kg), modal stiffness K* = 6.7129e+04 N/m, f_edge1 = sqrt(K*/M*)/(2 pi) = 1.0958 Hz.
- S.4 AdjBlMs = 1.05734: edgewise modal mass M* = 1432 kg (fraction 0.080 of the blade mass 17811 kg), modal stiffness K* = 6.7129e+04 N/m, f_edge1 = sqrt(K*/M*)/(2 pi) = 1.0896 Hz.
  Method: phi(x) = sum c_k x^k, k = 2..6, x = r/61.5; M* = AdjBlMs * integral of m phi^2 dr; K* = integral of EdgStff (d2phi/dr2)^2 dr. Cantilever blade, non-rotating, no gravity, no hub or tower motion, no centrifugal stiffening, no edge tuner (AdjEdSt = 1). Compare S1 Table 9-1 (whole turbine, brake on, asymmetric edgewise pitch): 1.0793 Hz FAST, 1.0740 Hz ADAMS.
- S.5 Region 2 constant in SI units: 0.0255764 N m/rpm^2 x (30/pi)^2 = 2.332288 N m/(rad/s)^2 on the generator shaft (DISCON VS_Rgn2K = 2.332287).
  On the low-speed shaft (T_LSS = N T_gen, omega_gen = N Omega): k_LSS = N^3 K = 97^3 x 2.332287 = 2128615 N m/(rad/s)^2; in rotor rpm: 0.0255764 x 97^3 = 23342.9 N m/rpm^2.
  Check with an air density of 1.225 kg/m^3 (an assumption of the scout, not read in S1): 0.5 rho pi R^5 Cp / lambda^3 = 2138774 N m/(rad/s)^2 for R = 63 m, Cp = 0.482, lambda = 7.55; ratio to k_LSS = 1.005.
  Region boundaries (generator rpm from S1 Table 7-2; rotor rpm = generator rpm / 97; wind speed = Omega R / lambda with R = 63 m and lambda = 7.55):
  - Region 1 to 1 1/2: 670.000 rpm generator = 6.9072 rpm rotor = 0.7233 rad/s rotor; wind speed at lambda 7.55: 6.04 m/s.
  - Region 1 1/2 to 2: 871.000 rpm generator = 8.9794 rpm rotor = 0.9403 rad/s rotor; wind speed at lambda 7.55: 7.85 m/s.
  - Region 2 1/2 to 3: 1161.963 rpm generator = 11.9790 rpm rotor = 1.2544 rad/s rotor; wind speed at lambda 7.55: 10.47 m/s.
  - rated: 1173.700 rpm generator = 12.1000 rpm rotor = 1.2671 rad/s rotor; wind speed at lambda 7.55: 10.57 m/s.
  DISCON constants in rpm (rad/s x 30/pi): VS_CtInSp 670.000, VS_Rgn2Sp 871.000, VS_RtGnSp 1161.963, PC_RefSpd 1173.700 rpm.
  From the DISCON formulas: VS_SySp = 110.6186 rad/s (1056.33 rpm generator, 10.890 rpm rotor); VS_Slope15 = 921.83 N m/(rad/s); VS_Slope25 = 3935.04 N m/(rad/s); VS_TrGnSp (Region 2 to 2 1/2) = 119.0138 rad/s = 1136.50 rpm generator = 11.716 rpm rotor, torque there K Omega^2 = 33035 N m.
  Rated torque: 5 296 610 W / 122.9096 rad/s = 43093.54 N m (S1: 43 093.55); at VS_RtGnSp: 43528.83 N m.
- S.6 Damping ratio from a 3 % logarithmic decrement: 0.477459 % of critical (S1: 0.477465 %). Rated rotor speed 12.1 rpm = 1.2671 rad/s; tip speed at R = 63 m = 79.83 m/s (S1: 80 m/s); tip-speed ratio at 11.4 m/s = 7.00. Rotor speed for lambda 7.55 at the 8 m/s of the Cp search = 9.155 rpm. Hub height 87.6 + 1.96256 + 5.0191 sin 5 deg = 90.0000 m (S1: 90).
  Turbulence: Lambda_1 = 0.7 x 60 = 42.0 m; L_c = 5.67 x 60 = 340.2 m and 8.1 x 42 = 340.2 m (8.1 x 0.7 = 5.67); Kaimal scales at z >= 60 m: L_u = 340.20 m, L_v = 113.40 m, L_w = 27.720 m.
  Chord and twist (S1 Table 3-1): at 60 % span (midpoint of nodes 10 and 11): chord 3.3790 m, twist 4.7745 deg; at 90 % span (one quarter from node 15 to 16): chord 2.2563 m, twist 0.7398 deg.
- S.7 The coherence page of S3 (printed page 38, PDF page 48) was rendered to `/tmp/claude-0/-home-user-SiteTest/8b34d6df-5462-5589-b418-3710ebaaeab4/scratchpad/sources/s1/p48-48.png` so that the square root in Eq. (47) can be checked by eye. Count of the square-root glyph in that page's text layer: 0.

## 6b. Unreviewed raw excerpts

The scout reached its call limit before reading these two passages. They are pasted unread by the command that wrote this file. Treat them as leads, not as findings.

S5(a), lines 150-165 of the text extraction of the DTU Orbit paper:

```
boxes for two wind speeds (U =11.4 and 18.0 m/s). We produced five turbulence boxes: one as
reference case for inflow conditions (Sec. 2.3) and four for the POD basis generation (Sec. 2.2).
   We characterized wind conditions using the IEC-recommended turbulence parameters for
the Mann model (L=33.6 m, Γ=3.9). The parameter αϵ2/3 was adjusted to achieve desired
turbulence intensities. For the reference case, a wind speed of 11.4 m/s and a target turbulence
intensity of 10% has been selected. For the POD basis generation, we examined two turbulence
intensities for each wind speed: a lower TI of approximately 10% and a higher T IN T M = σ1 /Vhub ,
with σ1 = Iref (0.75Vhub + 5.6), derived from the IEC standard recommendation for normal
turbulence models [7]. The turbulence standard deviation σ1 corresponds to the 90% quantile
for the specified hub height wind speed, where Iref is the reference turbulence intensity value
for a wind turbine class, set at 0.14 for class B turbines.
   For the reference case, the turbulence box had dimensions of 8192 × 64 × 64 (x × y × z),
with a grid spatial resolution of 3.125 m in the rotor plane, resulting in a box of 200 m × 200
m (y × z). The longitudinal dimension, over 800 s, extended 9120 m for Uo = 11.4 m/s. These
dimensions ensure sufficient turbulence field for 10-minute wind field simulation for aeroelastic
evaluation. The wind profile was modeled using a power-law with a shear exponent of 0.2.
```

S5(b), lines 280-310 of the text extraction of Wind Energy Science 9, 799-820:

```
                                                                                                    −1
mal distribution (T ∼ ln(µ, σ )), respectively (case 2). In ad-       K = 0.27Vhub + 1.4(m s ),                                    (7)
dition, Eq. (5) shows the 90 % quantile value of the same
                                                                                                    
                                                                      C = Iref 0.75Vhub + 3.3(m s−1 )                              (8)
distribution (case 1).
                                                                     In Eqs. (7) and (8), K and C represent the shape and scale
                       ln(T ) − µ                                     parameters of the Weibull distribution, respectively. Weibull
F (T ) = 0.5 1 + erf       √         ,                       (2)
                          σ 2                                         is very flexible and can be close to many other distribu-
                                                                      tions, including lognormal, depending on its shape parame-
     v                                   
     u                            !2
     u
     u         Iref 1.4(m s−1 )                                      ter. Figure 2 presents the cumulative probability distributions
σ = tln                                + 1,                 (3)
             0.75Vhub + 3.8(m s−1 )                                   of cases 2 and 3 in one mean wind speed of 8 m s−1 . In this
                                                                      plot, the horizontal axis shows turbulence (T ) levels, and ver-
                                    (σ )2                         tical axis refers to log10 (1−F (T )), where T ∼ ln(µT , σT ) and
µ = ln Iref 0.75Vhub + 3.8(m s−1 ) −          ,              (4)      T ∼ Wbl(K, C).
                                          2
                                                                       The lognormal distribution is generally heavy-tailed; how-
Trep. = Iref 0.75Vhub + 5.6(m s−1 )                          (5)
                                                                      ever, as Fig. 2 shows, for the distribution parameters provided
                                                                      in the standard, NTM with Weibull distribution has a thicker
   Equations (3) and (4) refer to the NTM model in IEC                tail. In other words, with the same accumulated probability
(2005). In these equations, T represents turbulence standard          in the tail (for example, the 10 % upper tail), the Weibull tail
deviation, and Iref is the reference turbulence intensity equal       covers lower turbulence levels than the lognormal distribu-
to 0.16 for the standard class 1 wind turbines (the current           tion and shows higher standard deviation. Overall, the two
case study). In addition, µ and σ are the mean and standard           distributions have opposite behaviors in the two portions be-
deviation of the logarithm of turbulence as a function of the         fore and after their intersection at the 90 % quantile.
```

## 7. Table of all numbers

Source codes: S1 report, S2 r-test, S3 TurbSim 1.50, S4 arXiv paper. "(d)" = derived by the scout (Section 6 item in the last column). "NE" = not established by any source the scout read.

| symbol | value | unit | source | location |
|---|---|---|---|---|
| R (TipRad) | 63 | m | S1; S2 | Table 1-1 p. 2 (diameter 126 m); ElastoDyn line 46 |
| R_hub (HubRad) | 1.5 | m | S1; S2 | Table 1-1 (hub diameter 3 m); ElastoDyn line 47 |
| blade length | 61.5 | m | S1 | Table 2-2 p. 6 |
| z_hub | 90 | m | S1 | Table 1-1 p. 2 |
| tower-top height; Twr2Shft | 87.6; 1.96256 | m | S1; S2 | Table 4-1 p. 13; ElastoDyn lines 64-65 |
| overhang; shaft tilt; precone | 5 (5.0191 along shaft); 5; 2.5 | m; deg; deg | S1; S2 | Table 1-1; ElastoDyn lines 48-57 (signs negative: upwind) |
| Omega_rated | 12.1 | rpm | S1; S2 | Tables 1-1, 5-1; ElastoDyn line 34 |
| Omega_cut-in = Omega_min | 6.9 | rpm | S1 | Table 1-1; p. 19 text |
| V cut-in, rated, cut-out | 3, 11.4, 25 | m/s | S1 | Table 1-1 |
| rated tip speed | 80 (79.83 d) | m/s | S1 (d: S.6) | Table 1-1 |
| N (GBRatio) | 97 | - | S1; S2 | Table 5-1 p. 14; ElastoDyn line 124 |
| rated generator speed | 1173.7 | rpm | S1 | Table 5-1 |
| generator efficiency | 94.4 | % | S1; S2 | Table 5-1; ServoDyn line 30 |
| I_hub | 115 926 | kg m^2 | S1; S2 | Table 4-1 p. 13; ElastoDyn line 84 |
| I_gen (HSS) | 534.116 | kg m^2 | S1; S2 | Table 5-1 p. 14; ElastoDyn line 86 |
| N^2 I_gen (LSS) | 5 025 497 (S1 states 5 025 500) | kg m^2 | S1; (d: S.3) | p. 14 text |
| m_blade | 17 740 | kg | S1 | Table 2-2 p. 6 |
| second mass moment about root | 11 776 047 | kg m^2 | S1 | Table 2-2 p. 6 |
| first mass moment about root | 363 231 | kg m | S1 | Table 2-2 p. 6 |
| CM from root | 20.475 | m | S1 | Table 2-2 p. 6 |
| AdjBlMs | 1.04536 (1.057344 for AeroDyn, per file comment) | - | S2 | blade file line 11 |
| zeta (blade, all modes) | 0.477465 | % of critical | S1; S2 | Table 2-2 p. 6; blade file lines 5-7 |
| BldEdgSh(2..6) | 0.3627, 2.5337, -3.5772, 2.376, -0.6952 | - | S2; S1 App. A | blade file lines 77-81; text-lines 2377-2381 |
| blade table | 49 rows | various | S2 | Section 5 of this file, lines 17-65 |
| I_rotor+hub, about the shaft | see S.3 (about 38.76e6) | kg m^2 | (d) | S.3; not given in S1 |
| I_drivetrain on LSS (rigid sum) | see S.3 (about 43.78e6) | kg m^2 | (d) | S.3; not given in S1 |
| edgewise modal mass, f_edge1 (isolated, Rayleigh) | see S.4 | kg; Hz | (d) | S.4 |
| full-system 1st edgewise (asym. pitch / yaw) | 1.0793 / 1.0898 (FAST); 1.0740 / 1.0877 (ADAMS) | Hz | S1 | Table 9-1 p. 30 (brake on, stationary) |
| full-system 1st collective flap | 0.6993 (FAST); 0.7019 (ADAMS) | Hz | S1 | Table 9-1 p. 30 |
| k (Region 2, HSS, rpm) | 0.0255764 | N m/rpm^2 | S1 | Table 7-2 p. 27; p. 19 |
| VS_Rgn2K (Region 2, HSS, SI) | 2.332287 | N m/(rad/s)^2 | S2; S1 App. | DISCON.F90 line 92; text-line 3645 |
| k_LSS (Region 2, LSS, SI) | 2 128 616 | N m/(rad/s)^2 | (d) | S.5 |
| gen. speed Region 1 / 1 1/2 | 670 (VS_CtInSp 70.16224 rad/s) | rpm | S1; S2 | Table 7-2; DISCON.F90 line 88 |
| gen. speed Region 1 1/2 / 2 | 871 (VS_Rgn2Sp 91.21091 rad/s) | rpm | S1; S2 | Table 7-2; DISCON.F90 line 93 |
| gen. speed Region 2 1/2 / 3 | 1 161.963 (VS_RtGnSp 121.6805 rad/s) | rpm | S1; S2 | Table 7-2; DISCON.F90 line 95 |
| gen. speed Region 2 / 2 1/2 | see S.5 (VS_TrGnSp) | rpm | (d) | S.5 |
| slip in Region 2 1/2 | 10 | % | S1; S2 | Table 7-2; DISCON.F90 line 99 |
| rated mech. power (VS_RtPwr) | 5.296610 MW (5 296 610) | MW; W | S1; S2 | Table 7-2; DISCON.F90 line 96 |
| rated gen. torque (VS_RtTq) | 43 093.55 | N m | S1 | Table 7-2; p. 19 (not a DISCON.F90 parameter) |
| max torque; torque rate | 47 402.91; 15 000 | N m; N m/s | S1; S2 | Table 7-2; DISCON.F90 lines 90-91 |
| low-pass corner | 0.25 (1.570796 rad/s) | Hz | S1; S2 | Table 7-2; DISCON.F90 line 58 |
| C_p,max; lambda_opt; beta | 0.482; 7.55; 0.0 | -; -; deg | S1 | Table 7-2 p. 27; text p. 19 (fixed 8 m/s, FAST+AeroDyn) |
| chord, twist, airfoil at 30 % span (r = 19.95 m) | 4.458 m; 10.162 deg; DU35 (about 35.1 % thick, d) | | S1 | Table 3-1 p. 7, node 6 |
| chord, twist, airfoil at 60 % span (r = 38.4 m) | 3.379 m; 4.77 deg; DU21 (about 21.0 %, d) | | S1 (d) | Table 3-1 nodes 10-11, midpoint |
| chord, twist, airfoil at 90 % span (r = 56.85 m) | 2.256 m; 0.74 deg; NACA64 (about 18.0 %, d) | | S1 (d) | Table 3-1 nodes 15-16, quarter point |
| rotor solidity | about 5.16 | % | S1 | p. 7 |
| Lambda_1 (edition 3) | 0.7 z for z <= 60 m; 42 above | m | S3 (42: d) | Eq. (23) p. 30 |
| L_u, L_v, L_w | 8.10, 2.70, 0.66 x Lambda_1 | m | S3 | Eq. (22) p. 30 |
| sigma_v/sigma_u; sigma_w/sigma_u | 0.8; 0.5 | - | S3; S4 | Eq. (24) p. 30; S4 below Eq. (2.1) |
| Kaimal S_K(f) | 4 sigma_K^2 (L_K/u_hub) / (1 + 6 f L_K/u_hub)^(5/3) | m^2/s | S3 | Eq. (21) p. 29 |
| coherence decrement a (edition 3) | 12 | - | S3 | Eq. (49) p. 38 |
| L_c (edition 3) | 5.67 min(60 m, z) = 8.1 Lambda_1 (d) | m | S3 | Eq. (49) p. 38 |
| coherence form | exp(-a sqrt((f r/u_hub)^2 + (0.12 r/L_c)^2)); root unconfirmed in the text layer | - | S3 | Eq. (47) p. 38; S.7 |
| coherence of v, w | 1 for i = j, 0 otherwise (TurbSim choice) | - | S3 | Eq. (50) p. 39 |
| NTM sigma_1 | I_ref (0.75 V_hub + b), b = 5.6 | m/s | S4 (second-hand; not in S3) | S4 Eq. (2.1) |
| I_ref meaning | expected turbulence intensity at 15 m/s | - | S4 | text under Eq. (2.1) |
| I_ref for classes A, B, C | NE (S4 uses 0.16 for its case) | - | NE | S3 Fig. 7 plots them; S4 |
| averaging time | 10 | min | S3; S4 | S3 p. 13 (IEC models, EWM); S4 |
| ETM | sigma_1 = c I_ref [0.072 (V_ave/c + 3)(u_hub/c - 4) + 10], c = 2 m/s | m/s | S3 | Eq. (8) p. 14 |

## 8. Open questions

1. **I_ref for classes A, B, C and the constants 0.75 and b = 5.6 m/s are not in any primary document the scout read.** S3 plots sigma_1 for A, B, C in Figure 7 (p. 13) but gives no numbers in text; S4 restates the formula and b but only I_ref = 0.16 for its own case. The lead's values 0.16, 0.14, 0.12 are consistent with that but unverified here. Next road: the same Figure 7 read from the PDF image; the two unread S5 papers (Section 6b); an NREL forum page; any open thesis that prints IEC 61400-1 Table 1.
2. **Edition 4 (2019) was not read at all.** S3 covers editions 2 and 3 only. Whether classes A+ / A / B / C and the b, Lambda_1 and coherence constants are unchanged in edition 4 is unverified.
3. **The square root in the coherence formula** (Eq. 47 of S3) could not be confirmed from the text layer. Check the rendered page named in S.7.
4. **Rotor inertia about the shaft** has no number in S1. The derived value (S.3) rests on Table 2-2, the 2.5 deg precone and the hub value. A primary check would be the ElastoDyn summary file of a real run, or a statement by the report authors. A search-result summary (not opened by the scout) quoted an NREL forum value of 38 759 236 kg m^2 for the rotor on the low-speed shaft; this is only a lead.
5. **Isolated-blade first edgewise frequency.** S1 gives only full-system values (Table 9-1, brake on) and the controller comment of about 1 Hz. S.4 gives a Rayleigh estimate with the ElastoDyn shape function; it ignores rotation, so the value in the rotating frame at 12.1 rpm needs centrifugal stiffening. Ref. [2] of S1 (Bir and Jonkman) may tabulate rotating frequencies; it was not opened.
6. **C_p(lambda).** S1 and S2 give one peak (0.482 at 7.55, 0 deg, found at 8 m/s). No curve or table was found. Roads left: run the AeroDyn driver or a BEM code on the S2 blade and airfoil files; read the ROSCO `Cp_Ct_Cq` file for the 5-MW; extract Figure 9-1 of S1.
7. **DISCON.IN** is not in the repository paths tried; constants come from `DISCON.F90`, which matches S1's own appendix. VS_RtTq is not a controller parameter; use 43 093.55 N m.
8. **Edgewise stiffness and mass tables carry two conventions.** S1 states that the tabulated BMassDen is pre-scaling; S2 applies AdjBlMs = 1.04536 (AD14) or 1.057344 (AeroDyn, per the file comment). S.2 shows which one reproduces 17 740 kg. The lead must choose, and say which.
9. **Pitch actuator constants** differ between S1 Table 7-2 (971 350 000 N m/rad; 206 000 N m/(rad/s)) and S2 ServoDyn (7.0e8; 2.3e5). Not needed for the pendulum study, noted for completeness.
10. **Commit of r-test** not recorded; the files were fetched from branch `main` on 23 October 2026.
