/* Moving between pages. Cross-document View Transitions (styles/i18n.css) photograph the old page once and move the two pictures
   on the graphics card; no script runs per frame. A change of language turns the page over: half a turn about the vertical axis
   maps x to -x, the same mirror that takes an English page to its Arabic one (type "lang"). Every other link lets the old page
   settle back and fade while the new one rises into place (type "page"; Numa, 3 November 2026). The arriving page then skips its
   own entrance animation (class "vt-arrive" on <html>), so the reader sees one motion, not two. Browsers without view
   transitions, and readers who ask for reduced motion, simply load the page.
   Loaded in <head>, before the first paint, so the arriving page can join the motion. */
(function () {
    'use strict';
    function lang(u) { var m = /\/(de|ar)\//.exec(new URL(u, location.href).pathname); return m ? m[1] : 'en'; }
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
        var root = document.documentElement;
        root.classList.add('vt-arrive');
        e.viewTransition.finished.then(function () { root.classList.remove('vt-arrive'); }, function () { root.classList.remove('vt-arrive'); });
    });
})();
