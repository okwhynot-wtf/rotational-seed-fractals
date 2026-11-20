"""Check the generated site without a network or browser.

Checks local links, fragment targets, media, image alternatives, and local
targets of this repository's GitHub source links. Does not replace visual QA.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.links, self.errors = path, set(), [], []
        self.images = self.videos = 0
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get("id"):
            if attrs["id"] in self.ids:
                self.errors.append(f"duplicate id {attrs['id']!r}")
            self.ids.add(attrs["id"])
        for key in ("href", "src", "poster"):
            if attrs.get(key):
                self.links.append((tag, key, attrs[key]))
        if tag == "img":
            self.images += 1
            if "alt" not in attrs:
                self.errors.append("image has no alt attribute")
            if not attrs.get("src"):
                self.errors.append("image has no source")
        if tag == "video":
            self.videos += 1
            if not (attrs.get("aria-label") or attrs.get("aria-labelledby")):
                self.errors.append("video has no accessible label")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="okwhynot-wtf/rotational-seed-fractals")
    parser.add_argument("--allow-pending-media", action="store_true",
                        help="Development only: report missing MP4s as pending instead of failing.")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    pages = {p.resolve(): Page(p) for p in SITE.glob("*.html")}
    if not pages:
        raise SystemExit("No HTML pages; run scripts/build_site.py first.")
    errors, pending = [], []
    checked_links = source_links = 0
    repo_prefix = "/" + args.repo + "/"
    for path, page in pages.items():
        label = path.relative_to(ROOT).as_posix()
        errors.extend(f"{label}: {e}" for e in page.errors)
        content = path.read_text(encoding="utf-8")
        if "MATHPLACEHOLDER" in content or re.search(r"(?:href|src)=[\"'][A-Za-z]:[/\\]", content):
            errors.append(f"{label}: unresolved math or workstation link")
        for tag, key, link in page.links:
            url = urlsplit(link)
            if url.netloc == "github.com" and url.path.startswith(repo_prefix):
                rest = url.path[len(repo_prefix):]
                if rest.startswith(("blob/main/", "tree/main/")):
                    relative = unquote(rest.split("/", 2)[2])
                    target = (ROOT / relative).resolve()
                    source_links += 1
                    if not target.is_relative_to(ROOT) or not target.exists():
                        errors.append(f"{label}: missing repository target {relative}")
                continue
            if url.scheme or url.netloc:
                continue
            relative = unquote(url.path)
            target = (path.parent / relative).resolve() if relative else path
            if target.is_dir():
                target /= "index.html"
            checked_links += 1
            if not target.is_relative_to(SITE):
                errors.append(f"{label}: local link escapes site: {link}")
                continue
            if not target.is_file() or (target.stat().st_size == 0 and target.name != ".nojekyll"):
                if args.allow_pending_media and target.suffix == ".mp4":
                    pending.append(link)
                else:
                    errors.append(f"{label}: missing or empty {key}: {link}")
                continue
            if url.fragment and target.suffix == ".html":
                fragment = unquote(url.fragment)
                destination = pages.get(target)
                if destination is None or fragment not in destination.ids:
                    errors.append(f"{label}: missing fragment: {link}")
    result = {
        "status": "failed" if errors else "passed with pending media" if pending else "passed",
        "html_pages": len(pages), "local_links_checked": checked_links,
        "repository_source_links_checked": source_links,
        "images_with_alt_checked": sum(p.images for p in pages.values()),
        "labelled_videos_checked": sum(p.videos for p in pages.values()),
        "pending_media": sorted(set(pending)), "errors": errors,
        "scope": "Static local validation; not video decoding, external URL validation, or browser visual review.",
    }
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
