#!/usr/bin/env bash
# Run by the Code session's monitor every 3 minutes. Prints what the session must do now.
# Output lines: STOP | ACK NNNN <file> | DO NNNN <file> | IDLE
cd "$(git rev-parse --show-toplevel)"
git fetch -q origin claude/guinness-projection-fix && git merge -q --ff-only FETCH_HEAD 2>/dev/null
[ -e notes/coord/STOP ] && { echo STOP; exit 0; }
open=0
for f in $(ls notes/coord/to-session/[0-9][0-9][0-9][0-9]-*.md | sort); do
  n=$(basename "$f" | cut -c1-4); [ "$n" = 0000 ] && continue
  [ -e notes/coord/to-coordinator/$n-report.md ] && continue
  [ -e notes/coord/to-coordinator/$n-ack.md ] || echo "ACK $n $f"
  echo "DO $n $f"; open=1; break   # one instruction at a time, in number order
done
[ $open = 0 ] && echo IDLE
exit 0
