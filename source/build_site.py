#!/usr/bin/env python3
"""Builds the Cerritos Piano Tuner static site into ./public.

Edit the SITE dict and PAGES below, then run:  python3 build_site.py
Copy comes from the 'Website copy: Cerritos Piano Tuner' doc.
"""
import html
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "public")

SITE = {
    "name": "Ryan Ellison Piano",
    "legal": "Cerritos Piano Tuner LLC",
    "short": "Ryan Ellison Piano",
    "owner": "Registered Piano Technician",
    "phone": "(657) 438-4984",
    "tel": "+16574384984",
    "email": "cerritospianotuner@outlook.com",
    "street": "13337 South St. #110",
    "city": "Cerritos",
    "state": "CA",
    "zip": "90703",
    "book": "https://gazelleapp.io/scheduling/p1CPJwKXWzDxfFYGpxzMSb9p",
    # Set this when the domain is connected (no trailing slash). Used for canonical URLs and sitemap.
    "domain": "https://www.ryanellisonpiano.com",
}

NAV = [
    ("index.html", "Home"),
    ("services.html", "Services & prices"),
    ("disklavier-silent-hybrid.html", "Disklavier / Silent / Hybrid"),
    ("bosendorfer.html", "Bösendorfer"),
    ("service-area.html", "Service area"),
    ("about.html", "About"),
    ("faq.html", "FAQ"),
    ("contact.html", "Contact"),
]

e = html.escape


def layout(fname, title, desc, body, schema=False):
    nav = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == fname else ""}>{e(label)}</a>'
        for href, label in NAV
    )
    canon = f'{SITE["domain"]}/{"" if fname == "index.html" else fname}'
    ld = ""
    if schema:
        ld = f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HomeAndConstructionBusiness",
  "additionalType": "https://schema.org/LocalBusiness",
  "name": "{SITE['name']}",
  "legalName": "{SITE['legal']}",
  "description": "Piano tuning and service for Bösendorfer, Yamaha, Disklavier, Silent and Hybrid pianos in Orange County, Riverside County and southeast Los Angeles County.",
  "url": "{SITE['domain']}/",
  "telephone": "{SITE['tel']}",
  "email": "{SITE['email']}",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "{SITE['street']}",
    "addressLocality": "{SITE['city']}",
    "addressRegion": "{SITE['state']}",
    "postalCode": "{SITE['zip']}",
    "addressCountry": "US"
  }},
  "openingHoursSpecification": [{{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Thursday", "Friday", "Saturday"],
    "opens": "09:00",
    "closes": "17:00"
  }}],
  "areaServed": ["Orange County, CA", "Riverside County, CA", "Los Angeles County, CA"],
  "priceRange": "$99-$495"
}}
</script>"""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#1f2a37">
<link rel="stylesheet" href="style.css">{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="index.html">{e(SITE['short'])}<small>{e(SITE['owner'])}</small></a>
    <input type="checkbox" id="menu" class="menu-toggle" aria-label="Toggle menu">
    <label for="menu" class="menu-btn" aria-hidden="true">Menu</label>
    <nav class="nav" aria-label="Main">{nav}</nav>
    <a class="btn call" href="tel:{SITE['tel']}">Call {e(SITE['phone'])}</a>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap cols">
    <div>
      <strong>{e(SITE['name'])}</strong><br>{e(SITE['legal'])}<br>
      {e(SITE['street'])}<br>{e(SITE['city'])}, {e(SITE['state'])} {e(SITE['zip'])}<br>
      <a href="tel:{SITE['tel']}">{e(SITE['phone'])}</a>
    </div>
    <div>
      Mon, Tue, Thu, Fri, Sat<br>9:00 am – 5:00 pm<br>Closed Wednesday and Sunday
    </div>
    <div>
      <a href="{SITE['book']}">Book online</a><br>
      <a href="services.html">Prices</a><br>
      <a href="faq.html">FAQ</a>
    </div>
  </div>
  <div class="wrap fine">&copy; 2026 {e(SITE['name'])}, a service of {e(SITE['legal'])}. Registered Piano Technician, Piano Technicians Guild.</div>
</footer>
</body>
</html>
"""


