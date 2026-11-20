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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools_text import TEXT_TOOLS
from tools_image import IMAGE_TOOLS
from tools_calc import CALC_TOOLS
from tools_gen import GENERATOR_TOOLS
from tools_time_count import TIME_TOOLS, COUNTER_TOOLS
from icons import icon, tool_icon, category_icon, icon as svg_icon

TOOLS = TEXT_TOOLS + IMAGE_TOOLS + CALC_TOOLS + GENERATOR_TOOLS + TIME_TOOLS + COUNTER_TOOLS
BY_SLUG = {t['slug']: t for t in TOOLS}

# ---------------- Site constants (PENDING: replace before go-live) ----------------
SITE_URL = 'https://calchub.tools'           # canonical origin (PENDING)
SITE_NAME = 'CalcHub'
SITE_TAGLINE = 'Free Tools for Everyday Tasks'
# No contact address is published: the site owner has not supplied a real,
# monitored inbox. The Contact page explains how to reach us instead of
# inventing an address (see policy_pages()). Set this only when a verified
# inbox exists.
CONTACT_EMAIL = ''

CATEGORIES = [
    {'slug': 'text-tools',     'cat': 'text',  'name': 'Text Tools',            'icon': '✎',
     'desc': 'Count words and characters, estimate reading time, change capitalization, remove duplicate lines and generate placeholder text.',
     'intro': [
         'These tools deal with text as text: how long it is, how it is capitalised, and whether a list contains the same line twice. They are most useful when a form, a brief or a publishing platform imposes a limit or a format.',
         'Everything here works on whatever you paste into the box. The text is not uploaded, so draft copy, customer lists and unpublished material can be checked without sending them anywhere.'
     ],
     'choosing': 'Use Word Counter when a limit is in words and Character Counter when it is in characters — the two answers often disagree. Reading Time turns a word count into an estimate. Text Case Converter changes formatting, Duplicate Line Remover cleans a list, and Lorem Ipsum Generator fills space in a layout that is still being designed.',
     'usecases': [
         'Checking an article against an 800-word brief before submitting it.',
         'Finding out why a meta title was rejected by a character limit.',
         'Removing repeated email addresses from a list pasted out of a spreadsheet.'
     ]},
    {'slug': 'image-tools',    'cat': 'image', 'name': 'Image & File Tools',     'icon': '🖼',
     'desc': 'Compress, resize and crop images, convert between formats, or build a favicon — all in your browser.',
     'intro': [
         'A photo that is too large, in the wrong format or the wrong shape is a common blocker when uploading to a site or sending an attachment. These tools fix those problems one image at a time.',
         'Each tool writes a fixed output format: the compressor produces JPEG, the resizer and cropper produce PNG, and the converters produce PNG or WebP. Choose by the file you need at the end, not only by the one you have now.'
     ],
     'choosing': 'Start with Image Compressor when size is the problem, Image Resizer when dimensions are, and Image Cropper when the framing is. Use the two converters when a site requires a particular format, and Favicon Generator when you need a small square site icon.',
     'usecases': [
         'Getting a phone photo under an upload limit before attaching it to a form.',
         'Producing a 1200 x 630 preview image for a shared link.',
         'Making a square avatar from a landscape photo.'
     ]},
    {'slug': 'calculators',    'cat': 'calc',  'name': 'Calculators',            'icon': '≡',
     'desc': 'Work out percentages, ages, date spans, unit conversions, BMI and sale prices, with the formula shown alongside the answer.',
     'intro': [
         'These are the small calculations that turn up in everyday decisions: a discount, a deadline, a conversion between units, a figure on a form. Each tool asks for the values it needs and shows the working next to the result.',
         'Where an answer depends on an assumption — an average month length, a standard BMI range, a single discount rather than stacked ones — the tool says so on its own page.'
     ],
     'choosing': 'Percentage Calculator covers the four common percentage questions; Discount Calculator adds a price and optional tax. Age Calculator gives calendar years, months and days, while Date Difference counts days between two dates. Unit Converter handles six measurement categories, and BMI Calculator reports an index with its limits clearly stated.',
     'usecases': [
         'Working out what a 25% discount actually costs before reaching the checkout.',
         'Converting a measurement between US and metric units.',
         'Checking the exact number of days between two dates on a contract.'
     ]},
    {'slug': 'generators',     'cat': 'gen',   'name': 'Generators & Converters','icon': '⚙',
     'desc': 'Generate passwords, QR codes, random numbers and UUIDs, pick a name at random, or format and validate JSON.',
     'intro': [
         'Sometimes you need a value you cannot sensibly invent yourself: a password, an identifier, a random pick from a list, or a readable version of a JSON response. These tools produce one on demand.',
         'Random tools here use the browser cryptographic random source rather than a predictable generator. That suits everyday use, though a generated identifier is still an identifier, not a secret or a credential.'
     ],
     'choosing': 'Use Password Generator for credentials and UUID Generator for identifiers — they solve different problems. Random Number Generator draws numbers in a range, Random Name Picker draws from a list, QR Code Generator encodes a link or short text into an image, and JSON Formatter checks and pretty-prints structured data.',
     'usecases': [
         'Creating a password for a new account and saving it in a password manager.',
         'Generating a QR code for a menu link on a printed card.',
         'Finding the syntax error in an API response that failed to parse.'
     ]},
    {'slug': 'time-tools',     'cat': 'time',  'name': 'Time & Productivity',    'icon': '⏱',
     'desc': 'Countdown and focus timers, a stopwatch, and a time zone converter for scheduling across regions.',
     'intro': [
         'These tools are about when things happen: how long something has taken, how long is left, and what time it is somewhere else. They run in the tab you have open and need no account.',
         'The timers read the clock rather than counting frames, so switching tabs does not make them lose time. None of them plays a sound — a finished phase is shown on the page.'
     ],
     'choosing': 'Use Countdown Timer when you know the duration in advance and Stopwatch when you want to measure elapsed time. Pomodoro Timer alternates focus and break blocks automatically, and Time Zone Converter compares a date and time between two IANA zones.',
     'usecases': [
         'Timing a presentation or a short break without an alarm going off in a meeting.',
         'Measuring how long a recurring task actually takes.',
         'Finding a meeting time that works between New York and London in July.'
     ]},
    {'slug': 'counters',       'cat': 'count', 'name': 'Counters & Trackers',    'icon': '⊕',
     'desc': 'Two manual tallies: one with steps and keyboard shortcuts, one with a single large button.',
     'intro': [
         'A manual tally is still the right tool for counting people at a door, repetitions in a set or items in a stack. These two counters do that job without turning it into a spreadsheet.',
         'They count only what you press. Neither tool tracks visits, clicks elsewhere on the site or any automatic activity.'
     ],
     'choosing': 'Online Counter gives you add and subtract buttons, an adjustable step and keyboard shortcuts — better when you are counting quickly or netting off removals. Click Counter is a single large button that adds one per press, which suits a touch screen or a repeated action. Both can optionally keep the count after a refresh.',
     'usecases': [
         'Counting attendees as they arrive, using the keyboard to keep your eyes up.',
         'Tallying stock in packs by setting a step size.',
         'Counting repetitions on a phone where a large target is easier to hit.'
     ]},
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

def brand_mark(size=32):
    """Distinct brand graphic: a blue rounded tile with a stylised 'C' made of
    three stacked bars, suggesting calculation / tools. Pure SVG, no text font."""
    return ('<svg class="logo-mark" width="%d" height="%d" viewBox="0 0 40 40" fill="none" '
            'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            '<rect width="40" height="40" rx="11" fill="#2563eb"/>'
            '<path d="M27 13.5a9 9 0 1 0 0 13" stroke="#fff" stroke-width="4.2" stroke-linecap="round"/>'
            '<circle cx="27" cy="20" r="2.6" fill="#93c5fd"/>'
            '</svg>' % (size, size))

def icon_svg():
    return brand_mark(30)

def logo_html(light=False):
    return ('<a class="logo" href="/" aria-label="CalcHub home">' + brand_mark(32) +
            '<span class="logo-word">Calc<em>Hub</em></span></a>')

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
            '<a class="header-search" href="/search/" aria-label="Search all tools">'
            + svg_icon('search', 17) + '<span>Search tools</span><kbd>/</kbd></a>\n'
            '<button class="menu-toggle" aria-expanded="false" aria-label="Toggle menu">'
            + svg_icon('menu', 20) + '</button>\n'
            '</div>\n  </div>\n</header>\n')

