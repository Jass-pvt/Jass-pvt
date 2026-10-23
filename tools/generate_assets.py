#!/usr/bin/env python3
"""
Generates the custom SVG artwork used by README.md (everything except the hand-made hero/footer).
Run from the repo root:  python tools/generate_assets.py
Edit the DATA section, re-run, commit the refreshed assets/ui-*.svg files.
Brand logos: simple-icons (CC0) via tools/icons.json.
Theme: black · purple · gold · ash (matches assets/jaswanth-hero.svg).
"""
import json, math
from pathlib import Path
from xml.sax.saxutils import escape as esc

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "assets"
OUT.mkdir(exist_ok=True)
ICONS = json.loads((ROOT / "icons.json").read_text())

# ── palette ────────────────────────────────────────────────────────────────
BG, TILE, LINE = "#0a0810", "#171126", "#35294f"
TEXT, ASH, ASH2 = "#f6f3fc", "#b3accb", "#dad4ea"          # all high-contrast on dark
GOLD, GOLD2 = "#d4af37", "#f3dd94"
PURPLE, VIOLET, DEEP = "#a855f7", "#7c3aed", "#4c1d95"
SERIF = "Georgia,'Times New Roman','DejaVu Serif',serif"
MONO = "'SF Mono','Fira Code',Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS = "'Segoe UI',Inter,'Helvetica Neue',Arial,sans-serif"

DEFS = f"""
<defs>
  <linearGradient id="acc" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="{DEEP}"/><stop offset=".5" stop-color="{PURPLE}"/><stop offset="1" stop-color="{GOLD}"/>
  </linearGradient>
  <linearGradient id="accv" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="{GOLD}"/><stop offset="1" stop-color="{PURPLE}"/>
  </linearGradient>
  <linearGradient id="bgp" x1="0" x2="1" y1="0" y2="1">
    <stop offset="0" stop-color="#0b0911"/><stop offset="1" stop-color="#1c1236"/>
  </linearGradient>
  <linearGradient id="gold" x1="0" x2="1" y1="0" y2="1">
    <stop offset="0" stop-color="{GOLD2}"/><stop offset="1" stop-color="{GOLD}"/>
  </linearGradient>
  <linearGradient id="shim" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="glow" cx="0" cy=".5" r="1">
    <stop offset="0" stop-color="{PURPLE}" stop-opacity=".30"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glow2" cx="1" cy="0" r="1">
    <stop offset="0" stop-color="{GOLD}" stop-opacity=".10"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="dots" width="14" height="14" patternUnits="userSpaceOnUse">
    <circle cx="1.5" cy="1.5" r="1" fill="#ffffff" opacity=".06"/>
  </pattern>
</defs>"""

def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)}">'
            f'<title>{esc(title)}</title>{DEFS}{body}</svg>')

def save(name, content):
    (OUT / name).write_text(content, encoding="utf-8")
    print("wrote", name)