def cta(text="Ready to book? Choose a time online or call " + SITE["phone"] + "."):
    return f"""<section class="cta"><div class="wrap">
<p>{e(text)}</p>
<p><a class="btn primary" href="{SITE['book']}">Book online</a>
<a class="btn" href="tel:{SITE['tel']}">Call or text {e(SITE['phone'])}</a></p>
</div></section>"""


PRICES = [
    ("Minimum Ear Tuning", "Basic tuning for everyday use, or for pianos that cannot hold concert pitch", "$99"),
    ("Full Ear Tuning", "Fine tuning at concert pitch", "$199"),
    ("Pin setting add-on", "Re-tensions loose or low tuning pins", "+$70"),
    ("Repeat customer discount", "Full Ear Tuning, within 18 months of your last tuning", "−$40"),
    ("New Piano Initial Prep", "Pin setting, fine tuning and minimum regulation for a newly delivered piano", "$495"),
    ("Minimum Regulation", "Action regulation to the level needed for performance", "$165"),
    ("D.S.H. Maintenance", "Disklavier, Silent and Hybrid calibration and adjustments. Prepaid by credit card when you book", "$179"),
    ("Repairs", "Sticky keys, broken strings and other acoustic repairs", "from $79"),
    ("Other work", "Full regulation, voicing, hammer mating and larger projects", "Quote on request"),
]


def price_table():
    rows = "".join(
        f"<tr><th scope=\"row\">{e(a)}</th><td>{e(b)}</td><td class=\"price\">{e(c)}</td></tr>"
        for a, b, c in PRICES
    )
    return f"""<div class="table-wrap"><table class="prices">
<thead><tr><th>Service</th><th>What it covers</th><th>Price</th></tr></thead>
<tbody>{rows}</tbody></table></div>"""


PAGES = {}

# ---------------- Home ----------------
PAGES["index.html"] = (
    "Piano Tuner in Orange County and Cerritos",
    "Tuning and service for Bösendorfer, Yamaha, Disklavier, Silent and Hybrid pianos. Book online or call (657) 438-4984.",
    f"""<section class="hero"><div class="wrap">
<h1>Piano tuning and service for Bösendorfer, Yamaha, Disklavier, Silent and Hybrid pianos</h1>
<p class="lead">I'm Ryan Ellison, RPT. After ten years working on Yamaha pianos, I now serve homes, schools and churches across Orange County, Riverside and the Gateway Cities.</p>
<p><a class="btn primary" href="{SITE['book']}">Book online</a>
<a class="btn" href="tel:{SITE['tel']}">Call or text {e(SITE['phone'])}</a></p>
<p class="trust">Registered Piano Technician (RPT), Piano Technicians Guild.</p>
</div></section>
<section class="wrap block">
<h2>Three reasons to choose me</h2>
<div class="cards">
<div class="card"><h3>Experience with pianos most tuners avoid</h3>
<p>Bösendorfer, Disklavier, Silent and Hybrid pianos need a technician who understands the acoustic instrument and the electronics. I do both.</p></div>
<div class="card"><h3>One technician, start to finish</h3>
<p>You deal with me, not a dispatcher. I tune, adjust and repair your piano myself.</p></div>
<div class="card"><h3>Clear pricing before I arrive</h3>
<p>I confirm the price when you book, so there are no surprises at the door.</p></div>
</div>
<p><a href="services.html">See services and prices</a> · <a href="service-area.html">See where I work</a></p>
</section>
<!-- REVIEWS STRIP: add one or two real Google/Yelp reviews here with the reviewer's permission. -->
{cta()}""",
    True,
)

