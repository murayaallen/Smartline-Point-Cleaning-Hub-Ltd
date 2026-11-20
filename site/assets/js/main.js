/* =====================================================================
   Smartline Point Cleaning Hub Ltd — site behaviour. Vanilla, no framework.
   Every feature is progressive: the site reads and the forms submit without it.
   ===================================================================== */
(function () {
  "use strict";
  var d = document, h = d.documentElement, w = window;
  var reduce = h.classList.contains("reduce-motion");
  function $(s, c) { return (c || d).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }
  function on(el, ev, fn, o) { if (el) el.addEventListener(ev, fn, o || false); }

  /* ------------------------------------------------------------- loader + hero entrance */
  var loader = $(".loader");
  function startHero() {
    var hero = $(".hero");
    if (!hero) return;
    requestAnimationFrame(function () {
      hero.classList.add("is-in");
      $$(".frame", hero).forEach(function (f) { f.classList.add("is-in"); });
    });
  }
  function loaderVisible() {
    return loader && !h.classList.contains("loaded-before") && !reduce && getComputedStyle(loader).display !== "none";
  }
  if (loaderVisible()) {
    var t0 = performance.now(), done = false;
    var finish = function () {
      if (done) return; done = true;
      var wait = Math.max(0, 1150 - (performance.now() - t0));
      setTimeout(function () {
        loader.classList.add("is-done");
        setTimeout(startHero, 260);
        setTimeout(function () { if (loader.parentNode) loader.parentNode.removeChild(loader); }, 900);
      }, wait);
    };
    if (d.readyState === "complete") finish(); else on(w, "load", finish);
    setTimeout(finish, 2600);
  } else {
    if (loader && loader.parentNode) loader.parentNode.removeChild(loader);
    startHero();
  }

  /* ------------------------------------------------------------- header */
  var hdr = $(".hdr"), ticking = false;
  function onScroll() {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () {
      var y = w.scrollY || w.pageYOffset;
      if (hdr) hdr.classList.toggle("is-scrolled", y > 40);
      parallax(y);
      ticking = false;
    });
  }
  on(w, "scroll", onScroll, { passive: true });
  onScroll();

  /* subtle hero parallax, desktop only */
  var heroImg = $(".hero .frame img"), ctaImg = $$(".cta__bg img");
  var wide = w.matchMedia("(min-width: 1041px)");
  function parallax(y) {
    if (reduce || !wide.matches) return;
    if (heroImg && y < 900) heroImg.style.translate = "0 " + (y * 0.06).toFixed(1) + "px";
    ctaImg.forEach(function (img) {
      var r = img.parentNode.getBoundingClientRect();
      if (r.bottom > 0 && r.top < w.innerHeight) img.style.translate = "0 " + ((r.top - w.innerHeight / 2) * -0.06).toFixed(1) + "px";
    });
  }

  /* ------------------------------------------------------------- mega menu */
  $$(".nav__item--mega").forEach(function (item) {
    var btn = $(".nav__link", item), panel = $(".mega", item), timer, hoveredAt = 0;
    function open() { clearTimeout(timer); item.classList.add("is-open"); btn.setAttribute("aria-expanded", "true"); }
    function close(focus) {
      item.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false");
      if (focus) btn.focus();
    }
    on(btn, "click", function (e) {
      e.preventDefault();
      /* a mouse opens it on hover; the click that follows must not shut it again */
      if (item.classList.contains("is-open") && Date.now() - hoveredAt > 700) close(); else open();
    });
    on(item, "mouseenter", function () { if (w.matchMedia("(hover: hover)").matches) { hoveredAt = Date.now(); open(); } });
    on(item, "mouseleave", function () { timer = setTimeout(function () { close(); }, 180); });
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
    requestAnimationFrame(function () { drawer.classList.add("is-open"); });
    d.body.classList.add("no-scroll");
    burger.setAttribute("aria-expanded", "true");
    on(d, "keydown", trap);
    setTimeout(function () { var c = $(".drawer__close", drawer); if (c) c.focus(); }, 60);
  }
  function closeDrawer() {
    drawer.classList.remove("is-open");
    d.body.classList.remove("no-scroll");
    burger.setAttribute("aria-expanded", "false");
    d.removeEventListener("keydown", trap);
    setTimeout(function () { drawer.hidden = true; }, 500);
    if (lastFocus) lastFocus.focus();
  }
  if (drawer && burger) {
    on(burger, "click", openDrawer);
    $$("[data-close-drawer]", drawer).forEach(function (b) { on(b, "click", closeDrawer); });
    $$(".drawer__nav a, .drawer__acc a", drawer).forEach(function (a) { on(a, "click", closeDrawer); });
  }

  /* ------------------------------------------------------------- reveal on scroll */
  $$("[data-stagger]").forEach(function (group) {
    $$(".reveal", group).forEach(function (el, i) { el.style.transitionDelay = (i * 90) + "ms"; });
  });
  var reveals = $$(".reveal");
  if ("IntersectionObserver" in w && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ------------------------------------------------------------- count-up */
  var counters = $$("[data-count]");
  function countUp(el) {
    var to = parseInt(el.getAttribute("data-count"), 10), suf = el.getAttribute("data-suffix") || "", t0 = null, dur = 1400;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(to * e) + suf;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if (counters.length && "IntersectionObserver" in w && !reduce) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { countUp(en.target); cio.unobserve(en.target); } });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { cio.observe(c); });
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
        anim = body.animate({ height: [hgt + "px", "0px"], opacity: [1, 0] }, { duration: 320, easing: "cubic-bezier(.22,.61,.36,1)" });
        anim.onfinish = function () { det.open = false; anim = null; };
      } else {
        det.open = true;
        var full = body.offsetHeight;
        anim = body.animate({ height: ["0px", full + "px"], opacity: [0, 1] }, { duration: 420, easing: "cubic-bezier(.16,1,.3,1)" });
        anim.onfinish = function () { anim = null; };
      }
    });
  });

  /* ------------------------------------------------------------- services sub-nav scroll-spy */
  var spyLinks = $$(".subnav a");
  if (spyLinks.length && "IntersectionObserver" in w) {
    var map = {};
    spyLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && map[en.target.id]) {
          spyLinks.forEach(function (a) { a.classList.remove("is-active"); a.removeAttribute("aria-current"); });
          map[en.target.id].classList.add("is-active");
          map[en.target.id].setAttribute("aria-current", "true");
        }
      });
    }, { rootMargin: "-35% 0px -60% 0px" });
    Object.keys(map).forEach(function (id) { var s = d.getElementById(id); if (s) sio.observe(s); });
    /* above the first group nothing is "current" */
    var firstGroup = d.getElementById(Object.keys(map)[0]);
    on(w, "scroll", function () {
      if (firstGroup && firstGroup.getBoundingClientRect().top > w.innerHeight * 0.4) {
        spyLinks.forEach(function (a) { a.classList.remove("is-active"); a.removeAttribute("aria-current"); });
      }
    }, { passive: true });
  }

  /* ------------------------------------------------------------- clients filter */
  var filterBtns = $$("[data-filter]");
  function applyFilter(key) {
    filterBtns.forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-filter") === key)); });
    var shown = 0;
    $$(".client").forEach(function (c) {
      var hit = key === "all" || c.getAttribute("data-sector") === key;
      c.classList.toggle("is-hidden", !hit);
      if (hit) shown++;
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
    var img = $("img", dlg), cap = $("figcaption", dlg), idx = 0;
    function show(i) {
      idx = (i + tiles.length) % tiles.length;
      var t = tiles[idx], ti = $("img", t);
      img.src = t.getAttribute("href");
      img.alt = ti ? ti.alt : "";
      cap.textContent = t.getAttribute("data-caption") || "";
    }
    tiles.forEach(function (t, i) {
      on(t, "click", function (e) { e.preventDefault(); show(i); dlg.showModal(); });
    });
    on($(".lightbox__close", dlg), "click", function () { dlg.close(); });
    on($(".lightbox__prev", dlg), "click", function () { show(idx - 1); });
    on($(".lightbox__next", dlg), "click", function () { show(idx + 1); });
    on(dlg, "keydown", function (e) {
      if (e.key === "ArrowLeft") show(idx - 1);
      if (e.key === "ArrowRight") show(idx + 1);
    });
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
    if (svc && sel) {
      $$("option", sel).forEach(function (o) { if (o.value.toLowerCase() === svc.toLowerCase()) sel.value = o.value; });
    }
    /* Errors clear while the visitor types, never on the tap that follows: clearing on
       blur shifted the layout under the finger and the Continue tap missed. */
    $$("input, select, textarea", form).forEach(function (f) {
      on(f, "input", function () { if (f.getAttribute("aria-invalid") === "true") check(f); });
      on(f, "change", function () { if (f.getAttribute("aria-invalid") === "true") check(f); });
      on(f, "blur", function (e) {
        var to = e.relatedTarget;
        if (to && to.tagName === "BUTTON" && form.contains(to)) return;   /* the button validates everything itself */
        if (f.value) check(f);
      });
    });

    var steps = $$("[data-step]", form);
    if (steps.length === 2) {
      var next = $("[data-next]", form), back = $("[data-back]", form), submit = $("[data-submit]", form);
      var marks = $$(".progress__step", form);
      function go(n, moveFocus) {
        steps.forEach(function (s, i) { s.hidden = i !== n; });
        marks.forEach(function (m, i) { m.classList.toggle("is-on", i <= n); });
        next.hidden = n !== 0; back.hidden = n !== 1; submit.hidden = n !== 1;
        if (!moveFocus) return;                       /* never steal focus on page load */
        var lg = $("legend", steps[n]);
        if (lg) { lg.setAttribute("tabindex", "-1"); lg.focus({ preventScroll: true }); }
        var top = form.getBoundingClientRect().top + w.scrollY - 120;
        if (top < w.scrollY) w.scrollTo({ top: top, behavior: reduce ? "auto" : "smooth" });
      }
      go(0, false);
      on(next, "click", function () { if (checkAll(steps[0])) go(1, true); });
      on(back, "click", function () { go(0, true); });
    }
    on(form, "submit", function (e) {
      if (steps.length === 2 && steps[1].hidden) {        /* Enter on step 1 advances, it never submits */
        e.preventDefault();
        var nx = $("[data-next]", form);
        if (nx) nx.click();
        return;
      }
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
  var GA = h.getAttribute("data-ga");
  var cookie = $(".cookie");
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
})();
