#!/usr/bin/env python3
"""Builds the Ryan Ellison Piano static site into ./public (design v3).

Edit SITE and PAGES below, then run:  python3 build_site.py
Copy comes from the 'Website copy: Cerritos Piano Tuner' doc.
"""
import html
import json
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
    ("services.html", "Services"),
    ("disklavier-silent-hybrid.html", "Disklavier, Silent, Hybrid"),
    ("bosendorfer.html", "Bösendorfer"),
    ("bellharp.html", "Bellharp"),
    ("service-area.html", "Service area"),
    ("about.html", "About"),
    ("faq.html", "FAQ"),
    ("contact.html", "Contact"),
]

e = html.escape

FONTS = (
    "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700"
    "&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap"
)


def layout(fname, title, desc, body, schema=False, script=""):
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
<meta name="theme-color" content="#1a2147">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="style.css">{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="index.html">{e(SITE['short'])}<small>{e(SITE['owner'])}</small></a>
    <input type="checkbox" id="menu" class="menu-toggle" aria-label="Open menu">
    <label for="menu" class="menu-btn">Menu</label>
    <nav class="nav" aria-label="Main">{nav}</nav>
    <a class="phone" href="tel:{SITE['tel']}">{e(SITE['phone'])}</a>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap cols">
    <div>
      <strong>{e(SITE['name'])}</strong>
      {e(SITE['legal'])}<br>
      {e(SITE['street'])}<br>{e(SITE['city'])}, {e(SITE['state'])} {e(SITE['zip'])}<br>
      <a href="tel:{SITE['tel']}">{e(SITE['phone'])}</a>
    </div>
    <div>
      <strong>Hours</strong>
      Monday, Tuesday, Thursday, Friday, Saturday<br>9:00 am to 5:00 pm<br>Closed Wednesday and Sunday
    </div>
    <div>
      <strong>Book</strong>
      <a href="{SITE['book']}">Book online</a><br>
      <a href="services.html">Prices</a><br>
      <a href="faq.html">Questions</a>
    </div>
  </div>
  <div class="wrap fine">&copy; 2026 {e(SITE['name'])}, a service of {e(SITE['legal'])}. Registered Piano Technician, Piano Technicians Guild.<br>Piano sounds: Salamander Grand Piano by Alexander Holm, <a href="https://creativecommons.org/licenses/by/3.0/">CC BY 3.0</a>.</div>
</footer>
<div class="mobilebar">
  <a class="btn" href="tel:{SITE['tel']}">Call</a>
  <a class="btn primary" href="{SITE['book']}">Book online</a>
</div>{script}
</body>
</html>
"""


def cta(text="Ready to book? Pick a time online or call " + SITE["phone"] + "."):
    return f"""<section class="cta"><div class="wrap">
<p>{e(text)}</p>
<p class="actions"><a class="btn primary" href="{SITE['book']}">Book online</a>
<a class="btn ghost" href="tel:{SITE['tel']}">Call or text {e(SITE['phone'])}</a></p>
</div></section>"""


def inner(h1, lead, body):
    """Standard inner page: green header band with a keyboard edge, then a readable column."""
    lead_html = f'<p class="lead">{e(lead)}</p>' if lead else ""
    return f"""<section class="pagehead"><div class="wrap"><h1>{e(h1)}</h1>{lead_html}</div></section>
<section class="wrap prose">
{body}
</section>"""


PRICES = [
    ("Minimum Ear Tuning", "Basic tuning for everyday playing, or pianos that can't hold concert pitch", "$99"),
    ("Full Ear Tuning", "A fine tuning at concert pitch", "$199"),
    ("Pin setting add-on", "Re-tensions loose or low tuning pins", "+$70"),
    ("Repeat customer discount", "Full Ear Tuning within 18 months of your last tuning", "−$40"),
    ("New Piano Initial Prep", "Pin setting, fine tuning and minimum regulation for a new piano", "$495"),
    ("Minimum Regulation", "Action regulation to performance level", "$165"),
    ("D.S.H. Maintenance", "Calibration and adjustments. Paid in full by credit card when you book", "$179"),
    ("Repairs", "Sticky keys, broken strings and other acoustic repairs", "from $79"),
    ("Other work", "Full regulation, voicing, hammer mating and bigger projects", "Quote on request"),
]


def price_table():
    rows = "".join(
        f"<tr><th scope=\"row\">{e(a)}</th><td class=\"what\">{e(b)}</td><td class=\"price\">{e(c)}</td></tr>"
        for a, b, c in PRICES
    )
    return f"""<table class="prices">
<thead><tr><th>Service</th><th>What it covers</th><th>Price</th></tr></thead>
<tbody>{rows}</tbody></table>"""


# ---------- Playable keyboard (hero) ----------
# Keyboard range: F3 to E5 (MIDI 53 to 76)
FIRST, LAST = 53, 76
NOTE_NAMES = ["C", "C sharp", "D", "D sharp", "E", "F", "F sharp", "G", "G sharp", "A", "A sharp", "B"]
BLACK_PCS = {1, 3, 6, 8, 10}


def keyboard():
    whites = [m for m in range(FIRST, LAST + 1) if m % 12 not in BLACK_PCS]
    n = len(whites)
    w = 100 / n
    keys, blacks = [], []
    for i, m in enumerate(whites):
        name = f"{NOTE_NAMES[m % 12]} {m // 12 - 1}"
        keys.append(f'<button class="wk" type="button" data-midi="{m}" aria-label="{name}"></button>')
        if (m + 1) % 12 in BLACK_PCS and m + 1 <= LAST:
            bm = m + 1
            left = (i + 1) * w - w * 0.3
            bname = f"{NOTE_NAMES[bm % 12]} {bm // 12 - 1}"
            blacks.append(
                f'<button class="bk" type="button" data-midi="{bm}" aria-label="{bname}" '
                f'style="left:{left:.3f}%;width:{w * 0.6:.3f}%"></button>'
            )
    return f'<div class="keys" role="group" aria-label="Piano keyboard from F3 to E5, tap to play">{"".join(keys)}{"".join(blacks)}</div>'


KEY_JS = """
<script>
(function () {
  var ctx = null;
  // Recorded piano samples (CC BY 3.0, see audio/CREDITS.txt). Key = MIDI note of the recording.
  var SAMPLES = {54:'Fs3', 57:'A3', 60:'C4', 63:'Ds4', 66:'Fs4', 69:'A4', 72:'C5', 75:'Ds5', 78:'Fs5'};
  var raw = {}, bufs = {};
  function audio() {
    if (!ctx) { var C = window.AudioContext || window.webkitAudioContext; if (!C) return null; ctx = new C(); }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }
  function preload() {
    Object.keys(SAMPLES).forEach(function (m) {
      fetch('audio/' + SAMPLES[m] + '.mp3').then(function (r) { return r.arrayBuffer(); })
        .then(function (b) { raw[m] = b; }).catch(function () {});
    });
  }
  if (document.readyState === 'complete') preload(); else window.addEventListener('load', preload);
  function nearest(m) {
    var best = null;
    Object.keys(SAMPLES).forEach(function (r) { if (best === null || Math.abs(r - m) < Math.abs(best - m)) best = +r; });
    return best;
  }
  function withBuf(root, cb) {
    if (bufs[root]) return cb(bufs[root]);
    if (!raw[root]) return cb(null);
    ctx.decodeAudioData(raw[root].slice(0), function (b) { bufs[root] = b; cb(b); }, function () { cb(null); });
  }
  function synth(f, dur) {
    var t = ctx.currentTime, o = ctx.createOscillator(), g = ctx.createGain();
    o.type = 'triangle'; o.frequency.value = f;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(0.2, t + 0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g); g.connect(ctx.destination); o.start(t); o.stop(t + dur + 0.05);
  }
  function note(m, hold) {
    var c = audio(); if (!c) return;
    hold = hold || 2.6;
    var root = nearest(m);
    withBuf(root, function (b) {
      if (!b) { synth(440 * Math.pow(2, (m - 69) / 12), hold); return; }
      var t = c.currentTime, src = c.createBufferSource(), g = c.createGain();
      src.buffer = b;
      src.playbackRate.value = Math.pow(2, (m - root) / 12);
      g.gain.setValueAtTime(0.9, t);
      g.gain.setValueAtTime(0.9, t + hold - 0.9);
      g.gain.linearRampToValueAtTime(0.0001, t + hold);
      src.connect(g); g.connect(c.destination);
      src.start(t); src.stop(t + hold + 0.05);
    });
  }
  var keys = document.querySelectorAll('.keys button');
  var status = document.getElementById('pitch-status');
  var stars = {};
  document.querySelectorAll('.star').forEach(function (s) { stars[s.dataset.n] = s; });
  function lit(m) {
    var s = stars[m - 20]; if (!s) return;
    s.classList.add('lit'); setTimeout(function () { s.classList.remove('lit'); }, 900);
  }
  function down(el) { el.classList.add('down'); lit(+el.dataset.midi); }
  function up(el) { el.classList.remove('down'); }
  keys.forEach(function (k) {
    var m = +k.dataset.midi;
    k.addEventListener('pointerdown', function (ev) { ev.preventDefault(); down(k); note(m); });
    ['pointerup', 'pointerleave', 'pointercancel', 'blur'].forEach(function (n) { k.addEventListener(n, function () { up(k); }); });
    k.addEventListener('keydown', function (ev) {
      if ((ev.key === 'Enter' || ev.key === ' ') && !ev.repeat) { ev.preventDefault(); down(k); note(m); }
    });
    k.addEventListener('keyup', function () { up(k); });
  });
  var a = document.getElementById('play-a');
  if (a) a.addEventListener('click', function () {
    note(69, 4.5);
    var key = document.querySelector('.keys [data-midi="69"]');
    if (key) { key.classList.add('down'); setTimeout(function () { key.classList.remove('down'); }, 600); }
    lit(69);
    if (status) status.textContent = 'Playing concert A at 440 Hz';
  });
})();
</script>"""


import random


def starfield():
    rnd = random.Random(88)
    pts = [(rnd.uniform(2, 998), rnd.uniform(6, 494), rnd.choice([1.1, 1.4, 1.8, 2.3, 3.0]), rnd.uniform(.45, 1)) for _ in range(88)]
    pts.sort(key=lambda t: t[0])
    circles = "".join(
        f'<circle class="star" data-n="{i + 1}" cx="{x:.1f}" cy="{y:.1f}" r="{r}" opacity="{o:.2f}"/>'
        for i, (x, y, r, o) in enumerate(pts)
    )
    return f'<svg class="stars" viewBox="0 0 1000 500" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">{circles}</svg>'


PAGES = {}

# ---------------- Home ----------------
PAGES["index.html"] = (
    "Piano Tuner in Orange County and Cerritos",
    "Tuning and service for Bösendorfer, Yamaha, Disklavier, Silent and Hybrid pianos. Book online or call (657) 438-4984.",
    f"""<div class="sky">{starfield()}
<section class="hero"><div class="wrap">
<h1>Piano tuning and service for Bösendorfer, Yamaha, Disklavier, Silent and Hybrid pianos</h1>
<p class="lead">I'm Ryan Ellison, a Registered Piano Technician. After ten years with Yamaha pianos, I now tune and care for pianos in homes, schools and churches across Orange County, Riverside and the Gateway Cities.</p>
<p class="actions"><a class="btn primary" href="{SITE['book']}">Book online</a>
<a class="btn" href="tel:{SITE['tel']}">Call or text {e(SITE['phone'])}</a></p>
</div></section>
<section class="keybed" aria-label="Playable keyboard">
<div class="wrap">
{keyboard()}
<p class="keyhint"><button id="play-a" type="button" class="btn ghost small">Hear concert A (440 Hz)</button>
<span id="pitch-status" role="status">Tap the keys to play. Each key lights its star.</span></p>
</div>
</section>
</div>
<section class="wrap block harmony">
<h2>88 keys, 88 constellations</h2>
<blockquote class="quote"><p>The 88 piano keys make music.</p><footer>Neil deGrasse Tyson, <a href="https://neildegrassetyson.com/books/1994-05-menagerie/">"Menagerie"</a> (1994)</footer></blockquote>
<p class="big">A piano has 88 keys. The sky has 88 official constellations. Tyson sets them side by side and jokes that the sky's side is a zoo. In 1619, Johannes Kepler wrote <em>Harmonices Mundi</em>, "The Harmony of the World," arguing the planets moved in musical ratios. He never proved the planets sing, but the book gave us his third law of planetary motion.</p>
<p>Every piano I tune is my small attempt at harmony.</p>
</section>
<section class="wrap block">
<h2>What I work on</h2>
<ul class="work">
<li><a href="bosendorfer.html"><span class="name">Bösendorfer</span><span class="desc">Tuning, regulation and service with the care it deserves.</span></a></li>
<li><a href="disklavier-silent-hybrid.html"><span class="name">Disklavier, Silent and Hybrid</span><span class="desc">Calibration and repairs for the piano and its electronics.</span></a></li>
<li><a href="services.html"><span class="name">Yamaha grands and uprights</span><span class="desc">Ten years of daily work on grands and uprights.</span></a></li>
</ul>
</section>
<section class="reasons"><div class="wrap">
<h2>Why book with me</h2>
<div class="three">
<div><h3>At home with the tricky ones</h3>
<p>Bösendorfer, Disklavier, Silent and Hybrid pianos need someone who knows both the acoustic piano and the electronics. I do.</p></div>
<div><h3>Me, start to finish</h3>
<p>No dispatcher, no handoff. I tune, adjust and repair your piano myself.</p></div>
<div><h3>Price up front</h3>
<p>I confirm the price when you book. No surprises.</p></div>
</div>
</div></section>
<!-- REVIEWS: add one or two real Google/Yelp reviews here with the reviewer's permission. -->
<section class="wrap block">
<h2>Prices</h2>
<dl class="quick">
<div><dt>Minimum Ear Tuning</dt><dd>$99</dd></div>
<div><dt>Full Ear Tuning</dt><dd>$199</dd></div>
<div><dt>D.S.H. Maintenance</dt><dd>$179</dd></div>
</dl>
<p><a href="services.html">See all services and prices</a></p>
</section>
<section class="wrap block areas">
<h2>Where I work</h2>
<div class="three">
<div><h3><a href="orange-county.html">Orange County</a></h3><p>Irvine, Newport Beach, Huntington Beach, Fullerton and more</p></div>
<div><h3><a href="riverside-county.html">Riverside County</a></h3><p>Riverside and Corona</p></div>
<div><h3><a href="cerritos-la-county.html">Cerritos and LA County</a></h3><p>Cerritos, Norwalk, Artesia, La Mirada, Downey, Long Beach</p></div>
</div>
</section>
{cta()}""",
    True,
    KEY_JS,
)

# ---------------- Services ----------------
PAGES["services.html"] = (
    "Piano Tuning Prices and Services",
    "Ear tuning from $99, regulation, repairs and new piano prep. See prices and book online.",
    inner(
        "Services and prices",
        "Flat rates for the services below. Anything else is $99 an hour, with a $99 minimum service call. Payment is due at the time of service.",
        price_table()
        + '<p>Disklavier, Silent or Hybrid? See <a href="disklavier-silent-hybrid.html">D.S.H. service</a>.</p>',
    )
    + cta(),
)

# ---------------- D.S.H. ----------------
PAGES["disklavier-silent-hybrid.html"] = (
    "Disklavier and Silent Piano Service",
    "Calibration and repair for Disklavier, Silent and Hybrid pianos by a registered piano technician.",
    inner(
        "Service for Disklavier, Silent and Hybrid pianos",
        "These pianos add sensors, solenoids and electronics to an acoustic piano, and many tuners avoid them. After ten years with Yamaha pianos, this is what I do every day.",
        """<h2>What D.S.H. Maintenance includes ($179)</h2>
<ul>
<li>Calibration and table updates for the Disklavier, Silent or Hybrid system</li>
<li>Adjustments so playback, recording and silent mode work as they should</li>
<li>A check of the connected hardware</li>
</ul>
<p><strong>Repairs</strong> start at $79. For bigger electronic or mechanical problems, I quote before I start.</p>
<p><strong>Tuning is separate.</strong> Most people book an ear tuning with D.S.H. Maintenance in the same visit. D.S.H. Maintenance is paid in full by credit card when you book.</p>""",
    )
    + cta("Not sure what your piano needs? Call " + SITE["phone"] + " or book online and tell me the model."),
)

# ---------------- Bösendorfer ----------------
PAGES["bosendorfer.html"] = (
    "Bösendorfer Piano Tuning in Southern California",
    "Tuning, regulation and service for Bösendorfer pianos by a Registered Piano Technician. Book online or call (657) 438-4984.",
    inner(
        "Bösendorfer piano tuning and service",
        "A Bösendorfer deserves a technician who treats it like the fine instrument it is. I tune, regulate and service Bösendorfers across Orange County, Riverside County and southeast LA County.",
        """<ul>
<li>Full Ear Tuning at concert pitch ($199)</li>
<li>Regulation and other action work, quoted before I start</li>
<li>Repairs and condition checks, with a plain explanation</li>
</ul>
<p>See all <a href="services.html">services and prices</a>, or call or book online and tell me the model.</p>
<!-- TODO (Ryan): add the Bösendorfer models and the kinds of work you have done on them, if you want to name them. -->""",
    )
    + cta(),
)

# ---------------- Service area ----------------
PAGES["service-area.html"] = (
    "Piano Tuner in Orange County, Riverside and LA County",
    "Piano tuning across Orange County, Riverside County and southeast Los Angeles County. Book online or call (657) 438-4984.",
    inner(
        "Piano tuning in Orange County, Riverside County and southeast Los Angeles County",
        "I come to you: home, studio or school.",
        f"""<div class="three areas">
<div><h3><a href="orange-county.html">Orange County</a></h3><p>Irvine, Newport Beach, Huntington Beach, Buena Park, Yorba Linda, Fullerton and more</p></div>
<div><h3><a href="riverside-county.html">Riverside County</a></h3><p>Riverside, Corona</p></div>
<div><h3><a href="cerritos-la-county.html">Cerritos and LA County</a></h3><p>Cerritos, Norwalk, Artesia, La Mirada, Downey, Long Beach</p></div>
</div>
<p>Don't see your city? Call {e(SITE['phone'])}. I can often still fit you in.</p>""",
    )
    + cta(),
)

