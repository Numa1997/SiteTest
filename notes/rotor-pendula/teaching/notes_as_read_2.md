
Part IA second blade on a turning blade

## 0 From scratch: the wind, the turbine, and the question

These notes ask one question: can a small swinging arm, hung at the tip of a wind-turbine blade, make enough electricity to run a sensor there? To answer it you need to know nothing about wind turbines in advance. This chapter builds what is needed from moving air upwards: how much power the wind carries, how much a turbine can take, how its blades turn, and what a blade feels as it goes round. Then it puts our machine on the blade and states the question properly.

One warning before we start. These notes work out the mechanics: gravity, the turning, the swing and the generator. The air also pushes on the swinging arm, and section 0.7 estimates that it pushes at least as hard as gravity does; what it does to the harvest is left for a later study. So what follows is the mechanical half of the answer. It is worth having on its own, because it says how much a swing driven by gravity can give at all, and who pays for it.

First, the parts, so that each has a name before the story begins (Figure 1). A tower, 90 m tall for the turbine of these notes, carries a long housing at its top, the nacelle. At the front of the nacelle, facing the wind, sits the hub, and three blades are fixed to it; hub and blades together are the rotor. The rotor turns a thick main shaft slowly, at most about 12 turns a minute. A gearbox, a set of gear wheels, turns that slow turning into a fast one, 97 times faster, and a generator turns the fast turning into electricity. A motor at the top of the tower keeps the nacelle turned to face the wind. That is all the machinery. The rest of this chapter explains the first link of the chain: how the wind makes the rotor turn.
[FIGURE: drawing; its caption follows]
Figure 1. A wind turbine seen from the side, not to scale: the nacelle is drawn far too large so that its inside can be seen. The wind comes from the left and turns the rotor, the hub with its three blades (seen from the side, the blade pointing up is a thin line, and the two pointing down overlap). The rotor turns the main shaft slowly; the gearbox makes the turning faster; the generator turns it into electricity. For the 5 MW turbine of these notes the hub stands 90 m above the ground, the rotor turns at most about 12 times a minute, and the gearbox speeds it up 97 times (Jonkman et al. 2009). The machine of these notes sits at the tip of a blade.

## 0.1 Moving air carries energy

Hold your flat hand out of the window of a car at motorway speed and the air shoves it back hard. At walking pace you feel nothing. Air has mass, about a kilogram in every cubic metre, and mass in motion carries kinetic energy.

[Warm-up]
A doorway 2 m high and 1 m wide stands open in a wind of 10 m/s. How much energy does the air carry through it every second? Try it before you open the answer.

[folded: Answer]
In one second the air that crosses the doorway is the air that was within 10 m upwind of it: a block 2 m × 1 m × 10 m, so 20 m³. At a density of 1.225 kg/m³ that is 24.5 kg. Each kilogram moving at 10 m/s carries $\tfrac12 v^2 = 50$ J. So 24.5 kg × 50 J/kg = 1 225 J every second: 1 225 W, about one electric kettle.

Do the same for any frame of area $A$ and any wind speed $v$. A cubic metre of air has the mass $\rho$, its density, so it carries the kinetic energy $\tfrac12\rho v^2$. In one second, the air within the distance $v$ upwind crosses the frame: a volume $Av$. So the wind carries through the frame the power
$$P_{\rm wind} = \tfrac12\rho v^2 \times A v = \tfrac12\,\rho\,A\,v^3. \tag{0.1}$$

The speed enters three times: twice in the energy of each kilogram, once more in how many kilograms arrive each second. That cube is the first fact of wind power. Double the wind and its power grows eightfold.

[On our turbine]
The turbine of these notes has blades that reach 63 m from the centre, so its blades sweep a disc of area $\pi\times 63^2$ = 12 469 m², about two football pitches. At 8 m/s every square metre of it receives 314 W, and the whole disc 3.91 MW. At 6 and 10 m/s the disc receives 1.65 and 7.64 MW: the wind speed grows by two thirds, its power by a factor of 4.6.

## 0.2 No turbine can take all of it

[Guess first]
A perfect turbine, with no friction and no losses of any kind, stands in the wind. What share of the wind's power (0.1) can it take: all of it, about half, or a tenth?

[folded: The answer, which this section derives]
At most 16/27, about 59 %. Not all of it, for a reason that has nothing to do with friction.

If a turbine took all of the wind's energy, the air leaving it would stand still. But still air cannot get out of the way, so the air arriving behind it would pile up and flow around the turbine instead of through it. So a turbine that stops the wind takes nothing, and a turbine that does not slow the wind takes nothing either. The best turbine slows the wind part of the way.

To find how far, treat the turbine as a thin disc of area $A$ that slows the air passing through it. Imagine the bundle of air that will pass through the disc as a tube, a stream tube. Far ahead of the disc the air in it moves at the wind speed $v$. At the disc it has been slowed to $v(1-a)$; the number $a$, the fraction of the speed lost by the time the air reaches the disc, is what we want to find. Far behind the disc the air has slowed further, to some speed $v_{\rm w}$ (the wake speed). Since slower air needs a wider tube to carry the same mass per second, the tube widens as it passes the disc.

Three laws you already know fix everything.

Mass. Every second the mass $\dot m = \rho A v(1-a)$ passes through the disc, and the same mass passes every cross-section of the tube.

Momentum. This air arrives with the speed $v$ and leaves with $v_{\rm w}$. Newton's second law says the force needed to slow it is its loss of momentum per second, $\dot m\,(v - v_{\rm w})$. That force comes from the disc, so the air pushes the disc downwind with the same force, the thrust. (This step ignores the push of the surrounding air on the sides of the widening tube; the standard derivation that avoids it, with Bernoulli's law applied in front of and behind the disc, gives the same thrust and the same results below.)
$$F = \dot m\,(v - v_{\rm w}).$$

Energy. The air loses kinetic energy at the rate $\tfrac12\dot m\,(v^2 - v_{\rm w}^2)$, and with no friction anywhere, all of it goes into the disc. But a force $F$ acting on air that moves through it at the speed $v(1-a)$ does work at the rate $F\,v(1-a)$. These are the same power, so
$$\tfrac12\dot m\,(v - v_{\rm w})(v + v_{\rm w}) = \dot m\,(v - v_{\rm w})\,v(1-a) \quad\Rightarrow\quad v(1-a) = \frac{v + v_{\rm w}}{2}.$$

The speed at the disc is the average of the speed far ahead and the speed far behind. So the disc does exactly half of the slowing, and the air goes on slowing behind it: $v_{\rm w} = v(1 - 2a)$. Put this back into the power, force times the speed at the disc:
$$P = \dot m\,(v - v_{\rm w})\,v(1-a) = \rho A v(1-a)\cdot 2av\cdot v(1-a) = \tfrac12\rho A v^3\cdot 4a(1-a)^2.$$

The first factor is the wind's power (0.1). The second is the share of it the disc takes, the power coefficient:
$$C_p = \frac{P}{P_{\rm wind}} = 4a(1-a)^2. \tag{0.2}$$

It is zero when the disc does not slow the air ($a = 0$). As $a$ grows towards $\tfrac12$ the wake slows to a standstill, $v_{\rm w} = v(1-2a) \to 0$; beyond that the formula would need the air behind the disc to flow backwards, so this simple model holds only for $a < \tfrac12$. (Real rotors pushed that hard make a turbulent, churning wake instead.) Between $a = 0$ and $a = \tfrac12$, $C_p$ rises and then falls. Its top is where $dC_p/da = 4(1-a)(1-3a) = 0$, at $a = \tfrac13$:
$$C_{p,\max} = 4\cdot\tfrac13\cdot\left(\tfrac23\right)^2 = \frac{16}{27} = 0.593. \tag{0.3}$$

No turbine of any shape can take more than 59 % of the power of the wind that crosses its disc. This is the Betz limit, found by Albert Betz in 1920. At the best setting the wind is slowed by a third at the disc and by two thirds in the wake.

[Check]
Units: $\rho A v^3$ is kg/m³ × m² × m³/s³ = kg m²/s³, which is a watt. At $a = 0$ the air passes untouched and $P = 0$, as the picture said. At $a = \tfrac12$ the wake stands still but $C_p = \tfrac12$, not zero: the picture's "a turbine that stops the wind" is a disc that stops the air at the disc itself, $a \to 1$, far outside the model, where indeed no air would pass. SymPy confirms each line of the derivation.

[On our turbine]
The turbine of these notes is a published design, the NREL 5 MW reference turbine (Jonkman et al. 2009). At its best it reaches $C_p = 0.482$, 81 % of the Betz limit; the rest is lost to the drag of the blades, to the swirl the rotor leaves in its wake, and to the gaps between three slender blades. At 6, 8 and 10 m/s, a moderate to fresh breeze, its rotor takes 0.80, 1.88 and 3.68 MW at its shaft. It starts turning at 3 m/s and reaches its full 5 MW at 11.4 m/s; in stronger wind it turns its blades a little out of the wind to spill the excess, and holds its rotor at a fixed speed. These notes stay in the winds below that, where the rotor's speed follows the wind.

## 0.3 How a blade turns a push into turning

[Warm-up]
Back to your hand out of the car window, flat and level. Now tilt its front edge up a little. What does your hand do?

