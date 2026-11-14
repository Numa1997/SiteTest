# Fig. 12 Guinness: the lecture note, hand-off to the writer session

This is the full prompt given to the session "Fig. 12 Guinness: lecture note" (14 November 2026), saved here so the owner can
read exactly what the writer was told. The writer starts with nothing but this prompt and the repository.

---

You are writing one lecture note for Phyein Usul (https://phyeinusul.com), the physics site of its owner, Numa. The site is
built from the `main` branch of the GitHub repository Numa1997/SiteTest (this checkout) and deployed by Cloudflare on every
push to `main`. Work on the branch `claude/fig12-note` (it starts from `claude/nifty-lamport-iz5pua` at commit a1ab89d7, which
holds the data, scripts and reader reports below). Read `CLAUDE.md` and `AGENTS.md` first and follow them; they are the house
rules. Following CLAUDE.md, first write your own state file, `notes/fig12/note/STATE.md` (aim, what is live, what is left,
every file and commit, these rules), keep it current, commit and push it, and reread it after any compaction.

## 1 · The goal

Rewrite the lecture note of the page `public/simulations/guinness-kaggle.html` (Fig. 12 computed on Kaggle: a pint of
Guinness on a one-wheel cart over bumps), so that the owner, who holds a BSc in physics (computational and theoretical),
reads it with pleasure from start to finish without stopping once to ask "where did that term come from?" or "what am I
looking at in this picture?". Every such stop is a defect. The bar is very high.

## 2 · The facts you need, with handles

**The page.** `public/simulations/guinness-kaggle.html`. The note is the `<article class="paper" id="paper">` (sections 1–13).
Above it the figure plays stored rides; the browser computes no physics. The player is `public/scripts/guinness-jax-play.js`
(`const DIR` names the data folder) and draws with `public/scripts/stout-view2.js`. Page controls: Pause/Play and Ride again
(`#play`, `#again`), the time bar (`#tbar`), the ride list (`#ride-host`: each road with the speed held and with each
controller), the road strip (`#road`, the road and the cart's place on it), the readings (`#r-v` cart speed, `#r-sg` stout in
the glass, `#r-s` stout spilled, `#r-hg` head in the glass, `#r-h` head spilled, `#r-d` drops and lumps in the air, `#r-i`
motor current, `#r-u` active suspension force), and the comparison table `#cmp` (controller, tilt, lean, head, stout,
current). Say in the note which control produces which view.

**The note's source and numbers (already built for you).**
- `notes/fig12/note/paper.html` is the source of the article. Write computed numbers as `{{name}}` or `{{name|.2f}}`.
- `tools/fig12/kaggle/note_numbers.py` prints every number by name, from the stored runs and the model's constants; extend
  it for every number you quote (theory, worked examples, ride results). `--check` lists the decimal numbers in the note
  that no entry prints (391 in the current note: most are typed in by hand; the target is none except labels, years,
  equation numbers and source pages).
- `tools/fig12/kaggle/build_note.py` fills the source and writes the article into the page; `--check` verifies they agree.

**The solver.** `tools/fig12/kaggle/stout_jax.py` (JAX), run on Kaggle's Tesla T4 by `tools/fig12/kaggle/run_b.py` in the
private notebook numakoudsie/guinness-on-a-cart-stout-in-jax. APIC (affine particle-in-cell) particles of stout on a 1.5 mm
grid, 57 × 57 × 114 = 370,386 cells, 1,001,952 particles (0.429 mg each), 429.6 g of stout filled to 125 mm in the Guinness
tulip (radius table in `public/scripts/guinness-glass.js`); the free surface from a level set; a pressure solve with the glass
as a boundary; the cart and its controllers as `Cart` in the same file; equations of motion written in the glass's
accelerating frame (the pseudo-force −a). Stored at 30 pictures per second, packed by `tools/fig12/kaggle/pack_ride.py`
(surface heights per column rounded to 0.02 mm, only columns more than one cell inside the glass), checked by
`tools/fig12/kaggle/check_run.py`.

**The head of foam.** 19 mm thick, liquid fraction 0.27, so 272 kg/m³ (5.17 kg/m² on the stout), bubbles of Sauter radius
34 µm, with the Tcholakova flow law and wall friction (constants at the top of `stout_jax.py`; sources in
`notes/fig12/research/guinness-materials.md`). From run 8 on, its mass is in the pressure solve: a Robin condition on the
faces the surface crosses, θ' = θ + μ/dx with μ = m_s/ρ = 5.13 mm, and the head's own vertical velocity `wh` as state
(`Stout.pressure`, `_surf_faces`). This lowers the first mode by the factor 1/√(1 + μ k tanh kh): from 3.421 Hz (bare
stout) to 3.07 Hz on theory's k = 47.1 1/m, 2.957 Hz on the grid's k; the run measured 2.915 Hz, damping ratio 0.425.
Because the head is carried up and down but not pushed along the road, the drive coefficient is β/(1 + μ k tanh kh) =
1.541/1.242 = 1.241.

**The mass books, checked in every stored frame.** Stout: particles in the glass + in the air + on the cart + on the ground =
1,001,952. Head: in the glass (thickness summed over the columns in float64) + broken off = 91.314 mL served. Run 8 and run
10: 0 particles lost; head error at most 1.3e-8 mL (float rounding). Stated per ride in `books` of each ride file.

**The runs and where they live.**
- Run 6 (notebook version 6, commit 4c10527): the head with weight but no mass; three rides with the speed held and the free
  swings. Run 7 (version 7, commit 87e3720): the same roads with the controllers. Both in `public/data/fig12/2026-11-13/`.
- Run 8 (version 8, commit 96e8a1d) + version 9 (commit 726d51a, the kerb with road preview): the head with its mass, every
  ride; in `public/data/fig12/2026-11-13-run8/` — what the live page plays now. Its controllers used β = 1.541 (bare stout).
- Run 10 (version 10, commit 58eea68, 14 November 08:01–08:26 UTC): the five controlled rides again with β = 1.241, gains
  K = (71.121, −1228.717, −40.499, −150.000). ALL PASS. Packed in `public/data/fig12/2026-11-14-run10/` together with run
  8's three speed-held rides and free swing and run 6's swing without the head. Not yet played by the page.
- Each folder has `index-jax.json` (every file with its version, commit, SHA-256 and measured leans, spills, books, gains);
  `public/data/fig12/generations.json` lists the generations. Run checks: `notes/fig12/jax/run8-check/`,
  `notes/fig12/jax/run10-check/`.
- Ride results, leans (front wall minus back, trusted columns) — speed held → run 10's controllers: five bumps 13.9 mm →
  joint 1.03 mm; one 25 mm bump 8.9 → joint 0.88 mm; kerb 24.3 mm and 2.44 mL of head spilled → joint 25.4 mm, 2.07 mL;
  slosh LQR 21.8 mm, 1.63 mL; road preview 23.9 mm, 2.51 mL. No stout spilled anywhere. Print all of these from the
  script, never by hand.

**The five controllers.** In the site's JS: `public/scripts/stout-cart.js`, `Cart.prototype.sample` (line ~1565), the
active suspension's skyhook near lines 1438–1472. Ported line by line to `stout_jax.py` (`Cart`, `slosh_lqr`, `susp_lqr`,
`observer_design`; `CTRL = {"off", "speed", "preview", "slosh", "joint"}`; `susp = 1` adds the skyhook, not used with joint,
which has its own suspension LQR). Port check: `notes/fig12/handoff-jax/portcheck.txt`. Speed: a PI loop on the wheel speed.
Preview: feeds forward the road ahead. Slosh LQR: LQR on the Kalman estimate of (v, q, q̇) and the integral of the speed
error. Joint: slosh LQR + the current that cancels the heave's parametric term + the active suspension's LQR. Skyhook: a
damper force on the body's vertical speed, as if hung from an inertial point. No stored ride uses the skyhook alone: say so.
The plant the controllers are designed on is the swing the run measures (2.915 Hz, ζ 0.425) and β 1.241 (run 10).