AREA_NOTE = (
    f"<p>Don't see your city? Call {e(SITE['phone'])}. I can often still fit you in.</p>"
    '<p><a href="services.html">Services and prices</a><br><a href="disklavier-silent-hybrid.html">Disklavier, Silent and Hybrid</a></p>'
)

PAGES["orange-county.html"] = (
    "Piano Tuner in Orange County, CA",
    "Piano tuning in Irvine, Newport Beach, Huntington Beach, Fullerton and nearby. Book online.",
    inner(
        "Piano tuner in Orange County",
        "I come to you: home, studio or school. Where I work most:",
        "<p>Irvine, Newport Beach, Huntington Beach, Buena Park, Yorba Linda, Fullerton, La Habra, Mission Viejo, Laguna Hills, San Clemente, Costa Mesa</p>"
        + AREA_NOTE,
    )
    + cta(),
)

PAGES["riverside-county.html"] = (
    "Piano Tuner in Riverside and Corona",
    "Piano tuning and service in Riverside and Corona. Book online or call (657) 438-4984.",
    inner(
        "Piano tuner in Riverside and Corona",
        "I come to you: home, studio or school. Where I work most: Riverside and Corona.",
        AREA_NOTE,
    )
    + cta(),
)

PAGES["cerritos-la-county.html"] = (
    "Piano Tuner in Cerritos and Norwalk",
    "Piano tuning in Cerritos, Norwalk, Artesia, La Mirada, Downey and Long Beach.",
    inner(
        "Piano tuner in Cerritos, Norwalk and southeast LA County",
        "I come to you: home, studio or school. Where I work most:",
        "<p>Cerritos, Norwalk, Artesia, La Mirada, Downey, Long Beach</p>" + AREA_NOTE,
    )
    + cta(),
)

