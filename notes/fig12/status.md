# Fig. 12 · A Pint of Stout on a Suspension — status (6 November 2026, one-wheel cart)

## Done, with evidence
- Glass from the dimensioned drawing (dimensions.com, vector outline) scaled to 160 × 85 mm, with the two sculpted panels of the 2010 glass (photographs): brim 576.2 mL (quadrature) vs 575.3 mL (Blender mesh, 64 sides, polygon factor 0.9984); 568 mL at 158.2 mm, 1.8 mm below the rim, as a brim-measure pint glass should; the photograph profile of the first version was 6 % too big. `tools/fig12/geom.py`, `glass.py`.
- Three-dimensional FEM (27-node hexahedra, curved to the real wall) gated against the exact cylinder: λ11 within 6e-6, kept modes within 1.2e-4, Q11 within 1.5e-6, wall integral within 5e-6; against the 2D solver on the round glass within 1.6e-4. `python3 tools/fig12/check_modes3d.py` → PASS.
- The panels change the frequencies by 0.003 % at 500 mL and 0.1 % at 300 mL: real in the geometry, irrelevant to the slosh. Stated in the note.
- Plant from a Lagrangian: hand assembly = SymPy Hessians exactly; modal row = boundary-value modal equation with tilt and Stokes–Joukowski terms. `python3 tools/fig12/check_plant.py` → PASS.
- Controller: LQR in suspension coordinates; the page's gains = SciPy's to 6e-12; τ_cl identical; bump peaks identical page vs offline (60.72 / 14.91 / 3.77 mm, with the head's turn inertia). `node notes/fig12/gate-ctl3.cjs`, `python3 tools/fig12/gate_ctl3.py` → PASS.
- Note numbers: 71/71 match. `python3 tools/fig12/check_note_numbers.py` → PASS.
- Browser (headless Chromium, SwiftShader WebGL), 1440 px: 0 errors, 0 KaTeX errors, no sideways scroll, 44/44 checks, both read-backs find ink, the scripted push works (53 N held, 0 after release), bump ordering passive > skyhook > LQR. `notes/fig12/test.cjs`. Regressions: `notes/fig12/regress.cjs` → PASS.
- Walkthrough: 55/55 quoted lines found. `node notes/walkcheck.cjs`.
- Physics cost 0.05 ms per 1 ms step (5 % of real time on this CPU).

## Findings worth telling Numa
- The pitch frequency of the default cart (3.39 Hz) sits 5 % from the slosh (3.23 Hz): the passive cart is a resonator for the pint. That, not the bump itself, is why it spills.
- The LQR's first design (wheel heights as states) pushed the wheel down on the bump and tilted the glass; in suspension coordinates (deflections) it holds the pint. The marginal mode (road slope) made the Riccati equation unsolvable with ψ as a state.
- The LQR tilts the glass more than the skyhook on the bump (1.4° vs 1.3°) and spills less: it levels the stout, not the body.
- The stout's turn coupling Q_r/Q = 103 mm against Z_s = 144 mm: the liquid is swung 71 % as hard as a frozen block.
- Without the parametric (Faraday) term the offline and page runs differed by 10 %; with it, identical.

## Uncertain values (said on the page)
- Panel depth 2 mm (photographs); head liquid fraction 0.15; dome limit 8 mm; foam friction transfer (factor 3); contact-line rate 0.05 1/s; Guinness surface tension (41–48 mN/m); the cart's numbers are a choice.

## Round 3 (6 November 2026): code review and referee, `code-review-r3.md`, `referee-r3.md`
- Fixed in the code: the mode data's sign between fills (the production data is sign-continuous, and the page aligns signs anyway; max|ψ(rim)| = 1 at 490 mL, was 0); the 3D body pitched the wrong way (now read back); restart kept the old road under the wheels (first LQR sample was −35 N, now 6e-4 N); the rough road started with a 5 mm step and ignored its slider; the design ran on every slider event (now once per control sample, warm-started; I_max no longer triggers it); a pinch left a push on; the plain wheel hijacked page scrolling; the straight glass kept the tulip's liquid mass and had no turn coupling; the strut drawing lagged a frame; the axis projection could flip; the tyre rate ignored the push speed; dead lines; store labels.
- Fixed in the physics: the head's inertia in the turn (Q_rn − κQ_n/λ, 2.6 %), in plant.py, the page, the SymPy gate and (12). Peaks now 60.72 / 14.91 / 3.77 mm.
- Fixed in the note: the drawing's scale factors; the volume check's honesty; the Rayleigh units and the modal-row claim; the controller's level-road tilt error (2.1° on the bump), why x_c is not a state, and why deflection coordinates (the kerb); the frame of reference and Galilean invariance; the vorticity picture of the lag and the closed form Q_r = Q(Z_s − 2/k) = 100.9 mm; the symbol clashes (pitch is now β; tyre deflections w; FEM matrices with h, cart's with c; cost 𝒥, Riccati P, weights W); the wrong Fig. 11 reference; the Problems boxes merged; sources: NASA SP-106 eq. (4.8a) read in place of the secondary quote of SP-8009, the ISO 8608 preview and an open reproduction of the class table.
- Left as stated in the note: Hrovat, Karnopp, Miles and Keulegan are abstract-level sources, and say so.

