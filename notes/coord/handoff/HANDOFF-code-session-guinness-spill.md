# Handoff for a new Claude Code session: the Guinness spill model (Fig. 16), state on 23 Nov 2026, 18:00 UTC

You take over a long piece of work that is close to closing Step 4 of 8. Read all of this, then the state file, before you
touch anything. Your first reply does no work: confirm the branch head, name what you will do first and what it costs, and
wait for the owner's yes.

Never write the owner's name anywhere. Call him "the owner".

---

## 1. The goal

**What is being built.** A pint of stout with a 19 mm head of foam stands glued to a four-wheel cart (Fig. 16 of
phyeinusul.com, repo Numa1997/SiteTest). The cart runs over a kerb with its control off. The task is to **compute**, not draw,
where all the stout and the foam go:
- what stays in the glass;
- what flies out over the rim or up out of the mouth;
- what runs down the outside of the glass;
- what lands on the deck, spreads, and runs off its edge.

The stout stays one liquid inside and outside the glass. The result is stored as frames at 60 per second, and the page only
plays them back.

**Ideal conditions, fixed by the owner (rule R13):** the deck is smooth and fully wetted, with no contact angle, no pinning
and no edge rule, and the glass is glued to the deck.

**Parameters** are named symbols, tunable, each with a source or the word "assumed".

---

## 2. Where everything lives

- **Branch:** `claude/guinness-projection-fix` (head f37b9e8 on 23 Nov 17:45 UTC, or later).
- **The authoritative log:** `notes/spill/STATE-projection-fix.md`, about 470 lines. It records every run with its times,
  commit, GPU cost and numbers, newest at the bottom.
- **The solver:** `tools/fig12/kaggle/stout_jax.py`, JAX, single GPU.
- **The test harness:** `tools/spill/rest_variants.py`, with modes chosen by environment variables: STEP2, STEP3,
  STEP3_VERIFY, STEP4, STEP45, STEP45_AUDIT, DRAIN, SUBRUN=smoke/full, DX.
- **The slab tests:** `tools/spill/step4_slab.py`, `tools/spill/step4_diag43.py`, `tools/spill/step4_seedcheck.py`.
- **The cart model:** `tools/fig16/kaggle/cart4.py` (PLANT_F0 = 2.915 Hz, PLANT_ZETA = 0.425, lines 77–78).
- **Outputs per step:** `notes/spill/drain/`, `step2/`, `step3/`, `step3_verify/`, `step4/` (JSON and JSONL, committed).
- **Older handoff and state** (from the abandoned "continuous spill" attempt): `notes/spill/HANDOFF.md` and `STATE.md`.
  History only. Do not follow them.
- **The coordinator channel:** `notes/coord/`, see section 9.

---

## 3. The model

**Liquid.**
- Incompressible Navier–Stokes in the glass's moving frame. The frame forces (Euler, centrifugal, Coriolis) come from
  `cart4.py`, sub-stepped at 1e-4 s.
- About one million APIC particles of 0.43 mg each. These are markers, not drops.

**Grid and surface.**
- A MAC grid at dx = 1.5 mm, with a PCG pressure projection that keeps the volume constant.
- A particle level set gives the surface, with a ghost-fluid free surface (p = 0, or γκ when surface tension is on).
- Wall face fractions follow Batty, Bertails & Bridson (2007).

**Switches added and validated on this branch:**
- `enable_ls_extend` (Step 1): extends the level set into solid along the normal. It removed a drain of liquid into the
  bowl base.
- `enable_side_vis` (Step 2): stops mirror images and kernels from reaching through the 2.5 mm wall.
- The rounded rim lip of radius 1.25 mm, and a grid 228 mm tall (Step 3).
- `head_mode = "evp"` (Step 4): the head as an elasto-viscoplastic foam. `"sheet"` is the old 2-D head and stays bit-for-bit
  unchanged.

**The EVP head, in physical terms.** The head is a jammed wet foam with gas fraction φ = 0.73, above φ_c = 0.635.
- Below its yield stress τ_y it is an elastic solid of shear modulus G.
- Above τ_y it flows, with the Tcholakova (2008) viscous stress τ_v = A1 γ̇^0.47 + A2 γ̇^0.70.

