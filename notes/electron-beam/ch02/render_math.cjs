// Renders TeX with the site's own KaTeX 0.16.11 (public/vendor/katex/katex.min.js), at build time.
// stdin: JSON [{tex, display}]; stdout: JSON [{html}|{error}]
const vm = require('vm'), fs = require('fs'), path = require('path');
const file = path.join(__dirname, '..', '..', '..', 'public', 'vendor', 'katex', 'katex.min.js');
const m = { exports: {} };
vm.runInNewContext(fs.readFileSync(file, 'utf8'), { module: m, exports: m.exports, self: {}, console });
const katex = m.exports;
let input = '';
process.stdin.on('data', d => { input += d; });
process.stdin.on('end', () => {
  const out = JSON.parse(input).map(({ tex, display }) => {
    try { return { html: katex.renderToString(tex, { displayMode: display, output: 'html', throwOnError: true, strict: 'ignore', trust: false }) }; }
    catch (e) { return { error: String(e.message || e), tex }; }
  });
  process.stdout.write(JSON.stringify(out));
});