[folded: Answer]
It rises. The tilted hand turns the oncoming air downwards; to push the air down, your hand must push on it, and the air pushes your hand up just as hard (Newton's third law). This sideways force, at right angles to the oncoming air, is lift. A wing, a sail and a turbine blade all work by it. There is also a smaller force along the oncoming air, the drag, which you feel as the push backwards.

A turbine's blades are not simply pushed round by the wind. Compare the spinning cups of a weather station's wind gauge. Each cup is pushed by the wind like a leaf blown along, so it can never move faster than the wind: once a cup moves as fast as the air, the air no longer pushes it. The tip of a turbine blade moves more than seven times faster than the wind. Only lift can do that, because lift acts across the air's motion: the blade gains speed sideways while the wind pushes on it from the front. So each blade is a long, twisted wing.

Look at one short piece of a blade, at the distance $r$ from the centre of the rotor (the hub). The rotor turns at the angular speed $\Omega$, in radians per second, so the piece moves sideways, in the plane in which the blades turn, at the speed $\Omega r$.

Ride on that piece. Two streams of air reach you. The wind comes from the front at $v(1-a)$, slowed at the rotor as section 0.2 found. And because you move sideways at $\Omega r$, air streams at you from the side you are moving towards, at $\Omega r$, just as a cyclist on a still day feels a head wind. You feel the sum of the two, the apparent wind. It comes in at the angle $\gamma$ (the inflow angle) to your own path, with
$$\tan\gamma = \frac{v(1-a)}{\Omega r}. \tag{0.4}$$

The lift on the piece is at right angles to the apparent wind. Because the apparent wind comes in at the angle $\gamma$, the lift leans forward by the same angle. Split it in two. Its part along the blade's path, $L\sin\gamma$, turns the rotor; its part along the wind, $L\cos\gamma$, pushes the whole rotor downwind. The drag $D$, along the apparent wind, holds the piece back by $D\cos\gamma$. So the piece helps to turn the rotor only if $L\sin\gamma > D\cos\gamma$, that is, if its lift is more than $\cot\gamma$ times its drag. Figure 2 draws this.
[FIGURE: drawing; its caption follows]
Figure 2. A piece of blade at the tip, seen along the blade from its tip, at 8 m/s. The blade moves to the right at 60.4 m/s, so air streams at it, from the direction it moves in, at that speed; the wind, from upwind along the shaft, blows through the rotor at 5.33 m/s, slowed by a third (section 0.2). Together they make the apparent wind, which comes in only 5.0° off the blade's path; the wind arrow is drawn 3 times too long so that the angle can be seen (it is drawn at 15°). The lift is at right angles to the apparent wind: mostly it pushes the rotor downwind, but it leans forward by the same angle, and that forward part is what turns the rotor.

An ice yacht can race across the wind at several times the wind's speed. Its sail is a wing, and most of the air it feels comes from its own motion. A turbine blade is a wing that sails round in a circle.

How fast should a rotor turn? The faster a blade moves, the smaller the angle $\gamma$ and the more the lift points downwind instead of round. Turn too slowly, and most of the wind passes through the wide gaps between the blades without being slowed. Turn too fast, and the blades sweep the disc so often that it behaves like a wall, and the wind goes round it. There is a second effect. A rotor that turns slowly must push hard on each piece of air to take the same power, and it leaves the air behind it swirling; the energy of that swirl is lost. The swirl shrinks as the rotor turns faster, while the losses to the blades' drag grow. With lift about a hundred times the drag, the best balance falls at a tip speed several times the wind's. The best speed is described by the ratio of the speed of the blade tips to the speed of the wind, the tip-speed ratio
$$\lambda = \frac{\Omega\,r_{\rm rot}}{v},$$

where $r_{\rm rot}$ is the rotor's radius. Every rotor has a best value $\lambda^*$, where it takes the largest share $C_p$ of the wind's power. For the 5 MW turbine $\lambda^* = 7.55$ (Jonkman et al. 2009), and its control system, a computer in the nacelle, holds the rotor close to it below 11.4 m/s by setting how hard the turbine's own generator, the main generator, brakes the shaft: brake harder and the rotor slows down, brake less and it speeds up. So at a steady wind $v$ the rotor turns at $\Omega = \lambda^*v/r_{\rm rot}$.

[On our turbine]
At 8 m/s, $\Omega = 7.55\times 8/63$ rad/s, one turn every 6.6 s. The tip moves sideways at 60.4 m/s while the wind, slowed by a third, reaches it at 5.33 m/s. The apparent wind is 60.6 m/s and comes in only 5.0° off the blade's path. The tip therefore turns the rotor only if its lift is more than 11.3 times its drag; good wing sections manage about a hundred. To the tip of a blade, the wind is a gentle side-draught on a fast, nearly head-on stream of air.

## 0.4 What a blade feels as it turns

Each blade of the 5 MW turbine is 61.5 m long and starts at a hub of radius 1.5 m, so its tip runs on a circle of radius 63 m. It is a hollow shell of glass fibre and resin, heavy near the hub and light at the tip: the published design gives it a mass of about 17.7 t, of which only 10 kg per metre sits at the very tip.

The rotor turns in a vertical plane, facing the wind. So every point of a blade climbs and falls once per turn: the tip rises 126 m, from the bottom of its circle to the top, and falls again, every 6.6 s at 8 m/s. And because the blade turns, "down" changes its direction relative to the blade once per turn. When the blade points straight up or straight down, gravity pulls along it. When the blade is level, gravity pulls across it, first to one side and, half a turn later, to the other. Anything that is free to swing at the tip of a blade is therefore pushed to and fro by gravity, once per turn. That push is what these notes are about.

[What to remember so far]

The wind carries the power $\tfrac12\rho A v^3$; at 8 m/s, 314 W per square metre.

No turbine can take more than 16/27 of it; the best slows the wind by a third at the rotor.

Blades are wings. They turn the rotor through lift, and run fastest where they work best: the tip moves at $\lambda^* = 7.55$ times the wind's speed.

Seen from a turning blade, gravity swings round once per turn.

## 0.5 A sensor that nobody can reach, and our machine

A large wind turbine is built to run for twenty years. Engineers would like to know, all that time, how each blade bends and shakes: a crack or a loose bolt changes how a blade vibrates long before it fails. A small sensor inside the blade can measure that. But it needs electricity, and the far end of a blade is the worst place on the machine to bring it. A cable would have to pass through the turning hub, and a battery 60 m out along a blade cannot be changed without stopping the turbine and sending a technician up a rope.

How much electricity? A minimal sensor reads an accelerometer all the time (the ADXL362 chip draws 1.8 µA at 2.0 V: 3.6 µW), sleeps (a radio chip, the CC2652R, draws 0.94 µA at 3.0 V: 2.8 µW) and once a second wakes for 1 ms of computing (3.39 mA at 3.0 V) and 1 ms of sending by radio (7.0 mA at 3.0 V): 10.2 µJ + 21.0 µJ = 31.2 µJ every second, 31.2 µW. In all about 37.6 µW, from the typical currents in the two datasheets; that leaves out the radio's start-up and the losses of a voltage converter. Is a harvester needed for so little? Over twenty years 37.6 µW adds up to 6.6 Wh, and one D-size lithium cell holds about 61 Wh (Saft LS 33600: 17 Ah at 3.6 V). So a battery could carry this minimal sensor, if it survives twenty years of cold, heat and shaking in a blade. The case for harvesting is the other end: the machine below gives about a thousand times more, enough for a sensor that measures faster, computes more and sends more, with no battery to fail.

The blade itself is full of motion, though. So here is an idea. At the very tip of the blade, put a hinge whose axle points along the rotor's shaft, and hang on it a second, much lighter blade, free to swing to and fro in the plane in which the blades turn. Call the big blade the mother blade. As it turns, gravity, swinging round once per turn (section 0.4), pushes the second blade to one side and then the other. A small generator in the hinge brakes that swing and turns it into electricity, and the sensor runs on that. From here on, the generator means this small one in the hinge; the turbine's own is the main generator.

Why call it a blade? Anything that sticks out at a blade tip meets the air at 45 to 76 m/s and would be built like a small blade, slim and smooth. Moving parts at blade tips are not new: many older turbines had tip brakes, the outer few metres of each blade mounted on a shaft along the blade so that they could turn across the wind and stop the rotor in a storm. These notes treat the second blade as a plain rod.

Tie a small weight to a short string, tie the string to the end of a stick 1 m long, and whirl the stick in a vertical circle, about once a second. The string stays stretched out along the stick, pointing away from your hand: the turning flings the weight outwards, about four times harder than gravity pulls it down, much as the tip of the turbine's blade is flung. But gravity keeps pulling down. Near the top and the bottom of the circle it pulls along the string; on the way up it pulls the weight back, on the way down it pulls it forward. So the string swings to and fro about the stick's line, once per turn. That once-per-turn push is what we harvest.
[FIGURE: drawing; its caption follows]
Figure 3. The machine. Left: the rotor seen along its shaft; the second blade (wine) is hinged at the tip of one blade, the mother blade. Right: the tip close up, seen from the turning mother blade; the second blade, of length $l$, has turned by the angle $\theta$ from the mother blade's outward line (dashed). The left view is not to scale here; the simulation draws it to scale, where a 1 m second blade on a 63 m rotor is a few pixels long.

## 0.6 Four questions, and the short answers

Four questions run through these notes. Here they are with their answers, so that you know where each chapter is going.

How much power? A second blade of 1 kg and 1 m, hinged at the 63 m tip, takes between 161 and 267 mW of mechanical power from its swing, in steady winds of 10 and 6 m/s: less in stronger wind, because a faster rotor flings the second blade outwards harder and holds it stiffer (chapters 2 and 3). A real motor and gearbox from a catalogue deliver 57 to 106 mW to the wires, more than 1 500 times the minimal sensor's 37.6 µW (chapter 7).

Who pays? The rotor. Every joule the generator takes comes from the rotor, through a slightly larger torque on its shaft (sections 1.8 and 3.2). The second blade takes at most 0.34 parts in a million of the turbine's power.

How big should it be? What counts is the second blade's mass times the distance from the hinge to its centre of mass, $ml/2$ (its first moment): the power grows in proportion to it (chapter 2). Where the mass sits matters as much as how much there is: the same mass in a lump at the end gives twice as much as when spread evenly (chapter 3). Over the sizes of real devices at blade tips, the best power at 6 m/s runs from 66.7 mW to 74.0 W, but the generator must grow with it; 1 kg on 1 m is the size the catalogue generator of chapter 7 serves best (section 7.6).

What about the wind's gusts and the blade's shaking? Gusts change the rotor's speed, and with it the power, by a few per cent (chapter 5). The mother blade bends under its own weight, and that adds a few per cent (chapter 6). Its vibration is the open question: the power it adds grows as the square of how far its tip vibrates; it is negligible at 5 mm and more than gravity gives at 100 mm, and we found no published value for this blade (chapter 6). Chapter 4 proves a ceiling: whatever the second blade does, chaotic or not, it cannot draw more from random shaking than a limit set by its mass and the shaking's strength.

## 0.7 Where the numbers come from, and what is left out

Every number in these notes is computed from the model; the inputs taken from datasheets and published designs are named with their sources. The simulation that comes with these notes, on the page beside them, solves the same equations live and draws the machine turning.

The rotor turns at $\Omega = \lambda^*v/r_{\rm rot}$ (section 0.3): 6.87, 9.16 and 11.44 turns a minute (rpm) at the three winds of these notes, 6, 8 and 10 m/s. The hinge sits at the tip, at the distance $r_p = r_{\rm rot}$ = 63 m from the hub, and moves at $\lambda^*v$: 45.3, 60.4 and 75.5 m/s.

The second blade is a thin, uniform rod. That is a choice that keeps the mathematics clean; its length $l = 1$ m is a choice too, and its mass $m = 1$ kg is set in chapter 7 by matching it to a real generator. The simulation draws it with a blade's tapered outline, but the physics treats it as a uniform rod.

One thing these notes leave out on purpose: the air on the second blade itself. At the tip the hinge moves through the air at 45.3 to 75.5 m/s. Air at that speed presses on anything in its way with a pressure of about $\tfrac12\rho v_{\rm tip}^2$: 2234 Pa at 8 m/s. Gravity pulls on the second blade with its weight, $mg = 9.81$ N. The air's pressure matches that on an area of only $mg/(\tfrac12\rho v_{\rm tip}^2) = 43.9$ cm², a little more than a playing card. A real second blade is far larger, so the air would push it at least as hard as gravity does. A steady push of the air would only make the second blade lean; what changes its harvest is the part of the air's push that varies once per turn, as the blade passes through stronger wind at the top of its circle than at the bottom, and through the slower air in front of the tower. Its size is not known without a model of the air. These notes answer the question for the mechanics alone; section 8.2 says what the air could change.

## 0.8 How to read these notes

Each step is built in the same order. A Warm-up or a Guess first box asks you something small before the main argument; try it, then open the answer. A Picture box gives something to imagine with your hands and eyes. The working follows, one line at a time, each with its reason. A green Check box tests the result: its units, its sign, and a case where the answer is already known. A wine-coloured On our blade box gives the numbers of the real machine. A What to remember box closes a chapter. Where a long piece of algebra was done by computer (SymPy, a program for symbolic algebra), the text says so and shows the steps a reader needs.

[Conventions]
SI units throughout. Gravity $g = 9.80665\ \mathrm{m/s^2}$, the standard value. A dot over a symbol is a derivative with respect to time $t$; a prime is a derivative with respect to the rotor's angle $\varphi$ (section 1.6). The second blade's angle $\theta$ is measured from the mother blade's outward direction, positive in the direction the rotor turns.

[Problems]

A storm brings 12 m/s instead of 8 m/s. By what factor does the wind's power through the rotor rise?

[folded: Answer]
By $(12/8)^3$ = 3.38, from (0.1): the speed counts three times.

A small turbine on a garden pole has a rotor 2 m across. How much power can it take, at most, from a wind of 6 m/s?

[folded: Answer]
Its disc has the area $\pi\times 1^2$ m², so the wind carries $\tfrac12\rho A v^3$ = 416 W through it (0.1). No turbine takes more than 16/27 of that (0.3): 246 W, enough for a few light bulbs.

Show that when a rotor runs at its best tip-speed ratio $\lambda^*$ and slows the wind by a third, the inflow angle at its tips does not depend on the wind speed. What is it for the 5 MW turbine?

[folded: Answer]
At the tip $\Omega r_{\rm rot} = \lambda^* v$, so (0.4) gives $\tan\gamma = v(1-a)/(\lambda^* v) = (1-a)/\lambda^*$: the wind speed cancels. With $a = \tfrac13$ and $\lambda^* = 7.55$, $\gamma$ = 5.0° at every wind in which the rotor is held at $\lambda^*$.

Halfway out along the blade, at $r$ = 31.5 m, what is the inflow angle at 8 m/s? What does the answer tell you about the shape of a blade?

[folded: Answer]
There the blade moves at only $\Omega r$ = 30.2 m/s, half the tip's speed, while the wind still arrives at 5.33 m/s. So $\tan\gamma$ is twice as large and $\gamma$ = 10.0°, against 5.0° at the tip. The air meets the blade at a steeper angle the nearer it is to the hub. To meet it at the same, best angle everywhere, the blade must be twisted along its length, set at a steeper angle to the plane in which it turns near the hub than at the tip. That is why blades are twisted.

Look at the rotor from the front. It turns anticlockwise, and the mother blade points level to the right, so its tip is moving up. A second blade hangs freely at that tip. Does gravity push it forward, in the direction the rotor turns, or backward? And half a turn later?

[folded: Answer]
The tip moves up, so "forward" is up, and gravity, pulling down, pushes the second blade backward. Half a turn later the mother blade points left and its tip moves down: now gravity pulls forward. So gravity pushes the second blade back and forth once per turn, the push of section 0.4.





## 1 Riding at the tip

This chapter finds the second blade's equation of motion. We find it the way you would if you sat at the tip of the mother blade: by noticing which pulls you feel there, and adding them up. The idea that makes this easy is one you already know from riding in a car.

## 1.1 Warm-up: a pendulum in a car

[Guess first]
A small weight hangs on a string from the mirror of a car. The car pulls away and keeps speeding up at a steady rate. While it speeds up, does the string hang straight down, tilted forward, or tilted back?

[folded: Answer]
Tilted back, and it stays tilted for as long as the car keeps speeding up at that rate.

Look at it first from the road. The weight speeds up with the car, at the car's acceleration $a$, so something must push it forward with the force $ma$. Only the string can, and a string pulls only along itself. So the string leans back until its pull has a forward part $ma$, as well as the upward part $mg$ that holds the weight up. Its angle $\alpha$ from the vertical follows from
$$\tan\alpha = \frac{a}{g}. \tag{1.1}$$

Now look at it from inside the car. There the weight hangs still, at an angle. To someone sitting in the car it seems as if a second gravity pulled everything backwards, with the strength $a$ for every kilogram: the same pull that presses you into your seat. Real gravity, $g$ down, and this apparent pull, $a$ backwards, add up to an apparent gravity of strength $\sqrt{g^2 + a^2}$, and the string hangs along it, as a plumb line hangs along real gravity. Nudge the weight and it swings about that tilted line, as an ordinary pendulum swings about the vertical.

Both descriptions are right. The road's is Newton's: the backward pull is not exerted by any object; it is what you must add when you describe motion from a frame that is itself accelerating. The car's description is the more convenient one, because in it the problem becomes a pendulum hanging still in a tilted gravity. We will do the same at the tip of the turbine's blade.

[Worked example]
A family car pulling away briskly speeds up at about 3 m/s². Then (1.1) gives $\tan\alpha = 3/9.81$, $\alpha$ = 17.0°. Keep that angle in mind: section 1.3 will find the second blade tilted to and fro by about as much at 6 m/s.

## 1.2 Riding the turning blade

[Guess first]
You whirl a stone on a string in a circle over your head and let go. Seen from above, does the stone fly straight outwards, away from your hand, or off along the circle, in the direction it was moving?

[folded: Answer]
Off along the circle, in the direction it was moving at the moment you let go. Nothing pushed it outwards: the string pulled it inwards, and when the pull stops the stone goes straight on.

Many people guess "outwards", because whirling a stone feels as if the stone pulled outwards on your hand. The feeling and the flight are both right; they are seen from two different frames. Seen from the ground, the stone moves on a circle, and anything that moves on a circle of radius $r$ at the angular speed $\Omega$ accelerates towards the centre, by $\Omega^2 r$, because the direction of its motion keeps turning. The string supplies the force for that. Seen by someone who turns with the stone, the stone stays put, held by the string against an apparent pull outwards, the centrifugal pull, of $\Omega^2 r$ for every kilogram. It is the turning frame's version of the car's backward pull.

Now sit at the tip of the mother blade. The hinge, our pivot, is at the distance $r_p$ from the hub, and the blade turns at $\Omega$. On every kilogram you feel two pulls: the centrifugal pull $\Omega^2 r$, straight away from the hub, with $r$ the distance from the hub; and gravity, $g$, straight down. Gravity is fixed to the ground, but you turn, so seen from your seat gravity goes round the other way, once per turn: while the blade climbs, gravity pulls back against its motion; at the top it pulls towards the hub; while the blade falls it pulls forward; at the bottom, outwards. The ratio of the two pulls at the hinge,
$$\Gamma = \frac{\Omega^2 r_p}{g}, \tag{1.2}$$

says which one wins.

[On our turbine]
At 8 m/s the rotor turns at $\Omega$ = 0.959 rad/s (section 0.3), so the hinge feels an outward pull of $\Omega^2 r_p$ = 0.919 s⁻² × 63 m = 57.9 m/s² for every kilogram: $\Gamma$ = 5.90. At 6 and 10 m/s, $\Gamma$ = 3.32 and 9.23. The outward pull beats gravity by a factor of three to nine, about as on the stick whirled once a second in section 0.5.

A turning frame has two more apparent forces. The Coriolis force acts on anything that moves relative to the turning frame; the Euler force acts while the turning speeds up or slows down. The next section shows what each does to the second blade.

## 1.3 The second blade: a pendulum in two gravities

Hang the second blade on the hinge: a thin uniform rod of mass $m$ and length $l$. Let $\theta$ be its angle from the mother blade's outward direction, positive in the direction the rotor turns. Put the hub at the origin with $y$ pointing up, and measure the rotor's angle $\varphi(t)$ from the horizontal, so that the hinge sits at $r_p(\cos\varphi, \sin\varphi)$. The point of the second blade at the distance $s$ from the hinge, $0 \le s \le l$, is at
$$x = r_p\cos\varphi + s\cos(\varphi+\theta), \qquad y = r_p\sin\varphi + s\sin(\varphi+\theta). \tag{1.3}$$
[FIGURE: drawing; its caption follows]
Figure 4. The second blade at the tip. The rotor angle $\varphi$ is measured from the horizontal; the hinge sits at $r_p$ from the hub; the second blade, of length $l$, makes the angle $\theta$ with the mother blade's outward direction (dashed). A piece of it at the distance $s$ from the hinge is pulled away from the hub by $\Omega^2 r$ per kilogram, with $r$ its own distance from the hub, and down by gravity, whose direction, seen from the turning mother blade, goes round once per turn. Not to scale: $r_p$ is 63 times $l$.

The rotor's motion $\varphi(t)$ is imposed from outside: the rotor is enormously heavier than the second blade, which cannot change it noticeably. So $\varphi(t)$ is a given function of time, not a second unknown.

Two numbers say how the rod resists turning and how a pull grips it. Its moment of inertia about the hinge, $I = ml^2/3$, is the sum of every piece's mass times its distance from the hinge squared. Its first moment about the hinge, $ml/2$, is the sum of every piece's mass times its distance: the whole mass times the distance from the hinge to the centre of mass. You know both from the rod pendulum, which under gravity alone swings at $\omega^2 = (ml/2)g/I = 3g/(2l)$.

Only torques about the hinge can turn the second blade; the hinge takes up every other force. So take the pulls one at a time and ask what torque each makes about the hinge.

The centrifugal pull. A piece at the distance $s$ from the hinge sits at $r_p\hat{\mathbf e} + s\,\hat{\mathbf e}_\theta$ from the hub, where $\hat{\mathbf e}$ points out along the mother blade and $\hat{\mathbf e}_\theta$ along the second blade. Its centrifugal pull, per kilogram, is $\Omega^2$ times that position, and it splits in two. The part $\Omega^2 s\,\hat{\mathbf e}_\theta$ points along the second blade, straight away from the hinge, so it has no lever arm: it only stretches the rod. The part left over, $\Omega^2 r_p\hat{\mathbf e}$, is the same for every piece: a uniform pull of strength $\Omega^2 r_p$, straight out along the mother blade. So, as far as turning the second blade goes, the centrifugal pull acts exactly like a second gravity, $\Gamma$ times stronger than the real one, pointing out along the mother blade.

Gravity. A uniform pull $g$ downwards, which, seen from the mother blade, goes round once per turn.

The Coriolis force. Per kilogram it is $-2\boldsymbol\Omega\times\mathbf v$, where $\mathbf v$ is the velocity relative to the turning frame and $\boldsymbol\Omega$ points along the rotor's shaft: it is always at right angles to the motion. A piece of the second blade can only swing about the hinge, so it moves at right angles to the second blade, and the Coriolis force on it therefore points along the second blade, through the hinge. No lever arm, no torque.

The Euler force. While the rotor's speed changes, at the angular acceleration $\ddot\varphi$, every kilogram at the position $\mathbf r$ from the hub feels $-\ddot\varphi\,\hat{\mathbf z}\times\mathbf r$, a pull against the way the rotor speeds up ($\hat{\mathbf z}$ along the shaft). Summed along the rod, its torque about the hinge is $-\left(I + \tfrac{ml}{2}r_p\cos\theta\right)\ddot\varphi$. It vanishes when the rotor turns steadily, and chapter 5 shows that gusts keep it tiny.

So the second blade is a pendulum hanging in two uniform gravities: a strong one, $\Gamma g$, fixed and pointing out along the mother blade, and the ordinary one, $g$, going round once per turn. Exactly as in the car, the two add up to an apparent gravity, and the second blade hangs along it like a plumb line.

Where does that plumb line point? Measure pulls in units of $g$. The outward one is an arrow of length $\Gamma$ along the mother blade. Gravity is an arrow of length 1 pointing down; along the mother blade it has the part $-\sin\varphi$, and across it, in the direction of increasing $\theta$, the part $-\cos\varphi$. So the apparent gravity has the parts $\Gamma - \sin\varphi$ along and $-\cos\varphi$ across, and it points at the angle $\theta_{\rm b}$ from the mother blade's line, with
$$\tan\theta_{\rm b} = -\frac{\cos\varphi}{\Gamma - \sin\varphi}.$$

How far can it tilt? Draw it: the long arrow ends at a fixed point, and the short arrow, added to its end, sweeps a circle of radius 1 around that point once per turn. Seen from the hinge, the sum points furthest off the mother blade's line when it just touches that circle, along a tangent; there the short arrow is at right angles to the sum, and the tilt is $\arcsin(1/\Gamma)$.

[On our turbine]
The largest tilt is 17.5°, 9.8° and 6.2° at 6, 8 and 10 m/s, to one side and then the other, once per turn. At 6 m/s that is about the tilt of the string in a car speeding up at 3 m/s² (section 1.1). At 10 m/s the outward pull is stronger and the plumb line rocks less.

## 1.4 The generator: a brake

Turn the wheel of an upside-down bicycle by hand, with its dynamo pressed against the tyre. With the lamp switched off the wheel spins freely; switch the lamp on and the wheel gets harder to turn, and the faster you turn it the harder it resists. That resistance is the electricity being made.

A generator is a coil turned past magnets. By Faraday's law of induction the voltage it makes is proportional to how fast it turns. Our generator's outer case, the stator, is fixed to the mother blade, and its turning part to the second blade, so it sees only the swing relative to the mother blade, $\dot\theta$. Its voltage $k_e\dot\theta$ drives the current $i = k_e\dot\theta/(R_c + R_L)$ through the coil's resistance $R_c$ and the load $R_L$, the sensor's circuit. The current, flowing in the magnets' field, makes a torque $k_t i$ that opposes the motion (Lenz's rule). So the generator's torque on the second blade is
$$-c\,\dot\theta, \qquad c = \frac{k_t k_e}{R_c + R_L},$$

