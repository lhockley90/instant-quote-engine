#!/usr/bin/env python3
"""Builds the AiEngineered static site into ./out (served by Vercel from the 'website' branch)."""
import json, os, shutil, html, datetime
from data import build_niches
from guides import GUIDES

BASE = os.environ.get('SITE_BASE', 'https://aiengineered.co.uk').rstrip('/')
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL', '')   # shown once hello@aiengineered.co.uk forwards to Liam's inbox
PORTAL = 'https://billing.stripe.com/p/login/dRm3cwd5bfqIaB6cCVbAs00'
INDEXNOW_KEY = '7f3c9a1e5b8d4c2fa6e1d0b9c8a7f6e5'
TODAY = datetime.date.today().isoformat()
TODAY_LONG = datetime.date.today().strftime('%-d %B %Y')
OUT = 'out'
NICHES = build_niches()
TRADES = [n for n in NICHES if n['kind'] == 'trade']
CLINICS = [n for n in NICHES if n['kind'] == 'clinic']
e = lambda s: html.escape(str(s), quote=True)
def money(n): return '£{:,}'.format(n)
def rng(r): return money(r[0]) + '–' + money(r[1])
CONTACT_LINE = (f'<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>' if CONTACT_EMAIL else '<a href="/contact/">our contact form</a>')

ICONS = {
 'lock': '<rect x="4.5" y="10.5" width="15" height="10" rx="2.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>',
 'cycle': '<path d="M4 12a8 8 0 0 1 13.7-5.6L20 8.5"/><path d="M20 4v4.5h-4.5"/><path d="M20 12a8 8 0 0 1-13.7 5.6L4 15.5"/><path d="M4 20v-4.5h4.5"/>',
 'chat': '<path d="M20 12a8 8 0 0 1-11.5 7.2L4 20l.9-4.2A8 8 0 1 1 20 12z"/>',
 'bolt': '<path d="M13 2.5 4.5 13.5H11l-1 8 8.5-11H12z"/>',
 'check': '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
 'chev': '<path d="m9 6 6 6-6 6"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m4 7 8 6 8-6"/>',
 'pin': '<path d="M12 21s7-6.2 7-11.5a7 7 0 0 0-14 0C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
}
def icon(n): return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{ICONS[n]}</svg>'
MARK = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="9" fill="#3E6FF6"/>'
        '<rect x=".5" y=".5" width="31" height="31" rx="8.5" fill="none" stroke="#ffffff" stroke-opacity=".18"/>'
        '<path d="M9.5 10.5v11M22.5 10.5v11" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>'
        '<path d="M13 16h6" stroke="#34E3A4" stroke-width="2.6" stroke-linecap="round"/></svg>')

