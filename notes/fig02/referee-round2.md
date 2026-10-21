# Fig. 2, double pendulum: referee report, round 2

Read blind (plan.md and check.md not opened) from the rendered page: `public/` served as is (Vite is not installed in this
checkout, and the build only copies `public/`), opened in headless Chromium 1194 at 1280 × 1000, every fold opened, each of the
nine sections photographed. KaTeX renders everywhere; no console errors. Two readers: **S**, a bachelor student meeting the double
pendulum for the first time; **G**, a reader of Landau, Goldstein and Taylor. Quotes are from the rendered text.

I also ran three checks of my own (physics copied from the page, RK4 with h = 1/600 s, start 120°, 150°, equal masses and lengths),
because three claims in the note rest on numbers it does not show.

| Check | Result |
|---|---|
| Energy drift at t = 60 s for h = 1/600, 1/1200, 1/2400 s | −7.2 × 10⁻⁸, −2.0 × 10⁻⁹, −8.3 × 10⁻¹¹: each halving cuts it by 35× and 25×, not 16× |
| Page path against a reference with step h/8 | apart by 1 mm at 10.9 s, by 0.1 m at 14.3 s, by 1 m at 16.5 s |
| Mean growth rate of a tiny separation over 20 s | 1.87 /s while the lower rod is more than 120° from straight down (5.3 s of the run), 1.01 /s otherwise |

These numbers support the note's "10 to 14 s" and its "grows most strongly near the top", but the note shows neither. The first
check contradicts how the note uses "sixteen times more accurate" (see 7.3).

---

## Abstract

**A1.** "whose future we can write down exactly and still cannot predict" (S, G). Section 7 then says "no formula exists
that gives the angles at a later time". What we can write down exactly is the *law*, not the future. Fix: "whose law of motion we
can write down exactly, and whose future we still cannot predict".

**A2.** "builds the equations of motion step by step from energy alone" (G, and it misleads S). The equations come from
\(L = T - V\) and Hamilton's principle. Energy conservation alone gives one equation for two unknowns. A student who reads this
will think conservation of energy is enough. Fix: "from the two energies, by Lagrange's method".

**A3.** "Every new word is explained where it first appears." The note does not keep this promise. "Radian" is used in
section 1 ("a thousandth of a radian") but defined in section 2; "total energy" appears in section 1, its meaning only in section 3.
Partial derivatives are used in the box of section 3 and in 4.1, but explained only in 4.2. Fix: either define these at first use or
soften the promise.

**A4.** "you can skip them on a first reading and still follow the story" (S). That is not true here. Section 4 is starred as a whole,
but section 5 starts from "equation (6) divided by \(ml\)" and section 7 from "Equations (9)". A student who skipped section 4 has
neither. This is the biggest structural problem; see the verdict.

## 1 · A pendulum on a pendulum

**1.1** "since Galileo … we have known how to predict exactly where it will be" (G). That is true only for small swings.
Galileo's isochronism fails at large amplitude, and the exact large-swing solution (elliptic functions) is nineteenth-century work.
Fix: "predict where it will be, at least for small swings".

**1.2** "passing their swing back and forth like two children on swings joined by a rope" (G). Swings that pass their motion back
and forth are beats, and beats need two nearly equal frequencies with weak coupling. Section 5 finds \(\omega_+/\omega_- = 2.41\), far
from equal, so the motion is a lumpy mixture, not a slow hand-over. The same image comes back in section 5, as "exactly like two coupled
playground swings". Fix: drop "exactly" in section 5. In section 1, say "both arms swing regularly, in a pattern that repeats almost
exactly".

**1.3** "the computer follows them so faithfully that … energy changes by less than one part in ten million" (G). Section 6 rightly
says the opposite: a small drift "shows that the computation is sound, not that its positions are the true ones". The opening uses
energy as a proof of faithfulness, and the later section takes that back. Fix: in section 1, "the computer keeps the energy constant to
better than one part in ten million". Also say one part in ten million *of what* (the drift is divided by \(E_\text{scale}\), not by
\(E\)).

