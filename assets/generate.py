"""Generates the profile README's animated SVG artwork, in a dark and a light theme."""
import os, html
OUT = os.path.dirname(os.path.abspath(__file__))
FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'SF Mono', 'JetBrains Mono', Menlo, Consolas, monospace"
T = {
  'dark':  dict(bg1='#0B0F1A', bg2='#121a2b', panel='#111827', line='#253047', ink='#E6EDF3', mute='#8B98A9', faint='#1f2a3d',
                a1='#8B5CF6', a2='#22D3EE', a3='#38BDF8', gold='#FBBF24', silver='#CBD5E1', teal='#2DD4BF', chip='#1A2337', chipInk='#C9D4E3',
                rose='#F472B6', green='#34D399'),
  'light': dict(bg1='#FFFFFF', bg2='#F3F6FB', panel='#FFFFFF', line='#D8DEE8', ink='#0F172A', mute='#5B6779', faint='#E9EEF6',
                a1='#7C3AED', a2='#0891B2', a3='#0284C7', gold='#B45309', silver='#475569', teal='#0F766E', chip='#EEF2F8', chipInk='#334155',
                rose='#BE185D', green='#047857'),
}
esc = lambda s: html.escape(s, quote=True)
RM = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"

def orrery(c):
    """The hero's right side: a model core floating over a tilted orbital plane. Six agents and tools orbit it;
    each call leaves the core as a packet, and the guardrail ring lets most through and stops the rest.
    Returns (defs, css, markup). CSS drives the motion; the SMIL packets carry class "pk" so reduced motion hides them."""
    import math
    CX, CY, TILT, R, G, RO = 1064, 198, .56, 136, 66, 162  # plane centre, squash, agent orbit, guardrail, outer dial
    T = 6.0  # seconds per call cycle
    agents = [('PLAN', 'a1'), ('RAG', 'a2'), ('MCP', 'teal'), ('ACT', 'gold'), ('EVAL', 'green'), ('MEMORY', 'a3')]
    blocked = {1, 4}
    rep = f'dur="{T}s" repeatCount="indefinite"'
    def anim(attr, values, times, b):
        return f'<animate attributeName="{attr}" values="{values}" keyTimes="{times}" {rep} begin="{b:.1f}s"/>'
    def motion(path, points, times, b):
        return f'<animateMotion path="{path}" keyPoints="{points}" keyTimes="{times}" calcMode="linear" {rep} begin="{b:.1f}s"/>'

    ticks = ''.join(
        f'<line x1="{(RO - (9 if k % 5 == 0 else 4)) * math.cos(math.radians(k*4)):.1f}" y1="{(RO - (9 if k % 5 == 0 else 4)) * math.sin(math.radians(k*4)):.1f}" '
        f'x2="{RO * math.cos(math.radians(k*4)):.1f}" y2="{RO * math.sin(math.radians(k*4)):.1f}"/>' for k in range(90))
    wedge = lambda a0, a1: (f'M0,0 L{RO*math.cos(math.radians(a0)):.1f},{RO*math.sin(math.radians(a0)):.1f} '
                            f'A{RO},{RO} 0 0,1 {RO*math.cos(math.radians(a1)):.1f},{RO*math.sin(math.radians(a1)):.1f} Z')
    sweep = ''.join(f'<path d="{wedge(-(j+1)*5, -j*5)}" fill="{c["a2"]}" fill-opacity="{.2 * (1 - j/9):.3f}"/>' for j in range(9))
    sweep += f'<line x1="0" y1="0" x2="{RO}" y2="0" stroke="{c["a2"]}" stroke-opacity=".7" stroke-width="1.2"/>'

    spokes, packets, nodes, flashes = [], [], [], []
    for i, (name, tone) in enumerate(agents):
        a = math.radians(i * 60 - 90); x, y = R * math.cos(a), R * math.sin(a); b = i * 1.0; col = c[tone]
        spokes.append(f'<line class="flow" x1="0" y1="0" x2="{x:.1f}" y2="{y:.1f}" stroke="{col}"/>')
        out = f'M0,0 L{x:.1f},{y:.1f}'
        if i in blocked:  # the call dies at the guardrail: packet turns rose, a burst, and the whole ring flashes
            f = G / R; gx, gy = G * math.cos(a), G * math.sin(a)
            packets.append(f'<circle class="pk" r="3.4" fill="{c["a2"]}" opacity="0">{motion(out, f"0;{f:.3f};{f:.3f}", "0;.15;1", b)}'
                           f'{anim("opacity", "0;1;1;0;0", "0;.03;.15;.18;1", b)}{anim("fill", f"{c["a2"]};{c["a2"]};{c["rose"]};{c["rose"]}", "0;.12;.15;1", b)}</circle>'
                           f'<circle class="pk" cx="{gx:.1f}" cy="{gy:.1f}" r="3" fill="none" stroke="{c["rose"]}" stroke-width="2" opacity="0">'
                           f'{anim("r", "3;3;20;20", "0;.15;.34;1", b)}{anim("opacity", "0;0;.95;0;0", "0;.149;.15;.34;1", b)}</circle>')
            flashes.append(f'<circle class="pk" r="{G}" fill="none" stroke="{c["rose"]}" stroke-width="2.5" opacity="0">{anim("opacity", "0;0;.85;0;0", "0;.149;.15;.4;1", b)}</circle>')
            halo = ''
        else:  # the call passes: out to the agent, the agent lights up, the answer comes back to the core
            packets.append(f'<circle class="pk" r="3.4" fill="{c["a2"]}" opacity="0">{motion(out, "0;1;1", "0;.3;1", b)}{anim("opacity", "0;1;1;0;0", "0;.03;.28;.3;1", b)}</circle>'
                           f'<circle class="pk" r="3" fill="{c["a1"]}" opacity="0">{motion(f"M{x:.1f},{y:.1f} L0,0", "0;0;1;1", "0;.4;.7;1", b)}'
                           f'{anim("opacity", "0;0;1;1;0;0", "0;.39;.4;.68;.7;1", b)}</circle>')
            halo = f'<rect class="pk" x="-{len(name)*3.6 + 17:.1f}" y="-15" width="{len(name)*7.2 + 34:.1f}" height="30" rx="15" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="1.5" opacity="0">{anim("opacity", "0;0;1;0;0", "0;.29;.31;.52;1", b)}</rect>'
        w = len(name) * 7.2 + 24
        nodes.append(f'<g transform="translate({x:.1f} {y:.1f})"><g class="cspin"><g transform="scale(1 {1/TILT:.4f})">{halo}'
                     f'<rect x="{-w/2:.1f}" y="-10.5" width="{w:.1f}" height="21" rx="10.5" fill="{c["panel"]}" stroke="{col}" stroke-opacity=".7"/>'
                     f'<circle cx="{-w/2 + 10:.1f}" cy="0" r="3" fill="{col}"/>'
                     f'<text class="mono" x="{-w/2 + 18:.1f}" y="3.6" font-size="10.5" font-weight="700" letter-spacing=".6" fill="{c["ink"]}">{name}</text></g></g></g>')

    rules = 'HARD RULES · POLICY · EVALS · GUARDRAILS · AUDIT TRAIL · TRACES · '
    GT = G + 9
    defs = f'''<radialGradient id="orb" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="{c['a2']}"/><stop offset=".55" stop-color="{c['a1']}"/><stop offset="1" stop-color="{c['a1']}" stop-opacity=".85"/></radialGradient>
 <radialGradient id="halo"><stop offset="0" stop-color="{c['a1']}" stop-opacity=".45"/><stop offset=".6" stop-color="{c['a2']}" stop-opacity=".12"/><stop offset="1" stop-color="{c['a2']}" stop-opacity="0"/></radialGradient>
 <radialGradient id="floor"><stop offset="0" stop-color="{c['a1']}" stop-opacity=".22"/><stop offset="1" stop-color="{c['a1']}" stop-opacity="0"/></radialGradient>
 <linearGradient id="beam" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{c['a2']}" stop-opacity=".75"/><stop offset="1" stop-color="{c['a2']}" stop-opacity="0"/></linearGradient>
 <linearGradient id="depthg" gradientUnits="userSpaceOnUse" x1="0" y1="{CY - RO*TILT:.0f}" x2="0" y2="{CY + RO*TILT:.0f}"><stop offset="0" stop-color="#fff" stop-opacity=".28"/><stop offset=".5" stop-color="#fff" stop-opacity=".75"/><stop offset="1" stop-color="#fff"/></linearGradient>
 <mask id="depth" maskUnits="userSpaceOnUse" x="860" y="0" width="420" height="340"><rect x="860" y="0" width="420" height="340" fill="url(#depthg)"/></mask>
 <path id="rules" d="M{-GT},0 a{GT},{GT} 0 1,1 {2*GT},0 a{GT},{GT} 0 1,1 {-2*GT},0"/>'''
    css = f'''.spin{{animation:spin 64s linear infinite}} .cspin{{animation:spin 64s linear infinite reverse}}
 .dial{{animation:spin 120s linear infinite reverse}} .sweep{{animation:spin 7s linear infinite}} .rules{{animation:spin 40s linear infinite reverse}}
 @keyframes spin{{to{{transform:rotate(360deg)}}}}
 .flow{{stroke-width:1.2;stroke-opacity:.45;stroke-dasharray:2 6;animation:flow 1.2s linear infinite}} @keyframes flow{{to{{stroke-dashoffset:-16}}}}
 .rip{{transform-box:fill-box;transform-origin:center;animation:rip 4.8s cubic-bezier(.2,.6,.3,1) infinite}} @keyframes rip{{0%{{transform:scale(.18);opacity:.7}}100%{{transform:scale(1);opacity:0}}}}
 .hx{{transform-box:fill-box;transform-origin:center;animation:spin 16s linear infinite}} .hx2{{animation-duration:10s;animation-direction:reverse}}
 .core{{transform-box:fill-box;transform-origin:center;animation:breathe 3.2s ease-in-out infinite}}
 @keyframes breathe{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.12)}}}}
 .up{{animation:up 2.6s ease-in infinite}} @keyframes up{{0%{{transform:translateY(0);opacity:0}}20%{{opacity:1}}100%{{transform:translateY(-118px);opacity:0}}}}
 .live{{animation:live 1.6s ease-in-out infinite}} @keyframes live{{50%{{opacity:.25}}}}
 @media (prefers-reduced-motion: reduce){{.pk{{display:none}}}}'''
    oy = CY - 34  # the core floats above the plane's centre
    markup = f'''<g mask="url(#depth)"><g transform="translate({CX} {CY}) scale(1 {TILT})">
 <circle r="{RO + 18}" fill="url(#floor)"/>
 <g class="dial" stroke="{c['mute']}" stroke-opacity=".45" stroke-width="1">{ticks}</g>
 <circle r="{RO}" fill="none" stroke="{c['line']}" stroke-width="1.2"/>
 <circle r="{R}" fill="none" stroke="{c['line']}" stroke-dasharray="3 6"/>
 <g class="sweep">{sweep}</g>
 <circle class="rip" r="{RO}" fill="none" stroke="{c['a2']}" vector-effect="non-scaling-stroke"/>
 <circle class="rip" r="{RO}" fill="none" stroke="{c['a1']}" vector-effect="non-scaling-stroke" style="animation-delay:2.4s"/>
 <circle r="{G}" fill="{c['a1']}" fill-opacity=".06" stroke="{c['a1']}" stroke-width="1.6"/>
 <circle r="{G - 5}" fill="none" stroke="{c['a1']}" stroke-opacity=".5" stroke-dasharray="1 4"/>
 <g class="rules"><text class="mono" font-size="8.5" font-weight="700" fill="{c['a1']}" fill-opacity=".9"><textPath href="#rules" textLength="{2*math.pi*GT - 6:.0f}" lengthAdjust="spacing">{esc(rules)}</textPath></text></g>
 {''.join(flashes)}
 <g class="spin">{''.join(spokes)}{''.join(packets)}{''.join(nodes)}</g>
</g></g>
<rect x="{CX - 16}" y="20" width="32" height="{oy - 20}" fill="url(#beam)" opacity=".14"/>
<rect x="{CX - 1}" y="24" width="2" height="{oy - 40}" fill="url(#beam)"/>
{''.join(f'<circle class="up" cx="{CX + dx}" cy="{oy - 24}" r="{r}" fill="{c["a2"]}" style="animation-delay:{d}s"/>' for dx, r, d in ((0, 2.2, 0), (-5, 1.5, .9), (5, 1.6, 1.7)))}
<line x1="{CX}" y1="{oy + 18}" x2="{CX}" y2="{CY}" stroke="{c['a2']}" stroke-opacity=".6" stroke-dasharray="2 3"/>
<ellipse cx="{CX}" cy="{CY}" rx="14" ry="{14*TILT:.1f}" fill="{c['a2']}" fill-opacity=".35"/>
<circle class="core" cx="{CX}" cy="{oy}" r="44" fill="url(#halo)"/>
<polygon class="hx" points="{' '.join(f'{CX + 31*math.cos(math.radians(60*k+30)):.1f},{oy + 31*math.sin(math.radians(60*k+30)):.1f}' for k in range(6))}" fill="none" stroke="{c['a2']}" stroke-width="1.4" stroke-dasharray="14 6"/>
<polygon class="hx hx2" points="{' '.join(f'{CX + 24*math.cos(math.radians(60*k)):.1f},{oy + 24*math.sin(math.radians(60*k)):.1f}' for k in range(6))}" fill="none" stroke="{c['a1']}" stroke-width="1.2"/>
<circle cx="{CX}" cy="{oy}" r="17" fill="url(#orb)"/>
<text class="mono" x="{CX}" y="{oy + 3.4}" font-size="9.5" font-weight="800" letter-spacing="1" text-anchor="middle" fill="#FFFFFF">LLM</text>
<g class="mono" font-size="10.5" font-weight="700" letter-spacing="2" text-anchor="end">
 <text x="1236" y="44" fill="{c['green']}"><tspan class="live">●</tspan> GUARDRAILS ON</text>
 <text x="1236" y="318" font-weight="600" letter-spacing="1" fill="{c['mute']}"><tspan fill="{c['a2']}">●</tspan> call  <tspan fill="{c['a1']}">●</tspan> answer  <tspan fill="{c['rose']}">●</tspan> blocked by policy</text>
</g>'''
    return defs, css, markup

