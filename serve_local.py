# -*- coding: utf-8 -*-
"""Local preview of site/ that behaves like the live .htaccess:
/page -> page.html, unknown -> 404.html with status 404, and a stand-in for the
PHP form handler (validates nothing, just redirects to /thank-you).

    python serve_local.py [port]      # default 8765
"""
import http.server
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def log_message(self, *a):
        pass

    def end_headers(self):
        # same prefetch-on-hover rules the live .htaccess announces
        if self.path.endswith(".html"):
            self.send_header("Speculation-Rules", '"/speculation-rules.json"')
        super().end_headers()

    def guess_type(self, path):
        if str(path).endswith("speculation-rules.json"):
            return "application/speculationrules+json"
        return super().guess_type(path)

    def _resolve(self):
        path = self.path.split("?")[0].split("#")[0]
        if path == "/":
            return "/index.html"
        full = os.path.join(ROOT, path.lstrip("/"))
        if os.path.isfile(full):
            return path
        if os.path.isfile(full + ".html"):
            return path + ".html"
        return None

    def do_GET(self):
        target = self._resolve()
        if target is None:
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(ROOT, "404.html"), "rb") as f:
                self.wfile.write(f.read())
            return
        q = self.path[len(self.path.split("?")[0]):]
        self.path = target + q
        return super().do_GET()

    def do_POST(self):
        if self.path.startswith("/form/enquiry.php"):
            self.send_response(303)
            self.send_header("Location", "/thank-you")
            self.end_headers()
            return
        self.send_response(405)
        self.end_headers()


if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
