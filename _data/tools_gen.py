# -*- coding: utf-8 -*-
"""CalcHub tool registry — Part 4: Generators & Converters (6).

Randomness claims are limited to what the code actually does: Web Crypto via
secureRandomInt, rejection sampling for integers, a 32-bit value scaled for
decimals, crypto.randomUUID for v4 identifiers. The password entropy figure
is an estimate (length x log2(pool)), not a security guarantee.
"""

GENERATOR_TOOLS = [
    {
        "slug": "password-generator",
        "name": "Password Generator",
        "cat": "gen",
        "popular": True,
        "icon": "Pw",
        "title": "Password Generator — Random Passwords With a Strength Estimate | CalcHub",
        "desc": "Generate a random password with your chosen length and character sets using browser cryptography. See an entropy estimate and what it does not guarantee.",
        "h1": "Password Generator",
        "lede": "Choosing a password yourself tends to produce something guessable. Set the length and character types here, and the browser creates a random string without sending it anywhere.",
        "howto": [
            "Set the length with the slider, from 4 to 64 characters. It starts at 16.",
            "Tick the character types you need: uppercase, lowercase, numbers and symbols. At least one type must stay selected.",
            "Click Generate new password. The strength bar and the bit estimate update with it.",
            "Use the copy button, then save the password in a password manager."
        ],
        "examples": [
            "16 characters with all four sets selected gives an estimate of about 104 bits and a Very strong label.",
            "8 lowercase-only characters drops to about 38 bits and reads as Weak — length matters more than any single character type.",
            "For a site that rejects symbols, untick Symbols and add a few characters of length instead."
        ],
        "understanding": [
            "Randomness comes from the browser's Web Crypto API. Each character is drawn with an unbiased rejection-sampling method over the character sets you enabled, and the finished string is shuffled with the same source so no position is privileged. The tool makes sure at least one character from every selected set appears before filling the rest.",
            "The strength label is an entropy estimate: password length multiplied by log2 of the size of the combined character pool. More length and a larger pool raise the number. It is a useful way to compare settings, not a measurement of how long an attacker would need."
        ],
        "limitations": [
            "No generated password is impossible to crack. A password can also be reused, phished, exposed in a breach or simply lost. Length and randomness reduce one kind of risk, not all of them.",
            "The entropy figure assumes every character is drawn independently from the full pool. Because the tool deliberately includes one character from each selected set, the true figure differs slightly. Treat the label as a guide.",
            "The strength label does not check whether a password has appeared in a known breach or resembles a common pattern.",
            "The password is displayed on screen and, if you use the copy button, sits on your system clipboard where other applications may read it. Clear it when you are done.",
            "Symbols are limited to the set !@#$%^&*()_+-=[]{}|;:,.<>? Some sites reject particular characters; untick Symbols and use a longer password instead.",
            "Store the result in a trusted password manager. This page does not keep it for you, and reloading generates a different value."
        ],
        "privacy": "Passwords are created in your browser and are never uploaded, logged or stored. The site runs no analytics that could capture them.",
        "faq": [
            {"q": "Is this really random?", "a": "Yes, in the sense that characters come from the browser's cryptographic random source rather than a predictable pseudo-random generator. Integers are drawn with rejection sampling to avoid bias, and the result is shuffled with crypto randomness too."},
            {"q": "What length should I use?", "a": "The default of 16 characters with several character sets is a reasonable starting point. If a site imposes a shorter maximum, keep as many character types as it allows and use its full length. Length contributes more to the estimate than adding one more symbol type."},
            {"q": "Are my passwords stored?", "a": "No. Nothing is uploaded, written to browser storage or logged, and the site has no analytics. A new value is generated when the page loads, and the previous one cannot be recovered."},
            {"q": "Does a Very strong label mean it cannot be cracked?", "a": "No. It reflects an entropy estimate based on length and character pool. It says nothing about reuse, phishing, a breach on the site you use it with, or whether you have saved the password somewhere safe."}
        ],
        "related": ["uuid-generator", "random-number-generator", "random-name-picker", "qr-code-generator"]
    },
    {
        "slug": "qr-code-generator",
        "name": "QR Code Generator",
        "cat": "gen",
        "popular": True,
        "icon": "Qr",
        "title": "QR Code Generator — Make a QR Code From a URL or Text | CalcHub",
        "desc": "Turn a link or short text into a QR code PNG at 256, 512 or 1024 pixels. Generated locally in your browser, ready to download and print.",
        "h1": "QR Code Generator",
        "lede": "A QR code is a machine-readable way to write a short string — most often a link — so a phone camera can pick it up without typing. Enter the text here and download an image you can print or place on a slide.",
        "howto": [
            "Type a URL or plain text into the field. A sample link is filled in to start with.",
            "Choose an output size: 256, 512 or 1024 pixels square.",
            "The code redraws as you type. Check that a scanner reads the value you intended.",
            "Click Download PNG to save the image."
        ],
        "examples": [
            "A menu link on a table card, so guests open it with their camera instead of typing a URL.",
            "A short piece of text, such as an event code or a contact detail, that a scanner should display rather than open.",
            "A 1024 x 1024 version for a printed poster, where a larger image stays sharp at size."
        ],
        "understanding": [
            "The tool encodes your string with medium error correction (level M), which lets a scanner recover the data if part of the code is slightly damaged or obscured. It draws the pattern onto a canvas with a white quiet zone around it, then exports that canvas as a PNG.",
            "The size setting is the pixel dimensions of the exported square image, not a change to the encoded content. A bigger image gives a scanner more pixels to work with when printed large, but it carries the same string."
        ],
        "limitations": [
            "A QR code says nothing about the safety of its destination. It can point to a phishing page as easily as a legitimate one — check the link before sharing it, and scan a test copy before printing a large batch.",
            "Input is limited to about 1500 characters. Longer strings produce a dense pattern that cameras struggle to read, so the tool refuses them.",
            "The tool produces a static PNG. It does not shorten URLs, track scans, create dynamic codes or let you change the destination after printing.",
            "Very long text, low-contrast printing or a code placed on a curved or reflective surface can fail to scan. Test the printed version.",
            "The QR library is bundled with the site and runs locally; no external service is contacted to build the code."
        ],
        "privacy": "The code is drawn in your browser. Your text is not uploaded or logged.",
        "faq": [
            {"q": "Can I use plain text instead of a URL?", "a": "Yes. Whatever you type is encoded as a string. A scanner will usually open a URL automatically and display plain text for you to read."},
            {"q": "Which size should I choose?", "a": "256 pixels is fine for a screen or a small label. Use 512 or 1024 when the code will be printed large, so the individual squares stay crisp enough for a camera."},
            {"q": "Does a QR code mean the website is safe?", "a": "No. A QR code is only a way of writing a link. It does not verify the site, check its certificate or warn about phishing. Check the destination yourself before sharing it."},
            {"q": "Can I change the link after printing?", "a": "Not with this tool. The code encodes the text you entered, so a change means generating and printing a new one. A redirect at a URL you control is the usual way to keep a printed code flexible."}
        ],
        "related": ["password-generator", "uuid-generator", "random-number-generator", "json-formatter"]
    },
    {
        "slug": "random-number-generator",
        "name": "Random Number Generator",
        "cat": "gen",
        "popular": False,
        "icon": "Rn",
        "title": "Random Number Generator — Integers or Decimals in a Range | CalcHub",
        "desc": "Generate one or many random numbers between a minimum and maximum, with optional decimals and a no-duplicates option. Uses browser cryptography.",
        "h1": "Random Number Generator",
        "lede": "Picking numbers by hand is neither random nor quick when you need twenty of them. Set the range and how many you want; the tool draws them with the browser's cryptographic random source.",
        "howto": [
            "Set Minimum and Maximum. If the minimum is larger, the two are swapped automatically.",
            "Set How many, from 1 to 1000, and choose Decimals: 0 for integers, or 1 to 3 decimal places.",
            "Tick Unique numbers only if repeats are not allowed. It applies to integers only.",
            "Click Generate and copy the comma-separated results."
        ],
        "examples": [
            "A raffle with 100 tickets: Minimum 1, Maximum 100, How many 1, Decimals 0.",
            "Five unique winners from a list of 30: set How many to 5 and tick Unique numbers only.",
            "A set of five decimal values between 0 and 1 for a simulation: set Decimals to 2."
        ],
        "understanding": [
            "Integer draws use an unbiased rejection-sampling method over the inclusive range: a 32-bit value from Web Crypto is accepted only when it falls within a whole multiple of the range size, which avoids favouring low numbers. Decimal draws take a separate 32-bit value, scale it into the range, then round to the number of places you chose.",
            "The output is a plain comma-separated list. Nothing is sorted, labelled or deduplicated for you beyond the Unique option."
        ],
        "limitations": [
            "Unique numbers only works with integers, meaning Decimals set to 0. With decimals enabled the checkbox has no effect, because rounding can produce coincidental repeats.",
            "If you ask for more unique integers than the range contains, the tool reports that the range is too small instead of looping or quietly returning fewer.",
            "Results are independent draws, so the same number can appear more than once unless Unique is ticked. A random draw is not a shuffle of the whole range.",
            "At most 1000 numbers are produced per click. There is no seed and nothing is saved, so a previous set cannot be reproduced — copy the output if you need a record.",
            "This is a convenience tool, not a certified source for cryptographic keys, lotteries or regulated sampling."
        ],
        "privacy": "Numbers are generated in your browser and are not uploaded or stored.",
        "faq": [
            {"q": "Are duplicate values allowed?", "a": "By default, yes — each draw is independent, so a number can repeat. Tick Unique numbers only with Decimals set to 0 to exclude repeats, which is useful for drawing distinct winners."},
            {"q": "How random is it?", "a": "It uses the browser's cryptographic random source rather than a predictable generator. Integers use rejection sampling to remove modulo bias; decimals are scaled from a 32-bit random value."},
            {"q": "Why did I get a 'range too small' message?", "a": "You asked for more unique integers than the range can supply — for example, 10 unique numbers between 1 and 5. Widen the range, lower the count, or untick Unique."},
            {"q": "Can I reproduce the same numbers later?", "a": "No. There is no seed or history, and nothing is stored. Copy the results before you clear the page."}
        ],
        "related": ["password-generator", "uuid-generator", "random-name-picker", "online-counter"]
    },
    {
        "slug": "random-name-picker",
        "name": "Random Name Picker",
        "cat": "gen",
        "popular": False,
        "icon": "Np",
        "title": "Random Name Picker — Draw a Name From a List | CalcHub",
        "desc": "Paste a list of names, one per line, and pick one at random. Optional no-repeat mode for giveaways, classroom selection and team draws.",
        "h1": "Random Name Picker",
        "lede": "Drawing a name from a hat is fair but awkward when the list lives in a spreadsheet. Paste the names here and pick one, with an option to stop a name coming up twice.",
        "howto": [
            "Paste your list into the box, one name per line.",
            "Tick Remove picked name (no repeats) if a name should be excluded once it has been drawn.",
            "Click Pick a name. The result appears above a running history of picks.",
            "Use Reset history to start over with the full list."
        ],
        "examples": [
            "A teacher calling on students: paste the class list and leave no-repeats off so anyone can be picked again.",
            "A giveaway with 50 entrants: tick no-repeats so each person can win once.",
            "Splitting a group into teams: draw one name at a time with no-repeats on and assign each to the next team."
        ],
        "understanding": [
            "Each line is trimmed and empty lines are ignored, so a list with blank rows still works. A pick is drawn uniformly from the eligible names using the browser's cryptographic random source, and the result is added to the top of the history list.",
            "With no-repeats enabled, previously picked names are removed from the pool before each draw. When none remain, the tool says so and waits for a reset. With it off, every name stays eligible on every draw, including the one just picked."
        ],
        "limitations": [
            "Names are matched as exact, case-sensitive text. Two identical lines count as two separate entries, and 'Ana' and 'ana' are different strings — remove duplicates from your list first.",
            "Leading and trailing spaces are trimmed from each line, and blank lines are skipped.",
            "Editing the name list clears the pick history and the no-repeat memory, so paste your final list before you start drawing.",
            "There is no weighting, grouping or seeding. Every eligible name has the same chance, and a previous draw cannot be reproduced.",
            "The tool does not store your list; reloading clears it."
        ],
        "privacy": "Names are processed in your browser and are never uploaded or stored.",
        "faq": [
            {"q": "Does it remove a name after picking?", "a": "Only if you tick Remove picked name (no repeats). Otherwise every name stays in the pool and the same person can be drawn again, which is what you want for repeated classroom questions."},
            {"q": "How are empty lines and duplicates handled?", "a": "Blank lines are skipped, and leading or trailing spaces are trimmed. Duplicates are not removed: two identical lines are two entries, and names differing only by case are treated as different. Clean the list before pasting it."},
            {"q": "Is the draw fair?", "a": "Every eligible name has the same chance on each draw, using the browser's cryptographic random source. There is no audit trail or reproducible seed, so for a regulated prize draw use a process that provides one."},
            {"q": "How do I start over?", "a": "Click Reset history. That clears the list of previous picks and puts every name back in the pool."}
        ],
        "related": ["random-number-generator", "password-generator", "uuid-generator", "click-counter"]
    },
    {
        "slug": "uuid-generator",
        "name": "UUID Generator",
        "cat": "gen",
        "popular": False,
        "icon": "Ud",
        "title": "UUID Generator — Create Version 4 Identifiers | CalcHub",
        "desc": "Generate one to twenty random UUID v4 values in your browser. Learn what a UUID is for and why it is an identifier, not a secret.",
        "h1": "UUID Generator",
        "lede": "When two systems need to label a record without asking each other first, a random 128-bit identifier avoids collisions. This tool generates version 4 UUIDs, one per line, ready to copy.",
        "howto": [
            "Set How many UUIDs, from 1 to 20.",
            "Click Generate UUIDs. Each value appears on its own line.",
            "Use Copy all to take the whole set.",
            "Generate again for a fresh batch."
        ],
        "examples": [
            "A database row id created on the client before the record is sent to a server.",
            "A correlation id attached to a log entry so a request can be traced across services.",
            "A temporary key for an item in a local cache or a test fixture."
        ],
        "understanding": [
            "A UUID is a 128-bit value written as 32 hexadecimal digits in five groups, such as 3f8a1c2e-9b44-4d7f-a1e0-6c5b2d9f8a13. Version 4 means the bits are generated randomly, apart from the fixed version and variant markers, rather than derived from a timestamp or a name.",
            "The tool uses the browser's crypto.randomUUID when available and otherwise builds the same version 4 layout from cryptographically random bytes. Each call produces a new, independent set of values."
        ],
        "limitations": [
            "UUIDs are identifiers, not secrets. They are not authentication tokens, passwords, API keys or session cookies, and an exposed value should not be treated as a credential.",
            "Randomness makes collisions extremely unlikely, not impossible. If uniqueness is critical, keep a uniqueness constraint at the storage layer as well.",
            "Version 4 UUIDs contain no timestamp or ordering information, so sorting them does not sort by creation time.",
            "At most 20 are generated per batch, and nothing is stored or seeded, so a previous set cannot be reproduced.",
            "The tool does not check whether a generated UUID is already in use in your system."
        ],
        "privacy": "UUIDs are created in your browser and are not uploaded or logged.",
        "faq": [
            {"q": "What is UUID version 4?", "a": "A 128-bit identifier whose bits are random, with a few fixed bits marking the version and variant. It is the most common form for identifiers generated without a central authority."},
            {"q": "Can I use these as passwords or API tokens?", "a": "No. A UUID is a label, not a secret. It is often visible in URLs and logs, and it is not designed to resist guessing the way a credential must. Use the Password Generator for credentials."},
            {"q": "Will two UUIDs ever collide?", "a": "The probability is extremely small, but it is not zero. For systems where a collision would be serious, still enforce uniqueness where the data is stored."},
            {"q": "Do UUIDs sort by creation time?", "a": "Not version 4. There is no timestamp embedded in the value, so lexical order is effectively random. Other UUID versions do encode time, but this tool generates version 4."}
        ],
        "related": ["password-generator", "random-number-generator", "json-formatter", "qr-code-generator"]
    },
    {
        "slug": "json-formatter",
        "name": "JSON Formatter & Validator",
        "cat": "gen",
        "popular": True,
        "icon": "{}",
        "title": "JSON Formatter & Validator — Pretty-Print and Check JSON | CalcHub",
        "desc": "Format, minify and validate JSON in your browser. See common syntax errors with their position, and learn what reformatting does and does not change.",
        "h1": "JSON Formatter & Validator",
        "lede": "A single missing comma can make an API response unreadable in a log. Paste JSON here to check whether it parses, then format it into something you can actually read.",
        "howto": [
            "Paste JSON into the input box. A small example is provided to start with.",
            "Choose Indentation: 2 spaces, 4 spaces, Tab, or Minified.",
            "Click Format / Minify to produce the output, or Validate to check syntax without reformatting.",
            "Use Copy output or Clear to manage the result."
        ],
        "examples": [
            "A compact object such as {\"name\":\"CalcHub\",\"tools\":30} becomes an indented, multi-line object at 2-space indentation.",
            "A trailing comma such as {\"a\":1,} fails validation, and the message points to the character position where parsing stopped.",
            "Minified strips the whitespace back out for a compact payload to paste into a config file."
        ],
        "understanding": [
            "Formatting runs JSON.parse followed by JSON.stringify with the indentation you chose. Validation runs the parse on its own and reports the browser's error message, including a character position when one is available. Minified uses no indentation at all.",
            "Reformatting changes whitespace and escaping, not the underlying data. The same keys, values, array order and nesting come back out; a number written as 1.0 is displayed as 1 because JSON has one numeric type. Formatting also discards things JSON.parse rejects, such as comments, and a duplicate key keeps only its last value.",
            "The mistakes that fail validation are usually small: a trailing comma after the last item, single quotes instead of double quotes, an unquoted key, a missing closing bracket or brace, an unescaped line break inside a string, or a // comment copied from JavaScript. JSON requires double-quoted keys and strings, no comments and no trailing commas."
        ],
        "limitations": [
            "The tool reports syntax errors but does not repair them. Use the position in the message to find the character, fix it in the input and validate again.",
            "It does not check a schema, data types, required fields or business rules. Valid JSON can still be the wrong shape for your application.",
            "Formatting normalises the text: numbers may lose trailing zeros, and duplicate keys collapse to the last occurrence. Do not rely on it to preserve the exact byte-for-byte source.",
            "Very large documents depend on your browser's memory and may be slow to stringify.",
            "Nothing is sent to a server, but the JSON remains in the input box only while the page is open."
        ],
        "privacy": "Your JSON is parsed and formatted in your browser. It is never uploaded or stored.",
        "faq": [
            {"q": "What does an error message look like?", "a": "It starts with 'Invalid JSON:' followed by the browser's parse message, and includes a character position when the browser provides one. For {\"a\":1,} the parser stops near the closing brace, which is where the trailing comma sits."},
            {"q": "Does formatting change my data?", "a": "No. Keys, values, order and nesting are preserved. What changes is presentation: whitespace, escaping and numeric notation. A value of 1.0 becomes 1, and comments — which are not valid JSON — are rejected rather than kept."},
            {"q": "Can I use tabs for indentation?", "a": "Yes. Choose Tab from the Indentation dropdown, along with 2 spaces, 4 spaces or Minified. The same dropdown controls whether Format produces pretty output or a compact one."},
            {"q": "Why does Validate say it is valid but my app still rejects it?", "a": "Validation checks syntax only. Your application may also require particular fields, types or a specific structure, which this tool does not inspect."}
        ],
        "related": ["uuid-generator", "qr-code-generator", "password-generator", "random-number-generator"]
    },
]
