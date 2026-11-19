# -*- coding: utf-8 -*-
"""
CalcHub static site generator.

Builds every page from the tool registries in _data/:
  - 30 tool pages at /tools/<slug>/index.html
  - home, /tools/ directory, 6 category pages, search, 404
  - policy pages: about, contact, privacy-policy, terms, disclaimer
  - SEO: sitemap.xml, robots.txt, tools-data.js, favicon.svg
Run: python3 _scripts/build.py
Output root: project root (calchub/)
"""
import os
import json
import sys
import html as html_mod

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '_data'))

from tools_text import TEXT_TOOLS
from tools_image import IMAGE_TOOLS
from tools_calc import CALC_TOOLS
from tools_gen import GENERATOR_TOOLS
from tools_time_count import TIME_TOOLS, COUNTER_TOOLS

TOOLS = TEXT_TOOLS + IMAGE_TOOLS + CALC_TOOLS + GENERATOR_TOOLS + TIME_TOOLS + COUNTER_TOOLS
BY_SLUG = {t['slug']: t for t in TOOLS}

# ---------------- Site constants (PENDING: replace before go-live) ----------------
SITE_URL = 'https://calchub.tools'           # canonical origin (PENDING)
SITE_NAME = 'CalcHub'
SITE_TAGLINE = 'Free Tools for Everyday Tasks'
CONTACT_EMAIL = 'hello@calchub.tools'        # placeholder inbox (PENDING)

CATEGORIES = [
    {'slug': 'text-tools',     'cat': 'text',  'name': 'Text Tools',            'icon': '✎', 'desc': 'Word counters, character counters, case converters, duplicate-line remover and lorem ipsum generator.'},
    {'slug': 'image-tools',    'cat': 'image', 'name': 'Image & File Tools',     'icon': '🖼', 'desc': 'Compress, resize, convert, crop images and generate favicons entirely in your browser.'},
    {'slug': 'calculators',    'cat': 'calc',  'name': 'Calculators',            'icon': '≡', 'desc': 'Percentage, age, date difference, unit, BMI and discount calculators with accurate formulas.'},
    {'slug': 'generators',     'cat': 'gen',   'name': 'Generators & Converters','icon': '⚙', 'desc': 'Secure passwords, QR codes, UUIDs, random data, name picking and JSON formatting.'},
    {'slug': 'time-tools',     'cat': 'time',  'name': 'Time & Productivity',    'icon': '⏱', 'desc': 'Countdown timer, stopwatch, Pomodoro timer and time zone converter with accurate timing.'},
    {'slug': 'counters',       'cat': 'count', 'name': 'Counters & Trackers',    'icon': '⊕', 'desc': 'Simple, fast counters for tallying anything — clicks, attendees, reps and more.'},
]
CAT_BY_ID = {c['cat']: c for c in CATEGORIES}

NAV_LINKS = [
    ('/', 'Home'),
    ('/tools/', 'Tools'),
    ('/about/', 'About'),
    ('/contact/', 'Contact'),
]

POPULAR_SLUGS = [
    'word-counter', 'image-compressor', 'password-generator', 'qr-code-generator',
    'percentage-calculator', 'age-calculator', 'countdown-timer', 'json-formatter'
]

# ---------------- Helpers ----------------
def esc(s):
    return html_mod.escape(s, quote=True)

def attr_esc(s):
    return html_mod.escape(s, quote=True) if isinstance(s, str) else s

def icon_svg():
    return ('<svg width="30" height="30" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            '<rect width="40" height="40" rx="10" fill="#2563eb"/>'
            '<text x="20" y="26" font-family="Arial,sans-serif" font-size="17" font-weight="800" fill="#fff" text-anchor="middle">CH</text></svg>')

def logo_html(light=False):
    cls = 'footer-logo' if light else ''
    return ('<a class="logo" href="/" aria-label="CalcHub home">' + icon_svg() +
            '<span>Calc<span>Hub</span></span></a>')

def head_html(title, desc, canonical, extra_ld=None, noindex=False):
    ld = []
    if extra_ld:
        ld = list(extra_ld)
    ld_json = ''
    if ld:
        ld_json = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>'
    robots = '<meta name="robots" content="noindex, nofollow">' if noindex else ''
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n'
            '<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '<title>' + esc(title) + '</title>\n'
            '<meta name="description" content="' + attr_esc(desc) + '">\n'
            '<link rel="canonical" href="' + canonical + '">\n'
            + robots +
            '<meta property="og:type" content="website">\n'
            '<meta property="og:site_name" content="' + SITE_NAME + '">\n'
            '<meta property="og:title" content="' + esc(title) + '">\n'
            '<meta property="og:description" content="' + attr_esc(desc) + '">\n'
            '<meta property="og:url" content="' + canonical + '">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="twitter:title" content="' + esc(title) + '">\n'
            '<meta name="twitter:description" content="' + attr_esc(desc) + '">\n'
            '<link rel="icon" type="image/svg+xml" href="/favicon.svg">\n'
            '<link rel="stylesheet" href="/assets/css/styles.css">\n'
            + ld_json +
            '</head>\n<body>\n')

def header_html(active=''):
    items = ''
    for href, label in NAV_LINKS:
        cls = ' class="active"' if active == href else ''
        items += '<li><a href="' + href + '"' + cls + '>' + label + '</a></li>'
    return ('<a class="skip-link" href="#main">Skip to content</a>\n'
            '<header class="site-header">\n  <div class="container header-inner">\n'
            + logo_html() +
            '<nav class="main-nav" aria-label="Main navigation"><ul>' + items + '</ul></nav>\n'
            '<div class="header-actions">\n'
            '<a class="icon-btn" href="/search/" aria-label="Search tools" title="Search tools">'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg></a>\n'
            '<button class="menu-toggle" aria-expanded="false" aria-label="Toggle menu"><span></span><span></span><span></span></button>\n'
            '</div>\n  </div>\n</header>\n')

def footer_html(extra_scripts=''):
    cats = ''
    for c in CATEGORIES:
        cats += '<a href="/category/' + c['slug'] + '/">' + c['name'] + '</a>'
    return ('<footer class="site-footer">\n  <div class="container">\n'
            '    <div class="footer-grid">\n'
            '      <div class="footer-brand">\n' + logo_html(light=True) +
            '        <p>' + SITE_TAGLINE + '. Simple, fast and useful tools. No signup required. All tools run directly in your browser.</p>\n'
            '      </div>\n'
            '      <div class="footer-col"><h4>Tools</h4>' + cats +
            '        <a href="/tools/">All Tools</a>\n      </div>\n'
            '      <div class="footer-col"><h4>Company</h4>\n'
            '        <a href="/about/">About Us</a>\n'
            '        <a href="/contact/">Contact</a>\n'
            '        <a href="/disclaimer/">Disclaimer</a>\n'
            '      </div>\n'
            '      <div class="footer-col"><h4>Legal</h4>\n'
            '        <a href="/privacy-policy/">Privacy Policy</a>\n'
            '        <a href="/terms/">Terms of Use</a>\n'
            '      </div>\n'
            '    </div>\n'
            '    <div class="footer-bottom">\n'
            '      <span>&copy; <span data-year></span> ' + SITE_NAME + '. All rights reserved.</span>\n'
            '      <span>Tools run locally in your browser — your data stays on your device.</span>\n'
            '    </div>\n  </div>\n</footer>\n'
            + extra_scripts +
            '<script src="/assets/js/main.js" defer></script>\n'
            '<script src="/assets/js/tools.js" defer></script>\n'
            '<script src="/assets/js/tools-data.js" defer></script>\n'
            '</body>\n</html>\n')

