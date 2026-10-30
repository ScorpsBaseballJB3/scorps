import json, gen
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
LINKS = json.load(open("links.json"))
W, H = letter
c = canvas.Canvas("Scorps_Player_QR_Codes.pdf", pagesize=letter)
c.setTitle("Scorps Throwing player QR codes")
def q(url, x, y, s):
    w = qr.QrCodeWidget(url, barLevel="M"); b = w.getBounds()
    d = Drawing(s, s, transform=[s / (b[2] - b[0]), 0, 0, s / (b[3] - b[1]), 0, 0]); d.add(w); renderPDF.draw(d, c, x, y)
P = sorted([(f"{f} {l}", l.lower().replace("é", "e")) for f, l, t, g in gen.PLAYERS], key=lambda p: p[0].split()[-1])
M, top, bw, bh, gx, gy = 40, 80, (W - 80 - 20) / 2, 205, 20, 18
for page in (P[:6], P[6:]):
    c.setFont("Helvetica-Bold", 26); c.drawCentredString(W / 2, H - 58, "SCORPS THROWING")
    for i, (name, s) in enumerate(page):
        col, row = i % 2, i // 2
        x = M + col * (bw + gx); y = H - 96 - (row + 1) * bh - row * gy
        c.setLineWidth(.6); c.setStrokeGray(.55); c.rect(x, y, bw, bh)
        sz = 150; q(f"https://scorpsbaseballjb3.github.io/scorps/{LINKS[s]}/", x + (bw - sz) / 2, y + 38, sz)
        c.setFillGray(0); c.setFont("Helvetica-Bold", 16); c.drawCentredString(x + bw / 2, y + 16, name)
    c.showPage()
c.save()
