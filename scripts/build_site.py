"""Build a portable static GitHub Pages site; preserve all supplied media assets.

Run: uv run --python 3.12 --with markdown python scripts/build_site.py
"""
from __future__ import annotations
import argparse
import html
import re
import shutil
from pathlib import Path
from urllib.parse import quote

import markdown

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
OUT = ROOT / 'site'
PAGES = [
    ('definition', 'Definitions'), ('results', 'Results'), ('related', 'Related work'),
    ('reproduce', 'Reproduce'), ('paper', 'Paper draft'), ('media', 'Media'),
    ('provenance', 'Provenance'),
]
DESCRIPTION = 'Exact self-similar spatial constructions: a linked threefold continuum, a fourfold membrane, and dense full-ball tangent points. Candidate families; research in progress.'
MARK = '<svg class="brand-mark" viewBox="0 0 40 40" fill="none" aria-hidden="true"><path d="M20 3 35 12 35 29 20 37 5 29 5 12Z M20 3 20 37 M5 12 35 29 M35 12 5 29" stroke="currentColor" stroke-width="1.2"/><path d="m20 12 7 4v8l-7 4-7-4v-8Z" stroke="currentColor" stroke-width="1.2"/></svg>'


def rewritten_links(content: str, repo: str) -> str:
    """Make manuscript local links public and documentation links site-relative."""
    base = f'https://github.com/{repo}/blob/main/'
    source_root = ROOT.as_posix().rstrip('/') + '/'
    def replace(match):
        value = match.group(2)
        if value.startswith(source_root):
            value = base + quote(value[len(source_root):], safe='/#')
        elif re.match(r'^[A-Za-z]:/', value):
            # Do not leak workstation paths in a rendered public manuscript.
            marker = '/fractal_discovery_2026/'
            value = base + quote(value.split(marker, 1)[-1], safe='/#') if marker in value else base
        elif value.startswith('../'):
            value = base + quote(value[3:], safe='/#')
        elif re.match(r'^[a-z_-]+\.md(?:#.*)?$', value):
            value = value.replace('.md', '.html', 1)
        return match.group(1) + value + match.group(3)
    return re.sub(r'(href=["\'])([^"\']+)(["\'])', replace, content)


def render_markdown(source: str, repo: str) -> str:
    # Preserve TeX delimiters, backslashes, and matrix row breaks through Markdown.
    math = []
    def stash(match):
        math.append(match.group(0))
        return f'MATHPLACEHOLDERX{len(math)-1}ENDX'
    protected = re.sub(r'\\\[.*?\\\]|\\\(.*?\\\)|\$\$.*?\$\$', stash, source, flags=re.S)
    body = markdown.markdown(protected, extensions=['fenced_code', 'tables', 'toc', 'sane_lists'],
                             extension_configs={'toc': {'permalink': False}}, output_format='html5')
    for i, equation in enumerate(math):
        body = body.replace(f'MATHPLACEHOLDERX{i}ENDX', html.escape(equation))
    return rewritten_links(body, repo)


