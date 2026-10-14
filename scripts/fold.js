/* Fold-out sections for every page of the site: the mechanism of Physik Radar (the Stelle app) and the two
   project apps, without their colour coding.

   Level 1 is a section card: a header band (number, title, one line of counts, round toggle) and a body that
   unfolds beneath it; while open, the header pins to the top of the window. Level 2 is a part inside a section:
   a smaller band that pins just under its section's header. Cards (the simulations list) keep their details
   behind More / Less. Everything starts open; what a reader closes is remembered in this browser, per page.
   Expand all / Collapse all act at once, without animation. A link to anything inside a closed fold opens
   the fold first, then scrolls to the target below the pinned headers. Folding happens in place, so the
   height really animates, and the scroll is managed so that nothing on screen jumps: a section that opens
   low is brought into view; a section closed from deep inside keeps its pinned header where it is.
   Without JavaScript the pages read as before, everything open. */
(function () {
    'use strict';

    var doc = document, root = doc.documentElement;
    var motion = function () { return !window.matchMedia('(prefers-reduced-motion: reduce)').matches; };

    /* one curve and two durations for everything that moves: the fold (CSS), the chevron (CSS), the scroll glide (JS) */
    var FOLD = { open: 320, close: 240, curve: [0.4, 0, 0.2, 1] };
    root.style.setProperty('--fold-open', FOLD.open + 'ms');
    root.style.setProperty('--fold-close', FOLD.close + 'ms');
    root.style.setProperty('--fold-ease', 'cubic-bezier(' + FOLD.curve.join(',') + ')');
    function bezier(c) {
        var cx = 3 * c[0], bx = 3 * (c[2] - c[0]) - cx, ax = 1 - cx - bx;
        var cy = 3 * c[1], by = 3 * (c[3] - c[1]) - cy, ay = 1 - cy - by;
        function sx(t) { return ((ax * t + bx) * t + cx) * t; }
        function sy(t) { return ((ay * t + by) * t + cy) * t; }
        function dx(t) { return (3 * ax * t + 2 * bx) * t + cx; }
        return function (x) {
            var t = x;
            for (var i = 0; i < 6; i++) { var e = sx(t) - x; if (Math.abs(e) < 1e-5) break; var d = dx(t); if (Math.abs(d) < 1e-6) break; t -= e / d; }
            return sy(Math.min(1, Math.max(0, t)));
        };
    }
    var ease = bezier(FOLD.curve);
    /* a close that also has to drop the page gets a little longer, in step with the distance */
    function closeMs(dist) { return dist > 0 ? Math.round(Math.min(420, Math.max(FOLD.close, dist * 0.45))) : FOLD.close; }

    /* moves the window on the fold's own curve and clock, so scroll and height stay in step; a wheel or touch cancels it */
    var glideId = 0;
    function glide(to, ms) {
        var id = ++glideId, from = window.scrollY;
        if (Math.abs(to - from) < 1) return;
        function stop() { if (id === glideId) glideId++; }
        window.addEventListener('wheel', stop, { once: true, passive: true });
        window.addEventListener('touchmove', stop, { once: true, passive: true });
        var dur = motion() ? ms : 0, t0 = null, frames = 0;
        (function step(now) {
            if (id !== glideId) return;
            frames++;
            if (!dur) { if (frames < 3) { requestAnimationFrame(step); return; } window.scrollTo({ top: to, behavior: 'instant' }); return; }
            if (t0 === null) t0 = now;
            var p = ease(Math.min(1, (now - t0) / dur));
            window.scrollTo({ top: from + (to - from) * p, behavior: 'instant' });
            if (p < 1) requestAnimationFrame(step);
        })(performance.now());
    }

    /* which folds this reader closed, per page */
    var KEY = 'fold:' + location.pathname.replace(/\/index\.html$/, '/');
    var closed = {};
    try { (JSON.parse(localStorage.getItem(KEY) || '[]') || []).forEach(function (id) { closed[id] = 1; }); } catch (e) { /* private mode */ }
    function remember(id, open) {
        if (!id) return;
        if (open) delete closed[id]; else closed[id] = 1;
        try { localStorage.setItem(KEY, JSON.stringify(Object.keys(closed))); } catch (e) { /* private mode */ }
    }

    function el(tag, cls, text) {
        var n = doc.createElement(tag);
        if (cls) n.className = cls;
        if (text != null) n.textContent = text;
        return n;
    }
    function chev(size) {
        var NS = 'http://www.w3.org/2000/svg', svg = doc.createElementNS(NS, 'svg'), path = doc.createElementNS(NS, 'path');
        svg.setAttribute('class', 'chev'); svg.setAttribute('viewBox', '0 0 14 14');
        svg.setAttribute('width', size); svg.setAttribute('height', size); svg.setAttribute('aria-hidden', 'true');
        path.setAttribute('d', 'M3 5l4 4 4-4'); path.setAttribute('fill', 'none'); path.setAttribute('stroke', 'currentColor');
        path.setAttribute('stroke-width', '1.8'); path.setAttribute('stroke-linecap', 'round'); path.setAttribute('stroke-linejoin', 'round');
        svg.appendChild(path);
        return svg;
    }

    var foldOf = function (node) { return node && node.querySelector(':scope > .fold'); };
    var isOpen = function (node) { return node && node.getAttribute('data-collapsed') === '0'; };
    var pageEnd = function () { return root.scrollHeight - window.innerHeight; };
    var headOf = function (node) { return node && node.querySelector(':scope > .fs-head'); };
    var top0 = function () { return parseFloat(getComputedStyle(root).getPropertyValue('--fold-top')) || 0; };

    /* where a fold's header pins: a section's at the top of the window (below any page bar), a part's under its section's header */
    function pinLine(node) {
        var outer = node && node.parentElement && node.parentElement.closest('[data-fold-level]');
        if (!outer) return top0();
        return pinLine(outer) + (headOf(outer) ? headOf(outer).offsetHeight : 0);
    }

    /** Sets a fold open or closed, without animation logic: attributes, inert body, toggle label. */
    function setFold(node, open) {
        if (!node) return;
        node.setAttribute('data-collapsed', open ? '0' : '1');
        var fold = foldOf(node);
        if (fold) { fold.setAttribute('data-open', open ? '1' : '0'); if (open) fold.removeAttribute('inert'); else fold.setAttribute('inert', ''); }
        var btn = node.querySelector(':scope > .fs-head .fs-toggle');
        if (btn) {
            btn.setAttribute('aria-expanded', String(open));
            btn.setAttribute('aria-label', (open ? 'Collapse ' : 'Expand ') + btn.getAttribute('data-label'));
        }
    }

    /* brings a fold into view when its header sits low (or above its pin line), aiming where the page will end once open */
    function reveal(node) {
        var line = pinLine(node), top = node.getBoundingClientRect().top;
        if (top >= line && top <= Math.max(line + 48, window.innerHeight * 0.4)) return;
        var fold = foldOf(node), inner = fold && fold.firstElementChild && fold.firstElementChild.firstElementChild;
        var growth = inner ? inner.offsetHeight - fold.getBoundingClientRect().height : 0;
        glide(Math.max(0, Math.min(window.scrollY + top - line - 12, pageEnd() + growth)), FOLD.open);
    }

    /* opens or closes one fold in place, managing the scroll so that nothing on screen jumps */
    function fold(node, open, bring) {
        if (!node) return;
        if (isOpen(node) !== open) {
            if (!open) {
                /* closing from deep inside: put the fold's top where its pinned header already is, so only the body folds away */
                var line = pinLine(node), top = node.getBoundingClientRect().top;
                if (top < line) window.scrollTo({ top: window.scrollY + top - line, behavior: 'instant' });
                var f = foldOf(node), end = pageEnd() - (f ? f.getBoundingClientRect().height : 0);
                var ms = closeMs(window.scrollY - end);
                node.style.setProperty('--fold-close', ms + 'ms');
                if (window.scrollY > end) glide(Math.max(0, end), ms);
            }
            setFold(node, open);
        }
        if (open && bring) reveal(node);
    }

    function toggle(node) {
        var open = !isOpen(node);
        remember(node.id, open);
        fold(node, open, true);
    }

    /* all at once, without animation: many heights moving together is noise, not information */
    function all(open) {
        var nodes = doc.querySelectorAll('[data-fold-level]'), cards = doc.querySelectorAll('[data-card]');
        if (!nodes.length && !cards.length) return;
        if (!open && nodes.length) {
            var first = nodes[0].getBoundingClientRect().top + window.scrollY - top0() - 12;
            if (window.scrollY > first) window.scrollTo({ top: first, behavior: 'instant' });
        }
        root.classList.add('fold-no-anim');
        Array.prototype.forEach.call(nodes, function (n) { setFold(n, open); remember(n.id, open); });
        Array.prototype.forEach.call(cards, function (c) { setCard(c, open); });
        if (Fold.onAll) Fold.onAll(open);
        void root.offsetWidth;
        requestAnimationFrame(function () { root.classList.remove('fold-no-anim'); });
    }

    /**
     * Turns `node` into a fold. `head` are the nodes that go into the header band (moved, not copied), `counts` one
     * line of text under the title, `level` 1 or 2. Everything else that `node` holds becomes the body.
     */
    function make(node, opt) {
        if (!node || node.hasAttribute('data-fold-level')) return node;
        var level = opt.level || 1, id = node.id || opt.id;
        if (!node.id && id) node.id = id;
        var open = !closed[id];
        var head = el('div', 'fs-head'), main = el('div', 'fs-main'), side = el('div', 'fs-side');
        (opt.head || []).forEach(function (h) { if (h) main.appendChild(h); });
        if (opt.counts) { var c = el('p', 'fs-counts'); c.textContent = opt.counts; main.appendChild(c); }
        var bodyId = (id || 'fold') + '-body';
        var btn = el('button', 'fs-toggle');
        btn.type = 'button';
        btn.setAttribute('aria-controls', bodyId);
        btn.setAttribute('data-label', opt.label || (main.textContent || '').trim().slice(0, 80));
        btn.appendChild(chev(level === 1 ? 14 : 12));
        side.appendChild(btn);
        head.appendChild(main); head.appendChild(side);
        var fold = el('div', 'fold'), inner = el('div', 'fold-i'), body = el('div', 'fs-body');
        fold.id = bodyId;
        while (node.firstChild) body.appendChild(node.firstChild);
        inner.appendChild(body); fold.appendChild(inner);
        node.appendChild(head); node.appendChild(fold);
        node.classList.add(level === 1 ? 'fsec' : 'fsub');
        node.setAttribute('data-fold-level', String(level));
        setFold(node, open);
        head.addEventListener('click', function (e) {
            if (e.target.closest('a, input, label, select, textarea, button:not(.fs-toggle)')) return;
            if (e.target.closest('.fs-toggle')) return;
            toggle(node);
        });
        btn.addEventListener('click', function (e) { e.stopPropagation(); toggle(node); });
        if (level === 1 && window.ResizeObserver) headObserver.observe(head);
        return node;
    }
    /* parts pin under their section's header, whose height varies: each section carries it as --head-h */
    var headObserver = window.ResizeObserver ? new ResizeObserver(function (entries) {
        entries.forEach(function (e) { if (e.target.parentElement) e.target.parentElement.style.setProperty('--head-h', e.target.offsetHeight + 'px'); });
    }) : null;

    /* cards: details behind More / Less (not remembered; the list redraws on every search) */
    function setCard(card, open) {
        card.setAttribute('data-collapsed', open ? '0' : '1');
        var f = card.querySelector('.fold'), b = card.querySelector('.fs-more');
        if (f) { f.setAttribute('data-open', open ? '1' : '0'); if (open) f.removeAttribute('inert'); else f.setAttribute('inert', ''); }
        if (b) {
            b.setAttribute('aria-expanded', String(open));
            b.firstChild.textContent = open ? 'Less' : 'More';
            b.setAttribute('aria-label', open ? 'Hide details' : 'Show details');
        }
    }
    doc.addEventListener('click', function (e) {
        var b = e.target.closest('.fs-more');
        if (!b) return;
        var card = b.closest('[data-card]');
        if (card) { setCard(card, card.getAttribute('data-collapsed') !== '0'); if (Fold.onCard) Fold.onCard(card); }
    });

    /* the page's Expand all / Collapse all */
    function tools(host, where) {
        if (!host || doc.querySelector('.fold-tools')) return;
        var t = el('div', 'fold-tools');
        t.setAttribute('role', 'group');
        t.setAttribute('aria-label', 'Open or close all sections');
        var a = el('button', 'fold-tool', 'Expand all'), b = el('button', 'fold-tool', 'Collapse all');
        a.type = b.type = 'button';
        a.addEventListener('click', function () { all(true); });
        b.addEventListener('click', function () { all(false); });
        t.appendChild(a); t.appendChild(b);
        if (where === 'append') host.appendChild(t);
        else if (where === 'after') host.parentNode.insertBefore(t, host.nextSibling);
        else host.parentNode.insertBefore(t, host);
    }

    /* opens every fold around `target` (at once), then scrolls it into view below the pinned headers */
    function openTo(target, smooth) {
        if (!target) return;
        var chain = [], n = target.closest('[data-fold-level]');
        if (n === target) n = n.parentElement && n.parentElement.closest('[data-fold-level]');
        while (n) { chain.unshift(n); n = n.parentElement && n.parentElement.closest('[data-fold-level]'); }
        var cardFold = target.closest('[data-card]');
        root.classList.add('fold-no-anim');
        chain.forEach(function (c) { if (!isOpen(c)) { setFold(c, true); remember(c.id, true); } });
        if (target.hasAttribute('data-fold-level') && !isOpen(target)) { setFold(target, true); remember(target.id, true); }
        if (cardFold && target !== cardFold) setCard(cardFold, true);
        void root.offsetWidth;
        requestAnimationFrame(function () { root.classList.remove('fold-no-anim'); });
        var offset = top0();
        chain.forEach(function (c) { var h = headOf(c); if (h) offset += h.offsetHeight; });
        var y = target.getBoundingClientRect().top + window.scrollY - offset - 12;
        if (smooth && motion()) glide(Math.max(0, y), FOLD.open); else window.scrollTo({ top: Math.max(0, y), behavior: 'instant' });
    }
    function targetOf(hash) {
        if (!hash || hash.length < 2) return null;
        try { return doc.getElementById(decodeURIComponent(hash.slice(1))); } catch (e) { return null; }
    }
    doc.addEventListener('click', function (e) {
        if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        var a = e.target.closest('a[href^="#"]');
        if (!a) return;
        var t = targetOf(a.getAttribute('href'));
        if (!t || !(t.closest('[data-fold-level]') || t.closest('[data-card]'))) return;
        e.preventDefault();
        if (history.pushState) history.pushState(null, '', a.getAttribute('href'));
        openTo(t, true);
    });
    window.addEventListener('hashchange', function () { openTo(targetOf(location.hash), false); });

    /* printing shows everything */
    var printOpen = null;
    window.addEventListener('beforeprint', function () {
        printOpen = [];
        Array.prototype.forEach.call(doc.querySelectorAll('[data-fold-level], [data-card]'), function (n) {
            printOpen.push([n, n.getAttribute('data-collapsed') === '0']);
            if (n.hasAttribute('data-card')) setCard(n, true); else setFold(n, true);
        });
    });
    window.addEventListener('afterprint', function () {
        (printOpen || []).forEach(function (p) { if (p[0].hasAttribute('data-card')) setCard(p[0], p[1]); else setFold(p[0], p[1]); });
        printOpen = null;
    });

    /* a page bar that sticks to the top of the window across its whole width (the home page index on phones) */
    function measureTop() {
        var h = 0;
        Array.prototype.forEach.call(doc.querySelectorAll('[data-fold-bar]'), function (b) {
            var cs = getComputedStyle(b);
            if ((cs.position === 'sticky' || cs.position === 'fixed') && parseFloat(cs.top) <= 1 && b.offsetWidth > window.innerWidth * 0.6) h = Math.max(h, b.offsetHeight);
        });
        root.style.setProperty('--fold-top', h + 'px');
    }
    window.addEventListener('resize', measureTop, { passive: true });

    var plural = function (n, one, many) { return n + ' ' + (n === 1 ? one : many); };
    var count = function (scope, sel) { return scope.querySelectorAll(sel).length; };
    var join = function (parts) { return parts.filter(Boolean).join(' · '); };

    /* ---------- the site's structures ---------- */

    /* lecture notes: every section is a fold, every numbered part inside it a fold one level down */
    function papers() {
        Array.prototype.forEach.call(doc.querySelectorAll('.paper .psec'), function (sec) {
            var h3 = sec.querySelector(':scope > h3');
            if (!h3) return;
            var html = sec.innerHTML;
            var eqs = (html.match(/\\\[/g) || []).length + count(sec, '.katex-display');
            var parts = count(sec, ':scope > h4');
            var counts = join([parts && plural(parts, 'part', 'parts'), eqs && plural(eqs, 'equation', 'equations'),
                count(sec, '.pfig') && plural(count(sec, '.pfig'), 'figure', 'figures'), count(sec, '.pbox') && plural(count(sec, '.pbox'), 'box', 'boxes')]);
            /* group each h4 with what follows it, up to the next h4 */
            var h4s = sec.querySelectorAll(':scope > h4');
            Array.prototype.forEach.call(h4s, function (h4, i) {
                var part = el('section', 'ppart');
                var n = h4.querySelector('.psub__n');
                part.id = h4.id || sec.id + '-' + (n ? n.textContent.trim().replace(/\W+/g, '-') : i + 1);
                if (h4.id === part.id) h4.removeAttribute('id');
                sec.insertBefore(part, h4);
                var next = h4.nextSibling;
                part.appendChild(h4);
                while (next && !(next.nodeType === 1 && next.tagName === 'H4')) { var after = next.nextSibling; part.appendChild(next); next = after; }
                make(part, { level: 2, head: [h4], label: h4.textContent.trim() });
            });
            make(sec, { level: 1, head: [h3], counts: counts, label: h3.textContent.replace('★', '').trim() });
        });
        var head = doc.querySelector('.paper__head');
        if (head && doc.querySelector('.psec')) tools(head, 'append');
    }

    /* "From symbols to code": called by sim.js once the walkthrough has drawn itself */
    function walk(host) {
        if (!host || host.hasAttribute('data-fold-level')) return;
        var h2 = host.querySelector('.walk__head h2');
        var steps = count(host, '.walk__steps > li');
        make(host, { level: 1, head: [h2], counts: join([steps && plural(steps, 'step', 'steps'), 'each formula beside the code that computes it and its value now']), label: 'From symbols to code' });
        var t = doc.querySelector('.fold-tools');
        if (!t) { var p = doc.querySelector('.paper__head'); tools(p || host, p ? 'append' : 'before'); }
        if (location.hash) openTo(targetOf(location.hash), false);
    }

    /* the home page: Positions, Education, Research, Simulations, Skills */
    function home() {
        var secs = doc.querySelectorAll('main .section[id]');
        if (!secs.length || !doc.querySelector('.layout')) return;
        var units = {
            positions: function (s) { return plural(count(s, 'article.entry'), 'role', 'roles'); },
            education: function (s) { return plural(count(s, 'h3'), 'qualification', 'qualifications'); },
            research: function (s) { return plural(count(s, 'article'), 'project', 'projects'); },
            simulations: function (s) { return plural(count(s, 'article'), 'figure', 'figures'); },
            skills: function (s) { return plural(count(s, 'dt'), 'area', 'areas'); }
        };
        Array.prototype.forEach.call(secs, function (sec, i) {
            var h2 = sec.querySelector(':scope > h2');
            if (!h2) return;
            var num = el('span', 'fs-num', String(i + 1).padStart(2, '0'));
            h2.insertBefore(num, h2.firstChild);
            var c = units[sec.id] ? units[sec.id](sec) : '';
            make(sec, { level: 1, head: [h2], counts: /^0 /.test(c) ? '' : c, label: h2.textContent.replace(/^\d+/, '').trim() });
        });
        tools(secs[0], 'before');
    }

    /* the Portfolios page: every project, and every numbered part inside it */
    function portfolios() {
        Array.prototype.forEach.call(doc.querySelectorAll('article.proj'), function (proj) {
            var band = proj.querySelector(':scope > .proj__band'), h2 = proj.querySelector('.proj__head h2');
            if (!band || !h2) return;
            Array.prototype.forEach.call(proj.querySelectorAll('.proj__part'), function (part, i) {
                var h3 = part.querySelector(':scope > h3');
                if (!h3) return;
                if (!part.id) part.id = proj.id + '-part-' + (i + 1);
                make(part, { level: 2, head: [h3], label: h3.textContent.trim() });
            });
            var num = band.querySelector('.proj__num'), bits = Array.prototype.map.call(band.querySelectorAll(':scope > p, :scope > span:last-child'), function (x) { return x.textContent.trim(); });
            var title = el('h2', 'fs-title');
            title.id = h2.id;
            if (num) title.appendChild(el('span', 'fs-num', num.textContent.trim()));
            title.appendChild(doc.createTextNode(h2.textContent.trim()));
            h2.remove();
            band.remove();
            make(proj, { level: 1, head: [title], counts: join(bits), label: title.textContent.replace(/^\d+/, '').trim() });
        });
        var first = doc.querySelector('article.proj');
        if (first) tools(first, 'before');
    }

    /* a reader who arrives with #target is taken there; when the mathematics is typeset the page grows, so go again
       unless the reader has started scrolling */
    var moved = false;
    ['wheel', 'touchmove', 'keydown'].forEach(function (ev) { window.addEventListener(ev, function () { moved = true; }, { once: true, passive: true }); });
    doc.addEventListener('typeset', function () { if (location.hash && !moved) openTo(targetOf(location.hash), false); });

    function boot() {
        measureTop();
        home();
        portfolios();
        papers();
        if (location.hash) openTo(targetOf(location.hash), false);
    }
    if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', boot); else boot();

    var Fold = window.Fold = { make: make, walk: walk, all: all, openTo: openTo, setCard: setCard, onCard: null, onAll: null, tools: tools };
})();
