# Content for the AiEngineered site. Prices come straight from the two calculators so the site and the product agree.
SIZE_MULT = [0.7, 1, 1.6]

def nice(n):
    step = 10 if n < 1000 else (50 if n < 10000 else 100)
    import math
    return int(math.floor(n / step + 0.5) * step)  # same as JS Math.round, so prices match the calculator

def trade_ranges(base):
    out = []
    for m in SIZE_MULT:
        t = base * m
        out.append((nice(t * 0.9), nice(t * 1.2)))
    return out

TRADE_RAW = {
 'roofer': ('Roofing', ['Small (porch / one slope)', 'Typical house', 'Large / detached'], [['New Roof', 7500], ['Flat Roofing', 3200], ['Roof Repairs', 450], ['Fascias & Soffits', 2200], ['Guttering', 800], ['Chimney Repairs', 650]]),
 'plumber': ('Plumbing', ['Small fix', 'Standard job', 'Large / multi-room'], [['Boiler Installation', 2800], ['Bathroom Fitting', 4500], ['Leak & Pipe Repairs', 280], ['Power Flush', 450], ['Hot Water Cylinder', 1500], ['Radiator Replacement', 350]]),
 'electrician': ('Electrical', ['1–2 bedrooms', '3 bedrooms', '4+ bedrooms'], [['Full Rewire', 4500], ['Consumer Unit Upgrade', 650], ['EV Charger Installation', 900], ['EICR Testing', 180], ['Lighting & Sockets', 450], ['Outdoor Lighting', 600]]),
 'builder': ('Building & Extensions', ['Small (1 room)', 'Medium (2–3 rooms)', 'Large (whole house)'], [['House Extension', 18000], ['Loft Conversion', 32000], ['Garage Conversion', 14000], ['Brickwork & Repairs', 1500], ['Structural Alterations', 3500], ['Full Renovation', 45000]]),
 'driveways': ('Driveways & Landscaping', ['Small (1 car)', 'Standard (2 cars)', 'Large (3+ cars)'], [['Resin Driveways', 4500], ['Block Paving', 6000], ['Tarmac Driveway', 3500], ['Patio & Landscaping', 4500], ['Dropped Kerb', 1800], ['Walls & Fencing', 1600]]),
 'heatingengineer': ('Heating', ['1–2 bedrooms', '3 bedrooms', '4+ bedrooms'], [['Boiler Installation', 2800], ['Boiler Servicing', 90], ['Central Heating', 5500], ['Underfloor Heating', 4500], ['Power Flush', 450], ['Smart Heating Controls', 350]]),
 'carpenter': ('Carpentry & Joinery', ['One room / item', 'A few rooms', 'Whole property'], [['Fitted Wardrobes', 2200], ['Kitchen Fitting', 2800], ['Doors & Skirting', 1100], ['Staircase Renovation', 2600], ['Decking & Pergolas', 2800], ['Bespoke Shelving', 900]]),
 'plasterer': ('Plastering', ['1 room', '2–3 rooms', 'Whole house'], [['Skimming', 450], ['Full Re-plaster', 1800], ['Plasterboarding', 1200], ['External Rendering', 4500], ['Coving & Cornice', 650], ['Artex Removal', 850]]),
 'painter': ('Painting & Decorating', ['1 room', '2–3 rooms', 'Whole house'], [['Interior Painting', 1800], ['Exterior Painting', 2800], ['Wallpapering', 550], ['Woodwork & Doors', 650], ['Kitchen Respray', 1800], ['Fence & Shed Painting', 450]]),
 'tiler': ('Tiling', ['Under 5 m²', '5–15 m²', '15 m² +'], [['Bathroom Tiling', 1100], ['Kitchen Splashback', 450], ['Floor Tiling', 1200], ['Wet Room Tanking', 2200], ['Patio Tiling', 1800], ['Feature Wall Tiling', 650]]),
 'hvac': ('Air conditioning & heat pumps', ['Small (1 zone)', 'Home (2–3 zones)', 'Large / commercial'], [['Air Conditioning', 2800], ['Heat Pumps', 9500], ['Ventilation & Extraction', 1200], ['MVHR Systems', 5500], ['AC Servicing', 180], ['Commercial Maintenance', 650]]),
 'glaziery': ('Windows & Doors', ['1–3 units', '4–8 units', '9+ units'], [['uPVC Windows', 3800], ['Bi-Fold Doors', 4800], ['Composite Doors', 1900], ['Misted Unit Repairs', 250], ['Roof Windows', 1500], ['Sash Window Restoration', 2200]]),
}

