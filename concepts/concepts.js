/* Smartline — hero concepts (dev review only; see make_concepts.py).
   One job each: start the entrance once the loader has gone, write --p (scroll progress through
   the pinned hero) for the CSS, and run concept C's word cycle and card deck. */
(function () {
  "use strict";
  var d = document, w = window, h = d.documentElement;
  var hero = d.querySelector("[data-cx]");
  if (!hero) return;
  var kind = hero.getAttribute("data-cx");
  var pin = hero.querySelector(".cx__pin");
  var reduce = h.classList.contains("reduce-motion") || (w.matchMedia && w.matchMedia("(prefers-reduced-motion: reduce)").matches);
  var p = 0, ticking = false, deck = function () {};

  /* entrance: wait for the loader (main.js takes it away), then play */
  var t0 = Date.now();
  (function wait() {
    var l = d.querySelector(".loader");
    if (reduce || !l || l.classList.contains("is-done") || Date.now() - t0 > 4500) {
      setTimeout(function () { hero.classList.add("is-in"); }, l && !reduce ? 260 : 40);
    } else setTimeout(wait, 80);
  })();

  /* scroll progress through the pinned hero */
  function measure() {
    var r = hero.getBoundingClientRect();
    var total = Math.max(1, hero.offsetHeight - w.innerHeight);
    p = Math.min(1, Math.max(0, -r.top / total));
    pin.style.setProperty("--p", p.toFixed(4));
    deck();
  }
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { ticking = false; measure(); });
  }

  /* B: the droplet's proportions, for placing the ripples where it lands */
  if (kind === "b") {
    var im = new Image();
    im.onload = function () { if (im.naturalWidth && im.naturalHeight) pin.style.setProperty("--da", (im.naturalWidth / im.naturalHeight).toFixed(4)); };
    im.src = "/concepts/img/droplet.svg";
  }

  /* C: the accent word cycles services; the deck follows; scroll fans the deck out */
  if (kind === "c") {
    var cards = [].slice.call(hero.querySelectorAll(".cxc__card"));
    var words = [].slice.call(hero.querySelectorAll(".cxc__word"));
    var deckEl = hero.querySelector(".cxc__deck");
    var active = 0;
    var ease = function (x) { return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
    deck = function () {
      if (!deckEl.offsetWidth) return;
      var mob = w.innerWidth <= 760;
      var W = deckEl.offsetWidth, H = deckEl.offsetHeight;
      var dr = deckEl.getBoundingClientRect(), pr = pin.getBoundingClientRect();
      var dx0 = (pr.left + pr.width / 2) - (dr.left + dr.width / 2);
      var dy0 = (pr.top + pr.height * (mob ? .52 : .55)) - (dr.top + dr.height / 2);
      var e = reduce ? 0 : ease(Math.min(1, Math.max(0, (p - .1) / .6)));
      cards.forEach(function (c, k) {
        var pos = (k - active + 4) % 4;
        var a = { x: pos * 22, y: pos * -16, r: pos * 5 - 3, s: 1 - pos * .06 };
        var f = mob ? { x: dx0 + ((k % 2) - .5) * (W * .52 + 12), y: dy0 + (Math.floor(k / 2) - .5) * (H * .52 + 12), r: 0, s: .5 }
                    : { x: dx0 + (k - 1.5) * (W * .66 + 22), y: dy0, r: 0, s: .64 };
        var x = a.x + (f.x - a.x) * e, y = a.y + (f.y - a.y) * e, r = a.r + (f.r - a.r) * e, s = a.s + (f.s - a.s) * e;
        c.style.transform = "translate(" + x.toFixed(1) + "px," + y.toFixed(1) + "px) rotate(" + r.toFixed(2) + "deg) scale(" + s.toFixed(3) + ")";
        c.style.zIndex = String(e > .5 ? 1 : 10 - pos);
      });
    };
    if (!reduce) {
      setInterval(function () {
        if (p > .04 || d.hidden || !hero.classList.contains("is-in")) return;
        var prev = active;
        active = (active + 1) % cards.length;
        words[prev].classList.remove("is-on");
        words[prev].classList.add("is-out");
        setTimeout(function () { words[prev].classList.remove("is-out"); }, 800);
        words[active].classList.add("is-on");
        deck();
      }, 2600);
    }
  }

  measure();
  if (!reduce) {
    w.addEventListener("scroll", onScroll, { passive: true });
    w.addEventListener("resize", onScroll);
  }
})();
