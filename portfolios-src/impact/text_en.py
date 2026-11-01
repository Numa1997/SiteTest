T = {}
T['title_tag'] = 'Iron, Cotton and the Head'
T['eyebrow'] = 'Newton · Morse · Hooke · an interactive study'
T['title'] = 'Why an iron ball hurts and a cotton ball does not'
T['lede'] = ('Two balls of the same mass fall from the same height onto a head, drawn as a plate on a spring and a damper. '
 'The iron ball is a lattice of atoms joined by stiff bonds. The cotton ball is a tangle of thin fibres that bend, cling where they cross and rub on each other. '
 'The model runs once when the page opens and every curve and number on this page comes from it; the text below derives what the model does and compares it with real iron, real cotton and a real skull.')
T['replay'] = 'Drop again'
T['drop'] = 'Drop'
T['dropping'] = 'Falling…'
T['startline'] = 'start: 10 m above the head'
T['open1'] = 'Both balls are held 10 m above the head.'
T['open2'] = 'Press “Drop” below to let them fall.'
T['open2wait'] = 'Computing the drop: {p} %. You can press “Drop” already.'
T['computing'] = 'computing'
T['speed1'] = 'Real time'
T['speed4'] = 'Slow ×4'
T['speed20'] = 'Slow ×20'
T['clock'] = 'Simulated time'
T['iron'] = 'Iron'
T['cotton'] = 'Cotton'
T['head'] = 'head: plate, spring, damper'
T['gain'] = 'plate travel drawn 10× larger'
T['scale'] = 'scale'
T['lcd_peak'] = 'PEAK'
T['lcd_now'] = 'NOW'
T['lcd_w'] = 'WEIGHT'
T['plot_title'] = 'What the scale reads'
T['plot_note'] = ('Left: the moment of impact, stretched out. Right: the whole run. The dashed green line is the weight of either ball, Mg = 9.81 N. '
 'The iron curve is a tall, narrow spike; the cotton curve is a low, wide hump. After the shaking stops, both settle on the same line.')
T['plot_zoom'] = 'Around the impact (0.4 s)'
T['plot_all'] = 'Whole run, 0 to 9 s'
T['ax_t'] = 'time (s)'
T['ax_f'] = 'force (N)'
T['weightline'] = 'weight Mg'
T['energy_title'] = 'Where the energy goes'
T['energy_note'] = ('The upper bar of each pair is the energy the fall has handed over so far: the height energy the ball has lost. '
 'The lower bar shows where that energy is now. If energy is conserved, the two bars are equally long; the line under them gives the difference in joules, which is the integrator’s own error.')
T['en_in'] = 'given by the fall'
T['en_out'] = 'where it is now'
T['en_books'] = 'books'
T['en_diff'] = 'difference'
T['en_ke'] = 'motion'
T['en_el'] = 'stored in the ball'
T['en_head'] = 'stored in the head spring'
T['en_heatball'] = 'heat in the ball'
T['en_heathead'] = 'heat in the head'
T['r_contact'] = 'first touch at'
T['r_pred'] = 'Newton predicts √(2h/g) ='
T['r_peak'] = 'impact force (peak)'
T['r_kg'] = 'what a kitchen scale would show for that instant (F/g)'
T['r_weight'] = 'weight after it settles'
T['r_mass'] = 'mass'
T['headnote'] = 'Each scale is the head itself: plate, spring and damper. Plate travel drawn 10× larger.'
T['r_settling'] = 'still shaking…'
T['r_heatball'] = 'heat made inside the ball'
T['r_heathead'] = 'heat made in the head'
T['r_heatair'] = 'energy given to the air'
T['r_pred_air'] = 'predicted with air ='
T['en_heatair'] = 'given to the air'
T['air_label'] = 'Air:'
T['air_levels'] = ['off (vacuum)', 'Mars, 0.020 kg/m³', '10 km up, 0.41 kg/m³', 'sea level, 1.2 kg/m³']
T['air_title'] = 'Add air drag on each ball, as a real 1 kg ball of its material would feel it; the run is computed again'
T['air_hint'] = 'Air is on ({rho} kg/m³): each ball feels the drag ½ρC<sub>d</sub>Av² of a real 1 kg ball of its material (iron 6.2 cm across, cotton 40 cm), pressing on its front, so the cotton arrives later and slower; the iron hardly notices.'