# ---------------- Services ----------------
PAGES["services.html"] = (
    "Piano Tuning Prices and Services",
    "Ear tuning from $99, regulation, repairs and new piano prep. See prices and book online.",
    f"""<section class="wrap block"><h1>Services and prices</h1>
<p class="lead">Other work is billed at $99 per hour, with a $99 minimum service call. Payment is due at the time of service.</p>
{price_table()}
<p>Disklavier, Silent and Hybrid owners: see <a href="disklavier-silent-hybrid.html">D.S.H. service</a> for what is included and how prepayment works.</p>
</section>
{cta()}""",
)

# ---------------- D.S.H. ----------------
PAGES["disklavier-silent-hybrid.html"] = (
    "Disklavier and Silent Piano Service",
    "Calibration and repair for Disklavier, Silent and Hybrid pianos by a registered piano technician.",
    f"""<section class="wrap block"><h1>Service for Disklavier, Silent and Hybrid pianos</h1>
<p class="lead">These pianos combine an acoustic piano with sensors, solenoids and electronics. Many tuners are not comfortable working on them. After ten years working on Yamaha pianos, this is what I do every day.</p>
<h2>What is included in D.S.H. Maintenance ($179)</h2>
<ul>
<li>Calibration and table updates for the Disklavier, Silent or Hybrid system</li>
<li>Adjustments to the system so playback, recording and silent mode respond correctly</li>
<li>A check of the connected hardware that the piano depends on</li>
</ul>
<p><strong>Repairs</strong> start at $79. Larger electronic or mechanical problems are quoted before work begins.</p>
<p><strong>Tuning is billed separately.</strong> Most owners book an ear tuning and D.S.H. Maintenance in the same visit, so the piano sounds right and plays right. D.S.H. Maintenance is paid in full by credit card when you book.</p>
</section>
{cta("Not sure what your piano needs? Call " + SITE["phone"] + " or book online and describe the model. I will tell you what to expect before I arrive.")}""",
)

# ---------------- Bösendorfer ----------------
PAGES["bosendorfer.html"] = (
    "Bösendorfer Piano Tuning in Southern California",
    "Tuning, regulation and service for Bösendorfer pianos by a Registered Piano Technician. Book online or call (657) 438-4984.",
    f"""<section class="wrap block"><h1>Bösendorfer piano tuning and service</h1>
<p class="lead">A Bösendorfer deserves a technician who treats it as the fine instrument it is. I tune, regulate and service Bösendorfer pianos across Orange County, Riverside County and southeast Los Angeles County.</p>
<ul>
<li>Full Ear Tuning at concert pitch ($199)</li>
<li>Regulation and other action work, quoted before I begin</li>
<li>Repairs and condition assessment, with a plain explanation of what the piano needs</li>
</ul>
<p>See all <a href="services.html">services and prices</a>. If you're not sure what your piano needs, call or book online and tell me the model.</p>
<!-- TODO (Ryan): add the Bösendorfer models and the kinds of work you have done on them, if you want to name them. -->
</section>
{cta()}""",
)

# ---------------- Service area ----------------
PAGES["service-area.html"] = (
    "Piano Tuner in Orange County, Riverside and LA County",
    "Piano tuning across Orange County, Riverside County and southeast Los Angeles County. Book online or call (657) 438-4984.",
    f"""<section class="wrap block"><h1>Piano tuning in Orange County, Riverside County and southeast Los Angeles County</h1>
<p class="lead">I travel to your home, studio or school.</p>
<div class="cards">
<a class="card link" href="orange-county.html"><h3>Orange County</h3><p>Irvine, Newport Beach, Huntington Beach, Buena Park, Yorba Linda, Fullerton and more</p></a>
<a class="card link" href="riverside-county.html"><h3>Riverside County</h3><p>Riverside, Corona</p></a>
<a class="card link" href="cerritos-la-county.html"><h3>Cerritos and LA County</h3><p>Cerritos, Norwalk, Artesia, La Mirada, Downey, Long Beach</p></a>
</div>
<p>Don't see your city? Call {e(SITE['phone'])}. I may still be able to schedule you, especially if neighbors are booking the same week.</p>
</section>
{cta()}""",
)

