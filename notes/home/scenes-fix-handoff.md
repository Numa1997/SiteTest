# Home page scenes: what was added, what is wrong, and the handoff to fix it (23 November 2026)

## Part 1. What Claude sessions added to the home page, and when

All of it lives in two files, `public/scripts/bg-scenes.js` (505 lines) and `public/styles/bg-scenes.css`, placed by `<div data-bg="…">`
holders in `index.html` (lines 29, 299 and 688) and in the German and Arabic copies. The full description is `docs/scripts/bg-scenes.md`.

| Date | Commit | What was added |
|---|---|---|
| 18 Nov 13:22 | e18f184f | "Living scenes": ten small animations (dust, seeds, falling atoms, shores, forest, iron powder, harmonica, spinners, mixing gas, chip), each in its own spot on four pages |
| 18 Nov 14:50 / 15:15 | 2794e575, 8ff82a39 | The chip beside the Projects title, the iron powder beside the Simulations title |
| 18 Nov 17:09 | 4d018708 | The strip under the home hero becomes soil with roots and a fungal network |
| 18 Nov 22:03 | 253826bc | The forest: one tree spreads over the land, four seasons, vapour, clouds, rain and snow |
| 20 Nov 19:40 | 45107e26 | The side margins of the home page: roots growing down on the left, Barton's pendulums on the right |
| 20 Nov 22:06 | 2c3b80d3 | The pendulums are no longer computed in the browser: they play `barton.bin`, computed once on Kaggle by `tools/sims/barton.py` |
| 21 Nov 21:11 | 16f5d20a | One line for every simulation in the Kaggle workflow |

## Part 2. What is wrong (the user's complaints, checked on the live site on 23 November 2026 at 1920 × 1080)

1. **The trees grow too fast.** Measured from the code: a year lasts 40 s (`YEAR: 40`, bg-scenes.js line 178); a seedling is fed
   `dt * need / 6`, so it is grown in about 6 s of spring and summer (line 241), that is about 12 s of real time; every grown tree
   may plant a new one at a rate of 0.25 per second (line 239). The forest fills the land in about 80 s. A reader sees trees shoot up.
2. **The pendulums look creepy and fast, and they do not hit each other or exchange momentum.** They are Barton's pendulums
   (`tools/sims/barton.py`): lengths 0.10 to 0.34 m, drawn at 420 px per metre, played in real time at 30 frames per second.
   The period is 2π√(L/g): 0.63 s for 0.10 m and 1.17 s for 0.34 m, so they swing one to two times a second. They are thin lines
   with small dots, and the light ones never touch each other; they only feel the driver through the shaking bar, which a reader cannot see.
3. **Big empty areas in the top left and top right.** In the screenshot at 1920 × 1080: left of the hero text, x 0 to about 410 px,
   y 0 to about 540 px, holds only a few dust specks; right of the poem and the Fig. 0 card, x about 1510 to 1920 px, y 0 to about
   870 px, holds only one small sprout. The forest places tall trees only where no text stands above (`room()`, line 182, and the
   `data-bg-avoid` list on `index.html` line 29), and nothing else fills those corners. Nothing on the page says why.
4. **No explanation anywhere on the page** of what the scenes are or why they look as they do.

## Part 3. The handoff (prompt for one Claude session; paste it as is)

THE TASK
Fix the home page's background scenes of Phyein Usul (repository Numa1997/SiteTest, live https://phyeinusul.com, published by
Cloudflare from main). Read this file first: notes/home/scenes-fix-handoff.md, Parts 1 and 2 are the facts. Then CLAUDE.md, AGENTS.md,
docs/scripts/bg-scenes.md, docs/kaggle-sims.md, tools/sims/barton.py and public/scripts/bg-scenes.js.

RULES
- Work yourself, in this session. No subagents.
- Refer to the user as "the user". Commits in the name and e-mail of the last human commit on main, no Claude attribution anywhere.
- Measure, never guess: screenshots and a short filmstrip in headless Chromium at 1920, 1600 and 1100 px (home page, top and
  the margins after scrolling 900 px), before and after.
- Another session may be editing tools/sims/registry.json, docs/kaggle-sims.md, notes/sims/PLAN.md, tools/inventory.py and
  docs/files.md at the same time: fetch and rebase before merging, keep their lines, regenerate docs/files.md with python3 tools/inventory.py.
- Do not open the user's Gmail, Calendar, Drive or other personal connectors. Create, fire or delete no scheduled tasks.
- Clean up: delete scratch files and temporary branches when done; say what you deleted and kept.

STEP 1. THE FOREST: slower and calmer. Lengthen the year and the growth so that a tree takes about a minute to grow and the land
fills over several minutes, not 80 s. Keep every parameter named at the top of the scene. Film 60 s before and after.

STEP 2. THE PENDULUMS: they must look like real pendulums that visibly exchange momentum. Replace Barton's pendulums with a system
whose exchange the eye can follow, generated once on Kaggle through the existing line (a new model in tools/sims/, an entry in
registry.json, the page plays the stored data; never compute it in the browser). Two candidates, choose one and say why in the
study note: (a) a Newton's cradle, steel balls on two strings each, whose collisions pass the momentum along the row; (b) two or
three pendulums tied by a weak spring, where the swing moves from one to the other and back (beats). Longer pendulums (about 1 to 2 m
drawn at a smaller scale) give periods of 2 to 3 s, which reads as calm; do not slow the playback below real time, because that
would show wrong physics. Heavier bobs and strings that a reader can see. Write the model with its equations in the docstring,
parameters as symbols, the checks (energy and momentum kept at each collision, or the beat period against 2π/(ω₂ − ω₁)).

STEP 3. THE EMPTY CORNERS: fill the top left and top right beside the hero with something that belongs to the forest and its
weather (for example the clouds and rain the forest already makes, grown into those corners, or tall trees that the avoid list
now forbids there), and say in the scene's comments and in docs/scripts/bg-scenes.md why each corner looks as it does.

STEP 4. EXPLAIN THE SCENES ON THE PAGE: one short, plain sentence per scene that the reader can open (a small "what you see"
note in the house style, docs/styles.md), saying what the picture shows and what physics drives it. In English, then German and
Arabic through tools/i18n/build.py.

STEP 5. TEST AND STOP: npm run build, headless Chromium at 1920, 1600, 1100 and 390 px, no console errors, no sideways scroll,
reduced motion still mounts nothing. Show the user the before and after screenshots and the filmstrips, and WAIT for their yes.

STEP 6. PUBLISH (after the yes): pull request into main; for the new pendulum model watch the workflow "Simulations on Kaggle"
put the data commit on main and the live page play it (generations.json lists it, SHA-256 matches). Update docs/scripts/bg-scenes.md
and docs/kaggle-sims.md to say what the code now does. Report briefly: what changed, the measured result, what is left.