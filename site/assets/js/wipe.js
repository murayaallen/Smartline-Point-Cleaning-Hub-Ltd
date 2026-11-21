/* =====================================================================
   Smartline — "wipe the glass". A misted pane sits over the window photo;
   the visitor clears it with the cursor (or a finger), or presses the
   button and a squeegee pass does it for them. Loaded by main.js only when
   the section comes near, never under reduced motion. The photo underneath
   is a normal <img>, so without this file the glass is simply clean.
   ===================================================================== */
(function (d, w) {
  "use strict";
  var stage = d.querySelector("[data-wipe]");
  if (!stage || stage._wipe) return;
  stage._wipe = 1;
  var img = stage.querySelector("img"), cv = stage.querySelector("canvas"), ctx = cv.getContext("2d");
  var go = d.querySelector("[data-wipe-go]"), bar = stage.querySelector(".wipe__bar span");
  var W = 0, H = 0, dpr = Math.min(w.devicePixelRatio || 1, 2), brush = 60, last = null;
  var touched = false, done = false, busy = false, checkT = 0;
  var probe = d.createElement("canvas"), pctx = probe.getContext("2d", { willReadFrequently: true });
  probe.width = 36; probe.height = 45;

  function cover(iw, ih) {
    var s = Math.max(W / iw, H / ih);
    return [(W - iw * s) / 2, (H - ih * s) / 2, iw * s, ih * s];
  }

  /* misted glass: the photo itself, blurred and washed out, a cold haze, condensation */
  function mist() {
    var r = stage.getBoundingClientRect();
    W = r.width; H = r.height;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.globalCompositeOperation = "source-over";
    var c = cover(img.naturalWidth || 4, img.naturalHeight || 5);
    ctx.filter = "blur(16px) saturate(.45) brightness(1.18)";
    ctx.drawImage(img, c[0], c[1], c[2], c[3]);
    ctx.filter = "none";
    var g = ctx.createLinearGradient(0, 0, W, H);
    g.addColorStop(0, "rgba(236,240,250,.72)");
    g.addColorStop(0.5, "rgba(214,222,240,.58)");
    g.addColorStop(1, "rgba(236,240,250,.7)");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);
    for (var i = 0; i < 260; i++) {
      var x = Math.random() * W, y = Math.random() * H, rr = Math.random() * 2.6 + 0.4;
      ctx.fillStyle = "rgba(255,255,255," + (Math.random() * 0.45 + 0.15).toFixed(2) + ")";
      ctx.beginPath(); ctx.arc(x, y, rr, 0, 7); ctx.fill();
    }
    for (var j = 0; j < 7; j++) {               /* a few drips running down the pane */
      var dx = Math.random() * W, dy = Math.random() * H * 0.5, len = 40 + Math.random() * 120;
      var dg = ctx.createLinearGradient(0, dy, 0, dy + len);
      dg.addColorStop(0, "rgba(255,255,255,.55)"); dg.addColorStop(1, "rgba(255,255,255,0)");
      ctx.fillStyle = dg; ctx.fillRect(dx, dy, 2, len);
    }
    brush = Math.max(44, W * 0.15);
    stage.classList.add("is-misted");
  }

  function stroke(x0, y0, x1, y1) {
    ctx.globalCompositeOperation = "destination-out";
    ctx.lineCap = "round"; ctx.lineJoin = "round";
    ctx.lineWidth = brush;
    ctx.strokeStyle = "#000";
    ctx.shadowColor = "#000"; ctx.shadowBlur = brush * 0.3;
    ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke();
    ctx.shadowBlur = 0;
    if (!checkT) checkT = setTimeout(check, 180);
  }

  /* how much glass is clear: read a 36x45 thumbnail of the mist, count the see-through cells */
  function check() {
    checkT = 0;
    pctx.clearRect(0, 0, 36, 45);
    pctx.drawImage(cv, 0, 0, 36, 45);
    var a = pctx.getImageData(0, 0, 36, 45).data, clear = 0;
    for (var i = 3; i < a.length; i += 4) if (a[i] < 60) clear++;
    var p = clear / (a.length / 4);
    if (bar) bar.style.transform = "scaleX(" + Math.min(1, p / 0.88).toFixed(3) + ")";
    if (p > 0.88 && !done) finish();
  }

  function finish() {
    done = true;
    stage.classList.add("is-spotless");
    if (go) { go.disabled = true; go.querySelector(".wipe__go-t").textContent = "Spotless"; }
  }

  function pt(e) { var r = cv.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; }
  var down = false;                     /* a mouse wipes on hover; a finger or pen wipes while pressed */
  var passId = 0, demo = false;
  function takeOver() { if (demo) { passId++; busy = false; demo = false; } }   /* the visitor beats the demo */
  cv.addEventListener("pointerdown", function (e) {
    takeOver();
    if (done || busy) return;
    down = true; touched = true; last = pt(e);
    stroke(last[0], last[1], last[0] + 0.1, last[1]);
  });
  cv.addEventListener("pointermove", function (e) {
    var p = pt(e), live = e.pointerType === "mouse" || down;
    if (live) takeOver();
    if (done || busy) return;
    if (live) {
      touched = true;
      stroke(last ? last[0] : p[0], last ? last[1] : p[1], p[0], p[1]);
      stage.classList.add("is-wiping");
    }
    last = live ? p : null;
  });
  ["pointerup", "pointercancel", "pointerleave"].forEach(function (t) { cv.addEventListener(t, function () { down = false; last = null; }); });

  /* a squeegee pass: overlapping horizontal strokes top to bottom, alternating direction */
  function pass(rows, dur, cb, isDemo) {
    busy = true; demo = !!isDemo;
    var id = ++passId, t0 = performance.now(), gap = brush * 0.72, n = Math.min(rows, Math.ceil(H / gap) + 1), prev = null;
    function at(t) {
      var k = Math.min(n, t * n), row = Math.floor(Math.min(k, n - 0.0001)), f = k - row;
      var y = gap * 0.4 + row * gap, x = row % 2 ? W * (1.05 - f * 1.1) : W * (-0.05 + f * 1.1);
      return [x, y];
    }
    (function tick(now) {
      if (id !== passId) return;                       /* cancelled: the visitor took over */
      var t = Math.min(1, (now - t0) / dur), p = at(t);
      if (prev && Math.abs(prev[1] - p[1]) < 1) stroke(prev[0], prev[1], p[0], p[1]);
      prev = p;
      if (t < 1) requestAnimationFrame(tick); else { busy = false; demo = false; check(); if (cb) cb(); }
    })(t0);
  }

  function start() {
    mist();
    if (go) go.addEventListener("click", function () { touched = true; takeOver(); if (!done && !busy) pass(99, 1700, finish); });
    if ("IntersectionObserver" in w) {
      var io = new IntersectionObserver(function (en) {
        if (!en[0].isIntersecting) return;
        io.disconnect();
        setTimeout(function () { if (!touched && !done && !busy) pass(2, 1300, null, true); }, 1100);   /* show, don't tell */
      }, { threshold: 0.55 });
      io.observe(stage);
    }
    var rw = W, rt;
    w.addEventListener("resize", function () {
      clearTimeout(rt);
      rt = setTimeout(function () { if (!done && Math.abs(stage.getBoundingClientRect().width - rw) > 40) { mist(); rw = W; } }, 200);
    });
  }
  if (img.complete && img.naturalWidth) start();
  else img.addEventListener("load", start, { once: true });
})(document, window);
