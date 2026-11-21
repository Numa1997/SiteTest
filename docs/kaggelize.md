# Kaggelize: one button that moves a simulation to data computed once on Kaggle

Written 21 November 2026. Nothing here has run on GitHub yet: the parts were tested in the workspace with a stand-in for the
Claude session (see "Tested"). The first real run is the trial on one simulation.

## What it is for

Many simulations of the site still compute in the visitor's browser. The goal ([notes/sims/PLAN.md](../notes/sims/PLAN.md)) is
that each one is computed once on Kaggle, stored in this repository, and only played by the page. The carrying is already
automatic: the line "Simulations on Kaggle" ([docs/kaggle-sims.md](kaggle-sims.md)). What is left for each simulation is
thinking work: understand the page and its physics, decide which numbers must be stored, write the model, change the page into
a player, and check the result. Kaggelize hands that thinking to Claude Code sessions, and keeps the owner in charge of every
step that matters.

Picture a workshop with a foreman's checklist on the wall. The checklist (the workflow) is fixed and anyone can read it. Three
craftsmen (the sessions) each do one kind of job and hand their piece back to the checklist. Between the jobs there are two
doors that only the owner can open.

## The flow for one simulation

```
You: Actions -> Kaggelize -> Run workflow -> titles: "Wave Interference"
        |
        v
  Study            builder session: reads the page, writes 01-study.md (a lesson and a plan). No code.
        |
  PAUSE 1          you read the study on the board's link, then Approve or Reject on the run page
        |
        v
  Build            builder session: model, registry entry, player, docs, 02-build.md, on a branch
        |
  PAUSE 2          you read the changes (the board links the comparison with main), then Approve or Reject
        |
        v
  Kaggle line      automatic: Kaggle computes, SHA-256 check, branch and data go to main together, live check
        |
        v
  Caretaker        second session: reads the reports, reruns checks, inspects the data and the live page
        |
   clear ---------> board: done
   not clear -----> Correction (third session) -> PAUSE -> Kaggle line -> Caretaker
                    at most two corrections; after that the board says "needs you"
```

Nothing reaches Kaggle, `main` or the live site before PAUSE 2 is approved. Until then everything a session wrote sits on a
branch named `kaggelize/<short name>`.

## The words

- **Workflow**: a list of steps GitHub runs on its own machines, written in a file in `.github/workflows/`. Here it plays the
  "mother": it starts each session and decides what comes next. It is plain code, not a session.
- **Session**: one run of Claude Code on a GitHub machine, started with one instruction and ended when it is done. It cannot
  ask questions; what it writes into its report is all the owner sees of its thinking. Its full log is on the run page.
- **Agent file**: the standing instructions of one kind of session, in `.claude/agents/`: `sims-builder.md`,
  `sims-caretaker.md`, `sims-corrector.md`.
- **Short name (slug)**: the title in lower case with underscores, for example `wave_interference`. It names the model file
  `tools/sims/<slug>.py`, the registry entry, the branch and the report folder `notes/sims/reports/<slug>/`.
- **Pause**: a job that GitHub holds until a named reviewer approves it. It is made with a GitHub "environment" called
  `kaggelize-review` that has the owner as required reviewer. There is no input that switches the pauses off, and the workflow
  refuses to start if that environment does not ask a reviewer.
- **Board**: one GitHub issue, "Kaggelizing the simulations", with one row per simulation: stage, state, time, link.
- **Round**: one pass of landing and checking. Round 1 is the build; rounds 2 and 3 follow a correction.

## Your controls

