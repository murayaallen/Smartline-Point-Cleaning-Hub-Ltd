/* Runs before first paint (render-blocking, tiny): sets the classes the CSS needs so
   reveals never flash, the loader shows once per visit, and — if main.js never runs —
   nothing stays hidden. */
(function (d, w) {
  var h = d.documentElement;
  h.classList.add("js");
  try {
    if (sessionStorage.getItem("sl-seen")) h.classList.add("loaded-before");
    else sessionStorage.setItem("sl-seen", "1");
  } catch (e) { h.classList.add("loaded-before"); }
  if (w.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) h.classList.add("reduce-motion");
  setTimeout(function () { if (!w.__slMotion) h.classList.add("motion-failed"); }, 3000);
})(document, window);
