/* From symbols to code — Fig. 8, draw and decompose.
   ⟦key|text⟧ marks a quantity; the same key in the formula, the code and the table lights up together.
   The "Now" column is filled from Sim.live() in draw-decompose.html. */
window.WALK = window.WALK || {};

window.WALK.dft = {
    intro: 'Six steps from a pen stroke to a chain of circles, with a built-in check at the end. The table reads the current shape live; draw something new and the numbers change.',
    steps: [
        {
            title: 'Equal arc length',
            where: 'resamp()',
            math: 's<sub>i</sub> = Σ<sub>j≤i</sub> |p<sub>j</sub> − p<sub>j−1</sub>|, &nbsp; ⟦L|L⟧ = s<sub>last</sub>, &nbsp; ⟦ds|Δs⟧ = L / (⟦N|N⟧ − 1)',
            note: 'Your hand does not move at constant speed, so raw points bunch up where you slowed down. Placing N points at equal distance along the stroke makes the parameter t proportional to distance travelled: the pen of the reconstruction moves at constant speed.',
            code: `tot += Math.hypot(pts[i].x - pts[i - 1].x, pts[i].y - pts[i - 1].y);
ds.push(tot);
...
var ⟦ds|step = tot / (N - 1)⟧, res = [{ x: pts[0].x, y: pts[0].y }], j = 0;`,
            syms: [
                ['N', 'N', 'NS', 'number of samples'],
                ['L', 'L', 'arcLen', 'stroke length, scale-free units'],
                ['ds', 'Δs', 'step', 'spacing between samples']
            ]
        },
        {
            title: 'Remove the centre',
            where: 'decompose()',
            math: 'z<sub>n</sub> = p<sub>n</sub> − (⟦mx|x̄⟧ + i⟦my|ȳ⟧), &nbsp; ⟦E|⟨|z|²⟩⟧ = (1/N) Σ |z<sub>n</sub>|²',
            note: 'The mean is exactly c<sub>0</sub>, the circle that does not turn. Subtracting it puts the origin at the centre of mass of a uniform wire bent into your shape. ⟨|z|²⟩ is then that wire’s moment of inertia per unit mass, I/m, which the circles share out between them.',
            code: `meanX /= NS; meanY /= NS;
samples = r.map(function (p) { return { x: p.x - meanX, y: p.y - meanY }; });
...
⟦E|meanZ2 /= NS⟧;`,
            syms: [
                ['mx', 'x̄', 'meanX', 'centre of the raw samples'],
                ['my', 'ȳ', 'meanY', ''],
                ['z0', 'z₀', 'samples[0]', 'first centred sample'],
                ['E', '⟨|z|²⟩', 'meanZ2', 'mean squared radius = I/m of the wire']
            ]
        },
        {
            title: 'One coefficient',
            where: 'dft() — the double loop',
            math: 'c<sub>k</sub> = (1/N) Σ<sub>n</sub> z<sub>n</sub> e<sup>−2πikn/N</sup> = ⟦re|a⟧ + i⟦im|b⟧',
            note: 'Writing z<sub>n</sub> = x + iy and e<sup>−iθ</sup> = cos θ − i sin θ, the real part is x cos θ + y sin θ and the imaginary part is y cos θ − x sin θ. The table shows the largest coefficient.',
            code: `var a = TAU * k * n / N, c = Math.cos(a), s = Math.sin(a);
⟦re|re += z[n].x * c + z[n].y * s⟧;
⟦im|im += z[n].y * c - z[n].x * s⟧;
...
re /= N;
im /= N;`,
            syms: [
                ['k1', 'k', 'coefs[0].k', 'frequency of the largest circle'],
                ['re', 'Re c', 're', ''],
                ['im', 'Im c', 'im', '']
            ]
        },
        {
            title: 'Radius, phase and sorting',
            where: 'dft() — end',
            math: '⟦A||c<sub>k</sub>|⟧ = √(a² + b²), &nbsp; ⟦ph|arg c<sub>k</sub>⟧ = atan2(b, a); &nbsp; keep the ⟦K|K⟧ largest',
            note: 'Each coefficient is one circle: radius |c<sub>k</sub>|, turning k times per loop, starting at angle arg c<sub>k</sub>. Parseval (step 6) shows that keeping the largest ones minimises the squared error.',
            code: `out.push({ k: k, re: re, im: im, ⟦A|amp: Math.hypot(re, im)⟧, ⟦ph|phase: Math.atan2(im, re)⟧ });
...
return out.sort(function (a, b) { return b.amp - a.amp; });`,
            syms: [
                ['A', '|c|', 'amp', 'radius of the largest circle'],
                ['ph', 'arg c', 'phase', 'its starting angle'],
                ['K', 'K', 'K.value', 'circles in use'],
                ['tot', '', 'coefs.length', 'coefficients computed']
            ]
        },
        {
            title: 'Circles redraw the shape',
            where: 'chainAt() and the clock',
            math: 'z<sub>K</sub>(⟦t|t⟧) = Σ<sub>top K</sub> |c<sub>k</sub>| e<sup>i(kt + arg c<sub>k</sub>)</sup> = ⟦x|x⟧ + i⟦y|y⟧, &nbsp; t ← t + 2π Δt / ⟦tl|T<sub>loop</sub>⟧',
            note: 'This is Fig. 7 again, with the arms chosen by the transform instead of by hand. At t = 2πn/N the sum hits sample n of your drawing exactly when K includes every coefficient.',
            code: `var c = coefs[i], ang = c.k * time + c.phase;
var vx = c.amp * Math.cos(ang), vy = c.amp * Math.sin(ang);
x += vx;
y += vy;
...
⟦t|t += TAU * dt / loop.value⟧;`,
            syms: [
                ['t', 't', 't', 'loop parameter'],
                ['tl', 'T', 'loop.value', 'seconds per loop'],
                ['x', 'Re z', 'z.x', 'pen x'],
                ['y', 'Im z', 'z.y', 'pen y']
            ]
        },
        {
            title: 'The check: Parseval',
            where: 'rebuild()',
            math: '⟦err|e<sub>RMS</sub>⟧ measured point by point &nbsp; = &nbsp; ⟦errP|√(⟨|z|²⟩ − Σ<sub>kept</sub>|c<sub>k</sub>|²)⟧',
            note: 'Two independent routes to one number. The left one reconstructs all 256 samples and measures the distance; the right one only adds up squared radii. If they agree, the transform, the sorting and the reconstruction are all right.',
            code: `for (i = 0; i < n; i++) ⟦kept|kept += coefs[i].amp * coefs[i].amp⟧;
⟦errP|errP = Math.sqrt(Math.max(0, meanZ2 - kept))⟧;
...
e2 += Math.pow(z.x - samples[i].x, 2) + Math.pow(z.y - samples[i].y, 2);
...
⟦err|err = Math.sqrt(e2 / NS)⟧;`,
            syms: [
                ['kept', 'Σ|c|²', 'kept', 'share of ⟨|z|²⟩ in the K circles'],
                ['cap', '', 'kept / meanZ2', 'fraction of ⟨|z|²⟩ kept'],
                ['err', 'e (direct)', 'err', 'RMS distance at the samples'],
                ['errP', 'e (Parseval)', 'errP', 'predicted RMS distance']
            ]
        }
    ]
};
