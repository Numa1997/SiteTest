/* Numa Koudsie · light / dark theme
   Applies the stored choice, or the system setting when none is stored, sets data-theme on <html>,
   keeps <meta name="theme-color"> in step, mounts toggle buttons and fires a "themechange" event. */
(function () {
    'use strict';
    if (window.Theme) return;
    var root = document.documentElement, KEY = 'theme';
    var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
    var buttons = [];

    function stored() { try { var t = localStorage.getItem(KEY); return t === 'dark' || t === 'light' ? t : null; } catch (e) { return null; } }
    function system() { return mq && mq.matches ? 'dark' : 'light'; }
    function current() { return root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light'; }

    function sync() {
        var dark = current() === 'dark';
        buttons.forEach(function (b) {
            b.setAttribute('aria-pressed', dark ? 'true' : 'false');
            b.title = dark ? 'Switch to the light theme' : 'Switch to the dark theme';
        });
    }
    function apply(t, save) {
        root.setAttribute('data-theme', t);
        if (save) { try { localStorage.setItem(KEY, t); } catch (e) { /* private mode: choice lasts for this page */ } }
        var meta = document.querySelector('meta[name="theme-color"]');
        if (meta) meta.setAttribute('content', t === 'dark' ? '#16110f' : '#f5f1ea');
        sync();
        var ev;
        try { ev = new CustomEvent('themechange', { detail: { theme: t } }); }
        catch (e) { ev = document.createEvent('CustomEvent'); ev.initCustomEvent('themechange', false, false, { theme: t }); }
        document.dispatchEvent(ev);
    }

    apply(stored() || system(), false);
    if (mq) {
        var follow = function () { if (!stored()) apply(system(), false); };
        if (mq.addEventListener) mq.addEventListener('change', follow); else if (mq.addListener) mq.addListener(follow);
    }

    var ICON = '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true" focusable="false">' +
        '<circle cx="8" cy="8" r="6.25" fill="none" stroke="currentColor" stroke-width="1.5"/>' +
        '<path d="M8 1.75a6.25 6.25 0 0 1 0 12.5z" fill="currentColor"/></svg>';
    function make() {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'theme-toggle';
        b.innerHTML = ICON + '<span>Dark</span>';
        b.addEventListener('click', function () { apply(current() === 'dark' ? 'light' : 'dark', true); });
        buttons.push(b);
        return b;
    }
    function mount() {
        Array.prototype.forEach.call(document.querySelectorAll('[data-theme-toggle]'), function (slot) {
            if (!slot.querySelector('.theme-toggle')) slot.appendChild(make());
        });
        var nav = document.querySelector('.sim-top .sim-nav');
        if (nav && !nav.querySelector('.theme-toggle')) nav.appendChild(make());
        sync();
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();

    window.Theme = { get: current, set: function (t) { apply(t === 'dark' ? 'dark' : 'light', true); } };
})();
