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
