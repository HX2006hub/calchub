# -*- coding: utf-8 -*-
"""Offline static audit of the generated CalcHub site. No network, no browser."""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parent.parent
errs, warns = [], []

htmls = sorted(ROOT.rglob('*.html'))
htmls = [h for h in htmls if '.git' not in h.parts]

def rel(p): return str(p.relative_to(ROOT)).replace('\\', '/')

for h in htmls:
    t = h.read_text(encoding='utf-8')
    # title / description / canonical / h1
    if len(re.findall(r'<title>.+?</title>', t, re.S)) != 1:
        errs.append('%s: title count != 1' % rel(h))
    if not re.search(r'<meta name="description" content="[^"]+"', t):
        errs.append('%s: missing meta description' % rel(h))
    if not re.search(r'<link rel="canonical" href="https://[^"]+"', t):
        errs.append('%s: missing canonical' % rel(h))
    h1 = re.findall(r'<h1[^>]*>(.*?)</h1>', t, re.S)
    if len(h1) != 1:
        errs.append('%s: H1 count = %d' % (rel(h), len(h1)))
    if not re.search(r'<html lang="en">', t):
        errs.append('%s: html lang not en' % rel(h))
    # OG tags
    for p in ['og:title', 'og:description', 'og:url', 'og:type']:
        if 'property="%s"' % p not in t:
            warns.append('%s: missing og:%s' % (rel(h), p))
    # Chinese chars (English-only) — allow only in code/attr? simply flag any CJK
    if re.search(r'[\u4e00-\u9fff]', t):
        errs.append('%s: contains CJK characters (English-only violation)' % rel(h))
    # placeholder text
    for token in ['lorem ipsum dolor sit amet', 'PENDING', 'TODO', 'FIXME', 'example.com']:
        # lorem ipsum is legitimate on the generator tool page only
        if token == 'lorem ipsum dolor sit amet' and 'lorem-ipsum' in rel(h):
            continue
        # example.com is a legitimate placeholder value in the QR tool's sample input
        if token == 'example.com' and 'qr-code-generator' in rel(h):
            continue
        if re.search(r'\b' + re.escape(token) + r'\b', t, re.I):
            warns.append('%s: contains %s' % (rel(h), token))
    # internal links resolve
    for m in re.finditer(r'href="(/(?:[^"#]*))(?:\#[^"]*)?"', t):
        target = (ROOT / m.group(1).lstrip('/')).resolve()
        if not target.exists():
            # directory index
            if not (target / 'index.html').exists():
                errs.append('%s: broken link %s' % (rel(h), m.group(1)))
    # script/link src resolve
    for m in re.finditer(r'(?:src|href)="(/(?:assets|favicon)[^"]*)"', t):
        target = (ROOT / m.group(1).lstrip('/')).resolve()
        if not target.exists():
            errs.append('%s: missing asset %s' % (rel(h), m.group(1)))
    # external script/style (should be none) — ignore canonical/OG/alternate metadata links
    for m in re.finditer(r'<(script|link)\b[^>]*>', t):
        tag = m.group(0)
        if re.search(r'rel="(canonical|alternate)"', tag):
            continue
        mm = re.search(r'(?:src|href)="(https?://[^"]+)"', tag)
        if mm:
            errs.append('%s: external resource %s' % (rel(h), mm.group(1)))
    # forms labels: each input with id should have a matching label or aria-label
    for m in re.finditer(r'<input[^>]*\bid="([^"]+)"[^>]*>', t):
        iid = m.group(1)
        if ('for="%s"' % iid) not in t and 'aria-label' not in m.group(0) and 'type="hidden"' not in m.group(0):
            warns.append('%s: input #%s without label' % (rel(h), iid))

# 30 tool pages exist
tools_dir = ROOT / 'tools'
tool_pages = [d for d in tools_dir.iterdir() if d.is_dir() and (d / 'index.html').exists()]
if len(tool_pages) != 30:
    errs.append('tool page count = %d (expected 30)' % len(tool_pages))

# sitemap / robots
sm = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
urls = re.findall(r'<loc>(.*?)</loc>', sm)
if len(urls) != 44:
    warns.append('sitemap url count = %d (expected 44)' % len(urls))
for h in htmls:
    if h.name == '404.html':  # 404 should not be indexed
        continue
    r = rel(h).replace('index.html', '').rstrip('/')
    loc = 'https://calchub.tools/' + r
    if loc + '/' not in sm and loc not in sm:
        errs.append('sitemap missing %s' % rel(h))
rb = (ROOT / 'robots.txt').read_text(encoding='utf-8')
if 'Sitemap:' not in rb:
    errs.append('robots.txt missing Sitemap directive')

# structured data JSON-LD parses
for h in htmls:
    t = h.read_text(encoding='utf-8')
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            import json
            json.loads(m.group(1))
        except Exception as e:
            errs.append('%s: invalid JSON-LD: %s' % (rel(h), e))

print('HTML files: %d | tool pages: %d | sitemap URLs: %d' % (len(htmls), len(tool_pages), len(urls)))
if warns:
    print('\nWARNINGS (%d):' % len(warns))
    for w in warns[:40]: print(' -', w)
if errs:
    print('\nERRORS (%d):' % len(errs))
    for e in errs[:60]: print(' -', e)
    sys.exit(1)
print('\nAll static SEO/link checks passed.')
