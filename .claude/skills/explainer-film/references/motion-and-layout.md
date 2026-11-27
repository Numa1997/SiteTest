# Motion and layout

## The stage

Portrait, 1080 by 1920 CSS pixels, scaled to the screen by `fit()`. 30 frames a second.

| Part | Place | Type |
|---|---|---|
| Film title | left 40, top 40 | Instrument Serif 62 px |
| Picture (canvas) | left 28, top 150, 1024 by 1024 | drawn in canvas; labels IBM Plex Mono 24 to 30 px on a dark plate |
| Caption kicker | left 42, top 1206 | IBM Plex Mono 22 px, letter-spacing 0.14 em, accent colour |
| Caption title | below the kicker | Instrument Serif 60 px |
| Caption sentence | below the title | IBM Plex Sans 33 px, line height 1.42 |
| Readout | left 42, top 1690 | IBM Plex Mono 27 px, two lines at most |

A landscape film (1920 by 1080) puts the picture left (1024 square) and the caption column right; keep the same sizes.

Colours (night): background `#140d10`, ink `#f5f1ea`, second ink `#d9cdc4`, muted `#b9a59b`, accent rose `#e2a2aa`,
second voice (a twin, a special line) pale blue `#8ce6ff`, curves of reference white. Fill the canvas with the darkest colour of
any picture you draw on it, so no edge shows when the picture moves.

## Easing and the clock

```js
const ease = u => { u = clamp(u, 0, 1); return u*u*u*(u*(6*u - 15) + 10); };   // slow in, slow out
const ramp = (scene, f, t0, dur) => ease((sec(scene, f) - t0) / dur);          // 0 -> 1, starting t0 s into the scene
```

Everything that moves is a `lerp(a, b, ramp(...))`. To make a thing appear and later leave, multiply two ramps:
`ramp('far', f, 3.6, 1.5) * (1 - ramp('lean', f, 0, 1.2))`. To chain camera moves, apply them in order to one variable:

```js
let h = 7.2;                                   // half-width of the view, in the picture's units
h = lerp(h, 16, ramp('fill', f, 6.4, 6.2));    // each line moves on from where the last one ended
h = lerp(h, 9.5, ramp('pupil', f, 0.3, 2.2));
```

Start a scene's main motion 0.3 to 1.6 s after the scene begins, so the caption has started to rise first.
End it at least 1.5 s before the scene ends.

## Drawing through a linear map

Keep one 2 by 2 matrix `M` and one scale `S` (pixels per unit) for the frame. A point of the picture goes to the screen by

```js
const scr = (x, y) => [W/2 + S*(M[0][0]*x + M[0][1]*y),  W/2 - S*(M[1][0]*x + M[1][1]*y)];   // y up
```

Draw every curve, axis, grid line and label through `scr`. Draw an image that covers x in ±hx, y in ±hy with one canvas transform:

```js
const kx = 2*hx/img.width, ky = 2*hy/img.height;
g.setTransform(S*M[0][0]*kx, -S*M[1][0]*kx, -S*M[0][1]*ky, S*M[1][1]*ky,
               W/2 + S*(-M[0][0]*hx + M[0][1]*hy),  W/2 - S*(-M[1][0]*hx + M[1][1]*hy));
g.drawImage(img, 0, 0);
```

Animate a transformation as named moves, each with its own 0-to-1 progress, and build the matrix from them in a fixed order
(for instance turn · stretch · shear). Show the moves one after another, never mixed, so each has a meaning.
At full progress the matrix must equal the closed form; put that in `FILM.checks()`.
To go back, multiply each progress by `(1 - ramp('back', ...))`, last move first.

## Many marks

Read mark colours from the stored picture (draw it to a small offscreen canvas once, `getImageData`), choose positions with a
seeded random generator so every render is the same, and keep them in a typed array. Draw them onto an offscreen canvas that
covers the picture's box, adding only the new ones each frame; if the frame number goes backwards, clear and redraw from zero.
The count grows as `n0 * exp(k * t)`; choose k so the last mark lands about 2 s before the scene ends, then crossfade to the
whole picture over 2 s. Give dark marks a floor of brightness, or half the dots are invisible and the growth looks slow.

## An example window

The object that the film is about (a pendulum, a machine) appears large first, then moves into a window of at least 400 px in
a corner that the picture does not need. Draw its recent path as a fading trail (the last 1.4 s). A second copy that is being
compared with it is drawn first, in the second voice colour, so the main one lies on top.

## Labels

Mono text on a plate of `rgba(20,13,16,.78)` so it reads over any picture. Attach a label to the point it names
(`scr(...)` plus a small offset) and clamp it inside the canvas. Fade labels with the thing they name.

## Simulations in a film

Integrate at start, store the states at a fixed rate (240 a second is plenty), and interpolate by time. A pendulum scene then
reads `at(run, t)` for any t, so frames are independent. Use RK4 with a step small enough that the energy drifts by less than
one part in a million over the scene; report the drift in the checks. Play simulations at real speed or slightly slower
(0.85 to 0.95); faster looks frantic.