**1.4** "A gymnast circling the high bar, a nunchaku, the hook of a crane" (G, mildly). A nunchaku held by one stick is a single
pendulum with a rigid handle. The crane hook is a double pendulum only when the load hangs from the hook on a second sling. Fix: keep
the gymnast (hips as the second joint), and use "a load hanging from a crane hook" instead.

**1.5** "Nothing random is involved." Determinism is stated three times: here, in "no dice thrown" four lines later, and in
"nothing random enters" in section 6. Fix: once in section 1 is enough. Section 6 can say "not noise" without repeating the reason.

**Physical picture: present and good.** The arm, felt from the inside, is exactly what STANDARD §4.1 asks for.

**Verdict against STANDARD:** needs work (small): fix 1.1, 1.2 and 1.3. Everything else, leave.

## 2 · The model

**2.1** "all its weight sits at a single point" (S). This should say mass, not weight. A point mass is about where the inertia sits
as well as the weight. Fix: "all its mass sits at a single point".

**2.2** Missing model numbers (STANDARD §4.2). The note names the ratios \(m_2/m_1\) and \(l_2/l_1\), but never gives their default
values (both 1) or the default start (120°, 150°, at rest). The start first appears in a figure label in section 6. The natural
time scale \(\sqrt{l/g} = 0.32\ \mathrm{s}\) is never given, and neither is the one number that decides "gentle" or "wild": the
starting energy against the energy scale. For the default start, \(E_0/E_\text{scale} = 0.62\). Fix: one sentence giving the default
values and \(E_0/E_\text{scale}\). Even better, give the energy above which the lower arm can go over the top, so that "start it
high" in section 1 gets a number.

**2.3** "the angular speed \(\omega_i = d\theta_i/dt\)" (G). \(\omega_i\) has a sign, so it is an angular *velocity*. Exercise 5.1
does say "both angular velocities at 0", so the note uses two names for one symbol. Fix: say "angular velocity" throughout.

**Verdict:** needs work (small): 2.2 is the only real gap. The radian explanation and the check of (1) against intuition are
good; leave them.

## 3 · Energy

**3.1** "energy comes in two kinds: the energy of motion and the energy of height" (G). Here, mechanically, yes. As a general
statement it is wrong (heat, chemical, elastic). Fix: "here energy comes in two kinds".

**3.2** "When the two rods point the same way and turn the same way, … the speeds simply add" (S). For the cosine to be 1, the
rods only need to point the same way. "Turn the same way" only decides whether the speeds add or subtract. Fix: delete "and turn the
same way", or say "add (or subtract, if they turn opposite ways)".

**3.3** "carries the whole story of the coupling" is a stock phrase. Fix: "is the coupling".

**3.4, a physics error (G).** In the box: "it only ever pushes at right angles to the marble's path … The rods here are such
a bowl". This is true for the upper rod, but false for the lower one. The lower rod pulls on ball 2 along rod 2, and ball 2's velocity
has a component along rod 2 of size \(l_1\omega_1\sin(\theta_2-\theta_1)\), carried by ball 1. So rod 2 does work on ball 2, and
exactly the opposite work on ball 1. Only the *total* work of each rod vanishes, because the rod's length is fixed. Section 4 repeats
the same claim: "they act along the rods, at right angles to every motion the rods allow, and so do no work". A Goldstein reader
will stop here, because this is d'Alembert's principle (zero *net* virtual work of the constraint forces), not "each force is
perpendicular". Fix, one sentence: "The lower rod does push ball 2 forward or back, but it pulls ball 1 back or forward by exactly the
same amount of work, because its length cannot change; summed over both balls, the rods do no work."

