// Fig. 13: the eye, straightened. Three pictures of the same chaos map (tools/fig13/spin_fold.py) and what each one teaches.
// A strike (p1, p2) is rewritten as spin X and fold Y with K = X^2 + Y^2; a tap pins one strike and reads its split.
(function () {
    'use strict';
    const $ = id => document.getElementById(id);
    if (!$('st-in')) return;
    const IMG = '../images/fig13/';
    const IS = 8 / 3, MU = 7 / 96;                                   // kg m^2: straight stick about the pin; the elbow's own inertia
    const a = 1 / Math.sqrt(2 * IS), b = Math.sqrt(MU / 2) / 7;      // X = a (p1 + p2),  Y = b (-30 p1 + 66 p2)
    const toXY = (p1, p2) => [a * (p1 + p2), b * (-30 * p1 + 66 * p2)];
    const det = a * 66 * b + a * 30 * b;
    const toP = (X, Y) => [(66 * b * X - a * Y) / det, (30 * b * X + a * Y) / det];
    const LK = Math.log(3000), R = 8.8;
    const VIEWS = {
        struck: {
            src: 'eye-struck.webp', ratio: '16 / 9',
            at: (fx, fy) => [-14.4 + 28.8 * fx, 8.1 - 16.2 * fy], of: (p1, p2) => [(p1 + 14.4) / 28.8, (8.1 - p2) / 16.2],
            labels: [[92, 13, 'spin'], [24, 5, 'fold'], [3, 93, 'across: push on the upper rod · up: push on the lower rod']],
            say: `<p><b>As struck.</b> This is the eye as the page has shown it so far: across, the push on the upper rod; up, the push on the lower rod. The white curves join strikes of equal energy (9.8, 29.4 and 39.2 J). They are ellipses, long and tilted, and the whole eye leans with them.</p>
<p><b>Why it leans.</b> The two pushes are not independent. The lower rod hangs from the moving end of the upper one, so pushing one rod drags the other along, and the energy of a strike is not simply "energy of the first push plus energy of the second". The sheet is drawn on square paper, but measured by energy its two axes stand at 139° to each other, not 90°. It is skew graph paper printed as if it were square. That is the shear you see.</p>
<p>The two grey lines are the directions that do stand at a right angle by energy. Along one the pendulum is struck so that both rods turn together, as one straight stick: <b>spin</b>. Along the other the rods are struck against each other so that the elbow bends and nothing turns as a whole: <b>fold</b>. Press "Spin and fold" to redraw the eye on those axes.</p>`
        },
        sf: {
            src: 'eye-spin-fold.webp', ratio: '1 / 1',
            at: (fx, fy) => toP(-R + 2 * R * fx, R - 2 * R * fy), of: (p1, p2) => { const [X, Y] = toXY(p1, p2); return [(X + R) / (2 * R), (R - Y) / (2 * R)]; },
            labels: [[80, 46, 'spin →'], [52, 2, 'fold ↑'], [70, 3, '60°'], [67, 44.5, '9.8 J'], [84, 52, '39.2 J']],
            say: `<p><b>Spin and fold.</b> The same map, nothing recomputed, only redrawn: across, how much of the strike is spin; up, how much is fold. Every strike is some of each, and on these axes the two do not share energy, so the energies simply add, as the squares of two perpendicular sides add in Pythagoras' theorem: energy = spin² + fold². Strikes of equal energy now lie on circles, and the eye stands upright.</p>
<p><b>The lashes are at 60°, exactly.</b> A lash is the border between strikes whose elbow folds right through and strikes whose elbow swings back. To fold through, the stick must pass the fully folded position while still carrying its spin. Fold a metre rule in half: it is half as long, and a body half as long is four times easier to turn. So, like a skater who pulls in her arms, the folded stick must spin four times as energetically. The strike can afford that when its fold part holds more than three times the energy of its spin part. The border, fold² = 3 · spin², is a pair of straight lines at 60° to the spin axis, the blue lines. With rods of other lengths or weights the angle is different; 60° belongs to two equal rods.</p>
<p><b>Almost a mirror.</b> Reverse the fold part of a strike and the picture nearly repeats: above and below the spin axis look alike. Without gravity they would be identical. Gravity spoils it most in the iris, where a mirrored strike gets the same verdict (chaotic or not) 69 times in 100; among hard strikes, above 196 J, 97 times in 100.</p>`
        },
        un: {
            src: 'eye-unrolled.webp', ratio: '16 / 9',
            at: (fx, fy) => { const ph = (-90 + 180 * fx) * Math.PI / 180, r = Math.sqrt(Math.exp(LK * (1 - fy))); return toP(r * Math.cos(ph), r * Math.sin(ph)); },
            of: (p1, p2) => { const [X, Y] = toXY(p1, p2); let ph = Math.atan2(Y, X) * 180 / Math.PI; if (ph > 90) ph -= 180; if (ph <= -90) ph += 180; return [(ph + 90) / 180, 1 - Math.log(Math.max(X * X + Y * Y, 1e-9)) / LK]; },
            labels: [[1, 2, 'pure fold'], [17.2, 2, '−60°'], [50.5, 2, 'pure spin'], [84, 2, '+60°'], [1, 67, '9.8 J'], [1, 53.3, '29.4 J'], [90, 49.6, '39.2 J'], [1, 29.5, '196 J'], [1, 94, 'up: energy of the strike, ×10 per step · across: the split between spin and fold']],
            say: `<p><b>Unrolled.</b> Cut the round eye along a radius and flatten it, as a map flattens the globe. Across is now the direction of the strike: pure spin in the middle, pure fold at the two edges. Up is its energy, from 1 J at the bottom to 3000 J at the top, ten times more with every equal step. Grey is beyond the edge of the sheet.</p>
<p><b>What it shows at a glance.</b> The pupil is the dark floor below 9.8 J. The iris is a band lying across the picture, roughly from 10 to 200 J: chaos is a matter of energy, of having about as much as gravity trades during the motion. The lashes are two upright lines at ±60°: far above the band, chaos is a matter of direction only.</p>
<p><b>How many numbers matter.</b> A strike is two numbers. High in this picture everything runs straight up and down, which says that only one of them counts there: the split. A harder strike with the same split draws the same curve, only faster, because gravity no longer has a say. Inside the band both numbers count, and finely: the pattern changes with every small step in either direction. </p>
<p><b>The lower edge depends on patience.</b> This picture watches each strike for 6.67 s, and a strike that is nearly pure spin looks regular up to about 16 J. Watched four times longer, the same strikes turn chaotic from about 12 J. Slow chaos needs time to show, so the floor of the band sinks as one waits.</p>`
        }
    };
    const inner = $('st-in'), img = $('st-img'), pin = $('st-pin'), read = $('st-read'), unpin = $('st-unpin'), lab = $('st-labels');
    let view = 'struck', pinned = null;
    function place() { if (!pinned) { pin.hidden = true; return; } const [x, y] = VIEWS[view].of(pinned[0], pinned[1]); pin.hidden = !(x > 0 && x < 1 && y > 0 && y < 1); pin.style.left = 100 * x + '%'; pin.style.top = 100 * y + '%'; }
    function show() {
        if (!pinned) { read.textContent = 'Tap the picture to pin a strike. It stays pinned when you change the picture, so you can follow one strike through all three.'; unpin.hidden = true; place(); return; }
        const [p1, p2] = pinned, [X, Y] = toXY(p1, p2), K = X * X + Y * Y; let ph = Math.atan2(Y, X) * 180 / Math.PI; if (ph > 90) ph -= 180; if (ph <= -90) ph += 180;
        read.textContent = `Strike: upper rod ${p1.toFixed(2)}, lower rod ${p2.toFixed(2)} kg·m²/s. Spin part ${(X * X).toFixed(1)} J + fold part ${(Y * Y).toFixed(1)} J = ${K.toFixed(1)} J. Split: ${ph.toFixed(1)}° from pure spin. ` + (Y * Y > 3 * X * X ? 'Fold has more than three times the spin: without gravity the elbow folds right through.' : 'Fold has less than three times the spin: without gravity the elbow swings back.');
        unpin.hidden = false; place();
    }
    function setView(v) {      // on a phone the unrolled chart is drawn taller (4:3): its axes are an angle and an energy, so stretching is harmless
        view = v; const V = VIEWS[v]; img.style.aspectRatio = v === 'un' && window.innerWidth < 640 ? '4 / 3' : V.ratio; img.src = IMG + V.src; inner.classList.toggle('is-square', V.ratio === '1 / 1');
        document.querySelectorAll('#st-views button').forEach(x => x.setAttribute('aria-pressed', x.dataset.v === v ? 'true' : 'false'));
        lab.innerHTML = V.labels.map(l => `<span style="left:${l[0]}%;top:${l[1]}%">${l[2]}</span>`).join(''); $('st-say').innerHTML = V.say; place();
    }
    inner.addEventListener('click', e => { const r = img.getBoundingClientRect(), fx = (e.clientX - r.left) / r.width, fy = (e.clientY - r.top) / r.height; if (fx < 0 || fx > 1 || fy < 0 || fy > 1) return; pinned = VIEWS[view].at(fx, fy); show(); });
    unpin.onclick = () => { pinned = null; show(); };
    document.querySelectorAll('#st-views button').forEach(x => x.onclick = () => setView(x.dataset.v));
    setView('struck'); show();
    window.__fig13straight = { setView, toXY, toP, state: () => ({ view, pinned }) };
})();
