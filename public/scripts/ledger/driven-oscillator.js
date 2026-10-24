/* Numa Koudsie · the ledger of Fig. 9, the driven oscillator (simulations/driven-oscillator.html)
   What the data panel (scripts/datalog.js) shows first, in which order the rest follows, and which books must balance.
   It only names variables of the page's dataset and adds checks for the numbers the page copies from its stored run;
   it computes nothing for display. Loaded after the page's own script and before datalog.js; the contract of every
   field is at the top of datalog.js. */
(function () {
    'use strict';
    var Sim = window.Sim, data = Sim && Sim.data, ds = data && data.ds, _t = window._t || function (s) { return s; };
    if (!ds) return;
    var g = function (n) { return ds.get(n); };
    /* a number shown now is a stored sample: x = x_n at n = n_now, unless your hand holds the block */
    function copy(name, arr, sym) {
        return function () {
            var i = g('i_now'), held = g('grabbed');
            return { formula: held ? _t('while your hand holds the block, this comes from the drag, not from the stored run') : sym + ' = ' + sym + '<sub>n</sub>, n = n<sub>now</sub>',
                inputs: [['n<sub>now</sub>', i, '', 0], [sym + '<sub>n</sub>', g(arr)[i], ds.vars[arr].attrs.units || '', 6]], value: held ? NaN : g(arr)[i] };
        };
    }
    var copies = { x_now: ['xs', 'x'], v_now: ['vs', 'v'], F_now: ['Fs', 'F'], u_now: ['us', 'u'], uP_now: ['uP', 'u<sub>P</sub>'], uI_now: ['uI', 'u<sub>I</sub>'], uD_now: ['uD', 'u<sub>D</sub>'],
        I_now: ['Is', 'I'], Fc_now: ['Fdamp', 'F<sub>c</sub>'], Fk_now: ['Fspr', 'F<sub>k</sub>'], Wc_now: ['Wc', 'W<sub>in</sub>'], Qc_now: ['Qc', 'W<sub>loss</sub>'], Ploss_now: ['Ploss', 'P<sub>loss</sub>'],
        E_now: ['Es', 'E'], ph_now: ['ph', 'Ωt'], Pin_now: ['Pin', 'P<sub>in</sub>'] };
    var check = {};
    Object.keys(copies).forEach(function (n) { check[n] = copy(n, copies[n][0], copies[n][1]); });
    /* the acceleration measured from the stored velocities: second-order differences, one-sided at the two ends */
    function accel(j) {
        var v = g('vs'), N = v.length, dt = g('ts')[1] - g('ts')[0];
        return (j === 0 ? 4 * v[1] - 3 * v[0] - v[2] : j === N - 1 ? 3 * v[j] - 4 * v[j - 1] + v[j - 2] : v[j + 1] - v[j - 1]) / (2 * dt);
    }
    check.as = function (j) { var v = g('vs'); return { formula: '(v<sub>n+1</sub> − v<sub>n−1</sub>) / 2Δt; ' + _t('one-sided at the first and last sample'), inputs: [['v<sub>n−1</sub>', v[j - 1], 'm/s', 6], ['v<sub>n+1</sub>', v[j + 1], 'm/s', 6], ['Δt', g('ts')[1] - g('ts')[0], 's', 3]], value: accel(j) }; };
    check.ma_now = function () { var i = g('i_now'); return { formula: 'm a<sub>n</sub>, n = n<sub>now</sub>', inputs: [['m', g('m'), 'kg', 1], ['a<sub>n</sub>', accel(i), 'm/s²', 6]], value: g('m') * accel(i) }; };
    check.E0 = function () { return { formula: '½ m ẋ(0)² + ½ k x(0)²', inputs: [['m', g('m'), 'kg', 1], ['ẋ(0)', g('vs')[0], 'm/s', 6], ['k', g('k'), 'N/m', 4], ['x(0)', g('xs')[0], 'm', 6]], value: 0.5 * g('m') * g('vs')[0] * g('vs')[0] + 0.5 * g('k') * g('xs')[0] * g('xs')[0] }; };
    check.bal_now = function () { return { formula: 'E(0) + W<sub>in</sub> − W<sub>loss</sub> − E', inputs: [['E(0)', g('E0'), 'J', 6], ['W<sub>in</sub>', g('Wc_now'), 'J', 6], ['W<sub>loss</sub>', g('Qc_now'), 'J', 6], ['E', g('E_now'), 'J', 6]], value: g('E0') + g('Wc_now') - g('Qc_now') - g('E_now') }; };
    check.fres_now = function () { return { formula: 'F + F<sub>c</sub> + F<sub>k</sub> − m a', inputs: [['F', g('F_now'), 'N', 6], ['F<sub>c</sub>', g('Fc_now'), 'N', 6], ['F<sub>k</sub>', g('Fk_now'), 'N', 6], ['m a', g('ma_now'), 'N', 6]], value: g('F_now') + g('Fc_now') + g('Fk_now') - g('ma_now') }; };
    check.stable = function () { return { formula: 'Δ<sub>RH</sub> > 0, (15)', inputs: [['Δ<sub>RH</sub>', g('margin'), '', 4]], value: g('margin') > 0 }; };
    check.fp_kind = function () {
        var re = Array.prototype.filter.call(g('lam_re'), function (x) { return x === x; }), im = g('lam_im'), maxRe = Math.max.apply(null, re), osc = Array.prototype.some.call(im, function (y) { return Math.abs(y) > 1e-12; });
        var kind = maxRe > 0 ? 'unstable' : (maxRe === 0 ? 'centre' : (osc ? 'stable focus' : (Math.abs(re[0] - re[1]) < 1e-9 * Math.abs(re[0]) ? 'degenerate stable node' : 'stable node')));
        return { formula: _t('from the signs of Re λ and whether any Im λ is not zero'), inputs: [['max Re λ', maxRe, '1/s', 4], ['Im λ ≠ 0', osc ? 'yes' : 'no', '']], value: kind };
    };
    function stopped() {
        if (g('grabbed')) return _t('Your hand holds the block, and the work of a hand is not in these books. They start again from the moment you let go.');
        var tb = g('t_blow');
        if (tb === tb && g('t_play') >= tb) return _t('The run grew without bound and the solver stopped; nothing after that moment is a motion to balance.');
        return null;
    }
    data.ledger = {
        headline: [{ v: 'x_now', title: 'displacement' }, { v: 'v_now', title: 'velocity' }, { v: 'F_now', title: 'coil force' }, { v: 'u_now', title: 'controller' },
            { v: 'E_now', title: 'energy' }, { v: 'Wc_now', title: 'work in' }, { v: 'Qc_now', title: 'heat out' }],
        sections: [
            { title: 'What you set', note: 'the sliders and your hand, as used by the last solve', how: 'set', vars: ['m', 'k', 'zeta', 'F0', 'fd', 'r', 'Kp', 'Ki', 'Kd', 'x0', 'v0', 'z0', 'released', 'grabbed', 'hand_now'] },
            { title: 'What follows from it', note: 'constants worked out from what you set, before anything moves', how: 'formula', vars: ['omega0', 'f0', 'c', 'Omega', 'tau', 'Q', 'BL', 'I0', 'xst', 'X', 'phi', 'phi_deg', 'G_drive', 'fr', 'ctrl_on', 'x_eq', 'F_eq', 'zeta_cl', 'margin', 'stable', 'H_drive', 'fp_kind', 'n_eig', 'lam_re', 'lam_im', 'mu_max', 'E0'] },
            { title: 'The state now', note: 'the stored sample on screen: where the block is, what pushes it, where the energy went', how: 'run', vars: ['t_play', 'i_now', 'x_now', 'v_now', 'F_now', 'u_now', 'uP_now', 'uI_now', 'uD_now', 'I_now', 'Fc_now', 'Fk_now', 'ma_now', 'E_now', 'Wc_now', 'Qc_now', 'Pin_now', 'Ploss_now', 'ph_now', 'bal_now', 'fres_now', 'playing'] },
            { title: 'The stored run', note: 'one row per stored sample, every 10 ms of the 60 s; the dot marks the sample on screen', how: 'run', vars: ['ts', 'xs', 'vs', 'as', 'zs', 'Fpush', 'us', 'uP', 'uI', 'uD', 'Fs', 'Is', 'Fdamp', 'Fspr', 'xqs', 'ph', 'Es', 'Pin', 'Ploss', 'Wc', 'Qc', 'xex'] },
            { title: 'The previous run', note: 'the run before the last Solve, drawn as the outlined block and the dotted curve', how: 'run', folded: true, vars: ['has_prev', 'prev_f0', 'prev_zeta', 'prev_F0', 'prev_fd', 'prev_x0', 'prev_v0', 'prev_z0', 'prev_r', 'prev_Kp', 'prev_Ki', 'prev_Kd', 'xs_prev', 'xmax_prev', 'ratio'] },
            { title: 'Curves of the figures', note: 'frequency response, steady orbit and flow field: worked out from the constants, not from the run', how: 'formula', folded: true, vars: ['view', 'fl', 'Al', 'Pl', 'Acl', 'Pcl', 'Amax', 'fb', 'Gmag', 'Gphase', 'Hmag', 'Hphase', 'orb_x', 'orb_v', 'strobe', 'fld_x', 'fld_v', 'fld_dx', 'fld_dv'] },
            { title: 'Solver', note: 'how the run was computed, and how well', how: 'solver', folded: true, vars: ['h', 'steps', 'solve_ms', 'err_max', 'Xm', 'Gm_drive', 'Win', 'Wloss', 'balance', 'stale', 't_blow'] },
            { title: 'Drawing', note: 'how stored values become pixels', how: 'drawing', folded: true, vars: ['xmax', 'need', 'span_before', 'fitted', 'span', 'held', 'ylim', 'amp_px', 'px_per_m', 'px_per_N', 'eq_px', 'block_px', 'block_y', 'ghost_shown', 'ghost_px', 'coil_px', 'Fd_px', 'Fc_px', 'Fk_px', 'hand_px', 'r_px', 'xeq_px', 'fprof', 'Wscale', 'uscale', 'Ploss_max', 'vmax', 'vlim', 'ph_x_px', 'ph_v_px', 'win_t0', 'win_T', 'box_w', 'box_h', 'fps'] }
        ],
        how: { m: 'constant', BL: 'constant', hand_now: 'formula', released: 'run', grabbed: 'set', t_play: 'set', playing: 'set', view: 'set', h: 'constant', steps: 'constant', xex: 'formula', E0: 'run' },
        books: [
            { title: 'Energy', short: 'energy', note: 'The coil’s work goes into the oscillator; the damper turns some of it into heat; the rest is the energy stored in spring and block.', rows: [[1, 'E0'], [1, 'Wc_now'], [-1, 'Qc_now']], total: 'E_now', residual: 'bal_now', tol: 1e-6, paused: stopped },
            { title: 'Newton’s second law', short: 'Newton', note: 'The three forces on the block add up to its mass times its acceleration, measured from the stored velocities; what is left is the error of that measurement, of order (Ω Δt)².', rows: [[1, 'F_now'], [1, 'Fc_now'], [1, 'Fk_now']], total: 'ma_now', residual: 'fres_now', tol: 1e-2, paused: stopped }
        ],
        deps: { f0: ['k'], omega0: ['k'], c: ['k', 'zeta'], Omega: ['fd'], tau: ['k', 'zeta'], Q: ['zeta'], I0: ['F0'], xst: ['F0', 'k'], X: ['F0', 'k', 'zeta', 'fd', 'Kp', 'Ki', 'Kd'], phi: ['k', 'zeta', 'fd', 'Kp', 'Ki', 'Kd'],
            phi_deg: ['phi'], G_drive: ['k', 'zeta', 'fd'], fr: ['k', 'zeta'], ctrl_on: ['Kp', 'Ki', 'Kd'], x_eq: ['r', 'Kp', 'Ki', 'k'], F_eq: ['x_eq', 'k'], zeta_cl: ['c', 'Kd', 'k', 'Kp'],
            margin: ['c', 'Kd', 'k', 'Kp', 'Ki'], stable: ['margin'], H_drive: ['k', 'Kp', 'c', 'Kd', 'Ki', 'fd'], lam_re: ['c', 'Kd', 'k', 'Kp', 'Ki'], lam_im: ['c', 'Kd', 'k', 'Kp', 'Ki'], n_eig: ['Ki'],
            fp_kind: ['lam_re', 'lam_im'], mu_max: ['lam_re', 'fd'], E0: ['x0', 'v0', 'k'], Al: ['k', 'zeta', 'F0'], Pl: ['k', 'zeta'], Acl: ['k', 'zeta', 'F0', 'Kp', 'Ki', 'Kd'], Pcl: ['k', 'zeta', 'Kp', 'Ki', 'Kd'],
            Gmag: ['k', 'zeta'], Gphase: ['k', 'zeta'], Hmag: ['k', 'c', 'Kp', 'Ki', 'Kd'], Hphase: ['k', 'c', 'Kp', 'Ki', 'Kd'], orb_x: ['x_eq', 'X'], orb_v: ['X', 'fd'] },
        controls: { kspring: 'k' },
        current: { n: 'i_now' },
        check: check
    };
})();