def breadcrumb_html(items):
    # items: list of (text, href or None)
    out = '<nav aria-label="Breadcrumb"><ol class="breadcrumb">'
    for text, href in items:
        if href:
            out += '<li><a href="' + href + '">' + esc(text) + '</a></li>'
        else:
            out += '<li aria-current="page">' + esc(text) + '</li>'
    out += '</ol></nav>'
    return out

def tool_card(t, cat_name=None):
    return ('<a class="tool-card" href="/tools/' + t['slug'] + '/" data-search-item="'
            + t['slug'] + ' ' + t['name'].lower() + '">'
            '<span class="icon" aria-hidden="true">' + esc(t['icon']) + '</span>'
            '<h3>' + esc(t['name']) + '</h3>'
            '<p>' + esc(t['lede'][:110]) + '</p>'
            '<span class="go">Open tool →</span>'
            '</a>')

def cat_card(c, count):
    return ('<a class="cat-card" href="/category/' + c['slug'] + '/">'
            '<span class="cat-icon" aria-hidden="true">' + c['icon'] + '</span>'
            '<h3>' + esc(c['name']) + '</h3>'
            '<p>' + esc(c['desc']) + '</p>'
            '<span class="cat-count">' + str(count) + ' tool' + ('s' if count != 1 else '') + '</span>'
            '</a>')

