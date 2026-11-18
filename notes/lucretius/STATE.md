# Lucretius page: state of the chat that builds it (kept current at every step)

Aim: the poem page `public/lucretius.html` (+ `/de/`, `/ar/`), Lucretius I 146–224 in Latin, English (Leonard), German (Diels), Arabic.

## What is live (18 November 2026)
- Flat, modern layout (no sheet, frame or ornaments): PR #140. Each language one column; unbroken hairlines between columns;
  a short dash between verses inside each column; sticky head with index 01–04, name, credit. Below 1100 px one language at a time.
- Arabic: tenth version, translated from the Latin as a poem, fully vowelled (`notes/lucretius/poem-ar-146-224.json`): PR #139.
- Background: none by default (fractal engine of PR #143 removed at the user's request: "looks so stupid"). Earlier backgrounds at
  `?bg=d` (currents and atoms, PR #142) and `?bg=a|b|c` (margin strips, PR #141).
- Design system artifact "Phyein Usul Design System" (slug 43974698-cdb2-438a-8609-9050a1e6a1a9): PoemLeaf component flat, tenth
  Arabic; it does NOT have any background ornament.

## In progress (18 November 2026, 05:10 Berlin)
The user rejected every abstract background (margin strips, currents and atoms, fractal engine, flow field, reaction-diffusion,
differential growth, DLA) and the Vanta.js templates were "good development, not quite there". What he called "gorgeous": backgrounds
that carry a meaning from the poem. Shown to him as live widgets in the chat (code lives only in the chat so far):
1. Dust in a sunbeam (Lucretius II 114-141, Brownian motion; particles.js motes visible only inside a diagonal beam).
2. Letters into words (I 196-197): drifting letters assemble SEMINA, NATVRA, NIHIL, NOTHING, SAMEN, بذور, العدم, نور, then scatter.
3. Seeds and seasons (I 174-175): a seed falls, a stem grows slowly into rose, wheat or grapes.
4. The swerve (II 216-293): parallel falling atoms, one tilts, a cascade of collisions.
5. Shores of light (in luminis oras, I 170 and 179): motes rise through a slow waterline and brighten.
His orders, in his order:
 a. FIRST show more examples on the theme "falling is necessary for growth", real physics, e.g. droplets collecting each other on a
    window. Done in chat: rain on a window (coalescence, sliding drops), drops collecting in a cloud (gravitational collection with
    breakup; his thesis topic), Galton board, falling sand with ledges, dripstone. Waiting for his verdict.
 b. THEN deploy "all of them" (the four of items 2-5; the sunbeam is a fifth candidate) as backgrounds of 4 subpages of the site.
    Which four pages is NOT settled: ask him one question.
 c. THEN make Kaggle notebooks that simulate them ("at least their data"); he gave explicit permission to write notebooks in his
    Kaggle account for this.
Nothing of this is in the repository or live yet. The poem page has no background.

Update 05:20: the five "falling" examples (window rain, cloud collection, Galton, sand, dripstone) were rejected ("shit",
"terrible"). He asked for four new ones, "more complicated degrees, functions", with his own directions. Shown in chat, waiting:
 - Drops in a shear wind: window drops advected by u(y) = 70 tanh((y-200)/60) px/s (left above, right below), a Kelvin-Helmholtz
   style ripple v = 20 sin(0.02x - 1.2t) sech^2((y-200)/60), mobility (r-3)/6 clipped, merging by volume, gravity slide for r > 9.
 - Roots and neurons: 48 nodes, 28 % "closed" (rings) that repel growing tips within 50 px; tips steer to the nearest unconnected
   open node within 170 px (turn rate 2.6 rad/s), connect within 7 px, a node takes at most 3 links, a connected node ejects 2 new
   tips, a tip that finds nothing in 380 px retracts; pulses run along finished links.
 - How a clock ticks: seconds pendulum (theta = 0.16 sin(pi t), T = 2 s), anchor rocking with it, 30-tooth escape wheel advancing
   pi/30 per half swing, second gear, falling weight on a cord.
 - Clocks falling into sync: 153 clock hands, Kuramoto model d(theta_i)/dt = omega_i + K r sin(psi - theta_i), omega ~ N(pi, 0.6),
   K(t) = 2.4 (0.5 - 0.5 cos(2 pi t / 36)), big faint hand = order parameter r at angle psi.
The earlier four he called gorgeous (letters, seeds, swerve, shores) still stand for deployment on 4 subpages + Kaggle notebooks.

## User's rules for this work
- Merge and publish finished, tested work without asking; verify the live site; docs must describe the code.
- Do only what is asked; reply in plain connected English; never use the user's name.
- Arabic only by Opus; modern literary Arabic, no calques, no archaic or Quranic voice unless asked.
- Design: modern, no paper sheets or frames; wine red (#7a1f2b) is the accent; the user wants creativity and few constraints for
  the background, "natural, famous, mathematically related fractals, smooth transitions, a fluid moving them, cheap to run".
- Build pages: `python3 notes/lucretius/make_page.py && python3 tools/i18n/build.py`, revert stamp-only de/ar files;
  `python3 tools/inventory.py`; PR via REST (`gh api .../pulls`), merge via REST.
