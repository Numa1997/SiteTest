// Numa Koudsie · the tool reader behind "How this site is made" on the home page (index.html, section #made).
// Reads the repository and writes public/scripts/site-tools.js: the languages (files counted by type), the libraries and
// services found in package.json files, Python imports, Node requires, the vendored KaTeX, the fonts and the hosting
// config. Known tools get a proper name and a group; anything new that it cannot name goes under "Also found" with its
// package name, so a tool added to the code shows up by itself. It runs before every `npm run build` (package.json
// "prebuild"), and so on every deploy, since Cloudflare builds the site from main. It never stops a build: on an error it
// keeps the old file and says why. The panel shows names and numbers only; its words live in index.html and are
// translated with the rest of the page. node tools/site-tools.mjs [--check]
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT = path.join(ROOT, 'public', 'scripts', 'site-tools.js');
const SKIP = new Set(['node_modules', 'dist', '.git', '.wrangler', 'vendor', 'shots']);
const GENERATED = ['public/de', 'public/ar'];          // copies made by tools/i18n/build.py: not counted twice

// name and group of every tool the reader knows; the key is how it appears in the code
const KNOWN = {
  npm: { vite: ['Vite', 'build'], tailwindcss: ['Tailwind CSS', 'build'], postcss: ['PostCSS', 'build'], autoprefixer: ['Autoprefixer', 'build'],
         typescript: ['TypeScript compiler', 'build'], lucide: ['Lucide icons', 'build'], wrangler: ['Wrangler', 'hosting'], acorn: ['Acorn', 'build'], 'acorn-walk': ['Acorn', 'build'],
         playwright: ['Playwright', 'testing'], katex: ['KaTeX', 'maths'], rtlcss: ['RTLCSS', 'build'] },
  py: { numpy: ['NumPy', 'maths'], scipy: ['SciPy', 'maths'], sympy: ['SymPy', 'maths'], mpmath: ['mpmath', 'maths'], matplotlib: ['Matplotlib', 'maths'],
        PIL: ['Pillow', 'testing'], playwright: ['Playwright', 'testing'], pandas: ['pandas', 'maths'], jax: ['JAX', 'maths'] }
};
const LANGS = { '.html': 'HTML', '.css': 'CSS', '.js': 'JavaScript', '.mjs': 'JavaScript', '.cjs': 'JavaScript', '.py': 'Python', '.ts': 'TypeScript', '.sh': 'Shell', '.md': 'Markdown' };
const PY_STD = new Set(('abc argparse array ast asyncio base64 bisect calendar cmath codecs collections concurrent contextlib copy csv dataclasses datetime decimal ' +
  'difflib email enum errno fnmatch fractions functools gc getpass glob gzip hashlib heapq hmac html http importlib inspect io itertools json locale logging ' +
  'math mimetypes multiprocessing numbers operator os pathlib pickle platform pprint queue random re secrets shlex shutil signal socket sqlite3 ssl stat ' +
  'statistics string struct subprocess sys tarfile tempfile textwrap threading time timeit tomllib traceback types typing unicodedata unittest urllib uuid ' +
  'warnings weakref xml zipfile zlib __future__').split(' '));
const NODE_STD = new Set('assert buffer child_process crypto events fs http https module os path process readline stream url util vm worker_threads zlib'.split(' '));

function walk(dir, out) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP.has(e.name) || e.name.startsWith('.')) continue;
    const p = path.join(dir, e.name), rel = path.relative(ROOT, p).split(path.sep).join('/');
    if (GENERATED.some(g => rel === g || rel.startsWith(g + '/'))) continue;
    if (e.isDirectory()) walk(p, out); else out.push(rel);
  }
  return out;
}

