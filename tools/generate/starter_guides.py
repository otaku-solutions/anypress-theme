# Starter pages from the Fluent plugins' own guides (Fluent Forms, FluentBooking, FluentCart): quote, project and
# onboarding forms, a home valuation, a restaurant's order and menu pages, a church's plan-your-visit page, booking
# pages for a consultation, a dental practice, a salon and a class studio, and cancellation and return policies.
# Run by kits.py after the kits, so every helper above is in scope.
#
# Each page is a whole designed page in its own layout, photo-led, built from the theme's section styles, AnyPress
# Blocks (carousel, counter, map) and core blocks, so it looks right in every kit's style. Photos are placeholders
# with their own alt text, for the owner's photos (and the preview's).
#
# A form or booking calendar goes in a spot: a group with the class "anypress-slot", named "Form: <key>" or
# "Booking calendar", inside a card. On any site the owner puts their form block in it. On an AnyPress store the store
# template swaps it for Fluent Forms' or FluentBooking's own block when the page is saved (anypress-starter-forms.php),
# so keep the names and keys stable: quote, project, onboarding, valuation, order, visit, consultation.

import re

ANCHORS.update({"Quote form": "quote", "Project form": "project", "Onboarding form": "start", "Valuation form": "valuation",
                "Order form": "order", "Visit form": "visit", "Consultation form": "consult", "Booking": "book",
                "Breakfast": "breakfast", "Lunch": "lunch", "Cakes": "cakes", "Drinks": "drinks", "Timetable": "timetable",
                "Cancelling": "cancelling", "No-shows": "no-shows", "Deposits": "deposits", "Returns": "returns", "Refunds": "refunds", "Exchanges": "exchanges", "Map": "map"})

# Headings, buttons and question titles on these pages are in Title Case (the owner's rule for AnyPress UI labels);
# the kits' own helpers are wrapped here and put back at the end of this file.
SMALL = set("a an and as at but by for from in into nor of on or per the to vs via with".split())
def title_case(text):
    words = re.split(r"(\s+|<[^>]+>)", text)
    idx = [i for i, w in enumerate(words) if w and not w.isspace() and not w.startswith("<")]
    for n, i in enumerate(idx):
        w = words[i]
        if any(c.isupper() for c in w[1:]) or not w[:1].isalpha() and not w[:1] in "“\"'(":
            continue
        core = w.lstrip("“\"'(")
        lead = w[:len(w) - len(core)]
        if n not in (0, len(idx) - 1) and core.lower().rstrip(".,:;!?") in SMALL and not (n > 0 and words[idx[n - 1]].endswith((":", ".", "?", "!"))):
            continue
        words[i] = lead + "-".join(part[:1].upper() + part[1:] for part in core.split("-"))
    return "".join(words)
_h, _btns, _details = h, btns, details
def h(text, *a, **k): return _h(title_case(text), *a, **k)
def btns(items, *a, **k): return _btns([(title_case(i[0]),) + tuple(i[1:]) for i in items], *a, **k)
def details(summary, *a, **k): return _details(title_case(summary), *a, **k)

STARS = "★★★★★"

def slot(name, note):
    """Where a form or booking calendar goes: a plain group the store template fills, with a line saying what goes there."""
    a = {"metadata": {"name": name}, "className": "anypress-slot", "layout": {"type": "default"}}
    return f'<!-- wp:group {j(a)} -->\n<div class="wp-block-group anypress-slot">' + p(note, "small", "secondary") + '</div>\n<!-- /wp:group -->'

def form_slot(key, what):
    return slot(f"Form: {key}", f"The {what} goes here. Put your form block in this box.")

def booking_slot():
    return slot("Booking calendar", "The booking calendar goes here: every service, with its free times. Put your booking block in this box.")

def form_card(title, note, key, what, name=None):
    """The form on a raised card: a title, a line on how long it takes, and the form."""
    inner = N([h(title, 2, "large"), p(note, "small", "secondary"), form_slot(key, what)])
    return grp(inner, "section-card", ("large", "large", "large", "large"), "small", {"type": "default"}, name=name, radius="md")

def cal_card(title, note):
    return grp(N([h(title, 2, "large"), p(note, "small", "secondary"), booking_slot()]), "section-card", ("large", "large", "large", "large"), "small", {"type": "default"}, radius="md")

def count(number, suffix="", prefix="", decimals=0, size="xxx-large"):
    a = {"number": number}
    if decimals: a["decimals"] = decimals
    if prefix: a["prefix"] = prefix
    if suffix: a["suffix"] = suffix
    a.update({"style": {"typography": {"fontWeight": "700", "lineHeight": "1"}}, "fontSize": size})
    return f'<!-- wp:anypress/counter {j(a)} /-->'

def numbers(items, style="section-dark", pad=("x-large", "x-large", None, None)):
    """Facts that count up: (number, suffix, prefix, decimals, label)."""
    return sec("Numbers", grid([stackg([count(n, sfx, pre, d, "xx-large"), p(lbl)], "x-small") for n, sfx, pre, d, lbl in items], 4, "12rem", "large"), style, pad)

def ticks(items, size=None):
    """Short promises, each after a tick."""
    return stackg([p("✓&nbsp;&nbsp;" + T(i), size, None, None, None, None, True) for i in items], "x-small")

def rating(text):
    return p(f'<strong>{STARS}</strong>&nbsp; ' + T(text), "small", None, None, None, None, True)

def gstep(n, file, alt, title, text):
    """A numbered step with a photo above it."""
    return stackg([img(file, alt, "4/3", "md"), mono(n, "primary"), h(title, 3, "large"), p(text, None, "secondary")], "small")

def nstep(n, title, text, style="section-card"):
    """A numbered step on a card, no photo."""
    return grp(N([p(n, "xx-large", "primary", None, None, {"lineHeight": "1", "fontWeight": "700"}), h(title, 3, "medium"), p(text, None, "secondary")]), style, PAD_CARD, "small", {"type": "default"}, radius="md")

def big_card(big, title, text, style="section-card"):
    """A fact at a glance: a big figure, what it is and one line. On the dark style the line keeps the section's own colour."""
    return grp(N([p(big, "xx-large", None, None, None, {"lineHeight": "1", "fontWeight": "700"}), h(title, 3, "medium"), p(text, "small", None if style == "section-dark" else "secondary")]), style, PAD_CARD, "small", {"type": "default"}, radius="md")

def review_card(text, who):
    return grp(N([p(STARS, None, "primary"), p(f"“{text}”", "medium", None, None, None, {"lineHeight": "1.45"}), mono(who)]), "section-card", PAD_CARD, "small", {"type": "default"}, radius="md")

def reviews(title, items, style="section-tint", lead=None):
    head = [h(title, 2, "xx-large")] + ([rating(lead)] if lead else [])
    return sec("Reviews", N([stackg(head, "small"), carousel([review_card(*r) for r in items], 3, title)]), style)

def split(name, file, alt, inner, flip=False, style=None, minh=34, inner_style=None):
    """A photo edge to edge beside the words."""
    photo = col(fill(file, minh, alt), "50%")
    words = col(N(inner), None, inner_style, ("xx-large", "xx-large", "x-large", "x-large"), "center")
    return sec(name, cols([words, photo] if flip else [photo, words], "0", "full", None), style, (None, None, None, None), layout={"type": "default"})

def faq_split(items, aside, style=None, title="Questions people ask"):
    """Questions in an accordion beside a card with another way to get an answer."""
    return sec("Questions", cols([
        col(N([h(title, 2, "xx-large"), aside]), "38%"),
        col(accordion(items))], "xx-large", "wide", "top"), style)

def ask_card(title, text, buttons, style="section-brand"):
    return grp(N([h(title, 3, "large"), p(text), btns(buttons)]), style, PAD_CARD, "small", {"type": "default"}, radius="md")

def closing(name, file, alt, title, text, buttons):
    """The last section: a photo band with one more way to act."""
    return cover(on_photo(grp(N([h(title, 2, "xxx-large", "center"), p(text, "large", None, "center"), btns(buttons, "center")]), gap="medium", layout={"type": "constrained", "contentSize": "44rem"})),
                 name, "placeholder-wide.svg", 60, "60vh", "center center", ("xx-large", "xx-large", "medium", "medium"), "44rem", alt=alt)

