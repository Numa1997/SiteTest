# One Guinness page (owner, 18 Nov 2026, ~21:30 UTC): "MERGE EVERYTHING INTO ONE PAGE"

Owner: the open-problems session (session_01DGmqipAnEdVvBLCf7CLGmT), branch claude/guinness-open-problems. Reread after a compaction.
Solver work stays with session_01DGmqioyaYR5VnnZaKfpEhD (claude/continuous-spill); pages, drawing, panels, docs are ours.

## Today: three English-only pages
- public/simulations/beer-slosh.html (1670 lines, 397 kB): the live in-browser cart (stout-cart.js, stout-gpu.js, inline player), "12" in
  the figure menu and the catalogue; note p-step .. p-refs (17 sections).
- public/simulations/guinness-kaggle.html (296 kB): Fig. 12's stored Kaggle rides, guinness-jax-play.js (5 controllers x roads); note
  p-pint .. p-refs (13 sections). Reached from beer-slosh.
- public/simulations/guinness-cart-control.html (80 kB, built by tools/fig16/build_page.py from notes/fig16/page/*.src.html): Fig. 16,
  Fig. 12's best ride and the new cart side by side (guinness16-play.js); note p-why .. p-limits (9 sections); "16" in the menu.

## Target: one page at beer-slosh.html (keeps the "12" menu slot and catalogue entry)
1. Figure: ONE picture, one cart at a time. Switch: cart (one-wheel | four-wheel), road, controller / control on-off; a mode
   "live in your browser" (today's beer-slosh solver) beside "computed on Kaggle". guinness16-play.js already plays both carts' stored
   rides: extend it to one canvas + cart switch + Fig. 12's five controllers (from guinness-jax-play.js).
2. One data panel (Sim.data) covering whichever cart is shown.
3. One lecture note: (a) the pint, the glass, the frame, the modes, the head (one copy of what the three notes repeat); (b) the solver
   and the books; (c) the one-wheel cart, its controllers, why it fails on the kerb; (d) the new cart, its control, the results;
   (e) limits, references. Numbered equations renumbered once.
4. guinness-kaggle.html and guinness-cart-control.html become short forwarding pages to the matching section (no broken links);
   "16" leaves the figure menu; catalogue, docs/simulations, docs/files.md, inventory updated.
5. Built and tested on Kaggle CPU (syntax, panel proof, screenshots at 390 and 1440 px), merged, curl-verified live.

## Status
- [ ] 1 figure  - [ ] 2 panel  - [ ] 3 note  - [ ] 4 forwarding + menu + docs  - [ ] 5 test, merge, live
