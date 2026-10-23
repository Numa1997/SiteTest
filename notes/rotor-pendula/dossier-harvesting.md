# Dossier: harvesting from random vibration, nonlinear and chaotic harvesters, pendula on rotors

Scout S3, 23 October 2026. For the Rotor Pendula study. Sources downloaded only into
`/tmp/claude-0/-home-user-SiteTest/8b34d6df-5462-5589-b418-3710ebaaeab4/scratchpad/sources/s3/` (text extracted with pdftotext; nothing executed).

Convention in this file: **[FULL]** = whole text opened and read; **[PARTIAL]** = part of the text (named); **[ABSTRACT]** = only an abstract or metadata reached; **[NOT OPENED]** = lead only.
"Derived by the scout" = arithmetic or algebra of my own, not printed in a source. Every other formula below was read in the named source.

---

## 0. Headline answer

**Does any source I opened show chaos beating a linear harvester at equal mass and best damping? No.**

- Under Gaussian white-noise base acceleration, three opened sources (Halvorsen 2013 [FULL], Green et al. 2012 [FULL], Daqaq 2011 [ABSTRACT]) say the opposite: mean power of a monostable Duffing or bistable harvester cannot exceed what a suitably chosen linear harvester gives. Halvorsen proves an upper bound that holds for any confining potential and shows a linear harvester can reach it, under stated conditions.
- The only opened source that credits chaos with a power gain is Cai & Zhu 2024 [FULL]. It compares the same device in different motion regimes (oscillation vs rolling or chaotic rotation) under harmonic horizontal shaking. It uses "gross output power" (the power dissipated in the damper) and runs no linear baseline. Its one random-excitation test has no linear baseline either. Its "double-mass pendulum" is a single-degree-of-freedom pendulum, not a double pendulum.
- Claims that a chaotic double pendulum raises harvested power (Kumar et al., the BIT, Korean and HIT papers) were reached only second-hand or through search-engine summaries. What they compare (equal mass? best damping? which excitation?) is unknown. See section 6.

**The sentence in the brief about Halvorsen 2008 (power depends only on proof mass and acceleration spectral density) holds only in a limit.** The 2013 paper (Eq. 14, below) shows the optimally loaded linear harvester's power depends on the resonance frequency unless the coupling is strong. See 1.1. I could not open the 2008 paper.

---

## 1. Halvorsen: white-noise bound

### 1.1 Halvorsen, E. (2008), "Energy Harvesters Driven by Broadband Random Vibrations", J. Microelectromech. Syst. 17(5):1061-1071. **[NOT OPENED]**

- DOI 10.1109/jmems.2008.928709 (Crossref, title, volume, pages, October 2008 confirmed). IEEE paywall. No open copy found: no arXiv entry, and the USN open-archive record I found (handle 11250/2468265) is the 2013 paper.
- I could not check: the exact formula, the spectral-density convention in that paper, and the sentence about resonance frequency.
- **What the 2013 paper (read in full) says about it.** Ref [13] there is this paper. Quote of scope: "All results for linear systems are exact and taken from [13] unless said otherwise." So the following linear results are 2008 results, as relayed by 2013 (section 1.2):
  - the exact linear optimum, Eq. (14);
  - the efficiency limit η → 1 as k²Qm → ∞.
- The mean input power Pin = m Sa/2 is credited by 2013 to Scruggs, J. Sound Vib. 320:707 (2009) (ref [19], proved there for linear harvesters), not to Halvorsen 2008.
- **Open for the study:** obtain the 2008 text (author copy via USN/HVL, interlibrary loan) before quoting its wording.

### 1.2 Halvorsen, E. (2013), "Fundamental issues in nonlinear wideband-vibration energy harvesting", Phys. Rev. E 87:042129. **[FULL]**