def hero_form(eyebrow, title, text, promises, rating_text, card, file, alt, dim=60):
    """A photo filling the screen, the promise on the left and the form on a card to the right, so it's the first thing seen."""
    left = on_photo(grp(N([mono(eyebrow, None), h(title, 1, "xxx-large", None, None, {"lineHeight": "1.05"}), p(text, "large"), ticks(promises, "medium"), rating(rating_text)]),
                        gap="medium", layout={"type": "default"}))
    return cover(cols([col(left, "52%", valign="center"), col(card, None, valign="center")], "xx-large", "wide", "center"),
                 "Hero", "placeholder-wide.svg", dim, "92vh", "center center", ("xx-large", "xx-large", "medium", "medium"), "80rem", alt=alt)

def chips(items):
    """Small facts in a row, each on its own soft card."""
    return row([grp(p(i, "small", None, None, None, {"fontWeight": "600"}), "section-brand-soft", ("x-small", "x-small", "small", "small"), radius="full") for i in items], "left", "small")

def photo_card(file, alt, title, text, price=None):
    meta = [row([h(title, 3, "medium"), p(price, "medium", None, None, None, {"fontWeight": "700"})], "space-between", "small", False, "top")] if price else [h(title, 3, "medium")]
    return stackg([img(file, alt, "1", "md")] + meta + [p(text, "small", "secondary")], "small")

def menu_line(name, text, price, tags=None, sub="secondary"):
    lead = grp(N([h(name, 3, "medium"), p(price, "medium")]), "menu-leader", layout={"type": "flex", "flexWrap": "nowrap", "justifyContent": "space-between", "verticalAlignment": "bottom"})
    under = text + (f" · {tags}" if tags else "")
    return stackg([lead, p(under, "small", sub)], "x-small")

def portrait(file, alt, name, role):
    return stackg([img(file, alt, "3/4", "md"), h(name, 3, "medium"), p(role, "small", "secondary")], "x-small")

def toc(items):
    """Links to each part of a long page, sticky beside it on a computer."""
    return grp(N([mono("On this page"), links(items)]), "sticky", None, "small", {"type": "default"})

def clause(title, paragraphs, items=None, anchor=None):
    hd = h(title, 2, "x-large")
    if anchor: hd = hd.replace('<!-- wp:heading {', '<!-- wp:heading {"anchor":"' + anchor + '",', 1).replace('<h2 class=', f'<h2 id="{anchor}" class=', 1)
    return stackg([hd] + [p(t, "medium") for t in paragraphs] + ([lst(items)] if items else []), "small")

# ---------------------------------------------------------------- Request a quote (trades)
page("page-quote", "Request a quote page",
 "A Request a quote page for trades and home services: a photo of the work with the quote form on a card beside the promise (free, fixed, fast), numbers that count up, how quoting works in three steps with photos, what every quote includes beside a photo of a finished job, reviews in a carousel, and questions beside a call-us card. Needs the AnyPress Blocks plugin. On AnyPress the form box becomes a Fluent Forms form when the page is saved.",
 "quote, request a quote, estimate, free quote, price, form, trades, plumber, builder, services",
 [hero_form("Free, written quotes", "Tell us about the job. Get a fixed price in two days.",
   "A real person reads every request the same day. No call centre, no pushy follow-ups.",
   ["Free, with no obligation", "A fixed price in writing, valid for 30 days", "Licensed, insured and guaranteed"], "4.9 from 380 local reviews",
   form_card("Request your quote", "One question at a time. About two minutes.", "quote", "quote form", "Quote form"),
   "placeholder-wide.svg", "A tradesperson at work in a customer's home"),
  numbers([(25, "", "", 0, "years in business"), (4000, "+", "", 0, "jobs finished"), (4.9, "", "", 1, "average from 380 reviews"), (2, " days", "", 0, "to get your quote")]),
  sec("How quoting works", N([stackg([mono("How it works"), h("Three steps to a price you can trust", 2, "xx-large")], "small"), grid([
    gstep("01", "placeholder-wide.svg", "Someone reading a quote request at a desk", "We read it the same day", "If anything is unclear we call you, so the price is right first time."),
    gstep("02", "placeholder-wide.svg", "A tradesperson measuring up in a customer's home", "We visit if it's needed", "Bigger jobs get a free visit to measure up. Small ones we price from your photos."),
    gstep("03", "placeholder-wide.svg", "A finished job, neat and tidy", "You get a fixed price", "In writing, with what's included and when we can start. No pressure to say yes.")], 3, "15rem", "x-large")])),
  split("What's included", "placeholder-tall.svg", "A finished job, photographed for the customer", [
    mono("Every quote includes"), h("Fixed means fixed", 2, "xx-large"),
    p("The price we quote is the price you pay, unless you change the job. If we find something hidden, we stop and ask before doing anything.", "medium"),
    ticks(["Every part and every hour, itemised", "Clearing up and taking away the waste", "A start date and how long it will take", "A one-year guarantee on our work"], "medium")], True, "section-tint", 38),
  reviews("What customers say", [
    ("The quote came the next morning and the final bill matched it to the cent. That never happens.", "Dana R. · Kitchen sink and tap"),
    ("They sent photos of the leak before and after. Tidy, quick and polite.", "Marcus T. · Burst pipe"),
    ("Three firms quoted. These were the only ones who explained every line.", "Priya S. · New boiler"),
    ("Booked for Tuesday, done by Tuesday lunchtime. Will use again.", "Joan W. · Bathroom refit")], None, "4.9 from 380 reviews on Google"),
  faq_split([("Is the quote really free?", "Yes, and so is the visit. You only pay if you go ahead."),
             ("How long is a quote valid?", "30 days. After that we check prices again before we start."),
             ("Can you work to my budget?", "Tell us your budget and we'll say honestly what it covers, and what we'd leave out."),
             ("Do you need to visit?", "Only for bigger jobs. For small repairs, a couple of photos is enough.")],
   ask_card("Rather talk?", "Call us and we'll take the details over the phone.", [("Call 555 0142", None, "tel:5550142", "phone")]))])

# ---------------------------------------------------------------- Project inquiry (studios, agencies, consultants)
page("page-project-inquiry", "Project inquiry page",
 "A project inquiry page for design studios, architects and agencies, set like an editorial page: one big sentence and the ways to get in touch beside the project brief form on a card, selected work in staggered photos with numbered captions, how a project runs in four phases, typical budgets and timelines in a table, a client's words on the dark section style and questions. On AnyPress the form box becomes a Fluent Forms form when the page is saved.",
 "project inquiry, project brief, start a project, agency, studio, consultant, designer, form, work with us",
 [sec("Start a project", cols([
    col(N([mono("Start a project"), h("Let's make something worth keeping.", 1, "poster", None, None, {"lineHeight": "0.95"}),
           p("Tell us what you're building. A short brief lets us come to the first call with ideas, not just questions.", "large", "secondary"),
           grid([stackg([mono(a), p(b, "medium", bind=k)], "x-small") for a, b, k in [("Email", "hello@example.com", "email_linked"), ("Phone", "555 0142", "phone_linked"), ("Studio", "14 Market Street, Springfield", "address"), ("Replies", "Within one working day", None)]], 2, "12rem", "medium")]), "55%"),
    col(form_card("Project brief", "One question at a time. Rough answers are fine.", "project", "project brief form"))], "xx-large", "wide", "top"), pad=("xx-large", "xx-large", None, None)),
  sec("Selected work", N([row([h("Selected work", 2, "xx-large"), mono("2023 to now")], valign="bottom"), cols([
    col(stackg([captioned("placeholder-tall.svg", "A project photo: a white spiral staircase", "4/5", "01 — A stair for a city library, 2025"),
                captioned("placeholder-wide.svg", "A project photo: a bright dining room", "4/3", "03 — A family home on Hill Street, 2024")], "xx-large"), "55%"),
    col(stackg([captioned("placeholder-tall.svg", "A project photo: a white apartment block", "3/4", "02 — Twelve flats by the river, 2025"),
                captioned("placeholder-tall.svg", "A project photo: stalls under a market hall roof", "3/4", "04 — The market hall, reopened, 2023")], "xx-large"), None, None, None, "bottom")], "x-large", "wide", None)])),
  sec("How we work", N([stackg([mono("How a project runs"), h("Four phases, no surprises", 2, "xx-large")], "small"), grid([
    nstep("Weeks 1–2", "Discover", "We visit, measure and listen to how you use the space. We agree goals, scope and fee in writing."),
    nstep("Weeks 3–5", "Shape", "Two or three directions, shown early and rough, so we pick one together before polishing."),
    nstep("Weeks 6–9", "Develop", "Drawings, materials and a cost plan for the chosen direction, with a short check-in every week."),
    nstep("Week 10 on", "Build", "We find the builder and visit the site every week until handover.")], 4, "13rem", "medium")]), "section-tint"),
  sec("Budgets", cols([
    col(N([h("Typical projects", 2, "xx-large"), p("Every project is priced on its own, but these are the usual ranges, so you know before you write.", "medium", "secondary")]), "38%"),
    col(table(["Project", "Usually costs", "Takes"], [["Interiors for one room", "$4,000 to $9,000", "4 to 6 weeks"], ["Kitchen or extension", "$12,000 to $30,000", "3 to 5 months"],
                                                     ["Whole-house renovation", "$30,000 to $60,000", "6 to 9 months"], ["A new building", "From 8% of the build cost", "Quoted on its own"]], "stripes"))], "xx-large", "wide", "top")),
  sec("Client words", N([quote("They asked better questions in the first call than we had asked ourselves in a year. The house works for how we actually live.", "Maya Chen, Hill Street", "xx-large")]), "section-dark", content="56rem"),
  faq_split([("Is there a minimum budget?", "Most projects start at $4,000. If yours is smaller, write anyway and we'll suggest someone good if it isn't us."),
             ("Do you sign an NDA?", "Yes, before the first call if you'd like."),
             ("Can you work with our builder?", "Yes. We can lead the build, or work alongside a builder you already trust."),
             ("When could you start?", "Usually within four to six weeks. We'll tell you on the first call.")],
   ask_card("Prefer a call first?", "Book 20 minutes with us and talk it through before you write a brief.", [("Email us", None, "mailto:hello@example.com", "email_link")], "section-brand-soft"))])

