# Dossier: edgewise (in-plane) blade vibration of multi-MW turbines in operation

Scout run of 23 Oct 2026, for the Rotor Pendula study (0.1 kg pendulum inside a turning blade, braked by a generator).
Question: how hard does a MW blade shake in the rotor plane, across the blade axis, near 8 m/s mean wind, at about 30, 60 and 90 % span; how weak is the edgewise damping; what does the rotationally sampled spectrum look like.

## 0. Read this first

1. I found no measurement of in-blade edgewise acceleration (in g or m/s2) on a multi-megawatt blade, and no simulation paper that prints edgewise acceleration standard deviations at 30, 60 and 90 % span. Every number about the resonant part is therefore missing, not uncertain.
2. What the sources do establish: the edgewise response is dominated by a once-per-revolution (1P) gravity term, the first edgewise mode shows as a small bump near 5 to 6 times the rotor frequency (simulation, IEA 15 MW), and the first edgewise whirling modes are weakly damped (measured on a 2.75 MW turbine: below 10 % logarithmic decrement, which is about 1.6 % of critical, derived).
3. "Derived by the scout" marks my own arithmetic or mechanics. "Eyeballed" marks a value I read off a plotted figure by eye. Neither is a printed number in a source.
4. Files were downloaded into `/tmp/claude-0/-home-user-SiteTest/8b34d6df-5462-5589-b418-3710ebaaeab4/scratchpad/sources/s2/` and extracted with pdftotext. Nothing was run.

Status key used per source: FULL = I downloaded the whole file and read the relevant sections as extracted text. FIG = I also looked at a rendered figure page. EXTRACT = a fetch tool returned a model-written extraction, so second-hand. SNIPPET = only a search-result summary; not opened, not usable as evidence.

---

## 1. Sources I opened and used

### 1.1 Schena, Munters, Helsen, Mendez (2025), POD-based sparse stochastic estimation of wind turbine blade vibrations [FULL + FIG]

- Reference: L. Schena, W. Munters, J. Helsen, M. A. Mendez, "POD-Based Sparse Stochastic Estimation of Wind Turbine Blade Vibrations", arXiv:2504.08505v1 [eess.SY], 11 Apr 2025 (preprint submitted to Journal of Sound and Vibration). Link: https://arxiv.org/abs/2504.08505 (PDF: https://arxiv.org/pdf/2504.08505).
- What it establishes: in OpenFAST/BeamDyn simulations of the IEA 15 MW turbine in turbulent wind, the edgewise tip motion is gravity-driven and periodic at the rotor frequency. The authors write the edgewise response is "mostly dominated by inertial and gravitational forces" (Sec. 5.1). Because the blade frame rotates, the static gravity load projects onto the edgewise axis once per revolution, giving a strong 1P line in the edgewise spectrum (Fig. 3d). A second bump near 6P "likely indicates" a structural mode of the blade in this direction (their wording, Sec. 5.1). The flapwise and axial spectra show peaks at nP (1P, 2P, 3P ...), Fig. 3b and 3f. The second POD mode is edgewise and nearly sinusoidal in azimuth (Sec. 5.3), small at the top and bottom positions where gravity is along the blade axis and larger on the rising and falling sides.
- Numbers, with location:
  - Turbine: IEA 15 MW reference turbine, hub height 150 m, blade length 117 m (Sec. 2).
  - Setup (Sec. 3): OpenFAST 3.5.3 with BeamDyn, AeroDyn v15 with dynamic BEM and Beddoes-Leishman dynamic stall, rigid tower, tower shadow, ROSCO controller. Below rated the pitch is fixed at 0 deg and the generator torque tracks optimal tip-speed ratio. Mean wind speeds 4 to 17.2 m/s in steps of 2.2 m/s, i.e. 4, 6.2, 8.4, 10.6, 12.8, 15.0, 17.2 m/s (list derived by the scout from the stated start, end, step; the labels 6.2, 8.4, 10.6, 12.8, 15.0, 17.2 appear in Fig. 3). Turbulence intensity 5, 10 and 15 %, Kaimal spectrum, TurbSim, three seeds each, 500 s runs with the first 100 s discarded. Sampling 160 Hz.
  - Text value (Sec. 5.1), as printed: at rated conditions the relative tip displacement "reaches ux = 15 m, uy = -2.2 m and uy = -0.7 m". The second "uy" is evidently a typo for uz (axial), since Fig. 3e shows the axial tip excursion reaching about -1 m near 10.6 m/s. Edgewise mean is biased negative (towards the leading edge) because of gravity and aerodynamic load projections (text, Sec. 5.1).
  - Fig. 3c, edgewise tip displacement uy as violin plots against mean wind speed, TI 5 % (blue) and 15 % (orange). Eyeballed from the rendered page: at 8.4 m/s the distribution runs from about -2.6 m to about +0.5 m; at 6.2 m/s from about -2.0 m to about +0.9 m. That is a lowest-to-highest span of about 3 m, centred about 1 m on the negative side. Reading error about 0.5 m. Distribution is bimodal at low TI (the two gravity extremes); high TI smooths it.
  - Fig. 3d, edgewise tip-displacement spectrum against f/f1P, eyeballed: the 1P peak sits at about 85 to 88 dB; the floor between 2P and 4P is near 45 dB; the bump near f/f1P of about 5 to 6 reaches about 60 to 62 dB (largest at the higher wind speeds, small or absent at 6.2 m/s in the legend colours I could separate). So the mode bump is about 25 dB below the 1P peak in tip displacement. The dB reference is not stated in the text I read.
