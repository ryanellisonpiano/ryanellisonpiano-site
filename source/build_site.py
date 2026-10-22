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
    ("yamaha-upright-rental.html", "Rentals"),
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
    "dayOfWeek": ["Saturday"],
    "opens": "09:00",
    "closes": "17:00"
  }}, {{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "18:00",
    "closes": "20:00"
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
      Saturday 9:00 am to 5:00 pm<br>Weekday evenings by appointment<br>Closed Sunday
    </div>
    <div>
      <strong>Book</strong>
      <a href="{SITE['book']}">Book online</a><br>
      <a href="services.html">Prices</a><br>
      <a href="faq.html">Questions</a>
    </div>
  </div>
  <div class="wrap fine">&copy; 2026 {e(SITE['name'])}, a service of {e(SITE['legal'])}. Registered Piano Technician, Piano Technicians Guild.<br>Piano sounds: Salamander Grand Piano by Alexander Holm, <a href="https://creativecommons.org/licenses/by/3.0/">CC BY 3.0</a>. Sky data: <a href="d3-celestial-LICENSE.txt">d3-celestial</a> by Olaf Frohn.</div>
</footer>
<div class="mobilebar">
  <a class="btn" href="tel:{SITE['tel']}">Call</a>
  <a class="btn primary" href="{SITE['book']}">Book online</a>
</div>{script}{PRICE_JS}
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


# ---------- Pricing: one schedule drives every price on the site ----------
import datetime as dt
import math

BASE = {"min": 99, "full": 199, "pin": 70, "disc": -40, "prep": 495, "reg": 165, "dsh": 179}
ADJ = ["full", "pin", "prep", "reg", "dsh"]          # prices that move with the holiday ramp and demand
RAMP_START, RAMP_END = dt.date(2026, 11, 1), dt.date(2026, 12, 24)
RAMP_PCT, POST_PCT, ROUND_TO = 0.15, 0.0, 5          # keep in sync with the Pricing_Tracker_2026 Settings tab
MAX_CHANGE, MIN_CHANGE = 0.25, -0.15
# Weekly demand overrides, keyed by the Monday of the week: {dt.date(2026, 11, 9): -0.10}
DEMAND = {}


# Rounding style per service: "nine" ends in 9 ($199, $209), "five" ends in 5 ($495, $505), "step" is a multiple of $5.
STYLE = {"full": "nine", "dsh": "nine", "prep": "five", "reg": "five", "pin": "step"}


def rnd(x):
    return int(math.floor(x + 0.5))


def mround(x, style):
    if style == "nine":
        return rnd((x - 9) / 10) * 10 + 9
    if style == "five":
        return rnd((x - 5) / 10) * 10 + 5
    return rnd(x / ROUND_TO) * ROUND_TO


def ramp_pct(d):
    if d > RAMP_END:
        return POST_PCT
    return max(0.0, min(1.0, (d - RAMP_START).days / (RAMP_END - RAMP_START).days)) * RAMP_PCT


def week_prices(monday):
    total = min(MAX_CHANGE, max(MIN_CHANGE, ramp_pct(monday) + DEMAND.get(monday, 0.0)))
    return {k: (mround(BASE[k] * (1 + total), STYLE[k]) if k in ADJ else BASE[k]) for k in BASE}


def monday_of(d):
    return d - dt.timedelta(days=d.weekday())


FIRST_WEEK = dt.date(2026, 11, 2)
WEEKS = [FIRST_WEEK + dt.timedelta(days=7 * i) for i in range(13)]   # Nov 2 to Jan 25
SCHEDULE = {w.isoformat(): week_prices(w) for w in WEEKS}
SCHEDULE["base"] = dict(BASE)
NOW = week_prices(monday_of(dt.date.today()))               # static fallback; the page script updates it by visitor date


def money(k, v):
    return ("+" if k == "pin" and v >= 0 else "") + ("\u2212$%d" % abs(v) if v < 0 else "$%d" % v)


def ps(key):
    """A price that the page script keeps current."""
    return f'<span data-price="{key}">{money(key, NOW[key])}</span>'


PRICE_JS = """
<script>
(function () {
  var S = __SCHEDULE__;
  var keys = Object.keys(S).filter(function (k) { return k !== 'base'; }).sort();
  function iso(d) { return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  var t = new Date(); t = new Date(t.getFullYear(), t.getMonth(), t.getDate());
  t.setDate(t.getDate() - ((t.getDay() + 6) % 7));
  var m = iso(t), cur = null;
  keys.forEach(function (k) { if (k <= m) cur = k; });
  var P = cur ? S[cur] : S.base;
  document.querySelectorAll('[data-price]').forEach(function (el) {
    var k = el.dataset.price; if (P[k] == null) return;
    el.textContent = (k === 'pin' ? '+' : '') + '$' + P[k];
  });
  var row = cur && document.querySelector('tr[data-week="' + cur + '"]');
  if (row) row.classList.add('now');
})();
</script>""".replace("__SCHEDULE__", json.dumps(SCHEDULE))

PRICES = [
    ("Minimum Ear Tuning", "Basic tuning for everyday playing, or pianos that can't hold concert pitch", "min"),
    ("Full Ear Tuning", "Fine tuning at concert pitch", "full"),
    ("Pin setting add-on", "Re-tensions loose or low tuning pins", "pin"),
    ("Repeat customer discount", "Full Ear Tuning within 18 months of your last tuning", "disc"),
    ("New Piano Initial Prep", "Pin setting, fine tuning and minimum regulation for a new piano", "prep"),
    ("Minimum Regulation", "Action regulation to performance level", "reg"),
    ("D.S.H. Maintenance", "Calibration and adjustments. Paid in full by credit card when you book", "dsh"),
    ("Repairs", "Sticky keys, broken strings and other acoustic repairs", "from $79"),
    ("Other work", "Full regulation, voicing, hammer mating and bigger projects", "Quote on request"),
]


def price_table():
    rows = ""
    for name, desc, key in PRICES:
        cell = ps(key) if key in BASE and key not in ("min", "disc") else (money(key, BASE[key]) if key in BASE else key)
        rows += f"<tr><th scope=\"row\">{e(name)}</th><td class=\"what\">{e(desc)}</td><td class=\"price\">{cell}</td></tr>"
    return f"""<table class="prices">
<thead><tr><th>Service</th><th>What it covers</th><th>Price</th></tr></thead>
<tbody>{rows}</tbody></table>"""


CAL_HTML = """
<section id="cal-section" hidden>
<h2>Pick your day</h2>
<p>Saturdays are my main service days. Weekday evenings, around 6 pm, are available near Cerritos, Los Angeles and Orange County by appointment. Tap a day to see its price.</p>
<div class="cal-tabs" id="cal-tabs" role="tablist">
<button type="button" data-a="la" class="on">Cerritos &amp; LA</button>
<button type="button" data-a="oc">Irvine &amp; Orange County</button>
<button type="button" data-a="far">Riverside &amp; beyond</button>
</div>
<div class="cal-key"><span><i class="gr"></i>Saturday</span><span><i class="ye"></i>Evening (about 6 pm)</span><span><i class="or"></i>Limited</span><span><i class="na"></i>Closed</span></div>
<div id="cal"></div>
<div id="cal-info" aria-live="polite">Select a day.</div>
<p><a class="btn primary" href="__BOOK__">Book online</a></p>
</section>
<script>
(function () {
  var S = __SCHEDULE__, keys = Object.keys(S).filter(function (k) { return k !== 'base'; }).sort();
  var area = 'la', END = new Date(2026, 11, 24);
  var now = new Date(), today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  if (today > END) return;
  document.getElementById('cal-section').hidden = false;
  function iso(d) { return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function wk(d) { var t = new Date(d); t.setDate(t.getDate() - ((t.getDay() + 6) % 7)); var m = iso(t), c = null; keys.forEach(function (k) { if (k <= m) c = k; }); return c; }
  function cls(d) { var w = d.getDay(); if (w === 0) return 'na'; if (w === 6) return area === 'far' ? 'ye' : 'gr'; return area === 'far' ? 'or' : 'ye'; }
  function draw() {
    var out = '', y = today.getFullYear(), m = today.getMonth();
    while (new Date(y, m, 1) <= END) {
      var first = new Date(y, m, 1), n = new Date(y, m + 1, 0).getDate();
      out += '<div class="cal-m"><h3>' + first.toLocaleString('en', { month: 'long' }) + ' ' + y + '</h3><div class="cal-g">';
      'MTWTFSS'.split('').forEach(function (x) { out += '<div class="cd hd">' + x + '</div>'; });
      for (var i = 0; i < (first.getDay() + 6) % 7; i++) out += '<div class="cd xx"></div>';
      for (var d = 1; d <= n; d++) {
        var dt = new Date(y, m, d);
        if (dt < today || dt > END) { out += '<div class="cd xx"></div>'; continue; }
        var c = cls(dt);
        out += '<div class="cd ' + c + '" data-d="' + iso(dt) + '" data-c="' + c + '" role="button" tabindex="0">' + d + '</div>';
      }
      out += '</div></div>';
      m++; if (m > 11) { m = 0; y++; }
    }
    document.getElementById('cal').innerHTML = out;
  }
  function pick(t) {
    if (!t || !t.dataset.d || t.dataset.c === 'na') return;
    document.querySelectorAll('.cd.sel').forEach(function (x) { x.classList.remove('sel'); });
    t.classList.add('sel');
    var d = new Date(t.dataset.d + 'T12:00'), k = wk(d), P = k ? S[k] : S.base;
    var msg = { gr: 'Saturday appointment.', ye: area === 'far' ? 'Saturday trip. Call or text to confirm.' : 'Evening appointment, about 6 pm.', or: 'Limited in your area. Call or text to ask.' }[t.dataset.c];
    document.getElementById('cal-info').innerHTML = '<b>' + d.toLocaleDateString('en', { weekday: 'long', month: 'long', day: 'numeric' }) + '</b><br>' + msg + '<br>Full Ear Tuning $' + P.full + ' &middot; Pin setting +$' + P.pin;
  }
  document.getElementById('cal-tabs').addEventListener('click', function (e) {
    if (!e.target.dataset.a) return; area = e.target.dataset.a;
    document.querySelectorAll('#cal-tabs button').forEach(function (b) { b.classList.toggle('on', b === e.target); });
    draw(); document.getElementById('cal-info').textContent = 'Select a day.';
  });
  document.getElementById('cal').addEventListener('click', function (e) { pick(e.target.closest('.cd')); });
  document.getElementById('cal').addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(e.target.closest('.cd')); } });
  draw();
})();
</script>""".replace("__SCHEDULE__", json.dumps(SCHEDULE)).replace("__BOOK__", SITE["book"])


def schedule_table():
    cols = [("full", "Full Ear Tuning"), ("pin", "Pin setting"), ("prep", "New piano prep"), ("reg", "Min. regulation"), ("dsh", "D.S.H.")]
    head = "".join(f"<th>{e(n)}</th>" for _, n in cols)
    rows = ""
    holiday = [w for w in WEEKS if w <= dt.date(2026, 12, 21)]
    for w in holiday:
        pr = SCHEDULE[w.isoformat()]
        label = "Week of " + w.strftime("%b ") + str(w.day)
        rows += f'<tr data-week="{w.isoformat()}"><td>{label}</td>' + "".join(f"<td>{money(k, pr[k])}</td>" for k, _ in cols) + "</tr>"
    after = SCHEDULE[dt.date(2026, 12, 28).isoformat()]
    rows += '<tr data-week="2026-12-28"><td>Dec 28 onward</td>' + "".join(f"<td>{money(k, after[k])}</td>" for k, _ in cols) + "</tr>"
    return f"""<h2>Book early, pay less</h2>
<p>Holiday prices rise a little each week until Dec 24, then return to standard. The price I confirm when you book is the price you pay.</p>
<div class="sched-wrap"><table class="sched"><thead><tr><th>Week</th>{head}</tr></thead><tbody>{rows}</tbody></table></div>
<p>The Minimum Ear Tuning stays $99 all season.</p>"""


# ---------- Playable keyboard (hero) ----------
# Keyboard range: F3 to E5 (MIDI 53 to 76)
FIRST, LAST = 53, 76
NOTE_NAMES = ["C", "C sharp", "D", "D sharp", "E", "F", "F sharp", "G", "G sharp", "A", "A sharp", "B"]
BLACK_PCS = {1, 3, 6, 8, 10}



# ---------- The 88 keys and the 88 constellations ----------
# IAU: 88 modern constellations, 36 in the northern sky and 52 in the southern (Wikipedia, IAU designated constellations by area).
# Piano: 88 keys, 36 black and 52 white. Black keys carry northern constellations, white keys southern ones.
# Each list is ordered by approximate central declination (degrees), low to high pitch.
NORTH = [("Monoceros", -3), ("Aquila", 3), ("Orion", 5), ("Canis Minor", 6), ("Serpens", 8), ("Equuleus", 8), ("Pisces", 10), ("Delphinus", 11),
         ("Leo", 15), ("Taurus", 16), ("Sagitta", 18), ("Cancer", 20), ("Aries", 20), ("Pegasus", 20), ("Gemini", 22), ("Coma Berenices", 23),
         ("Vulpecula", 24), ("Bootes", 30), ("Hercules", 30), ("Triangulum", 31), ("Corona Borealis", 32), ("Leo Minor", 32), ("Lyra", 36),
         ("Andromeda", 37), ("Canes Venatici", 40), ("Auriga", 42), ("Cygnus", 42), ("Lacerta", 45), ("Perseus", 45), ("Lynx", 45),
         ("Ursa Major", 55), ("Cassiopeia", 60), ("Draco", 65), ("Camelopardalis", 70), ("Cepheus", 70), ("Ursa Minor", 77)]
SOUTH = [("Octans", -85), ("Chamaeleon", -79), ("Mensa", -77), ("Apus", -75), ("Hydrus", -70), ("Volans", -70), ("Musca", -70), ("Pavo", -65),
         ("Tucana", -65), ("Triangulum Australe", -65), ("Circinus", -63), ("Reticulum", -60), ("Dorado", -60), ("Crux", -60), ("Carina", -60),
         ("Indus", -55), ("Ara", -55), ("Pictor", -53), ("Horologium", -53), ("Norma", -52), ("Telescopium", -51), ("Phoenix", -48), ("Vela", -47),
         ("Centaurus", -47), ("Grus", -45), ("Lupus", -42), ("Caelum", -40), ("Corona Australis", -40), ("Antlia", -35), ("Columba", -35),
         ("Microscopium", -35), ("Puppis", -32), ("Sculptor", -32), ("Piscis Austrinus", -30), ("Fornax", -30), ("Eridanus", -30), ("Pyxis", -27),
         ("Scorpius", -27), ("Sagittarius", -25), ("Canis Major", -22), ("Lepus", -20), ("Capricornus", -18), ("Corvus", -18), ("Crater", -15),
         ("Hydra", -15), ("Libra", -15), ("Scutum", -10), ("Aquarius", -10), ("Cetus", -8), ("Ophiuchus", -8), ("Virgo", -4), ("Sextans", -2)]
assert len(NORTH) == 36 and len(SOUTH) == 52


def key_stars():
    """MIDI 21..108 -> (constellation, 'N' or 'S', declination). Black keys north, white keys south."""
    out, n, so = {}, iter(NORTH), iter(SOUTH)
    for m in range(21, 109):
        if m % 12 in BLACK_PCS:
            c, d = next(n); out[m] = (c.replace("Bootes", "Boötes"), "N", d)
        else:
            c, d = next(so); out[m] = (c, "S", d)
    return out


KEYSTAR = key_stars()

def keyboard():
    whites = [m for m in range(FIRST, LAST + 1) if m % 12 not in BLACK_PCS]
    n = len(whites)
    w = 100 / n
    keys, blacks = [], []
    for i, m in enumerate(whites):
        name = f"{NOTE_NAMES[m % 12]} {m // 12 - 1}"
        cn = KEYSTAR[m][0]
        keys.append(f'<button class="wk" type="button" data-midi="{m}" aria-label="{name}, {cn}, southern sky" title="{cn}"></button>')
        if (m + 1) % 12 in BLACK_PCS and m + 1 <= LAST:
            bm = m + 1
            left = (i + 1) * w - w * 0.3
            bname = f"{NOTE_NAMES[bm % 12]} {bm // 12 - 1}"
            blacks.append(
                f'<button class="bk" type="button" data-midi="{bm}" aria-label="{bname}, {KEYSTAR[bm][0]}, northern sky" title="{KEYSTAR[bm][0]}" '
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
  var CONS = __CONMAP__;
  var figs = {};
  document.querySelectorAll('.con').forEach(function (g) { (figs[g.dataset.id] = figs[g.dataset.id] || []).push(g); });
  function lit(m) {
    var s = stars[m - 20]; if (!s) return;
    s.classList.add('lit'); setTimeout(function () { s.classList.remove('lit'); }, 900);
    (CONS[s.dataset.c] || CONS[s.dataset.c.replace('\u00f6', 'o')] || []).forEach(function (id) {
      (figs[id] || []).forEach(function (g) {
        g.classList.add('lit'); clearTimeout(g._t); g._t = setTimeout(function () { g.classList.remove('lit'); }, 2200);
      });
    });
    if (status) status.textContent = (s.dataset.h === 'N' ? 'Black key' : 'White key') + ': ' + s.dataset.c + ', ' + (s.dataset.h === 'N' ? 'northern' : 'southern') + ' sky';
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
  // Computer keyboard: lower row C4 to E5, number row F3 to B3.
  var QK = 'r5t6y7u' + 'zsxdcvgbhnjm,l.;/';
  var qmap = {};
  for (var qi = 0; qi < QK.length; qi++) qmap[QK[qi]] = 53 + qi;
  keys.forEach(function (k) {
    for (var q in qmap) if (qmap[q] === +k.dataset.midi) k.setAttribute('data-k', q === ',' || q === '.' || q === ';' || q === '/' ? q : q.toUpperCase());
  });
  var held = {};
  document.addEventListener('keydown', function (ev) {
    if (ev.ctrlKey || ev.metaKey || ev.altKey || ev.repeat) return;
    var t = ev.target; if (t && /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)) return;
    var m = qmap[ev.key.toLowerCase()]; if (m === undefined || held[ev.key]) return;
    var el = document.querySelector('.keys [data-midi="' + m + '"]'); if (!el) return;
    ev.preventDefault(); held[ev.key] = el; down(el); note(m);
  });
  document.addEventListener('keyup', function (ev) {
    var el = held[ev.key]; if (el) { up(el); delete held[ev.key]; }
  });
  var a = document.getElementById('play-a');
  if (a) a.addEventListener('click', function () {
    note(69, 4.5);
    var key = document.querySelector('.keys [data-midi="69"]');
    if (key) { key.classList.add('down'); setTimeout(function () { key.classList.remove('down'); }, 600); }
    lit(69);
  });
})();
</script>"""


import random


def starfield():
    """88 stars, one per key. Left to right is pitch, top to bottom is north to south (declination).
    Black keys are northern constellations, white keys southern."""
    rnd = random.Random(88)
    circles = ""
    for m in range(21, 109):
        c, h, d = KEYSTAR[m]
        x = 24 + (m - 21) * (952 / 87) + rnd.uniform(-5, 5)
        y = max(10, min(490, 250 - d * 2.6 + rnd.uniform(-12, 12)))
        r = rnd.choice([1.1, 1.4, 1.8, 2.3, 3.0]); o = rnd.uniform(.5, 1)
        circles += f'<circle class="star {h.lower()}" data-n="{m - 20}" data-c="{c}" data-h="{h}" cx="{x:.1f}" cy="{y:.1f}" r="{r}" opacity="{o:.2f}"/>'
    return f'<svg class="stars" viewBox="0 0 1000 500" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">{circles}</svg>'


import json, math, os

CON_ID = None


def skymaps():
    """Two polar charts (north, south) with all 88 constellation figures. Real data: d3-celestial (BSD 3-Clause)."""
    global CON_ID
    d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "sky.json")))
    CON_ID = {}
    for i, n in d["names"].items():
        CON_ID.setdefault(n, []).append(i)
    CON_ID["Corona Australis"] = ["CrA"]
    CON_ID["Serpens"] = ["Ser"]
    R, C = 120.0, 130.0

    def proj(lon, lat, hemi):
        r = (90 - lat) if hemi == "N" else (90 + lat)
        if r > R:
            return None
        a = math.radians(lon)
        sgn = -1 if hemi == "N" else 1
        return (C + sgn * r * math.sin(a), C + r * math.cos(a) * (1 if hemi == "N" else 1))

    out = ""
    for hemi, label in (("N", "Northern sky"), ("S", "Southern sky")):
        g = ""
        for t in d["stars"]:
            p = proj(t[0], t[1], hemi)
            if p:
                g += f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{max(.5, 1.7 - t[2] * .28):.2f}" class="bg"/>'
        for cid, segs in d["lines"].items():
            paths, dots = "", ""
            for seg in segs:
                pts = [proj(a, b, hemi) for a, b in seg]
                for i in range(len(pts) - 1):
                    if pts[i] and pts[i + 1]:
                        paths += f"M{pts[i][0]:.1f} {pts[i][1]:.1f}L{pts[i + 1][0]:.1f} {pts[i + 1][1]:.1f}"
                for p in pts:
                    if p:
                        dots += f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="1.6"/>'
            if paths:
                g += f'<g class="con" data-id="{cid}"><path d="{paths}"/>{dots}</g>'
        ring = f'<circle cx="{C}" cy="{C}" r="{R}" class="rim"/><circle cx="{C}" cy="{C}" r="90" class="eq"/>'
        out += (f'<figure class="skymap" data-h="{hemi}"><svg viewBox="0 0 260 260" role="img" aria-label="{label} with constellation figures">{ring}{g}</svg>'
                f'<figcaption>{label}</figcaption></figure>')
    return f'<div class="skymaps">{out}</div>'


def con_map():
    """Constellation name -> list of figure ids, for the page script."""
    return json.dumps(CON_ID, ensure_ascii=False)


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
<span id="pitch-status" role="status">Tap the keys, or use your computer keyboard (Z to / and R to U). Each key lights its constellation.</span></p>
{skymaps()}
<p class="skycredit">Constellation figures: d3-celestial by Olaf Frohn (BSD 3-Clause); stars from the Hipparcos catalogue. The inner ring is the celestial equator; each map reaches 30 degrees past it.</p>
<p class="skynote"><b>36 and 52.</b> A piano has 36 black keys and 52 white keys. The sky has 88 modern constellations, 36 in the northern sky and 52 in the southern. Here every black key is a northern constellation and every white key a southern one, ordered by declination: the lowest white key is Octans at the south pole, and the highest black key is Ursa Minor, home of Polaris. Tap a key and its constellation lights up in the sky map.</p>
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
<div><dt>Full Ear Tuning</dt><dd>{ps("full")}</dd></div>
<div><dt>D.S.H. Maintenance</dt><dd>{ps("dsh")}</dd></div>
</dl>
<p>Holiday prices rise a little each week, so booking early costs less.<br><a href="services.html">See all services and prices</a></p>
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
    KEY_JS.replace('__CONMAP__', con_map()),
)

# ---------------- Services ----------------
PAGES["services.html"] = (
    "Piano Tuning Prices and Services",
    "Ear tuning from $99, regulation, repairs and new piano prep. See prices and book online.",
    inner(
        "Services and prices",
        "Flat rates for the services below, updated weekly. Anything else is $99 an hour, with a $99 minimum service call. Payment is due at the time of service.",
        price_table()
        + CAL_HTML
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
        "<h2>What D.S.H. Maintenance includes (" + ps("dsh") + """)</h2>
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
        "<ul>\n<li>Full Ear Tuning at concert pitch (" + ps("full") + """)</li>
<li>Regulation and other action work, quoted before I start</li>
<li>Repairs and condition checks, with a plain explanation</li>
</ul>
<p>See all <a href="services.html">services and prices</a>, or call or book online and tell me the model.</p>
<!-- TODO (Ryan): add the Bösendorfer models and the kinds of work you have done on them, if you want to name them. -->""",
    )
    + cta(),
)