def card(w, h, rx=16, stroke=LINE, sw=1):
    return (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="url(#bgp)" stroke="{stroke}" stroke-width="{sw}"/>'
            f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="url(#dots)"/>')

def window_dots(x, y):
    return "".join(f'<circle cx="{x+i*16}" cy="{y}" r="4.5" fill="{c}" opacity=".95"/>' for i, c in enumerate((PURPLE, GOLD, "#8d879a")))

def shimmer_line(w, y, clip_id, inset=18):
    return (f'<clipPath id="{clip_id}"><rect x="{inset}" y="{y}" width="{w-2*inset}" height="3" rx="1.5"/></clipPath>'
            f'<g clip-path="url(#{clip_id})"><rect x="{inset}" y="{y}" width="{w-2*inset}" height="3" fill="url(#acc)"/>'
            f'<rect x="-160" y="{y}" width="160" height="3" fill="url(#shim)" opacity=".9">'
            f'<animate attributeName="x" from="-160" to="{w}" dur="4.5s" repeatCount="indefinite"/></rect></g>')

def icon(slug, x, y, size, fill=GOLD):
    return f'<g transform="translate({x},{y}) scale({size/24:.3f})"><path d="{ICONS[slug]}" fill="{fill}"/></g>'

def glyph(kind, x, y, size, color=GOLD):
    paths = {
        "shield": 'M12 2.5l8 3v6c0 5-3.4 8.6-8 10.5-4.6-1.9-8-5.5-8-10.5v-6z M9 12l2.2 2.2L15.5 10',
        "log":    'M6 3h9l4 4v14H6z M15 3v4h4 M9 12h7 M9 15h7 M9 18h4',
        "globe":  'M12 3a9 9 0 100 18 9 9 0 000-18z M3 12h18 M12 3c3.2 3 3.2 15 0 18 M12 3c-3.2 3-3.2 15 0 18',
        "lock":   'M6 11h12v9H6z M8.5 11V8a3.5 3.5 0 017 0v3 M12 14.5v2.5',
    }
    return (f'<g transform="translate({x},{y}) scale({size/24:.3f})" fill="none" stroke="{color}" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="{paths[kind]}"/></g>')

# ═════════════════════════ DATA (edit me) ════════════════════════════════
SECTIONS = [
    ("about",      "About",             "~/about",     "who I am and what I build"),
    ("arsenal",    "Technical Arsenal", "~/stack",     "tools I reach for, by layer"),
    ("projects",   "Featured Projects", "~/projects",  "from my public repositories"),
    ("analytics",  "GitHub Analytics",  "~/metrics",   "live activity dashboard"),
    ("opensource", "Open Source",       "~/community", "programs I've contributed through"),
    ("connect",    "Connect",           "~/contact",   "let's talk engineering"),
]
FOCUS = ["building full-stack + IoT projects", "sharpening DSA & system design",
         "deepening cybersecurity knowledge", "exploring AWS & GCP services"]

ARSENAL = [  # label, [(icon slug | glyph:<kind> | None, name)]
    ("Languages",        [("python","Python"),("javascript","JavaScript"),("typescript","TypeScript"),("c","C"),
                          ("r","R"),("gnubash","Bash"),("html5","HTML5"),("css3","CSS3")]),
    ("Frontend",         [("react","React"),("nextdotjs","Next.js"),("tailwindcss","Tailwind"),("bootstrap","Bootstrap")]),
    ("Backend & APIs",   [("nodedotjs","Node.js"),("express","Express"),("fastapi","FastAPI"),("django","Django"),("graphql","GraphQL")]),
    ("Databases",        [("postgresql","PostgreSQL"),("mongodb","MongoDB"),("mysql","MySQL"),("firebase","Firebase")]),
    ("AI / ML",          [("tensorflow","TensorFlow"),("pytorch","PyTorch"),("scikitlearn","Scikit-learn"),
                          ("numpy","NumPy"),("pandas","Pandas"),(None,"NLTK")]),
    ("Cloud",            [("amazonaws","AWS"),("googlecloud","Google Cloud"),("oracle","Oracle OCI")]),
    ("DevOps",           [("docker","Docker"),("kubernetes","Kubernetes"),("terraform","Terraform"),("linux","Linux")]),
    ("Tools",            [("git","Git"),("visualstudiocode","VS Code"),("jupyter","Jupyter"),("streamlit","Streamlit"),("figma","Figma")]),
    ("Security",         [("glyph:shield","IAM"),("glyph:log","Log Analysis"),("glyph:globe","WHOIS"),("glyph:lock","SSL/TLS")]),
]

PROJECTS = [  # file key, title, tag, flagship?
    ("phishguard", "PhishGuard AI",           "SECURITY · ML · FULL-STACK", True),
    ("talentlens", "TalentLens AI",           "AI · AUTOMATION",            False),
    ("smartgarden","Smart Garden IoT System", "IOT · MOBILE · CLOUD",       False),
    ("urlsafety",  "URL Safety Checker",      "SECURITY · TOOLING",         False),
]
PROGRAMS = [("elite", "2025", "Elite Coders", "Winter of Code 2025"),
            ("oscg",  "2025", "Open Source Connect Global", "Open-source contribution")]
BUTTONS = [  # key, label, sub, icon, primary?
    ("linkedin",  "LinkedIn",      "Let's connect",              "linkedin",   True),
    ("email",     "Email",         "rathoresjaswanth@gmail.com", "gmail",      True),
    ("portfolio", "Portfolio",     "jass-pvt.github.io",         "globe",      True),
    ("leetcode",  "LeetCode",      "Problem solving",            "leetcode",   False),
    ("hackerrank","HackerRank",    "Coding practice",            "hackerrank", False),
    ("skills",    "Google Skills", "Cloud learning",             "google",     False),
]
QUOTE = ["“Code is not just syntax — it's the language I use",
         "to build solutions that matter.”"]
# ═════════════════════════════════════════════════════════════════════════

# 1 ─ section banners
for key, title, path, sub in SECTIONS:
    W, H = 900, 84
    body = card(W, H) + f'<rect width="{W}" height="{H}" rx="16" fill="url(#glow)"/><rect width="{W}" height="{H}" rx="16" fill="url(#glow2)"/>'
    body += window_dots(30, 22)
    body += f'<text x="{W-30}" y="27" text-anchor="end" font-family="{MONO}" font-size="13" fill="{GOLD2}">{esc(path)}</text>'
    body += f'<rect x="30" y="36" width="5" height="30" rx="2.5" fill="url(#accv)"/>'
    body += f'<text x="50" y="63" font-family="{SERIF}" font-size="34" font-weight="700" fill="{TEXT}">{esc(title)}</text>'
    body += f'<text x="{W-30}" y="63" text-anchor="end" font-family="{MONO}" font-size="14" fill="{ASH2}">{esc(sub)}</text>'
    body += shimmer_line(W, 76, f"c-{key}")
    save(f"ui-sec-{key}.svg", svg(W, H, body, title))

# 2 ─ animated terminal tagline
W, H = 900, 66
body = (f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="#07050c" stroke="{LINE}"/>'
        f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="url(#glow)"/>')
body += window_dots(30, 22)
body += f'<text x="30" y="52" font-family="{MONO}" font-size="16" fill="{PURPLE}">jaswanth</text>'
body += f'<text x="112" y="52" font-family="{MONO}" font-size="16" fill="{ASH2}">❯ now:</text>'
x0, cw, cycle = 196, 9.7, 4 * 3.6
for i, phrase in enumerate(FOCUS):
    tw = len(phrase) * cw; begin = f"{i*3.6}s"; kt = "0;0.09;0.23;0.25;1"
    body += (f'<clipPath id="t{i}"><rect x="{x0}" y="32" width="{round(tw) if i == 0 else 0}" height="26">'
             f'<animate attributeName="width" values="0;{tw:.0f};{tw:.0f};0;0" keyTimes="{kt}" dur="{cycle}s" begin="{begin}" repeatCount="indefinite"/></rect></clipPath>'
             f'<text x="{x0}" y="52" font-family="{MONO}" font-size="16" fill="{TEXT}" clip-path="url(#t{i})">{esc(phrase)}</text>'
             f'<rect x="{x0}" y="36" width="9" height="19" fill="{GOLD}" opacity="0">'
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
             f'<text x="{x+18:.1f}" y="47" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="2" fill="{GOLD}">{lab}</text>')
    for j, ln in enumerate(lines):
        body += f'<text x="{x+18:.1f}" y="{74+j*24}" font-family="{SERIF}" font-size="16" font-weight="700" fill="{TEXT}">{esc(ln)}</text>'
    x += tw + g
save("ui-glance.svg", svg(W, H, body, "Role: Software Engineer. Base: Chennai, India. Strengths: Full-Stack, AI/ML, Cloud, Security. Learning: DSA, System Design, AWS, GCP, Security."))

# 4 ─ arsenal: ONE compact board, a row per category with inline pills
W, LABEL_X, PX0, PX1 = 720, 26, 172, 698
PH, GAP, ROWPAD = 34, 8, 13
def pill_w(label): return 48 + len(label) * 7.3
def flow(items):
    rows, x = [[]], PX0
    for it in items:
        w = pill_w(it[1])
        if x + w > PX1 and rows[-1]:
            rows.append([]); x = PX0
        rows[-1].append((it, x, w)); x += w + GAP
    return rows
blocks, total = [], 0
for label, items in ARSENAL:
    rows = flow(items)
    h = len(rows) * PH + (len(rows) - 1) * GAP + 2 * ROWPAD
    blocks.append((label, rows, total, h)); total += h
H = total
body = card(W, H, 18)
for n, (label, rows, top, h) in enumerate(blocks):
    if n:
        body += f'<line x1="18" x2="{W-18}" y1="{top}" y2="{top}" stroke="{LINE}" stroke-width="1"/>'
    body += f'<rect x="{LABEL_X-10}" y="{top+ROWPAD+9}" width="4" height="16" rx="2" fill="url(#accv)"/>'
    body += f'<text x="{LABEL_X+2}" y="{top+ROWPAD+22}" font-family="{MONO}" font-size="11.5" font-weight="700" letter-spacing="1" fill="{GOLD2}">{esc(label.upper())}</text>'
    for r, row in enumerate(rows):
        py = top + ROWPAD + r * (PH + GAP)
        for (slug, name), px, pw in row:
            body += f'<rect x="{px:.1f}" y="{py}" width="{pw:.1f}" height="{PH}" rx="17" fill="{TILE}" stroke="{LINE}"/>'
            if slug and slug.startswith("glyph:"):
                body += glyph(slug[6:], px + 11, py + 8, 18)
            elif slug:
                body += icon(slug, px + 11, py + 8, 18)
            else:
                body += f'<text x="{px+20}" y="{py+23}" text-anchor="middle" font-family="{SERIF}" font-size="16" font-weight="700" fill="{GOLD}">N</text>'
            body += f'<text x="{px+36:.1f}" y="{py+22}" font-family="{SANS}" font-size="12.5" font-weight="600" fill="{TEXT}">{esc(name)}</text>'
alt = "Technical arsenal. " + "; ".join(f"{n}: {', '.join(l for _, l in it)}" for n, it in ARSENAL)
save("ui-arsenal.svg", svg(W, H, body, alt))

# 5 ─ project banners (title bar of a project card; the description sits in the SAME card in the README)
for key, title, tag, flag in PROJECTS:
    W, H = 900, (118 if flag else 104)
    stroke, sw = ("url(#acc)", 2) if flag else (LINE, 1)
    body = card(W, H, 14, stroke, sw) + f'<rect width="{W}" height="{H}" rx="14" fill="url(#glow)"/><rect width="{W}" height="{H}" rx="14" fill="url(#glow2)"/>'
    pw = len(tag) * 9.6 + 34
    body += (f'<rect x="28" y="20" width="{pw:.0f}" height="26" rx="13" fill="{GOLD}" fill-opacity=".12" stroke="{GOLD}" stroke-opacity=".7"/>'
             f'<text x="44" y="37.5" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="1.6" fill="{GOLD2}">{esc(tag)}</text>')
    if flag:
        fx = 28 + pw + 10
        body += (f'<rect x="{fx:.0f}" y="20" width="122" height="26" rx="13" fill="{VIOLET}" stroke="{PURPLE}"/>'
                 f'<text x="{fx+14:.0f}" y="37.5" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="1.6" fill="#fff">★ FLAGSHIP</text>')
    body += f'<text x="28" y="{H-24}" font-family="{SERIF}" font-size="{38 if flag else 32}" font-weight="700" fill="{TEXT}">{esc(title)}</text>'
    cx, cy = W - 50, H / 2
    body += (f'<circle cx="{cx}" cy="{cy}" r="24" fill="{BG}" stroke="url(#acc)" stroke-width="2"/>'
             f'<path d="M{cx-8} {cy+8} L{cx+8} {cy-8} M{cx-2} {cy-8} H{cx+8} V{cy+2}" fill="none" stroke="{GOLD}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    body += shimmer_line(W, H - 8, f"p-{key}")
    save(f"ui-proj-{key}.svg", svg(W, H, body, f"{title} — {tag.title()}"))

# 6 ─ open-source rows
for key, year, title, sub in PROGRAMS:
    W, H = 900, 88
    body = card(W, H) + f'<rect width="{W}" height="{H}" rx="16" fill="url(#glow)"/>'
    body += f'<text x="30" y="62" font-family="{SERIF}" font-size="44" font-weight="700" fill="none" stroke="url(#gold)" stroke-width="1.5">{year}</text>'
    body += f'<rect x="156" y="20" width="1.5" height="48" fill="{GOLD}" opacity=".5"/>'
    body += f'<text x="178" y="47" font-family="{SERIF}" font-size="28" font-weight="700" fill="{TEXT}">{esc(title)}</text>'
    body += f'<text x="178" y="70" font-family="{MONO}" font-size="14" fill="{ASH2}">{esc(sub)}</text>'
    body += (f'<rect x="{W-196}" y="31" width="166" height="26" rx="13" fill="{GOLD}" fill-opacity=".10" stroke="{GOLD}" stroke-opacity=".7"/>'
             f'<text x="{W-113}" y="48.5" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="1.8" fill="{GOLD2}">OPEN SOURCE</text>')
    save(f"ui-os-{key}.svg", svg(W, H, body, f"{title} — {sub} ({year})"))

# 7 ─ contact buttons
for key, label, sub, ico, primary in BUTTONS:
    W, H = 300, 64
    body = (f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="32" fill="{BG}" stroke="{GOLD if primary else PURPLE}" stroke-opacity=".75"/>'
            f'<circle cx="34" cy="32" r="22" fill="{VIOLET if primary else TILE}" stroke="{LINE}"/>')
    body += glyph("globe", 22, 20, 24, "#fff") if ico == "globe" else icon(ico, 22, 20, 24, "#fff" if primary else GOLD)
    body += (f'<text x="70" y="30" font-family="{SANS}" font-size="17" font-weight="700" fill="{TEXT}">{esc(label)}</text>'
             f'<text x="70" y="49" font-family="{MONO}" font-size="11.5" fill="{ASH2}">{esc(sub)}</text>'
             f'<path d="M{W-42} 40 L{W-26} 24 M{W-35} 24 H{W-26} V33" fill="none" stroke="{GOLD}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    save(f"ui-btn-{key}.svg", svg(W, H, body, f"{label} — {sub}"))

# 8 ─ closing quote
W, H = 900, 150
body = card(W, H, 18) + f'<rect width="{W}" height="{H}" rx="18" fill="url(#glow)"/><rect width="{W}" height="{H}" rx="18" fill="url(#glow2)"/>'
body += f'<text x="34" y="112" font-family="{SERIF}" font-size="150" font-weight="700" fill="url(#gold)" opacity=".30">“</text>'
for i, ln in enumerate(QUOTE):
    body += f'<text x="450" y="{62+i*34}" text-anchor="middle" font-family="{SERIF}" font-size="25" font-style="italic" fill="{TEXT}">{esc(ln)}</text>'
body += f'<text x="450" y="128" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="2.5" fill="{GOLD}">— JASWANTH RATHORE .S</text>'
body += shimmer_line(W, H - 10, "c-quote")
save("ui-quote.svg", svg(W, H, body, " ".join(QUOTE) + " — Jaswanth Rathore .S"))