a brake proportional to speed, like a spoon pulled through honey. It takes the power $c\dot\theta^2$ from the swing, and that power is the electricity, less what the coil wastes as heat (chapter 7 works out the split). The constant $c$ is set by the choice of generator and load; chapter 2 finds its best value.

## 1.5 The equation of motion, and a bowl that rocks

A rod in a uniform pull behaves as if all its mass sat at its centre of mass, at $l/2$ along it. Its potential energy is its weight in that pull times the height of the centre of mass, measured "uphill" against the pull. For gravity that is the familiar $\tfrac{ml}{2}\,g\sin(\varphi+\theta)$. For the outward pull, uphill is towards the hub, and the centre of mass sits $\tfrac l2\cos\theta$ further out than the hinge, so it contributes $-\tfrac{ml}{2}\,\Omega^2 r_p\cos\theta$. The second blade's potential energy in the turning frame is the sum:
$$U(\theta,\varphi) = \frac{ml}{2}\left[-\,\Omega^2 r_p\cos\theta + g\sin(\varphi+\theta)\right]. \tag{1.4}$$

The torque of the two pulls is minus the slope of $U$ along $\theta$. Add the Euler torque and the generator, and Newton's law for turning about the hinge, moment of inertia times angular acceleration equals the sum of the torques, reads
$$I\ddot\theta = -\frac{ml}{2}\left[\Omega^2 r_p\sin\theta + g\cos(\varphi+\theta)\right] - \left(I + \frac{ml}{2}r_p\cos\theta\right)\ddot\varphi - c\,\dot\theta, \qquad \Omega = \dot\varphi. \tag{1.5}$$

Every term has a meaning. $I\ddot\theta$ is the second blade's inertia about the hinge. $\frac{ml}{2}\Omega^2 r_p\sin\theta$ is the outward pull bringing the second blade back to the mother blade's line, a restoring torque like a spring's: we call it the centrifugal spring. $\frac{ml}{2}g\cos(\varphi+\theta)$ is gravity's torque, which turns with the rotor. The $\ddot\varphi$ term is the Euler torque. $c\dot\theta$ is the generator.

Nothing in (1.5) depends on the second blade's shape except through $I$ and its first moment. The same equation holds for any rigid body on the hinge, with its own moment of inertia $I_p$ about the hinge and its own first moment $Ml_c$, its mass times the distance $l_c$ from the hinge to its centre of mass. A small lump of mass $m$ at the end of a massless rod of length $L$ has $I_p = mL^2$ and first moment $mL$; a uniform rod has $ml^2/3$ and $ml/2$. Section 3.3 uses that.

[Check]
Units: every term is a torque, kg m²/s² = N m. Limit: stop the rotor ($\Omega = \ddot\varphi = 0$) with the mother blade at the angle $\varphi_0$. Then (1.5) is $I\ddot\theta = -\tfrac{ml}{2}g\cos(\varphi_0+\theta) - c\dot\theta$, an ordinary braked rod pendulum: at rest hanging straight down, $\varphi_0+\theta = -90°$, and swinging about it at $\omega^2 = (ml/2)g/I = 3g/(2l)$, the textbook frequency of a rod swinging from one end. The same equation follows from Lagrange's method in the ground frame, where no apparent forces exist (section 1.7).

Put a marble in a salad bowl and tilt the bowl gently one way, then the other. The lowest point of the bowl slides from side to side, and the marble chases it. Fill the bowl with honey and the marble lags behind the moving bottom, and the honey warms a little with every pass. Our second blade is that marble, the generator is the honey, and the bowl is (1.4).

Read (1.4) as that bowl. Its first term, $-\frac{ml}{2}\Omega^2 r_p\cos\theta$, is a bowl with its bottom at $\theta = 0$: the second blade lies along the mother blade because that is downhill in the turning frame. Gravity's term tilts the bowl, and the tilt changes as the rotor turns. Setting $\partial U/\partial\theta = 0$ puts the bottom at the angle $\theta_{\rm b}$ of section 1.3, the direction of the apparent gravity: on the mother blade's line when the mother blade points straight up or down, and furthest off it, by $\arcsin(1/\Gamma)$, near the horizontal. Figure 5 draws the bowl at four positions of the rotor.
[FIGURE: drawing; its caption follows]
Figure 5. The second blade's potential energy (1.4) in the frame of the mother blade, at 6 m/s ($\Gamma = 3.32$), at four positions of the rotor. The shape of the bowl is the centrifugal term and does not change; gravity tilts it, and its lowest point (dots) swings between 17.5° on one side and 17.5° on the other, $\arcsin(1/\Gamma)$, and back, once per turn. The second blade is a marble in this bowl, held in honey by the generator: it chases the moving bottom, and the generator takes energy from the chase.

[Guess first]
A child sits on a swing. You put your hand on the seat and simply move with it, back and forth, exactly as the swing goes, never ahead of it and never behind. Does the swing gain energy from your hand?

[folded: Answer]
No. On the way out your hand pushes along the motion and gives energy; on the way back the swing pushes your hand and gives the same energy back. Over a full swing your hand does no net work.

The same holds for the bowl. A second blade that kept exactly to the moving bottom would move in step with gravity's tilting push, in step with the push's position, and a push in step with the position it drives does no net work over a cycle. Then there would be nothing for the generator to take. The generator makes the second blade lag behind the moving bottom. With a lag $\delta$, gravity's push does net work in proportion to $\sin\delta$ every turn, and that work is what the generator harvests. Chapter 2 finds the best lag, $45°$, and a surprise: the best brake is so strong that the second blade no longer rings on its own at all; it creeps after the moving bottom, like the marble in thick honey.

## 1.6 The rotor as a clock

