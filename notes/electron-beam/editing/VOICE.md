# One voice for "The Electron Beam, from Tip to Measurement"

Every editor works from this sheet, so that ten chapters written by different hands read as one book.
The authority above it: `CLAUDE.md` (Design and explanations; Talk plainly) and `notes/STANDARD.md`.

## The reader
A Bachelor's student in physics, second or third year: knows Newton, Maxwell, basic quantum mechanics, calculus and
statistics; has never seen an electron microscope from inside. Numa will read and extend this text later; it must be
easy to pick up again after months away.

## The voice
- A lecturer writing lecture notes for that student, set like a LaTeX book. Calm, exact, friendly, never chatty.
- "We" for lecturer and reader working together ("we follow one electron"). "You" only in problems. No "I".
- Present tense, active voice. Say who does what: "the lens bends the ray", not "the ray is bent".
- Every section opens from something the reader can see or feel (a torch beam, a magnifying glass, rain on a roof),
  then the model, then the mathematics. Keep these pictures where they exist; add one where a section starts cold.
- No question-and-answer format, no rhetorical questions, no headings that are questions.
- No marketing words (powerful, cutting-edge, seamless, crucial, robust, leverage, key insight), no filler
  (it is important to note, interestingly, basically, in order to, it should be noted).
- No dashes as sentence glue. Use a full stop, a colon or a semicolon.
- British spelling (colour, neighbouring, centre), as the text already uses. SI units only.

## The rhythm
- One idea per sentence. Mean sentence length about 18 words; a sentence over 30 words must earn it; over 40 words is
  split, unless it is a list the reader scans.
- Vary the beat: after two long sentences, a short one. A short sentence states the point; the long one supports it.
- Paragraphs of 3 to 6 sentences. The first sentence says what the paragraph does.
- A term is defined the first time it appears, in plain words, before or right after its symbol.
- Every symbol is introduced with its meaning and unit the first time ("the beam half-angle α, in radians").
- The same thing has the same name everywhere (see the term list the unifier keeps in `editing/TERMS.md`).

## What an editor must not change
- Physics, claims, numbers, equations and their order. If something looks wrong, list it in your report; do not fix it.
- Any `{{num:…}}`, `{{eq:…}}`, `{{fig:…}}`, `{{figure:…}}`, `{{sec:…}}` marker; anything inside `$…$`, `$$…$$`, `\(…\)`, `\[…\]`.
- The keys and values of the `literals` (or similar) dicts, `css`, `ui_js`, `sim_html`, SVG strings, ids, labels.
- No new numeral in prose: `checks/check_numbers.py` fails on any number not drawn from the store or the literals.
- Citations and quotations stay word for word.

## How to prove the edit
Run, from the repository root, and paste the last lines into your report:
`python3 portfolios-src/electron-beam/build.py` · `python3 portfolios-src/electron-beam/checks/check_numbers.py` ·
`python3 portfolios-src/electron-beam/checks/selftest.py`.
Report: sentence count and mean length before and after per chapter; the number of sentences over 30 and over 40 words
before and after; every change that touches meaning (should be none); doubts about the physics you saw.
