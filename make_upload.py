"""Package site/ into the zip that gets uploaded to public_html.

    python build_site.py && python make_upload.py

Writes dist/smartlinepointcleaning.co.ke-upload.zip with every file under site/,
dotfiles included (.htaccess, form/.htaccess, .well-known/security.txt), then
re-opens the zip and fails loudly if anything the server needs is missing.
dist/ is gitignored: the zip is always rebuilt from the committed site/ folder.
"""
import os
import sys
import zipfile

import site_content as C

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
DIST = os.path.join(ROOT, "dist")
ZIP = os.path.join(DIST, "%s-upload.zip" % C.DOMAIN)

REQUIRED = [
    ".htaccess", "robots.txt", "sitemap.xml", "site.webmanifest", "favicon.ico", "favicon.svg",
    "apple-touch-icon.png", "icon-192.png", "icon-512.png", ".well-known/security.txt",
    "form/.htaccess", "form/enquiry.php", "speculation-rules.json",
    "index.html", "about.html", "services.html", "commercial-cleaning.html",
    "residential-apartment-cleaning.html", "post-construction-cleaning.html", "clients.html",
    "contact.html", "thank-you.html", "privacy.html", "404.html",
    "assets/css/main.css", "assets/js/main.js", "assets/js/boot.js", "assets/img/icons.svg",
]
NEVER = (".py", ".pyc", ".md", ".map", ".DS_Store", "Thumbs.db")


def build():
    os.makedirs(DIST, exist_ok=True)
    files = []
    for base, dirs, names in os.walk(SITE):
        dirs.sort()
        for n in sorted(names):
            full = os.path.join(base, n)
            rel = os.path.relpath(full, SITE).replace(os.sep, "/")
            if rel.endswith(NEVER):
                sys.exit("upload: refusing to ship %s" % rel)
            files.append((full, rel))
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for full, rel in files:
            z.write(full, rel)
    return files


def verify():
    with zipfile.ZipFile(ZIP) as z:
        names = set(z.namelist())
        bad = z.testzip()
    missing = [r for r in REQUIRED if r not in names]
    if missing or bad:
        sys.exit("upload verify FAILED: missing %s, corrupt %s" % (missing, bad))
    sm = open(os.path.join(SITE, "sitemap.xml"), encoding="utf-8").read()
    if sm.count("<url>") != 9:
        sys.exit("upload verify FAILED: sitemap should list 9 URLs, has %d" % sm.count("<url>"))
    return len(names)


if __name__ == "__main__":
    build()
    n = verify()
    print("upload OK: %s (%d files, %.1f MB)" % (os.path.relpath(ZIP, ROOT), n, os.path.getsize(ZIP) / 1e6))