- Conditions: simulated, IEA 15 MW (not NREL 5 MW), tip displacement only, no accelerations printed for the full blade, wind speeds 6.2 and 8.4 m/s bracket 8 m/s.
- Does not establish: any acceleration value; any value at 30, 60, 90 % span (only the tip is shown in Fig. 3); edgewise damping; the frequency of the edgewise mode in Hz (only in units of the rotor frequency); tower motion (rigid tower here). The "uy" text value has a typo.

### 1.2 Hansen, Thomsen, Fuglsang, Knudsen (2006), two methods for estimating aeroelastic damping from experiments [FULL]

- Reference: M. H. Hansen, K. Thomsen, P. Fuglsang, T. Knudsen, "Two Methods for Estimating Aeroelastic Damping of Operational Wind Turbine Modes from Experiments", Wind Energy 9(1-2):179-191, 2006. Open copy (Aalborg University portal, publisher PDF): https://vbn.aau.dk/ws/files/58189002/Hansen2006.pdf
- What it establishes: measured (from strain gauges on a real turbine) modal damping of the first two edgewise whirling modes during normal operation above rated wind speed. In the paper's words: "The estimated damping of the edgewise whirling modes is below 10% logarithmic decrement" (p. 189), with a slight increase at higher wind speed. The model (HAWCStab) predicted lower damping than the estimate for both whirling modes but the same trend (p. 189-190). The paper states that the edgewise whirling modes need only 0.5 deg pitch amplitude at about 1.8 Hz to be excited in simulation, against more than 1 deg for the flapwise modes, and relates this to their low damping (Sec. on pitch excitation). In the 18 measurement periods the edgewise whirl peaks lie at about 5.5P and 7.5P, i.e. split by plus and minus 1P around the first edgewise blade frequency (Fig. 8 text, p. 188), and the same spectrum shows deterministic 1P, 3P, 6P and 9P components.
- Numbers, with location:
  - Edgewise whirl damping: below 10 % logarithmic decrement (p. 189). Converted by the scout: zeta = delta / (2 pi) is about 1.6 % of critical at 10 % log. decr. (derived by the scout; "below" so an upper bound).
  - Structural log. decrements used to tune the model: about 1.5 % and 1.8 % for the first two blade modes (stated as measured), about 2 % for the first tower modes (stated as estimated) (Sec. 3, model tuning). Derived by the scout: zeta about 0.24 % and 0.29 %.
  - Standstill edgewise frequencies, Table I (two columns, computed and peak-picked from measured strain, order as in the caption): first vertical edgewise 1.825 and 1.838 Hz; first horizontal edgewise 1.862 and 1.853 Hz.
  - Mean rotor speed used to scale the frequency axis of Fig. 8: 17.3 rpm (maximum rotor speed). Derived by the scout: 5.5P and 7.5P are 1.59 and 2.16 Hz, mean 1.87 Hz, consistent with the standstill 1.83 to 1.86 Hz.
  - Higher edgewise damping for forward whirl than backward whirl in the HAWCStab results (Fig. 1 text), but the paper says the estimates show no significant FW/BW difference.
- Conditions: NM80 prototype, pitch-regulated, variable speed, rated 2.75 MW, STABCON project; operational modal analysis (stochastic subspace identification) of seven strain-gauge signals over 18 periods, wind above rated; the five low-wind periods were discarded because tower modes coincide with 3P at minimum rotor speed. Measured, not simulated.
- Does not establish: damping at 8 m/s (below rated); damping from accelerometers; any acceleration amplitude; damping of the NREL 5 MW blade; a value, only an upper bound, for edgewise damping. Authors warn the estimated damping can be biased because the excited vibration is not a pure mode (their abstract) and the closed-loop controller is included in the estimate.