CLINIC_RAW = {
 'aesthetics': ('Aesthetics', ['Single area / 0.5ml', 'Standard / 1ml', 'Full package / multi-area'], [
   ('Anti-wrinkle injections (3 areas)', [[150, 220], [230, 320], [320, 450]], None), ('Lip & dermal fillers', [[150, 220], [200, 320], [550, 950]], None),
   ('Profhilo / skin boosters', [[220, 300], [300, 420], [580, 850]], None), ('Laser hair removal course', [[270, 450], [480, 840], [1200, 2200]], None),
   ('Microneedling & exosomes', [[160, 240], [260, 380], [650, 1000]], None), ('Hydrafacial Platinum', [[150, 190], [190, 260], [480, 690]], None)]),
 'tattoo': ('Tattoo', ['Small (2–3 hrs)', 'Half day (4 hrs)', 'Full day sitting (7–8 hrs)'], [
   ('Fine line / minimalist piece', [[150, 300], [350, 520], [600, 900]], None), ('Black & grey realism', [[250, 400], [450, 650], [750, 1100]], None),
   ('Half-sleeve / large custom', [[280, 420], [500, 700], [800, 1200]], None), ('Full-day studio sitting', [[260, 400], [450, 640], [750, 1050]], None),
   ('Cover-up / rework', [[280, 450], [480, 700], [800, 1200]], None), ('Portrait / detailed piece', [[300, 460], [520, 750], [850, 1250]], None)]),
 'dentist': ('Cosmetic dentistry', ['Minor / 1–2 teeth', 'Standard arch (4–6 teeth)', 'Full dual arch'], [
   ('Invisalign clear aligners', [[1500, 2500], [2500, 3800], [3500, 5500]], None), ('Composite bonding', [[250, 700], [1000, 2100], [3200, 6000]], None),
   ('Porcelain veneers', [[700, 2200], [3000, 6600], [10000, 18000]], None), ('Professional whitening', [[250, 400], [400, 650], [550, 900]], None),
   ('Dental implants', [[2200, 3200], [6000, 12000], [18000, 32000]], None), ('Full smile makeover', [[3000, 6000], [8000, 14000], [16000, 30000]], None)]),
 'cosmetic': ('Cosmetic surgery', ['Minor / single area', 'Standard procedure', 'Extensive / combined'], [
   ('Rhinoplasty', [[4500, 6000], [5500, 7500], [7000, 9500]], None), ('Breast augmentation', [[4500, 5800], [5200, 7000], [6800, 9000]], None),
   ('Liposuction / Vaser lipo', [[2800, 4000], [4000, 6000], [6000, 9500]], None), ('Tummy tuck', [[5000, 6500], [6000, 8000], [8000, 11000]], None),
   ('Eyelid surgery', [[2500, 3500], [3200, 4500], [4500, 6500]], None), ('Hair transplant (FUE / DHI)', [[2500, 4000], [4000, 6500], [6500, 10000]], None)]),
 'wedding': ('Wedding photography', ['Essentials (key moments)', 'Signature (most of the day)', 'Luxury (full day + album)'], [
   ('Wedding day photography', [[700, 1100], [1100, 1700], [1600, 2500]], None), ('Photography + second shooter', [[950, 1400], [1450, 2100], [2000, 3000]], None),
   ('Photo + videography', [[1400, 2200], [2200, 3300], [3000, 4600]], None), ('Elopement / registry office', [[350, 650], [550, 900], [800, 1300]], None),
   ('Engagement shoot', [[180, 300], [250, 400], [350, 550]], None), ('Destination wedding', [[1600, 2400], [2200, 3200], [2900, 4400]], None)]),
 'florist': ('Wedding flowers', ['Intimate (simple & seasonal)', 'Classic (lush & full)', 'Grand (luxe statement)'], [
   ('Bridal bouquet', [[90, 150], [150, 230], [230, 380]], None), ('Bridal party bouquets & buttonholes', [[200, 350], [350, 600], [600, 1000]], None),
   ('Ceremony arch & aisle', [[350, 650], [650, 1200], [1200, 2500]], None), ('Table centrepieces', [[250, 500], [500, 1100], [1100, 2500]], None),
   ('Full wedding flowers', [[800, 1400], [1500, 2800], [3000, 6000]], None), ('Event & venue styling', [[300, 600], [600, 1200], [1200, 3000]], None)]),
 'groomer': ('Dog grooming', ['Small dog', 'Medium dog', 'Large dog'], [
   ('Full groom', [[35, 45], [45, 60], [60, 85]], None), ('Bath, brush & tidy', [[25, 35], [30, 45], [40, 60]], None),
   ('Puppy intro groom', [[20, 30], [25, 35], [30, 40]], None), ('Hand stripping', [[45, 60], [55, 75], [70, 100]], None),
   ('De-shedding treatment', [[35, 45], [45, 60], [60, 80]], None), ('Nails, ears & hygiene tidy', [[10, 15], [12, 18], [15, 22]], None)]),
 'salon': ('Hair salon', ['Short hair', 'Medium / shoulder length', 'Long / thick hair'], [
   ('Cut & blow dry', [[35, 50], [40, 60], [50, 75]], None), ('Balayage / ombré', [[120, 160], [150, 200], [180, 260]], None),
   ('Full head highlights', [[100, 140], [120, 170], [150, 210]], None), ('Root colour / tint', [[50, 70], [55, 80], [65, 95]], None),
   ('Keratin smoothing', [[150, 200], [180, 250], [220, 320]], None), ('Hair extensions', [[200, 350], [350, 600], [500, 900]], ['Half head / volume', 'Full head', 'Full head, premium hair'])]),
 'cakes': ('Cakes', ['Small (serves 10–20)', 'Medium (serves 30–60)', 'Large (serves 70–120)'], [
   ('Wedding cake', [[250, 400], [400, 650], [650, 1100]], None), ('Birthday / celebration cake', [[45, 80], [80, 150], [150, 280]], None),
   ('Cupcakes', [[30, 45], [55, 80], [100, 150]], ['12 cupcakes', '24 cupcakes', '48 cupcakes']), ('Dessert table', [[150, 250], [250, 450], [450, 800]], None),
   ('Sculpted / novelty cake', [[120, 200], [200, 350], [350, 600]], None), ('Christening / baby shower cake', [[60, 100], [100, 180], [180, 320]], None)]),
 'family': ('Family photography', ['Mini (5–10 images)', 'Classic (15–25 images)', 'Luxury (full gallery + prints)'], [
   ('Newborn shoot', [[150, 250], [250, 400], [400, 650]], None), ('Family shoot', [[100, 180], [180, 300], [300, 500]], None),
   ('Maternity shoot', [[120, 200], [200, 320], [320, 500]], None), ('Cake smash', [[100, 160], [160, 250], [250, 380]], None),
   ('Milestone / sitter shoot', [[100, 160], [160, 260], [260, 400]], None), ('Seasonal mini session', [[50, 80], [80, 120], [120, 180]], ['Mini session', 'Mini + extra images', 'Mini + print box'])]),
}

