/* Numa Koudsie · simulation catalog
   The list every simulation page is known by. simulations.html draws itself from it:
   field groups, cards, search and filters. To add a simulation, add one entry to
   SIMULATIONS (and its field to SIM_FIELDS if the field is new) and one thumbnail
   in images/sims/<id>.webp, 800 × 500 px. Nothing else on the page needs editing.

   Entry fields
     id        short name, also the thumbnail file name
     fig       figure number, as printed on the simulation page
     title     the page's h1, without the final dot
     file      path from the site root
     field     an id from SIM_FIELDS
     stage     course stage the figure is written for: 1 = first year, 2 = second year
     subject   the subject line under the figure number on the page
     question  the question a student can answer with it
     summary   the page's lede
     model     the equations the figure is built on
     method    how the page computes them
     controls  what the reader sets
     concepts  search words and tags
     has       which of the shared tools the page carries (see SIM_TOOLS)
     added     date first published, YYYY-MM-DD */
(function () {
    'use strict';

    window.SIM_TOOLS = {
        derivation: 'From physics to pixels: picture, model, derivation, numerical method, what is on screen, limits.',
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
        { id: 'methods', name: 'Mathematical methods', blurb: 'Complex numbers, Fourier series and transforms, drawn.' }
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
            subject: "wave optics · Huygens' principle",
            question: 'Why do many point sources in a row send out one straight wavefront?',
            summary: 'Circular waves from point sources on one line add up crest by crest. With enough sources, the ripples merge into a straight wavefront.',
            model: '2D wave equation ∂²ψ/∂t² = v²∇²ψ; sum of N circular waves',
            method: 'closed form, split as C(r) cos ωt + S(r) sin ωt',
            controls: 'wavelength λ, frequency f, damping γ; click to add sources',
            concepts: ["Huygens' principle", 'superposition', 'plane wave', 'circular wave', 'damping'],
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
            question: 'How can a system with exact equations still be unpredictable?',
            summary: 'Two rigid rods, two point masses, one gravitational field. Deterministic, and yet a change of a thousandth of a radian in the start sends it somewhere else entirely.',
            model: 'Lagrangian L = T − V of two point masses; Euler–Lagrange equations',
            method: 'fourth-order Runge–Kutta, energy drift shown',
            controls: 'mass ratio m₂/m₁, length ratio l₂/l₁, angles θ₁ θ₂, angular velocities ω₁ ω₂, a chaos twin',
            concepts: ['Lagrangian mechanics', 'Euler–Lagrange equations', 'chaos', 'sensitive dependence', 'energy conservation', 'RK4'],
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
            question: 'What decides whether a point on the screen is bright or dark?',
            summary: 'Two slits, one point P. The two paths to P differ by δs, and that small difference decides whether P is bright or dark.',
            model: 'two coherent point sources; path difference δs ≈ b sin α',
            method: 'closed-form geometry, recomputed on every change',
            controls: 'distance d, angle α, slit separation b, wavelength λ',
            concepts: ['path difference', 'phase difference', 'interference order', 'small-angle approximation', 'fringes'],
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
            question: 'In a wave, what travels: the particles or the pattern?',
            summary: 'The same wave, twice. Above, the particles move across the direction of travel; below, along it. In both, each particle only oscillates in place while the pattern moves on.',
            model: 'harmonic travelling wave ξ(x, t) = A sin(kx − ωt)',
            method: 'exact evaluation at every particle, phase accumulated',
            controls: 'amplitude A, frequency f, wavelength λ, number of particles; follow one particle',
            concepts: ['travelling wave', 'phase velocity', 'transverse wave', 'longitudinal wave', 'compression', 'rarefaction'],
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
            question: 'How does water move under a passing wave, and why do the circles shrink with depth?',
            summary: 'As a crest passes, each parcel of water traces a small circle and comes back where it started. The circles shrink quickly with depth.',
            model: 'potential flow on deep water: ∇²φ = 0, orbits a·e^{kz}, ω² = gk',
            method: 'closed form at every frame',
            controls: 'orbit radius a, wavelength λ, frequency f, particles per layer, depth layers, dispersion on or off',
            concepts: ['potential flow', "Laplace's equation", 'dispersion relation', 'deep water', 'Stokes drift', 'orbital motion'],
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
            question: 'What does a sum of sine waves look like, and what is in its spectrum?',
            summary: 'A workbench for adding waves. Give each one its own amplitude, frequency, phase and speed, and watch the sum take shape.',
            model: 'yᵢ = Aᵢ sin(2π fᵢ (x/200 − sᵢ t) + φᵢ), summed',
            method: 'direct evaluation per pixel column; analytic spectrum',
            controls: 'amplitude, frequency, phase and speed of each wave; presets: one wave, beats, square wave',
            concepts: ['superposition', 'beats', 'Fourier series', 'square wave', 'spectrum', 'phase velocity'],
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
            question: 'What curve do rotating complex numbers draw when added tip to tail?',
            summary: 'Arms spinning on the tips of other arms. Add rotating complex numbers tip to tail and the last tip draws roses, beats and flowers; play a song and the bass makes the arms breathe.',
            model: 'z(t) = Σ Aₖ e^{i(ωₖ t + φₖ)}',
            method: 'exact evaluation, N cosines and N sines per frame',
            controls: 'radius, angular frequency and phase of each arm; speed, zoom, trail; an audio file',
            concepts: ['phasor', 'complex exponential', 'epicycles', 'rose curve', 'beats', 'period'],
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
            question: 'How can a list of spinning circles redraw any closed shape?',
            summary: 'Draw any closed shape with one stroke. Its Fourier transform turns it into a list of spinning circles, and the circles, chained tip to tail, draw it back.',
            model: 'closed curve as a periodic complex function z(t) = Σ cₖ e^{ikt}',
            method: '256 points at equal arc length, DFT, terms sorted by |cₖ|',
            controls: 'number of circles K, time per loop, zoom; your own drawing',
            concepts: ['discrete Fourier transform', 'Fourier series', "Parseval's theorem", 'truncation error', 'Gibbs overshoot'],
            has: ALL,
            added: '2026-10-06'
        }
    ];
})();