def footer_html(extra_scripts='', include_tools_js=True):
    cats = ''
    for c in CATEGORIES:
        cats += '<a href="/category/' + c['slug'] + '/">' + esc(c['name']) + '</a>'
    return ('<footer class="site-footer">\n  <div class="container">\n'
            '    <div class="footer-grid">\n'
            '      <div class="footer-brand">\n' + logo_html(light=True) +
            '        <p>Thirty free browser tools for writing, images, calculations, generation, time and counting. No account required, and nothing you enter is uploaded.</p>\n'
            '      </div>\n'
            '      <div class="footer-col"><h4>Tools</h4>' + cats +
            '        <a href="/tools/">All Tools</a>\n      </div>\n'
            '      <div class="footer-col"><h4>Company</h4>\n'
            '        <a href="/about/">About</a>\n'
            '        <a href="/contact/">Contact</a>\n'
            '      </div>\n'
            '      <div class="footer-col"><h4>Legal</h4>\n'
            '        <a href="/privacy-policy/">Privacy Policy</a>\n'
            '        <a href="/terms/">Terms of Use</a>\n'
            '        <a href="/disclaimer/">Disclaimer</a>\n'
            '      </div>\n'
            '    </div>\n'
            '    <div class="footer-bottom">\n'
            '      <span>&copy; <span data-year></span> ' + SITE_NAME + '. All rights reserved.</span>\n'
            '      <span>Free tools for everyday tasks. Your data stays on your device.</span>\n'
            '    </div>\n  </div>\n</footer>\n'
            + extra_scripts +
            '<script src="/assets/js/tools-data.js" defer></script>\n'
            + ('<script src="/assets/js/tools.js" defer></script>\n' if include_tools_js else '') +
            '<script src="/assets/js/main.js" defer></script>\n'
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
            + t['slug'] + ' ' + t['name'].lower() + '" data-cat="' + t['cat'] + '">'
            '<span class="tc-icon" aria-hidden="true">' + tool_icon(t['slug'], 22) + '</span>'
            '<h3>' + esc(t['name']) + '</h3>'
            '<p>' + esc(t['lede'][:118]) + '</p>'
            '<span class="go">Open tool' + svg_icon('arrow-up-right', 15) + '</span>'
            '</a>')