def hero(t):
    c = T[t]
    o_defs, o_css, o_markup = orrery(c)
    phrases = ["I build agentic AI systems, with hard rules around the models.",
               "Full-stack engineer · AI & workflow automation at Zurich Insurance.",
               "2 hackathon podiums among 24,000+ participants · open-source contributor."]
    rot = ''.join(f'<text class="r r{i+1}" x="72" y="236" font-size="21" fill="{c["mute"]}">{esc(p)}</text>' for i,p in enumerate(phrases))
    # `whoami` answers with the username on the same line, typed one character at a time on a 9s loop. Each character
    # (and the cursor's final position) is its resting state, so with reduced motion it simply reads in full.
    user, adv, D, t0, step, hold = 'rogerjeasy', 8.4, 9.0, .9, .14, 8.2
    x0 = 72 + len('$ whoami ') * adv  # same line, right after the command
    pct = lambda s: f'{s / D * 100:.2f}%'
    ty_css = ''.join(f'@keyframes t{k}{{0%{{opacity:0}}{pct(t0 + k*step)}{{opacity:1}}{pct(hold)},100%{{opacity:0}}}} .t{k}{{animation:t{k} {D}s step-end infinite both}}' for k in range(len(user)))
    cur_css = ('@keyframes cur{0%{transform:translateX(0)}' + ''.join(f'{pct(t0 + k*step)}{{transform:translateX({(k+1)*adv:.1f}px)}}' for k in range(len(user)))
               + f'{pct(hold)},100%{{transform:translateX(0)}}}} .cur{{animation:cur {D}s step-end infinite both}}')
    typed = ''.join(f'<text class="mono t{k}" x="{x0 + k*adv:.1f}" y="292" font-size="14" font-weight="700" fill="{c["a2"]}">{ch}</text>' for k, ch in enumerate(user))
    typed += f'<g class="cur" style="transform:translateX({len(user)*adv:.1f}px)"><text class="mono blink" x="{x0 + 1:.1f}" y="292" font-size="14" fill="{c["a2"]}">▍</text></g>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="340" viewBox="0 0 1280 340" role="img" aria-labelledby="t d">