# ---------------- About ----------------
PAGES["about.html"] = (
    "About Ryan Ellison, RPT",
    "Registered Piano Technician with ten years of Yamaha experience, specializing in Bösendorfer, Yamaha and Disklavier pianos.",
    inner(
        "Meet Ryan Ellison, RPT",
        "",
        """<!-- PHOTO: add a clear photo of yourself at work. -->
<h2>A musical family</h2>
<p class="big">I like to think my journey into piano technology started at birth. Both my parents were high-school orchestra directors and conductors, so practicing music was a requirement from about age eight. I sang in a children's choir, took piano lessons, and at twelve picked up the string bass like my dad. I played it through college, in orchestras, jazz bands and every kind of ensemble under the sun.</p>
<p>After fifteen years of studying and performing, I decided to go in a different direction.</p>

<h2>Finding piano tuning</h2>
<p>After college I worked at a music store in north Denver and learned to repair woodwinds, brass, guitars, strings and electronics. By 2010 the store was downsizing, and I took a leap of faith on a curiosity: piano tuning. We kept referring tuning calls to local technicians, and when I ran into the Piano Technicians Guild, something clicked. I thought, "I bet I can do this."</p>
<p>So I took my father's amateur tuning tools (which, technically, makes me a second-generation tuner), a guitar tuner and a YouTube video to my family's Baldwin console. Nope! The piano ended up far worse than when I started. You can't learn to tune a piano without formal training.</p>

<h2>Chicago</h2>
<p>After one very important phone call, I enrolled at the Chicago School for Piano Technology in August 2011. At 26, I left my path as a musician and moved to Chicago, to a school on the second floor of a historic Ukrainian Village warehouse. One rigorous year and more than 1,100 hours of classwork and skills testing taught me aural tuning, regulation and repair.</p>

<h2>Starting out in Denver</h2>
<p>I launched my first tuning business in Denver in October 2012, sure my old musician friends would send plenty of work. Wrong! I knew guitarists, horn players and drummers, and zero pianists. So I did what every tuner does: pounded the pavement, posted Craigslist ads and called piano stores.</p>
<p>A local piano store owner gave me a chance, long hair and all. His shop sold fine new European pianos and Yamahas, and rebuilt large Steinway and Baldwin grands. Over three years there, I also built a private clientele of about 300 pianos.</p>

<h2>West to Los Angeles, and Yamaha</h2>
<p>By late 2015 I was heading west. After three hard-fought years building my own business, the LA competition intimidated me, so I looked for a job at a piano store. Two trips later, I had nothing. My last appointment on my last trip was with a Yamaha dealer in Van Nuys, who told me Yamaha was hiring. That was another call I'm glad I made. In December 2015, I started at Yamaha in Buena Park.</p>
<p>There I had to start over, un-learning old habits and learning the Yamaha method from the beginning: unison, octave, fifth, fourth, and a slow-beating temperament. A marvelous technician from Osaka brought projection tuning to the US, and his pianos sounded calm and powerful at once. It changed how I hear a piano.</p>
<p>It all comes full circle. I started with nothing but a tuning lever in my pocket, and now I'm taking everything I've learned back to where it began: just me, my tools and your piano. There's more to come.</p>

<h2>Credentials</h2>
<ul>
<li>Registered Piano Technician, Piano Technicians Guild (2017)</li>
<li>Grand Piano Master Course, Yamaha Piano Technical Academy, Japan (2019)</li>
<li>Grand Piano Course, Yamaha Piano Technical Academy, Japan (2017)</li>
<li>Chicago School for Piano Technology (2012)</li>
<li>Bachelor of Music (2007)</li>
</ul>
<p><strong>Specialties:</strong> Yamaha grand and upright pianos, Disklavier, Silent and Hybrid pianos, and Bösendorfer pianos.</p>
<p><strong>What I care about:</strong> A piano that holds its tuning, feels even under the fingers, and sounds the way it should. I'll tell you plainly what your piano needs, and what it doesn't.</p>""",
    )
    + cta(),
)