### 1.3 Wanke, Bergami, Verelst (2020), edgewise whirl damping upwind versus downwind [FULL, text only; figures not rendered]

- Reference: G. Wanke, L. Bergami, D. R. Verelst, "Differences in damping of edgewise whirl modes operating an upwind turbine in a downwind configuration", Wind Energy Science 5:929-944, 2020, https://doi.org/10.5194/wes-5-929-2020 (open access; PDF https://wes.copernicus.org/articles/5/929/2020/wes-5-929-2020.pdf).
- What it establishes: in HAWC2 and HAWCStab2 simulations of a Suzlon S111 2.1 MW model, the edgewise damping (damping from decay of the edgewise blade displacement at 75 % radius, uniform wind, no turbulence) is a function of wind speed and rises from cut-in towards the middle of the operating range (Sec. 3.2, Fig. 4). Downwind configuration changes the forward whirl damping by up to minus 39 % and the backward whirl damping by up to plus 18 % (abstract). The introduction summarises earlier work: stall-induced edgewise vibration on stall-regulated turbines (Petersen et al. 1998), a 600 kW turbine excited with a rotating nacelle mass where the forward whirl mode was significantly better damped than the backward one (Thomsen et al. 2000), and Hansen (2007) deriving an aerodynamic damping coefficient for a single airfoil from inflow velocity and lift and drag slopes (Sec. 1, 2.1).
- Numbers: the damping values in Fig. 4 are normalised to the upwind configuration at 9 m/s, so no absolute percent of critical is printed in the text I read. The only absolute figures are relative changes (39 % lower FW, 18 % higher BW, largest near rated wind).
- Conditions: simulated, 2.1 MW, steady uniform wind, no turbulence, upwind baseline plus downwind variant.
- Does not establish: absolute edgewise damping in percent of critical; anything for 5 MW or larger; any acceleration. It is relevant only as the upwind baseline trend and as a pointer to Hansen (2007).

### 1.4 NREL 5 MW reference turbine definition report (OSTI 947422) [FULL, text only]

- Reference: J. Jonkman et al., definition report for the NREL 5 MW baseline turbine, downloaded from https://www.osti.gov/servlets/purl/947422 (25 pages as extracted; I did not read the cover, so I do not assert the report number here). Section and table numbers below are as printed in the text.
- What it establishes: the model's structural damping, the first edgewise natural frequencies of the full system, rotor-speed limits, and that rotor speed rises linearly with wind speed in Region 2 at constant tip-speed ratio.
- Numbers, with location:
  - Blade structural damping: 0.477465 % of critical in all modes of the isolated blade, "which corresponds to the 3% logarithmic decrement" of the DOWEC study (Sec. 2, repeated as Table 2-2 and the FAST blade file entries BldFlDmp and BldEdDmp). The check 3 % / (2 pi) = 0.4775 % holds (derived by the scout).
  - Blade length 61.5 m along the preconed axis, mass 17,740 kg, radial centre of mass 20.475 m from the root (Table 2-2).
  - Cut-in and rated rotor speed 6.9 rpm and 12.1 rpm (Table, rated rotor speed also in Sec. 3 text).
  - Table 9-1, full-system natural frequencies in hertz, stationary with brake engaged, blades at 0 deg pitch, aerodynamic damping ignored: 1st blade asymmetric edgewise pitch mode 1.0793 (FAST) and 1.0740 (ADAMS); 1st blade asymmetric edgewise yaw mode 1.0898 (FAST) and 1.0877 (ADAMS).
  - Fig. 9-1 (steady uniform wind runs) plots in-plane tip deflection IPDefl1 against wind speed; the text says the out-of-plane deflection peaks at rated and the peak is "visible, though less pronounced" in the in-plane tip deflection. The curve values are only in the figure, which I did not render.
  - Control and operating schedule: the report states rotor and generator speeds increase linearly with wind speed in Region 2 at constant tip-speed ratio, then the rotor speed is held above rated.
- Conditions: model definition and steady-state runs, not turbulence statistics.
- Does not establish: any turbulent-wind edgewise statistics or acceleration; operating-condition (aerodynamic) edgewise damping; the 8 m/s rotor speed as a printed number. Note the report's blade damping (0.477 %) is structural only and is much smaller than the 2.5 % used by Bir and Jonkman below.

### 1.5 Bir and Jonkman (2007), aeroelastic instabilities of large offshore and onshore wind turbines [FULL, text only; Fig. 5 not rendered]

