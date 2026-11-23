# 0006: new standing rules (the owner, 24 Nov 2026): Neon writes all code; you write none and run nothing. First task: the Neon request for the energy fix

## Standing rules from now on (they override every earlier rule that conflicts)
1. You run no scripts and no commands that execute code: no python, no tests, no smoke runs, no builders, no Kaggle pushes of your own.
   Allowed: reading files, git (pull, add, commit, push), and writing the code blocks the owner pastes to you.
2. You write no code yourself, not a single line. All code comes from Neon (a Gemini model the owner runs).
3. When code is needed, you write a complete-context request for Neon and present it to the owner in your chat as one block he can
   paste to Neon. It must stand alone: the measured numbers, the exact current code it touches (verbatim excerpts with file and
   function names), the constraints, and the exact format you need back (complete replacement functions or files, each headed with its
   path and the function it replaces; no diffs, no "...", no placeholders; new behaviour behind a flag, default off).
4. When the owner pastes Neon's code to you, put it into the repository exactly as written, at the stated place, commit under the
   owner's identity, push, and report in your chat what went where (file, function, commit). If a block does not fit the code (name
   missing, signature differs), do not adapt it: say exactly what does not fit and write the follow-up request for Neon.
5. Keep the channel as before: ack each instruction, report in to-coordinator/.

## First task under these rules
Write the Neon request for the energy fix, from your 0004 report: the adjoint break (W_constit / W_stress_grid = 3.088 at 3 mm, 62 %
interior foam, cell-strain shadow within 5.5 %), the +0.088 mJ from gravity+pressure, the 1.5 mm vs 3 mm difference (1.514 vs 1.130),
the step order in Stout.step (P2G with F_dev from tau at step start -> viscosity -> friction_evp -> F_dev kick u += dt F_dev / max(M_f,
m_floor) -> gravity -> pressure -> extrapolate -> G2P (C from the final extrapolated velocity) -> evp_return_map with that C), verbatim
excerpts of p2g_evp's F_dev, g2p's C, evp_return_map and the F_dev kick line, and the parameters. Ask Neon for: the diagnosis (which
velocity must drive the return map so constitutive work equals F_dev's grid work; USF vs USL; masking extrapolated faces; an objective
rate so pure rotation gives no stress), whether the +0.088 mJ needs a fix now, the complete code (flagged, default off, default path bit
for bit unchanged), one complete Kaggle CPU test notebook script at 3 mm with the flag on and off, pass marks fixed in advance and shown
reachable, the 4.5 marks unchanged, no tuning, and a one-sentence physical picture of why the fix works.
Present that request to the owner in your chat, commit a copy as notes/coord/neon/2026-11-24-energy-fix-request.md, then stop and wait.
