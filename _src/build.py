#!/usr/bin/env python3
"""Builds the AiEngineered static site into ./out. Change BASE once the custom domain is connected, then rebuild."""
import json, os, shutil, html, datetime
from data import build_niches

BASE = os.environ.get('SITE_BASE', 'https://aiengineered-hone9.vercel.app').rstrip('/')
CONTACT = 'L.hockley17121990@gmail.com'
PORTAL = 'https://billing.stripe.com/p/login/dRm3cwd5bfqIaB6cCVbAs00'
TODAY = datetime.date.today().isoformat()
OUT = 'out'
NICHES = build_niches()
TRADES = [n for n in NICHES if n['kind'] == 'trade']
CLINICS = [n for n in NICHES if n['kind'] == 'clinic']
e = lambda s: html.escape(str(s), quote=True)

def money(n): return '£{:,}'.format(n)
def rng(r): return money(r[0]) + '–' + money(r[1])

ORG = {"@type": "Organization", "@id": BASE + "/#org", "name": "AiEngineered", "url": BASE + "/",
       "logo": BASE + "/icon-512.png", "email": CONTACT,
       "description": "AiEngineered builds instant quote calculators for trades, clinics and local businesses in the UK, Ireland and the US.",
       "founder": {"@type": "Person", "name": "Liam Hockley"}, "areaServed": ["GB", "IE", "US"]}
OFFER = {"@type": "Offer", "price": "197.00", "priceCurrency": "GBP", "url": BASE + "/pricing/",
         "description": "£197 setup, then £49 a month. Cancel any time.",
         "priceSpecification": [
             {"@type": "UnitPriceSpecification", "name": "Setup", "price": "197.00", "priceCurrency": "GBP"},
             {"@type": "UnitPriceSpecification", "name": "Monthly plan", "price": "49.00", "priceCurrency": "GBP",
              "referenceQuantity": {"@type": "QuantitativeValue", "value": 1, "unitCode": "MON"}}]}

GLOBAL_FAQ = [
 ('What is an instant quote calculator?', 'A page where your customers pick a job and see a guide price straight away, instead of calling or messaging to ask. If the price suits them, they send you their name, phone, email and the job in one tap.'),
 ('How much does it cost?', '£197 to set up, then £49 a month. The monthly plan keeps your calculator online, sends every request to your inbox, and covers price changes and help. You can cancel any time.'),
 ('Can I see it before I pay?', 'Yes. Build a free preview with your business name and town and you will see exactly what your customers would see. You only pay if you switch it on.'),
 ('How does it get my prices right?', 'It starts from typical UK guide prices for your type of business, adjusted for your town. Clinics, salons and other local businesses change their own menu and prices from a private link. Trades tell us what they charge and we move the price level up or down to match, which is included in the monthly plan.'),
 ('Do I need a website?', 'No. Put your link in your Instagram bio, Google Business Profile, Facebook page, WhatsApp or a QR code on your van or flyers. If you do have a website, it goes on with one line of code, or we install it for you free.'),
 ('What happens when a customer sends a request?', 'You get an email with their name, phone number, email, the job, the guide price they saw and any notes, plus buttons to call or WhatsApp them in one tap. Pressing reply answers the customer directly.'),
 ('Do I have to get on a call?', 'No. Everything is done online and by email. If you want help, reply to any email from us.'),
 ('How do I cancel?', 'Use the “Manage my plan” link in your welcome email, which opens Stripe’s secure billing page. Your plan runs to the end of the month you have paid for, and then requests stop.'),
 ('Which countries do you cover?', 'The UK, Ireland and the US. The calculator shows prices in your customers’ currency.'),
 ('Why might I see “Brightpour Games” at checkout?', 'Payments are handled by Stripe through Liam Hockley’s existing Stripe account, which is called Brightpour Games, so you may see that name at checkout or on your bank statement. It is the same business.'),
]

NICHE_OPTIONS = ''.join([
    '<optgroup label="Trades">' + ''.join('<option value="%s" data-kind="trade">%s</option>' % (n['key'], e(n['name'])) for n in TRADES) + '</optgroup>',
    '<optgroup label="Clinics, salons and local services">' + ''.join('<option value="%s" data-kind="clinic">%s</option>' % (n['key'], e(n['name'])) for n in CLINICS) + '</optgroup>'])

