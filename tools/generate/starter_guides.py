# Starter pages from the Fluent plugins' own guides (Fluent Forms, FluentBooking, FluentCart, Ninja Tables,
# WPManageNinja): quote, project and onboarding forms, a home valuation, a restaurant's order and menu pages, a church's
# plan-your-visit page, booking pages for a law office, a dental practice, a salon and a yoga studio, and cancellation
# and return policies. Run by kits_more.py, so every helper above is in scope.
#
# A form or booking calendar goes in a spot: a card group with the class "anypress-slot", named "Form: <key>" or
# "Booking calendar". On any site the owner puts their form block in it. On an AnyPress store the store template
# swaps it for Fluent Forms' or FluentBooking's own block when the page is saved (anypress-starter-forms.php), so keep
# the names and keys stable: quote, project, onboarding, valuation, order, visit, consultation.

ANCHORS.update({"Quote form": "quote", "Project form": "project", "Onboarding form": "start", "Valuation": "valuation",
                "Order form": "order", "Plan your visit": "visit", "Consultation form": "consult", "Book": "book",
                "Cancellations": "cancellations", "Starters": "starters", "Mains": "mains", "Desserts": "desserts", "Drinks": "drinks", "No-shows": "no-shows", "Returns": "returns", "Refunds": "refunds"})

def gstep(n, title, text):
    return stackg([p(n, "xx-large", "primary"), h(title, 3, "medium"), p(text, None, "secondary")], "small")

def dish(name, text, price):
    return stackg([row([h(name, 3, "base"), p(price)], "space-between", "small", False), p(text, "small", "secondary")], "x-small")

def slot(name, note):
    """Where a form or booking calendar goes: a card the store template fills, with a line saying what goes there."""
    card_ = grp(p(note, None, "secondary"), "section-card", PAD_CARD, "small", {"type": "default"}, name=name, radius="md")
    return card_.replace('"className":"is-style-section-card"', '"className":"is-style-section-card anypress-slot"', 1).replace(
        'class="wp-block-group is-style-section-card"', 'class="wp-block-group is-style-section-card anypress-slot"', 1)

def form_slot(key, what):
    return slot(f"Form: {key}", f"The {what} goes here. Put your form block in this box.")

booking_slot = slot("Booking calendar", "The booking calendar goes here: every service, with its free times. Put your booking block in this box.")

def intro(eyebrow, title, text, buttons=None):
    parts = [mono(eyebrow), h(title, 1, "xxx-large"), p(text, "large", "secondary")]
    if buttons: parts.append(btns(buttons))
    return sec("Introduction", N(parts), pad=("xx-large", "large", None, None), content="52rem")

def next_steps(title, items, style="section-tint"):
    return sec("What happens next", N([h(title, 2, "x-large"), grid([gstep(str(i), a, b) for i, (a, b) in enumerate(items, 1)], 3, "14rem", "large")]), style)

def form_section(name, title, text, key, what, aside):
    """The form beside what to know before sending it."""
    return sec(name, cols([
        col(N([h(title, 2, "x-large"), p(text, None, "secondary"), form_slot(key, what)]), "60%"),
        col(card(N(aside), "section-brand-soft"))], "x-large", "wide", "top"))

def questions(items, style=None):
    return sec("Questions", N([h("Questions people ask", 2, "x-large"), stackg([details(q, a) for q, a in items], "small")]), style, content="52rem")

def clause(title, paragraphs, items=None):
    parts = [h(title, 2, "large")] + [p(t) for t in paragraphs] + ([lst(items)] if items else [])
    return N(parts)

def policy(slug, title, desc, kw, eyebrow, heading_, lead, toc, body, closing):
    page(slug, title, desc, kw, [
        sec("Introduction", N([mono(eyebrow), h(heading_, 1, "xxx-large"), p(lead, "large", "secondary"), p("Last updated: 1 January 2027", "small", "secondary")]), pad=("xx-large", "large", None, None), content="48rem"),
        sec("At a glance", card(N([h("At a glance", 2, "medium"), lst(toc)]), "section-tint"), pad=("medium", "large", None, None), content="48rem")]
        + body + [closing])