# ---------------- Widget HTML per tool ----------------
def widget_html(t):
    s = t['slug']
    W = {
        'word-counter': '''
<div class="field">
  <label for="wc-input">Your text</label>
  <textarea id="wc-input" spellcheck="false" placeholder="Type or paste your text here…"></textarea>
  <div class="form-actions">
    <button type="button" class="btn btn-secondary" data-select="sample">Insert sample text</button>
    <button type="button" class="btn btn-ghost" data-select="clear">Clear</button>
  </div>
</div>
<div class="result-card">
  <div class="result-grid">
    <div class="result-item"><div class="ri-label">Words</div><div class="ri-value" data-out="words">0</div></div>
    <div class="result-item"><div class="ri-label">Characters</div><div class="ri-value" data-out="chars">0</div></div>
    <div class="result-item"><div class="ri-label">Characters (no spaces)</div><div class="ri-value" data-out="charsNoSpace">0</div></div>
    <div class="result-item"><div class="ri-label">Sentences</div><div class="ri-value" data-out="sent">0</div></div>
    <div class="result-item"><div class="ri-label">Paragraphs</div><div class="ri-value" data-out="para">0</div></div>
    <div class="result-item"><div class="ri-label">Reading time</div><div class="ri-value" data-out="read">—</div></div>
  </div>
</div>''',
        'character-counter': '''
<div class="field">
  <label for="cc-input">Your text</label>
  <textarea id="cc-input" spellcheck="false" placeholder="Type or paste your text here…"></textarea>
  <div class="form-actions">
    <button type="button" class="btn btn-ghost" data-clear>Clear</button>
  </div>
</div>
<div class="result-card">
  <div class="result-grid">
    <div class="result-item"><div class="ri-label">Total characters</div><div class="ri-value" data-out="total">0</div></div>
    <div class="result-item"><div class="ri-label">Without spaces</div><div class="ri-value" data-out="noSpace">0</div></div>
    <div class="result-item"><div class="ri-label">Letters</div><div class="ri-value" data-out="letters">0</div></div>
    <div class="result-item"><div class="ri-label">Digits</div><div class="ri-value" data-out="digits">0</div></div>
    <div class="result-item"><div class="ri-label">Punctuation &amp; symbols</div><div class="ri-value" data-out="punct">0</div></div>
    <div class="result-item"><div class="ri-label">Spaces &amp; newlines</div><div class="ri-value" data-out="spaces">0</div></div>
  </div>
</div>''',
        'reading-time': '''
<div class="field">
  <label for="rt-input">Your text</label>
  <textarea id="rt-input" spellcheck="false" placeholder="Type or paste your text here…"></textarea>
</div>
<div class="field">
  <label for="rt-wpm">Reading speed <span class="field-hint">(words per minute — 225 is the average for adults)</span></label>
  <input id="rt-wpm" type="number" min="60" max="600" step="5" value="225">
</div>
<div class="result-card">
  <div class="result-grid">
    <div class="result-item"><div class="ri-label">Words</div><div class="ri-value" data-out="words">0</div></div>
    <div class="result-item"><div class="ri-label">Estimated reading time</div><div class="ri-value" data-out="read">—</div></div>
    <div class="result-item"><div class="ri-label">Minutes</div><div class="ri-value" data-out="mins">0</div></div>
    <div class="result-item"><div class="ri-label">Seconds (remainder)</div><div class="ri-value" data-out="secs">0</div></div>
    <div class="result-item"><div class="ri-label">Speaking time (~130 wpm)</div><div class="ri-value" data-out="speak">—</div></div>
  </div>
</div>''',
        'text-case-converter': '''
<div class="field">
  <label for="tc-input">Your text</label>
  <textarea id="tc-input" spellcheck="false" placeholder="Type or paste your text here…"></textarea>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-secondary" data-case="upper">UPPERCASE</button>
  <button type="button" class="btn btn-secondary" data-case="lower">lowercase</button>
  <button type="button" class="btn btn-secondary" data-case="title">Title Case</button>
  <button type="button" class="btn btn-secondary" data-case="sentence">Sentence case</button>
  <button type="button" class="btn btn-secondary" data-case="camel">camelCase</button>
  <button type="button" class="btn btn-secondary" data-case="alternating">aLtErNaTiNg</button>
  <button type="button" class="btn btn-ghost" data-clear>Clear</button>
</div>
<div class="field" style="margin-top:18px">
  <label for="tc-output">Converted text</label>
  <textarea id="tc-output" class="output-area" readonly spellcheck="false" data-output placeholder="Result appears here"></textarea>
</div>
<div class="status-msg"></div>''',
        'remove-duplicate-lines': '''
<div class="field">
  <label for="dl-input">Your lines <span class="field-hint">(one item per line)</span></label>
  <textarea id="dl-input" spellcheck="false" placeholder="apple&#10;Banana&#10;apple&#10;cherry"></textarea>
</div>
<div class="field">
  <label class="checkline"><input type="checkbox" data-ignore-case> Ignore case (Apple = apple)</label>
  <label class="checkline"><input type="checkbox" data-trim> Trim whitespace before comparing</label>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-run>Remove duplicates</button>
</div>
<div class="result-card">
  <div class="result-sub" data-count>Ready — paste lines to see unique lines.</div>
  <textarea class="output-area" data-output readonly spellcheck="false" placeholder="Unique lines will appear here"></textarea>
</div>''',
        'lorem-ipsum-generator': '''
<div class="form-row">
  <div class="field">
    <label for="li-paras">Paragraphs</label>
    <input id="li-paras" type="number" min="1" max="20" value="3" data-paras>
  </div>
  <div class="field">
    <label for="li-words">Words <span class="field-hint">(0 = use paragraphs)</span></label>
    <input id="li-words" type="number" min="0" max="1000" value="0" data-words>
  </div>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-generate>Generate</button>
</div>
<div class="field" style="margin-top:18px">
  <label for="li-output">Generated Lorem Ipsum</label>
  <textarea id="li-output" class="output-area" readonly spellcheck="false" data-output></textarea>
  <button type="button" class="btn btn-secondary" data-copy="#li-output">Copy to clipboard</button>
</div>''',
        'image-compressor': '''
<div class="field">
  <div class="dropzone" tabindex="0" role="button" aria-label="Upload image to compress">
    <input type="file" accept="image/*">
    <p><strong>Drop an image here</strong> or click to browse</p>
    <p style="font-size:.85rem">JPG, PNG or WebP — processed locally, never uploaded</p>
  </div>
</div>
<div class="form-row">
  <div class="field">
    <label for="ic-scale">Scale <span class="field-hint" data-scale-val>100%</span></label>
    <input id="ic-scale" type="range" min="10" max="100" step="5" value="80" data-scale>
  </div>
  <div class="field">
    <label for="ic-quality">JPEG quality <span class="field-hint" data-quality-val>80%</span></label>
    <input id="ic-quality" type="range" min="10" max="100" step="5" value="80" data-quality>
  </div>
</div>
<div class="status-msg"></div>
<div style="margin-top:16px">
  <img data-preview alt="Compressed image preview" style="max-width:100%;border:1px solid var(--border);border-radius:8px">
  <p class="result-sub" data-info></p>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-download>Download compressed JPG</button>
</div>
<p class="result-sub" style="margin-top:8px">Output is re-encoded as JPEG. Transparent PNGs lose their alpha channel when compressed to JPEG.</p>''',
        'image-resizer': '''
<div class="field">
  <div class="dropzone" tabindex="0" role="button" aria-label="Upload image to resize">
    <input type="file" accept="image/*">
    <p><strong>Drop an image here</strong> or click to browse</p>
    <p style="font-size:.85rem">JPG, PNG or WebP — processed locally, never uploaded</p>
  </div>
</div>
<div class="form-row">
  <div class="field">
    <label for="ir-width">Width (px)</label>
    <input id="ir-width" type="number" min="1" max="8000" value="800" data-width>
  </div>
  <div class="field">
    <label for="ir-height">Height (px)</label>
    <input id="ir-height" type="number" min="1" max="8000" value="600" data-height>
  </div>
  <div class="field" style="display:flex;align-items:center">
    <label class="checkline"><input type="checkbox" data-lock checked> Lock aspect ratio</label>
  </div>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-apply>Apply resize</button>
</div>
<div class="status-msg"></div>
<div style="margin-top:16px">
  <img data-preview alt="Resized image preview" style="max-width:100%;border:1px solid var(--border);border-radius:8px">
  <p class="result-sub" data-info></p>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-download>Download PNG</button>
</div>''',
        'jpg-to-png': '''
<div class="field">
  <div class="dropzone" tabindex="0" role="button" aria-label="Upload JPG image">
    <input type="file" accept="image/jpeg,image/jpg">
    <p><strong>Drop a JPG here</strong> or click to browse</p>
    <p style="font-size:.85rem">Converted locally — never uploaded</p>
  </div>
</div>
<div class="status-msg"></div>
<div style="margin-top:16px">
  <img data-preview alt="Converted PNG preview" style="max-width:100%;border:1px solid var(--border);border-radius:8px">
  <p class="result-sub" data-info></p>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-download>Download PNG</button>
</div>
<p class="result-sub" style="margin-top:8px">JPG has no alpha channel. If the source has transparent areas, they will appear white in the PNG.</p>''',
        'png-to-webp': '''
<div class="field">
  <div class="dropzone" tabindex="0" role="button" aria-label="Upload PNG image">
    <input type="file" accept="image/png,image/webp,image/jpeg">
    <p><strong>Drop a PNG here</strong> or click to browse</p>
    <p style="font-size:.85rem">Converted locally — never uploaded</p>
  </div>
</div>
<div class="status-msg"></div>
<div style="margin-top:16px">
  <img data-preview alt="Converted WebP preview" style="max-width:100%;border:1px solid var(--border);border-radius:8px">
  <p class="result-sub" data-info></p>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-download>Download WebP</button>
</div>''',
        'image-cropper': '''
<div class="field">
  <div class="dropzone" tabindex="0" role="button" aria-label="Upload image to crop">
    <input type="file" accept="image/*">
    <p><strong>Drop an image here</strong> or click to browse</p>
    <p style="font-size:.85rem">Cropped locally — never uploaded</p>
  </div>
</div>
<div class="field">
  <label for="cr-aspect">Aspect ratio</label>
  <select id="cr-aspect" data-aspect>
    <option value="free">Free (original)</option>
    <option value="1:1" selected>1:1 Square</option>
    <option value="4:3">4:3</option>
    <option value="3:2">3:2</option>
    <option value="16:9">16:9</option>
    <option value="9:16">9:16</option>
  </select>
</div>
<div class="status-msg"></div>
<div style="margin-top:16px">
  <img data-preview alt="Cropped image preview" style="max-width:100%;border:1px solid var(--border);border-radius:8px">
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-download>Download cropped PNG</button>
</div>''',
        'favicon-generator': '''
<div class="field">
  <div class="dropzone" tabindex="0" role="button" aria-label="Upload image for favicon">
    <input type="file" accept="image/*">
    <p><strong>Drop an image here</strong> to use it, or type a letter below</p>
    <p style="font-size:.85rem">Generated locally — never uploaded</p>
  </div>
</div>
<div class="form-row">
  <div class="field">
    <label for="fg-text">Letter or emoji</label>
    <input id="fg-text" type="text" maxlength="2" value="C" data-text>
  </div>
  <div class="field">
    <label for="fg-bg">Background color</label>
    <input id="fg-bg" type="color" value="#2563eb" data-bg>
  </div>
  <div class="field">
    <label for="fg-fg">Foreground color</label>
    <input id="fg-fg" type="color" value="#ffffff" data-fg>
  </div>
  <div class="field">
    <label for="fg-size">Size</label>
    <select id="fg-size" data-size>
      <option value="32" selected>32 × 32</option>
      <option value="48">48 × 48</option>
      <option value="64">64 × 64</option>
      <option value="128">128 × 128</option>
    </select>
  </div>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-render>Render favicon</button>
</div>
<div class="status-msg"></div>
<div style="margin-top:16px;text-align:center">
  <img data-preview alt="Favicon preview" style="border:1px solid var(--border);border-radius:8px">
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-download>Download PNG</button>
</div>''',
        'percentage-calculator': '''
<div class="field">
  <label for="pc-mode">Calculation type</label>
  <select id="pc-mode" data-mode>
    <option value="percent-of">What is X% of Y?</option>
    <option value="is-what">X is what percent of Y?</option>
    <option value="increase">Percentage increase (from X to Y)</option>
    <option value="decrease">Percentage decrease (from X to Y)</option>
  </select>
</div>
<div class="form-row">
  <div class="field">
    <label for="pc-a" data-label-a>Percentage (X)</label>
    <input id="pc-a" type="number" step="any" value="15" data-a>
  </div>
  <div class="field">
    <label for="pc-b" data-label-b>Whole number (Y)</label>
    <input id="pc-b" type="number" step="any" value="240" data-b>
  </div>
</div>
<div class="result-card">
  <div class="result-value" data-out1>—</div>
  <div class="result-sub" data-out2>Enter values to calculate.</div>
  <div class="result-sub" data-out3></div>
</div>''',
        'age-calculator': '''
<div class="form-row">
  <div class="field">
    <label for="ac-birth">Birth date</label>
    <input id="ac-birth" type="date" data-birth>
  </div>
  <div class="field">
    <label for="ac-target">Target date <span class="field-hint">(defaults to today)</span></label>
    <input id="ac-target" type="date" data-target>
  </div>
</div>
<div class="result-card">
  <div class="result-grid">
    <div class="result-item"><div class="ri-label">Age</div><div class="ri-value"><span data-out="y">—</span>y <span data-out="m">—</span>m <span data-out="d">—</span>d</div></div>
    <div class="result-item"><div class="ri-label">Total months</div><div class="ri-value" data-out="totalM">—</div></div>
    <div class="result-item"><div class="ri-label">Total weeks</div><div class="ri-value" data-out="totalW">—</div></div>
    <div class="result-item"><div class="ri-label">Total days</div><div class="ri-value" data-out="totalD">—</div></div>
  </div>
</div>''',
        'date-difference': '''
<div class="form-row">
  <div class="field">
    <label for="dd-start">Start date</label>
    <input id="dd-start" type="date" data-start>
  </div>
  <div class="field">
    <label for="dd-end">End date</label>
    <input id="dd-end" type="date" data-end>
  </div>
  <div class="field" style="display:flex;align-items:center">
    <label class="checkline" for="dd-include"><input id="dd-include" type="checkbox" data-include> Include end date</label>
  </div>
</div>
<div class="result-card">
  <div class="result-grid">
    <div class="result-item"><div class="ri-label">Days</div><div class="ri-value" data-out="d">—</div></div>
    <div class="result-item"><div class="ri-label">Weeks</div><div class="ri-value" data-out="w">—</div></div>
    <div class="result-item"><div class="ri-label">Months (approx.)</div><div class="ri-value" data-out="m">—</div></div>
    <div class="result-item"><div class="ri-label">Years (approx.)</div><div class="ri-value" data-out="y">—</div></div>
  </div>
  <div class="result-sub" data-out="desc"></div>
</div>''',
        'unit-converter': '''
<div class="field">
  <label for="uc-cat">Category</label>
  <select id="uc-cat" data-category>
    <option value="length" selected>Length</option>
    <option value="mass">Mass / Weight</option>
    <option value="temperature">Temperature</option>
    <option value="speed">Speed</option>
    <option value="area">Area</option>
    <option value="volume">Volume</option>
  </select>
</div>
<div class="form-row">
  <div class="field">
    <label for="uc-from">From</label>
    <select id="uc-from" data-from></select>
  </div>
  <div class="field">
    <label for="uc-to">To</label>
    <select id="uc-to" data-to></select>
  </div>
  <div class="field">
    <label for="uc-value">Value</label>
    <input id="uc-value" type="number" step="any" value="1" data-value>
  </div>
</div>
<div class="result-card">
  <div class="result-value" data-result>—</div>
  <div class="result-sub" data-result-sub>Pick units and enter a value.</div>
</div>''',
        'bmi-calculator': '''
<div class="field">
  <label for="bmi-sys">Unit system</label>
  <select id="bmi-sys" data-system>
    <option value="metric" selected>Metric (cm / kg)</option>
    <option value="imperial">Imperial (ft / in / lb)</option>
  </select>
</div>
<div class="form-row">
  <div class="field" data-cm>
    <label for="bmi-h1">Height (cm)</label>
    <input id="bmi-h1" type="number" min="50" max="250" step="0.5" value="175" data-h1>
  </div>
  <div class="field" data-ft style="display:none">
    <label for="bmi-h1b" data-ft-label>Height (feet)</label>
    <input id="bmi-h1b" type="number" min="3" max="8" step="0.1" value="5.8" data-h1>
  </div>
  <div class="field" data-ft style="display:none">
    <label for="bmi-h2">Height (inches)</label>
    <input id="bmi-h2" type="number" min="0" max="11" step="1" value="10" data-h2>
  </div>
  <div class="field">
    <label for="bmi-w">Weight</label>
    <input id="bmi-w" type="number" min="1" max="500" step="0.1" value="70" data-weight>
  </div>
</div>
<div class="result-card">
  <div class="result-value" data-result>—</div>
  <div class="result-sub" data-result-sub>Enter your height and weight.</div>
</div>
<p class="result-sub" style="margin-top:10px">BMI is a screening measure, not a medical diagnosis. Consult a healthcare professional for any health decision.</p>''',
        'discount-calculator': '''
<div class="form-row">
  <div class="field">
    <label for="dc-price">Original price ($)</label>
    <input id="dc-price" type="number" min="0" step="0.01" value="120" data-price>
  </div>
  <div class="field">
    <label for="dc-discount">Discount (%)</label>
    <input id="dc-discount" type="number" min="0" max="100" step="0.5" value="25" data-discount>
  </div>
  <div class="field" style="display:flex;align-items:center">
    <label class="checkline" for="dc-tax"><input id="dc-tax" type="checkbox" data-use-tax> Add sales tax</label>
  </div>
</div>
<div class="field" data-tax-field style="display:none">
  <label for="dc-taxrate">Tax rate (%)</label>
  <input id="dc-taxrate" type="number" min="0" max="40" step="0.1" value="7" data-tax>
</div>
<div class="result-card">
  <div class="result-value" data-final>—</div>
  <div class="result-sub" data-saved>Enter a price and discount.</div>
  <div class="result-sub" data-detail></div>
</div>''',
        'password-generator': '''
<div class="field">
  <label for="pg-len">Length <span class="field-hint" data-length-val>16</span></label>
  <input id="pg-len" type="range" min="4" max="64" value="16" data-length>
</div>
<div class="field">
  <label class="checkline"><input type="checkbox" data-upper checked> Uppercase (A–Z)</label>
  <label class="checkline"><input type="checkbox" data-lower checked> Lowercase (a–z)</label>
  <label class="checkline"><input type="checkbox" data-nums checked> Numbers (0–9)</label>
  <label class="checkline"><input type="checkbox" data-syms checked> Symbols (!@#$…)</label>
</div>
<div class="field">
  <label for="pg-output">Generated password</label>
  <textarea id="pg-output" class="output-area resize-none" readonly spellcheck="false" data-output autocomplete="off" autocapitalize="off"></textarea>
</div>
<div class="result-sub" data-strength></div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-generate>Generate new</button>
  <button type="button" class="btn btn-secondary" data-copy>Copy password</button>
</div>''',
        'qr-code-generator': '''
<div class="field">
  <label for="qr-text">Text or URL</label>
  <input id="qr-text" type="text" placeholder="https://example.com" data-text value="https://example.com">
</div>
<div class="field">
  <label for="qr-size">Output size</label>
  <select id="qr-size" data-size>
    <option value="256" selected>256 × 256</option>
    <option value="512">512 × 512</option>
    <option value="1024">1024 × 1024</option>
  </select>
</div>
<div class="status-msg"></div>
<div style="margin-top:16px;text-align:center">
  <canvas data-canvas style="max-width:100%;border:1px solid var(--border);border-radius:8px"></canvas>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-download>Download PNG</button>
</div>''',
        'random-number-generator': '''
<div class="form-row">
  <div class="field">
    <label for="rn-min">Minimum</label>
    <input id="rn-min" type="number" step="any" value="1" data-min>
  </div>
  <div class="field">
    <label for="rn-max">Maximum</label>
    <input id="rn-max" type="number" step="any" value="100" data-max>
  </div>
  <div class="field">
    <label for="rn-count">How many</label>
    <input id="rn-count" type="number" min="1" max="1000" value="5" data-count>
  </div>
  <div class="field">
    <label for="rn-dec">Decimals</label>
    <select id="rn-dec" data-decimals>
      <option value="0" selected>0 (integers)</option>
      <option value="1">1</option>
      <option value="2">2</option>
      <option value="3">3</option>
    </select>
  </div>
</div>
<div class="field">
  <label class="checkline"><input type="checkbox" data-unique> Unique numbers only (integers)</label>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-generate>Generate</button>
</div>
<div class="field" style="margin-top:18px">
  <label for="rn-output">Result</label>
  <textarea id="rn-output" class="output-area resize-none" readonly spellcheck="false" data-output></textarea>
</div>''',
        'random-name-picker': '''
<div class="field">
  <label for="np-names">Names <span class="field-hint">(one per line)</span></label>
  <textarea id="np-names" spellcheck="false" placeholder="Alice&#10;Bob&#10;Charlie"></textarea>
</div>
<div class="field">
  <label class="checkline"><input type="checkbox" data-remove> Remove picked name (no repeats)</label>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-pick>Pick a name</button>
  <button type="button" class="btn btn-secondary" data-reset>Reset history</button>
</div>
<div class="result-card">
  <div class="ri-label">Winner</div>
  <div class="result-value" data-result>—</div>
  <div class="result-sub" style="margin-top:12px">Picked history</div>
  <ul data-history style="list-style:none;margin-top:8px;display:flex;flex-direction:column;gap:4px"></ul>
</div>''',
        'uuid-generator': '''
<div class="field">
  <label for="ug-count">How many UUIDs (1–20)</label>
  <input id="ug-count" type="number" min="1" max="20" value="5" data-count>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-generate>Generate UUIDs</button>
</div>
<div class="field" style="margin-top:18px">
  <label for="ug-output">Result</label>
  <textarea id="ug-output" class="output-area" readonly spellcheck="false" data-output></textarea>
  <button type="button" class="btn btn-secondary" data-copy="#ug-output">Copy all</button>
</div>''',
        'json-formatter': '''
<div class="field">
  <label for="jf-input">JSON input</label>
  <textarea id="jf-input" spellcheck="false" data-input placeholder='{"name":"CalcHub","tools":30}'></textarea>
</div>
<div class="form-row">
  <div class="field">
    <label for="jf-indent">Indentation</label>
    <select id="jf-indent" data-indent>
      <option value="2" selected>2 spaces</option>
      <option value="4">4 spaces</option>
      <option value="tab">Tab</option>
      <option value="min">Minified</option>
    </select>
  </div>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-format>Format / Minify</button>
  <button type="button" class="btn btn-secondary" data-validate>Validate</button>
  <button type="button" class="btn btn-ghost" data-clear>Clear</button>
</div>
<div class="status-msg"></div>
<div class="field" style="margin-top:18px">
  <label for="jf-output">Output</label>
  <textarea id="jf-output" class="output-area" readonly spellcheck="false" data-output></textarea>
  <button type="button" class="btn btn-secondary" data-copy="#jf-output">Copy output</button>
</div>''',
        'countdown-timer': '''
<div class="form-row">
  <div class="field">
    <label for="ct-hh">Hours</label>
    <input id="ct-hh" type="number" min="0" max="99" value="0" data-hh>
  </div>
  <div class="field">
    <label for="ct-mm">Minutes</label>
    <input id="ct-mm" type="number" min="0" max="59" value="5" data-mm>
  </div>
  <div class="field">
    <label for="ct-ss">Seconds</label>
    <input id="ct-ss" type="number" min="0" max="59" value="0" data-ss>
  </div>
</div>
<div class="timer-display" data-display>00:00:00</div>
<div class="form-actions" style="justify-content:center">
  <button type="button" class="btn btn-primary" data-start>Start</button>
  <button type="button" class="btn btn-secondary" data-pause disabled>Pause</button>
  <button type="button" class="btn btn-ghost" data-reset>Reset</button>
</div>
<div class="status-msg"></div>
<p class="result-sub" style="text-align:center;margin-top:10px">Timestamp-based counting stays accurate even when the tab is in the background.</p>''',
        'stopwatch': '''
<div class="timer-display" data-display>00:00:00.00</div>
<div class="form-actions" style="justify-content:center">
  <button type="button" class="btn btn-primary" data-start>Start</button>
  <button type="button" class="btn btn-secondary" data-pause disabled>Stop</button>
  <button type="button" class="btn btn-ghost" data-reset>Reset</button>
</div>
<div class="status-msg"></div>
<p class="result-sub" style="text-align:center;margin-top:10px">Uses high-resolution timestamps, so it stays correct when you switch tabs.</p>''',
        'pomodoro-timer': '''
<div class="form-row">
  <div class="field">
    <label for="po-focus">Focus (minutes)</label>
    <input id="po-focus" type="number" min="1" max="120" value="25" data-focus>
  </div>
  <div class="field">
    <label for="po-short">Short break</label>
    <input id="po-short" type="number" min="1" max="60" value="5" data-short>
  </div>
  <div class="field">
    <label for="po-long">Long break</label>
    <input id="po-long" type="number" min="1" max="90" value="15" data-long>
  </div>
</div>
<div class="result-sub" style="text-align:center" data-phase>Focus</div>
<div class="timer-display" data-display>25:00</div>
<div class="result-sub" style="text-align:center;margin-bottom:8px" data-cycles>Completed focus sessions: 0</div>
<div class="form-actions" style="justify-content:center">
  <button type="button" class="btn btn-primary" data-start>Start</button>
  <button type="button" class="btn btn-secondary" data-pause disabled>Pause</button>
  <button type="button" class="btn btn-secondary" data-skip>Skip</button>
  <button type="button" class="btn btn-ghost" data-reset>Reset</button>
</div>
<div class="status-msg"></div>''',
        'time-zone-converter': '''
<div class="form-row">
  <div class="field">
    <label for="tz-source">From time zone</label>
    <select id="tz-source" data-source-tz></select>
  </div>
  <div class="field">
    <label for="tz-dt">Date &amp; time</label>
    <input id="tz-dt" type="datetime-local" data-datetime>
  </div>
  <div class="field">
    <label for="tz-target">To time zone</label>
    <select id="tz-target" data-target-tz></select>
  </div>
</div>
<div class="result-card">
  <div class="result-value" data-result>—</div>
  <div class="result-sub" data-result-sub>Pick zones and a time.</div>
</div>
<p class="result-sub" style="margin-top:10px">Daylight saving is handled with the browser's IANA time zone data — not a fixed offset.</p>''',
        'online-counter': '''
<div class="big-number" data-display>0</div>
<div class="form-actions" style="justify-content:center">
  <button type="button" class="btn btn-primary" data-plus>+ Add</button>
  <button type="button" class="btn btn-secondary" data-minus>− Subtract</button>
  <button type="button" class="btn btn-ghost" data-reset>Reset</button>
</div>
<div class="form-row" style="margin-top:20px">
  <div class="field">
    <label for="oc-step">Step size</label>
    <input id="oc-step" type="number" min="1" max="1000" value="1" data-step>
  </div>
</div>
<div class="field">
  <label class="checkline"><input type="checkbox" data-persist> Keep count after refresh (localStorage)</label>
</div>
<p class="result-sub" style="margin-top:8px">Tip: with the buttons focused, press <code>+</code>, <code>−</code> or <code>R</code> to count.</p>''',
        'click-counter': '''
<div class="big-number" data-display>0</div>
<div style="text-align:center;margin:14px 0">
  <button type="button" class="btn btn-primary" data-bigbtn style="padding:22px 46px;font-size:1.2rem;border-radius:14px">Click me!</button>
</div>
<div style="text-align:center">
  <button type="button" class="btn btn-ghost" data-reset>Reset</button>
</div>
<div class="field" style="margin-top:20px;max-width:420px;margin-left:auto;margin-right:auto">
  <label class="checkline"><input type="checkbox" data-persist> Keep count after refresh (localStorage)</label>
</div>''',
    }
    return '<div class="widget" data-tool="' + s + '">' + W[s] + '</div>'

