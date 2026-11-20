# State: documenting the build, then removing the history

Written 20 November 2026 by the session that does this work. Reread this file first after a compaction.

## Aim (the owner's order, 20 November 2026)

1. Read the whole history and document how the site was built, as the model to build on.
2. Save whatever a rebuild needs that only the history holds.
3. Then remove the old versions: `main` keeps only the latest version, in commits that carry the owner's name alone,
   and the old branches go.

## What is live

- phyeinusul.com serves `main`. Before this work `main` was `12c2e3a` (18 November 2026).
- This work added files only: `docs/method/` (three pages), `tools/kaggle/pinned-code/` (the solver code of 37 pinned
  commits and its manifest), `package-lock.json`, this file, rules in `tools/inventory.py`, one line of `docs/usul.md`,
  and the regenerated `docs/files.md`. No page, script or style of the site was changed.
- Checked before the commit: a build from the lockfile gave 4,836 files; all 202 built `.html`, `.js`, `.css` and
  `.svg` files outside `data/` were byte-identical to the live site.

## What is left

- Step 3 has **not** been done. It needs the owner's explicit yes for that exact action.
- Before step 3: the 152 remote branches hold the old commits too; 24 of them are not merged into `main`.
- Open gaps toward a full rebuild: [docs/method/rebuild.md](../../docs/method/rebuild.md), section 5.

## The owner's rules for this work

- Nothing is deleted, force-pushed or rewritten without his explicit yes for that exact action.
- Commits carry his name as author and no co-author line or session link.
- One step per turn; say what was done and what comes next in one sentence each.
- Never guess what can be checked; state facts with a command or file that shows them.