- Reference: G. Bir, J. Jonkman, "Aeroelastic Instabilities of Large Offshore and Onshore Wind Turbines", preprint NREL/CP-500-41804, Aug 2007, EAWE 2007 Torque from Wind Conference, Lyngby. OSTI 912953: https://www.osti.gov/servlets/purl/912953 (OSTI record of the same title, 1353160, not opened).
- What it establishes: linearised FAST/AeroDyn eigenanalysis of the NREL 5 MW turbine over the operating range 3 to 25 m/s, onshore and on a barge. The first edgewise (lag) blade mode appears as progressive, regressive and collective rotor modes. The authors state "all flap modes are highly damped" while the lag modes are the lower-damped ones. Damping of the progressive and regressive lag modes "increases rapidly" from 3 m/s to about 11 m/s, then decreases, and is almost constant beyond 22 m/s (Fig. 5 text, onshore). Offshore (barge) leaves the rotor-mode damping almost unchanged (Fig. 7 text).
- Numbers, with location:
  - Table 1: cut-in, rated, cut-out wind 3, 11.4, 25 m/s; cut-in and rated rotor speed 6.9 and 12.1 rpm; rated tip speed 80 m/s; blade structural damping ratio 2.5 %, tower 1.0 %. Sec. 5.3 compares 0.5 % and 2.5 % blade structural damping for a parked condition.
  - The numerical lag-mode damping at 8 m/s is only in Fig. 5, which is a plot I could not extract as text. Not printed in the text.
  - Derived by the scout: tip speed 80 m/s over rated 12.1 rpm (1.267 rad/s) gives a rotor radius of about 63 m.
- Conditions: simulated eigenvalues, uniform steady wind, controlled pitch and rotor speed schedule (Fig. 2), no turbulence, no unsteady aerodynamics in the linearisation (the text says FAST ignores some unsteady aerodynamic effects in this procedure; I read only the first part of that sentence).
- Does not establish: the lag-mode damping in percent at 8 m/s (curve not read); any acceleration or tip deflection under turbulence. The 2.5 % structural damping differs from the reference model's 0.477 %, so the lag damping in Fig. 5 is not the reference-model value.

### 1.6 Jonkman (2007), dynamics modelling and loads analysis of an offshore floating wind turbine [FULL, grepped only]

- Reference: J. M. Jonkman, NREL/TP-500-41958, OSTI 921803, https://doi.org/10.2172/921803, https://www.osti.gov/servlets/purl/921803 (233 pages).
- What I found: load-case tables of extremes (Appendix F) and a chapter comparing land- and sea-based responses of the NREL 5 MW turbine; the text states DLC 1.4 drives the extreme out-of-plane tip deflection (nearly 14 m, Sec. 6) and that in-plane tip-deflection extremes are larger on the barge because of faster rotor speed excursions. The 8 m/s mention is a control-design linearisation point only.
- Numbers: none usable. I did not find a mean and standard deviation table for in-plane tip deflection in normal turbulence at 8 m/s; I did not read Appendix F table by table.
- Does not establish: any normal-turbulence edgewise statistics at 8 m/s. Listed so the next scout does not repeat the search.

### 1.7 Muxica et al. (2024), autonomous sensor system for low-capacity wind turbine blade vibration measurement [EXTRACT only]

- Reference: D. Muxica et al., Sensors 24(6):1733, 2024, https://doi.org/10.3390/s24061733; open at https://pmc.ncbi.nlm.nih.gov/articles/PMC10976074.
- What the fetch tool's extraction reports: nine ADXL345 three-axis accelerometers (three per blade, spaced about 0.8 m) on the outer blade surface of 5 kW, 7 m diameter turbines, 200 Hz sampling, x edgewise and z flapwise; no wind speeds in m/s; no edgewise acceleration amplitude (RMS or peak) in g or m/s2 reported in the text; flapwise first peak 10.2 Hz shifting to 9.9 Hz on a damaged replica; rotor speeds above 170 r/min on a windy day.
- Use: none for the study except as evidence that this small-turbine data set does not give amplitudes. Second-hand; I did not read the paper myself.

---

## 2. Sources I looked for and could not open (do not cite from this dossier)