# ---------------------------------------------------------------- Lead forms (website)
page("page-quote", "Request a quote page",
 "A Request a quote page for trades and services: what a quote includes and costs, the quote form (what's needed, the job, where, when, budget, how to reply) beside what to send with it, how quoting works in three steps, and questions. On AnyPress the form box becomes a Fluent Forms form when the page is saved.",
 "quote, request a quote, estimate, free quote, price, form, trades, services",
 [intro("Free, written quotes", "Tell us about the job. We'll send a fixed price.",
        "Every quote is free, in writing and valid for 30 days. Most come back within two working days.", [("Start your quote", None, "#quote")]),
  form_section("Quote form", "Request a quote", "The more you tell us, the more exact the price. Questions with a star are the only ones you must answer.", "quote", "quote form",
   [h("Good to send", 3, "medium"), lst(["What the job is, and roughly how big", "The address or town", "Any date it must be done by", "Your budget, if you have one in mind"]),
    h("Rather talk?", 3, "medium"), p("Call us and we'll take the details over the phone.", None, "secondary"), btns([("Call 555 0142", "outline", "tel:5550142", "phone")])]),
  next_steps("How quoting works", [("We read it", "A real person reads every request the same day and calls if anything is unclear."),
       ("We visit if needed", "Bigger jobs get a free visit to measure up. Smaller ones we price from your details."),
       ("You get a fixed price", "In writing, with what's included and when we can start. No pressure to say yes.")]),
  questions([("Is the quote really free?", "Yes, and so is the visit. You only pay if you go ahead."),
             ("How long is a quote valid?", "30 days. After that we check prices again before we start."),
             ("Can you work to my budget?", "Tell us the budget and we'll say honestly what it covers, and what we'd leave out.")])])

page("page-project-inquiry", "Project inquiry page",
 "A project inquiry page for agencies, studios and consultants: who the business works with, the project brief form (company, website, what's needed, goals, budget range, deadline, who decides, how they heard) beside what makes a good brief, what happens after sending it, and questions. On AnyPress the form box becomes a Fluent Forms form when the page is saved.",
 "project inquiry, project brief, start a project, agency, studio, consultant, form, work with us",
 [intro("Start a project", "Tell us what you're building", "A short brief helps us see if we're the right fit, and lets us come to the first call with ideas, not just questions.", [("Send a brief", None, "#project")]),
  sec("Who we work with", N([h("Projects we take on", 2, "x-large"), grid([tfeat(a, b) for a, b in [
      ("New projects", "From the first idea to launch, with a fixed scope and price."), ("Improvements", "Make something you already have work better, faster or look sharper."),
      ("Ongoing help", "A set number of hours each month, booked ahead.")]], 3, "14rem", "x-large")])),
  form_section("Project form", "Your project brief", "Budgets and deadlines are ranges, not promises: they help us suggest the right size of project.", "project", "project brief form",
   [h("What makes a good brief", 3, "medium"), lst(["The problem to solve, in your words", "What success looks like in six months", "Who else needs to agree", "A rough budget range"]),
    p("We never share what you send. If we're not the right fit, we'll say so and suggest someone who is.", "small", "secondary")]),
  next_steps("What happens next", [("We read it within two days", "Every brief is read by someone who'd work on it."),
       ("A first call", "30 minutes to talk it through. No charge, and no sales pitch."), ("A written proposal", "Scope, timeline and a fixed price, usually within a week of the call.")]),
  questions([("Do you sign NDAs?", "Yes. Send yours with the brief, or ask for ours."),
             ("What if my budget is small?", "Tell us anyway. We'll suggest what's possible, or a first step that fits."),
             ("How soon can you start?", "Usually within three to six weeks. Say if there's a hard deadline.")])])

