# Terms and symbols of project 07, one name each

Written by V (voice session) in step 0, 11 November 2026, after reading ch00–ch09 and the guide whole.
Section numbers: chapter.section in the order of `SECTIONS` / `S` (ch00 §0.1 question … §0.5 road; ch01 §1.1 beam … §1.11 limits;
ch02 §2.1 intro … §2.13 hand; ch03 §3.1 gun … §3.8 checks; ch04 §4.1 picture … §4.8 checks; ch05 §5.1 blurs … §5.5 checks;
ch06 §6.1 picture … §6.8 checks; ch07 §7.1 picture … §7.7 checks; ch08 §8.1 picture … §8.5 checks).

Rule: a term is defined once, at the place in the "defined" column. Later chapters remind in a few words with a pointer
("the reduced brightness $B_r$ of chapter 2"), never define it again. "Other names" lists names the text now uses that must go
(or, where marked *keep*, variants that are legitimate in their context).

Symbols inside maths cannot be changed by the editors (VOICE.md). Where one letter means two things, the collision is listed under
"Symbol collisions" at the end so that the prose around the maths can name which meaning is meant.

## 1 · The task and light (chapter 0)

| term | symbol | meaning | unit | defined | other names to remove |
|---|---|---|---|---|---|
| pitch | $p$ | distance from the middle of one line to the middle of the next | nm | ch00 §0.1 | "period (pitch)" in §0.2 is a reminder, *keep* |
| half-pitch | — | half the pitch, the width of one line in a dense pattern | nm | ch00 §0.1 (as "a line about … wide"), named §0.2 | — |
| numerical aperture | NA | $n\sin\alpha$ of a lens | 1 | ch00 §0.2 | — |
| Abbe limit | $p_{\min}=\lambda/2\mathrm{NA}$ | smallest period light can resolve | nm | ch00 §0.2 | "optical limit" (caption, *keep* as description) |
| critical dimension | CD | the width of a chip feature as measured | nm | ch07 §7.1 (named forward in ch05 §5.4 with CD-SEM) | — |
| CD-SEM | — | scanning electron microscope that measures critical dimensions | — | ch05 §5.4 | — |

## 2 · The electron in fields (chapter 1)

| term | symbol | meaning | unit | defined | other names |
|---|---|---|---|---|---|
| elementary charge, electron mass | $e$, $m$ | CODATA 2018 | C, kg | ch01 §1.2 | — |
| cathode, anode | C, A | emitting electrode; positive electrode with a slit | — | ch01 §1.1 | — |
| anode voltage | $V_a$ | tube voltage of chapter 1 | V | ch01 §1.1 | — |
| Lorentz force | $q(\mathbf E+\mathbf v\times\mathbf B)$ | force on a charge | N | ch01 §1.3 (used), derived §1.4 | — |
| Lorentz factor | $\gamma$ | $(1-v^2/c^2)^{-1/2}$ | 1 | ch01 §1.4 (first used §1.3 example with pointer) | "relativistic factor" (ch00 table, *keep* in table) |
| relative energy | $\epsilon=eV/mc^2$ | kinetic energy over rest energy | 1 | ch01 §1.2 | — |
| Lagrangian, action, proper time | $L$, $S$, $\tau$ | — | — | ch01 §1.4 | — |
| canonical momentum | $\mathbf p=\gamma m\mathbf v+q\mathbf A$ | — | kg m/s | ch01 §1.4 | — |
| kinetic momentum | $\gamma m\mathbf v$ | — | kg m/s | ch01 §1.4 | — |
| Hamiltonian | $H$ | — | J | ch01 §1.5 | — |
| electronvolt | eV | energy gained falling through one volt | J | ch01 §1.5 | "electron volt" (ch01 §1.5) → electronvolt |
| de Broglie wavelength | $\lambda=h/p$ | — | pm | ch00 §0.3 (used), derived ch01 §1.5, exact ch03 §3.2 | — |
| gyroradius | $r_L$ | radius of the circle in a magnetic field | m | ch01 §1.3 | "Larmor radius" (*keep* once, as alias at definition) |
| cyclotron angular frequency | $\Omega$ | $eB/\gamma m$ | s⁻¹ | ch01 §1.3 | — |
| helix | — | path in a uniform axial field | — | ch01 §1.7 | — |
| Helmholtz pair | — | two coils a radius apart | — | ch01 §1.6 | — |
| RK4 (classical Runge–Kutta) | — | fourth-order integrator | — | ch01 §1.8 | — |
| Boris pusher | — | second-order rotation integrator | — | ch01 §1.8 | "Boris step", "Boris" (*keep* as short form after definition) |
| phase error | — | lag of the computed angle | rad | ch01 §1.8 | — |