# ---------------- Bellharp ----------------
PAGES["bellharp.html"] = (
    "The Bellharp: Bell-Like Piano Tone",
    "My ideas on achieving bell-like tone in the modern grand piano through aural tuning and regulation by ear.",
    inner(
        "The Bellharp",
        "My ideas on achieving bell-like tone in the modern grand piano. #hammerbellharp #bellharp",
        """<h2>A golden age of piano technology</h2>
<p>Modern grand pianos are in a class of their own compared with those of just a few decades ago: more powerful yet more subtle, with faster keyboards made from better materials. In my opinion, they have moved so far past their predecessors that the instrument is on the verge of being redefined.</p>

<h2>My Bellharp concept</h2>
<p>I believe a bell-like essence is built into the grand piano's design, like a seed lying dormant.</p>
<blockquote class="quote"><p>To play the piano is to play a chromatic keyed bell.</p></blockquote>
<p>So how do I draw out that bell tone? By focusing the instrument's energy through tuning and regulation.</p>

<h2>Tuning</h2>
<p>Aural tuning is a key principle of bell tone. I start from an external pitch, a Japanese tuning fork, matched to the piano's A4. Then I build the tuning note by note, like a cell dividing, each note derived from the one before it.</p>
<h3>The temperament, the heart of the piano</h3>
<p>The 12-note temperament, tuned in the third and fourth octaves, sets the width of the twelve base tones. I tune it in a circular pattern so every note relates to its neighbors, then tune the octaves above and below by ear. This fully aural method brings out the bell characteristics already in the frame.</p>

<h2>Tensioning the Bellharp so it sings</h2>
<p>Because I believe the frame is a major part of piano sound, I tension it firmly. If a tuning pin is lax, the string doesn't pull on the frame as it should, and the sound suffers.</p>

<h2>How I picture the piano</h2>
<p>I picture the grand piano as a tetrahedron, a shape that holds the sound like a vessel, with the cast-iron frame, the real bellharp, at its center.</p>

<h2>The action, regulated by ear</h2>
<p>If the piano is a chromatic keyed bell, the modern double-escapement action is its clapper: a sophisticated hammer mechanism that strikes the bell and sets it resonating. Every small deviation from specification costs some beauty of sound, so I regulate by listening, judging how the touch affects what the musician hears. I bed the keyboard solidly, then use my ear to find the ratio of key depth to striking distance that gives the liveliest bell tone. Every piano is unique.</p>

<p class="big">Then I sit back and enjoy. Let the piano do its magic under your fingers.</p>""",
    )
    + cta("Curious what this could do for your piano? Call " + SITE["phone"] + " or book online."),
)