# ---------------------------------------------------------------- Client onboarding (accountants, consultants, agencies)
page("page-client-onboarding", "Client onboarding page",
 "A welcome page for new clients: a thank-you beside a photo of the team, the onboarding form beside a numbered checklist of the steps, what to have ready on tiles, the first thirty days as a timeline, the people they'll work with and a note on keeping passwords safe. On AnyPress the form box becomes a Fluent Forms form when the page is saved.",
 "client onboarding, welcome, new client, intake, getting started, form, accountant, consultant, agency",
 [split("Welcome", "placeholder-tall.svg", "The team in their office, smiling", [
    mono("Welcome aboard", None), h("Glad you're here. Let's get you set up.", 1, "xxx-large", None, None, {"lineHeight": "1.05"}),
    p("This page has everything for your first month with us: one form, what to have ready and what happens when.", "large"),
    btns([("Fill in the form", None, "#start")])], False, "section-brand", 40),
  sec("Onboarding form", cols([
    col(grp(N([mono("Your checklist"), stackg([stackg([row([p(n, "large", "primary", None, None, {"fontWeight": "700", "lineHeight": "1"}), h(t, 3, "medium")], "left", "small", False, "center"), p(d, "small", "secondary")], "x-small") for n, t, d in [
        ("1", "Your details", "The business, who we talk to and who gets invoices."),
        ("2", "Your goals", "What a good first year looks like to you."),
        ("3", "Your tools", "The accounts and apps we'll need. No passwords."),
        ("4", "Your kick-off", "Pick a time for an hour together.")]], "large")]), "sticky", None, "medium", {"type": "default"}), "34%"),
    col(form_card("Your details", "One question at a time. Skip anything you don't know yet.", "onboarding", "onboarding form"))], "xx-large", "wide", "top"), "section-tint", content="72rem"),
  sec("Have ready", N([stackg([mono("Before you start"), h("Have these to hand", 2, "xx-large")], "small"), grid([
    big_card("01", "Legal name and number", "Your business's registered name, number and address."),
    big_card("02", "Who gets invoices", "A name and email, and a purchase order number if you use them."),
    big_card("03", "Last year's figures", "Accounts, reports or anything that shows where you are now."),
    big_card("04", "A list of your tools", "Bank, bookkeeping, email, website: just the names for now.")], 4, "13rem", "medium")])),
  sec("First 30 days", N([stackg([mono("Your first month"), h("What happens when", 2, "xx-large")], "small"), grid([
    stackg([sep(), mono("Day 1", "primary"), h("Kick-off", 3, "large"), p("An hour to agree goals, dates and how we'll keep in touch.", None, "secondary")]),
    stackg([sep(), mono("Week 1", "primary"), h("Access", 3, "large"), p("We send a safe way to share logins and set up your shared folder.", None, "secondary")]),
    stackg([sep(), mono("Weeks 2–3", "primary"), h("Set-up", 3, "large"), p("We read everything, tidy what needs it and build your plan.", None, "secondary")]),
    stackg([sep(), mono("Day 30", "primary"), h("First review", 3, "large"), p("Your first report: what's done, what we found and what's next.", None, "secondary")])], 4, "13rem", "large")]), "section-brand-soft"),
  sec("Your team", N([stackg([mono("Who you'll work with"), h("Your team", 2, "xx-large")], "small"), grid([
    portrait("placeholder-tall.svg", "Portrait of your account lead", "Helen Park", "Your account lead. Your first call for anything."),
    portrait("placeholder-tall.svg", "Portrait of your specialist", "David Osei", "Your specialist. Does the detailed work each month."),
    portrait("placeholder-tall.svg", "Portrait of the office manager", "Mei Lin", "Office manager. Invoices, meetings and access.")], 3, "9rem", "large")])),
  sec("Passwords", cols([col(N([h("Never send a password in a form or email", 2, "x-large"), p("List the accounts we'll need and we'll send a secure link to share access. You can take it back at any time.", "medium")])),
    col(btns([("Questions? Email us", "outline", "mailto:hello@example.com", "email_link")], "right"), "30%", valign="center")], "x-large", "wide", "center"), "section-dark", ("x-large", "x-large", None, None))])

# ---------------------------------------------------------------- Home valuation (real estate)
page("page-home-valuation", "Home valuation page (real estate)",
 "A free valuation page for an estate agent or realtor: a photo of a home with the valuation form on a card beside the promise, the agency's record in numbers that count up, how a valuation works in three steps with photos, homes recently sold nearby, the agent beside a portrait, and questions. Needs the AnyPress Blocks plugin. On AnyPress the form box becomes a Fluent Forms form when the page is saved.",
 "valuation, home value, what is my home worth, appraisal, sell my home, realtor, estate agent, real estate, form",
 [hero_form("Free, without obligation", "What is your home worth today?",
   "A local agent visits, looks at what's sold on your street and gives you a price you can plan with.",
   ["A price in writing within two days", "Based on real sales nearby, not an algorithm", "No obligation to sell with us"], "4.9 from 210 sellers",
   form_card("Get your free valuation", "A few quick questions. We call within one working day.", "valuation", "valuation form", "Valuation form"),
   "placeholder-wide.svg", "A house for sale on a quiet street", 50),
  numbers([(340, "", "", 0, "homes sold since 2019"), (21, " days", "", 0, "on the market, on average"), (98, "%", "", 0, "of asking price achieved"), (4.9, "", "", 1, "average from 210 reviews")], "section-brand"),
  sec("How it works", N([stackg([mono("How a valuation works"), h("A price you can plan with", 2, "xx-large")], "small"), grid([
    gstep("01", "placeholder-wide.svg", "A bright kitchen in a family home", "Tell us about the home", "A few details through the form, or by phone if you prefer."),
    gstep("02", "placeholder-wide.svg", "A living room with a sofa and a fireplace", "We walk round together", "About 45 minutes. We look at what's been done and answer your questions."),
    gstep("03", "placeholder-wide.svg", "House keys on a table", "Your valuation in writing", "The price we'd market it at, the homes we compared it with, and why.")], 3, "15rem", "x-large")])),
  sec("Recently sold", N([row([h("Sold nearby", 2, "xx-large"), p('<a href="/homes/">' + T("All homes for sale") + "</a>", "medium", raw=True)], valign="bottom"), grid([
    stackg([img("placeholder-wide.svg", "A sold home: a stone house with a garden", "4/3", "md"), mono("Sold in 12 days", "primary"), p("$612,000", "xx-large", None, None, None, {"lineHeight": "1", "fontWeight": "700"}), p("4 Mill Road, Kingston", "medium"), p("4 bed · 3 bath · 2,400 sq ft", "small", "secondary")], "x-small"),
    stackg([img("placeholder-wide.svg", "A sold home: a white farmhouse", "4/3", "md"), mono("Sold over asking", "primary"), p("$489,000", "xx-large", None, None, None, {"lineHeight": "1", "fontWeight": "700"}), p("12 Orchard Lane, Rhinebeck", "medium"), p("3 bed · 2 bath · 1,850 sq ft", "small", "secondary")], "x-small"),
    stackg([img("placeholder-wide.svg", "A sold home: a brick townhouse", "4/3", "md"), mono("Sold in 9 days", "primary"), p("$375,000", "xx-large", None, None, None, {"lineHeight": "1", "fontWeight": "700"}), p("31 Union Street, Hudson", "medium"), p("2 bed · 2 bath · 1,200 sq ft", "small", "secondary")], "x-small")], 3, "16rem", "large")]), "section-tint"),
  split("Agent", "placeholder-tall.svg", "Portrait of the agent", [
    mono("Your agent"), h("Claire Hollis", 2, "xxx-large"),
    quote("I'll tell you what your home is worth, not what you want to hear. That's how it sells.", "Claire, 22 years selling in the valley", "large"),
    btns([("Call Claire", None, "tel:5550186", "phone"), ("Email", "outline", "mailto:hello@example.com", "email_link")])], False, None, 36),
  faq_split([("Do I have to sell with you?", "No. The valuation is free, whatever you decide."),
             ("Is an online estimate enough?", "It's a start, but it can't see your kitchen, your garden or the work you've done. A visit can."),
             ("How soon can you come?", "Usually within three days, evenings and Saturdays included."),
             ("I'm buying too. Can you help?", "Yes. Tell us what you're looking for and we'll send homes before they're advertised.")],
   ask_card("Thinking of selling next year?", "We'll value it now and send a free update every six months.", [("Call 555 0186", None, "tel:5550186", "phone")], "section-brand-soft"))])