T['sections'] = r'''
<div class="card">
<h2><span class="num">1</span>The answer in one sentence</h2>
<p>A falling ball hurts because of how <em>short</em> a distance it takes to stop it. Both balls bring about the same energy (in the model, exactly the same). The iron ball does not give way, so the head has to stop it within the few millimetres a skull can yield, and a short stop needs a large force. The cotton ball gives way itself: it is stopped over a large part of its own size, and most of its energy turns into heat inside the cotton, not in the head.</p>
<div class="box pic"><div class="tag">Picture</div><p>Catch a raw egg with stiff hands and it breaks; let your hands travel back with it over 30 cm and it survives. The egg brings the same energy both times. Only the stopping distance changed.</p></div>
</div>

<div class="card">
<h2><span class="num">2</span>The fall: Newton's second law</h2>
<div class="box pic"><div class="tag">Picture</div><p>Drop a key and a ball of wool from a chair at the same moment: they land together. Gravity pulls every gram equally, and every gram has the same inertia to overcome, so in a vacuum everything falls alike.</p></div>
<p>Each ball is a set of particles with masses <span class="m">m<sub>i</sub></span>. Newton's second law holds for every one of them: mass times acceleration equals the sum of the forces on it. While the ball falls, nothing touches it and its bonds are relaxed, so only the weight acts:</p>
<div class="eq">m<sub>i</sub> ÿ<sub>i</sub> = − m<sub>i</sub> g &nbsp;&nbsp;⇒&nbsp;&nbsp; ÿ = − g</div>
<p>The mass cancels. Start at rest at height <span class="m">h</span> (measured from the plate to the lowest point of the ball) and integrate once, then once more:</p>
<div class="eq">v(t) = − g t, &nbsp;&nbsp; y(t) = h − ½ g t²</div>
<p>The ball reaches the plate when <span class="m">y = 0</span>:</p>
<div class="eq key">t* = √(2h/g), &nbsp;&nbsp; v* = g t* = √(2gh)</div>
<div class="box chk"><div class="tag">Check</div><p>Units: √(m / (m/s²)) = s. Energy gives the same speed without mentioning time: the height energy <span class="m">Mgh</span> becomes motion energy <span class="m">½Mv*²</span>, so <span class="m">v* = √(2gh)</span>.</p></div>
<div class="box toy"><div class="tag">In our model</div><p>With <span class="m">h = 10 m</span>: <span class="m">t* = 1.428 s</span> and <span class="m">v* = 14.0 m/s</span>. The model integrates the particles step by step and records the first touch; the readout above lets you compare it with the formula. With Air off, the model leaves out air, so both balls arrive with the same speed and the comparison isolates the material. With air, each ball feels the drag below on its front: in the thin air 10 km up the cotton arrives 0.03 s later, at 13.2 m/s; in air at sea level 0.09 s later, at 11.9 m/s, about 1 m behind the iron, which still arrives at 13.9 m/s. On Mars, with air 60 times thinner, neither ball notices.</p></div>
<h3>With air, for real balls</h3>
<p>A real ball also feels air drag, <span class="m">½ ρ<sub>air</sub> C<sub>d</sub> A v²</span>, where <span class="m">A</span> is its cross-section and <span class="m">C<sub>d</sub> ≈ 0.47</span> for a sphere. Take <span class="m">y</span> as the distance fallen, write the acceleration as <span class="m">dv/dt = v dv/dy = ½ d(v²)/dy</span>, and define the terminal speed <span class="m">v<sub>t</sub> = √(2mg / (ρ<sub>air</sub> C<sub>d</sub> A))</span>, at which drag equals weight:</p>
<div class="eq">½ d(v²)/dy = g (1 − v²/v<sub>t</sub>²) &nbsp;&nbsp;⇒&nbsp;&nbsp; v² = v<sub>t</sub>² (1 − e<sup>−2gy/v<sub>t</sub>²</sup>)</div>
<div class="box chk"><div class="tag">Check</div><p>For a short fall, <span class="m">e<sup>−x</sup> ≈ 1 − x</span> gives back <span class="m">v² = 2gy</span>, the vacuum result.</p></div>
<p>For a 0.5 kg ball dropped 10 m: solid iron (4.96 cm across) has <span class="m">v<sub>t</sub> = 95 m/s</span> and arrives at 13.9 m/s, almost the vacuum value of 14.0 m/s. A ball of loose cotton wool of the same mass (density about 30 kg/m³, so 31.7 cm across) has <span class="m">v<sub>t</sub> = 14.8 m/s</span> and arrives at 11.4 m/s. Air slows the cotton a little; it is not the main reason it is harmless.</p>
</div>

<div class="card">
<h2><span class="num">3</span>The bonds: what holds a solid together</h2>
<div class="box pic"><div class="tag">Picture</div><p>Think of a marble in a valley. One side of the valley is a steep wall, the other a long gentle slope that flattens into a plain. Nudge the marble and it rocks back and forth at the bottom. Push it towards the wall and it is thrown back hard. Push it up the gentle side hard enough and it rolls over the rim and away: the bond is broken. The marble is one atom, the bottom of the valley is its resting distance from its neighbour, and the shape of the valley is the bond.</p></div>
<p>Two atoms at distance <span class="m">r</span> have an energy <span class="m">U(r)</span>. The force on each, along the line joining them, is <span class="m">F = −dU/dr</span>. At the bottom of the valley, <span class="m">r = r<sub>0</sub></span>, the force is zero and the atoms rest. Expand around that point. The first derivative vanishes at a minimum, so</p>
<div class="eq">U(r) ≈ U(r<sub>0</sub>) + ½ U″(r<sub>0</sub>) (r − r<sub>0</sub>)² &nbsp;&nbsp;⇒&nbsp;&nbsp; F ≈ − k (r − r<sub>0</sub>), &nbsp; k = U″(r<sub>0</sub>)</div>
<p>Near rest, every bond is a Hooke spring. This is why springs appear everywhere in mechanics: any smooth valley looks like a parabola at its bottom.</p>
<h3>The Morse bond</h3>
<p>Philip Morse proposed in 1929 a valley with exactly the shape of the picture:</p>
<div class="eq key">U(r) = D [1 − e<sup>−α(r − r<sub>0</sub>)</sup>]²</div>
<p><span class="m">D</span> is the depth of the valley, the energy needed to pull the two atoms apart for good, and <span class="m">1/α</span> is its width. Expanding <span class="m">1 − e<sup>−αx</sup> ≈ αx</span> gives the spring constant <span class="m">k = 2Dα²</span>. The pull of the bond, <span class="m">dU/dr = 2Dα e<sup>−αx</sup>(1 − e<sup>−αx</sup>)</span>, is largest where <span class="m">e<sup>−αx</sup> = ½</span>, at a stretch <span class="m">x = ln 2 / α</span>, and there it equals <span class="m">Dα/2</span>. Stretch further and the bond pulls back <em>less</em>: it is letting go.</p>
<p>Girifalco and Weizer fitted Morse valleys to cubic metals in 1959, using each metal's cohesive energy, lattice spacing and compressibility. For iron they give <span class="m">D = 0.4174 eV</span>, <span class="m">α = 1.3885 Å⁻¹</span>, <span class="m">r<sub>0</sub> = 2.845 Å</span> (an electronvolt is 1.602×10⁻¹⁹ J, an ångström is 10⁻¹⁰ m). Then</p>
<div class="eq">k = 2Dα² = 1.61 eV/Å² = 25.8 N/m</div>
<p>One bond is a soft spring: a weight of 2.6 g would stretch it by a millimetre. A solid is strong because it has an enormous number of them. Stack such springs in a simple cubic pattern: every square metre of cross-section holds <span class="m">1/r<sub>0</sub>²</span> parallel bonds, and each layer is <span class="m">r<sub>0</sub></span> thick, so the stress per unit strain is</p>
<div class="eq">E ≈ k / r<sub>0</sub> = 25.8 N/m ÷ 2.845×10⁻¹⁰ m ≈ 9×10¹⁰ Pa = 90 GPa</div>
<p>Measured iron has a Young's modulus of about 210 GPa. A crude stack of pair springs gets the order of magnitude right; the real lattice geometry and the many-body nature of metallic bonding make up the rest.</p>
<div class="box note"><div class="tag">Honest note: metals are not really pair-bonded</div><p>In a metal the outer electrons are shared by all atoms, so how strongly an atom binds a neighbour depends on how many other neighbours it already has. A pair potential cannot express that, and it shows: in an unstressed cubic crystal held together by central pair forces, two of the elastic constants must be equal (the Cauchy relation <span class="m">C<sub>12</sub> = C<sub>44</sub></span>), and real metals break that rule. The embedded-atom method of Daw and Baskes (1984) fixes it. Each atom sits in the electron density <span class="m">ρ̄<sub>i</sub> = Σ<sub>j</sub> f(r<sub>ij</sub>)</span> made by its neighbours and pays an embedding energy <span class="m">F(ρ̄<sub>i</sub>)</span> for it: <span class="m">E = Σ<sub>i</sub> F(ρ̄<sub>i</sub>) + ½ Σ<sub>i≠j</sub> φ(r<sub>ij</sub>)</span>. For the small elastic squeeze of our question, every one of these models reduces to springs near rest, so the Morse bond is enough here.</p></div>
<div class="box toy"><div class="tag">In our model: iron</div><p>91 atoms on a triangular lattice, each bonded to its nearest neighbours by a Morse valley with <span class="m">αr<sub>0</sub> = 3.95</span>, the same shape as iron's (1.3885 × 2.845). The stiffness is set so that the ball is much stiffer than the head, as a real iron ball is: its stiffness is of order <span class="m">E·r ≈ 210 GPa × 2.5 cm ≈ 5×10⁹ N/m</span>, about a thousand times a skull's.</p></div>

<h3>Cotton: stiff fibres, soft tangle</h3>
<div class="box pic"><div class="tag">Picture</div><p>Push a dry spaghetti strand along its length and it resists. Push its middle sideways and it bends at once. Cotton is a loose tangle of such strands, and any push on the tangle ends up bending strands.</p></div>
<p>A cotton fibre is cellulose: glucose rings joined by strong covalent bonds into long chains, the chains packed side by side and held together by hydrogen bonds into fibrils, and the fibrils wound into a twisted, partly hollow fibre roughly 15 µm wide. As a material it is stiff, with a Young's modulus of several gigapascals. The softness of a cotton ball does not come from weak molecules. It comes from geometry.</p>
<p>Treat a fibre segment of length <span class="m">L</span> and diameter <span class="m">d</span> as a beam. Stretching it, its stiffness is <span class="m">k<sub>stretch</sub> = EA/L</span> with <span class="m">A = πd²/4</span>. Bending it like a diving board clamped at one end, the tip stiffness is <span class="m">k<sub>bend</sub> = 3EI/L³</span> with <span class="m">I = πd⁴/64</span>, the second moment of area, which measures how much material sits far from the bending line. Their ratio is</p>
<div class="eq key">k<sub>bend</sub> / k<sub>stretch</sub> = (3/16) (d/L)²</div>
<p>For <span class="m">d = 15 µm</span> and <span class="m">L = 1 mm</span> between contacts this is <span class="m">4×10⁻⁵</span>: bending is about 24 000 times softer than stretching. Thin things bend.</p>
<h3>Why a tangle stiffens as you squeeze it</h3>
<p>Let <span class="m">φ</span> be the volume fraction, the share of the ball's volume taken by fibre. For loose cotton wool <span class="m">φ ≈ 30/1520 ≈ 0.02</span>: the ball is 98 % air. The scaling argument below drops all numerical factors.</p>
<p>First, how far apart are the contacts along a fibre? A piece of fibre of length <span class="m">b</span> brushes past a slab of area about <span class="m">b·d</span>. Other fibres fill a fraction <span class="m">φ</span> of space, so roughly <span class="m">φ b d / d² = φ b/d</span> of them cross that slab. One contact per piece means <span class="m">b ≈ d/φ</span>: the denser the tangle, the closer the contacts. Compress the ball by a small strain <span class="m">ε</span>. Each free segment of length <span class="m">b</span> bends by <span class="m">δ ≈ εb</span> and pushes back with</p>
<div class="eq">f ≈ (E d⁴ / b³) · ε b = E d⁴ ε / b²</div>
<p>The fibre length per unit volume is <span class="m">4φ/(πd²)</span>, so a layer one segment thick contains about <span class="m">φ/d²</span> load-carrying segments per unit area. The stress is force per segment times segments per area:</p>
<div class="eq">σ ≈ (E d⁴ ε / b²) · (φ / d²) = E φ d² ε / b² = E φ³ ε</div>
<p>So the tangle's stiffness is about <span class="m">E φ³</span>. Because <span class="m">φ</span> rises as you squeeze, so does the stiffness. Integrating with <span class="m">dε = dφ/φ</span> gives van Wyk's law for fibre masses, first measured on wool in 1946:</p>
<div class="eq key">σ = K E (φ³ − φ<sub>0</sub>³)</div>
<div class="box chk"><div class="tag">Check</div><p>With <span class="m">φ = 0.02</span>, <span class="m">φ³ = 8×10⁻⁶</span>: the tangle is at least a hundred thousand times softer than the fibre it is made of. And the law says a squashed ball is harder to squash further, which your fingers confirm on any cotton ball.</p></div>
<div class="box toy"><div class="tag">In our model: cotton</div><p>18 fibres of 34 beads each, curled at random inside a circle. Four ingredients act on them. Stretch springs along each fibre. Bending springs on the angle between successive segments, whose rest angles are the fibre's natural curl. Junctions where fibres cross, made of shallow Morse valleys that can break, standing in for friction and entanglement. Finally, when beads of different fibres touch they push apart and rub, with friction. New contacts forming under the squeeze give the van Wyk stiffening, and the rubbing turns motion into heat.</p></div>
</div>

<div class="card">
<h2><span class="num">4</span>The hit: why stiff hurts</h2>
<p>When something stops the ball over a distance <span class="m">d</span>, the stopping force does work against its motion. The work–energy theorem says this work equals the motion energy removed:</p>
<div class="eq key">F̄ · d = ½ m v²</div>
<p>where <span class="m">F̄</span> is the force averaged over the distance. Same energy, ten times shorter stop, ten times larger force.</p>
<h3>Iron: the head does all the yielding</h3>
<p>Assume the ball is rigid (section 3 showed that a real iron ball is about a thousand times stiffer than a skull), the head is a linear spring of stiffness <span class="m">k<sub>h</sub></span>, and nothing is lost on the way in. A linear spring is a simplification: measured skulls stiffen as they are pressed further. The motion energy goes into the spring: <span class="m">½mv² = ½k<sub>h</sub>x<sub>max</sub>²</span>. Hence</p>
<div class="eq key">x<sub>max</sub> = v √(m/k<sub>h</sub>), &nbsp;&nbsp; F<sub>max</sub> = k<sub>h</sub> x<sub>max</sub> = v √(m k<sub>h</sub>), &nbsp;&nbsp; τ = π √(m/k<sub>h</sub>)</div>
<p>The contact lasts <span class="m">τ</span>, half an oscillation of the mass on the spring.</p>
<div class="box chk"><div class="tag">Check</div><p>Units: <span class="m">(m/s)·√(kg·N/m) = (m/s)·(kg/s) = N</span>. Limit: a softer head (<span class="m">k<sub>h</sub> → 0</span>) gives a gentler, longer push, as a pillow does.</p></div>
<p>A real head is not bolted down. During a millisecond the neck hardly acts, so the ball compresses the spring between itself and a free head of mass <span class="m">M<sub>h</sub></span>, and <span class="m">m</span> above is replaced by the reduced mass <span class="m">μ = mM<sub>h</sub>/(m + M<sub>h</sub>)</span>. In words: the head recoils a little, so the spring between them is squeezed a little less.</p>
<div class="box toy"><div class="tag">Real numbers</div><p>For the 0.5 kg iron ball at 13.9 m/s, and a mean dynamic skull stiffness of about 4.0 MN/m (measured by Yoganandan and co-workers on cadaver heads): <span class="m">F<sub>max</sub> = 19.8 kN</span> over <span class="m">τ = 1.1 ms</span>, with the skull yielding <span class="m">x<sub>max</sub> = 4.9 mm</span>. With a free head of about 4.5 kg (an assumed typical value), <span class="m">μ = 0.45 kg</span> and the peak drops to about 18.7 kN. The same study measured a mean dynamic failure load of 11.9 kN. The head's acceleration, <span class="m">F/M<sub>h</sub></span>, is about 4200 m/s², over 400 times gravity.</p></div>
<h3>Cotton: the ball does the yielding</h3>
<p>The cotton ball is far softer than the head, so the head barely moves and the ball crushes instead, over a good part of its 32 cm. Take a stopping distance of about 20 cm (my estimate, not a measurement): <span class="m">F̄ ≈ 32.5 J / 0.2 m ≈ 160 N</span>, an acceleration of the head of under 4 times gravity. That average is about 120 times below the iron's peak. The cotton's own peak lies above its average, because the tangle stiffens as it is squashed. By how much I could not pin down: a one-dimensional estimate of my own kept falling as I refined it, from 4.7 kN to 0.83 kN, and had not settled.</p>
<h3>The decisive test: a solid cellulose ball</h3>
<p>A solid ball of cellulose, the very molecule cotton is made of, is about a thousand times stiffer than a skull, just as iron is. In my one-dimensional model it hit with 19.5 kN, against 19.8 kN for iron. So the chemistry of the bonds does not decide the outcome. Their arrangement does.</p>
<div class="box note"><div class="tag">A second picture: how fast the news travels</div><p>When the front of a ball stops, the back learns of it through a compression wave. In iron that wave runs at <span class="m">√(E/ρ) ≈ 5.2 km/s</span> and crosses the 5 cm ball in about 10 µs, a hundred times faster than the contact lasts, so the whole ball stops as one body, like a hailstone. In loose cotton the wave runs at metres to tens of metres per second (I could not pin the number down), similar to the impact speed. The back of the ball keeps arriving after the front has stopped, so the cotton hits like a short shower of light pieces rather than like one stone.</p></div>
<div class="box toy"><div class="tag">In our model</div><p>Here <span class="m">v = 14.0 m/s</span>, <span class="m">m = 1 kg</span> and <span class="m">k<sub>h</sub> = 6000 N/m</span>, so the rigid-ball formula gives 1085 N. The model reads about 639 N, lower, because the head's damper and the soft contact between atoms and plate both cushion the peak. The cotton peaks near 188 N. The ratio in the model is about 3.4, far below the real one, because I had to keep the toy cotton much stiffer than real cotton for it to stay a visible ball.</p></div>
</div>

<div class="card">
<h2><span class="num">5</span>The scale: how force sensors work</h2>
<div class="box pic"><div class="tag">Picture</div><p>Stand at the end of a diving board and it bends; the heavier you are, the more it bends. Every scale is a diving board with a ruler. It measures how much something bends and turns that into a force.</p></div>
<p>The scale in the animation is the head itself: a plate on a spring. It reads Hooke's law backwards, <span class="m">F = k<sub>h</sub> × compression</span>. The black needle shows the force at this instant. The thin red pointer is a peak hold: the needle pushes it up and it stays at the largest force so far, which is the impact force. When the shaking has died away, the needle comes to rest where the spring holds the ball still, <span class="m">k<sub>h</sub>x = Mg</span>, and the display switches to the weight. The cotton keeps swaying gently for a few seconds, so the scale does what a digital scale does with a noisy signal: it averages its reading, here from 4 s onward, and shows the result from 6.5 s. Both balls then read 9.81 N, which is 1.000 kg, because both are exactly 1 kg. Same weight, very different blows.</p>
<p>A kitchen scale shows kilograms by dividing the force by <span class="m">g</span>. So for the instant of impact the iron ball would read about 65 kg, the cotton ball about 19 kg, and both settle at 1 kg.</p>
<h3>Inside a real kitchen or bathroom scale</h3>
<p>Under the platform sits a load cell: a small aluminium block shaped so that it bends very slightly under load. Glued to it is a strain gauge, a thin metal foil laid out in a zigzag. When the block bends, the foil is stretched, becoming longer and thinner, and its electrical resistance <span class="m">R = ρ<sub>e</sub>L/A</span> rises (here <span class="m">ρ<sub>e</sub></span> is the metal's resistivity). For common foil alloys the relative change is about twice the strain, <span class="m">ΔR/R ≈ 2ε</span>: a few tenths of a percent at most. To see such a small change, four resistors are wired in a diamond, a Wheatstone bridge, balanced so that it gives zero voltage with no load; any stretch unbalances it and a voltage appears. An amplifier measures it and the display divides by <span class="m">g</span>.</p>
<h3>Why a bathroom scale cannot read a blow</h3>
<p>A scale is itself a mass on a spring. It can follow only forces that change slower than its own natural frequency <span class="m">f<sub>0</sub> = (1/2π)√(k/m)</span>, the rate at which it rings when tapped; and its electronics average over a fraction of a second to show a steady number. A blow lasting a millisecond is over before the scale can respond.</p>
<p>For impacts, engineers use piezoelectric force sensors. Squeeze a quartz crystal and its positive and negative ions shift slightly relative to each other inside the lattice, so its faces become electrically charged, about 2.3 pC per newton for quartz (a picocoulomb is 10⁻¹² C). The crystal is so stiff that it barely moves, so its natural frequency is tens of kilohertz and it can follow a millisecond blow. The charge comes from atoms displaced in their bond valleys, the same valleys as in section 3.</p>
</div>

<div class="card">
<h2><span class="num">6</span>Where the energy goes</h2>
<p>Energy is conserved, so the books must balance at every instant:</p>
<div class="eq key">height energy released = motion + stored in the ball + stored in the head spring + heat</div>
<p>Heat is produced wherever something rubs or flows: in the dampers that stand for internal friction in the bonds, in fibres rubbing on fibres, in the head's damper (soft tissue) and in the contact between ball and plate. The model adds up each of these from its own law, so the two bars in the energy chart are computed independently and can disagree. They differ by a fraction of a joule, the numerical error of the time-stepping.</p>
<div class="box toy"><div class="tag">In our model</div><p>The iron ball turns about 98 J into heat, almost all of it in the head. The cotton ball turns about 104 J into heat, almost all of it inside the cotton. It releases more than the 98.1 J of the drop because it ends up squashed lower than it started, so its centre of mass (the average position of its mass) falls further; it also starts with about 1.2 J stored in fibres that were pressed together when the tangle was made. That is the cotton's protection, in energy terms: it burns the blow inside itself.</p></div>
</div>

<div class="card">
<h2><span class="num">7</span>What the model leaves out</h2>
<p>It is two-dimensional, a slice through a three-dimensional ball. Air is left out unless the Air menu is set; then each ball feels the drag of a real 1 kg ball of its material on its front, as thin as on Mars, as 10 km up, or as at sea level. Even at sea level it squashes the cotton by only about 5 cm and breaks none of its fibres: in a drop from rest the drag never exceeds the weight, so the air presses on the cotton no harder than a table it lies on. Tearing it would take air that pushes harder than the weight, such as a ball thrown down faster than its terminal speed. The cotton lands within 0.001 s of the closed form for a rigid ball at every level: real air hardly changes its shape. The head is a flat plate on a spring and a damper, not a curved skull around a brain. The toy iron is stiffer than the head by a much smaller factor than real iron, and the toy cotton is much stiffer than real cotton, so the model shows the mechanism with a peak ratio of about 3.4, where the real ratio of iron's peak to cotton's average force is about 120. The fibres' contacts in the slice stand in for contacts in three dimensions. The real-world numbers in sections 2 and 4 come from separate hand calculations, whose inputs are listed in the table.</p>
</div>
'''

