/* Numa Koudsie · the ledger of Rotor Pendula, the simulation tab (portfolios/rotor-pendula/index.html#sim,
   source portfolios-src/rotor-pendula/rotor_sim.html)
   What the data panel (scripts/datalog.js) shows first, in which order the rest follows, and the book that must balance.
   It only names variables of the page's dataset; the store, the checks and the read-backs are in the page's own store
   script. It computes nothing for display. Loaded after the page's scripts and before datalog.js; the contract of every
   field is at the top of datalog.js. */
(function () {
    'use strict';
    var Sim = window.Sim, data = Sim && Sim.data, ds = data && data.ds, _t = window._t || function (s) { return s; };
    if (!ds) return;
    var g = function (n) { return ds.get(n); };
    var SET = ['rpm_set', 'frac', 'pend', 'gen', 'brake', 'N', 'RL_set'];
    function stopped() {
        if (!g('phi') || !g('phi').length) return _t('Nothing is solved yet.');
        if (g('jammed')) return _t('The generator jams: the rod rides along at rest, and the rotor’s work is all potential energy.');
        return null;
    }
    data.ledger = {
        headline: [{ v: 't_now', title: 'time' }, { v: 'q1_now', title: 'rod angle' }, { v: 'w1_now', title: 'rod rate' }, { v: 'p_now', title: 'power' },
            { v: 'Win_now', title: 'rotor work' }, { v: 'Eh_now', title: 'harvest' }],
        window: 480,
        sections: [
            { title: 'What you set', note: 'the buttons, the brake and the generator, as used by the last solve', how: 'set', vars: ['rpm_set', 'frac', 'pend', 'gen', 'brake', 'N', 'RL_set'] },
            { title: 'Fixed for this study', note: 'constants of the physics block', how: 'constant', vars: ['g', 'M', 'L', 'v_tip'] },
            { title: 'What follows from it', note: 'the rotor, the two springs of the rod (centrifugal R, gravity G), its natural frequency and its best brake, before anything moves', how: 'formula',
                vars: ['Om', 'T_turn', 'rTip', 'rp', 'R', 'G', 'omega_n', 'I_p', 'kappaStar', 'c', 'kappa', 'Pstar', 'PstarModel', 'eta', 'csc', 'ce', 'RL', 'j', 'keep', 'jammed'] },
            { title: 'The state now', note: 'the stored frame on screen and the energy since the record began. Angular momentum has no book: the shaft’s torque holds Ω fixed, so it is not conserved.', how: 'run',
                vars: ['t_now', 'k_now', 'phi_now', 'q1_now', 'q2_now', 'w1_now', 'w2_now', 'p_now', 'pPaid_now', 'Ek_now', 'Ep_now', 'Espin_now', 'Win_now', 'Eh_now', 'Epaid_now', 'Efric_now', 'dEk_now', 'dEp_now', 'dEspin_now', 'Eother_now', 'book_res', 'book_rel'] },
            { title: 'What the solve found', note: 'means over the measuring turns', how: 'run', vars: ['P_mean', 'P_paid', 'P_fric', 'Theta', 'Theta2', 'trail', 'trailSin', 'bill', 'lag_deg', 'Win_mean'] },
            { title: 'The stored record', note: 'one row per frame of the last four turns; the dot marks the frame on screen', how: 'run',
                vars: ['turn', 'phi', 'q1', 'q2', 'w1', 'w2', 'p', 'pPaid', 'Ek', 'Ep', 'Espin', 'Win', 'Eh', 'Epaid', 'Efric'] },
            { title: 'Solver', note: 'Radau IIA, fixed step, in a Web Worker: how the run was computed', how: 'solver', folded: true, vars: ['steps', 'h', 'settle', 'measure', 'fpt', 'rec_turns', 'maxit', 'worker_ms', 'stale'] },
            { title: 'Drawing', note: 'how stored values become pixels', how: 'drawing', folded: true,
                vars: ['frame', 'speed', 'playing', 'mag', 'cx', 'cy', 'Rpx', 'sc', 'px', 'py', 'Lr', 'bobA_x', 'bobA_y', 'bx', 'by', 'L2', 'bobB_x', 'bobB_y', 'scene_w', 'scene_h',
                    'th_x0', 'th_x1', 'th_y0', 'th_y1', 'th_w', 'th_h', 'pw_x0', 'pw_x1', 'pw_y0', 'pw_y1', 'pw_w', 'pw_h', 'kp_x0', 'kp_x1', 'kp_y0', 'kp_y1', 'kp_w', 'kp_h', 'kap', 'Plin'] }
        ],
        how: { frame: 'set', speed: 'set', playing: 'set', jammed: 'formula', M: 'formula', L: 'formula', stale: 'set', k_now: 'set', t_now: 'run' },
        books: [
            { title: 'Energy', short: 'energy', note: 'Where the rotor’s work has gone since the record began: into the bobs’ motion and height, the motor’s spin, the harvest, friction, and the losses in winding and gears. The test is the rotor’s work, integrated from the forces at the pivot, against the energy the rod and the generator took.',
                rows: [[1, 'dEk_now'], [1, 'dEp_now'], [1, 'dEspin_now'], [1, 'Eh_now'], [1, 'Efric_now'], [1, 'Eother_now']], total: 'Win_now', residual: 'book_res', tol: 1e-9, paused: stopped }
        ],
        deps: {
            M: ['pend'], L: ['pend'], Om: ['rpm_set'], T_turn: ['Om'], rTip: ['Om'], rp: ['frac', 'rTip'], R: ['rp', 'L'], G: ['Om', 'L'], omega_n: ['Om', 'R'], I_p: ['pend'],
            kappaStar: ['R', 'pend', 'Om', 'rp'], c: ['brake', 'kappaStar', 'M', 'L', 'Om'], kappa: ['c', 'M', 'L', 'Om'], Pstar: ['Om', 'rp'], PstarModel: ['Pstar', 'kappaStar'],
            eta: ['N'], csc: ['N'], ce: ['N', 'RL_set', 'Om', 'rp'], RL: ['ce', 'N'], j: ['N'], keep: ['ce', 'csc'], jammed: ['N', 'eta', 'gen'],
            P_mean: SET, P_paid: SET, P_fric: SET, Theta: SET, Theta2: SET, trail: SET, trailSin: SET, bill: ['rp', 'Om', 'trailSin'], lag_deg: SET, Win_mean: SET,
            steps: ['gen'], h: ['T_turn', 'steps'], settle: ['gen'], measure: ['gen'], fpt: ['gen'],
            turn: SET, phi: SET, q1: SET, q2: SET, w1: SET, w2: SET, p: SET, pPaid: SET, Ek: SET, Ep: SET, Espin: SET, Win: SET, Eh: SET, Epaid: SET, Efric: SET,
            mag: ['q1', 'q2'], kap: ['kappaStar', 'kappa', 'ce'], Plin: ['kap', 'R', 'G', 'Om']
        },
        controls: { ratio: 'N', rl: 'RL_set' },
        current: { k: 'k_now' }
    };
})();
