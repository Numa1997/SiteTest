#!/bin/bash
# the acceptance matrix of the self field; 4 jobs at a time; each line is one JSON result
cd "$(dirname "$0")/.."
jobs_list=()
for med in glycerol honey water; do for ang in 0 90 45; do for U in 0.5 0.1 0.01; do
  [ "$med" = water ] && [ "$U" != 0.5 ] && continue
  for opt in base selfField; do jobs_list+=("MED=$med ANG=$ang U=$U OPT=$([ $opt = base ] && echo '' || echo $opt)"); done; done; done; done
for med in glycerol honey; do for opt in base selfField; do jobs_list+=("MED=$med ANG=0 U=0.5 DX=0.0125 OPT=$([ $opt = base ] && echo '' || echo $opt)"); done; done
for med in glycerol honey water; do for opt in base selfField; do jobs_list+=("MED=$med MODE=moving V=0.3 ANG=0 OPT=$([ $opt = base ] && echo '' || echo $opt)"); done; done
jobs_list+=("MED=glycerol MODE=moving V=0.3 ANG=45 OPT=" "MED=glycerol MODE=moving V=0.3 ANG=45 OPT=selfField")
printf '%s\n' "${jobs_list[@]}" | xargs -P 4 -I{} sh -c 'env {} node fix/t_selfall.cjs'
