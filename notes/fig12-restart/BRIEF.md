# Fig. 12, restarted from zero: a cup of coffee on a one-wheel cart

Brief written 6 November 2026 by the session that built the previous Fig. 12. Numa rejected that work completely: the Blender use,
the skills, the animation, the fluid mechanics, the physics and the translations. This file is the hand-over. Read it whole,
then read `CLAUDE.md`, `AGENTS.md` and `docs/styles.md`.

## 1. What Numa wants

The reference is the photo next to this file, `notes/fig12-restart/reference-mae-academy.jpg`. It is a screenshot of a mae.academy
Instagram reel, "Control Systems · Active Suspension: Can your suspension save this coffee?". The closest match found on the web
is the same account's reel <https://www.instagram.com/reel/Dbi718lzz_g/> ("Saving your coffee with control systems: Active
Suspension", mae.academy, 2 August 2026). The photo is dated 27 December 2025, so the link may be a repost or a sibling. Treat it as
"same account and topic", not as proven to be the identical video. In the photo:

- A cup of coffee stands on a block labelled BODY.
- Under the body are one spring and one damper, then one wheel on a wavy road.
- The cart drives in one direction, and the coffee surface moves.

In Numa's words: "A cup on a cart. Had coffee. The cart has one wheel. It moves straight on a straight flat surface. But if the
surface is bumpy, we'd have a different story. It drives in one direction rather beautifully, and the fluid is rendered so nicely."

**The first thing to do, before any code, is to ask Numa in one short message.** Recommend an answer to each question:

1. What does the picture look like? Either a clean 2D side view like the reel, or 3D.
2. What is in the cup? Coffee in a cup as in the photo (Fig. 12 used to be "A Pint of Stout"), and is the title changing?
3. Is Blender used at all, and if so, for what?

Numa's earlier wishes from this session are below. They are **not** settled: confirm them, don't assume them.

- "be able to see move around and be able to push it along some axis"
- "Solve the NS equations in 3d, mind the z axis symmetry, mind the constraints of motion"

English only. **No German or Arabic version of this page.**

## 2. Delete the old work first, entirely

Remove everything below in the first commit, so that none of it can steer you. The new page may keep the address
`public/simulations/beer-slosh.html`, because links and `public/_redirects` point there, but its content starts from an empty
file.

- `public/simulations/beer-slosh.html`. Rewrite it from scratch; do not copy from it.
- `public/de/simulations/beer-slosh.html` and `public/ar/simulations/beer-slosh.html`. Also take the page out of the German and
  Arabic build in `tools/i18n/build.py`, so it is never generated again. Remove its lines in `public/_redirects` for `/de/` and
  `/ar/`, and make sure the language switcher on the English page offers no German or Arabic.
- `i18n/de/simulations__beer-slosh.html.json`, `i18n/ar/simulations__beer-slosh.html.json`, the slosh entries in
  `i18n/*/walk.json`, and the Fig. 12 entries in `i18n/*/strings.json`.
- `public/scripts/slosh-modes.js` and `public/scripts/walk/slosh.js`, `walk/de/slosh.js`, `walk/ar/slosh.js`.
- `notes/fig12/` (all of it: reviews, referee reports, tests, figures).
- `tools/fig12/`, including the Blender glass `glass.py` and `glass.glb`, the 3D finite-element Steklov solver, the LQR and the
  road envelope.
- `docs/simulations/fig12-beer-slosh.md`, rewritten later for the new page.
- `public/images/sims/beer-slosh.webp`, replaced by a new thumbnail.
- The Fig. 12 text in `public/scripts/catalog.js`, `AGENTS.md` (the long Fig. 12 sentence), `docs/files.md` and `docs/assets.md`.
  Update them to the new page.

Do not reuse anything from it: not the Guinness glass, the foam head, the LQR, the skyhook, the kerb envelope, the two actuators,
or the three-language pipeline.

## 3. Where to work in the repository