page("page-client-onboarding", "Client onboarding page",
 "A welcome page for new clients: a thank you, the onboarding form (business details, address, website, who gets invoices, goals, the accounts and tools needed, how they like updates) beside what to have ready, the first weeks in steps, and questions. On AnyPress the form box becomes a Fluent Forms form when the page is saved.",
 "client onboarding, welcome, new client, intake, getting started, form",
 [intro("Welcome aboard", "Let's get you set up", "Thank you for choosing us. This form takes about ten minutes and gives us everything we need for your first meeting.", [("Fill in the form", None, "#start")]),
  form_section("Onboarding form", "Your details", "Answer what you can now; we'll go through the rest together at the first meeting.", "onboarding", "onboarding form",
   [h("Have these ready", 3, "medium"), lst(["Your business's legal name and address", "Who should get invoices", "Logins for the tools we'll use"]),
    h("About passwords", 3, "medium"), p("Never type passwords into a form or an email. List the accounts and we'll send a safe way to share access.", None, "secondary")]),
  next_steps("Your first weeks", [("Kick-off meeting", "An hour to agree goals, dates and how we'll keep in touch."),
       ("Set-up", "We get access, read everything and set up your project space."), ("First results", "Your first update, with what's done and what comes next.")]),
  questions([("Can I change my answers later?", "Yes. Just reply to any email from us with the change."),
             ("Who will I work with?", "One named person, from the kick-off to the end, with the team behind them.")])])

# ---------------------------------------------------------------- Industry starter pages (website)
page("page-home-valuation", "Home valuation page (real estate)",
 "A free valuation page for an estate agent or realtor: what a valuation includes, the valuation form (buying or selling, the address, type of home, bedrooms, when they plan to move) beside what the agent looks at, how it works in three steps, and questions. On AnyPress the form box becomes a Fluent Forms form when the page is saved.",
 "valuation, home value, appraisal, sell my home, realtor, estate agent, real estate, form",
 [intro("Free and without obligation", "What is your home worth today?", "A local agent visits, looks at what's sold nearby and gives you a price you can plan with. It takes about 45 minutes.", [("Ask for a valuation", None, "#valuation")]),
  form_section("Valuation", "Ask for your valuation", "Tell us a little about the home. An agent calls within one working day to arrange a visit.", "valuation", "valuation form",
   [h("What we look at", 3, "medium"), lst(["Homes like yours sold nearby in the last six months", "Size, condition and what's been updated", "The street, schools and transport", "How many buyers are looking right now"]),
    h("Buying too?", 3, "medium"), p("Tick Buying or Both and we'll send homes that match before they're advertised.", None, "secondary")]),
  next_steps("How it works", [("Tell us about the home", "A few details through the form or by phone."), ("A visit", "An agent walks round with you and answers your questions."),
       ("Your valuation in writing", "The price we'd market it at, and why, within two days.")]),
  questions([("Do I have to sell with you?", "No. The valuation is free, whatever you decide."),
             ("Is an online estimate enough?", "It's a start, but it can't see your kitchen, your garden or the work you've done. A visit can.")])])

page("page-order-pickup", "Order online page (restaurant)",
 "An order page for a restaurant, café or takeaway: opening and pickup times, the order form (pickup or delivery, what they'd like, when, allergies and notes, paid on collection) beside how ordering works, and questions. On AnyPress the form box becomes a Fluent Forms form when the page is saved. Shops that take card payments use the online store instead.",
 "order online, takeaway, pickup, collection, delivery, restaurant, cafe, food, form",
 [intro("Order ahead", "Order online, skip the wait", "Order by noon for lunch, by 5pm for dinner. We text you when it's ready.", [("Start your order", None, "#order")]),
  form_section("Order form", "Your order", "Write what you'd like, one item per line. We'll text to confirm the total and the time.", "order", "order form",
   [h("Times", 3, "medium"), p("Pickup and delivery: Tuesday to Sunday, 11:30am to 9pm", None, "secondary", bind="hours"),
    h("Paying", 3, "medium"), p("Pay by card or cash when you collect or when it arrives.", None, "secondary"),
    h("Allergies", 3, "medium"), p("Tell us in the form. If you're not sure about a dish, call before you order.", None, "secondary"), btns([("Call 555 0198", "outline", "tel:5550198", "phone")])]),
  questions([("How far do you deliver?", "Within three miles of the restaurant, for orders over $25."),
             ("Can I change my order?", "Call us up to 30 minutes before the time you picked."),
             ("Do you take large orders?", "Yes, for groups and offices. Give us a day's notice for more than ten people.")], "section-tint")])

