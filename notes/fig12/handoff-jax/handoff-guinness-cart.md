# active-memory handoff: Guinness on a cart (Fig. 12, JAX on Kaggle)

**Handoff #1** · 2026-11-13 · Lineage: #1 (2026-11-13): JAX solver written and run twice on Kaggle, materials researched, new drawing code working on real data; two GPU runs produced no usable data; the corrected model has never been executed.

## 0. Instructions for Claude (read first)

You are continuing work from a previous chat. That chat is gone; this file is the complete context and the source of truth.

1. Read this whole file before replying.
2. Follow sections 3 (Style), 4 (Hard rules) and 5 (Corrections) in every reply, for the rest of this chat. They override your defaults.
3. Use the values in section 8 exactly. Never round, re-estimate, or "correct" them.
4. Do not suggest anything listed in section 7 (Changed / rejected) again unless the user brings it up.
5. Code word: None active. If the user types /amcodeword, start every reply with the phrase they choose (default "Yes Boss!").
6. Your first reply: at most 5 lines covering the goal, the current state, and the next step (section 11). Mention any files from section 13 that were not attached. Ask the questions in section 12 if there are any. End with "Ready to continue with <next step>?" Then wait for the user's go.

Read next, in this order, before any work (all in the repository `Numa1997/SiteTest`, branch `claude/nifty-lamport-iz5pua`):
`notes/fig12/handoff-jax/01-mistakes-and-rules.md`, `02-launch-gates.md`, `03-model-and-numbers.md`, then `CLAUDE.md`, `AGENTS.md`,
`notes/fig12/research/data-for-solver.md`, `notes/fig12/research/verification.md`, `notes/fig12/handoff-control-session.md`,
`docs/simulations/fig12-beer-slosh.md`, `docs/kaggle-pipeline.md`, `docs/usul.md`, `docs/styles.md`, `notes/STANDARD.md`.
The previous session read only the first two of the last eight. Do not repeat that.

## 1. Mission
- **Goal:** replace the live page https://phyeinusul.com/simulations/guinness-kaggle with a pint of Guinness on a one-wheel cart whose stout, head of foam, spill and cart are all computed with JAX on Kaggle's GPU, stored, and played back in the browser from the stored data. Later: the full controller, controlled and uncontrolled rides side by side.
- **Done looks like:** the user opens the live page and sees real stout with real spillage and a real, thick Guinness head working its way over the bumps and losing quantity; no slow animation; no "weird peaks"; Guinness lettering on the glass; a place to write or draw the road; every number computed on Kaggle; tested in a real browser at 360, 390, 1024 and 1440 px.
- **Why it matters / context:** "The whole point of this project is to control the Guinness while coming up on top of the bumps."

## 2. About the user (as relevant to this work)
- The site owner. In anything written outside the chat call them "the user", never by name. Pronouns they/them.
- BSc in physics, computational and theoretical. Wants pictures from everyday experience and the mathematics (potentials, Lagrangians, derivations).
- Exhausted and very angry after four sessions failed them. Earlier that night they said, in anger, that they might hurt themselves. If any sentence like that appears, stop the task, answer the person first, and give the German Telefonseelsorge (0800 111 0 111, 116 123, emergency 112).
- They offered their own physical observations of a real pint (section 12). Use them: no published measurement of a sloshed pint exists.

## 3. Style & communication
- **Language:** English. Metric units only.
- **Tone:** plain, direct. No apologies at length, no defending, no flattery, no persuasion.
- **Reply length:** at most about 12 lines per chat message.
- **Formatting:** no tables in chat. Mark claims **Fact** (with a handle: file and line, link, or a command), **Inference**, or **Opinion**. Define each term at first use. End every message with `Where we are:` (one sentence) and `Next, if you say yes:` (one sentence).
- **Working style:** one step per turn; one decision at a time; build when the request is clear.
- **Avoid:** jargon ("smoke run" enraged them), option lists for things already decided, long status dumps, appended checkpoints or recaps when they are angry, "shall I proceed?" for work already ordered.

