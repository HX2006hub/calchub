# -*- coding: utf-8 -*-
"""CalcHub tool registry — Part 4: Generators & Converters (6)."""

GENERATOR_TOOLS = [
    {
        "slug": "password-generator",
        "name": "Password Generator",
        "cat": "gen",
        "popular": True,
        "icon": "Pw",
        "title": "Password Generator – Secure Random Passwords | CalcHub",
        "desc": "Generate strong, secure random passwords in your browser using crypto-grade randomness. Free password generator with custom length and character sets.",
        "h1": "Password Generator",
        "lede": "Create strong, random passwords on your own device using cryptographically secure randomness. Choose the length and character types you need — nothing is stored, logged or transmitted.",
        "howto": [
            "Choose a password length (we recommend at least 14 characters).",
            "Tick the character types you want: uppercase, lowercase, numbers and symbols.",
            "Click Generate for a new random password.",
            "Copy the password securely to your clipboard."
        ],
        "examples": [
            "A 16-character password with all four character types has roughly 100 bits of entropy.",
            "Generate a unique password for a new account instead of reusing one.",
            "Create a strong master password that is easy for you to type but hard to guess."
        ],
        "features": [
            "Cryptographically secure randomness (Web Crypto, not Math.random)",
            "Custom length from 4 to 128 characters",
            "Selectable character sets",
            "Copy to clipboard",
            "Passwords are never stored or transmitted"
        ],
        "privacy": "Passwords are generated locally using your browser's Web Crypto API. They are never stored, never sent to a server, and disappear when the page closes.",
        "faq": [
            {"q": "Is this really random?", "a": "Yes. We use the Web Crypto API's crypto.getRandomValues(), a cryptographically secure random source approved for security-sensitive use. We do not use Math.random()."},
            {"q": "What password length should I use?", "a": "12+ characters is a good minimum for most accounts; 16+ is better for anything important. Longer passwords add more entropy and are harder to brute-force."},
            {"q": "Are my passwords stored?", "a": "No. They exist only in your browser's memory. Close the page and they are gone. Consider using a reputable password manager to store them."}
        ],
        "related": ["uuid-generator", "random-number-generator", "random-name-picker", "qr-code-generator"]
    },
    {
        "slug": "qr-code-generator",
        "name": "QR Code Generator",
        "cat": "gen",
        "popular": True,
        "icon": "Qr",
        "title": "QR Code Generator – Create QR Codes Online Free | CalcHub",
        "desc": "Generate QR codes from text or URLs in your browser. Free online QR code generator with preview, size options and PNG download.",
        "h1": "QR Code Generator",
        "lede": "Turn a URL or any short text into a scannable QR code. Preview it instantly, choose the size, and download it as a PNG for print or web use.",
        "howto": [
            "Type a URL or any text into the input.",
            "The QR code preview updates automatically.",
            "Pick the size you need (256–1024 px).",
            "Download the QR code as a PNG."
        ],
        "examples": [
            "Generate a QR code for a business card linking to your website.",
            "Add a QR code to a poster for a product page or event.",
            "Create a Wi-Fi or contact code placeholder (text-based) for testing."
        ],
        "features": [
            "QR code from any text or URL",
            "Instant preview",
            "Size selection up to 1024 px",
            "PNG download",
            "Empty input and very long input warnings"
        ],
        "privacy": "QR codes are generated locally using a bundled open-source library. Your input is not sent to any server.",
        "faq": [
            {"q": "What can I put in a QR code?", "a": "Any text, but a URL is most common. Email addresses, plain text and short IDs also work. Very long inputs create denser codes that are harder to scan."},
            {"q": "Why is my input too long?", "a": "QR codes have a practical capacity limit. Text over a few hundred characters may not fit or may become too dense to scan reliably. We warn you when that happens."},
            {"q": "Can I use the PNG anywhere?", "a": "Yes. It is a standard PNG you can use in print, websites or documents, as long as the code remains readable."}
        ],
        "related": ["password-generator", "uuid-generator", "random-number-generator", "json-formatter"]
    },
    {
        "slug": "random-number-generator",
        "name": "Random Number Generator",
        "cat": "gen",
        "popular": False,
        "icon": "Rn",
        "title": "Random Number Generator – Pick Random Numbers Free | CalcHub",
        "desc": "Generate random numbers in any range, with options for count, uniqueness and decimals. Free online random number generator.",
        "h1": "Random Number Generator",
        "lede": "Generate one or many random numbers inside any range you set. Choose whether numbers can repeat and whether you want integers only or decimals.",
        "howto": [
            "Enter a minimum and maximum value.",
            "Set how many numbers you need.",
            "Choose whether repeats are allowed.",
            "Click Generate and copy the result."
        ],
        "examples": [
            "Pick a number between 1 and 100 for a classroom raffle.",
            "Generate 10 unique integers between 1 and 50 for a contest.",
            "Roll a single random decimal between 0 and 1 for a decision."
        ],
        "features": [
            "Custom minimum and maximum",
            "Multiple numbers at once",
            "Unique or repeatable results",
            "Integers or decimals"

        ],
        "privacy": "Numbers are generated locally in your browser. No input is stored or sent.",
        "faq": [
            {"q": "Is the randomness fair?", "a": "We use a cryptographically secure random source where available, falling back to a tested seeded generator. The distribution is uniform across the valid range."},
            {"q": "Can I get unique numbers only?", "a": "Yes. Toggle 'Allow repeats' off. If the range is too small for the requested count, we warn you instead of looping forever."},
            {"q": "Does it support negative ranges?", "a": "Yes. Minimum and maximum can be negative, so ranges like −10 to 10 work fine."}
        ],
        "related": ["password-generator", "uuid-generator", "random-name-picker", "online-counter"]
    },
    {
        "slug": "random-name-picker",
        "name": "Random Name Picker",
        "cat": "gen",
        "popular": False,
        "icon": "Np",
        "title": "Random Name Picker – Choose a Random Name Free | CalcHub",
        "desc": "Enter a list of names and pick one randomly. Free online name picker, processed entirely in your browser.",
        "h1": "Random Name Picker",
        "lede": "Paste a list of names — one per line — and pick one at random. Great for giveaways, classroom selection, team picking and friendly draws.",
        "howto": [
            "Paste or type names, one per line.",
            "Add more names with the quick-add field if you like.",
            "Click Pick a Name.",
            "See the winner; keep going or clear to start over."
        ],
        "examples": [
            "Choose a winner from 50 giveaway entries.",
            "Pick who presents first at a team meeting.",
            "Select a random participant for a classroom activity."
        ],
        "features": [
            "Paste any list, one name per line",
            "Random pick with a single click",
            "Option to remove picked names",
            "100% local processing"
        ],
        "privacy": "Names are processed locally in your browser. They are never uploaded to or stored on a server.",
        "faq": [
            {"q": "Does it remove the name after picking?", "a": "You can choose 'Remove picked name' to prevent repeats, or leave it off to allow the same name to be picked again."},
            {"q": "Can I use it for a large list?", "a": "Yes, within reasonable limits. Thousands of names work, though extremely large lists are slower to process."},
            {"q": "Is it fair?", "a": "Yes. We use a secure random source, so each name has an equal chance."}
        ],
        "related": ["random-number-generator", "password-generator", "uuid-generator", "click-counter"]
    },
    {
        "slug": "uuid-generator",
        "name": "UUID Generator",
        "cat": "gen",
        "popular": False,
        "icon": "Ud",
        "title": "UUID v4 Generator – Generate UUIDs Online Free | CalcHub",
        "desc": "Generate RFC 4122 UUID v4 values using secure randomness. Free online UUID generator (GUID) for databases, APIs and testing.",
        "h1": "UUID v4 Generator",
        "lede": "Generate standards-compliant UUID v4 (random) values on demand. Useful for database keys, API identifiers, test data and any place a unique ID is required.",
        "howto": [
            "Choose how many UUIDs you need (1–20).",
            "Click Generate.",
            "Copy a single UUID or the whole list."
        ],
        "examples": [
            "Create unique primary keys for a new database table.",
            "Generate test identifiers for API responses.",
            "Add IDs to rows in a migration or seed script."
        ],
        "features": [
            "RFC 4122 version 4 UUIDs",
            "Secure randomness via crypto.getRandomValues()/randomUUID",
            "Generate 1–20 at once",
            "Copy single or all values"
        ],
        "privacy": "UUIDs are generated locally. No values are stored, logged or transmitted.",
        "faq": [
            {"q": "Are these real UUIDs?", "a": "Yes. They follow RFC 4122 version 4 format (random). The version and variant bits are set correctly, so they are valid as database keys and identifiers."},
            {"q": "Is UUID slightly different from GUID?", "a": "For practical purposes, GUID is Microsoft's name for the same format. A generated UUID v4 works anywhere a GUID is expected."},
            {"q": "Can two generated UUIDs collide?", "a": "In principle any random ID can collide, but the 122 random bits in a UUID v4 make practical collision probabilities negligible for normal workloads."}
        ],
        "related": ["password-generator", "random-number-generator", "json-formatter", "qr-code-generator"]
    },
    {
        "slug": "json-formatter",
        "name": "JSON Formatter & Validator",
        "cat": "gen",
        "popular": True,
        "icon": "{}",
        "title": "JSON Formatter & Validator – Format JSON Online Free | CalcHub",
        "desc": "Format, validate and minify JSON with error highlighting. Free online JSON formatter for developers, processed entirely in your browser.",
        "h1": "JSON Formatter & Validator",
        "lede": "Paste JSON to format it with clean indentation, validate it for errors, or minify it to save space. Errors point to the location that caused the problem.",
        "howto": [
            "Paste or type JSON into the editor.",
            "Choose Format to indent it or Minify to compact it.",
            "Validation happens automatically — errors show position and message.",
            "Copy the formatted result."
        ],
        "examples": [
            "Format minified API responses before debugging.",
            "Validate a config file before deploying it.",
            "Minify a JSON payload to reduce transfer size."
        ],
        "features": [
            "JSON formatting with 2 or 4 space indentation",
            "Minification",
            "Validation with error position reporting",
            "Handles large inputs without freezing the page",
            "Local processing only"
        ],
        "privacy": "Your JSON is processed entirely in your browser and is never sent to a server.",
        "faq": [
            {"q": "What does an error message look like?", "a": "If your JSON is invalid, we show the line and column where parsing failed, plus a short message such as 'Unexpected token at position 123'."},
            {"q": "Does it handle large JSON files?", "a": "Yes. Formatting is done in a non-blocking way so large inputs do not freeze the page. Extremely large inputs may still be slow on low-end devices."},
            {"q": "Can I use tabs for indentation?", "a": "Yes. We offer 2 spaces, 4 spaces and tab indentation."}
        ],
        "related": ["uuid-generator", "qr-code-generator", "password-generator", "random-number-generator"]
    },
]