def header(repo: str, current: str) -> str:
    nav = f'<a href="index.html#families">Families</a><a href="results.html">Results</a><a href="paper.html">Paper draft</a><a href="https://github.com/{repo}">GitHub</a>'
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><a class="brand" href="index.html">{MARK}<span>ROTATIONAL<br>SEED FRACTALS</span></a><nav class="main-nav" aria-label="Main navigation">{nav}</nav><details class="mobile-menu"><summary>Menu</summary><nav aria-label="Mobile navigation">{nav}</nav></details></header>'''


def footer(repo: str) -> str:
    return f'''<footer class="site-footer"><div class="footer-top"><p>Rotational Seed Fractals<br>A mathematical and visual investigation by <a href="https://github.com/okwhynot-wtf">okwhynot-wtf</a>.</p><nav class="footer-links" aria-label="Footer"><a href="paper.html">Paper draft</a><a href="media.html">Media</a><a href="provenance.html">Provenance</a><a href="https://github.com/{repo}">Source repository</a></nav></div><div class="footer-bottom"><span>2026 · Candidate families · External mathematical review pending</span><span>Code &amp; data: MIT · Content: CC BY 4.0 · <a href="provenance.html">AI assistance disclosed</a></span></div></footer>'''


def page(title: str, body: str, slug: str, repo: str, url: str) -> str:
    canonical = url.rstrip('/') + '/' + ('index.html' if slug == 'index' else slug + '.html')
    title_full = 'Rotational Seed Fractals' if slug == 'index' else title + ' · Rotational Seed Fractals'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="dark"><meta name="theme-color" content="#080d10"><title>{html.escape(title_full)}</title><meta name="description" content="{html.escape(DESCRIPTION, quote=True)}"><link rel="canonical" href="{html.escape(canonical, quote=True)}"><meta property="og:title" content="{html.escape(title_full, quote=True)}"><meta property="og:description" content="{html.escape(DESCRIPTION, quote=True)}"><meta property="og:type" content="website"><meta property="og:image" content="{url.rstrip('/')}/assets/hero-poster.jpg"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css"><script>window.MathJax={{tex:{{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']],processEscapes:true}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script><script defer src="assets/site.js"></script></head><body>{header(repo, slug)}<main id="main">{body}</main>{footer(repo)}</body></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default='okwhynot-wtf/rotational-seed-fractals')
    parser.add_argument('--url', default='https://okwhynot-wtf.github.io/rotational-seed-fractals/')
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    assets = OUT / 'assets'
    assets.mkdir(exist_ok=True)
    shutil.copyfile(DOCS / 'theme.css', assets / 'site.css')
    shutil.copyfile(DOCS / 'site.js', assets / 'site.js')
    (assets / 'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="7" fill="#080d10"/><path d="M20 4 34 12v16l-14 8-14-8V12Z M20 4v32 M6 12l28 16 M34 12 6 28" fill="none" stroke="#85d6cc" stroke-width="1.4"/></svg>', encoding='utf-8')
    home = (DOCS / 'home.html').read_text(encoding='utf-8')
    (OUT / 'index.html').write_text(page('', home, 'index', args.repo, args.url), encoding='utf-8')
    for slug, label in PAGES:
        source = ROOT / 'research' / 'PAPER_DRAFT.md' if slug == 'paper' else DOCS / (slug + '.md')
        text = source.read_text(encoding='utf-8')
        title = next(line[2:].strip() for line in text.splitlines() if line.startswith('# '))
        content = render_markdown(text, args.repo)
        if slug == 'paper':
            content = content.replace('These local links should be replaced with repository links when a public version is prepared.', 'Source links below point to the working repository.')
        nav = ''.join(f'<a href="{s}.html"' + (' aria-current="page"' if s == slug else '') + f'>{l}</a>' for s, l in PAGES)
        sidebar = f'<aside class="doc-nav" aria-label="Research documentation"><p>Research notebook</p>{nav}<div class="source-nav"><p>Evidence</p><a href="https://github.com/{args.repo}/blob/main/research/INDEPENDENT_REVIEW.md">Internal review</a><a href="https://github.com/{args.repo}/blob/main/research/PRIOR_ART.md">Literature audit</a></div></aside>'
        origin = 'research/PAPER_DRAFT.md' if slug == 'paper' else 'docs/' + slug + '.md'
        meta = f'<div class="doc-meta">Working edition · 20 November 2026 · <a href="https://github.com/{args.repo}/blob/main/{origin}">View page source</a></div>'
        body = f'<div class="doc-shell">{sidebar}<article class="prose">{content}{meta}</article></div>'
        (OUT / (slug + '.html')).write_text(page(title, body, slug, args.repo, args.url), encoding='utf-8')
    (OUT / '.nojekyll').write_text('', encoding='utf-8')
    (OUT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: ' + args.url.rstrip('/') + '/sitemap.xml\n', encoding='utf-8')
    urls = [args.url.rstrip('/') + '/' + s + '.html' for s in ['index'] + [s for s, _ in PAGES]]
    (OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join('<url><loc>' + html.escape(u) + '</loc></url>' for u in urls) + '</urlset>', encoding='utf-8')
    print(f'Built {len(PAGES)+1} HTML pages in {OUT}; supplied media preserved.')


if __name__ == '__main__':
    main()