# ---------------------------------------------------------------- Order online (restaurants, cafés, bakeries)
page("page-order-pickup", "Order online page (restaurant)",
 "An order page for a restaurant, café or bakery: a food photo with the order form on a card beside pickup times and how paying works, today's favourites as photo cards with prices, how pickup works in three steps, the opening hours, address and a map, and a catering offer. Needs the AnyPress Blocks plugin. On AnyPress the form box becomes a Fluent Forms form when the page is saved. Shops that take card payments use the online store instead.",
 "order online, takeaway, pickup, collection, delivery, restaurant, cafe, bakery, food, form",
 [hero_form("Order ahead", "Order online. Skip the queue.",
   "Order by noon for lunch, by 5pm for dinner. We text you the moment it's ready.",
   ["Ready in about 20 minutes", "Pickup or delivery within three miles", "Pay by card or cash when you collect"], "4.8 from 520 reviews",
   form_card("Your order", "One step at a time. We text to confirm the total and the time.", "order", "order form", "Order form"),
   "placeholder-wide.svg", "Fresh pastries on the counter, ready to take away", 60),
  sec("Favourites", N([row([stackg([mono("Today's favourites"), h("What people order most", 2, "xx-large")], "small"), p('<a href="/menu/">' + T("See the full menu") + "</a>", "medium", raw=True)], valign="bottom"), grid([
    photo_card("placeholder-square.svg", "A croissant on a plate", "Butter croissant", "Laminated for three days. Baked every hour until noon.", "$4"),
    photo_card("placeholder-square.svg", "A bowl of soup with bread", "Soup and sourdough", "Changes daily. Always with a thick slice.", "$10"),
    photo_card("placeholder-square.svg", "A fried egg on seeded toast", "Eggs on toast", "Two eggs your way on seeded sourdough.", "$11"),
    photo_card("placeholder-square.svg", "A slice of cake with coffee", "Cake and a coffee", "Whatever came out of the oven at noon.", "$8")], 4, "13rem", "large")])),
  sec("How pickup works", N([h("How pickup works", 2, "xx-large"), grid([
    nstep("1", "Send your order", "Use the form above, or call us if it's easier."),
    nstep("2", "We text you", "A confirmation with the total, then again when it's ready."),
    nstep("3", "Collect and pay", "Come to the counter, skip the queue and pay there.")], 3, "14rem", "medium")]), "section-tint"),
  sec("Find us", cols([
    col(N([h("Find us", 2, "xx-large"), stackg([stackg([mono(a), p(b, "medium", bind=k)], "x-small") for a, b, k in [("Pickup hours", "Tuesday to Sunday, 7am to 2:30pm", "hours"), ("Address", "14 Market Street, Springfield", "address"), ("Phone", "555 0198", "phone_linked")]], "medium"),
           p("Allergies? Tell us in the order or call before you order. Our kitchen handles nuts, gluten, dairy and eggs.", "small", "secondary")]), "40%"),
    col(mapb("14 Market Street, Springfield", 39.7817, -89.6501, 15, "4/3", "md"))], "xx-large", "wide", "center")),
  closing("Catering", "placeholder-wide.svg", "A long table laid with food for a group", "Feeding a group?", "Office lunches, parties and meetings, from ten people. Give us a day's notice.", [("Ask about catering", None, "mailto:hello@example.com", "email_link")])])

# ---------------------------------------------------------------- Menu (restaurants, cafés)
page("page-menu", "Menu page (restaurant)",
 "A menu page for a restaurant or café: a photo with the serving times and links to each part of the menu, breakfast and lunch each beside a full-height photo with dotted lines to the prices, cakes as photo cards, drinks on the dark section style, a key to dietary marks, and a photo band to order or book. Easy to read on a phone, and every dish is plain text the owner edits in place.",
 "menu, food, dishes, prices, restaurant, cafe, bakery, breakfast, lunch, cakes, drinks",
 [cover(on_photo(grp(N([mono("Seasonal menu", None), h("The menu", 1, "poster", "center", None, {"lineHeight": "0.95"}), p("Breakfast from 7am, lunch from 11:30. Everything made here, from scratch.", "large", None, "center"),
     btns([("Breakfast", "outline", "#breakfast"), ("Lunch", "outline", "#lunch"), ("Cakes", "outline", "#cakes"), ("Drinks", "outline", "#drinks")], "center")]), gap="medium", layout={"type": "constrained", "contentSize": "48rem"})),
     "Hero", "placeholder-wide.svg", 60, "70vh", "center center", ("xx-large", "xx-large", "medium", "medium"), "48rem", alt="A table of breakfast dishes and coffee"),
  split("Breakfast", "placeholder-tall.svg", "A breakfast plate of eggs on toast", [
    stackg([mono("7am to 11:30am"), h("Breakfast", 2, "xxx-large")], "small"), stackg([
      menu_line("Sourdough toast", "Cultured butter and this week's jam", "$6", "v"), menu_line("Eggs on rye", "Two eggs your way, greens, chilli oil", "$11", "v"),
      menu_line("Almond croissant", "Baked twice, filled with frangipane", "$5", "v"), menu_line("Granola", "Yoghurt, honey and fruit of the season", "$9", "v, gf"),
      menu_line("The full plate", "Eggs, bacon, mushrooms, beans and toast", "$16")], "medium")], False, None, 44),
  split("Lunch", "placeholder-tall.svg", "A bowl of soup with bread on a wooden table", [
    stackg([mono("11:30am to 3pm"), h("Lunch", 2, "xxx-large")], "small"), stackg([
      menu_line("Soup and bread", "Changes daily. Always a slab of sourdough", "$10", "vg"), menu_line("Ham and pickles", "Rye, mustard butter, our own pickles", "$13"),
      menu_line("Leek tart", "Gruyère, thyme and a sharp salad", "$14", "v"), menu_line("Roast chicken salad", "Grains, herbs, lemon and toasted seeds", "$15", "gf"),
      menu_line("Mushroom toast", "Garlic, thyme and a soft egg", "$12", "v")], "medium")], True, "section-tint", 44),
  sec("Cakes", N([stackg([mono("From the counter"), h("Cakes and bakes", 2, "xxx-large")], "small"), grid([
    photo_card("placeholder-square.svg", "Cinnamon buns on baking paper", "Cinnamon bun", "Cardamom sugar, soft middle.", "$4"),
    photo_card("placeholder-square.svg", "A slice of carrot cake", "Carrot cake", "Brown butter and cream cheese.", "$6"),
    photo_card("placeholder-square.svg", "A slice of cheesecake with cherries", "Baked cheesecake", "Sour cherries, chocolate sauce.", "$6"),
    photo_card("placeholder-square.svg", "Croissants fresh from the oven", "Croissant", "Plain, almond or chocolate.", "$4")], 4, "13rem", "large")])),
  sec("Drinks", cols([
    col(N([mono("All day", None), h("Drinks", 2, "xxx-large"), p("Coffee roasted ten miles away. Oat and almond milk at no extra cost.", "medium")]), "36%"),
    col(grid([stackg([menu_line(*d, sub=None) for d in a], "medium") for a in [
      [("Espresso", "Single or double", "$3"), ("Flat white", "Or a latte, a little bigger", "$4"), ("Filter coffee", "Refills are free", "$3.50")],
      [("Loose-leaf tea", "Ask for this week's teas", "$3.50"), ("Hot chocolate", "Made with real chocolate", "$4.50"), ("Fresh lemonade", "Still or sparkling", "$4")]]], 2, "14rem", "x-large"))], "xx-large", "wide", "top"), "section-dark"),
  sec("Dietary", row([p("<strong>v</strong> " + T("vegetarian") + " &nbsp;·&nbsp; <strong>vg</strong> " + T("vegan") + " &nbsp;·&nbsp; <strong>gf</strong> " + T("made without gluten"), None, None, None, None, None, True),
    p("Allergies? Ask us before you order: we'll tell you exactly what's in each dish.", None, "secondary")], "space-between", "medium"), None, ("large", "large", None, None)),
  closing("Order or book", "placeholder-wide.svg", "The café with tables by the window", "Hungry already?", "Order ahead and skip the queue, or book a table for the weekend.", [("Order online", None, "/order/"), ("Book a table", "outline", "/contact/")])])

