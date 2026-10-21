"""Generates the profile README's animated SVG artwork, in a dark and a light theme."""
import os, html
OUT = os.path.dirname(os.path.abspath(__file__))
FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'SF Mono', 'JetBrains Mono', Menlo, Consolas, monospace"
T = {
  'dark':  dict(bg1='#0B0F1A', bg2='#121a2b', panel='#111827', line='#253047', ink='#E6EDF3', mute='#8B98A9', faint='#1f2a3d',
                a1='#8B5CF6', a2='#22D3EE', a3='#38BDF8', gold='#FBBF24', silver='#CBD5E1', teal='#2DD4BF', chip='#1A2337', chipInk='#C9D4E3'),
  'light': dict(bg1='#FFFFFF', bg2='#F3F6FB', panel='#FFFFFF', line='#D8DEE8', ink='#0F172A', mute='#5B6779', faint='#E9EEF6',
                a1='#7C3AED', a2='#0891B2', a3='#0284C7', gold='#B45309', silver='#475569', teal='#0F766E', chip='#EEF2F8', chipInk='#334155'),
}
esc = lambda s: html.escape(s, quote=True)
RM = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"

def hero(t):
    c = T[t]
    nodes = [(905,95),(1010,60),(1120,110),(960,190),(1075,200),(1180,245),(880,270),(1015,285),(1150,150)]
    edges = [(0,1),(1,2),(0,3),(3,4),(4,2),(4,5),(3,6),(6,7),(7,4),(2,8),(8,5),(1,4)]
    lines, pulses = [], []
    for i,(a,b) in enumerate(edges):
        (x1,y1),(x2,y2) = nodes[a], nodes[b]
        lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="url(#edge)" stroke-width="1.4" opacity=".55"/>')
        if i % 2 == 0:
            d = 2.6 + (i % 5) * .45
            pulses.append(f'<circle r="3" fill="{c["a2"]}"><animateMotion dur="{d:.2f}s" repeatCount="indefinite" begin="{i*0.37:.2f}s" path="M{x1},{y1} L{x2},{y2}"/><animate attributeName="opacity" values="0;1;1;0" dur="{d:.2f}s" begin="{i*0.37:.2f}s" repeatCount="indefinite"/></circle>')
    dots = ''.join(f'<g class="node" style="animation-delay:{k*0.35:.2f}s"><circle cx="{x}" cy="{y}" r="{11 if k in (2,4) else 8}" fill="{c["panel"]}" stroke="url(#edge)" stroke-width="2"/><circle cx="{x}" cy="{y}" r="3.2" fill="{c["a1"] if k%2 else c["a2"]}"/></g>' for k,(x,y) in enumerate(nodes))
    phrases = ["I build agentic AI systems, with hard rules around the models.",
               "Full-stack engineer · AI & workflow automation at Zurich Insurance.",
               "Hackathon winner · open-source contributor · Zurich, Switzerland."]
    rot = ''.join(f'<text class="r r{i+1}" x="72" y="236" font-size="21" fill="{c["mute"]}">{esc(p)}</text>' for i,p in enumerate(phrases))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="340" viewBox="0 0 1280 340" role="img" aria-labelledby="t d">
<title id="t">Roger Bavibidila</title><desc id="d">Full-stack and AI engineer in Zurich. Builds agentic AI systems, with hard rules around the models.</desc>
<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['bg1']}"/><stop offset="1" stop-color="{c['bg2']}"/></linearGradient>
 <linearGradient id="name" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox"><stop offset="0" stop-color="{c['ink']}"/><stop offset=".55" stop-color="{c['ink']}"/><stop offset=".78" stop-color="{c['a1']}"/><stop offset="1" stop-color="{c['a2']}"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-0.35 0;0.35 0;-0.35 0" dur="9s" repeatCount="indefinite"/></linearGradient>
 <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c['a1']}"/><stop offset="1" stop-color="{c['a2']}"/></linearGradient>
 <linearGradient id="bar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c['a1']}"/><stop offset="1" stop-color="{c['a2']}"/></linearGradient>
 <radialGradient id="glow" cx="0.78" cy="0.5" r="0.45"><stop offset="0" stop-color="{c['a1']}" stop-opacity=".18"/><stop offset="1" stop-color="{c['a1']}" stop-opacity="0"/></radialGradient>
 <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{c['faint']}" stroke-width="1"/></pattern>
 <clipPath id="clip"><rect width="1280" height="340" rx="22"/></clipPath>
