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

## License

Private repository — all rights reserved.
