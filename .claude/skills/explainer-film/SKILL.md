---
name: explainer-film
description: Make a short explanatory animation (an "explainer film", 1 to 2 minutes, captioned, no sound) that teaches one idea in physics, mathematics or data, as a live HTML page that is also rendered to an MP4. Use this skill whenever the user asks for an animation, a film, a video, a clip, a "small cute video", an animated explanation, or says "animate this", "show how it is built", "make a film of this figure", "explain it in an animation", or wants a picture transformed, populated or zoomed step by step, even if they do not use the word film. Also use it to revise or extend an existing film in tools/fig13/gift/.
---

# Explainer film

A film here is one HTML page that can draw any frame on request, plus an MP4 rendered from it. It teaches one idea to someone
who has not seen it before. The viewer watches on a phone, cannot pause to ask, and gives it about two minutes.

The films that were liked had three things in common, and everything below serves them:

1. **Every number on screen is true.** It is computed in the page or read from stored data, and a check proves it.
2. **One new thing per scene**, said in one sentence, with time to read it.
3. **Nothing jerks.** Every move starts slowly and ends slowly.

Start from the bundled template. It already runs, has the stage, captions, timeline, camera and checks, and it is much
cheaper to change a working film than to write one.

## The order of work

Do these in order. Each step ends with something you can show.

### 1. Understand before drawing

Write down, in plain sentences, the answers to these. If you cannot, read the code, the data and the sources until you can.

- What is one point, one mark, one curve on the picture? What experiment or object does it stand for?
- What are the axes? What unit?
- What decides the colour or the position of a mark? Which formula, which stored value?
- What is the surprising shape, and what causes it?
- If a transformation is shown: its exact formula, its parameters, where each number comes from, and its inverse.

Then get the numbers. Compute them (in the page, in a script, or with a symbolic tool) or read them from the stored data.
Do not estimate a number by looking at a picture, and do not write a number from memory. A film states things flatly, with no
room for "about" or "probably", so a wrong number in a film is worse than a wrong number in a text.

### 2. Write the storyboard

A table, one row per scene: what is on screen, what moves, the caption (kicker, title, one sentence), the seconds, and the
number shown in the readout. Read `references/storyboard.md` for the teaching order, the caption grammar, the timing table and
a complete worked example. Show the storyboard to the user if they asked to approve it; otherwise go on.

### 3. Build from the template

Copy `assets/film-template.html` to the film's place (in this repository: `tools/<figure>/gift/<name>.html`).
Keep the part marked KEEP. Replace the part marked REPLACE: the scene list, the data, and the drawing of each scene.
Read `references/motion-and-layout.md` before you draw: it has the stage geometry, the type sizes, the easing rules, the camera,
and the formulas for drawing a picture through a changing linear map.

Three rules of construction that make the rest possible:

- **A frame depends only on its number.** `renderFrame(f)` must draw frame f correctly whatever was drawn before, because
  the renderer and the player jump around. Precompute simulations at start and index them by time. If you accumulate
  something (dots piling up), be able to rebuild it from zero.
- **Every motion is `ramp(scene, f, start, duration)`**, an eased 0 to 1. No motion is written as raw frame arithmetic.
- **The film proves itself.** Fill `FILM.checks()` with one entry per claim: a matrix equals its closed form, energy is
  conserved by the integrator, two things that should part do part. The check script prints them.

### 4. Check before rendering

Run `scripts/check_film.cjs` (see `references/checks-and-render.md`). It loads the film, prints the checks and the scene table,
reports script errors, and saves the still frames you name. Then make a contact sheet with `scripts/contact_sheet.py` and
look at it: one frame near the middle of every scene, plus the busiest moments.

Look for: text over text, a label under a window, a caption cut off, a picture edge showing, a colour seam, something
unreadably small on a phone. Fix and repeat. This costs seconds; a full render costs minutes.

### 5. Render and deliver

Run `scripts/render_film.cjs ... --mp4 NAME.mp4`. Send the MP4. Say plainly what you checked and what you did not: if you
looked only at still frames, say that the pace is the user's to judge. List what they may want changed (length, the slowest
scenes, anything simplified).

### 6. Only after the user says it is good

Add it to the site (in this repository: the list in `tools/fig13/gift/film_page.py`, then `publish_films.py`), write what the
page now shows into the docs page of the figure, and update the notes. A film the user has not judged stays off the site.

## Rules of motion, text and honesty

These are short because the references explain them; they are here so you never have to open a file to remember them.

- Ease every move with smootherstep, `u*u*u*(u*(6u-15)+10)`. Linear motion reads as mechanical and sudden motion as a mistake.
- A camera move, a transformation or a fade takes 1.5 to 6 seconds. A caption gets 0.7 s to rise in and is fully readable for
  at least 4 seconds. A scene lasts at least a quarter of a second per word of its sentence, plus 1.5 s (the film that set this
  standard reads at that pace); the template's checks test it.
- Captions: a mono kicker with the scene number, a serif title of at most six words, one sentence in plain words.
  The sentence says what the viewer is looking at now, never what is coming.
- One readout line or two under the caption carries the live number: the matrix at this instant, the time, the count.
  It changes smoothly with the picture, so the viewer sees the formula move.
- Show an example before the many. One strike with its pendulum, then twelve dots one by one, then thousands.
  The viewer must know what one dot is before the dots multiply.
- When a picture is transformed, transform everything drawn on it with the same matrix: grid, curves, axes, labels.
  A grid makes a shear visible; without it the eye sees only a picture changing.
- A transformation that can be undone is shown undone at the end. It proves nothing was lost, and it returns the viewer to
  the picture they know.
- Use the house design: titles Instrument Serif, text IBM Plex Sans, labels IBM Plex Mono, the night palette of the template.
  Do not introduce a font or a colour that the template does not have without a reason you can state.
- No sound unless asked. No invented data. No "approximately" for a number you could compute.

## What went wrong before, so you can skip it

- A `//` comment added in the middle of a long line silently removed the rest of the line (the picture stopped loading, no
  error). Put comments on their own line.
- A label was drawn at a fixed place and ended up under an inset window. Let labels ride on the thing they name
  (`scr()` of a point on the axis), and clamp them to the stage.
- The panel behind a picture had a slightly different dark than the picture's own dark, so the picture's edge showed when it
  turned. Fill the stage with the picture's darkest colour.
- An inset that shows the example was too small to read on a phone. An example window is at least 400 px of the 1080.
- A test clicked before the picture had loaded. Wait for `window.__ready`.
- A claim in a caption came from looking at a picture ("starts at roughly 20 J"). Measured, it was 12 to 16 J. Measure first.

## Files

- `assets/film-template.html`: the working starting point. Read its comments.
- `references/storyboard.md`: how to plan the story; the worked example "Why the map is an eye".
- `references/motion-and-layout.md`: stage, type, colour, easing, camera, drawing through a matrix, dots, labels.
- `references/checks-and-render.md`: the commands, what to check, the encoder settings, sizes.
- `scripts/check_film.cjs`, `scripts/contact_sheet.py`, `scripts/render_film.cjs`.
- A finished film to read as a model: `tools/fig13/gift/eye.html` in this repository.
