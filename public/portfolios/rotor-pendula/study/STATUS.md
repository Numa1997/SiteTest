# Delivery status

Computed: all 18 corrected mountings for both single and double pendula; 54 original chaos cases; nine dimensionless geometries; four generator topologies; the headline regular/chaotic long and alternate-start checks; two epsilon-sensitivity checks; source-derived sensor budget. Original equations and stage kernel remain unchanged. All three initial anchors and wall times are recorded. The rounded double anchor discrepancy is documented in the report.

Computed: figures, tables and XeLaTeX report are regenerated. Derived: C1–C14 are audited in the report; historical claims depending on missing original files are explicitly not independently verified. The universal C_p versus tip-speed claim is not supported without an aerodynamic model.

Not measured, as expressly permitted by C5: large_o2_r2_middle_c0; damping_middle_opt; large_o1_r1_middle_opt; large_o1_r1_middle_c0; large_o0_r0_middle_opt. Their exponent entries are null/NaN and their regime is “not measured”; none is labelled regular by assumption. These legacy rows are not among the corrected turbine comparisons. Parameters and dimensionless coordinates are recorded in data/audit.json and the original manifest.

Assumed limitations: no blade aerodynamic model, hardware generator curve, efficiency measurement, cold-start/storage characterization or structural qualification. No global basin optimization, continuous mapping-range optimization or rigorous confidence intervals are claimed. Real hardware viability remains conditional.

Computed: original RK4 output arithmetic was checked against a 1e-8 relative-power threshold; the already-validated long RK4 integrations were not rerun. Original static/symbolic derivations were preserved rather than re-derived with a new package. New energy identity and similarity checks are in audit.json.