| What | Where |
|---|---|
| The page (one self-contained HTML file, the house design) | `public/simulations/beer-slosh.html`; shared code `public/scripts/sim.js` (the `Sim` object), data panel `public/scripts/dataset.js`, `datalog.js`; catalog card `public/scripts/catalog.js` |
| Design rules (fonts, colours, layout) | `docs/styles.md`, `public/styles/*.css`. Titles in Instrument Serif 400, text IBM Plex Sans, labels IBM Plex Mono. Never another font. |
| The lecture note on the page | `notes/STANDARD.md` (LaTeX-like, Latin Modern, KaTeX in `public/vendor/katex`) |
| Offline checks (Python) | a new `tools/fig12/`, kept small |
| Browser test | a new `notes/fig12/test.cjs` (Playwright; Chromium is pre-installed; serve with `python3 -m http.server 8765 --directory public`) |
| Docs for the page | a new `docs/simulations/fig12-beer-slosh.md`, plus the lines in `docs/files.md` |
| Build and deploy | `npm run build`; a merge to `main` deploys to <https://phyeinusul.com> through Cloudflare Workers Builds (`docs/usul.md`). Since 3 November 2026: when finished, checked against `main` and tested in a real browser, merge and verify the live site. Never touch Cloudflare or AppDeploy. |

## 4. The mechanics without control: the Lagrangian

**The picture.** Think of carrying a full mug across a kitchen while walking over a doorstep. Stepping up and down by itself spills
little. What spills it is the moment your hand jerks forward or back. The coffee surface then tilts like a level on a ruler, sinks
on one side, rises on the other, and rocks back and forth at its own rhythm, about three times a second for a mug. On the cart, the
bump does that jerk. When the wheel climbs, the road pushes the wheel along the normal to its surface, which tips backward, so the
cart is braked. Going down, it is shoved forward. The coffee then rocks at its own frequency.

**Coordinates** (metres, seconds; all motion in the vertical plane of travel):

- $x$: the cart's position along the road.
- $z_b$: the height of the body (with the cup, which is rigidly fixed to it and never tilts, because one wheel and a guided body
  give no pitch).
- $z_w$: the height of the wheel axle.
- $a_n$: amplitude of the $n$-th antisymmetric sloshing mode ($m = 1$), the wave height at the cup wall in the plane of travel.

**Parameters:**

| Symbol | Meaning |
|---|---|
| $M_s$ | the sprung mass: body, cup and liquid |
| $m_w$ | wheel mass |
| $I_w$ | wheel moment of inertia |
| $R_w$ | wheel radius |
| $k$, $c$ | suspension spring and damper |
| $k_t$, $c_t$ | radial tyre stiffness and damping |
| $z_r(x)$ | road height |
| $R$ | inner radius of the cup |
| $h$ | depth of the coffee |
| $\rho$ | density of the coffee |
| $m_l = \rho\pi R^2 h$ | liquid mass |
| $L_s$, $L_t$ | unloaded lengths of the spring and the tyre |

**Modes of an upright circular cylinder.** These are the textbook ones: Abramson, NASA SP-106 (1966), ch. 2; Ibrahim, *Liquid
Sloshing Dynamics* (2005), ch. 1–2; Faltinsen & Timokha, *Sloshing* (2009).

- $J_1'(\xi_n) = 0$, so $\xi_1 = 1.8412$, $\xi_2 = 5.3314$, $\xi_3 = 8.5363$.
- $k_n = \xi_n / R$ and $\omega_n^2 = g\,k_n \tanh(k_n h)$.
- Surface shape: $S_n(r,\theta) = J_1(k_n r)/J_1(\xi_n)\,\cos\theta$, and the free surface is $\eta = \sum_n a_n S_n$.
- Modal surface integral: $N_n = \int S_n^2\,dA = \pi R^2 (\xi_n^2 - 1)/(2\xi_n^2)$.
- Modal mass: $\mu_n = \rho N_n / (k_n \tanh k_n h)$.
- Coupling to the cart's horizontal motion: $\lambda_n = \rho\int x\,S_n\,dA = \rho\pi R^3/\xi_n^2$.

The Lagrangian, valid while the tyre touches the road, with $M_x = M_s + m_w + I_w/R_w^2$ (rolling without slip):

$$
\begin{aligned}
L ={}& \tfrac12 M_x\dot x^2 + \tfrac12 M_s\dot z_b^2 + \tfrac12 m_w\dot z_w^2
 + \sum_n\Big(\tfrac12\mu_n\dot a_n^2 + \lambda_n\,\dot x\,\dot a_n + \rho N_n\,\dot z_b\,a_n\dot a_n\Big)\\