ORG = {"@type": "Organization", "@id": BASE + "/#org", "name": "AiEngineered", "url": BASE + "/", "logo": BASE + "/icon-512.png",
       "description": "AiEngineered builds instant quote calculators for trades, clinics and local businesses in the UK, Ireland and the US.",
       "founder": {"@type": "Person", "name": "Liam Hockley"}, "areaServed": ["GB", "IE", "US"],
       "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "url": BASE + "/contact/", "availableLanguage": "en"}}
if CONTACT_EMAIL: ORG["email"] = CONTACT_EMAIL
OFFER = {"@type": "Offer", "price": "197.00", "priceCurrency": "GBP", "url": BASE + "/pricing/", "availability": "https://schema.org/InStock",
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
 ('Do I have to get on a call?', 'No. Everything is done online and by email. If you want help, reply to any email from us or use the contact form.'),
 ('How do I cancel?', 'Use the “Manage my plan” link in your welcome email, which opens Stripe’s secure billing page. Your plan runs to the end of the month you have paid for, and then requests stop.'),
 ('Which countries do you cover?', 'The UK, Ireland and the US. The calculator shows prices in your customers’ currency, and our terms follow the law where your business is based.'),
 ('Is my payment secure?', 'Yes. Payments are taken by Stripe, which handles card details on its own secure checkout. AiEngineered never sees your full card number.'),
]

def niche_options(selected=None):
    def opt(n, kind): return '<option value="%s" data-kind="%s"%s>%s</option>' % (n['key'], kind, ' selected' if n['key'] == selected else '', e(n['name']))
    return ('<optgroup label="Trades">' + ''.join(opt(n, 'trade') for n in TRADES) + '</optgroup>' +
            '<optgroup label="Clinics, salons and local services">' + ''.join(opt(n, 'clinic') for n in CLINICS) + '</optgroup>')

def ld(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'

def page(path, title, desc, body, schema=None, noindex=False, og_title=None):
    url = BASE + path
    graph = [ORG, {"@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": "AiEngineered", "inLanguage": "en-GB", "publisher": {"@id": BASE + "/#org"}}]
    if schema: graph += schema
    cta_href = '#build' if 'id="build"' in body else '/#build'
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{'noindex' if noindex else 'index, follow, max-image-preview:large, max-snippet:-1'}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="AiEngineered">
<meta property="og:title" content="{e(og_title or title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/og.png">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#070C1E">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600&family=Sora:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v=2">
{ld({"@context": "https://schema.org", "@graph": graph})}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
<a class="brand" href="/" aria-label="AiEngineered home">{MARK}<span>AiEngineered</span></a>
<nav class="nav" aria-label="Main"><a class="link" href="/instant-quote-calculator/">Calculators</a><a class="link" href="/pricing/">Pricing</a><a class="link" href="/guides/">Guides</a><a class="link" href="/faq/">FAQ</a><a class="btn sm" href="{cta_href}">Get started</a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap">
<div class="foot-grid">
<div><a class="brand" href="/">{MARK}<span>AiEngineered</span></a><p style="margin-top:14px">Instant quote calculators for trades, clinics and local businesses in the UK, Ireland and the US.</p><p class="secure" style="color:inherit">{icon('lock')}Secure checkout by Stripe</p></div>
<div><h4>Product</h4><ul><li><a href="/instant-quote-calculator/">Calculators</a></li><li><a href="/pricing/">Pricing</a></li><li><a href="/guides/">Guides</a></li><li><a href="/faq/">FAQ</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="/about/">About</a></li><li><a href="/contact/">Contact</a></li><li><a href="{PORTAL}">Manage my plan</a></li></ul></div>
<div><h4>Legal</h4><ul><li><a href="/terms/">Terms of service</a></li><li><a href="/privacy/">Privacy notice</a></li></ul></div>
</div>
<p class="legal">© {datetime.date.today().year} AiEngineered, a trading name of Liam Hockley, sole trader, United Kingdom. Prices on calculators are guide estimates, not quotes.</p>
</div></footer>
<script src="/assets/site.js?v=2" defer></script>
</body>
</html>
'''

def est_data(niches, current):
    d = {"current": current, "niches": [{"key": n['key'], "kind": n['kind'], "people": n['people'], "sizes": n['sizes'],
          "jobs": [{"name": j['name'], "r": [list(x) for x in j['r']], "sizes": j['sizes']} for j in n['jobs']]} for n in niches]}
    return '<script type="application/json" id="est-data">' + json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'

def app_panel(niches, current, show_select, title='Your instant quote page'):
    n = next(x for x in niches if x['key'] == current)
    j = n['jobs'][0]; sizes = j['sizes'] or n['sizes']; r = j['r'][1]
    mn, mx = j['r'][0][0], j['r'][2][1]; span = max(1, mx - mn)
    left = (r[0] - mn) / span * 100; width = max(4, (r[1] - r[0]) / span * 100)
    sel = f'<div class="f"><label for="est-niche">Business type</label><select id="est-niche">{niche_options(current)}</select></div>' if show_select else ''
    chips = ''.join('<button type="button" class="chip" aria-pressed="%s">%s</button>' % ('true' if i == 0 else 'false', e(x['name'])) for i, x in enumerate(n['jobs']))
    seg = ''.join('<button type="button" class="chip" aria-pressed="%s">%s</button>' % ('true' if i == 1 else 'false', e(s)) for i, s in enumerate(sizes))
    return f'''<div class="app" aria-label="Live guide price demo">
<div class="app-head"><b>{e(title)}</b><span class="live">Live demo</span></div>
{sel}
<div class="f"><span class="lab" id="est-jobs-l">Choose the job</span><div class="chips" id="est-jobs" role="group" aria-labelledby="est-jobs-l">{chips}</div></div>
<div class="f" style="margin-bottom:0"><span class="lab" id="est-sizes-l">How big is it?</span><div class="seg" id="est-sizes" role="group" aria-labelledby="est-sizes-l">{seg}</div></div>
<div class="readout" aria-live="polite">
<span class="lab">Guide price</span>
<div class="nums"><span id="est-lo">{money(r[0])}</span><span class="to">to</span><span id="est-hi">{money(r[1])}</span></div>
<div class="bar" aria-hidden="true"><i id="est-fill" style="left:{left:.1f}%;width:{width:.1f}%"></i></div>
<div class="scale" aria-hidden="true"><span id="est-min">{money(mn)}</span><span id="est-max">{money(mx)}</span></div>
<p class="cap" id="est-cap">{e(j['name'])}, {e(sizes[1][0].lower() + sizes[1][1:])}.</p>
</div>
<button type="button" class="btn" id="est-req">Request this quote</button>
<p class="app-note" id="est-note" hidden></p>
{est_data(niches, current)}
</div>'''

TRUST = f'<ul class="trust"><li>{icon("lock")}Secure checkout by Stripe</li><li>{icon("cycle")}Cancel any time</li><li>{icon("chat")}No calls needed</li></ul>'
FACTS = f'''<div class="facts"><div class="wrap"><ul>
<li>{icon('bolt')}<div><b>Live the same day</b>Your link and website code arrive by email in minutes.</div></li>
<li>{icon('mail')}<div><b>Requests to your inbox</b>With one-tap call and WhatsApp buttons.</div></li>
<li>{icon('lock')}<div><b>Secure payments</b>Card details are handled by Stripe.</div></li>
<li>{icon('cycle')}<div><b>No contract</b>£49 a month, cancel whenever you like.</div></li>
</ul></div></div>'''

def build_section(preset=None, heading='See your own calculator in seconds', sub=None):
    sub = sub or 'Type your business name and town to build a free preview with your services and local prices. Nothing to pay unless you switch it on.'
    return f'''<section class="sec cta" id="build"><div class="wrap box">
<div><h2>{e(heading)}</h2><p style="margin-top:14px">{e(sub)}</p>{TRUST}</div>
<form class="form" id="build-form" novalidate>
<div><label for="bf-name">Business name</label><input type="text" id="bf-name" autocomplete="organization" maxlength="60" required></div>
<div><label for="bf-city">Town or city</label><input type="text" id="bf-city" autocomplete="address-level2" maxlength="40" required></div>
<div><label for="bf-niche">What you do</label><select id="bf-niche" required><option value="">Choose one</option>{niche_options(preset)}</select></div>
<div><label for="bf-country">Country</label><select id="bf-country"><option value="uk">United Kingdom</option><option value="ie">Ireland</option><option value="us">United States</option></select></div>
<div class="full"><button class="btn" type="submit">Build my free preview</button></div>
<p class="err full" id="bf-err" role="alert"></p>
</form>
<noscript><p>The preview needs JavaScript. Use the <a href="/contact/">contact form</a> and we will send you a link.</p></noscript>
</div></section>'''

def faq_block(items, heading='Questions, answered', light=True):
    rows = ''.join(f'<details><summary>{e(q)}<i aria-hidden="true"></i></summary><p>{e(a)}</p></details>' for q, a in items)
    return f'<section class="sec" id="faq"><div class="wrap"><div class="sec-head"><h2>{e(heading)}</h2></div><div class="faq">{rows}</div></div></section>'
def faq_schema(items): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
def crumbs_schema(items): return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + p} for i, (n, p) in enumerate(items)]}

STEPS = '''<section class="sec" id="how"><div class="wrap">
<div class="sec-head"><h2>How it works</h2><p>From preview to live in one sitting. No calls, no meetings.</p></div>
<ol class="steps">
<li><h3>Build your free preview</h3><p>Type your business name, town and what you do. You see your own calculator straight away, with your services and local prices.</p></li>
<li><h3>Switch it on</h3><p>Happy with it? Pay £197 to set up, then £49 a month. Your link and website code arrive by email within minutes.</p></li>
<li><h3>Get requests in your inbox</h3><p>Customers pick a job, see a guide price and send their details. Each one arrives with buttons to call or WhatsApp them.</p></li>
</ol></div></section>'''

MAIL = f'''<div class="mail" aria-label="Example request email">
<div class="mail-top"><div class="av">IQ</div><div><b>Instant Quote Leads</b><span>New quote request</span></div></div>
<div class="mail-body"><h3>Jo Bloggs would like a quote for: Roof repairs</h3>
<table><tr><td>Phone</td><td>07700 900123</td></tr><tr><td>Best way to reach</td><td>WhatsApp</td></tr><tr><td>Size and timing</td><td>Typical house, within 7 days</td></tr><tr><td>Guide price shown</td><td>£450–£600</td></tr><tr><td>Notes</td><td>Slipped tiles above the back bedroom</td></tr></table>
<div class="btns"><span>WhatsApp Jo</span><span>Call Jo</span></div></div>
</div>'''

PLAN = f'''<div class="plan">
<div class="plan-price"><div><b>£197</b><span>one-off setup</span></div><div><b>£49</b><span>per month</span></div></div>
<ul class="ticks">
<li>{icon('check')}<span>Your calculator, built with your business name, services and local prices</span></li>
<li>{icon('check')}<span>A link for Instagram, Google and Facebook, plus one line of code for your website</span></li>
<li>{icon('check')}<span>Free installation on your website if you would rather we did it</span></li>
<li>{icon('check')}<span>Every customer request emailed to you, with one-tap call and WhatsApp</span></li>
<li>{icon('check')}<span>Price adjustments and help by email whenever you need them</span></li>
<li>{icon('check')}<span>No contract. Cancel from your billing link; it runs to the end of the month you have paid for</span></li>
</ul>
<p class="secure">{icon('lock')}Secure checkout by Stripe. Prices in GBP.</p>
</div>'''

def biz_list(items):
    li = ''
    for n in items:
        j = n['jobs'][0] if n['kind'] == 'clinic' else min(n['jobs'], key=lambda x: x['r'][1][0])
        li += f'<li><a href="/instant-quote-calculator/{n["slug"]}/"><b style="font-weight:550">{e(n["name"])}</b><span>{e(j["name"])} {rng(j["r"][1])}</span>{icon("chev")}</a></li>'
    return f'<ul class="biz">{li}</ul>'

def guide_cards(items):
    return '<div class="guides">' + ''.join(f'<a class="guide" href="/guides/{g["slug"]}/"><h3>{e(g["title"])}</h3><p>{e(g["summary"])}</p><span>Read the guide</span></a>' for g in items) + '</div>'

def write(path, content):
    fp = os.path.join(OUT, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(OUT, path.lstrip('/'))
    os.makedirs(os.path.dirname(fp) or OUT, exist_ok=True)
    open(fp, 'w', encoding='utf-8').write(content)

def dark_head(crumbs, h1, lede, extra=''):
    c = ' / '.join(f'<a href="{p}">{e(n)}</a>' if p else e(n) for n, p in crumbs)
    return f'<section class="hero"><div class="wrap narrow"><p class="crumbs">{c}</p><h1>{e(h1)}</h1><p class="lede">{lede}</p>{extra}</div></section>'

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    shutil.copytree('static', OUT)
    open(os.path.join(OUT, INDEXNOW_KEY + '.txt'), 'w').write(INDEXNOW_KEY)
    urls = []

    # ---------- Home ----------
    body = f'''<section class="hero"><div class="wrap split">
<div>
<h1>Show customers a price before they pick up the phone.</h1>
<p class="lede">AiEngineered builds instant quote calculators for trades, clinics and local businesses. Customers pick the job, see a guide price for your area, and send their details straight to your inbox.</p>
<div class="actions"><a class="btn" href="#build">Build my free preview</a><a class="btn ghost" href="#how">See how it works</a></div>
{TRUST}
</div>
{app_panel(NICHES, 'roofer', True)}
</div></section>
{FACTS}
{STEPS}
<section class="sec"><div class="wrap split">
<div><h2>Every request, ready to answer</h2>
<p class="muted" style="margin-top:14px">Requests arrive as an email with the customer’s details, the job they picked and the guide price they saw. Tap to call or WhatsApp them, or press reply to answer by email.</p>
<p class="muted">People who send a request have already seen a price, so you spend less time on enquiries that were never going to go ahead.</p></div>
{MAIL}
</div></section>
<section class="sec" id="businesses"><div class="wrap">
<div class="sec-head"><h2>Built for your kind of business</h2><p>Each calculator comes with the jobs and price ranges that make sense for the business, ready to adjust to yours.</p></div>
<div class="cols"><div><h3>Trades</h3>{biz_list(TRADES)}</div><div><h3>Clinics, salons and local services</h3>{biz_list(CLINICS)}</div></div>
</div></section>
<section class="sec" id="pricing"><div class="wrap split">
<div><h2>One simple plan</h2><p class="muted" style="margin-top:14px">£197 to set up your calculator, then £49 a month to keep it online and your requests coming in. No contract and no calls.</p><p><a href="/pricing/">Pricing in full</a></p></div>
{PLAN}
</div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><h2>Guides</h2><p>Straight answers to the questions business owners ask about pricing online.</p></div>{guide_cards(GUIDES)}</div></section>
{faq_block(GLOBAL_FAQ[:6])}
{build_section()}'''
    home_schema = [{"@type": "Service", "name": "Instant quote calculator", "serviceType": "Instant quote calculator for small businesses",
                    "provider": {"@id": BASE + "/#org"}, "areaServed": ["GB", "IE", "US"], "offers": OFFER,
                    "description": "A guide-price calculator for a business’s website, Instagram bio or Google profile. Customers pick a job, see a price range for the area and send their details to the business by email."},
                   faq_schema(GLOBAL_FAQ[:6])]
    write('/', page('/', 'Instant quote calculators for trades and local businesses | AiEngineered',
                    'Let customers see a guide price on your website or Instagram, then send you their details. Built for trades, clinics and local businesses. £197 setup, £49 a month.',
                    body, home_schema, og_title='Show customers a price before they pick up the phone'))
    urls.append(('/', '1.0'))

    # ---------- Calculator index ----------
    def idx_row(n): return f'<li><a href="/instant-quote-calculator/{n["slug"]}/"><b style="font-weight:550">{e(n["name"])}</b><span>{len(n["jobs"])} jobs priced</span>{icon("chev")}</a></li>'
    body = dark_head([('Home', '/'), ('Calculators', '')], 'Instant quote calculators', 'A calculator for each kind of business, with the jobs your customers ask about and typical UK guide prices to start from.') + f'''
<section class="sec"><div class="wrap"><div class="cols"><div><h3>Trades</h3><ul class="biz">{''.join(idx_row(n) for n in TRADES)}</ul></div><div><h3>Clinics, salons and local services</h3><ul class="biz">{''.join(idx_row(n) for n in CLINICS)}</ul></div></div></div></section>
{build_section()}'''
    write('/instant-quote-calculator/', page('/instant-quote-calculator/', 'Instant quote calculators for every kind of business | AiEngineered',
          'Instant quote calculators for roofers, plumbers, electricians, builders, aesthetics clinics, salons, groomers, photographers and more.', body,
          [crumbs_schema([('Home', '/'), ('Instant quote calculators', '/instant-quote-calculator/')]),
           {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": BASE + '/instant-quote-calculator/' + n['slug'] + '/', "name": 'Instant quote calculator for ' + n['plural']} for i, n in enumerate(NICHES)]}]))
    urls.append(('/instant-quote-calculator/', '0.9'))

    # ---------- Niche pages ----------
    for n in NICHES:
        path = '/instant-quote-calculator/%s/' % n['slug']
        rows = ''.join(f'<tr><td>{e(j["name"])}</td><td>{rng(j["r"][1])}</td></tr>' for j in n['jobs'])
        mid = n['sizes'][1]
        if n['kind'] == 'trade':
            gets = ['Six common jobs for your trade; tell us any you don’t do and we will hide them',
                    'Guide prices adjusted for your town, with a separate line for emergency call-outs where it applies',
                    'A request form that emails you the customer’s details, the job and the price they saw',
                    'One line of code for your website, or free installation; a link for Facebook and Google',
                    'Price level matched to what you charge, included in the monthly plan']
        else:
            gets = ['A booking page with your treatments or services, ready for your Instagram bio and website',
                    'A private edit link to change your menu, options and prices whenever you like',
                    'Guide prices in your clients’ currency, with clear wording that final prices are confirmed by you',
                    'Requests emailed to you with the client’s preferred way to be contacted and one-tap WhatsApp',
                    'One line of code for your website, or free installation']
        faqs = n['faqs'] + [GLOBAL_FAQ[1], GLOBAL_FAQ[4], GLOBAL_FAQ[7]]
        others = [x for x in (TRADES if n['kind'] == 'trade' else CLINICS) if x['slug'] != n['slug']][:6]
        body = f'''<section class="hero"><div class="wrap">
<p class="crumbs"><a href="/">Home</a> / <a href="/instant-quote-calculator/">Calculators</a> / {e(n["name"])}</p>
<div class="split">
<div><h1>Instant quote calculator for {e(n["plural"])}</h1>
<p class="lede">{e(n["intro"])}</p>
<div class="actions"><a class="btn" href="#build">Build my free preview</a><a class="btn ghost" href="#jobs">See the jobs it prices</a></div>
{TRUST}</div>
{app_panel([n], n['key'], False, 'Try it as a customer')}
</div></div></section>
{FACTS}
<section class="sec" id="jobs"><div class="wrap split" style="align-items:start">
<div><h2>Jobs it prices</h2>
<p class="muted" style="margin-top:14px">Starting guide prices for the middle option ({e(mid[0].lower() + mid[1:])}). Customers can switch size and see the price change.</p>
<table class="jobs"><thead><tr><th scope="col">Job</th><th scope="col">Typical guide range</th></tr></thead><tbody>{rows}</tbody></table>
<p class="small">Typical UK prices for {e(n["plural"])}. Guide prices are estimates, not quotes, and customers see that clearly.</p></div>
<div><h2>What you get</h2><ul class="ticks">{''.join('<li>%s<span>%s</span></li>' % (icon('check'), e(g)) for g in gets)}</ul>
<p style="margin-top:22px"><a href="/pricing/">£197 setup, then £49 a month</a>. Cancel any time.</p></div>
</div></section>
{STEPS}
{faq_block(faqs, 'Questions from ' + n['plural'])}
<section class="sec"><div class="wrap"><div class="sec-head"><h2>Also built for</h2></div><div class="cols"><div>{biz_list(others[:3])}</div><div>{biz_list(others[3:6])}</div></div></div></section>
{build_section(n['key'], 'See your calculator in seconds', 'Type your business name and town to see the calculator your ' + n['people'] + ' would use. Nothing to pay unless you switch it on.')}'''
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
            ('Is the setup fee refundable?', 'The £197 setup covers building and delivering your calculator, so it is not refundable once your calculator has been delivered. If something is wrong with it, reply to your welcome email and we will put it right.'),
            ('What currency do you charge in?', 'Pounds sterling (GBP). If you pay from Ireland, the US or elsewhere, Stripe or your bank converts it, and you see the exact amount before you pay.')]
    body = f'''<section class="hero"><div class="wrap split">
<div><p class="crumbs"><a href="/">Home</a> / Pricing</p>
<h1>£197 to set up. £49 a month.</h1>
<p class="lede">One plan for every business. The setup fee covers building your calculator; the monthly plan keeps it online and sends you every request.</p>
<div class="actions"><a class="btn" href="#build">Build my free preview</a></div>{TRUST}</div>
{PLAN}
</div></section>
{faq_block(pfaq, 'Pricing questions')}
{build_section()}'''
    write('/pricing/', page('/pricing/', 'Pricing: £197 setup, £49 a month | AiEngineered', 'AiEngineered instant quote calculators cost £197 to set up and £49 a month. No contract, cancel any time, secure checkout by Stripe.', body,
          [crumbs_schema([('Home', '/'), ('Pricing', '/pricing/')]), {"@type": "Service", "name": "Instant quote calculator", "provider": {"@id": BASE + "/#org"}, "offers": OFFER}, faq_schema(pfaq)]))
    urls.append(('/pricing/', '0.9'))

    # ---------- FAQ ----------
    body = dark_head([('Home', '/'), ('FAQ', '')], 'Questions and answers', 'Anything not covered here? Send a message through the <a href="/contact/">contact form</a>.') + faq_block(GLOBAL_FAQ, 'All questions') + build_section()
    write('/faq/', page('/faq/', 'Questions about instant quote calculators | AiEngineered', 'What an instant quote calculator is, what it costs, how prices are set, where requests go and how to cancel.', body,
          [crumbs_schema([('Home', '/'), ('FAQ', '/faq/')]), faq_schema(GLOBAL_FAQ)]))
    urls.append(('/faq/', '0.7'))

    # ---------- Guides ----------
    body = dark_head([('Home', '/'), ('Guides', '')], 'Guides', 'Straight answers for trades, clinics and local businesses about pricing online and getting more enquiries.') + f'<section class="sec"><div class="wrap">{guide_cards(GUIDES)}</div></section>' + build_section()
    write('/guides/', page('/guides/', 'Guides for small businesses on pricing online | AiEngineered', 'Practical guides on showing prices on your website, adding a quote calculator and getting better enquiries.', body,
          [crumbs_schema([('Home', '/'), ('Guides', '/guides/')])]))
    urls.append(('/guides/', '0.7'))
    for g in GUIDES:
        path = '/guides/%s/' % g['slug']
        body = dark_head([('Home', '/'), ('Guides', '/guides/'), (g['title'], '')], g['h1'], e(g['desc']), f'<p class="meta" style="margin-top:18px">By Liam Hockley, AiEngineered. Updated {TODAY_LONG}.</p>') + \
            f'<section class="sec"><div class="wrap"><article class="prose">{g["body"]}</article></div></section>' + faq_block(g['faqs'], 'Common questions') + build_section()
        schema = [crumbs_schema([('Home', '/'), ('Guides', '/guides/'), (g['title'], path)]),
                  {"@type": "Article", "headline": g['h1'], "description": g['desc'], "datePublished": TODAY, "dateModified": TODAY,
                   "author": {"@type": "Person", "name": "Liam Hockley"}, "publisher": {"@id": BASE + "/#org"}, "mainEntityOfPage": BASE + path, "image": BASE + "/og.png"},
                  faq_schema(g['faqs'])]
        write(path, page(path, g['h1'] + ' | AiEngineered', g['desc'], body, schema))
        urls.append((path, '0.7'))

    # ---------- About ----------
    body = dark_head([('Home', '/'), ('About', '')], 'About AiEngineered', 'AiEngineered is a small UK business run by Liam Hockley. It builds instant quote calculators for trades, clinics, salons and other local businesses.') + f'''
<section class="sec"><div class="wrap"><div class="prose">
<p>Most people want a rough price before they contact anyone, and most small businesses don’t have time to answer “how much?” all day. A calculator answers it straight away and sends you the people who are happy with the price.</p>
<h2>New, and open about it</h2>
<p>AiEngineered is a new business, so you won’t find a wall of reviews here yet. Instead, you can see exactly what you would get before paying anything: build a free preview with your business name and town.</p>
<h2>How we work</h2>
<ul><li>Everything is handled online and by email. There is no need to book a call.</li><li>Payments are taken securely by Stripe. We never see your full card details.</li><li>No contract. Cancel from your billing link whenever you like.</li></ul>
<h2>The business</h2>
<p>AiEngineered is a trading name of Liam Hockley, a sole trader in the United Kingdom. Get in touch through {CONTACT_LINE}.</p>
</div></div></section>{build_section()}'''
    write('/about/', page('/about/', 'About AiEngineered', 'AiEngineered is a small UK business run by Liam Hockley, building instant quote calculators for trades, clinics and local businesses.', body,
          [crumbs_schema([('Home', '/'), ('About', '/about/')]), {"@type": "AboutPage", "url": BASE + "/about/", "about": {"@id": BASE + "/#org"}}]))
    urls.append(('/about/', '0.5'))

    # ---------- Contact ----------
    body = dark_head([('Home', '/'), ('Contact', '')], 'Contact', 'Questions before you sign up, or help with your calculator. We reply by email, usually the same day.') + f'''
<section class="sec light-form"><div class="wrap split" style="align-items:start">
<form class="form" id="contact-form" novalidate>
<div><label for="cf-name">Your name</label><input type="text" id="cf-name" autocomplete="name" maxlength="80" required></div>
<div><label for="cf-email">Email</label><input type="email" id="cf-email" autocomplete="email" maxlength="120" required></div>
<div class="full"><label for="cf-business">Business name (optional)</label><input type="text" id="cf-business" autocomplete="organization" maxlength="80"></div>
<div class="full"><label for="cf-message">Message</label><textarea id="cf-message" maxlength="3000" required></textarea></div>
<input type="text" id="cf-hp" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
<div class="full"><button class="btn" type="submit">Send message</button></div>
<p class="err full" id="cf-err" role="alert"></p>
<p class="okmsg full" id="cf-ok" hidden>Thanks, your message has been sent. We will reply by email.</p>
</form>
<div><h2>Already a customer?</h2><p class="muted" style="margin-top:14px">Reply to your welcome email for price changes or help. To update your card, download invoices or cancel, use <a href="{PORTAL}">Manage my plan</a> and sign in with the email you paid with.</p>
{f'<p class="muted">Email: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>' if CONTACT_EMAIL else ''}</div>
</div></section>'''
    write('/contact/', page('/contact/', 'Contact AiEngineered', 'Get in touch with AiEngineered about instant quote calculators. We reply by email.', body,
          [crumbs_schema([('Home', '/'), ('Contact', '/contact/')]), {"@type": "ContactPage", "url": BASE + "/contact/", "about": {"@id": BASE + "/#org"}}]))
    urls.append(('/contact/', '0.5'))

    # ---------- Terms ----------
    terms = dark_head([('Home', '/'), ('Terms', '')], 'Terms of service', f'Last updated {TODAY_LONG}') + f'''
<section class="sec"><div class="wrap"><div class="prose">
<p>These terms cover AiEngineered instant quote calculators. AiEngineered is a trading name of Liam Hockley, a sole trader in the United Kingdom (“we”, “us”). By paying for a calculator you agree to these terms. Our service is for businesses, not consumers.</p>
<h2>1. What you get</h2>
<ul><li>A calculator page set up with your business name, services and guide prices.</li><li>A link you can share, and code to add it to your website. We will install it for you free if you ask.</li><li>Customer requests sent through the calculator emailed to the address you give us.</li><li>Price adjustments and help by email.</li></ul>
<h2>2. Price and payment</h2>
<ul><li>Setup costs £197, paid once at checkout. The monthly plan costs £49 a month, paid in advance, starting on the day you buy.</li><li>Prices are in pounds sterling (GBP). If you pay in another currency, Stripe or your bank converts it, and any conversion or bank fees are yours.</li><li>Payments are processed by Stripe. We never see your full card details.</li><li>We will give you at least 30 days’ notice by email before changing the monthly price.</li></ul>
<h2>3. Cancelling</h2>
<ul><li>Cancel at any time from the “Manage my plan” link in your welcome email, or by contacting us.</li><li>Your plan stays active until the end of the month you have paid for. After that, requests stop being sent and your calculator shows that you are not taking online requests.</li><li>We don’t refund part months. The setup fee is not refundable once your calculator has been delivered. If something is wrong with it, tell us and we will fix it.</li><li>If a monthly payment fails and is still unpaid after Stripe’s retries, your plan ends in the same way.</li></ul>
<h2>4. Guide prices and your customers</h2>
<p>Prices on your calculator are guide estimates. You are responsible for the prices and wording shown to your customers, for making sure they meet the rules that apply to your business and where you trade, and for replying to the requests you receive. Your customers are told that prices are guides and that you confirm the final price.</p>
<h2>5. Your customers’ details</h2>
<p>When your customers send a request, we pass their details to you by email, and you are responsible for how you use them. Our <a href="/privacy/">privacy notice</a> explains what we keep.</p>
<h2>6. Availability</h2>
<p>We work to keep calculators online and requests flowing, but we can’t promise the service will never be interrupted.</p>
<h2>7. Liability</h2>
<p>Nothing in these terms limits liability that can’t be limited by law. Otherwise, our total liability to you is limited to the amount you have paid us in the three months before the claim, and we are not liable for lost profits or lost business.</p>
<h2>8. Which law applies</h2>
<p>These terms are governed by the law of the place where your business is based, and the courts there can hear any dispute:</p>
<table><thead><tr><th>Where your business is based</th><th>Law and courts</th></tr></thead><tbody>
<tr><td>England or Wales</td><td>The law of England and Wales, and the courts of England and Wales</td></tr>
<tr><td>Scotland</td><td>Scots law, and the Scottish courts</td></tr>
<tr><td>Northern Ireland</td><td>The law of Northern Ireland, and the courts of Northern Ireland</td></tr>
<tr><td>Ireland</td><td>Irish law, and the courts of Ireland</td></tr>
<tr><td>United States</td><td>The law of the state where your business is based, and the state or federal courts in that state</td></tr>
<tr><td>Anywhere else</td><td>The law of the country where your business is based, and its courts</td></tr>
</tbody></table>
<p>If the law where your business is based gives you rights that can’t be changed by agreement, those rights still apply.</p>
<h2>9. Changes</h2>
<p>We may update these terms and will email you about important changes before they take effect.</p>
<h2>10. Contact</h2><p>{CONTACT_LINE.capitalize() if not CONTACT_EMAIL else CONTACT_LINE}</p>
</div></div></section>'''
    write('/terms/', page('/terms/', 'Terms of service | AiEngineered', 'Terms for AiEngineered instant quote calculators: what you get, price, cancelling, guide prices and which law applies.', terms))
    urls.append(('/terms/', '0.3'))

    privacy = dark_head([('Home', '/'), ('Privacy', '')], 'Privacy notice', f'Last updated {TODAY_LONG}') + f'''
<section class="sec"><div class="wrap"><div class="prose">
<p>This notice explains how AiEngineered (a trading name of Liam Hockley, a sole trader in the United Kingdom) handles personal information. You can reach us through {CONTACT_LINE}.</p>
<h2>Businesses that buy a calculator</h2>
<p>We keep your name, email address, business name, town and the details on your calculator, so we can set it up, send you requests and help you. Card payments are handled by Stripe; we don’t see your full card details. We keep this while you are a customer and for up to six years afterwards for our accounts.</p>
<h2>People who send a request through a calculator</h2>
<p>When you send a request, your name, phone number, email, the job you picked and any notes are emailed to the business whose calculator you used. That business decides how to use them, so please check their privacy information too. We act on the business’s behalf and keep a copy of each request so we can check it was delivered and help if something goes wrong. Ask us to delete it at any time.</p>
<h2>Messages through our contact form</h2>
<p>We use your name, email and message to reply to you, and keep them for as long as we need to deal with your message.</p>
<h2>Visitors to this website</h2>
<p>This website doesn’t use advertising or tracking cookies. Our hosting provider keeps basic technical logs for security, and fonts load from Google Fonts, which receives your IP address to deliver them.</p>
<h2>Who we share information with</h2>
<p>Only the services we need to run AiEngineered: Stripe (payments), Vercel (hosting), n8n (sending requests and messages) and Google (email and fonts). Some of these process information outside the UK and the EU under recognised safeguards.</p>
<h2>Your rights</h2>
<ul><li><strong>UK:</strong> under UK GDPR you can ask to see, correct or delete your information, or object to how we use it. You can complain to the Information Commissioner’s Office (ico.org.uk).</li>
<li><strong>Ireland and the EU:</strong> you have the same rights under the EU GDPR, and can complain to the Data Protection Commission (dataprotection.ie) or your local regulator.</li>
<li><strong>United States:</strong> you can ask to see or delete the information we hold about you. We don’t sell personal information.</li></ul>
<p>To use any of these rights, contact us and we will reply within one month.</p>
</div></div></section>'''
    write('/privacy/', page('/privacy/', 'Privacy notice | AiEngineered', 'How AiEngineered handles personal information for businesses, their customers and website visitors in the UK, Ireland and the US.', privacy))
    urls.append(('/privacy/', '0.3'))

    thanks = dark_head([('Home', '/'), ('Thank you', '')], 'Payment received. Thank you.', 'Your calculator link and website code are on their way to your email now. They usually arrive within a few minutes.') + f'''
<section class="sec"><div class="wrap"><div class="prose"><ul>
<li>Check your spam or promotions folder if you can’t see it.</li><li>Want it on your website? Reply to that email with your website platform and we will install it for you.</li><li>Nothing after 15 minutes? Use the <a href="/contact/">contact form</a>.</li></ul>
<p>You can manage or cancel your plan any time from <a href="{PORTAL}">your billing page</a>.</p></div></div></section>'''
    write('/thanks/', page('/thanks/', 'Thank you | AiEngineered', 'Your calculator is on its way.', thanks, noindex=True))
    nf = dark_head([('Home', '/')], 'That page isn’t here.', 'Try the <a href="/">home page</a> or see <a href="/instant-quote-calculator/">all calculators</a>.')
    open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8').write(page('/404', 'Page not found | AiEngineered', 'Page not found.', nf, noindex=True))

    # ---------- robots, sitemap, llms.txt, vercel.json ----------
    open(os.path.join(OUT, 'robots.txt'), 'w').write(
        'User-agent: *\nAllow: /\nDisallow: /thanks/\n\n# AI search and assistant crawlers are welcome\n' +
        ''.join(f'User-agent: {b}\nAllow: /\n\n' for b in ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User', 'PerplexityBot', 'Perplexity-User', 'Google-Extended', 'Bingbot', 'Applebot', 'Applebot-Extended']) +
        f'Sitemap: {BASE}/sitemap.xml\n')
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{BASE}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n' for p, pr in urls) + '</urlset>\n'
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(sm)
    llms = ['# AiEngineered', '',
            '> AiEngineered builds instant quote calculators for trades, clinics, salons and other local businesses in the UK, Ireland and the US. Customers pick a job, see a guide price for the area, and send their details to the business by email. Price: £197 setup, then £49 a month, cancel any time. Run by Liam Hockley, a sole trader in the United Kingdom.', '',
            '## How it works', '- A business builds a free preview with its name, town and type of business.',
            '- If they like it, they pay £197 setup plus £49 a month through Stripe and receive their calculator link and website code by email within minutes.',
            '- Their customers choose a job and size, see a guide price range, and send a request. The request is emailed to the business with one-tap call and WhatsApp buttons.',
            '- Clinics, salons and similar businesses edit their own prices from a private link; trades tell AiEngineered what they charge and the price level is adjusted to match.',
            '- Cancelling is self-serve through Stripe; the plan runs to the end of the paid month, then requests stop.', '',
            '## Key pages', f'- [Home]({BASE}/)', f'- [Pricing]({BASE}/pricing/): £197 setup, £49 a month', f'- [FAQ]({BASE}/faq/)', f'- [All calculators]({BASE}/instant-quote-calculator/)', f'- [Contact]({BASE}/contact/)', '',
            '## Guides'] + [f'- [{g["h1"]}]({BASE}/guides/{g["slug"]}/): {g["summary"]}' for g in GUIDES] + ['', '## Calculators by business type']
    for n in NICHES:
        llms.append(f'- [Instant quote calculator for {n["plural"]}]({BASE}/instant-quote-calculator/{n["slug"]}/): ' + ', '.join(j['name'] for j in n['jobs']))
    llms += ['', '## Contact', f'- Contact form: {BASE}/contact/'] + ([f'- Email: {CONTACT_EMAIL}'] if CONTACT_EMAIL else []) + ['- No calls needed; everything is handled online and by email.', '']
    open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf-8').write('\n'.join(llms))
    redirects = []
    if os.environ.get('REDIRECT_VERCEL_HOST') == '1':
        for h in ['aiengineered.vercel.app', 'aiengineered-hone9.vercel.app', 'aiengineered-git-website-hone9.vercel.app']:
            redirects.append({"source": "/(.*)", "has": [{"type": "host", "value": h}], "destination": BASE + "/$1", "permanent": True})
    open(os.path.join(OUT, 'vercel.json'), 'w').write(json.dumps({
        "cleanUrls": True, "trailingSlash": True,
        "headers": [{"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=604800"}]},
                    {"source": "/(.*)", "headers": [{"key": "X-Content-Type-Options", "value": "nosniff"}, {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                                                    {"key": "Strict-Transport-Security", "value": "max-age=63072000"}, {"key": "X-Frame-Options", "value": "SAMEORIGIN"}]}],
        "redirects": redirects}, indent=1))
    print('built', len(urls), 'indexable pages into', OUT)
    return urls

if __name__ == '__main__':
    build()
