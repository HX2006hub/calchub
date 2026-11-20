# -*- coding: utf-8 -*-
"""CalcHub tool registry — Part 1: Text & Writing Tools (6).

Editorial copy is written against the actual widget controls and runner code
in assets/js/tools.js. Fields:
  title / desc / h1 / lede / howto / examples / understanding /
  limitations / privacy / faq / related
`understanding` and `limitations` are rendered by prose_html() only when
present, so a simple tool never gets padded sections it does not need.
"""

TEXT_TOOLS = [
    {
        "slug": "word-counter",
        "name": "Word Counter",
        "cat": "text",
        "popular": True,
        "icon": "Aa",
        "title": "Word Counter: Live Word and Character Counts | CalcHub",
        "desc": "Paste text to see words, characters, sentences, paragraphs and an estimated reading time. Explains why counts differ between writing apps.",
        "h1": "Word Counter",
        "lede": "Most writing limits are expressed in words, but a word is not a fixed unit. Paste your text here and the six figures update as you type, so you can see exactly what is being counted before you start cutting.",
        "howto": [
            "Type or paste into the text box. Words, characters, sentences, paragraphs and reading time update on every keystroke.",
            "Use Insert sample text to see how blank lines and punctuation are treated, or Clear to start over.",
            "Check Characters (no spaces) when a form counts characters rather than words.",
            "Use the reading time line for a quick sense of how long the piece is."
        ],
        "examples": [
            "A 700-word draft shows a 4 min read at the default 225 words per minute.",
            "Two blocks separated by a blank line count as 2 paragraphs; a single line break between them still counts as 1.",
            "'Dr. Smith waited.' is counted as two sentences, because the period after 'Dr.' closes one."
        ],
        "understanding": [
            "Words are counted by splitting on whitespace: any run of non-space characters counts as one word. That makes 'state-of-the-art' one word and 'state of the art' three. Characters includes everything you typed, including spaces and line breaks; Characters (no spaces) removes all whitespace.",
            "Sentences are split on periods, exclamation marks and question marks. Paragraphs are split on blank lines, so a soft line break does not start a new one. Reading time divides the word count by 225 words per minute, rounds up, and shows 'Less than 1 minute' for short text."
        ],
        "limitations": [
            "Counts will not always match a word processor. Word, Google Docs and social platforms each treat hyphens, abbreviations and numbers differently, so use one consistent counter when comparing drafts.",
            "Sentence counting is punctuation-based. Abbreviations such as 'Dr.' or 'e.g.' can split a sentence in two, and a line with no final period may not be counted as a sentence at all.",
            "Characters uses the browser's string length, so an emoji outside the basic Unicode plane counts as two characters even though you see one symbol.",
            "Reading time is an estimate for uninterrupted silent reading. Technical material, tables and second-language reading usually take longer.",
            "The text stays in the box only while the page is open; reloading clears it."
        ],
        "privacy": "Your text is counted in this browser tab. Nothing is uploaded, stored or logged.",
        "faq": [
            {"q": "Why does this word count differ from Word or Google Docs?", "a": "This tool counts any run of non-space characters as one word, so hyphens keep a term together and punctuation attached to a word does not create a new one. Other applications apply their own rules, especially around hyphens, numbers and abbreviations. For a before-and-after comparison, measure both drafts with the same tool."},
            {"q": "Do emojis and symbols count as words?", "a": "A standalone emoji counts as one word because it is a run of non-space characters, and as two characters in the character figures if it sits outside the basic Unicode plane. Punctuation attached to a word stays inside that word."},
            {"q": "Is my text saved anywhere?", "a": "No. The counts are computed locally as you type, and the text is neither uploaded nor written to browser storage. Closing or reloading the tab discards it."}
        ],
        "related": ["character-counter", "reading-time", "text-case-converter", "remove-duplicate-lines"]
    },
    {
        "slug": "character-counter",
        "name": "Character Counter",
        "cat": "text",
        "popular": False,
        "icon": "Cc",
        "title": "Character Counter — With and Without Spaces | CalcHub",
        "desc": "Count total characters, characters without spaces, letters, digits, spaces and other symbols. Useful for form fields, meta titles and post limits.",
        "h1": "Character Counter",
        "lede": "Character limits are easy to hit and hard to predict, because every service counts spaces and line breaks a little differently. This counter reports six separate figures so you can tell which characters a limit is likely to include.",
        "howto": [
            "Paste your text into the box. All six numbers update as you type.",
            "Use Total characters when a field counts every keystroke, including spaces and line breaks.",
            "Compare Characters (no spaces) when a limit appears to ignore whitespace.",
            "Use Clear to empty the box and check a different string."
        ],
        "examples": [
            "A 280-character post: check Total characters first, then Characters (no spaces) if the platform ignores spaces.",
            "'CalcHub | Free Tools' is 20 characters, including the two spaces and the vertical bar.",
            "An address block with three line breaks adds three characters to the total, because line breaks are whitespace too."
        ],
        "understanding": [
            "Total characters is the full length of the text, including spaces, tabs and line breaks. Characters (no spaces) strips all of that away, so the gap between the two numbers tells you how much of your text is formatting rather than content.",
            "The four smaller figures group characters by type: ASCII letters, digits, whitespace, and everything else such as punctuation, symbols and emoji. They are most useful for diagnosing why a form rejected a string — a pasted phone number, for instance, may be contributing more digits than you expected."
        ],
        "limitations": [
            "Compatibility is not guaranteed. Platforms differ on whether spaces, line breaks, emoji and URLs count as one character or several, so check the specific service's rules before relying on these figures for a hard limit.",
            "Letters counts A-Z and a-z only. Accented characters such as e-acute or n-tilde fall into the other-characters group, and underscores are not counted in any of the four groups.",
            "Characters uses the browser's string length. An emoji outside the basic Unicode plane counts as two characters here even though you see one symbol.",
            "The counter reports numbers only. It does not enforce a limit, warn when you pass one, or trim the text for you."
        ],
        "privacy": "The text is processed in this browser tab and is never uploaded or stored.",
        "faq": [
            {"q": "Will this match the limit on a specific social platform?", "a": "Not necessarily. Some platforms count a URL as a fixed length regardless of its real size, others count emoji as two characters, and some ignore trailing whitespace. Use this tool to understand the makeup of your own text, then confirm against that platform's published rules."},
            {"q": "Why is Characters (no spaces) lower than I expected?", "a": "All whitespace is removed, not just the spaces between words. Tabs, line breaks and multiple consecutive spaces disappear from that figure, which is why formatted text shows a bigger drop than a single sentence."},
            {"q": "Can I paste a long document?", "a": "Yes, there is no server-side limit because nothing is sent anywhere. Very large pastes depend on your browser's available memory, but ordinary articles and page copy are fine."}
        ],
        "related": ["word-counter", "reading-time", "text-case-converter", "lorem-ipsum-generator"]
    },
    {
        "slug": "reading-time",
        "name": "Reading Time Calculator",
        "cat": "text",
        "popular": False,
        "icon": "Rt",
        "title": "Reading Time Calculator — Estimate Read and Speak Time | CalcHub",
        "desc": "Estimate how long a text takes to read or read aloud. Set your own words-per-minute pace and see why the result is only an approximation.",
        "h1": "Reading Time Calculator",
        "lede": "A reading-time label is a division problem: word count divided by an assumed pace. Change the pace here and the estimate changes with it, which is the quickest way to see how much that label depends on one assumption.",
        "howto": [
            "Paste your text into the box; the word count and both time estimates update immediately.",
            "Set Reading speed to the pace you want to assume. It defaults to 225 words per minute, a common figure for silent adult reading.",
            "Compare the reading estimate with the speaking estimate when preparing a talk or script.",
            "Use the Minutes and Seconds figures for a more precise number on short texts."
        ],
        "examples": [
            "A 900-word article shows 4.0 minutes at 225 wpm. At 150 wpm it shows 6.0 minutes — the same text, a different assumption.",
            "A 2,000-word draft is about 8.9 minutes at the default pace, but roughly 15.4 minutes at a careful 130 wpm.",
            "A 300-word announcement reads as 1.3 minutes at 225 wpm, while the speaking estimate puts the same words at about 2.3 minutes read aloud."
        ],
        "understanding": [
            "The reading estimate is the word count divided by the words-per-minute value you set. It is shown to one decimal place, with 'Less than 1 minute' for anything under a minute; the Minutes and Seconds figures are that same estimate split into whole minutes and remaining seconds.",
            "The speaking estimate uses a fixed 130 words per minute and does not change when you adjust the reading-speed field. It is a separate, conventional pace for reading aloud, not a second reading setting."
        ],
        "limitations": [
            "This is an estimate, not a measurement. It assumes continuous reading with no pauses and cannot tell how dense the material is.",
            "Real reading time varies widely: technical prose, tables, code, formulas and second-language reading take longer than general text, while skimming is faster.",
            "Words are counted by splitting on whitespace, so headings, captions, list items and bullet fragments all count as words.",
            "The speaking estimate is fixed at 130 wpm and cannot be adjusted on this page.",
            "Images, video and embedded media are not accounted for."
        ],
        "privacy": "The text is counted in your browser and is not uploaded or saved.",
        "faq": [
            {"q": "Where does 225 words per minute come from?", "a": "It is a widely used average for silent adult reading of general prose, offered here as a starting point rather than a measured value for your audience. The field is editable precisely because the right pace depends on the text and the reader."},
            {"q": "Why does a publishing platform show a different time?", "a": "Platforms choose their own words-per-minute value and their own rounding, and some add a fixed allowance per image. The same article can therefore be labelled 4 min read in one place and 6 min read in another."},
            {"q": "Does it account for code blocks or images?", "a": "No. Only the word count of the pasted text is used. If your article is heavy with screenshots or code, treat the result as a lower bound."}
        ],
        "related": ["word-counter", "character-counter", "text-case-converter", "remove-duplicate-lines"]
    },
    {
        "slug": "text-case-converter",
        "name": "Text Case Converter",
        "cat": "text",
        "popular": False,
        "icon": "Tt",
        "title": "Text Case Converter — Change Capitalization Instantly | CalcHub",
        "desc": "Convert text to uppercase, lowercase, title case, sentence case, camelCase or alternating case. See what each format does and where it is useful.",
        "h1": "Text Case Converter",
        "lede": "Capitalization rules differ between a headline, a database key and a line of code. Pick the format you need and the converted text appears in the second box, ready to copy.",
        "howto": [
            "Type or paste your text in the upper box.",
            "Click one of the six format buttons. The result appears in the Converted text box below.",
            "Copy the result from the lower box; conversion does not run automatically as you type.",
            "Use Clear to empty both boxes and try a different source."
        ],
        "examples": [
            "Title Case turns 'the lord of the rings' into 'The Lord of the Rings' — short words such as 'of' and 'the' stay lowercase except at the start.",
            "camelCase turns 'user profile settings' into 'userProfileSettings', the shape used for JavaScript variable names.",
            "Sentence case fixes 'hello world. second sentence' into 'Hello world. Second sentence'."
        ],
        "understanding": [
            "Each button applies a single pass over the text and writes the result to the lower box. The original text is left untouched, so you can compare the two or try another format without retyping.",
            "Title Case capitalizes the first letter of every word except a short list of common words (a, an, and, the, of, to, in and similar) when they appear after the first word. Sentence case capitalizes the first letter of the text and the first letter after a period followed by a space."
        ],
        "limitations": [
            "Case conversion is mechanical. Proper nouns and acronyms lose their original capitalization: 'NASA' becomes 'Nasa' in Title Case and 'nasa' in lowercase, and 'iPhone' becomes 'Iphone'. Proofread names before publishing.",
            "camelCase removes spaces and punctuation and is built for Latin letters and digits. Accented characters and non-Latin scripts may not convert as expected.",
            "Sentence case only capitalizes after a period followed by a space, so an abbreviation such as 'e.g.' or a line break may not start a new sentence.",
            "Alternating case toggles case by character position, including the spaces in between, and is intended for playful text rather than formal writing.",
            "Nothing is copied to the clipboard automatically — you take the text from the result box yourself."
        ],
        "privacy": "Conversion happens in your browser; the text is never uploaded or stored.",
        "faq": [
            {"q": "Will it preserve acronyms like API or NASA?", "a": "No. Each format works word by word or character by character without knowing which words are names, so acronyms are lowercased or title-cased like ordinary words. Restore them manually after conversion."},
            {"q": "Is the result copied automatically?", "a": "No. The converted text appears in the lower box and stays there until you copy it or click Clear, which empties both boxes."},
            {"q": "Can I undo a conversion?", "a": "Your original text remains in the upper box, so you can click a different format at any time. There is no separate undo step."}
        ],
        "related": ["word-counter", "character-counter", "reading-time", "remove-duplicate-lines"]
    },
    {
        "slug": "remove-duplicate-lines",
        "name": "Duplicate Line Remover",
        "cat": "text",
        "popular": False,
        "icon": "Dl",
        "title": "Duplicate Line Remover — Clean Lists, Keep the Order | CalcHub",
        "desc": "Remove repeated lines from a pasted list while keeping the first occurrence in place. Optional case-insensitive matching and whitespace trimming.",
        "h1": "Duplicate Line Remover",
        "lede": "Lists copied from spreadsheets, logs or email threads tend to acquire the same entry twice. This tool keeps the first occurrence of each line and drops later matches, so the items that survive stay in their original order.",
        "howto": [
            "Paste your list into the upper box, one item per line. The result updates as you type.",
            "Tick Ignore case if 'Apple' and 'apple' should count as the same item.",
            "Tick Trim whitespace before comparing if lines may carry stray leading or trailing spaces.",
            "Read the count line to see how many unique lines remain, then copy the result."
        ],
        "examples": [
            "A guest list of Alice, Bob, Alice, Carol becomes Alice, Bob, Carol — the second Alice is dropped and Bob stays ahead of Carol.",
            "An inventory export with 'Widget-A' and 'widget-a' collapses to one line when Ignore case is enabled.",
            "A tag list with 'design ' and 'design' becomes a single 'design' once Trim whitespace is enabled."
        ],
        "understanding": [
            "A line is treated as a duplicate when its comparison key has already been seen. The key is the line itself, optionally lowercased and optionally trimmed depending on the two checkboxes. Only the first line with a given key is kept.",
            "The list is read from top to bottom, so the surviving lines keep their original order — this is not a sort or an alphabetical deduplication. The count below shows how many unique lines were kept and how many lines were read in total, including blank ones."
        ],
        "limitations": [
            "Blank lines are always dropped, even with neither checkbox ticked. A line containing only spaces is also dropped when Trim whitespace is enabled.",
            "Matching is exact text (or case-insensitive text); it does not fuzzy-match near-duplicates such as 'Bob Smith' and 'Bob  Smith' with different internal spacing.",
            "The options only affect comparison. The tool does not sort, number or otherwise reformat your list.",
            "There is no server-side size limit, but very large lists depend on your browser's available memory."
        ],
        "privacy": "The list is processed in this browser tab and never uploaded or saved.",
        "faq": [
            {"q": "Does it keep the first or the last duplicate?", "a": "The first. The tool walks the list top to bottom and keeps the earliest line for each key, which also preserves the order of everything that survives."},
            {"q": "Is the output sorted alphabetically?", "a": "No. Sorting would change the order of your list, so the tool deliberately leaves it alone. If you need an alphabetical list, sort it separately afterwards."},
            {"q": "Why did my blank lines disappear?", "a": "Empty lines are skipped unconditionally so the result does not accumulate gaps. Lines with only whitespace are skipped too when Trim whitespace is on."}
        ],
        "related": ["word-counter", "text-case-converter", "character-counter", "lorem-ipsum-generator"]
    },
    {
        "slug": "lorem-ipsum-generator",
        "name": "Lorem Ipsum Generator",
        "cat": "text",
        "popular": False,
        "icon": "Li",
        "title": "Lorem Ipsum Generator — Placeholder Text for Layouts | CalcHub",
        "desc": "Generate lorem ipsum placeholder paragraphs or an exact word count for mockups and templates. Runs locally; replace the text before publishing.",
        "h1": "Lorem Ipsum Generator",
        "lede": "When a layout is still being designed, real copy becomes a distraction — reviewers start editing the words instead of the spacing. Placeholder text gives a page the right visual weight without asking to be read.",
        "howto": [
            "Set Paragraphs for the number of blocks you need; the default is 3.",
            "Leave Words at 0 to use paragraph mode, or enter a number to generate exactly that many words instead.",
            "Click Generate for a new variation. A first result is already waiting when the page loads.",
            "Use Copy to clipboard to paste the text into your design or template."
        ],
        "examples": [
            "A card grid needing three blocks of body copy: set Paragraphs to 3 and leave Words at 0.",
            "A layout test needing exactly 12 words: set Words to 12. The paragraph count is ignored in this mode.",
            "A template with a fixed length spec: generate a paragraph, then verify it with the Word Counter."
        ],
        "understanding": [
            "In paragraph mode, each block is built from a small fixed vocabulary of Latin-derived words, with three to five sentences of varying length. The sentences are shaped like prose but carry no meaning, which is the point: the eye sees a block of text rather than a message.",
            "In word mode the tool emits exactly the number of words you requested as a single sentence, and the paragraph setting is ignored. If you need to confirm a length against a spec, paste the result into the Word Counter."
        ],
        "limitations": [
            "This is a small repeating word list, not the full classical lorem ipsum passage. Expect the same words to recur across a long document.",
            "The output is not real content. Replace it before publishing: placeholder copy hurts accessibility, search visibility and anyone trying to review a live page.",
            "The lines are Latin-like and not localized, so they are unsuitable for testing non-Latin scripts, right-to-left layouts or line-break behaviour in other languages.",
            "Each Generate click produces a different arrangement. There is no seed and no way to reproduce a previous output."
        ],
        "privacy": "Text is generated in your browser and is not uploaded or stored.",
        "faq": [
            {"q": "When should I use placeholder text?", "a": "Use it while the layout is in flux — checking line lengths, wrapping, font sizes and how a card looks with a realistic amount of text. Replace it with real copy before a page is shared, reviewed for content, or published."},
            {"q": "Is this the traditional lorem ipsum passage?", "a": "No. It draws randomly from a short fixed vocabulary, so the wording differs from the classical text and repeats within longer output."},
            {"q": "Why did my Words setting override the paragraph count?", "a": "Word mode takes priority. When Words is greater than zero the tool produces exactly that many words in one sentence and ignores Paragraphs; set Words back to 0 to return to paragraph mode."}
        ],
        "related": ["word-counter", "character-counter", "text-case-converter", "remove-duplicate-lines"]
    },
]