Now let the rotor turn steadily, $\dot\varphi = \Omega$, $\ddot\varphi = 0$. The natural clock is then the rotor's own angle: one turn is $2\pi$. Write $\theta' = d\theta/d\varphi = \dot\theta/\Omega$, and divide (1.5) by $I\Omega^2$:
$$\boxed{\theta'' + \kappa\,\theta' + R\sin\theta + G\cos(\varphi+\theta) = 0,} \qquad R = \frac{(ml/2)\,r_p}{I} = \frac{3r_p}{2l},\quad G = \frac{(ml/2)\,g}{I\,\Omega^2} = \frac{3g}{2l\Omega^2},\quad \kappa = \frac{c}{I\Omega}. \tag{1.6}$$

Three numbers say everything. $R$ is the stiffness of the centrifugal spring: a free small swing makes $\sqrt R$ swings per rotor turn. $G$ is the strength of gravity's push. $\kappa$ is the generator's brake. Their ratio $R/G$ is the $\Gamma$ of (1.2). Two bodies with the same $R$, $G$ and $\kappa$ do exactly the same thing, turn for turn, whatever their size or shape.

[Guess first]
In a stronger wind the rotor turns faster. Does a free second blade then make more swings per rotor turn, fewer, or the same number?

[folded: Answer]
The same. $R = 3r_p/(2l)$ does not contain $\Omega$: a faster rotor stiffens the centrifugal spring in proportion to $\Omega^2$, which raises the swing's frequency in proportion to $\Omega$, exactly as fast as the turns themselves come.

[On our blade]
For the 1 m second blade at the 63 m tip, $R$ = 94.5 at every wind, so a free second blade swings $\sqrt R$ = 9.72 times per rotor turn: its own rhythm is far quicker than gravity's once-per-turn push, never near it. $G$ is 28.45, 16.00 and 10.24 at 6, 8 and 10 m/s.

## 1.7 A check by Lagrange's method

You know Lagrange's method. Here it checks (1.5) from the ground frame, where there are no apparent forces at all, and it gives the energy balance of section 1.8. Differentiate (1.3), square, and add up the pieces' kinetic energies, $\tfrac12(m/l)(\dot x^2 + \dot y^2)\,ds$, along the rod. Each piece's speed squared has three parts: the hinge's own motion, $r_p^2\dot\varphi^2$; the piece's motion about the hinge, $s^2(\dot\varphi+\dot\theta)^2$; and a cross term, $2r_ps\,\dot\varphi(\dot\varphi+\dot\theta)\cos\theta$. The integrals $\int_0^l s^k ds$ give $l$, $l^2/2$ and $l^3/3$:
$$T = \tfrac12 I(\dot\varphi+\dot\theta)^2 + \tfrac12 m\,r_p^2\dot\varphi^2 + \frac{ml}{2}\,r_p\,\dot\varphi(\dot\varphi+\dot\theta)\cos\theta. \tag{1.7}$$

The potential energy is $V = mg\left[r_p\sin\varphi + \tfrac l2\sin(\varphi+\theta)\right]$, and the generator enters through Rayleigh's dissipation function $\mathcal F = \tfrac12 c\dot\theta^2$, half its power. With $\mathcal L = T - V$, Lagrange's equation for $\theta$,
$$\frac{d}{dt}\frac{\partial\mathcal L}{\partial\dot\theta} - \frac{\partial\mathcal L}{\partial\theta} = -\frac{\partial\mathcal F}{\partial\dot\theta} = -c\,\dot\theta,$$

needs the two derivatives
$$\frac{\partial\mathcal L}{\partial\dot\theta} = I(\dot\varphi+\dot\theta) + \frac{ml}{2}r_p\dot\varphi\cos\theta, \qquad \frac{\partial\mathcal L}{\partial\theta} = -\frac{ml}{2}r_p\dot\varphi(\dot\varphi+\dot\theta)\sin\theta - \frac{ml}{2}g\cos(\varphi+\theta).$$

Differentiate the first in time and subtract the second: the two $\dot\varphi\dot\theta\sin\theta$ terms cancel, and what is left is (1.5), term for term, Euler torque included. SymPy repeats the calculation and agrees identically.

## 1.8 Who pays

Seen from the mother blade, gravity's tilting push feeds the swing. But seen from the ground, gravity cannot pay for anything over a turn: the second blade comes back to the same height every turn, so gravity's work on it adds up to zero. Who pays, then?

The rotor pushes the hinge round its circle, with some torque $\tau_{\rm rot}$ about the hub. Lagrange's method gives the energy balance directly. Treat $\varphi$ as a second coordinate, driven by $\tau_{\rm rot}$. The Lagrangian does not contain time explicitly and $T$ is quadratic in the velocities, so Lagrange's energy function is $E = T + V$, and it changes only through the work of outside torques: the rotor's, at the rate $\tau_{\rm rot}\dot\varphi$, and the generator's. The generator acts between the mother blade and the second blade, inside the pair that the rotor drives; it does no work when $\varphi$ changes with $\theta$ held fixed, so it appears only through $\dot\theta$:
$$\frac{dE}{dt} = \tau_{\rm rot}\,\dot\varphi - c\,\dot\theta^2. \tag{1.8}$$

In a steady swing $E$ returns to the same value every turn, so over a turn the two terms balance: the rotor pays for every joule the generator harvests. Section 3.2 shows the mechanism: the second blade trails slightly behind the mother blade's line, so the outward pull on the hinge gets a small lever arm about the hub and holds the rotor back.

[On our turbine]
The rotor's torque on the second blade is mostly not about harvesting. Each turn it carries the second blade's weight up 126 m and lets it down again, which takes a torque swinging by about $mgr_p$ = 618 N m to either side and averaging to zero. The steady part that pays for the harvest is only the harvested power over $\Omega$: at 6 m/s, 0.372 N m. At the same wind, the wind turns the turbine's shaft with 1.11 MN m. The rotor pays, and does not notice.

[Check]
A second blade too short to matter ($l \to 0$ at fixed mass) is a point mass sitting on the hinge. The rotor's torque on it must then be its weight times its lever about the hub, $mgr_p\cos\varphi$, and the Lagrangian gives exactly that.

[What to remember]

In a frame that accelerates or turns, add apparent pulls. They are bookkeeping, not forces exerted by anything, and they make hard problems into pendulums at rest.

At the tip the outward pull is $\Gamma$ = 3 to 9 times gravity. For turning the second blade it acts as a uniform second gravity along the mother blade. The Coriolis force has no torque about the hinge; the Euler force acts only while the rotor changes speed.

The second blade hangs along the apparent gravity, which rocks by up to $\arcsin(1/\Gamma)$ each way once per turn: a bowl that rocks.

The generator is a brake, $-c\dot\theta$. Only a lag behind the moving bottom lets gravity's push do net work.

Counted in rotor turns, $\theta'' + \kappa\theta' + R\sin\theta + G\cos(\varphi+\theta) = 0$. $R$ is the same at every wind; $G$ falls as the wind rises.

The rotor pays for every joule, with a torque far too small for it to notice.

[Problems]

The car of section 1.1 brakes hard, slowing at 7 m/s². Which way does the string hang, and at what angle?

[folded: Answer]
Forward: the car's frame now accelerates backwards, so the apparent pull points forward. By (1.1), $\tan\alpha = 7/9.81$, $\alpha$ = 35.5°.

At what wind speed would the outward pull at the tip only just equal gravity, $\Gamma = 1$, if the rotor kept to $\lambda^*$?

[folded: Answer]
$\Omega^2 r_p = g$ gives $\Omega = \sqrt{g/r_p}$, and $v = \Omega r_p/\lambda^*$ = 3.29 m/s. The turbine starts turning at 3 m/s, so in almost every wind in which it turns, the outward pull wins.

Show that the Coriolis force on a piece of the second blade points along the second blade.

[folded: Answer]
Relative to the mother blade, the piece at $s$ moves with the velocity $s\dot\theta\,\hat{\mathbf n}$, where $\hat{\mathbf n}$ is the unit vector across the second blade, in the plane of the rotor. $\boldsymbol\Omega = \Omega\hat{\mathbf z}$ is at right angles to that plane, and $\hat{\mathbf z}\times\hat{\mathbf n} = -\hat{\mathbf e}_\theta$. So $-2\boldsymbol\Omega\times\mathbf v = 2\Omega s\dot\theta\,\hat{\mathbf e}_\theta$: along the second blade, through the hinge.

How many times a second does a free second blade swing at 8 m/s? Compare a 1 m rod swinging from one end on the ground.

[folded: Answer]
$\sqrt R$ swings per turn, at 6.6 s per turn: $\Omega\sqrt R/2\pi$ = 1.48 Hz. On the ground, $\sqrt{3g/2l}/2\pi$ = 0.61 Hz. The ratio is $\sqrt\Gamma$ = 2.43: the outward pull acts as a gravity $\Gamma$ times stronger, and a pendulum's frequency grows as the square root of its gravity.

At which rotor angle $\varphi$ is the bottom of the bowl furthest from the mother blade's line?

[folded: Answer]

Where the slope of $\tan\theta_{\rm b}$ vanishes:
$$\frac{d\tan\theta_{\rm b}}{d\varphi} = \frac{\Gamma\sin\varphi - 1}{(\Gamma - \sin\varphi)^2} = 0, \qquad \sin\varphi = \frac1\Gamma:$$

A little above the horizontal, once while the mother blade climbs and once while it falls. At 6 m/s that is 17.5° above the horizontal, and the tilt there is also 17.5°, since both are $\arcsin(1/\Gamma)$.

Over one steady turn, how much net work does gravity do on the second blade, seen from the ground? Where, then, does the harvested energy come from, and through what average torque at 6 m/s?

[folded: Answer]
None: the second blade returns to the same height. The energy comes from the rotor, by (1.8), through an average extra torque of $P/\Omega$ = 0.372 N m.





## 2 The best brake, and how much it gives

Chapter 1 ended with equation (1.6). It cannot be solved in closed form, but for small swings it can, and the answer holds the whole design rule: how hard the generator should brake, and how much power it then gets. The answer has the same shape as a question about batteries, so start there.

[Warm-up]
A battery makes 12 V, but inside it has a resistance of 2 Ω, which its current must pass through as well as through whatever you connect. You connect a lamp of resistance $R_L$. Which lamp gets the most power: one of 1 Ω, 2 Ω or 4 Ω? And what do a bare wire (0 Ω) and no lamp at all (an open gap) get?

[folded: Answer]
The current is $12/(2 + R_L)$ amperes, and the lamp's power is the current squared times $R_L$: 16 W at 1 Ω, 18 W at 2 Ω, 16 W at 4 Ω. The bare wire carries a large current but has no resistance to turn it into heat: 0 W. The open gap carries no current: 0 W. The most goes to the lamp whose resistance matches the battery's own, 2 Ω. Keep the shape in mind: nothing at either extreme, and a best value in between, where the load matches the source.

## 2.1 Small swings: a driven, braked oscillator

Hang a weight on a stiff spring and move your hand slowly up and down, far slower than the spring's own bounce. The weight simply follows your hand. Put the weight in honey and it follows a little late. It never bounces, because you never push at its own rhythm.

Let $\theta$ be small, so $\sin\theta \approx \theta$ and $\cos(\varphi+\theta) \approx \cos\varphi - \theta\sin\varphi$. Keep the first piece, gravity's push $G\cos\varphi$. The second piece, $-G\theta\sin\varphi$, makes the spring's stiffness go up and down once per turn. It is not small because the swing is small: compared with the spring's own term $R\theta$ it has the size $G/R = 1/\Gamma$, up to 0.30 at 6 m/s. We may drop it because of when it acts. Multiplying a swing at once per turn by $\sin\varphi$ makes motion at zero and twice per turn, not at once per turn, and that motion acts back on the once-per-turn swing only by passing through the same term a second time. So its effect is of second order, and section 2.4 measures it, together with everything else the small-swing theory leaves out. Without it, (1.6) becomes
$$\theta'' + \kappa\,\theta' + R\,\theta = -G\cos\varphi. \tag{2.1}$$

You know this equation: the driven, damped oscillator. A spring of stiffness $R$ (natural frequency $\sqrt R$ per turn), a damper $\kappa$, and a push of amplitude $G$ at the frequency 1 per turn.

## 2.2 The swing

Once the start-up has died away the second blade swings at the frequency of the push. Write $\theta = \mathrm{Re}\,[A\,e^{i\varphi}]$, so that $\theta' \to iA$ and $\theta'' \to -A$. Then (2.1) is one line of algebra:
$$(R - 1 + i\kappa)A = -G \quad\Rightarrow\quad \theta = -\Theta\cos(\varphi - \delta), \qquad \Theta = \frac{G}{\sqrt{(R-1)^2 + \kappa^2}}, \qquad \tan\delta = \frac{\kappa}{R-1}. \tag{2.2}$$

Why $R - 1$ and not $R$? The $-1$ is the second blade's own inertia: shaking any body back and forth at the frequency 1 takes a torque proportional to its angular acceleration, $-\theta''$, which here works against the spring. So $R - 1$ is the spring minus the inertia at the push's frequency, the net stiffness the push meets. With no brake ($\kappa = 0$) the second blade moves exactly in step with the push and swings by $G/(R-1)$; a brake makes the swing smaller and makes it lag behind the push by the angle $\delta$.

A picture of (2.2): draw each torque as an arrow that turns once per turn, its length the torque's size. Gravity's push is one arrow. The net stiffness's torque points along the swing. The brake's torque opposes the velocity, so it stands at right angles to the swing. The two together must balance gravity's push, closing a right-angled triangle whose hypotenuse is gravity's arrow.

## 2.3 The harvested power

The generator takes the power $c\dot\theta^2$. Averaged over a turn, $\langle\dot\theta^2\rangle = \Omega^2\langle\theta'^2\rangle = \Omega^2\Theta^2/2$, so
$$\bar P = \tfrac12 c\,\Omega^2\Theta^2 = I\Omega^3\,\frac{\kappa\,G^2}{2\left[(R-1)^2 + \kappa^2\right]}. \tag{2.3}$$

Read it as the battery of the warm-up. A weak brake ($\kappa \to 0$) is the open gap: the second blade swings freely but nothing is taken. A strong brake ($\kappa \to \infty$) is the bare wire: it locks the second blade to the mother blade, nothing moves, and again nothing is taken. In between lies a best brake. Set $d\bar P/d\kappa = 0$:
$$(R-1)^2 + \kappa^2 - 2\kappa^2 = 0 \quad\Rightarrow\quad \kappa^* = |R - 1|. \tag{2.4}$$

The best brake equals the net stiffness: the load matches the source. At that setting $\tan\delta = 1$, and the second blade lags gravity's push by exactly 45°; in the triangle of torques the brake's arrow and the net stiffness's arrow are equal. Put $\kappa^*$ back into (2.3) and return to physical units with $I\Omega^2(R-1) = \left(\tfrac{ml}{2}r_p - I\right)\Omega^2$ and $I\Omega^2G = \tfrac{ml}{2}g$:
$$\boxed{P^* = \frac{\left(\tfrac{ml}{2}\,g\right)^2}{4\,\Omega\left(\tfrac{ml}{2}\,r_p - I\right)} = \frac{m\,g^2\,l}{8\,\Omega\left(r_p - \tfrac23 l\right)}.} \tag{2.5}$$

How strong is this brake? A spring of stiffness $R$ with a damper $\kappa$ just stops ringing when nudged, the brake called critical damping, at $\kappa = 2\sqrt R$. The best brake is $\kappa^*/(2\sqrt R)$ = 4.8 times that. Nudge the second blade and it does not ring at all; it creeps back. It does not need to ring, because it is pushed far below its own rhythm: it creeps after the moving bottom of the bowl of section 1.5, the marble in thick honey.

The exact electrical twin: an alternating supply feeds a resistor through a coil. The coil opposes the alternating current with its reactance, $\omega L_{\rm coil}$, but takes no power. The resistor takes the most power when its resistance equals that reactance. The generator is the resistor, the net stiffness $R - 1$ is the coil's reactance, and gravity's push is the supply.
[FIGURE: drawing; its caption follows]
Figure 6. The harvested power (2.3) over its maximum (2.5), against the brake over the best brake (2.4): $\bar P/P^* = 2x/(1+x^2)$ with $x = \kappa/\kappa^*$, the same curve at every wind and for every second blade. The top is flat: a brake 0.27 times the best, or 3.7 times it, still gives half the power ($x = 2 \mp \sqrt3$).

[Check]
Units: kg · (m/s²)² · m / (s⁻¹ · m) = kg m²/s³ = W. Limits: no gravity ($g \to 0$) gives no power, as it must, since nothing then pushes the second blade off the mother blade's line. At $\tfrac{ml}{2}r_p = I$, that is $l = \tfrac32 r_p$, the formula blows up: that is resonance, the second blade's own frequency $\sqrt R$ equal to the push's. Section 2.5 shows that no second blade shorter than its mother blade gets there. A small lump on a light rod, $I = mL^2$ and first moment $mL$, gives the simpler form $mLg^2/(4\Omega|r_p - L|)$.

Three results follow from (2.5).

The generator's torque. At the best brake the generator's torque swings with the amplitude
$$\tau^* = c^*\Omega\,\Theta^* = I\Omega^2(R-1)\cdot\frac{G}{\sqrt2\,(R-1)} \quad=\quad \frac{\tfrac{ml}{2}\,g}{\sqrt2},$$

3.47 N m for our second blade, at every wind. The triangle of torques says why: at the best brake its two short sides are equal, so each is the hypotenuse, gravity's largest torque $\tfrac{ml}{2}g$, divided by $\sqrt2$. That is the torque the generator must be built to hold.

The best brake in physical units. $c^* = \kappa^*I\Omega = \left(\tfrac{ml}{2}r_p - I\right)\Omega$, and on a large rotor, where $r_p \gg l$,
$$c^* \approx \frac{ml}{2}\,r_p\,\Omega: \tag{2.6}$$

the first moment times the speed of the hinge. For our second blade that is 22.4 to 37.4 N m s from 6 to 10 m/s, a hard brake for a small machine, and chapter 7 finds that building it is the hardest part of the generator.

[Guess first]
The wind gets stronger and the rotor turns faster. Does the second blade, at its best brake, give more power or less?

[folded: Answer]
Less, as the next equation shows.

The power on a large rotor.
$$P^* \approx \frac{\tfrac{ml}{2}\,g^2}{4\,\Omega r_p} = \frac{\tfrac{ml}{2}\,g^2}{4\,v_{\rm tip}}. \tag{2.7}$$

It depends on the second blade only through its first moment, and on the turbine only through the speed of the hinge, $v_{\rm tip} = \Omega r_p = \lambda^*v$. The faster the hinge moves, the less power: the outward pull grows as $\Omega^2$ and holds the second blade stiffer, so gravity, which does not change, moves it less. The second blade gives the most in light wind.

## 2.4 On our blade

[Worked example]
Take 8 m/s, with the 1 kg, 1 m second blade at the 63 m tip. The rotor turns at $\Omega$ = 0.959 rad/s, one turn every 6.6 s. The stiffness is $R = 3r_p/2l$ = 94.5 and gravity's number is $G = 3g/(2l\Omega^2)$ = 16.00. The best brake is $\kappa^* = R - 1$ = 93.5, that is $c^* = \kappa^* I\Omega$ = 29.9 N m s. The swing is $\Theta^* = G/(\sqrt2\,\kappa^*)$ = 0.121 rad, 6.9°: the free end of the second blade sways 12 cm to either side of the mother blade's line, once every 6.6 s, a slow, gentle sway. The generator holds a torque swinging by 3.47 N m, and (2.5) gives $P^*$ = 201 mW.

Table 1 does the same at the three winds, next to the full nonlinear model of chapter 3 at the same brake. $R$ and $\kappa^*$ are the same at every wind; $G$, $c^*$ and the swing change.

Table 1. The second blade at the three winds, at its best brake. At every wind $R = 94.5$ and $\kappa^* = R - 1 = 93.5$; full: the full nonlinear model of chapter 3 at the same brake.wind | rotor | $G$ | $c^*$ (N m s) | $\Theta^*$ (rad) | $P^*$ (2.5), mW | full, mW | 

6 m/s | 6.87 rpm | 28.45 | 22.4 | 0.215 | 268.2 | 267.4 | 

8 m/s | 9.16 rpm | 16.00 | 29.9 | 0.121 | 201.2 | 200.9 | 

10 m/s | 11.44 rpm | 10.24 | 37.4 | 0.077 | 160.9 | 160.9 | 

The closed form (2.5) is within 0.31 % of the full model at every wind. Equation (2.7), which leaves out the second blade's own inertia $I$ against $\tfrac{ml}{2}r_p$, gives 265.4, 199.0 and 159.2 mW: within 1.1 % of (2.5), because $l$ is 63 times shorter than $r_p$.

How far can the small-swing theory be trusted? Figure 7 sets it against the full equation (1.6), with $\sin\theta$ and $\cos(\varphi+\theta)$ kept whole. Near the best brake the two agree to 0.3 % at every wind. They part where the second blade swings furthest, at a light brake in light wind. At 6 m/s and a brake of 0.05 $\kappa^*$ the swing reaches 0.31 rad, and the full equation gives 11 % more power than (2.3); at 10 m/s, with a swing of 0.11 rad, only 1.3 %. Across the three winds the excess is 1.1 to 1.2 times the swing squared, $\Theta^2$. Every neglected effect grows that way: the cubic term of $\sin\theta$ and the $\theta^2\cos\varphi$ term of gravity's push are of higher order in the swing, and the dropped term of section 2.1, of order $G^2$, grows as $\Theta^2$ too, because the swing $\Theta$ is itself proportional to $G$. So the comparison shows how large the neglected effects are together, not which one dominates.

The right half of Figure 7 shows what the theory misses at the best brake. The timing of the swing is right, and so is its size: the theory's 0.215 rad at 6 m/s against the full model's 0.214 rad. But the whole full swing is shifted: its average angle is −0.0231 rad, slightly behind the mother blade's line, and that shift is most of the difference between the two curves (what remains is 0.0112 rad rms, the root of the mean of the squared difference). The second blade does not swing about the mother blade's line but about a line slightly behind it. A linear theory cannot produce a constant offset from a push that averages to zero; it takes the second-order terms. Section 3.2 shows that this small trail is exactly what makes the rotor pay.

[FIGURE: drawing; its caption follows][FIGURE: drawing; its caption follows]
Figure 7. The small-swing theory against the full equation (1.6), solved by the simulation's own engine. First panel: harvested power over its maximum $P^*$ (2.5), against the brake over the best brake. The line is formula (2.3), the same for every wind; the dots are the full equation at 6 (wine), 8 (ochre) and 10 m/s (blue). Second panel: one turn of the swing at the best brake; solid the full equation, dashed the theory (2.2). The two have the same shape and the same phase; the full swing is shifted down by its mean trail.

## 2.5 Resonance is out of reach

Any oscillator gives the most when it is pushed at its own rhythm, at resonance. Can the second blade get there? Its stiffness is $R = 3r_p/(2l)$, so the net stiffness $R - 1$ falls to zero only for $l = \tfrac32 r_p$, a second blade half as long again as the mother blade. For any second blade no longer than its mother blade, $R \ge \tfrac32$, and for ours $R - 1$ = 93.5. The centrifugal spring of a body hinged at the tip of a long blade is always far stiffer than its own inertia at the push's frequency. To reach resonance, extra inertia would have to cancel it, for example a heavy flywheel turned by the generator through a gearbox (chapter 7): it would have to add about 90 times the second blade's own moment of inertia. These notes do not pursue that.

[What to remember]

For small swings the second blade is a driven, braked oscillator: stiffness $R$, push $G$ once per turn, brake $\kappa$.

The best brake equals the net stiffness, $\kappa^* = R - 1$: the load matches the source, as for a lamp on a battery. The swing then lags the push by 45°.

The best brake is about five times critical damping: the second blade does not ring, it creeps after the moving bottom of the bowl.

$P^* \approx \tfrac{ml}{2}g^2/(4v_{\rm tip})$: proportional to the first moment, and smaller in stronger wind. At 6, 8 and 10 m/s, 268, 201 and 161 mW for 1 kg on 1 m.

The generator must hold $\tfrac{ml}{2}g/\sqrt2$ = 3.47 N m at every wind.

[Problems]

Show from (2.3) that a brake twice as strong as the best one, or half as strong, gives the same power. What fraction of $P^*$ is it?

[folded: Answer]
With $x = \kappa/\kappa^*$, (2.3) and (2.5) give $\bar P/P^* = 2x/(1 + x^2)$, which is unchanged when $x \to 1/x$. At $x = 2$ or $\tfrac12$ it is 4/5, 80 % of $P^*$. The hump of Figure 6 is flat-topped: the brake need not be set exactly.

At 10 m/s, how far does the free end of our second blade sway, and how much power does it give at the best brake?

[folded: Answer]
$\Theta^* = G/(\sqrt2\,\kappa^*)$ with $G$ = 10.24: 0.077 rad, so the free end sways 8 cm either way. (2.5) gives 161 mW.

The second blade's mass is doubled, at the same length. What happens to $P^*$, to the best brake $c^*$, and to the torque the generator must hold?

[folded: Answer]
All three double. In (2.5) the first moment appears squared on top and once below; $c^*$ and $\tau^*$ are each proportional to the first moment.

Why is the generator's torque at the best brake the same at every wind, although the power is not?

[folded: Answer]
Gravity's largest torque, $\tfrac{ml}{2}g$, does not depend on the wind, and at the best brake the generator carries $1/\sqrt2$ of it. What changes with the wind is how fast the swing goes: power is torque times angular speed, and the swing's angular speed, $\Omega\Theta^*$, falls as the rotor speeds up because $\Theta^*$ falls as $1/\Omega^2$.

In the warm-up, the lamp that gets the most power gets only half of what the battery makes; the other half heats the battery. Does the generator at its best brake waste half of the power in the same way?

[folded: Answer]
No. The net stiffness, like the coil in the electrical twin, stores energy and gives it back each swing but takes none. All of $P^*$ goes into the generator. (Inside the generator, some of it heats the coil; chapter 7.)





## 3 Big swings, the bill, and chaos

Chapter 2 kept only the terms of (1.6) that are linear in $\theta$. This chapter solves the full equation on a computer, finds out exactly how the rotor pays, asks where along the second blade its mass is best placed, and whether the motion can turn chaotic.

## 3.1 The full equation, solved numerically

Push a spoon slowly through thick honey and it moves calmly; flick it and the honey stops it almost at once. A heavily braked second blade has both kinds of motion at once: a slow swing, and a very fast death of any jerk the brake fights. An equation with two such different speeds in it is called stiff.

How different are the two speeds? A small disturbance of the braked spring behaves as $e^{\mu\varphi}$, with $\mu^2 + \kappa\mu + R = 0$. At the best brake, $\kappa^* = R - 1$, the two roots are far apart. The fast one, $\mu \approx -\kappa^*$, says that a jerk of the second blade against the generator dies in $1/(\kappa^*\Omega)$: 0.011 s at 8 m/s. The slow one, $\mu \approx -R/\kappa^*$, says that a second blade pushed off its path creeps back to it in $\kappa^*/(R\Omega)$: 1.03 s. One turn lasts 6.55 s.

Equation (1.6), with $\sin\theta$ and $\cos(\varphi+\theta)$ kept whole, is integrated step by step on a computer. A method that computes each step only from the present state (an explicit method, such as the classical Runge–Kutta method) must take steps shorter than the fast time, or its errors grow without bound. An implicit method instead solves, at each step, an equation for the state at the end of the step, and stays stable with steps as long as the slow swing allows. These notes use one, the three-stage Radau IIA method, which is of fifth order: halving the step should cut the error by $2^5$. On this equation its error falls on average by $2^{ 5.2 }$ per halving. The torques it uses agree with a direct sum of Newton's law over the pieces of the second blade to 4·10⁻¹⁵, and after the start-up it agrees with an independent high-accuracy solver to 2·10⁻¹² in the harvested energy. Started from rest, its first turns carry an error of 8·10⁻⁷, because a step, 1/240 of a turn, is longer than the fast time; the runs let 60 turns pass before they measure, and by then it has died away.

The closed form (2.5) is within 0.31 % of the full model at every wind, although the second blade swings up to 0.214 rad (12.2°). Why so close? At second order three effects appear, and the computer can switch each on alone, holding the brake at $\kappa^*$. At 6 m/s, where the swing is largest, the term section 2.1 dropped, $-G\theta\sin\varphi$, changes the power by +1.43 %; the softer spring of $\sin\theta$ by +0.59 %; and gravity's push kept whole, which includes the dropped term and also lowers the push by $\tfrac12G\theta^2\cos\varphi$, by −0.90 %. Together, the full equation: −0.31 %. The effects pull both ways and nearly cancel. At 8 and 10 m/s each is three and eight times smaller, as the swing squared (the full equation: −0.10 % and −0.04 %).

## 3.2 The second blade trails, and that is the bill

[Guess first]
Averaged over a turn, does the second blade sit exactly on the mother blade's line, a little ahead of it, or a little behind?

[folded: Answer]
A little behind, against the direction of rotation; and that small trail is exactly what makes the rotor pay.

Keep the term that section 2.1 dropped, $-G\theta\sin\varphi$. Because the swing $\theta$ is itself of order $G$, this term is of second order in $G$. Average (1.6) over a steady turn: the averages of $\theta''$, $\theta'$ and $\cos\varphi$ vanish, and what is left is
$$R\,\bar\theta = G\,\langle\theta\sin\varphi\rangle, \tag{3.1}$$

with the swing (2.2), $\theta = -\Theta\cos(\varphi-\delta)$, on the right. Its average with $\sin\varphi$ is $-\tfrac12\Theta\sin\delta$, and (2.2) gives $\sin\delta = \kappa\Theta/G$, so
$$\bar\theta = -\frac{\kappa\,\Theta^2}{2R}, \qquad\text{at the best brake}\quad \bar\theta = -\frac{G^2}{4R(R-1)}. \tag{3.2}$$

The minus sign means the second blade trails behind the mother blade's line, against the rotation, like a weight towed behind a boat.

Now compare (3.2) with the harvested power (2.3), $\bar P = I\Omega^3\cdot\tfrac12\kappa\Theta^2$. The same combination $\kappa\Theta^2$ appears in both, and since $IR = \tfrac{ml}{2}r_p$, for every brake setting
$$\boxed{\bar P = -\,\frac{ml}{2}\,r_p\,\Omega^3\,\bar\theta.} \tag{3.3}$$

The trail is the bill. The exact version holds for any steady swing, large or small. Write out the rotor's torque on the second blade, $\tau_{\rm rot}$ of section 1.8, for a steadily turning rotor, and use (1.5) to remove the second blade's angular acceleration. SymPy and a page of algebra give
$$\tau_{\rm rot} = -\frac{ml}{2}r_p\Omega^2\sin\theta + mgr_p\cos\varphi + \frac{d}{dt}\left[\frac{ml}{2}r_p\,\frac{d\sin\theta}{dt} + ml\,r_p\Omega\cos\theta - c\,\theta\right].$$

The second term is the rotor carrying the second blade's weight round, which averages to zero over a turn. The bracket is a total time derivative of something that returns to its value every turn, so it averages to zero too; it holds the generator's torque, $-c\dot\theta = -d(c\theta)/dt$. Only the first term survives the average, so $\bar P = \langle\tau_{\rm rot}\rangle\Omega = -\tfrac{ml}{2}r_p\Omega^3\langle\sin\theta\rangle$, exactly. (With the geared generator of chapter 7 the identity changes, because the gearbox's own torque enters the rotor's.)

Figure 8 shows the mechanism. The second blade, flung outwards, pulls on the hinge, along the line from the hub to its own centre of mass, with the force $m\Omega^2$ times that centre's distance from the hub. When the second blade trails, its centre of mass sits a little behind the mother blade's line, so that pull is no longer aimed straight away from the hub: its line misses the hub by a small lever arm, and it pulls the rotor backwards with the torque $\tfrac{ml}{2}r_p\Omega^2\sin\theta$, negative while the second blade trails. That is the first term above with its sign reversed: the rotor's torque on the second blade balances the second blade's torque on the rotor. The rotor must push against that pull, all the time, and that steady push is the power it pays.
[FIGURE: drawing; its caption follows]
Figure 8. Why the trail is the bill. The second blade trails behind the mother blade's line, against the rotation; the trail is drawn 15 times too large (at 6 m/s it is 1.31°). Flung outwards, the second blade pulls on the hinge along the line from the hub to its centre of mass (green). That line misses the hub by a small lever arm (wine), so the pull holds the rotor back, with the torque $\tfrac{ml}{2}r_p\Omega^2\sin\theta$; on average 0.372 N m at 6 m/s. The rotor pushes against it, and that steady push is the power it pays.

[On our blade]
By (3.2) the trail at the best brake is 1.31°, 0.42° and 0.17° at 6, 8 and 10 m/s: the bill shrinks fast as the wind rises. At 6 m/s, (3.2) gives $\bar\theta$ = −0.0229 rad and the full model −0.0231 rad. In all nine runs of the full model (three winds, three brakes), the exact identity holds to 1·10⁻¹².

## 3.3 Where the mass sits

Swing a hammer held at the very end of its handle, then grip the same hammer halfway up. The second swing is easier and weaker: the same mass now sits nearer your hand, with less leverage. Spreading the second blade's mass along its length does the same to it.

Section 1.5 noted that (1.5) holds for any rigid body on the hinge, with its own moment of inertia $I_p$ and first moment $Ml_c$. Redo chapter 2 for such a body: $I$ becomes $I_p$, the first moment $ml/2$ becomes $Ml_c$, and (2.5) becomes
$$P^*_{\rm rigid} = \frac{(M\,l_c\,g)^2}{4\,\Omega\,(M\,l_c\,r_p - I_p)}. \tag{3.4}$$

On a large rotor this is simply proportional to the first moment $Ml_c$, as (2.7) said for the rod. So the same mass placed farther from the hinge gives more, in proportion to the distance of its centre of mass. A uniform blade has its centre of mass halfway out; the same mass as a lump at its end has it all the way out, and gives, by (3.4), 2.011 times as much as the uniform blade, almost exactly twice. A real blade-shaped second blade tapers towards its free end like the mother blade, which puts its centre of mass nearer the hinge than halfway: for harvesting, the wrong way round.

[Check]
For the lump on a light rod, $I_p = mL^2$ and $Ml_c = mL$, and (3.4) is $mLg^2/(4\Omega|r_p - L|)$ of section 2.3. For the uniform rod, $I_p = ml^2/3$ and $Ml_c = ml/2$, and (3.4) is (2.5).

## 3.4 Chaos and the harvest

A pendulum driven periodically and braked can move chaotically: two copies started a hair apart drift apart exponentially, like two leaves dropped side by side into a stream. Our second blade is such a pendulum, (1.6), so the question must be asked. The rate of that drift is the largest Lyapunov exponent $\Lambda$: start two copies $10^{-8}$ apart, follow them, rescale their separation back every quarter turn of the rotor, and divide the logarithm of the total growth by the number of turns. A regular, damped motion gives $\Lambda < 0$; chaos gives $\Lambda > 0$. Because chaos depends on where the motion starts, every case is run from 8 different starts, the second blade at rest on the mother blade's line and 7 at random angles and rates, some tumbling right over at first; and at the best brake and at a tenth and a hundredth of it, where a lightly braked swing has the most freedom.

[On our blade]

Table 2. The largest Lyapunov exponent per turn at each wind and brake, the largest over the 8 starting states tried; beside it the decay rate per turn of a small disturbance of the braked spring alone, $2\pi\,\max\,\mathrm{Re}\,\mu$, where $\mu$ are the two roots of $\mu^2 + \kappa\mu + R = 0$.wind | $G$ | brake | $\Lambda$ per turn | small-swing decay | 

6 m/s | 28.45 | 1 $\kappa^*$ | −6.50 | −6.42 | 

6 m/s | 28.45 | 0.1 $\kappa^*$ | −29.36 | −29.37 | 

6 m/s | 28.45 | 0.01 $\kappa^*$ | −2.92 | −2.94 | 

8 m/s | 16.00 | 1 $\kappa^*$ | −6.44 | −6.42 | 

8 m/s | 16.00 | 0.1 $\kappa^*$ | −29.36 | −29.37 | 

8 m/s | 16.00 | 0.01 $\kappa^*$ | −2.92 | −2.94 | 

10 m/s | 10.24 | 1 $\kappa^*$ | −6.43 | −6.42 | 

10 m/s | 10.24 | 0.1 $\kappa^*$ | −29.36 | −29.37 | 

10 m/s | 10.24 | 0.01 $\kappa^*$ | −2.92 | −2.94 | 

Every exponent is negative: every start, at every wind and brake, ends on the same regular, periodic swing. More than that, each exponent is the decay rate of a small disturbance of the braked centrifugal spring alone, to within 1.2 %: the motion forgets its start as fast as a linear, damped spring forgets a nudge. Halving the step changes the exponents by at most 0.7 % of their size. The physical reason is the centrifugal spring: at $R = 94.5$ it is 3.3 to 9.2 times stronger than gravity's push, so whatever the start, the second blade is pulled back to the mother blade's line and swings there in step with the push; chaos needs a spring and a push of similar strength, near resonance, and section 2.5 showed that a second blade never gets there.

[What to remember]

The braked second blade has two time scales: a jerk dies in about a hundredth of a second, a displaced swing creeps back in about a second. That makes its equation stiff, and an implicit solver handles it.

The full equation agrees with the small-swing power (2.5) to a third of a per cent.

On average the second blade trails slightly behind the mother blade. Its outward pull then holds the rotor back, and that torque times $\Omega$ is exactly the harvested power: the trail is the bill.

Mass far from the hinge is worth more: the same mass as a lump at the end gives twice what a uniform rod gives.

The motion is regular, never chaotic, at every wind and brake tried: the centrifugal spring holds the second blade too firmly.

[Problems]

At 10 m/s, how long does a second blade pushed off its path take to creep back, at the best brake?

[folded: Answer]
$\kappa^*/(R\Omega)$, with $\Omega$ = 1.198 rad/s at 10 m/s: 0.83 s. It is shorter than at 8 m/s because the rotor turns faster; counted in turns, it is the same.

Use (3.3) and the full model's trail at 6 m/s, −0.0231 rad, to estimate the harvested power. Compare the full model's 267 mW.

[folded: Answer]
$\tfrac{ml}{2}r_p\Omega^3|\bar\theta|$ = 270 mW, about one per cent above. The exact identity uses $\langle\sin\theta\rangle$ over the full swing rather than the small-swing relation (3.3), and with it the agreement is exact.

Which way does the second blade's pull on the hinge turn the rotor when the second blade trails, and which way when it leads? Why can it, on average, only trail?

[folded: Answer]
Trailing, its pull holds the rotor back; leading, it would push the rotor on. A second blade that led on average would give the rotor energy while also feeding the generator, from nothing. So with a brake taking energy, energy conservation demands a trail.

A 1 kg lump on a massless 1 m rod is compared with a uniform 1 kg rod of 1 m. Which needs the stronger generator, and by how much?

[folded: Answer]
The lump: its first moment, $mL$ = 1 kg m, is twice the rod's, $ml/2$ = 0.5 kg m, and the generator's torque at the best brake, (first moment)$\cdot g/\sqrt2$, is proportional to it: twice as large.




Part IIRandomness: shaking, gusts and a bending blade

## 4 A ceiling on random shaking

So far the second blade was driven by one clean push, gravity once per turn. But wind is gusty, and a blade in gusty wind shakes. Physicists have proposed that oscillators which move irregularly, even chaotically, catch more of a random shaking than a calm one does (Cottone, Vocca and Gammaitoni 2009). Could our second blade, perhaps tumbling chaotically, turn the wind's randomness into extra power? Before any model of the wind, one exact result sets a ceiling. To keep it clean, this chapter takes a body, or a chain of bodies, hinged to a point that is shaken at random while it hangs in gravity, with no rotor; the last section says what carries over to the turning blade.

## 4.1 Random kicks add energy through their square

Stand in a bus on a rough road with a full cup of coffee. Every jolt kicks the coffee, sometimes with its slosh and sometimes against it. On average the "with" and the "against" cancel, and yet the coffee sloshes harder the rougher the road. A kick adds kinetic energy even when it is equally likely to help or oppose the motion, because kinetic energy goes as the square of the velocity.

Start with the simplest case: a small mass $m$ that can move only along one direction $\hat t$, across its rod. Shake its pivot to and fro along a direction $\hat e$. In the pivot's frame each jolt is a sudden extra force on the mass, which changes its velocity along $\hat t$ by a small random amount $\Delta v$. Its kinetic energy $\tfrac12mv^2$ changes by $mv\,\Delta v + \tfrac12m\,\Delta v^2$. The first term is as often negative as positive and averages to zero. The second is never negative. Call the shaking's strength $S$, in m²/s³: the spread (the variance) of the velocity kicks it gives per second. The kicks along $\hat t$ then have the variance $S(\hat e\cdot\hat t)^2$ per second, and the shaking feeds in, on average, the power $\tfrac12Sm(\hat e\cdot\hat t)^2$. That is the whole idea. The next paragraphs prove it for any body or chain of bodies, with Lagrange's equations; a reader who skips them loses only the proof, and can go on to the result (4.2) and its plain-words form after (4.4).

Shake the pivot along a fixed direction $\hat e$ with the acceleration $\ddot u(t)$. In the pivot's frame every piece of mass $dm$ feels the extra force $-\ddot u(t)\,\hat e\,dm$. For a body or chain with the angles $q_k$, that force enters Lagrange's equations as the generalised force
$$Q_k = -\ddot u(t)\,b_k(q), \qquad b_k = \int \hat e\cdot\frac{\partial \mathbf x}{\partial q_k}\,dm = \frac{\partial}{\partial q_k}\left(M\,\hat e\cdot\mathbf x_{\rm cm}\right), \tag{4.1}$$

the rate at which turning the angle $q_k$ moves the whole mass $M$ along the shaking, through its centre of mass $\mathbf x_{\rm cm}$. Let the shaking be white noise of strength $S$: kicks so quick and so unrelated that $\langle\ddot u(t)\ddot u(t')\rangle = S\,\delta(t - t')$, where $\delta(\cdot)$ is the Dirac delta function (not the lag $\delta$ of chapter 2); it says that the shaking at two different instants is unrelated, however close the instants are. Over a short time $dt$ the momenta $p_k = \partial\mathcal L/\partial\dot q_k$ receive the random kick $\Delta p = -b\,\sqrt{S}\,dW$, where $dW$ is a random number of mean zero and variance $dt$. Why $\sqrt{dt}$? Within $dt$ there are many independent tiny kicks, and, like the steps of a random walk, their sum grows as the square root of their number, so as $\sqrt{dt}$, and its square is of order $dt$. That is why the square of the kick, which would be negligible for a smooth force, survives here. The kinetic energy is $K = \tfrac12\dot q^{\mathsf T}\mathsf M\,\dot q = \tfrac12p^{\mathsf T}\mathsf M^{-1}p$, with $\mathsf M(q)$ the mass matrix (for one rigid body on its pivot, simply its moment of inertia). To second order in the kick,
$$\Delta K = \dot q\cdot\Delta p + \tfrac12\,\Delta p^{\mathsf T}\mathsf M^{-1}\Delta p.$$

The first term averages to zero: the kick is as likely to help as to oppose. The second does not: its average is $\tfrac12S\,b^{\mathsf T}\mathsf M^{-1}b\,dt$. So on average the shaking feeds in the power
$$\boxed{P_{\rm in} = \frac S2\,\big\langle m_{\rm eff}\big\rangle, \qquad m_{\rm eff} = b^{\mathsf T}\mathsf M^{-1}b.} \tag{4.2}$$

Nothing else entered: not the stiffness, not the damping, not gravity, not whether the motion is regular or chaotic. In a steady state everything fed in is dissipated, and the generator is where it is dissipated. (Random kicks have one subtlety, known as the Itô–Stratonovich question: the result can depend on whether a kick's strength is evaluated at the start or in the middle of each step. That matters only when the kick's strength depends on the velocity it kicks; here $b$ depends only on the angles, so the two readings agree.)

## 4.2 The effective mass never exceeds the real mass

$m_{\rm eff}$ measures how much of the body's mass the shaking can grab. For one body on its pivot it is $b^2/I_p$. For a small bob it is $m(\hat e\cdot\hat t)^2$: the full mass when the bob can move along the shaking, none when its rod points along it. For our uniform second blade, $b = \tfrac{ml}{2}\cos\psi$, where $\psi$ is the angle between the shaking and the direction in which the blade's pieces move, and
$$m_{\rm eff} = \frac{\left(\tfrac{ml}{2}\right)^2\cos^2\psi}{ml^2/3} = \tfrac34\,m\cos^2\psi \le \tfrac34\,m.$$

The shaking can grab at most three quarters of a uniform rod's mass: the pieces near the hinge hardly move, so they take their share of the kinetic energy without catching their share of the kicks. The general proof takes three lines. For any velocities $\dot q$, the pieces move with velocities $\mathbf v$, the kinetic energy is $\tfrac12\dot q^{\mathsf T}\mathsf M\dot q = \tfrac12\int|\mathbf v|^2dm$, and $b\cdot\dot q = \int\hat e\cdot\mathbf v\,dm$. Then
$$m_{\rm eff} = \max_{\dot q}\frac{(b\cdot\dot q)^2}{\dot q^{\mathsf T}\mathsf M\dot q} = \max\frac{\left(\int\hat e\cdot\mathbf v\,dm\right)^2}{\int|\mathbf v|^2dm} \le \frac{\left(\int dm\right)\left(\int(\hat e\cdot\mathbf v)^2dm\right)}{\int|\mathbf v|^2dm} \le M_{\rm total}. \tag{4.3}$$

The first step is the Cauchy–Schwarz inequality for the product $u^{\mathsf T}\mathsf Mv$: $(b\cdot\dot q)^2 \le (b^{\mathsf T}\mathsf M^{-1}b)(\dot q^{\mathsf T}\mathsf M\dot q)$, with equality at $\dot q = \mathsf M^{-1}b$. The second is Cauchy–Schwarz again, and the third holds because $(\hat e\cdot\mathbf v)^2 \le |\mathbf v|^2$. Equality would need every piece to move along $\hat e$ with the same velocity, carrying all the mass along the shaking at once, which a body turning on a hinge never can. So
$$P_{\rm in} \le \frac S2\,M_{\rm total}, \qquad\text{and for the second blade}\quad P_{\rm in} \le \frac S2\cdot\frac34\,m. \tag{4.4}$$

In plain words: random shaking cannot feed in more than $S/2$ times the body's mass, whatever the body does, regular or chaotic, and a rod on a hinge takes at most three quarters of that.

[How hard would it have to shake?]
For the 1 kg second blade to take as much from white-noise shaking as from gravity at 8 m/s, 201 mW, (4.4) needs $S$ = 0.54 m²/s³ at least. Spread evenly over every frequency from 0 to 10 Hz, that is a shaking of 3.3 m/s² rms (the root of the mean square), about a third of gravity, all the time. The blade's own shaking is nothing like that, as chapter 6 shows.

[Check]
A computer test of the general theorem on two simpler bodies: a bob of 0.1 kg on 0.2 m, and a double pendulum of the same mass and reach, hang in gravity, braked with a damping ratio of 0.2 (a fifth of the brake that just stops ringing), while their pivot is shaken sideways with white noise of strength $S = 0.028$ m²/s³ (gentle: swings of 0.05 rad) or $S = 48$ m²/s³ (violent: swings of more than a radian, the double pendulum's top rod tumbling right over about a hundred times in each 40-second window). For each case 1000 independent runs compare the generator's power with $\tfrac S2\langle m_{\rm eff}\rangle$: they agree within 0.22 to 0.65 %, at statistical errors of 0.4 to 0.7 %. In the violent runs $\langle m_{\rm eff}\rangle$ falls to 0.48 of the total mass for the bob and 0.55 for the tumbling double pendulum: chaos took less, not more. The rod's value $\tfrac34m\cos^2\psi$ is checked in SymPy.

On the turning blade, gravity's once-per-turn push, paid for by the rotor, also drives the second blade. The noise's own feed is still (4.2), whatever else drives the motion, because its first-order term averages to zero in any state. But the noise also changes the motion, and with it what gravity's push feeds in; (4.4) bounds the noise's own feed, not that indirect change. A blade bends two ways. Flapwise it bends out of the rotor's plane, along the wind; that moves the hinge along its own axle and cannot turn the second blade at all. Edgewise it bends in the rotor's plane, across the blade; that moves the hinge across a second blade lying along the mother blade, so the second blade starts with its full effective mass, $\tfrac34m$, and any wandering can only lower it. A real blade, though, does not shake as white noise: it shakes mostly near its own edgewise frequency, about 1.08 Hz for the 5 MW turbine's blade (1.0793 Hz in Jonkman et al. 2009, Table 9-1). Then what matters is how the second blade responds near that one frequency, and shaking at one frequency acts like a push, as gravity's does. Chapter 6 works it out.

[What to remember]

A random kick adds energy through its square, even when it is as likely to help as to oppose.

White-noise shaking of strength $S$ feeds in $\tfrac S2$ times an effective mass, never more than the real mass, $\tfrac34m$ for a rod on a hinge, whatever the motion: chaos cannot beat the ceiling.

To match gravity's harvest, the blade tip would have to shake far harder than a blade does.

## 5 Gusts and the rotor's speed

So far the rotor turned at a steady speed. In gusty wind it does not: a gust speeds it up over some seconds, a lull slows it down. This chapter asks what that does to the second blade. It needs three things: how the rotor's speed answers the wind, a realistic gusty wind, and how the second blade's power depends on the rotor's speed.

A heavy flywheel turned by a hand that pushes unevenly turns almost evenly: the flywheel smooths the pushes. The turbine's rotor is such a flywheel. At 8 m/s it carries, as kinetic energy, about 11 s of its own output, so a gust lasting a second barely changes its speed; only changes that last tens of seconds do.

How the rotor answers. The 5 MW turbine's rotor and main generator together have a moment of inertia $J_{\rm rot} = 4.38\times10^7$ kg m², and the rotor's speed obeys Newton's law for turning, $J_{\rm rot}\dot\Omega = Q_{\rm aero} - Q_{\rm gen}(\Omega)$: the wind's torque against the main generator's. The wind's torque is its power over the angular speed, $Q_{\rm aero} = P/\Omega = \tfrac12\rho\pi r_{\rm rot}^2v^3C_p(\lambda)/\Omega$, and with $\Omega = \lambda v/r_{\rm rot}$ this is $\tfrac12\rho\pi r_{\rm rot}^3v^2C_p(\lambda)/\lambda$, with $C_p(\lambda)$ from NREL's published table. The main generator's torque is set by the control computer from the rotor's speed alone, by a rule called the torque law. Its main part is a square law, $Q_{\rm gen} = k\,\Omega^2$. Why a square? At the best tip-speed ratio the wind's torque is proportional to $v^2$, and so to $\Omega^2$; a square law with the right $k$ balances it at $\lambda^*$ in every wind, so the rotor settles at its best speed by itself. Below 8.98 rpm the law has a kink: there the torque ramps down in a straight line to zero at 6.9 rpm, so that the turbine starts and stops gently. At a steady 8 m/s the two torques balance at 9.07 rpm, 1.0 % below the $\lambda^*v/r_{\rm rot}$ of section 0.3, because that ramp holds the rotor a little off its best ratio.

A gusty wind. Turbines are designed against a standard description of gusty wind, set out in the international standard IEC 61400-1. Its strongest class of turbulence, class A, makes the wind's speed at 8 m/s fluctuate with a standard deviation of 1.86 m/s, 23 % of the mean. How that fluctuation spreads over slow and fast changes is given by the Kaimal spectrum, a formula fitted to measured winds: most of it lies in changes lasting tens of seconds to minutes, and less and less in quicker wiggles. Two points of the rotor's disc a few tens of metres apart wander together only in the slow changes, so the wind averaged over the disc, which is what turns the rotor, is smoother than the wind at any one point. NREL's program TurbSim generates such winds; these notes use 40 generated ten-minute records at a mean of 8 m/s, not measurements. In them the rotor's speed wanders about its mean with a standard deviation of 10.3 % of the mean. Only 8 m/s was simulated.

What the second blade feels. The gusts reach the second blade in two ways. While the rotor speeds up or slows down, the Euler torque of (1.5) acts; it changes the power by about 2 parts in 10 000, nothing. More important, the rotor's speed itself changes. The second blade settles to a new speed in about a second (section 3.1), while the rotor's speed changes over tens of seconds, so at every moment the second blade swings as it would at that moment's speed in a steady wind. With the hinge generator's constant $c$ fixed, (2.3) at the speed $\Omega$, divided by its value at the speed $\Omega_0$ for which $c$ is the best brake, is
$$\frac{\bar P(\Omega)}{\bar P(\Omega_0)} = \frac{2}{1 + \Omega^2/\Omega_0^2}.$$

(In rotor turns, $R$ stays the same at every speed, but $\kappa = c/(I\Omega)$ and $G$ change with $\Omega$; this formula carries both.) Its slope at $\Omega_0$ is $-1$: a shift of the mean speed by a fraction $\epsilon$ changes the power by $-\epsilon$. And it curves upwards there (its second derivative in $\Omega/\Omega_0$ is $+1$), so a speed that wanders about a fixed mean raises the average power, whichever way it wanders: by about $s^2/2$ for a relative spread $s$, 0.53 % here.

[On our blade]
The full equation of the second blade was run through each of the 40 records, with the rotor's speed taken from the turbine's own equation, and compared with steady rotation. Two main-generator rules were tried. With a pure square law ($Q_{\rm gen} \propto \Omega^2$, no kink) the second blade's power changes by +0.77 % against steady operation at 8 m/s: the wandering speed adds +0.90 %, a little more than the 0.53 % the curvature alone predicts (we have not traced the rest), and the mean speed moves by +0.11 % and changes the power by −0.11 %, as the slope of $-1$ predicts. With the turbine's real torque law, kink included, the total turns to −1.99 %. At 8 m/s the rotor runs just above the kink. In a lull it drops onto the ramp, where the main generator brakes much less, so it slows less than it speeds up in a gust; its mean speed rises by +2.60 %, which changes the power by −2.55 %, again as the slope predicts, while the wander still adds +0.53 %. That is a property of this turbine's control, not of the wind. Either way, gusts change the second blade's power by a few per cent.

[What to remember]

The rotor is a flywheel: gusts make its speed wander slowly, by about a tenth.

The second blade follows the rotor's speed from moment to moment. A wander about a fixed mean adds a little; a shift of the mean speed by a fraction $\epsilon$ costs $\epsilon$ of the power.

Net effect at 8 m/s: a few per cent, its sign set by the main generator's torque law.

## 6 The blade bends and shakes

A real blade is not rigid. It bends under its own weight, once per turn, and it shakes in gusty wind near its own edgewise frequency. Both move the hinge, and at the tip they move it most.

## 6.1 The sag: a large push that cancels itself

Hold a long, springy ruler out sideways and turn your wrist slowly: the ruler sags first one way and then the other, following gravity, and its end sags most. A blade 61.5 m long does the same as it turns, in its own plane.

The blade's mass and stiffness, metre by metre, are published (the OpenFAST blade file of the 5 MW turbine). From them, gravity bends the blade edgewise so that its tip moves to and fro by $w$ = 431 to 467 mm either side of its straight position, once per turn and in step with gravity's push; the range comes from two ways of taking the shape of the bend, from the blade's first mode of vibration or by integrating the bending directly. The hinge, at the tip, therefore moves across the mother blade by $w\cos\varphi$.

That motion adds to gravity's push in two ways, each worth $\Omega^2 w$ per kilogram. First, seen from the turning mother blade, the hinge accelerates to and fro by $-\Omega^2w\cos\varphi$, which in the hinge's frame is an apparent push of $+\Omega^2w\cos\varphi$, in step with gravity's. Second, a hinge moved sideways by $w\cos\varphi$ sits at a slightly different angle seen from the hub, $w\cos\varphi/r_p$, so the outward pull, which points away from the hub, turns by that angle, and its part across the mother blade grows by $\Omega^2r_p\cdot w\cos\varphi/r_p = \Omega^2w\cos\varphi$. Together, gravity's push $g$ becomes $g + 2\Omega^2w$. (Linearising the Lagrangian with a moving hinge, in SymPy, gives the same.) On its own that would raise the power, which goes as the push squared (2.5), by 16.9 to 18.4 % at 8 m/s.

But a bending blade also turns: each cross-section tilts with the slope of the bend, and at the tip the slope is largest. The generator's stator, fixed in the mother blade, tilts with it by an angle $\beta$. The generator brakes the second blade's motion relative to the stator, $-c(\dot\theta - \dot\beta)$, so the tilting stator drags the second blade with the extra torque $c\dot\beta$. That drag follows the rate of change of the slope, a quarter turn out of step with the sag's push, while at the best brake the swing lags its push by 45° (section 2.3); so part of the drag works against the swing. The two effects largely cancel. What is left is a small difference of two large numbers, so it depends on the exact shape of the bend: a net change of +2.2 to +3.5 % for the two shapes. (For the first shape, linear theory and a full nonlinear run with the moving, tilting hinge agree within 0.2 percentage points.) The lesson: a generator brakes motion relative to its own frame, so when that frame moves, the frame's motion counts too.

## 6.2 Random shaking

Gusts make the blade's first edgewise mode vibrate near 1.08 Hz. How far the tip of this blade vibrates edgewise in ordinary operation, we found no published value. So the notes take a range of tip vibrations, 5, 20 and 100 mm rms, and say what each would give; the answer rests on that unknown.

The model has two parts, coupled both ways. The blade's first edgewise mode is one oscillator: a modal mass, the mass that, sitting at the tip on a spring, would vibrate like the whole blade in that mode (1416 kg, computed from the blade's mass table and the mode's shape), on a spring tuned to 1.08 Hz, with a damping ratio $\zeta_b$ of 0.5 % or 3 % of critical, two assumed values. It is driven by a random force whose spectrum is flat near 1.08 Hz, scaled so that the blade alone would vibrate at the stated tip level. At the tip the hinge moves sideways with the tip, and the section tilts by 28.1 mrad per metre of tip motion. The second blade is (2.1) with its hinge shaken sideways and its stator tilted by that much, and it pushes back on the blade's mode with the force and torque it needs. Gravity's push is left out of this part (it is in chapter 2 and section 6.1). Everything is linear, so the response is computed frequency by frequency, and the generator's mean power is the brake times the mean square of the relative speed. (The full linear equations, with the second blade integrated along its length and the turning frame's centrifugal and Coriolis terms, were derived in SymPy.) The model checks that the second blade never takes more than the gusts feed into the blade.

[On our blade]
At a 5 mm tip vibration the gusts feed 0.110 W into the blade's vibration, and the 1 m second blade, at its best brake for the shaking, 1.89 N m s, takes 3.38 mW of it. At 20 mm it takes 54.2 mW; at 100 mm, 1 350 mW, more than gravity gives. For comparison, gravity gives 202 mW at its own best brake, 29.6 N m s. Since the model is linear, the swings from shaking and from gravity add; but the two best brakes differ by a factor of fifteen, so the two best powers cannot simply be added. At the shaking's best brake the second blade's damping ratio is only 0.3: here, unlike under gravity's push, it really does ring. The motion is regular (section 3.4).

The 1 m second blade takes so little at small vibrations because its own frequency, $\sqrt R$ times the rotor's, is 1.36 times the blade's: it is far from the blade's resonance. A second blade tuned to the blade, its own frequency $\Omega\sqrt{3r_p/(2l)}$ equal to the blade's $\omega_e = 2\pi\times1.08$ Hz at the mean rotor speed, needs a length of 1.85 m; with the same mass per metre it weighs 1.85 kg. It would then be a tuned mass damper, the device that calms swaying skyscrapers, and it would draw on the blade's vibration directly: at 5 mm and 0.5 % blade damping, the linear model gives it 64.6 mW. But gravity's term $-G\theta\sin\varphi$ (section 2.1) stiffens and softens it once per turn, shifting its frequency by $\pm1/(2\Gamma) = \pm$8.6 % at 8 m/s, while the blade's resonance is only 1 to 6 % wide; the rotor's wandering speed detunes it too. So it is detuned and retuned every turn, and whether any of that gain survives is an open question that only a calculation in time, with gravity kept whole, can answer.

[What to remember]

The blade's sag moves and tilts the hinge once per turn. The two effects largely cancel: a few per cent net.

A generator brakes motion relative to its own frame; when the frame moves, that counts.

The blade's random vibration adds power as the square of the tip's vibration: negligible at 5 mm, more than gravity at 100 mm. The real level for this blade is not known, so this stays open.





## 7 From swing to watts

Every chapter so far has treated the generator as a perfect brake: a torque $-c\dot\theta$ that takes the power $c\dot\theta^2$ and loses none of it. A real one is a small electric motor driven backwards, behind a gearbox. This chapter takes one from a catalogue, puts it in the hinge, follows the power from the swinging second blade to the wires of the sensor, and then sizes the second blade to suit it.

## 7.1 A generator is a brake

A bicycle dynamo pressed against the tyre makes the wheel harder to turn when the lamp is lit, and harder still if you join its two wires together; with the wires loose it spins almost freely. What pushes back on the wheel is the electric current.

A small motor with permanent magnets has two constants. Turning its shaft at the angular speed $\omega_m$ induces the voltage $e = k_e\,\omega_m$ in its coil, by Faraday's law; this voltage is called the back-EMF (electromotive force), because in a motor it pushes back against the supply. A current $i$ in the coil gives a torque $k_t i$ on the shaft. The two constants are equal in SI units, because the electrical power $ei$ and the mechanical power $k_ti\,\omega_m$ are the same power. Connect a load resistor $R_L$: the current is $i = e/(R_c + R_L)$, where $R_c$ is the resistance of the coil itself. The torque on the shaft is then $k_tk_e\,\omega_m/(R_c + R_L)$, proportional to the speed: exactly the brake of chapter 1. (The coil's inductance would delay the current by $L_c/R_c = 0.12$ ms, nothing next to a swing that lasts seconds, and is left out.)

Between the second blade and the motor sits a gearbox of ratio $N$: the motor turns $N$ times for each turn of the hinge, $\omega_m = N\dot\theta$, and its torque reaches the second blade multiplied by $N$. The ratio therefore enters twice, once in the voltage and once in the torque, and the brake constant at the hinge is
$$c_e = \frac{N^2\,k_t\,k_e}{R_c + R_L}. \tag{7.1}$$

The power $c_e\dot\theta^2$ is the electrical power $ei$, and the current shares it between the coil and the load in proportion to their resistances. The load gets the fraction $R_L/(R_c + R_L)$. Call $c_{\rm sc} = N^2k_tk_e/R_c$ the brake with the wires joined ($R_L = 0$, the "short circuit"): it is the strongest brake this motor can give through this gearbox. Since $R_L/(R_c+R_L) = 1 - c_e/c_{\rm sc}$,
$$P_{\rm load} = c_e\left(1 - \frac{c_e}{c_{\rm sc}}\right)\langle\dot\theta^2\rangle. \tag{7.2}$$

This is section 2.3's contest once more, now inside the generator: a brake near the short circuit takes plenty of power but burns it in its own coil; a light brake sends nearly all of it to the load but takes little.

[On our blade]
Take the maxon RE 25, a motor 25 mm across, rated 20 W, in its 24 V winding: $R_c = 1.53$ Ω, $k_t = 20.8$ mN m/A, and a speed constant of 460 rpm/V, which is $k_e = 60/(2\pi\cdot460) = 0.02076$ V s; the two constants agree to the catalogue's rounding, two parts in a thousand. Without a gearbox its strongest brake is $c_{\rm sc} = k_tk_e/R_c = 0.000282$ N m s. The best brake of chapter 2, (2.6), is 22.4 to 37.4 N m s: some 79 000 to 130 000 times more. Because the brake grows as $N^2$, a ratio of at least 282 to 364 is needed just to reach the best brake with the wires joined. The reason is the shape of the job. At the best brake the second blade pushes with 3.47 N m (section 2.3) while its hinge turns at only 0.09 to 0.15 rad/s at its fastest; a small motor is built to give a hundredth of that torque (the RE 25's rated torque is 30.4 mN m) at thousands of rpm. The gearbox converts one into the other.

## 7.2 What the gearbox costs

Turn the crank of a hand-held egg beater. The beaters are light, yet the crank feels heavy when you start and stop it, because each turn of the crank spins the beaters four times. Seen from the slow side, everything on the fast side of a gearbox is magnified: a torque by $N$, and an inertia by $N^2$.

The gearbox that makes the brake strong enough brings three costs.

Inertia. The motor's rotor, of moment of inertia $J$, turns at $N\dot\theta$, so its kinetic energy is $\tfrac12JN^2\dot\theta^2$: to the second blade it is an extra moment of inertia $JN^2$ about the hinge. In the units of chapter 1, where the second blade's own is $I$, it adds
$$j = \frac{J\,N^2}{I}. \tag{7.3}$$

It does not feel the centrifugal pull or gravity, because the motor's rotor sits on the hinge's axis; it only resists being accelerated. In (2.2) the second blade's inertia gave the $-1$ of the net stiffness $R - 1$; the rotor adds its own, and the net stiffness becomes $R - 1 - j$.

Friction. Brushes and bearings resist turning with a torque $T_0$ that hardly depends on speed. Through the gearbox it reaches the second blade as $NT_0$.

Gear losses. A gearhead's efficiency $\eta$ is the fraction of the power it passes on, whichever way the power flows. While the second blade drives the motor, every torque the motor side needs costs the second blade $N/\eta$ times that torque, not $N$ times; while the motor's spinning rotor slows down and gives its energy back, the second blade receives only $\eta$ of it. In the formula below we keep the simple part: the brake the second blade feels is $c_e/\eta$ and the friction $NT_0/\eta$, and the rotor's inertia passes without loss. The full equation of section 7.4 charges the loss on every flow.

Put the three into (1.6): the rotor's inertia joins $\theta''$, the brake becomes $\kappa_e/\eta$, and the friction is a torque of constant size $f$ that always opposes the swing:
$$(1 + j)\,\theta'' + \frac{\kappa_e}{\eta}\,\theta' + f\,\mathrm{sgn}\,\theta' + R\sin\theta + G\cos(\varphi + \theta) = 0, \qquad \kappa_e = \frac{c_e}{I\Omega},\quad f = \frac{N\,T_0}{\eta\,I\Omega^2}. \tag{7.4}$$

In these units gravity's largest torque, $\tfrac{ml}{2}g$, is $G$, so $f/G = NT_0/(\eta\,\tfrac{ml}{2}g)$ compares the friction with the push that drives the swing, and it is the same at every wind. If $f \ge G$ the friction is stronger than gravity can ever push, and a second blade at rest never moves: the gearbox has jammed it.

[On our blade]
The RE 25's rotor has $J = 14.7$ g cm², and the GP 32 C gearhead adds 0.7 to 1.5 g cm² at its input. (A planetary gearhead is a compact gearbox in which small gear wheels, the planets, run round a central one, the sun, inside a ring; several such stages in a row multiply their ratios.) Through the largest catalogue ratio, 492 : 1, that gives $j = 1.12$: against a net stiffness $R - 1 = 93.5$, nothing. The catalogue gives no friction torque; the no-load current, 40.2 mA, gives an estimate $T_0 \approx k_ti_0 = 0.84$ mN m, measured at 10 900 rpm. The gearhead's catalogue efficiency is 80 % for one stage, 75 % for two, 70 % for three and 60 % for four. Through 492 : 1 (four stages) the friction at the hinge is 0.686 N m, 14 % of gravity's largest torque $\tfrac{ml}{2}g = 4.90$ N m. At the catalogue's friction the second blade would jam only beyond a ratio of 4 105 on a three-stage gearhead and 3 518 on a four-stage one: no catalogue ratio jams it.

Two of these numbers are less certain than the rest. The catalogue gives the gearhead's best forward efficiency, driven from the motor at its best load; driven backwards and lightly loaded, a gearhead can do worse. And friction measured at 10 900 rpm includes losses that grow with speed, so at the slow speeds here it may be lower. The first makes the numbers below optimistic, the second pessimistic. Only a test on a bench can settle them.

## 7.3 Friction as a brake that weakens

Push a heavy box across the floor. The floor pushes back with the same force whether you walk or run, so it takes the same toll for every metre. A brake like the dynamo is different: it pushes back harder the faster you go.

Equation (7.4) is no longer linear, because of $\mathrm{sgn}\,\theta'$, but chapter 2's method still works with one more step. Suppose the second blade still swings as $\theta = -\Theta\cos(\varphi - \delta)$. The friction torque $f\,\mathrm{sgn}\,\theta'$ is then a square wave, $+f$ while the blade moves one way and $-f$ while it moves back, in step with $\theta'$. A square wave of height $f$ is a sum of sine waves at frequencies 1, 3, 5, …, the first of amplitude $4f/\pi$ and the others of $1/3$, $1/5$, … of it. Keep only the first, the one at the frequency of the swing. A damper $\kappa_f\theta'$ gives a torque of amplitude $\kappa_f\Theta$ in step with $\theta'$, so the friction acts like a damper with
$$\kappa_f = \frac{4f}{\pi\,\Theta}. \tag{7.5}$$

This is called the describing function of friction. It is a brake that weakens as the swing grows, since the toll per swing is fixed but the swing is longer. In (2.2), replace $R - 1$ by $R - 1 - j$ and $\kappa$ by $\kappa_e/\eta + \kappa_f$, and multiply through by $\Theta$:
$$\Theta^2(R - 1 - j)^2 + \left(\frac{\kappa_e}{\eta}\,\Theta + \frac{4f}{\pi}\right)^2 = G^2. \tag{7.6}$$

This is a quadratic equation for $\Theta$. It has a positive root only if $4f/\pi < G$, a slightly stricter form of the jamming condition above. The power the load receives is (7.2) with $\langle\dot\theta^2\rangle = \Omega^2\Theta^2/2$, and the rotor pays for everything the second blade loses, in the coil, the load, the gears and the friction:
$$P_{\rm load} = I\Omega^3\,\kappa_e\left(1 - \frac{c_e}{c_{\rm sc}}\right)\frac{\Theta^2}{2}, \qquad P_{\rm rotor} = I\Omega^3\left[\frac{\kappa_e}{\eta}\,\frac{\Theta^2}{2} + \frac{2}{\pi}\,f\,\Theta\right]. \tag{7.7}$$

The last term is the friction's toll: torque times the mean speed $\langle|\theta'|\rangle = 2\Theta/\pi$.

[Check]
Remove the losses: $f = 0$, $j = 0$, $\eta = 1$ and $c_{\rm sc}\to\infty$ (a coil without resistance). Then (7.6) is (2.2), and both powers in (7.7) become (2.3). Units: $\kappa_e$, $j$, $f$ and $G$ are pure numbers, and $I\Omega^3$ is a power.

## 7.4 On our blade

Formulas (7.6) and (7.7) give, at each wind and each catalogue ratio of the GP 32 C, the load resistor that gives the load the most power, with the peak torque at the hinge within the torque the gearhead may carry continuously (6 N m for the largest ratios) and the swing below 0.5 rad, the range in which these notes use the formula (the best settings swing at most 0.22 rad, so that limit never bites); ratios that jam are out. Then, as a second route, the full equation is solved with the method of section 3.1. It is (7.4) with the gear loss charged on every power that flows through the gearhead. Let $x$ be the torque the motor side needs, as felt through a perfect gear (in the units of (7.4), and without $\eta$ in the friction: $f_0 = NT_0/(I\Omega^2)$); the second blade feels $x/\eta$ while power flows into the motor side and $\eta x$ while it flows back:
$$\theta'' + R\sin\theta + G\cos(\varphi + \theta) + k\,x = 0, \qquad x = j\,\theta'' + f_0\,\mathrm{sgn}\,\theta' + \kappa_e\,\theta', \qquad k = \eta^{-\mathrm{sgn}(x\theta')}. \tag{7.8}$$

Because $\theta''$ appears on both sides, each step solves for it (the left side grows steadily with $\theta''$, so there is exactly one answer). Each sign is smoothed over a narrow band: a thousandth of the swing for $\mathrm{sgn}\,\theta'$, and a thousandth of the gear's own power scale for $\mathrm{sgn}(x\theta')$. The full equation is run at the formula's brake and at half and twice it, at every wind, and at 8 m/s with every other ratio at its own best brake; the rotor's work is integrated too, so the energy book closes in the full equation as well.

[On our blade]

Table 3. The maxon RE 25 with a GP 32 C gearhead in the hinge, at the ratio (492 : 1 at every wind) and load the formula (7.6)–(7.7) finds best. Swing and load are given as formula / full: the describing-function formula, and the full equation (7.8). Paid: what the rotor pays; the last two columns are the shares of it that reach the load and that friction takes.wind | $R_L$, Ω | swing, rad | load, mW | paid, mW | load | friction | 

6 m/s | 9.24 | 0.220 / 0.221 | 104.2 / 106.1 | 271.3 | 39 % | 14 % | 

8 m/s | 7.03 | 0.127 / 0.124 | 74.0 / 75.5 | 203.3 | 37 % | 15 % | 

10 m/s | 5.73 | 0.083 / 0.080 | 56.1 / 57.2 | 161.9 | 35 % | 15 % | 

The load receives 57 to 106 mW: 36 to 40 % of what the perfect brake of chapter 2 would take, and 35 to 39 % of what the rotor pays. The motor's friction takes 14 to 15 % of what the rotor pays; the gears and the coil take most of the rest. The largest ratio, 492, wins at every wind: a smaller one cannot brake hard enough without burning most of the power in the coil. Even so the motor brakes only 0.39 to 0.43 of the best brake (2.6), which is why the second blade swings wider than in chapter 2 and gives less. Even the strongest wind, which gives the least, gives more than 1 500 times what the minimal sensor of section 0.5 needs. The full equation agrees with the formula within 2.1 %, and of the three brakes tried, the formula's is the best.

Follow the power down the chain, from the rotor to the load: of what the rotor pays, the motor's friction takes 14 to 15 %, the gears and the coil's resistance most of the rest, and 35 to 39 % reaches the load.

How much do the two uncertain numbers of section 7.2 matter? By the formula: if the gearhead's own drag doubles the friction, the load gets 41 to 75 mW; if the backdriven efficiency is 50 % instead of the catalogue's 60 %, 46 to 84 mW; with both, 30 to 57 mW, still 811 times the sensor's need.

One more thing the sensor's designer must know: the voltage. The load sees an alternating voltage that peaks at 0.80 to 1.39 V and alternates once per turn, at 0.114 to 0.191 Hz, with the motor turning at most 743 rpm, far below the gearhead's limit of 8000 rpm. Turning that into the steady few volts a radio chip needs is a problem of electronics that these notes do not solve. The motor's graphite brushes also have a voltage drop of their own where they touch the turning commutator; the catalogue does not give it, and at peaks of about a volt it could matter, so it too waits for a bench test. The margins above are therefore before the electronics, and a bench test of the whole chain is the next step.

## 7.5 Sizing the second blade to its generator

Chapter 2 says the power grows with the second blade's first moment, and (2.6) says the best brake grows with it too: $c^* \approx \tfrac{ml}{2}r_p\Omega$. A given generator can brake only so hard, so for a given generator there is a second blade it serves best. Too light a second blade asks for a brake the motor gives easily, but takes little; too heavy a one asks for more brake than the motor can give, or more torque than its gearhead may carry, and the motor takes only a small share of what the second blade could give.

[On our blade]
With the length fixed at 1 m, the formula of section 7.3, at each mass of the series 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5 and 10 kg and at each wind, with the best ratio and load within the gearhead's rating, gives the load these shares of $P^*$ (mean over the three winds):

Table 4. The share of the best power $P^*$ the RE 25 + GP 32 C delivers to its load, against the mass of a 1 m second blade; mean over the three winds, and the ratio and load power at 8 m/s.mass (kg) | share of $P^*$ | ratio at 8 m/s | load at 8 m/s (mW) | 

0.01 | 7.1 % | 14 | 0.14 | 

0.02 | 13.6 % | 33 | 0.54 | 

0.05 | 16.8 % | 51 | 1.66 | 

0.1 | 25.3 % | 111 | 5.07 | 

0.2 | 31.5 % | 190 | 12.65 | 

0.5 | 30.6 % | 492 | 29.96 | 

1 | 36.8 % | 492 | 73.96 | 

2 | 33.3 % | 492 | 133.33 | 

5 | 5.9 % | 246 | 56.84 | 

10 | 3.0 % | 246 | 57.34 | 

The share of $P^*$ that reaches the load peaks at 1 kg, which is the mass these notes use: the lightest second blade whose best brake this motor can reach. Beyond 2 kg the largest ratio would exceed the gearhead's continuous torque, and the share collapses. With twice the catalogue's friction and a gear efficiency of 50 %, the 1 kg second blade still gives the sensor 811 times its need at the poorest wind.

## 7.6 Bigger second blades

Hang a ruler and a plank side by side from the rim of a turning wheel. Both lean back by the same few degrees, because gravity's push and the outward pull both grow with how much mass sits how far from the hinge. But to hold the plank against its swing you need a far stronger hand than for the ruler.

Our second blade is light for a blade tip. The NREL blade itself weighs 10.3 kg per metre at its very tip, and its outer 3 m weigh 115 kg. Real devices fitted at blade tips are of the same build: retrofit tip extensions reach about one metre past the old tip and are about three metres long in all (a Vestas patent, US 10 927 809, listed with the sources below), and the tip brakes of older turbines (section 0.5), on turbines that limit their power in strong wind by letting their blades stall rather than by turning them, are 5 to 20 % of the rotor radius long (US patent 8 403 641, also below). So it is worth asking what the formulas of chapters 2 and 7 give over that range. Table 5 runs them for lengths from half a metre to three metres and for four mass densities: a light hollow sensor blade (1 kg per metre), a light composite (3 kg per metre), the mother blade's own tip (10 kg per metre) and its build a metre further in (30 kg per metre).

[On our blade, and bigger ones]

Table 5. The second blade over the range of real tip devices: length $l$, mass per length, mass $m$, first moment $ml/2$; the best power $P^*$ (2.5) at 6 and 10 m/s; the generator torque $\tau^* = \tfrac{ml}{2}g/\sqrt2$ it must hold; the extra pull on the mother blade's tip at 10 m/s, $m\Omega^2(r_p + l/2)$; and what the RE 25 + GP 32 C delivers to its load at 6 m/s. The row in bold is the size these notes use.$l$, m | kg/m | $m$, kg | $ml/2$, kg m | $P^*$ 6 m/s, W | $P^*$ 10 m/s, W | $\tau^*$, N m | pull, kN | RE 25, mW | 

0.5 | 1 | 0.5 | 0.125 | 0.0667 | 0.0400 | 0.867 | 0.0454 | 23.5 | 

0.5 | 3 | 1.5 | 0.375 | 0.200 | 0.120 | 2.60 | 0.136 | 73.5 | 

0.5 | 10 | 5 | 1.25 | 0.667 | 0.400 | 8.67 | 0.454 | 93.9 | 

0.5 | 30 | 15 | 3.75 | 2.00 | 1.20 | 26.0 | 1.36 | 100 | 

1 | 1 | 1 | 0.5 | 0.268 | 0.161 | 3.47 | 0.0912 | 104 | 

1 | 3 | 3 | 1.5 | 0.805 | 0.483 | 10.4 | 0.274 | 96.9 | 

1 | 10 | 10 | 5 | 2.68 | 1.61 | 34.7 | 0.912 | 102 | 

1 | 30 | 30 | 15 | 8.05 | 4.83 | 104 | 2.74 | 102 | 

2 | 1 | 2 | 2 | 1.08 | 0.651 | 13.9 | 0.184 | 101 | 

2 | 3 | 6 | 6 | 3.25 | 1.95 | 41.6 | 0.551 | 104 | 

2 | 10 | 20 | 20 | 10.8 | 6.51 | 139 | 1.84 | 104 | 

2 | 30 | 60 | 60 | 32.5 | 19.5 | 416 | 5.51 | 104 | 

3 | 1 | 3 | 4.5 | 2.47 | 1.48 | 31.2 | 0.278 | 106 | 

3 | 3 | 9 | 13.5 | 7.40 | 4.44 | 93.6 | 0.834 | 107 | 

3 | 10 | 30 | 45 | 24.7 | 14.8 | 312 | 2.78 | 107 | 

3 | 30 | 90 | 135 | 74.0 | 44.4 | 936 | 8.34 | 107 | 

Three things follow. First, the best power grows in proportion to the first moment $ml/2$, as (2.7) says: at 6 m/s from 66.7 mW to 74.0 W over the table. Second, the swing does not change: $\Theta^*$ at 6 m/s stays between 0.214 and 0.220 rad for every size. The reason is in (2.2): at the best brake $\Theta^* = G/[\sqrt2(R-1)]$, and gravity's push $G$ and the centrifugal stiffness $R$ both carry the same factor $\tfrac{ml}{2}/I$, so their ratio is $g/(\Omega^2 r_p)$ for any second blade much shorter than its mother blade, which gives 0.213 rad. Third, the torque the generator must hold, $\tau^*$, grows with the first moment too, from 0.867 to 936 N m. The RE 25 behind its gearhead cannot follow: once the first moment passes about half a kilogram-metre, it delivers 93.9 to 107 mW at 6 m/s whatever the size, because the gearhead's continuous torque, not the second blade, sets the limit. A bigger second blade needs a bigger generator, sized by $\tau^*$ and $c^*$ as in section 7.5. The largest blades of the table also pull on the mother blade's tip with up to 8.34 kN at 10 m/s, close to the pull of its own outer 3 m, 10.1 kN; such a device would need a check of the blade's structure, which these notes do not make. Ours adds 91 N.

For the minimal sensor, every size in the table is more than enough: through the RE 25 the poorest case, the smallest blade in the strongest wind, still gives 311 times its need. So the size is not set by that sensor. These notes size the second blade for the most power from one small catalogue generator, because a sensor that does more can use it (section 0.5): 1 kg on 1 m is the lightest second blade that generator serves fully, and the lightest load on the mother blade's tip.

[What to remember]

A motor driven backwards is a brake: $c_e = N^2k_tk_e/(R_c + R_L)$. The load gets the share $R_L/(R_c + R_L)$ of what it brakes, so a stronger brake and a larger share pull against each other.

A gearbox turns a small, fast motor into a strong, slow brake. It costs inertia (negligible here), friction (a brake that weakens as the swing grows) and gear losses.

Through a catalogue motor and gearhead the load receives 57 to 106 mW, 35 to 39 % of what the rotor pays.

Bigger second blades give proportionally more, but need a generator that holds a proportionally larger torque.

[Problems]

Without a gearbox, the RE 25's strongest brake is 0.000282 N m s. What gear ratio does it need, at the least, to reach the best brake of 6 and of 10 m/s?

[folded: Answer]
The brake grows as $N^2$, so $N \ge \sqrt{c^*/c_{\rm sc}}$: 282 at 6 m/s and 364 at 10 m/s. And that is with the wires joined, when the coil burns everything; a load needs a still larger ratio.

With the wires joined ($R_L = 0$), how much power reaches the load? And with the wires apart ($R_L \to \infty$)?

[folded: Answer]
None either way. Joined, the brake is strongest but all its power heats the coil; apart, no current flows and the motor does not brake at all. In between lies a best load, the contest of section 2.3 once more.

The motor's friction proved ten times the catalogue's estimate. Would the four-stage gearhead at 492 : 1 jam the second blade?

[folded: Answer]
At the catalogue's friction it jams only beyond a ratio of 3 518; the jamming ratio falls in proportion to the friction, so ten times the friction jams it beyond about a tenth of that, below 492. Yes, it would jam: the friction would hold the second blade still against gravity's push. A bench test of the friction comes first.

How fast does the motor turn at most, through 492 : 1, and why is that slow for a motor?

[folded: Answer]
At most 743 rpm, at 6 m/s, where the swing is fastest. Small motors are built for thousands of rpm; here even a 492-fold gearbox leaves it turning slowly, which is why its voltage peaks at only about a volt.

## 8 The answer

## 8.1 The ceiling

Lower a bag of shopping on a rope: the power you can take from it is its weight times the speed at which it falls, however it falls. The second blade is the same, with its weight acting at its centre of mass, $l/2$ from the hinge, and moving relative to the mother blade at the speed $\tfrac l2|\dot\theta|$.

The mechanics of these notes meets in one inequality. Watch the second blade from the turning mother blade, with the rotor's speed steady and the mother blade rigid. In this frame gravity does the work; seen from the ground, the same energy comes from the rotor (section 1.8). The two are one bookkeeping in two frames. There the centrifugal pull is a fixed field of force with a potential energy, so over a steady turn it gives as much as it takes; the Coriolis force is always at right angles to the motion and does no work. Gravity is the only force whose direction changes, and the only one that can feed the swing on average. Its torque on the second blade is $-\tfrac{ml}{2}g\cos(\varphi+\theta)$, never larger than $\tfrac{ml}{2}g$, so the power it feeds in, and with it every watt the generator can take, obeys
$$\bar P \le \frac{ml}{2}\,g\,\langle|\dot\theta|\rangle. \tag{8.1}$$

It holds for any motion: small swings or large, regular or chaotic, with any brake and any gearbox. (A rotor whose speed wanders, or a blade that shakes, adds a feed of its own: a few per cent from gusts and sag, and from the blade's vibration an amount that depends on a vibration level we could not find (chapters 5 and 6). The air, left out of these notes, would add a feed of its own too.) To harvest more, the second blade must move faster, and a stiff centrifugal spring does not let it. At the best brake of chapter 2 the power is $P^* = \tfrac12\,\tau^*\,\Omega\Theta^*$ with $\tau^* = \tfrac{ml}{2}g/\sqrt2$, a fixed fraction, $\pi/(4\sqrt2) = 0.555$, of the right side of (8.1): the best brake already takes more than half of what gravity could ever give at that swing.

The inequality also names the one design lever that always works: the right side grows with the first moment $\tfrac{ml}{2}$. A heavier second blade, or one whose mass sits farther out, gives proportionally more, as (2.7) says. What limits it is the generator, whose best brake (2.6) and torque $\tau^*$ grow with the first moment too (section 7.5), and the air.

## 8.2 What the second blade can and cannot do

The question was how much power a second blade hinged at the tip of a turbine blade can give, who pays for it, and what the wind's gusts and the blade's motion add. The answers, in short:

A uniform second blade of 1 kg and 1 m takes 161 to 267 mW from the rotor at steady winds of 10 to 6 m/s, by the best-brake rule $\kappa^* = R - 1$, and the rotor pays for every joule. The power grows with the first moment $ml/2$ and falls with the speed of the hinge, so it is largest in light wind (chapters 2 and 3).

Resonance is out of reach for any second blade shorter than its mother blade, and the motion is regular at every wind and brake tried (chapters 2 and 3).

Gusts change the power by a few per cent (chapter 5), and so does the mother blade's sag under its own weight (chapter 6). Random shaking of white-noise type can feed in at most $\tfrac S2$ times three quarters of the second blade's mass, whatever the motion (chapter 4). The blade's real vibration is the open question: the second blade takes little from tip vibrations of 5 mm and more than gravity gives at 100 mm, and we found no published value for this blade (chapter 6).

A real geared generator from a catalogue delivers 57 to 106 mW to the load, more than 1 500 times what the minimal sensor of section 0.5 needs, and still hundreds of times if the gearbox proves twice as draggy and less efficient than its catalogue (chapter 7). The second blade is sized to that generator. Turning its slow alternating voltage into a steady supply is an open problem of electronics.

What the mechanics leaves open is the air. At the tip the second blade moves through the air at 45.3 to 75.5 m/s, and section 0.7 showed that a few square centimetres of it, at a force coefficient of one, would feel a force as large as its weight. A real second blade, many times larger, would be pushed by the air at least as hard as by gravity. That push could feed the swing, as a flag's flutter is fed by the wind, or damp it; it would certainly load the hinge and the generator. These notes answer the question for the mechanics alone: gravity, turning once per revolution as seen from the blade, drives a swing worth about a fifth of a watt for a kilogram on a metre, and the rotor pays for it without noticing. The air must be modelled before these numbers can be trusted for a real tip device; it is the next model, and it decides whether this machine is worth building.

## 8.3 Sources

Every value taken from outside these notes comes from one of these, each of which a reader can open.

A. Betz, Das Maximum der theoretisch möglichen Ausnützung des Windes durch Windmotoren, Zeitschrift für das gesamte Turbinenwesen 26 (1920) 307–309. The limit $C_p \le 16/27$ of section 0.2.

J. Jonkman, S. Butterfield, W. Musial, G. Scott, Definition of a 5-MW Reference Wind Turbine for Offshore System Development, NREL/TP-500-38060, 2009, osti.gov/servlets/purl/947422. Rotor radius, hub radius, hub height, blade mass, gearbox ratio, rated speeds (Table 1-1), peak power coefficient and its tip-speed ratio (Table 7-2), inertia, torque law, edgewise frequency 1.0793 Hz (Table 9-1).

OpenFAST regression tests, NREL 5-MW blade file NRELOffshrBsline5MW_Blade.dat, github.com/OpenFAST/r-test (glue-codes/openfast/5MW_Baseline). The blade's mass and stiffness tables of chapter 6.

NREL ROSCO, Examples/Test_Cases/NREL-5MW/Cp_Ct_Cq.NREL5MW.txt, github.com/NREL/ROSCO. The power coefficient $C_p(\lambda)$ of chapter 5.

B. J. Jonkman, TurbSim User's Guide, Version 1.50, NREL/TP-500-46198, 2009, osti.gov/servlets/purl/965520. The IEC 61400-1 (edition 3) Kaimal spectrum, turbulence intensity class A and coherence used in chapter 5; the standard itself is not freely available.

maxon, RE 25 ∅25 mm, graphite brushes, 20 W, catalogue page 153, maxongroup.com (EN-22-153.pdf); product 339152 (the 24 V winding), maxongroup.com/maxon/view/product/339152. The motor of chapter 7.

maxon, Planetary Gearhead GP 32 C, catalogue pages 430–431, maxongroup.com (GP-32-C.pdf). Ratios, efficiencies, continuous torques, inertias, backlash, input speed limit.

Analog Devices, ADXL362 datasheet, revision D, analog.com; Texas Instruments, CC2652R datasheet, SWRS207J, ti.com. The sensor node of section 0.5.

Saft, LS 33600 primary lithium-thionyl chloride cell, D size, 3.6 V, 17 Ah, datasheet, saftbatteries.com. The battery of section 0.5.

F. Cottone, H. Vocca, L. Gammaitoni, Nonlinear energy harvesting, Physical Review Letters 102 (2009) 080601. The proposal that irregular oscillators catch more of random shaking, which motivates chapter 4.

Vestas Wind Systems, Method of attaching a tip extension to a wind turbine blade, US patent 10 927 809 B2, patents.google.com/patent/US10927809B2. A retrofit tip extension about three metres long, of which about one metre reaches past the old tip (section 7.6).

Wind turbine blade tip brake apparatus and method, US patent 8 403 641 B2, patents.google.com/patent/US8403641. A pivoting tip brake whose tip is, in the preferred form, 5 % to 20 % of the rotor radius (section 7.6).


