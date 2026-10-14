# Exact regeneration

Run from the extracted wind_pendulum directory. No simulation, plotting or report script accesses the network. No package was installed for this delivery. Python 3.12.14 was used with numpy 2.3.5, scipy 1.17.0, matplotlib 3.10.8, and fontTools 4.61.1. XeLaTeX (XeTeX 0.999995, TeX Live 2023/Debian), Latin Modern and the included three font files build the report. GCC is needed only for the optional C stage acceleration.

The supplied model.py, accelerator.py, lyapunov.py and other reference sources are unchanged in code/reference. The new study is compute.py. The old reference pipeline is historical and is not the regenerated report workflow; its optional symbolic derivation requires SymPy, which was not installed or rerun. The report reproduces the algebra explicitly.

Cached numerical metadata in data/runs prevents repeated integrations. To recompute all trajectories, move data/runs to a backup location first and create an empty data/runs directory. Run these commands in order:

```bash
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
PENDULUM_NATIVE=0 python code/anchors.py
export PENDULUM_NATIVE=1
python code/compute.py --workers 6
python code/audit.py
python code/sensitivity.py
python code/figures.py
python code/write_report.py
xelatex -interaction=nonstopmode -halt-on-error report.tex
xelatex -interaction=nonstopmode -halt-on-error report.tex
python code/package.py
```

Set PENDULUM_NATIVE=0 to use unmodified SciPy. The scalar DOP853 stage arithmetic can differ in chaotic trajectories across backends or versions; long-window means and block statistics should be compared, not exact chaotic states. Period-one anchor differences are documented in data/anchors.json. This file preserves the initial anchor timings; rerunning simulations is not expected to reproduce machine timing.

compute.py records every initial state and window in corrected_manifest.json and each result JSON. The unchanged original_run_manifest.json specifies every original run. R_nd is r_p/(l1+l2), G_nd is g/[Omega^2(l1+l2)], Gamma is R_nd/G_nd. R_rotor_m is the assumed turbine radius, distinct from R_nd. The corrected sampling is 6 speeds times 3 blade fractions times 2 topologies. The single model places m1+m2 at l1+l2; its two stored q/u columns duplicate one degree of freedom.

For corrected mappings, the linear optimum is confirmed with 100 discarded and 200 averaged periods. If the deflection or power criterion fails, a local periodic-branch nonlinear maximum is sought between half and twice its damping, then confirmed. This is not a global optimization over basins. Linear CSV rows are evaluations at the final damping, which can be the refined nonlinear damping. They are predictions, not independently integrated runs.

The chaos regime requires lambda_dimensionless > 0.002 and every exponent block positive. Nonperiod-one candidates use four 50-period blocks; settled period-one cases use a 24-period stability check. No exponent is invented for a mapping that was not measured. The five unmeasured legacy cases are individually recorded in audit.json and STATUS.md.

All 111 nonlinear run metadata files and 49 linear evaluations are retained. To keep the ZIP compact, only trajectories used by the two long-run section plots are retained. Other trajectories can be regenerated from their metadata. Float32 arrays contain SI time, blade-relative q, dimensionless u, mechanical harvest power, torque on the rotor, and integrated harvest/work. Use theta=Omega*t+q and omega=Omega*(1+u) to reconstruct inertial variables. Samples are 16 per rotor period; quadrature and calculations used float64.

The summary's rotor_power_W is mean mechanical power supplied to the pendulum. turbine_output_W is the assumed baseline turbine output and must not be confused with it. energy_balance_rel_err = abs(W_rotor-H-DeltaE)/abs(H). A finite-window difference in input and harvest can be stored mechanical energy.

Datasheet current times voltage gives a typical-current reference. The duty cycle, conversion efficiency and 1 mW optional engineering allowance are assumptions. Datasheet PDFs are omitted; hashes and conditions are in sources/README.md. Included fonts permit offline rendering. No deployment, cloud write or repository publication occurred.
