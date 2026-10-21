# Fig. 10 · Wind turbine control · plan

Page `public/simulations/wind-turbine.html`, note L150–L537. Judged against notes/STANDARD.md §4 and Numa's verdicts:
a clear section is not touched; where work is needed, the smallest change. No new sections, figures, boxes or display
equations are planned, so equations (1)–(10) keep their numbers.

Measurements: `notes/fig10/cp_checks.cjs` (the page's `cp()` and `tauAero()` copied verbatim, run in Node) and
`notes/fig10/measure.cjs` (the built page in headless Chromium, read from `Sim.data.ds`; all eight controller–wind runs;
the same page served with only L555 changed to h = 5 ms and h = 20 ms for the step study). Output: `measure-out.json`.

## Verdicts

| § | Section | Verdict |
|---|---|---|
| Abstract | | clear, leave it |
| 1 | From wind to electricity | needs work: "the tips move at \(\omega R\)" uses \(\omega\) and \(R\) before either is named. |
| 2 | The power in the wind | needs work, one clause: "its mass is \(\rho A v\)" uses \(\rho\) before saying it is the air's density. The derivation of (1), (2) and the numbers (1.58 MW, 4.10 MW, measured) are clear. |
| 3 ★ | The Betz limit | needs work: "Bernoulli's equation, applied separately in front of and behind the disc, gives the pressure jump" is asserted; the two Bernoulli equations, why Bernoulli may not be used across the disc, why the speed is the same on both faces, and the cancellation of \(v - v_w\) are silent steps. The root \(a = 1\) of \(\mathrm dc_p/\mathrm da = 0\) is dropped silently. Eq. (3), (4) and the box are right. |
| 4 | Tip-speed ratio | needs work, one sentence: "How large \(c_p\) is depends mainly on one number" is asserted; the angle-of-attack picture is there but not why it depends on \(\omega\) and \(v\) only through \(\lambda\). Numbers checked: \(c_{p,\max} = 0.4800\) at 8.100, variant 0.502 at 8.245 (prints as 8.25), zero at 13.40; Figure 2 caption 757 kW at 15.5 rpm. All right. |
| 5 | The rotor's equation of motion | clear, leave it |
| 6.1 ★ | Optimal-torque law | needs work: \(\omega_*\) is used without definition; "its slope at the equilibrium is \(-K_\text{opt}\omega_*\)" skips the step (power stationary at the peak, so \(\tau = P/\omega\) has slope \(-P/\omega_*^2\)). The net-torque expression uses \(v = \omega R/\lambda\) silently. Numbers checked: \(K_\text{opt} = 1.78\times10^5\), 4.62 s, rise of \(c_p/\lambda^3\) between 2.44 and 4.28, no sign violation on a \(10^{-4}\) grid. |
| 6.2 ★ | PI controller | needs work: \(\tau_0\) in (9) is never defined; the linearisation skips the step between (6)+(9) and (10) (the integro-differential equation before differentiating); "decays within a few seconds without ringing" is not quite right for \(\zeta_c = 0.8 < 1\). Gains checked: slope \(-2.48\times10^5\), \(K_p = 3.59\times10^6\), \(K_i = 1.44\times10^6\). |
| 7 | Same wind, two answers | needs work, two small items: \(\Delta v\) is used without a word on what it is; "the captured share drops from 0.48 to 0.44" mixes the instantaneous \(c_p\) after the step (0.427, measured) with the whole-run share (0.437). Figure 4 caption (1.30 m/s, 14.4–15.7 and 12.5–19.8 rpm) and all eight table rows reproduce exactly. |
| 8 | Solve first, then play | needs work: matches the code, but §4 item 5 asks why the step is good enough and what error to expect; neither is said. Energy balance 8.2 × 10⁻¹³ (measured) supports "about 10⁻¹²". |
| 9 | On screen | needs work, one clause: the rose \(P_\text{aero}\) curve on the power strip is drawn but not named in the note. Everything else matches the code. |
| 10 | What the model leaves out | clear, leave it |
| 10.1 | Further reading | needs work: none of the four items has a link. |

## Changes

1. §1: "a disc of radius \(R\) and area \(\pi R^2\)"; "15 turns per minute, an angular speed \(\omega = 1.57\) rad/s".
2. §2: "with \(\rho\) the density of air".
3. §3: write the two Bernoulli equations inline (in front, behind), say why not across, continuity at the thin disc,
   add them so \(p_0\) and the disc speed drop out; "dividing by \(v - v_w\)"; one clause on the root \(a = 1\).
4. §4: one sentence: a blade element at radius \(r\) meets the air at \(\tan\phi = v/(\omega r) = (R/r)/\lambda\), about 7° at
   the tip at \(\lambda = 8.1\) (computed: 7.04°), so the angles depend on \(\lambda\) alone.
5. §6.1: define \(\omega_* = \lambda_\text{opt} v/R\); give the slope step; "with \(v = \omega R/\lambda\) in (2)".
6. §6.2: define \(\tau_0 = \tau_\text{aero}(\omega_\text{ref}, v(0))\); write \(J\delta\dot\omega = (\partial\tau/\partial\omega - K_p)\delta\omega - K_i\int\delta\omega\,\mathrm dt'\)
   inline before "differentiating"; replace "without ringing" by the measured Step-run overshoot (0.40 rpm) and dip (0.01 rpm).
7. §7: gloss \(\Delta v\); "\(c_p\) drops from 0.48 to 0.43, which pulls the share of the whole run down to 0.44".
8. §8: three sentences in item 1: why 10 ms is small; h = 5 ms changes the stored rotor speed by at most 2 × 10⁻¹¹ rpm,
   h = 20 ms by 16 times as much (fourth order); torque limits make a corner where RK4 loses order; none of the eight runs
   reaches a limit.
9. §9: name the rose \(P_\text{aero}\) curve and what the gap between it and \(P_\text{gen}\) means (eq. 7).
10. §10.1: links to sources opened: Burton et al. doi:10.1002/9781119992714 (chapters 3 and 8 seen in the Wiley table of
    contents); Manwell et al. doi:10.1002/9781119994367 (first published 18 Dec 2009); Heier 1998: the book itself could
    not be opened; link the publisher's description at the Library of Congress (catdir.loc.gov, LCCN 98018157);
    Shirzadeh et al. doi:10.5194/wes-5-1755-2020 (equation (4), the EOG shape with T = 10.5 s, checked in the PDF).

Doc `docs/simulations/fig10-wind-turbine.md`: update the line counts and any line links my edits shift (the note lies
above the code, so every code link after L537 moves if the note gains lines; edits are kept on existing lines so it does not).
