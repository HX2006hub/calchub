# -*- coding: utf-8 -*-
"""Unified inline SVG icon system for CalcHub (Lucide-style, stroke 1.8).

Zero dependencies. Every icon is drawn on a 24x24 viewBox with
stroke="currentColor" so it inherits the surrounding text colour.
Used by the build script to render tool icons, category icons and UI glyphs.
"""

# Shared wrapper: paths are the raw inner SVG of a 24x24 Lucide icon.
_PATHS = {
    # --- Tools: Text & Writing ---
    'word-counter': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/>',
    'character-counter': '<path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/>',
    'reading-time': '<path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/>',
    'text-case-converter': '<path d="m3 15 4-8 4 8"/><path d="M4.5 12h5"/><path d="M15 12V7h5"/><path d="M15 12v5h5"/>',
    'remove-duplicate-lines': '<path d="M8 6h13"/><path d="M8 12h13"/><path d="M8 18h13"/><path d="M3 6h.01"/><path d="M3 12h.01"/><path d="M3 18h.01"/>',
    'lorem-ipsum-generator': '<path d="M15 12H3"/><path d="M17 18H3"/><path d="M21 6H3"/>',

    # --- Tools: Image & File ---
    'image-compressor': '<rect width="18" height="18" x="3" y="3" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.1-3.1a2 2 0 0 0-2.8 0L6 21"/><path d="M9 21h4"/>',
    'image-resizer': '<path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="M21 3l-7 7"/><path d="M3 21l7-7"/>',
    'jpg-to-png': '<path d="M4 22h14a2 2 0 0 0 2-2V7.5L14.5 2H6a2 2 0 0 0-2 2v4"/><path d="M14 2v6h6"/><rect width="8" height="7" x="2" y="13" rx="1"/><circle cx="6" cy="16.5" r="1"/>',
    'png-to-webp': '<path d="M4 22h14a2 2 0 0 0 2-2V7.5L14.5 2H6a2 2 0 0 0-2 2v4"/><path d="M14 2v6h6"/><path d="m3 17 2-2 2 2 2-2"/>',
    'image-cropper': '<path d="M6 2v14a2 2 0 0 0 2 2h14"/><path d="M18 22V8a2 2 0 0 0-2-2H2"/>',
    'favicon-generator': '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/><path d="m12 8 1.2 2.6 2.8.3-2.1 1.9.6 2.7L12 13.8l-2.5 1.7.6-2.7-2.1-1.9 2.8-.3z"/>',

    # --- Tools: Calculators ---
    'percentage-calculator': '<path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    'age-calculator': '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/><path d="M8 14h.01"/><path d="M12 14h.01"/><path d="M8 18h.01"/>',
    'date-difference': '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/><path d="M8 14h8"/><path d="M8 18h5"/>',
    'unit-converter': '<path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/>',
    'bmi-calculator': '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    'discount-calculator': '<path d="M12.6 2.6A2 2 0 0 0 11.2 2H4a2 2 0 0 0-2 2v7.2a2 2 0 0 0 .6 1.4l8.7 8.7a2.4 2.4 0 0 0 3.4 0l6.6-6.6a2.4 2.4 0 0 0 0-3.4z"/><circle cx="7.5" cy="7.5" r="1" fill="currentColor" stroke="none"/>',

    # --- Tools: Generators & Converters ---
    'password-generator': '<path d="M2.6 17.4A2 2 0 0 0 2 18.8V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.2a2 2 0 0 0 1.4-.6l.8-.8a6.5 6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r="1" fill="currentColor" stroke="none"/>',
    'qr-code-generator': '<rect width="5" height="5" x="3" y="3" rx="1"/><rect width="5" height="5" x="16" y="3" rx="1"/><rect width="5" height="5" x="3" y="16" rx="1"/><path d="M21 16h-3a2 2 0 0 0-2 2v3"/><path d="M12 7v3a2 2 0 0 1-2 2H7"/><path d="M12 16v.01"/><path d="M16 12h1"/><path d="M21 12v.01"/>',
    'random-number-generator': '<rect x="2" y="2" width="16" height="16" rx="2"/><path d="M6.5 6.5h.01"/><path d="M11 6.5h.01"/><path d="M15.5 6.5h.01"/><path d="M6.5 11h.01"/><path d="M11 11h.01"/><path d="M15.5 11h.01"/><path d="M7 22h11a3 3 0 0 0 3-3V8"/>',
    'random-name-picker': '<path d="m18 14 4 4-4 4"/><path d="m18 2 4 4-4 4"/><path d="M2 18h3c.8 0 1.5-.4 1.9-1.1L12 9"/><path d="M22 2h-3c-.8 0-1.5.4-1.9 1.1L12 11"/>',
    'uuid-generator': '<path d="M4 9h16"/><path d="M4 15h16"/><path d="M10 3 8 21"/><path d="M16 3l-2 18"/>',
    'json-formatter': '<path d="M8 3H7a2 2 0 0 0-2 2v5a2 2 0 0 1-2 2 2 2 0 0 1 2 2v5a2 2 0 0 0 2 2h1"/><path d="M16 21h1a2 2 0 0 0 2-2v-5a2 2 0 0 1 2-2 2 2 0 0 1-2-2V5a2 2 0 0 0-2-2h-1"/>',

    # --- Tools: Time & Productivity ---
    'countdown-timer': '<path d="M10 2h4"/><path d="M12 14l3-3"/><circle cx="12" cy="14" r="8"/>',
    'stopwatch': '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2 2"/><path d="M9 2h6"/><path d="M19 8l2-2"/>',
    'pomodoro-timer': '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2"/><path d="M9 2h6"/><path d="m5 3-2 2"/>',
    'time-zone-converter': '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/><path d="M12 8v4l2 2"/>',

    # --- Tools: Counters & Trackers ---
    'online-counter': '<path d="M4 9h16"/><path d="M4 15h16"/><path d="M10 3 8 21"/><path d="M16 3l-2 18"/><circle cx="18" cy="6" r="3" fill="currentColor" stroke="none"/>',
    'click-counter': '<path d="m8 3 3 3"/><path d="M13 2v5"/><path d="m18 6-3 3"/><path d="M12 11v9a2 2 0 0 0 3 2l2-2"/><path d="M9 13a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v2a2 2 0 0 0 2 2h1"/>',

    # --- Categories ---
    'cat-text': '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    'cat-image': '<rect width="18" height="18" x="3" y="3" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.1-3.1a2 2 0 0 0-2.8 0L6 21"/>',
    'cat-calc': '<rect width="16" height="20" x="4" y="2" rx="2"/><path d="M8 6h8"/><path d="M8 11h.01"/><path d="M12 11h.01"/><path d="M16 11h.01"/><path d="M8 15h.01"/><path d="M12 15h.01"/><path d="M16 15h.01"/><path d="M8 19h.01"/><path d="M12 19h.01"/>',
    'cat-gen': '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/>',
    'cat-time': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    'cat-count': '<path d="M10 6h11"/><path d="M10 12h11"/><path d="M10 18h11"/><path d="M4 6h1v4"/><path d="M4 10h2"/><path d="M6 18H4c0-1 2-2 2-3s-1-1.5-2-1"/>',

    # --- UI glyphs ---
    'search': '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    'arrow-right': '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
    'arrow-up-right': '<path d="M7 17 17 7"/><path d="M8 7h9v9"/>',
    'check': '<path d="M20 6 9 17l-5-5"/>',
    'copy': '<rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2"/>',
    'download': '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/>',
    'refresh': '<path d="M21 2v6h-6"/><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M3 22v-6h6"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/>',
    'shield': '<path d="M20 13c0 5-3.5 7.5-8 9-4.5-1.5-8-4-8-9V5l8-3 8 3z"/><path d="m9 12 2 2 4-4"/>',
    'bolt': '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
    'gift': '<rect width="18" height="4" x="3" y="8" rx="1"/><path d="M12 8v13"/><path d="M4 12v9a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-9"/><path d="M12 8C9 8 7 7 7 5a2 2 0 0 1 3-1.7C11 4 12 6 12 8z"/><path d="M12 8c3 0 5-1 5-3a2 2 0 0 0-3-1.7C13 4 12 6 12 8z"/>',
    'menu': '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    'close': '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    'chevron-down': '<path d="m6 9 6 6 6-6"/>',
}

CATEGORY_ICON = {
    'text': 'cat-text',
    'image': 'cat-image',
    'calc': 'cat-calc',
    'gen': 'cat-gen',
    'time': 'cat-time',
    'count': 'cat-count',
}


def icon(name, size=20, cls='icon-svg', stroke=1.8):
    """Return an inline SVG icon. Falls back to a neutral dot for unknown names."""
    inner = _PATHS.get(name)
    if inner is None:
        inner = '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="2" fill="currentColor" stroke="none"/>'
    return ('<svg class="%s" width="%d" height="%d" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="%s" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>'
            % (cls, size, size, stroke, inner))


def tool_icon(slug, size=22, cls='icon-svg'):
    return icon(slug, size=size, cls=cls)


def category_icon(cat_id, size=26, cls='icon-svg'):
    return icon(CATEGORY_ICON.get(cat_id, 'cat-gen'), size=size, cls=cls)