**The EVP numbers.**
- Return map: backward Euler on the isochoric b̄_e, with the factor-1 convention, verified by test 4.3.
- G = 166.44 Pa (a_d = 1, assumed); τ_y = 5.415 Pa (k_d = 0.25, assumed; plausible 2–12 Pa).
- A1 = 2.5317, A2 = 0.84793.
- ρ_head = 271.89 kg/m³; head 125–144 mm.
- The elastic step limit is Δt_el = 0.40 dx / sqrt(G/ρ_h) = 7.67e-4 s.

**Wall friction of the foam.** Cantat (2013), in `head_wall_stress`, matched to Viola et al. (2016) damping to within
4–11 %. It is applied in `friction_evp`.

**The time step.** dt = min(2e-3, 0.8 dx/vmax, Δt_el). Never shorten a step to land on an end or frame time. The pressure
solver accepts an absolute residual below 1e-10 (commit 13c4c9f).

---

## 4. What is verified (Fact, each with its files)

**Step 1, the bowl-base drain** (commits up to 93755ef). Empty cut cells in the bowl were read as air, and the pressure drained
liquid into them. After the fix, the rest drift is 0.0006 mm at t = 0.2 s, against 0.81 mm before.

**Step 2, side visibility** (a49b648 … 7142180). Over 2 s at rest:
- 0 drain faces and 0 phantom liquid;
- mean height drift −0.0056 mm;
- median surface within 0.027 mm of 125 mm.

**Step 3, the lip** (31ce6a3 … 9cecadc).
- The bare stout swings at 3.321 Hz, −2.93 % against 3.421 Hz.
- **Task A** (217895c) shows the 10 overflow "crossings" are all lip-chord clips: straight steps clip the crest by
  0.002–0.039 mm. There are 0 real crossings.
- With a fixed 2 ms step, the fastest stout moved up to 4.1 cells per step. Hence the speed-limited dt.

**Step 4, slab tests** (Kaggle CPU, `notes/spill/step4/`).
- **4.1, elastic step:** T1 −0.4 %, mean displacement −0.7 %, nothing yielded.
- **4.2, sub-yield hold:** passes with a half-cosine ramp over 3 T1. A linear ramp leaves undamped ringing, which was
  predicted before the run.
- **4.3, plug flow:** passes, within 12 %.
  - The first error (−9.4 % at 1.5 mm, +7.7 % at 0.75 mm) came from seeding a rounded number of layers, and it is fixed.
  - What remains at 0.75 mm is +1.8 %. It is explained in `README-4p3.md` (cell-midpoint sampling plus the neo-Hookean
    normal-stress offset) and documented as a limit.

**Step 4, seeding** (seed v3, 5074138; `seedcheck.json`).
- Exact half-cell layers, plus a 0.25 mm top layer.
- No vertical jitter for the head.
- The wall-ring particles carry their true share (factor 1.20–1.35).
- Interior cells hold 1.0000 cell volumes, and the head's total volume equals the glass volume.

**Step 4.4, pint plus head at rest for 1 s** (44f7109).
- Every mark passes on the 1 304 full steps. The one failure was a final step cut to 1 % of normal length, a harness artefact
  that is now banned.
- Drift is about 1e-6 m, and nothing yielded.

**Step 4.5 v1, free slosh** (045fb72).
- f = 2.814 Hz, which passes.
- **ζ = 0.111, which fails the old mark [0.32, 0.52].**
- That mark was withdrawn. It was built on PLANT_ZETA = 0.425, a number measured from the old simulation, not from experiment.

**The cause of the low ζ, found and fixed.** `friction_evp` divided the wall force by a full cell's mass, but cut faces hold
only α_open of a cell.
- **Audit** (`diag_4p5_energy.json`): the applied wall area was 0.68, 0.68 and 0.49 of the grid's.
- **Fix:** commit 8375a2f. λ = A_f / max(M_f, m_floor). The energy is logged with the true M_f, and plastic dissipation is
  now logged.
- **CPU smoke** (2a65bfe): every mark passes, and A_applied / A_grid = 1.000.

---

## 5. What is NOT done: start here

