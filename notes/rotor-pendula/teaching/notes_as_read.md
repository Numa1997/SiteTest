
Part IA second blade on a turning blade

# 0 From scratch: the wind, the turbine, and the question

This chapter assumes nothing about wind turbines. It starts from moving air, finds how much power a turbine can take from it and why, and only then puts our machine on the turbine.

## 0.1 Moving air carries energy

[Picture] Hold a flat hand out of the window of a car at motorway speed and the air shoves it back hard; at walking pace you feel nothing. Moving air is mass in motion, and mass in motion carries kinetic energy.

Take a box of air one cubic metre in volume. Its mass is the air's density, $\rho = 1.225$ kg/m³ at sea level. Moving at speed $v$, it carries the kinetic energy $\tfrac12\rho v^2$, in joules per cubic metre. Now stand a frame of area $A$ across the wind. In one second, all the air within a distance $v$ upwind passes through it: a volume $Av$. So the frame is crossed every second by the energy
$$P_{\rm wind} = \tfrac12\rho v^2 \times A v = \tfrac12\,\rho\,A\,v^3. \tag{0.1}$$

Two factors of $v$ come from the energy of each kilogram, the third from how many kilograms arrive per second. That cube is the first fact of wind power: double the wind and its power grows eightfold.

[On our turbine] At 8 m/s, each square metre facing the wind receives $314$ W. The turbine of these notes sweeps a disc of radius 63 m, an area $\pi\,63^2 = 12 469$ m², about two football pitches. Through it flow 1.65, 3.91 and 7.64 MW at 6, 8 and 10 m/s: from 6 to 10 m/s the wind's speed grows by two thirds and its power by a factor of 4.6.

## 0.2 No turbine can take all of it

[Picture] If a turbine took all the wind's energy, the air behind it would stand still. But still air cannot move out of the way, so the air arriving next would pile up and flow around the turbine instead of through it. A turbine that stops the wind gets nothing; one that does not slow it gets nothing either. The best turbine slows the wind part way.

Model the rotor as a thin disc of area $A$ that the air passes through and that slows it. Far upwind the wind has speed $v$; at the disc it is slowed to $v(1-a)$, where $a$, the fraction lost at the disc, is to be found; far downwind it has slowed further, to $v_{\rm w}$. Three laws fix the rest.

Mass is conserved: every second the mass $\dot m = \rho A v(1-a)$ crosses the disc. Momentum: the disc pushes back on this air and takes away its momentum per second, so the force on the disc, the thrust, is $F = \dot m\,(v - v_{\rm w})$. Energy: the air loses kinetic energy per second $\tfrac12\dot m\,(v^2 - v_{\rm w}^2)$, and that is the power the disc takes. But the power the disc takes is also force times the speed of the air through it, $F\,v(1-a)$. Setting the two equal,
$$\tfrac12\dot m\,(v - v_{\rm w})(v + v_{\rm w}) = \dot m\,(v - v_{\rm w})\,v(1-a) \quad\Rightarrow\quad v(1-a) = \tfrac12(v + v_{\rm w}) \quad\Rightarrow\quad v_{\rm w} = v(1-2a):$$

the speed at the disc is the average of the speeds far upwind and far downwind, so the disc does half the slowing, and the wake behind it the other half. Put this back into the power:
$$P = \dot m\,(v - v_{\rm w})\,v(1-a) = \tfrac12\rho A v^3 \cdot 4a(1-a)^2 = C_p\,P_{\rm wind}, \qquad C_p = 4a(1-a)^2. \tag{0.2}$$

$C_p$, the power coefficient, is the share of the wind's power the disc takes. It is zero with no slowing ($a = 0$) and zero again when the wake would stop dead ($a = \tfrac12$). In between, $dC_p/da = 4(1-a)(1-3a) = 0$ gives $a = \tfrac13$ and
$$C_{p,\max} = \frac{16}{27} = 0.593. \tag{0.3}$$

No turbine, however shaped, can take more than 59 % of the power of the wind crossing it; this is the Betz limit (Betz 1920). The 5 MW turbine of these notes, a published reference design (Jonkman et al. 2009), reaches $C_p = 0.482$ at its best, 81 % of the limit: at 6, 8 and 10 m/s it delivers 0.80, 1.88 and 3.68 MW.

[Check] Units: $\rho A v^3$ is kg/m³ · m² · m³/s³ = kg m²/s³ = W. Limits: $a = 0$ gives $P = 0$ (the air passes untouched); $a = \tfrac12$ gives $v_{\rm w} = 0$ and again $P = 0$ (the wake stands still). The maximum lies between, at $a = \tfrac13$, where the wake moves at a third of the wind's speed.

## 0.3 How a blade turns a push into turning

[Picture] An ice yacht can race across the wind at several times the wind's speed. Its sail is not pushed by the wind like a hand out of a car window; it is a wing, and the air it feels comes mostly from its own motion. A turbine blade is a wing that sails round in a circle.

Look at one short piece of blade at distance $r$ from the hub, while the rotor turns at angular speed $\Omega$ (radians per second). The piece moves sideways at $\Omega r$. The wind comes at it from the front at $v(1-a)$, slowed at the rotor as section 0.2 found. Riding on the blade, you feel both at once: the apparent wind, coming at the angle
$$\tan\phi = \frac{v(1-a)}{\Omega r} \tag{0.4}$$

to the blade's own path. A wing in a stream of air feels a force at right angles to the stream, the lift, and a much smaller force along it, the drag. Because the apparent wind comes in at the angle $\phi$, the lift leans forward by the same angle: its component $L\sin\phi$ points along the blade's motion and turns the rotor, its component $L\cos\phi$ pushes the rotor downwind. The drag, along the apparent wind, holds the blade back by $D\cos\phi$. So the piece turns the rotor only if $L\sin\phi > D\cos\phi$, that is, if its lift is more than $\cot\phi$ times its drag. Figure 1 draws the speeds at the tip.

Why does the tip move so much faster than the wind? The rotor takes power as torque times $\Omega$. A slowly turning rotor meets the wind at a steep angle: its blades are pushed downwind more than round, and most of the wind goes through the wide gaps between them untouched. A rotor turning too fast blocks the wind like a solid disc and sends it around. In between, the blades sweep the whole disc often enough to slow all of its air by the right third, and that sets the ratio of the tip's speed to the wind's speed, the tip-speed ratio $\lambda = \Omega r_{\rm rot}/v$, for which a given rotor takes the most. For the 5 MW turbine, $\lambda^* = 7.55$ (Jonkman et al. 2009), and its controller holds the rotor near that ratio in moderate wind by adjusting the generator's braking torque.

