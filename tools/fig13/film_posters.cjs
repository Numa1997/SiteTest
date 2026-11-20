// Fig. 13: one still for each film of the films panel on the Fig. 13 page, taken from the film itself (window.renderFrame) in
// headless Chromium, and the film's length. Writes public/images/fig13/films/<n>.png (converted to .webp by film_posters.py) and
// prints the lengths.   Serve public/ on port 8765 first:  (cd public && python3 -m http.server 8765) &  node tools/fig13/film_posters.cjs
const { chromium } = require('playwright'), path = require('path');
const OUT = path.join(__dirname, '../../public/images/fig13/films/');
const FILMS = [   // [file, stage width, height, fraction of the film for the still]
    ['live-gift.html', 1080, 1920, 0.93], ['live-construction.html', 1080, 1920, 0.9], ['live-catch.html?auto=1', 1080, 1920, 0.6],
    ['dive.html', 1080, 1920, 0.85], ['together.html?scene=phone', 1080, 1920, 0.7], ['together.html?scene=wide', 1920, 1080, 0.7],
    ['turning.html?scene=wheel', 1920, 1080, 0.6], ['turning.html?scene=butterfly', 1920, 1080, 0.7], ['bell.html', 1920, 1080, 0.6]];
(async () => {
    const b = await chromium.launch();
    for (let k = 0; k < FILMS.length; k++) {
        const [file, W, H, at] = FILMS[k];
        const pg = await (await b.newContext({ viewport: { width: W, height: H } })).newPage();
        await pg.goto('http://localhost:8765/simulations/fig13/' + file + (file.includes('?') ? '&' : '?') + 'film=1&theme=dark&dpr=1');
        await pg.waitForFunction(() => window.__ready && window.FILM, null, { timeout: 120000 });
        const n = await pg.evaluate(() => window.FILM.frames());
        await pg.evaluate(f => window.renderFrame(f), Math.floor(n * at)); await pg.waitForTimeout(300);
        await pg.screenshot({ path: OUT + (k + 1) + '.png' });
        console.log(k + 1, file, n, 'frames', (n / 30).toFixed(0) + ' s');
        await pg.close();
    }
    await b.close();
})();
