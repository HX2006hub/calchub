# -*- coding: utf-8 -*-
"""CalcHub tool registry — Part 5: Time & Productivity (4) + Counters (2).

Timing claims are verified against buildTimer()/RUNNERS in assets/js/tools.js:
timers use Date.now() timestamps with requestAnimationFrame, the stopwatch
shows hundredths of a second and has NO lap feature, there is NO sound on
any timer, the Pomodoro tool switches phase automatically after every fourth
focus session, and only the Online Counter registers keyboard shortcuts.
"""

TIME_TOOLS = [
    {
        "slug": "countdown-timer",
        "name": "Countdown Timer",
        "cat": "time",
        "popular": True,
        "icon": "Ct",
        "title": "Countdown Timer — Set Hours, Minutes or Seconds | CalcHub",
        "desc": "Set a countdown with hours, minutes and seconds, then start, pause, resume or reset it. Runs on a timestamp so it stays correct when you switch tabs.",
        "h1": "Countdown Timer",
        "lede": "A kitchen timer, a presentation slot or a short break all need a countdown you can leave running while you do something else. Set the duration here and come back to an accurate remaining time.",
        "howto": [
            "Enter Hours, Minutes and Seconds. The timer starts at 5 minutes.",
            "Press Start. Pause freezes the remaining time; press Start again to resume.",
            "Watch the HH:MM:SS display count down. A message appears when it reaches zero.",
            "Use Reset to clear the display, or change any of the three fields to set a new duration."
        ],
        "examples": [
            "A 25-minute focus block: set Minutes to 25 and leave the other fields at zero.",
            "A 90-second exercise interval: set Minutes to 1 and Seconds to 30.",
            "Timing a long process: set Hours to 2 for a two-hour countdown."
        ],
        "understanding": [
            "The timer records the clock time at which it should finish and subtracts the current time on each frame. That is why it does not drift when the browser slows down: it is reading a deadline, not accumulating ticks. The display shows whole hours, minutes and seconds.",
            "Pause stores the remaining time and stops the frame loop; Start rebuilds the deadline from that remainder, which is what makes resuming work. Reset returns everything to zero and waits for a new duration."
        ],
        "limitations": [
            "There is no audible alarm. When the countdown reaches zero the page shows a 'Time is up!' message, so keep the tab visible if you need to notice it immediately.",
            "Browsers throttle animation frames in background tabs, so the display may jump rather than tick smoothly. The remaining time is still correct when you return, because it is computed from the deadline.",
            "Display updates are limited to whole seconds. This is not a millisecond or laboratory-grade timer.",
            "The timer lives in the open tab. Closing or reloading the page loses the countdown, and nothing is stored for later.",
            "There is no repeat, loop or multiple-timer support."
        ],
        "privacy": "The countdown runs entirely in your browser. Nothing is uploaded or stored.",
        "faq": [
            {"q": "Is the timer accurate if I switch tabs?", "a": "Yes for the remaining time. The tool computes how much time is left from a fixed end timestamp rather than counting frames, so a throttled or suspended tab resumes at the right value. The visual countdown may skip ahead when you come back."},
            {"q": "What happens when time runs out?", "a": "The display stops at 00:00:00 and the page shows a 'Time is up!' message. There is no sound and no browser notification."},
            {"q": "Can I pause and continue?", "a": "Yes. Pause freezes the remainder, and Start continues from that point. Changing any of the duration fields resets the timer instead."}
        ],
        "related": ["stopwatch", "pomodoro-timer", "time-zone-converter", "online-counter"]
    },
    {
        "slug": "stopwatch",
        "name": "Online Stopwatch",
        "cat": "time",
        "popular": False,
        "icon": "Sw",
        "title": "Online Stopwatch — Measure Elapsed Time | CalcHub",
        "desc": "Start, stop and reset a browser stopwatch showing elapsed time in hundredths of a second. Simple local timing with no account required.",
        "h1": "Online Stopwatch",
        "lede": "For timing how long something takes, a start button and an elapsed display are usually enough. This stopwatch measures from the moment you press Start until you stop it.",
        "howto": [
            "Press Start to begin. The display shows hours, minutes, seconds and hundredths.",
            "Press Stop to freeze the elapsed time at its current value.",
            "Press Start again to continue from where you stopped, or Reset to return to zero.",
            "Read the final figure directly from the display."
        ],
        "examples": [
            "Timing how long a task takes: press Start when you begin and Stop when you finish.",
            "Measuring a short process of a few seconds, where the hundredths column shows the finer detail.",
            "Timing separate attempts by pressing Reset between runs."
        ],
        "understanding": [
            "Like the countdown timer, this stopwatch works from clock timestamps: it subtracts the start time from the current time on each frame. The last two digits are hundredths of a second, derived from the milliseconds value — not a separate high-resolution measurement.",
            "Stop freezes the elapsed value. Starting again shifts the start time backwards by that amount, so the display continues rather than restarting. Reset clears it to zero."
        ],
        "limitations": [
            "There is no lap or split-time feature and no history of intermediate times. To record several intervals, note each value as you go.",
            "The hundredths column is a rounded display of elapsed time, not a reading of individual milliseconds, and the display is limited by how often the browser paints a frame.",
            "Accuracy depends on your device clock and browser scheduling. It is suitable for everyday timing, not scientific or competitive measurement.",
            "There is no sound, alarm or target-time alert.",
            "Closing or reloading the tab loses the elapsed time; nothing is saved."
        ],
        "privacy": "Timing happens in your browser. No data is uploaded or stored.",
        "faq": [
            {"q": "Can I record lap times?", "a": "No. This stopwatch has a single elapsed display with Start, Stop and Reset, and it does not store intermediate splits. If you need laps, note the displayed value at each point and reset or continue as needed."},
            {"q": "How precise is the display?", "a": "It shows hundredths of a second, which are derived from the elapsed milliseconds. Browser frame timing and device clock scheduling limit the real resolution, so treat it as a convenient everyday measure rather than a precision instrument."},
            {"q": "Does it keep running in another tab?", "a": "The elapsed value is based on a timestamp, so it stays correct when you return to the tab even if the browser throttled its animation frames while it was hidden. The display may jump forward rather than tick smoothly."}
        ],
        "related": ["countdown-timer", "pomodoro-timer", "time-zone-converter", "click-counter"]
    },
    {
        "slug": "pomodoro-timer",
        "name": "Pomodoro Timer",
        "cat": "time",
        "popular": False,
        "icon": "Pt",
        "title": "Pomodoro Timer — Focus Blocks and Breaks | CalcHub",
        "desc": "Run a focus timer with configurable short and long breaks. See how the phases rotate, skip or reset, and pick durations that suit your work.",
        "h1": "Pomodoro Timer",
        "lede": "Working in fixed blocks with a break in between is a simple way to make a long task feel manageable. Set the lengths you want here and the timer moves between focus and break phases for you.",
        "howto": [
            "Set Focus, Short break and Long break in minutes. They start at 25, 5 and 15.",
            "Press Start to begin a focus block. The phase label and remaining time show where you are.",
            "Use Pause, Skip to jump to the next phase, or Reset to start the cycle over.",
            "Watch the completed-focus counter as you work through the sequence."
        ],
        "examples": [
            "A common starting point is 25 minutes of focus and a 5-minute short break, with a 15-minute long break after four focus blocks.",
            "If 25 minutes feels long, try 15-minute focus blocks with a 3-minute break and adjust from there.",
            "Pressing Skip moves you straight to the next phase without waiting for the timer to finish."
        ],
        "understanding": [
            "The tool rotates through focus and break phases automatically. After each focus block it schedules a short break, and after every fourth completed focus block it schedules a long break instead. The counter shows how many focus blocks you have completed.",
            "Phase changes happen on their own when a phase ends, so the timer continues without you pressing anything. Skip advances immediately; Reset returns to the first focus block and clears the counter. Durations are read from the three fields whenever a phase begins."
        ],
        "limitations": [
            "There is no sound, desktop notification or alarm when a phase ends — the timer simply moves to the next phase and shows a brief message. Keep the tab visible if you rely on the transition.",
            "No single schedule works for everyone. The 25/5/15 defaults are a starting point, not a rule; the three duration fields can be changed at any time.",
            "Focus accepts 1 to 120 minutes, short breaks 1 to 60, and long breaks 1 to 90. Changing a field resets the current cycle.",
            "As with the other timers, closing or reloading the tab loses the current phase and count. Nothing is stored between sessions.",
            "The long break is fixed to every fourth focus block; the interval itself cannot be configured."
        ],
        "privacy": "The timer runs in your browser. No session data is uploaded or stored.",
        "faq": [
            {"q": "What is the Pomodoro technique?", "a": "A time-management approach built around focused work intervals separated by short breaks, with a longer break after several intervals. It is a framework rather than a fixed rule — the point is to give work a clear boundary and make breaks deliberate."},
            {"q": "Can I change the durations?", "a": "Yes. All three fields are editable within their limits, and the new value is used the next time that phase begins. Changing a field also resets the current cycle, so set your preferences before starting."},
            {"q": "Does it keep track of cycles?", "a": "It counts completed focus blocks, which is what determines when a long break is due. The count resets to zero when you press Reset or reload the page."},
            {"q": "Will it alert me when a break starts?", "a": "No. Phase changes are shown in the page with a short message and an updated label, but there is no audio or system notification."}
        ],
        "related": ["countdown-timer", "stopwatch", "time-zone-converter", "online-counter"]
    },
    {
        "slug": "time-zone-converter",
        "name": "Time Zone Converter",
        "cat": "time",
        "popular": False,
        "icon": "Tz",
        "title": "Time Zone Converter — Compare Two IANA Time Zones | CalcHub",
        "desc": "Convert a date and time between two IANA time zones, with daylight saving handled for the date you choose. Uses your browser's time-zone data.",
        "h1": "Time Zone Converter",
        "lede": "Arranging a call across countries goes wrong when someone assumes a fixed offset. Choose the two zones and the date, and this tool works out the local time on the other side — including any daylight saving in force on that day.",
        "howto": [
            "Pick the From time zone. It starts as the zone your browser reports.",
            "Enter the Date and time as it would be read in that source zone.",
            "Pick the To time zone and read the converted result below.",
            "Change either zone or the date to compare another moment."
        ],
        "examples": [
            "Scheduling a 9:00 meeting in New York for a colleague in London during summer, when the two cities are four hours apart rather than five.",
            "Checking what 18:00 on 15 January in Tokyo means in Los Angeles, where the date will usually still be the previous day.",
            "Comparing a deadline written in UTC with your own local zone before submitting work."
        ],
        "understanding": [
            "The tool treats the date and time you enter as a wall-clock reading in the source zone. It then asks the browser's Intl data for the UTC offset of each zone at that specific instant and applies the difference. The result line shows the converted time plus the UTC offsets used for both zones.",
            "Because offsets are looked up for the chosen date rather than assumed, daylight saving is applied correctly for that moment. A date in January and a date in July can therefore produce different offsets for the same pair of zones."
        ],
        "limitations": [
            "Zones are identified by IANA names such as Europe/London or America/New_York, not fixed UTC offsets. That is what makes daylight saving work, but it also means the answer depends on your browser's time-zone data being current, especially for future dates where rules may change.",
            "The zone list comes from the browser's supported time-zone values. Where that list is unavailable, the tool falls back to a shorter built-in set of common zones.",
            "The date-time field has minute precision and carries no time-zone information of its own; the source zone you select supplies that context. Double-check ambiguous times around a daylight-saving clock change.",
            "The result is formatted as a date and time with a UTC offset, not with a named zone abbreviation such as EST or BST.",
            "Historical dates, future rule changes and political decisions about time zones are only as accurate as the browser data behind Intl."
        ],
        "privacy": "The conversion uses your browser's built-in time-zone data. No date or time is uploaded or stored.",
        "faq": [
            {"q": "Are daylight saving changes handled?", "a": "Yes, for the date you enter. The tool asks the browser for each zone's UTC offset at that instant, so a summer date and a winter date can show different offsets for the same pair of cities. It does not assume a fixed offset."},
            {"q": "Why do some results show a different date?", "a": "A large offset can push the converted time into the previous or next calendar day. The result includes the full date as well as the time so this is visible."},
            {"q": "Which time zones are available?", "a": "The dropdowns are filled from your browser's list of IANA time zones, with a shorter fallback list of common zones if that data is unavailable. IANA names are used because they encode daylight-saving rules; a plain UTC offset would not."}
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
        "title": "Online Counter — Tally With a Step Size and Keyboard Keys | CalcHub",
        "desc": "Count up or down with adjustable steps, on-screen buttons or keyboard shortcuts. Optionally keep the count after a refresh using local browser storage.",
        "h1": "Online Counter",
        "lede": "When you are counting people arriving, repetitions or items in a stack, a tally you can update without looking down is more useful than a calculator. Set a step size and add or subtract with buttons or keys.",
        "howto": [
            "Set Step size to how much each press should change the count. It starts at 1.",
            "Use + Add and - Subtract, or press + (or =), - (or _) and R on the keyboard.",
            "Tick Keep count after refresh if you want the number to survive a page reload.",
            "Press Reset to return to zero."
        ],
        "examples": [
            "Counting attendees at a door with a step of 1 and the keyboard so you can keep watching the entrance.",
            "Tallying stock in packs of 12 by setting Step size to 12.",
            "Subtracting returns or cancellations with the - key without resetting the total."
        ],
        "understanding": [
            "The counter adds or subtracts the step value on each action and shows the running total. Subtraction can take the number below zero, which is useful when you are netting additions against removals.",
            "The keyboard shortcuts apply to the whole page, so you can tally without clicking: + or = adds one step, - or _ subtracts one step, and R resets to zero."
        ],
        "limitations": [
            "This is a manual tally, not an analytics or tracking system. It counts what you press, not visits, clicks elsewhere on the site or any automatic event.",
            "Keeping the count after refresh uses localStorage in this browser only. The value does not sync to other devices, and clearing site data removes it. Leaving the option unticked means a reload starts at zero.",
            "The step size accepts values from 1 to 1000 and applies to both Add and Subtract equally.",
            "Keyboard shortcuts listen on the page, so typing + or R into another input on the same page could also change the count.",
            "There is no history, timestamp or export of individual increments."
        ],
        "privacy": "The count stays in this browser tab. If you enable persistence, it is written to your own localStorage and is never uploaded.",
        "faq": [
            {"q": "What keyboard shortcuts are available?", "a": "Press + or = to add one step, - or _ to subtract one step, and R to reset to zero. They work anywhere on the page, so avoid typing those characters into other fields while tallying."},
            {"q": "Will my count be there tomorrow?", "a": "Only if you tick Keep count after refresh and use the same browser on the same device. The value lives in that browser's localStorage; it is not synced and is removed if you clear site data."},
            {"q": "Can the count go below zero?", "a": "Yes. Subtraction is unrestricted, which is deliberate for netting additions against removals. Reset returns it to zero."}
        ],
        "related": ["click-counter", "random-number-generator", "stopwatch", "random-name-picker"]
    },
    {
        "slug": "click-counter",
        "name": "Click Counter",
        "cat": "count",
        "popular": False,
        "icon": "Kc",
        "title": "Click Counter — One Big Button for Manual Tallying | CalcHub",
        "desc": "A single large button that counts each click, with a reset and an optional keep-count-after-refresh setting. No tracking, no account.",
        "h1": "Click Counter",
        "lede": "Sometimes the whole job is one repeated action and one number. This counter gives you a large button to press and a total that goes up by one each time.",
        "howto": [
            "Click the large button. The total increases by one on every press.",
            "Use Reset to set it back to zero.",
            "Tick Keep count after refresh to retain the number across reloads.",
            "Read the total underneath the button."
        ],
        "examples": [
            "Counting repetitions during a workout without breaking rhythm to use a keyboard.",
            "Tallying people through a door on a touch screen, where a big target is easier to hit.",
            "A quick show-of-hands count in a classroom or small meeting."
        ],
        "understanding": [
            "Every press of the main button adds exactly one to the total. There is no step setting and no subtract button — the count only moves upward until you reset it.",
            "Unlike the Online Counter, this page has no keyboard shortcuts and no step size. That is intentional: it is built for a single repeated click on one obvious target."
        ],
        "limitations": [
            "This is a manual click tally, not an analytics system. It does not track visitors, page views or clicks on other parts of the site.",
            "Only the button increases the count. Keys, clicks elsewhere and scrolling have no effect, so it is not a substitute for a site-wide click tracker.",
            "Keeping the count after refresh relies on localStorage in this browser. It is not synced across devices and is cleared with site data.",
            "There is no subtract, step size, history or export of individual clicks.",
            "Rapid or automated clicking will be counted exactly as pressed; the tool does not filter or deduplicate input."
        ],
        "privacy": "The count stays in this browser tab. If enabled, persistence uses your own localStorage and is never uploaded.",
        "faq": [
            {"q": "How is this different from the Online Counter?", "a": "This tool is one large button that adds one per click, with no step size, subtract button or keyboard shortcuts. The Online Counter offers add and subtract, a configurable step and keyboard keys. Use whichever matches how you are tallying."},
            {"q": "Does it track clicks anywhere on the site?", "a": "No. Only presses of the main button count. It is a manual tally, not a tracking or analytics tool."},
            {"q": "Can I subtract or change the step?", "a": "No. Each press adds exactly one, and Reset is the only way back to zero. For adjustable steps or subtraction, use the Online Counter."}
        ],
        "related": ["online-counter", "random-name-picker", "random-number-generator", "stopwatch"]
    },
]
