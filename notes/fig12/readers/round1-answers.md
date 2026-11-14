# Fig. 12 note, round 1: the answer to each mark

Marks: `round1-owner.md` (70), `round1-student.md` (95 counted), `round1-check.md` (13 wrong, 8 unverifiable).
Every mark was fixed in `notes/fig12/note/paper.html` and, where a number was involved, in `tools/fig12/kaggle/note_numbers.py`,
unless the answer below says otherwise. "O" = owner, "S" = student, "C" = checker row.

## Errors of fact (fixed first)
- O1 / abstract, 12.3, 12.10, 13: at 1.5 m/s the motor gives at most 11.25 N forward (supply limit), not 15 N. All four places
  now say so; the ratio road/motor is 7.3 and "about a fifth" became 0.14 (printed `motor_vs_road`).
- C N87–N89, O57, S86: the kerb's touch point is where `road_table` first lifts the axle, x = 1.437 m (printed `x_touch`),
  not 1.40 m. The early-current test now starts 4 ms before that; the speed rises to 1.51, falls to 1.23 m/s; the sudden loss is
  0.28 m/s, the first peak 11.1 mm (was 8.3). Figure 4's time zero moved accordingly; both ±15 N lines drawn; even ticks.
- C N114, S95: the first forward surges at the kerb are now read before 0.8 s (22.2, 21.2, 21.8, 25.4 mm); the text says the
  largest leans of Table 8 can come from the back-swing.
- C N75, O48: 11.3 now says the single bump leaves 7.1 mm with the head, just below the 7.6 mm that breaks the foam.
- C N111, O59: Figure 5 caption corrected ("by several millimetres at each bump, up to 13.9 mm").
- C N118, O23, S44: the key result and Problem 2 now use the printed ζ = 0.0055 and ω = 21.49 (8.5 s, 20.1 swings, 19.5 s).
- C N56, O44: the cost per simulated second is for the rides only, 43 to 48 s.
- C N76: Floquet search refined: Ω = 1.81 ω, 5.28 Hz.
- C M12: only the pressure solver's sums are double precision; the head sheet's are single. Text corrected.
- C M14: the table's leans were read after the run by the packing program; text corrected.
- C M15: 11.1 now says ring points beside the trusted columns are read half a cell further in.
- C E71, O28, S1: equations renumbered in order of appearance (old 23→27, 24–27→23–26, 31→36, 32–36→31–35); all references
  follow. Sources renumbered in order of first citation (O70).

