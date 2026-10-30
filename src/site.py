import os, glob, shutil
from PIL import Image
SITE = "/home/claude/site"
HEAD = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#0c0a11"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"><meta name="apple-mobile-web-app-title" content="Scorps"><meta name="robots" content="noindex,nofollow"><link rel="apple-touch-icon" href="../icon.png"><link rel="icon" href="../icon.png"><style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head>
'''
lg = Image.open("logo.png").convert("RGBA"); lg.thumbnail((150, 150))
ic = Image.new("RGBA", (180, 180), (12, 10, 17, 255)); ic.paste(lg, ((180 - lg.width) // 2, (180 - lg.height) // 2), lg)
ic.convert("RGB").save(f"{SITE}/icon.png")
for f in glob.glob("out/scorps-*.html"):
    slug = os.path.basename(f)[7:-5]
    if slug == "coach":
        continue
    os.makedirs(f"{SITE}/{slug}", exist_ok=True)
    open(f"{SITE}/{slug}/index.html", "w").write(HEAD + open(f).read() + "\n</html>\n")
open(f"{SITE}/robots.txt", "w").write("User-agent: *\nDisallow: /\n")
open(f"{SITE}/index.html", "w").write(HEAD.replace("../icon.png", "icon.png") + '<title>Scorps Throwing</title><body style="background:#0c0a11;color:#cfccd8;font:16px system-ui;display:grid;place-items:center;min-height:100vh"><p>Scorps Throwing. Use the link Coach Brooks sent you.</p></body></html>\n')
print(sorted(os.listdir(SITE)))