def menu_part(title, note, items):
    return sec(title, N([h(title, 2, "x-large"), p(note, None, "secondary"), grid([dish(a, b, c) for a, b, c in items], 2, "18rem", "large")]))
page("page-menu", "Menu page (restaurant)",
 "A menu page for a restaurant or café: a short introduction with links to each part of the menu, starters, mains, desserts and drinks with prices, a note on allergies, and a call to order or book. Easy to read on a phone, and every dish is plain text the owner edits in place.",
 "menu, food, dishes, prices, restaurant, cafe, starters, mains, desserts, drinks",
 [sec("Introduction", N([mono("Seasonal menu"), h("The menu", 1, "xxx-large"), p("Cooked from scratch with what's good this week. Dishes marked (v) are vegetarian, (vg) vegan.", "large", "secondary"),
     links([("Starters", "#starters"), ("Mains", "#mains"), ("Desserts", "#desserts"), ("Drinks", "#drinks")])]), pad=("xx-large", "large", None, None), content="52rem"),
  menu_part("Starters", "To share, or for one.", [("Burrata (v)", "Roast tomatoes, basil oil, grilled bread.", "$12"), ("Crispy squid", "Lemon, chilli and aioli.", "$11"),
      ("Soup of the day (vg)", "Ask what it is today. With bread.", "$8"), ("Chicken wings", "Honey, soy and sesame.", "$10")]),
  menu_part("Mains", "Served with a side of your choice.", [("Roast chicken", "Half a bird, garlic and thyme, pan juices.", "$22"), ("Mushroom risotto (v)", "Wild mushrooms and parmesan.", "$18"),
      ("Steak frites", "8oz sirloin, peppercorn sauce, fries.", "$29"), ("Fish of the day", "From the market this morning, with greens.", "$24")]),
  menu_part("Desserts", "Made here every morning.", [("Chocolate tart", "Salted caramel and cream.", "$9"), ("Lemon posset (v)", "With shortbread.", "$8")]),
  menu_part("Drinks", "Local beer, natural wine and good coffee.", [("House wine", "Red, white or rosé, by the glass.", "$8"), ("Local beer", "Ask what's on tap.", "$7"),
      ("Lemonade (vg)", "Made here, still or sparkling.", "$4"), ("Coffee", "Espresso, flat white or filter.", "$3.50")]),
  sec("Allergies", card(N([h("Allergies and dietary needs", 2, "medium"), p("Our kitchen handles nuts, gluten, dairy and shellfish. Tell us about any allergy when you order and we'll tell you exactly what's in each dish.")]), "section-tint"), pad=("large", "large", None, None), content="52rem"),
  sec("Order or book", N([h("Hungry already?", 2, "xx-large", "center"), btns([("Order online", None, "/order/"), ("Book a table", "outline", "/contact/")], "center")]), "section-dark", content="44rem")])

