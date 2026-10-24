/* Numa Koudsie · the ledger of Rotor Pendula, the simulation tab (portfolios/rotor-pendula/index.html#sim,
   source portfolios-src/rotor-pendula/rotor_sim.html)
   What the data panel (scripts/datalog.js) shows first, in which order the rest follows, and the book that must balance.
   The machine: a second blade (a thin uniform rod of mass m and length l) hinged at the tip of the NREL 5-MW blade, braked
   at its hinge. It only names variables of the page's dataset; the store, the checks and the read-backs are in the page's
   own store script. It computes nothing for display. Loaded after the page's scripts and before datalog.js; the contract of
   every field is at the top of datalog.js. */
(function () {
    'use strict';
    var Sim = window.Sim, data = Sim && Sim.data, ds = data && data.ds, _t = window._t || function (s) { return s; };
    if (!ds) return;
    var g = function (n) { return ds.get(n); };
    var SET = ['wind', 'gen', 'brake', 'N', 'RL_set'];
    function stopped() {
        if (!g('phi') || !g('phi').length) return _t('Nothing is solved yet.');
        if (g('jammed')) return _t('The generator jams: the second blade rides along at rest, and the rotor’s work is all potential energy.');
        return null;
    }
    data.ledger = {
        // W_in swings by about ±m g r_p each turn (the rotor lifts the whole second blade through 2 r_p and lets it down), so
        // the headline sets ΔE_pot beside it: the two nearly cancel, and the harvest is what is left over the turns.
        headline: [{ v: 'q1_now', title: 'blade angle' }, { v: 'w1_now', title: 'blade rate' }, { v: 'p_now', title: 'power' },
            { v: 'Win_now', title: 'rotor work' }, { v: 'dEp_now', title: 'lifted' }, { v: 'Eh_now', title: 'harvest' }],
        window: 480,
        sections: [
            { title: 'What you set', note: 'the wind, the brake and the generator, as used by the last solve', how: 'set', vars: ['wind', 'gen', 'brake', 'N', 'RL_set'] },
            { title: 'Fixed for this study', note: 'the second blade and the NREL 5-MW turbine: constants of the physics block', how: 'constant', vars: ['g', 'm', 'l', 'r_rot', 'lamStar'] },
            { title: 'What follows from it', note: 'the rotor’s speed, the second blade’s inertia I and first moment m l/2, its two springs (centrifugal R, gravity G), its natural frequency and its best brake, before anything moves', how: 'formula',
                vars: ['Om', 'n_rpm', 'T_turn', 'v_tip', 'rp', 'I', 'mlc', 'R', 'G', 'Gp', 'omega_n', 'kappaStar', 'c', 'kappa', 'Pstar', 'tauStar', 'eta', 'csc', 'ce', 'RL', 'j', 'keep', 'jammed'] },
            { title: 'The state now', note: 'the stored frame on screen and the energy since the record began. Angular momentum has no book: the shaft’s torque holds Ω fixed, so it is not conserved.', how: 'run',
                vars: ['t_now', 'k_now', 'phi_now', 'q1_now', 'w1_now', 'p_now', 'pPaid_now', 'Ek_now', 'Ep_now', 'Espin_now', 'Win_now', 'Eh_now', 'Epaid_now', 'Efric_now', 'dEk_now', 'dEp_now', 'dEspin_now', 'Eother_now', 'book_res', 'book_rel'] },
            { title: 'What the solve found', note: 'means over the measuring turns', how: 'run', vars: ['P_mean', 'P_paid', 'P_fric', 'Theta', 'trail', 'trailSin', 'bill', 'lag_deg', 'Win_mean'] },
            { title: 'The stored record', note: 'one row per frame of the last four turns; the dot marks the frame on screen', how: 'run',
                vars: ['turn', 'phi', 'q1', 'w1', 'p', 'pPaid', 'Ek', 'Ep', 'Espin', 'Win', 'Eh', 'Epaid', 'Efric'] },
            { title: 'Solver', note: 'Radau IIA, fixed step, in a Web Worker: how the run was computed', how: 'solver', folded: true, vars: ['steps', 'h', 'settle', 'measure', 'fpt', 'rec_turns', 'maxit', 'worker_ms', 'stale'] },
            { title: 'Drawing', note: 'how stored values become pixels: one scale for the rotor view, a second, named one for the close-up; no magnification of angles', how: 'drawing', folded: true,
                vars: ['frame', 'speed', 'playing', 'cx', 'cy', 'Rpx', 'sc', 'px', 'py', 'lA', 'cmA_x', 'cmA_y', 'sc2', 'zoom', 'bx', 'by', 'lB', 'cmB_x', 'cmB_y', 'scene_w', 'scene_h',
                    'th_x0', 'th_x1', 'th_y0', 'th_y1', 'th_w', 'th_h', 'pw_x0', 'pw_x1', 'pw_y0', 'pw_y1', 'pw_w', 'pw_h', 'kp_x0', 'kp_x1', 'kp_y0', 'kp_y1', 'kp_w', 'kp_h', 'kap', 'Plin'] }
        ],
        how: { frame: 'set', speed: 'set', playing: 'set', jammed: 'formula', stale: 'set', k_now: 'set', t_now: 'run' },
        books: [
            { title: 'Energy', short: 'energy', note: 'Where the rotor’s work has gone since the record began: into the second blade’s motion and height, the motor’s spin, the harvest, friction, and the losses in winding and gears. The test is the rotor’s work, integrated from the torque the mother blade exerts at the hinge, against the energy the second blade and the generator took.',
                rows: [[1, 'dEk_now'], [1, 'dEp_now'], [1, 'dEspin_now'], [1, 'Eh_now'], [1, 'Efric_now'], [1, 'Eother_now']], total: 'Win_now', residual: 'book_res', tol: 1e-9, paused: stopped }
        ],
        deps: {
            Om: ['wind', 'lamStar', 'r_rot'], n_rpm: ['Om'], T_turn: ['Om'], v_tip: ['Om', 'r_rot'], rp: ['r_rot'], I: ['m', 'l'], mlc: ['m', 'l'],
            R: ['mlc', 'rp', 'I'], G: ['mlc', 'g', 'I', 'Om'], Gp: ['m', 'g', 'rp', 'I', 'Om'], omega_n: ['Om', 'R'],
            kappaStar: ['R'], c: ['brake', 'kappaStar', 'I', 'Om'], kappa: ['c', 'I', 'Om'], Pstar: ['mlc', 'g', 'Om', 'rp', 'I'], tauStar: ['mlc', 'g'],
            eta: ['N'], csc: ['N'], ce: ['N', 'RL_set', 'Om', 'rp'], RL: ['ce', 'N'], j: ['N', 'I'], keep: ['ce', 'csc'], jammed: ['N', 'eta', 'gen', 'mlc'],
            P_mean: SET, P_paid: SET, P_fric: SET, Theta: SET, trail: SET, trailSin: SET, bill: ['mlc', 'rp', 'Om', 'trailSin'], lag_deg: SET, Win_mean: SET,
            steps: ['gen'], h: ['T_turn', 'steps'], settle: ['gen'], measure: ['gen'], fpt: ['gen'],
            turn: SET, phi: SET, q1: SET, w1: SET, p: SET, pPaid: SET, Ek: SET, Ep: SET, Espin: SET, Win: SET, Eh: SET, Epaid: SET, Efric: SET,
            lA: ['l', 'sc'], lB: ['l', 'sc2'], zoom: ['sc', 'sc2'], kap: ['kappaStar', 'kappa', 'ce'], Plin: ['kap', 'I', 'Om', 'R', 'G']
        },
        controls: { ratio: 'N', rl: 'RL_set' },
        current: { k: 'k_now' }
    };
})();
