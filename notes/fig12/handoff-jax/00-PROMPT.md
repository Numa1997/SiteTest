# PROMPT FOR THE NEXT SESSION: Guinness on a cart, in JAX on Kaggle. Read the mistakes first; they must not happen again

Written 13 November 2026, about 12:10 UTC (13:10 Berlin), by the session "Guinness cart page rebuild". You are a fresh session.
You cannot ask that session anything. Everything is in this prompt, in the four files beside it, and in the repository.

Repository `Numa1997/SiteTest`, branch `claude/nifty-lamport-iz5pua` (fetch it first). Folder: `notes/fig12/handoff-jax/`.

## 1. Read, in this order, before you write a word to the user

1. `handoff-guinness-cart.md`: the state, the user's rules word for word, the exact numbers, what is open.
2. `01-mistakes-and-rules.md`: twelve mistakes of the last session, what each cost, and the rule against it.
3. `02-launch-gates.md`: the six gates. Nothing goes to the GPU, and nothing goes to the site, past a gate that has not printed PASS.
4. `03-model-and-numbers.md`: the physics as coded, and which parts have never been executed.
5. Then the repository's own: `CLAUDE.md`, `AGENTS.md`, `notes/fig12/research/data-for-solver.md`, `notes/fig12/research/verification.md`,
   `notes/fig12/handoff-control-session.md`, `docs/simulations/fig12-beer-slosh.md`, `docs/kaggle-pipeline.md`, `docs/usul.md`,
   `docs/styles.md`, `notes/STANDARD.md`.
Say in your first message which of these you read. The last session skipped five of them.

## 2. The user

The site owner; call them "the user" in anything written; they/them. A physicist (BSc, computational and theoretical). Four
sessions in a row have failed them on this figure, and the last one spent their GPU time on two runs whose data cannot be used.
They said: "I don't trust you anymore." Earlier that night they said, in anger, that they might hurt themselves: if anything like
that appears again, stop the task, answer the person, and give the German Telefonseelsorge (0800 111 0 111, 116 123; emergency 112).

How to write to them: short plain sentences; at most about 12 lines; no tables; metric units; each claim marked Fact (with a file,
link or command), Inference or Opinion; every message ends with `Where we are:` and `Next, if you say yes:`. No jargon. No recap
unless asked. When they are angry: answer the question asked, briefly, and work.

## 3. What they want (their words)

- "The whole point of this project is to control the Guinness while coming up on top of the bumps."
- "I want to see real fluid with real spillage, a real stout, beautiful looking foam, the top head of it, working its way across
  these bumps, losing quantity of the foam in the first place as well."
- "I don't want to see any slow animation." "I don't want to see any weird peaks."
- "JAX ONLY. No Taichi, not even as a fallback."
- "Produce all data, absolutely all the data possible, using JAX on Kaggle's GPU", stored on Kaggle and on the site, played back
  in the browser from the stored data.
- Guinness lettering on the glass; a place to write or draw the road.
- Of the head: "It's thick. It doesn't produce any kind of waves … if you splash it onto someone, it leaves as a solid foam,
  more like. … If you walk and you bump into shit, you will not exactly find what you expect out of a fluid or out of a foam."
  And: "It's absolutely not a goddamn solid." It is a wet nitrogen foam.
- Of the model: "don't make them a bazillion parameters … We need to be beautiful with our mathematics, as Dirac describes."
- Later, the full controller (`notes/fig12/handoff-control-session.md`, section 11).

## 4. Where things stand, in six lines

1. A JAX solver exists and has run twice on Kaggle's T4 pair (62 to 111 ms per step on a 1.5 mm grid, a million particles).
2. Neither run's data is usable. Run 1 was water without a head. Run 2 had five coding faults and one modelling fault.
3. The corrected solver (commit `80f4700`: the head as a sheet that resists shear, a corrected surface read-out, larger lists,
   drops that land on the cart) has **never been executed**. It was only linted.
4. A free check for it is written (`tools/fig12/kaggle/gate_rest.py`) and has also never been executed.
5. The measured numbers for the stout, the head and the boundary layers are gathered and verified (`notes/fig12/research/`).
6. New drawing code draws real stored frames (glass, lettering, head, stout, drops); the page is half reworked on the branch;
   the live site is unchanged and still shows every fault.

## 5. Your first three moves, and nothing else before them

1. Read (section 1). Then tell the user in at most five lines what you read, where things stand, and ask the one question that
   blocks everything: **may the model be run on this session's CPU, coarse and for one simulated second, as a free check before
   each GPU launch?** Their last order was "who told you to run anything in this session"; their other order is no wasted GPU.
   The two collide for code that has never run. Do not choose for them.
2. Ask them, in the same message or the next, for what only they have: what a real pint does. When a full pint is jolted, does the
   top of the head stay level or tilt with the stout? Does the stout come out under the head or does the head go first? After one
   knock, how many swings? No paper answers this; the model's central prediction (the swing dies within a period) rests on it.
3. Run the gates of `02-launch-gates.md` in order, printing each PASS or FAIL. Only then propose run 3, with its budget in
   **quota seconds** (run seconds × 2: Kaggle charges both T4 cards), the quota read fresh.

## 6. Never

- Never launch code that has not passed Gate A and Gate B.
- Never code a physical term before writing its size against its competitor (Gate C).
- Never quote a budget in run seconds, or one built on a speed you did not measure for that code.
- Never put data under `public/` from a run that has not passed Gate E.
- Never execute anything without one line first: what, where, how long, what it costs.
- Never resolve a collision between two of the user's orders silently: name it and ask.
- Never say a thing works that you have not opened and looked at in this session.
- Never use Taichi. Never slow the animation. Never interpolate between runs. Never compute physics in the browser.
- Never ask for, print or store the Kaggle token. Never touch the Workers `phyein-usul` or `stellenrecherche`.
- Never merge to `main` before Gate F, and never without showing the user screenshots first.

## 7. The yes you need, and only these

A GPU budget (one budget, one yes, with the arithmetic); deploying code to the Worker `kaggle-bridge`; spending money; and, new,
the answer to the question in section 5. Everything else you do without asking.