</defs>
<style>
 text{{font-family:{FONT}}}
 .mono{{font-family:{MONO}}}
 .r{{opacity:0;animation:rot 12s infinite}} .r1{{opacity:1}} .r2{{animation-delay:4s}} .r3{{animation-delay:8s}}
 @keyframes rot{{0%{{opacity:0;transform:translateY(8px)}}4%,31%{{opacity:1;transform:none}}35%,100%{{opacity:0;transform:translateY(-6px)}}}}
 .node{{animation:breathe 4s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
 @keyframes breathe{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.12)}}}}
 .blink{{animation:blink 1.1s steps(1) infinite}} @keyframes blink{{50%{{opacity:0}}}}
 {RM} @media (prefers-reduced-motion: reduce){{.r1{{opacity:1}}}}
</style>
<g clip-path="url(#clip)">
 <rect width="1280" height="340" fill="url(#bg)"/><rect width="1280" height="340" fill="url(#grid)" opacity=".7"/><rect width="1280" height="340" fill="url(#glow)"/>
 {''.join(lines)}{''.join(pulses)}{dots}
</g>
<rect x=".5" y=".5" width="1279" height="339" rx="22" fill="none" stroke="{c['line']}"/>
<g class="rise"><text class="mono" x="72" y="92" font-size="14" letter-spacing="3" fill="{c['a2']}">FULL-STACK &amp; AI ENGINEER  ·  ZURICH</text></g>
<g class="rise d1"><text x="68" y="168" font-size="66" font-weight="800" letter-spacing="-1.5" fill="url(#name)">Roger Bavibidila</text></g>
<rect class="bar" x="72" y="190" width="168" height="4" rx="2" fill="url(#bar)"/>
{rot}
<g class="rise d2"><text class="mono" x="72" y="292" font-size="14" fill="{c['mute']}"><tspan fill="{c['a1']}">$</tspan> whoami <tspan class="blink" fill="{c['a2']}">▍</tspan></text></g>
</svg>'''

def divider(t):
    c = T[t]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="10" viewBox="0 0 1280 10" role="presentation">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c['line']}" stop-opacity="0"/><stop offset=".5" stop-color="{c['line']}"/><stop offset="1" stop-color="{c['line']}" stop-opacity="0"/></linearGradient>
<linearGradient id="s" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c['a1']}" stop-opacity="0"/><stop offset=".5" stop-color="{c['a2']}"/><stop offset="1" stop-color="{c['a1']}" stop-opacity="0"/></linearGradient></defs>
<style>.s{{animation:sweep 6s ease-in-out infinite}}@keyframes sweep{{0%{{transform:translateX(-260px)}}100%{{transform:translateX(1280px)}}}}{RM}</style>
<rect x="0" y="4.5" width="1280" height="1" fill="url(#g)"/><rect class="s" x="0" y="4" width="240" height="2" rx="1" fill="url(#s)"/>
</svg>'''

def chips_svg(c, chips, x, y, maxw):
    out, cx, cy = [], x, y
    for ch in chips:
        w = int(len(ch) * 7.4 + 26)
        if cx + w > x + maxw: cx, cy = x, cy + 34
        out.append(f'<rect x="{cx}" y="{cy}" width="{w}" height="26" rx="13" fill="{c["chip"]}" stroke="{c["line"]}"/><text x="{cx + w/2}" y="{cy+17.5}" font-size="12.5" font-weight="600" text-anchor="middle" fill="{c["chipInk"]}">{esc(ch)}</text>')
        cx += w + 8
    return ''.join(out)