PAGES["orange-county.html"] = (
    "Piano Tuner in Orange County, CA",
    "Piano tuning in Irvine, Newport Beach, Huntington Beach, Fullerton and nearby. Book online.",
    f"""<section class="wrap block"><h1>Piano tuner in Orange County</h1>
<p class="lead">I travel to your home, studio or school. Areas I serve regularly:</p>
<p>Irvine, Newport Beach, Huntington Beach, Buena Park, Yorba Linda, Fullerton, La Habra, Mission Viejo, Laguna Hills, San Clemente, Costa Mesa</p>
<p>Don't see your city? Call {e(SITE['phone'])}. I may still be able to schedule you, especially if neighbors are booking the same week.</p>
<p><a href="services.html">Services and prices</a> · <a href="disklavier-silent-hybrid.html">Disklavier, Silent and Hybrid</a></p>
</section>
{cta()}""",
)

PAGES["riverside-county.html"] = (
    "Piano Tuner in Riverside and Corona",
    "Piano tuning and service in Riverside and Corona. Book online or call (657) 438-4984.",
    f"""<section class="wrap block"><h1>Piano tuner in Riverside and Corona</h1>
<p class="lead">I travel to your home, studio or school. Areas I serve regularly: Riverside and Corona.</p>
<p>Don't see your city? Call {e(SITE['phone'])}. I may still be able to schedule you, especially if neighbors are booking the same week.</p>
<p><a href="services.html">Services and prices</a> · <a href="disklavier-silent-hybrid.html">Disklavier, Silent and Hybrid</a></p>
</section>
{cta()}""",
)

PAGES["cerritos-la-county.html"] = (
    "Piano Tuner in Cerritos and Norwalk",
    "Piano tuning in Cerritos, Norwalk, Artesia, La Mirada, Downey and Long Beach.",
    f"""<section class="wrap block"><h1>Piano tuner in Cerritos, Norwalk and southeast LA County</h1>
<p class="lead">I travel to your home, studio or school. Areas I serve regularly:</p>
<p>Cerritos, Norwalk, Artesia, La Mirada, Downey, Long Beach</p>
<p>Don't see your city? Call {e(SITE['phone'])}. I may still be able to schedule you, especially if neighbors are booking the same week.</p>
<p><a href="services.html">Services and prices</a> · <a href="disklavier-silent-hybrid.html">Disklavier, Silent and Hybrid</a></p>
</section>
{cta()}""",
)

# ---------------- About ----------------
PAGES["about.html"] = (
    "About Ryan Ellison, RPT",
    "Registered Piano Technician with ten years of Yamaha experience, specializing in Bösendorfer, Yamaha and Disklavier pianos.",
    f"""<section class="wrap block"><h1>Meet Ryan Ellison, RPT</h1>
<!-- PHOTO: add a clear photo of yourself at work. -->
<p class="lead">I've spent more than ten years working on pianos for a living, including Yamaha grands and uprights, Disklavier, Silent and Hybrid pianos, and Bösendorfer. I started Ryan Ellison Piano to give local piano owners the same careful, technical service on every instrument, from a family upright to a high-end grand.</p>
<p><strong>Specialties:</strong> Yamaha grand and upright pianos · Disklavier, Silent and Hybrid pianos · Bösendorfer pianos</p>
<h2>Training and credentials</h2>
<ul>
<li>Registered Piano Technician, Piano Technicians Guild (2017)</li>
<li>Grand Piano Master Course, Yamaha Piano Technical Academy, Japan (2019)</li>
<li>Grand Piano Course, Yamaha Piano Technical Academy, Japan (2017)</li>
<li>Chicago School for Piano Technology (2011)</li>
<li>Bachelor of Music (2007)</li>
</ul>
<p><strong>What I care about:</strong> A piano that holds its tuning, feels even under the fingers, and sounds the way it should. I'll tell you plainly what your piano needs and what it doesn't.</p>
<!-- PERSONAL SENTENCE: add one line on what first drew you to pianos. -->
</section>
{cta()}""",
)

