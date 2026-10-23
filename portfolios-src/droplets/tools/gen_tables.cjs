// Generate the collision-efficiency tables (L2) with the study's own trajectory solver and store them in data/.
//   node tools/gen_tables.cjs            -> data/etab_warm.json (water on water, 10 C, 850 hPa)
// The table records its air state and the generator's version; checks/check_physics.py recomputes E(40 um, 8 um) independently.
'use strict';
const fs = require('fs'), path = require('path');
const P = require('../physics.cjs');
const which = process.argv[2] || 'warm';
const cases = { warm: { T: 283.15, p: 85000, rhoR: 1000, rhoP: 1000 } };
const c = cases[which];
const t0 = Date.now();
const tab = P.makeTable(P.air(c.T, c.p), { rhoR: c.rhoR, rhoP: c.rhoP });
tab.E = tab.E.map(e => Math.round(e * 1e6) / 1e6);
tab.generated = 'tools/gen_tables.cjs ' + which;
fs.writeFileSync(path.join(__dirname, '..', 'data', 'etab_' + which + '.json'), JSON.stringify(tab));
console.log(`etab_${which}.json: ${tab.lnR.length} x ${tab.lnp.length} entries in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