## 3 · The source (chapter 2)

| term | symbol | meaning | unit | defined | other names |
|---|---|---|---|---|---|
| Fermi level | — | top of filled states; zero of energy in ch02 | eV | ch02 §2.1 | — |
| work function | $\varphi$ | energy from Fermi level to rest outside | eV | ch02 §2.1 | — |
| thermionic, Schottky, field emission | — | three ways out | — | ch02 §2.1 | — |
| cold field emission (CFE) | — | field emission from an unheated tip | — | ch00 §0.4 (quoted), ch02 §2.1 (physics) | "cold source", "cold tip", "cold field emitter", "cold preset" (*keep*: the device, the tip, the preset) |
| apex field | $F=V/(kr)$ | field at the tip | V/nm | ch02 §2.1 | — |
| field factor | $k$ | geometry factor of the apex field | 1 | ch02 §2.1 | — |
| image force / image energy | $F_\mathrm{im}$, $U_\mathrm{im}$ | — | N, eV | ch02 §2.2 | — |
| Schottky–Nordheim barrier | $U(x)$ | — | eV | ch02 §2.2 | "SN barrier" |
| scaled field | $f=F/F_R$ | — | 1 | ch02 §2.2 | — |
| Schottky lowering | $\Delta\varphi$ | — | eV | ch02 §2.2 | — |
| WKB exponent, transmission | $G$, $D$ | — | 1 | ch02 §2.3 | — |
| barrier functions | $v(f)$, $t(f)$, $s(f)$ | — | 1 | ch02 §2.3 ($v$), §2.5 ($t$, $s$) | — |
| supply function | $N(w)$ | electrons per area, time, energy | m⁻² s⁻¹ J⁻¹ | ch02 §2.4 | — |
| normal energy, transverse energy | $w$, $\varepsilon_t$ | — | eV | ch02 §2.4 | — |
| Fowler–Nordheim equation | $J_0$ | — | A/m² | ch02 §2.5 | — |
| decay width | $d$ | energy scale of the emitted distribution | eV | ch02 §2.5 | — |
| voltage conversion length | $\zeta=kr$ | — | nm | ch02 §2.5 | — |
| Richardson–Dushman law | $A_R$ | — | A m⁻² K⁻² | ch02 §2.6 | — |
| total-energy distribution | $P(\varepsilon)$ | — | — | ch02 §2.7 | — |
| energy spread | $\Delta E$ | FWHM of $P$ | eV | ch02 §2.7 | "energy width" (ch02 fig caption, ch05 caption) → energy spread |
| FW50 energy spread | $\Delta E_{50}$ | narrowest interval holding half the electrons | eV | ch05 §5.2 | "FW50 energy width" → FW50 energy spread |
| brightness | $B$ | current per area per solid angle | A m⁻² sr⁻¹ | ch02 §2.8 (named in ch00 §0.4) | — |
| reduced brightness | $B_r$ | $B/V$ (ch02), exactly $B/V^*$ (ch03) | A m⁻² sr⁻¹ V⁻¹ | ch02 §2.8; exact form and proof ch03 §3.4 | — |
| virtual source, its diameter | $d_v$ | disc the far-field paths seem to come from | nm | ch02 §2.8 | "virtual source size" (ch02 table, ch08) → virtual source diameter |
| working point | — | ch02's example values (4 V/nm, 4.5 eV, 300 K) | — | ch02 §2.1–2.3 examples | — |
| cold preset, Schottky preset | — | the two parameter sets of ch02's simulation | — | ch02 §2.6 (Schottky), §2.7 (cold) | — |
| Hertz–Knudsen flux | $\Phi$ | molecules per area per time | m⁻² s⁻¹ | ch02 §2.10 | — |
| coverage | $\theta$ | fraction of apex sites occupied | 1 | ch02 §2.10 | — |
| sticking, capture, desorption | $s$, $\kappa$, $k_d$, $E_d$, $\nu_0$ | — | — | ch02 §2.10 | — |
| flash (cleaning) | — | short heating that desorbs the apex | — | ch02 §2.10 | — |
| emission current | $I_e$ | — | A | ch02 §2.13 table | — |

