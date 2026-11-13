# Fig. 15: the final goal, and every mistake made on Fig. 14

Written on 13 November 2026 by the session that built Fig. 14, on the owner's explicit instruction. Read it with `BRIEF.md`; where
the two differ, this file wins. Its purpose: you must not repeat a single one of these mistakes.

## 1. The final goal (the owner's words, repeated many times)

**A working, smooth, functioning animation, live on the website.** The pipeline, fixed:

1. **Generate the data on Kaggle.** That means every frame of every case the page offers. The project is 3D (see the CORRECTION
   in `BRIEF.md`): the 3D runs go on Kaggle's GPUs, each launch with the owner's yes and a bill. It is built on all the stored 3D
   data of Fig. 14, not only the flat wall.
2. **Bring it into the repository** (GitHub), filed under `public/data/resonant-tunnelling/<date>/…` with SHA-256 and provenance.
   Cloudflare then serves it on the website.
3. **The page only plays the stored frames.** Between two stored frames it interpolates smoothly (section 3, item 1). It never
   generates the wave step by step, never solves an equation while the reader watches, and never recomputes what the store holds.
   (`BRIEF.md` first said B3's analytic reconstruction could run in the page. That is overruled: the reconstruction runs on Kaggle,
   or in a tool script whose output is stored, and the page plays its output.)
4. **Derived data has its own place.** Data made from Fig. 14's stored runs goes in `derived/`, and every file in it names its parent
   files by SHA-256. New Kaggle runs go in `kaggle/`.

Everything else (the derivation, the lecture note, the panel) serves this goal. A beautiful note next to a stuttering animation
is a failure.

## 2. What went wrong on Fig. 14, and what fixed it

### Pictures that were not what they claimed

- **Wrong labels.** "Ball" shapes were shown as spherical waves, but they were slices of a flat wave. The owner rightly exploded.
  Never label a picture as something it is not.
- **Holes and needles.** Spherical shells were drawn by marching cubes on a coarse cube (0.75 a), which made a "football pattern" of
  holes and needle spikes. Fix: draw from the exact geometry (true spheres, surfaces of revolution), or resample finely first.
- **Ragged sheet edges.** Marching cubes on the stored 0.5 a grid (4 to 6 points per wavelength) cut the rims into saw teeth. Fix:
  resample the field before cutting (Lanczos, 1/6 a along the flight, 1/3 a across) and do the cutting in a worker.
- **Needle spikes on the height surface.** The tallest point was set to a seventh of the sheet's width, but the waves are 2 to 6 a
  long on a sheet 48 a wide, so the crests stood up as needles. Fix: limit the steepest slope to 1.5. Choose a height scale from
  the slope, never from the width alone.
- **Facets.** A sheet stretched over the stored points alone looks faceted. Fix: band-limited (Fourier) resampling to at least
  12 points per wavelength. It passes through every stored value and adds no new wave. Say so on the page.
- **Sheets vanished late in a run.** The level that draws the sheets was fixed, so they disappeared as the wave spread out. Fix:
  set the level relative to each frame's largest value.
- **Torn sheets from coarse storage.** One stored set kept only 127 levels relative to the *first* frame's peak; once the wave had
  spread, a crest was a handful of levels. Fix: store 8-bit levels of **each frame's own peak**, with the list of peaks in the file
  header.
- **Rendering details**, each of which cost a round with the owner:
  - colours washed out (vertex colours must be converted from sRGB to linear in three.js);
  - moiré (a surface must not receive its own shadow);
  - black sheets (the triangle winding flips when you swap axes for the renderer);
  - colours outside the house palette (use the house colours from the start: slate `#55607a` at the bottom, paper `#fbf6ee` at
    zero, wine `#a3303f` at the top, ink `#1c1518` for lines).
- **The barrier moved with the wave and looked flat.** In the mesh view the barrier was only an outline laid on the wave sheet and
  lifted to its height, so it rode up and down with the crests. The 3D solid was hidden in that view. Still open on Fig. 14. On
  Fig. 15 the potential must be a static solid from the first version.

### Motion that was not smooth

The owner's judgement of the first animation: "horrible, glitches and slow". Every cause:

- **Steps instead of motion.** 48 stored frames shown one after the other means five jumps a second. Fix: interpolate on every
  screen frame between stored frames f and f+1, inside the frame that turns at the wave's energy:

  ψ(t₀ + τ) = e^{−iEτ} [(1 − s) ψ_f + s e^{iEΔt} ψ_{f+1}], with s = τ/Δt.

  At a stored frame this gives exactly that frame. Better still for Fig. 15: store enough frames (e.g. 200 to 400 per run for a
  run) so the interpolation only smooths.
- **Freezes on every new frame.** Resampling took 25 to 70 ms and marching cubes 100 to 200 ms, on the main thread. Fix: Web
  Workers that work ahead of the playhead; no per-frame allocation (reuse typed arrays, a colour lookup table). Target under 5 ms
  of page work per screen frame, **measured**.
- **A jumping height scale.** Normalising each frame separately made the picture jump. Fix: blend the scale between frames like
  the wave, or use one scale per run.
- **Slow playback.** A "governor" slowed playback near slider edges and through the last quarter of each run. Fix: a stored run
  plays at full speed, rests about 1 s at its end, and loops.
