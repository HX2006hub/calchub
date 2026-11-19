# -*- coding: utf-8 -*-
"""CalcHub tool registry — Part 5: Time & Productivity (4) + Counters (2)."""

TIME_TOOLS = [
    {
        "slug": "countdown-timer",
        "name": "Countdown Timer",
        "cat": "time",
        "popular": True,
        "icon": "Ct",
        "title": "Countdown Timer – Free Online Countdown | CalcHub",
        "desc": "Set a countdown timer with hours, minutes and seconds. Free online countdown with start, pause, resume and reset.",
        "h1": "Countdown Timer",
        "lede": "Set a countdown for seconds, minutes or hours and let it run accurately in your browser. Start, pause, resume and reset whenever you need.",
        "howto": [
            "Set the hours, minutes and seconds you need.",
            "Click Start to begin the countdown.",
            "Pause and resume anytime.",
            "Reset to set a new time."
        ],
        "examples": [
            "Count down 60 seconds for a quick warm-up or stretch.",
            "Time a 25-minute work block before a break.",
            "Run a 10-minute cooking timer while you prep."
        ],
        "features": [
            "Adjustable hours, minutes and seconds",
            "Start, pause, resume and reset",
            "Timestamp-based counting stays accurate in the background",
            "Clear visual feedback when time is up"
        ],
        "privacy": "The timer runs entirely in your browser. Nothing is recorded or sent.",
        "faq": [
            {"q": "Is the timer accurate if I switch tabs?", "a": "Yes. The countdown is based on real timestamps, not incremental ticks, so it stays correct even if the tab is throttled in the background."},
            {"q": "What happens when time runs out?", "a": "The timer stops at 00:00 and gives a visual cue. A sound plays only if you enable it and your browser allows notifications."},
            {"q": "Can I pause and continue?", "a": "Yes. Pause freezes the remaining time; resume continues from where you paused."}
        ],
        "related": ["stopwatch", "pomodoro-timer", "time-zone-converter", "online-counter"]
    },
    {
        "slug": "stopwatch",
        "name": "Online Stopwatch",
        "cat": "time",
        "popular": False,
        "icon": "Sw",
        "title": "Online Stopwatch – Free Stopwatch and Laps | CalcHub",
        "desc": "Start, pause and reset a precise online stopwatch with lap times. Free stopwatch with millisecond precision using high-resolution time.",
        "h1": "Online Stopwatch",
        "lede": "Time anything with a simple, precise stopwatch. Start, pause, record laps and reset — all locally, with high-resolution timing that stays accurate in the background.",
        "howto": [
            "Click Start to begin timing.",
            "Record laps with the Lap button as needed.",
            "Pause to stop the clock; Start again to continue.",
            "Reset to clear the time and laps."
        ],
        "examples": [
            "Timer for a 5 km run split checkpoints.",
            "Measure a task to improve your workflow.",
            "Run a science experiment with lap recording."
        ],
        "features": [
            "High-resolution elapsed time",
            "Start, pause, continue and reset",
            "Lap recording",
            "Accurate when the tab is in the background"
        ],
        "privacy": "Everything happens locally in your browser. No timing data is stored or transmitted.",
        "faq": [
            {"q": "How precise is the stopwatch?", "a": "We use the Performance API's high-resolution time for display, with millisecond precision. Browser scheduling can cause minor delays, but for everyday timing it is accurate."},
            {"q": "Does it keep running in another tab?", "a": "Yes. The elapsed time is computed from timestamps, so switching tabs does not reset it. Suspended tabs may briefly not update, but the computed time stays correct."},
            {"q": "Can I delete a lap?", "a": "You can clear all laps with Reset. Individual lap removal is not implemented to keep the interaction simple."}
        ],
        "related": ["countdown-timer", "pomodoro-timer", "time-zone-converter", "click-counter"]
    },
    {
        "slug": "pomodoro-timer",
        "name": "Pomodoro Timer",
        "cat": "time",
        "popular": False,
        "icon": "Pt",
        "title": "Pomodoro Timer – Focus Timer Online Free | CalcHub",
        "desc": "Use the Pomodoro technique with a focus timer, short breaks and long breaks. Free online Pomodoro timer with custom durations.",
        "h1": "Pomodoro Timer",
        "lede": "Work in focused Pomodoro intervals with scheduled short and long breaks. Configure durations, start/pause/skip, and keep your session on track.",
        "howto": [
            "Use the default 25-minute focus and 5-minute break, or set your own.",
            "Click Start to begin the focus session.",
            "When it finishes, the timer moves to a break automatically.",
            "Use Skip to move to the next phase manually."
        ],
        "examples": [
            "Four 25-minute focus blocks with 5-minute breaks make a classic Pomodoro cycle.",
            "Longer 50-minute blocks work well for deep coding sessions.",
            "Short 15-minute blocks fit a busy call schedule."
        ],
        "features": [
            "Focus, short break and long break phases",
            "Custom durations",
            "Start, pause, skip and reset",
            "Cycle counter",
            "Optional sound notification"
        ],
        "privacy": "The timer runs locally. No session data is stored or transmitted.",
        "faq": [
            {"q": "What is the Pomodoro technique?", "a": "A time-management method where you work in focused blocks (traditionally 25 minutes) followed by short breaks, with a longer break after several cycles."},
            {"q": "Can I change the durations?", "a": "Yes. Set focus, short break and long break lengths before starting."},
            {"q": "Does it keep track of cycles?", "a": "Yes. The cycle counter shows how many focus sessions you have completed; after four, a long break is suggested."}
        ],
        "related": ["countdown-timer", "stopwatch", "time-zone-converter", "online-counter"]
    },
    {
        "slug": "time-zone-converter",
        "name": "Time Zone Converter",
        "cat": "time",
        "popular": False,
        "icon": "Tz",
        "title": "Time Zone Converter – Convert Time Across Zones | CalcHub",
        "desc": "Convert a time between IANA time zones with daylight saving handled correctly. Free online time zone converter for meetings and travel.",
        "h1": "Time Zone Converter",
        "lede": "Convert a local time to any IANA time zone, with daylight saving handled correctly using the browser's Intl API. Perfect for scheduling calls across countries.",
        "howto": [
            "Pick the source time zone (or use your local one).",
            "Enter the date and time to convert.",
            "Pick the target time zone.",
            "Read the converted time, including the correct date."
        ],
        "examples": [
            "Schedule a 2 PM London call for a colleague in New York.",
            "Convert an event time from UTC to your local zone.",
            "Check whether a meeting falls on the same day in both zones."
        ],
        "features": [
            "Full IANA time zone list",
            "DST-aware conversion via Intl API",
            "Shows both date and time in the result",
            "Handles cross-day conversions"
        ],
        "privacy": "Conversion runs locally using your browser's time zone data. Nothing is stored or sent.",
        "faq": [
            {"q": "Are daylight saving changes handled?", "a": "Yes. We use the Internationalization API with IANA time zones, so the result reflects the DST rules in effect at the selected date, not a fixed offset."},
            {"q": "Why do some zones show different dates?", "a": "Zones east of UTC can be a day ahead and zones west can be a day behind. We always show the calendar date alongside the time."},
            {"q": "Which time zones are available?", "a": "Every IANA zone the browser supports, which includes all major city zones, UTC variants and regions like Europe, America, Asia and Australia."}
        ],
        "related": ["countdown-timer", "pomodoro-timer", "stopwatch", "date-difference"]
    },
]

