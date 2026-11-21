/* =====================================================================
   Smartline Point Cleaning Hub Ltd — v2 behaviour + motion engine.
   Vanilla, no framework, one requestAnimationFrame loop for everything
   that reads the scroll position. Every module is progressive: with
   reduced motion or no JS the page is complete and still.
   ===================================================================== */
(function () {
  "use strict";
  var d = document, h = d.documentElement, w = window;
  w.__slMotion = true;
  var reduce = h.classList.contains("reduce-motion");
  var fine = w.matchMedia && w.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var wide = w.matchMedia("(min-width: 1041px)");
  function $(s, c) { return (c || d).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }
  function on(el, ev, fn, o) { if (el) el.addEventListener(ev, fn, o || false); }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function pad(n) { return (n < 10 ? "0" : "") + n; }

  /* ------------------------------------------------------------- the scroll loop */
  var subs = [], layouts = [], sy = w.scrollY || 0, lastY = sy, vel = 0, vh = w.innerHeight, ticking = false;
  function frame() {
    ticking = false;
    sy = w.scrollY || w.pageYOffset; vel = sy - lastY; lastY = sy;
    for (var i = 0; i < subs.length; i++) subs[i](sy, vel);
  }
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  on(w, "scroll", req, { passive: true });
  var rt;
  on(w, "resize", function () {
    clearTimeout(rt);
    rt = setTimeout(function () { vh = w.innerHeight; layouts.forEach(function (f) { f(); }); req(); }, 120);
  });

  /* ------------------------------------------------------------- loader → hero entrance */
  var loader = $(".loader");
  function startHero() {
    var hero = $(".hero");
    if (hero) requestAnimationFrame(function () { hero.classList.add("is-in"); });
  }
  function loaderVisible() {
    return loader && !h.classList.contains("loaded-before") && !reduce && getComputedStyle(loader).display !== "none";
  }
  if (loaderVisible()) {
    var t0 = performance.now(), done = false;
    var finish = function () {
      if (done) return; done = true;
      setTimeout(function () {
        loader.classList.add("is-done");
        setTimeout(startHero, 280);
        setTimeout(function () { if (loader.parentNode) loader.parentNode.removeChild(loader); }, 950);
      }, Math.max(0, 1650 - (performance.now() - t0)));
    };
    if (d.readyState === "complete") finish(); else on(w, "load", finish);
    setTimeout(finish, 2800);
  } else {
    if (loader && loader.parentNode) loader.parentNode.removeChild(loader);
    startHero();
  }

  /* ------------------------------------------------------------- header: solid, hide on the way down, progress */
  var hdr = $(".hdr"), prog = $(".hdr__progress"), docH = 1, menuOpen = false;
  function measure() { docH = Math.max(1, d.documentElement.scrollHeight - vh); }
  layouts.push(measure); measure();
  on(w, "load", function () { measure(); req(); });
  subs.push(function (y, v) {
    if (!hdr) return;
    var solid = y > 40;
    hdr.classList.toggle("is-scrolled", solid);
    if (y < 500 || v < -3 || menuOpen) hdr.classList.remove("is-hidden");
    else if (v > 3) hdr.classList.add("is-hidden");
    d.body.classList.toggle("hdr-shown", solid && !hdr.classList.contains("is-hidden"));
    if (prog) prog.style.setProperty("--p", clamp(y / docH, 0, 1).toFixed(4));
  });

  /* ------------------------------------------------------------- split headings into masked words */
  function split(el) {
    var walker = d.createTreeWalker(el, NodeFilter.SHOW_TEXT), nodes = [], i = 0;
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function (n) {
      var frag = d.createDocumentFragment();
      n.nodeValue.split(/(\s+)/).forEach(function (p) {
        if (!p) return;
        if (/^\s+$/.test(p)) { frag.appendChild(d.createTextNode(p)); return; }
        var o = d.createElement("span"), inner = d.createElement("span");
        o.className = "sw-w"; inner.className = "sw-i"; inner.textContent = p;
        inner.style.setProperty("--d", (Math.min(i++, 14) * 0.055).toFixed(3) + "s");
        o.appendChild(inner); frag.appendChild(o);
      });
      n.parentNode.replaceChild(frag, n);
    });
    el.classList.add("is-split");
  }
  if (!reduce) $$("[data-split]").forEach(split);

  /* ------------------------------------------------------------- reveals */
  $$("[data-stagger]").forEach(function (group) {
    $$("[data-reveal]", group).forEach(function (el, i) { el.style.transitionDelay = (Math.min(i, 8) * 80) + "ms"; });
  });
  var revealables = $$("[data-reveal], [data-split], .tl");
  if ("IntersectionObserver" in w && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -9% 0px", threshold: 0.06 });
    revealables.forEach(function (el) { io.observe(el); });
  } else {
    revealables.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ------------------------------------------------------------- the statement lights up word by word */
  if (!reduce) {
    $$("[data-scrub]").forEach(function (el) {
      var words = [];
      var parts = el.textContent.split(/(\s+)/);
      el.textContent = "";
      parts.forEach(function (p) {
        if (/^\s+$/.test(p) || !p) { el.appendChild(d.createTextNode(p)); return; }
        var s = d.createElement("span"); s.className = "sw"; s.textContent = p; el.appendChild(s); words.push(s);
      });
      var lit = -1;
      subs.push(function () {
        var r = el.getBoundingClientRect();
        if (r.bottom < -vh || r.top > vh * 1.5) return;
        var p = clamp((vh * 0.82 - r.top) / (r.height + vh * 0.3), 0, 1);
        var n = Math.round(p * words.length * 1.12);
        if (n === lit) return;
        lit = n;
        for (var i = 0; i < words.length; i++) words[i].classList.toggle("is-lit", i < n);
      });
    });
  }

  /* ------------------------------------------------------------- parallax: hero, framed photos, band backgrounds */
  if (!reduce) {
    var heroImg = $(".hero__img"), heroCopy = $(".hero__copy");
    if (heroImg) subs.push(function (y) {
      if (y > vh * 1.2) return;
      heroImg.style.translate = "0 " + (y * 0.28).toFixed(1) + "px";
      if (heroCopy) { heroCopy.style.translate = "0 " + (y * 0.12).toFixed(1) + "px"; heroCopy.style.opacity = clamp(1 - y / (vh * 0.85), 0, 1).toFixed(3); }
    });
    var px = $$("[data-parallax-box] img, .cta__bg img, .phero__bg img");
    if (px.length) subs.push(function () {
      for (var i = 0; i < px.length; i++) {
        var box = px[i].parentNode.getBoundingClientRect();
        if (box.bottom < 0 || box.top > vh) continue;
        var k = px[i].closest("[data-parallax-box]") ? -0.07 : -0.12;
        px[i].style.translate = "0 " + ((box.top + box.height / 2 - vh / 2) * k).toFixed(1) + "px";
      }
    });
  }

  /* ------------------------------------------------------------- services rail: vertical scroll drives it sideways */
  var rail = $(".rail"), track = rail ? $(".rail__track", rail) : null;
  if (rail && track) {
    var meter = $(".rail__bar", rail), count = $(".rail__count", rail), dist = 0, cards = $$(".rcard", track).length;
    var setRail = function () {
      var pin = !reduce && wide.matches;
      rail.classList.toggle("is-pinned", pin);
      if (!pin) { rail.style.height = ""; track.style.transform = ""; return; }
      dist = Math.max(0, track.scrollWidth - w.innerWidth);
      rail.style.height = (dist + vh) + "px";
      measure();
    };
    layouts.push(setRail); setRail();
    if (wide.addEventListener) wide.addEventListener("change", function () { setRail(); req(); });
    /* keyboard: a card tabbed to off to the side scrolls the page until the rail brings it into view */
    on(track, "focusin", function (e) {
      if (!rail.classList.contains("is-pinned")) return;
      var card = e.target.closest(".rcard");
      if (!card || !dist) return;
      var p = clamp((card.offsetLeft - 60) / dist, 0, 1);
      var top = rail.getBoundingClientRect().top + w.scrollY + p * dist;
      w.scrollTo({ top: top, behavior: "auto" });
    });
    subs.push(function () {
      if (!rail.classList.contains("is-pinned")) return;
      var p = clamp(-rail.getBoundingClientRect().top / Math.max(1, dist), 0, 1);
      track.style.transform = "translate3d(" + (-p * dist).toFixed(1) + "px,0,0)";
      if (meter) meter.style.setProperty("--p", (0.2 + p * 0.8).toFixed(3));
      if (count) count.textContent = pad(1 + Math.round(p * (cards - 1)));
    });
  }

  /* ------------------------------------------------------------- how we work: the active step follows the reader */
  var sxItems = $$("[data-sx-item]"), sxNow = $(".sx__now"), sxBar = $(".sx__bar");
  if (sxItems.length && "IntersectionObserver" in w && !reduce) {
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var idx = sxItems.indexOf(en.target);
        sxItems.forEach(function (it, i) { it.classList.toggle("is-active", i === idx); });
        if (sxNow) sxNow.textContent = pad(idx + 1);
        if (sxBar) sxBar.style.setProperty("--p", ((idx + 1) / sxItems.length).toFixed(3));
      });
    }, { rootMargin: "-46% 0px -46% 0px" });
    sxItems.forEach(function (it) { sio.observe(it); });
    sxItems[0].classList.add("is-active");
  }

  /* ------------------------------------------------------------- count-up */
  var counters = $$("[data-count]");
  function countUp(el) {
    var to = parseInt(el.getAttribute("data-count"), 10), suf = el.getAttribute("data-suffix") || "", t0 = null, dur = 1600;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 4);
      el.textContent = Math.round(to * e) + suf;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if (counters.length && "IntersectionObserver" in w && !reduce) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { setTimeout(function () { countUp(en.target); }, 600); cio.unobserve(en.target); } });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { cio.observe(c); });
  }

  /* ------------------------------------------------------------- marquees: drift, pushed by scroll speed */
  if (!reduce) {
    $$("[data-marquee]").forEach(function (m) {
      var trk = $(".marquee__track", m), grp = $(".marquee__group", m), base = parseFloat(m.getAttribute("data-marquee")) || 0.5;
      var x = 0, gw = grp.offsetWidth, visible = true, dir = base < 0 ? -1 : 1, last = performance.now();
      layouts.push(function () { gw = grp.offsetWidth; });
      if ("IntersectionObserver" in w) new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }).observe(m);
      (function loop(t) {
        var dt = Math.min(48, t - last); last = t;
        if (visible && gw) {
          if (vel > 1) dir = base < 0 ? -1 : 1; else if (vel < -1) dir = base < 0 ? 1 : -1;
          var boost = 1 + Math.min(Math.abs(vel) * 0.06, 5);
          x -= Math.abs(base) * dir * boost * dt * 0.06;
          if (x <= -gw) x += gw; if (x > 0) x -= gw;
          trk.style.transform = "translate3d(" + x.toFixed(2) + "px,0,0)";
          vel *= 0.9;
        }
        requestAnimationFrame(loop);
      })(last);
    });
  }

  /* ------------------------------------------------------------- pointer niceties: magnetic buttons, card glow */
  if (fine && !reduce) {
    $$("[data-magnetic]").forEach(function (b) {
      on(b, "pointermove", function (e) {
        var r = b.getBoundingClientRect();
        b.style.translate = ((e.clientX - r.left - r.width / 2) * 0.18).toFixed(1) + "px " + ((e.clientY - r.top - r.height / 2) * 0.28).toFixed(1) + "px";
      });
      on(b, "pointerleave", function () { b.style.translate = ""; });
    });
    $$("[data-glow]").forEach(function (c) {
      on(c, "pointermove", function (e) {
        var r = c.getBoundingClientRect();
        c.style.setProperty("--mx", (e.clientX - r.left) + "px");
        c.style.setProperty("--my", (e.clientY - r.top) + "px");
      });
    });
  }

  /* ------------------------------------------------------------- FAQ: animated height */
  $$(".faq__item").forEach(function (det) {
    var sum = $("summary", det), body = $(".faq__a", det), anim;
    if (!sum || !body || reduce || !body.animate) return;
    on(sum, "click", function (e) {
      e.preventDefault();
      if (anim) anim.cancel();
      if (det.open) {
        var hgt = body.offsetHeight;
        anim = body.animate({ height: [hgt + "px", "0px"], opacity: [1, 0] }, { duration: 340, easing: "cubic-bezier(.65,0,.35,1)" });
        anim.onfinish = function () { det.open = false; anim = null; };
      } else {
        det.open = true;
        var full = body.offsetHeight;
        anim = body.animate({ height: ["0px", full + "px"], opacity: [0, 1] }, { duration: 480, easing: "cubic-bezier(.16,1,.3,1)" });
        anim.onfinish = function () { anim = null; };
      }
    });
  });

  /* ------------------------------------------------------------- mega menu */
  $$(".nav__item--mega").forEach(function (item) {
    var btn = $(".nav__link", item), panel = $(".mega", item), timer, hoveredAt = 0;
    function open() { clearTimeout(timer); item.classList.add("is-open"); btn.setAttribute("aria-expanded", "true"); menuOpen = true; }
    function close(focus) {
      item.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); menuOpen = false;
      if (focus) btn.focus();
    }
    on(btn, "click", function (e) {
      e.preventDefault();
      if (item.classList.contains("is-open") && Date.now() - hoveredAt > 700) close(); else open();
    });
    on(item, "mouseenter", function () { if (fine) { hoveredAt = Date.now(); open(); } });
    on(item, "mouseleave", function () { timer = setTimeout(function () { close(); }, 200); });
    on(item, "keydown", function (e) {
      var links = $$("a", panel), i = links.indexOf(d.activeElement);
      if (e.key === "Escape") { close(true); }
      else if (e.key === "ArrowDown") { e.preventDefault(); open(); (links[i + 1] || links[0]).focus(); }
      else if (e.key === "ArrowUp" && i > -1) { e.preventDefault(); (links[i - 1] || btn).focus(); }
    });
    on(d, "click", function (e) { if (!item.contains(e.target)) close(); });
    on(item, "focusout", function (e) { if (!item.contains(e.relatedTarget)) close(); });
  });

  /* ------------------------------------------------------------- drawer */
  var drawer = $(".drawer"), burger = $(".hdr__burger"), lastFocus;
  function trap(e) {
    if (e.key === "Escape") return closeDrawer();
    if (e.key !== "Tab") return;
    var f = $$("a, button, summary", drawer).filter(function (x) { return x.offsetParent !== null; });
    if (!f.length) return;
    if (e.shiftKey && d.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
    else if (!e.shiftKey && d.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
  }
  function openDrawer() {
    lastFocus = d.activeElement;
    drawer.hidden = false;
    requestAnimationFrame(function () { requestAnimationFrame(function () { drawer.classList.add("is-open"); }); });
    d.body.classList.add("no-scroll");
    burger.setAttribute("aria-expanded", "true");
    menuOpen = true;
    on(d, "keydown", trap);
    setTimeout(function () { var c = $(".drawer__close", drawer); if (c) c.focus(); }, 60);
  }
  function closeDrawer() {
    drawer.classList.remove("is-open");
    d.body.classList.remove("no-scroll");
    burger.setAttribute("aria-expanded", "false");
    menuOpen = false;
    d.removeEventListener("keydown", trap);
    setTimeout(function () { drawer.hidden = true; }, 700);
    if (lastFocus) lastFocus.focus();
  }
  if (drawer && burger) {
    on(burger, "click", openDrawer);
    $$("[data-close-drawer]", drawer).forEach(function (b) { on(b, "click", closeDrawer); });
    $$(".drawer__nav > a, .drawer__acc a", drawer).forEach(function (a) { on(a, "click", closeDrawer); });
  }

  /* ------------------------------------------------------------- services sub-nav scroll-spy */
  var spyLinks = $$(".subnav a");
  if (spyLinks.length && "IntersectionObserver" in w) {
    var map = {};
    spyLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var clearSpy = function () { spyLinks.forEach(function (a) { a.classList.remove("is-active"); a.removeAttribute("aria-current"); }); };
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && map[en.target.id]) {
          clearSpy();
          map[en.target.id].classList.add("is-active");
          map[en.target.id].setAttribute("aria-current", "true");
        }
      });
    }, { rootMargin: "-35% 0px -60% 0px" });
    Object.keys(map).forEach(function (id) { var s = d.getElementById(id); if (s) spy.observe(s); });
    var firstGroup = d.getElementById(Object.keys(map)[0]);
    subs.push(function () { if (firstGroup && firstGroup.getBoundingClientRect().top > vh * 0.4) clearSpy(); });
  }

  /* ------------------------------------------------------------- clients filter */
  var filterBtns = $$("[data-filter]");
  function applyFilter(key) {
    filterBtns.forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-filter") === key)); });
    var shown = 0;
    $$(".client").forEach(function (c) {
      var hit = key === "all" || c.getAttribute("data-sector") === key;
      c.classList.toggle("is-hidden", !hit);
      if (hit) { shown++; if (!reduce && c.animate) c.animate({ opacity: [0, 1], transform: ["translateY(16px)", "none"] }, { duration: 500, easing: "cubic-bezier(.16,1,.3,1)", delay: shown * 40 }); }
    });
    var live = $("#filter-status");
    if (live) live.textContent = shown + (shown === 1 ? " client" : " clients") + " shown";
  }
  if (filterBtns.length) {
    filterBtns.forEach(function (b) { on(b, "click", function () { applyFilter(b.getAttribute("data-filter")); }); });
    var want = new URLSearchParams(w.location.search).get("sector");
    if (want && $('[data-filter="' + want.replace(/[^a-z-]/g, "") + '"]')) applyFilter(want);
  }

  /* ------------------------------------------------------------- gallery lightbox */
  var tiles = $$("a.tile");
  if (tiles.length && typeof HTMLDialogElement === "function") {
    var dlg = d.createElement("dialog");
    dlg.className = "lightbox";
    dlg.setAttribute("aria-label", "Image viewer");
    dlg.innerHTML = '<figure class="lightbox__fig"><img alt=""><figcaption class="lightbox__cap"></figcaption></figure>' +
      '<button class="lightbox__btn lightbox__close" type="button" aria-label="Close"><svg class="icon"><use href="/assets/img/icons.svg#i-x"></use></svg></button>' +
      '<button class="lightbox__btn lightbox__prev" type="button" aria-label="Previous image"><svg class="icon"><use href="/assets/img/icons.svg#i-chevron-left"></use></svg></button>' +
      '<button class="lightbox__btn lightbox__next" type="button" aria-label="Next image"><svg class="icon"><use href="/assets/img/icons.svg#i-chevron-right"></use></svg></button>';
    d.body.appendChild(dlg);
    var limg = $("img", dlg), cap = $("figcaption", dlg), idx = 0;
    var show = function (i) {
      idx = (i + tiles.length) % tiles.length;
      var t = tiles[idx], ti = $("img", t);
      limg.src = t.getAttribute("href");
      limg.alt = ti ? ti.alt : "";
      cap.textContent = t.getAttribute("data-caption") || "";
      if (!reduce && limg.animate) limg.animate({ opacity: [0, 1], transform: ["scale(.97)", "none"] }, { duration: 450, easing: "cubic-bezier(.16,1,.3,1)" });
    };
    tiles.forEach(function (t, i) { on(t, "click", function (e) { e.preventDefault(); show(i); dlg.showModal(); }); });
    on($(".lightbox__close", dlg), "click", function () { dlg.close(); });
    on($(".lightbox__prev", dlg), "click", function () { show(idx - 1); });
    on($(".lightbox__next", dlg), "click", function () { show(idx + 1); });
    on(dlg, "keydown", function (e) { if (e.key === "ArrowLeft") show(idx - 1); if (e.key === "ArrowRight") show(idx + 1); });
    on(dlg, "click", function (e) { if (e.target === dlg || e.target.classList.contains("lightbox__fig")) dlg.close(); });
  }

  /* ------------------------------------------------------------- forms */
  var PHONE_RE = /^(?:\+?254|0)?\s*[17]\d{2}\s*\d{3}\s*\d{3}$/;
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  function setErr(field, msg) {
    var wrap = field.closest(".field") || field.closest(".consent"), err = wrap ? $(".field__err", wrap) : null;
    if (wrap) wrap.classList.toggle("has-error", !!msg);
    field.setAttribute("aria-invalid", msg ? "true" : "false");
    if (err) err.textContent = msg || "";
  }
  function check(field) {
    var v = (field.value || "").trim(), msg = "";
    if (field.type === "checkbox") { if (field.required && !field.checked) msg = "Please tick to let us contact you."; }
    else if (field.required && !v) msg = "Please fill this in.";
    else if (v && field.name === "phone" && !PHONE_RE.test(v.replace(/[-()]/g, ""))) msg = "Enter a Kenyan mobile, e.g. 0711 128 736.";
    else if (v && field.type === "email" && !EMAIL_RE.test(v)) msg = "That email address does not look right.";
    setErr(field, msg);
    return !msg;
  }
  function checkAll(scope) {
    var ok = true, first = null;
    $$("input, select, textarea", scope).forEach(function (f) {
      if (f.closest(".hp") || f.type === "hidden") return;
      if (!check(f)) { ok = false; if (!first) first = f; }
    });
    if (first) first.focus();
    return ok;
  }
  var params = new URLSearchParams(w.location.search);
  $$("form.js-form").forEach(function (form) {
    var ts = $('input[name="t"]', form);
    if (ts) ts.value = String(Math.floor(Date.now() / 1000));
    var svc = params.get("service"), sel = $('select[name="service"]', form);
    if (svc && sel) $$("option", sel).forEach(function (o) { if (o.value.toLowerCase() === svc.toLowerCase()) sel.value = o.value; });
    /* errors clear while typing, never on the tap that follows (no layout shift under the finger) */
    $$("input, select, textarea", form).forEach(function (f) {
      on(f, "input", function () { if (f.getAttribute("aria-invalid") === "true") check(f); });
      on(f, "change", function () { if (f.getAttribute("aria-invalid") === "true") check(f); });
      on(f, "blur", function (e) {
        var to = e.relatedTarget;
        if (to && to.tagName === "BUTTON" && form.contains(to)) return;
        if (f.value) check(f);
      });
    });
    var steps = $$("[data-step]", form);
    if (steps.length === 2) {
      var next = $("[data-next]", form), back = $("[data-back]", form), submit = $("[data-submit]", form);
      var marks = $$(".progress__step", form);
      var go = function (n, moveFocus) {
        steps.forEach(function (s, i) { s.hidden = i !== n; });
        marks.forEach(function (m, i) { m.classList.toggle("is-on", i <= n); });
        next.hidden = n !== 0; back.hidden = n !== 1; submit.hidden = n !== 1;
        if (!reduce && moveFocus && steps[n].animate) steps[n].animate({ opacity: [0, 1], transform: ["translateX(" + (n ? 24 : -24) + "px)", "none"] }, { duration: 480, easing: "cubic-bezier(.16,1,.3,1)" });
        if (!moveFocus) return;
        var lg = $("legend", steps[n]);
        if (lg) { lg.setAttribute("tabindex", "-1"); lg.focus({ preventScroll: true }); }
        var top = form.getBoundingClientRect().top + w.scrollY - 120;
        if (top < w.scrollY) w.scrollTo({ top: top, behavior: reduce ? "auto" : "smooth" });
      };
      go(0, false);
      on(next, "click", function () { if (checkAll(steps[0])) go(1, true); });
      on(back, "click", function () { go(0, true); });
    }
    on(form, "submit", function (e) {
      if (steps.length === 2 && steps[1].hidden) { e.preventDefault(); var nx = $("[data-next]", form); if (nx) nx.click(); return; }
      if (!checkAll(form)) { e.preventDefault(); return; }
      var btn = $("[type=submit]:not([hidden])", form);
      if (btn) { btn.disabled = true; btn.setAttribute("aria-busy", "true"); }
    });
  });
  var err = params.get("error"), msgBox = $("#form-msg");
  if (err && msgBox) {
    var MSGS = {
      invalid: "Some details were missing or did not look right. Please check the form and send it again.",
      rate: "We have received several requests from you already. Please call or WhatsApp us instead.",
      server: "Something went wrong on our side. Please call or WhatsApp " + (msgBox.getAttribute("data-phone") || "us") + "."
    };
    msgBox.textContent = MSGS[err] || MSGS.invalid;
    msgBox.hidden = false;
  }

  /* ------------------------------------------------------------- consent + analytics (only if configured) */
  var GA = h.getAttribute("data-ga"), cookie = $(".cookie");
  function loadGA() {
    if (!GA || w.gtag) return;
    var s = d.createElement("script");
    s.async = true; s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(GA);
    d.head.appendChild(s);
    w.dataLayer = w.dataLayer || [];
    w.gtag = function () { w.dataLayer.push(arguments); };
    w.gtag("js", new Date());
    w.gtag("config", GA, { anonymize_ip: true });
    if (d.body.getAttribute("data-page") === "thank-you") w.gtag("event", "generate_lead");
    $$('a[href^="tel:"]').forEach(function (a) { on(a, "click", function () { w.gtag("event", "click_call"); }); });
    $$('a[href^="https://wa.me/"]').forEach(function (a) { on(a, "click", function () { w.gtag("event", "click_whatsapp"); }); });
  }
  function consent(v) {
    try { localStorage.setItem("sl-consent", v + "|" + Date.now()); } catch (e) {}
    if (cookie) { cookie.classList.remove("is-in"); setTimeout(function () { cookie.hidden = true; }, 450); }
    if (v === "granted") loadGA();
  }
  if (GA && cookie) {
    var saved = null;
    try { saved = localStorage.getItem("sl-consent"); } catch (e) {}
    var fresh = saved && (Date.now() - parseInt(saved.split("|")[1], 10)) < 31536000000;
    if (fresh && saved.indexOf("granted") === 0) loadGA();
    else if (!fresh) { cookie.hidden = false; setTimeout(function () { cookie.classList.add("is-in"); }, 1600); }
    on($("[data-consent=granted]", cookie), "click", function () { consent("granted"); });
    on($("[data-consent=denied]", cookie), "click", function () { consent("denied"); });
    $$("[data-cookie-settings]").forEach(function (b) {
      on(b, "click", function () { cookie.hidden = false; requestAnimationFrame(function () { cookie.classList.add("is-in"); }); });
    });
  }

  req();
})();