# ---------------- FAQ ----------------
FAQ = [
    ("How often should I tune my piano?", "Twice a year for most pianos, and at least once a year. New or recently moved pianos need it more often in the first year."),
    ("How long does a tuning take?", "A Full Ear Tuning usually takes about two hours. A Minimum Ear Tuning takes about an hour."),
    ("Can I tune my piano myself?", "I tried it with a guitar tuner and a YouTube video, and made my family's piano worse. Tuning takes training and the right tools. Call me instead."),
    ("What is the difference between Minimum and Full Ear Tuning?", "Full brings your piano to concert pitch. Minimum is a basic tuning for everyday playing, or for older pianos that can't safely be brought up to pitch."),
    ("What if my piano has not been tuned in years?", "It has probably gone flat and may need the pin setting add-on (+$70) to hold a tuning. I'll tell you what I find before I start."),
    ("Can tuning damage an old piano?", "Pianos are under very high string tension, and old parts can fail during tuning. I explain the risks first and repair what I can on the spot. The service form has the full terms."),
    ("How do I pay?", "Cash, check, Zelle, Venmo or card, all at the same price. The exception is D.S.H. Maintenance, which is paid in full by credit card when you book and applied to your final bill."),
]
faq_html = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in FAQ)
faq_ld = ",".join(
    '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
    % (json.dumps(q, ensure_ascii=False), json.dumps(a, ensure_ascii=False))
    for q, a in FAQ
)
PAGES["faq.html"] = (
    "Piano Tuning FAQ",
    "How often to tune a piano, how long tuning takes, pricing and payment. Answers from Ryan Ellison, RPT.",
    inner("Frequently asked questions", "", faq_html)
    + f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{faq_ld}]}}</script>'
    + cta(),
)

