# Editing project 07 as one book: the session tree

Why this shape: the ten chapters are one argument read in order. A chapter's voice depends on the chapter before it
(what the reader already knows, which picture was used, what was promised). So the writing runs **in series**, one
chapter after the other, in one hand. Work that does not depend on order runs **in parallel** beside it: the rhythm
pass of the chapter just finished, the physics guard of the chapter before that, and the figures.
A first attempt with five editors in parallel failed: chapter 8 re-defined terms from chapters 2–6 and long sentences
were chopped into staccato (`AUDIT.md` §8).

## The tree

```
Coordinator (session_01DGmqinvppVjsHzqgu5FjbP, branch eb/finisher)
│  plans, dispatches, merges, runs every check, publishes, keeps AUDIT.md
│
├── V  Voice (one session, the spine, SERIES)          branch eb/voice
│      step 0: read all ten chapters, write TERMS.md and LEDGER.md
│      steps 1–11: ch00, ch01, …, ch09, guide, strictly in order
│
├── R  Rhythm holder (one session, PIPELINED one chapter behind V)   branch eb/rhythm
│      takes chapter N when V hands it over, while V writes N+1
│
├── G  Physics guard (one session, PIPELINED one chapter behind R)   branch eb/guard
│      proves chapter N kept its physics, numbers, maths, markers and terms
│
├── F  Figures (two agents already running, PARALLEL; figures are independent)
│
└── B  Blind reader (one session, SERIES, after G passes the guide)   branch eb/reader
       reads the built book as a Bachelor's student; findings go back to V → R → G
```

Time line (each column a step; V, R and G work at the same time on different chapters):

```
V:  terms  ch00  ch01  ch02  ch03 … ch09  guide              fixes(B)
R:               ch00  ch01  ch02 …       ch09  guide              fixes
G:                     ch00  ch01 …             ch09  guide              recheck
B:                                                        read
```

## Rules every session follows
- `notes/electron-beam/editing/VOICE.md` (voice, rhythm, what must not change), `CLAUDE.md`, `notes/STANDARD.md`.
- `TERMS.md` (written by V in step 0): each term and symbol, its one name, the chapter and section where it is defined.
  A term is defined once, there. Later chapters may remind in a few words with a pointer ("the reduced brightness
  $B_r$ of chapter 2"), never define it again.
- `LEDGER.md` (kept by V): for each finished chapter, its opening picture, the terms it introduces, what it promises
  later chapters, and its last paragraph. V reads it before every chapter.
- Ownership: V edits a chapter only before handing it over (and later only for the blind reader's findings, after R
  has finished it). R edits only chapters V has handed over. G edits no text. Figures belong to F; nobody touches SVG
  strings or `physics/*.js`.
- Before every commit: `python3 portfolios-src/electron-beam/build.py`, `checks/check_numbers.py`, `checks/selftest.py`.
- Commit messages end with the two attribution lines of `CLAUDE.md`'s convention:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` and `Claude-Session: https://claude.ai/code/session_01DGmqinvppVjsHzqgu5FjbP`.
- Hand-over: push the branch, then send the coordinator a one-line message ("V: ch03 done, eb/voice abc1234"). If messaging
  fails, append the same line to `notes/electron-beam/editing/STATUS.md` on your branch and push.

## Done means
Every chapter passed V, R and G in order; B's findings fixed and re-guarded; figures without collisions at four
widths; all checks pass; published to `main`; live page verified; `AUDIT.md` §8 and the finish report updated.