## Published (6 November 2026)
- German and Arabic translated (all 180 page pieces, 98 strings, 42 walkthrough texts per language); glossary: body = Aufbau / الهيكل, actuator = Aktor / المشغّل, strut deflection = Einfederung.
- Merged as https://github.com/Numa1997/SiteTest/pull/95; live on phyeinusul.com about 75 s later. `test.cjs` against the live site in en/de/ar: 47/47 checks, read-backs and the 3D pitch read-back pass.
- The one console error on the live site is Cloudflare's analytics beacon, blocked by the site's own Content-Security-Policy meta; it appears on every page (also pendulum-control.html), not from this figure.

## Open
- The 3D look: the glass is the only Blender asset, without a material; the cart is three.js boxes and cylinders; no environment map, tone mapping, shadows or see-through glass. Waiting for Numa's choice (Blender assets plus a proper three.js setup, three.js only, or as is).
- Arabic glossary: heave = الارتفاع and pitch = الانعطاف الطولي read poorly (the translator suggests الحركة الرأسية and الميل الطولي); a site-wide decision.

## The one-wheel cart (6 November 2026)
Numa's reference (a mae.academy reel, a coffee cup on a one-wheel quarter-car over a bumpy road, made with Manim) and his words: the 3D Blender
cart took the attention away from the target, the stout. Rebuilt as a 2D side view in the house style, the glass drawn 3.2 times larger.
- Physics from first principles: the quarter-car; the axle's path as the envelope of the road under the wheel's circle; the road's push
  along the normal of that path, so its horizontal part, the kick −N z_a′, is what sloshes the stout. A purely vertical cart could not
  slosh a cup from rest (the reel draws its wave; here it is computed). The drive holds the speed with −c_drive ẋ_c.
- Checks: plant gate (SymPy Hessians exact; modal row 3e-16; free roll keeps energy to 6e-6 and reaches sqrt(v² − 2gh); the step's envelope
  is the circle round the edge); controller gate (gains 2e-9, nine peaks within 0.1 %); note 79/79; walkthrough 56/56; browser 53/53 checks,
  four read-backs, kick sign, kerb envelope; regressions; 27 fps on a slowed phone.
- Findings: the bump at walking pace is a resonant kick (crossing 0.33 s, slosh period 0.31 s); passive 19.8 mm, skyhook 13.5, LQR 0.9;
  the kick alone 10.6 mm, the pumping alone 0, together 19.8 (the heave doubles the kicked wave); the strut cannot reach the slosh in the
  linear model, the drive motor can, and the LQR's motor force mirrors the kick; a stiff drive alone (2000 N s/m) gives 2.5 mm.
- Removed: public/vendor/three, public/models/fig12 (no page uses them).