MARK_SVG = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="1" y="1" width="30" height="30" rx="5" fill="#F9F35A" stroke="#16246B" stroke-width="2"/>'
            '<path d="M7 23 L12.5 9 L18 23 M9.2 18 H15.8" fill="none" stroke="#16246B" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>'
            '<path d="M22.5 13 V23 M22.5 8.6 V9.2" stroke="#16246B" stroke-width="2.6" stroke-linecap="round"/></svg>')

def ld(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'

def page(path, title, desc, body, schema=None, noindex=False, og_title=None):
    url = BASE + path
    graph = [ORG, {"@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": "AiEngineered", "publisher": {"@id": BASE + "/#org"}}]
    if schema: graph += schema
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{'<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'}
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="AiEngineered">
<meta property="og:title" content="{e(og_title or title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/og.png">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#16246B">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
{ld({"@context": "https://schema.org", "@graph": graph})}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
<a class="mark" href="/" aria-label="AiEngineered home">{MARK_SVG}<span>AiEngineered</span></a>
<nav class="nav" aria-label="Main"><a class="link" href="/instant-quote-calculator/">Calculators</a><a class="link" href="/pricing/">Pricing</a><a class="link" href="/faq/">FAQ</a><a class="btn sm" href="{'#build' if 'id="build"' in body else '/#build'}">Build my free preview</a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="foot">
<div class="wrap" style="padding:0">
<div class="title-block">
<div><h4>Business</h4><p><b>AiEngineered</b><br>Instant quote calculators for trades, clinics and local businesses.</p></div>
<div><h4>Run by</h4><p>Liam Hockley<br>United Kingdom</p></div>
<div><h4>Contact</h4><p><a href="mailto:{CONTACT}">{CONTACT}</a></p></div>
<div><h4>Pages</h4><ul><li><a href="/pricing/">Pricing</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/about/">About</a></li><li><a href="{PORTAL}">Manage my plan</a></li><li><a href="/terms/">Terms</a> and <a href="/privacy/">privacy</a></li></ul></div>
</div>
<p class="legal">AiEngineered is a trading name of Liam Hockley, a sole trader in the United Kingdom. Guide prices on calculators are estimates, not quotes.</p>
</div>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
'''

def est_data(niches, current):
    d = {"current": current, "niches": [{"key": n['key'], "kind": n['kind'], "people": n['people'], "sizes": n['sizes'],
          "jobs": [{"name": j['name'], "r": [list(x) for x in j['r']], "sizes": j['sizes']} for j in n['jobs']]} for n in niches]}
    return '<script type="application/json" id="est-data">' + json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'

def estimator(niches, current, show_select):
    n = next(x for x in niches if x['key'] == current)
    j = n['jobs'][0]; sizes = j['sizes'] or n['sizes']; r = j['r'][1]
    sel = ''
    if show_select:
        opts = NICHE_OPTIONS.replace('value="%s" ' % current, 'value="%s" selected ' % current)
        sel = f'<div class="field"><label for="est-niche">Your business</label><select id="est-niche">{opts}</select></div>'
    chips = ''.join('<button type="button" class="chip" aria-pressed="%s">%s</button>' % ('true' if i == 0 else 'false', e(x['name'])) for i, x in enumerate(n['jobs']))
    seg = ''.join('<button type="button" class="chip" aria-pressed="%s">%s</button>' % ('true' if i == 1 else 'false', e(s)) for i, s in enumerate(sizes))
    return f'''<div class="sheet" aria-label="Live guide price demo">
<div class="sheet-head"><b>Try it as a customer</b><span>Live demo</span></div>
{sel}
<div class="field"><span class="lab" id="est-jobs-l">The job</span><div class="chips" id="est-jobs" role="group" aria-labelledby="est-jobs-l">{chips}</div></div>
<div class="field"><span class="lab" id="est-sizes-l">How big</span><div class="seg" id="est-sizes" role="group" aria-labelledby="est-sizes-l">{seg}</div></div>
<div class="dim" aria-live="polite">
<div class="dim-row"><span class="dim-num" id="est-lo">{money(r[0])}</span><span class="dim-line" aria-hidden="true"><i></i><i></i></span><span class="dim-num" id="est-hi">{money(r[1])}</span></div>
<p class="dim-cap" id="est-cap">Guide price for {e(j['name'][0].lower() + j['name'][1:])}, {e(sizes[1][0].lower() + sizes[1][1:])}.</p>
</div>
<button type="button" class="btn" id="est-req">Request this quote</button>
<p class="sheet-note" id="est-note" hidden></p>
{est_data(niches, current)}
</div>'''

def build_form(preset=None, heading='Build your free preview', sub=None):
    opts = NICHE_OPTIONS
    if preset: opts = opts.replace('value="%s" ' % preset, 'value="%s" selected ' % preset)
    sub = sub or 'Type your business name and town and see your own calculator in seconds. Nothing to pay unless you switch it on.'
    return f'''<section id="build"><div class="wrap"><div class="build">
<h2>{e(heading)}</h2>
<p>{e(sub)}</p>
<form id="build-form" novalidate>
<div><label for="bf-name">Business name</label><input type="text" id="bf-name" autocomplete="organization" maxlength="60" required></div>
<div><label for="bf-city">Town or city</label><input type="text" id="bf-city" autocomplete="address-level2" maxlength="40" required></div>
<div><label for="bf-niche">What you do</label><select id="bf-niche" required><option value="">Choose one</option>{opts}</select></div>
<div><label for="bf-country">Country</label><select id="bf-country"><option value="uk">United Kingdom</option><option value="ie">Ireland</option><option value="us">United States</option></select></div>
<div class="full"><button class="btn" type="submit">Show me my calculator</button></div>
<p class="err full" id="bf-err" role="alert"></p>
</form>
<noscript><p>The preview needs JavaScript. Email <a href="mailto:{CONTACT}">{CONTACT}</a> with your business name and town and we will send you a link.</p></noscript>
</div></div></section>'''

def faq_block(items, heading='Questions'):
    rows = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in items)
    return f'<section id="faq"><div class="wrap"><h2>{e(heading)}</h2><div class="faq">{rows}</div></div></section>'

def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def crumbs_schema(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + p} for i, (n, p) in enumerate(items)]}

STEPS = '''<section id="how"><div class="wrap"><h2>How it works</h2>
<ol class="steps">
<li><h3>Build your free preview</h3><p>Type your business name, town and what you do. You see your own calculator straight away, with your services and local prices.</p></li>
<li><h3>Switch it on</h3><p>Happy with it? Pay £197 to set up, then £49 a month. Your link and website code arrive by email within a few minutes.</p></li>
<li><h3>Get requests in your inbox</h3><p>Customers pick a job, see a guide price and send their details. Each one lands in your email with buttons to call or WhatsApp them.</p></li>
</ol></div></section>'''

MAIL = '''<div class="mail" aria-label="Example of a request email">
<div class="subj">New quote request: Roof repairs (Jo Bloggs)</div>
<div class="from">From: Instant Quote Leads. Pressing reply answers Jo.</div>
<table><tr><td>Name</td><td><b>Jo Bloggs</b></td></tr><tr><td>Phone</td><td><b>07700 900123</b></td></tr><tr><td>Best way to reach</td><td><b>WhatsApp</b></td></tr><tr><td>Job</td><td><b>Roof repairs</b></td></tr><tr><td>Size and timing</td><td><b>Typical house, within 7 days</b></td></tr><tr><td>Guide price shown</td><td><b>£450–£600</b></td></tr><tr><td>Notes</td><td><b>Slipped tiles above the back bedroom</b></td></tr></table>
<div class="btns"><span>WhatsApp Jo</span><span>Call Jo</span></div>
</div>'''

PRICE_CARD = f'''<div class="price-card">
<p class="price-line"><b>£197</b><span>one-off setup</span></p>
<p class="price-line"><b>£49</b><span>a month, cancel any time</span></p>
<ul class="ticks">
<li>Your calculator, built with your business name, services and local prices</li>
<li>A link for Instagram, Google, Facebook and WhatsApp, plus one line of code for your website</li>
<li>Free installation on your website if you would rather we did it</li>
<li>Every customer request emailed to you with one-tap call and WhatsApp buttons</li>
<li>Price adjustments and help whenever you need them</li>
<li>No contract and no calls. Cancel from your billing link; it runs to the end of the month you have paid for</li>
</ul></div>'''

def biz_list(items):
    li = ''
    for n in items:
        j = n['jobs'][0] if n['kind'] == 'clinic' else min(n['jobs'], key=lambda x: x['r'][1][0])
        li += f'<li><a href="/instant-quote-calculator/{n["slug"]}/">{e(n["name"])}<span>{e(j["name"])} {rng(j["r"][1])}</span></a></li>'
    return f'<ul class="biz">{li}</ul>'

def write(path, content):
    fp = os.path.join(OUT, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(OUT, path.lstrip('/'))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w', encoding='utf-8').write(content)

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    shutil.copytree('static', OUT)
    urls = []

    # ---------- Home ----------
    body = f'''<section class="hero"><div class="wrap split">
<div>
<h1>Show customers a price before they pick up the phone.</h1>
<p class="lede">AiEngineered builds instant quote calculators for trades, clinics and local businesses. Customers pick the job, see a guide price for your area, and send their details straight to your inbox.</p>
<div class="actions"><a class="btn" href="#build">Build my free preview</a><a class="btn ghost" href="/pricing/">See pricing</a></div>
<ul class="facts"><li>No calls needed</li><li>Live the same day</li><li>£197 setup, £49 a month</li></ul>
</div>
{estimator(NICHES, 'roofer', True)}
</div></section>
{STEPS}
<section><div class="wrap split">
<div><h2>What lands in your inbox</h2>
<p>Every request arrives as an email with the customer’s details, the job they picked and the guide price they saw. Tap to call or WhatsApp them, or press reply to answer by email.</p>
<p>People who send a request have already seen a price, so you spend less time on enquiries that were never going to go ahead.</p></div>
{MAIL}
</div></section>
<section id="businesses"><div class="wrap"><h2>Built for your kind of business</h2>
<p>Each calculator comes with the jobs and price ranges that make sense for the business. You can change them.</p>
<div class="cols"><div><h3>Trades</h3>{biz_list(TRADES)}</div><div><h3>Clinics, salons and local services</h3>{biz_list(CLINICS)}</div></div>
</div></section>
<section id="pricing"><div class="wrap split"><div><h2>One plan</h2><p>£197 to set up your calculator, then £49 a month to keep it online and your requests coming in. No contract.</p><p><a href="/pricing/">Pricing in full</a></p></div>{PRICE_CARD}</div></section>
{faq_block(GLOBAL_FAQ[:6])}
{build_form()}'''
    home_schema = [{"@type": "Service", "name": "Instant quote calculator", "serviceType": "Instant quote calculator for small businesses",
                    "provider": {"@id": BASE + "/#org"}, "areaServed": ["GB", "IE", "US"], "offers": OFFER,
                    "description": "A guide-price calculator for a business’s website, Instagram bio or Google profile. Customers pick a job, see a price range for the area and send their details to the business by email."},
                   faq_schema(GLOBAL_FAQ[:6])]
    write('/', page('/', 'AiEngineered: instant quote calculators for trades and local businesses',
                    'Let customers see a guide price on your website or Instagram, then send you their details. Built for trades, clinics and local businesses. £197 setup, £49 a month.',
                    body, home_schema, og_title='Show customers a price before they pick up the phone'))
    urls.append(('/', '1.0'))

    # ---------- Calculator index ----------
    def idx_row(n):
        return f'<li><a href="/instant-quote-calculator/{n["slug"]}/">{e(n["name"])}<span>{len(n["jobs"])} jobs priced</span></a></li>'
    body = f'''<section class="hero"><div class="wrap narrow">
<p class="crumbs"><a href="/">Home</a> / Instant quote calculators</p>
<h1>Instant quote calculators</h1>
<p class="lede">A calculator for each kind of business, with the jobs your customers ask about and typical UK guide prices to start from.</p>
</div></section>
<section style="padding-top:24px"><div class="wrap"><div class="cols"><div><h2>Trades</h2><ul class="biz">{''.join(idx_row(n) for n in TRADES)}</ul></div><div><h2>Clinics, salons and local services</h2><ul class="biz">{''.join(idx_row(n) for n in CLINICS)}</ul></div></div></div></section>
{build_form()}'''
    write('/instant-quote-calculator/', page('/instant-quote-calculator/', 'Instant quote calculators for every kind of business | AiEngineered',
          'Instant quote calculators for roofers, plumbers, electricians, builders, aesthetics clinics, salons, groomers, photographers and more.', body,
          [crumbs_schema([('Home', '/'), ('Instant quote calculators', '/instant-quote-calculator/')]),
           {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": BASE + '/instant-quote-calculator/' + n['slug'] + '/', "name": 'Instant quote calculator for ' + n['plural']} for i, n in enumerate(NICHES)]}]))
    urls.append(('/instant-quote-calculator/', '0.9'))

    # ---------- Niche pages ----------
    for n in NICHES:
        path = '/instant-quote-calculator/%s/' % n['slug']
        rows = ''.join(f'<tr><td>{e(j["name"])}</td><td>{rng(j["r"][1])}</td></tr>' for j in n['jobs'])
        sizes_note = n['sizes'][1]
        if n['kind'] == 'trade':
            gets = ['Six common jobs for your trade; tell us any you don’t do and we will hide them',
                    'Guide prices adjusted for your town, with a separate line for emergency call-outs where it applies',
                    'A request form that emails you the customer’s details, the job and the price they saw',
                    'One line of code for your website, or free installation; a link for Facebook and Google',
                    'Price level matched to what you charge, included in the monthly plan']
        else:
            gets = ['A booking page with your treatments or services, ready for your Instagram bio and website',
                    'A private edit link to change your menu, options and prices whenever you like',
                    'Guide prices in your clients’ currency, with your own wording about final prices',
                    'Requests emailed to you with the client’s preferred way to be contacted and one-tap WhatsApp',
                    'One line of code for your website, or free installation']
        faqs = n['faqs'] + [GLOBAL_FAQ[1], GLOBAL_FAQ[4], GLOBAL_FAQ[7]]
        others = [x for x in (TRADES if n['kind'] == 'trade' else CLINICS) if x['slug'] != n['slug']][:6]
        body = f'''<section class="hero"><div class="wrap">
<p class="crumbs"><a href="/">Home</a> / <a href="/instant-quote-calculator/">Instant quote calculators</a> / {e(n["name"])}</p>
<div class="split">
<div>
<h1>Instant quote calculator for {e(n["plural"])}</h1>
<p class="lede">{e(n["intro"])}</p>
<div class="actions"><a class="btn" href="#build">Build my free preview</a><a class="btn ghost" href="#jobs">See the jobs it prices</a></div>
<ul class="facts"><li>No calls needed</li><li>Live the same day</li><li>£197 setup, £49 a month</li></ul>
</div>
{estimator([n], n['key'], False)}
</div></div></section>
<section id="jobs"><div class="wrap split">
<div><h2>Jobs it prices</h2>
<p>These are the starting guide prices your calculator uses before they are matched to your prices. Ranges shown for the middle option ({e(sizes_note[0].lower() + sizes_note[1:])}); your customers can switch size and see the price change.</p>
<table class="jobs"><thead><tr><th scope="col">Job</th><th scope="col">Typical guide range</th></tr></thead><tbody>{rows}</tbody></table>
<p class="small">Typical UK prices for {e(n["plural"])}. Guide prices are estimates, not quotes, and your customers see that clearly.</p></div>
<div><h2>What you get</h2><ul class="ticks">{''.join('<li>%s</li>' % e(g) for g in gets)}</ul>
<p style="margin-top:22px"><a href="/pricing/">£197 setup, then £49 a month</a>. Cancel any time.</p></div>
</div></section>
{STEPS}
{faq_block(faqs, 'Questions from ' + n['plural'])}
<section><div class="wrap"><h2>Also built for</h2><div class="cols"><div>{biz_list(others[:3])}</div><div>{biz_list(others[3:6])}</div></div></div></section>
{build_form(n['key'], 'Build your free preview', 'Type your business name and town to see the calculator your ' + n['people'] + ' would use. Nothing to pay unless you switch it on.')}'''
        schema = [crumbs_schema([('Home', '/'), ('Instant quote calculators', '/instant-quote-calculator/'), (n['name'], path)]),
                  {"@type": "Service", "name": "Instant quote calculator for " + n['plural'], "serviceType": "Instant quote calculator",
                   "audience": {"@type": "BusinessAudience", "name": n['name']}, "provider": {"@id": BASE + "/#org"},
                   "areaServed": ["GB", "IE", "US"], "offers": OFFER, "description": n['intro']},
                  faq_schema(faqs)]
        first_jobs = ', '.join(j['name'].lower() if not j['name'][:2].isupper() else j['name'] for j in n['jobs'][:3])
        desc = f'An instant quote calculator for {n["plural"]}: {n["people"]} see a guide price for {first_jobs} and more, then send you their details. £197 setup, £49 a month.'
        write(path, page(path, f'Instant quote calculator for {n["plural"]} | AiEngineered', desc, body, schema))
        urls.append((path, '0.8'))

    # ---------- Pricing ----------
    pfaq = [GLOBAL_FAQ[1], GLOBAL_FAQ[2], GLOBAL_FAQ[7], GLOBAL_FAQ[9],
            ('Is there a contract?', 'No. Pay monthly and cancel whenever you like.'),
            ('Is the setup fee refundable?', 'The £197 setup covers building and delivering your calculator, so it is not refundable once your calculator has been delivered. If something is wrong with it, reply to your welcome email and we will put it right.')]
    body = f'''<section class="hero"><div class="wrap split">
<div><p class="crumbs"><a href="/">Home</a> / Pricing</p>
<h1>£197 to set up. £49 a month.</h1>
<p class="lede">One plan for every business. The setup fee covers building your calculator; the monthly plan keeps it online and sends you every request.</p>
<div class="actions"><a class="btn" href="#build">Build my free preview</a></div></div>
{PRICE_CARD}
</div></section>
{faq_block(pfaq, 'Pricing questions')}
{build_form()}'''
    write('/pricing/', page('/pricing/', 'Pricing: £197 setup, £49 a month | AiEngineered', 'AiEngineered instant quote calculators cost £197 to set up and £49 a month. No contract, cancel any time.', body,
          [crumbs_schema([('Home', '/'), ('Pricing', '/pricing/')]), {"@type": "Service", "name": "Instant quote calculator", "provider": {"@id": BASE + "/#org"}, "offers": OFFER}, faq_schema(pfaq)]))
    urls.append(('/pricing/', '0.9'))

    # ---------- FAQ ----------
    body = f'''<section class="hero"><div class="wrap narrow"><p class="crumbs"><a href="/">Home</a> / FAQ</p><h1>Questions and answers</h1>
<p class="lede">Anything not covered here, email <a href="mailto:{CONTACT}">{CONTACT}</a>.</p></div></section>
{faq_block(GLOBAL_FAQ, 'All questions')}
{build_form()}'''
    write('/faq/', page('/faq/', 'Questions about instant quote calculators | AiEngineered', 'What an instant quote calculator is, what it costs, how prices are set, where requests go and how to cancel.', body,
          [crumbs_schema([('Home', '/'), ('FAQ', '/faq/')]), faq_schema(GLOBAL_FAQ)]))
    urls.append(('/faq/', '0.7'))

    # ---------- About ----------
    body = f'''<section class="hero"><div class="wrap narrow prose"><p class="crumbs"><a href="/">Home</a> / About</p>
<h1>About AiEngineered</h1>
<p class="lede">AiEngineered is a small UK business run by Liam Hockley. It builds instant quote calculators for trades, clinics, salons and other local businesses.</p>
<p>The idea is simple. Most people want a rough price before they call anyone, and most small businesses don’t have time to answer “how much?” all day. A calculator answers it straight away and sends you the people who are happy with the price.</p>
<p>AiEngineered is new, so you won’t find a wall of reviews here yet. You can see exactly what you would get before paying anything: build a free preview with your business name and town.</p>
<h2>How to get in touch</h2>
<p>Email <a href="mailto:{CONTACT}">{CONTACT}</a>. Everything is handled by email, so there is no need to book a call.</p>
<h2>The business</h2>
<p>AiEngineered is a trading name of Liam Hockley, a sole trader in the United Kingdom. Payments are taken by Stripe.</p>
</div></section>
{build_form()}'''
    write('/about/', page('/about/', 'About AiEngineered', 'AiEngineered is a small UK business run by Liam Hockley, building instant quote calculators for trades, clinics and local businesses.', body,
          [crumbs_schema([('Home', '/'), ('About', '/about/')]), {"@type": "AboutPage", "url": BASE + "/about/", "about": {"@id": BASE + "/#org"}}]))
    urls.append(('/about/', '0.5'))

    # ---------- Terms ----------
    terms = f'''<section class="hero"><div class="wrap narrow prose"><p class="crumbs"><a href="/">Home</a> / Terms</p>
<h1>Terms of service</h1><p class="small">Last updated {datetime.date.today().strftime('%-d %B %Y')}</p>
<p>These terms cover AiEngineered instant quote calculators. AiEngineered is a trading name of Liam Hockley, a sole trader in the United Kingdom (“we”, “us”). By paying for a calculator you agree to these terms. Our service is for businesses, not consumers.</p>
<h2>What you get</h2>
<ul><li>A calculator page set up with your business name, services and guide prices.</li><li>A link you can share, and code to add it to your website. We will install it for you free if you ask.</li><li>Customer requests sent from the calculator emailed to the address you give us.</li><li>Price and service changes on request, and help by email.</li></ul>
<h2>Price and payment</h2>
<ul><li>Setup costs £197, paid once at checkout.</li><li>The monthly plan costs £49 a month, paid in advance by card through Stripe, starting on the day you buy.</li><li>We will give you at least 30 days’ notice by email before changing the monthly price.</li></ul>
<h2>Cancelling</h2>
<ul><li>You can cancel at any time from the “Manage my plan” link in your welcome email, or by emailing us.</li><li>Your plan stays active until the end of the month you have paid for, then requests stop being sent and your calculator shows that you are not taking online requests.</li><li>We don’t refund part months. The setup fee is not refundable once your calculator has been delivered. If something is wrong with it, tell us and we will fix it.</li><li>If a monthly payment fails and is not paid after Stripe’s retries, your plan ends in the same way.</li></ul>
<h2>Guide prices</h2>
<p>Prices on your calculator are guide estimates. You are responsible for the prices and wording shown to your customers, for checking they are suitable for your business, and for replying to the requests you receive. Your customers are told that prices are guides and that you confirm the final price.</p>
<h2>Your customers’ details</h2>
<p>When your customers send a request, we pass their details to you by email. You are responsible for how you use them. Our <a href="/privacy/">privacy notice</a> explains what we keep.</p>
<h2>Availability</h2>
<p>We work to keep calculators online and requests flowing, but we can’t promise the service will never be interrupted. If a request can’t be sent, your customer is shown a way to email you directly where possible.</p>
<h2>Liability</h2>
<p>Nothing in these terms limits liability that can’t be limited by law. Otherwise, our total liability to you is limited to the amount you have paid us in the three months before the claim, and we are not liable for lost profits or lost business.</p>
<h2>Changes and law</h2>
<p>We may update these terms and will email you about important changes. These terms are governed by the law of England and Wales.</p>
<h2>Contact</h2><p><a href="mailto:{CONTACT}">{CONTACT}</a></p>
</div></section>'''
    write('/terms/', page('/terms/', 'Terms of service | AiEngineered', 'Terms for AiEngineered instant quote calculators: what you get, price, payment, cancelling and guide prices.', terms))
    urls.append(('/terms/', '0.3'))

    privacy = f'''<section class="hero"><div class="wrap narrow prose"><p class="crumbs"><a href="/">Home</a> / Privacy</p>
<h1>Privacy notice</h1><p class="small">Last updated {datetime.date.today().strftime('%-d %B %Y')}</p>
<p>This notice explains how AiEngineered (a trading name of Liam Hockley, a sole trader in the United Kingdom) handles personal information. Contact: <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
<h2>Businesses that buy a calculator</h2>
<p>We keep your name, email address, business name, town and the details on your calculator, so we can set it up, send you requests and help you. Card payments are handled by Stripe; we don’t see your full card details. We keep this while you are a customer and for up to six years afterwards for our accounts.</p>
<h2>People who send a request through a calculator</h2>
<p>When you send a request, your name, phone number, email, the job you picked and any notes are emailed to the business whose calculator you used. That business decides how to use them, so please check their privacy information too. We keep a copy of each request email so we can check it was delivered and help if something goes wrong. Ask us to delete it at any time.</p>
<h2>Visitors to this website</h2>
<p>This website doesn’t use advertising or tracking cookies. Our hosting provider keeps basic technical logs for security.</p>
<h2>Who we share information with</h2>
<p>Only the services we need to run AiEngineered: Stripe (payments), Vercel (hosting), n8n (sending requests) and Google (email). Some of these may process information outside the UK under appropriate safeguards.</p>
<h2>Your rights</h2>
<p>You can ask to see, correct or delete the information we hold about you by emailing us. If you are unhappy with how we handle your information, you can complain to the Information Commissioner’s Office (ico.org.uk).</p>
</div></section>'''
    write('/privacy/', page('/privacy/', 'Privacy notice | AiEngineered', 'How AiEngineered handles personal information for businesses, their customers and website visitors.', privacy))
    urls.append(('/privacy/', '0.3'))

    thanks = f'''<section class="hero"><div class="wrap narrow prose">
<h1>Payment received. Thank you.</h1>
<p class="lede">Your calculator link and website code are on their way to your email now. They usually arrive within a few minutes.</p>
<ul><li>Check your spam or promotions folder if you can’t see it.</li><li>Want it on your website? Reply to that email with your website platform and we will install it for you.</li><li>Nothing after 15 minutes? Email <a href="mailto:{CONTACT}">{CONTACT}</a>.</li></ul>
<p>You can manage or cancel your plan any time from <a href="{PORTAL}">your billing page</a>.</p>
</div></section>'''
    write('/thanks/', page('/thanks/', 'Thank you | AiEngineered', 'Your calculator is on its way.', thanks, noindex=True))

    notfound = '''<section class="hero"><div class="wrap narrow"><h1>That page isn’t here.</h1>
<p class="lede">Try the <a href="/">home page</a> or see <a href="/instant-quote-calculator/">all calculators</a>.</p></div></section>'''
    open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(page('/404', 'Page not found | AiEngineered', 'Page not found.', notfound, noindex=True))

    # ---------- robots, sitemap, llms.txt ----------
    open(os.path.join(OUT, 'robots.txt'), 'w').write(
        'User-agent: *\nAllow: /\nDisallow: /thanks/\n\n'
        '# AI search and assistant crawlers are welcome\nUser-agent: GPTBot\nAllow: /\n\nUser-agent: OAI-SearchBot\nAllow: /\n\nUser-agent: ChatGPT-User\nAllow: /\n\n'
        'User-agent: ClaudeBot\nAllow: /\n\nUser-agent: Claude-SearchBot\nAllow: /\n\nUser-agent: PerplexityBot\nAllow: /\n\nUser-agent: Google-Extended\nAllow: /\n\nUser-agent: Bingbot\nAllow: /\n\n'
        f'Sitemap: {BASE}/sitemap.xml\n')
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{BASE}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n' for p, pr in urls) + '</urlset>\n'
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(sm)
    llms = [f'# AiEngineered', '',
            '> AiEngineered builds instant quote calculators for trades, clinics, salons and other local businesses in the UK, Ireland and the US. Customers pick a job, see a guide price for the area, and send their details to the business by email. Price: £197 setup, then £49 a month, cancel any time. Run by Liam Hockley, a sole trader in the United Kingdom.', '',
            '## How it works', '- A business builds a free preview with its name, town and type of business.',
            '- If they like it, they pay £197 setup plus £49 a month through Stripe and receive their calculator link and website code by email within minutes.',
            '- Their customers choose a job and size, see a guide price range, and send a request. The request is emailed to the business with one-tap call and WhatsApp buttons.',
            '- Clinics, salons and similar businesses edit their own prices from a private link; trades send their rates and AiEngineered updates them.',
            '- Cancelling is self-serve through Stripe; the plan runs to the end of the paid month, then requests stop.', '',
            '## Key pages', f'- [Home]({BASE}/)', f'- [Pricing]({BASE}/pricing/): £197 setup, £49 a month', f'- [FAQ]({BASE}/faq/)', f'- [All calculators]({BASE}/instant-quote-calculator/)', '',
            '## Calculators by business type']
    for n in NICHES:
        llms.append(f'- [Instant quote calculator for {n["plural"]}]({BASE}/instant-quote-calculator/{n["slug"]}/): ' + ', '.join(j['name'] for j in n['jobs']))
    llms += ['', '## Contact', f'- Email: {CONTACT}', '- No calls needed; everything is handled online and by email.', '']
    open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf-8').write('\n'.join(llms))
    open(os.path.join(OUT, 'vercel.json'), 'w').write(json.dumps({
        "cleanUrls": True, "trailingSlash": True,
        "headers": [{"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=86400"}]},
                    {"source": "/(.*)", "headers": [{"key": "X-Content-Type-Options", "value": "nosniff"}, {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"}]}],
        "redirects": [{"source": "/_src/:path*", "destination": "/", "permanent": False}]}, indent=1))
    print('built', len(urls), 'indexable pages into', OUT)

if __name__ == '__main__':
    build()