| Source | What happened | What the snippet said (unverified) |
|---|---|---|
| Hansen (2007), "Aeroelastic instability problems for wind turbines", Wind Energy 10:551-577, doi 10.1002/we.242 | Only the DTU Orbit record and an abstract mirror; no open full text found | Abstract only: stall-induced vibration and classical flutter; edgewise aerodynamic damping not discussed in the snippet |
| NREL 2.8 MW edgewise structural damping paper (research-hub.nrel.gov, Journal of Physics Conf. Ser. 022069) | curl to research-hub returned a proxy 502 | Snippet: structural damping falls across the first three edgewise modes after correcting a bias of the Cov-SSI method |
| Bir and Jonkman (2008), OMAE, "Modal dynamics of large wind turbines with different support structures" | nrel.gov refused by both curl and WebFetch (no DNS) | Snippet confirms only the title and that BModes was used |
| MMU e-space paper, "Dynamic responses analysis of a 5MW NREL wind turbine blade under flapwise and edgewise vibrations" | Download returned HTTP 202 with an empty body | none |
| Fitzgerald thesis and Fitzgerald, Basu, Nielsen (2013), active TMD for in-plane vibration | thesis PDF on tara.tcd.ie returned HTTP 403 | Snippet: edgewise aerodynamic damping low; no numbers seen. A master's thesis in the same results (Cunha 2017) says aerodynamic damping almost completely inhibited a passive TMD in-plane |
| MDPI Sensors 24(8):2480 (bistable piezoelectric harvester for blade monitoring), doi 10.3390/s24082480 | Not opened | Snippet: lab tests with 1 g base acceleration stated as "representative" of mid-span of a 55 m blade at 10 m/s. This is an assumption in a design paper, not a measurement; do not use without opening it |
| Grundkotter et al. (2022), precision blade deflection measurement using wireless inertial sensor nodes, Wind Energy; IEEE 8956859 energy-self-sufficient inertial node | Not opened | Snippets say a harvester powers an IMU node each revolution; no edgewise amplitudes in the excerpt |
| Galhardo et al., identifying natural frequencies of a rotor with blade-mounted accelerometers and strain gauges (SSRN 7227934); ScienceDirect S0263224124023170 (single accelerometer, operating offshore blade) | Not opened | Snippet: in power production only the first edgewise asymmetric pair was observed. These are the best leads for real blade-mounted accelerometer data |
| Rotationally sampled turbulence papers (AAU "efficient rotational sampling method", Applied Energy 2013 111:624-635 on IDEAS, FAU abstract, NSF PAR 10532195) | AAU, IDEAS, FAU not opened; NSF PAR 10532195 was downloaded and is a flutter paper (Caracoglia 2024), not about rotational sampling | Snippet: spectral concentrations at multiples of the rotor frequency, first spike at 1P, split peaks at 1P/2, 1P, 3P/2 |
| Risoe-R-1388 modal analysis of blades; Spectral kurtosis DD-SSI offshore blade paper; NREL forum threads | Not opened. Forum posts are not primary and I did not use them | none |

---

## 3. Derived by the scout (arithmetic and mechanics, not printed in a source unless stated)

All depend on stated inputs; check before use.

