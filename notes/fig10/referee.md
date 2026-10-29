# Fig. 10 · referee report (blind reading)

Page: `public/simulations/wind-turbine.html`, the lecture note "Wind turbine control: catching energy from a wind you cannot
choose". Read as it renders: built with `OUT_DIR=/tmp/fig10-ref-dist npm run build`, served by a small Node static
server, opened in headless Chromium (Playwright) at 1440 × 900, all folds opened with *Expand all*. The page changed during the
reading (equations (3) and (10) were reflowed). This report is on the current build: I rebuilt, extracted the text again and
diffed it against the first reading. Only those two displays had changed. No KaTeX errors, no console errors, and no `\(` left
unrendered.

Screenshots, one per section with all folds open: `notes/fig10/shots/ref-00-head.png`, `ref-01-p-wind.png` … `ref-10-p-limits.png`,
and `ref-06-eq8-at-1600.png`.

Kinds of finding:
- **(A)** a real obstacle: the reader gets lost, a step is skipped, a symbol is used before it is defined, a claim is wrong or
  unsupported, or a needed physical picture is missing. Only (A) items count toward a verdict.
- **(B)** taste, plus small rendering defects that do not stop the reader.
- **(C)** overloaded: the passage is longer or heavier than its point needs.

## What I checked by measuring

- **Numbers in sections 1–6, recomputed from the note's own formulas.** All correct:
  - πR² = 5027 m². 15 rpm = 1.571 rad/s, so ωR = 62.8 m/s.
  - P_wind = 1.576 MW at 8 m/s and 4.098 MW at 11 m/s.
  - Fit (5): the maximum is 0.48001 at λ = 8.100, and the curve crosses zero at λ = 13.40.
  - The c₆λᵢ variant peaks at 0.5023 at λ = 8.245.
  - The tip inflow angle is atan(1/8.1) = 7.04°.
  - K_opt = 1.780 × 10⁵ N m s², and the relaxation time is 4.62 s.
  - c_p/λ³ rises between λ = 2.44 and 4.28. Below λ_opt it never drops to its value at λ_opt.
  - ∂τ_aero/∂ω = −2.480 × 10⁵ N m s, K_p = 3.592 × 10⁶ N m s, K_i = 1.44 × 10⁶ N m.
  - The overshoot for ζ = 0.8 is 1.5 %.
  - After the step: λ = 6.61, c_p = 0.427, and 18.4 rpm puts λ back at 8.1.
- **The table in section 7, driven through the page's own buttons and *Solve*.** All eight rows came out identical to the note
  (energy, mean power, rpm range, captured share). The generator torque stays between 32 kN m and 916 kN m in all eight runs,
  so "none of the eight runs of section 7 reaches a limit" is true.
- **The convergence claim in section 8.** I re-ran the page's own solver with h = 5, 10 and 20 ms (copies of the page with only
  `H` and `EVERY` changed, so the stored rows fall at the same times):
  - max |Δrpm| between 10 and 5 ms is 2.03 × 10⁻¹¹ rpm;
  - max |Δrpm| between 20 and 10 ms is 3.26 × 10⁻¹⁰ rpm;
  - the ratio is 16.03, as the note says;
  - the energy balance is 8.2 × 10⁻¹³.
- **Further reading.**
  - The Heier (Library of Congress) and Shirzadeh et al. (WES) links return 200.
  - The two Wiley DOIs resolve at doi.org to the right books. onlinelibrary.wiley.com answers a script with 403 (bot block), and
    Crossref confirms the titles and years.
  - I read Shirzadeh et al., eq. (4): it is the IEC extreme operating gust, U(t) = U_hub − 0.37 U_gust sin(3πt/T)(1 − cos 2πt/T).
    The page's Gust wind uses exactly this shape, with T = 10.5 s.
- **Display maths overflow (scrollWidth > clientWidth).** At 1280 and 1440 px nothing overflows any more. In my first reading,
  (3) was cut off by 76 px and (10) by 31 px; the reflow fixed both. At 1600 px, (8) still overflows by 16 px.

---

## Abstract

Clear. Nothing to report.

## 1 · From wind to electricity

**(A)**
1. **Figure 1 draws the tip speed pointing along the wind, but the caption says the tips move across it.** The caption reads:
   "The blade tips move across the wind at \(\omega R\), several times faster than the wind itself."
   - The SVG arrow labelled ωR is horizontal (`x1=380 → x2=440` at `y=70`). It points downstream, parallel to the wind arrows and
     the same way.
   - It is also shorter (60 px) than the wind arrows (80 px plus the head), although the tip should move about 8 times faster.
   - So the only picture of the tip velocity shows a tip moving *with* the wind, and *slower* than it.
   - Section 4 depends on the opposite picture: "moves across the wind at \(\omega r\), so it meets the air coming from an angle
     whose tangent is \(v/(\omega r)\)". A reader who trusts the figure adds the two speeds as parallel arrows, and the 7° angle
     makes no sense.
   - Smallest fix: draw the tip velocity in the plane of the disc. For example, a ⊙ (out of the page) at the top tip labelled
     "ωR, out of the page", or a small front-view inset with a tangential arrow. Keep the caption.