page("page-plan-your-visit", "Plan your visit page (church)",
 "A first-visit page for a church: service times and the address up top, what to expect (how long, what to wear, parking, children's groups), a plan-your-visit form so someone looks out for them, a welcome from the pastor, other ways to get involved, and questions. On AnyPress the form box becomes a Fluent Forms form when the page is saved.",
 "church, plan your visit, new here, visit, sunday service, worship, first time, form",
 [intro("New here?", "We'd love to meet you", "Come as you are: there's coffee from 8:30, and someone at the door to show you around.", [("Plan your visit", None, "#visit"), ("Directions", "outline", "#visit")]),
  sec("What to expect", N([h("What to expect", 2, "x-large"), grid([tfeat(a, b) for a, b in [
      ("About an hour", "Songs, a short talk from the Bible and a prayer. Nobody will ask you to stand up or speak."), ("Come as you are", "Jeans or a suit: you'll see both."),
      ("Parking", "Free in the lot behind the hall, with spaces for visitors by the door."), ("Children", "Groups for ages 2 to 11 during the service, with checked and trained leaders."),
      ("Coffee after", "Stay for coffee in the hall and meet people. No pressure."), ("Accessible", "Step-free entry, a hearing loop and accessible toilets.")]], 3, "14rem", "x-large")]), "section-tint"),
  form_section("Plan your visit", "Plan your visit", "Let us know you're coming and someone will meet you at the door, show you around and save you a seat.", "visit", "plan-your-visit form",
   [h("Find us", 3, "medium"), p("12 Chapel Lane, Springfield", None, "secondary", bind="address"),
    h("Service times", 3, "medium"), p("Sundays at 9am and 11am", None, "secondary", bind="hours"),
    h("Questions?", 3, "medium"), btns([("Call the office", "outline", "tel:5550164", "phone_link")])]),
  sec("Welcome", cols([col(img("placeholder-square.svg", "The pastor outside the church", "1", "md"), "40%"),
      col(N([h("A welcome from our pastor", 2, "x-large"), p("Whether you've been to church all your life or never at all, you're welcome here. Come with your questions; we'd love to hear them.", "large"), p("Pastor James and the team", None, "secondary")]), valign="center")], "x-large", "wide", "center")),
  sec("Get involved", N([h("When you're ready", 2, "x-large"), grid([tfeat(a, b) for a, b in [
      ("Small groups", "Meet midweek in a home to talk, eat and pray."), ("Serve", "Welcome team, kids' groups, music, the food bank."),
      ("Give", "Support the church's work, once or every month.")]], 3, "14rem", "x-large")]), "section-brand-soft"),
  questions([("Do I have to be a member?", "No. Everyone is welcome, every week."),
             ("Is there something during the week?", "Small groups, youth on Fridays and a lunch club for older neighbours on Wednesdays.")])])

# ---------------------------------------------------------------- Booking pages (bookings site type)
def booking_page(slug, title, desc, kw, eyebrow, heading_, lead, services, know, faq, extra=None):
    page(slug, title, desc, kw, [
        intro(eyebrow, heading_, lead, [("Book now", None, "#book")]),
        sec("Services", N([h("Services and prices", 2, "x-large"), stackg([sep()] + [x for a, b, c in services for x in (svc_row_simple(a, b, c), sep())], "small")]), content="60rem"),
        sec("Book", cols([col(N([h("Pick a time", 2, "x-large"), p("Choose a service, then a time that suits you. You'll get a confirmation by email straight away, and a reminder the day before.", None, "secondary"), booking_slot]), "62%"),
            col(card(N(know), "section-brand-soft"))], "x-large", "wide", "top"), "section-tint")]
        + (extra or []) + [questions(faq)])

def svc_row_simple(name, text, price):
    return row([stackg([h(name, 3, "medium"), p(text, None, "secondary")], "x-small"), p(price, "medium")], "space-between", "medium", False, "top")