1. Gravity in the blade frame. In a frame turning with the blade, gravity (9.81 m/s2) rotates once per revolution. Its component along the edgewise axis therefore has amplitude 9.81 m/s2 (1 g) at the rotor frequency, for any point on the blade and any wind speed, independent of span, for a blade with the edgewise axis in the rotor plane (pitch near 0 deg below rated; pre-cone and twist corrections not applied). A pendulum or accelerometer feels this as part of the specific force. Support in sources: Schena et al. attribute the strong 1P edgewise component to gravity (Sec. 5.1); the number 1 g is mine.
2. Rotor speed at 8 m/s for the NREL 5 MW. Not read. Scaling the rated 12.1 rpm linearly with wind speed to 8 m/s from the rated wind 11.4 m/s gives 8.5 rpm (12.1 x 8 / 11.4 = 8.49 rpm), so f1P = 0.14 Hz and Omega = 0.889 rad/s. This is likely a little low, because the report's Region 2 line is a constant tip-speed-ratio line that reaches the rated rotor speed before rated wind (the report's Fig. 9-1 has the exact value and I did not extract it). Rated: 12.1 rpm gives f1P = 0.2017 Hz and Omega = 1.267 rad/s.
3. Edgewise resonance in units of rotor frequency. First edgewise frequency 1.0793 Hz (Table 9-1, stationary, so centrifugal stiffening is not included and the rotating value is somewhat higher). That is 5.35 f1P at rated (1.0793 / 0.2017) and about 7.6 f1P at 8.5 rpm. Whirling modes split by plus and minus 1P around this (Hansen 2006).
4. Centripetal acceleration (radial, along the blade). Omega squared is 0.79 s-2 at 8.5 rpm and 1.61 s-2 at 12.1 rpm. With a rotor radius of about 63 m (derived from tip speed and rotor speed, section 1.5), at 30, 60, 90 % of radius (19, 38, 57 m) that is 15, 30, 45 m/s2 (1.5, 3.0, 4.6 g) at 8.5 rpm. This points outward along the axis, perpendicular to the edgewise direction; the study needs it because it sets the effective gravity the pendulum hangs in.
5. Acceleration from edgewise tip amplitude at the first mode, NREL 5 MW. (2 pi x 1.0793 Hz)^2 = 46.0 s-2. A tip amplitude of 0.005 m gives 0.23 m/s2 (0.023 g); 0.01 m gives 0.46 m/s2; 0.1 m gives 4.6 m/s2 (0.47 g). Mode-shape factor at 30, 60, 90 % span not applied (see open questions). Ignores centrifugal stiffening.
6. Spectrum weighting. A displacement spectrum converts to an acceleration spectrum with a factor (2 pi f)^4 in power (f^2 in amplitude). For a bump at f/f1P of about 5.5 against the peak at 1P, that factor is 5.5^4 = 915, i.e. +29.6 dB whichever dB convention the figure uses. So the IEA 15 MW bump that is about 25 dB below the 1P peak in tip displacement (eyeballed, section 1.1) would sit at roughly +5 dB relative to the 1P peak in an acceleration spectrum, in peak height. That compares only the kinematic structural acceleration (second derivative of the plotted displacement), not the 1 g gravity term of item 1, which a displacement plot does not show as an acceleration. Rough, one figure, different turbine.
7. Random-vibration scaling. For a lightly damped mode driven by broadband forcing the rms response goes as zeta^(-1/2) (textbook Miles-type result, not from these sources). Between the two structural dampings in the sources (0.477 % and 2.5 %) that is a factor 2.3 in rms (sqrt(2.5/0.477)).
8. Pendulum back-reaction on the blade. 0.1 kg over 17,740 kg is 5.6e-6, negligible.
9. Hansen's damping converted: 10 % log. decr. gives about 1.6 % critical (see 1.2).

---

## 4. Rotationally sampled turbulence: what I actually have

- Verified in the sources I opened (qualitative only): in OpenFAST with Kaimal turbulence at 5, 10, 15 % TI, the IEA 15 MW tip-displacement spectra show peaks at the rotor frequency and its harmonics, 1P, 2P, 3P and so on (Schena et al., Fig. 3b flapwise: eyeballed about 90 dB at 1P and about 72 dB at 2P, then weaker; Fig. 3f axial). In the edgewise direction the line is almost entirely at 1P (gravity), with the mode bump near 5 to 6 P (Fig. 3d). The NM80 measured tower-moment spectrum has deterministic 1P, 3P, 6P, 9P components and the edgewise whirl modes at about 5.5P and 7.5P (Hansen et al. 2006, Fig. 8 text).
- Not verified: the classical shape of the rotationally sampled spectrum (energy moved from low frequency into peaks at multiples of the rotor frequency, first peak at 1P, peaks narrowing and growing with a point nearer the tip). My search snippets say this, but I did not open the papers behind them. From memory the classics are by Connell, and by Kristensen and Frandsen (early 1980s), and Veers (Sandia, late 1980s); I did not locate or read them in this run, so treat the names as leads only.

---

## 5. Table of usable numbers

Only rows that come from sources I opened. "d" = derived by the scout; "e" = eyeballed from a plotted figure.