**3.5** "★ In Lagrange's language of section 4: when \(L\) does not contain \(t\) itself" (S, G). This uses \(L\) and \(\partial\)
before either is defined, and it asserts, without proof, that \(h\) is conserved. The step "every term contains exactly two angular
speeds, so … = 2T" is Euler's theorem for homogeneous functions, and it is not named. Fix: move this ★ paragraph to the end of 4.1,
where \(L\) and (5) exist. Add the one line \(dh/dt = -\partial L/\partial t\), which follows from (5), and name Euler's theorem.

**3.6** "Nothing in \(T\) or \(V\) depends on the clock time itself, and there is no friction, so … never changes" (S). This is a
claim first and an explanation later: the salad bowl comes one paragraph after it. That is acceptable, but a student does not see why
"no clock time" implies conservation until the ★ part, which they may skip. The bowl is the real reason at their level. Fix: open the
box with the bowl, and state the conclusion after it.

**Verdict:** needs work. 3.4 is a wrong physical statement, and 3.5 is a forward reference. 3.1 and 3.2 are one-word fixes. The
derivation of (2)–(4) itself is clear; leave it.

## 4 · From energy to motion ★

**4.1** "Form the difference of the two energies, the Lagrangian \(L = T - V\)" (S). A student asks why the difference, after a
whole section on the sum. The note never motivates the minus sign. Fix: one sentence (along the lines of Feynman, *Lectures* II,
ch. 19): nature balances kinetic against potential energy along the path, and the minus sign is what makes the stationary path obey
\(F = ma\). Show this in one line for a single falling ball, \(m\ddot y = -mg\).

**4.2** "later put in its deepest form by Hamilton" is puffery. Fix: "and stated as a principle about whole paths by Hamilton in
1834".

**4.3, a symbol clash (S, G).** In the same subsection the note uses \(\delta\theta_i\), \(\delta\omega_i\) and \(\delta S\) for
the variation, then writes "writing \(\delta = \theta_1 - \theta_2\) for the angle between the rods". From then on, \(\delta\) means an
angle in (6)–(9). Both readers will trip over this. Fix: use \(\varphi\) or \(\Delta\) for the angle between the rods. (The walkthrough
file would need the same change; list it in walk.md.)

**4.4** "(5) says that its rate of change equals \(\partial L/\partial\theta_i\), which plays the part of a force" (G). This is fine
as written. "This is an angular momentum" for \(p_1\) is loose, though: \(p_1\) is not the angular momentum of any body about any
point. The exact and nicer statement is that \(p_1 + p_2\) is the total angular momentum of both balls about the pivot. Fix: say that.

**4.5** "Now subtract the third line from the second … The two terms with \(\omega_1\omega_2\) cancel" (S). The student has to find
for themselves where the surviving \(\omega_2^2\) term comes from (\(-\omega_2(\omega_1-\omega_2)\) gives \(+\omega_2^2\)), and see
that everything except the accelerations was moved to the right. Fix: one clause naming the survivor.

**4.6** "The term with \(\omega_2^2\) is the lower ball … tugging outward on the end of the upper rod" (S, G). The picture is right,
but the reader is not told why it comes with \(\sin\delta\). Only the part of the tug that is across rod 1 can turn it; the part along
rod 1 is taken up by the pivot. Fix: add that half sentence. It is the physical meaning of \(\sin\delta\).

**4.7** "The same three steps for \(\theta_2\) start from …" (S). This is a skipped step. The upper angle gets all three lines, but
the lower angle gets one line, then "again … cancel". A student cannot check (7). Fix: show the other two lines, as in 4.2. That is two
display lines.

**4.8** "Cramer's rule gives it … Three trigonometric identities then tidy the result" (S, G). The jump from (8) to (9) hides the
unsimplified Cramer result. Nobody can apply the three identities to an expression they have not seen. The change of denominator from
\(l_1 l_2(m_1 + m_2\sin^2\delta)\) to \(l_1(2m_1 + m_2 - m_2\cos 2\delta)\) (a factor 2 and \(l_2\) cancelled) is also left to the
reader. Fix: one display line, \(\alpha_1 = [\,\cdots\,]/\det\), before the identities.