<title id="t">Roger Bavibidila</title><desc id="d">Full-stack and AI engineer in Zurich. Builds agentic AI systems, with hard rules around the models.</desc>
<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['bg1']}"/><stop offset="1" stop-color="{c['bg2']}"/></linearGradient>
 <linearGradient id="name" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox"><stop offset="0" stop-color="{c['ink']}"/><stop offset=".55" stop-color="{c['ink']}"/><stop offset=".78" stop-color="{c['a1']}"/><stop offset="1" stop-color="{c['a2']}"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-0.35 0;0.35 0;-0.35 0" dur="9s" repeatCount="indefinite"/></linearGradient>
 <linearGradient id="bar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c['a1']}"/><stop offset="1" stop-color="{c['a2']}"/></linearGradient>
 <radialGradient id="glow" cx="0.83" cy="0.5" r="0.45"><stop offset="0" stop-color="{c['a1']}" stop-opacity=".18"/><stop offset="1" stop-color="{c['a1']}" stop-opacity="0"/></radialGradient>
 <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{c['faint']}" stroke-width="1"/></pattern>
 <clipPath id="clip"><rect width="1280" height="340" rx="22"/></clipPath>
 {o_defs}
</defs>
<style>
 text{{font-family:{FONT}}}
 .mono{{font-family:{MONO}}}
 .r{{opacity:0;animation:rot 12s infinite}} .r1{{opacity:1}} .r2{{animation-delay:4s}} .r3{{animation-delay:8s}}
 @keyframes rot{{0%{{opacity:0;transform:translateY(8px)}}4%,31%{{opacity:1;transform:none}}35%,100%{{opacity:0;transform:translateY(-6px)}}}}
 {o_css}
 .blink{{animation:blink 1.1s steps(1) infinite}} @keyframes blink{{50%{{opacity:0}}}}
 {ty_css} {cur_css}
 {RM} @media (prefers-reduced-motion: reduce){{.r1{{opacity:1}}}}