## Missing physics and unexplained results
- S49 (section 6 never predicts the head's damping): new paragraph in 6.3 derives ζ_edge = Π/(2E_s ω) ∝ q^(-1/3) from Cantat's
  law; 0.62 at 1 mm, 0.36 at 5 mm. 11.2 compares it with the measured 0.425 at the fitted 2.3 mm swing: 0.47, 11 % above.
- O49, S81 (foam left on the five bumps below 7.6 mm): the stored surface shows the back wall rose 8.1 mm at 1.40 s while the
  front fell 5.8 mm; the surface is not a pure first mode. Said in 11.5.
- O60 (lean persists after the kerb): measured from the stored files: mean lean after 1.5 s is 0.2, −0.6, 1.8 and 2.5 mm
  (speed, preview, slosh, joint); the speed is back at 1.50 m/s, so it is not a steady acceleration; the head can hold about
  1 mm; the rest is stated as not traced.
- O55, S94 (which part of joint control works): no stored ride separates them; stated as an inference with its reasons (the
  cancellation current is below 0.016 A; the heave cannot pump; so the motor's regulator).
- O39, S62 (method's extra damping 0.0105 with APIC): 8.2 now says APIC removes the transfer loss, that the method keeps
  other losses (surface, cut cells, time stepping), measured in 11.2 and not traced to their sources.
- O51, S77 (3 % below the prediction): stated as not explained, with one candidate.
- O24 (bare surface's protein film): 5.4 now says a real film could add up to ζ_skin and the model leaves it out; listed as a limit.
- O17 (pitch): 3.1 says the model keeps the body from tipping, as in a guide; a real one-wheeled cart would need more.
- O47, S70, S71 (energy book not closed): 9 now says the heat D of the rest test was not stored, so (35) cannot be closed;
  the "lattice" claim was removed.
- O53: the box now says stout_jax.py is unchanged between versions 8 and 10 (checked with git diff 96e8a1d 58eea68).
- O35: 7.2 now says the five-bump road was tuned to the bare stout, and that the head detunes it.
- O11: 2 and 6.1 now say the head's wet bottom is near jamming.
- O32, S50: the wedge estimate is derived in one line (Culmann's plane: z = 4τ_y/(ρ_f g sin 2ϑ), lowest at 45°).
- O40, S66: the lagged-load instability is shown (error multiplied by −λ_h k each step).
- O15: Example 3.1's conclusion corrected: a steady 1.9 m/s² breaks the foam; added to Example 6.2 (no forward reference).
- O43: the two meanings of "drop" separated (left the glass and counted spilled; drawn and counted above the surface).
- O69, S97: the drop count is printed (at most 11 particles at a time).
- O58, S87: Figure 4 draws the delivered push dashed on top.
- O13, S20, S69: 2 explains 91.26 mL (flat disc) against 91.314 mL (the grid's open column areas, 0.06 % more).
- S82: Table 4's kerb row with head > bare explained (short hard push; β_h/ω close to β/ω₁₁).
- S73: 11.2 says why the first computed swings are below the undamped 5.0 mm.

## One symbol, one meaning
α → ϑ for inclinations (α only the ghost fraction); κ of 8.2 → k (κ only the edge drag); e^{jκx} → cos kx (no imaginary unit
beside the face index j); Φ of Van Loan → Γ; E (energy) → E_s; Z(z) → 𝒵(z); φ₁ → Υ; δ (Stokes) → δ_s; g_eff,z → g' (apparent
gravity, magnitude); Δv only the sudden change, δv the speed error; N_s → Y_s; sum to N → n_e; sample index k → [n];
noise window τ → T_w; variance σ² → V_y; Stephens's K → K_Λ; summation index k in 12.6 written out. (O21, O31, O34, O41, O42,
O61, S2–S12.)

## Definitions, steps, wording
- O4, S15, S16: LQR and skyhook glossed in 1. O5: tilt and lean introduced in 1. O6: "drops and lumps outside the glass".
- O7, S19: the two scale factors stated as separate; the base height printed. O8: "shear rate" wording. O9: "at room temperature".
- O10, S22: the drainage estimate is named as the project's own calculation, with its file, not a measurement.
- O12: "below it" ambiguity removed in passing. O14, S21: 426.6 mL × 1.007 g/mL shown.
- O16, S28: the full viscous term with μ∇(∇·u)/3 given. S29: "Effective gravity" made a sentence.
- O18, S34: the constant gh absorbed into C(t), said. O19, S33: Bernoulli step shown and wording fixed. S32: cylindrical Laplacian.
- S35: d[x²J₂]/dx = x²J₁ quoted with DLMF §10.6. O20, S37: "hardly notice" removed.
- O22: why the push is tuned to the bare swing, said. S31, S14: new Key result box "a sudden push" restates (12)–(13).
- S39, S40: x_∥ and Re defined. O26, S41: Figure 2 labels moved off the curves; minus signs. O27: 2δ_s means 14 %.
- S42: 0.5575 shown as its formula. S43: σ_wall ≈ σ_skin explained as a coincidence. S45: rounded parts given.
- O25: the lid is called the model's choice. O29: random against ordered packing. S47: "stiff surfaces" defined.
- S52: finite-time stop shown (v^(1/3) falls linearly). O30, S48: κ defined without grid columns.
- O33, S53: the sheet force derived from the stress on vertical planes. S51: why foam pushes on a free face. S54: yield result restated.
- O37: kerb crest curvature 24 mm < R_w stated; z_a defined (O62, S85). O38: 2.79 against 2.75 Hz explained.
- O36, S57: 343 ms (a measured value) replaced by the theory's head-loaded period. S58: the head's vertical momentum only affects F_z.
- S60: Table 2 inertia as 2.4 × 10⁻⁴. S56: "any point of its rim".
- O45: the explicit-step stability stated as a non-negative weight. S61: where the sinc² comes from. S64: "second order" defined.
- S65: the head-mass paragraph starred and restated plainly. S67: 0.68 is a fixed offset of the code. S68: CG not re-explained.
- O46, S13: scientific notation via ×10ⁿ (formatter "sci" in the script); hyphens replaced by minus signs.
- O50, S76: the rhetorical question removed; 11.4 heading is a statement.
- O63: the a_z term's omission in 12.6 stated. O64: "for this ω_c". O65, S83: the PI gains kept from the headless design, said.
- O66, S91: Example 12.4 rewritten without double negatives; the ratio 1.23 compared with β_h directly.
- O67: "pictures" converted to milliseconds. O68: the in-browser page introduced in the box.
- O56: Table 6 lists joint control's sensors explicitly. S84: what the crossover means. S93: "bounce" for the tyre.
- S72: reddish edge wording. S75: grid's slowness: not separated, said. S78–S80: 11.3/11.4 wording; |a_z| range explained.
- S88: Example 12.2 gives the preview distance at 1.0 m/s for the bumps. S99: Åström–Murray: book 2021, read in online v3.1.5 (2020).

## Not changed, with the reason
- O2 (2.915 Hz is the natural, not the ringing, frequency): the abstract now says "natural frequency"; the key result keeps both.
- O3 (a "kerb" is a hump): kept as the chapter's name for the hump, now introduced as "a short, sharp hump ... which we call the kerb".
- S27 (head drawn flat in Figure 1): the figure shows the pint at rest, where the head is flat; caption unchanged.
- S55, S59 (line wrapping in a rendered table/paragraph): browser layout, not the text; checked at 1440 and 390 px.
- C N77 (last digit of the tilt 13.6): the page table shows the index value 13.55 → 13.6; the stored-surface value 13.54 differs
  by the 0.02 mm rounding the details box states.
- Unverifiable source quotes (C N3, N6, N9, N28, N35, N125): sources not re-opened in this round; the drainage numbers now name
  their file.
