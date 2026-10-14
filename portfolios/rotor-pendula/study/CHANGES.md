# Changes from the first delivery (C1–C14)

Computed/Derived changes below; unchanged mechanics and reproduced anchors are preserved. Full row-level replacements are in summary.csv.

1. C1: original reported 15,859,712-byte incomplete archive → compact verified ZIP below 8,000,000 bytes; FILE_INVENTORY.csv lists every delivered file and byte count. Original lost 16-page report → 14-page reconstructed report.
2. C2: assumed rotor radius 0.7 m → 5.347606 m at 10.471976 rad/s; baseline power 217.237 W → 12,678.190 W; original anchor fraction 6.98780e-4 → 1.19734e-5. Rotor tip-speed ratio is now assumed 7. The universal C_p/required-tip-speed claim is unproved without an aerodynamic model.
3. C3/C10: six paired mountings → 18 speed/fraction mountings. Pivot radii (m), old → new at each speed:
   0.5 → 1.6043, 3.2086, 4.8128; 1.0 → 0.8021, 1.6043, 2.4064; 1.5 → 0.4011, 0.8021, 1.2032; 20 → 20.0535, 40.1070, 60.1606; 40 → 11.4592, 22.9183, 34.3775; 60 → 8.0214, 16.0428, 24.0642.
4. Corrected headline: 0.151801 W → 0.05708639 W; the original 0.151801 W remains valid only for its original pivot. Double/single range 0.6672–0.7353 → 0.6351–0.7354. Best corrected turbine fraction is 7.20436e-5. Changed mapping, not changed equations.
5. C4: old centrifugal range 1.4–268 times g → 1.435–215.277; radial specific-force envelope adds one times g. ±8 times g is verified. Six slow mountings pass the gravity-only range guard; no fast mounting passes.
6. C5: five provisional regular labels → “not measured”; missing exponents remain unmeasured, as permitted.
7. C6/C7: historical four chaotic cases → two of 54 in this rerun. Matched short-window chaotic 0.2439 W, exponent 0.03578 → 0.253 ± 0.003 W, 0.032 ± 0.008; arithmetic/backend sensitivity and finite windows preclude exact trajectory reproduction. Long-window result remains 0.244 ± 0.002 W. Errors are naive block SEMs.
8. C8: regular robustness source c=0.010 → headline c=0.022 N m s/rad, now checked for 800 periods and two alternate starts; 0.378920 W. Long chaotic/regular ratio 0.6436 → 0.6448. Epsilon checks 0.04429/0.03495 → 0.027/0.039 from the explicitly recorded common checkpoint; all blocks positive.
9. C9: “passed” → measured relative RK4 differences 4.61e-12 and 3.21e-12, threshold 1e-8; retained outputs, not redundant integrations.
10. C11: unsupported 1000 µW budget → sourced 37.58436 µW typical-current reference; mechanical requirement 75.16872 µW at assumed 50% efficiency. 1 mW remains only an assumed overhead allowance.
11. C12/C13: middle motion “small relative to first arm” → ratio 0.261–0.325. Topology values explicitly R=5, G=0.1, nonlinear at linear optima. Middle damping 0.912 → 0.930; normalized power 2.759e-5 → 2.758e-5; nonlinear correction 2.60%. No global optimum claim.
12. C14: uniform scaling of every mass and rod stated; power factor 6 unchanged. Trajectory difference 8.130e-11 → 2.05e-10, rtol=1e-10, atol=1e-12, current kernel/backend. Rounded double anchor 0.101285 → 0.101284543458 W is a display-precision correction.
