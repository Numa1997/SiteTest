# Fig. 16 spill derived from the stored ride: state on 19-20 Nov 2026 (handoff)

Branch `claude/guinness-open-problems`. Nothing here is merged or live. Read CLAUDE.md, then this file, before any work.
Earlier history: notes/spill/HANDOFF.md, notes/spill/STATE.md, notes/spill/FINDINGS-review-19-nov.md.

## The owner's rules (in force)
- No recomputation of the stored ride. Derive what is missing outside the glass from the stored data, with textbook physics,
  and check it against the stored data. The CPU rerun (`rerun_rim_cpu.py`) is outside the method: don't use it.
- Everything runs on the owner's Kaggle CPU. Nothing is computed in the container: only reading, editing, git, curl
  downloads and the Kaggle API. Validate code by reading it. GPU is off.
- Every action needs the owner's explicit yes for that action. One step per turn. Each turn ends with "Where we are:" and
  "Next, if you say yes:". Mark statements as Fact (with a handle), Inference or Opinion. Metric units. No flattery.
- Every Kaggle run: give a time estimate first, place a live Monitor that reports each change of state with the clock time
  and the time elapsed, and report the run times at the end.
- Ideal conditions: the deck is smooth and fully wetted, the glass is glued to it, and there are no contact angles.
  Don't ask the owner for a contact angle.
- The spill is a LIQUID. Don't compare markers one by one; compare fields (mass per cell per time window).
- Never touch the Workers, R2, `public/de/`, `public/ar/`, `scripts/i18n/` or `*.rtl.css`. No model names in commits.
  Never write the owner's name. Don't merge `claude/guinness-realism`. No renumbering of figures.

## Kaggle (curl to api.kaggle.com; the proxy injects the credentials)
- Save and run: `KernelsApiService/SaveKernel`, with `datasetDataSources: ["numakoudsie/fig16-guinness-cart-control"]`.
  The MCP save_notebook drops dataset attachments; don't use it. Status: `GetKernelSessionStatus`.
  Outputs: `ListKernelSessionOutput` (`.files[].url`, `.log`).
- The kernel is a small launcher that downloads the script from raw.githubusercontent.com at a pinned commit and runs it.
  Examples: notebook `fig16-spray-derived` (`derive_liquid.py`) and `fig16-lip-detach` (`lip_detach.py`).
- Stored ride: `fig-16-guinness-cart-with-control/v8/output/2026-11-15/kerb_off.npz`.
  - 241 pictures at 60/s.
  - N = 1 001 952 markers of mp = 0.429 mg.
  - `drops`: an even subsample of at most 16 384, float16.
  - Counters: nact, nfly, nstuck, nlanded, ndrops. Head: lumps, lumpvol, foam_spill.
  - Frame and surface: gx, gz, om, th, v, vzc, H (57×57 surface height, 1.5 mm columns).

## Results (Fact: each is from the run named)
1. **The stored counters close exactly.** In the glass + in the air + frozen + fallen − N = 0 in all 241 pictures. The head's
   lumps match foam_spill to 0.000 g. (derive_liquid v5 and v7, REPORT.md.)
2. **The missing 5.8 g was in the derivation**, not the data. Of the 5.00 g lost at −14 mm, 0.98 g was liquid with no
   velocity and about 4.3 g net came from the rule that a crossing counts only if it happens within one picture interval.
   The other 0.81 g was lost between −14 and −30 mm by the same rule (v5). The marker-by-marker figures (62.4 and 58.1 g)
   are dropped, per the owner.
3. **The stored flight already uses the full frame equation**: gravity and the cart's acceleration, plus Euler, centrifugal
   and Coriolis forces (`tools/fig12/kaggle/stout_jax.py:871-875`, `frame_accel` at `:382-391`). What the stored solver
   lacks: liquid cannot cling to the outer wall of the glass, because a marker over the rim is in free flight at once
   (`:866-869`), and flying liquid passes through the glass, since only the cart body is a target (`:876`).
4. **Lip test** (`tools/fig16/derived/lip_detach.py`, notebook fig16-lip-detach v1, 48 s): exit speed from continuity,
   u0 = Q/(ρ b h_rim).
   - Mass-weighted medians: h_rim 11.8 mm, b 82 mm, u0 0.42 m/s. r_lip = 1.25 mm (half the 2.5 mm wall).
   - Mass that leaves the lip: simple balance 68.1 g (90.1 %); Duez et al. 2010 (PRL 104, 084503, Eq. 2, θ0 = 0,
     c = 0.4 read off Fig. 3b) 74.4 g (98.5 %); with their intercept 69.7 g (92.3 %).
   - Caveat: the sheet is far thicker than the lip (h/r_lip ≈ 10), outside Duez's thin-film regime.
   - Conclusion: the stored flight stands for about 90 % or more of the mass. The wall film (option B) concerns at most 1–7.5 g.
5. **Run A** (`derive_liquid.py` at commit 260ae1f8 on this branch, notebook fig16-spray-derived v7; launched 14:23:36 UTC,
   finished 14:29:30, 5 min 54 s, of which 259 s computing):
   - Total landed 75.57 g of 75.57 g over the rim, exact by construction: frozen part 32.29 g, fallen part 43.28 g.
   - On Fig. 16's deck 47.24 g; off it 28.33 g.
   - Field check: per 5 mm cell and 0.1 s window, the L1 mismatch of the deck landing against the stored frozen mass is 74.5 %.
     With the derived velocities alone it is 97.9 %. **But the sampling floor is 129.2 %**: at this resolution the stored
     subsample cannot resolve the field, so the check does not discriminate.
   - The frozen markers could not be followed one by one: only 28.6 % of the listed frozen markers reappear from picture to
     picture, because the subsample changes. So the "stored positions" fell back to the difference of the frozen fields on
     5 mm cells.
   - 6.85 g of sampling noise was clipped from the fallen flux. The total stays exact, but the timing is smoothed.
   - Check 2 (prediction of picture k+2) still FAILS: 17.5 mm against 21.0 mm unmoved, sampling floor 16.6 mm.

## Open (nothing started; the owner decides)
- Make the field check discriminating: coarser cells or windows (for example 10–20 mm and 0.25 s), chosen so that the
  sampling floor falls well below the mismatch, with the pass mark fixed before the run.
- Option B: a wall film for the slow 1–7.5 g (falling film on the outer wall, u = g h²/(3ν)).
- The deck stage: the thin-layer model `tools/fig16/derived/puddle_ideal.py`, fed by `deck_source.npz` (v7 output). Huppert
  check from a thin start (the earlier spreading check was +8 % at 4 s, from a dam-break start).
- Docs: `docs/simulations/fig16-guinness-cart-control.md` must describe the derived spill once it is final. Player integration.
