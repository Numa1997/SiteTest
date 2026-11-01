---
name: tune-with-numa
description: Use for any change judged by eye on Phyein Usul (layout, line breaks, spacing, sizes, colours, how strong an effect looks, animation speed, "make it look right"), and whenever a fix loop is not converging. Stop and review; instead of iterating alone with screenshots and scripts, build a ?tune=1 panel with live sliders, include Numa, let Numa find the values, then apply them once. Also how Claude helps Numa prompt better and how Numa helps Claude not waste time.
---

# Tune with Numa

Numa's rule (1 November 2026): minimise waste on both sides. Claude builds and measures; Numa's eye decides how it looks.
Seven rounds of "build, screenshot, find a flaw, patch" cost more than one tuner and two minutes of Numa's time.

## The deal, in Numa's words

1. **Stop and review.** Before each new round, ask: is what I am doing now ridiculous? If it is, stop, say so in one line, and
   change the method instead of trying harder.
2. **Visual edits are done differently:** not by Claude guessing, but on a human interface, a `?tune=1` panel where Numa tests
   and finds the right parameters.
3. **Include Numa** in any edit judged by eye, from the start, not after five rounds.
4. **Best use of one another.** Always ask: what is Claude fast at (code, measurement, checks), and what can only Numa do (see,
   judge, decide)? Give each the part they are good at.
5. **No endless scripts.** Never write a script without knowing what it is for; say its purpose in one line first. No pile of
   throwaway probes.
6. **Minimise waste on both sides.**
7. **Claude helps Numa prompt better:** when a request is vague or costly, say so in one line and offer the sharper prompt (below).
8. **Numa helps Claude not waste time:** Claude asks for what only Numa has (a screenshot, the device, the values from the tuner, a
   yes or no) instead of reconstructing it.

## When this applies

The result is judged by looking, and more than one value could be "right": where an equation breaks, an indent, a gap, a font
size, a colour, a line weight, a speed, the strength of a visible effect (how much drag shows), a threshold.

It does not apply when the answer is a fact you can check (a wrong number, a crash, a failing check): fix those directly.

## The procedure

1. **One attempt, at most.** If the first try is not clearly right, stop. Do not start a second blind round.
2. **Name the knobs, in two lines, and ask.** "The knobs are A (range), B (range), C (on/off). Tune it yourself on `?tune=1`, or
   shall I pick?" If Numa is busy, pick sensible defaults and say which.
3. **Ask for Numa's eyes.** If you need to know what Numa sees, ask for a screenshot and the device; do not reconstruct it with
   probe scripts.
4. **Build the tuner** (template below): a small fixed panel on the page itself, shown only with `?tune=1`, one slider or toggle
   per knob, the page redrawn live, values kept in `localStorage`, and **Copy settings**, which copies them as JSON.
5. **Hand over** with one line: the address (`…/page.html?tune=1`), what each knob does, "press Copy settings and paste it here".
6. **Apply once**: write the pasted values into the code as the defaults, remove the tuner (or leave it behind `?tune=1` if Numa
   wants it), check once in a browser, one screenshot, done.

Every round with Numa: what changed, one screenshot, the one decision needed. If two rounds have not converged, stop and say so.

## Tuner template

Paste into the page under work (inline script is allowed by the site's policy). Bind each knob to a CSS custom property or to a
JavaScript constant the drawing reads, and call the page's redraw in `apply`.

```html
<script>
(function () {
  if (new URLSearchParams(location.search).get('tune') !== '1') return;
  var KEY = 'tune:' + location.pathname;
  /* one entry per knob: name, min, max, step, default, apply(value) */
  var knobs = [
    { name: 'indent (rem)', min: 0, max: 4, step: 0.25, value: 2,
      apply: function (v) { document.documentElement.style.setProperty('--eq-indent', v + 'rem'); } },
    { name: 'drag on', min: 0, max: 1, step: 1, value: 0,
      apply: function (v) { window.TUNE_DRAG = !!v; if (window.redraw) window.redraw(); } }
  ];
  var saved = {}; try { saved = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) {}
  var box = document.createElement('div');
  box.style.cssText = 'position:fixed;left:8px;bottom:8px;z-index:9999;background:#fff;border:1px solid #333;border-radius:8px;' +
    'padding:8px 10px;font:12px/1.4 monospace;max-width:92vw;box-shadow:0 2px 8px rgba(0,0,0,.2)';
  knobs.forEach(function (k) {
    if (k.name in saved) k.value = saved[k.name];
    var row = document.createElement('label'), out = document.createElement('b'), inp = document.createElement('input');
    row.style.cssText = 'display:flex;gap:8px;align-items:center';
    inp.type = 'range'; inp.min = k.min; inp.max = k.max; inp.step = k.step; inp.value = k.value;
    out.textContent = k.value;
    inp.oninput = function () { k.value = +inp.value; out.textContent = k.value; k.apply(k.value); store(); };
    row.append(k.name, inp, out); box.append(row); k.apply(k.value);
  });
  var copy = document.createElement('button'); copy.textContent = 'Copy settings';
  copy.onclick = function () { var o = {}; knobs.forEach(function (k) { o[k.name] = k.value; });
    navigator.clipboard.writeText(JSON.stringify(o)); copy.textContent = 'Copied'; };
  box.append(copy); document.body.append(box);
  function store() { var o = {}; knobs.forEach(function (k) { o[k.name] = k.value; }); try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {} }
})();
</script>
```

To let Numa try it on a phone before anything is merged, push to the branch and say so; Cloudflare builds only `main`
(`docs/usul.md`), so for a phone test either merge with Numa's yes, or serve it locally and send screenshots.

## Helping Numa prompt (the other half)

When a request is ambiguous or will be costly, say so in one line and offer the sharper version. A good prompt for a visual change
names five things:

1. **Where:** the page and the element ("Iron, Cotton and the Head, phone, the box 'Where the energy goes'").
2. **What is wrong:** what Numa sees, best with a screenshot ("keeps growing downwards as I scroll").
3. **What right looks like:** a reference or a rule ("a long equation breaks into rows at its = signs").
4. **Who tunes:** "build me a tuner" or "pick it yourself".
5. **Limits:** what must not change (the physics, the text, the other languages), and whether to merge.

Example: "Phone, Fig. 9 note: equations run past the box. Break them at = into rows; give me a tuner for the indent and the
spacing; don't change the TeX; don't merge."
