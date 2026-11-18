# Guinness realism (Fig. 12 and Fig. 16): this chat's state

Reread this file first after any compaction. Keep it current at every step that changes what is live or what is left.
Session: session_01DGmqioyaYR5VnnZaKfpEhD. Branch: `claude/guinness-realism` (from main 81e6fe2).

## Aim
The owner, 18 November 2026: "they both look no where near realistic .. very sad state". Make the two Guinness figures look like a
real pint of Guinness on a real cart: glass, stout, head of foam, light, cart, road, motion. Judge every change against photographs
of the real thing, side by side. The physics and the stored data stay as they are; the page only reads the stored fields.

## Rules (binding)
- EVERY run goes through Kaggle, saved there and organised; in parallel where possible (owner, 18 Nov). Nothing runs in this
  container: no python, node, npm, browsers, agents (owner, 15 Nov). Read, edit, git, curl, jq, Kaggle tools only.
- The owner's yes before every action (proposal: what, why, effect, cost, undo). One step per turn.
- Report to the owner in this chat. The coordinator session no longer exists.
- Never touch the Workers, R2, public/de/, public/ar/, scripts/i18n/, *.rtl.css. No model names in commits. Never write the owner's name.
- Owner: BSc physics; metric units; define terms; Fact (with handle) / Inference / Opinion; mechanism in one line.

## File split with session_01DGmqipAnEdVvBLCf7CLGmT (open problems), agreed 18 Nov
- Mine (drawing only): public/scripts/stout-view.js, stout-view2.js, guinness-glass.js, cart16-view.js, drawing parts of pint3d-view.js.
- Theirs: Fig. 16 data panel, page HTML (guinness-cart-control.html and src), frame timing, Kaggle dataset, inventory.
- Their request, accepted (owner's pick A): during my rework of cart16-view.js, at the end of View.prototype.draw, record the deck
  top's front and rear edge (y = 0) in CSS px into `this.deckStore` (NOT this.ds): deck_px_fx, deck_px_fy, deck_px_rx, deck_px_ry.

## Reference photographs (openly licensed, found through api.openverse.org; Wikimedia's API refused this container)
1. https://www.flickr.com/photos/73451168@N00/2665596032 (J Wynia, CC BY), settled pint on a bar.
2. https://www.flickr.com/photos/95142644@N00/150310646 (Ruth and Dave, CC BY), head close up, back light.
3. https://www.flickr.com/photos/18378655@N00/3344498497 (James Cridland, CC BY), pouring at the tap.
4. https://www.flickr.com/photos/44124323632@N01/2999818919 (Steve Burt, CC BY-SA), pint still settling.
5. https://www.flickr.com/photos/19994833@N00/388700 (Bernie Goldbach, CC BY-SA), not yet looked at.
6. https://www.flickr.com/photos/10785432@N03/4844117199 (Groume, CC BY-SA), not yet looked at.
Seen in them: head ivory-cream (not white), about a finger thick, domed just above the rim, fine pits; sharp head/stout boundary,
a tan band under the head while settling; stout near-black when settled, brown above and black below while settling; thin clear
glass with vertical highlight streaks and a bright rim line; thick clear foot catching light; gold harp, white lettering; warm low
light, reflection on the table, soft shadow. Physics of the cascade: https://www.rsc.org/news/2010/march/mystery-solved-why-guinness-bubbles-go-down

## The owner's order (18 Nov, evening)
"Resolve the split. I don't care what it takes. Learn from one another. Complete both works. Merge them into a functioning
animation already." Plan sent to session_01DGmqipAnEdVvBLCf7CLGmT: one integration branch (this one), main gets one merge of both
works after panel16_check and frames_check pass on it.
- Method chosen: the live page stays a real-time animation of the stored frames; the drawing becomes physically based in three.js
  (glass n 1.52 transmissive, stout Beer-Lambert from deLange's average beer spectrum at SRM 40, foam head, warm room). The Blender
  path-traced frame (render_pint.py) is the reference look; rendering every stored frame that way costs ~5 min per frame (too much
  for 241 frames x several rides on the remaining GPU quota).
- Done (9a6e8ef): pint3d-view.js physically based; cart16-view.js records deck_px_* into this.deckStore.
- Next: the 2D carts and road in the same style; then the page layout with the other session; checks; merge; live verify; docs.

## Steps (status)
1. Reads, session check, split — done.
2. Reference photographs — done (above).
3. "Before" screenshots on Kaggle: tools/realism/kaggle_shots.py, notebooks guinness-realism-fig12 / guinness-realism-fig16 (CPU,
   in parallel) — script written, waiting for the owner's yes to save and run.
4. List what looks unrealistic, before pictures beside the photographs; show the owner.
5. Build, re-shoot on Kaggle ("after"), compare, merge per CLAUDE.md, verify live, update the docs.

## Kaggle run register
- guinness-realism-fig12 v1 and guinness-realism-fig16 v1 (18 Nov, CPU, commit 9bb8503, TAG before, ran in parallel): both ERROR
  at the first screenshot, "Page.screenshot: Timeout 30000ms exceeded" (no graphics card: WebGL drawn in software). No pictures.
- v2 of both (18 Nov, commit 162286d, parallel): COMPLETE. Fig. 12: 24 pictures (12 moments), Fig. 16: 16 pictures (8 moments),
  0 console errors; 18-102 s per picture in software WebGL. Pictures stay in the notebooks' output (version 2).
- guinness-realism-render v1 (18 Nov, GPU T4, commit 67ea2ae): Blender 4.2 Cycles, 512 samples, kerb_full frame 36 (0.6 s),
  Poly Haven brown_photostudio_02 light. COMPLETE, 392 s in all, render 5 min 06 s. Outputs render.png, compare.png (render beside
  photo 1), render.log. Device used not confirmed (log tail cut). Seen: real glass, refraction, reflection on the table, foot right;
  stout too see-through and grey (ALPHA provisional), no ruby edge, head too white and flat, no print on the glass, studio room
  not a pub, table plain.

## Commits
- this file and tools/realism/kaggle_shots.py.