| Quantity | Value | Unit | Turbine | Wind | Span | Source | Location |
|---|---|---|---|---|---|---|---|
| Edgewise tip displacement, lowest to highest (e) | about -2.6 to +0.5 | m | IEA 15 MW, 117 m blade (simulated) | 8.4 m/s, TI 5 and 15 % | tip | Schena et al. 2025 | Fig. 3c |
| Edgewise tip displacement, lowest to highest (e) | about -2.0 to +0.9 | m | IEA 15 MW | 6.2 m/s, TI 5 and 15 % | tip | Schena et al. 2025 | Fig. 3c |
| Edgewise tip displacement at rated, as printed | -2.2 | m | IEA 15 MW | 10.6 m/s | tip | Schena et al. 2025 | Sec. 5.1 text (typo in the sentence) |
| Edgewise tip PSD, 1P peak (e) | 85 to 88 | dB (reference not stated) | IEA 15 MW | 6.2 to 17.2 m/s | tip | Schena et al. 2025 | Fig. 3d |
| Edgewise tip PSD, mode bump near 5 to 6 f1P (e) | 60 to 62 | dB (reference not stated) | IEA 15 MW | mainly 8.4 to 17.2 m/s | tip | Schena et al. 2025 | Fig. 3d |
| Edgewise tip PSD, floor between 2P and 4P (e) | about 45 | dB | IEA 15 MW | all | tip | Schena et al. 2025 | Fig. 3d |
| Gravity edgewise component, 1P amplitude (d) | 9.81 | m/s2 (1 g) | any | any | any | scout; qualitative support Schena et al. | Sec. 5.1 |
| First edgewise asymmetric modes, stationary (FAST) | 1.0793 and 1.0898 | Hz | NREL 5 MW | none (parked, aero damping ignored) | blade | NREL 5 MW report | Table 9-1 |
| First edgewise asymmetric modes, stationary (ADAMS) | 1.0740 and 1.0877 | Hz | NREL 5 MW | none | blade | NREL 5 MW report | Table 9-1 |
| Blade structural damping, all modes | 0.477465 | % critical (= 3 % log. decr.) | NREL 5 MW | none | blade | NREL 5 MW report | Sec. 2, Table 2-2 |
| Blade structural damping used in stability study | 2.5 | % critical | NREL 5 MW | 3 to 25 m/s | blade | Bir and Jonkman 2007 | Table 1, Sec. 5 |
| Edgewise whirl damping, measured, upper bound | below 10 (about 1.6 as zeta, d) | % log. decr. | NM80, 2.75 MW | above rated | blade (root strain gauges) | Hansen et al. 2006 | p. 189, Fig. 9 |
| Blade-mode structural log. decrements, measured | 1.5 and 1.8 (about 0.24 and 0.29 as zeta, d) | % log. decr. | NM80 | standstill | blade | Hansen et al. 2006 | Sec. 3, model tuning |
| NM80 edgewise standstill frequencies | 1.825/1.838 and 1.862/1.853 | Hz | NM80 | none | blade | Hansen et al. 2006 | Table I |
| NM80 whirl peaks, in rotor-frequency units | about 5.5P and 7.5P at 17.3 rpm (about 1.59 and 2.16 Hz, d) | P, Hz | NM80 | above rated | blade | Hansen et al. 2006 | Fig. 8 text |
| Rotor speed, cut-in and rated | 6.9 and 12.1 | rpm | NREL 5 MW | 3 and 11.4 m/s | rotor | Bir and Jonkman 2007; NREL 5 MW report | Table 1 |
| Rated tip speed | 80 | m/s | NREL 5 MW | 11.4 m/s | tip | Bir and Jonkman 2007 | Table 1 |
| Blade length, mass, centre of mass from root | 61.5; 17,740; 20.475 | m; kg; m | NREL 5 MW | none | blade | NREL 5 MW report | Table 2-2 |
| Lag-mode damping trend | rises rapidly 3 to about 11 m/s, falls to about 20 m/s, flat above 22 m/s | text only, no values | NREL 5 MW | 3 to 25 m/s | blade (rotor modes) | Bir and Jonkman 2007 | Fig. 5 text |
| Edgewise whirl damping change, downwind vs upwind | FW up to minus 39, BW up to plus 18 | % (relative) | Suzlon S111 2.1 MW | near rated | blade (75 % radius) | Wanke et al. 2020 | abstract, Fig. 4 |
| Rotor speed at 8 m/s (d) | about 8.5 (probably a little low) | rpm | NREL 5 MW | 8 m/s | rotor | scout from NREL 5 MW report | section 3, item 2 |
| Omega squared at 8.5 rpm (d) | 0.79 | s-2 | NREL 5 MW | 8 m/s | rotor | scout | section 3, item 4 |
| Tip acceleration per metre of edgewise tip amplitude, mode 1 (d) | 46.0 | m/s2 per m | NREL 5 MW | any | tip | scout from Table 9-1 | section 3, item 5 |

Missing rows I looked for and did not find: edgewise acceleration standard deviation (any span), tip deflection standard deviation at 8 m/s for the NREL 5 MW, aerodynamic edgewise damping of the NREL 5 MW at 8 m/s as a number, resonant fraction of the edgewise response.

---

## 6. The decomposition the study asked for

