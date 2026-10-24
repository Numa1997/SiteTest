/* Numa Koudsie · simulation catalog
   The list every simulation page is known by. simulations.html draws itself from it, in figure order:
   cards, search and filters. To add a simulation, add one entry to SIMULATIONS (and its field to
   SIM_FIELDS if the field is new) and one thumbnail in images/sims/<id>.webp, 800 × 500 px.
   For a new course year, also extend STAGES, load() validation and the year wording in simulations.html. Existing years 1 and 2 need no catalog-page edit.

   Entry fields
     id        short name, also the thumbnail file name
     fig       figure number, as printed on the simulation page; the catalog is ordered by it
     title     the page's h1, without the final dot
     file      path from the site root; its lecture note is at file + '#paper'
     field     an id from SIM_FIELDS
     stage     course stage the figure is written for: 1 = first year, 2 = second year
     subject   the subject line under the figure number on the page
     summary   two or three sentences, the abstract of the lecture note
     equation  the key equation, in TeX for KaTeX (display style)
     model     the equations the figure is built on, in words
     method    how the page computes them
     controls  what the reader sets
     concepts  search words and tags
     has       which of the shared tools the page carries (see SIM_TOOLS)
     added     date first published, YYYY-MM-DD */
(function () {
    'use strict';

    window.SIM_TOOLS = {
        derivation: 'Lecture note: motivation, model, derivation, numerical method, what is on screen, limits.',
        walkthrough: 'From symbols to code: each formula next to the line of code that computes it.',
        data: 'Data panel: every variable the figure draws, with units and the line that computes it.',
        read: 'Read values: click the figure to pin a point and read its numbers.',
        round: 'Record one round: a time series with charts, a table, .npz and CSV.',
        check: 'Check: stored value, formula recomputed, pixel read back.'
    };

    window.SIM_FIELDS = [
        { id: 'mechanics', name: 'Mechanics', blurb: 'Bodies, forces and the equations of motion.' },
        { id: 'waves', name: 'Oscillations and waves', blurb: 'Displacement fields, travelling waves and their superposition.' },
        { id: 'fluids', name: 'Fluids', blurb: 'Flow, pressure and waves in liquids.' },
        { id: 'optics', name: 'Wave optics', blurb: 'Light and water as waves: path difference, phase, interference.' },
        { id: 'methods', name: 'Mathematical methods', blurb: 'Complex numbers, Fourier series and transforms, drawn.' },
        { id: 'control', name: 'Control systems', blurb: 'Systems driven from outside, and controllers that answer back.' }
    ];

    var ALL = ['derivation', 'walkthrough', 'data', 'read', 'round', 'check'];

    window.SIMULATIONS = [
        {
            id: 'wave-sources',
            fig: 1,
            title: 'Wave Interference',
            file: 'simulations/Circular Wave Interference Visualization.html',
            field: 'optics',
            stage: 1,
            subject: "wave optics · Huygens’ principle",
            summary: 'Drop pebbles into a pond in a row and their rings cross. Where crest meets crest the water rises twice as high, where crest meets trough it stays flat, and with enough sources the rings fuse into one straight wavefront: Huygens’ principle, seen in the act.',
            equation: '\\psi(\\mathbf r, t) = \\frac{1}{N}\\sum_{i=1}^{N} e^{-g r_i}\\cos\\left(k r_i - \\omega t\\right)',
            model: 'superposition of N damped circular waves from the 2D wave equation',
            method: 'closed form, split as C(r) cos ωt + S(r) sin ωt',
            controls: 'wavelength λ, frequency f, damping γ; click to add sources',
            concepts: ["Huygens’ principle", 'superposition', 'plane wave', 'circular wave', 'damping'],
            has: ALL,
            added: '2026-10-06'
        },
        {
            id: 'double-pendulum',
            fig: 2,
            title: 'Double Pendulum',
            file: 'simulations/Double Pendulum.html',
            field: 'mechanics',
            stage: 2,
            subject: 'classical mechanics · chaos',
            summary: 'A pendulum hung from another pendulum: two angles, one gravitational field, and equations we can write down exactly. Started high, it becomes unpredictable within seconds; a twin started a thousandth of a radian apart shows by how much.',
            equation: '\\frac{\\mathrm d}{\\mathrm dt}\\frac{\\partial L}{\\partial\\dot\\theta_i} - \\frac{\\partial L}{\\partial\\theta_i} = 0, \\qquad L = T - V',
            model: 'Lagrangian of two point masses on massless rods; Euler–Lagrange equations',
            method: 'fourth-order Runge–Kutta, energy drift shown',
            controls: 'mass ratio m₂/m₁, length ratio l₂/l₁, angles θ₁ θ₂, angular velocities ω₁ ω₂, a chaos twin',
            concepts: ['Lagrangian mechanics', 'Euler–Lagrange equations', 'chaos', 'sensitive dependence', 'normal modes', 'Lyapunov exponent', 'RK4'],
            has: ALL,
            added: '2026-10-06'
        },
        {
            id: 'double-slit',
            fig: 3,
            title: 'Double-Slit Interference',
            file: 'simulations/Interactive Double-Slit Experiment Visualization.html',
            field: 'optics',
            stage: 1,
            subject: 'wave optics · wave–particle duality',
            summary: 'Light from two narrow slits reaches every point by two paths. Their difference in length, a fraction of a wavelength, decides whether the point is bright or dark: the pattern that convinced physics that light is a wave, and later that electrons are too.',
            equation: '\\delta s = L_2 - L_1 \\approx b\\sin\\alpha, \\qquad I \\propto \\cos^2\\!\\left(\\frac{\\pi\\,\\delta s}{\\lambda}\\right)',
            model: 'two coherent point sources; path difference δs ≈ b sin α',
            method: 'closed-form geometry, recomputed on every change',
            controls: 'distance d, angle α, slit separation b, wavelength λ',
            concepts: ['path difference', 'phase difference', 'interference order', 'small-angle approximation', 'fringes', 'wave–particle duality'],
            has: ALL,
            added: '2026-10-06'
        },
        {
            id: 'transverse-longitudinal',
            fig: 4,
            title: 'Transverse & Longitudinal',
            file: 'simulations/Transverse and longitudinal waves.html',
            field: 'waves',
            stage: 1,
            subject: 'oscillations · wave kinematics',
            summary: 'The same wave twice: once with the particles moving across the direction of travel, as on a guitar string, once along it, as in sound. Each particle only rocks in place; what travels is the pattern, and with it energy.',
            equation: '\\xi(x, t) = A\\sin(kx - \\omega t), \\qquad v = \\frac{\\omega}{k} = f\\lambda',
            model: 'harmonic travelling wave ξ(x, t) = A sin(kx − ωt)',
            method: 'exact evaluation at every particle, phase accumulated',
            controls: 'amplitude A, frequency f, wavelength λ, number of particles; follow one particle',
            concepts: ['travelling wave', 'phase velocity', 'transverse wave', 'longitudinal wave', 'compression', 'rarefaction', 'wave equation'],
            has: ALL,
            added: '2026-10-06'
        },
        {
            id: 'water-wave',
            fig: 5,
            title: 'Circular Water Waves',
            file: 'simulations/water-wave.html',
            field: 'fluids',
            stage: 2,
            subject: 'fluid dynamics · particle motion',
            summary: 'Under a passing wave each parcel of water runs in a small circle and comes back almost to where it began. The circles shrink exponentially with depth, long waves outrun short ones, and the small part that does not come back is the Stokes drift.',
            equation: '\\omega^2 = g k, \\qquad r(z) = a\\,e^{kz}',
            model: 'potential flow on deep water: Laplace’s equation, dispersion relation',
            method: 'closed form at every frame',
            controls: 'orbit radius a, wavelength λ, frequency f, particles per layer, depth layers, dispersion on or off',
            concepts: ['potential flow', "Laplace’s equation", 'dispersion relation', 'deep water', 'Stokes drift', 'orbital motion', 'group velocity'],
            has: ALL,
            added: '2026-10-06'
        },
        {
            id: 'wave-bench',
            fig: 6,
            title: 'Wave Interference Simulator',
            file: 'simulations/wave-interference.html',
            field: 'waves',
            stage: 1,
            subject: 'superposition · Fourier analysis',
            summary: 'A workbench for adding waves. Two close tones make beats, odd harmonics in the right proportions make a square wave, and the spectrum under the plot shows which sines are inside any sum you build.',
            equation: 'y(x, t) = \\sum_i A_i \\sin\\left(k_i x - \\omega_i t + \\varphi_i\\right)',
            model: 'sum of travelling sine waves, each with its own speed',
            method: 'direct evaluation per pixel column; analytic spectrum',
            controls: 'amplitude, frequency, phase and speed of each wave; presets: one wave, beats, square wave',
            concepts: ['superposition', 'beats', 'Fourier series', 'square wave', 'spectrum', 'Gibbs phenomenon', 'phase velocity'],
            has: ALL,
            added: '2026-10-06'
        },
        {
            id: 'phasor-sums',
            fig: 7,
            title: 'Phasor Sums',
            file: 'simulations/phasor-sums.html',
            field: 'methods',
            stage: 2,
            subject: 'complex analysis · epicycles',
            summary: 'Arms spinning on the tips of other arms. Adding rotating complex numbers tip to tail draws roses, beats and flowers; the same sums describe alternating current and the epicycles of ancient astronomy.',
            equation: 'z(t) = \\sum_k A_k\\, e^{i(\\omega_k t + \\varphi_k)}',
            model: 'sum of uniform circular motions in the complex plane',
            method: 'exact evaluation, N cosines and N sines per frame',
            controls: 'radius, angular frequency and phase of each arm; speed, zoom, trail; an audio file',
            concepts: ['phasor', 'complex exponential', "Euler’s formula", 'epicycles', 'rose curve', 'beats', 'period'],
            has: ALL,
            added: '2026-10-06'
        },
        {
            id: 'draw-decompose',
            fig: 8,
            title: 'Draw & Decompose',
            file: 'simulations/draw-decompose.html',
            field: 'methods',
            stage: 2,
            subject: 'Fourier analysis · discrete Fourier transform',
            summary: 'Draw any closed shape with one stroke. Its discrete Fourier transform turns it into a list of spinning circles; chained tip to tail, the largest of them draw it back, and Parseval’s theorem says how much is missing.',
            equation: 'z(t) = \\sum_k c_k\\, e^{ikt}, \\qquad c_k = \\frac{1}{N}\\sum_{n=0}^{N-1} z_n\\, e^{-2\\pi i k n / N}',
            model: 'closed curve as a periodic complex function, Fourier series',
            method: '256 points at equal arc length, DFT, terms sorted by |cₖ|',
            controls: 'number of circles K, time per loop, zoom; your own drawing',
            concepts: ['discrete Fourier transform', 'Fourier series', "Parseval’s theorem", 'truncation error', 'Gibbs overshoot', 'aliasing'],
            has: ALL,
            added: '2026-10-06'
        },
        {
            id: 'driven-oscillator',
            fig: 9,
            title: 'Driven Oscillator',
            file: 'simulations/driven-oscillator.html',
            field: 'control',
            stage: 1,
            subject: 'control systems · forced oscillations',
            summary: 'A mass on a spring, pushed by a force that someone else controls. The motion is solved first and stored, then played back: resonance, phase lag, beats and the Bode plot of the simplest system an engineer has to control.',
            equation: 'm\\ddot x + c\\dot x + k x = F_0\\cos\\Omega t, \\qquad G(s) = \\frac{1}{m s^2 + c s + k}',
            model: 'linear damped oscillator with an outside time-dependent force; exact solution for grading',
            method: 'RK4, solved and stored before playback; error against the exact solution shown',
            controls: 'natural frequency f₀, damping ratio ζ, force amplitude F₀, drive frequency f; solve, play, seek',
            concepts: ['driven oscillator', 'resonance', 'phase lag', 'quality factor', 'transfer function', 'Bode plot', 'beats', 'transient'],
            has: ALL,
            added: '2026-10-14'
        },
        {
            id: 'wind-turbine',
            fig: 10,
            title: 'Wind Turbine Control',
            file: 'simulations/wind-turbine.html',
            field: 'control',
            stage: 2,
            subject: 'control systems · wind energy',
            summary: 'Wind turns the rotor, the generator brakes it, and a controller decides how hard. Two minutes of turbulent wind, solved and stored, compare holding a constant speed with following the wind at the best tip-speed ratio.',
            equation: 'J\\dot\\omega = \\frac{\\rho A v^3 c_p(\\lambda)}{2\\,\\omega} - \\tau_\\text{gen}, \\qquad \\lambda = \\frac{\\omega R}{v}',
            model: 'rotor equation of motion with Heier’s power coefficient; PI and optimal-torque controllers',
            method: 'RK4, solved and stored before playback; energy balance checked',
            controls: 'controller, target speed, wind profile (steady, gust, step, turbulent), mean wind, size of change',
            concepts: ['wind energy', 'Betz limit', 'tip-speed ratio', 'power coefficient', 'feedback', 'PI controller', 'optimal torque', 'gust'],
            has: ALL,
            added: '2026-10-14'
        },
        {
            id: 'pendulum-control',
            fig: 11,
            title: 'Double Pendulum under Control',
            file: 'simulations/pendulum-control.html',
            field: 'control',
            stage: 2,
            subject: 'control systems · underactuated mechanics',
            summary: 'A double pendulum hangs from a fixed pivot; a sprung telescopic strut ties its lower ball to a cart that a moving coil drives. The aim: pushing only the cart, bring the whole chain back to rest where you choose. Pull it anywhere and let go; full-state feedback designed by LQR brings it home.',
            equation: '\\mathbf M(\\mathbf q)\\ddot{\\mathbf q} + \\mathbf C\\dot{\\mathbf q} + \\nabla V = (0, 0, F), \\qquad F = F^* - \\mathbf K(\\mathbf y - \\mathbf y^*)',
            model: 'Lagrangian double pendulum coupled to a cart by a two-force strut with a spring and end stops; moving-coil actuator with a current limit',
            method: 'RK4, solved and stored before playback; graded against a half-step run; energy books checked',
            controls: 'controller on or off, target position r, LQR weights for swing, cart, speed and effort, strut pull and stiffness, current limit; drag a ball or the cart',
            concepts: ['underactuated control', 'Lagrangian mechanics', 'generalised coordinates', 'controllability', 'LQR', 'Riccati equation', 'normal modes', 'phase space', 'Lyapunov function', 'region of attraction'],
            has: ALL,
            added: '2026-10-24'
        }
    ];
})();