def lower_job(name):
    # "Roof Repairs" -> "Roof repairs" (keep acronyms like EV, EICR, AC, MVHR, uPVC)
    words = name.split(' ')
    out = [words[0]]
    for w in words[1:]:
        out.append(w if (w.isupper() or w[:1].islower() or w in ('&',)) else w.lower())
    return ' '.join(out)

# Each page: slug, calculator key, kind, plural (for "for X"), short label, who the customers are, intro, FAQs
NICHES = [
 dict(slug='roofers', key='roofer', kind='trade', plural='roofers', name='Roofers', people='homeowners',
  intro='Most roofing enquiries start with the same question: roughly what will this cost? Your calculator answers it on the spot for repairs, re-roofs, flat roofs, fascias, guttering and chimney work, then sends you the homeowner’s name, number and the job they priced.',
  faqs=[('Can it show a call-out charge for emergency repairs?', 'Yes. When a homeowner picks “Emergency”, the guide price adds an urgency uplift and a call-out charge, shown on its own line so nobody is surprised.'),
        ('What if I need to see the roof before I can price it?', 'That is expected. Every price is labelled as a guide, and the calculator tells the homeowner you will confirm an exact quote once you have seen the job. It sets expectations and filters out people whose budget is nowhere near.')]),
 dict(slug='plumbers', key='plumber', kind='trade', plural='plumbers', name='Plumbers', people='homeowners',
  intro='A guide price for a boiler, a bathroom or a leak, on your website, at any hour. Homeowners pick the job and how big it is, see a price range for your area, and send their details to your inbox with one-tap call and WhatsApp buttons.',
  faqs=[('Can I keep emergency work separate from planned jobs?', 'Yes. Homeowners choose flexible, within 7 days or emergency. Emergency adds an uplift and a call-out charge, so urgent jobs are priced like urgent jobs.'),
        ('I do heating as well as plumbing. Which one should I pick?', 'Pick whichever is most of your work. Each version lists six common jobs, and we can hide any you don’t do.')]),
 dict(slug='electricians', key='electrician', kind='trade', plural='electricians', name='Electricians', people='homeowners and landlords',
  intro='Rewires, consumer units, EV chargers, EICRs and lighting, each with a guide price by property size. Homeowners and landlords see a range in seconds and send you the job, their postcode and the best way to reach them.',
  faqs=[('Can landlords use it for EICR quotes?', 'Yes. EICR testing is one of the standard jobs, priced by number of bedrooms, so a landlord can get a guide price and send you their details in under a minute.'),
        ('Does it replace my written quote?', 'No. It gives a guide range so people know roughly what to expect. You still confirm the exact price, and your certification and terms stay exactly as they are.')]),
 dict(slug='builders', key='builder', kind='trade', plural='builders', name='Builders', people='homeowners',
  intro='Extensions, loft and garage conversions, brickwork, structural alterations and full renovations vary a lot in price, which is exactly why homeowners want a rough figure first. A guide range on your website tells them early whether you are the right fit, and sends you the serious ones.',
  faqs=[('Big projects vary hugely. Is a guide range still useful?', 'Yes, because it filters. Someone with £5,000 for an extension sees the range and either adjusts their plans or moves on, and you spend your evenings quoting people whose budget fits.'),
        ('Can it include driveways as well as building work?', 'Yes. If your website shows both, the calculator can list driveway and building jobs together.')]),
 dict(slug='driveway-installers', key='driveways', kind='trade', plural='driveway installers', name='Driveway installers', people='homeowners',
  intro='Resin, block paving, tarmac, patios, dropped kerbs and walls, priced by how many cars the driveway holds. Homeowners compare options in seconds and send you the one they want, with their postcode.',
  faqs=[('Can homeowners compare resin with block paving?', 'Yes. They can switch between jobs and sizes and watch the guide price change, which is often what they are trying to work out before they call anyone.'),
        ('Are the prices set for my area?', 'They start from typical guide prices adjusted for your town. Tell us what you charge and we will move the price level up or down to match.')]),
 dict(slug='heating-engineers', key='heatingengineer', kind='trade', plural='heating engineers', name='Heating engineers', people='homeowners',
  intro='New boilers, servicing, central heating, underfloor heating, power flushes and smart controls, priced by property size. The calculator answers the “how much is a new boiler?” question before anyone has to ring you.',
  faqs=[('Can I show boiler servicing as well as installs?', 'Yes. Servicing is one of the standard jobs, so you can pick up small regular work as well as big installs.'),
        ('What about winter call-outs?', 'Homeowners can choose emergency timing, which adds an uplift and a call-out charge on a separate line.')]),
 dict(slug='carpenters-joiners', key='carpenter', kind='trade', plural='carpenters and joiners', name='Carpenters & joiners', people='homeowners',
  intro='Fitted wardrobes, kitchen fitting, doors and skirting, staircases, decking and shelving, each with a guide price by the scale of work. Customers see a range and send you the job with any notes about sizes or materials.',
  faqs=[('My work is mostly bespoke. Can a calculator really price it?', 'It gives a starting range, which is what most people want before they get in touch. Notes from the customer come through with every request, so you know what they have in mind before you reply.'),
        ('Can I remove jobs I don’t do?', 'Yes. Tell us which jobs you don’t do and we will hide them.')]),
 dict(slug='plasterers', key='plasterer', kind='trade', plural='plasterers', name='Plasterers', people='homeowners',
  intro='Skimming, full re-plasters, plasterboarding, rendering, coving and Artex removal, priced by area. Homeowners see a guide range for one room or the whole house and send you their details straight away.',
  faqs=[('Can it price external rendering separately?', 'Yes. Rendering is its own job with its own guide price, so it doesn’t get mixed up with internal work.'),
        ('Do customers have to phone me?', 'No. They send their name, number, email and the job, and you choose how to reply: call, WhatsApp, text or email.')]),
 dict(slug='painters-decorators', key='painter', kind='trade', plural='painters and decorators', name='Painters & decorators', people='homeowners',
  intro='Interior and exterior painting, wallpapering, woodwork, kitchen resprays and fences, priced by how many rooms. It turns “can you give me a rough idea?” messages into requests with the job and size already filled in.',
  faqs=[('Can it handle kitchen resprays?', 'Yes. Kitchen respraying is one of the standard jobs, with its own guide price.'),
        ('What do I get when someone uses it?', 'An email with their name, phone, email, the job, the size, the guide price they saw and any notes, plus buttons to call or WhatsApp them in one tap.')]),
 dict(slug='tilers', key='tiler', kind='trade', plural='tilers', name='Tilers', people='homeowners',
  intro='Bathrooms, splashbacks, floors, wet rooms, patios and feature walls, priced by square metres. Customers choose the job and area, see a guide range and send you the details.',
  faqs=[('Can it price by square metre?', 'Yes. The size options are in square metres (under 5, 5 to 15, and 15 plus), which is how most tiling jobs are thought about.'),
        ('Can it include wet room tanking?', 'Yes. Wet room tanking is one of the standard jobs.')]),
 dict(slug='air-conditioning-installers', key='hvac', kind='trade', plural='air conditioning and heat pump installers', name='Air con & heat pump installers', people='homeowners and businesses',
  intro='Air conditioning, heat pumps, ventilation, MVHR, servicing and maintenance contracts, priced by system size. Homeowners and businesses see a guide range and send you the job and their details.',
  faqs=[('Does it work for commercial customers?', 'Yes. Commercial maintenance is one of the jobs, and “Large / commercial” is one of the size options.'),
        ('Can it show prices in US dollars?', 'Yes. If your business is in the US, prices are shown in dollars and adjusted for your city.')]),
 dict(slug='window-door-fitters', key='glaziery', kind='trade', plural='window and door fitters', name='Window & door fitters', people='homeowners',
  intro='uPVC windows, bi-folds, composite doors, misted units, roof windows and sash restoration, priced by the number of units. Homeowners see a guide range before they ask for a home visit.',
  faqs=[('Can it price small repairs like misted units?', 'Yes. Misted unit repairs are a standard job, so you can pick up quick work as well as full installs.'),
        ('Will it replace my survey visit?', 'No. It gives a guide range so the homeowner knows what to expect, and you confirm the exact price after measuring.')]),
 dict(slug='aesthetics-clinics', key='aesthetics', kind='clinic', plural='aesthetics clinics', name='Aesthetics clinics', people='clients',
  intro='A booking page for your Instagram bio and website. Clients choose a treatment and package, see a guide price straight away, and send a consultation request with their preferred way to be contacted. You set your own treatments and prices from a private link.',
  faqs=[('Can I set my own treatments and prices?', 'Yes. You get a private edit link where you change treatments, options and prices whenever you like. Changes show on your page straight away.'),
        ('Does it check clients are over 18?', 'Yes. For aesthetics treatments the request form asks clients to confirm they are 18 or over before they can send it.')]),
 dict(slug='tattoo-studios', key='tattoo', kind='clinic', plural='tattoo studios', name='Tattoo studios', people='clients',
  intro='Clients choose a style and session length, see a guide price, and send a consultation request with placement, size and references in the notes. It cuts down the “how much for a small tattoo?” DMs and leaves you the serious enquiries.',
  faqs=[('Can clients tell me about placement and size?', 'Yes. The request form has a notes box for placement, size, style references and colour, and it all arrives in your email.'),
        ('Can I change the styles and prices?', 'Yes, any time, from your private edit link.')]),
 dict(slug='cosmetic-dentists', key='dentist', kind='clinic', plural='cosmetic dentists', name='Cosmetic dentists', people='patients',
  intro='Invisalign, bonding, veneers, whitening, implants and smile makeovers, with a guide price by scope. Patients see a range before they book, and you receive consultation requests with the treatment and budget already clear.',
  faqs=[('Does it give clinical advice?', 'No. It shows guide prices only and makes clear the final price follows a clinical assessment.'),
        ('Can I list treatments that aren’t in the standard menu?', 'Yes. Your private edit link lets you change treatments, options and prices.')]),
 dict(slug='cosmetic-surgery-clinics', key='cosmetic', kind='clinic', plural='cosmetic surgery clinics', name='Cosmetic surgery clinics', people='patients',
  intro='Guide prices for procedures such as rhinoplasty, breast augmentation, liposuction, tummy tucks, eyelid surgery and hair transplants. Patients see a range and request a consultation with the surgeon. The page reminds them that surgery always needs a consultation and a cooling-off period.',
  faqs=[('Can it show prices to patients travelling from abroad?', 'Yes. Clinics in Turkey can show package prices in each visitor’s own currency.'),
        ('Does it encourage people to book surgery straight away?', 'No. It shows guide prices and asks for a consultation request only, with a clear note about consultation and cooling-off before any booking.')]),
 dict(slug='wedding-photographers', key='wedding', kind='clinic', plural='wedding photographers', name='Wedding photographers', people='couples',
  intro='Couples pick their coverage and package, see a guide price, and check availability for their date in one tap. You get their date, venue and what matters to them in one email.',
  faqs=[('Can couples send their wedding date?', 'Yes. The form asks for the wedding date, and it arrives in your email with their package and budget range.'),
        ('Can I put it in my Instagram bio?', 'Yes. That is what most photographers do: the link goes in your bio, and couples get a price without messaging you first.')]),
 dict(slug='wedding-florists', key='florist', kind='clinic', plural='wedding florists', name='Wedding florists', people='couples',
  intro='Bouquets, buttonholes, arches, centrepieces and full wedding flowers, priced by style. Couples see a guide range and request a flower consultation with their date, venue and colours.',
  faqs=[('Can couples tell me their colours and venue?', 'Yes. The notes box covers venue, colour palette, guest numbers and favourite flowers.'),
        ('Can I set seasonal prices?', 'Yes. Change prices whenever you like from your private edit link.')]),
 dict(slug='dog-groomers', key='groomer', kind='clinic', plural='dog groomers', name='Dog groomers', people='dog owners',
  intro='Full grooms, bath and tidy, puppy intros, hand stripping, de-shedding and nails, priced by the size of dog. Owners see a guide price and request an appointment with their dog’s breed and coat in the notes.',
  faqs=[('Can owners tell me about their dog?', 'Yes. The notes box asks for name, breed, age, coat condition and anything you should know.'),
        ('What about matted coats?', 'The page explains that the final price depends on coat condition, matting and temperament, so owners aren’t surprised.')]),
 dict(slug='hair-salons', key='salon', kind='clinic', plural='hair salons', name='Hair salons', people='clients',
  intro='Cuts, balayage, highlights, roots, keratin and extensions, priced by hair length. Clients see a guide price and request an appointment, which saves your team answering the same price questions all day.',
  faqs=[('Can it price by hair length?', 'Yes. Short, medium and long or thick hair each have their own guide price. Extensions use half head, full head and premium options.'),
        ('Can clients pick a preferred date and time?', 'Yes. The request form includes a preferred date and time.')]),
 dict(slug='cake-makers', key='cakes', kind='clinic', plural='cake makers', name='Cake makers', people='customers',
  intro='Wedding cakes, celebration cakes, cupcakes, dessert tables and novelty cakes, priced by how many people they serve. Customers see a guide price and check your availability for their date.',
  faqs=[('Can customers tell me about allergies?', 'Yes. The notes box asks for guest numbers, flavours, theme and any allergies.'),
        ('Can I price cupcakes by the dozen?', 'Yes. Cupcakes are priced as 12, 24 or 48.')]),
 dict(slug='newborn-family-photographers', key='family', kind='clinic', plural='newborn and family photographers', name='Newborn & family photographers', people='parents',
  intro='Newborn, family, maternity, cake smash and mini sessions, priced by package. Parents see a guide price and check your availability, with due dates and ages in the notes.',
  faqs=[('Can parents book around a due date?', 'Yes. They can add a preferred shoot date and their baby’s due date or age in the notes.'),
        ('Can I run seasonal mini sessions?', 'Yes. Seasonal mini sessions are part of the standard menu.')]),
]

def build_niches():
    out = []
    for n in NICHES:
        if n['kind'] == 'trade':
            label, sizes, svc = TRADE_RAW[n['key']]
            jobs = [dict(name=lower_job(s[0]), r=trade_ranges(s[1]), sizes=None) for s in svc]
        else:
            label, sizes, svc = CLINIC_RAW[n['key']]
            jobs = [dict(name=j[0], r=[tuple(x) for x in j[1]], sizes=j[2]) for j in svc]
        d = dict(n); d.update(label=label, sizes=sizes, jobs=jobs)
        out.append(d)
    return out