page("page-book-consultation", "Book a consultation page (law office)",
 "A consultation page for a law office: practice areas with consultation lengths and fees, the consultation request form (what they need help with, who else is involved for the conflict check, any court date, a short summary, and the disclaimer that asking doesn't make the firm their lawyers) beside what to bring, the booking calendar, and questions. On AnyPress the form box becomes a Fluent Forms form and the calendar box FluentBooking's calendar when the page is saved.",
 "law firm, lawyer, attorney, consultation, legal advice, book, appointment, conflict check, form",
 [intro("Talk to a lawyer", "Book a consultation", "Tell us what you need and pick a time. We check for conflicts before we meet, so everything you tell us stays protected.", [("Request a consultation", None, "#consult"), ("Pick a time", "outline", "#book")]),
  sec("Services", N([h("Practice areas", 2, "x-large"), stackg([sep()] + [x for a, b, c in [
      ("Family law", "Divorce and separation, custody, support, adoption, prenuptial agreements. 45 minutes.", "$150"),
      ("Business law", "Forming a company, contracts and leases, disputes, buying or selling a business. 30 minutes.", "$120"),
      ("Wills and estates", "Wills, trusts, powers of attorney and probate. 30 minutes.", "Free"),
      ("Criminal defense", "DUI, drug, assault, theft and white-collar charges, or if you haven't been charged yet. 30 minutes.", "Free")] for x in (svc_row_simple(a, b, c), sep())], "small")]), content="60rem"),
  form_section("Consultation form", "Request a consultation", "A few questions first, so the right lawyer is ready for you.", "consultation", "consultation request form",
   [h("Bring with you", 3, "medium"), lst(["Photo ID", "Any letters, contracts or court papers", "A list of dates and names that matter"]),
    h("Is it urgent?", 3, "medium"), p("If someone is in custody or a court date is days away, call us now.", None, "secondary"), btns([("Call 555 0119", "outline", "tel:5550119", "phone")])]),
  sec("Book", N([h("Pick a time", 2, "x-large"), p("Choose your practice area, then a time. Online and in-office meetings are both fine.", None, "secondary"), booking_slot]), "section-tint", content="60rem"),
  questions([("Does booking make you my lawyers?", "Not yet. We become your lawyers when we both sign an engagement letter, usually after the consultation."),
             ("Why do you ask who else is involved?", "Lawyers can't act against a current or former client. We check every name before we meet."),
             ("Is what I tell you confidential?", "Yes. Keep the details for the meeting itself; the form only needs a few lines.")])])

booking_page("page-book-dental", "Book an appointment page (dental)",
 "An appointment page for a dental practice: treatments with how long they take and what they cost, the booking calendar beside what new patients should know, emergencies, and questions. On AnyPress the calendar box becomes FluentBooking's calendar, with every booking type, when the page is saved.",
 "dentist, dental, appointment, checkup, cleaning, emergency, new patients, book",
 "New patients welcome", "Book your dental appointment", "Checkups, cleaning and treatment, booked online in a minute. Same-day emergency appointments every weekday.",
 [("New patient exam", "Full checkup, X-rays and a treatment plan. 60 minutes.", "$95"), ("Checkup and cleaning", "For existing patients, every six months. 45 minutes.", "$85"),
  ("Emergency appointment", "Pain, swelling or a broken tooth. Same day. 30 minutes.", "$65"), ("Whitening consultation", "Is it right for you, and what it costs. 20 minutes.", "Free")],
 [h("New patients", 3, "medium"), lst(["Arrive ten minutes early", "Bring your insurance card and a list of medicines", "Tell us if you're nervous: we'll take it slowly"]),
  h("In pain right now?", 3, "medium"), p("Call before 10am for a same-day appointment.", None, "secondary"), btns([("Call 555 0133", "outline", "tel:5550133", "phone")])],
 [("Do you take my insurance?", "We work with most plans. Bring your card and we'll check before any treatment."),
  ("Can I change my appointment?", "Yes, through the link in your confirmation email, up to 24 hours before."),
  ("Do you see children?", "Yes, from their first tooth. Children's checkups are free with a parent's appointment.")])

