/* GitHub Pages preview only -- written by make_pages.py, never shipped to the live host.
   Pages cannot run form/enquiry.php, so once main.js has validated an enquiry (this listener sits
   on window, so it runs after the form's own), show a note instead of posting into a 405. */
(function () {
  window.addEventListener("submit", function (e) {
    var form = e.target;
    if (e.defaultPrevented || !form.classList || !form.classList.contains("js-form")) return;
    e.preventDefault();
    document.documentElement.classList.remove("pt-leave");
    try { sessionStorage.removeItem("sl-pt"); } catch (x) {}
    var btn = form.querySelector("[type=submit][aria-busy]");
    if (btn) { btn.disabled = false; btn.removeAttribute("aria-busy"); }
    var box = document.getElementById("form-msg");
    if (!box) return;
    box.textContent = "This is the preview link, so the form does not send yet \u2014 it goes live with "
      + "smartlinepointcleaning.co.ke. Until then, call or WhatsApp " + (box.getAttribute("data-phone") || "+254 711 128736") + ".";
    box.style.background = "#EEEDF8";
    box.style.color = "#1C1A5C";
    box.hidden = false;
    box.scrollIntoView({ block: "center", behavior: "smooth" });
  });
})();
