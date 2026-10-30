import json, base64, datetime as dt, re
LINKS = json.load(open("links.json"))
import gen

URL = {"Fredericks": "QoZVuSrtVFgCCCMejbVr3Q", "Pirches": "RQgXZTPbNm9mud8cdSAJF9", "Campion": "6XNSRH9j7HqvsrxYXqS4xe",
       "Carlisle": "BefgCUG3cHgGB8K1KvNMR8", "Paré": "HnayJQopHpuUAJtkkSFGob", "Miller": "2orQAbYV97D1mZcvTWidHf",
       "Kelley": "FijiJn1LWQHDYZB9PHVtH7", "Davis": "SS39u31YJCuAvVh6xzfE7h", "Cote": "WvKWwWnqb1i4YeAuXaiGuq",
       "Knychalski": "YCtQnpbYN7gWWtDbM4v2hD", "Sydney": "WQkwpwgoJ4FdGXCPCWMTPK"}

kids, sess = [], {}
for f, l, t, g in gen.PLAYERS:
    slug = l.lower().replace("é", "e")
    data = gen.post(gen.build(f, l, t, g))
    kids.append({"s": slug, "f": f, "l": l, "tier": t, "wed": data["wed"], "sat": data["sat"], "cat": data["catcher"],
                 "url": "https://scorpsbaseballjb3.github.io/scorps/" + LINKS[slug] + "/", "firstpen": data["firstpen"], "focus": None})
    for w in data["weeks"]:
        for d in w["days"]:
            if not d.get("group"):
                continue
            row = {"title": d["title"], "eff": d.get("effl"), "grp": d["group"], "phase": w["phase"], "wk": w["n"]}
            for b in d["blocks"]:
                if b["t"] == "Med ball":
                    row["mb"] = True
                for it in b["items"]:
                    if it["n"] == "Bullpen":
                        row["pen"] = int(re.search(r"\+ (\d+)", it["txt"]).group(1))
                    elif it["n"].startswith("Pulldowns"):
                        row["pull"] = int(it["txt"].split()[0])
                    elif it["n"] == "Throwdowns":
                        row["td"] = int(it["txt"].split()[0])
                    elif it["n"] == "Velo test":
                        row["vt"] = True
            sess.setdefault(d["d"], {})[slug] = row

# key dates
D = lambda s: s
dates = [
    ("2026-11-04", "Day 1: ROM, video, intake sheets", "big"),
    ("2026-11-18", "Med ball add-on starts (non-pen days)", ""),
    ("2026-11-25", "Velo test #1 · Pat out", "big"),
    ("2026-11-22", "Light week (wk 4) · Nov 22–28", "light"),
    ("2026-12-02", "Pat out", "pat"), ("2026-12-09", "Pat out", "pat"), ("2026-12-16", "Pat out", "pat"),
    ("2026-12-20", "Light week (wk 8) · Dec 20–26", "light"),
    ("2026-12-26", "Pat out", "pat"),
    ("2026-12-30", "Bullpens start: Tier A and B · Campion throwdowns start · weekly velo updates start", "big"),
    ("2027-01-13", "Bullpens start: Tier C · Tier A pulldowns (3)", "big"),
    ("2027-01-19", "CCRI starts (Tue/Thu/Fri 4–6)", ""),
    ("2027-01-20", "Tier B pulldowns (3)", ""),
    ("2027-01-24", "Deload week (wk 13) · Jan 24–30", "light"),
    ("2027-01-31", "Peak starts", ""),
    ("2027-02-03", "Pulldowns: A 4, B 3 · Pat out", "pat"),
    ("2027-02-17", "Pulldowns: A 5, B 3", ""),
    ("2027-02-28", "Taper week · Feb 28–Mar 6", "light"),
    ("2027-03-03", "Final velo test", "big"),
    ("2027-03-06", "Last session · Pat out", "big"),
    ("2027-03-08", "HS pitchers and catchers report", "big"),
]
dates.sort()
data = {"kids": kids, "sess": sess, "dates": [{"d": a, "t": b, "k": c} for a, b, c in dates],
        "velo": {}, "checkins": [], "ckAsOf": None, "tallyGrades": [],
        "groups": {"wed": gen.WED_T, "sat": gen.SAT_T}}

tpl = open("coach_template.html").read()
logo = "data:image/png;base64," + base64.b64encode(open("logo.png", "rb").read()).decode()
html = (tpl.replace("/*PENSCSS*/", open("pens.css").read()).replace("/*PENSJS*/", open("pens.js").read())
        .replace("__LOGO__", logo).replace("__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":"))))
open("out/scorps-coach.html", "w").write(html)
print(len(html), len(sess))