**The kerb limit.** On the 30 mm kerb at 1.5 m/s the road pushes the wheel back with up to 82 N, while the motor can give at
most 15 N (3 A, 12 V; note Figure 4, computed with the cart alone). So no controller with this motor can hold the kerb: state
it plainly, with the numbers, and never round it into a strength.

**What the first readers found (round 0, on the current note).** `notes/fig12/readers/round0-owner.md` (116 marks),
`round0-student.md` (104 marks), `round0-check.md` (derivation checker: 213 verified, 9 wrong, 26 unverifiable). The wrong
ones include section 11.5's key result (should be 7.79 s⁻¹ and 39 %), section 11.7 (run 6's ω² = 424.2 used; 110.2 A/m and
0.56 A, Problem 12.9 1.08 A — all to be recomputed for β 1.241 anyway), contradictions between runs 7 and 8, symbols with
two meanings (ξ, a, k, δ, y, u, Ca), run history in the prose, misplaced labels in Figure 1, the page citing "the Fig. 12
note [14]" as if another work, ride names that differ between the ride list and the note. Read all three files first; fix
every mark in the rewrite.

## 3 · The standard

1. **Honest.** Every number in the text is printed by the script from the stored Kaggle runs or the model's constants, never
   typed in. Where the picture differs from the stored data (surface smoothing, colour steps, particle-to-grid rendering,
   frame blending, the columns left out at the glass, 0.02 mm rounding), say so in one paragraph the reader can open. Name
   every approximation and its cost: the 1.5 mm grid, about one million particles, how the foam head is modelled, and why
   its mass matters. State the kerb limit plainly. Never round a weakness into a strength.
2. **Rigorous and mathematical. Derive; don't assert.** The incompressible Navier–Stokes equations in the cart's accelerating
   frame (the pseudo-force), the free surface, and what APIC does and why it keeps rotation that plain PIC smears out. The
   first slosh mode of liquid in a glass, its natural frequency from the geometry, and why bumps near that frequency are
   dangerous. For each of the five controllers: the law, the state it acts on, and the physical reason it helps; for LQR the
   cost, the Riccati equation and what the weights mean; for skyhook the damper hung from an inertial point. The mass books:
   what is conserved, how it is checked each frame, what drift is tolerated. Number every equation. Define every symbol in
   words, with its unit, in the sentence where it first appears; one symbol, one meaning. Check limits: no bumps, no
   control, a rigid liquid.