def cat_card(c, count, minor=False):
    cls = 'cat-card minor' if minor else 'cat-card'
    return ('<a class="' + cls + '" href="/category/' + c['slug'] + '">'
            '<span class="cat-icon" aria-hidden="true">' + category_icon(c['cat'], 25) + '</span>'
            '<h3>' + esc(c['name']) + '</h3>'
            '<p>' + esc(c['desc']) + '</p>'
            '<span class="cat-foot"><span class="cat-count">' + str(count) + ' tool' + ('s' if count != 1 else '') + '</span>'
            '<span class="cat-browse">Browse' + svg_icon('arrow-right', 15) + '</span></span>'
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
  <div class="dropzone" tabindex="0" role="button" aria-label="Upload an image to compress">
    <input type="file" accept="image/*">
    <span class="dz-icon">' + svg_icon('image-compressor', 26) + '</span>
    <strong>Drop your image here</strong>
    <small>or <span style="color:var(--primary);font-weight:600">click to browse</span> · JPG, PNG or WebP</small>
  </div>
</div>
<div class="form-row">
  <div class="field">
    <label for="ic-scale">Resize <span class="field-hint" data-scale-val>80%</span></label>
    <input id="ic-scale" type="range" min="10" max="100" step="5" value="80" data-scale>
  </div>
  <div class="field">
    <label for="ic-quality">JPEG quality <span class="field-hint" data-quality-val>80%</span></label>
    <input id="ic-quality" type="range" min="10" max="100" step="5" value="80" data-quality>
  </div>
</div>
<div class="status-msg"></div>
<div class="preview-wrap" data-preview-wrap hidden>
  <img data-preview alt="Compressed image preview">
  <div class="preview-meta" data-info></div>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary" data-download disabled>' + svg_icon('download', 17) + 'Download compressed JPG</button>
</div>
<p class="result-sub" style="margin-top:14px">Output is re-encoded as JPEG. Transparent PNGs lose their alpha channel when compressed to JPEG. Your image never leaves this device.</p>''',
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
<div class="form-row calc-inputs">
  <div class="field">
    <label for="pc-a" data-label-a>Percentage (X)</label>
    <input id="pc-a" type="number" step="any" value="15" data-a>
  </div>
  <div class="field">
    <label for="pc-b" data-label-b>Whole number (Y)</label>
    <input id="pc-b" type="number" step="any" value="240" data-b>
  </div>
</div>
<div class="result-card calc-result">
  <div class="rc-label">Result</div>
  <div class="result-value" data-out1>—</div>
  <div class="formula-line" data-out2>Enter values to calculate.</div>
  <div class="formula-sub" data-out3></div>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-secondary" id="pc-reset">' + svg_icon('refresh', 16) + 'Reset values</button>
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
  <label for="pg-len">Password length <span class="field-hint"><span data-length-val>16</span> characters</span></label>
  <input id="pg-len" type="range" min="4" max="64" value="16" data-length>
</div>
<div class="field">
  <span class="field-label">Include characters</span>
  <div class="pw-options">
    <label class="checkline"><input type="checkbox" data-upper checked> Uppercase <span class="field-hint">A–Z</span></label>
    <label class="checkline"><input type="checkbox" data-lower checked> Lowercase <span class="field-hint">a–z</span></label>
    <label class="checkline"><input type="checkbox" data-nums checked> Numbers <span class="field-hint">0–9</span></label>
    <label class="checkline"><input type="checkbox" data-syms checked> Symbols <span class="field-hint">!@#$…</span></label>
  </div>
</div>
<div class="field">
  <label for="pg-output">Generated password</label>
  <div class="pw-output-wrap">
    <textarea id="pg-output" class="output-area resize-none" readonly spellcheck="false" data-output autocomplete="off" autocapitalize="off"></textarea>
    <button type="button" class="pw-copy" data-copy aria-label="Copy password">' + svg_icon('copy', 18) + '</button>
  </div>
</div>
<div class="pw-strength">
  <div class="pw-meter" data-pw-meter><i></i><i></i><i></i><i></i></div>
  <span data-strength></span>
</div>
<div class="form-actions">
  <button type="button" class="btn btn-primary btn-lg" data-generate>' + svg_icon('refresh', 17) + 'Generate new password</button>
</div>
<p class="result-sub" style="margin-top:14px">Generated locally with your browser's secure random source. Your password is never stored or transmitted.</p>''',
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
    """Editorial body for a tool page.

    Content lives in _data/*.py; this function only arranges it. The
    `understanding` and `limitations` fields are optional so short, simple
    tools are not padded out with sections they do not need.
    """
    howto = '<h2>How to Use</h2><ol>' + ''.join('<li>' + esc(x) + '</li>' for x in t['howto']) + '</ol>'
    ex = '<h2>Practical Examples</h2><ul>' + ''.join('<li>' + esc(x) + '</li>' for x in t['examples']) + '</ul>'
    understanding = ''
    if t.get('understanding'):
        understanding = ('<h2>Understanding the Result</h2>' +
                         ''.join('<p>' + esc(x) + '</p>' for x in t['understanding']))
    limitations = ''
    if t.get('limitations'):
        limitations = ('<h2>Limitations and Useful Notes</h2><ul>' +
                       ''.join('<li>' + esc(x) + '</li>' for x in t['limitations']) + '</ul>')
    # Legacy registries may still carry a `features` list. Render it only when
    # present so a partial migration cannot break the build.
    feats = ''
    if t.get('features'):
        feats = '<h2>Key Features</h2><ul>' + ''.join('<li>' + esc(x) + '</li>' for x in t['features']) + '</ul>'
    priv = '<div class="privacy-note"><strong>Privacy:</strong> ' + esc(t['privacy']) + '</div>'
    faq = '<h2>Common Questions</h2>'
    for item in t['faq']:
        faq += ('<div class="faq-item"><h3>' + esc(item['q']) + '</h3><p>' + esc(item['a']) + '</p></div>')
    return '<div class="prose">' + howto + ex + understanding + limitations + feats + priv + faq + '</div>'

def side_panel_html(t):
    cat = CAT_BY_ID[t['cat']]
    related = ''
    for slug in t['related'][:5]:
        rt = BY_SLUG.get(slug)
        if rt:
            related += ('<li><a href="/tools/' + rt['slug'] + '/">' + esc(rt['name']) +
                        svg_icon('arrow-up-right', 15) + '</a></li>')
    count = len([x for x in TOOLS if x['cat'] == cat['cat']])
    return ('<aside class="side-panel">'
            '<div class="side-box"><h3>Related Tools</h3><ul>' + related + '</ul></div>'
            '<div class="side-box"><h3>Category</h3><p>' + esc(cat['name']) + ' · ' + str(count) + ' tool' + ('s' if count != 1 else '') + '</p>'
            '<a class="btn btn-secondary" href="/category/' + cat['slug'] + '/">' + svg_icon('arrow-right', 16) + 'Browse category</a></div>'
            '<div class="side-box"><h3>Explore More</h3><p>See all 30 tools in one list.</p>'
            '<a class="btn btn-secondary" href="/tools/">' + svg_icon('arrow-right', 16) + 'All tools</a></div>'
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
            '<div class="tool-page-head">'
            '<div class="th-title"><span class="th-icon" aria-hidden="true">' + tool_icon(t['slug'], 28) + '</span>'
            '<h1>' + esc(t['h1']) + '</h1></div>'
            '<p class="lead">' + esc(t['lede']) + '</p></div>'
            '<div class="tool-layout"><div>'
            '<section class="tool-panel">'
            '<div class="tool-panel-head"><span class="tp-title">' + esc(t['name']) + '</span>'
            '<span class="tp-badge">' + svg_icon('shield', 14) + 'Runs in your browser</span></div>'
            '<div class="tool-panel-body">' + widget_html(t) + '</div>'
            '</section>'
            '<div class="content-card">' + prose_html(t) + '</div>'
            '</div>' + side_panel_html(t) + '</div>'
            '</div></main>' + footer_html(extra_scripts_for(t)))
    return head_html(t['title'], t['desc'], canonical, tool_ld(t, cat)) + body

# ---------------- Home ----------------
def hero_visual_html():
    """A composed UI snippet showing real tool types — no stock illustration."""
    rows = ''
    for slug, name, label in [
        ('word-counter', 'Word Counter', '1,284 words'),
        ('password-generator', 'Password Generator', 'Kx9#pL2@vN7'),
        ('image-compressor', 'Image Compressor', '840 KB saved'),
    ]:
        rows += ('<div class="hv-row"><span class="sr-icon">' + tool_icon(slug, 18) + '</span>'
                 '<span class="hv-lines"><b>' + name + '</b><i></i></span>'
                 '<span class="result-sub" style="margin:0;white-space:nowrap">' + label + '</span></div>')
    return (
        '<div class="hero-visual" aria-hidden="true">'
        '<div class="hv-window">'
        '<div class="hv-bar"><i></i><i></i><i></i><span>calchub / tools</span></div>'
        '<div class="hv-body">'
        '<div class="hv-tabs"><span class="on">Popular</span><span>Text</span><span>Images</span><span>Calculators</span><span>Generators</span></div>'
        + rows +
        '<div class="hv-result"><div><b>Result</b><strong>36.8% smaller</strong></div>' + svg_icon('check', 24) + '</div>'
        '</div></div>'
        '<div class="hv-float one">' + svg_icon('shield', 16) + 'Runs in your browser</div>'
        '<div class="hv-float two">' + svg_icon('bolt', 16) + 'No signup needed</div>'
        '</div>')

def quick_search_html():
    """Dropdown search backed by window.CalcHubData (all 30 tools, keyboard ready)."""
    return (
        '<div class="hero-search">'
        '<div class="search-field">'
        + svg_icon('search', 20) +
        '<input id="home-search" type="text" placeholder="Search tools, e.g. image or timer" aria-label="Search all tools" '
        'autocomplete="off" role="combobox" aria-expanded="false" aria-controls="home-results">'
        '<button type="button" class="btn btn-primary" id="home-search-go">Search' + svg_icon('arrow-right', 16) + '</button>'
        '</div>'
        '<div class="search-results" id="home-results" role="listbox" aria-label="Tool results"></div>'
        '</div>')

def value_props_html():
    items = [
        ('shield', 'Your data stays on your device', 'Text, numbers and images are processed in the browser. We never receive them, so there is nothing to store or share.'),
        ('bolt', 'No account, no setup', 'Open a tool and start using it. There is nothing to sign up for and no settings to configure first.'),
        ('gift', 'Free to use', 'Every tool here is free. There is no paid tier, no trial and no registration wall.'),
    ]
    out = ''
    for ic, title, text in items:
        out += ('<div class="value-item"><span class="vi-icon">' + svg_icon(ic, 24) + '</span>'
                '<div><h3>' + title + '</h3><p>' + text + '</p></div></div>')
    return '<div class="value-grid">' + out + '</div>'

def home_page():
    popular = [BY_SLUG[s] for s in POPULAR_SLUGS if s in BY_SLUG]
    popular_cards = ''.join(tool_card(t) for t in popular)
    all_cards = ''.join(tool_card(t) for t in sorted(TOOLS, key=lambda x: x['name'].lower()))
    counts = {c['cat']: len([x for x in TOOLS if x['cat'] == c['cat']]) for c in CATEGORIES}
    # Core four categories first; Counters given lower visual weight.
    core = [c for c in CATEGORIES if c['cat'] in ('text', 'image', 'calc', 'gen')]
    minor = [c for c in CATEGORIES if c['cat'] in ('time', 'count')]
    cat_cards = ''.join(cat_card(c, counts[c['cat']]) for c in core)
    cat_minor = ''.join(cat_card(c, counts[c['cat']], minor=True) for c in minor)

    filter_tabs = '<button type="button" class="filter-tab active" data-filter="all">All Tools</button>'
    filter_tabs += ''.join('<button type="button" class="filter-tab" data-filter="' + c['cat'] + '">' + esc(c['name']) + '</button>' for c in CATEGORIES)

    ld = [
        {'@context': 'https://schema.org', '@type': 'WebSite',
         'name': SITE_NAME, 'url': SITE_URL + '/',
         'potentialAction': {'@type': 'SearchAction', 'target': SITE_URL + '/search/?q={search_term_string}', 'query-input': 'required name=search_term_string'}},
        {'@context': 'https://schema.org', '@type': 'Organization', 'name': SITE_NAME, 'url': SITE_URL + '/'}
    ]
    body = (header_html('/') +
            '<main id="main">'

            '<section class="hero"><div class="container hero-inner">'
            '<div class="hero-copy">'
            '<span class="eyebrow">30 free online tools</span>'
            '<h1>Free Tools for <span class="accent">Everyday Tasks.</span></h1>'
            '<p class="hero-sub">Count words, resize an image, work out a percentage, generate a password. Open a tool and use it — no account, no setup.</p>'
            '<p class="hero-note">Your text and files are processed on your device. <strong>Nothing you enter is uploaded.</strong></p>'
            + quick_search_html() +
            '</div>'
            + hero_visual_html() +
            '</div></section>'

            '<section class="section"><div class="container">'
            '<div class="section-head"><div><h2>Popular Tools</h2><p>A few good places to start if you are not sure which tool you need.</p></div>'
            '<a class="head-link" href="/tools/">View all tools' + svg_icon('arrow-right', 16) + '</a></div>'
            '<div class="tool-grid">' + popular_cards + '</div>'
            '</div></section>'

            '<section class="section soft"><div class="container">'
            '<div class="section-head"><div><h2>Tool Categories</h2><p>Grouped by the kind of job: writing, images, calculations, generation, time and counting.</p></div></div>'
            '<div class="cat-grid">' + cat_cards + '</div>'
            '<div class="cat-grid" style="margin-top:20px;grid-template-columns:repeat(2,minmax(0,1fr))">' + cat_minor + '</div>'
            '</div></section>'

            '<section class="section"><div class="container" id="all-tools">'
            '<div class="section-head"><div><h2>All Tools</h2><p>All 30 tools in one list. Filter by category or search by name to narrow it down.</p></div></div>'
            '<div class="filter-bar"><div class="filter-tabs">' + filter_tabs + '</div>'
            '<span class="filter-count" id="all-tools-count">' + str(len(TOOLS)) + ' tools</span></div>'
            '<div class="tool-grid" id="home-tool-list">' + all_cards + '</div>'
            '<div class="filter-empty" id="all-tools-empty"><strong>No tools found</strong>Try a different search or category.</div>'
            '</div></section>'

            '<section class="section soft"><div class="container">'
            '<div class="why-intro"><h2>Why CalcHub?</h2><p>A few things worth knowing before you use the tools.</p></div>'
            + value_props_html() +
            '<div class="why-links"><a href="/about/">Learn more about CalcHub</a> &nbsp;·&nbsp; <a href="/tools/">Browse all tools</a></div>'
            '</div></section>'

            '<section class="cta-band"><div class="container"><div class="cta-inner">'
            '<div><h2>Find the tool you need</h2><p>Browse all 30, or search by the job you are trying to do. Everything runs in your browser.</p></div>'
            '<a class="btn btn-lg btn-primary" href="/tools/">Explore all ' + str(len(TOOLS)) + ' tools' + svg_icon('arrow-right', 17) + '</a>'
            '</div></section>'
            '</main>' + footer_html(include_tools_js=False))
    return head_html(SITE_NAME + ' — ' + SITE_TAGLINE,
                     'Thirty free tools for counting, converting, calculating, generating and timing. They run in your browser with no account, and nothing you enter is uploaded.',
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
            '<p class="lead">All 30 tools, grouped by what they do. Filter by name below, or open a category to see the tools inside it.</p>'
            '<div class="search-field" style="margin-top:24px;max-width:560px">' + svg_icon('search', 19) +
            '<input id="category-search" type="text" placeholder="Filter all tools by name..." aria-label="Filter tools">'
            '</div>'
            '</div></section>'
            '<div id="category-tool-list"><p class="result-sub search-count" style="margin-bottom:16px">30 tools</p>' + cat_sections + '</div>'
            '</main>' + footer_html(include_tools_js=False))
    return head_html('All 30 Free Tools | CalcHub',
                     'Browse all 30 CalcHub tools grouped by category: text, images, calculators, generators, time and counters. Free, browser-based, no account needed.',
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
    names = ', '.join(t['name'] for t in sorted(tools, key=lambda x: x['name'].lower()))
    guide = ('<div class="content-card"><div class="prose">'
             '<h2>What belongs in this category</h2>'
             + ''.join('<p>' + esc(x) + '</p>' for x in c['intro']) +
             '<h2>Choosing the right tool</h2><p>' + esc(c['choosing']) + '</p>'
             '<p class="cat-tool-list"><strong>Tools here:</strong> ' + esc(names) + '.</p>'
             '<h2>Common situations</h2><ul>'
             + ''.join('<li>' + esc(x) + '</li>' for x in c['usecases']) +
             '</ul></div></div>')
    body = (header_html('/tools/') +
            '<main id="main"><section class="page-hero"><div class="container">'
            + breadcrumb_html([('Home', '/'), ('Tools', '/tools/'), (c['name'], None)]) +
            '<h1>' + esc(c['name']) + '</h1>'
            '<p class="lead">' + esc(c['desc']) + '</p>'
            '<div class="search-field" style="margin-top:24px;max-width:520px">' + svg_icon('search', 19) +
            '<input id="category-search" type="text" placeholder="Filter tools in this category..." aria-label="Filter tools">'
            '</div></div></section>'
            '<section class="section"><div class="container">'
            '<p class="result-sub search-count" style="margin-bottom:18px">' + str(len(tools)) + ' tool' + ('s' if len(tools) != 1 else '') + '</p>'
            '<div class="tool-grid" id="category-tool-list">' + cards + '</div>'
            '<div class="filter-empty" id="category-empty"><strong>No tools found</strong>Try a different keyword.</div>'
            '</div></section>'
            '<section class="section soft"><div class="container">' + guide + '</div></section>'
            '</main>' + footer_html(include_tools_js=False))
    return head_html(c['name'] + ' – Free Online Tools | CalcHub',
                     c['desc'],
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
            '<p class="lead">Search all 30 tools by name. Type a word like image, timer or password.</p>'
            '<div class="search-field" style="margin-top:24px;max-width:560px">' + svg_icon('search', 19) +
            '<input id="page-search" type="text" placeholder="e.g. password, image, timer..." aria-label="Search tools">'
            '</div></div></section>'
            '<section class="section"><div class="container">'
            '<p class="result-sub search-count" style="margin-bottom:18px">' + str(len(TOOLS)) + ' tools</p>'
            '<div class="tool-grid" id="page-tool-list">' +
            ''.join(tool_card(t) for t in sorted(TOOLS, key=lambda x: x['name'].lower())) +
            '<p class="search-empty" style="display:none;grid-column:1/-1;color:var(--muted);text-align:center;padding:48px 0"><strong style="color:var(--ink-2);display:block;font-size:1.05rem;margin-bottom:4px">No tools found</strong>Try a different keyword.</p>'
            '</div></div></section></main>' + footer_html(include_tools_js=False))
    return head_html('Search Tools | CalcHub',
                     'Search the full list of 30 CalcHub tools by name. Everything runs in your browser and needs no account.',
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
            '</div></main>' + footer_html(include_tools_js=False))
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
            '<section class="section"><div class="container legal-page">' + h2 + '</div></section></main>' + footer_html(include_tools_js=False))
    return head_html(title + ' | CalcHub', desc, SITE_URL + '/' + slug + '/', None) + body

def policy_pages():
    pages = []
    # About
    about_secs = [
        ('What CalcHub is', '<p>CalcHub is a collection of 30 free tools for small, recurring jobs: counting words, checking a percentage, resizing an image, generating a password, or finding the time in another city. Each page contains one tool and a short explanation of how to use it.</p><p>There is no account to create and nothing to install. You open a tool, put in your text, numbers or file, and read the result.</p>'),
        ('What you will find', '<p>The tools are grouped into six collections:</p><ul><li><a href="/category/text-tools/">Text Tools</a> — word and character counts, reading time, case conversion, duplicate-line removal and placeholder text.</li><li><a href="/category/image-tools/">Image &amp; File Tools</a> — compress, resize, crop, convert formats and generate a favicon.</li><li><a href="/category/calculators/">Calculators</a> — percentages, age, date difference, unit conversion, BMI and discounts.</li><li><a href="/category/generators/">Generators &amp; Converters</a> — passwords, QR codes, UUIDs, random values, name picking and JSON tools.</li><li><a href="/category/time-tools/">Time &amp; Productivity</a> — countdown, stopwatch, Pomodoro timer and time zone conversion.</li><li><a href="/category/counters/">Counters &amp; Trackers</a> — two simple manual tallies.</li></ul>'),
        ('How the tools work', '<p>Processing happens in your browser. Text you paste, images you drop and numbers you enter are handled on your device using standard browser features, and are not sent to a server. Where a result depends on an assumption — an average reading speed, a standard BMI range, an average month length — the tool page says so.</p><p>The explanations on each page are written against what the tool actually does. If a timer has no sound, or a converter always outputs a particular format, that is stated rather than left for you to discover.</p>'),
        ('Privacy', '<p>Because the tools process input locally, we do not receive what you enter. The only optional storage is in the counter tools, where a tickbox can keep a running number in your own browser. See the <a href="/privacy-policy/">Privacy Policy</a> for the details.</p>'),
        ('Contact', '<p>Questions, corrections or suggestions? Use the <a href="/contact/">Contact</a> page.</p>'),
    ]
    pages.append(('about', legal_page('about', 'About Us', 'What CalcHub is, what the 30 tools cover and how they handle your input.', 'November 2026', about_secs)))

    # Contact
    contact_secs = [
        ('Get in touch', '<p>If a tool gives a result you did not expect, a page is unclear, or you have a suggestion, we would like to hear about it.</p>'
         + ('<p><strong>Email:</strong> <a href="mailto:' + CONTACT_EMAIL + '">' + CONTACT_EMAIL + '</a></p>' if CONTACT_EMAIL else
            '<p>CalcHub does not publish a contact email address, because no monitored inbox has been confirmed. If you are reading this on a hosted preview or in the project repository, use that platform\u2019s issue tracker or feedback channel to reach the maintainers.</p>')
         + '<p>Please do not send passwords, personal data or confidential material through any channel.</p>'),
        ('What to include', '<ul><li>Which tool or page you are writing about.</li><li>What you expected to happen and what happened instead.</li><li>Your browser and device, if the problem is visual or interactive.</li><li>For a calculation, the numbers you entered and the result you saw.</li></ul>'),
        ('Response times', '<p>CalcHub is a small independent project with no formal support desk. We read feedback, but we cannot guarantee a reply to every message or a fix on any particular timeline.</p>'),
    ]
    pages.append(('contact', legal_page('contact', 'Contact Us', 'Send feedback, a correction or a bug report about a CalcHub tool.', 'November 2026', contact_secs)))

    # Privacy
    privacy_secs = [
        ('Introduction', '<p>This Privacy Policy explains what happens to information when you use ' + SITE_NAME + '. The short version: the tools process your input in your browser, and we do not collect it.</p>'),
        ('Information we collect', '<p>We operate a static website with no user accounts and no database of visitors. You do not need to provide a name, email address or any other personal details to use a tool.</p><p>CalcHub itself does not collect or store visitor information. The company hosting these pages may record standard technical data such as IP address and browser type while delivering them; that is handled under the host\u2019s own policy, not by CalcHub.</p>'),
        ('Cookies and local storage', '<p>We do not set cookies and we do not run advertising. The only browser storage used is localStorage in the two counter tools, and only if you tick the optional "Keep count after refresh" checkbox. That number stays on your device; unticking the box or clearing site data removes it.</p>'),
        ('Analytics', '<p>We do not use Google Analytics, Cloudflare Analytics or any other analytics service. We do not run advertising pixels or trackers, and we never log the content you type into a tool.</p>'),
        ('Local processing of tool data', '<p>All tool processing happens in your browser using standard Web APIs such as Canvas, File, Blob, Clipboard, Web Crypto and Intl. Your text, uploaded images and calculated values are not uploaded to our server, are not stored by us, and disappear when you close the page.</p>'),
        ('Third-party services', '<p>We do not load third-party fonts, analytics or advertising scripts. The only bundled third-party code is the open-source QR code generator library, which is served from this site itself and runs locally in your browser. Your hosting provider delivers the static pages under its own privacy policy.</p>'),
        ('Data security', '<p>Because we do not collect tool inputs or account data, there is little personal data for us to protect. The pages are served over HTTPS by the hosting provider.</p>'),
        ('Your rights', '<p>Depending on where you live (for example, under the GDPR or CCPA), you may have rights to access, correct or delete personal data. Since we do not collect tool inputs or account data, there is generally nothing to access or delete. To raise a privacy question, use the <a href="/contact/">Contact</a> page.</p>'),
        ('Changes to this policy', '<p>We may update this policy when the site or the law changes. The "Last updated" date at the top of this page reflects the latest revision.</p>'),
    ]
    pages.append(('privacy-policy', legal_page('privacy-policy', 'Privacy Policy', 'How CalcHub handles your information: tools run in your browser, no accounts, no analytics and a clear note on local storage.', 'November 2026', privacy_secs)))

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
    pages.append(('terms', legal_page('terms', 'Terms of Use', 'The terms that apply when you use CalcHub, including disclaimers on results and the no-warranty section.', 'November 2026', terms_secs)))

    # Disclaimer
    disc_secs = [
        ('General information only', '<p>The tools and content on ' + SITE_NAME + ' are provided for general informational and utility purposes. They are not professional advice.</p>'),
        ('Calculations and estimates', '<p>Results from calculators, converters, timers and other tools are based on common formulas and are provided for convenience. They may not suit professional, legal, medical or financial decisions. For example, BMI is a screening measure and not a medical diagnosis, and reading time is an estimate based on an assumed reading speed.</p>'),
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
            '<rect width="64" height="64" rx="15" fill="#2563eb"/>'
            '<path d="M44 21a14 14 0 1 0 0 22" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round"/>'
            '<circle cx="44" cy="32" r="4" fill="#93c5fd"/></svg>\n')

# ---------------- Writer ----------------
def ensure_dirs():
    dirs = [os.path.join(ROOT, 'tools'), os.path.join(ROOT, 'category'), os.path.join(ROOT, 'assets', 'js')]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

import re as _re

# Single source of truth for link resolution on GitHub Pages project sites.
# HTML static links and JS-generated links share the SAME prefix, computed once
# per page in _localize_paths (relative form), which works for both the
# /calchub/ subpath deployment and local file:// preview. Keep this constant in
# sync with the deployment subpath; it is documentation/validation only — the
# runtime prefix is injected as <meta name="calchub-base"> below.
BASE_PATH = '/calchub/'

def _localize_paths(rel, content):
    """Convert site-root paths (/assets/..., /tools/...) into paths relative
    to the current page, so GitHub Pages subpath (/calchub/) and local file
    preview both work. Full URLs (canonical/og/JSON-LD) are untouched because
    they never start with a bare '/'. tools-data.js and SEO text files skip.

    The same `prefix` is injected as <meta name="calchub-base"> so that JS
    dynamic links (search dropdown, search submit) resolve against exactly the
    same base as the static HTML links — no second pathname-derived mechanism."""
    if not rel.endswith('.html'):
        return content
    depth = rel.count('/')  # e.g. index.html=0, tools/x/index.html=2
    prefix = '../' * depth
    # Inject the unified base token once, before any HTML link rewriting.
    if '<head>' in content and 'name="calchub-base"' not in content:
        content = content.replace('<head>',
                                  '<head>\n<meta name="calchub-base" content="' + prefix + '">',
                                  1)
    def repl(m):
        attr, path = m.group(1), m.group(2)
        if path.startswith('/'):
            return '%s="%s%s"' % (attr, prefix, path[1:])
        return m.group(0)
    return _re.sub(r'(href|src)="(/[^"]*)"', repl, content)

def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(_localize_paths(rel, content))
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