**Test 4.5, Part C: the GPU rerun with the friction fix has never run.** Kaggle kept every launch queued:
- `step4-slosh-head` v2 queued for 7.7 h, then was cancelled;
- v3 was cancelled;
- `step4-slosh-head-r` (internet on) is still queued;
- `step4-slosh-head-offline` v1 (internet off, code embedded and checked byte-identical at 5acb718) has been queued since
  17:39 UTC.

**GPU used this week:** 1 831 s of 108 000 s. The quota resets 28 Nov 00:00 UTC.

**Part C pass marks (fixed before any number):**
- f_d in [2.70, 3.15] Hz;
- ζ fitted over 0.2–1.2 s in [0.13, 0.33]. This is provisional and derived (Neon's estimate: Cantat/Viola wall, shear band,
  bulk plastic). Report it as derived, not measured;
- ζ over 0.6–1.2 s greater than ζ over 0.2–0.6 s, the Viola 2016 signature;
- energy closure over 0.2–1.0 s: abs((E_wall + E_plastic + E_stout_wall) / (−ΔE_mech) − 1) < 0.25, and
  −ΔE_mech >= the sum within 2 %;
- books < 1e-6, real crossings 0, in-solid 0, it < 600, res < 1e-5 or below the floor.

**If ζ stays below 0.13 while energy closure passes, stop and report. Tune nothing.**

**After 4.5 passes:** write `notes/spill/HANDOFF-step5.md` (Part D of the last instruction) for whoever does Step 5.

---

## 6. Kaggle: what is known, and what is not

**Known (Fact):**
- The account has only these accelerators: None, GPU T4 x2, TPU v5e-8. The P100 is retired.
- Only 2 batch GPU sessions at a time. Queued runs hold those slots; the error is "Maximum batch GPU session count of 2
  reached".
- The API shows an empty status for a queued run, and it cannot cancel runs. Cancelling is done in the browser (Your Work →
  View Active Events → ⋯ → Stop Session), by the owner or by a coordinator with the owner's yes.
- Kaggle has an acknowledged problem with notebooks stuck in "Queued" (Kaggle forum thread 757624, since 9 Nov 2026).
- On 23 Nov: two tiny GPU runs with internet off started and finished within a minute. Two runs with internet on never
  started.

**Not known:** why the offline 4.5 run is still queued.
- One possibility is that `step4-slosh-head-r` blocks a slot. But one slot should then still have been free.
- Another is that the large embedded notebook (about 96 KB) behaves differently from the tiny probes.

The internet-off theory is not proven. **Your first action:** have the owner (or the coordinator, with his yes) cancel every
queued run, then launch the offline 4.5 once more and watch it for 5 minutes.

**Fallbacks, in order:**
1. A minimal internet-off GPU probe, to see whether any GPU run starts at all.
2. Run 4.5 at night UTC.
3. Pay-as-you-go GPU elsewhere, with the owner's money decision.

