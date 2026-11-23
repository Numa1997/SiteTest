# State of the Kaggelize session for Fig. 2, Double Pendulum

Kept current at every step that changes what is live or what is left (CLAUDE.md). Branch `kaggelize/double_pendulum`.

- Aim: the page `public/simulations/Double Pendulum.html` plays runs computed once on Kaggle by `tools/sims/double_pendulum.py`.
- Rules of the task: work alone (no subagents, no Kaggelize workflow); commits as the last human author on main, no co-author or
  session lines; do not touch .github/, .claude/, tools/sims/pipeline.py, kaggle_sims.py, verify_live.py, tools/sims/agents/,
  public/data/sims/; launch nothing on Kaggle; stop after the build and wait for the user's yes before merging.
- Done: step 1, the study (`study.md`); the model written and run here (108 files, 17 635 750 bytes, 253 s on 2 CPUs).
- 23 Nov, later: page player, registry entry and note sections 7-9 drafted on the branch. The user objected to the cut
  controls (ω sliders, sand curve, 30° grid, 20 s runs): building is stopped until the user chooses between a fine grid stored
  in Cloudflare R2 and leaving Fig. 2 live. main and the live site are untouched; nothing deleted.
- Left (if the user says go): step 2 build (registry, page player, walkthrough, note, doc, German and Arabic pages, docs, inventory); step 3 show and wait;
  step 4 publish after the yes; step 5 final doc.