- **Sliders jump from run to run.** Each slider jumps between stored grid points, and the owner asked why it isn't smooth "when you
  have all the data". Decide this up front: a grid fine enough in the parameter the reader drags most, and/or a clearly labelled
  blend between neighbouring runs. Say which on the page.
- **Checking.** Before saying "smooth", measure in a browser: the median and largest gap between screen frames, and the page's
  milliseconds per frame. Look at screenshots at early, middle and late times, at 390 and 1440 px. Then publish.

### Physics and data mistakes

- **Wrong start waves.**
  - The spherical wave "from the side" started with its source 12 a away and r₀ = 6, so the shell began *inside* the barrier.
  - Hard walls were applied after the start, so the tail of the start wave inside the wall stayed there (up to 85 % of the peak).

  243 runs had to be recomputed. Rule: check the start state of every run in code before launch (no amplitude inside any barrier,
  packet wholly on one side), and set the start wave to zero inside a hard wall.
- **"Hard wall" as an infinitely high potential.** Removing ψ inside after every step lost 4 % of the probability, and up to 26 %.
  Fix: a finite height (200) with a shorter time step, which is pure phase and conserves probability. State the method.
- **A grid far too large.** The 3D batch had 1458 runs; coin and tube alone (13 heights × 5 sizes) were 80 % of the cost. Size the
  grid from what the page will show and justify each axis.
- **A wrong claim, made and retracted.** A "first order" convergence claim came from comparing results at mismatched end times.
  Compare like with like.
- **Tests that weren't tests.** A direct-solve test returned no solution at 2 of 6 parameter sets (an ill-conditioned linear
  system) and that was nearly reported as agreement. If a check fails to run, say so.

### Kaggle and process mistakes

- **Launched jobs nobody could watch**, twice. The connector shows logs only after a session ends. The owner: "I just gave you
  shit over it, and you just made the same mistake again." Rule: a tracker *you* can read during the run, or short notebooks that
  finish and report. Tell the owner before launching, not after.
- **A GPU launch without asking.** One was attempted without the owner's yes; the permission check blocked it. Never.
- **CPU notebooks that died in 10 s** because the code called `nvidia-smi`. Run the notebook's own code end to end on a tiny case
  locally before sending. Run pyflakes.
- **Runs that couldn't be cancelled.** The connector's cancel needs a session id it does not return. Know this before launching
  four parallel notebooks.
- **Bad cost reports.** One message read "about 2.1 GPU hours, about 1 hour on the clock" with no explanation, and called a 4.6×
  speed-up "only". Report costs properly:
  - define clock time and device time;
  - show the arithmetic: runs × cells × steps × measured time per cell-step;
  - state the share of the weekly 30 GPU hours.
- **Silent fallbacks.** When the owner asks for Wolfram, use Wolfram (the MCP tools and the wolfram-language skill), not SymPy.
  Ask before substituting tools.
- **Too many tests, too many questions.** The owner said "stop testing" and "quit stalling". Test once, properly, before publishing.
  Don't ask about things already decided, such as option lists whose answer is "all of them".

### Explanation mistakes (the owner rejected four attempts)

- **Results quoted instead of derived.** One version cited a problem number from a textbook from memory; it was never checked.
  Never cite from memory; read the source.
- **Search summaries passed off as sources.** Read the paper itself (Griffiths & Steinke was read in full; do the same for every
  source).
- **Steps skipped and symbols thrown at the reader.** Matrices with w, z, z\* were never explained, and "functional analysis" was
  hand-waved. What finally worked: one running numerical example. Every symbol was introduced in words with its value, every
  substitution shown, and each matrix built from the two edge equations by hand with numbers. Then the same answer was shown two
  ways (matrix product and summed bounces) and checked to agree. Then the source was cited equation by equation, with what Wolfram
  checked.
- **Tables and jargon instead of a story.** The note must read top to bottom like a good lecture: picture, model, mathematics,
  numbers, device.

## 3. Code rules that would have prevented most of the above

1. The page reads, it never computes physics: `Sim.dataset()` store, every number written where it is computed, the panel only
   reads.
2. Heavy work in Web Workers, ahead of the playhead; measured frame times.
3. Stored data: per-frame normalisation with the peaks in the header (or float32), SHA-256 per file, `index.json` and
   `generations.json`, provenance (notebook, version, commit; parent files for derived data).
4. Resampling only by methods that return the stored values at stored points (band-limited or Lanczos), and the page says so.
5. Static potentials, drawn as solids, never tied to the wave's height.
6. One worked example carried through note, code checks and data panel.
7. Before claiming anything works: real browser, screenshots you have looked at, frame times measured, live page checked after
   merge.

## 4. A mistake made in writing this brief (13 November 2026)

The first version of `BRIEF.md` and of this file framed Fig. 15 as one-dimensional and CPU-only, built on the 1D flat-wall cut
alone. It ignored the 3D runs already stored (sphere, true-3D sphere, pillar, spherical waves, coin, tube, the side cases), though
the owner had said again and again that the new figure must use the data we already have. That framing is withdrawn; see the
CORRECTION at the top of `BRIEF.md`.

