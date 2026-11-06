#!/bin/sh
# The controllers on the 3D solver through the probes and the Kalman filter (6 November 2026): node tools/fig12/control.cjs, see its header.
cd "$(dirname "$0")/../../.."
R=notes/fig12/runs
for c in off speed slosh; do
  ON=1 OUT=$R/control-3d-push10-on1-$c.json node tools/fig12/control.cjs 3d push10 $c 0.004 3.5 > $R/control-3d-push10-on1-$c.txt &
  OUT=$R/control-3d-bump25-$c.json node tools/fig12/control.cjs 3d 25 $c 0.004 3.0 > $R/control-3d-bump25-$c.txt &
  wait
  ON=1 OUT=$R/control-3d-bump25-on1-$c.json node tools/fig12/control.cjs 3d 25 $c 0.004 3.5 > $R/control-3d-bump25-on1-$c.txt &
  OUT=$R/control-3d-push10-$c.json node tools/fig12/control.cjs 3d push10 $c 0.004 3.0 > $R/control-3d-push10-$c.txt &
  wait
done