**4.9** "Checked against a direct numerical solve of (8) at 10 000 random states" (G). This is a fragment without a subject and reads
like a lab log. Fix: "We checked (9) against …", or move it into a footnote-sized remark.

**4.10** The units test and the \(m_2 \to 0\) limit are good, and exactly what STANDARD §4.4 asks for. Leave them.

**Verdict:** needs work. 4.3 (the clash between \(\delta\) as variation and \(\delta\) as angle) and 4.7/4.8 (skipped steps) block
the student. 3.4/4.0 ("no work") and 4.1 (why \(T - V\)) block the graduate. The Euler–Lagrange derivation itself (4.1) is clear and
well paced; leave it.

## 5 · Small swings: two normal modes

**5.0, a structural problem (S).** "With equal masses \(m\) and equal lengths \(l\), equation (6) divided by \(ml\) …" For the student
who obeyed the ★ and skipped section 4, (6) and (7) do not exist. Fix: either end section 4 with a short unstarred paragraph that
states (6) and (7) in words and repeats them (they are short), or un-star 4.2–4.3 and star only 4.1 and 4.4.

**5.1, a symbol clash (S, G).** "we try … one common frequency \(\omega\)". \(\omega\) already means \(d\theta/dt\), and two lines
earlier "the terms with \(\omega^2\)" meant angular velocity squared. In the determinant, \(\omega^2\) is now the mode frequency. Fix:
call the trial frequency \(\Omega\), keeping \(\omega_\pm\) or renaming them \(\Omega_\pm\).

**5.2** "where two dots mean … the angular acceleration" (S). \(\alpha_i\) was introduced in 4.2 for exactly this, and section 5
switches to \(\ddot\theta_i\) without saying they are the same. Fix: "\(\ddot\theta_i\), the same \(\alpha_i\) as before".

**5.3** "Multiplying top and bottom by \(\sqrt2(\sqrt2\mp1)\) cleans this up" (S). The ± becomes ∓ and the subscript label changes
sides in the same line. The student cannot tell which sign is the slow mode. Fix: write the two cases out:
\(1 + 1/\sqrt2 \Rightarrow \omega_-^2 = (2-\sqrt2)g/l\), and \(1 - 1/\sqrt2 \Rightarrow \omega_+^2 = (2+\sqrt2)g/l\).

**5.4** The periods 2.62 s and 1.09 s are in Figure 2 and the exercise, but the period \(2\pi/\omega\) is never written. "Frequency"
is used for an angular frequency in rad/s, while a student expects hertz. Fix: "angular frequency" at first use, and "period
\(2\pi/\omega_-= 2.62\ \mathrm{s}\)" in the text.

**5.5** "These equations are linear … That changes everything" is a stock phrase. Fix: delete "That changes everything"; the
sentence after it says why linearity matters.

**5.6** "Any small motion at all is a mixture of the two" (G). This is stated, not shown. It is fine at this level, but one clause
would do it: two independent shapes, two angles, so any starting shape and speed can be split into them.

**5.7** "exactly like two coupled playground swings" (G). See 1.2: with a frequency ratio of 2.41 there is no slow hand-over. Fix:
drop the simile, or say "unlike two weakly coupled swings, which hand their motion over slowly, these two modes are far apart in
frequency".

**5.8** Exercise 5.1 is good: it matches the page sliders and the numbers check (\(\sqrt2 \times 5^\circ = 7.07^\circ\); ratio 2.41).
Leave it.

**Verdict:** needs work. 5.0 and 5.1 are serious, 5.3 and 5.4 small. The determinant step and the mode shapes are well explained;
leave them.

## 6 · Chaos