# ---------------- Prose sections ----------------
def prose_html(t):
    howto = '<div class="prose"><h2>How to Use</h2><ol>' + ''.join('<li>' + esc(x) + '</li>' for x in t['howto']) + '</ol>'
    ex = '<h2>Practical Examples</h2><ul>' + ''.join('<li>' + esc(x) + '</li>' for x in t['examples']) + '</ul>'
    feats = '<h2>Key Features</h2><ul>' + ''.join('<li>' + esc(x) + '</li>' for x in t['features']) + '</ul>'
    priv = '<div class="privacy-note"><strong>Privacy:</strong> ' + esc(t['privacy']) + '</div>'
    faq = '<h2>Frequently Asked Questions</h2>'
    for item in t['faq']:
        faq += ('<div class="faq-item"><h3>' + esc(item['q']) + '</h3><p>' + esc(item['a']) + '</p></div>')
    return howto + ex + feats + priv + faq + '</div>'

def side_panel_html(t):
    cat = CAT_BY_ID[t['cat']]
    related = ''
    for slug in t['related'][:5]:
        rt = BY_SLUG.get(slug)
        if rt:
            related += '<li><a href="/tools/' + rt['slug'] + '/">' + esc(rt['name']) + '</a></li>'
    count = len([x for x in TOOLS if x['cat'] == cat['cat']])
    return ('<aside class="side-panel">'
            '<div class="side-box"><h3>Related Tools</h3><ul>' + related + '</ul></div>'
            '<div class="side-box"><h3>Category</h3><p style="font-size:.92rem;color:var(--text-secondary);margin-bottom:10px">' +
            esc(cat['name']) + ' (' + str(count) + ' tool' + ('s' if count != 1 else '') + ')</p>'
            '<a class="btn btn-secondary" href="/category/' + cat['slug'] + '/" style="width:100%">Browse category</a></div>'
            '<div class="side-box"><h3>All Tools</h3><p style="font-size:.88rem;color:var(--text-secondary)">Browse every CalcHub tool.</p>'
            '<a class="btn btn-secondary" href="/tools/" style="width:100%">All tools</a></div>'
            '</aside>')