# ---------------- FAQ ----------------
FAQ = [
    ("How often should I tune my piano?", "Twice a year for most pianos, and at least once a year. New pianos and pianos that have been moved need more frequent tuning in the first year."),
    ("How long does a tuning take?", "A Full Ear Tuning usually takes about two hours. A Minimum Ear Tuning takes about an hour."),
    ("What is the difference between Minimum and Full Ear Tuning?", "A Full Ear Tuning brings the piano to concert pitch. A Minimum Ear Tuning is a basic tuning for everyday playing, or for older pianos that cannot safely hold concert pitch."),
    ("What if my piano has not been tuned in years?", "It may be flat and need a pin setting add-on (+$70) to bring it up to pitch and make the tuning last. I will tell you what I find before I go ahead."),
    ("Can tuning damage an old piano?", "Pianos are under very high string tension, and aged parts can fail during tuning. I explain the risks before I start, and I will repair what I can on the spot. The service form lists these terms in full."),
    ("How do I pay?", "Cash, check, Zelle, Venmo or card. The price is the same whichever you use. The exception is D.S.H. Maintenance for Disklavier, Silent and Hybrid pianos, which is prepaid by credit card when you book and applied to your final bill."),
]
faq_html = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in FAQ)
faq_ld = ",".join(
    '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
    % (__import__("json").dumps(q, ensure_ascii=False), __import__("json").dumps(a, ensure_ascii=False))
    for q, a in FAQ
)
PAGES["faq.html"] = (
    "Piano Tuning FAQ",
    "How often to tune a piano, how long tuning takes, pricing and payment. Answers from Ryan Ellison, RPT.",
    f"""<section class="wrap block"><h1>Frequently asked questions</h1>
{faq_html}
</section>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_ld}]}}</script>
{cta()}""",
)

# ---------------- Contact ----------------
PAGES["contact.html"] = (
    "Contact and Book a Piano Tuning",
    "Book your piano tuning online or call (657) 438-4984. Cerritos Piano Tuner LLC, serving Orange County, Riverside and LA County.",
    f"""<section class="wrap block"><h1>Book your piano tuning</h1>
<p><a class="btn primary" href="{SITE['book']}">Book online</a></p>
<ul class="plain">
<li><strong>Call or text:</strong> <a href="tel:{SITE['tel']}">{e(SITE['phone'])}</a></li>
<li><strong>Business:</strong> {e(SITE['name'])} ({e(SITE['legal'])}), {e(SITE['street'])}, {e(SITE['city'])}, {e(SITE['state'])} {e(SITE['zip'])}</li>
<li><strong>Hours:</strong> Monday, Tuesday, Thursday, Friday and Saturday, 9:00 am – 5:00 pm. Closed Wednesday and Sunday.</li>
</ul>
</section>""",
)

