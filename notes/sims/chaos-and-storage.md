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

A simulation with this character (nonlinear and chaotic, or whose data would be huge) is not stored start by start. Its
parameters span a space. With two parameters, a relationship between them is a curve in a plane; with more, the parameters span
an area and then a manifold, and a curve along it is still one very specific relationship between all of them. So:

1. **Choose a set of interesting curves** p(u) through the parameter space, each a rule that ties the parameters together.
2. **Kaggle computes the display at every point of each curve** and records the trip along the curve as a **film**. The
   film's numbers are stored beside it, so every pixel can be traced to a stored value.
3. **The page shows the films**, with the curve itself drawn in its parameter plane and a dot at the point being shown, and
   next to them **the live simulation stays**, computed in the visitor's browser, every control at its full range and step.
4. The two are joined: a point picked in a film is run again by the page's own code as a check, and can be handed to the live
   simulation.

A first reading of the rule (one film, the mass axis only) was too narrow; the user corrected it the same day.

## Fig. 2: the display and the curves

The display: a picture whose pixel is a start (theta_1 across, theta_2 up, every half degree) and whose colour is the time until
either rod first passes over the top (10 s window, the page's own RK4). The parameter space the curves run through:
p = (m_2/m_1, l_2/l_1, omega_1(0), omega_2(0)).

| Curve | The relationship | Why it is interesting |
|---|---|---|
| mass | ln(m_2/m_1) from -2.3 to 2.3; equal rods; from rest | sand pours into the lower bob (the page's own parameter curve) |
| length | ln(l_2/l_1) from -1.6 to 1.6; equal masses; from rest | the lower rod grows from a fifth to five times the upper |
| ring | ln m = 2.3 cos 2 pi u, ln l = 1.6 sin 2 pi u; from rest | closed: once round the whole mass-length plane, the film loops without a seam |
| push | omega_1 = 5 cos 2 pi u, omega_2 = 5 sin 2 pi u | closed: every direction of a 5 rad/s push; frame u + 1/2 is the mirror image of frame u (a check) |
| octave | l_2/l_1 from 0.295 to 3.387, m_2/m_1 = 6.25 lam / (1 + lam)^2 - 1 | the two small-swing frequencies stay exactly 2 : 1 all along it |

The octave curve, derived. Linearise about both rods hanging: M q'' + K q = 0 with
M = [[(m_1+m_2) l_1^2, m_2 l_1 l_2], [m_2 l_1 l_2, m_2 l_2^2]], K = diag((m_1+m_2) g l_1, m_2 g l_2). With x = omega^2 l_1 / g,
lam = l_2/l_1, mu = m_2/m_1, det(K - omega^2 M) = 0 becomes

    lam x^2 - (1 + mu)(1 + lam) x + (1 + mu) = 0.

Its roots obey (x_+ + x_-)^2 / (x_+ x_-) = (1 + mu)(1 + lam)^2 / lam. A frequency ratio of 2 means x_+/x_- = 4, for which the
left side is 25/4, so mu = 6.25 lam / (1 + lam)^2 - 1. Checks: equal masses and rods give 8, i.e. x_+/x_- = 3 + 2 sqrt 2 and a
frequency ratio 2.4142 = 1 + sqrt 2, the known value; and the eigenvalues of M^-1 K at all 240 points of the curve give a ratio
within 8.9e-16 of 2 (computed 26 November 2026; algebra only, no equation of motion integrated).

Each film: 240 points of the curve x 720 x 720 starts = 124 416 000 runs of 10 s; maps 240 x 1 036 800 B = 249 MB plus the
video. Expected GPU time per film, scaled from the old pendulum run's measured rate (8.97e7 start-steps a second on two T4,
notebook version 6): 720^2 x 6000 x 240 / 8.97e7 = 8 320 s = 2.3 h; five films 11.6 h. Not yet measured for this model: the
small test run (double_pendulum_film_smoke) measures it before any full run is started.
