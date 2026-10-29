// A 30-line element builder, so the view files read as structure rather
// than as a pile of createElement calls. This is the whole "framework".
// Carried over from Physik Radar (src/claude/view/dom.js), unused helpers removed.

/**
 * el('div', {class: 'x', onclick: fn}, child, 'text', …)
 *
 * Properties starting with `on` become listeners; everything else is set
 * as an attribute. Null/undefined/false children are skipped, so callers
 * can write `cond && el(…)` inline. An href that is not http(s) or a #fragment
 * is dropped, so a stored javascript: link can never become clickable.
 */
export function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v == null || v === false) continue;
    if (k === 'href' && !String(v).startsWith('#') && !String(v).startsWith('/')) {
      try { if (!['https:', 'http:'].includes(new URL(String(v)).protocol)) continue; } catch { continue; }
    }
    if (k.startsWith('on') && typeof v === 'function') node.addEventListener(k.slice(2), v);
    else node.setAttribute(k, v === true ? '' : String(v));
  }
  return append(node, children);
}

export function append(node, children) {
  for (const c of children.flat(Infinity)) {
    if (c == null || c === false) continue;
    node.append(c instanceof Node ? c : document.createTextNode(String(c)));
  }
  return node;
}

/** Replaces a node's contents in one go. */
export function fill(node, ...children) {
  node.replaceChildren();
  return append(node, children);
}

/** The hostname of a URL, for cards without a company name. */
export function hostOf(url) {
  try { return new URL(url).hostname.replace(/^www\./, ''); } catch { return url ?? ''; }
}
