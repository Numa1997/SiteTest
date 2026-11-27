# Checks and rendering

All three scripts use the Chromium and Playwright already installed. Do not install another.
The film is opened over HTTP, so start a server at the repository root first and leave it running:

```bash
nohup python3 -m http.server 8766 >/dev/null 2>&1 &
```

`SK` below is this skill's folder; `OUT` is a scratch folder outside the repository.

## 1. Check

```bash
node SK/scripts/check_film.cjs "http://localhost:8766/tools/fig13/gift/NAME.html" OUT/stills 60 250 450 ...
```

It prints the length, the scene table, every entry of `FILM.checks()` with pass or fail, and any script error, and saves a
JPEG of each frame number you list. Choose one frame near the middle of every scene and one at each busiest moment.
A film with a failing check or a script error is not rendered.

## 2. Contact sheet

```bash
python3 SK/scripts/contact_sheet.py OUT/stills OUT/sheet 7
```

Writes `sheet_1.jpg`, `sheet_2.jpg`, ... with seven frames a row. Read each sheet as an image and look at every frame.
Then read two or three single stills at full size where text is small.

## 3. Render

```bash
node SK/scripts/render_film.cjs "http://localhost:8766/tools/fig13/gift/NAME.html" OUT/frames --mp4 OUT/NAME.mp4
```

Run it in the background; a two-minute film (about 3,900 frames) takes five to ten minutes. It writes JPEG frames, then
encodes with `libx264`, quality 18, `yuv420p`, 30 frames a second, with the index at the front so the video starts at once.
A two-minute film is about 40 MB. Delete the frames afterwards.

Options: `--size 1920x1080` for a landscape film, `--frames 0,30,60` to render a few frames only, `--scale 2` for stills at
double density (do not use it for the whole film).

## What a film page must provide

- `window.__ready = true` when pictures, fonts and precomputed data are loaded.
- `window.FILM.frames()`: the number of frames.
- `window.renderFrame(f)`: draw frame f, whatever was drawn before.
- `window.FILM.scenes`: `{ name: [firstFrame, endFrame] }`.
- `window.FILM.checks()`: `[{ name, pass, value }]`.
- With `?film=1` it draws only on request; without it, it plays by itself in a loop, so it can be opened and watched.

## Before saying it is done

- The checks pass and are quoted in the report with their values.
- Every scene was looked at in a still.
- The MP4 exists, its length matches frames / 30, and it was sent.
- The report says what was not verified (usually: the pace, since stills cannot show it).
- Nothing was added to the site.