[FIGURE:  Figure 1. A piece of blade at the tip, seen along the blade from its tip, at 8 m/s. The blade moves to the right at 60.4 m/s, so it meets air coming at it from the front at that speed; the wind blows through the rotor at 5.33 m/s, slowed by a third (section 0.2). Together they make the apparent wind, which comes in only 5.0° off the blade's path; the wind arrow is drawn 3 times too long so that the angle can be seen (it is drawn at 15°). The lift is at right angles to the apparent wind: mostly it pushes the rotor downwind, but it leans forward by the same angle, and that forward part is what turns the rotor. ]

[On our turbine] At 8 m/s, $\Omega = \lambda^*v/r_{\rm rot} = 7.55 \times 8/63$, a turn every 6.6 s. At the tip the blade moves sideways at 60.4 m/s while the wind, slowed by a third, meets it at 5.33 m/s. The apparent wind is 60.6 m/s, coming in only 5.0° off the blade's path, so the tip turns the rotor only if its lift is more than 11.3 times its drag; good wing sections manage about a hundred. To the tip of the blade, the wind is a gentle side-draught on a fast, almost head-on stream of air.

## 0.4 What the blade is, and what our question needs from it

Each blade of the 5 MW turbine is 61.5 m long and starts at a hub of radius 1.5 m, so its tip runs on a circle of radius 63 m. It is a hollow shell of glass fibre and resin, heavy near the hub and light at the tip: the published design weighs it at about 17.7 t, with 10 kg per metre at the very tip. The rotor turns in a vertical plane, so every point of a blade goes up and down once per turn. Everything the rest of these notes uses comes from this chapter so far: the rotor's speed $\Omega$ at each wind from $\lambda^*$, the radius 63 m of the tip, and gravity, which a turning blade feels from a direction that goes round once per turn.

## 0.5 A sensor that nobody can reach

The blades of a large wind turbine are some 60 m long and turn ten times a minute for twenty years. Engineers would like to know how each blade bends and shakes while it works: a crack or a loose bolt changes how a blade vibrates long before it fails. A small sensor glued inside the blade can measure that, but it needs electricity, and the far end of a blade is the worst place on the machine to bring it. A cable must pass through the rotating hub; a battery 60 m out along a blade cannot be changed without stopping the turbine and sending a technician up a rope.

The blade itself is full of motion. So here is an idea. At the very tip of the blade, put a hinge whose axis is parallel to the rotor's shaft, and hang on it a second, much lighter blade, free to turn in the rotor plane. As the big blade (the mother blade) turns, the second blade swings back and forth about its hinge. A small generator in the hinge brakes that swing and turns it into electricity, and the sensor runs on that.

[Picture] Ride a Ferris wheel holding a ruler loosely by one end, so that it can turn in the plane of the wheel. The wheel presses everything outwards, so the ruler lies along the spoke, pointing away from the hub. But gravity keeps pulling down while the wheel carries you round: near the top and the bottom it pulls along the ruler, on the way up and on the way down it pulls across it, first to one side and then to the other. Once per turn the ruler is pushed one way and then the other. That once-per-turn push is what we harvest.
[SVG DRAWING]
Figure 2. The machine. Left: the rotor seen along its shaft; the second blade (wine) is hinged at the tip of one blade, the mother blade. Right: the tip close up, seen from the turning mother blade; the second blade, of length $l$, has turned by the angle $\theta$ from the mother blade's outward line (dashed). The left view is not to scale here; the simulation draws it to scale, where a 1 m second blade on a 63 m rotor is a few pixels long.

## 0.6 Four questions, and the short answers

Four questions run through these notes: how much power, who pays for it, how big the second blade should be, and whether the wind's randomness helps. In short:

The power. A second blade of 1 kg and 1 m, hinged at the 63 m tip of a 5 MW turbine, takes between 161 and 267 mW of mechanical power from the swing, at steady winds of 10 and 6 m/s (chapters 2 and 3). A sensor node that samples an accelerometer continuously (ADXL362) and once a second wakes a radio chip (CC2652R) for 1 ms of computing and 1 ms of sending needs about 37.6 µW, from the typical currents of the two datasheets (section 8.3); that budget leaves out the radio's start-up and receive windows and the losses of a power converter. A real motor and gearbox from a catalogue deliver 57 to 106 mW of it to the wires, 1 522 times the sensor's need or more (chapter 7).

Who pays. The rotor. Every joule the generator takes, the rotor supplies, through a slightly larger torque on its shaft (sections 1.4 and 3.2). The second blade takes at most 0.34 parts in a million of the turbine's power.

How big. What counts is the second blade's first moment, its mass times the distance from the hinge to its centre of mass, $ml/2$: the power grows in proportion to it (chapter 2). Where the mass sits matters as much as how much there is: a uniform blade of mass $m$ and length $l$ gives half of what the same mass would give in a lump at its end (chapter 3). The size these notes use, 1 kg on 1 m, is the one the generator of chapter 7 serves best. Over the sizes of real tip devices, up to three metres long and as heavy as the blade's own tip, the best power at 6 m/s runs from 66.7 mW to 74.0 W, but the generator must grow with it (section 7.6).

The wind's randomness. Mostly it does not help. Random shaking of white-noise type has a hard ceiling that no motion, chaotic or not, can beat (chapter 4). Gusts change the rotor's speed, and that changes the power by a few per cent at most (chapter 5). The blade's sag at its tip adds a few per cent; its shaking, strongest at the tip, adds a little at tip vibrations of 5 mm and more than gravity gives at 100 mm, a level no source we found confirms (chapter 6).

## 0.7 Where the numbers come from

Every number in these notes is computed here: the equations are derived in the text, solved by a stiff integrator checked against an independent solver, and the results are put into the text by a script.

The turbine is the NREL 5 MW reference turbine, a published design of a utility turbine (Jonkman, Butterfield, Musial and Scott 2009), with a rotor radius of 63 m. Its blade tip moves about 7.55 times faster than the wind when it works best (its tip-speed ratio $\lambda^* = 7.55$, where its power coefficient peaks at $C_p = 0.482$), and in moderate wind its controller holds it close to that. At a steady wind $v$ the rotor then turns at
$$\Omega = \frac{\lambda^*\,v}{r_{\rm rot}}, \qquad r_{\rm rot} = 63\ \mathrm{m},$$

which for the three winds of these notes, 6, 8 and 10 m/s, is 6.87, 9.16 and 11.44 rpm. The hinge sits at the tip, $r_p = r_{\rm rot}$, and moves at $\lambda^*v$: 45.3, 60.4 and 75.5 m/s. The turbine's own power, for the share quoted above, is $P_T = \tfrac12\rho\pi r_{\rm rot}^2v^3C_p$: the kinetic energy of the air that flows through the rotor's disc each second, $\tfrac12(\rho\pi r_{\rm rot}^2v)v^2$, of which the fraction $C_p$ is caught, with air density $\rho = 1.225$ kg/m³.

The second blade is a thin uniform rod, a modelling choice that keeps the mathematics clean; its length $l = 1$ m is a choice too, and its mass $m = 1$ kg is set in chapter 7 by matching it to a real generator. The drawing of the simulation gives it a blade's tapered outline, but the physics treats it as a uniform rod.

One thing these notes leave out on purpose: the air. At the tip the hinge moves through the air at 45.3 to 75.5 m/s, and the air pushes on anything moving that fast with a pressure of order $\tfrac12\rho v_{\rm tip}^2$, 2234 Pa at 8 m/s. To match gravity's whole pull on the second blade, $mg = 9.81$ N, that pressure needs to act on an area, times a force coefficient, of only $mg/(\tfrac12\rho v_{\rm tip}^2) = 43.9$ cm². A real blade is far larger than that, so air would shape its motion at least as strongly as gravity does. These notes answer the question for the mechanics alone; a model of the air on the second blade is the next step, and section 8.2 says what it could change.

## 0.8 How to read these notes

Each step is built in the same order. A Picture box gives something to imagine with your hands and eyes. The working follows, one line at a time, with the reason for each line. A green Check box tests the result: its units, its sign, and a limit where we already know the answer. A wine-coloured On our blade box gives the numbers of the real machine, all computed from the model; the few inputs typed by hand (datasheet values and the chosen sizes) are listed with their sources, and a script checks every number in the text. Where a long piece of algebra was done by computer (SymPy, a program for symbolic algebra), the text says so and shows the steps a reader needs.

[Conventions] SI units throughout. Gravity $g = 9.80665\ \mathrm{m/s^2}$, the standard value. A dot is a derivative with respect to time $t$; a prime is a derivative with respect to the rotor's angle $\varphi$ (section 1.5). The second blade's angle $\theta$ is measured from the mother blade's outward direction, positive in the direction the rotor turns.




# 1 Sitting at the tip

Before any equation, ride along. Almost everything the second blade does follows from two pulls it feels in the mother blade's own frame: one outwards, one that turns round.

## 1.1 Two pulls

[Picture] Sit at the rim of a fast Ferris wheel. You are pressed outwards, away from the hub, and the faster the wheel turns the harder you are pressed. Gravity still pulls you towards the ground, but the wheel carries you round, so as seen from your seat "down" sweeps round once per turn: outwards at the bottom, towards the hub at the top, sideways in between.

A turbine rotor turns in a vertical plane. The hinge, at distance $r_p$ from the hub, moves on a circle at angular speed $\Omega$. Seen from the mother blade, every piece of the second blade feels a centrifugal pull $\Omega^2 r$ per kilogram, straight away from the hub, with $r$ its own distance from the hub, and gravity $g$ per kilogram, whose direction turns once per turn. At the hinge the ratio of the two,
$$\Gamma = \frac{\Omega^2 r_p}{g},$$

says which wins. At the 63 m tip $\Gamma$ is 3.32, 5.90 and 9.23 at 6, 8 and 10 m/s: the outward pull wins, by a factor of three to nine. Add the two pulls and you get an apparent gravity that points roughly out along the mother blade and tilts to one side, then to the other, once per turn, by up to $\arcsin(1/\Gamma)$: 17.5°, 9.8° and 6.2°. The second blade, free on its hinge, behaves like a weathervane in that apparent wind: it lies along the mother blade and leans with the tilt.

In a turning frame there are two more apparent forces. The Coriolis force acts on anything moving relative to the mother blade; a piece of the second blade moves at right angles to the second blade, so the Coriolis force on it points along the second blade and has no lever arm about the hinge: it cannot turn the second blade. The Euler force appears only while the rotor speeds up or slows down; it is kept in the equations below and studied in chapter 5.

## 1.2 Coordinates

Put the hub at the origin, with $y$ pointing up. The rotor's angle is $\varphi(t)$, so the hinge sits at $r_p(\cos\varphi, \sin\varphi)$. The second blade is a thin uniform rod of mass $m$ and length $l$, hinged at one end; let $\theta$ be its angle from the mother blade's outward direction, so it points along the absolute angle $\varphi + \theta$. The point at distance $s$ from the hinge, $0 \le s \le l$, is at
$$x = r_p\cos\varphi + s\cos(\varphi+\theta), \qquad y = r_p\sin\varphi + s\sin(\varphi+\theta). \tag{1.1}$$
[SVG DRAWING]
Figure 3. The second blade at the tip. The rotor angle $\varphi$ is measured from the horizontal; the hinge sits at $r_p$ from the hub; the second blade, of length $l$, makes the angle $\theta$ with the mother blade's outward direction (dashed). A piece at distance $s$ from the hinge is pulled away from the hub by $\Omega^2 r$, with $r$ its own distance from the hub, and down by gravity, whose direction turns once per turn. Split each piece's centrifugal pull in two: the part along the second blade has no lever arm about the hinge, and what is left is a pull $\Omega^2 r_p$ straight out along the mother blade, the same for every piece and every position. Summed over the pieces, it acts as if all the mass sat at the centre of mass, $l/2$ from the hinge, and it turns a tilted second blade back to the mother blade's line, as gravity turns an ordinary pendulum back to the vertical: that is the centrifugal spring. Not to scale: $r_p$ is 63 times $l$.

The rotor's motion $\varphi(t)$ is imposed from outside: the rotor is enormously heavier than the second blade, so the second blade cannot change it noticeably. We treat $\varphi(t)$ as a given function of time, not as a second unknown, and do not yet say what it is, so the same equations will hold later when gusts make the rotor speed up and slow down.

## 1.3 The Lagrangian and the generator

Why Lagrange and not Newton? Newton would need the forces inside the second blade and at the hinge, which we do not know and do not want. Lagrange's method avoids them. Write the kinetic energy $T$ and the potential energy $V$ in terms of the one angle the second blade is free to move through, $\theta$, and form $\mathcal L = T - V$. Then Lagrange's equation, $\frac{d}{dt}\frac{\partial\mathcal L}{\partial\dot\theta} - \frac{\partial\mathcal L}{\partial\theta} = Q$, is Newton's second law for the angle: the left side is the rate of change of the second blade's angular momentum about the hinge minus the torques that come from the energies, and $Q$ is any other torque, here the generator's. The hinge's forces never appear, because they do no work when the second blade moves the way the hinge allows.

A piece of length $ds$ has the mass $(m/l)\,ds$. Differentiate (1.1), square, and add up the pieces' kinetic energies, $\tfrac12(m/l)(\dot x^2 + \dot y^2)\,ds$, along the second blade. Each piece's speed squared has three parts: the hinge's own motion, $r_p^2\dot\varphi^2$; the piece's motion about the hinge, $s^2(\dot\varphi+\dot\theta)^2$; and a cross term, $2r_ps\,\dot\varphi(\dot\varphi+\dot\theta)\cos\theta$. Integrating over the length turns $\int_0^l ds$ into $l$, $\int_0^l s\,ds$ into $l^2/2$ and $\int_0^l s^2\,ds$ into $l^3/3$:
$$T = \tfrac12 I(\dot\varphi+\dot\theta)^2 + \tfrac12 m\,r_p^2\dot\varphi^2 + \frac{ml}{2}\,r_p\,\dot\varphi(\dot\varphi+\dot\theta)\cos\theta, \qquad I = \frac{ml^2}{3}. \tag{1.2}$$

Two numbers describe the second blade from here on. $I = ml^2/3$ is its moment of inertia about the hinge, the sum of every piece's mass times its distance from the hinge squared. $ml/2$ is its first moment about the hinge, the sum of every piece's mass times its distance: its mass times the distance from the hinge to its centre of mass. The potential energy is the weight of the pieces times their height, which adds up to the whole mass at the centre of mass:
$$V = mg\left[r_p\sin\varphi + \frac l2\sin(\varphi+\theta)\right].$$

The generator's stator is fixed to the mother blade and its rotor to the second blade, so it brakes only the second blade's motion relative to the mother blade. In an ideal generator the voltage is proportional to the speed, $k_e\dot\theta$; it drives a current $i = k_e\dot\theta/(R_c + R_L)$ through the coil (resistance $R_c$) and the load ($R_L$); and the current makes a braking torque $k_t\,i$. So the torque is $-c\dot\theta$ with $c = k_tk_e/(R_c + R_L)$: a pure brake proportional to speed. A brake of this kind enters Lagrange's equation as $Q = -c\dot\theta$, which can be written as the derivative of Rayleigh's dissipation function $\mathcal F$, half the brake's power:
$$\mathcal F = \tfrac12 c\,\dot\theta^2, \qquad \frac{d}{dt}\frac{\partial \mathcal L}{\partial\dot\theta} - \frac{\partial\mathcal L}{\partial\theta} = -\frac{\partial\mathcal F}{\partial\dot\theta} = -c\,\dot\theta.$$

The two derivatives, from (1.2) and $V$:
$$\frac{\partial\mathcal L}{\partial\dot\theta} = I(\dot\varphi+\dot\theta) + \frac{ml}{2}r_p\,\dot\varphi\cos\theta, \qquad \frac{\partial\mathcal L}{\partial\theta} = -\frac{ml}{2}r_p\,\dot\varphi(\dot\varphi+\dot\theta)\sin\theta - \frac{ml}{2}g\cos(\varphi+\theta).$$

Take the time derivative of the first, $I(\ddot\varphi+\ddot\theta) + \frac{ml}{2}r_p(\ddot\varphi\cos\theta - \dot\varphi\dot\theta\sin\theta)$, subtract the second, and the two $\dot\varphi\dot\theta\sin\theta$ terms cancel:
$$I(\ddot\theta+\ddot\varphi) + \frac{ml}{2}\,r_p\left(\ddot\varphi\cos\theta + \dot\varphi^2\sin\theta\right) + \frac{ml}{2}\,g\cos(\varphi+\theta) + c\,\dot\theta = 0. \tag{1.3}$$

Every term has a meaning. $I\ddot\theta$ is the second blade's inertia about the hinge. $\frac{ml}{2}r_p\dot\varphi^2\sin\theta$ is the centrifugal pull trying to bring it back along the mother blade: a restoring torque, like a spring, which acts on the first moment. $\frac{ml}{2}g\cos(\varphi+\theta)$ is gravity's torque, the weight at the centre of mass times its lever, which turns with the rotor. The two terms with $\ddot\varphi$ appear only when the rotor speeds up or slows down. $c\dot\theta$ is the generator.

Nothing in (1.3) depends on the second blade's shape except through $I$ and the first moment. The same equation holds for any rigid body on the hinge, with its own moment of inertia $I_p$ about the hinge and its own first moment $Ml_c$ (mass times the distance $l_c$ from the hinge to its centre of mass). A small bob of mass $m$ at the end of a massless rod of length $L$, the simplest pendulum, has $I_p = mL^2$ and $Ml_c = mL$; a uniform rod has $I = ml^2/3$ and $ml/2$. Section 3.3 uses that.

[Check] Units: every term is a torque, kg m²/s² = N m. Limit: stop the rotor ($\dot\varphi = \ddot\varphi = 0$) with the mother blade pointing along $\varphi_0$. Then (1.3) is $I\ddot\theta + \frac{ml}{2}g\cos(\varphi_0+\theta) + c\dot\theta = 0$: an ordinary braked physical pendulum, at rest hanging straight down, $\varphi_0+\theta = -\pi/2$, and swinging about it at $\omega^2 = (ml/2)g/I = 3g/(2l)$, the textbook frequency of a rod swinging from one end. A second limit: a second blade too short to matter, $l \to 0$ at fixed mass, must behave like a point mass sitting on the hinge; the torque the rotor needs (section 1.4) then becomes $mgr_p\cos\varphi$, which is that point mass's weight times its lever about the hub. The derivation was repeated by computer in two ways, by Lagrange in SymPy from the positions (1.1), and by Newton's law in the turning frame, summing the torques of the centrifugal, Coriolis and gravity forces on every piece; the two results agree identically.

## 1.4 Who pays

The rotor must push the hinge along its path. The torque it needs is Lagrange's expression for the other angle, $\varphi$: the torque that makes $\varphi(t)$ happen,
$$\tau_{\rm rot} = \frac{d}{dt}\frac{\partial\mathcal L}{\partial\dot\varphi} - \frac{\partial\mathcal L}{\partial\varphi}.$$

The brake does not appear here: its torque acts between the mother blade and the second blade, inside the pair, and the rotor drives the pair. Now follow the second blade's energy $E = T + V$ in time. The quickest route treats $\varphi$ as a second coordinate, driven by the torque $\tau_{\rm rot}$. $\mathcal L$ does not contain $t$ explicitly, so the energy function $h = \dot\varphi\,\partial\mathcal L/\partial\dot\varphi + \dot\theta\,\partial\mathcal L/\partial\dot\theta - \mathcal L$ changes only through the outside torques: $dh/dt = \tau_{\rm rot}\dot\varphi - c\dot\theta^2$. And because $T$ is a quadratic form in $(\dot\varphi, \dot\theta)$, the first two terms of $h$ add up to $2T$, so $h = T + V = E$. (SymPy confirms it the long way, by differentiating $E$ and using (1.3).) So
$$\frac{dE}{dt} = \tau_{\rm rot}\,\dot\varphi - c\,\dot\theta^2. \tag{1.4}$$

The first term is the work the rotor does on the second blade; the second is the power the generator takes. In a steady swing $E$ returns to the same value every turn, so over a turn the two balance: the rotor pays for every joule the generator harvests. Gravity does no net work over a turn, since the second blade comes back to the same height. Seen from the mother blade, gravity is the hand that pushes the second blade; seen from the ground, it only steers energy that the rotor supplies. Section 3.2 shows where, physically, the rotor's extra torque comes from. Both pictures will be used: whenever these notes say that gravity feeds the swing, they speak from the mother blade, and the energy still comes from the rotor.

The rotor's torque is large even when nothing is harvested: it lifts the whole second blade up the turbine's height, $2r_p$, once per turn, and lets it down again. Its own share is the term $mgr_p\cos\varphi$, which averages to zero over a turn; the simulation's data log shows it as the large swing of the rotor's work against the energy lifted.

## 1.5 The rotor as a clock

Now let the rotor turn steadily, $\dot\varphi = \Omega$. A natural clock is the rotor's own angle: one turn is $2\pi$. Write $\theta' = d\theta/d\varphi = \dot\theta/\Omega$ and divide (1.3) by $I\Omega^2$:
$$\boxed{\theta'' + \kappa\,\theta' + R\sin\theta + G\cos(\varphi+\theta) = 0,} \qquad R = \frac{(ml/2)\,r_p}{I} = \frac{3r_p}{2l},\quad G = \frac{(ml/2)\,g}{I\,\Omega^2} = \frac{3g}{2l\Omega^2},\quad \kappa = \frac{c}{I\Omega}. \tag{1.5}$$

Three numbers say everything. $R$ is the stiffness of the centrifugal spring: seen from the mother blade, a free small swing makes $\sqrt R$ oscillations per rotor turn (gravity's own stiffening changes sign every half turn and averages out). $G$ is the strength of gravity's push. $\kappa$ is the generator. Their ratio $R/G$ is the $\Gamma$ of section 1.1. Two bodies with the same $R$, $G$ and $\kappa$ do exactly the same thing, turn for turn, whatever their size or shape.

[On our blade] For the 1 m second blade at the 63 m tip, $R = 94.5$ at every wind, and $G$ is 28.45, 16.00 and 10.24 at 6, 8 and 10 m/s. The second blade's own frequency is therefore $\sqrt R = 9.72$ times the once-per-turn push of gravity: far above it, never near it.

## 1.6 The same equation from the turning frame: a bowl that rocks

[Picture] Put a marble in a salad bowl and tilt the bowl gently one way, then the other. The lowest point of the bowl slides from side to side, and the marble chases it. Fill the bowl with honey and the marble lags behind the moving bottom; the honey warms a little with every pass. Our second blade is that marble, the generator is the honey, and the bowl is made by the rotor's turning.

Lagrange's method in the ground frame gave (1.3). For a rotor turning steadily at $\Omega$, the same equation follows in four lines from the frame that turns with the mother blade, and that route shows its physics directly. In the turning frame a piece of mass $dm$ at distance $r$ from the hub feels the centrifugal force $\Omega^2 r\,dm$, pointing away from the hub. That force is minus the gradient of the centrifugal potential energy $-\tfrac12\Omega^2 r^2\,dm$: the turning frame behaves as if the hub sat at the top of a hill whose height falls as $-r^2$. By (1.1), a piece at distance $s$ from the hinge has $r^2 = r_p^2 + s^2 + 2r_ps\cos\theta$. Summed over the second blade, only the last term depends on $\theta$:
$$U_{\rm c}(\theta) = -\tfrac12\Omega^2\!\int_0^l \frac{m}{l}\left(r_p^2 + s^2 + 2r_ps\cos\theta\right)ds = -\frac{ml}{2}\,\Omega^2 r_p\cos\theta + \text{const.}$$

Add gravity's potential energy, the weight at the centre of mass times its height, $\frac{ml}{2}g\sin(\varphi+\theta)$, and the second blade's potential energy in the turning frame is
$$U(\theta,\varphi) = \frac{ml}{2}\left[-\,\Omega^2 r_p\cos\theta + g\sin(\varphi+\theta)\right]. \tag{1.6}$$

Two more apparent forces act in a turning frame. The Euler force needs $\dot\Omega \ne 0$ and is absent here. The Coriolis force, $-2\,\boldsymbol\Omega\times\mathbf v\,dm$, is at right angles to the velocity $\mathbf v$ of each piece; every piece of the second blade moves at right angles to the second blade, so the Coriolis force on it points along the second blade, through the hinge, and has no lever arm. So the torque balance about the hinge contains only the slope of $U$ and the generator:
$$I\ddot\theta = -\frac{\partial U}{\partial\theta} - c\,\dot\theta = -\frac{ml}{2}\left[\Omega^2 r_p\sin\theta + g\cos(\varphi+\theta)\right] - c\,\dot\theta, \tag{1.7}$$

which is (1.3) with $\ddot\varphi = 0$.

Now read (1.6) as a picture. The first term, $-\frac{ml}{2}\Omega^2 r_p\cos\theta$, is a bowl with its bottom at $\theta = 0$: the second blade lies along the mother blade because that is downhill in the turning frame. Its curvature at the bottom, $\frac{ml}{2}\Omega^2 r_p$, is the spring constant of section 1.5, $R$ in units of $I\Omega^2$. The second term, gravity, is a tilt of that bowl, and it changes as the rotor turns. Setting $\partial U/\partial\theta = 0$, the bottom of the bowl sits at
$$\tan\theta_{\rm b} = -\frac{\cos\varphi}{\Gamma - \sin\varphi}, \qquad \Gamma = \frac{\Omega^2 r_p}{g},$$

which is the direction of the apparent gravity of section 1.1, the sum of the outward pull and gravity. When the mother blade points up or down, gravity pulls along it and the bottom of the bowl sits on the mother blade's line; near the horizontal, where gravity pulls across it, the bottom is displaced furthest, by $\arcsin(1/\Gamma)$ where $\sin\varphi = 1/\Gamma$: 17.5° either way at 6 m/s. Figure 4 draws the bowl at four positions of the rotor. A second blade that kept exactly to the moving bottom would move in step with gravity's tilting push, and a push in step with the motion it drives does no net work over a cycle: it gives energy on one half and takes it back on the other, as a hand that only follows a swing never keeps it going. Then there would be nothing for the generator to take. The generator makes the second blade lag the moving bottom; with a lag $\delta$ the push does net work in proportion to $\sin\delta$ every turn, and that work is what the generator harvests. Chapter 2 finds the best lag: $45°$.

[FIGURE:  Figure 4. The second blade's potential energy (1.6) in the frame of the mother blade, at 6 m/s ($\Gamma = 3.32$), at four positions of the rotor. The shape of the bowl is the centrifugal term and does not change; gravity tilts it, and its lowest point (dots) swings between 17.5° on one side and 17.5° on the other, $\arcsin(1/\Gamma)$, and back, once per turn. The second blade is a marble in this bowl, held in honey by the generator: it chases the moving bottom, and the generator takes energy from the chase. ]

[Check] Units: $\frac{ml}{2}\Omega^2 r_p$ is kg m · s⁻² · m = J. Limit: with the rotor stopped, $\Omega = 0$, (1.6) is $\frac{ml}{2}g\sin(\varphi+\theta)$, the potential energy of an ordinary rod pendulum, lowest when the rod hangs straight down, $\varphi+\theta = -90°$. Consistency: the curvature of $U$ at its bottom, divided by $I\Omega^2$, is $R\cos\theta_{\rm b} - G\sin(\varphi+\theta_{\rm b})$, which at $\theta_{\rm b} \approx 0$ is $R - G\sin\varphi$: the stiffness $R$ plus gravity's own stiffening of section 2.1, which changes sign every half turn.



# 2 The best brake, and how much it gives

Equation (1.5) cannot be solved in closed form. For small swings it can, and the answer contains the whole design rule.

## 2.1 Small swings: a driven, braked oscillator

[Picture] Hold a stiff spring vertically with a weight on it and move your hand slowly up and down, far below the spring's own bounce. The weight simply follows your hand, a little late. Put the weight in honey and it lags further. It never bounces, because you never push at its rhythm.

Let $\theta$ be small: $\sin\theta \approx \theta$ and $\cos(\varphi+\theta) \approx \cos\varphi - \theta\sin\varphi$. Keep the first piece, gravity's push $G\cos\varphi$. The second piece, $-G\theta\sin\varphi$, makes the spring's stiffness go up and down once per turn. Compared with the centrifugal stiffness $R\theta$ its size is $G/R = 1/\Gamma$, up to 0.30 at 6 m/s. We drop it anyway, for a reason that has nothing to do with its size: multiplying a swing at frequency 1 by $\sin\varphi$ produces motion at frequencies 0 and 2, not at frequency 1, so to first order it does not change the swing that the push drives. Its effect enters only at second order, and chapter 3 measures it against the full equation. Without it, (1.5) becomes
$$\theta'' + \kappa\,\theta' + R\,\theta = -G\cos\varphi. \tag{2.1}$$

This is the textbook driven, damped oscillator: a spring of stiffness $R$ (natural frequency $\sqrt R$ per turn), a damper $\kappa$, and a push of amplitude $G$ at frequency 1 per turn.

## 2.2 The swing

After the start-up has died away the second blade swings at the frequency of the push. Use complex notation: $\theta = \mathrm{Re}\,[A\,e^{i\varphi}]$, so that $\theta' \to iA$ and $\theta'' \to -A$. Then (2.1) gives one line of algebra:
$$(R - 1 + i\kappa)A = -G \quad\Rightarrow\quad \theta = -\Theta\cos(\varphi - \delta), \qquad \Theta = \frac{G}{\sqrt{(R-1)^2 + \kappa^2}}, \qquad \tan\delta = \frac{\kappa}{R-1}. \tag{2.2}$$

Why $R - 1$ and not $R$? The $-1$ is the second blade's own inertia: driving any body back and forth at frequency 1 costs a torque proportional to its angular acceleration, $-\theta''$, which here works against the spring. So $R - 1$ is the spring minus the inertia at the push frequency, the net stiffness the push meets. With no brake ($\kappa = 0$) the second blade follows the push exactly in step and swings $G/(R-1)$; the brake reduces the swing and makes it lag by $\delta$.

## 2.3 The harvested power

The generator takes the power $c\dot\theta^2$. Averaged over a turn, $\langle\dot\theta^2\rangle = \Omega^2\langle\theta'^2\rangle = \Omega^2\Theta^2/2$, so
$$\bar P = \tfrac12 c\,\Omega^2\Theta^2 = I\Omega^3\,\frac{\kappa\,G^2}{2\left[(R-1)^2 + \kappa^2\right]}. \tag{2.3}$$

Read it as a contest. A weak brake ($\kappa \to 0$) lets the second blade swing freely but takes nothing from it. A strong brake ($\kappa \to \infty$) locks it to the mother blade, so nothing moves and again nothing is taken. In between lies a best brake. Set $d\bar P/d\kappa = 0$:
$$(R-1)^2 + \kappa^2 - 2\kappa^2 = 0 \quad\Rightarrow\quad \kappa^* = |R - 1|. \tag{2.4}$$

The best brake equals the net stiffness. At that setting $\tan\delta = 1$: the second blade lags gravity's push by exactly 45°. Put $\kappa^*$ back into (2.3) and return to physical units with $I\Omega^2(R-1) = \left(\tfrac{ml}{2}r_p - I\right)\Omega^2$ and $I\Omega^2G = \tfrac{ml}{2}g$:
$$\boxed{P^* = \frac{\left(\tfrac{ml}{2}\,g\right)^2}{4\,\Omega\left(\tfrac{ml}{2}\,r_p - I\right)} = \frac{m\,g^2\,l}{8\,\Omega\left(r_p - \tfrac23 l\right)}.} \tag{2.5}$$

[Picture] Connect a resistor to an AC supply through a coil. Too small a resistor and the current flows but little power is turned into heat in it; too large and hardly any current flows. The resistor takes the most power when its resistance equals the coil's opposition to the alternating current, its reactance $\omega L_{\rm coil}$. The generator is the resistor; the net stiffness of the second blade, $R - 1$, plays the coil's reactance; gravity's push is the supply. The best brake is that match.

[FIGURE:  Figure 5. The harvested power (2.3) over its maximum (2.5), against the brake over the best brake (2.4): $\bar P/P^* = 2x/(1+x^2)$ with $x = \kappa/\kappa^*$, the same curve at every wind and for every second blade. The top is flat: a brake 0.27 times the best, or 3.7 times it, still gives half the power ($x = 2 \mp \sqrt3$). ]

[Check] Units: kg · (m/s²)² · m / (s⁻¹ · m) = kg m²/s³ = W. Limits: no gravity ($g \to 0$) gives no power, as it must, since nothing then pushes the second blade off the mother blade's line. At $\tfrac{ml}{2}r_p = I$, that is $l = \tfrac32 r_p$, the formula diverges: that is resonance, the second blade's own frequency $\sqrt R$ equal to the push. Section 2.5 shows that no second blade shorter than its mother blade gets there. The point bob on a rod, $I = mL^2$ and first moment $mL$, gives back the simpler form $mLg^2/(4\Omega|r_p - L|)$. The steps (2.2) to (2.5) were also checked symbolically in SymPy.

Three consequences are worth a second look. First, the generator's torque at the optimum has the amplitude
$$\tau^* = c^*\Omega\,\Theta^* = I\Omega^2(R-1)\cdot\frac{G}{\sqrt2\,(R-1)} \quad=\quad \frac{\tfrac{ml}{2}\,g}{\sqrt2},$$

3.47 N m for our second blade, at every wind. The reason: at the best brake the generator's torque and the torque of the net stiffness (spring minus inertia) are equal in size and 90° apart, and together they balance gravity's push, whose largest torque is the weight at the centre of mass times its lever, $\tfrac{ml}{2}g$; each of the two therefore carries $1/\sqrt2$ of it. That is the torque the generator must be built to resist.

Second, the best brake itself. In physical units $c^* = \kappa^*I\Omega = \left(\tfrac{ml}{2}r_p - I\right)\Omega$, and on a large rotor, where $r_p \gg l$,
$$c^* \approx \frac{ml}{2}\,r_p\,\Omega: \tag{2.6}$$

the first moment times the speed of the hinge. The generator has to brake as hard as that, which chapter 7 finds is the hardest part of building it.

Third, the power on a large rotor:
$$P^* \approx \frac{\tfrac{ml}{2}\,g^2}{4\,\Omega r_p} = \frac{\tfrac{ml}{2}\,g^2}{4\,v_{\rm tip}}. \tag{2.7}$$

It depends on the second blade only through its first moment, and on the turbine only through the speed of the hinge, $v_{\rm tip} = \Omega r_p = \lambda^*v$. The faster the hinge moves, the less: a stiffer centrifugal spring lets gravity move the second blade less. So the second blade gives more in weaker wind, when the rotor turns slower.

## 2.4 On our blade

[On our blade] Table 1 gives the three winds for the 1 kg, 1 m second blade: the rotor, gravity's number $G$ ($R$ and the best brake $\kappa^* = R - 1$ are the same at every wind: the centrifugal spring and the second blade's inertia at the push frequency both grow as $\Omega^2$, so their ratio does not change; the brake constant $c^* = \kappa^*I\Omega$ does grow with the wind), the best brake constant $c^*$, the swing $\Theta^*$ of (2.2) at that brake, $P^*$ from (2.5), and the full nonlinear model of chapter 3 at the same brake.

[TABLE:  Table 1. The second blade at the three winds, at its best brake. At every wind $R = 94.5$ and $\kappa^* = R - 1 = 93.5$; full: the full nonlinear model of chapter 3 at the same brake. ]

The closed form (2.5) is within 0.31 % of the full model at every wind. Equation (2.7) alone, with $v_{\rm tip}$ in place of $\Omega r_p$, gives 265.4, 199.0 and 159.2 mW: within 1.1 % of (2.5), because $l$ is 63 times shorter than $r_p$.

How far can the small-swing theory be trusted? Figure 6 puts it against the full equation (1.5), with $\sin\theta$ and $\cos(\varphi+\theta)$ kept whole. Near the best brake the two agree to 0.3 % at every wind. They part where the second blade swings furthest: at a light brake in weak wind. At 6 m/s and a brake of 0.05 $\kappa^*$ the swing reaches 0.31 rad, and the full equation gives 11 % more power than (2.3); at 10 m/s, with a swing of 0.11 rad, only 1.3 %. Across the three winds the excess is 1.1 to 1.2 times the swing squared, $\Theta^2$. That is the fingerprint of what (2.1) threw away. The terms $\theta^3$ in $\sin\theta$ and $\theta^2\cos\varphi$ in gravity's push are of higher order in the swing; the one first-order term dropped, $\theta\sin\varphi$, moves the second blade at 0 and 2 times the push frequency, not at the push frequency itself (section 2.1), so it reaches the power only at second order too. The error must therefore grow as $\Theta^2$, and it does.

The right half of Figure 6 shows what the theory misses at the best brake. The timing of the swing is right, and so is its size, 0.215 rad at 6 m/s. But the full swing is lowered as a whole, by −0.024 rad on average, which is most of the difference between the two curves (what remains is 0.0113 rad rms). The second blade does not swing about the mother blade's line: it swings about a line slightly behind it. A linear theory cannot produce a constant offset from a push that averages to zero; it takes the second-order terms. Section 3.2 shows that this small lean is precisely what makes the rotor pay.

[FIGURE:  Figure 6. The small-swing theory against the full equation (1.5), solved by the simulation's own engine ( tools/compare.js ). First panel: harvested power over its maximum $P^*$ (2.5), against the brake over the best brake. The line is formula (2.3), the same for every wind; the dots are the full equation at 6 (wine), 8 (ochre) and 10 m/s (blue). Second panel: one turn of the swing at the best brake; solid the full equation, dashed the theory (2.2). The two have the same shape and the same phase; the full swing is shifted down by its mean trail. ]

## 2.5 Resonance is out of reach

The second blade is never near resonance. Its stiffness is $R = 3r_p/(2l)$, so the net stiffness $R - 1$ falls to zero only for $l = \tfrac32 r_p$, a second blade half as long again as the mother blade. For any second blade no longer than its mother blade, $R \ge \tfrac32$, and for ours $R - 1 = 93.5$. At resonance the small-swing power would grow without limit as the brake weakens, so it is worth saying why that route is closed: the centrifugal spring of a body hinged at the tip of a long blade is always much stiffer than the inertia it must overcome at the push frequency. Two ways of softening it exist on paper, tilting the hinge out of the rotor plane and adding inertia through the generator's gearbox (chapter 7); for a rod at the tip of a 63 m blade both would have to cancel a stiffness of about 90, and these notes do not pursue them.




# 3 Big swings, the bill, and chaos

Chapter 2 dropped every term that is not linear in $\theta$. This chapter solves the full equation, finds out who really pays and how, asks where along the second blade its mass is best placed, and whether chaos can help.

## 3.1 The full equation, solved numerically

[Picture] Push a spoon slowly through thick honey and it moves calmly; flick it and the honey stops it almost at once. A heavily braked blade has both kinds of motion at once: a slow swing, and a very fast relaxation of any motion the brake fights. That makes its equation "stiff".

Equation (1.5), with $\sin\theta$ and $\cos(\varphi+\theta)$ kept whole, is integrated step by step on a computer. A simple step-by-step method that only looks at the present moment (an explicit method, such as the classical Runge–Kutta method) must take steps shorter than the fastest relaxation, or its errors grow without bound. Here that relaxation is fast indeed: at the best brake a disturbance of the swing dies in $1/(\kappa^*\Omega)$, 0.011 s at 8 m/s, while one turn lasts 6.55 s. An implicit method instead solves, at each step, for the state at the end of the step, and stays stable with steps as long as the slow swing allows. These notes use one such method, a three-stage Radau IIA method of fifth order. On this equation its error falls on average 5.2 powers of two each time the step is halved, its torques agree with Newton's law summed over the second blade to 4·10⁻¹⁵, and after the start-up it agrees with an independent high-accuracy solver to 2·10⁻¹² in the harvested energy. (From rest, the first turns carry a start-up error of 8·10⁻⁷: the brake's relaxation is shorter than one step of 240 per turn. It dies away in the 60 turns the runs let pass before they measure.)

The closed form (2.5) is within 0.31 % of the full model at every wind, although the second blade swings up to 0.214 rad (12.2°). Two reasons make the agreement plausible. At second order in the swing three effects appear: the term $-\tfrac12G\theta^2\cos\varphi$ changes gravity's push itself, by about $\Theta^2/4$ of it; the cubic term of $\sin\theta$ softens the spring; and the mean trail of section 3.2 feeds back through $-G\bar\theta\sin\varphi$. These notes have not measured the three separately; the full model shows only their sum. They partly cancel, and what remains acts near the flat top of Figure 5, where a small change in the push or the stiffness moves the best brake but hardly the best power.

## 3.2 The second blade trails, and that is the bill

One effect of the dropped terms is visible and easy to derive: on average, the second blade is not straight out along the mother blade. Keep the gravity term to second order, $G\cos(\varphi+\theta) \approx G\cos\varphi - G\theta\sin\varphi$, and average (1.5) over a steady turn. The averages of $\theta''$, $\theta'$ and $\cos\varphi$ vanish, and what is left is
$$R\,\bar\theta = G\,\langle\theta\sin\varphi\rangle, \tag{3.1}$$

with $\theta$ on the right the swing (2.2), $\theta = -\Theta\cos(\varphi-\delta)$. Its average with $\sin\varphi$ is $-\tfrac12\Theta\sin\delta$, and (2.2) gives $\sin\delta = \kappa\Theta/G$, so
$$\bar\theta = -\frac{\kappa\,\Theta^2}{2R}, \qquad\text{at the best brake}\quad \bar\theta = -\frac{G^2}{4R(R-1)}. \tag{3.2}$$

The minus sign means the second blade trails behind the mother blade's line, against the direction of rotation, like a weight towed behind a boat.

Now compare (3.2) with the harvested power (2.3), $\bar P = I\Omega^3\cdot\tfrac12\kappa\Theta^2$. The same combination $\kappa\Theta^2$ appears in both, and since $IR = \tfrac{ml}{2}r_p$, for every brake setting
$$\boxed{\bar P = -\,\frac{ml}{2}\,r_p\,\Omega^3\,\bar\theta.} \tag{3.3}$$

The trail is the bill. In fact the exact version, $\bar P = -\tfrac{ml}{2}r_p\Omega^3\langle\sin\theta\rangle$, holds for any steady swing, large or small, with the ideal brake: the rotor's torque of section 1.4 is $-\tfrac{ml}{2}r_p\Omega^2\sin\theta + mgr_p\cos\varphi$ plus terms that are exact time derivatives, and over a steady turn those and $\cos\varphi$ average to zero. (With the geared generator of chapter 7 the identity changes, because the gearbox's own torque enters the rotor's.) There is a picture behind it. The second blade, flung outwards, pulls on the hinge, in the direction pointing from the hub to its own centre of mass, with the force $m\Omega^2$ times that centre's distance from the hub. When the second blade trails, its centre of mass sits a little behind the mother blade's line, so that pull, applied at the hinge, is no longer aimed straight away from the hub: it has a lever arm about the hub, $r_p$ times the sine of the small angle between the two lines, and it pulls the rotor backwards. Worked out, its torque is $\tfrac{ml}{2}r_p\Omega^2\sin\theta$, the term in the rotor's torque above. The rotor must push against it, all the time, and that steady push is the power it pays.

[On our blade] At 6 m/s, where the swing is largest, (3.2) gives $\bar\theta = −0.0229$ rad, a trail of 1.31°; the full model gives −0.0231 rad. In all nine runs of the full model (three winds, three brakes) the exact identity holds to 1·10⁻¹².

## 3.3 Where the mass sits

[Picture] Swing a hammer held at the very end of its handle, then grip the same hammer halfway up. The second swing is easier and weaker: the same mass now sits closer to your hand, so it has less leverage. Spreading the second blade's mass along its length does the same thing to it.

Section 1.3 noted that the equation holds for any rigid body on the hinge, with its own moment of inertia $I_p$ and first moment $Ml_c$. Redo chapter 2 for such a body: the inertia $I$ becomes $I_p$, the first moment $ml/2$ becomes $Ml_c$, and (2.5) becomes
$$P^*_{\rm rigid} = \frac{(M\,l_c\,g)^2}{4\,\Omega\,(M\,l_c\,r_p - I_p)}. \tag{3.4}$$

On a large rotor this is simply proportional to the first moment $Ml_c$, as (2.7) said for the rod. So the same mass placed farther from the hinge gives more, in proportion to the distance of its centre of mass. A uniform blade has its centre of mass halfway out; the same mass in a lump at its end would have it all the way out, and gives, from (3.4), 2.011 times as much as the uniform blade, almost exactly twice. A real second blade is neither: like the mother blade it tapers, so its centre of mass sits nearer the hinge than halfway, and it gives somewhat less than a uniform one. If the second blade's only job were to harvest, it should be heavy at its tip; a blade shaped for the air is the opposite.

[Check] For the point bob, $I_p = mL^2$ and $Ml_c = mL$, and (3.4) is the bob's $mLg^2/(4\Omega|r_p - L|)$. For the uniform rod, $I_p = ml^2/3$ and $Ml_c = ml/2$, and (3.4) is (2.5).

## 3.4 Chaos and the harvest

[TABLE:  Table 2. The largest Lyapunov exponent per turn, the largest over the starts, at each wind and brake; beside it the decay rate per turn of a small disturbance of the braked spring, $2\pi\,\max\,\mathrm{Re}\,s$ with $s^2 + \kappa s + R = 0$. ]



Part IIRandomness: shaking, gusts and a bending blade

# 4 A ceiling on random shaking

Wind is gusty, and a blade in gusty wind shakes. Could the second blade, perhaps moving chaotically, turn that randomness into extra power? Before any model of the wind, one exact result sets a limit. To keep it clean, this chapter treats a body (or a chain of bodies) hinged to a point that is shaken at random while it hangs in gravity, with no rotor; the last paragraph says what carries over to the turning blade.

## 4.1 Random kicks add energy through their square

[Picture] Stand on a bus over a rough road with a cup of coffee. Every jolt kicks the coffee, sometimes with its slosh and sometimes against it. On average the "with" and "against" cancel, yet the coffee still sloshes harder the rougher the road: a kick adds kinetic energy even when it is equally likely to help or oppose the motion, because energy goes as the square of velocity.

Start with the simplest case, a small mass $m$ that can move only along a direction $\hat t$ (across its rod). Shake its pivot to and fro along a direction $\hat e$. In the pivot's frame each jolt is a sudden extra force on the mass; over a short time it changes its velocity along $\hat t$ by a small random amount $\Delta v$. The kinetic energy $\tfrac12 m v^2$ changes by $m v\,\Delta v + \tfrac12 m\,\Delta v^2$. The first term is as often negative as positive and averages to zero. The second is never negative. If the shaking's strength is $S$ (in m²/s³: the spread, the variance, of the velocity kicks it gives per second), the kicks along $\hat t$ have variance $S(\hat e\cdot\hat t)^2$ per second, and the shaking feeds in, on average, the power $\tfrac12 S\,m(\hat e\cdot\hat t)^2$. That is the whole idea. The next paragraphs say the same for any body or chain of bodies, in the language of Lagrangian mechanics; readers who skip them lose nothing but the proof, and can go on to the result (4.2) and its plain-words form after (4.4).

Shake the pivot along a fixed direction $\hat e$ with acceleration $a(t)$. In the pivot's frame every piece of mass $dm$ feels an extra force $-a(t)\,\hat e\,dm$. For a body (or a chain of bodies) with angles $q_k$, that force enters Lagrange's equations as a generalised force
$$Q_k = -a(t)\,b_k(q), \qquad b_k = \int \hat e\cdot\frac{\partial \mathbf x}{\partial q_k}\,dm = \frac{\partial}{\partial q_k}\left(M\,\hat e\cdot\mathbf x_{\rm cm}\right), \tag{4.1}$$

the rate at which turning the angle $q_k$ moves the whole mass $M$ along the shaking, through its centre of mass $\mathbf x_{\rm cm}$. Let the shaking be white noise of strength $S$: kicks so quick and so uncorrelated that $\langle a(t)a(t')\rangle = S\,\delta(t - t')$ (the Dirac delta $\delta$ says that the shaking at two different instants is unrelated, however close the instants are). Over a short time $dt$ the momenta $p_k = \partial\mathcal L/\partial\dot q_k$ of the angles receive a random kick $\Delta p = -b\,\sqrt{S}\,dW$, where $dW$ is a random number of mean zero and variance $dt$. Why $\sqrt{dt}$? Within $dt$ there are many independent tiny kicks; like the steps of a random walk, their sum grows as the square root of their number, so as $\sqrt{dt}$, and its square is of order $dt$. That is why the square of the kick, which would be negligible for a smooth force, survives here. The kinetic energy is $K = \tfrac12 \dot q^{\mathsf T}A\,\dot q = \tfrac12 p^{\mathsf T}A^{-1}p$, with $A(q)$ the mass matrix (for one rigid body on its pivot, simply its moment of inertia). Expand to second order in the kick:
$$\Delta K = \dot q\cdot\Delta p + \tfrac12\,\Delta p^{\mathsf T}A^{-1}\Delta p.$$

The first term averages to zero: the kick is as likely to help as to oppose. The second does not: its average is $\tfrac12 S\,b^{\mathsf T}A^{-1}b\,dt$. So on average the shaking feeds in the power
$$\boxed{P_{\rm in} = \frac S2\,\big\langle m_{\rm eff}\big\rangle, \qquad m_{\rm eff} = b^{\mathsf T}A^{-1}b.} \tag{4.2}$$

Nothing else entered: not the stiffness, not the damping, not gravity, not whether the motion is regular or chaotic. In a steady state everything fed in is dissipated, and the generator is where it is dissipated. (One subtlety of random kicks is that the result can depend on whether the kick is evaluated at the start or in the middle of each step; that matters only when the kick's strength depends on the velocity it kicks. Here $b$ depends only on the angles, so the two readings agree. The algebra is checked in SymPy for a bob, for two bobs on two rods, and for the uniform rod.)

## 4.2 The effective mass never exceeds the real mass

$m_{\rm eff}$ measures how much of the body's mass the shaking can grab. For one body on its pivot it is $b^2/I_p$. For a small bob, $m_{\rm eff} = m(\hat e\cdot\hat t)^2$: the full mass when the bob can move along the shaking, none when its rod points along it. For our second blade, $b = \tfrac{ml}{2}\cos\psi$, where $\psi$ is the angle between the shaking and the direction the blade's pieces move, and
$$m_{\rm eff} = \frac{\left(\tfrac{ml}{2}\right)^2\cos^2\psi}{ml^2/3} = \tfrac34\,m\cos^2\psi \le \tfrac34\,m.$$

A uniform blade can give the shaking at most three quarters of its mass: its pieces near the hinge hardly move, and pay for their share of the kinetic energy without catching their share of the kicks. In general, the proof takes three lines. For any velocity $\dot q$, the pieces move with velocities $\mathbf v$, the kinetic energy is $\tfrac12\dot q^{\mathsf T}A\dot q = \tfrac12\int|\mathbf v|^2dm$, and $b\cdot\dot q = \int\hat e\cdot\mathbf v\,dm$. Then
$$m_{\rm eff} = \max_{\dot q}\frac{(b\cdot\dot q)^2}{\dot q^{\mathsf T}A\dot q} = \max\frac{\left(\int\hat e\cdot\mathbf v\,dm\right)^2}{\int|\mathbf v|^2dm} \le \frac{\left(\int dm\right)\left(\int(\hat e\cdot\mathbf v)^2dm\right)}{\int|\mathbf v|^2dm} \le M_{\rm total}, \tag{4.3}$$

The first step is itself the Cauchy–Schwarz inequality, in the product $u^{\mathsf T}Av$: $(b\cdot\dot q)^2 \le (b^{\mathsf T}A^{-1}b)(\dot q^{\mathsf T}A\dot q)$, with equality at $\dot q = A^{-1}b$. The second is Cauchy–Schwarz again, and the third holds because $(\hat e\cdot\mathbf v)^2 \le |\mathbf v|^2$. Equality needs every piece to move along $\hat e$, all with the same velocity: the body must be able to carry all of its mass along the shaking at once, which a body turning on a hinge never can. So
$$P_{\rm in} \le \frac S2\,M_{\rm total}, \qquad\text{and for the second blade}\quad P_{\rm in} \le \frac S2\cdot\frac34\,m. \tag{4.4}$$

In plain words: random shaking cannot feed in more than $S/2$ times the body's mass, whatever the body does, regular or chaotic, and a rod on a hinge takes at most three quarters of that.

[Check] A computer experiment on the general theorem, made for an earlier version of this study: a bob of 0.1 kg on 0.2 m and a double pendulum of the same mass and reach hang in gravity, braked with a damping ratio of 0.2, and their pivot is shaken sideways with white noise of strength $S = 0.028$ m²/s³ (gentle: swings of 0.05 rad) or $S = 48$ m²/s³ (violent: swings of more than a radian, the double's top rod tumbling right over about a hundred times in each 40-second window). For each case 1000 independent runs compare the generator's power with $\tfrac S2\langle m_{\rm eff}\rangle$: they agree within 0.22 to 0.65 %, at statistical errors of 0.4 to 0.7 %. In the violent runs $\langle m_{\rm eff}\rangle$ falls to 0.48 of the total mass for the bob and 0.55 for the tumbling double. The rod's value $\tfrac34 m\cos^2\psi$ is checked in SymPy.

On the turning blade the second blade is also driven by gravity's once-per-turn push, paid for by the rotor. The noise's own feed is still (4.2), whatever else drives the motion, because its first-order term averages to zero in any state. But the noise also changes the motion, and with it what gravity's push feeds in, which can rise or fall; (4.4) bounds the noise's own feed, not that indirect change. The mother blade's edgewise shaking, in the rotor plane and across the mother blade, is at right angles to a second blade lying along it, so the second blade starts with its full effective mass, $\tfrac34 m$; any wandering can only lower it. A real blade, though, does not shake as white noise: it shakes mostly near its own edgewise frequency, about 1.08 Hz on the 5 MW reference turbine of chapter 5 (1.0793 Hz in Jonkman et al. 2009, Table 9-1). Then what matters is how the second blade responds near that one frequency, and shaking at one slow frequency acts like a push, as gravity's does. Chapter 6 works it out.

# 5 Gusts and the rotor's speed

So far the rotor turned at a steady speed. In gusty wind it does not: a gust speeds it up over some seconds, a lull slows it down. To see what that does to the second blade we need the turbine's own dynamics and a real wind.

The NREL 5 MW turbine's rotor and generator together have a moment of inertia $J = 4.38\times10^7$ kg m², and the rotor's speed obeys $J\dot\Omega = Q_{\rm aero} - Q_{\rm gen}(\Omega)$: the wind's torque, $Q_{\rm aero} = \tfrac12\rho\pi r_{\rm rot}^3v^2C_p(\lambda)/\lambda$ with the tip-speed ratio $\lambda = \Omega r_{\rm rot}/v$ and the power coefficient $C_p(\lambda)$ from NREL's published table, against the generator's torque, which the controller sets as a function of $\Omega$. At a steady 8 m/s the two torques balance at 9.07 rpm, 1.0 % below the $\lambda^*v/r_{\rm rot}$ of section 0.7, because the controller's torque law holds the rotor a little off its best tip-speed ratio. The wind is the standard model of gusty wind used to design turbines (IEC 61400-1, edition 3, turbulence class A, as implemented in NREL's TurbSim): at 8 m/s its speed fluctuates with a standard deviation of 1.86 m/s, with the Kaimal spectrum, mostly over tens of seconds. The rotor feels the average over its disc: two points of the disc a distance apart fluctuate together only at low frequencies (the IEC coherence), so the disc average is smoother than the wind at the hub. In 40 ten-minute records the rotor's speed wanders about its mean with a standard deviation of 10.3 % of the mean.

[Picture] A metronome on a train that slowly speeds up and slows down keeps its own beat, so a push timed to the train's wheels would drift in and out of step with it. Our second blade's beat, $\sqrt R$ per turn, and gravity's push, once per turn, both ride on the rotor's speed, so the two stay in step whatever the rotor does.

The gusts reach the second blade in two ways. They make the rotor speed up and slow down, which adds a small torque (the Euler terms of (1.3), with $\ddot\varphi$); and they move the rotor's speed away from its steady value, which changes the power through (2.3). The first is negligible: it changes the power by about 2 parts in 10 000. The second has two parts. With the generator constant fixed, the power at speed $\Omega$ is, from (2.3) with $\kappa = \kappa^*$ at the steady speed $\Omega_0$, exactly $\bar P(\Omega)/\bar P(\Omega_0) = 2/(1 + \Omega^2/\Omega_0^2)$. Its slope at $\Omega_0$ is $-1$: a shift of the mean speed by a fraction $\epsilon$ changes the power by $-\epsilon$. And it curves upwards (its second derivative in $\Omega/\Omega_0$ is $+1$ there), so a speed that wanders about a fixed mean raises the average power, whichever way it wanders: by about $s^2/2$ for a relative spread $s$, 0.53 % here.

[On our blade] Each of the 40 records is run twice through the full equation of the second blade at the tip, once with the Euler terms and once without, and compared with steady rotation at the record's own mean speed and at the steady speed. With a pure square-law controller ($Q_{\rm gen} \propto \Omega^2$) the second blade gains +0.77 % over steady operation at 8 m/s: the wandering speed gives +0.90 %, more than the 0.53 % the curvature alone predicts (these notes have not separated where the rest comes from), and the mean speed moves by +0.11 % and costs −0.11 %, as the slope of $-1$ predicts. With the turbine's full controller the result changes sign, to −1.99 %: at 8 m/s the full controller works just above a kink in its torque law, at 8.98 rpm. Below the kink the generator's torque falls away steeply, so in a lull the rotor is braked less and slows less than it speeds up in a gust; the average speed rises by +2.60 %, and the power falls by −2.55 %, again as the slope predicts, while the wander still adds +0.53 %. That is a property of this turbine's controller, not of the wind. Either way, gusts change the second blade's power by a few per cent at most.

# 6 The blade bends and shakes

A real blade is not rigid. It bends under its own weight, once per turn, and it shakes in gusty wind near its own edgewise frequency. Both move the hinge, and at the tip they move it most.

## 6.1 The sag: a large push that cancels itself

[Picture] Hold a long, springy ruler out sideways and turn your wrist slowly: the ruler sags first one way and then the other, following gravity, and its end sags most. A blade 61.5 m long does the same as it turns, in its own plane.

From the NREL blade's mass and stiffness tables, gravity bends it edgewise by 431 to 467 mm at the tip, depending on how the bend's shape is taken, once per turn and in step with gravity's push. The hinge therefore moves sideways by $w\cos\varphi$. Put a moving hinge into the Lagrangian of chapter 1 and linearise (done in SymPy): the hinge's motion adds $2\Omega^2w$ to gravity's push $g$, once from the hinge's own acceleration and once from the shift of the centrifugal pull as the hinge moves sideways, exactly as it would for a bob. On its own that would raise the power by 16.9 to 18.4 % (the power goes as the square of the push, (2.5)).

But a bending blade also turns: its cross-section rotates with the slope of the bend, and at the tip the slope is largest. The generator's stator, fixed in the mother blade, rotates with it. The generator brakes the second blade's motion relative to the stator, $-c(\dot\theta - \dot\beta)$, where $\beta$ is the section's angle; so the turning stator drags on the second blade with the extra torque $c\dot\beta$. That drag follows the rate of change of the bend's slope, a quarter turn out of step with the sag's push, while at the best brake the swing lags its push by 45° (section 2.3); so part of the drag works against the swing. The two effects largely cancel. What is left is a small difference of two large numbers, so it depends on the exact shape of the bend: taking the shape from the blade's first mode of vibration, or integrating the static bend directly from the same blade tables, gives a net change of +2.2 to +3.5 %. (For the first shape, linear theory and a full nonlinear run with the moving, turning hinge agree within 0.2 percentage points.) The lesson: a generator brakes motion relative to its own frame, so when that frame moves, the frame's motion counts too.

## 6.2 Random shaking

Gusts make the blade's first edgewise mode vibrate near 1.08 Hz. How strongly, no source we could open says for this blade, so the notes take a range: a tip vibration of 5, 20 or 100 mm rms. The model has two parts, coupled both ways. The blade's first edgewise mode is one oscillator: a modal mass of 1416 kg on a spring tuned to 1.08 Hz, with a damping ratio $\zeta_b$ of 0.5 % or 3 % of critical, driven by a random force whose spectrum is flat near 1.08 Hz and scaled so that the blade alone would vibrate at the stated tip level. At the tip the hinge moves sideways with the tip itself, and the section turns by 28.1 mrad per metre of tip motion. The second blade is (2.1) with its hinge shaken sideways and its stator turned by that much, and it pushes back on the blade's mode with the force and torque it needs. Gravity's push is left out of this part (it is in chapter 2 and section 6.1). Everything is linear, so the response is computed frequency by frequency, and the generator's mean power is the brake times the mean square relative speed. The full linear equations, with the second blade integrated along its length and the turning frame's centrifugal and Coriolis terms, were derived in SymPy. Since the model is linear, the swing from shaking and the swing from gravity add; but the brake that takes most from shaking is not the one that takes most from gravity (1.89 N m s against 29.6 N m s), so the two best powers cannot simply be added. The model checks that the second blade never takes more than the gusts feed into the blade.

[On our blade] At a 5 mm tip vibration the gusts feed 0.110 W into the blade's vibration, and the 1 m second blade, at its best brake for the shaking, takes 3.38 mW of it, against 202 mW from gravity. At 20 mm it takes 54.2 mW; at 100 mm, the top of the range, 1 350 mW, more than gravity gives. Chaos plays no part: at $R$ near 94 the second blade is held firmly along the mother blade.

The 1 m second blade takes so little at small vibrations because its own frequency, $\sqrt R$ times the rotor's, is 1.36 times the blade's: it is far from the blade's resonance. A second blade tuned to the blade, with its own frequency equal to 1.08 Hz at the mean rotor speed, needs $\Omega\sqrt{3r_p/(2l)} = \omega_e$, a length of 1.85 m. With the same mass per metre it weighs 1.85 kg. It is then a tuned mass damper, the device that calms swaying skyscrapers, and it draws on the blade's vibration directly.

[On our blade] At a 5 mm tip vibration and a blade damping of 0.5 % the tuned second blade takes 64.6 mW, 59 % of what the gusts feed into the blade, and calms the blade's tip motion by 36 %; at 3 % blade damping it takes 85.1 mW. Its swing is 0.06 rad rms. Three catches. First, the rotor's speed wanders by 10.3 %, and the tuned blade's frequency wanders with it while the mother blade's does not; averaged over that wander the gain falls to 25.0 mW. Second, at 20 mm of tip vibration the linear model asks it to swing 0.22 rad rms; at 100 mm, 1.11 rad, where a linear model no longer describes it. Third, and worst, this model leaves gravity out of the stiffness. Gravity's term $-G\theta\sin\varphi$ (section 2.1) stiffens and softens the second blade once per turn, by $\pm G/R$ of its stiffness, so by $\pm G/(2R) = \pm1/(2\Gamma) = \pm8.6$ % of its frequency at 8 m/s, whatever its length, while the blade's resonance is only 1 to 6 % wide (twice the damping ratio). So the tuned blade is detuned and retuned every turn, and its true gain may be somewhat below these numbers or several times below them. The tuned second blade is an idea these notes have not shown to work; only a calculation in time, with gravity kept whole, can say how much of it survives. For comparison, the longer blade also takes 698 mW from gravity alone, simply because its first moment is larger.




# 7 From swing to watts

Every chapter so far has treated the generator as a perfect brake: a torque $-c\dot\theta$ that takes the power $c\dot\theta^2$ and loses none of it. A real generator is a small electric motor driven backwards, behind a gearbox. This chapter takes one from a catalogue, puts it in the hinge, follows the power from the swinging second blade to the wires of the sensor, and then sizes the second blade to suit it.

## 7.1 A generator is a brake

[Picture] A bicycle dynamo pressed against the tyre makes the wheel harder to turn when the lamp is lit, and harder still if you join its two wires together; with the wires loose it spins almost freely. What pushes back on the wheel is the electric current.

A small motor with permanent magnets has two constants. Turning its shaft at angular speed $\omega_m$ induces a voltage $e = k_e\,\omega_m$ in its coil (the back-EMF). A current $i$ in the coil gives a torque $k_t i$ on the shaft. The two constants are equal in SI units, because the electrical power $ei$ and the mechanical power $k_ti\,\omega_m$ are the same power. Connect a load resistor $R_L$: the current is $i = e/(R_c + R_L)$, where $R_c$ is the resistance of the coil itself. The torque on the shaft is then $k_tk_e\,\omega_m/(R_c + R_L)$, proportional to the speed: exactly the brake of chapter 1. (The coil's inductance would delay the current by $L_c/R_c = 0.12$ ms, nothing next to a swing that lasts seconds, and is left out.)

Between the second blade and the motor sits a gearbox of ratio $N$: the motor turns $N$ times for each turn of the hinge, $\omega_m = N\dot\theta$, and its torque reaches the second blade multiplied by $N$. The ratio therefore enters twice, once in the voltage and once in the torque, and the brake constant at the hinge is
$$c_e = \frac{N^2\,k_t\,k_e}{R_c + R_L}. \tag{7.1}$$

The power $c_e\dot\theta^2$ is the electrical power $ei$, and the current shares it between the coil and the load in proportion to their resistances. The load gets the fraction $R_L/(R_c + R_L)$. Call $c_{\rm sc} = N^2k_tk_e/R_c$ the brake with the wires joined ($R_L = 0$, the "short circuit"): it is the strongest brake this motor can give through this gearbox. Since $R_L/(R_c+R_L) = 1 - c_e/c_{\rm sc}$,
$$P_{\rm load} = c_e\left(1 - \frac{c_e}{c_{\rm sc}}\right)\langle\dot\theta^2\rangle. \tag{7.2}$$

This is section 2.3's contest once more, now inside the generator: a brake near the short circuit takes plenty of power but burns it in its own coil; a light brake sends nearly all of it to the load but takes little.

[On our blade] Take the maxon RE 25, a 25 mm, 20 W motor, in its 24 V winding (catalogue part 339152): $R_c = 1.53$ Ω, $k_t = 20.8$ mN m/A, and a speed constant of 460 rpm/V, which is $k_e = 60/(2\pi\cdot460) = 0.02076$ V s; the two constants agree to the catalogue's rounding, two parts in a thousand. Without a gearbox its strongest brake is $c_{\rm sc} = k_tk_e/R_c = 0.000282$ N m s. The best brake of chapter 2, (2.6), is 22.4 to 37.4 N m s: some 79 000 to 130 000 times more. Because the brake grows as $N^2$, a ratio of at least 282 to 364 is needed just to reach the best brake with the wires joined. The reason is the shape of the job. At the best brake the second blade pushes with 3.47 N m (section 2.3) while its hinge turns at most about a tenth of a radian per second; a small motor is built to give a hundredth of that torque (the RE 25's rated torque is 30.4 mN m) at thousands of rpm. The gearbox converts one into the other.

## 7.2 What the gearbox costs

[Picture] Turn the crank of a hand-held egg beater. The beaters are light, yet the crank feels heavy when you start and stop it, because each turn of the crank spins the beaters four times. Seen from the slow side, everything on the fast side of a gearbox is magnified: a torque by $N$, and an inertia by $N^2$.

The gearbox that makes the brake strong enough brings three costs.

Inertia. The motor's rotor, of moment of inertia $J$, turns at $N\dot\theta$, so its kinetic energy is $\tfrac12JN^2\dot\theta^2$: to the second blade it is an extra moment of inertia $JN^2$ about the hinge. In the units of chapter 1, where the second blade's own is $I$, it adds
$$j = \frac{J\,N^2}{I}. \tag{7.3}$$

It does not feel the centrifugal pull or gravity, because the motor's rotor sits on the hinge's axis; it only resists being accelerated. In (2.2) the second blade's inertia gave the $-1$ of the net stiffness $R - 1$; the rotor adds its own, and the net stiffness becomes $R - 1 - j$.

Friction. Brushes and bearings resist turning with a torque $T_0$ that hardly depends on speed. Through the gearbox it reaches the second blade as $NT_0$.

Gear losses. A gearhead's efficiency $\eta$ is the fraction of the power it passes on, whichever way the power flows. While the second blade drives the motor, every torque the motor side needs costs the second blade $N/\eta$ times that torque, not $N$ times; while the motor's spinning rotor slows down and gives its energy back, the second blade receives only $\eta$ of it. In the formula below we keep the simple part: the brake the second blade feels is $c_e/\eta$ and the friction $NT_0/\eta$, and the rotor's inertia passes without loss. The full equation of section 7.4 charges the loss on every flow.

Put the three into (1.5): the rotor's inertia joins $\theta''$, the brake becomes $\kappa_e/\eta$, and the friction is a torque of constant size $f$ that always opposes the swing:
$$(1 + j)\,\theta'' + \frac{\kappa_e}{\eta}\,\theta' + f\,\mathrm{sgn}\,\theta' + R\sin\theta + G\cos(\varphi + \theta) = 0, \qquad \kappa_e = \frac{c_e}{I\Omega},\quad f = \frac{N\,T_0}{\eta\,I\Omega^2}. \tag{7.4}$$

In these units gravity's largest torque, $\tfrac{ml}{2}g$, is $G$, so $f/G = NT_0/(\eta\,\tfrac{ml}{2}g)$ compares the friction with the push that drives the swing, and it is the same at every wind. If $f \ge G$ the friction is stronger than gravity can ever push, and a second blade at rest never moves: the gearbox has jammed it.

[On our blade] The RE 25's rotor has $J = 14.7$ g cm², and the GP 32 C planetary gearhead adds 0.7 to 1.5 g cm² at its input. Through the largest catalogue ratio, 492 : 1, that gives $j = 1.12$: against a net stiffness $R - 1 = 93.5$, nothing. The catalogue gives no friction torque; the no-load current, 40.2 mA, gives an estimate $T_0 \approx k_ti_0 = 0.84$ mN m, measured at 10 900 rpm. The gearhead's catalogue efficiency is 80 % for one stage, 75 % for two, 70 % for three and 60 % for four. Through 492 : 1 (four stages) the friction at the hinge is 0.686 N m, 14 % of gravity's largest torque $\tfrac{ml}{2}g = 4.90$ N m. At the catalogue's friction the second blade would jam only beyond a ratio of 4 105 on a three-stage gearhead and 3 518 on a four-stage one: no catalogue ratio jams it.

Two of these numbers are less certain than the rest. The catalogue gives the gearhead's best forward efficiency, driven from the motor at its best load; driven backwards and lightly loaded, a gearhead can do worse. And friction measured at 10 900 rpm includes losses that grow with speed, so at the slow speeds here it may be lower. The first makes the numbers below optimistic, the second pessimistic. Only a test on a bench can settle them.

## 7.3 Friction as a brake that weakens

[Picture] Push a heavy box across the floor. The floor pushes back with the same force whether you walk or run, so it takes the same toll for every metre. A brake like the dynamo is different: it pushes back harder the faster you go.

Equation (7.4) is no longer linear, because of $\mathrm{sgn}\,\theta'$, but chapter 2's method still works with one more step. Suppose the second blade still swings as $\theta = -\Theta\cos(\varphi - \delta)$. The friction torque $f\,\mathrm{sgn}\,\theta'$ is then a square wave, $+f$ while the blade moves one way and $-f$ while it moves back, in step with $\theta'$. A square wave of height $f$ is a sum of sine waves at frequencies 1, 3, 5, …, the first of amplitude $4f/\pi$ and the others of $1/3$, $1/5$, … of it. Keep only the first, the one at the frequency of the swing. A damper $\kappa_f\theta'$ gives a torque of amplitude $\kappa_f\Theta$ in step with $\theta'$, so the friction acts like a damper with
$$\kappa_f = \frac{4f}{\pi\,\Theta}. \tag{7.5}$$

This is called the describing function of friction. It is a brake that weakens as the swing grows, since the toll per swing is fixed but the swing is longer. In (2.2), replace $R - 1$ by $R - 1 - j$ and $\kappa$ by $\kappa_e/\eta + \kappa_f$, and multiply through by $\Theta$:
$$\Theta^2(R - 1 - j)^2 + \left(\frac{\kappa_e}{\eta}\,\Theta + \frac{4f}{\pi}\right)^2 = G^2. \tag{7.6}$$

This is a quadratic equation for $\Theta$. It has a positive root only if $4f/\pi 
$$P_{\rm load} = I\Omega^3\,\kappa_e\left(1 - \frac{c_e}{c_{\rm sc}}\right)\frac{\Theta^2}{2}, \qquad P_{\rm rotor} = I\Omega^3\left[\frac{\kappa_e}{\eta}\,\frac{\Theta^2}{2} + \frac{2}{\pi}\,f\,\Theta\right]. \tag{7.7}$$

The last term is the friction's toll: torque times the mean speed $\langle|\theta'|\rangle = 2\Theta/\pi$.

[Check] Remove the losses: $f = 0$, $j = 0$, $\eta = 1$ and $c_{\rm sc}\to\infty$ (a coil without resistance). Then (7.6) is (2.2), and both powers in (7.7) become (2.3). Units: $\kappa_e$, $j$, $f$ and $G$ are pure numbers, and $I\Omega^3$ is a power.

## 7.4 On our blade

Formulas (7.6) and (7.7) give, at each wind and each catalogue ratio of the GP 32 C, the load resistor that gives the load the most power, with the swing kept below 0.5 rad and the peak torque at the hinge within the gearhead's continuous rating; ratios that jam are out. Then, as a second route, the full equation is solved with the method of section 3.1. It is (7.4) with the gear loss charged on every power that flows through the gearhead. Let $x$ be the torque the motor side needs, as felt through a perfect gear (in the units of (7.4), and without $\eta$ in the friction: $f_0 = NT_0/(I\Omega^2)$); the second blade feels $x/\eta$ while power flows into the motor side and $\eta x$ while it flows back:
$$\theta'' + R\sin\theta + G\cos(\varphi + \theta) + k\,x = 0, \qquad x = j\,\theta'' + f_0\,\mathrm{sgn}\,\theta' + \kappa_e\,\theta', \qquad k = \eta^{-\mathrm{sgn}(x\theta')}. \tag{7.8}$$

Because $\theta''$ appears on both sides, each step solves for it (the left side grows steadily with $\theta''$, so there is exactly one answer). Each sign is smoothed over a narrow band: a thousandth of the swing for $\mathrm{sgn}\,\theta'$, and a thousandth of the gear's own power scale for $\mathrm{sgn}(x\theta')$. The full equation is run at the formula's brake and at half and twice it, at every wind, and at 8 m/s with every other ratio at its own best brake; the rotor's work is integrated too, so the energy book closes in the full equation as well.

[On our blade] 
[TABLE:  Table 3. The maxon RE 25 with a GP 32 C gearhead in the hinge, at the ratio (492 : 1 at every wind) and load the formula (7.6)–(7.7) finds best. Swing and load are given as formula / full: the describing-function formula, and the full equation (7.8). Paid: what the rotor pays; the last two columns are the shares of it that reach the load and that friction takes. ]

The load receives 57 to 106 mW: 36 to 40 % of what the perfect brake of chapter 2 would take, and 35 to 39 % of what the rotor pays. The motor's friction takes 14 to 15 % of what the rotor pays; the gears and the coil take most of the rest. The largest ratio, 492, wins at every wind: a smaller one cannot brake hard enough without burning most of the power in the coil. Even so the motor brakes only 0.39 to 0.43 of the best brake (2.6), which is why the second blade swings wider than in chapter 2 and gives less. Even the poorest wind gives 1 522 times what the sensor of section 0.6 needs. The full equation agrees with the formula within 2.1 %, and of the three brakes tried, the formula's is the best or within 0.0 % of it.

How much do the two uncertain numbers of section 7.2 matter? By the formula: if the gearhead's own drag doubles the friction, the load gets 41 to 75 mW; if the backdriven efficiency is 50 % instead of the catalogue's 60 %, 46 to 84 mW; with both, 30 to 57 mW, still 811 times the sensor's need.

One more thing the sensor's designer must know: the voltage. The load sees an alternating voltage that peaks at 0.80 to 1.39 V and alternates once per turn, at 0.114 to 0.191 Hz, with the motor turning at most 743 rpm, far below the gearhead's limit of 8000 rpm. Turning that into the steady few volts a radio chip needs is a problem of electronics that these notes do not solve; the motor's graphite brushes also have a contact voltage drop of their own, which these notes do not model. The margins above are therefore before the electronics, and a bench test of the whole chain is the next step.

## 7.5 Sizing the second blade to its generator

Chapter 2 says the power grows with the second blade's first moment, and section 7.1 says the best brake grows with it too: $c^* \approx \tfrac{ml}{2}r_p\Omega$. A given generator can brake only so hard, so for a given generator there is a second blade it serves best. Too light a second blade asks for a brake the motor gives easily, but takes little; too heavy a one asks for more brake than the motor can give, or more torque than its gearhead may carry, and the motor takes only a small share of what the second blade could give.

[On our blade] With the length fixed at 1 m, the formula of section 7.3, at each mass of the series 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5 and 10 kg and at each wind, with the best ratio and load within the gearhead's rating, gives the load these shares of $P^*$ (mean over the three winds):

[TABLE:  Table 4. The share of the best power $P^*$ the RE 25 + GP 32 C delivers to its load, against the mass of a 1 m second blade; mean over the three winds, and the ratio and load power at 8 m/s. ]

The share peaks at 1 kg, which is the mass these notes use. Beyond 2 kg the largest ratio would exceed the gearhead's continuous torque, and the share collapses. With twice the catalogue's friction and a gear efficiency of 50 %, the 1 kg second blade still gives the sensor 811 times its need at the poorest wind.

## 7.6 Bigger second blades

[Picture] Hang a ruler and a plank side by side from the rim of a turning wheel. Both lean back by the same few degrees, because gravity's push and the outward pull both grow with how much mass sits how far from the hinge. But to hold the plank against its swing you need a far stronger hand than for the ruler.

Our second blade is light for a blade tip. The NREL blade itself weighs 10.3 kg per metre at its very tip, and its outer 3 m weigh 115 kg. Real devices fitted at blade tips are of the same build: retrofit tip extensions reach about one metre past the old tip and are about three metres long in all (a Vestas patent, US 10 927 809, listed with the sources below), and the pivoting tip brakes of small stall-regulated turbines are 5 to 20 % of the rotor radius long (US patent 8 403 641, also below). So it is worth asking what the formulas of chapters 2 and 7 give over that range. Table 5 runs them for lengths from half a metre to three metres and for four mass densities: a light hollow sensor blade (1 kg per metre), a light composite (3 kg per metre), the mother blade's own tip (10 kg per metre) and its build a metre further in (30 kg per metre).

[On our blade, and bigger ones] 

[TABLE:  Table 5. The second blade over the range of real tip devices: length $l$, mass per length, mass $m$, first moment $ml/2$; the best power $P^*$ (2.5) at 6 and 10 m/s; the generator torque $\tau^* = \tfrac{ml}{2}g/\sqrt2$ it must hold; the extra pull on the mother blade's tip at 10 m/s, $m\Omega^2(r_p + l/2)$; and what the RE 25 + GP 32 C delivers to its load at 6 m/s. The row in bold is the size these notes use. ]

Three things follow. First, the best power grows in proportion to the first moment $ml/2$, as (2.7) says: at 6 m/s from 66.7 mW to 74.0 W over the table. Second, the swing does not change: $\Theta^*$ at 6 m/s stays between 0.214 and 0.220 rad for every size. The reason is in (2.2): at the best brake $\Theta^* = G/[\sqrt2(R-1)]$, and gravity's push $G$ and the centrifugal stiffness $R$ both carry the same factor $\tfrac{ml}{2}/I$, so their ratio is $g/(\Omega^2 r_p)$ for any second blade much shorter than its mother blade, which gives 0.213 rad. Third, the torque the generator must hold, $\tau^*$, grows with the first moment too, from 0.867 to 936 N m. The RE 25 behind its gearhead cannot follow: once the first moment passes about half a kilogram-metre, it delivers 93.9 to 107 mW at 6 m/s whatever the size, because the gearhead's continuous torque, not the second blade, sets the limit. A bigger second blade needs a bigger generator, sized by $\tau^*$ and $c^*$ as in section 7.5. The largest blades of the table also pull on the mother blade's tip with up to 8.34 kN at 10 m/s, close to the pull of its own outer 3 m, 10.1 kN; such a device would need a check of the blade's structure, which these notes do not make. Ours adds 0.0912 kN.For the sensor, every size in the table is more than enough: through the RE 25 the poorest case, the smallest blade in the strongest wind, still gives 311 times its need. So the size these notes use, 1 kg on 1 m, is chosen by the generator and the structure, not by the power: it is the lightest second blade the catalogue generator serves fully.

# 8 The answer

## 8.1 The ceiling

[Picture] Lower a bag of shopping on a rope: the power you can take from it is its weight times the speed at which it falls, however it falls. The second blade is the same, with its weight acting at its centre of mass, $l/2$ from the hinge, and moving relative to the mother blade at the speed $\tfrac l2|\dot\theta|$.

All the chapters meet in one inequality. Watch the second blade from the turning mother blade, with the rotor's speed steady and the mother blade rigid. In this frame gravity does the work; seen from the ground, the same energy comes from the rotor (section 1.4). The two are one bookkeeping in two frames. There the centrifugal pull is a fixed field of force with a potential energy, so over a steady turn it gives as much as it takes; the Coriolis force is always at right angles to the motion and does no work. Gravity is the only force whose direction changes, and the only one that can feed the swing on average. Its torque on the second blade is $-\tfrac{ml}{2}g\cos(\varphi+\theta)$, never larger than $\tfrac{ml}{2}g$, so the power it feeds in, and with it every watt the generator can take, obeys
$$\bar P \le \frac{ml}{2}\,g\,\langle|\dot\theta|\rangle. \tag{8.1}$$

It holds for any motion: small swings or large, regular or chaotic, with any brake and any gearbox. (A rotor whose speed wanders, or a blade that shakes, adds a feed of its own; chapters 4 to 6 measured how little that gives, at the shaking levels the sources support. Air, left out of these notes, would add a feed of its own too.) To harvest more, the second blade must move faster, and a stiff centrifugal spring does not let it. At the best brake of chapter 2 the power is $P^* = \tfrac12\,\tau^*\,\Omega\Theta^*$ with $\tau^* = \tfrac{ml}{2}g/\sqrt2$, a fixed fraction, $\pi/(4\sqrt2) = 0.555$, of the right side of (8.1): the best brake already takes more than half of what gravity could ever give at that swing.

The inequality also names the one design lever that always works: the right side grows with the first moment $\tfrac{ml}{2}$. A heavier second blade, or one whose mass sits farther out, gives proportionally more, as (2.7) says. What limits it is the generator, whose best brake (2.6) and torque $\tau^*$ grow with the first moment too (section 7.5), and the air.

## 8.2 What the second blade can and cannot do

The question of these notes was how much power a second blade hinged at the tip of a turbine blade can give, who pays for it, and whether the wind's disorder helps. Here is the whole answer, chapter by chapter.

A uniform second blade of 1 kg and 1 m takes 161 to 267 mW from the rotor at steady winds of 10 to 6 m/s, by the best-brake rule $\kappa^* = R - 1$, and the rotor pays for every joule. The power grows with the first moment $ml/2$ and falls with the speed of the hinge, so it is largest in light wind (chapters 2 and 3).

Resonance is out of reach for any second blade shorter than its mother blade, and the motion is regular at every wind and brake tried (chapters 2 and 3).

The disorder of the wind: random shaking of white-noise type has a hard ceiling set by the second blade's mass, three quarters of it for a rod (chapter 4); gusts change the power by a few per cent at most (chapter 5), and the mother blade's sag at the tip by a few per cent. Whether the blade's shaking helps depends on how hard the blade shakes, and no source we found states that for this blade: the second blade takes little from tip vibrations of 5 mm, but more than gravity gives at 100 mm (chapter 6).

A real geared generator from a catalogue delivers 57 to 106 mW to the load, 1 522 times or more what the sensor of section 0.6 needs, and still about 811 times if the gearbox proves twice as draggy and less efficient than its catalogue (chapter 7). The second blade is sized to that generator. Turning its slow alternating voltage into a steady supply is an open problem of electronics.

What the mechanics leaves open is the air. At the tip the second blade moves through the air at 45.3 to 75.5 m/s, and section 0.7 showed that a few square centimetres of it, at a force coefficient of one, would feel a force as large as its weight. A real second blade, many times larger, would be pushed by the air at least as hard as by gravity. That push could feed the swing, as a flag's flutter is fed by the wind, or damp it; it would certainly load the hinge and the generator. These notes answer the question for the mechanics alone, and say plainly that the air must be modelled before the numbers above can be trusted for a real tip device. So the order the wind cannot spoil, gravity turning once per revolution, steers the energy and the rotor pays it; the disorder adds little at the levels the sources support; and the air, the next model, decides whether this machine is worth building.

## 8.3 Sources

Every value taken from outside these notes comes from one of these, each of which a reader can open.

A. Betz, Das Maximum der theoretisch möglichen Ausnützung des Windes durch Windmotoren, Zeitschrift für das gesamte Turbinenwesen 26 (1920) 307–309. The limit $C_p \le 16/27$ of section 0.2.

J. Jonkman, S. Butterfield, W. Musial, G. Scott, Definition of a 5-MW Reference Wind Turbine for Offshore System Development, NREL/TP-500-38060, 2009, osti.gov/servlets/purl/947422. Rotor radius, hub radius, chord table, peak power coefficient and its tip-speed ratio (Table 7-2), inertia, torque law, edgewise frequency 1.0793 Hz (Table 9-1).

OpenFAST regression tests, NREL 5-MW blade file NRELOffshrBsline5MW_Blade.dat, github.com/OpenFAST/r-test (glue-codes/openfast/5MW_Baseline). The blade's mass and stiffness tables of chapter 6.

NREL ROSCO, Examples/Test_Cases/NREL-5MW/Cp_Ct_Cq.NREL5MW.txt, github.com/NREL/ROSCO. The power coefficient $C_p(\lambda)$ of chapter 5.

B. J. Jonkman, TurbSim User's Guide, Version 1.50, NREL/TP-500-46198, 2009, osti.gov/servlets/purl/965520. The IEC 61400-1 (edition 3) Kaimal spectrum, turbulence intensity class A and coherence used in chapter 5; the standard itself is not freely available.

maxon, RE 25 ∅25 mm, graphite brushes, 20 W, catalogue page 153, maxongroup.com (EN-22-153.pdf); product 339152, maxongroup.com/maxon/view/product/339152. The motor of chapter 7.

maxon, Planetary Gearhead GP 32 C, catalogue pages 430–431, maxongroup.com (GP-32-C.pdf). Ratios, efficiencies, continuous torques, inertias, backlash, input speed limit.

Analog Devices, ADXL362 datasheet, revision D (the current revision could not be opened from where these notes were written; revision D was read), analog.com; Texas Instruments, CC2652R datasheet, SWRS207J, ti.com. The sensor node of section 0.6.

Vestas Wind Systems, Method of attaching a tip extension to a wind turbine blade, US patent 10 927 809 B2, patents.google.com/patent/US10927809B2. A retrofit tip extension about three metres long, of which about one metre reaches past the old tip (section 7.6).

Wind turbine blade tip brake apparatus and method, US patent 8 403 641 B2, patents.google.com/patent/US8403641. A pivoting tip brake whose tip is, in the preferred form, 5 % to 20 % of the rotor radius (section 7.6).