</style>
<g clip-path="url(#clip)">
 <rect width="1280" height="340" fill="url(#bg)"/><rect width="1280" height="340" fill="url(#grid)" opacity=".7"/><rect width="1280" height="340" fill="url(#glow)"/>
 {o_markup}
</g>
<rect x=".5" y=".5" width="1279" height="339" rx="22" fill="none" stroke="{c['line']}"/>
<g class="rise"><text class="mono" x="72" y="92" font-size="14" letter-spacing="3" fill="{c['a2']}">FULL-STACK &amp; AI ENGINEER  ·  ZURICH</text></g>
<g class="rise d1"><text x="68" y="168" font-size="66" font-weight="800" letter-spacing="-1.5" fill="url(#name)">Roger Bavibidila</text></g>
<rect class="bar" x="72" y="190" width="168" height="4" rx="2" fill="url(#bar)"/>
{rot}
<g class="rise d2"><text class="mono" x="72" y="292" font-size="14" fill="{c['mute']}"><tspan fill="{c['a1']}">$</tspan> whoami</text>{typed}</g>
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
 'kintwadi': dict(w=632, h=300, pill='WINNER · BEST DESIGN · $2,000 + $2,000 AWS CREDITS', tone='gold', title='Kintwadi', sub='One shared record for family caregiving.',
   lines=['Aurora PostgreSQL with 74 Row-Level Security policies', 'across 34 tables, and a RAG assistant that inherits them.'],
   chips=['Aurora PostgreSQL', 'pgvector', 'Bedrock', 'Next.js'], cta='Devpost'),
 'karma': dict(w=632, h=300, pill='2ND PLACE · DYNATRACE TRACK · $3,000', tone='silver', title='Karma', sub='The reincarnation agent for deprecated services.',
   lines=["Four ADK agents learn a deprecated service's contracts", 'from telemetry and flag silent regressions after cutover.'],
   chips=['Vertex AI Agents', 'Gemini 2.5', 'Dynatrace', 'MCP'], cta='Devpost'),
 'hslu': dict(w=632, h=300, pill='LIVE · RAG', tone='teal', title='HSLU Exam Assistant', sub='AI exam prep, course by course.',
   lines=['Course-specific Q&A, summaries and practice', 'questions grounded in the course material.'],
   chips=['FastAPI', 'Pinecone', 'Next.js', 'RAG'], cta='Open the app'),
 'letusconnect': dict(w=632, h=300, pill='LIVE · REAL-TIME', tone='teal', title='Let Us Connect', sub='Networking and collaboration, in real time.',
   lines=['A platform to meet, connect and work together,', 'with real-time notifications.'],
   chips=['Go Fiber', 'Firestore', 'Next.js'], cta='Open the app'),
}

def frame(c, w, h):
    """Shared panel chrome: gradient fill, corner glow and the slowly rotating border."""
    return f'''<defs><linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['a1']}"/><stop offset=".5" stop-color="{c['line']}"/><stop offset="1" stop-color="{c['a2']}"/>
<animateTransform attributeName="gradientTransform" type="rotate" values="0 .5 .5;360 .5 .5" dur="14s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c['panel']}"/><stop offset="1" stop-color="{c['bg2']}"/></linearGradient>
<radialGradient id="gl" cx="1" cy="0" r=".9"><stop offset="0" stop-color="{c['a1']}" stop-opacity=".12"/><stop offset="1" stop-color="{c['a1']}" stop-opacity="0"/></radialGradient></defs>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="url(#bg)"/><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="url(#gl)"/>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="none" stroke="url(#bd)" stroke-width="1.6"/>'''

