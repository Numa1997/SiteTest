// The Electron Beam · bridge.cjs: the one place where Python (build.py, checks/) runs the page's JavaScript in Node.
//   node bridge.cjs modules        -> JSON: every physics/chNN.js with id, inputs, outputs, ui, tolerance, cases (functions left out)
//   node bridge.cjs compute        stdin JSON [{module, inputs}] -> JSON [{inputs, outputs} | {error}]; missing inputs take contract defaults
//   node bridge.cjs core           -> JSON: the constants of physics/core.js (C and D), for the parity check against ref/core.py
//   node bridge.cjs katex          stdin JSON [{tex, display}] -> JSON [{html} | {error}], with the site's own KaTeX 0.16.11
//   node bridge.cjs fmt            stdin JSON [[x, sig]] -> JSON [string], core.fmt, for the formatter parity check
// KaTeX is the site's vendor copy, public/vendor/katex/katex.min.js, so the build and the page can never disagree on the version.
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const HERE = __dirname, ROOT = path.resolve(HERE, '..', '..');
const core = require('./physics/core.js');
const contract = JSON.parse(fs.readFileSync(path.join(HERE, 'contract.json'), 'utf8'));

function modules() {
  const dir = path.join(HERE, 'physics');
  return fs.readdirSync(dir).filter(f => /^ch\d\d\.js$/.test(f)).sort().map(f => ({ file: 'physics/' + f, mod: require(path.join(dir, f)) }));
}
function stdin() { return JSON.parse(fs.readFileSync(0, 'utf8') || 'null'); }
function plain(x) { return JSON.parse(JSON.stringify(x, (k, v) => (typeof v === 'function' ? undefined : v))); }

const cmd = process.argv[2];
let out;
if (cmd === 'modules') {
  out = modules().map(({ file, mod }) => ({ file, id: mod.id, inputs: mod.inputs, outputs: mod.outputs, ui: plain(mod.ui || null),
    tolerance: mod.tolerance || null, cases: mod.cases || [], hasDraw: typeof mod.draw === 'function' }));
} else if (cmd === 'compute') {
  const mods = Object.fromEntries(modules().map(({ mod }) => [mod.id, mod]));
  out = stdin().map(({ module, inputs }) => {
    try {
      const m = mods[module];
      if (!m) throw new Error('no physics module ' + module);
      const p = core.withDefaults(contract, m.inputs, inputs || {});
      return { inputs: p, outputs: plain(m.compute(p)) };
    } catch (e) { return { error: String(e.message || e) }; }
  });
} else if (cmd === 'core') {
  out = { C: core.C, D: core.D, U: core.U };
} else if (cmd === 'fmt') {
  out = stdin().map(([x, sig]) => core.fmt(x, sig));
} else if (cmd === 'katex') {
  const m = { exports: {} };
  vm.runInThisContext('(function (module, exports) {' + fs.readFileSync(path.join(ROOT, 'public/vendor/katex/katex.min.js'), 'utf8') + '\n})')(m, m.exports);
  const katex = m.exports;
  if (katex.version !== '0.16.11') throw new Error('expected KaTeX 0.16.11, found ' + katex.version);
  out = stdin().map(({ tex, display }) => {
    try { return { html: katex.renderToString(tex, { displayMode: display, output: 'html', throwOnError: true, strict: 'ignore', trust: false }) }; }
    catch (e) { return { error: String(e.message || e) }; }
  });
} else {
  console.error('usage: node bridge.cjs modules | compute | core | katex | fmt');
  process.exit(2);
}
process.stdout.write(JSON.stringify(out));