**6.1** "Some starts then show chaotic motion, although high energy alone does not guarantee it" (S, G). This is a claim without
support. The student asks what *does* decide it; the graduate expects "regular islands survive inside the chaotic sea" with a source.
Fix: one sentence and one example start that is high and still regular, or a reference (Strogatz, or a double-pendulum Poincaré-section
paper).

**6.2** "How do we recognise chaos?", "Why do the two pendulums part?", "Why must the bracket itself be zero?" (4.1), "Why exactly this
sum …?" (3). These are rhetorical questions answered in the next breath. CLAUDE.md forbids a question-and-answer format. These are
borderline (Feynman does it), but there are five of them. Fix: turn at least the section-opening ones into statements.

**6.3** "a small swing keeps its size: that is the flat low-energy curve" (S). The low-energy curve in Figure 3 is not flat: it is a
row of arches dipping by about a factor of ten on the log scale. Fix: "the row of arches that never climbs".

**6.4** "Each such moment magnifies the gap, so it grows in bursts, most strongly while the lower rod is near the top." This is
plausible and true (my run: 1.87 /s near the top against 1.01 /s elsewhere), but the note shows nothing for it. Fix: either one
sentence with this number, or mark it in Figure 3 by shading the times when the lower rod is above the horizontal.

**6.5** "follows a tiny change of the whole state, … shrinks it back whenever it has grown large" (S). The reader is not told why
it has to be shrunk back. The reason is that the distance cannot grow beyond the pendulum's size: Figure 3 shows it saturate. Fix: that
half sentence.

**6.6** "\(d\) is now the distance in the full four-number state" (G). Two of the coordinates are radians and two are rad/s, so this
"distance" needs a stated metric (here Euclidean, with seconds set to 1). Fix: say so, and add that \(\lambda\) does not depend on the
choice.

**6.7** "And a small energy drift in the computer proves no more than itself." This is awkward and slightly mannered. Fix: "A small
energy drift shows only that the steps are fine enough to respect the conservation law."

**6.8** "Note also what chaos is not. It is not noise … It is not a failure …". The "It is not X. It is not Y." pattern reads as
generated. Fix: one plain sentence: "Chaos is neither noise nor a failure of energy conservation: the energy stays fixed while the
motion wanders over much of what that energy allows."

**6.9** "Find the smallest starting angles at which you can see the two pendulums separate" (S). This is ambiguous: two angles, and
"smallest" is not defined. Fix: "Keep \(\theta_2 = \theta_1\) and find the smallest \(\theta_1\) …".

**6.10** The numbers check: 1.4 /s, 0.1 m at 4.1 s, \(e^{14.5}\approx 2\times10^6\), half a nanometre, and Figure 3's twin
separation (1.0 m at 5 s in my run). Leave them.

**Verdict:** needs work (moderate): 6.1 and 6.6 for the graduate; 6.3 and 6.5 for the student; 6.7 and 6.8 are voice. The log-scale
explanation, the pencil on its tip, and the order-of-limits sentence are very good; leave them.

## 7 · Solving it step by step

**7.1** "no formula exists that gives the angles at a later time directly" (G). This is a deep claim (non-integrability) stated
flatly. Fix: "and because the motion is chaotic, no such formula can exist" ties it to section 6.

**7.2** "The weights 1, 2, 2, 1 are those of Simpson's rule" (S). Simpson's rule weights are 1, 4, 1, so the student will not see
it. Fix: "Simpson's 1, 4, 1, with the middle weight shared by the two middle looks". "cancel each other to a high degree" is vague;
cut it.

**7.3, unsupported and partly contradicted (G).** "Halving the step therefore makes the result sixteen times more accurate." That
holds for the error in the path. For the Drift readout, which is the only error the reader can see, my run gives 35× and 25× per
halving (−7.2 × 10⁻⁸ → −2.0 × 10⁻⁹ → −8.3 × 10⁻¹¹ at 60 s). Fix: "sixteen times more accurate *in position*", and give the drift
numbers, since STANDARD §4.5 asks for the error measured by running the page.