booking_page("page-book-salon", "Book an appointment page (salon)",
 "An appointment page for a hair salon, barber or beauty studio: services with times and prices from, the booking calendar beside what to know before a first visit, and questions. On AnyPress the calendar box becomes FluentBooking's calendar, with every booking type, when the page is saved.",
 "salon, hair, barber, beauty, appointment, haircut, colour, book online",
 "Book online", "Book your appointment", "Pick your service and your stylist, and choose a time. It takes less than a minute.",
 [("Cut and finish", "Wash, cut and blow-dry. 45 minutes.", "From $45"), ("Colour", "Roots or full colour, with a cut. 2 hours.", "From $95"),
  ("Balayage", "Hand-painted colour, toner and finish. 3 hours.", "From $160"), ("Blow-dry", "Wash and style. 30 minutes.", "From $30")],
 [h("First visit?", 3, "medium"), lst(["Colour needs a patch test 48 hours before: book it free", "Arrive five minutes early for a quick chat", "Bring a photo of what you'd like"]),
  h("Changing plans", 3, "medium"), p("Move or cancel your appointment free up to 24 hours before.", None, "secondary")],
 [("Can I choose my stylist?", "Yes. Pick them when you book, or choose anyone for the first free time."),
  ("How much is a deposit?", "Colour and balayage take a $20 deposit when you book, taken off the bill."),
  ("Do you sell gift vouchers?", "Yes, for any amount or service, at the front desk or online.")])

booking_page("page-book-classes", "Classes and booking page (yoga studio)",
 "A classes page for a yoga studio, gym or dance school: the classes with their length, level and price, the booking calendar beside what to bring to a first class, a weekly timetable, and questions. On AnyPress the calendar box becomes FluentBooking's calendar, with every class, when the page is saved.",
 "yoga, classes, timetable, schedule, studio, pilates, book a class, group class",
 "Classes for every body", "Book a class", "Small classes, seven days a week, in the studio and online. Your first class is free.",
 [("Morning flow", "Gentle, all levels. 60 minutes, up to 14 people.", "$18"), ("Power yoga", "Strong and sweaty. 60 minutes, some experience.", "$18"),
  ("Yin and meditation", "Slow and deep. 75 minutes, all levels.", "$20"), ("Private session", "One to one, at a time that suits you. 60 minutes.", "$70")],
 [h("Your first class", 3, "medium"), lst(["Come ten minutes early", "Mats, blocks and towels are here", "Tell your teacher about any injuries"]),
  h("Can't make it?", 3, "medium"), p("Cancel up to 12 hours before and your class goes back on your pass.", None, "secondary")],
 [("Do I need experience?", "No. Morning flow and yin are made for beginners."),
  ("Do you have passes?", "Yes: ten classes for $150, or unlimited for $89 a month."),
  ("What if a class is full?", "Join the waiting list when you book. If a place opens, it's yours.")],
 [sec("Timetable", N([h("This week", 2, "x-large"), table(["Day", "Morning", "Evening"], [
     ["Monday", "Morning flow, 7am", "Power yoga, 6pm"], ["Tuesday", "Yin and meditation, 9am", "Morning flow, 7pm"], ["Wednesday", "Morning flow, 7am", "Power yoga, 6pm"],
     ["Thursday", "Power yoga, 7am", "Yin and meditation, 7pm"], ["Friday", "Morning flow, 7am", ""], ["Saturday", "Morning flow, 9am", "Yin and meditation, 5pm"], ["Sunday", "Power yoga, 10am", ""]], "stripes")]), content="60rem")])