| Part | What the sources give | Honest status |
|---|---|---|
| (i) 1P gravity | 1 g amplitude along the edgewise axis (derived). The only simulation I read confirms that 1P gravity dominates the edgewise tip motion. Tip displacement amplitude about 1.5 m (half of the eyeballed 3 m span) for IEA 15 MW, a stiff-static effect, not a structural acceleration | Solid in principle; amplitude of the kinematic part depends on rotor speed |
| (ii) Resonant near the first edgewise mode | Frequency 1.08 Hz (NREL 5 MW stationary, FAST). Appears as a bump near 5 to 6 f1P in IEA 15 MW tip spectra, about 25 dB under the 1P peak in displacement (eyeballed). Damping below 10 % log. decr. measured on NM80 above rated; structural only 0.477 % (reference) to 2.5 % (Bir and Jonkman) | No sourced amplitude. Only a conversion factor and a damping range |
| (iii) The rest | A displacement floor about 40 dB below the 1P peak between 2P and 4P (IEA 15 MW, eyeballed); nP lines in flapwise and axial | No acceleration number |

---

## 7. Range the study should sweep, stated honestly

The sources I could read do not agree, and in most places they say nothing.

- Damping of the first edgewise mode (total, structural plus aerodynamic): the sources span 0.48 % of critical (structural only, reference model) through 2.5 % (structural, a stability study) with a measured upper bound near 1.6 % on a different turbine above rated wind. The aerodynamic part at 8 m/s on the NREL 5 MW is not printed in any text I read (it is a curve in Bir and Jonkman Fig. 5). Sweep total zeta from 0.5 % to 3 % of critical as the span of the printed numbers; if the study needs a higher edge, 5 % is my judgement, not a sourced value.
- Resonant amplitude: no sourced value. The only bound the sources give is that the resonant tip motion is small against the 1P gravity motion (about 25 dB lower at the peak in one simulation, eyeballed, another turbine). For a swept free parameter, use tip edgewise rms amplitude of 0.005 to 0.1 m, which maps to 0.23 to 4.6 m/s2 (0.02 to 0.47 g) at the tip at 1.08 Hz (derived, section 3, item 5). This range is my judgement and has no source; scale it by the mode shape at 30, 60, 90 % span.
- 1P gravity: fixed at 1 g amplitude. Do not sweep it. Sweep the rotor frequency instead: 0.14 Hz (about 8.5 rpm at 8 m/s, estimate) to 0.20 Hz (12.1 rpm rated), which places the first edgewise mode at about 7.6P to 5.3P; whirling modes at plus and minus 1P of that.
- Do not treat the IEA 15 MW and NM80 numbers as NREL 5 MW numbers. They are the only quantitative anchors I opened; they bracket the physics but are different blades.

---

## 8. Open questions for the next pass

1. Is there a published measurement of in-blade edgewise acceleration (RMS, spectrum) on a MW blade in operation? Best leads, not opened: Galhardo et al. (SSRN 7227934), the single-accelerometer offshore blade paper (ScienceDirect S0263224124023170), Grundkotter et al. 2022 (Wind Energy, wireless inertial nodes), the MDPI Sensors 24(8):2480 design paper (check the source of its "1 g" assumption).
2. What is the NREL 5 MW first edgewise damping, total, at 8 m/s? Bir and Jonkman 2007 Fig. 5 contains it (render page; read the Lag1_reg and Lag1_prog curves at 8 m/s; note the 2.5 % structural assumption). The study itself could also get it by linearising OpenFAST, which I was told not to do.
3. What is the exact rotor speed at 8 m/s for the NREL 5 MW? Fig. 9-1 of the report (GenSpeed and RotSpeed) answers it; replaces my 8.5 rpm estimate.
4. Mode shape of the first edgewise mode at 30, 60, 90 % span. The FAST blade file in the 5 MW report carries polynomial mode-shape coefficients (I saw the damping lines of that file but did not read the coefficients).
5. Whether the pendulum feels the kinematic structural acceleration only through the blade frame (relative motion) or through the full non-inertial frame. The 1 g gravity term, the centripetal term and the tangential term r times the rotor-speed derivative are all in the frame of the blade; only the last two are not in a displacement spectrum. Rotor-speed variation at 8 m/s turbulence (control response, Region 2 torque control) is not in any source I opened; Jonkman 2007 notes in-plane tip extremes follow rotor acceleration, only for extreme events.
6. Primary source on the shape of the rotationally sampled turbulence spectrum, with peak heights against span position, for a spectrum the study can reuse. Not found.
7. Hansen (2007), Wind Energy 10:551, full text for the aerodynamic damping coefficient of an airfoil in edgewise motion; the open PDF was not found. Wanke et al. cite it for a formula that depends on inflow velocity and lift and drag slopes.
8. The NREL 2.8 MW paper (structural damping of the first three edgewise modes, Cov-SSI) for the claim that structural damping is not a simple stiffness-proportional model.
