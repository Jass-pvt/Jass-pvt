#!/usr/bin/env python3
"""
Generates the custom SVG artwork used by README.md (everything except the hero/footer).
Run from the repo root:  python tools/generate_assets.py
Edit the DATA section below, re-run, commit the refreshed assets/ui-*.svg files.
Theme: purple. Brand logos come from simple-icons (CC0) via tools/icons.json.
"""
import json, math
from pathlib import Path
from xml.sax.saxutils import escape as esc

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "assets"
OUT.mkdir(exist_ok=True)
ICONS = json.loads((ROOT / "icons.json").read_text())

# ── palette: black · ash · purple (violet → lilac) ───────────────────────────
BG, PANEL, TILE, LINE = "#09060f", "#130d20", "#190f2b", "#2f2150"
TEXT, ASH, ASH2 = "#f3eefc", "#9a8fb5", "#c4b8e0"
ACCENT, ACCENT2 = "#c084fc", "#e9d5ff"          # lilac highlights
PURPLE, VIOLET, VIOLET2 = "#a855f7", "#6d28d9", "#8b5cf6"
SERIF = "Georgia,'Times New Roman','DejaVu Serif',serif"
MONO = "'SF Mono','Fira Code',Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS = "'Segoe UI',Inter,'Helvetica Neue',Arial,sans-serif"

DEFS = f"""
<defs>
  <linearGradient id="acc" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="{VIOLET}"/><stop offset=".55" stop-color="{PURPLE}"/><stop offset="1" stop-color="{ACCENT}"/>
  </linearGradient>
  <linearGradient id="bgp" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="#1b1033"/><stop offset="1" stop-color="#0b0716"/>
  </linearGradient>
  <linearGradient id="gold" x1="0" x2="1" y1="0" y2="1">
    <stop offset="0" stop-color="{ACCENT2}"/><stop offset="1" stop-color="{ACCENT}"/>
  </linearGradient>
  <linearGradient id="shim" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="glow" cx="0" cy=".5" r="1">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity=".42"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glow2" cx="1" cy="0" r="1">
    <stop offset="0" stop-color="{PURPLE}" stop-opacity=".22"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="dots" width="14" height="14" patternUnits="userSpaceOnUse">
    <circle cx="1.5" cy="1.5" r="1" fill="#ffffff" opacity=".07"/>
  </pattern>
</defs>"""

def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)}">'
            f'<title>{esc(title)}</title>{DEFS}{body}</svg>')

def save(name, content):
    (OUT / name).write_text(content, encoding="utf-8")
    print("wrote", name)

