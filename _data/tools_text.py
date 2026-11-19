# -*- coding: utf-8 -*-
"""CalcHub tool registry — Part 1: Text & Writing Tools (6)."""

TEXT_TOOLS = [
    {
        "slug": "word-counter",
        "name": "Word Counter",
        "cat": "text",
        "popular": True,
        "icon": "Aa",
        "title": "Word Counter – Free Online Word Count Tool | CalcHub",
        "desc": "Count words, characters, sentences and paragraphs in text instantly. Free online word counter with live results and no signup required.",
        "h1": "Word Counter",
        "lede": "Count words, characters, sentences and paragraphs in any text instantly. The counter updates live as you type or paste, so you always know exactly where your text stands.",
        "howto": [
            "Type or paste your text into the main text area.",
            "The counts update automatically as you type — no button needed.",
            "Review the breakdown: words, characters, characters without spaces, sentences and paragraphs.",
            "Use the Copy button to copy your text or the Clear button to start over."
        ],
        "examples": [
            "A 500-word blog post usually needs 35–45 sentences and 4–6 paragraphs.",
            "Tweet-style copy has a 280-character limit; the character count shows exactly where you stand.",
            "Paste a full article to see paragraph and sentence counts before you submit it anywhere."
        ],
        "features": [
            "Live word, character, sentence and paragraph counting",
            "Characters with and without spaces",
            "Handles Unicode text, em-dashes, apostrophes and line breaks correctly",
            "Copy and clear actions with one click"
        ],
        "privacy": "Your text never leaves your browser. All counting happens locally on your device, and nothing you paste is stored or sent to a server.",
        "faq": [
            {"q": "How does the word counter treat hyphenated words?", "a": "Words like 'well-known' are counted as a single word, which matches standard word count behaviour. Apostrophes inside words, such as 'don't', also count as one word."},
            {"q": "Does it count emoji and symbols?", "a": "Yes. Emoji and symbols count toward the character total. They are not counted as words unless part of a word-like sequence."},
            {"q": "Is my text saved anywhere?", "a": "No. Everything is processed locally in your browser. Refreshing the page clears your text."}
        ],
        "related": ["character-counter", "reading-time", "text-case-converter", "remove-duplicate-lines"]
    },
    {
        "slug": "character-counter",
        "name": "Character Counter",
        "cat": "text",
        "popular": False,
        "icon": "Cc",
        "title": "Character Counter – Count Characters Online | CalcHub",
        "desc": "Count characters in text instantly, with and without spaces. Free online character counter for social media, forms and SEO meta tags.",
        "h1": "Character Counter",
        "lede": "See exactly how many characters your text contains — including and excluding spaces. Perfect for social media posts, meta descriptions and anywhere a character limit matters.",
        "howto": [
            "Type or paste your text in the input box.",
            "The live count shows total characters and characters without spaces.",
            "Check the breakdown for the number of spaces, lines and words.",
            "Copy the result or the text itself with the buttons provided."
        ],
        "examples": [
            "A good meta description is typically 150–160 characters to avoid truncation in search results.",
            "X posts have a 280-character limit (formerly Twitter); verify before you publish.",
            "Product listing fields often cap at 100–200 characters — check before submitting."
        ],
        "features": [
            "Live character counting with and without spaces",
            "Counts spaces, lines and words too",
            "Works with Unicode, emoji and special characters",
            "Copy and clear buttons"
        ],
        "privacy": "All counting happens locally in your browser. Your text is never uploaded, stored or shared.",
        "faq": [
            {"q": "Do spaces count as characters?", "a": "Yes. The total character count includes spaces. We also show a separate count excluding spaces so you can use whichever your limit requires."},
            {"q": "Are line breaks counted?", "a": "Line breaks count as one character each in the total. They are also shown in the lines count."},
            {"q": "What counts as a character?", "a": "Every symbol in your text: letters, numbers, punctuation, spaces, emoji and line breaks each count as one character."}
        ],
        "related": ["word-counter", "reading-time", "text-case-converter", "lorem-ipsum-generator"]
    },
    {
        "slug": "reading-time",
        "name": "Reading Time Calculator",
        "cat": "text",
        "popular": False,
        "icon": "Rt",
        "title": "Reading Time Calculator – Estimate Read Time Online | CalcHub",
        "desc": "Estimate how long it takes to read any text. Free reading time calculator with adjustable words-per-minute speed.",
        "h1": "Reading Time Calculator",
        "lede": "Estimate how long it takes someone to read your text. The calculator uses an average reading speed of 225 words per minute, which you can adjust to match your audience.",
        "howto": [
            "Paste your text into the box, or use the word count field directly.",
            "Choose a reading speed in words per minute (WPM), or keep the 225 WPM default.",
            "See the estimated reading time in minutes and seconds.",
            "Use the settings to fine-tune for technical content or young readers."
        ],
        "examples": [
            "A 1,100-word blog post at 225 WPM takes about 4 minutes 55 seconds to read.",
            "Academic articles are often read slower, around 175 WPM; switch the speed to match.",
            "If your landing page reads in under 60 seconds, most visitors will finish it."
        ],
        "features": [
            "Reading time estimate based on word count",
            "Adjustable WPM (words per minute)",
            "Results in minutes and seconds",
            "Estimates are clearly labelled as estimates"
        ],
        "privacy": "Your text is processed entirely in your browser. We do not store or transmit any content you paste.",
        "faq": [
            {"q": "What is a good default reading speed?", "a": "225 words per minute is a common average for adult English readers. Technical or dense content is often read around 175–200 WPM."},
            {"q": "Is reading time exact?", "a": "No. Reading speed varies by person and content type, so the result is an estimate — not a guarantee."},
            {"q": "Can I calculate without pasting text?", "a": "Yes. If you already know the word count, clear the text area and enter it in the word count field instead."}
        ],
        "related": ["word-counter", "character-counter", "text-case-converter", "duplicate-line-remover"]
    },
    {
        "slug": "text-case-converter",
        "name": "Text Case Converter",
        "cat": "text",
        "popular": False,
        "icon": "Tt",
        "title": "Text Case Converter – UPPERCASE, lowercase, Title Case | CalcHub",
        "desc": "Convert text to UPPERCASE, lowercase, Title Case, Sentence case and more. Free online case converter with one-click copy.",
        "h1": "Text Case Converter",
        "lede": "Convert any text between UPPERCASE, lowercase, Title Case, Sentence case and alternating case. Useful for headlines, folder names, code and consistent communication.",
        "howto": [
            "Type or paste your text into the input area.",
            "Click a case option — Uppercase, Lowercase, Title Case, Sentence case or Alternate.",
            "The converted result appears instantly in the output box.",
            "Copy the result with one click."
        ],
        "examples": [
            "Turn a headline into Title Case: 'free tools for everyday tasks' becomes 'Free Tools for Everyday Tasks'.",
            "Normalise pasted text to Sentence case for professional emails.",
            "Quickly check how a style guide would capitalise a title."
        ],
        "features": [
            "Uppercase, lowercase, Title Case, Sentence case and alternating case",
            "Correct handling of Unicode letters",
            "Live conversion with no upload",
            "One-click copy"
        ],
        "privacy": "All conversion happens locally in your browser. Your text is never sent to a server.",
        "faq": [
            {"q": "How is Title Case decided?", "a": "The converter capitalises the first letter of every word except short conjunctions, articles and prepositions (such as 'and', 'the' or 'of'), which stay lowercase unless they are the first word. Small differences exist between style guides; this is the most common convention."},
            {"q": "Does it work with accented characters?", "a": "Yes. Unicode characters such as à, é, ü and their uppercase forms are handled correctly."},
            {"q": "What is alternating case for?", "a": "Alternating case switches between upper and lower case (LiKe ThIs). It is sometimes used for mockery or emphasis in casual text. We convert it faithfully but keep it optional."}
        ],
        "related": ["word-counter", "character-counter", "reading-time", "remove-duplicate-lines"]
    },
    {
        "slug": "remove-duplicate-lines",
        "name": "Duplicate Line Remover",
        "cat": "text",
        "popular": False,
        "icon": "Dl",
        "title": "Remove Duplicate Lines Online – Free Line Deduplicator | CalcHub",
        "desc": "Delete duplicate lines from text and keep the first occurrence order. Free online duplicate line remover, processed locally.",
        "h1": "Duplicate Line Remover",
        "lede": "Remove duplicate lines from any list while keeping the order of first appearance. Ideal for cleaning up CSV exports, keyword lists, emails and inventory data.",
        "howto": [
            "Paste your list into the input area — one item per line.",
            "Choose options: ignore case and trim whitespace.",
            "Click Remove Duplicates.",
            "Copy the cleaned list from the output box."
        ],
        "examples": [
            "An email list with repeated addresses is deduplicated before an import.",
            "A keyword export with mixed-case entries is normalised with 'ignore case' enabled.",
            "Product SKUs pasted from multiple sources are merged into one clean list."
        ],
        "features": [
            "Removes duplicate lines and keeps first occurrence order",
            "Optional case-insensitive matching",
            "Optional whitespace trimming before comparison",
            "Blank lines are removed automatically"
        ],
        "privacy": "Your list is processed entirely in your browser. Nothing you paste is uploaded or stored.",
        "faq": [
            {"q": "Will it change the order of my lines?", "a": "No. The first occurrence of each line stays in place, and later duplicates are removed. The original relative order of unique lines is preserved."},
            {"q": "What does 'ignore case' do?", "a": "When enabled, lines that differ only by letter case are treated as duplicates (for example 'Apple' and 'apple')."},
            {"q": "Are blank lines removed?", "a": "Yes. Empty lines are always removed unless every line is blank."}
        ],
        "related": ["word-counter", "text-case-converter", "character-counter", "lorem-ipsum-generator"]
    },
    {
        "slug": "lorem-ipsum-generator",
        "name": "Lorem Ipsum Generator",
        "cat": "text",
        "popular": False,
        "icon": "Li",
        "title": "Lorem Ipsum Generator – Free Dummy Text Generator | CalcHub",
        "desc": "Generate lorem ipsum placeholder text by paragraphs, sentences or words. Free dummy text generator with one-click copy.",
        "h1": "Lorem Ipsum Generator",
        "lede": "Generate classic lorem ipsum placeholder text for mockups, wireframes and design drafts. Choose paragraphs, sentences or words, then copy the result.",
        "howto": [
            "Choose how much text you need: paragraphs, sentences or words.",
            "Set the quantity using the number input.",
            "Click Generate.",
            "Copy the generated text with one click."
        ],
        "examples": [
            "Designers drop 3 paragraphs of lorem ipsum into a layout to test typography and spacing.",
            "Developers generate a word count target to test content wrapping and pagination.",
            "Editors use placeholder text to reserve space before real copy arrives."
        ],
        "features": [
            "Generate by paragraphs, sentences or words",
            "Quality output with realistic Latin-style words",
            "One-click copy",
            "No limits on generation"
        ],
        "privacy": "Generation happens locally in your browser. No server requests are made.",
        "faq": [
            {"q": "What is lorem ipsum?", "a": "Lorem ipsum is a pseudo-Latin text used since the 1500s as placeholder content in typesetting and web design. It lets designers judge layout without being distracted by readable copy."},
            {"q": "Can I use lorem ipsum in real projects?", "a": "Yes. It is intentionally meaningless, so it is safe for mockups. Replace it with real copy before publishing."},
            {"q": "Is there a maximum amount?", "a": "No. You can generate large amounts of text locally, though we recommend generating only what your layout needs."}
        ],
        "related": ["word-counter", "character-counter", "text-case-converter", "remove-duplicate-lines"]
    },
]