**7.4** "The page uses \(h = 1/600\) s: ten steps for every picture" (S, G). STANDARD §4.5 asks *why* this step. The note gives no
reason against the motion's own time scale. Fix: "about 100 steps per period of the fast mode (1.09 s), and many more per kick at the
top".

**7.5** "RK4 leaks energy, very slowly but steadily" (G). The note does not say why, and does not name the alternative. RK4 is not
symplectic, so its energy error grows steadily instead of staying bounded. An implicit midpoint (symplectic) method would bound it.
Fix: one sentence. That is also the "why chosen, where it fails" of STANDARD §4.5.

**7.6** "divided by the depth of the potential valley, \(E_\text{scale}\)" (G). \(V\) runs from \(-E_\text{scale}\) to
\(+E_\text{scale}\), so the depth from the bottom to the top is \(2E_\text{scale}\). Fix: "the energy needed to lift both balls from
hanging straight down to the height of the pivot".

**7.7** "Each time the rods pass within a few degrees of a straight line" (S). This is ambiguous: lined up (\(\delta\approx0\)) or
folded back (\(\delta\approx\pi\))? It also misses the link to (8), where the determinant \(l_1l_2(m_1 + m_2\sin^2\delta)\) is
smallest exactly then: at a mass ratio of 10, \(m_1\) is small next to \(m_2\). Fix: "lined up or folded back, where \(\sin\delta\)
and the determinant (8) become small". That gives the reader the reason, not just the symptom.