# ---------------------------------------------------------------- Plan your visit (churches)
page("page-plan-your-visit", "Plan your visit page (church)",
 "A first-visit page for a church: a full-screen welcome photo, service times, address and children's groups on cards, what to expect on a Sunday, children and youth each beside a photo, a welcome from the pastor beside a portrait, the plan-your-visit form on the brand colour so someone meets them at the door, a map and questions. Needs the AnyPress Blocks plugin. On AnyPress the form box becomes a Fluent Forms form when the page is saved.",
 "church, plan your visit, new here, visit, sunday service, worship, first time, form",
 [cover(on_photo(grp(N([mono("New here?", None), h("We saved you a seat", 1, "poster", None, None, {"lineHeight": "0.95"}),
     p("Come as you are. There's coffee from 8:30 and someone at the door to show you around.", "large"),
     btns([("Plan your visit", None, "#visit"), ("Get directions", "outline", "#map")])]), gap="medium", layout={"type": "constrained", "contentSize": "52rem", "justifyContent": "left"})),
     "Hero", "placeholder-wide.svg", 50, "92vh", "bottom left", ("xx-large", "x-large", "medium", "medium"), "80rem", alt="People gathered for a Sunday service"),
  sec("Times", grid([
    grp(N([mono("Sundays"), h("Service times", 2, "large"), p("9am and 11am", "large", None, None, None, {"fontWeight": "700"}, bind="hours"), p("Kids' groups at both services.", "small", "secondary")]), "section-card", PAD_CARD, "small", {"type": "default"}, radius="md"),
    grp(N([mono("Find us"), h("Address", 2, "large"), p("12 Chapel Lane, Springfield", "large", None, None, None, {"fontWeight": "700"}, bind="address"), btns([("Get directions", "outline", "#map")])]), "section-card", PAD_CARD, "small", {"type": "default"}, radius="md"),
    grp(N([mono("Parking"), h("Free and easy", 2, "large"), p("Lot behind the hall", "large", None, None, None, {"fontWeight": "700"}), p("Spaces for visitors right by the door.", "small", "secondary")]), "section-card", PAD_CARD, "small", {"type": "default"}, radius="md")], 3, "15rem", "medium"),
    "section-tint", ("x-large", "x-large", None, None)),
  sec("What to expect", N([stackg([mono("Before you come"), h("What a Sunday looks like", 2, "xx-large")], "small"), grid([
    big_card("1 hr", "About an hour", "Songs, a short talk from the Bible and a prayer. Nobody will ask you to stand up or speak.", "section-brand-soft"),
    big_card("Jeans", "Come as you are", "Jeans or a suit: you'll see both, and nobody minds.", "section-brand-soft"),
    big_card("2–11", "Kids' groups", "During the service, with checked and trained leaders.", "section-brand-soft"),
    big_card("Coffee", "Stay after", "Coffee in the hall and a chance to meet people. No pressure.", "section-brand-soft")], 4, "13rem", "medium")])),
  split("Children", "placeholder-tall.svg", "Children drawing together at a table", [
    mono("Ages 2 to 11"), h("Your kids will love it here", 2, "xx-large"),
    p("Safe, fun groups during both services, with songs, stories and crafts. Check in at the kids' desk ten minutes early the first time and we'll show you round.", "medium"),
    ticks(["Every leader checked and trained", "A secure check-in and pick-up", "A quiet room for parents with babies"])], False, None, 34),
  split("Youth", "placeholder-tall.svg", "Teenagers talking together outside", [
    mono("Ages 11 to 18"), h("A place for teenagers, too", 2, "xx-large"),
    p("Youth meet on Friday evenings for food, games and honest conversation, and join the 11am service on Sundays.", "medium"),
    btns([("Ask about youth", "outline", "mailto:hello@example.com", "email_link")])], True, "section-tint", 34),
  sec("Pastor", cols([
    col(img("placeholder-tall.svg", "Portrait of the pastor", "4/5", "md"), "34%"),
    col(N([mono("A welcome from our pastor"), quote("Whether you've been to church all your life or never at all, you're welcome here. Bring your questions; we'd love to hear them.", "Pastor James Reed", "x-large")]), None, None, None, "center")], "xx-large", "wide", "center"), content="64rem"),
  sec("Visit form", cols([
    col(N([mono("Plan your visit", None), h("Tell us you're coming", 2, "xxx-large"), p("We'll meet you at the door, help you check in the kids and save you a seat. There's a small welcome gift too.", "large"),
           ticks(["Someone to meet you, so you're not on your own", "Kids checked in before the service", "No mailing lists unless you ask"], "medium")]), "48%", valign="center"),
    col(form_card("Plan your visit", "A few quick questions. We'll text the day before.", "visit", "plan-your-visit form"), None, valign="center")], "xx-large", "wide", "center"), "section-brand"),
  sec("Map", cols([
    col(mapb("12 Chapel Lane, Springfield", 39.7990, -89.6440, 15, "4/3", "md"), "55%"),
    col(N([h("Getting here", 2, "xx-large"), p("Five minutes from the station. Buses 4 and 12 stop outside.", "medium"), p("Step-free entry, a hearing loop and accessible toilets.", None, "secondary"),
           btns([("Call the office", "outline", "tel:5550164", "phone_link")])]), None, None, None, "center")], "xx-large", "wide", "center")),
  faq_split([("Do I have to be a member?", "No. Everyone is welcome, every week."),
             ("Will I be asked to give money?", "No. Giving is for people who call this church home. Guests are guests."),
             ("Is there something during the week?", "Small groups, youth on Fridays and a lunch club for older neighbours on Wednesdays."),
             ("Can I watch online first?", "Yes. The 11am service is streamed live and saved on our channel.")],
   ask_card("Still unsure?", "Call the office and talk to a real person. We'd love to hear from you.", [("Call 555 0164", None, "tel:5550164", "phone")], "section-brand-soft"), "section-tint")])

