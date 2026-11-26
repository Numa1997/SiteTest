# Why a chaotic simulation cannot be stored start by start, and what the site does instead

Written 26 November 2026, while moving Fig. 2 (the double pendulum) to Kaggle. The rule at the end is the user's.

## The question

Fig. 1 (two circular wave sources) is stored whole, every slider at its full step, in 290 files and 36.5 MB
(docs/kaggle-sims.md, "Figures on the line"). The double pendulum, stored at the full step of only its two angle sliders, would
need about 1 587 GB. Why is one simulation 40 000 times larger than the other?

## Linear systems: sizes add

The wave equation is linear, so solutions superpose: the field of two sources is the sum of two copies of one ring,

    psi(x, t) = f(|x - x_1|, t; k, gamma) + f(|x - x_2|, t; k, gamma).

The page stores the one ring function f once, as a table. Moving a source only changes where in the table the page reads; it
needs no new data. The ring also depends smoothly on its parameters (wave number k, damping gamma), and Fig. 1 chose its stored
variable so that the dependence is linear: a value between two stored nodes is an exact blend of its neighbours. Each control
therefore adds one axis to one table, and the sizes of the axes add: tens of MB for every state the sliders can reach.

Picture: a kitchen where every dish is a mix of two stock sauces. Store the sauces; mix at the table.

## Chaotic systems: sizes multiply

The double pendulum is nonlinear, so the motion from start A plus start B is not motion A plus motion B: nothing can be shared
between runs. It is also chaotic: two starts a distance d_0 apart separate as

    d(t) ~ d_0 exp(lambda t),     lambda = 1.38 per second (default start, measured: reports/double_pendulum/study.md, section 2).

Over a 20 s run the gap grows by exp(1.38 x 20) = exp(27.6) ~ 1e12. For a blend of two stored neighbours to stay within 1 mm of
the true motion at t = 20 s, the neighbours would have to start about 1e-15 m apart, below the resolution of a 64-bit number near
1 m. So there is no blending: every start is its own film, and the number of films is the product of the number of steps of
every slider.

Picture: the weather. Yesterday's forecast says nothing about a day that started one degree warmer; each day is computed from
its own start.

## The numbers (from the full GPU run of 23 November 2026, notebook version 6)

| | starts | bytes | Kaggle time |
|---|---|---|---|
| one stored film (20 s, about 54 frames a second, 9 int16 columns, twin included) | 1 | 19 594 (7 053 765 604 / 360 000, measured) | 2.6 ms (937.7 s / 360 000) |
| the stored grid: angles every 15 degrees, 5 mass ratios, 5 length ratios, 5 values of each omega | 360 000 | 7.05 GB | 16 min |
| angles at the slider's 1 degree, the other axes as above | 360 x 360 x 625 = 81 000 000 | 1 587 GB | 58.6 h |
| every slider at its full step (93 x 65 x 360 x 360 x 101 x 101) | 8.0e12 | 157 PB | 5.8 million h |

Packing a film harder (no twin, fewer frames) saves a factor of 2 or 3, never the factors above.

## The rule (the user, 26 November 2026)

A simulation with this character (nonlinear and chaotic, or whose data would be huge) is not stored start by start. Instead:

1. **Kaggle computes the interesting parameterized manifold** of the system: a map over its parameter space that the browser
   could never compute in a frame, swept through a further parameter, and records it as a **film**. The film's numbers are
   stored beside it, so every pixel can be traced to a stored value.
2. **The page shows the film**, and next to it **the live simulation stays**, computed in the visitor's browser, with every
   control at its full range and step, for play and for changing parameters live.
3. The two are joined: a point picked in the film can be started in the live simulation, and the live run checks the stored
   value (same equations, same method, same step).

For Fig. 2 the manifold is the flip-time map: each pixel is a start (theta_1, theta_2) released from rest; its colour is the time
until either rod first passes over the top; the film sweeps the mass ratio m_2/m_1 from 0.1 to 10.
