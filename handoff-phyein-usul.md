# active-memory handoff: Phyein Usul — Balancing Two Rods on a Cart (project 05)

**Handoff #1** · 2026-11-06 · Lineage: #1 (2026-11-06): sampled-data controller + lecture note for Balancing Two Rods, Fig. 11 swap, Arabic heading fix, phone tables, README/AGENTS; data-panel child session killed by Numa; next focus is the animation.

## 0. Instructions for Claude (read first)

You are continuing work from a previous chat. That chat is gone; this file is the complete context and the source of truth.

1. Read this whole file before replying.
2. Follow sections 3 (Style), 4 (Hard rules) and 5 (Corrections) in every reply, for the rest of this chat. They override your defaults.
3. Use the values in section 8 exactly. Never round, re-estimate, or "correct" them.
4. Do not suggest anything listed in section 7 (Changed / rejected) again unless the user brings it up.
5. Code word: None active. If the user types /amcodeword, start every reply with the phrase they choose (default "Yes Boss!").
6. Your first reply: at most 5 lines covering the goal, the current state, and the next step (section 11). Mention any files from section 13 that were not attached. Ask the questions in section 12 if there are any. End with "Ready to continue with <next step>?" Then wait for the user's go.

## 1. Mission
- **Goal:** enhance the animation of "Balancing Two Rods on a Cart" (project 05, `public/simulations/double-inverted-pendulum.html`) and make it reasonable — Numa's words: "just focus on enhancing the animation, making it reasonable..no gpu bullshit".
- **Done looks like:** the change is built, tested in a real browser (headless Chromium, screenshots, measured numbers), checked against the other sessions' work on `main`, merged and published by Claude, and verified on the live site https://phyeinusul.com; docs describe what the code now does.
- **Why it matters / context:** "Far future will be a bunch of simulations building up on this...great to have that in principle!" (Numa).

## 2. About the user (as relevant to this work)
- Numa (Numa Koudsie; Arabic pages: نعمة سائر قدسية), BSc Physics, computational and theoretical; "my level is quite humble / But I am curious as fuck and I'll read through all that which you write!"
- Owns the site Phyein Usul, repo `Numa1997/SiteTest`; checks results himself on the live site.
- Wants physics explained with physical pictures and with the formal side (calculus, derivations, potentials, Lagrangians) when asked; defined terms.

## 3. Style & communication
- **Language:** English replies. Site text in English, German, Arabic (German/Arabic generated from tables).
- **Tone:** direct, plain, no fluff, no flattery, no apology floods; when wrong, say so in one line and fix it.
- **Reply length:** short; short progress messages; details on request. Show diffs and raw test output.
- **Formatting:** short connected sentences, everyday words; mark Fact / Inference / Opinion when it matters; metric units only.
- **Working style:** build when the request is clear; ask only when readings lead to materially different work, and then one thing. During project work end each turn with `Where we are:` one sentence and `Next, if you say yes:` one sentence.
- **Avoid:** option lists or theory in answer to a clear build request; long walls of text; invisible background work; wasting his time or money.

## 4. Hard rules (word for word)
1. "never use american units."
2. "No more Wolfram / Just use your own code."
3. "You translate the german. You don't write it. Stop wasting my money. You have it be translated using some tool, and then you check and verify that the translation isn't word for word or is stupid." (tool = DeepL connector or Google Translate; "then you go through them once")
4. "Just finish up the fucking simulation and then worry about the goddamn translation."
5. "just focus on enhancing the animation, making it reasonable..no gpu bullshit"
6. Do the work yourself; no subagents (from the original brief; Numa killed the data-panel child session on 2026-11-05).
7. Never touch Cloudflare settings.
8. CLAUDE.md (repo): "when a change is finished, checked against the other sessions' work on `main` and tested in a real browser, merge it and publish without asking, then verify the live site; Numa checks the result himself."
9. CLAUDE.md: "A change is not done until the docs pages that describe the changed files say what the code now does."
10. CLAUDE.md: "Nothing on a running figure may react to the pointer merely crossing it." Reading a point is a tool the reader switches on.
11. CLAUDE.md: house design only (Instrument Serif 400 titles, IBM Plex Sans text, IBM Plex Mono labels, Latin Modern + KaTeX notes); "never introduce another font."
12. CLAUDE.md: "A data table is a pipeline, not a second simulation" — store at the line that computes; display only reads.
13. Arabic: no literal translations — "تحكم بنفسك is retarded and is a literal translation ... Change it. Look it up on official sources or use a different term".