# ---------------------------------------------------------------- Booking pages (bookings site type)
page("page-book-consultation", "Book a consultation page",
 "A consultation page for a lawyer, accountant, coach or consultant: the promise and what the first meeting covers beside the booking calendar on a card, three things the meeting covers, the consultant beside a portrait with credentials, reviews in a carousel, a short request form for people who'd rather write first, and questions. Needs the AnyPress Blocks plugin. On AnyPress the calendar box becomes FluentBooking's calendar and the form box a Fluent Forms form when the page is saved.",
 "consultation, book a consultation, free consultation, lawyer, attorney, accountant, coach, consultant, appointment, book",
 [sec("Booking", cols([
    col(N([mono("Free 30-minute consultation"), h("Talk it through with someone who knows.", 1, "xxx-large", None, None, {"lineHeight": "1.05"}),
           p("Pick a time that suits you, online or in the office. You'll leave knowing your options and what they'd cost.", "large", "secondary"),
           ticks(["Straight answers, in plain words", "A written summary afterwards", "No obligation to go further"], "medium"), rating("4.9 from 160 clients")]), "44%"),
    col(cal_card("Pick a time", "Choose the kind of meeting, then a time. You'll get a confirmation straight away."))], "xx-large", "wide", "top"), pad=("xx-large", "xx-large", None, None)),
  sec("What we cover", N([stackg([mono("In 30 minutes"), h("What we'll cover", 2, "xx-large")], "small"), grid([
    gstep("01", "placeholder-wide.svg", "Two people talking across a desk", "Where you are", "You tell us what's happening. We listen and ask the questions that matter."),
    gstep("02", "placeholder-wide.svg", "Papers and a notebook on a desk", "Your options", "Every way forward we can see, with the risks and the likely cost of each."),
    gstep("03", "placeholder-wide.svg", "A handshake at the end of a meeting", "The next step", "What we'd do first, if you'd like us to help. Or who to see if it isn't us.")], 3, "15rem", "x-large")]), "section-tint"),
  split("About", "placeholder-tall.svg", "Portrait of the consultant in the office", [
    mono("Who you'll meet"), h("Helen Park", 2, "xxx-large"),
    p("Twenty years advising small businesses and families. Helen takes every first meeting herself, so you start with the person who'll do the work.", "medium"),
    ticks(["Licensed and insured", "In practice since 2005", "Spanish and English"])], True, None, 36),
  reviews("What clients say", [
    ("Thirty minutes and I finally understood where I stood. The written summary was worth it alone.", "Rosa M. · Family matter"),
    ("No jargon, no pressure, and a clear price for the next step.", "Tom B. · Business contract"),
    ("She told me I didn't need her yet, and what to do instead. That's why I went back.", "Ana L. · Estate planning"),
    ("Booked online at 10pm, met the next morning.", "Kwame A. · Lease dispute")], "section-brand-soft", "4.9 from 160 clients"),
  sec("Consultation form", cols([
    col(N([h("Rather write first?", 2, "xx-large"), p("Send a few lines and we'll reply within one working day with a time, or an answer if it's quick.", "medium", "secondary"),
           p("Keep details for the meeting itself: the form only needs the outline.", "small", "secondary")]), "40%"),
    col(form_card("Request a consultation", "One question at a time. About two minutes.", "consultation", "consultation request form", "Consultation form"))], "xx-large", "wide", "top")),
  faq_split([("Is the consultation really free?", "Yes, the first 30 minutes. If you'd like us to go further, we'll give you a fixed price first."),
             ("Is what I tell you confidential?", "Yes, from the first conversation."),
             ("Can we meet online?", "Yes. Pick online when you book and you'll get a video link."),
             ("What should I bring?", "Any letters, contracts or papers, and a list of the dates and names that matter.")],
   ask_card("Is it urgent?", "If a deadline is days away, call us now.", [("Call 555 0119", None, "tel:5550119", "phone")]), "section-tint")])

page("page-book-dental", "Book an appointment page (dental)",
 "An appointment page for a dental practice: a calm photo with the promise and three quick facts, the booking calendar beside what new patients should know, treatments with times and prices, your first visit in three steps with photos, insurance plans accepted, reviews in a carousel, hours and a map with an emergency card, and questions. Needs the AnyPress Blocks plugin. On AnyPress the calendar box becomes FluentBooking's calendar when the page is saved.",
 "dentist, dental, appointment, checkup, cleaning, emergency, new patients, insurance, book",
 [cover(on_photo(grp(N([mono("New patients welcome", None), h("Book your dental visit online", 1, "poster", None, None, {"lineHeight": "0.95"}),
     p("Checkups, cleaning and treatment, booked in a minute. Same-day emergency appointments every weekday.", "large"), btns([("Book now", None, "#book"), ("Dental emergency?", "outline", "tel:5550133", "phone_link")]),
     rating("4.9 from 640 patients")]), gap="medium", layout={"type": "constrained", "contentSize": "52rem", "justifyContent": "left"})),
     "Hero", "placeholder-wide.svg", 50, "80vh", "bottom left", ("xx-large", "x-large", "medium", "medium"), "80rem", alt="A bright, calm dental treatment room"),
  sec("Booking", cols([
    col(grp(N([h("New to the practice?", 2, "x-large"), ticks(["Arrive ten minutes early", "Bring your insurance card and a list of medicines", "Tell us if you're nervous: we'll take it slowly"]),
               sep(), h("In pain right now?", 3, "medium"), p("Call before 10am for a same-day appointment.", None, "secondary"), btns([("Call 555 0133", None, "tel:5550133", "phone")])]), "sticky", None, "medium", {"type": "default"}), "34%"),
    col(cal_card("Pick a time", "Choose your treatment, then a time. We'll send a reminder the day before."))], "xx-large", "wide", "top"), "section-tint", content="72rem"),
  sec("Treatments", cols([
    col(N([mono("Treatments and prices"), h("Clear prices, before we start", 2, "xx-large"), p("With insurance, most checkups cost you nothing. We check your cover before any treatment.", "medium", "secondary")]), "38%"),
    col(stackg([menu_line(*t) for t in [("New patient exam", "Full checkup, X-rays and a treatment plan · 60 minutes", "$95"), ("Checkup and cleaning", "Every six months · 45 minutes", "$85"),
       ("Emergency appointment", "Pain, swelling or a broken tooth · 30 minutes", "$65"), ("Whitening", "Take-home trays and a follow-up visit", "$295"),
       ("Children's checkup", "With a parent's appointment", "Free")]], "medium"))], "xx-large", "wide", "top")),
  sec("First visit", N([stackg([mono("Your first visit"), h("What happens at your first appointment", 2, "xx-large")], "small"), grid([
    gstep("01", "placeholder-wide.svg", "The welcoming reception desk", "A warm welcome", "A short form, a chat about your teeth and anything that worries you."),
    gstep("02", "placeholder-wide.svg", "A dentist talking with a patient in the chair", "A full checkup", "X-rays, a gentle exam and a cleaning if there's time."),
    gstep("03", "placeholder-wide.svg", "A patient smiling after treatment", "Your plan, in writing", "What we found, what can wait and what each step costs.")], 3, "15rem", "x-large")]), "section-brand-soft"),
  sec("Insurance", cols([
    col(N([h("Insurance we accept", 2, "xx-large"), p("Not on the list? Call us: we work with most plans, and offer payment plans for everything else.", None, "secondary")]), "38%"),
    col(grid([grp(p(n, "medium", None, "center", None, {"fontWeight": "600"}), "section-card", ("medium", "medium", "small", "small"), radius="md") for n in ["Delta Dental", "Cigna", "Aetna", "MetLife", "Guardian", "United Concordia", "Humana", "Payment plans"]], 4, "9rem", "small"))], "xx-large", "wide", "center")),
  reviews("What patients say", [
    ("I've avoided dentists for years. They were patient, explained everything and it didn't hurt.", "Sarah K. · New patient"),
    ("Cracked a tooth on Monday morning, fixed by lunchtime.", "Amir H. · Emergency"),
    ("Booking online took less than a minute. Reminder the day before was handy.", "Grace L. · Cleaning"),
    ("They're brilliant with my kids. Both of them actually look forward to it.", "Holly P. · Family checkups")], "section-tint", "4.9 from 640 patients on Google"),
  sec("Visit", cols([
    col(N([h("Hours and location", 2, "xx-large"), stackg([stackg([mono(a), p(b, "medium", bind=k)], "x-small") for a, b, k in [("Hours", "Monday to Friday, 8am to 7pm. Saturday, 9am to 2pm.", "hours"), ("Address", "220 Elm Street, Springfield", "address")]], "medium"),
           ask_card("Dental emergency?", "Call before 10am for a same-day appointment, every weekday.", [("Call 555 0133", None, "tel:5550133", "phone")], "section-dark")]), "42%"),
    col(mapb("220 Elm Street, Springfield", 39.8010, -89.6480, 15, "4/3", "md"), None, None, None, "center")], "xx-large", "wide", "center")),
  faq_split([("Do you take my insurance?", "We work with most plans. Bring your card and we'll check before any treatment."),
             ("Can I change my appointment?", "Yes, through the link in your confirmation email, up to 24 hours before."),
             ("Do you see children?", "Yes, from their first tooth. Children's checkups are free with a parent's appointment."),
             ("I'm nervous. What can you do?", "Tell us when you book. We'll go slowly, explain each step, and stop whenever you raise a hand.")],
   ask_card("Questions first?", "Our front desk is happy to help.", [("Call 555 0133", None, "tel:5550133", "phone")], "section-brand-soft"))])

