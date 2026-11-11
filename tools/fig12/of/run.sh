#!/bin/bash
# Run one Fig. 12 OpenFOAM case: bash tools/fig12/of/run.sh <case dir> [processes]
# Writes log.foamRun and walltime (seconds) in the case. With processes > 1 the case is split with decomposePar (scotch)
# and run with mpirun, then reconstructed. Must not run as root (OpenFOAM refuses to compile the case's coded parts).
set -e
case="$1"; np="${2:-1}"
source /opt/openfoam13/etc/bashrc
cd "$case"
start=$(date +%s.%N)
if [ "$np" -gt 1 ]; then
  printf 'FoamFile { format ascii; class dictionary; object decomposeParDict; }\nnumberOfSubdomains %s;\nmethod scotch;\n' "$np" > system/decomposeParDict
  decomposePar -force > log.decomposePar 2>&1
  mpirun -np "$np" foamRun -parallel > log.foamRun 2>&1
  reconstructPar > log.reconstructPar 2>&1 || true
else
  foamRun > log.foamRun 2>&1
fi
end=$(date +%s.%N)
echo "$end - $start" | bc > walltime
