#!/bin/bash
# 3 mm checks, two at a time
cd "$(dirname "$0")/../../.."
o=notes/fig12/runs
(node tools/fig12/check.cjs cylfreq 0.003 > $o/cylfreq3.txt 2>&1; node tools/fig12/check.cjs cyltilt 0.003 > $o/cyltilt3.txt 2>&1; node tools/fig12/check.cjs rest 0.003 > $o/rest3.txt 2>&1) &
(node tools/fig12/check.cjs freq 0.003 > $o/freq3.txt 2>&1; node tools/fig12/check.cjs tilt 0.003 > $o/tilt3.txt 2>&1) &
wait
echo done3 > $o/done3.txt
