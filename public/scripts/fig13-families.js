// Fig. 13: where the repeating motions live, and the zoom into the fractal border.
// The pictures are computed once (tools/fig13/closed_map.py, closed_stability.py, kaggle_fractal.py) and only shown here.
// The page reads a point on request: tap to pin, the values appear in a fixed place under the picture.
(function () {
    'use strict';
    const $ = id => document.getElementById(id);
    if (!$('fam-in')) return;
    const IMG = '../images/fig13/';
    const PW = 20 * 16 / 9, PH = 20;                       // the sheet: p1 in ±35.56, p2 in ±20 kg m²/s
    const hsv = h => { const f = n => { const k = (n + h * 6) % 6; return Math.round(255 * (1 - .75 * Math.max(0, Math.min(k, 4 - k, 1)))); }; return `rgb(${f(5)},${f(3)},${f(1)})`; };
    const HUE = { 1: 0, 2: .08, 3: .14, 4: .30, 5: .47, 6: .56, 7: .66, 8: .76, 9: .86, 10: .94 };
    const petals = Object.keys(HUE).map(k => `<span><i style="background:${hsv(HUE[k])}"></i>${k}</span>`).join('');

    const VIEWS = {
        kind: {
            src: 'families-petals.webp', box: [-PW, PW, -PH, PH],
            key: `<b>Petals in the drawing</b> ${petals}<span><i style="background:#fff"></i>butterfly</span>`,
            say: `<p><b>What you see.</b> Every coloured line is a row of strikes that make the pendulum repeat. Pick any point on a line, strike the hanging pendulum that hard, and its tip draws one closed curve and then retraces it for ever. There is no friction in this model, so nothing dies away: repeating means exactly repeating.</p>
<p><b>Why lines and not dots.</b> A strike is two numbers, the push on each rod. The motion repeats when there is a moment at which both rods are straight up or straight down together; from there the pendulum runs its own film backwards and arrives where it began. That is one demand on two numbers, and one demand on two numbers leaves a line, the way "height 500 m" leaves a contour line on a map. Walk along a line and the drawing changes smoothly: same number of turns, a little larger or smaller, a little faster or slower.</p>
<p><b>The colours.</b> The colour counts the petals of the drawing, which is how many more times one rod goes round than the other in one lap. White lines are butterflies: the upper rod only swings while the lower one goes round. Far from the centre the strike is so hard that gravity hardly matters, and the lines run out straight like spokes. Near the centre gravity bends them, and inside the bright ring of the eye they crowd, split and break off.</p>`
        },
        stab: {
            src: 'families-stability.webp', box: [-PW, PW, -PH, PH],
            key: `<b>Give it a small push. Then:</b><span><i style="background:#5cf2c7"></i>stable, it stays (20.5 %)</span><span><i style="background:#ffcc6b"></i>neutral, it drifts (28.6 %)</span><span><i style="background:#ff4d4d"></i>unstable, it grows (42.3 %)</span><span><i style="background:#f259f2"></i>unstable and flipping (8.7 %)</span>`,
            say: `<p><b>What you see.</b> The same lines, now coloured by what happens when the repeating motion is disturbed a little. The test is done for 258,868 points along the lines: follow a tiny push through one full lap and see how large it has become.</p>
<p><b>Stable (green).</b> A marble in a bowl. The push never grows; the drawing wobbles around itself and the wobble stays. These are the motions a real pendulum could keep for a while. Almost none of them lies in the glow: 0.5 % sit on chaotic ground.</p>
<p><b>Unstable (red).</b> A pencil balanced on its tip. The push is multiplied by the same factor every lap, so it wins in the end and the pendulum leaves the drawing. Most red lines are only mildly unstable: the typical factor is 1.35 per lap, so they hold their shape for many laps.</p>
<p><b>Unstable and flipping (magenta).</b> The push also changes side every lap, left of the drawing, then right, each time larger. These are the violent ones: the typical factor is 62 per lap, and three quarters of them (74 %) lie inside the glow. Chaos is built around them.</p>
<p><b>Neutral (gold).</b> The border case between bowl and pencil tip: a push neither oscillates nor multiplies, it drifts away at a steady pace. Much of the far field is close to this, because there the pendulum behaves almost as if gravity were switched off.</p>
<p>Along one line the colour can change. Where green turns red, a stable motion loses its hold, and a new line of repeating motions usually branches off at that very point.</p>`
        },
        chaos: {
            src: 'chaos-sheet-fine.webp', box: [-PW, PW, -PH, PH],
            key: `<b>The ground alone</b><span><i style="background:#140d10;outline:1px solid rgba(245,241,234,.4)"></i>dark: a twin struck a hair differently stays beside it</span><span><i style="background:#e2a2aa"></i>bright: the twin goes its own way (chaotic)</span>`,
            say: `<p><b>What you see.</b> The map under the lines, without the lines, at four times the detail of the one behind Fig. 13: 3840 × 2160 strikes, 8.3 million. Each strike is run together with a twin struck a hair differently, for 6.67 s; the brightness says how far apart the two end up. On the whole sheet 5.5 % of the strikes are chaotic by this measure, and they sit in the eye at the centre and along its two lashes.</p>
<p>Switch between this view and the two others: the green lines keep to the dark ground, the magenta ones to the bright.</p>`
        },
        eye: {
            src: 'chaos-eye-fine.webp', box: [-14.4, 14.4, -8.1, 8.1],
            key: `<b>The eye, close</b><span><i style="background:#140d10;outline:1px solid rgba(245,241,234,.4)"></i>dark: regular</span><span><i style="background:#e2a2aa"></i>bright: chaotic</span>`,
            say: `<p><b>What you see.</b> The centre of the sheet, 2.5 times closer, 3840 × 2160 strikes, each watched four times longer (26.67 s). Watching longer gives slow chaos time to show, and the iris fills in: 37 % of this picture is chaotic. The dark islands inside the iris are not noise. Each one surrounds a stable repeating motion, and every strike on the island circles that motion without ever leaving.</p>`
        }
    };

    const inner = $('fam-in'), pan = $('fam-pan'), img = $('fam-img'), read = $('fam-read'), run = $('fam-run'), unpin = $('fam-unpin'), pin = $('fam-pin');
    let view = 'kind', zoom = 1, pinned = null, near = null;
    const O = (window.FIG13_CATALOGUE || []).map((r, i) => ({ i, p1: r[0], p2: r[1], T: r[2], n1: r[3], n2: r[4], E: r[5], s: r[6] }));
    const dots = O.map(o => { const d = document.createElement('span'); d.className = 'fam__dot'; inner.appendChild(d); return d; });
    const stabOf = s => Math.abs(Math.abs(s) - 2) <= .01 ? 'neutral' : Math.abs(s) < 2 ? 'stable' : s > 2 ? 'unstable' : 'unstable and flipping';
    const nameOf = o => o.n1 === 0 ? `a butterfly (lower rod ${Math.abs(o.n2)} turns per lap)` : `a flower of ${Math.abs(o.n1 - o.n2)} petal${Math.abs(o.n1 - o.n2) === 1 ? '' : 's'} (turns per lap ${o.n1}, ${o.n2})`;
    const X = p1 => { const b = VIEWS[view].box; return (p1 - b[0]) / (b[1] - b[0]); }, Y = p2 => { const b = VIEWS[view].box; return (b[3] - p2) / (b[3] - b[2]); };

    function place() {
        O.forEach((o, k) => { const x = X(o.p1), y = Y(o.p2), on = x > 0 && x < 1 && y > 0 && y < 1 && $('fam-dots').getAttribute('aria-pressed') === 'true'; dots[k].hidden = !on; if (on) { dots[k].style.left = 100 * x + '%'; dots[k].style.top = 100 * y + '%'; } });
        if (pinned) { const x = X(pinned[0]), y = Y(pinned[1]); pin.hidden = !(x > 0 && x < 1 && y > 0 && y < 1); pin.style.left = 100 * x + '%'; pin.style.top = 100 * y + '%'; } else pin.hidden = true;
    }
    function setView(v) {
        view = v; img.src = IMG + VIEWS[v].src;
        document.querySelectorAll('#fam-views button').forEach(b => b.setAttribute('aria-pressed', b.dataset.v === v ? 'true' : 'false'));
        $('fam-key').innerHTML = VIEWS[v].key; $('fam-say').innerHTML = VIEWS[v].say; place();
    }
    function setZoom(z) {
        const cx = (pan.scrollLeft + pan.clientWidth / 2) / inner.clientWidth, cy = (pan.scrollTop + pan.clientHeight / 2) / inner.clientHeight;
        zoom = z; inner.style.width = 100 * z + '%';
        pan.scrollLeft = cx * inner.clientWidth - pan.clientWidth / 2; pan.scrollTop = cy * inner.clientHeight - pan.clientHeight / 2;
        document.querySelectorAll('#fam-zoom button').forEach(b => b.setAttribute('aria-pressed', +b.dataset.z === z ? 'true' : 'false'));
    }
    function show() {
        if (!pinned) { read.textContent = 'Tap the picture to pin a strike: its two pushes and its energy are read here, with the nearest repeating motion of the catalogue.'; run.hidden = unpin.hidden = true; place(); return; }
        const [p1, p2] = pinned, K = (6 / 7) * p1 * p1 - (18 / 7) * p1 * p2 + (24 / 7) * p2 * p2;
        let t = `Strike: upper rod ${p1.toFixed(2)}, lower rod ${p2.toFixed(2)} kg·m²/s. It gives the pendulum ${K.toFixed(1)} J. `;
        t += K < 9.8 ? 'Too little for either rod to go over the top (that needs 9.8 J).' : K < 39.2 ? 'Enough for a rod to go over the top; this is the band where chaos is most common.' : 'More than enough for both rods to stand straight up (39.2 J).';
        near = null; let best = 1e9;
        O.forEach(o => { const d = Math.hypot(o.p1 - p1, o.p2 - p2); if (d < best) { best = d; near = o; } });
        if (near) t += ` Nearest in the catalogue, ${best.toFixed(2)} away: ${nameOf(near)}, ${stabOf(near.s)}, period ${near.T.toFixed(2)} s.`;
        read.textContent = t; unpin.hidden = false; run.hidden = !(near && window.__fig13cat); place();
    }
    inner.addEventListener('click', e => {
        const r = inner.getBoundingClientRect(), b = VIEWS[view].box, fx = (e.clientX - r.left) / r.width, fy = (e.clientY - r.top) / r.height;
        let p = [b[0] + fx * (b[1] - b[0]), b[3] - fy * (b[3] - b[2])], best = 22;      // snap to a catalogue dot within 22 px
        if ($('fam-dots').getAttribute('aria-pressed') === 'true') O.forEach(o => { const d = Math.hypot((X(o.p1) - fx) * r.width, (Y(o.p2) - fy) * r.height); if (d < best) { best = d; p = [o.p1, o.p2]; } });
        pinned = p; show();
    });
    unpin.onclick = () => { pinned = null; show(); };
    run.onclick = () => { if (near && window.__fig13cat) window.__fig13cat.choose(window.__fig13cat.orbits[near.i], true); };
    document.querySelectorAll('#fam-views button').forEach(b => b.onclick = () => setView(b.dataset.v));
    document.querySelectorAll('#fam-zoom button').forEach(b => b.onclick = () => setZoom(+b.dataset.z));
    $('fam-dots').onclick = e => { const b = e.currentTarget; b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') === 'true' ? 'false' : 'true'); place(); };
    if (window.innerWidth < 760) $('fam-dots').setAttribute('aria-pressed', 'false');   // on a phone the rings would cover the lines
    setView('kind'); show();

    // ------------------------------------------------------------ the zoom into the border between order and chaos
    const Z = [
        { src: 'chaos-sheet-fine.webp', c: [0, 0], hx: PW, share: 5.5, watch: 6.67, say: 'The whole sheet. The frame marks a piece of the iris, where dark and bright meet.' },
        { src: 'chaos-zoom0.webp', c: [2.046805, 3.987946], hx: 4, share: 47, watch: 26.67, say: 'A piece of the iris. Bright bands of chaos lie between dark tongues of regular motion.' },
        { src: 'chaos-zoom1.webp', c: [5.440555, 2.019196], hx: .5, share: 51, watch: 26.67, say: 'Eight times closer. The edge of a tongue is not a clean line: it is made of thinner tongues.' },
        { src: 'chaos-zoom2.webp', c: [5.420502917, 2.04028975], hx: .0625, share: 48, watch: 26.67, say: 'Eight times closer again. The thinner tongues have thinner tongues along their own edges.' },
        { src: 'chaos-zoom3.webp', c: [5.404650052, 2.027496781], hx: .0078125, share: 49, watch: 26.67, say: 'And again. Still stripes inside stripes, and still about half of the picture is chaotic.' },
        { src: 'chaos-zoom4.webp', c: [5.405337715, 2.027240434], hx: .0009765625, share: 47, watch: 26.67, say: 'The whole picture is now two thousandths of a unit wide: the difference between two taps no hand could tell apart.' },
        { src: 'chaos-zoom5.webp', c: [5.405156135, 2.027106665], hx: .0001220703125, share: 46, watch: 26.67, say: 'The deepest picture, 291,000 times closer than the whole sheet. Dark and bright are still mixed half and half.' }
    ];
    const zi = $('zm-img'), zf = $('zm-frame'), zs = $('zm-say'), zr = $('zm-read'), zp = $('zm-play');
    let zk = 0, timer = null;
    const fmt = w => w >= 1 ? w.toFixed(1) : w >= .01 ? w.toFixed(3) : w.toFixed(6);
    function step(k) {
        zk = k; const z = Z[k], nx = Z[k + 1]; zi.src = IMG + z.src;
        document.querySelectorAll('#zm-steps button').forEach((b, j) => b.setAttribute('aria-pressed', j === k ? 'true' : 'false'));
        if (nx) { const hy = z.hx * 9 / 16, nhy = nx.hx * 9 / 16; zf.hidden = false; zf.style.left = 100 * (nx.c[0] - nx.hx - z.c[0] + z.hx) / (2 * z.hx) + '%'; zf.style.top = 100 * (z.c[1] + hy - nx.c[1] - nhy) / (2 * hy) + '%'; zf.style.width = 100 * nx.hx / z.hx + '%'; zf.style.height = 100 * nhy / hy + '%'; } else zf.hidden = true;
        zs.textContent = z.say;
        zr.textContent = `Picture ${k + 1} of ${Z.length} · width ${fmt(2 * z.hx)} kg·m²/s · ${k ? Math.round(PW / z.hx).toLocaleString('en') + ' times closer than the sheet' : 'the whole sheet'} · chaotic ${z.share} % · each strike watched ${z.watch} s`;
    }
    function stop() { clearInterval(timer); timer = null; zp.textContent = 'Play'; }
    zp.onclick = () => { if (timer) return stop(); zp.textContent = 'Pause'; if (zk === Z.length - 1) step(0); timer = setInterval(() => { if (zk === Z.length - 1) return stop(); step(zk + 1); }, 2600); };
    document.querySelectorAll('#zm-steps button').forEach((b, j) => b.onclick = () => { stop(); step(j); });
    zf.onclick = () => { stop(); if (zk < Z.length - 1) step(zk + 1); };
    step(0);
    window.__fig13fam = { setView, setZoom, step, state: () => ({ view, zoom, pinned, near: near && near.i, zk }) };
})();
