/* Numa Koudsie · the ledger of Rotor Pendula, the wind tab (portfolios/rotor-pendula/index.html#wind,
   source portfolios-src/rotor-pendula/rotor_wind.html)
   What the data panel (scripts/datalog.js) shows first, in which order the rest follows, and the book that must balance.
   The page synthesises a turbulent wind over the rotor of the NREL 5-MW turbine (IEC Kaimal spectra and coherences, Veers'
   method), turns the rotor in it and swings the second blade at its tip. This file only names variables of the page's dataset;
   the store, the checks and the read-backs are in the page's own script. It computes nothing for display. Loaded after the
   page's scripts and before datalog.js; the contract of every field is at the top of datalog.js. */
(function () {
    'use strict';
    var Sim = window.Sim, data = Sim && Sim.data, ds = data && data.ds;
    if (!ds) return;
    var SET = ['U_hub', 'cls', 'seed'];
    data.ledger = {
        headline: [{ v: 'veff', title: 'wind on the disc' }, { v: 'n_rpm', title: 'rotor' }, { v: 'U_tip', title: 'wind at the tip' },
            { v: 'th', title: 'second blade' }, { v: 'p', title: 'power' }, { v: 'P_mean', title: 'mean power' }],
        window: 600,
        sections: [
            { title: 'What you set', note: 'the mean wind, the turbulence class, the record, the shape, and the clock', how: 'set', vars: ['U_hub', 'cls', 'seed', 'shape', 'speed', 'playing'] },
            { title: 'Fixed for this study', note: 'the second blade, the turbine, the air and the integrator', how: 'constant', vars: ['g', 'm', 'l', 'rp', 'rho', 'J', 'alpha', 'chord', 'CL0', 'CD', 'h', 'dtf', 'Trec'] },
            { title: 'The wind record', note: 'the statistics the standard prescribes, and what this record of 256 s turned out to have', how: 'formula',
                vars: ['sigma_u', 'sigma_v', 'sigma_w', 'var_hub', 'vbar', 'sig_eff', 'n_disc', 'synth_ms'] },
            { title: 'What follows for the machine', note: 'the rotor’s steady speed at the mean wind, and the brake set for it', how: 'formula', vars: ['Om0', 'c', 'Pstar', 'gam0'] },
            { title: 'The state now', note: 'the rotor, the wind it feels, and the second blade', how: 'run',
                vars: ['t', 'turns', 'phi', 'Om', 'n_rpm', 'Omdot', 'lam', 'veff', 'u_hub', 'Qa', 'Qg', 'th', 'w', 'U_tip', 'Ua', 'Ut', 'gam', 'CL', 'Ft', 'tauAir', 'p', 'Eh', 'P_mean'] },
            { title: 'Energy since the start', note: 'the rotor’s work, from Newton’s law for the second blade’s centre of mass, the air’s work, the second blade’s energy and the harvest', how: 'run',
                vars: ['Wrot', 'Wair', 'E', 'dE', 'book_res', 'book_rel'] },
            { title: 'The field now', note: 'the gusts at the 121 grid points at this instant, and where the points are', how: 'run', vars: ['u_now', 'v_now', 'w_now', 'U_p', 'gy', 'gz', 'disc'] },
            { title: 'The whole record', note: 'the synthesised field at every 0.5 s, and the disc average', how: 'run', folded: true, vars: ['field_u', 'field_v', 'field_w', 'veff_k'] },
            { title: 'History', note: 'what the traces draw, every 0.1 s of simulated time (a ring of 900 samples)', how: 'run', folded: true,
                vars: ['hist_t', 'hist_uhub', 'hist_veff', 'hist_rpm', 'hist_th', 'hist_p', 'hist_Pm'] },
            { title: 'Drawing', note: 'how stored values become pixels', how: 'drawing', folded: true,
                vars: ['sc', 'sc2', 'zoom', 'cx', 'cy', 'tipx', 'tipy', 'ix', 'iy', 'ir', 'sbx', 'sby', 'ulim', 'karr', 'karr2', 'ox2', 'oy2'] }
        ],
        how: { speed: 'set', playing: 'set' },
        books: [
            { title: 'Energy of the second blade', short: 'energy', note: 'What the rotor and the air have given the second blade since the start has gone into its energy (motion and height, in the ground frame) and into the harvest. The rotor’s work is integrated from the hinge force of Newton’s law, so the residual tests the integrator and the equations together; fourth-order Runge–Kutta at 5 ms leaves about 10⁻⁶ of the energies after a few minutes.',
                rows: [[1, 'Wrot'], [1, 'Wair'], [-1, 'Eh']], total: 'dE', residual: 'book_res', tol: 1e-5 }
        ],
        deps: {
            sigma_u: SET, sigma_v: ['sigma_u'], sigma_w: ['sigma_u'], var_hub: SET, vbar: SET, sig_eff: SET,
            Om0: ['vbar'], c: ['Om0'], Pstar: ['Om0'], gam0: ['Om0', 'U_hub'], chord: ['shape'], CL0: ['shape'], CD: ['shape']
        },
        controls: { seg_U: 'U_hub', seg_cls: 'cls', seg_seed: 'seed', seg_shape: 'shape', seg_speed: 'speed' }
    };
})();
