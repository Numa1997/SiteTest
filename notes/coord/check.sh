#!/usr/bin/env bash
# Coordinator check: one call shows where every instruction stands.
# Stages per instruction NNNN: pushed -> ack (session listening) -> report (done) -> verified (coordinator).
set -e
cd "$(git rev-parse --show-toplevel)"
git fetch -q origin claude/guinness-projection-fix
B=origin/claude/guinness-projection-fix
echo "UTC now: $(date -u +%H:%M:%S)   branch head: $(git log -1 --format='%h %cd %s' --date=format:%H:%M $B)"
[ -n "$(git ls-tree $B notes/coord/STOP)" ] && echo "STOP file present"
for f in $(git ls-tree --name-only $B notes/coord/to-session/ | grep -E '/[0-9]{4}-' | sort); do
  n=$(basename "$f" | cut -c1-4); [ "$n" = 0000 ] && continue
  pushed=$(git log -1 --format='%cd' --date=format:%H:%M $B -- "$f")
  ack=$(git log -1 --format='%cd' --date=format:%H:%M $B -- notes/coord/to-coordinator/$n-ack.md)
  rep=$(git log -1 --format='%cd' --date=format:%H:%M $B -- notes/coord/to-coordinator/$n-report.md)
  echo "$n  pushed ${pushed:--}  ack ${ack:--}  report ${rep:--}"
done
echo "Session commits in the last 2 h:"; git log --since='2 hours ago' --format='  %cd %h %s' --date=format:%H:%M $B | grep -v 'Coordinator' || echo "  none"