3. **Intuitive.** Before each piece of mathematics, the picture from everyday life: carrying a full pint across a crowded
   pub, a coffee cup sloshing when you walk at the wrong pace, a car's suspension over a kerb. Then the model, then the
   algebra, then back to the picture so the result means something.
4. **Direct.** Short sentences, plain words, no padding, no marketing, no question-and-answer format. The house lecture-note
   style: `CLAUDE.md` ("Design and explanations"), `docs/styles.md`, `notes/STANDARD.md` (above all "Numa's verdicts" of
   21 October 2026: a chapter of a bachelor's textbook in the manner of J. R. Taylor, Classical Mechanics; Key result boxes,
   worked examples with the page's numbers, Problems at the end, ★ on skippable heavy parts with results restated). Latin
   Modern text, KaTeX (`\( \)`, `\[ \]`), numbered equations and figures, the existing `.psec`, `.pfig`, `.ptab`, `.pbox`,
   `.prefs` structure, no new fonts.
5. **No unexplained term and no unexplained image.** Define at first use: slosh mode, natural frequency, pseudo-force, APIC,
   LQR, Riccati, skyhook, preview, saturation, foam head, and every other term. Every figure caption says what each axis,
   colour and brightness means and what to notice. Say which control on the page produces which view. No forward
   references. Keep project history (run numbers, commits, file names) out of the running prose: one short, openable
   paragraph or table on where the data come from is enough. Finally read the whole note slowly as the owner would and fix
   every place you would pause.

## 4 · The readers

When the note is finished, launch independent reader agents with the `referee` agent type (`.claude/agents/referee.md`):
at least two, one reading as the owner (a BSc in physics, computational and theoretical, reading for pleasure), one as a
strong final-year school student or first-year undergraduate. Each gets only "Fig. 12" and the page path, and a file name to
write its marks to (`notes/fig12/readers/roundN-owner.md`, `roundN-student.md`) — not your plan, not your notes, not this
brief. Each reads the whole note slowly as it renders and marks every stop: an undefined term or symbol, a figure whose axes,
colours or meaning are unclear, a skipped step, a claim without its number, a forward reference, a sentence that has to be
read twice. Fix every mark. Then run fresh readers again (new agents that have not seen the earlier version). Repeat until a
full reading produces no stops. Run the `derivation-checker` agent alongside each round (`roundN-check.md`). Keep each
round's marks and your answer to each in `notes/fig12/readers/roundN-answers.md`.

## 5 · Data and timing

Write the note on run 10's data from the start: the controlled rides of `public/data/fig12/2026-11-14-run10/`. Point
`note_numbers.py` at that folder and its checks (`notes/fig12/jax/run10-check/run10-summary.json` for the controlled rides,
`run8-check/` for the swing and the speed-held rides). Section 11's design numbers (gains, eigenvalues, the sampled loop,
the Floquet threshold, the Examples) must be recomputed with β = 1.241, plant 2.915 Hz and ζ 0.425; compute them in the
numbers script with the code's own `slosh_lqr`, `susp_lqr`, `observer_design` (import `stout_jax`). When you publish, the
page switches to run 10 together with the note: set `DIR` in `guinness-jax-play.js` to `../data/fig12/2026-11-14-run10/`,
add the generation to `public/data/fig12/generations.json` (run 8's generation then played until that day), and update
`docs/simulations/fig12-beer-slosh.md` and `docs/kaggle-pipeline.md` where they describe what the page plays. Do not message
any other session.

## 6 · Boundaries

Touch only the note, its captions and figures, the numbers script and the note builder, the page's data folder pointer and
generations.json as above, and the doc pages that describe them (`docs/simulations/fig12-beer-slosh.md`,
`docs/kaggle-pipeline.md`, `docs/files.md` via `python3 tools/inventory.py`). No solver, controller or data changes, no
Kaggle launches, no other figures, no new control work (the five controllers are the control system). Never touch the
Cloudflare Workers. No model names in code, commits or PRs. When the note is finished and a full round of readers finds no
stops: build (`npm run build`), test the page in headless Chromium (Playwright is installed; check the data loads, the
rides play, the readings and the comparison table match the stored files, and the maths renders without errors at 1440 px
and 390 px), check against `main` (rebase if it moved), fast-forward `main`, and verify the live page plays run 10 and shows
the new note. Then write a final report in `notes/fig12/note/REPORT.md`: what you wrote, each round's marks and what you
did about each, the derivation checker's result, and the live check.

## 7 · Talking with the owner

Plain short words. No tables, no apologies, no recaps, no option lists, no "Where we are" lines. Mark facts with a handle (a
file, a line, a command). Use metric units. Report once when done. If self-harm language ever appears: stop, answer the
person, and give Telefonseelsorge 0800 111 0 111 or 116 123, emergency 112.