**(B)**
- "nacelle" is used without a word of explanation (the housing on top of the tower).

**(C)** None.

**Verdict: needs work** (one figure fix; the prose is clear and should stay as it is).

## 2 · The power in the wind

**(A)**
1. **Equation (2) introduces torque and the rule P = τω with no words.** The sentence is: "A rotor takes a share \(c_p\), the power
   coefficient, of this flux:", and then (2) also gives \(\tau_\text{aero} = P_\text{aero}/\omega\).
   - The symbol τ_aero appears here for the first time. It is never called the torque the wind exerts on the rotor.
   - The step "power = torque × angular speed" is used without comment.
   - This one relation is the bridge from the power story (sections 2–4) to the torque story (sections 5–6), so the whole
     control part rests on it. A school student meets τ = P/ω cold. The meaning only becomes clear in section 5 ("Two torques
     act: the wind's…").
   - Smallest fix, one clause: "…and, since power is torque times angular speed (as power is force times speed for a push), the
     torque the wind puts on the rotor is τ_aero = P_aero/ω."

**(B)** None.

**(C)** None.

**Verdict: needs work** (one clause). The derivation of (1) and the "eight times the power" paragraph are excellent; leave them.

## 3 · The Betz limit ★

**(A)** None in the current build. In the first reading, (3) overflowed its box at 1440 px, which cut off the square of
"4a(1−a)²" and hid the number (3). The reflow onto two aligned lines fixed this: measured, there is no overflow at 1280 or 1440 px.

**(B)**
- **The momentum step has an unstated assumption.** "The force on the disc, \(\Delta p\,A\), must equal the momentum the air loses
  per second" assumes the pressure on the stream tube's curved sides gives no net push along the flow. This is the textbook
  assumption, and a graduate may notice it is unstated. A parenthesis would cover it.
- **The box says slightly more than the derivation.** "No rotor in open air can turn more than 59.3 % of the power flowing through
  its disc into shaft power". In (3) the reference is ½ρAv³, the power that would cross the disc area if the rotor were absent.
  The flow actually through the disc is smaller.
- Lanchester (1915) and Joukowsky (1920) reached the same limit. Naming only Betz is fine for this audience.

**(C)** None.

**Verdict: clear.**

## 4 · Tip-speed ratio

**(A)** None. The physical argument is good: the angle of attack, and why only the ratio matters. The fit and its numbers are
correct.

**(B)**
- "with the blades at zero pitch": the word "pitch" is explained only in section 7.
- **c₃ is missing from the list of constants.** Equation (5) lists c₁, c₂, c₄, c₅, c₆. A careful reader will look for c₃ (in
  Heier's fit it multiplies the pitch angle, zero here). Half a clause would settle it.
- **The 7° angle uses the free wind v.** Section 3 has just shown that the air at the disc moves at v(1−a). With a = 1/3 the angle
  at the tip would be about 4.7°. The similarity argument is unaffected; a graduate may notice.
- **A picture is missing where it would help.** The velocity triangle is given only in words, and Figure 1 (see 1-A) contradicts
  it. An everyday image would make it concrete: rain falling straight down seems to come from ahead when you run.

**(C)**
1. **The same point is stated three times in a row:**
   - "Between the two extremes lies a best ratio."
   - "The curve \(c_p(\lambda)\) used here is an empirical fit for one rotor; it has a maximum between its slow- and fast-running
     limits."
   - "This page uses an empirical fit to measured rotor curves due to Heier, with the blades at zero pitch,"

   The middle sentence repeats both of its neighbours and can go.
2. **The source-criticism sentence is a detour for most readers.** "One widely copied reproduction of the formula writes the last
   term as \(c_6\lambda_i\); that version peaks at 0.502 at \(\lambda = 8.25\) and does not match the quoted optimum, so the page
   uses \(c_6\lambda\)."
   - "the quoted optimum" points to nothing: the note never quotes an optimum from a source.
   - Keep it short, as a parenthesis that names where 0.48 at 8.1 is quoted, or move it to the Heier entry in Further reading.

**Verdict: clear** (with two (C) trims).

## 5 · The rotor's equation of motion

**(A)** None.

**(B)**
- **Figure 3 has two rendering defects.** They do not stop the reader, but they look broken:
  - The label "wind, set by the weather" runs under the *aerodynamics* box and reads "wind, set by the weath". Measured: the text
    ends at x = 155, the box starts at x = 144.
  - The box labels are literal `τ_aero(ω, v)` and `τ_gen(ω)`, with the underscore showing, where the text sets subscripts.
- **One step in the energy statement is silent.** "Multiplying (6) by \(\omega\) turns it into an energy statement" uses
  Jω dω/dt = d(½Jω²)/dt. A school student would welcome those five symbols.

**(C)** None.

**Verdict: clear.**

## 6 · Two controllers ★

**(A)** None. Both linearisations are complete, every step carries its meaning, and every number checks.

**(B)**
- ω_n and ζ_c appear in (10) before they are named. They are named a paragraph later ("Picking a natural frequency…"). In a ★
  section, and with the pointer to Fig. 9, the reader is not lost.
- The derivative is written \(dc_p/d\lambda\) here, with an italic d, but with an upright d (\(\mathrm{d}\)) elsewhere.
- At 1600 px, (8) overflows by 16 px and its number shows as "(8". See `ref-06-eq8-at-1600.png`.

**(C)**
1. **6.1, the global-stability argument is heavier than its point.** It runs from "The global one follows from the net torque…"
   to "…below, it is a property of this fit."
   - The point is that in steady wind the rotor finds its way back to λ_opt. The sentence that follows says it physically: "too
     slow and the wind wins, too fast and the brake wins".
   - The aside on non-monotonicity ("it rises between \(\lambda = 2.4\) and \(4.3\)") and "checked on a grid of step
     \(10^{-4}\)" add weight but no understanding.
   - In a ★ part this is tolerable. It is the heaviest passage of the note.
2. **6.2, the paragraph after (10) repeats earlier text and breaks the derivation.** It reads: "The proportional term reacts to the
   speed error now. A positive error means overspeed, so it asks for more generator braking; a negative error reduces braking.
   The integral term remembers an error that persists… Torque limits and changing wind can take the rotor outside that
   approximation."
   - It restates the sentence before (9): "brakes harder the faster the rotor turns, adding a term that remembers past errors".
   - It sits between (10) and the choice of gains, which interrupts the derivation.
   - It could shrink to its last sentence, or move to just after (9).

**Verdict: clear** (with two (C) trims).

## 7 · Same wind, two answers

**(A)** None. All eight rows of the table reproduce exactly from the page.

**(B)**
- **"captured share" is never defined.** In the store it is E_aero/E_wind (`captured_pct = 100 Ea / Ew`), the energy-weighted
  c_p. Five words in the table sentence would define it.
- **One slider has two names.** The text calls it "Δv" in the table sentence and "σ" in the rows and caption.
- "IEC shape" and "rated wind speed" are not explained.
- **Figure 4 shows something the text never names.** With *Hold speed*, the generator power swings far more than with *Follow
  the wind*: in follow-the-wind the rotor's inertia buffers the gusts, while at constant speed they pass straight to the
  generator. A reader will see this in the figure and may wonder about it. It is optional.

**(C)** None.

**Verdict: clear.**

## 8 · Solve first, then play

**(A)** None. Integrator, order, step, why it was chosen, where it fails and the measured error are all there, and all are true.
I re-measured the convergence and the energy balance; see above.

**(B)** None.

**(C)** None.

**Verdict: clear.**

## 9 · On screen

**(A)** None.

**(B)**
- **A pronoun has lost its noun.** "Only the wind arrow grows with the wind speed. They pass through the rotor unchanged;" — so
  "They" now points at the arrow, not the streaks. Moving the arrow sentence after the streak sentences fixes it.

**(C)** None. The pixel details (5 px per metre, 16/22 px dashes) are the house rule for saying where the drawing differs from the
store. They are not overload.

**Verdict: clear.**

## 10 · What the model leaves out (and 10.1 Further reading)

**(A)** None.

**(B)**
- **The next, more complete model is implied but not named** (standard, item 7). The bullets imply it: blade-element momentum
  theory with pitch control, dynamic inflow and a flexible drive train. One clause would name it, with Burton ch. 3.
- **The pendulum-harvester bullet is not a limit of the model.** It is a project idea inside a list of limits. Its physics is right:
  every joule harvested comes out of the rotor.
- "changes height by height" is an odd phrase for wind shear.
- **All four references are real and their links resolve.** See the measuring section above.

**(C)** None.

**Verdict: clear.**

---

## Summary

| Section | Verdict | (A) | (C) |
|---|---|---|---|
| 1 From wind to electricity | needs work | Fig. 1: ωR arrow points along the wind and is shorter than v | — |
| 2 The power in the wind | needs work | τ_aero = P_aero/ω: torque and P = τω used without a word | — |
| 3 The Betz limit ★ | clear | — (the clipping of (3) seen earlier is fixed) | — |
| 4 Tip-speed ratio | clear | — | the point stated three times; the c₆λᵢ provenance sentence |
| 5 Equation of motion | clear | — | — |
| 6 Two controllers ★ | clear | — | 6.1 global-stability paragraph; 6.2 paragraph after (10) |
| 7 Same wind, two answers | clear | — | — |
| 8 Solve first, then play | clear | — | — |
| 9 On screen | clear | — | — |
| 10 What the model leaves out | clear | — | — |

The note is clear and correct throughout. Two small (A) fixes are needed: one figure arrow and one clause. Everything else is
taste, or a trim of the passages listed under (C).