def tool_ld(t, cat):
    return [
        {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
         'itemListElement': [
             {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE_URL + '/'},
             {'@type': 'ListItem', 'position': 2, 'name': 'Tools', 'item': SITE_URL + '/tools/'},
             {'@type': 'ListItem', 'position': 3, 'name': t['name'], 'item': SITE_URL + '/tools/' + t['slug'] + '/'}
         ]},
        {'@context': 'https://schema.org', '@type': 'FAQPage',
         'mainEntity': [{'@type': 'Question', 'name': i['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': i['a']}} for i in t['faq']]}
    ]

def extra_scripts_for(t):
    extra = ''
    if t['slug'] == 'qr-code-generator':
        extra += '<script src="/assets/vendor/qrcode-generator.min.js" defer></script>\n'
    return extra

def tool_page(t):
    cat = CAT_BY_ID[t['cat']]
    canonical = SITE_URL + '/tools/' + t['slug'] + '/'
    crumbs = breadcrumb_html([('Home', '/'), ('Tools', '/tools/'), (cat['name'], '/category/' + cat['slug'] + '/'), (t['name'], None)])
    body = (header_html('/tools/') +
            '<main id="main" class="tool-page"><div class="container">' +
            crumbs +
            '<div class="tool-page-head"><h1>' + esc(t['h1']) + '</h1>'
            '<p class="lead">' + esc(t['lede']) + '</p></div>'
            '<div class="tool-layout"><div>' +
            '<div class="tool-card-ui">' + widget_html(t) + '</div>' +
            prose_html(t) +
            '</div>' + side_panel_html(t) + '</div>'
            '</div></main>' + footer_html(extra_scripts_for(t)))
    return head_html(t['title'], t['desc'], canonical, tool_ld(t, cat)) + body