page("page-book-salon", "Book an appointment page (salon)",
 "An appointment page for a hair salon, barber or beauty studio: a full-screen photo with the booking button, the price list with dotted lines beside the booking calendar, the stylists with portraits, photos of recent work, three short booking rules on cards, reviews in a carousel and questions. Needs the AnyPress Blocks plugin. On AnyPress the calendar box becomes FluentBooking's calendar when the page is saved.",
 "salon, hair, barber, beauty, appointment, haircut, colour, balayage, stylist, book online",
 [cover(on_photo(grp(N([mono("Book online", None), h("Your chair is waiting", 1, "poster", None, None, {"lineHeight": "0.95"}),
     p("Pick your service and your stylist, and choose a time. It takes less than a minute.", "large"), btns([("Book now", None, "#book"), ("See prices", "outline", "#book")]), rating("4.9 from 410 clients")]),
     gap="medium", layout={"type": "constrained", "contentSize": "48rem", "justifyContent": "left"})),
     "Hero", "placeholder-tall.svg", 50, "92vh", "bottom left", ("xx-large", "x-large", "medium", "medium"), "80rem", alt="A stylist finishing a client's hair in the salon"),
  sec("Booking", cols([
    col(N([h("Prices", 2, "xxx-large"), p("Prices depend on hair length and your stylist's level. We confirm before we start.", None, "secondary"), stackg([
      price_group("Cut and style", [("Cut and finish", "from $45"), ("Men's cut", "from $30"), ("Blow-dry", "from $30", "Add curls or waves for $10.")]),
      price_group("Colour", [("Root colour", "from $75"), ("Balayage", "from $160", "Includes toner and a cut."), ("Gloss", "$45", "Shine and tone between colours.")])], "x-large")]), "44%"),
    col(cal_card("Book your appointment", "Choose a service and a stylist, then a time. You'll get a confirmation by email."))], "xx-large", "wide", "top"), "section-brand-soft"),
  sec("Stylists", N([stackg([mono("Who you'll sit with"), h("Our stylists", 2, "xxx-large")], "small"), grid([
    portrait("placeholder-tall.svg", "Portrait of Nadia", "Nadia", "Owner and colour director. Balayage and grey blending."),
    portrait("placeholder-tall.svg", "Portrait of Ollie", "Ollie", "Senior stylist. Short cuts and curly hair."),
    portrait("placeholder-tall.svg", "Portrait of Bea", "Bea", "Brows and lashes. Fixes over-plucked brows."),
    portrait("placeholder-tall.svg", "Portrait of Jess", "Jess", "Stylist. Blow-dries, braids and bridal hair.")], 4, "9rem", "medium")])),
  sec("Recent work", N([row([h("Recent work", 2, "xx-large"), p('<a href="https://www.instagram.com/">' + T("More on Instagram") + "</a>", "medium", raw=True)], valign="bottom"), grid([
    zoom(img("placeholder-tall.svg", "Recent work: soft copper curls", "3/4", "md")), zoom(img("placeholder-tall.svg", "Recent work: a glossy brunette blow-dry", "3/4", "md")),
    zoom(img("placeholder-tall.svg", "Recent work: blonde balayage", "3/4", "md")), zoom(img("placeholder-tall.svg", "Recent work: neat braids", "3/4", "md"))], 4, "8rem", "small")]), "section-tint"),
  sec("Good to know", grid([
    big_card("24 hrs", "Free changes", "Move or cancel free up to 24 hours before your appointment."),
    big_card("48 hrs", "Patch test first", "New to colour with us? Book a free patch test two days before."),
    big_card("$20", "Colour deposit", "Taken when you book colour, and taken off your bill.")], 3, "14rem", "medium"), None, ("x-large", "x-large", None, None)),
  reviews("What clients say", [
    ("Nadia listened to what I actually wanted. Best colour I've had in ten years.", "Lena M. · Balayage"),
    ("Booked at midnight, in the chair the next afternoon.", "Chris D. · Men's cut"),
    ("Ollie is the only person I trust with my curls.", "Ama O. · Curly cut"),
    ("Calm, kind and the coffee is good.", "Rachel T. · Blow-dry")], "section-dark", "4.9 from 410 reviews"),
  faq_split([("Can I choose my stylist?", "Yes. Pick them when you book, or choose anyone for the first free time."),
             ("How much is a deposit?", "Colour and balayage take a $20 deposit when you book, taken off the bill."),
             ("I'm running late. What happens?", "Call us. Up to 10 minutes we'll fit you in; after that we may need to shorten or move it."),
             ("Do you sell gift vouchers?", "Yes, for any amount or service, at the front desk or online.")],
   ask_card("Not sure what to book?", "Book a free 15-minute consultation and we'll plan it with you.", [("Call 555 0155", None, "tel:5550155", "phone")]))])

page("page-book-classes", "Classes and booking page",
 "A classes page for a yoga or pilates studio, gym or dance school: a photo with the first-class-free offer, the class types as photo cards with length and level, the week's timetable, the booking calendar beside what to bring, passes and prices on cards, the teachers with portraits, and questions. Needs the AnyPress Blocks plugin. On AnyPress the calendar box becomes FluentBooking's calendar, with every class, when the page is saved.",
 "classes, class timetable, schedule, yoga, pilates, gym, dance, studio, book a class, group class, passes",
 [cover(on_photo(grp(N([mono("Your first class is free", None), h("Find your class", 1, "poster", None, None, {"lineHeight": "0.95"}),
     p("Small classes, seven days a week, for every level. Book in a minute, cancel free up to 12 hours before.", "large"),
     btns([("Book a free class", None, "#book"), ("See the timetable", "outline", "#timetable")])]), gap="medium", layout={"type": "constrained", "contentSize": "52rem", "justifyContent": "left"})),
     "Hero", "placeholder-wide.svg", 50, "88vh", "bottom left", ("xx-large", "x-large", "medium", "medium"), "80rem", alt="A group class in a bright studio"),
  sec("Classes", N([stackg([mono("Classes"), h("Something for every day", 2, "xxx-large")], "small"), grid([
    photo_card("placeholder-square.svg", "A gentle morning class on mats", "Morning flow", "60 minutes · All levels. A gentle start to the day."),
    photo_card("placeholder-square.svg", "A strong class mid-workout", "Power", "60 minutes · Some experience. Strong and sweaty."),
    photo_card("placeholder-square.svg", "A slow stretching class", "Slow and stretch", "75 minutes · All levels. Long holds and deep rest."),
    photo_card("placeholder-square.svg", "A teacher helping one student", "Private session", "60 minutes · One to one, at a time that suits you.")], 4, "13rem", "large")])),
  sec("Timetable", N([row([h("This week", 2, "xxx-large"), p("All classes 60 minutes unless shown.", None, "secondary")], valign="bottom"), table(["Day", "Morning", "Lunchtime", "Evening"], [
     ["Monday", "Morning flow, 7am", "Power, 12:15pm", "Power, 6pm"], ["Tuesday", "Slow and stretch, 9am (75 min)", "", "Morning flow, 7pm"], ["Wednesday", "Morning flow, 7am", "Power, 12:15pm", "Power, 6pm"],
     ["Thursday", "Power, 7am", "", "Slow and stretch, 7pm (75 min)"], ["Friday", "Morning flow, 7am", "Power, 12:15pm", ""], ["Saturday", "Morning flow, 9am", "", "Slow and stretch, 5pm (75 min)"], ["Sunday", "Power, 10am", "", ""]], "stripes")]), "section-tint"),
  sec("Booking", cols([
    col(grp(N([h("Your first class", 2, "x-large"), ticks(["Come ten minutes early", "Mats, blocks and towels are here", "Tell your teacher about any injuries"]),
               sep(), h("Can't make it?", 3, "medium"), p("Cancel up to 12 hours before and the class goes back on your pass.", None, "secondary")]), "sticky", None, "medium", {"type": "default"}), "34%"),
    col(cal_card("Book a class", "Choose a class, then a time. Your place is held the moment you book."))], "xx-large", "wide", "top"), content="72rem"),
  sec("Passes", N([stackg([mono("Passes and prices"), h("Pay as you go, or save", 2, "xxx-large")], "small"), grid([
    big_card("Free", "First class", "Any class, once. No card needed.", "section-brand-soft"),
    big_card("$20", "Drop in", "One class, whenever you like."),
    big_card("$150", "Ten classes", "Save $50. Use them within six months."),
    big_card("$89", "Unlimited, monthly", "Every class, every week. Cancel any time.", "section-dark")], 4, "12rem", "medium")])),
  sec("Teachers", N([stackg([mono("Your teachers"), h("Who's teaching", 2, "xx-large")], "small"), grid([
    portrait("placeholder-tall.svg", "Portrait of a teacher", "Priya", "Morning flow. Teaching since 2012."),
    portrait("placeholder-tall.svg", "Portrait of a teacher", "Marcus", "Power. Former athlete, kind but firm."),
    portrait("placeholder-tall.svg", "Portrait of a teacher", "Dee", "Slow and stretch. Loves beginners."),
    portrait("placeholder-tall.svg", "Portrait of a teacher", "Tom", "Private sessions and injuries.")], 4, "9rem", "medium")]), "section-tint"),
  faq_split([("Do I need experience?", "No. Morning flow and Slow and stretch are made for beginners."),
             ("What if a class is full?", "Join the waiting list when you book. If a place opens, it's yours and we'll email you."),
             ("Can I pause my membership?", "Yes, for up to two months a year, for travel or injury."),
             ("Is there parking?", "Free parking behind the studio, and bike racks by the door.")],
   ask_card("Not sure where to start?", "Tell us what you're after and we'll suggest a class.", [("Email us", None, "mailto:hello@example.com", "email_link")]))])

