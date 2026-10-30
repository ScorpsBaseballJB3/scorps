import math, base64
from playwright.sync_api import sync_playwright

LOGO = "data:image/png;base64," + base64.b64encode(open("logo.png", "rb").read()).decode()
P, PD, INK, MUT, LINE, RED, GRN = "#6d3fc0", "#2a1650", "#16121f", "#6b6480", "#d9d2e8", "#c0392b", "#1e8e5a"


def fig(theta, label=None, arc=None, coach=True, lift=False, bad_elbow=False, w=360, h=230):
    """Side view of an athlete lying on his back, head on the left, throwing arm out toward you at 90/90.
    theta = forearm angle from straight up; negative = toward head (ER), positive = toward feet (IR)."""
    SK, SKD, SH, SHD, PANT, HAIR, CO, COD = "#e9c39f", "#b98b63", "#5b3a9e", "#3b2470", "#2c2c38", "#3a2a1e", "#8d97a6", "#5d6674"
    ly = -12 if lift else 0
    ex, ey = (124, 150) if not bad_elbow else (140, 160)
    L = 74
    a = math.radians(theta)
    hx, hy = ex + L * math.sin(a), ey - L * math.cos(a)
    s = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    # table
    s.append(f'<rect x="8" y="178" width="{w-16}" height="12" rx="4" fill="#d8d2e6"/><rect x="30" y="190" width="8" height="30" fill="#d8d2e6"/><rect x="{w-38}" y="190" width="8" height="30" fill="#d8d2e6"/>')
    # legs (knees bent, feet flat)
    s.append(f'<path d="M232,160 L282,112" stroke="{PANT}" stroke-width="26" stroke-linecap="round"/>')
    s.append(f'<path d="M282,112 L318,168" stroke="{SK}" stroke-width="17" stroke-linecap="round"/>')
    s.append(f'<path d="M262,120 L290,112" stroke="{PANT}" stroke-width="22" stroke-linecap="round"/>')
    s.append(f'<path d="M306,172 q4,-10 16,-6 l22,6 q6,4 0,6 l-38,0 z" fill="#f2f2f2" stroke="#9a9a9a" stroke-width="2"/>')
    # torso (shirt) with chest rise; shoulder end lifts if lift
    s.append(f'<path d="M86,178 L86,{150+ly} Q92,{128+ly} 116,{126+ly} Q150,122 176,132 Q205,138 236,140 L244,178 Z" fill="{SH}"/>')
    s.append(f'<path d="M222,138 L244,178 L206,178 Z" fill="{PANT}"/>')
    # neck + head (face up)
    s.append(f'<path d="M70,{156+ly/2} L90,{152+ly/2}" stroke="{SK}" stroke-width="15" stroke-linecap="round"/>')
    s.append(f'<ellipse cx="48" cy="{150+ly/3}" rx="24" ry="22" fill="{SK}"/>')
    s.append(f'<path d="M26,{146+ly/3} Q28,{124+ly/3} 50,{127+ly/3} Q40,{136+ly/3} 30,{160+ly/3} Z" fill="{HAIR}"/>')
    s.append(f'<path d="M58,{129+ly/3} q5,-8 9,-1" fill="{SK}" stroke="{SKD}" stroke-width="1.5"/>')
    s.append(f'<circle cx="56" cy="{140+ly/3}" r="2" fill="{HAIR}"/>')
    # towel roll under elbow
    s.append(f'<ellipse cx="{ex}" cy="171" rx="26" ry="8" fill="#ffffff" stroke="#b9b2c8" stroke-width="2"/>')
    # shoulder cap + upper arm coming toward viewer
    s.append(f'<ellipse cx="114" cy="{140+ly}" rx="20" ry="17" fill="{SH}"/>')
    s.append(f'<path d="M110,{142+ly} L{ex},{ey}" stroke="{SK}" stroke-width="24" stroke-linecap="round"/>')
    # dotted 0° line + arc
    if arc is not None:
        r = 52
        x1, y1 = ex + r * math.sin(math.radians(arc)), ey - r * math.cos(math.radians(arc))
        s.append(f'<line x1="{ex}" y1="{ey}" x2="{ex}" y2="{ey-L-14}" stroke="#7a7290" stroke-width="2" stroke-dasharray="3 4"/>')
        s.append(f'<text x="{ex}" y="{ey-L-18}" text-anchor="middle" font-size="12" fill="#7a7290" font-family="Inter">0°</text>')
        s.append(f'<path d="M{ex},{ey-r} A{r},{r} 0 0 {1 if arc>0 else 0} {x1:.1f},{y1:.1f}" fill="none" stroke="{P}" stroke-width="3.5" stroke-dasharray="6 5"/>')
    # forearm + hand
    s.append(f'<line x1="{ex}" y1="{ey}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{SK}" stroke-width="17" stroke-linecap="round"/>')
    s.append(f'<line x1="{ex}" y1="{ey}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{SKD}" stroke-width="17" stroke-linecap="round" stroke-opacity=".18"/>')
    s.append(f'<g transform="translate({hx:.1f},{hy:.1f}) rotate({theta})"><ellipse cx="0" cy="-8" rx="10" ry="14" fill="{SK}" stroke="{SKD}" stroke-width="1.5"/><path d="M-6,-16 l0,-6 M0,-18 l0,-7 M6,-16 l0,-6" stroke="{SKD}" stroke-width="2" stroke-linecap="round"/></g>')
    s.append(f'<circle cx="{ex}" cy="{ey}" r="12" fill="{SK}" stroke="{SKD}" stroke-width="2"/>')
    # phone on forearm
    pm = .5
    px, py = ex + (hx - ex) * pm, ey + (hy - ey) * pm
    s.append(f'<g transform="translate({px:.1f},{py:.1f}) rotate({theta})"><rect x="-8" y="-17" width="16" height="30" rx="3" fill="#1b1b22" stroke="#fff" stroke-width="2"/><rect x="-5" y="-13" width="10" height="20" rx="1" fill="{P}"/></g>')
    if coach:
        # coach's arm reaching down, flat hand on the front of the shoulder
        s.append(f'<path d="M14,38 L104,{118+ly}" stroke="{CO}" stroke-width="20" stroke-linecap="round"/>')
        s.append(f'<path d="M14,38 L104,{118+ly}" stroke="{COD}" stroke-width="20" stroke-linecap="round" stroke-opacity=".25"/>')
        s.append(f'<path d="M108,{126+ly} q8,-16 26,-12 q8,4 2,10 q-14,8 -28,2 z" fill="{SK}" stroke="{SKD}" stroke-width="1.5"/>')
        s.append(f'<text x="8" y="26" font-size="12" font-weight="800" fill="{GRN}" font-family="Inter">YOUR HAND</text>')
        s.append(f'')
    if lift:
        s.append(f'<path d="M100,176 l0,-36 m-8,10 l8,-10 l8,10" fill="none" stroke="{RED}" stroke-width="4" stroke-linecap="round"/>')
    if bad_elbow:
        s.append(f'<path d="M118,176 l26,-4" stroke="{RED}" stroke-width="4" stroke-linecap="round"/><path d="M140,166 l6,6 l-8,4" fill="none" stroke="{RED}" stroke-width="4" stroke-linecap="round"/>')
    if label:
        lx = 250
        s.append(f'<text x="{lx}" y="58" text-anchor="middle" font-size="26" font-weight="900" fill="{P}" font-family="Inter Display">{label}</text>')
    s.append(f'<text x="14" y="{h-4}" font-size="11" fill="#7a7290" font-family="Inter">HEAD</text><text x="{w-14}" y="{h-4}" text-anchor="end" font-size="11" fill="#7a7290" font-family="Inter">FEET</text>')
    s.append("</svg>")
    return "".join(s)


