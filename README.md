# CalcHub

Free online tools for everyday tasks — word counters, image tools, calculators, generators, timers and more. No signup required; everything runs directly in your browser, so your text, files and numbers never leave your device.

## Overview

CalcHub is a lightweight, static-site collection of 30+ browser-based tools across six categories:

- **Text Tools** — word/character counters, case converter, duplicate-line remover, lorem ipsum generator, reading time
- **Image & File Tools** — compress, resize, crop, convert images, generate favicons (all client-side)
- **Calculators** — percentage, age, date difference, unit, BMI, discount
- **Generators & Converters** — password, QR code, UUID, random number/name, JSON formatter
- **Time & Productivity** — countdown, stopwatch, Pomodoro timer, time zone converter
- **Counters & Trackers** — click counter, online counter

## Structure

```
.
├── index.html          # Home page
├── tools/              # Individual tool pages
├── category/           # Category landing pages
├── assets/             # CSS, JS, vendored libraries
├── _data/              # Python data sources for tool metadata
├── _scripts/build.py   # Static build script
├── sitemap.xml
└── robots.txt
```

The site has no backend and no build step required to view — open `index.html` via any static server. `assets/js/tools-data.js` holds the tool catalog used for search and listings.

## Build

```bash
python3 _scripts/build.py
```

The script is deterministic: it regenerates all 30 tool pages, the home page,
`/tools/`, 6 category pages, search, 404, 5 policy pages, `tools-data.js`,
`sitemap.xml`, `robots.txt` and `favicon.svg` from the registries in `_data/`.
Edit tool metadata/content in `_data/tools_*.py` and widget markup or page
templates in `_scripts/build.py`; edit tool logic in `assets/js/tools.js`.
Do not hand-edit generated HTML — the next build will overwrite it.

## Third-party dependencies

- `assets/vendor/qrcode-generator.min.js` — QR Code Generator for JavaScript,
  Copyright (c) 2009 Kazuhiko Arase, MIT License. Full notice in
  `assets/vendor/LICENSE-qrcode-generator.txt`. Bundled locally, loaded only
  on the QR tool page. "QR Code" is a trademark of DENSO WAVE INCORPORATED.
- No other third-party runtime libraries, fonts, analytics or ad scripts.

## Before go-live (owner decisions required)

- `SITE_URL` in `_scripts/build.py` is a placeholder canonical origin. Set it
  to the real production origin before publishing, then rebuild. Do not ship
  the placeholder canonical in production.
- No contact email is published because no monitored inbox has been confirmed.
  Set `CONTACT_EMAIL` only when a real address exists, then rebuild.

## License

Original site code and copy: private, all rights reserved. The bundled QR
library remains under its own MIT license (see above).