# ---------------------------------------------------------------- Policies
def policy_hero(eyebrow, title, lead, file, alt):
    return cover(on_photo(grp(N([mono(eyebrow, None), h(title, 1, "xxx-large", None, None, {"lineHeight": "1.05"}), p(lead, "large"), p("Last updated: 1 January 2027", "small")]), gap="medium", layout={"type": "constrained", "contentSize": "44rem", "justifyContent": "left"})),
                 "Hero", "placeholder-wide.svg", 60, "55vh", "bottom left", ("xx-large", "x-large", "medium", "medium"), "72rem", alt=alt)

def policy_body(nav, clauses):
    return sec("Policy", cols([col(toc(nav), "28%"), col(stackg(clauses, "xx-large"))], "xx-large", "wide", "top"), content="72rem")

page("page-cancellation-policy", "Cancellation policy page",
 "A cancellation and no-show policy for a business that takes bookings, in plain words: a photo heading, the four rules at a glance on cards, then cancelling, moving, no-shows, deposits and emergencies with links to each part beside them, and a card to cancel or move a booking. Set the numbers to the business's own before publishing, and show the policy where people book.",
 "cancellation policy, no-show, late cancellation, rescheduling, deposit, refund, bookings, policy",
 [policy_hero("Our policy", "Cancellations and no-shows", "When someone cancels late, that time can't go to anyone else. This is what we ask, so it's fair for everyone.", "placeholder-wide.svg", "The quiet reception of the studio"),
  sec("At a glance", grid([
    big_card("24 hrs", "Free changes", "Cancel or move for free up to 24 hours before."),
    big_card("$25", "Late cancellation", "Less than 24 hours' notice."),
    big_card("100%", "No-show", "The full price, if you don't come or tell us."),
    big_card("Fair", "Emergencies", "Tell us as soon as you can and we'll waive the fee.", "section-brand-soft")], 4, "12rem", "medium"), "section-tint", ("x-large", "x-large", None, None)),
  policy_body([("Cancelling", "#cancelling"), ("Moving an appointment", "#moving"), ("No-shows", "#no-shows"), ("Deposits and refunds", "#deposits"), ("Emergencies", "#emergencies")], [
    clause("Cancelling", ["You can cancel for free up to 24 hours before your appointment, through the link in your confirmation email or by calling us.", "If you cancel less than 24 hours before, we charge a $25 late cancellation fee."], None, "cancelling"),
    clause("Moving an appointment", ["Moving is free up to 24 hours before. A move with less notice counts as a late cancellation."], None, "moving"),
    clause("No-shows", ["If you don't come and don't tell us, we charge the full price of the appointment.", "After two no-shows, we ask for a deposit to book again."], None, "no-shows"),
    clause("Deposits and refunds", ["Some appointments take a deposit when you book. It comes off the final bill."], ["Cancel 24 hours or more before: your deposit is refunded in full", "Move your appointment: your deposit moves with it", "Cancel late or don't come: the deposit isn't refunded"], "deposits"),
    clause("Emergencies", ["Illness, accidents and family emergencies happen. Tell us as soon as you can and we'll waive the fee."], None, "emergencies")]),
  sec("Contact", cols([col(N([h("Need to cancel or move?", 2, "xx-large"), p("Use the link in your confirmation email, or call us. It takes a minute.", "medium")])),
    col(btns([("Call 555 0142", None, "tel:5550142", "phone"), ("Email us", "outline", "mailto:hello@example.com", "email_link")], "right"), "40%", valign="center")], "x-large", "wide", "center"), "section-brand", ("x-large", "x-large", None, None))])

page("page-return-policy", "Return and refund policy page (online store)",
 "A return and refund policy for an online store, written as answers to the questions shoppers ask: a photo heading, the four promises at a glance on cards, how to return in three steps with photos, then how long, condition, what can't come back, return shipping, refunds, exchanges and digital products with links to each part beside them, a holiday note, and a card to start a return. Set the numbers to the shop's own, check the law where the shop sells, and link the policy from the footer and checkout.",
 "return policy, refund policy, returns, refunds, exchanges, online store, shipping, policy",
 [policy_hero("Shopping with us", "Returns made easy", "Changed your mind? Send it back within 30 days for a full refund. Here's how it works.", "placeholder-wide.svg", "Folded clothes ready to pack"),
  sec("At a glance", grid([
    big_card("30 days", "To send it back", "From the day your order arrives."),
    big_card("Free", "If it's faulty or wrong", "We send a prepaid label."),
    big_card("5 days", "To refund you", "Once your return reaches us."),
    big_card("Swap", "Exchanges", "A new size or colour, sent as soon as yours is on its way.", "section-brand-soft")], 4, "12rem", "medium"), "section-tint", ("x-large", "x-large", None, None)),
  sec("How to return", N([stackg([mono("How to return"), h("Three steps", 2, "xx-large")], "small"), grid([
    gstep("01", "placeholder-wide.svg", "Someone choosing an order on a laptop", "Start your return", "Sign in and choose the order, or email us with your order number."),
    gstep("02", "placeholder-wide.svg", "Clothes folded into a parcel", "Pack it up", "In the original packaging if you still have it (any sturdy box will do), with the tags on."),
    gstep("03", "placeholder-wide.svg", "A parcel being handed over", "Send it back", "Drop it at any post office. We email you when it arrives.")], 3, "15rem", "x-large")])),
  policy_body([("How long do I have?", "#returns"), ("Condition", "#condition"), ("What can't be returned", "#exceptions"), ("Return shipping", "#shipping"), ("Refunds", "#refunds"), ("Exchanges", "#exchanges"), ("Digital products", "#digital")], [
    clause("How long do I have?", ["30 days from the day your order arrives."], None, "returns"),
    clause("What condition must items be in?", ["Unused and unwashed, with the tags on, so we can sell them again. The original packaging helps but isn't needed."], None, "condition"),
    clause("What can't be returned?", ["For hygiene and safety, some things can't come back unless they're faulty:"], ["Underwear, swimwear and earrings", "Personalised or made-to-order items", "Gift cards", "Food and flowers"], "exceptions"),
    clause("Who pays for return shipping?", ["If an item is faulty or we sent the wrong thing, we pay and send a free label. Otherwise return shipping is up to you."], None, "shipping"),
    clause("When will I get my money?", ["We refund to your original payment method within 5 working days of your return reaching us. Your bank may take another 5 to 10 days to show it."], None, "refunds"),
    clause("Can I exchange instead?", ["Yes. Choose an exchange when you start your return and we'll send the new size or colour as soon as yours is on its way back."], None, "exchanges"),
    clause("Digital products", ["Downloads can be refunded within 14 days if they don't work as described or never arrived, and you haven't downloaded them more than once."], None, "digital")]),
  sec("Holidays", cols([col(N([mono("Holiday returns"), h("Bought a gift? Take your time.", 2, "xx-large"),
      p("Anything delivered between November 15 and December 15 can come back until January 15. Later deliveries keep the full 30 days.", "medium")])),
    col(img("placeholder-wide.svg", "A wrapped gift on a table", "4/3", "md"), "40%")], "xx-large", "wide", "center"), "section-brand-soft"),
  sec("Contact", cols([col(N([h("Start a return", 2, "xx-large"), p("Sign in and choose the order, or email us with your order number. We reply within one working day.", "medium")])),
    col(btns([("Email us", None, "mailto:hello@example.com", "email_link")], "right"), "35%", valign="center")], "x-large", "wide", "center"), "section-dark", ("x-large", "x-large", None, None))])
h, btns, details = _h, _btns, _details
print("guide pages ok")
