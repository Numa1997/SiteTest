/* Numa Koudsie · the ledger of Fig. 10, wind turbine control (simulations/wind-turbine.html)
   What the data panel (scripts/datalog.js) shows first, in which order the rest follows, and the energy book that must
   balance. It only names variables of the page's dataset and adds checks for the numbers the page copies from its stored
   run; it computes nothing for display. Loaded after the page's own script and before datalog.js; the contract of every
   field is at the top of datalog.js. */
(function () {
    'use strict';
    var Sim = window.Sim, data = Sim && Sim.data, ds = data && data.ds, _t = window._t || function (s) { return s; };
    if (!ds) return;
    var g = function (n) { return ds.get(n); };
    /* a number shown now is a stored sample: v = v_n at n = n_now */
    function copy(arr, sym) {
        return function () {
            var i = g('i_now');
            return { formula: sym + ' = ' + sym + '<sub>n</sub>, n = n<sub>now</sub>', inputs: [['n<sub>now</sub>', i, '', 0], [sym + '<sub>n</sub>', g(arr)[i], ds.vars[arr].attrs.units || '', 6]], value: g(arr)[i] };
        };
    }
    var check = { v_now: copy('vw', 'v'), rpm_now: copy('rpm', 'n<sub>rot</sub>'), P_now: copy('Pg', 'P<sub>gen</sub>'), lam_now: copy('lam', 'λ'), cp_now: copy('cpv', 'c<sub>p</sub>'),
        th_now: copy('th', 'θ'), Ea_now: copy('Eas', 'E<sub>aero</sub>'), Eg_now: copy('Eg', 'E<sub>gen</sub>') };
    check.K_now = function () { var w = g('om')[g('i_now')]; return { formula: '½ J ω<sub>n</sub>², n = n<sub>now</sub>', inputs: [['J', g('J'), 'kg m²', 0], ['ω<sub>n</sub>', w, 'rad/s', 6]], value: 0.5 * g('J') * w * w }; };
    check.K0 = function () { var w = g('om')[0]; return { formula: '½ J ω(0)²', inputs: [['J', g('J'), 'kg m²', 0], ['ω(0)', w, 'rad/s', 6]], value: 0.5 * g('J') * w * w }; };
    check.ebal_now = function () { return { formula: 'K(0) + E<sub>aero</sub> − E<sub>gen</sub> − K', inputs: [['K(0)', g('K0'), 'J', 0], ['E<sub>aero</sub>', g('Ea_now'), 'J', 0], ['E<sub>gen</sub>', g('Eg_now'), 'J', 0], ['K', g('K_now'), 'J', 0]], value: g('K0') + g('Ea_now') - g('Eg_now') - g('K_now') }; };
    data.ledger = {
        headline: [{ v: 'v_now', title: 'wind' }, { v: 'rpm_now', title: 'rotor speed' }, { v: 'lam_now', title: 'tip-speed ratio' }, { v: 'cp_now', title: 'share taken' },
            { v: 'P_now', title: 'power out' }, { v: 'Eg_now', title: 'energy out' }],
        sections: [
            { title: 'What you set', note: 'the controller, the wind and the target speed, as used by the last solve', how: 'set', vars: ['ctrl', 'profile', 'v0', 'dv', 'rpm_ref'] },
            { title: 'The turbine', note: 'fixed for this rotor', how: 'constant', vars: ['rho', 'R', 'J', 'cp_betz', 'lam_opt', 'cp_max', 'K_opt'] },
            { title: 'What follows from it', note: 'the controller tuned at the target speed, and the start', how: 'formula', vars: ['w_ref', 'dtau_dw', 'Kp', 'Ki', 'tau0', 'K0'] },
            { title: 'The state now', note: 'the stored sample on screen: the wind, the rotor, the power and where the energy went', how: 'run', vars: ['t_play', 'i_now', 'v_now', 'rpm_now', 'lam_now', 'cp_now', 'P_now', 'th_now', 'Ea_now', 'Eg_now', 'K_now', 'ebal_now', 'playing'] },
            { title: 'The stored run', note: 'one row per stored sample, every 20 ms of the 120 s; the dot marks the sample on screen', how: 'run', vars: ['ts', 'vw', 'om', 'rpm', 'vtip', 'th', 'lam', 'cpv', 'ta', 'tg', 'Ictl', 'Pa', 'Pg', 'Eas', 'Eg', 'sw'] },
            { title: 'Over the whole run', note: 'totals and extremes of the 120 s', how: 'run', vars: ['Ew', 'Ea', 'Eg_end', 'captured_pct', 'P_mean', 'rpm_min', 'rpm_max', 'balance'] },
            { title: 'Power curve', note: 'the curve of the second figure', how: 'formula', folded: true, vars: ['lamL', 'cpL'] },
            { title: 'Solver', note: 'how the run was computed', how: 'solver', folded: true, vars: ['h', 'steps', 'solve_ms', 'stale'] },
            { title: 'Drawing', note: 'how stored values become pixels', how: 'drawing', folded: true, vars: ['v_hi', 'rpm_lo', 'rpm_hi', 'P_hi', 'px_per_m_air', 'hub_x', 'hub_y', 'r_px', 'box_w', 'box_h', 'fps'] }
        ],
        how: { t_play: 'set', playing: 'set', K0: 'run', h: 'constant', steps: 'constant' },
        books: [
            { title: 'Energy', short: 'energy', note: 'The wind’s work on the rotor either goes into the generator or changes how fast the rotor turns; what is left is the rotor’s kinetic energy.', rows: [[1, 'K0'], [1, 'Ea_now'], [-1, 'Eg_now']], total: 'K_now', residual: 'ebal_now', tol: 1e-6 }
        ],
        deps: { w_ref: ['rpm_ref'], dtau_dw: ['rpm_ref', 'v0'], Kp: ['dtau_dw'], tau0: ['rpm_ref', 'v0', 'dv', 'profile'], K0: ['rpm_ref', 'v0', 'ctrl', 'profile'] },
        controls: { rpm: 'rpm_ref' },
        current: { n: 'i_now' },
        check: check
    };
})();