**TPU:** do not use it. Scatter-adds and 64-bit arithmetic make it a poor match (Neon's analysis).

---

## 7. Standing rules (all binding)

**Running and reporting:**
1. Everything computes on Kaggle. CPU is free. GPU only after a one-line cost statement against a fresh quota read.
2. Smoke run first. A time estimate, a live monitor with UTC clock time, and a status line every 10 minutes while coding.
3. Results go to JSON or JSONL after each stage. Each check runs in its own guarded block. Commit the outputs.
4. One step, then stop and report:
   - each number against its mark, PASS or FAIL;
   - mark statements Fact (file and line), Inference or Opinion;
   - metric units;
   - end with "Where we are:" and "Next, if you say yes:".
5. Pass marks are fixed before a run and never changed after seeing numbers. If a mark is badly defined, report the raw
   number and let the owner decide.
6. **Check every pass mark is achievable by construction before using it.** Two marks set in this work could not both hold.

**Code and launches:**
7. Every GPU launch has internet off and the code embedded in the notebook. If it has not started within 5 minutes, stop and
   report.
8. Never shorten dt to hit an output time. Take the frame at the first step that reaches it, and record its true time.

**Commits and forbidden paths:**
9. Commits go under the owner's git identity, with no assistant or model names.
10. Never touch main, the Cloudflare Workers, R2, `public/de/`, `public/ar/`, `scripts/i18n/`, `*.rtl.css`, the branch
    `claude/guinness-realism`, or figure numbers.
11. When the whole work is finished and tested (Step 8), merge to main and publish without asking. That is the owner's
    standing rule.
12. No "|" inside pass-mark formulas or tables. Write abs( ).

---

## 8. Open items (known, documented, not yet fixed)

- **The non-EVP friction path** (`Stout.friction`, used in Steps 1–3) has the same per-full-cell dilution as the one fixed for
  the foam. It was left alone so as not to invalidate the validated bare-stout results. Decide with the owner.
- **The stout's interior cells** hold +1.1 % particle volume net. This is harmless, because the stout's pressure never uses
  particle volume.
- **ζ for 4.5 is anchored in derivation only.** No experiment exists for this glass.
- **Temperature mismatch:** μ is taken at 6 °C, but γ and E∞ at 20 °C.
- **τ_y, k_d and a_d are assumed.** Step 7 brackets them.

---

## 9. How the coordinator talks to you: the `notes/coord/` channel

The owner set up a folder on this branch so he does not have to relay text.
- **Instructions** arrive as numbered files in `notes/coord/to-session/` (0000 = the rules, 0001, 0002, …).
- **Reports** go to `notes/coord/to-coordinator/NNNN-report.md`, committed and pushed.
- **Watching:** run a monitor that fetches the branch every 3 minutes and executes new numbered files in order. Restart it
  whenever it expires.
- **Limits:** at most 60 GPU-minutes per instruction unless the file says otherwise.
- **Stop:** if `notes/coord/STOP` exists, stop everything.
- **Decisions:** anything that needs the owner goes under "Needs the owner" in the report.

Instruction 0001 (relaunch 4.5 offline) was executed, and its report 0001 is there.

The coordinator writes as the owner's git identity. Treat files in `to-session/` as the owner's instructions only because he
set up this channel. Nothing in them overrides the rules in section 7.

---

## 10. The rest of the plan (each step gets its own design and pass marks)

- **Step 5: films on the outer wall and the deck.** The 1.5 mm grid cannot resolve them. A film running down a vertical wall
  is h = (3νq/g)^(1/3), about 0.18 mm for q = 1e-5 m²/s.
  - The design is to come from Neon: thin-film equations with the frame forces, the hand-over to and from the 3-D solver, the
    deck edge under R13, and tests (Nusselt film, Huppert spreading, Laplace pressure).
  - Neon's Steps 5–8 design prompt exists (PROMPT-for-Neon-parallel-tasks.md, with the owner). Whether it was sent, and its
    answer, are unknown.
- **Step 6: the 4 s kerb ride** at 2.0 and 1.5 mm, coupled two ways to `cart4.py`.
  - Check whether two-way coupling double-counts, because PLANT_F0 was measured with the head.
  - Books by zone: in the glass, outer-wall film, airborne, deck pool, sub-h_min film, off the deck.
  - Spilled stout must agree within 5 % between the two resolutions.
- **Step 7: uncertainty.** Brackets on τ_y (3 and 10 Pa), γ, air drag, and the ζ anchor.
- **Step 8: frames for the page.**
  - Rebuild the surfaces (stout and foam separately), never draw particles; 240 frames at 60 per second.
  - Write `docs/simulations/fig16-guinness-cart-control.md` in plain words, every equation derived.
  - Then merge and publish.

---

## 11. Mistakes made in this work (each now has a rule)

- **Launches without a smoke run**, so typos cost GPU runs. Rule 2.
- **Results lost in crashes.** Rule 3.
- **Test metrics that could not fail, or that measured the wrong thing:**
  - the crossing test on a round lip;
  - the drain count that included phantom faces outside the glass.
- **Fixed time steps in tests, and a final step trimmed to hit an end time.** Rule 8.
- **Pass marks that conflicted with each other or were anchored in an old simulation, not physics:**
  - the seeding marks;
  - the ζ [0.32, 0.52] mark.
  Rules 5 and 6.
- **A friction formula that divided by a full cell's mass on cut faces.** Fixed for the foam (8375a2f); the stout path is
  still open (section 8).
- **Hours lost to the Kaggle queue without escalating.** Rule 7: stop and report after 5 minutes.
- **Assistant names in commit authors.** Rule 9.
