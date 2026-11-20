# -*- coding: utf-8 -*-
"""CalcHub tool registry — Part 3: Calculators (6).

Formulas and edge cases below are taken from the runners in
assets/js/tools.js: the percentage tool has four modes with specific zero
guards, date difference divides by 30.437/365.25, unit conversion uses a
separate temperature formula, and BMI uses kg / m^2 with four adult ranges.
"""

CALC_TOOLS = [
    {
        "slug": "percentage-calculator",
        "name": "Percentage Calculator",
        "cat": "calc",
        "popular": True,
        "icon": "%",
        "title": "Percentage Calculator — Four Everyday Percentage Problems | CalcHub",
        "desc": "Work out X% of a number, what percent one value is of another, or a percentage increase and decrease. Includes formulas and worked examples.",
        "h1": "Percentage Calculator",
        "lede": "Percentage questions come in a few recurring shapes: a tip, a test score, a price change. Choose the shape you have and enter two numbers — the calculator shows the answer, the working and a related figure.",
        "howto": [
            "Choose a Calculation type. The labels on the two input fields change to match the mode.",
            "Enter the values those labels ask for. Results update as you type.",
            "Read the three output lines: the answer, the working, and a related figure such as the remainder or the complement.",
            "Use Reset values to go back to the default example of 15% of 240."
        ],
        "examples": [
            "What is 15% of 240? 36. The third line also shows 204 remaining.",
            "42 out of 60 is 70%, with a 30% complement.",
            "A price rising from 80 to 96 is a 20% increase: (96 - 80) / 80 x 100.",
            "A price falling from 80 to 64 in Percentage decrease mode gives 20%: (80 - 64) / 80 x 100."
        ],
        "understanding": [
            "Percent of a number uses (X / 100) x Y. The third line shows Y minus the result, which is what remains after taking that share.",
            "Is what percent of uses (X / Y) x 100. The complement line shows how far short of 100% the first value is.",
            "Increase uses (new - original) / original x 100; decrease uses (original - new) / original x 100. The second line gives the absolute difference between the two values, and the third restates the new value and whether it is larger or smaller. Results are displayed with up to six decimal places."
        ],
        "limitations": [
            "The first value cannot be zero in any mode, and the second value cannot be zero in the percent-of and is-what-percent modes. When a value is zero or blank, the outputs show dashes instead of a number.",
            "The increase and decrease modes use the same formula with the subtraction reversed. Choose Percentage increase but enter a lower new value and you will get a negative percentage — the tool does not swap the numbers for you.",
            "Percentages above 100 and negative inputs are accepted mathematically, but may not describe a real situation. Interpret them in context.",
            "This is arithmetic, not a financial calculator. It does not handle compounding, sequential discounts, tax or currency rounding. Two successive 20% discounts are not a 40% discount; use the Discount Calculator for a single discount with optional tax.",
            "Nothing is stored. Refreshing the page clears the fields."
        ],
        "privacy": "The calculation runs in your browser. Nothing is sent or saved.",
        "faq": [
            {"q": "How do I calculate X% of Y?", "a": "Multiply Y by X and divide by 100. For 15% of 240 that is 240 x 15 / 100 = 36. The third output line also tells you what is left over, which is 204 in this case."},
            {"q": "Why do I get a dash instead of a result?", "a": "One of the fields is empty, zero, or not a number. Division by zero is undefined, so the calculator stops rather than showing infinity. In the increase and decrease modes a zero original value triggers a specific message asking for a value greater than zero."},
            {"q": "Can I use the increase mode for a decrease?", "a": "You will get a negative percentage, because the formula is fixed for each mode. It is clearer to pick Percentage decrease, which reverses the subtraction and reports a positive result when the new value is lower."},
            {"q": "Does it handle stacked discounts?", "a": "No. Apply one discount, take the resulting price, then run the tool again for the next one. Adding the percentages together overstates the total reduction."}
        ],
        "related": ["discount-calculator", "bmi-calculator", "unit-converter", "age-calculator"]
    },
    {
        "slug": "age-calculator",
        "name": "Age Calculator",
        "cat": "calc",
        "popular": True,
        "icon": "Ae",
        "title": "Age Calculator — Exact Age in Years, Months and Days | CalcHub",
        "desc": "Work out age in years, months and days from a birth date, with an optional target date. Also shows total days, weeks and months elapsed.",
        "h1": "Age Calculator",
        "lede": "Age in whole years is usually enough, but forms, records and eligibility checks sometimes need the exact years, months and days between two dates. Enter a birth date and, if you need it, a second date to measure against.",
        "howto": [
            "Pick the Birth date.",
            "Optionally change the Target date. It is set to today when the page loads.",
            "Read the age in years, months and days, plus the total weeks, months and days figures.",
            "Change either date to recalculate."
        ],
        "examples": [
            "Someone born on 15 June 1990 turns 35 on 15 June 2025 — set the target date to the birthday itself when you only need whole years.",
            "To find how old a document was when it was signed, set the target date to the signing date rather than today.",
            "The total days figure is useful for an exact 'days old' count, such as a newborn's age in days."
        ],
        "understanding": [
            "The years, months and days line is calendar arithmetic. It compares the year, month and day of the two dates, borrowing from the previous month when the target day is earlier than the birth day, and from the previous year when the target month is earlier. It counts complete calendar years and months rather than dividing a total number of days.",
            "The totals are a different kind of measurement. Total days is the exact number of days between the dates. Total weeks and total months divide that day count by 7 and by about 30.437 (the average length of a month), so they are approximations rather than counts of calendar months."
        ],
        "limitations": [
            "The target date must be on or after the birth date. If it is earlier, the tool shows dashes instead of a negative age.",
            "Total months and total weeks are converted from a day count using averages, so they will not match a count of calendar months. Real months vary from 28 to 31 days.",
            "Dates are read from the calendar fields you enter, with no time of day or time zone involved.",
            "For a 29 February birth date, the result follows ordinary calendar arithmetic rather than a fixed legal convention about when the birthday falls in non-leap years. If a specific rule matters for a form or entitlement, confirm it with the organisation concerned.",
            "The tool reports an age only. It does not apply legal age thresholds or historical calendar changes."
        ],
        "privacy": "Dates are processed locally in your browser and are not saved or transmitted.",
        "faq": [
            {"q": "Can I calculate age at a past or future date?", "a": "Yes. Change the Target date to any date on or after the birth date. It defaults to today, but it is just another input — useful for backdating a record or checking an upcoming milestone."},
            {"q": "Why do total months and calendar months disagree?", "a": "Total months divides the elapsed days by 30.437, the average month length. A calendar month is 28 to 31 days, so a conversion from days will drift from a month-by-month count over long spans. Use the years/months/days line for calendar precision."},
            {"q": "What if the target date is before the birth date?", "a": "All fields show dashes. The tool does not produce a negative age, so check the order of the two dates if nothing appears."}
        ],
        "related": ["date-difference", "percentage-calculator", "bmi-calculator", "discount-calculator"]
    },
    {
        "slug": "date-difference",
        "name": "Date Difference Calculator",
        "cat": "calc",
        "popular": False,
        "icon": "Dd",
        "title": "Date Difference Calculator — Days Between Two Dates | CalcHub",
        "desc": "Count the days, weeks, months and years between two dates, with a clear choice to include or exclude the end date.",
        "h1": "Date Difference Calculator",
        "lede": "Counting days between two dates depends on whether you count the last one. A stay from the 1st to the 3rd covers two nights but three days if the final day is included — this tool lets you choose which rule applies.",
        "howto": [
            "Pick the Start date and End date. End date defaults to today.",
            "Tick Include end date if the final day should count as a full day.",
            "Read the days, weeks, months and years figures.",
            "Check the description line to confirm which counting rule was used."
        ],
        "examples": [
            "1 March to 3 March is 2 days excluding the end date, or 3 days inclusive.",
            "A project running 1 January to 31 January is 30 days excluding the end date and 31 including it.",
            "An end date before the start date returns a negative day count with the same rule applied."
        ],
        "understanding": [
            "The day count is the number of whole days between the two dates, plus one when Include end date is ticked. The description line states 'Including' or 'Excluding' so you can always see which rule produced the number.",
            "Weeks, months and years are conversions of that day count using 7, 30.437 and 365.25 days respectively. They are convenient approximations, not calendar-aware counts — a month here always has the same length."
        ],
        "limitations": [
            "By default the end date is excluded. Tick the checkbox if your count needs to include it; otherwise an inclusive span will come out one day shorter than you expect.",
            "Months and years are average-based conversions and will not match a calendar count. For exact calendar months between dates, use the Age Calculator.",
            "The tool works with dates only, not times of day.",
            "A reversed range produces a negative result rather than an error, so check the order of the dates if a minus sign appears.",
            "Historical calendar reforms and time-zone shifts are not modelled."
        ],
        "privacy": "Dates are computed in your browser and are not uploaded or stored.",
        "faq": [
            {"q": "Is the end date included?", "a": "Not by default. The unchecked state counts the days strictly between the two dates. Tick Include end date to add one, which is what you usually want for an inclusive period such as a leave of absence or an event duration."},
            {"q": "Why does 30 days show as about 0.99 months?", "a": "Months are computed by dividing the day count by 30.437, the average length of a month in the Gregorian calendar. It is a conversion for convenience, not a count of calendar months."},
            {"q": "Can I measure a range entirely in the past?", "a": "Yes. Both date fields are editable and there is no restriction to future dates."}
        ],
        "related": ["age-calculator", "percentage-calculator", "unit-converter", "discount-calculator"]
    },
    {
        "slug": "unit-converter",
        "name": "Unit Converter",
        "cat": "calc",
        "popular": False,
        "icon": "Uc",
        "title": "Unit Converter — Length, Weight, Temperature and More | CalcHub",
        "desc": "Convert between length, mass, temperature, speed, area and volume units. See the working, including why Celsius, Fahrenheit and Kelvin need a different formula.",
        "h1": "Unit Converter",
        "lede": "Most unit conversions are one multiplication: a value times a fixed ratio. Temperature is the exception. Pick a category here and the converter uses the right method for it.",
        "howto": [
            "Choose a Category. The From and To dropdowns fill with that category's units.",
            "Enter a Value and select the source and target units.",
            "The result and the working line update as you type or change a unit.",
            "Switch categories to load a different set of units."
        ],
        "examples": [
            "1 mile is 1609.344 metres, so 5 miles is 8046.72 metres.",
            "1 kilogram is about 2.2046 pounds; the result shows up to eight decimal places.",
            "100 degrees Celsius is 212 degrees Fahrenheit — an offset-and-scale formula, not a ratio.",
            "1 US gallon is 3.78541 litres."
        ],
        "understanding": [
            "For length, mass, speed, area and volume, each unit is stored as a factor relative to a base unit in that category. The conversion is value x factor(from) / factor(to). That single ratio is why a kilometre is 1000 metres and a metric ton is 1000 kilograms.",
            "Temperature cannot work that way, because Celsius and Fahrenheit have different zero points as well as different degree sizes. The converter first turns the input into Celsius, then into the target: C to F is C x 9/5 + 32, F to C is (F - 32) x 5/9, and Kelvin is Celsius plus 273.15. The working line beneath the result shows the expression used.",
            "Results are displayed with up to eight decimal places. The factors are fixed constants, so a conversion is deterministic rather than an estimate."
        ],
        "limitations": [
            "Volume units here are US customary (US cups, fluid ounces and gallons), not the imperial measures that share some of these names.",
            "Mass and weight are treated as interchangeable for everyday use; the tool does not adjust for gravity or local conditions.",
            "Rounding to eight decimal places is for display. Very large or very small values may still show a long decimal tail.",
            "One value is converted at a time. Compound units such as feet-and-inches or miles per gallon cannot be entered as a combined expression.",
            "A conversion is only as precise as the number you enter. The tool does not track significant figures."
        ],
        "privacy": "Conversions run in your browser. No value is uploaded or stored.",
        "faq": [
            {"q": "Why is temperature handled differently?", "a": "Celsius and Fahrenheit start at different zero points, so a simple ratio would be wrong: 0 C is 32 F, not 0 F. The converter normalises to Celsius first, then applies the offset and scale for the target scale."},
            {"q": "Which volume units are used?", "a": "US customary units for cups, tablespoons, teaspoons, fluid ounces and gallons, alongside millilitres, litres and cubic metres. An imperial gallon is a different quantity and is not included."},
            {"q": "Can I convert feet and inches together?", "a": "Not as a single entry. Convert one value at a time and combine them yourself, or use the BMI Calculator, which accepts feet and inches together for height."}
        ],
        "related": ["percentage-calculator", "age-calculator", "discount-calculator", "bmi-calculator"]
    },
    {
        "slug": "bmi-calculator",
        "name": "BMI Calculator",
        "cat": "calc",
        "popular": False,
        "icon": "Bi",
        "title": "BMI Calculator — Body Mass Index With Context | CalcHub",
        "desc": "Calculate BMI from height and weight in metric or imperial units. See the formula, the standard adult ranges and why BMI is a screening measure, not a diagnosis.",
        "h1": "BMI Calculator",
        "lede": "BMI condenses height and weight into a single number that is easy to track and easy to overread. This calculator shows the figure and its usual range, along with what the number cannot tell you.",
        "howto": [
            "Choose Metric (cm / kg) or Imperial (ft / in / lb). The height fields change to match.",
            "Enter your height and weight. In imperial, fill in both feet and inches.",
            "Read the BMI value and the range label beneath it.",
            "Change any value to recalculate."
        ],
        "examples": [
            "Metric: 170 cm and 70 kg gives a BMI of about 24.2.",
            "Imperial: 5 ft 7 in and 154 lb gives roughly 24.1.",
            "The same person entered in either unit system lands in the same range, because both are converted to metres and kilograms before the division."
        ],
        "understanding": [
            "BMI is weight in kilograms divided by height in metres squared: kg / m2. Imperial values are converted first — pounds to kilograms and feet plus inches to metres — so both unit systems use the same formula.",
            "The label under the result is the standard adult range: below 18.5 is Underweight, 18.5 to under 25 is Normal weight, 25 to under 30 is Overweight, and 30 or above is Obesity. The page states alongside it that BMI is a screening measure, not a medical diagnosis.",
            "The result is rounded to one decimal place, so a small change in height or weight may not move the displayed number."
        ],
        "limitations": [
            "BMI is a screening measure based only on height and weight. It does not distinguish muscle from fat, account for body shape or fat distribution, or reflect age, sex, ethnicity or fitness.",
            "It is not a medical diagnosis and should not be used to judge an individual's health on its own. Standard adult ranges do not apply to children, and may be misleading for pregnant people, athletes or older adults.",
            "This tool offers no medical advice, interpretation or recommendations. For a health assessment, speak with a qualified professional.",
            "A zero, missing or invalid value leaves the result blank rather than producing a misleading figure.",
            "The categories are the widely used adult thresholds; different organisations may publish slightly different cut-offs for specific populations."
        ],
        "privacy": "Height and weight are calculated in your browser and are not stored or transmitted.",
        "faq": [
            {"q": "What formula is used?", "a": "Weight in kilograms divided by the square of height in metres. If you choose imperial, pounds are converted to kilograms and feet plus inches to metres first, so the underlying calculation is identical."},
            {"q": "Is BMI a medical diagnosis?", "a": "No. It is a population-level screening index that ignores body composition. The result on this page is labelled as a screening measure, and it should not be read as an assessment of your health."},
            {"q": "What are the standard ranges?", "a": "Below 18.5 Underweight, 18.5 to under 25 Normal weight, 25 to under 30 Overweight, and 30 or above Obesity. These are adult thresholds."},
            {"q": "Why can two people with the same BMI be quite different?", "a": "Because the formula uses only height and total weight. Muscle mass, fat distribution, age and sex all affect health but do not appear in the number."}
        ],
        "related": ["percentage-calculator", "age-calculator", "unit-converter", "discount-calculator"]
    },
    {
        "slug": "discount-calculator",
        "name": "Discount Calculator",
        "cat": "calc",
        "popular": False,
        "icon": "Dc",
        "title": "Discount Calculator — Sale Price, Savings and Tax | CalcHub",
        "desc": "Work out the final price and the amount saved from an original price and discount percentage, with optional sales tax. Includes a worked shopping example.",
        "h1": "Discount Calculator",
        "lede": "A sale tag tells you the percentage off, not what you will actually pay. Enter the price and the discount here to see the saving, the reduced price and, if you need it, the effect of sales tax.",
        "howto": [
            "Enter the Original price and the Discount percentage.",
            "Tick Add sales tax and enter the Tax rate if tax applies where you are.",
            "Read the final price, the amount saved and the price before tax.",
            "Change any field to compare a different offer."
        ],
        "examples": [
            "A $120 jacket at 25% off: you save $30 and pay $90 before tax.",
            "With 8% sales tax ticked, that $90 becomes $97.20.",
            "A $200 item at 15% off saves $30, leaving $170 — the same dollar saving as 25% off $120, from a different percentage."
        ],
        "understanding": [
            "The discount amount is original price x discount / 100. Subtracting it gives the discounted price. The savings line shows both the dollar amount and the percentage of the original price it represents.",
            "Tax, when enabled, is applied to the discounted price rather than the original: final = discounted price x (1 + tax rate / 100). The third line always shows the pre-tax price, so you can see exactly what the tax added.",
            "Two successive discounts are not the same as adding them together. 20% off followed by another 20% off takes $100 to $64, not $60, because the second discount applies to the already-reduced $80. This tool handles one discount; to compare stacked offers, run it twice."
        ],
        "limitations": [
            "Only one discount is applied. Stacked or 'extra percent off an already reduced price' offers need to be calculated step by step.",
            "Values outside a normal range are accepted mathematically. A discount above 100% produces a negative price and a negative discount increases it; the tool does not block these, so check your inputs.",
            "Tax is a flat percentage on the discounted price. It does not model rounding rules, tax-exempt items, multiple jurisdictions or compounding.",
            "The dollar sign in the output is a label, not a currency conversion. The tool does not convert between currencies.",
            "Results are rounded to two decimal places for display."
        ],
        "privacy": "Prices are calculated in your browser and are not stored or transmitted.",
        "faq": [
            {"q": "How is the discount calculated?", "a": "Original price x discount / 100 gives the amount saved, and subtracting that from the original gives the price before tax. On $120 at 25% off, that is $30 saved and $90 to pay."},
            {"q": "Does the calculator include sales tax?", "a": "Only if you tick Add sales tax and enter a rate. It is applied to the discounted price, not the original, and the pre-tax price stays visible in the detail line."},
            {"q": "What if the discount is more than 100%?", "a": "The calculation still runs and produces a negative final price, which is not a meaningful shopping result. The tool does not clamp or validate the range, so treat anything unusual as a sign to recheck the inputs."},
            {"q": "Can I combine two discounts?", "a": "Not in one step. Apply the first discount, take the resulting price as the new original, then run the tool again. Adding the two percentages together overstates the reduction."}
        ],
        "related": ["percentage-calculator", "unit-converter", "age-calculator", "bmi-calculator"]
    },
]
