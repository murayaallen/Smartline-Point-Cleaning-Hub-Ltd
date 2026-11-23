"""Tell IndexNow search engines (Bing, Yandex, Seznam, Naver) which pages are live or changed.

    python tools/indexnow.py            # dry run: prints what would be sent
    python tools/indexnow.py --send     # sends it — run only after the upload passes RUNBOOK §3 live checks

Reads site/sitemap.xml, so it submits exactly the indexable pages. The key file
(/<INDEXNOW_KEY>.txt) is published by build_site.py and must already be live, or the
engines reject the ping (HTTP 403). Google does not use IndexNow: for Google, submit the
sitemap in Search Console (RUNBOOK §4). Stdlib only.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import site_content as C  # noqa: E402

ENDPOINT = "https://api.indexnow.org/indexnow"


def payload():
    sm = open(os.path.join(ROOT, "site", "sitemap.xml"), encoding="utf-8").read()
    urls = re.findall(r"<loc>([^<]+)</loc>", sm)
    if not urls:
        sys.exit("indexnow: sitemap.xml lists no URLs")
    return {"host": C.DOMAIN, "key": C.INDEXNOW_KEY,
            "keyLocation": "%s/%s.txt" % (C.ORIGIN, C.INDEXNOW_KEY), "urlList": urls}


def main():
    body = payload()
    print("IndexNow: %d URLs for %s (key file %s)" % (len(body["urlList"]), body["host"], body["keyLocation"]))
    if "--send" not in sys.argv:
        print(json.dumps(body, indent=1))
        print("dry run — add --send once the site is live")
        return
    req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("sent: HTTP %d (200 = accepted, 202 = accepted, key check pending)" % r.status)
    except urllib.error.HTTPError as e:
        hint = {400: "bad request", 403: "key file not found or wrong — is it live?",
                422: "URLs do not belong to the host", 429: "too many requests — try later"}.get(e.code, "")
        sys.exit("IndexNow refused: HTTP %d %s" % (e.code, hint))


if __name__ == "__main__":
    main()