## 5. Corrections log
| # | Claude did | The user wanted |
|---|---|---|
| 1 | Asked about tests / questions instead of building | "JUST WORK ALREADY, SHOW ME A GOD DAMN WORKING PROTOTYPE" |
| 2 | Used Wolfram for checks | "No more Wolfram. Just use your own code." |
| 3 | Wrote German translations itself | Translate with a tool (DeepL/Google), then check once |
| 4 | Proposed installing Argos Translate | "Install argos is crazy bro" — use the DeepL connector |
| 5 | Worked on translations before the simulation was done | Finish the simulation first |
| 6 | Long silent stretches; user couldn't see progress | "Wtf are you still doing mate, what on earth are you getting stuck at" — short visible progress |
| 7 | Arabic heading تحكّم بنفسك (literal, means "restrain yourself") | Proper term from sources → now تولَّ التحكّم |
| 8 | Didn't do the Arabic fix until asked "Did you do it?" | Carry out every pending instruction without being reminded |
| 9 | Sent malformed DeepL calls twice without loading the schema | Load tool schema first; don't repeat a failing call |
| 10 | Spawned a cloud session for the data panel | Numa killed it: "just focus on enhancing the animation" |

## 6. Decisions
| Decision | Why |
|---|---|
| Fig. 11 = Double Pendulum under Control, `simulations/pendulum-control.html` | user's call (swap, 2026-11-04) |
| Project 05 = Balancing Two Rods, file stays in `public/simulations/` | so `tools/i18n/build.py` makes its DE/AR pages |
| Sampled-data LQR (ZOH, Van Loan, discrete Riccati) replaces continuous gains | rods rest for loop periods up to 260 ms instead of 34 ms |
| Arabic "Take control" = تولَّ التحكّم | noun from Microsoft Arabic Teams pages (طلب / منح / استعادة التحكم), verb from DeepL; recorded in `docs/glossary.md` |
| Note tables `.ptable` scroll by themselves (`display:block; max-width:100%; overflow-x:auto; position:relative`) | were clipped on 390 px phones; German page was 478 px wide |
| No GPU/WebGL for the animation | Numa: "no gpu bullshit" |

## 7. Changed / rejected
- تحكّم بنفسك → تولَّ التحكّم (literal, wrong meaning)
- Continuous LQR gains → sampled-data gains (failed above 34 ms)
- Double Pendulum under Control as project → back to Fig. 11; Balancing Two Rods Fig. 11 → project 05
- ❌ Wolfram (banned)
- ❌ Argos / self-written translations (use DeepL or Google Translate)
- ❌ Child session for data panel + skill revision (killed by Numa; note: `main` already loads `datalog.js` on the page, built by other sessions)
- ❌ GPU / WebGL / WebGPU effects