- arXiv:1209.3184v2 [nlin.AO], 2 May 2013: <https://arxiv.org/abs/1209.3184>, PDF <https://arxiv.org/pdf/1209.3184>. Read the arXiv v2 text, not the PRE typeset page. The PRE reference is as given in the brief.
- A second copy exists at the USN open archive (<https://openarchive.usn.no/usn-xmlui/handle/11250/2468265>). The server returned a 2 KB HTML stub to curl, so I did not use it.

**What it establishes (paraphrase).** A mechanically nonlinear harvester (any elastic potential U(x)) is driven by Gaussian white-noise base acceleration. The mean input power is fixed. Upper bounds on output power versus load resistance hold for any such potential, and under mild stated conditions a linear harvester with suitable stiffness reaches the bound. Nonlinear stiffness can still help when implementation constraints fix or forbid the linear stiffness one wants. Short quote: "not fundamentally better than linear ones".

**Model and conventions (as read).**
- State equations:
  - Eq. (1) ẋ = v.
  - Eq. (2) m v̇ = −U′(x) − Γq/C − b v + m a.
  - Eq. (3) −R q̇ = R I = V = Γx/C + q/C.
- Symbols:
  - m proof mass; x relative displacement; U open-circuit internal energy; q charge.
  - b mechanical damping coefficient; R load; C clamped capacitance; Γ transduction factor.
  - Device-frame acceleration ÿ = −a.
- **a is "Gaussian white noise with a two-sided spectral density Sa".** The paper does not say per Hz or per rad/s.
  - Its own Eq. (4) fixes the scaling: the weak-coupling stationary density is W ∝ exp(−b v²/(m Sa) − 2bU/(m² Sa)), so ⟨v²⟩₀ = m Sa/(2b).
  - A Langevin equation v̇ = −(b/m)v + a with ⟨a(t)a(t′)⟩ = D δ(t−t′) gives ⟨v²⟩ = D m/(2b). So **Sa = D = the delta-function strength of ⟨a(t)a(t′)⟩ = Sa δ(t−t′)** (derived by the scout from Eq. 4).
  - That number is the same whether the two-sided density is taken per Hz or per rad/s (when the density is the Fourier transform of the autocorrelation). It is half the one-sided density G in (m/s²)²/Hz, G = 2 Sa (derived by the scout).
- Electrical time scale τ = RC. Weak-coupling limit Γ → 0.
- k² = Γ²/(KC) ≤ 1 is the electromechanical coupling factor; K is the open-circuit stiffness; Qm is the open-circuit quality factor.

**Equations we may use (Halvorsen's numbering).**
- Mean power: P = ⟨V²⟩/R.
- **Input power**: Pin = m Sa/2. Efficiency η = 2P/(m Sa). Power balance **(5)** P = m Sa/2 − b⟨v²⟩. Argument: Stratonovich integral m v∘da = m v da + m Sa dt/2, the Itô part having zero mean. The text says Pin is independent of U.
- Small-τ bound **(6)**: P ~ Γ²⟨v²⟩τ/C ≤ Γ²τ m Sa/(2bC). Valid for any U that admits a stationary distribution; output then independent of U.
- Large-τ **(7)**: P ~ Γ²⟨(x−⟨x⟩)²⟩/(τC). This is strongly U-dependent.
- Improved bounds:
  - **(10)** Pu1 = Γ²τ⟨v²⟩⟨(x−⟨x⟩)²⟩ / (C[⟨(x−⟨x⟩)²⟩ + τ²⟨v²⟩]).
  - **(11)** Pu2 = (m Sa/2)(Γ²τ/Cb) / (1 + Γ²τ/Cb + ωm²τ²).
  - **(12)** ωm² = ⟨v²⟩/⟨δx²⟩, the rms frequency of the displacement spectrum.
  - **(13)** at ωmτ = 1: Pu2,Opt = (m Sa Γ²/2Cb) / (2ωm + Γ²/Cb).
- **Exact linear optimum (from the 2008 paper, via 2013), Eq. (14):** PLin,Opt = (m Sa Γ²/2Cb) / (2ω0 + b/m + Γ²/Cb), with ω0 the open-circuit resonance. A linear device meets the bound when ω0 = ωm − b/2m.
- Realisability, **(15)**: ωm > b/2m + |Γ|/√(mC). This is the stability condition k² < 1.
- Weak-coupling bound **(17)**: Pu1 = Pu2 = (m Sa Γ² τ/2Cb)/(1 + ωm²τ²). Maximum m Sa Γ²/(4Cbωm) at τ = 1/ωm.
- Output power as the Laplace transform of the velocity autocorrelation **(16)**: P = (Γ²/C) K̃vv(1/τ).

**Consequences for "power independent of resonance frequency" (derived by the scout from Eq. 14 and the definitions k²Qm = Γ²/(ω0 C b), b/m = ω0/Qm):**
- η = P/Pin = k²Qm / (2 + 1/Qm + k²Qm).
  - The paper states "η → 1 as k²Qm → ∞".
  - Its example device with k²Qm ≈ 7.8 has η ≈ 0.79. My formula gives 7.8/9.8 ≈ 0.80 for large Qm, which agrees.
- So P → m Sa/2, independent of ω0 and of b, only in the strong-coupling or high-Q limit.
- At weak coupling P ≈ m Sa Γ²/(4 C b ω0) in the large-Q limit. It falls as ω0 rises, consistent with the paper's remark on the "monotonic frequency-behavior" of (14).

**Numbers and checks the paper gives.**
- Symmetric quartic U = A x²/2 + B x⁴/4, weak coupling, γ* = b/(mωs) = 0.01, B* = 1.
  - The bound grossly overestimates the power of a bistable device at small Sa* (Sa* = 10⁻⁴: ωm* = 0.101, rare interwell jumps).
  - Maximum power over load is at negative A* (bistable). But a linear device with ω0 = ωm − b/2m gives more. For small negative and all positive A*, linear devices with the same stiffness as the nonlinear one at its minimum give more.
- Asymmetric cubic-quartic U = ½Kx² + (Kξ/(√2 l)) x³ + (K/(4l²)) x⁴ (Eq. 18), |ξ| < 1:
  - With linear stiffness held at K (ω0 = ωs), softening potentials (ξ ≠ 0) beat the linear device over a range of Sa*, even at fixed load τ* = 1.
  - A linear device with ω0 = 0.5 ωs gives P*/(Sa*Γ*²) ≈ 50, above all the nonlinear cases at all Sa* in Fig. 5.
  - Conclusion drawn: "the motivation for utilizing nonlinear stiffness is rather one of necessity than one of advantage".

**Conditions of validity.**
- Stationary Gaussian white-noise base acceleration along the sensing axis.
- One mechanical coordinate x with viscous damping b and a conservative potential U that permits a stationary distribution.
- Linear transducer, RC load.
- Mild restriction (15).
- Exact statements for linear harvesters are exact. Nonlinear statements are bounds (rigorous), and numbers are weak-coupling Kramers-equation results.

**What it says about coloured noise.**
- White noise is a good model when the correlation time is short compared with the system's times.
- Effects that depend on a finite correlation time, "albeit interesting, necessarily rely" on a limited bandwidth.
- The conclusion does not exclude advantages for nonlinear stiffness for vibrations significantly different from wide-band noise, "e.g. off-resonance, sufficiently band-limited vibrations".
- It does not treat coloured noise itself.

**What it does not establish.**
- Nothing on parametric or centrifugal forcing, rotating frames, two-degree-of-freedom or chaotic oscillators, or pendula.
- The bound's proof uses one coordinate x with a potential U(x). Extending it to a double pendulum is **a scout's inference, not in the paper**: the power balance P = Pin − (dissipated) with Pin = m Sa/2 looks general, but the paper does not do it.
- No claim that a linear device is realisable when (15) fails (strong coupling, little damping).
- No comparison at equal volume or equal stroke. A confining stroke limit is what makes nonlinearity attractive (Green, section 2).

---

## 2. Green, Worden, Atallah, Sims (2012), J. Sound Vib. 331(20):4504-4517. **[FULL]**

- "The benefits of Duffing-type nonlinearities and electrical optimisation of a mono-stable energy harvester under white Gaussian excitations". DOI 10.1016/j.jsv.2012.04.035.
- Author's version (White Rose): <https://eprints.whiterose.ac.uk/74419/1/WRRO_74419.pdf>. It is a preprint submitted 20 June 2012; the published text may differ in small ways.

**What it establishes (paraphrase).**
- Single-degree-of-freedom electromagnetic harvester with cubic spring, white base acceleration. The exact stationary Fokker-Planck solution factorises, p(z, ż) = p(z)·p(ż). The velocity density does not depend on the cubic coefficient β or on the linear stiffness ωn².
- So mean power cannot be raised by a Duffing term. The benefit is smaller displacement at the same power, which allows a smaller device. Short quote: "cannot be used to improve power output".
- Equivalent linearisation and Monte Carlo agree on the displacement.
- The optimum load resistance differs from impedance matching. Experiment supports this.

**Model and conventions (as read).**
- Eq. (7): z̈ + (2ωnζ + γ/m) ż + ωn² z + β z³ = −ÿ, with γ = α²/(RL + RC), α = dΦ/dz (flux gradient).
- **White-noise convention:** Eq. (11) E[ÿ(t1)ÿ(t2)] = (S/2) δ(t1−t2). So the delta strength is S/2.
  - Compare Halvorsen: Sa = S/2, so G (one-sided, per Hz) = 2 Sa = S (derived by the scout).
  - Their figures use (m/s²)²/Hz, consistent with S being one-sided per Hz. The text labels it "Watts/Hz" in one place, which looks like a units slip.
- Joint density **(14)**, with η = 2ωnζ + γ/m:
  - p = A1 exp(−(4η/S)(ωn² z1²/2 + β z1⁴/4)) × A2 exp(−2η z2²/S).
  - So ⟨ż²⟩ = S/(4η) (derived by the scout from the Gaussian factor; matches their Eq. 31).
  - Eq. (31): E[z2²] = S/(2(4ζωn + 2γ/m)).
- **Mean load power (32):** E[Pload] = S RL α² / (2(4ζωn + 2γ/m)(RL + RC)²).
- Consistency check (derived by the scout): total dissipated power = (m η)(S/(4η)) = m S/4 = m Sa/2, equal to Halvorsen's Pin.
- Optimum load, Eq. (38)-(39): the quadratic (−2ζωn m)RL² + (2ζωn m RC² + α² RC) = 0.
  - Simplified (derived by the scout): RL,opt = RC √(1 + α²/(RC·c)), with c = 2ζωn m the mechanical damping coefficient.
  - With the paper's identified numbers (RC = 0.48 Ω, α = 0.1992 Wb/m, c = 0.08863 N s/m) this gives 0.667 Ω. The paper reports 0.67 Ω.
- Displacement variance with Duffing term, Eq. (19)-(20), in terms of parabolic-cylinder functions. Equivalent stiffness (30): keq = [θk + √(θ²k² + 3 k3 S m² θ)]/(2θ), θ = c + α²/(RL + RC).

**Numbers we may quote.**
- Test rig: m = 0.02358 kg, c = 0.08863 N s/m, Coulomb Fd = 0.02488 N, k = 60.034 N/m, k3 = 70565 N/m³ (Table 1); 83 turns; α = 0.1992 Wb/m; natural frequency about 8 Hz; flat acceleration PSD 4-20 Hz; RMS base acceleration 1.9-2.3 m/s²; coil resistance 0.48 Ω.
- Friction (Coulomb damping) had to be added to the model to match the experiment.

**Conditions.** White noise only. Monostable potential. Inductance negligible. Viscous damping for the exact solution.

**What it does not establish.**
- Nothing on coloured noise. The authors list it as future work.
- Nothing on bistable devices (they point to Daqaq 2011).
- It reports that Daqaq (Nonlinear Dyn. 69:1063, 2012; ref [25]) showed Duffing nonlinearity can hurt when the electrical and mechanical time constants are close. That is second-hand.
- Nothing on chaos or pendula.

---

## 3. Daqaq, M. F. (2011), J. Sound Vib. 330(11):2554-2564. **[ABSTRACT + introduction + section snippets; full text paywalled]**

- "Transduction of a bistable inductive generator driven by white and exponentially correlated Gaussian noise". DOI 10.1016/j.jsv.2010.12.005.
- Page: <https://www.sciencedirect.com/science/article/abs/pii/S0022460X10007984>. I read the ScienceDirect preview (abstract, introduction, three section snippets, reference list) through a web-capture tool. I did not read the body or any equations beyond the snippets.

**What it establishes (abstract, paraphrase).**
- Symmetric bistable potential, Ornstein-Uhlenbeck (exponentially correlated) noise and white noise.
- White limit: exact stationary Fokker-Planck solution. The expected output power is independent of the potential shape, so bistability gives no gain over a traditional single-well linear resonant generator. Short quote: "bistabilities in the potential do not provide any enhancement".
- Exponentially correlated noise: an approximate expression for mean power that depends on potential shape, design parameters, noise bandwidth and intensity. An optimal potential shape maximises power, with an optimal escape frequency between wells that stays constant as the noise intensity varies.
- The introduction says monostable Duffing generators under random excitation were found to have a detrimental effect on mean power, "especially pronounced under colored excitations with small bandwidths". This is the author's literature summary, not his result.

**Model and conventions (snippets).**
- m ẍ + c ẋ + U*′(x) = −α i − m ẍb, α ẋ = i R.
- U*(x) = −½a*x² + ¼b*x⁴.
- c_eff = (1/m)(c + α²/R).
- ξ(t) = −ẍb.
- **⟨ξ(t)ξ(t0)⟩ = 2S δ(t−t0).** So the delta strength is 2S. Compared with Halvorsen: S_Daqaq = Sa/2 (derived by the scout).
- Inductance neglected.

**What it does not establish (from the abstract).**
- The abstract does not say whether the optimal bistable potential beats an optimally tuned linear harvester under coloured noise at equal mass and damping. It only says there is an optimum within the bistable family. Read the full text before using any coloured-noise claim.

### 3.1 Daqaq, Nonlinear Dyn. 69:1063-1079 (2012), "On intentional introduction of stiffness nonlinearities for energy harvesting under white Gaussian excitations" (DOI 10.1007/s11071-012-0327-0). **[NOT OPENED]**
- Known only through Green's remark above and Crossref metadata.

### 3.2 Daqaq, chapter "Role of Stiffness Nonlinearities in the Transduction of Energy Harvesters under White Gaussian Excitations" (Springer, 2013; DOI 10.1007/978-1-4614-5705-3_7). **[NOT OPENED]**
- A search-engine summary says a Springer chapter reports that a monostable Duffing harvester can never outperform its linear counterpart, and a bistable one only under specific conditions. The summary did not name the author or conditions. Treat as a lead.

### 3.3 Review lead (listed on the ScienceDirect page, **[NOT OPENED]**)
- Daqaq, Masana, Erturk, Quinn, "On the role of nonlinearities in vibratory energy harvesting: a critical review and discussion", Appl. Mech. Rev. 66, 040801 (2014). This is the natural next read for "can nonlinearity beat linear".

---

## 4. Rotating structures: pendulum and centrifugally tuned harvesters

### 4.1 Gu, L. and Livermore, C. (2010), Appl. Phys. Lett. 97, 081904, "Passive self-tuning energy harvester for extracting energy from rotational motion". **[ABSTRACT only]**
- DOI 10.1063/1.3481689 (Crossref; abstract text from Crossref; paper not opened). The patent US 2014/0035438 shares the title (Justia page, not read).
- **Abstract content (paraphrase):** a radially oriented piezoelectric cantilever carries tensile stress from centrifugal force. This tunes its resonance. Because centrifugal force goes as the square of the driving frequency, the resonance of an optimised harvester can track and match the driving frequency over a wide range. An analytical model and a prototype that does much better than an untuned one are described.
- Relevance: a beam whose stiffness is tuned by Ω², not a pendulum. It is the same Ω² scaling that gives a pendulum its order tuning (section 5).
- **Not established here:** gravity-driven once-per-turn forcing; random excitation; any comparison with nonlinear or chaotic devices. I cannot say what the paper's excitation is beyond "rotational vibration applications".

### 4.2 Cai, Q. and Zhu, S. (2024), "Nonlinear double-mass pendulum for vibration-based energy harvesting", Nonlinear Dyn. 112:5109-5128. **[FULL]**
- DOI 10.1007/s11071-023-09236-6 (open access, CC BY 4.0): <https://link.springer.com/article/10.1007/s11071-023-09236-6>.

**What it establishes (paraphrase).**
- The device (DMP) is a single-degree-of-freedom pendulum with two masses on one bar. The authors state it is "completely different" from a traditional double pendulum (which is two-degree-of-freedom).
- Undamped small-amplitude frequency (Eq. 2), a = l2/l1: ω0 = √(g(1−a)/(l1(1+a²))). Energy barrier **(31)** Edmp = 2 mm g l1 (1−a).
- Damped horizontal-base equation **(18)**, dimensionless **(21)**: θ̃″ + 2ξ θ̃′ + sin θ̃ = γ cos(κ s) cos θ̃, with γ = Ag/g and κ = ω/ω0. This is a periodically forced damped pendulum.
- Metric is the **gross output power** **(29)**: Pd = average of ct (l1² + l2²) θ̇², the power dissipated in the damper. Electrical efficiency was explicitly left out.
- Numerics: RK4, step 0.002 s. Bifurcation sweeps in γ show alternating single-period, multiple-period and chaotic behaviour. Rolling (swing-over) motion, periodic or chaotic, gives a "power leap" and a broader bandwidth than oscillation at the same γ. Chaotic rolling is above the leap level; initial conditions matter for γ > 1.
- Short quote: "rotating motion, regardless of chaotic or periodic rolling motions, improves".
- Parameter-space plots: the rolling threshold falls with lower damping and with excitation frequency slightly below the natural frequency. Example in the paper: for damping ratio 3.96%, rotation starts at about γ = 0.8 when κ = 0.78.
- Prototype: mm = 0.947 kg (each of two masses), l1 = 0.125 m, l2 = 0.035-0.125 m, ct = 1.1 N s/m total damping, inherent damping ratio 0.002. A shake table was used; the estimated gross output was about 0.6 W at κ ≈ 0.9, γ ≈ 0.28 (high-damping case).
- **Random excitation (their section 8):** white noise 0-500 Hz, Monte Carlo, a = 0.36. Gross power rises with RMS excitation. It is "considerably lower" than under resonant harmonic input. There is no linear or single-pendulum baseline.

**Second-hand statements in its introduction (not verified):**
- Kumar et al. [26], double-pendulum harvester under base excitation: they "claimed that the pendulum that exhibited chaotic motions could considerably increase the harvested power".
- Malaji & Ali [27]: two spring-coupled simple pendula improve magnitude and bandwidth (experiment).
- Dai [24]: a rotary pendulum with two sector masses has a 3 dB bandwidth of 3.2 Hz at 0.5 g RMS.
- Marszal et al. [25]: a 2:1-resonance simple pendulum is more efficient for shorter reduced length.
- Abbas Hassan et al. [23]: a self-tuning variable-length pendulum, tunable 0.47-0.68 Hz.
- Yurchenko & Alevras [33]: N-mass pendulum and a parametric rotating pendulum under realistic wave profiles.
- Daqaq et al. [40] (as cited): for a bistable beam with a buck circuit, charging efficiency under chaotic input was lower than under periodic input. Cai & Zhu say their result differs, probably because of rotation.

**What it does not establish (answers to "what do they actually compare").**
- Not equal mass: no baseline harvester of any kind.
- Not best damping: ct is fixed (1.1 N s/m); for the parameter plots only ξ is varied by case, never optimised.
- Excitation: harmonic horizontal base shaking (main result); one white-noise run.
- "Power" is the gross damper power, not electrical power. At fixed ct a larger angular velocity raises it by construction.
- The comparison is rolling versus oscillating motion of the same pendulum, and the "power leap" near γ ≈ 1 is a jump to a high-amplitude branch. Nothing here ranks chaos against a tuned linear oscillator.
- The chaos here is a forced single-degree-of-freedom pendulum, not the autonomous chaos of a two-degree-of-freedom double pendulum.
- No rotor, no centrifugal field. Gravity is the restoring force.

### 4.3 Leads on rotating harvesters, all **[NOT OPENED]**
- Gunn et al. (2021), Appl. Energy 302:117..., "A self-tuned rotational vibration energy harvester for self-powered wireless sensing in powertrains". The Birmingham PDF returned 403; a Loughborough record exists.
- Deng, Jiang, Zhang, Zhou (2021), Energy 235:121414, "Design and modeling a frequency self-tuning vibration energy harvester for rotational applications" (Crossref metadata only).
- NWPU, Smart Mater. Struct. (2020), passively self-tuning nonlinear harvester in rotational motion (search-result title only).
- Search summaries (not sources) for double-pendulum harvesters, each unverified:
  - Beijing Institute of Technology: a double-pendulum electromagnetic harvester, peak average power about 1.45 mW and 1.3 mW under human running, with chaotic, periodic and rotating modes.
  - A 2015 Korean optimal-design thesis: a double pendulum "more efficient than single" for suitable parameters.
  - A HIT study of a magnetic chaotic pendulum piezoelectric harvester, comparing a cantilever, single-pendulum and double-pendulum harvester.
  - Auckland repository record 2292/47004 and PolyU 10397/104960 (titles not read).
- **Not found at all:** a paper on a pendulum harvester on a wind-turbine blade or a tyre that uses gravity once per turn. I found none by search and opened none.

---

## 5. Centrifugal pendulum absorbers (order tuning)

**None of the requested primary sources was opened** (Denman 1992; Shaw, Haddow and co-authors). Michigan State thesis PDFs (d.lib.msu.edu/etd/147 and /4599) returned HTTP 403 to curl, and a Firecrawl query on the first timed out at 60 s.

- Denman, H. H. (1992), "Tautochronic bifilar pendulum torsion absorbers for reciprocating engines", J. Sound Vib. 159(2):251-277. DOI 10.1016/0022-460x(92)90035-v. Crossref metadata only. **[NOT OPENED]**
- Borowski, Denman, Cronin, Shaw (1991), SAE 911876, crankshaft pendulum absorbers. The Crossref abstract says crank-mounted pendulums "can reduce torsional vibration by over 90%" in tests of a four-cylinder engine. **[ABSTRACT only]**

**Search-engine summaries naming patent text and MSU theses (secondary, unverified):**
- Absorbers use the centrifugal field instead of an elastic element and are tuned to an engine order, not a frequency.
- A patent gives a tautochronic ratio n²/(n²+1) for target order n.
- A patent cites Denman for circle, cycloid and epicycloid paths tuned to order M.
- Small-amplitude motion of the absorber mass is close to a circle of radius L about a centre C.

**Derived by the scout (not read in a source): the circular-path pendulum on a uniformly turning rotor.**
- Setup: pivot at distance R0 from the axis, arm length L, angle φ measured from the outward radial direction through the pivot, rotor speed Ω constant, no gravity.
- Lagrangian from the inertial-frame velocity: |v|² = R0²Ω² + L²(Ω+φ̇)² + 2R0LΩ(Ω+φ̇)cos φ.
- Result: **φ̈ + (R0/L) Ω² sin φ = 0.** A pendulum in an effective gravity g_eff = Ω² R0, so the small-amplitude angular frequency is Ω√(R0/L) and the order is **n = √(R0/L)**.
- This matches the "n = sqrt(R0/L) type" relation in the brief. I did not find it printed in an opened source. Check against Denman and Shaw before quoting it as literature.
- With gravity on a vertical-plane rotor (wind-turbine blade), the dimensionless number that decides whether the once-per-turn gravity term matters is g/(Ω²R0). A sketch of that term is still to be derived; I have not done it.

**Wind-turbine-blade pendulum absorbers:** none opened; none confirmed by search.

---

## 6. Linear response of chaotic systems

### 6.1 Ruelle, D. (2009), "A review of linear response theory for general differentiable dynamical systems", Nonlinearity 22:855. **[FULL]**
- Read arXiv:0901.0484v1 [nlin.CD], 5 Jan 2009: <https://arxiv.org/abs/0901.0484>. The numbering in the published version may differ.
- Ruelle (1998) Phys. Lett. A 245:220, "General linear response formula in statistical mechanics, and the fluctuation-dissipation theorem far from equilibrium": **[NOT OPENED]**. The 2009 review cites it (ref [39]) for the effect of kicking the system in the stable direction. Crossref confirms DOI 10.1016/s0375-9601(98)00419-8.
- **Warning about my first attempt:** two arXiv numbers I tried for the 1998 paper and the review (chao-dyn/9712017 and 0804.2587) were unrelated papers (a recurrence-quantification paper and a finite-element optics paper). I read their text, discarded the files, and use nothing from them.

**What it establishes (paraphrase).**
- Setting: smooth flow dx/dt = X(x) or map f on a compact manifold, perturbed by dx/dt = X + X_t (Eq. 0.1 and after).
- A physically observed steady state is identified with an **SRB measure** ρ, whose time-average property is Eq. (1.1): ρ(A) = lim (1/T)∫0^T dt ∫ ℓ(dx) A(f^t x), for ℓ absolutely continuous. Conditions: ergodic, and (maps) no zero Lyapunov exponent, (flows) one zero exponent along the flow.
- **Linear response is a property of the dynamics, not of the observable.** Informal derivation: δρ(A) = Σ_{n≥0} ∫ρ(dx) X(x)·∇(A∘fⁿ) (2.2). Susceptibility Ψ(λ) (2.3) in discrete time and κ̂(ω) (2.4) in continuous time. The sum over n ≥ 0 plays the role of causality.
- **Uniformly hyperbolic case (Axiom A attractor; C³ diffeomorphism or C³ vector field; A of class C²; mixing for maps).** The map a → ρ_a(A) is differentiable (for flows, C¹) and equals the response formula. For flows, κ̂ is holomorphic for Im ω > 0 and extends meromorphically to Im ω > −Λ with no pole at ω = 0. Kramers-Kronig relations hold.
- **Fluctuation-dissipation relation: it survives only in modified form.** The response splits into a part along unstable (centre-unstable) directions, which is the Fourier transform of a time correlation function in the FDT sense, and a part along stable directions, which describes oscillations around the attractor and is not a spontaneous-fluctuation correlation. At an equilibrium state (absolutely continuous ρ) the usual FDT holds, Eq. (2.5), the response being a correlation function of the unperturbed system. Short quote from the abstract: "survives in a modified form".
- **Outside uniform hyperbolicity.** For unimodal maps the dependence of ρ on the map can be (mildly) non-differentiable, and the susceptibility can have singularities in the upper half-plane (an "active" steady state that can give energy to the outside). Linear response can fail or be hard to see. Evidence is for Misiurewicz-type maps and Hénon numerics (Cessac) and not a proof. The Lorenz system seems, in numerical studies cited, to behave like a uniformly hyperbolic system for linear response (Lucarini; a "mathematical study would be very desirable").
- SRB states are stable under small stochastic perturbations (stated in passing).

**What it does not establish.**
- Nothing about energy harvesting, power, or comparison with a linear oscillator.
- No statement that a damped, forced double pendulum on a rotor is uniformly hyperbolic or an SRB system. Typical physical chaotic systems are not uniformly hyperbolic.
- Strictly a statement about small perturbations of deterministic dynamics. Turbulent forcing is a stochastic input that is not small.
- Whether a response formula holds for a stationary mean power as a function of the load (damping) parameter is then a question to test numerically, not to quote.

---

## 7. Convention table (for the page; mapping derived by the scout)

| Source | Noise statement | Delta strength D in ⟨a(t)a(t′)⟩ = D δ | One-sided PSD G, (m/s²)²/Hz |
|---|---|---|---|
| Halvorsen 2013 | two-sided spectral density Sa | Sa | 2 Sa |
| Green et al. 2012 | Eq. (11): ⟨ÿÿ⟩ = (S/2) δ | S/2 | S |
| Daqaq 2011 (snippet) | ⟨ξξ⟩ = 2S δ | 2S | 4S |

Mean input power at proof mass m (Halvorsen): Pin = m Sa/2 = m G/4. Worked illustration (derived by the scout): m = 1 kg and G = 1 (m/s²)²/Hz give Pin = 0.25 W.

---

## 8. Open questions

1. **Halvorsen 2008 full text.** Confirm the exact formula, the spectral-density convention, and whether the "independent of resonance frequency" statement is the high-k²Qm limit. Until read, state it with the qualification in 1.2.
2. **Rotor-frame spectrum.** Turbulence seen from a turning blade is not white. I read no source on its spectrum (peaks near multiples of the rotor frequency are what I would look for). Without it the white-noise bound is the wrong comparison for the rotor, and Halvorsen's own text names band-limited input as the case where nonlinearity might win.
3. **Does the power-balance argument carry over?** Halvorsen's Pin = m Sa/2 argument is for additive base acceleration along one coordinate. A pendulum on a turning rotor feels the forcing through centrifugal and Coriolis terms, partly parametric. A double pendulum has two coordinates. We need our own derivation or a source.
4. **Coloured noise and the best linear baseline.** Daqaq 2011 full text: with exponentially correlated noise, does the optimal bistable potential beat the best tuned linear harvester at equal mass and damping, and by how much? Also Daqaq Nonlinear Dyn. 2012 and the 2014 Appl. Mech. Rev. review.
5. **Double-pendulum claims.** Get Kumar et al. and the BIT, Korean and HIT papers; for each record: equal mass? best damping per device? excitation (harmonic, random, human)? metric (gross damper power or electrical)? Cai & Zhu's own lines (chaotic rolling above oscillation) need a linear or single-pendulum baseline at equal mass and optimised damping before they say anything about chaos.
6. **Order tuning and CPVA sources.** Obtain Denman 1992 and Shaw's group papers for n = √(R0/L), the tautochronic ratio, and path families. Check my derived φ̈ + (R0/L)Ω² sin φ = 0. Find any work on pendulum absorbers or harvesters on wind-turbine blades.
7. **Gravity once per turn.** Find the source for harvesters on blades or tyres that use gravity as the 1-per-turn drive. Gu & Livermore full text, Gunn 2021 and Deng 2021 are the nearest leads. The size of g/(Ω²R0) for a real blade is for the study to compute; I have no source numbers.
8. **Ruelle 1998 text**, and a check on whether any numerical response study exists for dissipative forced pendula (Lorenz-like, Lucarini-style tests). Without it, "chaos has a linear response" is a theorem only for uniformly hyperbolic systems.
9. **Stroke limits.** Halvorsen and Green both note that nonlinearity can win when stroke or stiffness is constrained. Is a rotor pendulum's range (angle limit, blade length) such a constraint? Not answered by any source.

## 9. Access log (what failed)

- IEEE (Halvorsen 2008), AIP (Gu & Livermore), ScienceDirect body text, Springer Nonlinear Dyn. 69, Birmingham PDF (403), MSU thesis PDFs (403), USN open-archive PDF (HTML stub): not read.
- OpenAlex API answered 429 (credits exhausted); Semantic Scholar answered 429. Crossref worked (metadata and some abstracts).
- Downloaded and read (kept in the scratch folder): `halvorsen2013_arxiv.pdf/.txt`, `green2012_wrro.pdf/.txt`, `ruelle2009_arxiv0901.0484.pdf` and `ruelle2009.txt`, `springer_dp2023.pdf/.txt`.
