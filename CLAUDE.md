# Working with Numa: method

Read this before any work in this repository. It records how Numa expects Claude to think and persist.
Project facts (layout, where the site runs, boundaries) are in AGENTS.md.

## Persist; never settle for "I can't find anything"
- One empty search is a fact about that search, not about the world. Before saying something does not exist,
  look at least three ways: the skills, plugins and connectors already in the session; the open web; and every
  place Numa names (Stack Exchange, GitHub, coursework, papers, open-source projects).
- When a tool is blocked, take another road to the same source, and say which road you took.
  Example: the web search tool refuses stackoverflow.com, but the public Stack Exchange API
  (api.stackexchange.com/2.3) answers, and its "similar" endpoint matches a plain-language question.
- Web search has many roads in this workspace; one failing (no credits, a paid plan, a block) is never the end. Try them in
  turn before saying anything is out of reach: WebSearch and WebFetch, Exa (web_search_exa, web_fetch_exa), TinyFish
  (search, fetch_content), Nimble, Tavily, Bright Data, Firecrawl, and the research and design connectors (Consensus,
  Mobbin). Say which ones failed and which one answered. (Numa, 28 October 2026, after Firecrawl ran out of credits and
  only one fallback was tried.)
- Read primary sources whole. Download the PDF, open the source file, run the code. Never pass off a search
  summary as the source, and never cite a paper you have not read when you could have read it.
- Measure numbers instead of estimating them. Example: the Fig. 1 field grid is 360 × 162 = 58 320 points on a
  1280–1600 px wide screen, 360 × 360 at 880 px; measured in headless Chromium, not guessed.

## Build when the request is clear
- "Display the data in a table" is a build request. Build it, test it in a real browser, show screenshots,
  commit. Do not answer a clear build request with option lists, theory or questions.
- Ask only when different readings would lead to materially different work, and then ask one thing.

## Work with Numa, not around Numa: minimise waste on both sides (Numa, 1 November 2026)
- Ask what is the best use of each of us. Claude is fast at code, measurement and checks; Numa's eye is the judge of how a page looks
  and feels. Do not spend Numa's tokens guessing what only Numa can see.
- Visual and feel work (line breaks, spacing, sizes, colours, how strong an effect looks, animation speed): one attempt at most, then
  stop and build a tuner, a `?tune=1` panel on the page itself with a slider or toggle for each parameter that matters, the live result,
  and a "Copy settings" button. Numa finds the values; Claude writes them into the code once and checks them once. Use the skill
  `.claude/skills/tune-with-numa/SKILL.md`.
- Before such work, say in two lines what the knobs are and ask: "tune it yourself, or shall I pick?" Ask Numa for a screenshot of what
  Numa sees rather than reconstructing it with probe scripts.
- No pile of throwaway scripts. A script is written only to measure what cannot be seen, and its purpose is said in one line first.
- After each round: what changed, one screenshot, the one decision needed. When a loop is not converging after two rounds, stop and say so.
- Help Numa prompt: when a request is ambiguous or will be costly, say so in one line and offer the sharper prompt (template in the skill).

## Talk plainly
- Short sentences, everyday words. Physics pictures where they help; formulas only when asked.
- When wrong, say so in one line and fix it. No grovelling, no excuses, no walls of text.

## The live site comes from the repository (since 20 October 2026)
- The thing Numa looks at is Phyein Usul, <https://phyeinusul.com>, built from this repository's `main` and served by Cloudflare.
  Work in the repository: change, build (`npm run build`), test in a real browser, commit. Since 21 October 2026 Cloudflare builds and
  deploys every push or merge to `main` by itself, so merge only when Numa says so, then verify the live site. See `docs/usul.md`.
- GitHub Pages also republishes `main` at <https://numa1997.github.io/SiteTest/>, kept on as a backup (Numa, 29 October 2026).
- A change is not done until the docs pages that describe the changed files say what the code now does.

## A data table is a pipeline, not a second simulation
- The simulation writes each number into the store at the line that computes it; the display only reads. Never recompute for display.
- Prove the pipeline three ways and show the proof to the reader: the stored value, the formula recomputed from the stored inputs, the pixel
  read back from the picture. Aim for "identical"; name a float32 or rounding gap as what it is.
- A read-back test must first check that something was drawn: a transparent pixel passes a "dark" test. Check alpha before colour.
- Where the drawing and the store differ (colour steps, smoothing, trails, relaxation), say so on the page, in one paragraph the reader can open.
- Nothing on a running figure may react to the pointer merely crossing it. Reading a point is a tool the reader switches on, as in
  MATLAB's data cursor or PhET's probes: click to pin, the values in a fixed place outside the figure, words rewritten at a readable
  rate (about 4 per second), the marker every frame. Measure it: what shows during a sweep, how much it covers, how often text changes.

## Design and explanations
- The design is the house design, as the stylesheets implement it and `docs/styles.md` records it. Read it before touching fonts, colours or layout,
  and generalise it; never introduce another font. Titles in Instrument Serif at weight 400 (simulations,
  catalog and Portfolios pages); the home page alone sets its titles in IBM Plex Serif at weight 600 (`site.css`). Text in IBM Plex
  Sans, labels in IBM Plex Mono.
- Explanations are lecture notes set like a LaTeX document (Latin Modern text, KaTeX maths, numbered equations and figures), written as a
  professor for undergraduates and school students: motivate from everyday experience first, then the model, then the mathematics, with
  pictures. No question-and-answer format anywhere.
- Lists of figures run in figure order.