&- M_s g z_b - m_w g z_w - \tfrac12 k\,(z_b - z_w - L_s)^2 - \tfrac12 k_t\,\big(z_w - z_r(x) - L_t\big)^2
 - \sum_n \tfrac12\rho g N_n\,a_n^2 .
\end{aligned}
$$

Rayleigh function:

$$D = \tfrac12 c(\dot z_b - \dot z_w)^2 + \tfrac12 c_t(\dot z_w - \dot z_r)^2 + \sum_n \zeta_n\omega_n\mu_n\dot a_n^2 + \tfrac12 c_x\dot x^2 .$$

**Where each term comes from:**

- The term $\lambda_n\dot x\dot a_n$ is the cross term of $\tfrac{\rho}{2}\int|\nabla\Phi|^2dV$ between the container's motion
  $\dot x\,x$ and the wave potential. By Green's identity, with no flow through the walls, it reduces to the surface integral
  $\rho\int x\,S_n\,dA$.
- The term $\rho N_n\dot z_b a_n\dot a_n$ is exact at quadratic order. The waves raise the liquid's centre of mass by
  $\tfrac{\rho}{2m_l}\int\eta^2dA$, and the vertical kinetic energy $m_l\dot z_b\,\dot z_{cm}$ contains it. It gives the parametric
  term below. Leave it out and vertical shaking cannot do anything to the liquid, which is wrong.
- The tyre term depends on $x$ through $z_r(x)$, so $-\partial V/\partial x = -N\,z_r'(x)$, with $N = k_t(z_r - z_w + L_t)$ the
  full tyre load. That is the horizontal kick of the road. Nothing has to be added by hand.

**The equations of motion** (the Euler–Lagrange equations of $L$ with $D$):

$$
\begin{aligned}
M_x\ddot x + \sum_n\lambda_n\ddot a_n + c_x\dot x &= -N\,z_r'(x) + F_{\rm drive},\\
M_s\ddot z_b + c(\dot z_b - \dot z_w) + k(z_b - z_w - L_s) &= -M_s g,\\
m_w\ddot z_w - c(\dot z_b - \dot z_w) - k(z_b - z_w - L_s) &= -m_w g + N,\\
\ddot a_n + 2\zeta_n\omega_n\dot a_n + \omega_n^2\Big(1 + \frac{\ddot z_b}{g}\Big)a_n &= -\frac{\omega_n^2}{g}\,\frac{2R}{\xi_n^2 - 1}\,\ddot x .
\end{aligned}
$$

Here $N = k_t(z_r - z_w + L_t) + c_t(\dot z_r - \dot z_w)$ while $N > 0$. When $N$ would be negative, the wheel has left the road:
set $N = 0$. That is a unilateral constraint, and it sits outside the smooth Lagrangian.

**Two checks of the slosh equation:**

- A constant $\ddot x = A$ gives $a_n = -\tfrac{2R}{\xi_n^2-1}\tfrac{A}{g}$. Since $\sum_n \tfrac{2}{\xi_n^2-1} = 1$, the wall
  height sums to $-RA/g$: the surface is a plane tilted by $A/g$. That is the level on the ruler.
- With $\ddot x = 0$, the vertical motion acts only through $(1 + \ddot z_b/g)$. It changes the stiffness of the waves and does
  not drive them. This is Mathieu/Faraday parametric resonance. It grows only near $2\omega_n$, and only above a threshold of about
  $|\ddot z_b|/g \gtrsim 4\zeta_n$.

**Why a horizontal degree of freedom is needed.** If the cart's speed is prescribed ($x = vt$, $\ddot x = 0$), a cup that only goes
up and down barely sloshes on a bump. Either let $x$ be free (coasting, or with a constant $F_{\rm drive}$ balancing $c_x$), or
state openly that it is prescribed. The bump's horizontal kick $-N z_r'$ is what rocks the coffee.

**Axisymmetric modes ($m = 0$).** These are $J_0'(\xi) = 0$, with $\xi_{01} = 3.8317$. They obey
$\ddot c_n + 2\zeta\omega\dot c_n + \omega^2(1+\ddot z_b/g)\,c_n = 0$, are excited only parametrically, and are optional.

**Numbers for a mug.** With $R = 4$ cm and $h = 6$ cm:

- $\xi_1 h/R = 2.76$ and $\tanh = 0.992$, so $f_{11} = \sqrt{g\,\xi_1\tanh(\xi_1 h/R)/R}/2\pi \approx 3.4$ Hz.
- Bond number $\rho g R^2/\sigma \approx 220$, so surface tension can be neglected.
- Damping $\zeta_n \sim C\sqrt{\nu/(\omega_n R^2)}$, about 0.5–1 % for a water-like liquid. Take $C$ and the depth correction
  from Abramson SP-106 §4 or Ibrahim §2 after **reading them**. Do not quote a number unread.

## 5. The approximations, stated exactly

1. **Potential flow in the liquid:** incompressible, inviscid and irrotational bulk. Viscosity enters only as the boundary-layer
   damping $\zeta_n$. This is not a 3D Navier–Stokes solution. If Numa insists on Navier–Stokes, that is a separate, much larger
   decision; present it to him with its cost.
2. **Linear free surface:** $|\eta| \ll R$, wave slope $\ll 1$, say $|a_1| \lesssim 0.1R$. Nonlinear sloshing (swirl, the Miles
   rotary mode near $\omega_{11}$, breaking, spilling) is outside the model. The page must say when it is exceeded.
3. **The cup is a rigid upright circular cylinder** of radius $R$ and depth $h$. A tapered cup would need numerically computed
   modes; do this only if Numa asks.
4. **The cup translates and never rotates:** one wheel, and the body is guided vertically. This is the photo's model.
5. **Mode truncation:** $m = 1$, $n = 1..3$ (the coupling falls as $1/\xi_n^2$), plus the $m = 0$ modes if the parametric effect
   is shown.
6. **The tyre is a radial point-contact spring and damper:** rolling without slip, slope $|z_r'| \ll 1$ (so $\sin \approx \tan$),
   lift-off as $N \ge 0$. Road wavelengths are long compared with the contact patch.
7. **Quarter car:** rigid body, linear spring and damper, no pitch.
8. **Two-way coupling:** the liquid's reaction on the cart appears through $\lambda_n\ddot a_n$ in the $x$ equation. Its reaction on
   $z_b$ is of second order in $a$ and is neglected.
9. **Rendering:** in the vertical plane of travel the surface is
   $\eta(s) = \sum_n a_n\,J_1(\xi_n|s|/R)/J_1(\xi_n)\,\mathrm{sgn}(s)$ along the diameter, for $-R \le s \le R$. That curve is the
   exact linear-theory surface. Draw it, fill the coffee under it, and nothing more is needed for a reel-like picture.

Control (the reel's "active suspension") comes only after the uncontrolled cart is right and Numa asks for it.

## 6. How to work

- **Before building, find out how the reel is made.** It is very likely Manim, with this analytic surface. Make a 10-second
  side-by-side comparison with the reel first, show it to Numa, and only then build the page.
- **One clear picture first.** The cup, the coffee surface, the body, one spring, one damper, one wheel and the road, driving in one
  direction. No decorative geometry that pulls the eye away from the coffee.
- **Skills when they help, not as ritual.** `phyein-usul-physics-content`, `phyein-usul-data-panel`, `phyein-usul-smooth-site`,
  `theoretical-fluids-and-pdes`. No referee and teacher agent rounds before Numa has approved the animation.
- Short messages. One decision at a time, with a recommendation. Measure numbers, don't guess them. Look at screenshots.

## 7. What went wrong last time (do not repeat)

- It did not follow the photo. It built a Guinness pint on a two-wheel half-car with pitch in 3D, then a side view with a sculpted
  pint glass. The request was a simple cup on a one-wheel cart, driving one way.
- **Blender** was used to sculpt a glass profile and a cart, which were then rendered as crude geometry in the browser. The cart
  distracted from the coffee. When Numa asked why Blender was used at all, the question went unanswered.
- **The fluid.** Heavy machinery (a 3D finite-element Steklov eigenproblem on the sculpted glass, foam-head damping, many damping
  terms) produced an unconvincing moving surface. The effort went into eigenvalues, not into what the reader sees.
- **The physics** was buried under an LQR with 9 states and two actuators, skyhook, a kerb envelope and lift-off counters. The
  simple story, bump → horizontal kick → coffee rocks, was not visible.
- **Hours on German and Arabic translations** of a page that was not right yet.
- Rounds of review agents (referee r1–r3, code review r1–r3, derivation checks) instead of getting the picture right with Numa.
- Long reports and option lists, and new "problems" handed back to Numa.
