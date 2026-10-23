/* A language switch turns the page over: half a turn about the vertical axis maps x to -x, the same mirror that takes an English
   page to its Arabic one. Cross-document View Transitions (styles/i18n.css) photograph the old page once and turn the two
   pictures on the graphics card; no script runs per frame. Only a change of language turns; every other link keeps the
   browser's normal switch. Browsers without view transitions, and readers who ask for reduced motion, simply load the page.
   Loaded in <head>, before the first paint, so the arriving page can join the turn. */
(function () {
    'use strict';
    function lang(u) { var m = /\/(de|ar)\//.exec(new URL(u, location.href).pathname); return m ? m[1] : 'en'; }
    window.addEventListener('pageswap', function (e) {
        if (!e.viewTransition) return;
        var to = e.activation && e.activation.entry && e.activation.entry.url;
        if (!to || lang(to) === lang(location.href)) e.viewTransition.skipTransition();
    });
    window.addEventListener('pagereveal', function (e) {
        if (!e.viewTransition) return;
        var from = window.navigation && navigation.activation && navigation.activation.from;
        if (!from || !from.url || lang(from.url) === lang(location.href)) e.viewTransition.skipTransition();
    });
})();
