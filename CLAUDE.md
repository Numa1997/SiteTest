# Working with Numa: method

Read this before any work in this repository. It records how Numa expects Claude to think and persist.
Project facts (layout, AppDeploy app, boundaries) are in AGENTS.md.

## Persist; never settle for "I can't find anything"
- One empty search is a fact about that search, not about the world. Before saying something does not exist,
  look at least three ways: the skills, plugins and connectors already in the session; the open web; and every
  place Numa names (Stack Exchange, GitHub, coursework, papers, open-source projects).
- When a tool is blocked, take another road to the same source, and say which road you took.
  Example: the web search tool refuses stackoverflow.com, but the public Stack Exchange API
  (api.stackexchange.com/2.3) answers, and its "similar" endpoint matches a plain-language question.
- Read primary sources whole. Download the PDF, open the source file, run the code. Never pass off a search
  summary as the source, and never cite a paper you have not read when you could have read it.
- Measure numbers instead of estimating them. Example: the Fig. 1 field grid is 350 × 158 = 55 300 points on a
  1280–1600 px wide screen, 360 × 360 at 880 px; measured in headless Chromium, not guessed.

## Build when the request is clear
- "Display the data in a table" is a build request. Build it, test it in a real browser, show screenshots,
  commit. Do not answer a clear build request with option lists, theory or questions.
- Ask only when different readings would lead to materially different work, and then ask one thing.

## Talk plainly
- Short sentences, everyday words. Physics pictures where they help; formulas only when asked.
- When wrong, say so in one line and fix it. No grovelling, no excuses, no walls of text.

## The application comes first, the repository second
- The thing Numa looks at is the AppDeploy app. Work on it first: read its stored source (`src_read`), build and test against
  that, deploy, verify the live site. Only then migrate the same change into the GitHub repository, commit and push.
- Never start with the repository, and never report the repository first. The live app is the deliverable; the repo is its copy.

## A data table is a pipeline, not a second simulation
- The simulation writes each number into the store at the line that computes it; the display only reads. Never recompute for display.
- Prove the pipeline three ways and show the proof to the reader: the stored value, the formula recomputed from the stored inputs, the pixel
  read back from the picture. Aim for "identical"; name a float32 or rounding gap as what it is.
- A read-back test must first check that something was drawn: a transparent pixel passes a "dark" test. Check alpha before colour.
- Where the drawing and the store differ (colour steps, smoothing, trails, relaxation), say so on the page, in one paragraph the reader can open.