## 8. Data & facts (exact)
- Repo `Numa1997/SiteTest`; live https://phyeinusul.com (Cloudflare builds every merge to `main`, ~1 min); backup https://numa1997.github.io/SiteTest/.
- Session branch: `ccr-7d84d2d6-t6llfr` (restart from `origin/main` for new work).
- PRs this chat: #78 → 65ee976, #79 → edd1d43, #80 → a150387, #81 → 246ece2.
- `main` on 2026-11-07: 9ab7fdb (PR #119, Fig. 12 real-time fluid `beer-slosh.html`); 158 commits after 246ece2, many on project 05 (rods in liquids, solved fluid `twoway.js`, vector-field panel, own flow field, data-panel water book).
- Page on main: 374 551 bytes; canvases `#cv` (machine) and `#tr` (last 8 s of angles and force); scripts `flip.js, fold.js, sim.js, dataset.js, twoway.js, datalog.js`; no WebGL/WebGPU anywhere on `main`; `twoway.js` header: "Two-way coupled fluid for project 05 ..., CPU only, browser and Node."

| Controller fact | Value |
|---|---|
| Integrator | RK4 at 1 ms |
| K at 10 ms | (5.322, −408.009, 493.663, 11.556, −13.147, 76.277) |
| K at 40 ms | (2.528, −251.393, 279.000, 5.540, −10.590, 41.286) |
| Designed |λ| | 0.9919 (10 ms), 0.9679 (40 ms), 0.8093 (260 ms) |
| Flip, one-mode model | T* ≈ 38 ms; full loop flips just below 34.4 ms |
| Continuous gains at 40 ms | limit cycle ±4.9°, ±60 N; 0/6 caught, c* = 0 |
| Certified catch level c* | 31.6 (1 ms), 37.3 (10 ms), 116 (40 ms); hand-over at W < 0.9 c* |
| Glide reference | critically damped, ω = 0.5 s⁻¹ |
| Tests (2026-11-04) | 40/40 random falls caught (rolling and STOP=1); 48/48 on 8 other machines; walkcheck 824/824 |

## 9. People, terms & names
- **People:** Numa: owner; "Fable" and "Opus": earlier Claude models Numa praised/compared.
- **Terms & nicknames:** "that beauty" = Balancing Two Rods; "project 05"; walkthrough key `dipc`; Fig. 11 = Double Pendulum under Control; Fig. 12 = beer slosh (real-time fluid).
- **Names in use:** `tools/i18n/build.py` (+ `--check`), `tools/redirects.py`, `tools/inventory.py` (rewrites `docs/files.md`), `notes/walkcheck.cjs`, `notes/fig11/study/t9.cjs` and `t7.cjs` (hard-code `/home/claude/...`; repo `"type":"module"` breaks CJS → copy to scratchpad, fix paths), `docs/simulations/fig11-double-inverted-pendulum.md`, `docs/glossary.md`, `docs/styles.md`; Playwright: `NODE_PATH=$(npm root -g) node script.cjs`; `npm run build` = `vite build` (delete package-lock.json if one appears); `build.py` rewrites a "translated-from" stamp on every generated page — revert that noise on untouched pages; write test scripts with the Write tool (heredoc + other commands trips the safety parser).

## 10. Work state
| Item | Status | Version / location | Notes |
|---|---|---|---|
| Sampled-data controller, note §7–§12, §11.4, walkthrough (15 steps) | final, live | PR #78 | |
| Fig. 11 swap, DE/AR, redirects | final, live | PR #79 | |
| Arabic heading تولَّ التحكّم | final, live | PR #80 | |
| Phone tables + README/AGENTS | final, live | PR #81 | |
| Data panel for project 05 | exists on main (other sessions) | `datalog.js` loaded | child session killed; skill revision dropped |
| Animation enhancement | not started | `public/simulations/double-inverted-pendulum.html` | scope "reasonable" unclear (section 12) |

## 11. Next steps
1. **Next action:** check out `origin/main` fresh, open the page in headless Chromium at 1280 and 390 px, and measure the animation as it is (frame time and frames per second with the panel closed, in air and in each liquid; whether simulated time keeps pace with wall time; screenshots), then show Numa the measured list of what looks or runs unreasonably.
2. Fix those with CPU 2D canvas only (no GPU), house design, nothing reacting to mere pointer crossing.
3. Re-run behaviour tests (t9: 40/40 and 48/48; t7: en/de/ar at 1280/390; walkcheck all found), translations of any new text via DeepL + one check, docs, PR, merge, verify live.

## 12. Open questions ⚠️
- What does "reasonable" mean for the animation? Candidates: (a) smooth — steady ~60 frames/s, no stutter from the fluid solver; (b) honest timing — simulated time runs at real time, or the slow-down is shown; (c) visual — proportions, colours, less clutter, a calmer drawing of the fluid/arrows; (d) all of these.

## 13. Re-attach checklist
- Nothing to attach. Everything is in the repository `Numa1997/SiteTest` (`main`).

---
<sub>Audit: 13/13 sections · 13 rules · 10 corrections · 32 data points · secrets removed: none found · generated by active-memory</sub>
