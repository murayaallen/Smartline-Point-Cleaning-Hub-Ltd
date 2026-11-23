/* Runs before first paint (render-blocking, tiny): sets the classes the CSS needs so
   reveals never flash, the loader shows on every fresh landing (not page-to-page), and — if main.js never runs —
   nothing stays hidden. */
(function (d, w) {
  var h = d.documentElement;
  h.classList.add("js");
  try {
    if (sessionStorage.getItem("sl-pt")) h.classList.add("loaded-before");   /* came from another page */
  } catch (e) { h.classList.add("loaded-before"); }
  if (w.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) h.classList.add("reduce-motion");
  try {   /* arriving from another page of the site: the loading panel covers the first paint */
    if (sessionStorage.getItem("sl-pt")) {
      sessionStorage.removeItem("sl-pt");
      if (!h.classList.contains("reduce-motion")) h.classList.add("pt-arrive");
    }
  } catch (e) {}
  setTimeout(function () { if (!w.__slMotion) h.classList.add("motion-failed"); }, 3000);
})(document, window);