CSS = """
:root{--ink:#1c2430;--muted:#58636f;--bg:#faf8f5;--card:#fff;--line:#e4dfd7;--navy:#1f2a37;--accent:#9b5a2a;--accent-d:#7c4720}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font:17px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:var(--bg)}
h1,h2,h3{font-family:Georgia,"Times New Roman",serif;line-height:1.2;color:var(--navy)}
h1{font-size:clamp(1.8rem,5vw,2.8rem);margin:0 0 .6em}
h2{font-size:1.6rem;margin:1.6em 0 .6em}
h3{font-size:1.2rem;margin:1.4em 0 .3em}
a{color:var(--accent-d)}
.wrap{max-width:1040px;margin:0 auto;padding:0 16px}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:#fff;padding:8px;z-index:10}
.site-header{background:var(--navy);color:#fff;position:sticky;top:0;z-index:5}
.bar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding-top:10px;padding-bottom:10px}
.brand{color:#fff;text-decoration:none;font-family:Georgia,serif;font-size:1.2rem;font-weight:bold;margin-right:auto}
.brand small{display:block;font:12px system-ui;opacity:.75;font-weight:normal}
.nav{display:none;width:100%;flex-direction:column;order:5}
.nav a{color:#fff;text-decoration:none;padding:9px 0;border-top:1px solid rgba(255,255,255,.15)}
.nav a[aria-current]{font-weight:bold;color:#f1c9a5}
.menu-toggle{position:absolute;opacity:0}
.menu-btn{cursor:pointer;border:1px solid rgba(255,255,255,.4);border-radius:6px;padding:6px 10px;font-size:.9rem}
.menu-toggle:checked ~ .nav{display:flex}
.menu-toggle:focus-visible ~ .menu-btn{outline:2px solid #f1c9a5}
.btn{display:inline-block;padding:11px 18px;border-radius:8px;border:2px solid var(--navy);color:var(--navy);text-decoration:none;font-weight:600;margin:4px 6px 4px 0;background:#fff}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.primary:hover{background:var(--accent-d)}
.btn.call{background:transparent;border-color:rgba(255,255,255,.6);color:#fff;margin:0;padding:8px 12px;font-size:.9rem}
.hero{background:linear-gradient(135deg,#fff 0%,#f3ece3 100%);padding:48px 0 40px;border-bottom:1px solid var(--line)}
.lead{font-size:1.15rem;color:#2d3744}
.trust{color:var(--muted);font-size:.95rem}
.block{padding-top:36px;padding-bottom:36px}
.cards{display:grid;gap:16px;grid-template-columns:1fr;margin:20px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px}
.card h3{margin-top:0}
a.card.link{text-decoration:none;color:inherit}a.card.link:hover{border-color:var(--accent)}
.table-wrap{overflow-x:auto;margin:20px 0}
table.prices{border-collapse:collapse;width:100%;background:var(--card);min-width:520px}
.prices th,.prices td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}
.prices thead th{background:var(--navy);color:#fff}
.prices .price{white-space:nowrap;font-weight:700}
.cta{background:var(--navy);color:#fff;padding:32px 0;text-align:center}
.cta .btn{border-color:#fff}
.cta .btn.primary{border-color:var(--accent)}
ul.plain{list-style:none;padding:0}ul.plain li{margin:.6em 0}
.site-footer{background:#141b24;color:#cdd3da;padding:28px 0 18px;font-size:.95rem}
.site-footer a{color:#f1c9a5}
.cols{display:grid;gap:18px;grid-template-columns:1fr}
.fine{margin-top:18px;font-size:.85rem;opacity:.7}
@media(min-width:900px){
 .nav{display:flex;flex-direction:row;width:auto;order:0;gap:14px}
 .nav a{border:0;padding:4px 0;font-size:.92rem}
 .menu-btn{display:none}
 .btn.call{display:none}
 .cards{grid-template-columns:repeat(3,1fr)}
 .cols{grid-template-columns:repeat(3,1fr)}
}
"""


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for fname, page in PAGES.items():
        title, desc, body = page[0], page[1], page[2]
        schema = len(page) > 3 and page[3]
        with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
            f.write(layout(fname, title, desc, body, schema))
    with open(os.path.join(OUT, "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS.strip() + "\n")
    urls = "".join(
        f"  <url><loc>{SITE['domain']}/{'' if n == 'index.html' else n}</loc></url>\n" for n in PAGES
    )
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + urls + "</urlset>\n"
        )
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE['domain']}/sitemap.xml\n")
    print("built", len(PAGES), "pages ->", OUT)


if __name__ == "__main__":
    main()
