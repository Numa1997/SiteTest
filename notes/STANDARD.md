# The standard for the ten lecture notes

Sections 4 and 2 of the brief "Prompt for a Claude Code session · a team of physics teachers rewrites the ten lecture notes"
(version 2, 20 October 2026), word for word. Every agent of the team reads this file. Numa's verdicts on the pilot are added
at the end, under "Numa's verdicts", before any other work continues.

## 4 · The standard every note must meet

1. **The physical picture, from human experience**, outside and inside the body: the swing of a playground swing, the beat of
   two guitar strings, a gull lifted and dropped by a swell. Sensory detail before any symbol.
2. **The model, stated:** assumptions, the regime where they hold, the dimensionless numbers with the page's actual values
   (damping ratio, ka, d/λ, tip-speed ratio, …).
3. **The derivation from first principles, every step with its physical meaning:** the natural formal route (Lagrangian or
   Hamiltonian, potentials, conservation laws, symmetries, Fourier or phasor algebra, boundary conditions). No bare formula,
   no "it can be shown", no silent step. Heavier parts carry ★ (house convention): a school student can skip them, a physics
   graduate reads them.
4. **Checks:** dimensional analysis, limiting cases, a conserved quantity where one exists, one small number worked with the
   page's own parameters.
5. **The numerical method as the code really does it:** integrator, order, step size with the page's values; why it was
   chosen, where it fails, and the error the reader should expect, measured by running the page.
6. **Equation to screen:** which drawn thing is which symbol, and where the drawing differs from the model.
7. **Limits of the model** and the next, more complete model.
8. **Further reading:** only real sources you opened and read (textbook chapters, arXiv papers, lecture notes), each with a
   working link.

Form: connected prose, defined terms, SI units, no question-and-answer format, no filler. KaTeX: `\( … \)` inline,
`\[ … \]` display; equations numbered. Figures in notes are inline SVG in the house chart style (white plate, Plex Mono ticks)
plotted from the page's own formulas. Keep the note's structure: `section.psec` with `h3` and `span.psec__n`, lead
`p.psec__lead`, figures `.pfig`, tables `.ptab`, boxes `.pbox`, references `.prefs`. House type: Instrument Serif titles at
weight 400, IBM Plex Sans text, IBM Plex Mono labels, Latin Modern in notes, wine `#7a1f2b`. Numa dislikes IBM Plex Serif
headings; add no font.

**The reader.** `CLAUDE.md` says the notes speak "as a professor for undergraduates and school students"; Numa now also wants
theoretical sophistication. The layered form (picture and model for everyone, the full ★ derivation for the graduate) is
meant to serve both. Show it in the pilot and **ask Numa** whether this is the balance he wants.

## 2 · Where to work

- **Repository:** `Numa1997/SiteTest`, in this session's checkout. Nowhere else: no other repository, no AppDeploy app, no
  Cloudflare deploy.
- **Branch.** First **ask Numa** which branch to start from: `docs/usul-cloudflare` holds unmerged corrections to the very
  docs you will edit, so `main` may be behind. Then create `notes/teacher-team` from it and do all work there.
- **Files each simulation team may change:** the note inside its page (only between `<article class="paper" id="paper">` and
  its `</article>`), its own doc in `docs/simulations/`, and its working folder `notes/fig<NN>/`. Its walkthrough file
  `public/scripts/walk/<key>.js` only if Numa allows it in the pilot.
- **Files only you, the lead, change:** `.claude/agents/*`, `docs/research-theory-audit.md`, `docs/files.md` (via
  `python3 tools/inventory.py`), `README.md`.
- **Never changed without Numa's yes:** the page's physics code (state, integrator, drawing), the data-store taps
  (`ds.set`, `ds.var`; `docs/scripts/dataset.md`), the `<head>` with its security tags, the fold markup, the data panel, the
  shared scripts and stylesheets. A walkthrough's quoted code lines must stay character for character identical to the
  page's code; a mark `⟦key|…⟧` works only in its `math` and `code` fields, not in `note`.

## Numa's decisions so far

- 20 October 2026, branch: start from `docs/usul-cloudflare` (`db1a24b`); work on `claude/physics-notes-rewrite-cwctkk`,
  the branch this session may push to, in place of `notes/teacher-team`.

## Numa's verdicts

**20 October 2026, before the pilot. This rule overrides anything above that reads as "rewrite".** Numa, in his words:
"What rewrite? It should simply offer a proper derivations and explanations, good relaxed feynmaj like writing, IF NEEDED.
IF THE JUDGMENT SAYS THE EXPLANATIONS ARE CLEAR, THEN NO NEED. DO NOT OVER KILL MY SOMULATIONS!"

What this means for every agent:
1. **Judge first, edit second.** Read each section of the note against section 4 and give it a verdict: *clear, leave it*,
   or *needs work*, naming the exact sentence, step or symbol and why. No edit before the judgment exists.
2. **A clear section is not touched.** Not reworded, not lengthened, not restructured. The default is to leave things as they are.
3. **Where work is needed, the smallest change that fixes it:** a missing step in a derivation, a symbol defined before use, a
   physical picture where there is none, a wrong or unsupported claim, a missing link to a source. Not a new section where a
   sentence will do.
4. **Voice: relaxed and Feynman-like.** Plain, warm, physical; the reasoning shown as a person would explain it at a
   blackboard. No padding, no new formalism for its own sake.
5. **Do not overload the simulations.** No new sections, figures or boxes unless the judgment shows the explanation cannot
   stand without them. The page's code is never touched.

**20 October 2026, later.** Numa: "YOU JUDGE, YOU DECIDE, NOT ME". The lead judges each note and decides what changes; Numa
is not asked to choose between options. Where the brief says "ask Numa" or "wait for Numa's yes" about the notes (pilot
choice, pilot verdict, the swarm, the notes/ folder in the pull request), the lead decides and reports the decision with its
reason. Still out of bounds without his explicit word: page code, the walkthrough files `public/scripts/walk/*.js`, deploys, other
repositories, merging. Mismatches between a walkthrough and its note are listed with exact old → new text in
`notes/figNN/walk.md`, ready to apply when Numa allows it.