# ---------------- Contact ----------------
PAGES["contact.html"] = (
    "Contact and Book a Piano Tuning",
    "Book your piano tuning online or call (657) 438-4984. Ryan Ellison Piano, serving Orange County, Riverside and LA County.",
    inner(
        "Book your piano tuning",
        "",
        f"""<p><a class="btn primary" href="{SITE['book']}">Book online</a></p>
<ul class="plain">
<li><strong>Call or text:</strong> <a href="tel:{SITE['tel']}">{e(SITE['phone'])}</a></li>
<li><strong>Business:</strong> {e(SITE['name'])} ({e(SITE['legal'])}), {e(SITE['street'])}, {e(SITE['city'])}, {e(SITE['state'])} {e(SITE['zip'])}</li>
<li><strong>Hours:</strong> Monday, Tuesday, Thursday, Friday and Saturday, 9:00 am to 5:00 pm. Closed Wednesday and Sunday.</li>
</ul>""",
    ),
)

CSS = """
:root{
  --key:#fcfcfa; --ebony:#1b1d22; --felt:#1a2147; --felt-d:#0f1430; --brass:#e0b95a; --brass-d:#7a5c1e; --rule:#a07f20; --steel:#e9ecf4; --muted:#555d66;
  --display:"Bricolage Grotesque","Avenir Next","Segoe UI",system-ui,sans-serif;
  --body:"Source Serif 4",Charter,"Bitstream Charter",Georgia,serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font:1.125rem/1.7 var(--body);color:var(--ebony);background:var(--key);padding-bottom:64px}
h1,h2,h3{font-family:var(--display);color:var(--ebony);line-height:1.1;letter-spacing:-.02em;margin:0}
h1{font-size:clamp(2.1rem,5.2vw,3.9rem);font-weight:700;max-width:22ch}
h2{font-size:clamp(1.6rem,3.4vw,2.2rem);font-weight:700;margin:0 0 .7em}
h3{font-size:1.25rem;font-weight:700;letter-spacing:-.01em;margin:1.6em 0 .3em}
p{margin:0 0 1em;max-width:62ch}
a{color:var(--felt)}
a:hover{color:var(--brass-d)}
:focus-visible{outline:3px solid var(--brass);outline-offset:3px}
.wrap{max-width:1160px;margin:0 auto;padding:0 20px}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:#fff;padding:8px;z-index:20}

/* header */
.site-header{background:var(--key);border-bottom:1px solid #dfe3e0}
.bar{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding-top:12px;padding-bottom:12px}
.brand{font-family:var(--display);font-weight:700;font-size:1.35rem;letter-spacing:-.02em;color:var(--ebony);text-decoration:none;margin-right:auto;line-height:1.1}
.brand small{display:block;font:500 .78rem var(--display);letter-spacing:0;color:var(--muted);margin-top:2px}
.nav{display:none;width:100%;flex-direction:column;order:5;padding:6px 0 10px}
.nav a{font-family:var(--display);font-weight:500;color:var(--ebony);text-decoration:none;padding:10px 0;border-top:1px solid #e3e6e4}
.nav a[aria-current]{color:var(--felt);font-weight:700}
.phone{display:none}
.menu-toggle{position:absolute;opacity:0}
.menu-btn{cursor:pointer;font:500 .95rem var(--display);border:1.5px solid var(--ebony);border-radius:6px;padding:6px 12px}
.menu-toggle:checked ~ .nav{display:flex}
.menu-toggle:focus-visible ~ .menu-btn{outline:3px solid var(--brass);outline-offset:2px}

/* buttons */
.btn{display:inline-block;font:700 1rem var(--display);padding:12px 20px;border-radius:6px;border:2px solid var(--ebony);color:var(--ebony);background:transparent;text-decoration:none;margin:0 8px 8px 0;cursor:pointer}
.btn:hover{color:var(--ebony);background:#fff}
.btn.primary{background:var(--brass);border-color:var(--brass);color:var(--ebony)}
.btn.primary:hover{background:#c29a4a;border-color:#c29a4a}
.btn.ghost{border-color:#fff;color:#fff}
.btn.ghost:hover{background:#fff;color:var(--felt)}
.btn.small{padding:8px 14px;font-size:.92rem;margin:0}
.actions{margin:1.4em 0 0}

/* hero */
.sky{position:relative;background:radial-gradient(120% 90% at 70% 0%,#26306b 0%,#1a2147 45%,#0f1430 100%);color:#fff;overflow:hidden}
.stars{position:absolute;inset:0;width:100%;height:100%;opacity:.55;-webkit-mask-image:linear-gradient(90deg,rgba(0,0,0,.25),#000 70%);mask-image:linear-gradient(90deg,rgba(0,0,0,.25),#000 70%)}
@media(min-width:900px){.stars{opacity:1;-webkit-mask-image:linear-gradient(90deg,rgba(0,0,0,.12) 0,rgba(0,0,0,.2) 40%,#000 75%);mask-image:linear-gradient(90deg,rgba(0,0,0,.12) 0,rgba(0,0,0,.2) 40%,#000 75%)}}
.star{fill:#f6efd6;transform-box:fill-box;transform-origin:center;transition:transform .25s,fill .25s}
.star.lit{fill:#ffe08a;transform:scale(3.4);filter:drop-shadow(0 0 5px #ffd770)}
.sky .hero,.sky .keybed{position:relative}
.sky h1{color:#fff}
.sky .lead{color:#d5daf0}
.sky .btn:not(.primary){border-color:#fff;color:#fff}
.sky .btn:not(.primary):hover{background:#fff;color:var(--felt)}
.harmony{padding-top:56px}
.harmony .big{font-size:1.3rem;line-height:1.6;max-width:56ch}
.quote{margin:1.2em 0 1.4em;padding:4px 0 4px 20px;border-left:4px solid var(--rule);max-width:56ch}
.quote p{font:700 clamp(1.5rem,3.4vw,2.1rem)/1.2 var(--display);letter-spacing:-.02em;margin:0 0 .4em}
.quote footer{color:var(--muted);font-size:1rem}
.hero{padding:56px 0 44px}
.hero .lead{font-size:1.3rem;max-width:44ch;margin-top:1.2em}
.keybed{background:transparent;padding:26px 0 22px;border-bottom:6px solid var(--brass)}
.keys{position:relative;display:flex;height:clamp(120px,22vw,190px);background:var(--ebony);padding:0 2px 3px;border-radius:0 0 8px 8px;user-select:none;-webkit-user-select:none;touch-action:manipulation}
.wk{flex:1;border:0;border-right:1px solid #9aa09c;background:linear-gradient(#fff,#f3f2ec 85%,#d9d6c8);border-radius:0 0 5px 5px;padding:0;cursor:pointer;margin:0 .5px}
.wk:last-of-type{border-right:0}
.bk{position:absolute;top:0;height:62%;border:0;border-radius:0 0 4px 4px;background:linear-gradient(#34373d,#0f1013);cursor:pointer;padding:0;z-index:2;box-shadow:0 2px 3px rgba(0,0,0,.5)}
.wk.down{background:linear-gradient(#e9e6d6,#d5d1bd);transform:translateY(2px)}
.bk.down{background:#000;transform:translateY(2px)}
.keyhint{display:flex;align-items:center;gap:14px;flex-wrap:wrap;color:#dfe8e5;font:500 .95rem var(--display);margin:16px 0 0;max-width:none}

/* body sections */
.block{padding-top:56px;padding-bottom:20px}
.work{list-style:none;margin:0;padding:0;border-top:3px solid var(--ebony)}
.work li{border-bottom:1px solid #cfd4d1}
.work a{display:grid;gap:4px;padding:22px 4px;text-decoration:none;color:var(--ebony)}
.work .name{font:700 clamp(1.5rem,3.4vw,2.3rem)/1.1 var(--display);letter-spacing:-.02em}
.work .desc{color:var(--muted);max-width:52ch}
.work a:hover .name{color:var(--felt);text-decoration:underline;text-decoration-color:var(--rule);text-decoration-thickness:3px;text-underline-offset:6px}
.reasons{background:var(--steel);margin-top:48px;padding:56px 0 40px}
.three{display:grid;gap:8px 40px;grid-template-columns:1fr}
.three h3{margin-top:.9em;padding-top:14px;border-top:4px solid var(--rule)}
.three p{max-width:36ch}
.three h3 a{color:var(--ebony)}
.quick{margin:0 0 1em;max-width:560px}
.quick div{display:flex;justify-content:space-between;align-items:baseline;gap:20px;padding:12px 0;border-bottom:1px solid #cfd4d1}
.quick dt{font-family:var(--body)}
.quick dd{margin:0;font:700 1.6rem var(--display)}
.areas{padding-bottom:48px}

/* inner pages */
.pagehead{position:relative;background:radial-gradient(120% 140% at 80% 0%,#26306b 0%,#1a2147 55%,#0f1430 100%);padding:52px 0 76px}
.pagehead::before{content:"";position:absolute;inset:0;opacity:.8;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='260' height='140'%3E%3Cg fill='%23f6efd6'%3E%3Ccircle cx='20' cy='30' r='1.2'/%3E%3Ccircle cx='70' cy='95' r='1.8' opacity='.7'/%3E%3Ccircle cx='120' cy='20' r='1' opacity='.8'/%3E%3Ccircle cx='160' cy='70' r='2.2' opacity='.6'/%3E%3Ccircle cx='210' cy='120' r='1.2'/%3E%3Ccircle cx='235' cy='40' r='1.6' opacity='.7'/%3E%3Ccircle cx='100' cy='125' r='1' opacity='.7'/%3E%3C/g%3E%3C/svg%3E")}
.pagehead .wrap{position:relative}
.pagehead h1,.pagehead .lead{color:#fff}
.pagehead .lead{font-size:1.2rem;max-width:56ch;margin:1em 0 0;color:#dfe8e5}
.pagehead::after{content:"";position:absolute;left:0;right:0;bottom:0;height:30px;border-top:4px solid var(--brass);
  background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='30' viewBox='0 0 140 30'%3E%3Crect width='140' height='30' fill='%23fcfcfa'/%3E%3Cpath d='M20 0V30M40 0V30M60 0V30M80 0V30M100 0V30M120 0V30' stroke='%231b1d22' stroke-opacity='.35'/%3E%3Cg fill='%231b1d22'%3E%3Crect x='14' width='12' height='18'/%3E%3Crect x='34' width='12' height='18'/%3E%3Crect x='74' width='12' height='18'/%3E%3Crect x='94' width='12' height='18'/%3E%3Crect x='114' width='12' height='18'/%3E%3C/g%3E%3C/svg%3E") repeat-x left bottom/140px 30px}
.prose{padding-top:44px;padding-bottom:56px}
.prose h2{margin-top:1.6em}
.prose ul{max-width:62ch;padding-left:1.2em}
.prose li{margin:.4em 0}
.prose .big{font-size:1.3rem;line-height:1.6;max-width:56ch}
.prose h3+p{margin-top:0}
ul.plain{list-style:none;padding:0}ul.plain li{margin:.8em 0}
.areas.three h3{margin-top:.2em}
table.prices{width:100%;border-collapse:collapse;margin:8px 0 24px}
table.prices thead{position:absolute;left:-9999px}
table.prices tr{display:grid;grid-template-columns:1fr auto;gap:0 16px;padding:16px 0;border-bottom:1px solid #cfd4d1}
table.prices th,table.prices td{display:block;text-align:left;padding:0;font-weight:400}
table.prices th{font:700 1.2rem var(--display);letter-spacing:-.01em}
table.prices .what{grid-column:1/2;grid-row:2;color:var(--muted);max-width:56ch}
table.prices .price{grid-column:2;grid-row:1/3;align-self:center;font:700 1.5rem var(--display);white-space:nowrap}

.cta{background:var(--ebony);color:#fff;padding:44px 0}
.cta p{color:#fff;font:500 1.35rem var(--display);max-width:none}
.cta .actions{margin-top:1em}

.site-footer{background:var(--felt-d);color:#c9d6d2;padding:36px 0 20px;font-size:1rem;line-height:1.6}
.site-footer a{color:#f0d79b}
.site-footer strong{display:block;font:700 1rem var(--display);color:#fff;margin-bottom:4px}
.cols{display:grid;gap:22px;grid-template-columns:1fr}
.fine{margin-top:26px;font-size:.88rem;opacity:.75}

.mobilebar{position:fixed;left:0;right:0;bottom:0;display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:8px 12px;background:var(--key);border-top:1px solid #cfd4d1;z-index:10}
.mobilebar .btn{margin:0;text-align:center}

@media(min-width:900px){
  body{padding-bottom:0}
  .mobilebar{display:none}
  .nav{display:flex;flex-direction:row;width:auto;order:0;gap:20px;padding:0}
  .nav a{border:0;padding:4px 0;font-size:.93rem}
  .nav a:hover{text-decoration:underline;text-decoration-color:var(--brass);text-decoration-thickness:2px;text-underline-offset:5px}
  .menu-btn{display:none}
  .phone{display:inline-block;font:700 .98rem var(--display);color:var(--felt);text-decoration:none}
  .three{grid-template-columns:repeat(3,1fr)}
  .cols{grid-template-columns:1.2fr 1.2fr .8fr}
  .work a{grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:40px;align-items:baseline}
  .hero{padding:84px 0 64px}
  .pagehead{padding:72px 0 96px}
}
@media(min-width:900px) and (max-width:1219px){
  .nav{display:none;width:100%;flex-direction:column;order:5;padding:6px 0 10px;gap:0}
  .menu-toggle:checked ~ .nav{display:flex}
  .nav a{border-top:1px solid #e3e6e4;padding:10px 0;font-size:1rem}
  .menu-btn{display:inline-block}
}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for fname, page in PAGES.items():
        title, desc, body = page[0], page[1], page[2]
        schema = len(page) > 3 and page[3]
        script = page[4] if len(page) > 4 else ""
        with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
            f.write(layout(fname, title, desc, body, schema, script))
    shutil.copytree(os.path.join(HERE, "audio_src"), os.path.join(OUT, "audio"))
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