T['h_par'] = 'Every parameter'
T['par_intro'] = ('The model uses SI units, but its balls are drawn and tuned for clarity, not to match real iron and real cotton. '
 'Every force law is listed here, then the inputs of the real-world estimates.')
T['th'] = ['Symbol', 'Value', 'Meaning']
T['rows'] = [
 ['Model: shared'],
 ['g, h', '9.81 m/s², 10 m', 'gravity; drop height from the plate to the lowest point of the ball'],
 ['M', '1 kg', 'mass of each ball, shared equally among its particles'],
 ['Δt, t<sub>end</sub>', '2×10⁻⁴ s, 9 s', 'time step (iron takes 5 sub-steps and cotton 2, for stability); length of the run; positions are stored every 1 ms up to 2.5 s and every 2 ms after that, for playback'],
 ['Integrator', 'semi-implicit Euler', 'new velocity from the forces, then new position from the new velocity'],
 ['Model: iron'],
 ['N, a', '91, 0.10 m', 'atoms on a triangular lattice; spacing'],
 ['k, αr<sub>0</sub>', '10⁵ N/m, 3.95', 'Morse bond stiffness at rest (k = 2Dα²) and shape (iron’s, from Girifalco and Weizer)'],
 ['c', '2 N·s/m', 'bond damper, standing for internal friction'],
 ['Model: cotton'],
 ['fibres × beads, s', '18 × 34, 0.08 m', 'fibres, beads per fibre, bead spacing (612 beads)'],
 ['k<sub>ax</sub>, c', '300 N/m, 0.3 N·s/m', 'stretch spring along a fibre, and its damper'],
 ['κ, c<sub>b</sub>', '0.25 N·m/rad, 0.004 N·m·s/rad', 'bending spring on the angle between segments (rest angle = natural curl), and bending friction'],
 ['k<sub>j</sub>, F<sub>j</sub>', '40 N/m, 4 N', 'junction where fibres cross: Morse valley with this stiffness and largest pull; breaks at three times the stretch of largest pull'],
 ['d<sub>c</sub>, k<sub>c</sub>, c<sub>c</sub>', '0.06 m, 20 N/m, 0.4 N·s/m', 'fibre–fibre contact: range, push-back stiffness, rubbing friction'],
 ['Model: head and scale'],
 ['m<sub>p</sub>, k<sub>h</sub>, c<sub>h</sub>', '0.2 kg, 6000 N/m, 62 N·s/m', 'plate mass, head spring, head damper'],
 ['ω<sub>c</sub>, ζ<sub>c</sub>', '1350 rad/s, 0.5', 'skin contact between a particle and the plate: each particle rebounds at this angular frequency, with this damping ratio (ζ = 1 is the border between bouncing back and creeping back)'],
 ['Reading', 'F = k<sub>h</sub> × compression', 'what the scale shows; the weight is the average of the reading from 4 s onward, shown from 6.5 s; mass = weight / g'],
 ['Real-world estimates'],
 ['m, h', '0.5 kg, 10 m', 'ball mass, drop height'],
 ['ρ', '7870, 1520, 30 kg/m³', 'iron, cellulose, loose cotton wool (the cotton value is my assumption)'],
 ['ρ<sub>air</sub>, C<sub>d</sub>', '1.2 kg/m³, 0.47', 'air density, drag coefficient of a sphere'],
 ['ρ<sub>air</sub> (menu)', '0, 0.020, 0.41, 1.2 kg/m³', 'the Air menu: vacuum; the ground on Mars; 10 km up; sea level'],
 ['ρ<sub>Fe</sub>, ρ<sub>c</sub>', '7874, 30 kg/m³', 'densities of real iron and of loose cotton wool: with Air on they give the cross-sections A of real 1 kg balls, 30.6 cm² and 1252 cm²'],
 ['k<sub>h</sub>', '4.0 MN/m', 'mean dynamic skull stiffness, Yoganandan et al.'],
 ['M<sub>h</sub>', '4.5 kg', 'mass of a head, assumed typical value'],
 ['E', '210 GPa, ~10 GPa', 'Young’s modulus of iron; of cellulose (rounded, assumed)'],
 ['D, α, r<sub>0</sub>', '0.4174 eV, 1.3885 Å⁻¹, 2.845 Å', 'Morse parameters of iron, Girifalco and Weizer (1959)'],
]
T['h_src'] = 'Sources'
T['sources'] = [
 'L. A. Girifalco, V. G. Weizer, “Application of the Morse potential function to cubic metals”, Phys. Rev. 114, 687 (1959). <a href="https://doi.org/10.1103/PhysRev.114.687">doi:10.1103/PhysRev.114.687</a>; model listing: <a href="https://www.ctcms.nist.gov/potentials/entry/1959--Girifalco-L-A-Weizer-V-G--Fe">NIST Interatomic Potentials Repository</a>. The iron values are quoted from my knowledge of the paper’s table; I could not open the table online.',
 'M. S. Daw, M. I. Baskes, “Embedded-atom method”, Phys. Rev. B 29, 6443 (1984). <a href="https://link.aps.org/doi/10.1103/PhysRevB.29.6443">link</a>',
 'N. Yoganandan et al., biomechanics of the human head under quasistatic and dynamic loading (cadaver tests; mean dynamic failure load 11.9 kN, stiffness 4023 N/mm). <a href="https://wbldb.lievers.net/10149876.html">abstract</a>',
 'C. M. van Wyk, “A study of the compressibility of wool”, Onderstepoort J. Vet. Sci. 21, 99 (1946). <a href="https://repository.up.ac.za/handle/2263/59727">repository</a>',
 'Discrete fibre-network models of paper, Chalmers University of Technology. <a href="https://research.chalmers.se/en/publication/532887">link</a>',
]
