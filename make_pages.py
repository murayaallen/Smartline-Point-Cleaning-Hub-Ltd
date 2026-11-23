"""Build the GitHub Pages preview of site/ into dist/pages/.

    python make_pages.py

GitHub Pages serves this repository at https://murayaallen.github.io/Smartline-Point-Cleaning-Hub-Ltd/
-- a sub-path -- while site/ is written for the root of smartlinepointcleaning.co.ke. This copies
site/ and:
  - prefixes every root path: href, src, srcset, action, data-fx/data-wipe, CSS url(), JS, manifest
  - marks every page noindex, nofollow, so the preview never competes with the real domain in
    Google (canonical tags still point at smartlinepointcleaning.co.ke)
  - points og:url / og:image / twitter:image at the preview, so a link shared on WhatsApp shows the card
  - leaves out what only the Apache host can use: .htaccess, form/ (PHP), robots.txt, sitemap.xml,
    .well-known/, speculation-rules.json, and the readable JS sources
  - adds preview.js to form pages: GitHub Pages cannot run PHP, so a valid enquiry shows a note
    ("the form goes live with the domain") instead of posting into a 405
  - adds .nojekyll, so GitHub serves the files as they are

Stdlib + site_content only: .github/workflows/pages.yml runs this on every push to main and
publishes dist/pages to the gh-pages branch. verify() fails loudly if any root path escaped the
prefix or any local link, image or script points at a file that is not in the preview.
"""
import json
import os
import re
import shutil
import sys

import site_content as C

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
OUT = os.path.join(ROOT, "dist", "pages")

_repo = os.environ.get("GITHUB_REPOSITORY", "murayaallen/Smartline-Point-Cleaning-Hub-Ltd")
OWNER, REPO = _repo.split("/", 1)
BASE = "/%s/" % REPO                                     # every root path gains this prefix
PAGES_ORIGIN = "https://%s.github.io" % OWNER.lower()
URL = PAGES_ORIGIN + BASE

SKIP_FILES = {".htaccess", "robots.txt", "sitemap.xml", "speculation-rules.json",
              "assets/js/main.js", "assets/js/wipe.js", "assets/js/fx.js"}
SKIP_DIRS = {"form", ".well-known"}

URL_ATTR = re.compile(r'\b(href|src|action|poster|data-fx|data-wipe)="/(?!/)')
SRCSET = re.compile(r'\b(srcset|imagesrcset)="([^"]*)"')
ROBOTS = re.compile(r'<meta name="robots" content="[^"]*">')
SHARE = re.compile(r'(<meta (?:property="og:(?:url|image)"|name="twitter:image") content=")%s/'
                   % re.escape(C.ORIGIN))

PREVIEW_JS = """/* GitHub Pages preview only -- written by make_pages.py, never shipped to the live host.
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
    box.textContent = "This is the preview link, so the form does not send yet \\u2014 it goes live with "
      + "%(domain)s. Until then, call or WhatsApp " + (box.getAttribute("data-phone") || "%(phone)s") + ".";
    box.style.background = "#EEEDF8";
    box.style.color = "#1C1A5C";
    box.hidden = false;
    box.scrollIntoView({ block: "center", behavior: "smooth" });
  });
})();
""" % {"domain": C.DOMAIN, "phone": C.PHONE}


def _srcset(m):
    items = re.sub(r"(^|,\s*)/(?!/)", lambda k: k.group(1) + BASE, m.group(2))
    return '%s="%s"' % (m.group(1), items)


def rewrite_html(s, rel):
    s = URL_ATTR.sub(lambda m: '%s="%s' % (m.group(1), BASE), s)
    s = SRCSET.sub(_srcset, s)
    s, n = ROBOTS.subn('<meta name="robots" content="noindex, nofollow">', s)
    if n != 1:
        sys.exit("pages: %s has %d robots metas, expected 1" % (rel, n))
    s = SHARE.sub(lambda m: m.group(1) + URL, s)
    if "js-form" in s:
        tag = '<script src="%sassets/js/preview.js" defer></script>' % BASE
        if s.count("</body>") != 1:
            sys.exit("pages: %s has no single </body>" % rel)
        s = s.replace("</body>", tag + "\n</body>")
    return s


def rewrite_css(s):
    return re.sub(r"""url\((["']?)/(?!/)""", lambda m: "url(%s%s" % (m.group(1), BASE), s)


def rewrite_js(s):
    return re.sub(r"""(["'])/assets/""", lambda m: "%s%sassets/" % (m.group(1), BASE), s)