## 4 · Acceleration (chapter 3)

| term | symbol | meaning | unit | defined | other names |
|---|---|---|---|---|---|
| extractor, extraction voltage | $V_\mathrm{ex}$ | electrode that pulls electrons out | V | ch03 §3.1 | "extractor voltage" → extraction voltage |
| acceleration voltage | $V_\mathrm{acc}$ | sets the column energy | V | ch03 §3.1 | "column voltage" (*keep* as description) |
| landing voltage | $V_\mathrm{land}$ | energy at the wafer | V | ch03 §3.1 | "landing energy" (ch00, ch06: energy $eV_\mathrm{land}$, *keep*) |
| relativistically corrected voltage, beam voltage | $V^*$ | $V(1+eV/2mc^2)$ | V | ch03 §3.2 | — (both names stated at definition; later "the beam voltage $V^*$ of chapter 3") |
| retarding field | — | field that slows the beam before the wafer | — | ch03 §3.3 | — |
| Liouville's theorem | — | phase-space area conserved | — | ch03 §3.4 | — |
| practical brightness | $B_\mathrm{pr}=B_r/\ln 2$ | — | A m⁻² sr⁻¹ V⁻¹ | ch03 §3.5 | — |
| FW50 | — | diameter holding half the current | nm | ch03 §3.5 | — |
| probe current | $I_p$ | — | A | ch03 §3.5 | — |
| beam half-angle | $\alpha$ | half-angle of the cone at the wafer | rad | ch00 §0.3 (named), ch03 §3.5 (formula) | — |
| Boersch effect | — | energy broadening by Coulomb pushes | — | ch03 §3.6 (named ch02 §2.13) | — |

## 5 · The lens (chapter 4)

| term | symbol | meaning | unit | defined | other names |
|---|---|---|---|---|---|
| axial field | $B(z)$ | field on the axis | T | ch04 §4.2 | — |
| Glaser's bell field | $B_0$, $a$ | peak and half-width | T, m | ch04 §4.2 | — |
| Busch's theorem, Larmor rate | $\dot\theta=eB/2\gamma m$ | — | s⁻¹ | ch04 §4.3 | — |
| paraxial ray equation | $r''=-\eta B^2 r$ | — | — | ch04 §4.3 | — |
| lens constant | $\eta=e/8mV^*$ | — | C kg⁻¹ V⁻¹ | ch04 §4.3 | — |
| image rotation | $\theta_\mathrm{rot}$ | — | rad | ch04 §4.3 | — |
| dimensionless lens strength | $k^2$, $\omega$ | — | 1 | ch04 §4.4 | — |
| focal length | $f$ | — | mm | ch04 §4.4 | — |
| objective lens | — | last lens of the column | — | ch04 §4.5 | — |
| working distance | $W\!D$ | lens centre to wafer | mm | ch04 §4.5 | — |
| magnification | $M$ | — | 1 | ch04 §4.5 | — |
| spherical / chromatic aberration coefficient | $C_s$, $C_c$ | — | mm | ch04 §4.6 | — |
| Scherzer's theorem | — | $C_s,C_c>0$ for round static lenses | — | ch04 §4.6 | — |
| Airy disc | — | diffraction pattern of a round aperture | — | ch04 §4.6 Ex. 4.3 (radius), ch05 §5.2 (diameter) | — |

