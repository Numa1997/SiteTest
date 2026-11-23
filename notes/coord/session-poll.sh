#!/usr/bin/env bash
# Run by the Code session's monitor every 3 minutes. Prints what the session must do now.
# Output lines: STOP | ACK NNNN <file> (every instruction not yet acked, newest included) | DO NNNN <file> | IDLE
# A newer instruction may answer a question raised inside an open one (e.g. 0005 approves a choice asked in 0004):
# read every ACK file before continuing the DO instruction, and follow the newer one where they differ.
cd "$(git rev-parse --show-toplevel)"
git fetch -q origin claude/guinness-projection-fix && git merge -q --ff-only FETCH_HEAD 2>/dev/null
[ -e notes/coord/STOP ] && { echo STOP; exit 0; }
do_line=""
for f in $(ls notes/coord/to-session/[0-9][0-9][0-9][0-9]-*.md | sort); do
  n=$(basename "$f" | cut -c1-4); [ "$n" = 0000 ] && continue
  [ -e notes/coord/to-coordinator/$n-report.md ] && continue
  [ -e notes/coord/to-coordinator/$n-ack.md ] || echo "ACK $n $f"
  [ -z "$do_line" ] && do_line="DO $n $f"
done
[ -n "$do_line" ] && echo "$do_line" || echo IDLE
exit 0
