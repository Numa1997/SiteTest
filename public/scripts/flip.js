/* Moving between pages. Cross-document View Transitions (styles/i18n.css) photograph the old page once and move the two pictures
   on the graphics card; no script runs per frame. A change of language turns the page over: half a turn about the vertical axis
   maps x to -x, the same mirror that takes an English page to its Arabic one (type "lang"). Every other link lets the old page
   settle back and fade while the new one rises into place (type "page"; Numa, 3 November 2026). The arriving page then skips its
   own entrance animation for good (class "vt-arrive" on <html>; "vt-arriving" lasts only for the motion and holds the home
   page's scroll reveals), so the reader sees one motion, not two. Browsers without view
   transitions, and readers who ask for reduced motion, simply load the page.
   Loaded in <head>, before the first paint, so the arriving page can join the motion. */
(function () {
    'use strict';
    function lang(u) { var m = /\/(de|ar)\//.exec(new URL(u, location.href).pathname); return m ? m[1] : 'en'; }
    /* Fonts ready for the first frame (Numa, 3 November 2026). A page asks for its fonts only once its stylesheets have come back
       (a round trip to Cloudflare each), so the first frame, the one the motion shows, is drawn in the fallback face and the text
       moves when the real one arrives. The font files are kept for a year (_headers), so after the first page each is in the
       browser's cache: this page asks for the fonts the earlier pages of this language used, at once, and from the cache they
       are there in milliseconds. A first visit has no list yet and asks for nothing extra, so it loses no bandwidth. */
    var FKEY = 'fonts:' + lang(location.href);
    try {
        (JSON.parse(localStorage.getItem(FKEY) || '[]')).forEach(function (u) {
            var l = document.createElement('link');
            l.rel = 'preload'; l.as = 'font'; l.type = 'font/woff2'; l.crossOrigin = 'anonymous'; l.href = u;
            document.head.appendChild(l);
        });
    } catch (e) { /* storage blocked: the page loads as before */ }
    window.addEventListener('pagehide', function () {
        try {
            var seen = JSON.parse(localStorage.getItem(FKEY) || '[]');
            performance.getEntriesByType('resource').forEach(function (r) {
                if (/\.woff2(\?|$)/.test(r.name) && r.name.indexOf(location.origin + '/') === 0 && seen.indexOf(r.name) < 0) seen.push(r.name);
            });
            localStorage.setItem(FKEY, JSON.stringify(seen.slice(-24)));
        } catch (e) { /* storage blocked */ }
    });
    function name(vt, other) {
        if (vt.types) vt.types.add(other && lang(other) !== lang(location.href) ? 'lang' : 'page');
    }
    window.addEventListener('pageswap', function (e) {
        if (!e.viewTransition) return;
        name(e.viewTransition, e.activation && e.activation.entry && e.activation.entry.url);
    });
    window.addEventListener('pagereveal', function (e) {
        if (!e.viewTransition) return;
        var from = window.navigation && navigation.activation && navigation.activation.from;
        name(e.viewTransition, from && from.url);
        var root = document.documentElement, done = function () { root.classList.remove('vt-arriving'); };
        root.classList.add('vt-arrive', 'vt-arriving');   /* vt-arrive stays: taking it off would start the entrance animations over */
        e.viewTransition.finished.then(done, done);
    });
})();