## 4. Hard rules (word for word)
1. "never use american units."
2. "JAX ONLY. No Taichi, not even as a fallback."
3. "no fucking smoke runs" (no throwaway GPU runs; every GPU run must be one whose result is needed).
4. "I don't want to see any slow animation."
5. "I don't want to see any weird peaks."
6. "Why the fuck are you running in this session? Who told you to run anything in this session?" (they forbade running the model in the chat session; see section 12, question 1: this collides with rule 3 and must be settled first.)
7. "Use the goddamn numbers you have at hand." "I don't care about your validation or verification right now." (said when source checks were blocked by crawlers; the numbers are in section 8.)
8. "don't make them a bazillion parameters. We can turn an ant to an elephant with a bazillion parameters. … We need to be beautiful with our mathematics, as Dirac describes."
9. "It's absolutely not a goddamn solid." (the head is a foam: gas bubbles in films of stout; never call it a solid.)
10. The user's yes is needed ONLY for: a GPU budget (one budget, one yes, with the arithmetic and the quota read fresh), deploying code to the Cloudflare Worker `kaggle-bridge`, and spending money. Everything else is done without asking.
11. Never ask for, print, log or store the Kaggle token. Kaggle notebooks stay private.
12. Never touch the Cloudflare Workers `phyein-usul` (the website) or `stellenrecherche`.
13. Never claim anything about the page, a result or a number that you have not opened or run yourself in this session. Look at screenshots (360, 390, 1024, 1440 px) before saying it works; show the user screenshots before each publish.
14. Do not message other sessions except a research session you start yourself on the user's word.
15. No model names in code, commits or pull requests.

## 5. Corrections log
| # | Claude did | The user wanted |
|---|---|---|
| 1 | Asked for a GPU budget for "smoke runs" built on the old solver's speed | No throwaway runs; "solve the god damn system already" |
| 2 | Began inventing foam constants (collapse rate, lacing thickness, bubble size) before any research | Measured numbers first; a research session gathered them |
| 3 | Called the head "a soft solid that floats on the stout" | Look it up: it is a wet nitrogen foam, not a solid |
| 4 | Launched run 1 as a plain port: water's viscosity, no head | "wtf have you been running": only the right model on the GPU |
| 5 | Ran a two-frame code check in the chat session without saying so first | "what and where are you running": say what runs where, before it runs |
| 6 | Kept checking sources while crawlers were blocked | "Use the goddamn numbers you have at hand." |
| 7 | Launched run 2 with code that had never been executed; found its bugs after the GPU time was spent | Find mistakes before computing, not after |
| 8 | Gave GPU budgets in run seconds; Kaggle charges both T4 cards, so the real cost was double | Budgets must be the real quota cost |
| 9 | Put run 2's faulty data in `public/data/fig12/2026-11-13/` on the branch | Incorrect data must never be near the site (moved to `notes/fig12/jax/run2-data/`) |
| 10 | Appended a long recap to a reply while the user was furious | Short answers; "fuck off and keep working" |
| 11 | Did not read the handoff brief's reading list (five documents) | Read first, in the order given |

## 6. Decisions
| Decision | Why |
|---|---|
| JAX on Kaggle's GPU for everything computed | user's order |
| The stout is single-phase, Newtonian, rho 1007 kg/m³, mu 2.06 mPa s | measured (section 8); a settled pint has under 0.1 % gas |
| The head is a wet foam from the stout's own bubbles; its behaviour follows from R32, liquid fraction, surface tension and surface elasticity | few parameters, all measured or derived (rule 8) |
| A separate research session gathers numbers; the working session reads all of it before modelling | user's order |
| The page plays stored frames in real time, never slows, never interpolates, offers only computed rides | user's order |
| The lettering is the word GUINNESS in Instrument Serif plus an original harp drawn from strokes | house font rule; no trademark image pasted |

## 7. Changed / rejected
- Taichi solver (`tools/fig12/kaggle/solver.py`) → JAX solver (`stout_jax.py`). ❌ Taichi even as fallback.
- "Smoke runs" → every launch is a needed run, preceded by free checks (see `02-launch-gates.md`).
- Water's viscosity 1e-6 m²/s → stout's 2.05e-6 m²/s.
- Head as a drawing → head as a computed layer. ❌ Head as "a solid".
- Head gripping only its edge on the glass (run 2) → head as a sheet that resists shear over its whole thickness (code at `80f4700`, never executed).
- Guessed head numbers (R 50–60 µm, liquid fraction 0.20, gamma 0.045) → R32 34 µm, liquid fraction 0.27, gamma 0.0442 N/m, E∞ 0.0187 N/m.
- ❌ Gemini's "drained liquid fraction 0.05–0.15" and "head bubble radius 50–60 µm" (rejected by the research).
- ❌ Robinson's bubble diameter 94–122 µm (settling time contradicts it); "r = 61 µm" in the Huddersfield table is that diameter misused as a radius.
- The old page's slowing near the edge of computed data, hollow "not computed" stops, browser preview solver → removed.
- Budgets in run seconds → budgets in quota seconds (run seconds × 2).