# ---------------------------------------------------------------- Policies
policy("page-cancellation-policy", "Cancellation policy page (bookings)",
 "A cancellation and no-show policy for a business that takes bookings, in plain words: how much notice to give, the late cancellation and no-show fees, rescheduling, deposits and refunds, emergencies, and how to cancel. Set the numbers to the business's own before publishing, and show the policy where people book.",
 "cancellation policy, no-show, late cancellation, rescheduling, deposit, refund, bookings, policy",
 "Our policy", "Cancellations and no-shows", "When someone cancels late, that time can't go to anyone else. This page says what we ask, so it's fair for everyone.",
 ["Cancel or move for free up to 24 hours before", "Less than 24 hours: a $25 fee", "No-show: the full price", "Emergencies: tell us and we'll be fair"],
 [sec("Cancellations", N([clause("Cancelling", ["You can cancel for free up to 24 hours before your appointment, through the link in your confirmation email or by calling us.",
      "If you cancel less than 24 hours before, we charge a $25 late cancellation fee."]),
    clause("Moving your appointment", ["Moving an appointment is free up to 24 hours before. A move with less notice counts as a late cancellation."])]), content="48rem"),
  sec("No-shows", N([clause("No-shows", ["If you don't come and don't tell us, we charge the full price of the appointment.",
      "After two no-shows, we ask for a deposit to book again."])]), content="48rem"),
  sec("Deposits and refunds", N([clause("Deposits and refunds", ["Some appointments take a deposit when you book. It comes off the final bill."],
      ["Cancel 24 hours or more before: your deposit is refunded in full", "Move your appointment: your deposit moves with it", "Cancel late or don't come: the deposit isn't refunded"]),
    clause("Emergencies", ["Illness, accidents and family emergencies happen. Tell us as soon as you can and we'll waive the fee."])]), content="48rem")],
 sec("Contact", N([h("Need to cancel or move?", 2, "x-large"), p("Use the link in your confirmation email, or call us.", None, "secondary"), btns([("Call 555 0142", None, "tel:5550142", "phone")])]), "section-tint", content="48rem"))

policy("page-return-policy", "Return and refund policy page (online store)",
 "A return and refund policy for an online store, written as answers to the questions shoppers ask: how long they have, what condition items must be in, what can't be returned, who pays for return shipping, how and when refunds arrive, exchanges, digital products, and how to start a return. Set the numbers to the shop's own, check the law where the shop sells, and link the policy from the footer and checkout.",
 "return policy, refund policy, returns, refunds, exchanges, online store, shipping, policy",
 "Shopping with us", "Returns and refunds", "Changed your mind? Send it back within 30 days for a full refund. Here's how it works.",
 ["30 days from delivery to send items back", "Unused, with tags and in the original packaging", "Free returns if something arrives faulty or wrong", "Refunds within 5 working days of the return reaching us"],
 [sec("Returns", N([clause("How long do I have?", ["30 days from the day your order arrives. Over the holidays, anything delivered between November 15 and December 15 can come back until January 15. Later deliveries keep the full 30 days."]),
    clause("What condition must items be in?", ["Unused and unwashed, with the tags on and in the original packaging, so we can sell them again."]),
    clause("What can't be returned?", ["For hygiene and safety, some things can't come back unless they're faulty:"], ["Underwear, swimwear and earrings", "Personalised or made-to-order items", "Gift cards", "Food and flowers"]),
    clause("Who pays for return shipping?", ["If an item is faulty or we sent the wrong thing, we pay and send a free label. Otherwise return shipping is up to you."])]), content="48rem"),
  sec("Refunds", N([clause("When will I get my money?", ["We refund to your original payment method within 5 working days of your return reaching us. Your bank may take another 5 to 10 days to show it."]),
    clause("Can I exchange instead?", ["Yes. Choose an exchange when you start your return and we'll send the new size or colour as soon as yours is on its way back."]),
    clause("Digital products", ["Downloads can be refunded within 14 days if they don't work as described or never arrived, and you haven't downloaded them more than once."])]), content="48rem")],
 sec("Contact", N([h("Start a return", 2, "x-large"), p("Sign in to your account and choose the order, or email us with your order number. We reply within one working day.", None, "secondary"),
     btns([("Email us", None, "mailto:hello@example.com", "email_link")])]), "section-tint", content="48rem"))
print("guide pages ok")
