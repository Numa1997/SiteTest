# Skeptic, Gate 1, contract L3 (elastic blade: sag and shaking), round 2

Re-read only what changed:
- the "Round 2: answers" section of `contract-L3.md`;
- `derive/L3_sag_static.py` and `L3_sag_static.json`;
- `portfolios-src/rotor-pendula/theory/04_shaking.src.html` §6.1–6.2;
- the matching entries of `numbers.json`.

`L3_sag_static.json` reproduces my round-1 numbers exactly: at 90 % the net change is +1.99 % with edgewise stiffness alone and +2.06 %
with the twist-projected stiffness.

## Major objections of round 1

| # | Objection | Judgement |
|---|---|---|
| M1 | sag depends on the shape; P1 sits on its line | **Answered.** The note now gives the spread across shape models: −0.4 to −0.3 %, −0.8 to +0.1 % and +0.5 to +2.1 % at 30, 60 and 90 %. It explains why the result depends on the shape (a difference of two large numbers). P1 is reported as sitting on its line at 90 %, not rescued. That is the honest outcome. |
| M2 | tuned rod: gravity's 1P stiffness modulation | **Answered by withdrawal.** Observable (c) and P3 are withdrawn. §6.2 states the ±G/2R = ±9.6 % frequency swing per turn, against a resonance 1–6 % wide. It says the gains "may be several times" too high, and that the tuned rod "is an idea these notes have not shown to work". The time-domain run is listed as open work. |
| M3 | predictions after the runs | **Answered for Gate 1.** A fresh numeric prediction is registered before any run: in a time-domain run with gravity kept whole (5 mm, ζ_e = 0.5 %, uniform Ω), the tuned rod's harvest will fall below half of the linear 19 mW. It is untested, so it must be run, and reported whichever way it comes out, before the tuned rod returns to any later gate. |

## Minor points still open (do not block the gate)

- n1. **§6.2 still calls the swing linear.** It says the tuned rod's 0.26 rad rms swing is "small enough for the linear model". Two
  things argue otherwise. The rod's amplitude detuning, Θ²/16 ≈ 0.5–1.5 % once the 0.2 rad gravity swing is added, is as wide as the
  resonance it relies on. And the linear swing should not be advertised as valid when the gain itself is withdrawn. Replace the phrase
  with "within the linear model".
- n2. **The tip sag is quoted from one shape only.** §6.1 gives "about {{n:sag_tip_cm}} = 47 cm at the tip". That is the modal value; the
  static integration gives 43–44 cm. Since the section now quotes a shape spread, quote the tip as 43–47 cm.
- n3. **Round-1 minors carried forward and acknowledged:** m2 (OpenFAST regression output for the shaking level not opened), m4
  (speed-wander averaging is quasi-static; give the wander's correlation time against the rod's settling time of about 40 s), m6
  (1P aerodynamic in-plane loads left out). They are acceptable as stated limits.

## Verdict: PASS

No fatal or major objection remains open. The sag is reported with its shape uncertainty, and the tuned rod is withdrawn rather than
claimed. The registered prediction must be tested before the tuned rod is used again.