## 6 · The spot (chapter 5)

| term | symbol | meaning | unit | defined | other names |
|---|---|---|---|---|---|
| probe | — | the focused beam on the wafer | — | ch00 §0.1 ("a very thin probe") | "spot" (*keep*: the footprint, chapter title) |
| source image | $d_I$ | image of the virtual source on the wafer | nm | ch05 §5.1 | — |
| disc of least confusion | — | narrowest section of an aberrated bundle | nm | ch05 §5.2 | — |
| root-power sum | — | Barth–Kruit rule for adding FW50 terms | — | ch05 §5.2 | — |
| probe diameter | $d_p$ | FW50 (or quadrature) diameter | nm | ch05 §5.2 | — |
| FW50 terms | $d_A$, $d_S$, $d_C$ | diffraction, spherical, chromatic | nm | ch05 §5.2 | — |
| optimum angle | $\alpha_\mathrm{opt}$ | angle of the smallest probe | mrad | ch05 §5.3 | "best angle" (*keep*, plain-word alias) |

## 7 · The wafer (chapter 6)

| term | symbol | meaning | unit | defined | other names |
|---|---|---|---|---|---|
| elastic, inelastic collision | — | turn at a nucleus; loss to electrons | — | ch06 §6.1 | — |
| backscattered electrons | BSE | leave with most of their energy | — | ch06 §6.1 (named ch00 §0.3) | — |
| backscattering coefficient | $\eta$ | BSE per incident electron | 1 | ch06 §6.1 | "backscatter" (as noun, ch06 Ex. 6.4) → backscattering |
| secondary electrons | SE | leave with < 50 eV | — | ch06 §6.1 | — |
| secondary yield | $\delta$ | SE per incident electron | 1 | ch06 §6.1 | "secondary-electron yield" (*keep*) |
| Monte Carlo simulation | — | following electrons one by one with random draws | — | ch06 §6.1 | — |
| dwell time | $t_d$ | time the probe stays on a pixel | s | ch06 §6.2 | — |
| differential cross-section | $\mathrm d\sigma/\mathrm d\Omega$ | — | m² sr⁻¹ | ch06 §6.3 | — |
| impact parameter | $b$ | — | m | ch06 §6.3 | — |
| screening parameter | $a$ | — | 1 | ch06 §6.3 | — |
| elastic mean free path | $\lambda_\mathrm{el}$ | — | nm | ch06 §6.3 | — |
| Sommerfeld parameter | $Z\alpha_\mathrm{fs}/\beta$ | — | 1 | ch06 §6.3 | — |
| Mott cross-section | — | relativistic partial-wave cross-section with spin | — | ch06 §6.3 | — |
| stopping power | $\mathrm dE/\mathrm ds$ | — | keV/cm | ch06 §6.4 | — |
| mean ionisation energy | $J$ | — | eV | ch06 §6.4 | — |
| plasmon | — | collective oscillation of valence electrons | eV | ch06 §6.4 | — |
| escape depth | $\lambda_s$ | absorption length of secondaries | nm | ch06 §6.6 | — |
| energy per secondary | $\varepsilon$ | — | eV | ch06 §6.6 | — |
| universal yield law | $\delta_\mathrm{max}$, $E_\mathrm{max}$ | — | 1, eV | ch06 §6.6 | — |
| Kanaya–Okayama range | $R_\mathrm{KO}$ | — | nm | ch06 §6.7 | — |
| interaction volume, $r_{90}$ | $V_\mathrm{int}$ | — | nm³, nm | ch06 §6.7 | — |
| lateral spread | $\sigma_s$ | rms birth distance of escaping SE | nm | ch06 §6.7 | — |
| core width, core fraction, halo width | $\sigma_\mathrm{core}$, $f_\mathrm{core}$, $\sigma_\mathrm{halo}$ | — | nm, 1, nm | ch06 §6.7 | — |

