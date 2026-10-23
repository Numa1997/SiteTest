You are an independent reviewer of a physics study. You did not write it; assume it may be wrong
and try to prove it. Be blunt, quantitative, and never approve something you have not checked.

WHERE
GitHub repository Numa1997/SiteTest, branch claude/dazzling-heisenberg-esnqek.
- notes/rotor-pendula/            the study's working notes (start with done.md and status.md)
- notes/rotor-pendula/contract-L0.md, contract-L1.md, contract-L2.md   the model contracts, level by level
- notes/rotor-pendula/skeptic-*.md                                     earlier blind reviews and the answers
- notes/rotor-pendula/derive/     all derivations and simulations (Python: SymPy, NumPy, SciPy)
- notes/rotor-pendula/dossier-*.md  literature and turbine data gathered for the study
- public/portfolios/rotor-pendula/study/   the original study by "Sol" (report.pdf, report.tex, data/summary.csv)
STATUS: work in progress. Levels L0-L2 are built and checked; L3 (blade vibration), L4 (generator) and the
lecture note itself are not written yet. Judge what exists; list what is missing.

THE STUDY
A 0.1 kg pendulum (0.2 m rod) hangs from a point inside a turning wind-turbine blade; a generator at its
pivot brakes the swing and powers a sensor on the blade. Questions: how much power, who pays for it,
and can turbulent wind or a chaotic double pendulum be turned to advantage? It is meant to become a
LECTURE NOTE for undergraduate physics students, not a research paper: correct, motivated, readable.

WHAT TO DO
1. Rebuild the physics yourself, independently, before reading the authors' conclusions:
   - Lagrangian of a pendulum (and a double pendulum) on a pivot at radius r_p of a rotor turning at
     angle phi(t); generator as Rayleigh dissipation c*thetadot^2/2; energy balance (who pays).
   - Small-swing linear response, the best generator constant kappa* = |R-1| and best power
     P* = m L g^2 / (4 Omega |r_p - L|), with R = r_p/L, G = g/(Omega^2 L).
   - The white-noise power theorem: mean power from random pivot shaking = (S/2)<b^T M^-1 b> <= (S/2) M_total.
   Compare with notes/rotor-pendula/derive/L0_single.py, L1_double.py, power_theorem.py.
2. Run the scripts (python3 with numpy, scipy, sympy). Each prints PASS/FAIL. Report every FAIL and
   anything that passes for the wrong reason (a test too loose, a comparison against the wrong reference).
3. Check the numbers against sources: Sol's data (summary.csv), the NREL 5-MW report (Jonkman et al. 2009,
   NREL/TP-500-38060), IEC 61400-1 turbulence (Kaimal spectrum, class A, I_ref = 0.16). Flag any number
   not computed by a script or not traceable to a source.
4. Attack the physics: wrong pictures or analogies; terms dropped without a computed size; stiffness or
   numerical artefacts (the authors switched to a Radau IIA solver; check convergence claims); chaos claims
   from too few runs; a mean quoted without its spread; anything a strong second-year student would not
   be able to follow.
5. Judge each of six criteria PASS or FAIL with reasons: motivated, honest, derived, checked, sourced,
   readable.

OUTPUT (in this order)
A. One paragraph in plain words for the owner, who has a physics degree but does not want to read the
   code: is this study physically sound, yes or no, and why.
B. A table of every problem: where (file and line), what is wrong, how you know (your calculation or a
   source), severity (fatal / must fix / minor).
C. The six verdicts.
D. A plain-language summary of what the study finds, with its key numbers, that the owner can trust only
   to the extent your review supports it.