COUNTER_TOOLS = [
    {
        "slug": "online-counter",
        "name": "Online Counter",
        "cat": "count",
        "popular": False,
        "icon": "Oc",
        "title": "Online Counter – Add, Subtract and Reset | CalcHub",
        "desc": "A simple online counter for tallying anything. Press the buttons or use your keyboard to count up, down and reset.",
        "h1": "Online Counter",
        "lede": "A fast, tactile counter for anything you need to tally. Use the buttons, arrow keys or +/- shortcuts to count up and down, and reset with a click.",
        "howto": [
            "Click the + button (or press the '+' key) to count up.",
            "Click the − button (or press the '-' key) to count down.",
            "Press Reset to return to zero.",
            "Optionally set a custom step size."
        ],
        "examples": [
            "Tally attendees entering a room.",
            "Count repetitions during a workout.",
            "Track items packed or produced."
        ],
        "features": [
            "Count up and down",
            "Keyboard support (+ / − / R)",
            "Custom step size",
            "Touch-friendly buttons",
            "Optional localStorage persistence (clearly labelled)"
        ],
        "privacy": "The counter runs locally. If you enable persistence, the value is stored only in your browser's localStorage and is never sent to a server.",
        "faq": [
            {"q": "Does the counter save when I refresh?", "a": "Only if you enable 'Keep count after refresh'. It then saves to your browser's localStorage on this device. Otherwise, the value resets to zero."},
            {"q": "Can I count faster with the keyboard?", "a": "Yes. Press the + and − keys to count, and R to reset, when the counter is focused."},
            {"q": "Can I set a step bigger than 1?", "a": "Yes. Change the step size in the settings to jump by any number."}
        ],
        "related": ["click-counter", "random-number-generator", "stopwatch", "random-name-picker"]
    },
    {
        "slug": "click-counter",
        "name": "Click Counter",
        "cat": "count",
        "popular": False,
        "icon": "Kc",
        "title": "Click Counter – Count Clicks Online Free | CalcHub",
        "desc": "A simple click counter that counts every click of a button, with optional local storage. Free online click counter for games, tests and tallying.",
        "h1": "Click Counter",
        "lede": "Count clicks by clicking the big button — every click is registered instantly. Ideal for printable click tests, games and any quick tally.",
        "howto": [
            "Click the big button to increment the count.",
            "Each click registers immediately with visual feedback.",
            "Press Reset to start over.",
            "Optionally enable persistence to keep the count after refresh."
        ],
        "examples": [
            "Run a quick clicks-per-second test.",
            "Tally free-throw attempts at a casual event.",
            "Count times a switch is pressed during a test."
        ],
        "features": [
            "Instant click registration",
            "Zero latency feedback",
            "Reset button",
            "Optional localStorage persistence"
        ],
        "privacy": "Clicks are tallied locally. If persistence is enabled, only the count is stored in your browser's localStorage — never sent to a server.",
        "faq": [
            {"q": "Is the count accurate if I click fast?", "a": "Yes. Each click is counted on the click event, which fires on every click regardless of speed. The UI stays responsive."},
            {"q": "Does it save after refresh?", "a": "Only if you turn on 'Keep count'. It then uses localStorage on your device. By default the count resets."},
            {"q": "Can I accidentally double-count?", "a": "No. One physical click produces one click event. Keyboard presses and touch taps each count once."}
        ],
        "related": ["online-counter", "random-name-picker", "random-number-generator", "stopwatch"]
    },
]