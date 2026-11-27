# Motion inventory before the change (27 November 2026, main at 2e7c2e9)

Everything that moves or appears on a click, a hover or a page change. Simulation canvases and animated backgrounds are left out.
Paths under `public/` unless stated. "Snaps" = changes in one frame.

## Folds (fold.css, fold.js): every page with cards
| Where | Trigger | Now | Verdict |
|---|---|---|---|
| fold.js:20-23 | load | `FOLD = {open 320, close 240, curve (.4,0,.2,1)}` written inline on `<html>` as --fold-open/--fold-close/--fold-ease | durations live in JS, not CSS |
| fold.css:57-61 | click a card header or toggle | grid-template-rows 1fr↔0fr, 0.32 s open / 0.24 s close, (.4,0,.2,1); body fades and moves 8 px | already the right technique; quick, a little brisk |
| fold.css:53 | same | chevron turns 180°, same 0.32 s | fine |
| fold.css:22,25 | open | card border and shadow, 0.32 s | fine |
| fold.css:30,47,77 | hover header, toggle, Expand all buttons | 0.15 s colour, toggle press scale .94 in 0.1 s | quick, slightly flicky |
| fold.js:36 `closeMs` | close from deep inside | close lengthened to ≤ 0.42 s with the distance, scroll glides with it | fine |
| fold.js:41-58 `glide` | open a low card; close from inside; jump to a #link inside a fold | rAF scroll on the cubic-bezier, 0.32 s | fine, but not smootherstep |
| fold.js:128-132 | close while scrolled inside the card | `scrollTo(... 'instant')` first, then glide | an instant correction before the glide; usually 0 px |
| fold.js:146-163 `all` | Expand all / Collapse all | folds in view 28 ms apart (≤ 0.3 s); Collapse all first jumps instantly to the first card if below it | the instant jump snaps |
| fold.js:243-259 `openTo` | click a #link into a closed fold | folds open with animation off (`fold-no-anim`), then glide 0.32 s | content appears at once (snap), then a glide |
| fold.js:264-273 | click a #link outside any fold | not handled: html `scroll-behavior: smooth` (site.css:39) on home/lists; **instant jump on simulation pages** (sim.css has no smooth scroll) | jumps on simulation pages |
| fold.js:274 | back/forward to a #hash | instant scroll | snaps |
| fold.js:209-222 `setCard` | More / Less on a simulations-list card | class change on a `.fold`; same 0.32 s | fine |
| — | opening any card | the content appears as one block | no rise-in of items |

## Page changes (i18n.css, flip.js)
| i18n.css:55-62 | any link to another page | view transition: old page out 0.16 s (.4,0,1,1), new page in 0.28 s (0,0,.2,1) after 0.06 s; 0.34 s | brisk |
| i18n.css:64-68 | language switch | half turn about the vertical axis, 0.28 s + 0.28 s | brisk |
| i18n.css:74 | reduced motion | view transitions off | good |
| site.css:146-251, sim.css:57,67,77 | page arrival | hero/heads rise 0.8–0.9 s, figure fades 1–1.2 s; skipped after a view transition (`vt-arrive`) | entrance, not a click; left |

## Hover, press and buttons
| site.css:220 `.btn` | hover | colour, shadow, transform 0.2 s ease | fast |
| site.css:341 `.index a` | hover | colour, border, padding-left 0.2 s (text shifts sideways) | fast |
| site.css:454,497 entry/row | hover | colour/background 0.2 s | fast |
| site.css:590-615 `.plate` | hover | lifts 5 px, 0.3 s; sketch scales 1.05 in 0.5 s | lifts too far, quick |
| site.css:684-691 `.plate__launch` | hover | 0.2 s; arrow moves 0.2 s | fast |
| site.css:988,1022,1110,1132 shelf buttons, dots, bubble | hover/click | 0.12–0.3 s | fast |
| site.css:1201, sim.css:259 | press | dims to 72 % in 0 s, back in 0 s | snaps (a deliberate tap mark, 3 Nov.) |
| sim.css:51 sim-nav, :98 .btn, :106-107 switch, :145 walk steps, :160 .k, :168 table cells | hover/click | 0.15–0.2 s ease | fast |
| catalog.css:254 `.entry__open` | hover | 0.15 s | fast |
| index.html:62-63 | hover a Lucretius verse | background/colour 0.25 s | fine |
| index.html:67 `.lq-card` | hover/tap a verse | card fades 0.18 s, rises 0.26 s | quick |
| lucretius.html:83 | language tab | underline grows 0.28 s ease | quick |
| lucretius.html:95 | language tab | verses re-appear with `lp-turn` 0.32 s | quick |

## Tabs and panels
| sim.css:149 `.walk__card` | click a step of "From symbols to code" | card rises 6 px in 0.3 s | quick |
| data.css:33-37 `.dp` | open/close the data panel | slides 0.32 s ease | quick |
| data.css:17,19 `.dp-tab` | hover | padding grows 0.2 s (the tab widens) | fine |
| data.css:202-205 `.dp-sec` | click a section of the data table | arrow turns 0.2 s; rows `display: none` | **rows snap open and shut** |
| data.css:183-184 `.dp-exp` | click a row | arrow 0.2 s; detail row inserted at once | detail snaps in |
| data.css:388 `.dp-tab` phone | scroll | slides away 0.24 s | fine |

## Reduced motion
site.css:878-900, sim.css:187,224, fold.css:95-97, data.css:446-451, i18n.css:74, index.html:73, lucretius.html:108:
covered piecemeal; hover transitions, plates, buttons and the walk card are not switched off.
