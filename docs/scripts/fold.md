# public/scripts/fold.js

| | |
|---|---|
| File | [public/scripts/fold.js](../../public/scripts/fold.js), 414 lines, 24.5 kB (24 526 bytes; measured 29 October 2026) |
| Loaded by | [index.html:723](../../index.html#L691) (the home page); [portfolios.html:420](../../public/portfolios.html#L453); [simulations.html:124](../../public/simulations.html#L124), before `catalog.js`; the eleven simulation pages, first of the shared scripts (load-order table in [sim.md](sim.md#load-order-on-the-pages)) |
| Defines | `window.Fold = { make, walk, all, openTo, setCard, onCard, onAll, tools }` ([fold.js:413](../../public/scripts/fold.js#L413)) |
| Sets on `<html>` | CSS variables `--fold-open`, `--fold-close`, `--fold-ease` ([fold.js:21-23](../../public/scripts/fold.js#L21-L23)) and `--fold-top` ([fold.js:297](../../public/scripts/fold.js#L297)) |
| Stores | nothing across visits since 3 November 2026; removes the old `localStorage['fold:<path>']` ([fold.js:64-67](../../public/scripts/fold.js#L64-L67)) |
| Styles | [styles/fold.css](../../public/styles/fold.css) |

`fold.js` turns the long pages of the site into fold-out sections, the mechanism of the Physik Radar app and the two project
apps without their colour coding ([fold.js:1-12](../../public/scripts/fold.js#L1-L12)). A level-1 fold is a section card: a
header band with a number, a title, one line of counts and a round toggle, and a body that unfolds beneath it; while open, its
header pins to the top of the window. A level-2 fold is a part inside a section, whose smaller band pins just under its
section's header. On the simulations list, cards keep their details behind More / Less. The file remembers per page what the
reader opened or closed, opens the folds around any `#link` target, opens everything for printing, and, without JavaScript,
leaves every page fully open.

## How it works

### The picture

A fold is a drawer. Pulling it open makes the cabinet taller; everything below moves down. A good drawer moves smoothly, and
when you close a drawer you are standing deep inside, the room should not jump. `fold.js` animates the real height of the
drawer (so the page below moves with it) and moves the window in step, on the same curve and clock, so that what the reader
is looking at stays put.

### The structure a fold builds

`make(node, opt)` ([fold.js:169-202](../../public/scripts/fold.js#L169-L202)) rearranges `node` in place:

```
node.fsec | node.fsub            data-fold-level="1|2"  data-collapsed="0|1"
├── div.fs-head                  (the band; sticky while open, by fold.css)
│   ├── div.fs-main              the nodes in opt.head (moved, not copied) + p.fs-counts
│   └── div.fs-side
│       └── button.fs-toggle     aria-controls, aria-expanded, aria-label "Collapse …/Expand …", svg.chev
└── div.fold#<id>-body           data-open="0|1", inert when closed
    └── div.fold-i
        └── div.fs-body          everything else node held
```

The height animation is done by CSS: `.fold` is a one-row grid whose row goes from `0fr` to `1fr`, with `transition:
grid-template-rows var(--fold-open) var(--fold-ease)` ([fold.css:57-61](../../public/styles/fold.css#L57-L61)); the body also
fades. Closing uses `--fold-close`. Closed bodies are `inert`, so they cannot take focus
([fold.js:108](../../public/scripts/fold.js#L108)).

### Timing and easing

Since 27 November 2026 the pace is the site's, set once in [`styles/motion.css`](../../public/styles/motion.css) (see
[styles.md, Motion](../styles.md#motioncss--motion)): `--dur` 0.75 s for opening and closing, `--ease`
`cubic-bezier(.65, 0, .35, 1)`, and the rise-in values `--rise*`. `fold.css` maps `--fold-open`, `--fold-close` and `--fold-ease`
onto them, and `fold.js` reads the same values from the page's CSS at the moment it needs them (`ms()`,
[fold.js:21-25](../../public/scripts/fold.js#L21-L25)), so changing `motion.css` changes the scripted scroll too.

The scroll that goes with a fold follows smootherstep ([fold.js:27](../../public/scripts/fold.js#L27)),
$$s(t) = t^3\,(6t^2 - 15t + 10), \qquad s'(0) = s'(1) = s''(0) = s''(1) = 0,$$
which starts and stops at rest with no jolt; the CSS curve `--ease` is a close cubic Bézier to it. A jump within the page (a click
on a `#` link) uses ease-out instead, $1 - (1 - t)^3$, over 0.7 s (`JUMP`, [fold.js:29-30](../../public/scripts/fold.js#L29-L30)):
it answers the click at once and settles slowly.

### Items rise in

When a fold or a card opens, `rise(fold)` ([fold.js:137-156](../../public/scripts/fold.js#L137-L156)) numbers the items of its
body (`--i`) and adds the class `is-rising`; `fold.css` ([line 68](../../public/styles/fold.css#L68)) then lets each item rise
14 px and fade in over 0.7 s, starting 120 ms + `--i` × 45 ms after the click. Items that will sit below the window share the
number of the last item in view, so a long section never keeps the reader waiting. The class comes off once every item has
arrived. Only on opening, never on Expand all, a link jump or a redraw; nothing is re-rendered, only a class changes.

### Opening and closing one fold

`toggle(node)` remembers the choice and calls `fold(node, open, true)`. `fold()` ([fold.js:118-133](../../public/scripts/fold.js#L118-L133)):

- **Closing.** Its pinned header may sit at the top while the fold's real top is far above. First the window jumps (no
  animation) so the fold's top is exactly where the header already appears: nothing on screen moves, but now only the body will
  fold away. Then, if the page will become too short for the current scroll position (the scroll is beyond the page end minus
  the body height), the window glides up to the new end while the body closes, in the same 0.75 s.
- **Opening.** The attributes flip and CSS animates; then `reveal()` ([fold.js:117-123](../../public/scripts/fold.js#L117-L123))
  leaves the window alone if the header sits between its pin line and the larger of (pin line + 48 px) and
  40 % of the window height; otherwise it glides so the header lands 12 px below its pin line, no further than the page end will be once the
  body has grown.

`pinLine(node)` is where a fold's header pins: `--fold-top` for a section, plus the height of each enclosing section header for
a part ([fold.js:97-101](../../public/scripts/fold.js#L97-L101)).

`glide(to, ms, curve)` ([fold.js:34-50](../../public/scripts/fold.js#L34-L50)) scrolls on its own animation frames with the eased
progress (smootherstep unless another curve is given). A newer glide cancels an older one through the counter `glideId`; a wheel or touch movement by the reader cancels it
too. With reduced motion it waits two frames, so the new layout exists, and then jumps.

### Expand all, Collapse all

`all(open)` ([fold.js:150-163](../../public/scripts/fold.js#L150-L163)) moves every fold as one motion (since 3 November 2026,
at Numa's request; before, it switched the transitions off): it reads where each fold is, gives each fold on screen (or within
200 px of it) a start 45 ms (`--rise-step`) after the one above it, at most 0.36 s (`--fold-delay`, read by the transitions in
[fold.css:53-59](../../public/styles/fold.css#L53-L59)), sets every fold and card, remembers every fold for this visit, calls
`Fold.onAll`, and removes the delays once the motion has ended. Collapsing first glides to the top of the first fold if the reader is below
it. `tools(host, where)` ([fold.js:227-240](../../public/scripts/fold.js#L227-L240)) puts the two buttons once per page,
`'before'` (default), `'after'` or `'append'` to `host`.

### Links into closed folds

A click on any `a[href^="#"]` with a target on the page is taken over; one whose target lies outside every fold glides there
(ease-out, 0.7 s) below whatever is pinned at the top and moves the keyboard focus there. One whose target lies inside a fold or card: default prevented, the address updated with
`history.pushState`, then `openTo(target, true)` ([fold.js:264-273](../../public/scripts/fold.js#L264-L273)). Clicks with a
modifier key or another mouse button are left alone. `openTo` ([fold.js:243-259](../../public/scripts/fold.js#L243-L259)) opens
every enclosing fold from the outside in, and the target itself if it is a fold, without animation, and remembers them open;
it opens an enclosing card; then it glides (ease-out, 0.7 s) or, without a click, scrolls so the target sits 12 px below the stack of pinned headers (`--fold-top` plus each
enclosing header's height). On `hashchange`, and at boot when the address has a hash, it jumps without a glide
([fold.js:274](../../public/scripts/fold.js#L274), [fold.js:409](../../public/scripts/fold.js#L409)).

When KaTeX finishes, the lecture note grows. `fold.js` listens for `sim.js`'s `typeset` event and aims again at the hash, unless
the reader has already used the wheel, touch or a key ([fold.js:400-402](../../public/scripts/fold.js#L400-L402)).

### Pinned headers below a page bar

A bar that sticks across the whole width (the home page index on phones; the search bar of the simulations list) carries
`data-fold-bar` ([index.html:64](../../index.html#L64), [simulations.html:57](../../public/simulations.html#L57)).
`measureTop()` ([fold.js:291-298](../../public/scripts/fold.js#L291-L298)) takes the tallest such bar that is currently `sticky`
or `fixed`, at `top ≤ 1 px`, and wider than 60 % of the window, and writes its height to `--fold-top`. Headers pin below it
([fold.css:33](../../public/styles/fold.css#L33)). It re-measures on window `resize` and when a bar changes size.

Each level-1 header is watched by a `ResizeObserver` that writes its height to `--head-h` on the section
([fold.js:200-206](../../public/scripts/fold.js#L200-L206)); level-2 headers pin at `--fold-top + --head-h`
([fold.css:68](../../public/styles/fold.css#L68)).

### Printing

`beforeprint` opens every fold and card and notes how each was; `afterprint` puts them back
([fold.js:276-288](../../public/scripts/fold.js#L276-L288)). The print stylesheet also forces bodies open and hides the toggles
([fold.css:98-103](../../public/styles/fold.css#L98-L103)).

### Adapters: what becomes a fold on each page

`boot()` runs at `DOMContentLoaded`, or at once when the script tag carries `data-now` (the Projects page, whose tag stands after everything it folds and whose `<link rel="expect" href="#folded" blocking="render">` holds the first frame until the cards are folded, so they never show open and snap shut): `measureTop`, then the three adapters, then `openTo(hash)`
([fold.js:404-411](../../public/scripts/fold.js#L404-L411)). Each adapter returns at once on a page without its structure.

| Adapter | Page | Level 1 | Level 2 | Counts line | Default |
|---|---|---|---|---|---|
| `home()` [353-372](../../public/scripts/fold.js#L353-L372) | `index.html` (needs `main .section[id]` and `.layout`) | each section, `h2` numbered `01`…`05` | none | `positions`: roles (`article.entry`), `education`: qualifications (`h3`), `research`: projects (`article`), `simulations`: figures (`article`), `skills`: areas (`dt`); a count of 0 is left out | open |
| `portfolios()` [375-396](../../public/scripts/fold.js#L375-L396) | `portfolios.html` | each `article.proj`; its `.proj__band` is removed and its number and texts become the title number and counts | each `.proj__part` with an `h3` (id `<project>-part-<n>` if missing) | the band's `p` and last `span` | open |
| `papers()` [313-339](../../public/scripts/fold.js#L313-L339) | simulation pages | each `.paper .psec` with an `h3` | each `h4` with what follows it up to the next `h4`, wrapped in `section.ppart` (id from the `h4`, else `<section id>-<number>`) | parts, equations (`\[` in the source plus `.katex-display`), figures (`.pfig`), boxes (`.pbox`) | open |
| `walk()` [342-350](../../public/scripts/fold.js#L342-L350) | simulation pages, called by `sim.js` ([sim.js:407](../../public/scripts/sim.js#L407)) | `#walk`, titled by its `h2` | none | "N steps · each formula beside the code that computes it and its value now" | open |
| page script | `simulations.html` ([simulations.html:242-247](../../public/simulations.html#L242-L247)) | each `section.simfold`, one per simulation | none | the entry's `subject` | closed (`defaultOpen: false`); open while a search or chip filters (`forceOpen`) |

Expand all / Collapse all sits at the end of the paper's header (`.paper__head`) on simulation pages, before the first section
on the home page, before the first project on Portfolios, and before the list on the simulations page
([fold.js:338](../../public/scripts/fold.js#L338), [348](../../public/scripts/fold.js#L348), [371](../../public/scripts/fold.js#L371),
[395](../../public/scripts/fold.js#L395), [simulations.html:345](../../public/simulations.html#L345)).

Measured in headless Chromium (1.5 s after load): the ten simulation pages of the time (before Fig. 11) have 10 or 11 level-1 folds and 2 to 10 level-2
folds each; on Fig. 2 the counts lines of the first sections read "1 figure", "1 equation", "3 equations · 1 box",
"4 parts · 7 equations", and the walkthrough's reads "8 steps · each formula beside the code that computes it and its value
now". The home page has 5 folds, counted "7 roles", "3 qualifications", "3 projects", "8 figures", "7 areas". The simulations
page opens with 10 folds, all closed; `?q=chaos` shows 1 fold, open.

## Public interface

| Name | Lines | Arguments | What it does / returns |
|---|---|---|---|
| `Fold.make` | [169-202](../../public/scripts/fold.js#L169-L202) | `node, { level (1), id, head: [nodes], counts, label, defaultOpen (false since 3 November 2026), forceOpen }` | Builds the fold (once; a second call returns `node` unchanged). Open state: `forceOpen`, else this visit's choice, else `defaultOpen`. Returns `node`. |
| `Fold.walk` | [342-350](../../public/scripts/fold.js#L342-L350) | `host` | Folds the walkthrough section; adds the tools if the page has none; re-aims at the hash. |
| `Fold.all` | [150-163](../../public/scripts/fold.js#L150-L163) | `open` | Opens or closes every fold and card at once. |
| `Fold.openTo` | [243-259](../../public/scripts/fold.js#L243-L259) | `target, smooth` | Opens the folds around `target` and scrolls to it. |
| `Fold.setCard` | [209-218](../../public/scripts/fold.js#L209-L218) | `card, open` | Sets a `[data-card]`'s More / Less state (not remembered). |
| `Fold.onCard` | set by the page | `(card)` | Called after a reader toggles a card ([fold.js:223](../../public/scripts/fold.js#L223)). |
| `Fold.onAll` | set by the page | `(open)` | Called by `all()` ([fold.js:160](../../public/scripts/fold.js#L160)). |
| `Fold.tools` | [227-240](../../public/scripts/fold.js#L227-L240) | `host, where` | Adds Expand all / Collapse all, once per page. |

Markup the file reacts to: `[data-fold-level]`, `[data-card]` with a `.fold` and a `.fs-more` button inside, `[data-fold-bar]`,
and the page structures in the adapter table.

**Words on translated pages.** The strict-mode line ([fold.js:14](../../public/scripts/fold.js#L14)) defines `T(s, vars)`: it
returns the translation of the English `s` from `window.I18N` (set by `scripts/i18n/strings-<lang>.js` on a German or Arabic
page) and `s` itself on an English page, filling `{name}` placeholders from `vars`. Every word fold.js writes goes through it
(More, Less, Show details, Expand all, "Expand {x}", the walkthrough's count line), and `plural(n, one, many)`
([fold.js:306](../../public/scripts/fold.js#L306)) picks the plural form with `Intl.PluralRules` when the table holds an object
for `many` (Arabic has six forms). See [i18n.md](../i18n.md#words-inside-scripts-t-and-i18nlangstringsjson).

## Internal functions

| Name | Lines | What it does |
|---|---|---|
| `motion` | [17](../../public/scripts/fold.js#L17) | False when the system asks for reduced motion. |
| `ms`, `ease`, `easeOut` | [21-30](../../public/scripts/fold.js#L21-L30) | The site's durations read from CSS; smootherstep; ease-out. |
| `rise` | [137-156](../../public/scripts/fold.js#L137-L156) | Items of an opening fold rise in. |
| `glide` (inner `stop`, `step`) | [34-50](../../public/scripts/fold.js#L34-L50) | Eased, cancellable window scroll. |
| `remember` | [68-72](../../public/scripts/fold.js#L68-L72) | Writes the reader's choice for one id. |
| `el` | [74-79](../../public/scripts/fold.js#L74-L79) | Creates an element with class and text. |
| `chev` | [80-88](../../public/scripts/fold.js#L80-L88) | The chevron SVG. |
| `foldOf`, `isOpen`, `pageEnd`, `headOf`, `top0` | [90-94](../../public/scripts/fold.js#L90-L94) | Body of a fold; open test; largest scroll position; header; `--fold-top` in px. |
| `pinLine` | [97-101](../../public/scripts/fold.js#L97-L101) | Where a fold's header pins. |
| `setFold` | [104-114](../../public/scripts/fold.js#L104-L114) | Attributes, `inert`, toggle labels; no animation logic. |
| `reveal` | [117-123](../../public/scripts/fold.js#L117-L123) | Brings an opened fold into view if needed. |
| `fold` | [126-141](../../public/scripts/fold.js#L126-L141) | Opens or closes one fold with scroll management. |
| `toggle` | [143-147](../../public/scripts/fold.js#L143-L147) | Reader's click: remember and fold. |
| `all` | [150-163](../../public/scripts/fold.js#L150-L163) | Everything at once. |
| `make` | [169-202](../../public/scripts/fold.js#L169-L202) | Builds a fold. |
| `headObserver` | [204-206](../../public/scripts/fold.js#L204-L206) | Writes `--head-h`. |
| `setCard` | [209-218](../../public/scripts/fold.js#L209-L218) | More / Less on a card. |
| `tools` | [227-240](../../public/scripts/fold.js#L227-L240) | Expand all / Collapse all. |
| `openTo` | [243-259](../../public/scripts/fold.js#L243-L259) | Open around a target and scroll. |
| `targetOf` | [260-263](../../public/scripts/fold.js#L260-L263) | Element for a `#hash` (URL-decoded). |
| `measureTop`, `watchBars` | [291-304](../../public/scripts/fold.js#L291-L304) | Height of the sticky page bar. |
| `plural`, `count`, `join` | [307-308](../../public/scripts/fold.js#L307-L308) | Counts-line helpers ("3 equations · 1 box"). |
| `papers`, `walk`, `home`, `portfolios` | [313-396](../../public/scripts/fold.js#L313-L396) | Adapters. |
| `boot` | [404-414](../../public/scripts/fold.js#L404-L414) | Start-up; `data-now` on the tag folds at once. |

## State it keeps

- Nothing is stored across visits (since 3 November 2026): `chosen` holds what the reader opened or closed during this visit
  ([fold.js:60-72](../../public/scripts/fold.js#L60-L72)), so a list that redraws (a search) keeps it; on load the keys that
  earlier versions stored (`fold:` + the path, with and without `.html`) are removed. Errors (private mode) are ignored.
- In memory: `chosen` (the parsed object), `glideId`, `printOpen`, `moved` ([fold.js:62](../../public/scripts/fold.js#L62),
  [41](../../public/scripts/fold.js#L41), [277](../../public/scripts/fold.js#L277), [400](../../public/scripts/fold.js#L400)).
- DOM written: the fold structure above; `data-fold-level`, `data-collapsed`, `data-open`, `inert`, `aria-expanded`,
  `aria-label`, `data-label`, `aria-controls`; classes `fsec`, `fsub`, `ppart`; `--head-h` on sections; `--fold-*` and the class
  `fold-no-anim` on `<html>`; `.fold-tools`; on Portfolios it removes `.proj__band` and replaces the project `h2`.

## Timing and events

| What | Rate or delay | Where |
|---|---|---|
| Open, close | `--dur` 0.75 s, `--ease` (styles/motion.css) | [fold.css:14-16](../../public/styles/fold.css#L14-L16) |
| Items rise in | 0.7 s each, 120 ms + 45 ms × item | [fold.css:68](../../public/styles/fold.css#L68), [fold.js:137-156](../../public/scripts/fold.js#L137-L156) |
| Glide | smootherstep over `--dur`; link jumps ease-out over 0.7 s | [fold.js:27-50](../../public/scripts/fold.js#L27-L50) |
| Expand / Collapse all | one motion, each fold on screen 45 ms after the one above (0.36 s at most) | [fold.js:162-176](../../public/scripts/fold.js#L162-L176) |
| `openTo` | no animation; transitions back on the next frame | [249-254](../../public/scripts/fold.js#L249-L254) |
| Reduced motion | glide jumps after two frames; no rise-in; every transition and animation 0 s (motion.css) | [fold.js:40-44](../../public/scripts/fold.js#L40-L44), [motion.css:29-33](../../public/styles/motion.css#L29-L33) |

Listeners: `click` on each header and toggle; `click` on `document` for `.fs-more` and for `#` links; `hashchange`;
`beforeprint`, `afterprint`; `resize` (passive); `wheel`, `touchmove` (once per glide, and once at load) and `keydown` (once
at load); the `typeset` event; `ResizeObserver` on level-1 headers and on `[data-fold-bar]` elements; `DOMContentLoaded`.

## Contracts with other files

- **`sim.js`** calls `Fold.walk(#walk)` after building the walkthrough ([sim.js:407](../../public/scripts/sim.js#L407)) and fires
  `typeset` ([sim.js:445](../../public/scripts/sim.js#L445)). `fold.js` must load first so that `window.Fold` exists then
  ([sim.md](sim.md)).
- **`simulations.html`** builds one `section.simfold` per simulation with an `article[data-card]` inside, calls `Fold.make` with
  `defaultOpen: false` and `forceOpen` while filtering, sets `Fold.onCard` and `Fold.onAll` to keep its own record of open
  cards, and places the tools before the list ([simulations.html:242-247](../../public/simulations.html#L242-L247),
  [342-346](../../public/simulations.html#L342-L346)); see [catalog.md](catalog.md).
- **`fold.css`** owns the look and the height animation; class and attribute names are shared ([../styles.md](../styles.md)).
- **Lecture notes** must keep the structure `.paper .psec > h3` and `> h4` with `.psub__n` numbers for the counts and ids to
  work; the home page `main .section[id] > h2` inside `.layout`; Portfolios `article.proj > .proj__band` and `.proj__head h2`,
  `.proj__part > h3`.

## How to change it safely

- Change durations or the curve only in `FOLD` (line 20): the CSS reads them from the variables, so CSS and scroll stay in
  step.
- An id is the key of the reader's remembered choice. Renaming a section id on a page forgets that choice for every reader
  (harmless) and breaks links to it (not harmless).
- A new page bar that sticks must carry `data-fold-bar`, or pinned headers slide under it.
- A new fold structure needs a new adapter called from `boot()` or a `Fold.make` call from the page; call it before
  `openTo(hash)` runs, or the first hash jump misses.
- Test: open and close a section deep inside, link into a closed part from the contents list, Expand all / Collapse all, print
  preview, reload (choices kept), the same page in a private window (no storage, still works), and reduced motion.

## Notes for maintainers

1. `papers()` counts equations as the number of `\[` in a section's HTML plus the number of `.katex-display` elements
   ([fold.js:318](../../public/scripts/fold.js#L318)). It runs before KaTeX, so the first term counts; a `\[` inside a `.notex`
   element or in code would also be counted.
2. A fold made without any id gets the body id `fold-body` ([fold.js:178](../../public/scripts/fold.js#L178)); two such folds on
   one page would share an id. All current adapters supply ids.
3. The home page's Simulations section is counted as "8 figures" (measured), while the catalog lists eleven simulations. The count
   is taken from the home page's own `article` elements ([fold.js:360](../../public/scripts/fold.js#L360)); whether the home page
   should show all eleven is a question for [../pages.md](../pages.md).
