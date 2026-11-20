/* Runs before first paint (render-blocking, ~400 bytes): sets the classes the CSS
   needs so reveals never flash and the loader shows once per visit, not per page. */
(function (d) {
  var h = d.documentElement;
  h.classList.add("js");
  try {
    if (sessionStorage.getItem("sl-seen")) h.classList.add("loaded-before");
    else sessionStorage.setItem("sl-seen", "1");
  } catch (e) { h.classList.add("loaded-before"); }
  if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) h.classList.add("reduce-motion");
})(document);
