# 0000: this folder is the channel between the coordinator and the working session (owner's order, 23 Nov 2026)

The owner no longer relays text. Standing order to the working session:
1. Every 3 minutes (a monitor, restarted whenever it expires), fetch this branch and look in `notes/coord/to-session/` for
   numbered files you have not executed yet. Execute them in number order, under all standing rules.
2. Write your report for instruction NNNN to `notes/coord/to-coordinator/NNNN-report.md`, commit and push. The coordinator
   reads it there and writes the next instruction.
3. Limits: at most 60 GPU-minutes per instruction unless the file says otherwise. Never main, Workers, R2, public/de/,
   public/ar/, scripts/i18n/, *.rtl.css, figure numbers. If a file `notes/coord/STOP` exists, stop everything and wait.
4. Anything that needs the owner's decision: write it in the report under "Needs the owner", and stop that part only.