# ---------------- Home ----------------
def home_page():
    popular = [BY_SLUG[s] for s in POPULAR_SLUGS if s in BY_SLUG]
    popular_cards = ''.join(tool_card(t) for t in popular)
    cat_cards = ''.join(cat_card(c, len([x for x in TOOLS if x['cat'] == c['cat']])) for c in CATEGORIES)
    all_cards = ''.join(tool_card(t) for t in sorted(TOOLS, key=lambda x: x['name'].lower()))

    ld = [
        {'@context': 'https://schema.org', '@type': 'WebSite',
         'name': SITE_NAME, 'url': SITE_URL + '/',
         'potentialAction': {'@type': 'SearchAction', 'target': SITE_URL + '/search/?q={search_term_string}', 'query-input': 'required name=search_term_string'}},
        {'@context': 'https://schema.org', '@type': 'Organization', 'name': SITE_NAME, 'url': SITE_URL + '/'}
    ]
    body = (header_html('/') +
            '<main id="main">'
            '<section class="hero"><div class="container hero-inner">'
            '<h1>Free Tools for Everyday Tasks</h1>'
            '<p>Simple, fast and useful tools. No signup required. Every tool runs in your browser — your text, files and numbers never leave your device.</p>'
            '<div class="search-box">'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>'
            '<input id="home-search" type="text" placeholder="Search 30 tools…" aria-label="Search tools">'
            '<button type="button">Search</button></div>'
            '</div></section>'

            '<section class="section"><div class="container">'
            '<div class="section-head"><div><h2>Popular Tools</h2><p>The tools people reach for most.</p></div></div>'
            '<div class="tool-grid" id="home-tool-list">' + popular_cards + '</div>'
            '</div></section>'

            '<section class="section" style="background:var(--bg-alt)"><div class="container">'
            '<div class="section-head"><div><h2>Tool Categories</h2><p>Six collections that cover everyday tasks.</p></div></div>'
            '<div class="cat-grid">' + cat_cards + '</div>'
            '</div></section>'

            '<section class="section"><div class="container">'
            '<div class="section-head"><div><h2>All Tools</h2><p>Every CalcHub tool, ready to use.</p></div></div>'
            '<div class="tool-grid">' + all_cards + '</div>'
            '</div></section>'

            '<section class="section" style="background:var(--bg-alt)"><div class="container" style="max-width:760px">'
            '<div class="prose" style="max-width:none">'
            '<h2 style="margin-top:0">Why CalcHub?</h2>'
            '<p>CalcHub is a collection of free online tools for everyday tasks — writing, images, calculations, generators, time management and counting. Everything is built as a lightweight static site: no accounts, no plugins, no waiting, no uploads.</p>'
            '<p>Because tools run directly in your browser, your content stays private and the pages stay fast. We keep the interface simple and the descriptions honest. Where a tool involves an estimate — reading time, BMI, approximate month counts — we say so on the page.</p>'
            '<p><a href="/about/">Learn more about CalcHub</a> or <a href="/tools/">browse all tools</a>.</p>'
            '</div></div></section>'
            '</main>' + footer_html())
    return head_html(SITE_NAME + ' — ' + SITE_TAGLINE,
                     'Free online tools for everyday tasks: word counters, image tools, calculators, generators, timers and more. No signup required — everything runs in your browser.',
                     SITE_URL + '/', ld) + body

# ---------------- All tools directory ----------------
def tools_directory_html():
    cat_sections = ''
    for c in CATEGORIES:
        tools = [t for t in TOOLS if t['cat'] == c['cat']]
        cards = ''.join(tool_card(t) for t in sorted(tools, key=lambda x: x['name'].lower()))
        cat_sections += ('<section class="section" id="cat-' + c['slug'] + '"><div class="container">'
                         '<div class="section-head"><div><h2>' + esc(c['name']) + '</h2><p>' + esc(c['desc']) + '</p></div>'
                         '<a class="btn btn-secondary" href="/category/' + c['slug'] + '/">Browse category</a></div>'
                         '<div class="tool-grid">' + cards + '</div></div></section>')
    body = (header_html('/tools/') +
            '<main id="main"><section class="page-hero"><div class="container">'
            '<nav aria-label="Breadcrumb"><ol class="breadcrumb"><li><a href="/">Home</a></li><li aria-current="page">Tools</li></ol></nav>'
            '<h1>All CalcHub Tools</h1>'
            '<p class="lead">Browse all 30 free online tools. Every tool runs locally in your browser with no signup required.</p>'
            '<div class="search-box" style="margin-top:20px">'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>'
            '<input id="category-search" type="text" placeholder="Filter tools by name…" aria-label="Filter tools">'
            '</div>'
            '</div></section>'
            '<div id="category-tool-list"><p class="result-sub search-count" style="margin-bottom:16px">30 tools</p>' + cat_sections + '</div>'
            '</main>' + footer_html())
    return head_html('All Free Online Tools | CalcHub',
                     'Browse all 30 free online tools from CalcHub: text tools, image tools, calculators, generators, timers and counters. No signup, all in-browser.',
                     SITE_URL + '/tools/', [
                         {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
                          'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE_URL + '/'},
                                              {'@type': 'ListItem', 'position': 2, 'name': 'Tools', 'item': SITE_URL + '/tools/'}]}
                     ]) + body

