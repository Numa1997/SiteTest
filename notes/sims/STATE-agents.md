# State of the "kaggelize every simulation" work (chat of 21 November 2026)

Reread this first after a compaction.

## Aim
Every simulation that still computes live in the browser gets its data generated once on Kaggle, carried to GitHub
and the site automatically, and played by the page. Claude sessions do the per-simulation thinking; the user presses
one Run button and watches one board.

## What is live
- The automatic line: `.github/workflows/sims-kaggle.yml` (workflow "Simulations on Kaggle"), `tools/sims/pipeline.py`,
  `kaggle_sims.py`, `verify_live.py`, `registry.json`. Proven on the Barton pendulums of the home page (rails scene).
- Order of conversion: `notes/sims/PLAN.md`.

## Built on 21 November 2026 (guide: docs/kaggelize.md; not yet run on GitHub)
- Button: `.github/workflows/kaggelize.yml` -> `kaggelize-one.yml` -> `kaggelize-land.yml` -> `sims-kaggle.yml` (now callable with a branch commit).
- Sessions: `.claude/agents/sims-builder.md`, `sims-caretaker.md`, `sims-corrector.md`, run by `tools/sims/agents/stage.py`.
- Board: `tools/sims/agents/board.py` (one issue). Pauses: environment `kaggelize-review`, always on, no switch.
- Tested in the workspace with a stand-in for Claude. Waiting for the owner: secret `CLAUDE_CODE_OAUTH_TOKEN`, environment
  `kaggelize-review`, then the trial run with one title.

## Design agreed in chat
- Builder (one simulation at a time, then moves on) → automatic Kaggle line → Caretaker reads the report →
  clear: done; not clear: Corrector, at most 2 rounds, then the user is asked.
- The user's plan: try it on ONE simulation, then make it a function and run it on TWO, then on all the rest.

## Facts checked on 21 November 2026 (Claude Code 2.1.330 docs)
- Subagents may nest up to 3 layers by default (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`); this cloud session has it set
  to 1 (nesting off). Bug report anthropics/claude-code#80036: nesting at depth 2 missing in practice.
- `claude --agent <name>` runs a whole session as one agent file in `.claude/agents/`.
- Agent teams: experimental, interactive only (not with `-p`), no nested teams, no resume of in-process teammates.
- GitHub Actions: `CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token` (one year, Pro/Max/Team/Enterprise) runs on the
  subscription; the token makes model requests only, no claude.ai connectors. claude-code-action commits as the Claude
  GitHub App, so for owner-name commits run the CLI directly and commit with `git -c user.name=...`.

## Open
- The trial on one simulation (Fig. 1, Wave Interference); then two titles in one run; then the rest.
- Usage per simulation: unknown until the trial; write it into docs/kaggelize.md, 'Costs'.
- "The one with a circle" (spinners or seeds strip) and the Fig. 14 live preview: unanswered.
