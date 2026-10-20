#!/usr/bin/env python3
"""Crawls the site and checks that every internal link and asset answers 200.

Local (serve the PARENT folder so the site sits in /vivaservice24/, like on GitHub Pages):
    cd .. && python3 -m http.server 4317
    python3 tools/check_links.py http://127.0.0.1:4317/vivaservice24/

Live:
    python3 tools/check_links.py https://welcometothenextlevel.github.io/vivaservice24/

Checks href, src, srcset, poster, data-src / data-sm / data-lg (video sources, .mp4 and .webm),
CSS url() references, and flags any root-absolute path ("/img/...") which would break in the subfolder.
"""
import re
import sys
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag, urlparse

START = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:4317/vivaservice24/"
ROOT = START if START.endswith("/") else START + "/"
UA = {"User-Agent": "Mozilla/5.0 (link-check)"}


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for k in ("href", "src", "poster", "data-src", "data-merci"):
            if a.get(k):
                self.refs.append((tag, k, a[k]))
        for k in ("srcset", "imagesrcset"):
            if a.get(k):
                for part in a[k].split(","):
                    u = part.strip().split(" ")[0]
                    if u:
                        self.refs.append((tag, k, u))
        for k in ("data-sm", "data-lg"):
            if a.get(k):
                self.refs.append((tag, k, a[k] + ".mp4"))
                self.refs.append((tag, k, a[k] + ".webm"))


cache = {}


def fetch(url):
    if url in cache:
        return cache[url]
    try:
        req = urllib.request.Request(url, headers=UA, method="GET")
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read() if (r.headers.get("Content-Type", "").startswith(("text/html", "text/css"))) else b""
            res = (r.status, r.headers.get("Content-Type", ""), body)
    except urllib.error.HTTPError as e:
        res = (e.code, "", b"")
    except Exception as e:  # noqa
        res = (0, str(e), b"")
    cache[url] = res
    return res


def main():
    todo, seen_pages = [ROOT], set()
    bad, absolute, anchors = [], [], []
    checked = 0
    page_ids = {}
    while todo:
        page = todo.pop()
        if page in seen_pages:
            continue
        seen_pages.add(page)
        st, ct, body = fetch(page)
        if st != 200:
            bad.append((page, "(page)", st))
            continue
        html = body.decode("utf-8", "replace")
        p = P()
        p.feed(html)
        page_ids[page] = p.ids
        # inline style url() (critical CSS)
        for u in re.findall(r"url\(([^)\"']+)\)", html):
            p.refs.append(("style", "url", u))
        for tag, attr, ref in p.refs:
            if ref.startswith(("mailto:", "tel:", "data:", "javascript:", "#")):
                if ref.startswith("#") and len(ref) > 1 and ref[1:] not in p.ids and attr == "href":
                    anchors.append((page, ref))
                continue
            if ref.startswith("/") and not ref.startswith("//"):
                absolute.append((page, ref))
            full = urljoin(page, ref)
            full, frag = urldefrag(full)
            if not full.startswith(ROOT):
                continue  # external
            checked += 1
            st2, ct2, body2 = fetch(full)
            if st2 != 200:
                bad.append((page, ref, st2))
                continue
            if ct2.startswith("text/html") and full not in seen_pages:
                todo.append(full)
            if ct2.startswith("text/css"):
                for u in re.findall(r"url\(([^)\"']+)\)", body2.decode("utf-8", "replace")):
                    if u.startswith("data:"):
                        continue
                    cu = urljoin(full, u)
                    st3 = fetch(cu)[0]
                    checked += 1
                    if st3 != 200:
                        bad.append((full, u, st3))
    # 404 page
    st404 = fetch(ROOT + "this/page/does-not-exist/")[0]
    print(f"pages crawled: {len(seen_pages)}  references checked: {checked}")
    for pg in sorted(seen_pages):
        print("  ", urlparse(pg).path)
    print(f"404 for a missing URL returns status {st404}")
    if absolute:
        print("\nROOT-ABSOLUTE PATHS (break in the subfolder):")
        for a in absolute:
            print("  ", a)
    if anchors:
        print("\nMISSING IN-PAGE ANCHORS:")
        for a in sorted(set(anchors)):
            print("  ", a)
    if bad:
        print("\nBROKEN:")
        for b in bad:
            print("  ", b)
        sys.exit(1)
    print("\nall internal links and assets OK" + ("" if not absolute else " (but fix the absolute paths)"))


if __name__ == "__main__":
    main()