# ---------------- Category page ----------------
def category_page(c):
    tools = [t for t in TOOLS if t['cat'] == c['cat']]
    cards = ''.join(tool_card(t) for t in sorted(tools, key=lambda x: x['name'].lower()))
    canonical = SITE_URL + '/category/' + c['slug'] + '/'
    body = (header_html('/tools/') +
            '<main id="main"><section class="page-hero"><div class="container">'
            + breadcrumb_html([('Home', '/'), ('Tools', '/tools/'), (c['name'], None)]) +
            '<h1>' + esc(c['name']) + '</h1>'
            '<p class="lead">' + esc(c['desc']) + '</p>'
            '<div class="search-box" style="margin-top:20px">'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>'
            '<input id="category-search" type="text" placeholder="Filter tools…" aria-label="Filter tools">'
            '</div></div></section>'
            '<section class="section"><div class="container"><div class="tool-grid" id="category-tool-list">' + cards + '</div></div></section>'
            '</main>' + footer_html())
    return head_html(c['name'] + ' – Free Online Tools | CalcHub',
                     c['desc'] + ' All tools are free, run in your browser and need no signup.',
                     canonical, [
                         {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
                          'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE_URL + '/'},
                                              {'@type': 'ListItem', 'position': 2, 'name': 'Tools', 'item': SITE_URL + '/tools/'},
                                              {'@type': 'ListItem', 'position': 3, 'name': c['name'], 'item': canonical}]}
                     ]) + body

# ---------------- Search page ----------------
def search_page():
    body = (header_html('') +
            '<main id="main"><section class="page-hero"><div class="container">'
            '<h1>Search Tools</h1>'
            '<p class="lead">Find the free online tool you need. Search by name or keyword.</p>'
            '<div class="search-box" style="margin-top:20px">'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>'
            '<input id="page-search" type="text" placeholder="e.g. password, image, timer…" aria-label="Search tools">'
            '</div></div></section>'
            '<section class="section"><div class="container">'
            '<p class="result-sub search-count" style="margin-bottom:16px">30 tools</p>'
            '<div class="tool-grid" id="page-tool-list">' +
            ''.join(tool_card(t) for t in sorted(TOOLS, key=lambda x: x['name'].lower())) +
            '<p class="search-empty" style="display:none;grid-column:1/-1;color:var(--text-muted)">No tools match that search.</p>'
            '</div></div></section></main>' + footer_html())
    return head_html('Search Tools | CalcHub',
                     'Search all CalcHub free online tools by name or keyword. Every tool is free and runs in your browser.',
                     SITE_URL + '/search/', None) + body

# ---------------- 404 ----------------
def not_found_page():
    body = (header_html('') +
            '<main id="main"><div class="container error-page">'
            '<div class="code">404</div>'
            '<h1>Page not found</h1>'
            '<p>The page you are looking for does not exist or has moved. Try searching for a tool instead.</p>'
            '<a class="btn btn-primary" href="/">Back to home</a> '
            '<a class="btn btn-secondary" href="/tools/">Browse all tools</a>'
            '</div></main>' + footer_html())
    return head_html('Page Not Found (404) | CalcHub',
                     'The page you requested could not be found. Browse CalcHub free online tools instead.',
                     SITE_URL + '/404.html', None, noindex=True) + body

# ---------------- Policy pages ----------------
def legal_page(slug, title, desc, updated, sections):
    h2 = ''
    for sec in sections:
        h2 += '<h2>' + esc(sec[0]) + '</h2>' + sec[1]
    body = (header_html('') +
            '<main id="main"><section class="page-hero"><div class="container">'
            + breadcrumb_html([('Home', '/'), (title, None)]) +
            '<h1>' + esc(title) + '</h1>'
            '<p class="lead">' + esc(desc) + '</p>'
            '<p class="updated">Last updated: ' + updated + '</p>'
            '</div></section>'
            '<section class="section"><div class="container legal-page">' + h2 + '</div></section></main>' + footer_html())
    return head_html(title + ' | CalcHub', desc, SITE_URL + '/' + slug + '/', None) + body

