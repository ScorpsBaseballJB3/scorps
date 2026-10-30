from playwright.sync_api import sync_playwright
P=[("Ryan Campion",17),("Cam Carlisle",16),("Cam Cote",13),("Jared Davis",14),("Maddux Fredericks",17),("Liam Kelley",15),("Andrew Knychalski",13),("Nick Miller",15),("Colby Paré",16),("Kenny Pirches",17),("Eli Sydney",13),("",None)]
def box(t): return f'<span class="bx"></span>{t}'
def ln(w=1): return f'<span class="ln" style="flex:{w}"></span>'
def kid(n,age):
    a=f'<span class="v">{age}</span>' if age else ln(.5)
    return f'''<div class="kid">
<div class="r top"><span class="nm">{n or ""}</span>{"" if n else ln(2)}</div>
<div class="lb">Basics</div>
<div class="r"><b>Age</b>{a}<b>Height</b>{ln()}<b>Weight</b>{ln()}<b>Grown a lot last year?</b>{box("Yes")}{box("No")}{box("Not sure")}</div>
<div class="r"><b>Fall ball?</b>{box("Yes")}{box("No")}<b>Last threw</b>{ln(1.2)}<b>Pitch types</b>{box("FB")}{box("CH")}{box("CB")}{box("SL")}{box("Other")}{ln(.6)}</div>
<div class="r"><b>Winter goals</b>{ln()}</div>
<div class="r"><b>Role</b>{box("Pitcher")}{box("Two-way")}{box("Catcher")}<b>Other sports</b>{ln(1.3)}<b>Days</b>{ln()}</div>
<div class="lb">Health</div>
<div class="r"><b>Arm pain in last 12 months?</b>{box("No")}{box("Yes")}<b>Where</b>{ln()}</div>
<div class="r"><b>Past injuries / sore now</b>{ln()}</div>
<div class="lb">Range of motion</div>
<table><tr><th></th><th>IR</th><th>ER</th><th>Total</th></tr><tr><td>Throwing arm</td><td></td><td></td><td></td></tr><tr><td>Other arm</td><td></td><td></td><td></td></tr></table>
</div>'''
pages="".join(f'<div class="pg"><div class="hd">Scorps Throwing · Day 1 · Coach only · Nov 4, 2026</div>{kid(*P[i])}<div class="cut"></div>{kid(*P[i+1])}<div class="cut"></div>{kid(*P[i+2])}</div>' for i in range(0,len(P),3))
html=f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page{{size:Letter;margin:0}}*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:Inter,sans-serif;color:#222;font-size:9.6pt}}
.pg{{width:8.5in;height:11in;padding:.3in .45in;display:flex;flex-direction:column;page-break-after:always}}
.hd{{font-size:7.5pt;letter-spacing:.18em;text-transform:uppercase;color:#777;margin-bottom:6px}}
.kid{{flex:1;display:flex;flex-direction:column;gap:2px}}
.cut{{border-top:.75px dashed #aaa;margin:6px 0}}
.top{{margin-bottom:2px}}.nm{{font-family:'Inter Display';font-weight:600;font-size:13pt;min-width:2.4in}}
.lb{{font-size:7pt;letter-spacing:.16em;text-transform:uppercase;color:#888;margin-top:3px}}
.r{{display:flex;align-items:flex-end;gap:6px;min-height:24px}}.r b{{font-weight:500;white-space:nowrap;margin-left:8px}}.r b:first-child{{margin-left:0}}
.ln{{border-bottom:.75px solid #999;height:15px;min-width:24px}}.v{{min-width:20px}}
.bx{{display:inline-block;width:10px;height:10px;border:.75px solid #666;border-radius:2px;margin:0 2px -1px 4px}}
table{{width:72%;border-collapse:collapse;margin-top:2px}}th,td{{border:.75px solid #bbb;padding:2px 6px;height:23px;text-align:left}}th{{font-size:8.5pt;font-weight:500}}td:first-child{{width:32%}}
</style></head><body>{pages}</body></html>"""
open("day1.html","w").write(html)
with sync_playwright() as pw:
    b=pw.chromium.launch();pg=b.new_page();pg.goto("file:///home/claude/scorps/day1.html");pg.wait_for_timeout(300)
    pg.pdf(path="Scorps_Day1_Sheets.pdf",format="Letter",print_background=True);b.close()
print("ok")