| Control | Where | What it does |
|---|---|---|
| Run | Actions -> Kaggelize -> Run workflow | starts the flow for the titles you type (commas between titles) |
| Approve / Reject | the run page, yellow box "Review deployments" | opens or closes a pause; Reject stops that simulation, nothing is merged |
| Notes to the sessions | a comment on the board issue, written by you | the next session reads your comments (only the owner's are read) |
| Cancel | the run page, "Cancel workflow" | stops everything at once |
| How many at once | the Run form, "together" | 1 means one simulation after the other; 2 or 3 let them overlap |
| Model | the Run form | the model the sessions use |
| The board | Issues -> "Kaggelizing the simulations" | where each simulation stands |
| The logs | the run page, each job | every tool call of every session, numbered |

To send a study back for changes: write what is wrong as a comment on the board, Reject PAUSE 1, and run the same title again.
The builder continues on the same branch with your comment in front of it.

## The files

| File | What it does |
|---|---|
| `.github/workflows/kaggelize.yml` | the button: checks the titles, the secret and the pauses, then starts one flow per title |
| `.github/workflows/kaggelize-one.yml` | the flow of one simulation, top to bottom |
| `.github/workflows/kaggelize-land.yml` | pause, Kaggle line, caretaker; used once per round |
| `.github/actions/kaggelize-stage/action.yml` | one box: board row, tools, session, push, board row |
| `tools/sims/agents/stage.py` | runs one session inside its limits and commits what it wrote |
| `tools/sims/agents/board.py` | the board; the owner's notes; the check that the pauses pause |
| `tools/sims/agents/titles.py` | titles to short names |
| `.claude/agents/sims-*.md` | the instructions of the builder, the caretaker and the corrector |
| `.github/workflows/sims-kaggle.yml` | the Kaggle line; it can now be called with a branch's commit |

`stage.py`, function by function: `prepare` puts the working copy on the right branch; `owner_notes` and `failed_log` collect
what the session should know; `prompt_for` writes the one instruction; `run_session` starts Claude Code and prints the log;
`enforce` throws away changes outside the allowed paths; `required` checks the stage's files exist (and reads the verdict);
`commit` regenerates `docs/files.md` and commits in the owner's name.

## The limits a session works inside

- It never holds the GitHub token, so it cannot push, merge, comment or start workflows. The workflow pushes for it.
- Study and caretaker may only write inside `notes/sims/reports/<slug>/`. Anything else they change is thrown away.
- Build and correction may not change the machinery: `.github/`, `.claude/`, `tools/sims/agents/`, `pipeline.py`,
  `kaggle_sims.py`, `verify_live.py`, `public/data/sims/`, `CLAUDE.md`, `AGENTS.md`.
- Turn limits: study 120, build 300, caretaker 120, correction 200. Time limits: 90 min, 4 h, 90 min, 3 h.
- One Kaggelize run at a time; at most 12 titles per run; at most two corrections per simulation.

## Setting up (once, by the owner)

1. **The secret for the sessions.** On your computer, in a terminal: `claude setup-token`. It opens the browser, you approve,
   and it prints a token that is valid for one year and uses your Claude plan. In the repository: Settings -> Secrets and
   variables -> Actions -> New repository secret, name `CLAUDE_CODE_OAUTH_TOKEN`, paste the token. Show it to nobody.
2. **The pause.** Settings -> Environments -> New environment, name `kaggelize-review` -> tick "Required reviewers" -> add
   yourself -> Save protection rules.

`KAGGLE_API_TOKEN` is already there from the Kaggle line.

## Costs

GitHub's machines are free for a public repository. Kaggle's CPU runs spend no GPU quota. Each session spends usage of the
Claude plan; how much per simulation is not known until the trial has run, and will be written here.

## What can go wrong

| What happens | What you see | What then |
|---|---|---|
| the secret is missing or expired | "Make the list" fails with that sentence | set the secret again |
| the environment asks nobody | "Make the list" fails and says how to create it | create it; nothing has run |
| a session ends without its report | that job fails; board "failed: open the run" | read the log; run the title again |
| a session changed the machinery | a warning lists what was thrown away | nothing to do |
| Kaggle fails or the data check fails | the Kaggle line fails; nothing reached `main` | the corrector gets the failed log, then a pause |
| the caretaker says not clear | board shows the report | the corrector works from the verdict, then a pause |
| still not clear after two corrections | board "needs you" | you decide; the reports say what is left |
| `main` moved under the branch and the changes clash | the Kaggle line fails at the commit step | run the title again from the study |

Known weak points, said plainly: the logs of a public repository are public, so everything a session prints can be read by
anyone. A session has the plan's token in its own process; a web page it reads could try to trick it into sending that token
away. The limits above do not stop that; revoking the token does (claude.ai settings). The sessions cannot use the claude.ai
connectors or the skills saved in the account: everything they need is in this repository.

## Tested (21 November 2026, in the workspace)

- `titles.py`: titles to short names; empty input, unusable titles and duplicates are refused.
- `board.py`: rows written to a local file (`BOARD_FILE`), table drawn, a `|` in a title and a non-GitHub link made harmless.
- `stage.py` with a stand-in for Claude (`CLAUDE_CMD`), in a scratch copy with its own origin: study, build, correction before
  and after landing, caretaker rounds 1 and 2. Checked: branches, commits in the owner's name, the verdict read (`clear=false`
  then `true`), changes to `index.html`, `CLAUDE.md`, `pipeline.py`, `.github/` and `public/data/sims/` thrown away, the token
  absent from the session's environment, a second study of a finished simulation refused.
- All workflow files parse as YAML.

Not tested, because it needs GitHub itself: the workflows running, the pauses, the board issue, the Kaggle line called with a
branch commit, and a real session. The trial on one simulation is that test.