## 8. Data & facts (exact)
All numbers with their status are in `notes/fig12/research/data-for-solver.md`; the essentials:

| Quantity | Value | Source |
|---|---|---|
| Stout density, 5–6 °C | 1007 kg/m³ | Benilov, Cummins & Lee, arXiv 1205.5233 sec. II (measured) |
| Stout viscosity, 6 °C | 2.06e-3 Pa s (nu = 2.05e-6 m²/s) | same |
| Surface tension, degassed Guinness, 20 °C | 44.2 mN/m | Völp & Willenbacher, Soft Matter 17, 3937 (2021), Table 2; read by the previous session in the KIT copy; DOI 10.1039/d0sm02246b (the research note prints a wrong DOI) |
| Surface dilatational elasticity | 18.7 mN/m | same row |
| Head thickness as served | 18–20 mm (19 used) | Nature Reviews Physics 5, 197 (2023) |
| Bubble diameter | mean 61 µm, log-normal sigma 0.24 → Sauter radius R32 = 34 µm | Watamura 2019 SI; derived |
| Head liquid fraction | 0.27 (0.24–0.36) | derived, not measured |
| Head density | 272 kg/m³ | 0.27 × 1007 |
| Head modulus, yield stress | G0 = 166 Pa, tau_y = 5.4 Pa | Völp law, (gamma + 2E)/R32 = 2400 Pa, prefactors 1 and 0.25, jamming 0.635 |
| Foam wall friction | Cantat 2013: sigma = Z (gamma/r_b)(6.82 Ca^(2/3) + 0.94 (l/r_m) Ca^(1/3)); Z = 0.18, l/r_m = 0.004 at liquid fraction 0.25 | predicts Viola 2016's measured alpha within 4–11 % (`wolfram/04_verification`) |
| First slosh mode, R = 39.1 mm, depth 125 mm | 3.42 Hz; Stokes layer 0.436 mm | derived |
| Damping ratio | wall 0.0051, with bulk 0.0055, plus skin or lid 0.0051 → 0.0107 | Bongarzone & Gallaire 2022 eq. 17, recomputed |
| Contact angle, Guinness on clean glass | static 28.5 ± 2.0°, receding 4.2 ± 2.4° | Hamlett 2015 (row order unconfirmed) |
| Glass | 296 radii every 0.5 mm; rim 147.5 mm; fill 125 mm; radius 39.1 mm at the fill; narrowest 27.7 mm at z = 30.5 mm; largest 39.3 mm | `public/scripts/guinness-glass.js` |
| Grid | 1.5 mm: 57 × 57 × 114 = 370,386 cells; 1,002,808 particles; stout 429.6 g; head 91.0 mL | run logs |

GPU and quota:
| Item | Value |
|---|---|
| Weekly quota | 108,000 s, resets Saturday 14 Nov 2026 00:00 UTC |
| Quota used at 01:45 UTC | 18,243 s |
| Quota used at about 03:55 UTC | 23,029 s |
| Run 1 (notebook version 1) | 1,503 s of running |
| Run 2 (version 2) | 890 s of running |
| Charged for both | 4,786 s = 2 × 2,393 s: Kaggle charges both T4 cards |
| Approved by the user | 2,700 s (taken as run seconds; spent 4,786 quota seconds) |
| Speed | 62–111 ms per 2 ms step at 1.5 mm; rest 62.6, free swing 76.2, hard slosh 111.4 |

Run 2 results (faulty model, for the record): ride over five 20 mm bumps at 1.0 m/s: 9.04 g of stout over the rim, 11.58 mL of head, lean up to 32.5 mm, cart speed 0.944–1.051 m/s; impulse on the cart −0.00057994 N s against the stout's momentum +0.00057995; free swing 3.3375 Hz, damping ratio 0.0255. Run 1 (water, no head): 3.289 Hz, 0.0169; without any friction 3.327 Hz, 0.0200 at 1.5 mm, 0.0229 at 2 mm, 0.0487 at 3 mm.

