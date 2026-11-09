
## From S3 (branch eb/ch01): contract change for chapter 1, and two remarks

1. **contract.json, stage ch01 (needed for the chapter to build).** The stage as proposed (E, B, v_0, theta_0, dt, integrator in; r_g,
   omega_c, energy_drift, trajectory out) is the right physics: one electron in uniform E (+y) and B (+z). A quoted number must be a
   scalar module output, so the chapter needs a run time and the end of the path: new input `t_run`; new outputs `x_end`, `y_end`,
   `z_end`, `theta_end`. Ready patch: `notes/electron-beam/ch01/contract-ch01.patch` (`git apply` it to portfolios-src/electron-beam/contract.json).
   I tested everything with it applied locally and did not commit contract.json. Without it `build.py` stops with a contract disagreement.
2. **contract.json, symbol d_opt (ch00).** Its meaning says "smallest half-pitch light can resolve, lambda/(2 NA)". Abbe's lambda/(2 NA) is the
   smallest *period* (pitch); the half-pitch is lambda/(4 NA) (derived in chapter 0). Please reword "half-pitch" to "period". The number is unchanged.
3. **Live integrator figure.** The generic simulation slot takes one module per chapter. Chapter 1's second live figure (Boris and RK4 error
   against the exact helix, log-log) is therefore a static picture drawn from ref/ch01.py; a second slot per chapter would make it live.
4. **tools/inventory.py** needs rules for `notes/electron-beam/ch01/check_thomson_vs_librarian.py` and `notes/electron-beam/ch01/contract-ch01.patch` (`--check` reports them undescribed), and for `docs/files.md` to be regenerated.
