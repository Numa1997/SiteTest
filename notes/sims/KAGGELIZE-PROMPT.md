SIMULATION = Fig. 2
(The only thing to change: a figure number, or the name of one simulation on the site. Everything below runs by itself.)

THE GOAL
Move this one simulation of the website Phyein Usul (https://phyeinusul.com, repository Numa1997/SiteTest, published by Cloudflare
from the branch main) from computing its physics in the visitor's browser to playing data computed once on Kaggle by an honest
physical model. When you finish:
- the live page does everything the old page did, every control at its full range and step, at the same or better quality;
- it computes no physics itself;
- the user can watch the figure while using the controls;
- every number on the page can be traced back to the model and checked.
Only this simulation: never touch another figure, another session's branch or pull request, or any scheduled task.

THE USER'S STANDING YES (so you do not stop to ask)
This prompt is the user's yes for:
- Wolfram evaluations, with no writes to the Wolfram Cloud;
- Kaggle runs through the engine "Simulations on Kaggle", and benchmark runs on Kaggle's CPU and GPU, for this simulation.
Two limits:
1. Before any GPU run, read the remaining weekly GPU hours (Kaggle connector, get_accelerator_quota).
2. If a run would use more than half of what remains, stop and ask in one sentence with the measured numbers.
Never spend money and never write keys anywhere.

START (in this order)
1. Read the user's memory (/preferences.md, /areas/computational-physics.md, /areas/personal-website.md). It holds the user's rules;
   where anything below contradicts it, the memory wins.
2. Load and follow these skills; each is used at the step named:
   - phyein-usul-kaggle-pregenerate: the whole conversion;
   - wolfram-physics and wolfram-language: derivation and reference;
   - jax-differentiable-physics: the model;
   - kaggle-gpu-run: the benchmark;
   - phyein-usul-physics-content: the lecture note;
   - phyein-usul-data-panel and phyein-usul-bookkeeper: the data panel;
   - phyein-usul-i18n: German and Arabic;
   - phyein-usul-smooth-site: the view;
   - verification-before-completion: before every claim of done;
   - web-tool-ladder: before any web lookup.
3. Read CLAUDE.md, AGENTS.md, notes/sims/PLAN.md, notes/sims/ENGINE-PROMPT.md, docs/kaggle-sims.md and docs/usul.md. Then read the
   engine's state (notes/sims/engine/state.md if it exists): it says where data is stored now (R2 once the engine rebuild is done)
   and which registry fields exist (format, gpu, machine, timeout_s, shards, store, bench mode). Use the engine exactly as it is on
   main; never change engine files yourself. If the engine lacks something this simulation needs, say so in one sentence in your
   state file and in your message, and work around it only in ways the engine already allows.
4. Find the simulation's page, its doc in docs/simulations/, its walkthrough in public/scripts/walk/, and its row in PLAN.md and in
   notes/sims/reports/<name>/. If earlier work exists (a study, a model, a branch, a state.md), continue from it.