SKILLS = [  # left label, title, tagline, colour, chips, shipped in
 ('AI Agents & LLMs', 'AI Agents & LLMs', 'Multi-agent systems, with hard rules around the models.', 'a1',
  ['Google ADK', 'Vertex AI Agent Builder', 'Bedrock AgentCore', 'Strands Agents', 'Amazon Bedrock', 'Claude', 'Gemini 2.5',
   'OpenAI', 'Model Context Protocol', 'RAG', 'LangChain', 'Claude Code plugins', 'Agent evaluation'],
  'Karma · Wick · Kintwadi · win-hackathon · Zurich Insurance'),
 ('Machine Learning', 'Machine Learning', 'Models trained on real signals: audio, video and text.', 'rose',
  ['PyTorch', 'TensorFlow', 'scikit-learn', 'Hugging Face', 'OpenCV', 'Multimodal emotion recognition', 'Feature engineering',
   'Embeddings', 'Semantic search', 'LLMs'],
  'Earkick AI · HSLU Exam Assistant · Kintwadi'),
 ('Backend & APIs', 'Backend & APIs', 'Typed services and clean, documented APIs.', 'a2',
  ['Python', 'Go', 'TypeScript', 'Java', 'SQL', 'FastAPI', 'Go Fiber', 'Spring Boot', 'Express', 'Node.js',
   'OpenAPI / Swagger', 'Pub/Sub', 'Async pipelines'],
  'Karma · HSLU Exam Assistant · Let Us Connect · Zurich Insurance'),
 ('Frontend & TV', 'Frontend & 10-foot UI', 'Interfaces people actually enjoy using, from the browser to the TV.', 'a3',
  ['Next.js', 'React', 'TypeScript', 'Tailwind CSS', 'shadcn/ui', 'Radix', 'Material UI', 'Vite', 'React Native',
   'Vega OS / Fire TV', 'Accessibility: 7:1 contrast, 32 pt'],
  'Kintwadi · Wick · vega-calm-ui · Let Us Connect'),
 ('Data & Vectors', 'Data & Vector Search', 'Access control enforced by the database, not by the prompt.', 'teal',
  ['PostgreSQL', 'Aurora Serverless v2', 'Row-Level Security', 'pgvector (HNSW)', 'Pinecone', 'Redis', 'MongoDB',
   'Firestore', 'Cosmos DB', 'MySQL'],
  'Kintwadi: 74 RLS policies on 34 tables · HSLU Exam Assistant'),
 ('Cloud & DevOps', 'Cloud & DevOps', 'Infrastructure as code, tested and deployed on every push.', 'gold',
  ['AWS', 'Google Cloud', 'Cloud Run', 'Azure', 'AKS', 'Docker', 'Terraform', 'GitHub Actions', 'CI/CD', 'Nginx',
   'Vercel', 'Render'],
  'Karma on Cloud Run · Wick with Terraform · Zurich Insurance on AKS'),
 ('Observability & QA', 'Observability & Quality', "If an agent can't be observed, it can't be trusted.", 'green',
  ['Dynatrace', 'Davis AI', 'OpenTelemetry', 'Prometheus', 'Grafana', 'Loki', 'Sentry', 'k6', 'Vitest', 'JUnit', 'SonarCloud'],
  'Karma: Dynatrace MCP + OpenTelemetry · Wick: ~6,500 tests'),
]

