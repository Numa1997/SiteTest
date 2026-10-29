// Cleans the HTML of one e-mail so it can sit inside the /absagen page. Pure JavaScript, no runtime APIs,
// so it runs in the Worker and in Node's tests alike, in linear time (one pass with a sticky regex).
//
// The principle: nothing of the input is passed through. The mail is cut into tokens (tags, text, comments);
// every tag on the allow-list is written out anew by this code, with only allow-listed attributes, each value
// decoded, checked and escaped again; text is escaped; every element is closed in the right order; end tags
// that close nothing are dropped. So whatever the input, the output is well-formed, holds no script, no event
// handler, no style block, no form, no frame, no outside address except https/mailto links, and cannot close
// the box it is placed in. Elements that are not allowed lose their tag and keep their text; elements whose
// content is code or hidden text (script, style, xmp, noembed, …) are dropped with their content.

const ALLOWED = new Set(('a abbr address article aside b bdi bdo big blockquote br caption center cite code col colgroup dd del dfn div dl ' +
  'dt em figcaption figure font footer h1 h2 h3 h4 h5 h6 header hr i img ins kbd label li main mark nav ol p pre q s samp section ' +
  'small span strike strong sub sup table tbody td tfoot th thead time tr tt u ul wbr').split(' '));
const VOID = new Set(['br', 'col', 'hr', 'img', 'wbr']);
// Content is code, hidden or raw text: drop the element together with everything inside it.
const DROP_WITH_CONTENT = new Set(['script', 'style', 'title', 'textarea', 'xmp', 'plaintext', 'noembed', 'noframes', 'noscript', 'iframe',
  'object', 'embed', 'applet', 'template', 'svg', 'math', 'head', 'select', 'option', 'button', 'canvas', 'audio', 'video', 'frameset', 'frame']);
const RAW_TEXT = new Set(['script', 'style', 'title', 'textarea', 'xmp', 'noembed', 'noframes', 'noscript', 'iframe']);
const ATTRS = new Set(['style', 'title', 'dir', 'lang', 'align', 'valign', 'width', 'height', 'bgcolor', 'color', 'face', 'size', 'border',
  'cellpadding', 'cellspacing', 'colspan', 'rowspan', 'nowrap', 'start', 'span', 'alt', 'href', 'src', 'datetime', 'type']);
const BLOCKED_CSS = /^(position|top|left|right|bottom|inset(-.*)?|z-index|transform(-.*)?|translate|scale|rotate|content|clip-path|mask(-.*)?|behavior|-moz-binding|pointer-events|cursor)$/;