## 9. People, terms & names
- **People:** the user (site owner).
- **Terms & nicknames:** "the head" = the foam on the stout; "the body" = the stout; "daughter session" = the research session `session_01DGmqiqdB1Z4JbSB3tyEpLZ` ("Guinness: body, head and boundary layers"), finished; "Taichi" = a programming library, not a method or a person; "Guinness cart page rebuild" = the previous working session.
- **Names in use:** repository `Numa1997/SiteTest`; live branch `main`; work branch `claude/nifty-lamport-iz5pua`; research branch `claude/guinness-materials-research` (last commit `b8a3e09`); Kaggle user `numakoudsie`, notebook `guinness-on-a-cart-stout-in-jax` (slug must be passed as `numakoudsie/guinness-on-a-cart-stout-in-jax`); private Drive folder "Guinness research videos" (id 14BjGMr_hyN7_nZa3Q4tiMx-QpLOfivQN).

## 10. Work state
| Item | Status | Version / location | Notes |
|---|---|---|---|
| JAX solver | draft, NEVER EXECUTED in its current form | `tools/fig12/kaggle/stout_jax.py` at `80f4700` | new since run 2: `head_sheet`, corrected `surface`, landing of drops, larger lists. Only linted. |
| Run script | draft | `tools/fig12/kaggle/run_b.py` | five tasks; writes .npz per task and `summary.json` |
| Notebook cell | must be re-pinned | `tools/fig12/kaggle/nb/run_b_cell.py` | still pinned to `afe5212` (run 2) |
| Packer | works | `tools/fig12/kaggle/pack_ride.py` | packs .npz into the page's JSON; packing should move into the Kaggle run so the site file equals the Kaggle file |
| Drawing code | works on run 2's data, seen at 900 px only | `public/scripts/stout-view2.js` | drops drawn as a cloud of dots; no test at 360/390/1024/1440 px yet |
| Player | written, never run in a browser | `public/scripts/guinness-jax-play.js` | expects `public/data/fig12/2026-11-13/index-jax.json`, which no longer exists there |
| Page | half reworked, branch only | `public/simulations/guinness-kaggle.html` | figure and controls changed; lecture note below still describes the old data; data panel removed and not rebuilt; no road-drawing control |
| Test page and screenshots | works | `notes/fig12/jax/view-test.html`, `shots.cjs` | needs `python3 -m http.server 8765` at the repository root |
| Run 2 data | faulty, kept off the site | `notes/fig12/jax/run2-data/` | never publish |
| Research | finished | `notes/fig12/research/` | `data-for-solver.md`, `guinness-materials.md`, `verification.md`, `sources/`, `wolfram/`, `sympy/` |
| Live site | unchanged | https://phyeinusul.com/simulations/guinness-kaggle | all eight faults of the old brief still live |
| Controller port | never run | `tools/fig12/control/cartctl.py` | from the session before |

## 11. Next steps
1. **Next action:** get the user's answer to question 1 of section 12, then run the gates of `02-launch-gates.md` on the code at `80f4700` before any GPU launch.
2. Launch run 3 only after the gates pass and the user approves a budget in quota seconds.
3. Look at run 3's frames in a real browser; fix; then size the data runs (roads that spill, many speeds) from the measured speed and ask once.
4. Finish the page: data panel, road input, lecture note to `notes/STANDARD.md`, docs, catalogue, four widths, then merge and verify live.
5. Then the full controller.

## 12. Open questions ⚠️
1. May the model be run in the chat session on the CPU, on a coarse grid, for one simulated second, as a free check before each GPU launch? Candidates: yes (recommended: it would have caught every coding bug of run 2 at no GPU cost) / no (then every check costs GPU time, which collides with "no smoke runs").
2. The user's own observations of a real pint, which no paper gives: when a full pint is jolted, does the top of the head stay level or tilt with the stout? Does stout come over the rim under the head, or does the head go first? After one knock, how many swings before it is still?
3. Head liquid fraction 0.27 and bubble radius 34 µm are derived, not measured. Accept, or measure (weigh a scoop of head; macro photo with a scale)?

## 13. Re-attach checklist
- [ ] `01-mistakes-and-rules.md`: the previous session's mistakes and the rule that prevents each
- [ ] `02-launch-gates.md`: what must pass before any GPU launch
- [ ] `03-model-and-numbers.md`: the physical model as coded, what is checked and what is not
- [ ] The user's file `guinness_stout_physics_dataset_and_photo_directory.md` (already kept in `notes/fig12/research/sources/gemini-dataset-2026-11-13.txt`)
- Everything else is in the repository on branch `claude/nifty-lamport-iz5pua`.

---
<sub>Audit: 13/13 sections · 15 rules · 11 corrections · 40 data points · secrets removed: none found · generated by active-memory</sub>