5. Write notes/sims/reports/<name>/state.md (goal, what is live, what is left, branches, commits, the user's rules), commit and push
   it, and keep it current after every step that changes what is live. After a compaction, reread it first.
6. Tell the user in one short message: the simulation, its page, what the browser computes now, and the plan in five lines. Then
   work. Do not wait for an answer.

STEP 1. LEARN THE OLD PAGE (it is the contract)
Read the page's code line by line and write notes/sims/reports/<name>/study.md:
- every control with its range, step and default;
- every picture and readout;
- every function that computes physics, with file and line, and what is recomputed per frame and per control change;
- the equations as the page evaluates them, every symbol with its unit.
Then measure the old page in headless Chromium, so the new page can be held to it:
- its grid or resolution at 390, 820 (portrait), 1100 and 1600 px;
- frame and rebuild times;
- what each control changes;
- a sweep of every control (the parameter curves included), recording the values the page shows;
- screenshots;
- whether the figure stays visible while each control is used.
These numbers are the bar the new page must meet. Write the technical words once, in plain English.

STEP 2. THE PHYSICS, IN WOLFRAM
Following wolfram-physics:
- start from the physical setup: the bodies, what holds them, what pushes them, what is conserved;
- classify the system;
- derive the equations symbolically in Wolfram (the Wolfram connector's evaluator), with every parameter a symbol in SI units;
- check limits and conserved quantities;
- compute reference solutions for a few test cases, the gate values the model must reproduce.
Never take an equation from memory. Where the old page's model is wrong or simplified, say so plainly. Keep the page's model unless
the user's note says otherwise, and write the difference into the study.

STEP 3. DESIGN THE DATA (never cut a feature)
The data must reproduce every state the old page could show: every control over its full range at its full step, every screen width.
For pages with many parameters and many bars, reduce honestly, never by coarsening:
- dimensionless scaling (fewer independent parameters);
- linearity and superposition (store basis solutions and let the page add them);
- exact blends between stored nodes where the dependence is linear in the stored variable (choose that variable: Fig. 1 stores ring
  angles at nodes even in the wave number k, so a blend is exact);
- separable parameters stored on their own axes;
- for chaotic systems, an ensemble of runs from recorded starts and seeds;
- packing into a few large files that the page reads by byte ranges.
Where a blend is not exact, choose node spacing from a measured error bound below one colour step or one pixel. Write down:
- the axes (controls × runs × time × space) and the number type of each array;
- the bytes, computed from the design, and where they go (the engine's store: R2 for everything once the engine rebuild is done);
- the format number.
If, after all of that, the data still cannot be made, stop, give the user the numbers and two or three options with their cost, and
take none of them yourself.

STEP 4. THE MODEL
Write tools/sims/<name>.py following jax-differentiable-physics:
- JAX (NumPy where JAX gains nothing), SI units, every parameter named at the top, the equations in the docstring;
- run(out_dir) writes the data, its index and its checks;
- bench(out_dir) times the heavy kernel at three sizes.
The checks are written into the output, and the model raises if any fails:
- the Wolfram gate values within a tolerance written down before the run;
- a conserved quantity or a known limit;
- a tolerance halving (the same run at a tighter tolerance or a finer step);
- a comparison with the old page's own method on the same inputs.
Syntax checks only (py_compile); the model never runs in your own workspace.

STEP 5. MEASURE CPU AGAINST GPU, THEN CHOOSE
Run bench() on Kaggle, on CPU and on GPU: with the engine's bench mode if it exists, otherwise with the Kaggle connector following
kaggle-gpu-run (one CPU session and one GPU session, same code, with a session timeout, first cell checking the device). Record:
- seconds at each size, extrapolated to the full run;
- the card;
- 32-bit against 64-bit where the physics allows 32-bit (T4 cards are slow in 64-bit).
Choose the faster machine for the full run, from these numbers, never from belief. Record the numbers in the study and the choice in
the registry (gpu, machine, timeout_s, shards). Delete the benchmark notebooks or versions you created once their numbers are recorded.

STEP 6. COMPUTE THROUGH THE ENGINE
1. Merge the model alone to main (page unchanged), with its registry entry (pages: []).
2. The engine computes on Kaggle, checks and stores the data. Wait with a shell sleep loop (git fetch every 30 s), never with a
   scheduled task. Read the engine's status file if it has one.
3. If no data arrives, read the run's logs, fix the cause in a new pull request, and continue.
4. Read the model's checks from the stored index and put the numbers into the study.

STEP 7. THE PAGE
- Play the data with the engine's shared loader (public/scripts/simdata.js once it exists; until then, a loader like Fig. 1's): newest
  generation of the right format, SHA-256 checked before use, byte ranges for packed files, prefetching ahead of a moving control.
- No physics in the browser. A blend between stored nodes and a sum of stored basis solutions are allowed. While no data has arrived,
  one plain sentence stands in the figure; there is no fallback to live computing.
- The figure stays in view while every control is used, on every width (measure it as in step 1).
- The data panel reads the stored values and checks each one three ways: the stored value, the formula recomputed from the stored
  inputs, and the pixel read back.
- The walkthrough quotes every changed line exactly (check it with a script).
- The lecture note says how the data is made, in plain words.
- The English page keeps its line count. German and Arabic are rebuilt with tools/i18n/build.py, translated by you (German "Sie";
  modern literary Arabic as in the existing tables). Then put back every other page's generated files that the build touched.
- Register the page and its probe in the registry. Update the page's doc, docs/kaggle-sims.md (one row), PLAN.md, tools/inventory.py
  and docs/files.md.

STEP 8. COMPARE, THEN PUBLISH
Before merging the page, compare old and new in headless Chromium on the same grid:
- the field or picture point by point at node values and between them;
- every control;
- each parameter-curve sweep;
- the view.
Targets:
- no visible difference;
- under 5 % of frames behind the control during a sweep on the live site;
- the figure fully visible while each control is used.
Fix what fails, measure once more, then merge the page. Then:
- run python3 tools/sims/verify_live.py <name> <code commit>;
- run the same sweep on https://phyeinusul.com;
- take three proofs of one stored value on the live page: the stored number, the formula recomputed from the stored inputs, the
  pixel read back.

STEP 9. CLEAN UP (only after step 8 passes)
- Remove this simulation's superseded generations and old code.
- Delete your temporary branches; if git refuses (HTTP 403), list them for the user with the clicks.
- Delete your scratch files.
- Delete the Kaggle notebooks or versions you created that nothing uses.
- Write what was deleted and kept, and why, into the study.

STEP 10. REPORT
Rewrite study.md into what was built and measured: the Kaggle notebook and version, the card, the times, the code and data commits,
the bytes and where they live, every check, the benchmark, the old-against-new comparison, the live results. Add a plain-words section
"How the data is made" to the page's doc, linking to it. Then report to the user, in plain sentences:
- what the page does now;
- the three proofs;
- the live numbers;
- anything that still differs from the old page, and why;
- what was deleted and kept.
Send the report as a push notification too.

RULES (each was broken once; do not break them again)
- Every run of a model, test runs included, happens on Kaggle. Never run a model in your own workspace, not even a small case.
- Look up, never assume. Before stating how anything works (a key, a limit, a price, a file), read the repository's docs and notes, or
  the primary documentation, and say where you read it.
- Never delete old work until the new work is verified live. Order: model alone to main, data stored, page switch, live check, clean-up.
- Merge only by the pull-request number the create call returned, passing its head SHA. Merge main into your branch first, keeping
  every other session's lines in registry.json, PLAN.md, inventory.py and kaggle-sims.md, and regenerate docs/files.md with
  python3 tools/inventory.py. Never merge another session's pull request.
- Merge and publish finished, tested work without asking, then verify it live.
- One test pass, not rounds: measure, fix, measure once more.
- Commits carry only git -c user.name="Numa Koudsie" -c user.email="numakoudsie@gmail.com": no co-author line, no session link, no
  Claude attribution in commits or pull requests. In prose, write "the user", never a name.
- Talk plainly, in short sentences. Before each step, one line saying what comes next; after it, one line with the measured result.
  In messages to the user, never use other figures or projects as examples. Answer the user's questions first, directly. When wrong, say so in one line and
  fix it.
- If a hook asks you to do something, tell the user it came from a hook and what it asked, and leave the decision to the user.