**7.8** Form. The second half of the section is a bulleted list ("Each picture advances …", "RK4 does not keep …", "The step is not
equally good …", "Moving a … slider restarts …"). STANDARD asks for connected prose, and the first bullet ("the safety limit of 600
steps in the code is never reached") and the last are page-behaviour notes. They will bore the student and give the graduate nothing.
The drift paragraph carries a lot of precision for one point ("+5.0 × 10⁻⁸, at t ≈ 8.7 s; … +4.7 × 10⁻⁸ there"). Fix: turn the
bullets into two paragraphs (drift, and where the step fails). Shrink the frame-cap and slider remarks to one sentence, or move them
to "From metres to pixels".

**Verdict:** needs work: 7.3, 7.4 and 7.5 are the STANDARD §4.5 items; 7.7 is the missed physics; 7.8 is form. The hiker in fog and
the Euler failure are good; leave them.

## 8 · From metres to pixels

**8.1** "\(\sigma = (\min(W,H)/2 - 34)/(l_1+l_2)\)" (S). The 34 is unexplained. Fix: "minus a 34-pixel margin".

**8.2** The trail's half-life and the 1/255 rounding that stops the fade at a quarter are explained well, and honestly. This is
exactly the "where the drawing differs from the model" that CLAUDE.md asks for. Leave it.

**8.3** Missing from the equation-to-screen map (STANDARD §4.6): the pale chaos twin and the two readouts (Drift, Twin separation ·
bob 2). Which symbol is each one? The separation readout is \(d(t)\) of Figure 3, but section 8 does not say so. Fix: one sentence.
The terms also vary: "ball", "mass" (Figure 3 axis) and "bob" (readout label) mean the same thing. Pick one, or say once that they
are the same.

**Verdict:** mostly clear: needs one sentence (8.3) and one word (8.1).

## 9 · What the model leaves out

**9.1** "it is just as chaotic" (G). This is unsupported. Fix: a source. Shinbrot, Grebogi, Wisdom and Yorke, "Chaos in a double
pendulum", *Am. J. Phys.* 60, 491 (1992), measured a real two-bar pendulum and is the natural one.

**9.2** "After some fifteen to twenty Lyapunov times … 10 to 14 s for the default start" (S, G). The number is right (my run: the
page path leaves a reference eight times finer by 1 mm at 10.9 s and by 0.1 m at 14.3 s), but the note does not say where it comes
from. Fix: one sentence. The step error starts at about 10⁻¹⁰ and grows by \(e^{\lambda t}\) until it reaches decimetres, so
\(t \approx \ln(10^{9})/\lambda \approx 14\ \mathrm{s}\). Or quote the measurement.

**9.3** "the next, more complete model" (STANDARD §4.7) is only half there: solid bars are named, friction is named, but no model
for either is given. One phrase each would satisfy the standard: "moment of inertia \(\tfrac13 ml^2\) about the end" for the bars,
and "a torque \(-b\,\omega\) at each joint" for friction.

**9.4** Bullets again; see 7.8.

**9.5 Further reading** (STANDARD §4.8). Taylor ch. 7, 11 and 12 and Landau §5 problem 1 are correctly cited (Taylor §11.4 treats
exactly this double pendulum; pointing to it would help the student). The links go to Google Books and an Elsevier shop page, which
are not readable sources. Strogatz has no chapter. Nothing on the double pendulum's chaos itself is cited. Fix: give Strogatz a chapter
(9 or 10), add Shinbrot et al. 1992 (DOI 10.1119/1.16860), and, for the minus sign in \(L = T - V\), Feynman, *Lectures on Physics*
II, ch. 19, which is free at feynmanlectures.caltech.edu.

**Verdict:** needs work (small): 9.1, 9.2 and 9.5.

---

## The two readers in one paragraph each

**The student** follows sections 1–3 well. The arm, the train and the bowl are good pictures, and the derivation of the
velocities is paced right. They are lost at section 5 if they skipped the ★ section. If they did not skip it, they trip over \(\delta\)
meaning two things in 4.1, over the skipped lines in 4.3 and 4.4, and over \(\omega\) meaning two things in section 5. They are bored
by the frame-cap and drift-decimal bullets in section 7.

**The graduate** finds the structure sound and the checks honest, but stops at the claim that every rod force is perpendicular to its
ball's path (wrong for the lower rod), at "high energy alone does not guarantee it" with no support, at a Lyapunov distance with no
metric, at "sixteen times" with no measurement, and at an integrator section that never says *symplectic*. They also miss the one
elegant fact the note leaves out: \(p_1 + p_2\) is the total angular momentum about the pivot.

## Verdict

**Would this pass as a textbook chapter? No, not yet.** It is close. The voice is mostly right, the pictures are good, and every
number I checked (the frequencies, periods, the ratio 2.41, \(\lambda\), the drift, the separation at 5 s, the 10–14 s horizon) is
correct. About a dozen sentences, and two short display lines, stand between it and a pass.

**The three biggest problems:**

1. **The ★ layering breaks the student's path.** Section 4 is starred as a whole, but sections 5 and 7 are built on its results (6),
   (7) and (9), and the box in section 3 uses \(L\) and partial derivatives from section 4. Fix: an unstarred closing paragraph of
   section 4 that states the two equations of motion in words, and the ★ box of section 3 moved into section 4.
2. **Symbols mean two things.** \(\delta\) is both the variation and the angle between the rods (4.1 onward), and \(\omega\) is both
   the angular velocity and the trial mode frequency (section 5). Also, \(h\) is both the step and the Jacobi integral, and the
   accelerations switch from \(\alpha\) to \(\ddot\theta\) without notice. Rename the angle \(\varphi\) and the trial frequency
   \(\Omega\).
3. **One wrong physical statement and several unsupported ones.** "The rods steer the balls without doing any work" is false for the
   lower rod ball by ball; only the sum vanishes. "High energy alone does not guarantee it", "just as chaotic", "sixteen times more
   accurate" (the readout improves by 25–35×), and "15–20 Lyapunov times" are stated without support, although the last is right. The
   integrator section does not say why RK4 leaks energy (not symplectic) or why \(h = 1/600\) s was chosen.
