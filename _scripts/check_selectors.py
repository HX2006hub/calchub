# -*- coding: utf-8 -*-
"""Cross-check runner $()/[data-*] selectors against generated tool pages.
Offline, static only. Factory-based runners are checked leniently."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
js = (ROOT / 'assets/js/tools.js').read_text(encoding='utf-8')

# Split on the numbered section comments that precede each runner/factory so
# factory helpers (timers/counters/converters) don't bleed into the prior block.
markers = list(re.finditer(r'/\*\s*-+\s*(\d+)\s+([a-z0-9-]+)\s*-+\s*\*/', js))
blocks = {}
for idx, m in enumerate(markers):
    end = markers[idx + 1].start() if idx + 1 < len(markers) else len(js)
    blocks[m.group(2)] = js[m.end():end]

sel_re = re.compile(r"\$\$?\(\s*'\[data-([A-Za-z0-9_-]+)(?:=\"[^\"]*\")?\]'")
missing = []
for slug, code in sorted(blocks.items()):
    page = ROOT / 'tools' / slug / 'index.html'
    if not page.exists():
        continue
    html = page.read_text(encoding='utf-8')
    # factory runners share one code body; restrict branch-specific selectors
    branch_only = {'online-counter': {'bigbtn'}, 'click-counter': {'plus', 'minus'}}
    # optional selectors with an explicit `|| root` fallback are valid when absent
    optional = set(re.findall(r"\$\(\s*'\[data-([A-Za-z0-9_-]+)\]'\s*,\s*root\s*\)\s*\|\|\s*root", code))
    for attr in sorted(set(sel_re.findall(code))):
        if attr in optional:
            continue
        if attr in branch_only.get(slug, set()):
            continue
        if 'data-' + attr not in html:
            missing.append((slug, attr))

print('Direct runners:', len(blocks))
if missing:
    print('Selectors not found on page (manual review needed):')
    for slug, attr in missing:
        print(' -', slug, 'data-' + attr)
else:
    print('All direct-runner data-* selectors resolve on their pages.')
