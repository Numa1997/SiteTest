# Kaggle presentation: handoff, 24 November 2026 (Berlin)

Aim (the user): the Kaggle account `numakoudsie` is presentable for job applications. Datasets and notebooks must correspond to one another.
Nothing was changed on Kaggle in this session. Only read-only calls were made.

## The user's rules (binding)
- Turn things public, but NOT: Fig. 12, Fig. 16, anything Guinness (until the user says finished), and the notebook `fig15-filer-2026-11-18`
  (its code holds 7 temporary kaggleusercontent.com download links with access codes; v3 and v4). Public may be irreversible.
- No new runs. No deletions unless the user names the item. Berlin time only. Say what you are doing before doing it. Plain words.
- Never ask for or write passwords or keys. Commits as Numa Koudsie, no co-author line.
- The user said NO to renaming Fig 12/14/16 datasets to "Fig. N Name: simulation data" (reason not given).

## Verified today (Kaggle connector, read-only)
- 8 datasets, all private: fig1-wave-interference, fig2-double-pendulum, fig12-guinness-on-a-cart, fig14-schrodinger-sphere,
  fig15-resonant-tunnelling (26.7 GB, v1), fig16-guinness-cart-control, phyein-usul-barton, phyein-usul-coupled.
- Fig 12, 14, 16 datasets: empty subtitles, old title style. Fig 1, 2, 15, Barton, Coupled: proper title + subtitle.
- Fig. 15 card flaws: column "files identical to the site's" shows 0 on every row (comparison bug in tools/sims/file_figure.py:
  names do not match the site index); description cut off after "**Layout.** `". Fix = rewrite the card through the workflow
  (tools/sims/dataset.py update_card keeps isPrivate true). A figure-card mode does not exist yet.
- 32 notebooks listed; privacy is shown only for fig15-filer (private). The other 31 are unverified (search does not return the flag).
- Every notebook's code and output already sits in its figure's dataset, folder per notebook version (Fig. 15: 20 notebooks, 25 versions).
- Fig. 15 data on the site: Cloudflare R2 `resonant-tunnelling/2026-11-18/runs/` 2,782 objects 4.44 GB (see notes/fig15/coordinator-2026-11-18/r2_upload.log).

## What cannot be done from a cloud session
- No access to the user's logged-in browser. A cloud browser (TinyFish) showed Kaggle's login page, logged out. No Kaggle command-line tool installed here.
- The Kaggle connector cannot change metadata (licence error) or visibility. The key lives only in the GitHub secret KAGGLE_API_TOKEN (workflow "Simulations on Kaggle").
- Re-pushing a notebook with the command-line tool re-runs it (a new run): do not use it to change visibility.

## Plan (user decides each public step; wait for the yes)
1. Fix the Fig. 15 card (remove the bad column, full description, keep private) via the workflow.
2. Fill the Fig 14 subtitle and description (private) before it goes public.
3. Make public: datasets Fig 1, 2, 14, 15, Barton, Coupled; notebooks `phyein-usul-simulations` and `fig-14-schrodinger-sphere`.
   Do it in Kaggle's own pages (Settings, Sharing) with the user's logged-in browser (Claude in Chrome) or let the user click.
4. Everything else stays private. Check the text of each notebook for keys or links before it goes public.

## Other sources
- notes/inventory/KAGGLE_REPORT.md and KAGGLE.md on branch branch/fervent-galileo-x0t3vu; docs/kaggle-pipeline.md; docs/kaggle-sims.md.