## 8 · The measurement (chapters 7 and 8)

| term | symbol | meaning | unit | defined | other names |
|---|---|---|---|---|---|
| secant law | $1/\cos\theta$ | yield on a tilted surface | 1 | ch07 §7.1 | — |
| sidewall angle | $\beta$ | wall lean from vertical | ° | ch07 §7.2 | — |
| expected profile | $Y(x)$ | — | 1 | ch07 §7.2 | — |
| shot noise | — | Poisson scatter of counted electrons | — | ch00 §0.4 (picture), ch07 §7.3 (law) | — |
| collection fraction | $\eta_c$ | share of emitted electrons detected | 1 | ch07 §7.3 | — |
| contrast-to-noise ratio of one line | SNR | — | 1 | ch07 §7.3 | — |
| dose | — | charge per area per image | µC cm⁻² | ch07 §7.3 Ex. 7.1 | — |
| threshold rule, floor level | $S_\text{floor}$ | — | counts | ch07 §7.4 | — |
| bias | — | read width minus true width | nm | ch07 §7.4 | — |
| precision | $\sigma_\mathrm{CD}$ | scatter of the measured width | nm | ch07 §7.5 | — |
| lines averaged | $N$ | rows of a square image | 1 | ch07 §7.5, §7.6 | — |
| overhead | $t_\mathrm{ov}$ | stage move, focus, recognition per site | s | ch07 §7.6 | — |
| normalised sensitivity | $S_{yx}$ | $\partial\ln y/\partial\ln x$ | 1 | ch08 §8.2 | — |
| tolerance Monte Carlo | — | random draws of machine errors | — | ch08 §8.3 | — |
| measurement window | — | map of settings that meet a specification | — | ch08 §8.4 | "process window" (*keep* for lithography's own term only) |

## Symbol collisions (maths cannot change; the prose must say which is meant)

- $p$: pitch (ch00), momentum (ch00 §0.3 says so; ch01 on), pressure (ch02 §2.10), pattern period (ch07 §7.2). The pitch of a helix (ch01 §1.7) is a word, not $p$.
- $B_r$: reduced brightness (ch02, ch03, ch05, ch08) and the radial field component (ch04 §4.1–4.2). Doubt listed in LEDGER.md.
- $\eta$: lens constant $e/8mV^*$ (ch04), backscattering coefficient (ch06, ch07), with $\eta_c$ the collection fraction (ch07).
- $f$: scaled field (ch02), focal length (ch04), $f_\mathrm{core}$ (ch06).
- $a$: arrival rate (ch02 §2.10), lattice constant (ch02), Glaser half-width (ch04), screening parameter (ch06), FN constant $a$ (ch02 §2.5).
- $k$: field factor (ch02), Boltzmann constant in $kT$ (ch02), lens strength $k^2$ (ch04), Joy–Luo $k$ (ch06), counts $k$ (ch07).
- $\varepsilon$: transverse/total energy (ch02), excitation drift (ch08), energy per secondary (ch06); $\epsilon=eV/mc^2$ (ch01).
- $\theta$: deflection angle (ch01), coverage (ch02), azimuth (ch04), wall tilt (ch07).
- $\alpha$: beam half-angle (ch00, ch03, ch05), angle to the field (ch01 §1.7), lens acceptance angle (ch00 §0.2).
- $N$: turns (ch01 §1.6), steps per turn (ch01 §1.8), supply function $N(w)$ (ch02), electrons simulated (ch06), lines averaged (ch07).