def skills(t):
    c = T[t]; W, H, N, S = 1280, 450, len(SKILLS), 4.0
    D, p = N * S, 100 / N
    rows, panels = [], []
    for i, (short, title, tag, tone, chips, shipped) in enumerate(SKILLS):
        col, ry, dl = c[tone], 100 + i * 46, f'animation-delay:{i*S:.1f}s'
        rows.append(f'''<text class="mono" x="54" y="{ry+24}" font-size="12" fill="{c['mute']}">{i+1:02d}</text>
<text x="92" y="{ry+25}" font-size="16" font-weight="600" fill="{c['mute']}">{esc(short)}</text>
<g class="on row o{i}" style="{dl}"><rect x="32" y="{ry}" width="326" height="38" rx="10" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".45"/>
<rect x="32" y="{ry+9}" width="3" height="20" rx="1.5" fill="{col}"/>
<text class="mono" x="54" y="{ry+24}" font-size="12" font-weight="700" fill="{col}">{i+1:02d}</text>
<text x="92" y="{ry+25}" font-size="16" font-weight="600" fill="{c['ink']}">{esc(short)}</text></g>
<rect class="pb" x="44" y="{ry+34}" width="302" height="2" rx="1" fill="{col}" style="{dl}"/>''')
        x0, cx, cy, ch_out = 432, 432, 196, []
        for k, ch in enumerate(chips):
            w = int(len(ch) * 7.9 + 40)
            if cx + w > 1240: cx, cy = x0, cy + 44
            ch_out.append(f'<g class="chip" style="animation-delay:{i*S + .2 + k*.06:.2f}s"><rect x="{cx}" y="{cy}" width="{w}" height="32" rx="16" fill="{c["chip"]}" stroke="{c["line"]}"/>'
                          f'<circle cx="{cx+16}" cy="{cy+16}" r="3.5" fill="{col}"/><text x="{cx+27}" y="{cy+21}" font-size="14" font-weight="600" fill="{c["chipInk"]}">{esc(ch)}</text></g>')
            cx += w + 10
        panels.append(f'''<g class="on pn o{i}" style="{dl}">
<text class="mono" x="432" y="74" font-size="13" font-weight="700" letter-spacing="2" fill="{col}">{i+1:02d} / {N:02d}</text>
<text x="430" y="124" font-size="36" font-weight="800" letter-spacing="-.6" fill="{c['ink']}">{esc(title)}</text>
<text x="432" y="160" font-size="17" fill="{c['mute']}">{esc(tag)}</text>
{''.join(ch_out)}
<text x="432" y="{max(cy + 78, 384)}" font-size="14.5" fill="{c['ink']}"><tspan class="mono" font-size="11.5" font-weight="700" letter-spacing="2" fill="{col}">SHIPPED IN  </tspan>{esc(shipped)}</text></g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">Tech stack, by field</title><desc id="d">{esc(' '.join(f'{s[1]}: {", ".join(s[4])}.' for s in SKILLS))}</desc>
{frame(c, W, H)}
<style>text{{font-family:{FONT}}} .mono{{font-family:{MONO}}}
 .on{{opacity:0;animation:on {D:.0f}s infinite both}} .o0{{opacity:1}}
 @keyframes on{{0%{{opacity:0;transform:translateX(12px)}}{p*.12:.2f}%,{p*.93:.2f}%{{opacity:1;transform:none}}{p:.2f}%,100%{{opacity:0;transform:translateX(-8px)}}}}
 .row{{animation-name:row}} @keyframes row{{0%{{opacity:0}}{p*.08:.2f}%,{p*.95:.2f}%{{opacity:1}}{p:.2f}%,100%{{opacity:0}}}}
 .chip{{animation:chip {D:.0f}s cubic-bezier(.2,.8,.2,1) infinite both}}
 @keyframes chip{{0%{{opacity:0;transform:translateY(12px)}}{p*.2:.2f}%,100%{{opacity:1;transform:none}}}}
 .pb{{opacity:0;transform-box:fill-box;transform-origin:0 50%;animation:pb {D:.0f}s linear infinite both}}
 @keyframes pb{{0%{{opacity:.9;transform:scaleX(0)}}{p:.2f}%{{opacity:.9;transform:scaleX(1)}}{p+.01:.2f}%,100%{{opacity:0;transform:scaleX(1)}}}}
 {RM}</style>
<text class="mono" x="48" y="54" font-size="13" font-weight="700" letter-spacing="3" fill="{c['a2']}">TECH STACK</text>
<text x="48" y="78" font-size="14" fill="{c['mute']}">grouped by field</text>
{''.join(rows)}
<rect x="392" y="40" width="1" height="{H-80}" fill="{c['line']}"/>
{''.join(panels)}
</svg>'''

USER = 'rogerjeasy'
YEAR_QUERY = '''query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){createdAt contributionsCollection(from:$from,to:$to){
 totalCommitContributions totalPullRequestContributions totalIssueContributions totalRepositoryContributions
 contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}'''

def contributions():
    """Every contribution since the account was created, one GraphQL call per year (the API's maximum span).
    Returns None without a token, in which case the activity SVGs on disk are kept."""
    import json, urllib.request, datetime
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    if not token: return None
    def year(y):
        body = {'query': YEAR_QUERY, 'variables': {'login': USER, 'from': f'{y}-01-01T00:00:00Z', 'to': f'{y}-12-31T23:59:59Z'}}
        req = urllib.request.Request('https://api.github.com/graphql', data=json.dumps(body).encode(),
                                     headers={'Authorization': f'bearer {token}', 'User-Agent': USER})
        return json.load(urllib.request.urlopen(req, timeout=30))['data']['user']
    today = datetime.date.today()
    first = year(today.year)
    years = {today.year: first['contributionsCollection']}
    for y in range(int(first['createdAt'][:4]), today.year):
        years[y] = year(y)['contributionsCollection']
    return {'today': today.isoformat(), 'years': dict(sorted(years.items()))}

def mix(a, b, k):
    """Blend hex colour a towards b by k (0..1)."""
    pa, pb = [int(a[i:i+2], 16) for i in (1, 3, 5)], [int(b[i:i+2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(x + (y - x) * k):02X}' for x, y in zip(pa, pb))

def activity(t, data):
    """All-time activity, which the profile's own last-year graph cannot show: a 3D skyline with one row per year
    and one tower per month since day one, beside the lifetime totals and streaks."""
    import datetime
    c = T[t]; W, H = 1280, 540
    D = datetime.date.fromisoformat
    today, years = D(data['today']), {int(y): v for y, v in data['years'].items()}
    days = sorted((D(d['date']), d['contributionCount']) for v in years.values()
                  for w in v['contributionCalendar']['weeks'] for d in w['contributionDays'] if D(d['date']) <= today)
    total = sum(v['contributionCalendar']['totalContributions'] for v in years.values())
    since = next(d for d, n in days if n)
    # Streaks: runs of consecutive days with at least one contribution. Today may simply not have started yet.
    runs, run, start = [], 0, None
    for d, n in days:
        if n: start = d if not run else start; run += 1
        else: run = 0
        runs.append((run, start, d))
    lr, ls, le = max(runs, key=lambda r: r[0])
    cr, cs, ce = runs[-1] if runs[-1][0] or len(runs) < 2 else runs[-2]
    sums = lambda k: sum(v[k] for v in years.values())
    month = {}
    for d, n in days: month[(d.year, d.month)] = month.get((d.year, d.month), 0) + n
    ys = sorted(years)
    by_year = {y: years[y]['contributionCalendar']['totalContributions'] for y in ys}
    prev = by_year.get(today.year - 1) or 0
    growth = f'{by_year[today.year] / prev:.1f}×' if prev else '—'
    best = max(month, key=month.get)
    fmt = lambda d: d.strftime('%b %-d, %Y')
    span = lambda a, b: f'{a.strftime("%b %-d")} – {b.strftime("%b %-d, %Y")}' if a.year == b.year else f'{fmt(a)} – {fmt(b)}'

    # Projection: months run to the right, years run into the distance with the newest year at the back.
    ux, uy, vx, vy = 38.0, 9.5, -34.0, 21.0
    rows = len(ys); ox, oy = 722, 206
    g0, g1 = .12, .88
    sux, suy, svx, svy = (g1-g0)*ux, (g1-g0)*uy, (g1-g0)*vx, (g1-g0)*vy
    cap = max(month.values()) or 1
    hgt = lambda n: 2 if n == 0 else 5 + 158 * (n / cap) ** .6
    P = lambda w, d, s=0, r=0: (ox + (w + s) * ux + (d + r) * vx, oy + (w + s) * uy + (d + r) * vy)
    f = lambda v: f'{v:.1f}'.rstrip('0').rstrip('.')
    shade = '#000000' if t == 'dark' else '#1E1B4B'
    row_col = lambda y: mix(c['a1'], c['a2'], (ys.index(y)) / max(1, rows - 1)) if by_year[y] else mix(c['line'], c['bg1'], .2)
    css = ''.join(f'.y{y} .t{{fill:{row_col(y)}}} .y{y} .a{{fill:{mix(row_col(y), shade, .3)}}} .y{y} .b{{fill:{mix(row_col(y), shade, .48)}}}' for y in ys)
    css += f'.ghost{{fill:none;stroke:{c["line"]};stroke-dasharray:3 3}} .floor{{fill:{mix(c["line"], c["bg1"], .35)}}}'
    towers = []
    for d, y in enumerate(reversed(ys)):  # back row first so nearer rows paint over it
        for m in range(1, 13):
            w = m - 1; ax, ay = P(w, d, g0, g0)
            if (y, m) < (since.year, since.month): continue
            top = lambda h, cls: f'<path class="{cls}" d="M{f(ax)},{f(ay-h)}l{f(sux)},{f(suy)}l{f(svx)},{f(svy)}l{f(-sux)},{f(-suy)}z"/>'
            if (y, m) > (today.year, today.month):  # the rest of this year, still to be built
                towers.append(top(0, 'ghost')); continue
            n = month.get((y, m), 0); h = hgt(n)
            if n == 0:
                towers.append(top(1.5, 'floor')); continue
            dx, dy, bx, by = ax + svx, ay + svy, ax + sux, ay + suy
            towers.append(f'<g class="c y{y}" style="animation-delay:{.3 + (rows - 1 - d) * .16 + w * .045:.2f}s">'
                          f'<path class="a" d="M{f(dx)},{f(dy-h)}l{f(sux)},{f(suy)}v{f(h)}l{f(-sux)},{f(-suy)}z"/>'
                          f'<path class="b" d="M{f(bx)},{f(by-h)}l{f(svx)},{f(svy)}v{f(h)}l{f(-svx)},{f(-svy)}z"/>{top(h, "t")}</g>')
    labels = []
    for d, y in enumerate(reversed(ys)):
        rx, ry = P(12, d, .1, .55)  # labels sit at the row's right end, where no nearer tower can cover them
        labels.append(f'<text x="{f(rx + 6)}" y="{f(ry + 4)}" font-size="13" font-weight="700" fill="{row_col(y) if by_year[y] else c["mute"]}">'
                      f'<tspan class="mono" font-size="11.5" fill="{c["mute"]}">{y}</tspan><tspan dx="7">{by_year[y]:,}</tspan></text>')
    for w, m in enumerate('JFMAMJJASOND'):
        mx, my = P(w, rows, .5, .45)
        labels.append(f'<text class="mono" x="{f(mx)}" y="{f(my + 12)}" text-anchor="middle" font-size="11" fill="{c["mute"]}">{m}</text>')
    nx, ny = P(today.month - 1, 0, .5, .5); nh = hgt(month.get((today.year, today.month), 0))
    bw, bd = best[1] - 1, rows - 1 - ys.index(best[0])
    bx_, by_ = P(bw, bd, .5, .5); bh = hgt(month[best])
    scan_to = (12 * ux, 12 * uy)
    s0, s1 = P(0, 0), P(0, rows)
    sheet = f'M{f(s0[0])},{f(s0[1])}L{f(s1[0])},{f(s1[1])}L{f(s1[0])},{f(s1[1] - 176)}L{f(s0[0])},{f(s0[1] - 176)}z'

    stats = [(f'{cr}', 'CURRENT STREAK', span(cs, ce) if cr else 'starts today', 'a1'),
             (f'{lr}', 'LONGEST STREAK', span(ls, le), 'teal'),
             (growth, f'{today.year} VS {today.year - 1}', f'{by_year[today.year]:,} so far vs {prev:,}', 'gold')]
    stat_svg = ''.join(f'''<g class="rise" style="animation-delay:{.25 + i*.1:.2f}s"><text x="48" y="{258 + i*70}" font-size="30" font-weight="800" letter-spacing="-.5" fill="{c[tone]}">{v}<tspan dx="8" font-size="13" font-weight="600" letter-spacing="0" fill="{c['mute']}">{'days' if i < 2 else ''}</tspan></text>
<text class="mono" x="50" y="{278 + i*70}" font-size="10.5" font-weight="700" letter-spacing="1.6" fill="{c['ink']}">{k}</text>
<text x="50" y="{295 + i*70}" font-size="12.5" fill="{c['mute']}">{esc(s)}</text></g>''' for i, (v, k, s, tone) in enumerate(stats))
    kinds = [(sums('totalCommitContributions'), 'commits'), (sums('totalPullRequestContributions'), 'pull requests'),
             (sums('totalIssueContributions'), 'issues'), (sums('totalRepositoryContributions'), 'repositories')]
    kinds_svg = ''.join(f'<text x="{48 + (i % 2) * 150}" y="{H - 62 + (i // 2) * 22}" font-size="13" fill="{c["mute"]}"><tspan font-weight="700" fill="{c["ink"]}">{n:,}</tspan> {k}</text>' for i, (n, k) in enumerate(kinds))
    desc = (f'{total:,} total contributions since {fmt(since)}. Current streak {cr} days, longest streak {lr} days ({span(ls, le)}). '
            + ' '.join(f'{y}: {by_year[y]:,}.' for y in ys) + ' ' + ', '.join(f'{n:,} {k}' for n, k in kinds) + '.')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">All-time activity</title><desc id="d">{esc(desc)}</desc>
{frame(c, W, H)}
<defs><linearGradient id="scan" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{c['a2']}" stop-opacity=".3"/><stop offset="1" stop-color="{c['a2']}" stop-opacity="0"/></linearGradient>
<linearGradient id="bm" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{c['a2']}"/><stop offset="1" stop-color="{c['a2']}" stop-opacity="0"/></linearGradient>
<linearGradient id="tot" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c['a1']}"/><stop offset="1" stop-color="{c['a2']}"/></linearGradient></defs>
<style>text{{font-family:{FONT}}} .mono{{font-family:{MONO}}} {css}
 .c{{transform-box:fill-box;transform-origin:50% 100%;animation:grow 1.2s cubic-bezier(.2,.9,.25,1.1) both}} @keyframes grow{{from{{transform:scaleY(0)}}}}
 .scan{{animation:scan 10s cubic-bezier(.45,0,.55,1) 3s infinite both}}
 @keyframes scan{{0%{{transform:translate(0,0);opacity:0}}6%{{opacity:1}}60%{{transform:translate({f(scan_to[0])}px,{f(scan_to[1])}px);opacity:1}}66%,100%{{transform:translate({f(scan_to[0])}px,{f(scan_to[1])}px);opacity:0}}}}
 .ping{{transform-box:fill-box;transform-origin:center;animation:ping 2.2s ease-out infinite}} @keyframes ping{{0%{{transform:scale(.3);opacity:1}}100%{{transform:scale(2.6);opacity:0}}}}
 .live{{animation:live 1.6s ease-in-out infinite}} @keyframes live{{50%{{opacity:.3}}}}
 .rise{{animation:rise .9s ease-out both}} @keyframes rise{{from{{opacity:0;transform:translateY(8px)}}}}
 .pop{{animation:rise .8s ease-out 2.4s both}}
 {RM}</style>
<text class="mono" x="48" y="56" font-size="13" font-weight="700" letter-spacing="3" fill="{c['a2']}">ACTIVITY · ALL TIME</text>
<g class="rise"><text x="44" y="138" font-size="72" font-weight="800" letter-spacing="-2.5" fill="url(#tot)">{total:,}</text>
<text class="mono" x="50" y="166" font-size="11.5" font-weight="700" letter-spacing="2" fill="{c['ink']}">TOTAL CONTRIBUTIONS</text>
<text x="50" y="188" font-size="14" fill="{c['mute']}">{fmt(since)} – Present</text></g>
<rect x="48" y="210" width="300" height="1" fill="{c['line']}"/>
{stat_svg}
<rect x="48" y="{H - 92}" width="300" height="1" fill="{c['line']}"/>
{kinds_svg}
<g>{''.join(towers)}</g>
<g class="scan"><path d="{sheet}" fill="url(#scan)"/><path d="M{f(s0[0])},{f(s0[1])}L{f(s1[0])},{f(s1[1])}" stroke="{c['a2']}" stroke-width="2" stroke-linecap="round"/></g>
{''.join(labels)}
<g class="pop"><path d="M{f(bx_)},{f(by_ - bh - 4)}v-20h-14" fill="none" stroke="{c['gold']}" stroke-width="1.2"/><circle cx="{f(bx_)}" cy="{f(by_ - bh - 4)}" r="2.4" fill="{c['gold']}"/>
 <text class="mono" x="{f(bx_ - 18)}" y="{f(by_ - bh - 20)}" font-size="11" font-weight="700" text-anchor="end" fill="{c['gold']}">BEST MONTH · {month[best]:,}</text></g>
<g class="pop"><rect x="{f(nx - 1)}" y="{f(ny - nh - 70)}" width="2" height="66" fill="url(#bm)"/>
 <ellipse class="ping" cx="{f(nx)}" cy="{f(ny - nh)}" rx="10" ry="5" fill="none" stroke="{c['a2']}" stroke-width="1.5"/>
 <text class="mono" x="{f(nx + 8)}" y="{f(ny - nh - 62)}" font-size="11" font-weight="700" fill="{c['a2']}"><tspan class="live">●</tspan> NOW</text></g>
</svg>'''

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
contrib = contributions()
if contrib is None: print('No GITHUB_TOKEN: keeping the activity SVGs on disk.')
for t in T:
    if contrib: open(f'{OUT}/activity-{t}.svg', 'w').write(activity(t, contrib))
    open(f'{OUT}/hero-{t}.svg', 'w').write(hero(t))
    open(f'{OUT}/divider-{t}.svg', 'w').write(divider(t))
    open(f'{OUT}/footer-{t}.svg', 'w').write(footer(t))
    open(f'{OUT}/skills-{t}.svg', 'w').write(skills(t))
    for k, v in CARDS.items(): open(f'{OUT}/card-{k}-{t}.svg', 'w').write(card(t, **v))
print(sorted(os.listdir(OUT)))