const NAMED = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', colon: ':', tab: '\t', newline: '\n', sol: '/', lpar: '(', rpar: ')' };
/** Decodes character references enough to see what an attribute really says (e.g. &#106;avascript:). */
export function decodeEntities(s) {
  return s.replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);?/gi, (m, ref) => {
    if (ref[0] === '#') {
      const code = ref[1] === 'x' || ref[1] === 'X' ? parseInt(ref.slice(2), 16) : parseInt(ref.slice(1), 10);
      return Number.isFinite(code) && code > 0 && code < 0x110000 ? String.fromCodePoint(code) : '';
    }
    return Object.hasOwn(NAMED, ref.toLowerCase()) ? NAMED[ref.toLowerCase()] : m;
  });
}
const escAttr = s => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// Text: keep character references (they can only ever become characters), escape everything else that matters.
const escText = s => s.replace(/&(?!(?:#x[0-9a-f]+|#\d+|[a-z][a-z0-9]{1,31});)/gi, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function cleanStyle(raw) {
  const v = decodeEntities(raw);
  if (/[\\<>]|\/\*|url\s*\(|expression|@|javascript:|image-set|-webkit-image/i.test(v)) return null;   // escapes and tricks: drop it all
  const keep = [];
  for (const decl of v.split(';')) {
    const i = decl.indexOf(':');
    if (i < 1) continue;
    const prop = decl.slice(0, i).trim().toLowerCase();
    const val = decl.slice(i + 1).trim();
    if (!/^-?[a-z][a-z-]*$/.test(prop) || BLOCKED_CSS.test(prop) || !val) continue;
    keep.push(prop + ':' + val);
  }
  return keep.length ? keep.join(';') : null;
}

/**
 * @param {string} html  the mail's HTML
 * @param {(cid: string) => string|null} imageFor  maps an inline image (src="cid:…") to this site's address for it, or null
 * @returns {string} clean HTML
 */
export function sanitizeMail(html, imageFor = () => null) {
  const out = [];
  const stack = [];
  const open = new Map();                                       // how many of each element are open: an end tag for none costs nothing
  const n = html.length;
  let i = 0;
  let nextGt = html.indexOf('>');                               // no ">" left means no tag can end: the rest is text
  while (i < n) {
    const lt = html.indexOf('<', i);
    if (lt < 0) { out.push(escText(html.slice(i))); break; }
    if (lt > i) out.push(escText(html.slice(i, lt)));
    i = lt;
    if (html.startsWith('<!--', i)) {                           // comment (also conditional comments): gone
      const e = html.indexOf('-->', i + 4);
      i = e < 0 ? n : e + 3;
      continue;
    }
    const c1 = html.charCodeAt(i + 1);
    if (c1 === 33 || c1 === 63) {                               // <!doctype …>, <?xml …?>: gone
      const e = html.indexOf('>', i + 2);
      i = e < 0 ? n : e + 1;
      continue;
    }
    if (nextGt < i) nextGt = html.indexOf('>', i);
    if (nextGt < 0) { out.push(escText(html.slice(i))); break; }
    if (nextGt - i >= MAX_TAG) { out.push('&lt;'); i += 1; continue; }   // no ">" close enough: cannot be a tag
    const isEnd = c1 === 47;                                    // "/"
    const nameAt = isEnd ? i + 2 : i + 1;
    NAME.lastIndex = nameAt;
    const nm = NAME.exec(html);
    if (!nm) { out.push('&lt;'); i += 1; continue; }            // a lone "<" is text
    const name = nm[0].toLowerCase();
    const end = tagEnd(html, nameAt + nm[0].length, Math.min(n, i + MAX_TAG));
    if (end < 0) { out.push('&lt;'); i += 1; continue; }        // unfinished tag: show it as text, never as markup
    const inner = html.slice(nameAt + nm[0].length, end);
    i = end + 1;
    if (isEnd) {
      if (!open.get(name)) continue;                            // an end tag that closes nothing is dropped
      const at = stack.lastIndexOf(name);                       // the stack is at most MAX_DEPTH deep
      while (stack.length > at) { const top = stack.pop(); open.set(top, open.get(top) - 1); out.push('</' + top + '>'); }
      continue;
    }
    if (DROP_WITH_CONTENT.has(name)) {
      if (name === 'plaintext') break;                          // everything after it would be raw text: drop the rest
      if (/\/\s*$/.test(inner) && !RAW_TEXT.has(name)) continue;
      const close = new RegExp('<(/?)' + name + '(?=[\\s/>])', 'gi');
      close.lastIndex = i;
      let depth = 1, c;
      while (depth > 0 && (c = close.exec(html))) { if (c[1]) depth--; else if (!RAW_TEXT.has(name)) depth++; }
      if (!c) { i = n; continue; }
      const e = html.indexOf('>', close.lastIndex);
      i = e < 0 ? n : e + 1;
      continue;
    }
    if (!ALLOWED.has(name)) continue;                           // unknown element: tag gone, its text stays
    if (!VOID.has(name) && stack.length >= MAX_DEPTH) continue; // deeper than any real mail: the tag is dropped, the text stays
    out.push(openTag(name, inner, imageFor));
    if (!VOID.has(name)) { stack.push(name); open.set(name, (open.get(name) ?? 0) + 1); }
  }
  while (stack.length) out.push('</' + stack.pop() + '>');
  return out.join('');
}

const NAME = /[a-zA-Z][a-zA-Z0-9-]*/y;
const MAX_TAG = 4096;
const MAX_DEPTH = 200;
const ATTR = /([^\s"'>\/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/g;

/** Where the tag that starts before k ends (index of its ">"), honouring quoted values; -1 if not within limit. */
function tagEnd(html, k, limit) {
  let afterEq = false;
  for (; k < limit; k++) {
    const c = html.charCodeAt(k);
    if (c === 62) return k;                                     // >
    if (afterEq && (c === 34 || c === 39)) {                    // " or ' opens a value
      const e = html.indexOf(c === 34 ? '"' : "'", k + 1);
      if (e < 0 || e >= limit) return -1;
      k = e; afterEq = false; continue;
    }
    if (c === 61) afterEq = true;                               // =
    else if (c > 32) afterEq = false;
  }
  return -1;
}

function openTag(name, inner, imageFor) {
  const attrs = [];
  let a;
  ATTR.lastIndex = 0;
  while ((a = ATTR.exec(inner))) {
    const key = a[1].toLowerCase();
    if (!ATTRS.has(key)) continue;
    const raw = a[2] ?? a[3] ?? a[4] ?? '';
    const val = decodeEntities(raw);
    if (key === 'href') {
      if (name !== 'a') continue;
      if (!/^(https?:\/\/|mailto:)/i.test(val.replace(/[\u0000-\u0020]/g, ''))) continue;
      attrs.push(['href', val.trim()]);
      continue;
    }
    if (key === 'src') {
      if (name !== 'img') continue;
      const v = val.trim();
      if (/^cid:/i.test(v)) { const local = imageFor(v.slice(4)); if (local) attrs.push(['src', local]); }
      else if (/^data:image\/(png|jpe?g|gif|webp);base64,[a-z0-9+/=\s]+$/i.test(v)) attrs.push(['src', v.replace(/\s+/g, '')]);
      continue;
    }
    if (key === 'style') { const st = cleanStyle(raw); if (st) attrs.push(['style', st]); continue; }
    if (key === 'type' && !['ol', 'ul', 'li'].includes(name)) continue;
    if (val.length > 300) continue;
    attrs.push([key, val]);
  }
  if (name === 'a') attrs.push(['target', '_blank'], ['rel', 'noopener noreferrer nofollow']);
  return '<' + name + attrs.map(([k, v]) => ' ' + k + '="' + escAttr(v) + '"').join('') + '>';
}