# ---------------- Yamaha upright rental ----------------
PAGES["yamaha-upright-rental.html"] = (
    "Rent a Yamaha Upright Piano with Muffler Pedal | Southern California",
    "Rent a Yamaha B-series upright with a muffler (practice) pedal, delivered, tuned and ready to record. Home studios in Los Angeles, Orange County and the Inland Empire.",
    inner(
        "Rent a Yamaha upright with a muffler pedal",
        "Built for home studios. Want that soft, muted, felt-piano sound without buying a piano? Rent a real Yamaha B-series upright with a muffler (practice) pedal, delivered, tuned and ready to record.",
        """<ul>
<li><strong>Quiet, intimate tone.</strong> The muffler pedal softens and mutes the piano for close-mic'd recording, late-night writing and practice. It is much quieter, not silent.</li>
<li><strong>Mic-ready tuning included.</strong> Every piano is tuned at delivery by a professional piano technician.</li>
<li><strong>Delivery and setup.</strong> I deliver, level and set up the piano in your space.</li>
<li><strong>Flexible terms.</strong> Rent for as long as your project runs. Studio terms start at 3 to 4 months.</li>
<li><strong>Simple pricing.</strong> Call or text for current monthly pricing, plus delivery and pickup. No hidden fees.</li>
<li><strong>I maintain it.</strong> Normal tuning and wear are on me. Ask about a tuning plan.</li>
</ul>
<p>Serving Los Angeles, Orange County and the Inland Empire. Ask about availability.</p>
""",
    )
    + cta("Ask about availability: call or text " + SITE["phone"] + "."),
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
<p>Modern grand pianos are in a class of their own: more powerful yet more subtle, with faster keyboards and better materials. In my opinion, the instrument is on the verge of being redefined.</p>

<h2>My Bellharp concept</h2>
<p>I believe a bell-like essence is built into the grand piano's design.</p>
<blockquote class="quote"><p>To play the piano is to play a chromatic keyed bell.</p></blockquote>
<p>I draw it out through tuning and regulation.</p>

<h2>Tuning</h2>
<p>Aural tuning is key to bell tone. I start from a Japanese tuning fork matched to A4, then build the tuning note by note, each derived from the one before it.</p>
<h3>The temperament, the heart of the piano</h3>
<p>I tune the 12-note temperament in a circular pattern so every note relates to its neighbors, then tune the octaves above and below by ear. This brings out the bell characteristics already in the frame.</p>

<h2>Tensioning the bell frame</h2>
<p>I tension the frame firmly. If a tuning pin is lax, the string doesn't pull on the frame as it should, and the sound suffers.</p>

<h2>How I picture the piano</h2>
<p>I picture the grand piano as a tetrahedron that holds sound like a vessel, with the cast-iron frame, the real bellharp, at its center.</p>

<h2>The action, regulated by ear</h2>
<p>If the piano is a keyed bell, the double-escapement action is its clapper. I regulate by listening, judging how the touch affects what the musician hears, and I use my ear to find the ratio of key depth to striking distance that gives the liveliest bell tone.</p>

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
    ("What if my piano has not been tuned in years?", "It has probably gone flat and may need the pin setting add-on to hold a tuning. I'll tell you what I find before I start."),
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
<li><strong>Hours:</strong> Saturday, 9:00 am to 5:00 pm. Weekday evening appointments (about 6 pm) by arrangement. Closed Sunday.</li>
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
.keys button[data-k]::after{content:attr(data-k);position:absolute;left:0;right:0;bottom:6px;text-align:center;font:600 .75rem var(--display,sans-serif);color:#6b6f80;pointer-events:none;display:none}
.bk[data-k]::after{color:#aab}
@media(hover:hover) and (min-width:900px){.keys button[data-k]::after{display:block}}
.skymaps{position:relative;z-index:1;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:32px;margin:22px auto 0;max-width:880px}
.skymap{margin:0;text-align:center}
.skymap svg{width:100%;height:auto;aspect-ratio:1/1;display:block;background:#0a1030;border-radius:50%;box-shadow:0 0 0 1px #3a4680,0 8px 30px rgba(0,0,0,.45)}
.skymap figcaption{font-size:.9rem;color:#c9d0ea;margin-top:4px}
.skymap .bg{fill:#aab6e0;opacity:.55}
.skymap .rim{fill:none;stroke:#3a4680;stroke-width:1}
.skymap .eq{fill:none;stroke:#2c376e;stroke-width:.7;stroke-dasharray:2 3}
.con path{fill:none;stroke:#6c7bbd;stroke-width:.7;opacity:.55;transition:stroke .3s,opacity .3s,stroke-width .3s}
.con circle{fill:#9fb0ee;opacity:.6;transition:fill .3s,opacity .3s}
.con.lit path{stroke:#ffe08a;stroke-width:1.9;opacity:1;filter:drop-shadow(0 0 3px #ffd770)}
.con.lit circle{fill:#fff3c4;opacity:1;filter:drop-shadow(0 0 3px #ffd770)}
.skycredit{margin:10px 0 0;font-size:.8rem;color:#98a2cc;max-width:46rem}
@media(max-width:700px){.skymaps{gap:8px}}
.star{fill:#f6efd6;transform-box:fill-box;transform-origin:center;transition:transform .25s,fill .25s}
.star.n{fill:#dbe6ff}
.star.lit{fill:#ffe08a;transform:scale(3.4);filter:drop-shadow(0 0 5px #ffd770)}
.sky .hero,.sky .keybed{position:relative}
.skynote{margin:14px 0 0;font-size:.95rem;line-height:1.55;color:#c9d0ea;max-width:46rem}
.skynote b{color:#fff}
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
.wk{position:relative;flex:1;border:0;border-right:1px solid #9aa09c;background:linear-gradient(#fff,#f3f2ec 85%,#d9d6c8);border-radius:0 0 5px 5px;padding:0;cursor:pointer;margin:0 .5px}
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
.cal-tabs{display:flex;gap:6px;margin:10px 0}.cal-tabs button{flex:1;padding:10px 4px;border-radius:10px;border:1px solid var(--rule);background:#fff;color:var(--felt);font:600 .9rem var(--display);cursor:pointer}.cal-tabs button.on{background:var(--felt);color:#fff}
.cal-key{display:flex;flex-wrap:wrap;gap:12px;font-size:.9rem;margin-bottom:10px}.cal-key i{display:inline-block;width:14px;height:14px;border-radius:4px;margin-right:5px;vertical-align:-2px}
.cal-m{background:var(--felt-d);border-radius:14px;padding:14px;margin-bottom:14px}.cal-m h3{margin:0 0 8px;color:var(--brass);font:700 1.05rem var(--display)}
.cal-g{display:grid;grid-template-columns:repeat(7,1fr);gap:4px}.cd{aspect-ratio:1;border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:600;color:#10142b;cursor:pointer;border:2px solid transparent}
.cd.hd{aspect-ratio:auto;color:#aab2d0;font-weight:400;font-size:.8rem;cursor:default}.cd.xx{cursor:default}
.gr{background:#5fd18b}.ye{background:#f2cf4f}.or{background:#f0a24a}.na{background:#2a3266;color:#8890b8;cursor:default}.cd.sel{border-color:#fff}
#cal-info{background:var(--steel);border-radius:12px;padding:14px;margin:0 0 14px}
.sched-wrap{overflow-x:auto;margin:8px 0 12px}
.sched{width:100%;min-width:520px;border-collapse:collapse}
.sched th,.sched td{padding:9px 10px;text-align:right;border-bottom:1px solid #cfd4d1}
.sched th:first-child,.sched td:first-child{text-align:left;white-space:nowrap}
.sched thead th{font:700 .9rem var(--display);background:var(--steel)}
.sched tr.now td{background:#fff3cf;font-weight:700}
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
    shutil.copy(os.path.join(HERE, "data", "d3-celestial-LICENSE.txt"), os.path.join(OUT, "d3-celestial-LICENSE.txt"))
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