def rewrite_manifest(s):
    data = json.loads(s)
    data["start_url"] = BASE
    data["scope"] = BASE
    for icon in data.get("icons", []):
        if icon["src"].startswith("/"):
            icon["src"] = BASE + icon["src"][1:]
    return json.dumps(data, indent=1)


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    count = 0
    for base, dirs, names in os.walk(SITE):
        rel_dir = os.path.relpath(base, SITE).replace(os.sep, "/")
        dirs[:] = sorted(d for d in dirs if (d if rel_dir == "." else rel_dir + "/" + d) not in SKIP_DIRS)
        for n in sorted(names):
            rel = n if rel_dir == "." else rel_dir + "/" + n
            if rel in SKIP_FILES or n == ".htaccess" or n == C.INDEXNOW_KEY + ".txt":
                continue
            src, dst = os.path.join(base, n), os.path.join(OUT, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if n.endswith((".html", ".css", ".js", ".webmanifest")):
                s = open(src, encoding="utf-8").read()
                if n.endswith(".html"):
                    s = rewrite_html(s, rel)
                elif n.endswith(".css"):
                    s = rewrite_css(s)
                elif n.endswith(".js"):
                    s = rewrite_js(s)
                else:
                    s = rewrite_manifest(s)
                with open(dst, "w", encoding="utf-8", newline="\n") as f:
                    f.write(s)
            else:
                shutil.copyfile(src, dst)
            count += 1
    with open(os.path.join(OUT, "assets", "js", "preview.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write(PREVIEW_JS)
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    return count + 2


def _exists(path):
    """Resolve a preview path the way GitHub Pages does: dir -> index.html, /about -> about.html."""
    rel = path[len(BASE):].split("#")[0].split("?")[0]
    full = os.path.join(OUT, *rel.split("/")) if rel else OUT
    if os.path.isdir(full):
        return os.path.isfile(os.path.join(full, "index.html"))
    return os.path.isfile(full) or os.path.isfile(full + ".html")


def verify():
    errors, refs = [], 0
    for base, _, names in os.walk(OUT):
        for n in names:
            full = os.path.join(base, n)
            rel = os.path.relpath(full, OUT).replace(os.sep, "/")
            if n.endswith(".php") or n == ".htaccess":
                errors.append("server-only file shipped: " + rel)
            if not n.endswith((".html", ".css", ".js", ".webmanifest")):
                continue
            s = open(full, encoding="utf-8").read()
            if n.endswith(".html"):
                for m in re.finditer(r'\b(href|src|action|poster|data-fx|data-wipe)="(/[^"]*)"', s):
                    attr, v = m.groups()
                    if v.startswith("//"):
                        continue
                    if not v.startswith(BASE):
                        errors.append("%s: %s escaped the prefix: %s" % (rel, attr, v))
                    elif attr != "action" and not _exists(v):    # the form action never runs here: preview.js
                        errors.append("%s: %s points at a missing file: %s" % (rel, attr, v))
                    refs += 1
                for m in SRCSET.finditer(s):
                    for item in m.group(2).split(","):
                        v = item.strip().split(" ")[0]
                        if not v.startswith(BASE) or not _exists(v):
                            errors.append("%s: srcset entry wrong or missing: %s" % (rel, v))
                        refs += 1
                if '<meta name="robots" content="noindex, nofollow">' not in s:
                    errors.append(rel + ": not marked noindex")
                if C.ORIGIN + "/assets/" in s.split("application/ld+json")[0]:
                    errors.append(rel + ": share image still points at the live domain")
            elif n.endswith(".css"):
                for v in re.findall(r"""url\(["']?(/[^)"']*)""", s):
                    if not v.startswith(BASE) or not _exists(v):
                        errors.append("%s: url() wrong or missing: %s" % (rel, v))
                    refs += 1
            elif n.endswith(".js"):
                for v in re.findall(r"""["'](/assets/[^"']*)""", s):
                    errors.append("%s: root path escaped the prefix: %s" % (rel, v))
    for need in ("index.html", "404.html", ".nojekyll", "assets/js/preview.js", "assets/css/main.css"):
        if not os.path.isfile(os.path.join(OUT, need)):
            errors.append("missing " + need)
    if errors:
        sys.exit("pages verify FAILED (%d):\n  %s" % (len(errors), "\n  ".join(errors[:40])))
    return refs


if __name__ == "__main__":
    n = build()
    refs = verify()
    size = sum(os.path.getsize(os.path.join(b, f)) for b, _, fs in os.walk(OUT) for f in fs)
    print("pages OK: %s (%d files, %.1f MB, %d local references resolved) -> %s"
          % (os.path.relpath(OUT, ROOT), n, size / 1e6, refs, URL))