function read() {
  const files = walk(ROOT, []), found = new Map(), other = new Set();
  const add = (name, group, via) => { if (!found.has(name)) found.set(name, { name, group, via }); };
  const known = (kind, key, via) => { const k = KNOWN[kind][key]; if (k) add(k[0], k[1], via); else other.add(key); };

  // the engine: the repository is set up for Claude Code (CLAUDE.md); every line of it was written by Claude
  if (files.includes('CLAUDE.md')) add('Claude (Anthropic) · Claude Code', 'engine', 'CLAUDE.md');

  // languages: files counted by type
  const langs = {};
  for (const f of files) { const l = LANGS[path.extname(f)]; if (l) langs[l] = (langs[l] || 0) + 1; }

  // package.json files: every dependency
  for (const f of files.filter(f => path.basename(f) === 'package.json')) {
    let j; try { j = JSON.parse(fs.readFileSync(path.join(ROOT, f), 'utf8')); } catch (e) { continue; }
    for (const sec of ['dependencies', 'devDependencies', 'optionalDependencies'])
      for (const d of Object.keys(j[sec] || {})) { if (d.startsWith('@rollup/rollup-')) continue; known('npm', d.replace(/^@[^/]+\//, ''), f); }
  }

  // Python imports, except the standard library and the repository's own modules
  const own = new Set(files.filter(f => f.endsWith('.py')).map(f => path.basename(f, '.py')));
  for (const f of files.filter(f => f.endsWith('.py'))) {
    const src = fs.readFileSync(path.join(ROOT, f), 'utf8');
    for (const m of src.matchAll(/^\s*(?:from\s+([A-Za-z_][\w]*)[\w.]*\s+import|import\s+([A-Za-z_][\w]*))/gm)) {
      const mod = m[1] || m[2];
      if (!PY_STD.has(mod) && !own.has(mod)) known('py', mod, f);
    }
  }

  // Node requires and imports in the tools, notes and tests, except Node's own modules and relative paths
  for (const f of files.filter(f => /\.(c|m)?js$/.test(f) && /^(tools|notes|tests|portfolios-src)\//.test(f))) {
    const src = fs.readFileSync(path.join(ROOT, f), 'utf8');
    for (const m of src.matchAll(/(?:require\(\s*|\bfrom\s+|\bimport\s+)['"]([^'"./][^'"]*)['"]/g)) {
      const mod = m[1].replace(/^node:/, '').replace(/^(@[^/]+\/[^/]+|[^/]+).*$/, '$1');
      if (!/^(@[a-z0-9._-]+\/)?[a-z0-9._-]+$/i.test(mod)) continue;
      if (!NODE_STD.has(mod)) known('npm', mod.replace(/^@[^/]+\//, ''), f);
    }
  }
  if (found.has('Playwright')) add('Chromium (headless)', 'testing', 'Playwright');

  // KaTeX shipped with the site
  if (fs.existsSync(path.join(ROOT, 'public', 'vendor', 'katex'))) add('KaTeX', 'maths', 'public/vendor/katex');

  // fonts: every family the site's own style sheets load with @font-face
  for (const f of files.filter(f => /^public\/.*\.css$/.test(f)))
    for (const m of fs.readFileSync(path.join(ROOT, f), 'utf8').matchAll(/@font-face\s*\{[^}]*?font-family:\s*['"]([^'"]+)['"]/g)) add(m[1], 'fonts', f);

  // hosting: the Cloudflare config and the GitHub repository it builds from
  if (files.includes('wrangler.jsonc')) { add('Cloudflare', 'hosting', 'wrangler.jsonc'); add('GitHub', 'hosting', 'docs/usul.md'); }

  for (const n of found.keys()) other.delete(n);
  for (const k of [...other]) if ([...found.values()].some(t => t.name.toLowerCase() === k.toLowerCase())) other.delete(k);
  const groups = {};
  for (const t of found.values()) (groups[t.group] = groups[t.group] || []).push(t.name);
  for (const g of Object.keys(groups)) if (g !== 'engine') groups[g].sort((a, b) => a.localeCompare(b));
  groups.other = [...other].sort();
  return { languages: Object.entries(langs).sort((a, b) => b[1] - a[1]), groups, files: files.length };
}

function render(data, date) {
  const json = JSON.stringify({ ...data, read: date });
  return `/* Generated by tools/site-tools.mjs from the repository; do not edit. Fills the tool list of index.html #made. */
(function () {
    var T = ${json};
    var box = document.getElementById('made'); if (!box) return;
    var lang = document.documentElement.lang || 'en', nf = new Intl.NumberFormat(lang);
    function fill(key, items) {
        var dd = box.querySelector('[data-tools="' + key + '"]'); if (!dd) return;
        if (!items.length) { dd.parentNode.hidden = true; return; }
        dd.textContent = '';
        items.forEach(function (it, i) {
            if (i) dd.appendChild(document.createTextNode(' · '));
            var s = document.createElement('span'); s.textContent = it[0]; dd.appendChild(s);
            if (it[1] != null) { var n = document.createElement('span'); n.className = 'lvl'; n.textContent = nf.format(it[1]); dd.appendChild(document.createTextNode(' ')); dd.appendChild(n); }
        });
    }
    fill('engine', (T.groups.engine || []).map(function (n) { return [n]; }));
    fill('languages', T.languages);
    ['maths', 'testing', 'build', 'hosting', 'fonts', 'other'].forEach(function (g) { fill(g, (T.groups[g] || []).map(function (n) { return [n]; })); });
    var d = box.querySelector('[data-tools="date"]');
    if (d) d.textContent = new Intl.DateTimeFormat(lang, { day: 'numeric', month: 'long', year: 'numeric' }).format(new Date(T.read + 'T12:00:00Z'));
    var c = box.querySelector('[data-tools="files"]'); if (c) c.textContent = nf.format(T.files);
})();
`;
}

const check = process.argv.includes('--check');
try {
  const data = read(), today = new Date().toISOString().slice(0, 10);
  if (check) {
    const old = fs.existsSync(OUT) ? fs.readFileSync(OUT, 'utf8') : '';
    const m = old.match(/"read":"(\d{4}-\d\d-\d\d)"/), want = render(data, m ? m[1] : today);
    if (old !== want) { console.error('site-tools.js is out of date: run node tools/site-tools.mjs'); process.exit(1); }
    console.log('site-tools.js is current'); process.exit(0);
  }
  fs.writeFileSync(OUT, render(data, today));
  const n = Object.values(data.groups).reduce((s, g) => s + g.length, 0);
  console.log(`site-tools.js: ${data.languages.length} languages, ${n} tools (${data.groups.other.length} not yet named: ${data.groups.other.join(', ') || 'none'}), ${data.files} files`);
} catch (e) {
  if (check) { console.error(e); process.exit(1); }
  console.warn('site-tools: could not read the repository, keeping the old list: ' + e.message);
}