def card(t, w, h, pill, tone, title, sub, lines, chips, cta):
    c = T[t]; col = {'gold': c['gold'], 'silver': c['silver'], 'violet': c['a1'], 'teal': c['teal']}[tone]
    pw = int(len(pill) * 8.9 + 40)
    body = ''.join(f'<text x="32" y="{150 + i*24}" font-size="15.5" fill="{c["mute"]}">{esc(l)}</text>' for i, l in enumerate(lines))
    cy = 150 + len(lines) * 24 + 14
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">
<title id="t">{esc(title)}</title><desc id="d">{esc(pill)}. {esc(sub)} {esc(' '.join(lines))}</desc>
<defs><linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['a1']}"/><stop offset=".5" stop-color="{c['line']}"/><stop offset="1" stop-color="{c['a2']}"/>
<animateTransform attributeName="gradientTransform" type="rotate" values="0 .5 .5;360 .5 .5" dur="14s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c['panel']}"/><stop offset="1" stop-color="{c['bg2']}"/></linearGradient>
<radialGradient id="gl" cx="1" cy="0" r=".9"><stop offset="0" stop-color="{col}" stop-opacity=".14"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>
<style>text{{font-family:{FONT}}} .p{{animation:pulse 2.8s ease-in-out infinite}} @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.45}}}} {RM}</style>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="url(#bg)"/><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="url(#gl)"/>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="none" stroke="url(#bd)" stroke-width="1.6"/>
<g class="in">
<rect x="32" y="28" width="{pw}" height="26" rx="13" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".55"/>
<circle class="p" cx="47" cy="41" r="4" fill="{col}"/><text x="58" y="45.5" font-size="12" font-weight="700" letter-spacing="1" fill="{col}">{esc(pill)}</text>
<text x="32" y="96" font-size="30" font-weight="800" letter-spacing="-.5" fill="{c['ink']}">{esc(title)}</text>
<text x="32" y="122" font-size="16" font-weight="600" fill="{c['a3']}">{esc(sub)}</text>
{body}
{chips_svg(c, chips, 32, cy, w - 64)}
<text x="{w-32}" y="45.5" font-size="13" font-weight="700" text-anchor="end" fill="{c['mute']}">{esc(cta)} →</text>
</g></svg>'''

CARDS = {
 'wick': dict(w=1280, h=300, pill='SUBMITTED · AMAZON DEVELOPER HACKATHON 2026 · FIRE TV TRACK', tone='violet', title='Wick',
   sub='Fire TV as the care surface for the person being cared for.',
   lines=['Who is at the door, notes that wait for a natural break, and a family kept close — all on the TV she already watches,',
          'answered with one button on her remote. Three agents on Bedrock AgentCore, an MCP server for Alexa+, Ring, ~6,500 tests.'],
   chips=['Vega OS', 'Fire OS', 'React Native', 'Bedrock AgentCore', 'Strands', 'MCP', 'Ring API', 'AWS', 'Terraform'], cta='Watch the demo'),
 'kintwadi': dict(w=632, h=300, pill='WINNER · BEST DESIGN', tone='gold', title='Kintwadi', sub='One shared record for family caregiving.',
   lines=['Permission-aware caregiving record with role-based', 'RLS and a permission-scoped RAG assistant.'],
   chips=['Aurora PostgreSQL', 'pgvector', 'Bedrock', 'Next.js'], cta='Devpost'),
 'karma': dict(w=632, h=300, pill='2ND PLACE · DYNATRACE TRACK', tone='silver', title='Karma', sub='The reincarnation agent for deprecated services.',
   lines=["Four agents learn a deprecated service's behaviour", 'and flag silent regressions after cutover.'],
   chips=['Vertex AI Agents', 'Gemini 2.5', 'Dynatrace', 'MCP'], cta='Devpost'),
 'hslu': dict(w=632, h=300, pill='LIVE · RAG', tone='teal', title='HSLU Exam Assistant', sub='AI exam prep, course by course.',
   lines=['Course-specific Q&A, summaries and practice', 'questions grounded in the course material.'],
   chips=['FastAPI', 'Pinecone', 'Next.js', 'RAG'], cta='Open the app'),
 'letusconnect': dict(w=632, h=300, pill='LIVE · REAL-TIME', tone='teal', title='Let Us Connect', sub='Networking and collaboration, in real time.',
   lines=['A platform to meet, connect and work together,', 'with real-time notifications.'],
   chips=['Go Fiber', 'Firestore', 'Next.js'], cta='Open the app'),
}

def footer(t):
    c = T[t]
    def wave(amp, phase, y):
        pts = ' '.join(f'{x},{y + amp * __import__("math").sin((x / 1280) * 6.283 * 1.5 + phase):.1f}' for x in range(0, 1281, 40))
        return f'M0,120 L{pts.replace(" ", " L")} L1280,120 Z'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="120" viewBox="0 0 1280 120" role="presentation">
<defs><linearGradient id="w" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c['a1']}"/><stop offset="1" stop-color="{c['a2']}"/></linearGradient></defs>
<style>.a{{animation:drift 9s ease-in-out infinite alternate}} .b{{animation:drift 13s ease-in-out infinite alternate-reverse}}
@keyframes drift{{from{{transform:translateX(-40px)}}to{{transform:translateX(40px)}}}} {RM}</style>
<g transform="translate(-60 0) scale(1.1 1)"><path class="b" d="{wave(10, 1.2, 62)}" fill="url(#w)" opacity=".18"/><path class="a" d="{wave(14, 0, 74)}" fill="url(#w)" opacity=".32"/></g>
</svg>'''

os.makedirs(OUT, exist_ok=True)
for t in T:
    open(f'{OUT}/hero-{t}.svg', 'w').write(hero(t))
    open(f'{OUT}/divider-{t}.svg', 'w').write(divider(t))
    open(f'{OUT}/footer-{t}.svg', 'w').write(footer(t))
    for k, v in CARDS.items(): open(f'{OUT}/card-{k}-{t}.svg', 'w').write(card(t, **v))
print(sorted(os.listdir(OUT)))