def card(w, h, rx=16, stroke=LINE, sw=1, extra=""):
    return (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="url(#bgp)" stroke="{stroke}" stroke-width="{sw}"/>'
            f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="url(#dots)"/>{extra}')

def window_dots(x, y):
    return "".join(f'<circle cx="{x+i*16}" cy="{y}" r="4.5" fill="{c}" opacity=".9"/>' for i, c in enumerate((VIOLET2, ACCENT, PURPLE)))

def shimmer_line(w, y, clip_id):
    return (f'<clipPath id="{clip_id}"><rect x="18" y="{y}" width="{w-36}" height="3" rx="1.5"/></clipPath>'
            f'<g clip-path="url(#{clip_id})"><rect x="18" y="{y}" width="{w-36}" height="3" fill="url(#acc)"/>'
            f'<rect x="-160" y="{y}" width="160" height="3" fill="url(#shim)" opacity=".9">'
            f'<animate attributeName="x" from="-160" to="{w}" dur="4.5s" repeatCount="indefinite"/></rect></g>')

def icon(slug, x, y, size, fill=ACCENT):
    s = size / 24
    return f'<g transform="translate({x},{y}) scale({s:.3f})"><path d="{ICONS[slug]}" fill="{fill}"/></g>'

def glyph(kind, x, y, size, color=ACCENT):
    s = size / 24
    paths = {
        "shield": 'M12 2.5l8 3v6c0 5-3.4 8.6-8 10.5-4.6-1.9-8-5.5-8-10.5v-6z M12 9.5v4 M12 9.5a1.6 1.6 0 100 .01',
        "log":    'M6 3h9l4 4v14H6z M15 3v4h4 M9 12h7 M9 15h7 M9 18h4',
        "globe":  'M12 3a9 9 0 100 18 9 9 0 000-18z M3 12h18 M12 3c3.2 3 3.2 15 0 18 M12 3c-3.2 3-3.2 15 0 18',
        "lock":   'M6 11h12v9H6z M8.5 11V8a3.5 3.5 0 017 0v3 M12 14.5v2.5',
    }
    return (f'<g transform="translate({x},{y}) scale({s:.3f})" fill="none" stroke="{color}" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="{paths[kind]}"/></g>')

# ═════════════════════════ DATA (edit me) ════════════════════════════════
SECTIONS = [
    ("about", "About",             "~/about",     "who I am and what I build"),
    ("arsenal", "Technical Arsenal", "~/stack",     "tools I reach for, by layer"),
    ("projects", "Featured Projects", "~/projects",  "from my public repositories"),
    ("analytics", "GitHub Analytics",  "~/metrics",   "live activity dashboard"),
    ("opensource", "Open Source",       "~/community", "programs I've contributed through"),
    ("connect", "Connect",           "~/contact",   "let's talk engineering"),
]
FOCUS = ["building full-stack + IoT projects", "sharpening DSA & system design",
         "deepening cybersecurity knowledge", "exploring AWS & GCP services"]

# (slug-or-None, label)
ARSENAL = [
    ("Languages", [("python","Python"),("javascript","JavaScript"),("typescript","TypeScript"),("c","C"),
                   ("r","R"),("gnubash","Bash"),("html5","HTML5"),("css3","CSS3")], VIOLET2),
    ("Frontend", [("react","React"),("nextdotjs","Next.js"),("tailwindcss","Tailwind"),("bootstrap","Bootstrap")], PURPLE),
    ("Backend & APIs", [("nodedotjs","Node.js"),("express","Express"),("fastapi","FastAPI"),("django","Django"),("graphql","GraphQL")], PURPLE),
    ("Databases", [("postgresql","PostgreSQL"),("mongodb","MongoDB"),("mysql","MySQL"),("firebase","Firebase")], VIOLET2),
    ("AI / ML", [("tensorflow","TensorFlow"),("pytorch","PyTorch"),("scikitlearn","Scikit-learn"),
                 ("numpy","NumPy"),("pandas","Pandas"),(None,"NLTK")], VIOLET2),
    ("Cloud", [("amazonaws","AWS"),("googlecloud","Google Cloud"),("oracle","Oracle OCI")], PURPLE),
    ("DevOps & Systems", [("docker","Docker"),("kubernetes","Kubernetes"),("terraform","Terraform"),("linux","Linux")], PURPLE),
    ("Tools", [("git","Git"),("visualstudiocode","VS Code"),("jupyter","Jupyter"),("streamlit","Streamlit"),("figma","Figma")], VIOLET2),
]
SECURITY = [("shield","IAM"),("log","Log Analysis"),("globe","WHOIS"),("lock","SSL/TLS")]

PROJECTS = [  # file key, title, tag, flagship?
    ("phishguard", "PhishGuard AI",           "SECURITY · ML · FULL-STACK", True),
    ("talentlens", "TalentLens AI",           "AI · AUTOMATION",            False),
    ("geomeasure", "GeoMeasure API",          "BACKEND · GEOSPATIAL",       False),
    ("smartgarden","Smart Garden IoT System", "IOT · MOBILE · CLOUD",       False),
    ("urlsafety",  "URL Safety Checker",      "SECURITY · TOOLING",         False),
]
PROGRAMS = [("elite", "2025", "Elite Coders", "Winter of Code 2025"),
            ("oscg",  "2025", "Open Source Connect Global", "Open-source contribution")]
BUTTONS = [  # key, label, sub, icon slug / glyph, primary?
    ("linkedin",  "LinkedIn",     "Let's connect",       "linkedin", True),
    ("email",     "Email",        "rathoresjaswanth@gmail.com", "gmail", True),
    ("portfolio", "Portfolio",    "jass-pvt.github.io",  "globe",    True),
    ("leetcode",  "LeetCode",     "Problem solving",     "leetcode", False),
    ("hackerrank","HackerRank",   "Coding practice",     "hackerrank", False),
    ("skills",    "Google Skills","Cloud learning",      "google",   False),
]
QUOTE = ["“Code is not just syntax — it's the language I use",
         "to build solutions that matter.”"]
# ═════════════════════════════════════════════════════════════════════════

# 1 ─ section banners
for key, title, path, sub in SECTIONS:
    W, H = 900, 96
    body = card(W, H) + f'<rect width="{W}" height="{H}" rx="16" fill="url(#glow)"/>'
    body += window_dots(30, 24)
    body += f'<text x="{W-30}" y="29" text-anchor="end" font-family="{MONO}" font-size="13" fill="{ASH}">{esc(path)}</text>'
    body += f'<rect x="30" y="44" width="5" height="38" rx="2.5" fill="url(#acc)"/>'
    body += f'<text x="50" y="79" font-family="{SERIF}" font-size="38" font-weight="700" fill="{TEXT}">{esc(title)}</text>'
    body += f'<text x="{W-30}" y="79" text-anchor="end" font-family="{MONO}" font-size="13" fill="{ASH2}">{esc(sub)}</text>'
    body += shimmer_line(W, 88, f"c-{key}")
    save(f"ui-sec-{key}.svg", svg(W, H, body, title))

# 2 ─ animated terminal tagline
W, H = 900, 66
body = (f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="#07040d" stroke="{LINE}"/>'
        f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="url(#glow2)"/>')
body += window_dots(30, 22)
body += f'<text x="30" y="52" font-family="{MONO}" font-size="16" fill="{PURPLE}">jaswanth</text>'
body += f'<text x="112" y="52" font-family="{MONO}" font-size="16" fill="{ASH}">❯ now:</text>'
x0, cw, cycle = 196, 9.7, 4 * 3.6
for i, phrase in enumerate(FOCUS):
    tw = len(phrase) * cw
    begin = f"{i*3.6}s"
    kt = "0;0.09;0.23;0.25;1"
    body += (f'<clipPath id="t{i}"><rect x="{x0}" y="32" width="{(round(tw) if i == 0 else 0)}" height="26">'
             f'<animate attributeName="width" values="0;{tw:.0f};{tw:.0f};0;0" keyTimes="{kt}" dur="{cycle}s" begin="{begin}" repeatCount="indefinite"/></rect></clipPath>'
             f'<text x="{x0}" y="52" font-family="{MONO}" font-size="16" fill="{TEXT}" clip-path="url(#t{i})">{esc(phrase)}</text>'
             f'<rect x="{x0}" y="36" width="9" height="19" fill="{ACCENT}" opacity="0">'
             f'<animate attributeName="x" values="{x0};{x0+tw:.0f};{x0+tw:.0f};{x0};{x0}" keyTimes="{kt}" dur="{cycle}s" begin="{begin}" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.01;0.23;0.25;1" dur="{cycle}s" begin="{begin}" repeatCount="indefinite"/></rect>')
save("ui-terminal.svg", svg(W, H, body, "Currently: " + "; ".join(FOCUS)))

# 3 ─ at-a-glance tiles
tiles = [("ROLE", ["Software Engineer"]), ("BASE", ["Chennai, India"]),
         ("STRENGTHS", ["Full-Stack · AI/ML", "Cloud · Security"]), ("LEARNING", ["DSA · System Design", "AWS · GCP · Security"])]
W, H, g = 900, 112, 16
widths = [190, 170, 226, 264]
body, x = "", 0
for (lab, lines), tw in zip(tiles, widths):
    body += (f'<rect x="{x+.5:.1f}" y=".5" width="{tw-1:.1f}" height="{H-1}" rx="14" fill="url(#bgp)" stroke="{LINE}"/>'
             f'<rect x="{x+.5:.1f}" y=".5" width="{tw-1:.1f}" height="{H-1}" rx="14" fill="url(#dots)"/>'
             f'<rect x="{x+18:.1f}" y="20" width="22" height="3" rx="1.5" fill="url(#acc)"/>'
             f'<text x="{x+18:.1f}" y="46" font-family="{MONO}" font-size="12" letter-spacing="2" fill="{ACCENT}">{lab}</text>')
    for j, ln in enumerate(lines):
        body += f'<text x="{x+18:.1f}" y="{74+j*24}" font-family="{SERIF}" font-size="16" font-weight="700" fill="{TEXT}">{esc(ln)}</text>'
    x += tw + g
save("ui-glance.svg", svg(W, H, body, "Role: Software Engineer. Base: Chennai, India. Strengths: Full-Stack, AI/ML, Cloud, Security. Learning: DSA, System Design, AWS, GCP, Security."))

# 4 ─ arsenal board
W, colw, gap, pad = 900, 440, 20, 16
tile_w, tile_h, tg, per = 76, 70, 7, 5
def panel_h(items): 
    rows = math.ceil(len(items) / per)
    return 46 + rows * tile_h + (rows - 1) * 8 + 16
body, y = "", 0
for r in range(0, len(ARSENAL), 2):
    pair = ARSENAL[r:r + 2]
    ph = max(panel_h(p[1]) for p in pair)
    for c, (name, items, accent) in enumerate(pair):
        x = c * (colw + gap)
        body += (f'<g transform="translate({x},{y})"><rect x=".5" y=".5" width="{colw-1}" height="{ph-1}" rx="16" fill="url(#bgp)" stroke="{LINE}"/>'
                 f'<rect x=".5" y=".5" width="{colw-1}" height="{ph-1}" rx="16" fill="url(#dots)"/>'
                 f'<rect x="{pad}" y="18" width="4" height="16" rx="2" fill="{accent}"/>'
                 f'<text x="{pad+14}" y="31" font-family="{MONO}" font-size="12.5" letter-spacing="2" fill="{ACCENT}">{esc(name.upper())}</text>')
        for k, (slug, label) in enumerate(items):
            tx = pad + (k % per) * (tile_w + tg); ty = 46 + (k // per) * (tile_h + 8)
            body += f'<rect x="{tx}" y="{ty}" width="{tile_w}" height="{tile_h}" rx="11" fill="{TILE}" stroke="{LINE}"/>'
            if slug:
                body += icon(slug, tx + tile_w/2 - 14, ty + 11, 28)
            else:
                body += f'<text x="{tx+tile_w/2}" y="{ty+33}" text-anchor="middle" font-family="{SERIF}" font-size="22" font-weight="700" fill="{ACCENT}">N</text>'
            body += f'<text x="{tx+tile_w/2}" y="{ty+58}" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{ASH2}">{esc(label)}</text>'
        body += "</g>"
    y += ph + 16
# security row (full width)
sh = 46 + 54 + 16
body += (f'<g transform="translate(0,{y})"><rect x=".5" y=".5" width="{W-1}" height="{sh-1}" rx="16" fill="url(#bgp)" stroke="{LINE}"/>'
         f'<rect x=".5" y=".5" width="{W-1}" height="{sh-1}" rx="16" fill="url(#dots)"/>'
         f'<rect x="{pad}" y="18" width="4" height="16" rx="2" fill="{VIOLET2}"/>'
         f'<text x="{pad+14}" y="31" font-family="{MONO}" font-size="12.5" letter-spacing="2" fill="{ACCENT}">SECURITY &amp; ANALYSIS</text>')
sw_ = (W - 2*pad - 3*10) / 4
for k, (g_, label) in enumerate(SECURITY):
    tx = pad + k * (sw_ + 10)
    body += (f'<rect x="{tx:.1f}" y="46" width="{sw_:.1f}" height="54" rx="11" fill="{TILE}" stroke="{LINE}"/>'
             + glyph(g_, tx + 20, 46 + 15, 24)
             + f'<text x="{tx+58:.1f}" y="79" font-family="{SANS}" font-size="14" font-weight="600" fill="{TEXT}">{esc(label)}</text>')
body += "</g>"
H = y + sh
names = "; ".join(f"{n}: {', '.join(l for _, l in it)}" for n, it, _ in ARSENAL) + "; Security & Analysis: " + ", ".join(l for _, l in SECURITY)
save("ui-arsenal.svg", svg(W, H, body, "Technical arsenal. " + names))

# 5 ─ project banners
for key, title, tag, flag in PROJECTS:
    W, H = 900, (164 if flag else 128)
    stroke, sw = ("url(#acc)", 2) if flag else (LINE, 1)
    body = card(W, H, 18, stroke, sw) + f'<rect width="{W}" height="{H}" rx="18" fill="url(#glow)"/><rect width="{W}" height="{H}" rx="18" fill="url(#glow2)"/>'
    body += (f'<circle cx="{W-58}" cy="{H/2}" r="{58 if flag else 52}" fill="none" stroke="{ACCENT}" stroke-opacity=".10"/>'
             f'<circle cx="{W-58}" cy="{H/2}" r="{86 if flag else 78}" fill="none" stroke="{ACCENT}" stroke-opacity=".06"/>')
    pw = len(tag) * 8.6 + 30
    body += (f'<rect x="32" y="26" width="{pw:.0f}" height="26" rx="13" fill="{ACCENT}" fill-opacity=".08" stroke="{ACCENT}" stroke-opacity=".6"/>'
             f'<text x="47" y="43.5" font-family="{MONO}" font-size="12" letter-spacing="1.6" fill="{ACCENT}">{esc(tag)}</text>')
    if flag:
        fx = 32 + pw + 10
        body += (f'<rect x="{fx:.0f}" y="26" width="118" height="26" rx="13" fill="{VIOLET}" stroke="{VIOLET2}"/>'
                 f'<text x="{fx+14:.0f}" y="43.5" font-family="{MONO}" font-size="12" letter-spacing="1.6" fill="#fff">★ FLAGSHIP</text>')
    body += f'<text x="32" y="{H-38}" font-family="{SERIF}" font-size="{50 if flag else 40}" font-weight="700" fill="{TEXT}">{esc(title)}</text>'
    body += (f'<text x="32" y="{H-14}" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="{ASH}">github.com/Jass-pvt ▸ view repository</text>')
    cx, cy = W - 58, H / 2
    body += (f'<circle cx="{cx}" cy="{cy}" r="26" fill="{BG}" stroke="url(#acc)" stroke-width="2"/>'
             f'<path d="M{cx-9} {cy+9} L{cx+9} {cy-9} M{cx-2} {cy-9} H{cx+9} V{cy+2}" fill="none" stroke="{ACCENT}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    body += shimmer_line(W, H - 9, f"p-{key}")
    save(f"ui-proj-{key}.svg", svg(W, H, body, f"{title} — {tag.title()}"))

# 6 ─ open-source ticket rows
for key, year, title, sub in PROGRAMS:
    W, H = 900, 92
    body = card(W, H) + f'<rect width="{W}" height="{H}" rx="16" fill="url(#glow)"/>'
    body += f'<text x="30" y="64" font-family="{SERIF}" font-size="46" font-weight="700" fill="none" stroke="url(#gold)" stroke-width="1.5">{year}</text>'
    body += f'<rect x="160" y="22" width="1.5" height="48" fill="{ACCENT}" opacity=".45"/>'
    body += f'<text x="182" y="48" font-family="{SERIF}" font-size="28" font-weight="700" fill="{TEXT}">{esc(title)}</text>'
    body += f'<text x="182" y="72" font-family="{MONO}" font-size="13" fill="{ASH2}">{esc(sub)}</text>'
    body += (f'<rect x="{W-186}" y="33" width="156" height="26" rx="13" fill="none" stroke="{PURPLE}" stroke-opacity=".7"/>'
             f'<text x="{W-108}" y="50.5" text-anchor="middle" font-family="{MONO}" font-size="12" letter-spacing="1.8" fill="{PURPLE}">OPEN SOURCE</text>')
    save(f"ui-os-{key}.svg", svg(W, H, body, f"{title} — {sub} ({year})"))

# 7 ─ contact buttons
for key, label, sub, ico, primary in BUTTONS:
    W, H = 300, 64
    fill = "url(#acc)" if primary else TILE
    body = (f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="32" fill="{BG}" stroke="{ACCENT if primary else LINE}" stroke-opacity="{.7 if primary else 1}"/>'
            f'<circle cx="34" cy="32" r="22" fill="{fill}" fill-opacity="{.9 if primary else 1}" stroke="{LINE}"/>')
    body += glyph("globe", 22, 20, 24, "#fff") if ico == "globe" else icon(ico, 22, 20, 24, "#fff" if primary else ACCENT)
    body += (f'<text x="70" y="30" font-family="{SANS}" font-size="17" font-weight="700" fill="{TEXT}">{esc(label)}</text>'
             f'<text x="70" y="48" font-family="{MONO}" font-size="11" fill="{ASH}">{esc(sub)}</text>'
             f'<path d="M{W-42} 40 L{W-26} 24 M{W-35} 24 H{W-26} V33" fill="none" stroke="{ACCENT}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    save(f"ui-btn-{key}.svg", svg(W, H, body, f"{label} — {sub}"))

# 8 ─ closing quote
W, H = 900, 150
body = card(W, H, 18) + f'<rect width="{W}" height="{H}" rx="18" fill="url(#glow)"/>'
body += f'<text x="34" y="112" font-family="{SERIF}" font-size="150" font-weight="700" fill="url(#gold)" opacity=".28">“</text>'
for i, ln in enumerate(QUOTE):
    body += f'<text x="450" y="{62+i*34}" text-anchor="middle" font-family="{SERIF}" font-size="25" font-style="italic" fill="{TEXT}">{esc(ln)}</text>'
body += f'<text x="450" y="128" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing="2.5" fill="{ACCENT}">— JASWANTH RATHORE .S</text>'
body += shimmer_line(W, H - 10, "c-quote")
save("ui-quote.svg", svg(W, H, body, " ".join(QUOTE) + " — Jaswanth Rathore .S"))