STEPS = [
    ("Set up", fig(0, None, None), "On his back, arm out level with the shoulder, elbow bent 90°, forearm straight up. Towel under the elbow so it sits level.",
     "Upper arm level. Elbow at 90°."),
    ("Lock the shoulder", fig(0, None, None), "Flat hand on the front of his shoulder. Phone (Level app) flat against the forearm. Forearm straight up reads 0°.",
     "Same phone spot every time."),
    ("External rotation", fig(-105, "ER", -105), "Slowly lower his hand back toward his head. Stop at firm resistance or when the shoulder pushes into your hand. Read the angle.",
     "You move the arm. He stays relaxed."),
    ("Internal rotation", fig(50, "IR", 50), "Slowly lower his hand toward his feet. Stop the moment the front of the shoulder starts to rise. Read the angle.",
     "IR ends early. That's normal."),
]
DONTS = [
    (fig(70, None, None, lift=True), "Shoulder lifting", "Letting the shoulder rise to get more IR. Fake numbers."),
    (fig(-60, None, None, bad_elbow=True), "Arm drifting", "Elbow sliding off 90° out or down. Reset and redo."),
]

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: Letter; margin: 0 }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ font-family: Inter, sans-serif; color: {INK}; font-size: 11.5pt; line-height: 1.4 }}
.page {{ width: 8.5in; height: 11in; padding: .45in .55in; position: relative; overflow: hidden; page-break-after: always; display: flex; flex-direction: column; gap: 14px }}
.band {{ position: absolute; inset: 0 0 auto 0; height: 1.72in; background: {PD} }}
.hd {{ position: relative; display: flex; align-items: center; gap: 18px; color: #fff; height: 1.05in }}
.hd img {{ height: .95in }}
.kick {{ font-size: 9pt; letter-spacing: .25em; font-weight: 700; color: #c9b3f5 }}
h1 {{ font-family: 'Inter Display'; font-weight: 900; font-size: 31pt; line-height: .95; letter-spacing: -.01em }}
.sub {{ position: relative; color: #e6dcfa; font-size: 10.5pt; margin-top: -6px }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 16px }}
.step {{ border: 2px solid {LINE}; border-radius: 14px; padding: 12px 14px; display: flex; flex-direction: column; gap: 6px; break-inside: avoid }}
.num {{ font-family: 'Inter Display'; font-weight: 900; font-size: 26pt; color: {P}; line-height: .9 }}
.st {{ display: flex; align-items: baseline; gap: 10px }}
h3 {{ font-family: 'Inter Display'; font-weight: 800; font-size: 15pt }}
.cue {{ font-weight: 700; color: {P}; font-size: 10pt }}
.cue::before {{ content: "▸ " }}
svg {{ width: 100%; height: auto; max-height: 1.72in }}
h2 {{ font-family: 'Inter Display'; font-weight: 900; font-size: 18pt; letter-spacing: .02em; text-transform: uppercase; display: flex; align-items: center; gap: 10px }}
h2::after {{ content: ""; flex: 1; height: 3px; background: {P} }}
.tips {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6px 22px; font-size: 10.5pt }}
.tips div::before {{ content: "✓ "; color: {GRN}; font-weight: 900 }}
.tips.x div::before {{ content: "✕ "; color: {RED} }}
.no svg {{ max-height: 1.15in }}
.p2 {{ gap: 10px }}
.p2 .flag {{ padding: 8px 14px }}
.no {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px }}
.nocard {{ border: 2px solid {RED}; border-radius: 14px; padding: 10px 14px }}
.nocard h3 {{ color: {RED} }}
.nocard h3::before {{ content: "✕  " }}
.flags {{ display: flex; flex-direction: column; gap: 10px }}
.flag {{ display: grid; grid-template-columns: 1.5in 1fr; gap: 14px; align-items: center; border-left: 6px solid {P}; background: #f4effc; padding: 12px 16px; border-radius: 0 12px 12px 0 }}
.flag .big {{ font-family: 'Inter Display'; font-weight: 900; font-size: 20pt; color: {PD}; line-height: 1 }}
.flag .lab {{ font-size: 9pt; letter-spacing: .14em; font-weight: 700; color: {MUT}; text-transform: uppercase }}
.calc {{ border: 2px dashed {P}; border-radius: 14px; padding: 14px 18px; font-size: 11pt }}
.calc b {{ color: {P} }}
.next {{ display: grid; grid-template-columns: repeat(3,1fr); gap: 10px }}
.next div {{ background: {PD}; color: #fff; border-radius: 12px; padding: 12px 14px; font-size: 10.5pt }}
.next b {{ display: block; font-family: 'Inter Display'; font-size: 13pt; color: #c9b3f5; margin-bottom: 2px }}
.foot {{ margin-top: auto; font-size: 8.5pt; color: {MUT}; border-top: 1px solid {LINE}; padding-top: 8px }}
</style></head><body>
<div class="page"><div class="band"></div>
 <div class="hd"><img src="{LOGO}"><div><div class="kick">SCORPS THROWING · COACH ONLY</div><h1>Shoulder range<br>of motion</h1></div></div>
 <div class="sub">Day 1 screen · about 2 minutes per player · both arms · before throwing</div>
 <div class="grid">{''.join(f'<div class="step"><div class="st"><span class="num">{i+1}</span><h3>{t}</h3></div>{svg}<div>{d}</div><div class="cue">{c}</div></div>' for i,(t,svg,d,c) in enumerate(STEPS))}</div>
 <h2>Get clean numbers</h2>
 <div class="tips"><div>Measure before throwing, never after</div><div>Same table, same position, every time</div><div>Take 2 reads, record the higher one</div><div>Throwing arm first, then the other arm</div></div>
 <div class="foot">Phone: iPhone Measure app → Level, or any free inclinometer app. Lay it along the outside of the forearm.</div>
</div>
<div class="page p2"><div class="band" style="height:.9in"></div>
 <div class="hd" style="height:.45in"><div><div class="kick">SCORPS THROWING · COACH ONLY</div><h1 style="font-size:22pt">What not to do · what to look for</h1></div></div>
 <h2 style="margin-top:22px">Don't</h2>
 <div class="no">{''.join(f'<div class="nocard">{s}<h3>{t}</h3><div>{d}</div></div>' for s,t,d in DONTS)}</div>
 <div class="tips x"><div>Don't force past firm resistance</div><div>Don't let him help move the arm</div><div>Don't measure the day after a big outing</div><div>Don't compare kids to each other, compare arms</div></div>
 <h2>Do the math</h2>
 <div class="calc"><b>Total arc</b> = ER + IR, for each arm. &nbsp;Then: <b>throwing arm total − other arm total</b>. The MASTER sheet does this for you and turns the cell red if it's off by more than 5°.</div>
 <h2>Red flags</h2>
 <div class="flags">
  <div class="flag"><div><div class="lab">Total arc</div><div class="big">5°+ lower</div></div><div>Throwing arm's total arc is more than 5° below the other arm. The biggest one to watch.</div></div>
  <div class="flag"><div><div class="lab">Internal rotation</div><div class="big">20°+ lower</div></div><div>Some IR loss on the throwing arm is normal. 20° or more less than the other arm is not.</div></div>
  <div class="flag"><div><div class="lab">External rotation</div><div class="big">Any loss</div></div><div>Throwing arm should have <i>more</i> ER than the other arm. Less ER (5°+) is a flag.</div></div>
 </div>
 <h2>If you see a flag</h2>
 <div class="next"><div><b>Recheck</b>Measure again next week. One bad read happens.</div><div><b>Back off</b>Still there? Keep him at moderate effort, no pulldowns.</div><div><b>Refer</b>Flag plus pain, or it won't clear: tell the parents, see a PT or athletic trainer.</div></div>
 <div class="foot">A screening tool for spotting changes, not a diagnosis. Normal throwers' arms differ side to side; the trend over time matters most.</div>
</div></body></html>"""
open("rom.html", "w").write(html)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); pg.goto("file:///home/claude/scorps/rom.html"); pg.wait_for_timeout(300)
    pg.pdf(path="Scorps_ROM_Guide.pdf", format="Letter", print_background=True)
    b.close()
print("ok")