def policy_pages():
    pages = []
    # About
    about_secs = [
        ('What is CalcHub?', '<p>CalcHub is a free online tool platform with the simple goal of helping you get everyday tasks done quickly and privately. We publish a curated set of utilities for writing, images, calculations, generation, time management and counting.</p><p>All tools run as a static website. Pages are lightweight, load fast, and work on phones, tablets and desktops.</p>'),
        ('What you will find', '<p>Six categories of tools:</p><ul><li><a href="/category/text-tools/">Text Tools</a> — word counts, character counts, case conversion, duplicate removal and placeholder text.</li><li><a href="/category/image-tools/">Image &amp; File Tools</a> — compress, resize, convert, crop and generate favicons.</li><li><a href="/category/calculators/">Calculators</a> — percentage, age, date difference, unit, BMI and discount calculators.</li><li><a href="/category/generators/">Generators &amp; Converters</a> — passwords, QR codes, UUIDs, random data and JSON tools.</li><li><a href="/category/time-tools/">Time &amp; Productivity</a> — countdown, stopwatch, Pomodoro and time zone tools.</li><li><a href="/category/counters/">Counters &amp; Trackers</a> — simple tally counters.</li></ul>'),
        ('How we choose tools', '<p>We only publish tools that are genuinely useful, work without an account, and can run reliably in a standard browser. We describe features honestly: where a result is an estimate (such as reading time or BMI), the page says so. We do not invent usage statistics, reviews or performance claims.</p>'),
        ('Privacy by design', '<p>Processing happens in your browser. Your text, numbers and files are not uploaded to us, so we have nothing to sell or lose. See the <a href="/privacy-policy/">Privacy Policy</a> for details.</p>'),
        ('Contact', '<p>Questions or suggestions? Use the <a href="/contact/">Contact</a> page.</p>'),
    ]
    pages.append(('about', legal_page('about', 'About Us', 'Learn about CalcHub — a free online tool platform focused on privacy, speed and useful everyday utilities.', 'November 2026', about_secs)))

    # Contact
    contact_secs = [
        ('Get in touch', '<p>We welcome feedback, bug reports and tool suggestions. The simplest way to reach us is email.</p>'
         '<p><strong>Email:</strong> <a href="mailto:' + CONTACT_EMAIL + '">' + CONTACT_EMAIL + '</a></p>'
         '<p>We aim to respond to genuine enquiries within a few business days. Please do not send sensitive personal data by email.</p>'),
        ('What to include', '<ul><li>Which tool or page you are writing about.</li><li>What you expected to happen.</li><li>What actually happened.</li><li>Your browser and device (if relevant).</li></ul>'),
        ('Response times', '<p>This is a small independent project. We cannot guarantee a response to every message, but we read everything and prioritise issues that affect many users.</p>'),
    ]
    pages.append(('contact', legal_page('contact', 'Contact Us', 'Contact the CalcHub team with feedback, bug reports or suggestions.', 'November 2026', contact_secs)))

    # Privacy
    privacy_secs = [
        ('Introduction', '<p>This Privacy Policy explains how ' + SITE_NAME + ' handles information when you visit and use our website. We designed the site to minimise data collection: the tools themselves process your content in your browser and do not send it to our servers.</p>'),
        ('Information we collect', '<p>We operate a static website with no user accounts and no database of visitors. We do not require you to provide a name, email address or any personal details to use any tool.</p><p>Depending on how the site is hosted and connected to third-party services, standard technical data may be collected automatically — for example your IP address, browser type, referring page, and pages visited. This data is used by hosting providers and analytics services to operate and improve the site, and is generally retained according to those providers\u2019 policies.</p>'),
        ('Cookies', '<p>We do not set advertising cookies ourselves. Some tools use your browser\u2019s local storage only if you explicitly enable a "keep count" option. That data stays on your device.</p><p>If we later enable Google AdSense, Google may use cookies (including DoubleClick cookies) to serve and personalise ads. We would clearly update this policy, and where required, ask for consent before personalised advertising. You can control or disable cookies in your browser settings.</p>'),
        ('Analytics', '<p>If the site uses an analytics service such as Google Analytics or privacy-friendly alternatives (for example Cloudflare Web Analytics), it may process aggregate, privacy-preserving data about visits. We do not combine this with personal identifiers, and we do not log the content you type into tools.</p>'),
        ('Local processing of tool data', '<p>All tool processing happens in your browser using standard Web APIs such as Canvas, File, Blob, Clipboard, Web Crypto and Intl. Your text, uploaded images and calculated values are not uploaded to our server, are not stored by us, and disappear when you close the page.</p>'),
        ('Third-party services', '<p>Our pages may load resources from third-party providers for core functions (such as hosting, fonts or analytics). These providers process only the minimal technical data needed to deliver those resources, under their own privacy policies.</p>'),
        ('Data security', '<p>Because we do not collect or store tool inputs, there is little personal data for us to protect. Standard security measures (HTTPS, updated dependencies) are used to keep the site itself safe.</p>'),
        ('Your rights', '<p>Depending on your location (for example, under the GDPR or CCPA), you may have rights to access, correct or delete personal data. Since we do not collect tool inputs or account data, there is generally nothing to access or delete. To raise a privacy question, contact us via the <a href="/contact/">Contact</a> page.</p>'),
        ('Changes to this policy', '<p>We may update this policy when the site or law changes. The "Last updated" date at the top of this page reflects the latest revision.</p>'),
    ]
    pages.append(('privacy-policy', legal_page('privacy-policy', 'Privacy Policy', 'How CalcHub protects your privacy: tools run in your browser, no accounts, minimal data collection and clear disclosure of cookies and analytics.', 'November 2026', privacy_secs)))

    # Terms
    terms_secs = [
        ('Acceptance of terms', '<p>By accessing or using ' + SITE_NAME + ', you agree to these Terms of Use. If you do not agree, please do not use the site.</p>'),
        ('Use of the tools', '<p>The tools are provided free of charge for personal and business use. You may use them for lawful purposes only. You may not attempt to disrupt the site, reverse-engineer it, or use it to process unlawful content.</p>'),
        ('No warranty', '<p>We provide the website and tools on an "as is" and "as available" basis, without warranties of any kind, express or implied, including fitness for a particular purpose. We work to keep tools accurate and available, but we cannot guarantee that results will be correct in every situation or that the site will be uninterrupted and error-free.</p>'),
        ('Results are provided without liability', '<p>Tools such as calculators, converters and timers produce results based on standard formulas. Always verify important results independently. To the maximum extent permitted by law, ' + SITE_NAME + ' and its operators are not liable for any damages arising from your use of the site or reliance on its results.</p>'),
        ('Intellectual property', '<p>The site design, text and original code are owned by or licensed to ' + SITE_NAME + '. The bundled open-source QR code library remains under its original license (MIT) and copyright notice.</p>'),
        ('Changes to the service', '<p>We may add, change, or remove tools and pages at any time without notice.</p>'),
        ('Governing law', '<p>These terms are governed by the laws applicable to the site operator\u2019s jurisdiction. If a court finds any part of these terms unenforceable, the rest remains in effect.</p>'),
        ('Contact', '<p>Questions about these terms? <a href="/contact/">Contact us</a>.</p>'),
    ]
    pages.append(('terms', legal_page('terms', 'Terms of Use', 'The terms that apply when you use CalcHub free online tools, including disclaimers on results and the no-warranty section.', 'November 2026', terms_secs)))

    # Disclaimer
    disc_secs = [
        ('General information only', '<p>The tools and content on ' + SITE_NAME + ' are provided for general informational and utility purposes. They are not professional advice.</p>'),
        ('Calculations and estimates', '<p>Results from calculators, converters, timers and other tools are based on common formulas and are provided for convenience. Acceptable for most everyday uses, they may not suit professional, legal, medical or financial decisions. For example, BMI is a screening measure and not a medical diagnosis, and reading time is an estimate based on an average reading speed.</p>'),
        ('No professional relationship', '<p>Using a tool does not create a professional relationship with the operators of this site. For medical, legal, tax or investment decisions, consult a qualified professional.</p>'),
        ('External links', '<p>Pages may link to external websites. We are not responsible for the content, accuracy or practices of third-party sites.</p>'),
        ('Limitation of liability', '<p>To the maximum extent permitted by law, ' + SITE_NAME + ' disclaims liability for any loss or damage caused by reliance on information obtained from this site or by use of its tools.</p>'),
    ]
    pages.append(('disclaimer', legal_page('disclaimer', 'Disclaimer', 'CalcHub tools and content are provided for general purposes. Calculators give estimates, not professional advice.', 'November 2026', disc_secs)))
    return pages

# ---------------- SEO files ----------------
def tools_data_js():
    data = {
        'tools': [{'slug': t['slug'], 'name': t['name'], 'cat': t['cat'], 'icon': t['icon'], 'desc': t['lede']} for t in TOOLS],
        'categories': CATEGORIES
    }
    return 'window.CalcHubData = ' + json.dumps(data, ensure_ascii=False) + ';\n'

def sitemap_xml():
    urls = [SITE_URL + '/', SITE_URL + '/tools/', SITE_URL + '/search/',
            SITE_URL + '/about/', SITE_URL + '/contact/', SITE_URL + '/privacy-policy/',
            SITE_URL + '/terms/', SITE_URL + '/disclaimer/']
    for c in CATEGORIES:
        urls.append(SITE_URL + '/category/' + c['slug'] + '/')
    urls.extend(SITE_URL + '/tools/' + t['slug'] + '/' for t in TOOLS)
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        out.append('  <url><loc>' + u + '</loc><changefreq>weekly</changefreq></url>')
    out.append('</urlset>')
    return '\n'.join(out) + '\n'

def robots_txt():
    return ('User-agent: *\nAllow: /\n\n'
            'Sitemap: ' + SITE_URL + '/sitemap.xml\n')

def favicon_svg():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
            '<rect width="64" height="64" rx="14" fill="#2563eb"/>'
            '<text x="32" y="42" font-family="Arial,Helvetica,sans-serif" font-size="28" font-weight="800" fill="#ffffff" text-anchor="middle">CH</text></svg>\n')

# ---------------- Writer ----------------
def ensure_dirs():
    dirs = [os.path.join(ROOT, 'tools'), os.path.join(ROOT, 'category'), os.path.join(ROOT, 'assets', 'js')]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('wrote', rel)

def build():
    ensure_dirs()
    for t in TOOLS:
        write('tools/' + t['slug'] + '/index.html', tool_page(t))
    write('index.html', home_page())
    write('tools/index.html', tools_directory_html())
    for c in CATEGORIES:
        write('category/' + c['slug'] + '/index.html', category_page(c))
    write('search/index.html', search_page())
    write('404.html', not_found_page())
    for rel, content in policy_pages():
        write(rel + '/index.html', content)
    write('assets/js/tools-data.js', tools_data_js())
    write('sitemap.xml', sitemap_xml())
    write('robots.txt', robots_txt())
    write('favicon.svg', favicon_svg())
    print('DONE:', len(TOOLS), 'tool pages + site pages')

if __name__ == '__main__':
    build()