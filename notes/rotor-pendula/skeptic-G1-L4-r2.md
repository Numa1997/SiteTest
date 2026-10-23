# Skeptic, Gate 1, contract L4 (geared DC generator), round 2

Re-read only what changed:
- the "Round 2: answers" section of `contract-L4.md`;
- `derive/L4_sensitivity.py` and its log;
- `derive/L4_stick.py`, `L4_stick.log` and `L4_stick.json` (all 18 mountings);
- the new `L4_check_2000.json` and `L4_check_4000.json`;
- `portfolios-src/rotor-pendula/theory/05_watts.src.html` §7.2–7.5 and the summary list;
- the lines of `tools/make_numbers.py` that make the new numbers, and the matching entries of `numbers.json`.

I re-ran `python3 -I L4_converge.py`: **PASS, largest difference 0.27 %** across all 18 mountings, with the version-3 key format.

## Major objections of round 1

| # | Objection | Judgement |
|---|---|---|
| M1 | gearhead drag missing | **Answered.** Friction ×1/×2/×3 and η = 0.5 now run at all nine large-rotor mountings. The worst case (×2 and η = 0.5) gives 0.41 mW, 10.9× the sensor, so P1 holds, if barely. The jamming ratio is restated as scaling with 1/(friction multiple): 164 at the sheet value, 82 at twice. The drag itself stays unsourced. It is now an explicit range, not a silent zero. |
| M2 | voltage, brushes | **Answered as a stated limit.** §7.4 states the alternating, sub-volt, once-per-turn voltage. It says that conversion is unsolved and that the brushes need a test, and every margin is quoted "before the electronics". The summary list says "turning that slow, low voltage into a steady supply is the open problem." |
| M3 | backlash | **Answered.** Table 4 marks 2 mountings † (swing below the half play) and 7 mountings ‡ (swing under 6 × the half play). The text says the teeth may never engage there, and the headline numbers come from the large rotors only (swing ≥ 0.06 rad). |
| M4 | "never sticks" false | **Answered.** The claim is withdrawn. `L4_stick.py` measures the time stopped: 25–29 % of each turn on the large rotors. The band test has been rerun with the version-3 keys (10⁻³ against 3×10⁻⁴, 2000 against 4000 steps): 0.27 % at worst. So the smoothed model resolves the averages. |
| M5 | predictions after the runs | **Answered, narrowly.** P1 (≥ 10×) was written in round 1, before the sensitivity runs existed. Those runs could have broken it, and the closest case came within 9 %. That is a genuine test. P4 remains post hoc, and is labelled as such. |

## Minor points still open (fix in the notes; they do not block the gate)

- n1. **The voltage numbers are computed, not read back.** `make_numbers.py` takes the peak load voltage from a sinusoidal swing,
  k_e N Θ Ω·R_L/(R_c + R_L), which gives 88–326 mV. But the rod stops for a quarter of each turn and then moves faster. The measured peaks
  in `L4_stick.json` are **130–553 mV** on the large rotors (for example 138 mV against about 100 mV at 8 rpm 90 %, and 553 against
  339 mV at 8 rpm 30 %). Also, `Theta` in `L4_check` is max|θ|, which includes the mean lean. Quote the stored peaks from `L4_stick.json`
  (house rule: the display reads the store; it does not recompute).
- n2. **The rod's stops are not on the page.** §7.3 still begins "Suppose the rod still swings as θ = −Θ cos(φ − δ)". Add one sentence:
  on the large rotors the rod stands still about a quarter of every turn, so the describing function's sine is a rough picture, yet it
  matches the full equation within 9 %. A reader of the animation will see the stops.
- n3. **Chapter 0 overstates the sensor link.** `00_machine.src.html` line 13 says "Even if the electronics lose half of the power…" and
  "still deliver … mW to the wires, at least 47 times the need". It does not mention the 0.1–0.5 V alternating voltage or the brushes.
  Add the same qualifier as the summary list ("before the electronics; converting the slow, low voltage is the open problem").
- n4. **Cite maxon on the brushes.** §7.4 says the brushes "need a test". maxon's own support article ("Properties of brushed DC motor
  commutation systems") says graphite brushes are "not suited for small currents". That is a reason to name a precious-metal-brush
  alternative (RE 25 EB, or the Faulhaber 2232 SR from the dossier), not only a test.
- n5. **The jam ratios in §7.2 are not conditional.** The text calls 190, 246 and 492 "useless … on every rotor" and gives the jam
  ratio as 164. That is true at the catalogue friction. With an unknown gearhead drag the threshold can fall to about 82, which would put
  111 at risk. Say "at the catalogue friction".
- n6. **P3 now passes by 9 % against a 10 % line** (`df_gap_big` = 9; earlier runs gave 6.5 %). Fine, but note that it is close.

## Verdict: PASS

No fatal or major objection remains open. Fix n1–n5 in the lecture note before Gate 2.
