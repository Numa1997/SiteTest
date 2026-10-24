#!/usr/bin/env bash
# Every browser test of Fig. 12, in English, German and Arabic, at 1400 and 390 px. Prints one PASS/FAIL line each.
# Usage: bash notes/fig12/alltests.sh
cd "$(dirname "$0")/../.." || exit 1
fail=0
for lang in en de ar; do
  for w in 1400 390; do
    r=$(node notes/fig12/datacheck.cjs $w $lang | tail -1); echo "data  $lang $w: $r"; [[ $r == PASS* ]] || fail=1
    r=$(node notes/fig12/interact.cjs $w $lang | tail -1); echo "drag  $lang $w: $r"; [[ $r == PASS* ]] || fail=1
  done
  r=$(node notes/fig12/notecheck.cjs $lang | tr '\n' ' '); echo "note  $lang: $r"; [[ $r == *'"katexErr":0'* ]] || fail=1
  node notes/fig12/i18ncheck.cjs $lang || fail=1
done
echo "walk: $(node notes/walkcheck.cjs | grep furuta)"
[ $fail = 0 ] && echo "ALL PASS" || echo "SOME FAILED"
exit $fail
