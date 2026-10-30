/* Numa Koudsie · the ledger of the double pendulum under control (simulations/pendulum-control.html)
   What the data panel (scripts/datalog.js) shows first, in which order the rest follows, and the energy book that must
   balance. It only names variables of the page's dataset and adds checks for the two numbers of the book; it computes
   nothing for display. Loaded after the page's own script and before datalog.js; the contract of every field is at the
   top of datalog.js. */
(function () {
    'use strict';
    var Sim = window.Sim, data = Sim && Sim.data, ds = data && data.ds, _t = window._t || function (s) { return s; };
    if (!ds) return;
    var g = function (n) { return ds.get(n); };
    var check = {
        E0: function () { return { formula: _t('E<sub>n</sub> at n = 0, the first stored sample'), inputs: [], value: g('Es')[0] }; },
        bal_now: function () {
            if (g('grabbed') !== 'nothing') return { formula: _t('NaN while your hand holds the rig'), inputs: [], value: NaN };
            return { formula: 'E(0) + W<sub>coil</sub> − Q<sub>stop</sub> − E', inputs: [['E(0)', g('E0'), 'J', 6], ['W<sub>coil</sub>', g('Wc_now'), 'J', 6], ['Q<sub>stop</sub>', g('Qs_now'), 'J', 6], ['E', g('E_now'), 'J', 6]],
                value: g('E0') + g('Wc_now') - g('Qs_now') - g('E_now') };
        }
    };
    var rest = ['N0', 'ks', 'r'], design = ['N0', 'ks', 'r', 'qa', 'qx', 'qv', 'rho', 'ctrl_on'];
    data.ledger = {
        headline: [{ v: 'th1_now', title: 'upper rod' }, { v: 'th2_now', title: 'lower rod' }, { v: 'X_now', title: 'cart' },
            { v: 'F_now', title: 'coil force' }, { v: 'N_now', title: 'strut pull' }, { v: 'E_now', title: 'energy' }],
        sections: [
            { title: 'What you set', note: 'the target, the controller’s weights, the strut and the coil’s limit, as used by the last solve', how: 'set', vars: ['r', 'sched', 'ctrl_on', 'qa', 'qx', 'qv', 'rho', 'N0', 'ks', 'Imax'] },
            { title: 'The rig', note: 'fixed for this rig: the two balls and rods, the cart, the strut’s stops and the coil', how: 'constant', vars: ['m1', 'm2', 'l1', 'l2', 'mc', 'Hr', 'g', 'kappa', 'lmin', 'lmax', 'kst', 'cst'] },
            { title: 'What follows from it', note: 'the spring’s rest length, the coil’s largest force, and the rest the controller aims at', how: 'formula', vars: ['ell0', 'L0', 'Fmax', 'th1_eq', 'th2_eq', 'F_eq', 'N_eq', 'ell_eq', 'E_rest'] },
            { title: 'The controller', note: 'the linear model at that rest: gains, eigenvalues, the rank of the controllability test, the kind of rest', how: 'formula', vars: ['Kg', 'rank', 'lamo_re', 'lamo_im', 'lamc_re', 'lamc_im', 'slow', 'fp_kind'] },
            { title: 'The state now', note: 'the stored sample on screen, or the pose your hand holds: angles, cart, forces and where the energy went', how: 'run', vars: ['t_play', 'i_now', 'r_now', 'th1_now', 'th2_now', 'X_now', 'w1_now', 'w2_now', 'vX_now', 'F_now', 'I_now', 'N_now', 'ell_now', 'E_now', 'E0', 'Wc_now', 'Qs_now', 'bal_now', 'grabbed', 'playing'] },
            { title: 'Start of the run', note: 'hanging straight down after Solve; where your hand let go after a drag', how: 'run', vars: ['y0s', 'released'] },
            { title: 'The stored run', note: 'one row per stored sample, every 10 ms of the 30 s; the dot marks the sample on screen', how: 'run', vars: ['ts', 'r_ref', 'th1_ref', 'th2_ref', 'F_ref', 'th1', 'th2', 'Xs', 'w1', 'w2', 'vX', 'Fs', 'Is', 'Ns', 'ells', 'Es', 'Wc', 'Qs', 'sat'] },
            { title: 'Over the whole run', note: 'when the chain came to rest, how long the coil and the strut sat at their limits, and how good the run is', how: 'run', vars: ['t_settle', 't_sat', 't_stop', 'balance', 'err_half', 'err_end'] },
            { title: 'Solver', note: 'how the run was computed', how: 'solver', folded: true, vars: ['h', 'steps', 'solve_ms', 'stale'] },
            { title: 'Drawing', note: 'how stored values become pixels', how: 'drawing', folded: true, vars: ['px_per_m', 'px_per_N', 'pivot_px', 'pivot_py', 'b1_px', 'b1_py', 'b2_px', 'b2_py', 'cart_px', 'cart_py', 'r_px', 'F_px', 'win_t0', 'ylim', 'Flim', 'Escale', 'box_w', 'box_h', 'fps'] }
        ],
        how: { t_play: 'set', grabbed: 'set', playing: 'set', E0: 'run', h: 'constant', steps: 'constant' },
        books: [
            { title: 'Energy', short: 'energy', note: 'The coil’s work on the cart either stays in the rig, as motion, height and the spring’s stretch, or turns into heat in the strut’s stops when they are struck.',
              rows: [[1, 'E0'], [1, 'Wc_now'], [-1, 'Qs_now']], total: 'E_now', residual: 'bal_now', tol: 1e-8,
              paused: function () { return g('grabbed') !== 'nothing' ? _t('your hand holds the rig; the book starts again from the pose you let go') : null; } }
        ],
        deps: { ell0: [], L0: ['N0', 'ks'], Fmax: ['Imax'], th1_eq: rest, th2_eq: rest, F_eq: rest, N_eq: rest, ell_eq: rest, E_rest: rest,
            Kg: design, rank: rest, lamo_re: rest, lamo_im: rest, lamc_re: design, lamc_im: design, slow: design, fp_kind: design },
        current: { n: 'i_now' },
        check: check
    }; if (data.curve) data.curve.extend(data);   // the parameter curve: its group, its section, checks and read-backs (scripts/curve.js)
})();
