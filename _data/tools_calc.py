# -*- coding: utf-8 -*-
"""CalcHub tool registry — Part 3: Calculators (6)."""

CALC_TOOLS = [
    {
        "slug": "percentage-calculator",
        "name": "Percentage Calculator",
        "cat": "calc",
        "popular": True,
        "icon": "%",
        "title": "Percentage Calculator – Free Online Percent Calculator | CalcHub",
        "desc": "Calculate percentages online: X% of Y, X is what percent of Y, and percentage increase or decrease. Free percent calculator with instant results.",
        "h1": "Percentage Calculator",
        "lede": "Solve common percentage problems in seconds: find a percentage of a number, work out what percent one value is of another, or calculate percentage increase and decrease.",
        "howto": [
            "Choose the calculation mode: % of, is what % of, or increase/decrease.",
            "Enter the numbers for the mode you selected.",
            "The result updates instantly.",
            "Use the result in your work immediately — no signup needed."
        ],
        "examples": [
            "What is 15% of 240? Answer: 36.",
            "You scored 42 out of 60 — that is 70%.",
            "A price rises from 80 to 96 — that is a 20% increase."
        ],
        "features": [
            "X% of Y calculation",
            "X is what percent of Y",
            "Percentage increase and decrease",
            "Handles zero and invalid inputs gracefully"
        ],
        "privacy": "Calculations run entirely in your browser. No values are sent to or stored on any server.",
        "faq": [
            {"q": "How do I calculate X% of Y?", "a": "Multiply Y by X and divide by 100. For example, 15% of 240 = 240 × 15 / 100 = 36. The calculator does this instantly."},
            {"q": "What does 'is what percent of' mean?", "a": "It tells you what percentage one number is of another. If 30 is what percent of 150, the answer is 20%."},
            {"q": "Can it handle percentage decrease?", "a": "Yes. Select the increase/decrease mode and enter the original and new values. A negative result shows a decrease."}
        ],
        "related": ["discount-calculator", "bmi-calculator", "unit-converter", "age-calculator"]
    },
    {
        "slug": "age-calculator",
        "name": "Age Calculator",
        "cat": "calc",
        "popular": True,
        "icon": "Ae",
        "title": "Age Calculator – Calculate Age Online Free | CalcHub",
        "desc": "Calculate exact age in years, months and days from any birth date. Free online age calculator with optional target date.",
        "h1": "Age Calculator",
        "lede": "Find out exactly how old someone is in years, months and days. Pick a birth date and (optionally) a target date — the calculator handles leap years and month boundaries correctly.",
        "howto": [
            "Pick the birth date.",
            "Optionally set a target date; it defaults to today.",
            "See the age in years, months and days.",
            "Check the extra details like total months and days."
        ],
        "examples": [
            "A child born on 29 February 2016 has their birthday on 28 February in non-leap years.",
            "Calculate the exact age of a document or contract signed years ago.",
            "Find how many days old a new project is for an anniversary."
        ],
        "features": [
            "Age in years, months and days",
            "Optional target date",
            "Correct leap-year and month-boundary handling",
            "Shows total months, total weeks and total days"
        ],
        "privacy": "Dates are calculated locally in your browser and are not saved or transmitted.",
        "faq": [
            {"q": "How is a leap-day birthday handled?", "a": "If someone is born on 29 February, we treat the birthday as 28 February in non-leap years and 1 March in some conventions. We use the standard 28 February approach for non-leap years."},
            {"q": "Can I calculate age at a past or future date?", "a": "Yes. Set a custom target date to calculate age as of that date."},
            {"q": "Do the months consider exact month lengths?", "a": "Yes. The day difference uses real calendar days, so month lengths are handled correctly."}
        ],
        "related": ["date-difference", "percentage-calculator", "bmi-calculator", "discount-calculator"]
    },
    {
        "slug": "date-difference",
        "name": "Date Difference Calculator",
        "cat": "calc",
        "popular": False,
        "icon": "Dd",
        "title": "Date Difference Calculator – Days Between Dates | CalcHub",
        "desc": "Calculate the number of days, weeks, months and years between two dates. Free online date difference calculator with calendar-day precision.",
        "h1": "Date Difference Calculator",
        "lede": "Find out how many days are between two dates, including an option to count the end date. Results are based on real calendar days, so daylight saving or time zones do not skew the answer.",
        "howto": [
            "Pick the start date.",
            "Pick the end date.",
            "Choose whether to include the end date in the count.",
            "Read the difference in days, weeks, months and years."
        ],
        "examples": [
            "How many days until a project deadline?",
            "Trip duration between departure and return dates.",
            "Contract length between a start and end date."
        ],
        "features": [
            "Days, weeks, months and years between dates",
            "Option to include or exclude the end date",
            "Calendar-day based, immune to DST errors",
            "Works across date order (can be negative)"
        ],
        "privacy": "All date math happens locally in your browser. Nothing is stored or sent.",
        "faq": [
            {"q": "Does 'include end date' change the result?", "a": "Yes. Excluding the end date counts the number of full days between the two dates. Including it adds one day (useful for booking nights or subscription lengths)."},
            {"q": "Is daylight saving handled?", "a": "Yes. We work with calendar dates rather than fixed milliseconds, so DST changes do not affect the day count."},
            {"q": "What if I reverse the dates?", "a": "The result is shown as a negative number so you can spot the order. Swap the dates for a positive count."}
        ],
        "related": ["age-calculator", "percentage-calculator", "unit-converter", "discount-calculator"]
    },
    {
        "slug": "unit-converter",
        "name": "Unit Converter",
        "cat": "calc",
        "popular": False,
        "icon": "Uc",
        "title": "Unit Converter – Length, Weight, Temperature, Speed | CalcHub",
        "desc": "Convert units online: length, weight, temperature, speed and more. Free unit converter with accurate factors and temperature formulas.",
        "h1": "Unit Converter",
        "lede": "Convert between units of length, mass, temperature, speed, area and volume with accurate, tested factors. Temperature uses the correct formulas rather than a simple factor.",
        "howto": [
            "Select a category (e.g. Length, Temperature).",
            "Choose the input unit and output unit.",
            "Type the value to convert.",
            "See the result instantly, updated live."
        ],
        "examples": [
            "Convert 5 feet 6 inches to centimetres — useful for health forms.",
            "Convert 25 kilograms to pounds for a shipping label.",
            "Convert 30°C to Fahrenheit for a weather forecast: 86°F."
        ],
        "features": [
            "Length, mass, temperature, speed, area and volume categories",
            "Correct temperature conversion formulas",
            "Live conversion as you type",
            "Large set of common units"
        ],
        "privacy": "Conversions run locally in your browser. No input is stored or sent anywhere.",
        "faq": [
            {"q": "Which units are included?", "a": "We cover the most common units in each category: metric and imperial for length and mass, Celsius/Fahrenheit/Kelvin for temperature, mph/kph/knots for speed, plus common area and volume units."},
            {"q": "How is temperature converted?", "a": "Using the standard formulas: °F = °C × 9/5 + 32, and the reverse for °C to °F. Kelvin uses its offset correctly."},
            {"q": "Are conversion factors rounded?", "a": "We use precise factors and round only the final display. Results are accurate for practical purposes."}
        ],
        "related": ["percentage-calculator", "age-calculator", "discount-calculator", "bmi-calculator"]
    },
    {
        "slug": "bmi-calculator",
        "name": "BMI Calculator",
        "cat": "calc",
        "popular": False,
        "icon": "Bi",
        "title": "BMI Calculator – Calculate Body Mass Index Online | CalcHub",
        "desc": "Calculate your Body Mass Index (BMI) from height and weight. Free online BMI calculator with metric and imperial units.",
        "h1": "BMI Calculator",
        "lede": "Calculate your Body Mass Index using height and weight in metric or imperial units. BMI is a simple screening measure — it is not a medical diagnosis.",
        "howto": [
            "Choose your preferred unit system (metric or imperial).",
            "Enter your height and weight.",
            "See your BMI and the standard category range.",
            "Read the note explaining what BMI does and does not measure."
        ],
        "examples": [
            "A person 1.75 m tall and 70 kg has a BMI of about 22.9.",
            "A 5'9\" adult weighing 165 lb has a BMI of about 24.4.",
            "Track BMI over time as a rough weight trend marker."
        ],
        "features": [
            "Metric and imperial units",
            "Standard BMI formula and category ranges",
            "Clear non-medical disclaimer",
            "Instant calculation"
        ],
        "privacy": "Your height and weight are calculated locally in your browser and are never stored or transmitted.",
        "faq": [
            {"q": "What BMI formula is used?", "a": "Metric: weight (kg) divided by height (m) squared. Imperial: 703 × weight (lb) / height (in) squared. Both produce the same BMI value."},
            {"q": "Is BMI a medical diagnosis?", "a": "No. BMI is a general screening measure. It does not account for muscle mass, bone density, age, sex or distribution of fat. Always consult a healthcare professional for health decisions."},
            {"q": "What are the standard categories?", "a": "Underweight below 18.5, normal 18.5–24.9, overweight 25–29.9, and obesity 30 and above. Ranges can vary slightly by organisation."}
        ],
        "related": ["percentage-calculator", "age-calculator", "unit-converter", "discount-calculator"]
    },
    {
        "slug": "discount-calculator",
        "name": "Discount Calculator",
        "cat": "calc",
        "popular": False,
        "icon": "Dc",
        "title": "Discount Calculator – Calculate Sale Price Online Free | CalcHub",
        "desc": "Calculate the final price after a discount and how much you save. Free online discount calculator with percent-off and final price.",
        "h1": "Discount Calculator",
        "lede": "Enter the original price and a discount percentage to see the final price, the exact amount you save, and what fraction of the price remains.",
        "howto": [
            "Enter the original price.",
            "Enter the discount percentage.",
            "The final price and savings update instantly.",
            "Optionally add tax if your price is pre-tax."
        ],
        "examples": [
            "A $120 jacket at 25% off costs $90 — you save $30.",
            "A 10% discount on a $55 order saves $5.50.",
            "Price with 7% sales tax added after a 15% discount."
        ],
        "features": [
            "Final price after discount",
            "Exact amount saved",
            "Optional tax addition",
            "Handles invalid or negative inputs gracefully"
        ],
        "privacy": "All calculations happen locally in your browser. No values are stored or sent.",
        "faq": [
            {"q": "How is the discount calculated?", "a": "Discount amount = original price × discount % / 100. Final price = original − discount. If tax is enabled, we add the tax rate to the discounted price."},
            {"q": "What if the discount is more than 100%?", "a": "We show the price going below zero to flag an invalid discount. Real discounts should be between 0% and 100%."},
            {"q": "Does the calculator include sales tax?", "a": "Only if you enable the tax field. By default the result is pre-tax."}
        ],
        "related": ["percentage-calculator", "unit-converter", "age-calculator", "bmi-calculator"]
    },
]