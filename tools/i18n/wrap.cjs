// node tools/i18n/wrap.cjs <page.html> [--dry]: wrap the reader-visible English strings of the page's inline scripts in _t(...).
// Used by hydraulics.py on its temporary copies (the ten simulation pages were wrapped once, in place, on 23 October 2026).
const fs = require('fs'), acorn = require('acorn'), walk = require('acorn-walk');
const file = process.argv[2], dry = process.argv.includes('--dry');
let html = fs.readFileSync(file, 'utf8');
const prose = s => {
  if (/\\|\d+px|IBM Plex|Instrument|serif|monospace|https?:|^use strict$/.test(s)) return false;
  let t = s.replace(/<[^>]*>/g, ' ').replace(/[\w-]+="[^"]*"?/g, ' ').replace(/="?/g, ' ');
  if (!/[A-Za-z]{2,}/.test(t)) return false;
  return /[A-Za-z]{2,}[ ,.;:·]+[A-Za-z]{2,}/.test(t) || /(^|\s)[A-Z][a-z]{2,}/.test(t) || /[a-z]{3,}\s*$|^\s*[a-z]{3,}\s/.test(t) && /\s/.test(t);
};
const HOOK_KEYS = new Set(['what', 'drawn', 'expected', 'note', 'title', 'label', 'about', 'kicker']);
const SKIP_CALLEE = /^(querySelector|querySelectorAll|getElementById|addEventListener|getAttribute|setProperty|get|set|var|coord|dim|has|touch|indexOf|includes|startsWith|split|replace|match|test|_t|T|fmt|createElement|attr|dataset|Function|log)$/;
const edits = [];
const re = /<script>([\s\S]*?)<\/script>/g; let m;
while ((m = re.exec(html))) {
  const code = m[1], base = m.index + '<script>'.length;
  let ast; try { ast = acorn.parse(code, { ecmaVersion: 'latest', sourceType: 'script' }); } catch (e) { continue; }
  walk.ancestor(ast, {
    Literal(node, anc) {
      if (typeof node.value !== 'string' || !prose(node.value) || code[node.start] !== "'") return;
      const p = anc[anc.length - 2], gp = anc[anc.length - 3];
      let ok = false;
      if (p.type === 'BinaryExpression' && p.operator === '+') ok = true;
      if (p.type === 'ConditionalExpression' && p.test !== node) ok = true;
      if (p.type === 'AssignmentExpression' && p.right === node && p.left.type === 'MemberExpression' && /^(textContent|innerHTML|innerText|title|placeholder|value)$/.test(p.left.property.name || '')) ok = true;
      if (p.type === 'ReturnStatement') ok = true;
      if (p.type === 'Property' && p.value === node && HOOK_KEYS.has(p.key.name || p.key.value)) ok = true;
      if (p.type === 'ArrayExpression') ok = !!process.env.WRAP_ARRAYS && /[A-Za-z]{2,}\s+[A-Za-z]{2,}/.test(node.value.replace(/<[^>]*>/g, ' '));   // table rows of prose, only where asked
      if (p.type === 'CallExpression') {
        const c = p.callee, name = c.type === 'MemberExpression' ? (c.property.name || '') : (c.name || '');
        if (name === 'fillText' && p.arguments[0] === node) ok = true;
        if (name === 'setAttribute' && p.arguments[1] === node && /aria-label|title/.test(p.arguments[0].value || '')) ok = true;
      }
      // never inside a comparison, a switch case, an object key or a call that uses the string as a name
      for (const a of anc) {
        if (a.type === 'BinaryExpression' && /^(===|!==|==|!=|in)$/.test(a.operator)) ok = false;
        if (a.type === 'SwitchCase') ok = false;
        if (a.type === 'CallExpression') { const c = a.callee, n = c.type === 'MemberExpression' ? (c.property.name || '') : (c.name || ''); if (SKIP_CALLEE.test(n) && a !== p) ok = false; if (SKIP_CALLEE.test(n) && a === p) ok = false; }
      }
      if (p.type === 'Property' && p.key === node) ok = false;
      if (ok) edits.push([base + node.start, base + node.end]);
    }
  });
}
edits.sort((a, b) => b[0] - a[0]);
for (const [s, e] of edits) html = html.slice(0, s) + '_t(' + html.slice(s, e) + ')' + html.slice(e);
if (!dry) fs.writeFileSync(file, html);
console.log(file.split('/').pop().slice(0, 30), edits.length);
