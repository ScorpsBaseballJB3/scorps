import json, datetime as dt, base64, urllib.parse

START = dt.date(2026, 11, 1)  # Sunday of week 1
PLAYERS = [
    ("Maddux", "Fredericks", "A", 2), ("Kenny", "Pirches", "A", 1), ("Ryan", "Campion", "A", 2),
    ("Cam", "Carlisle", "A", 1), ("Colby", "Paré", "A", 1), ("Nick", "Miller", "B", 2),
    ("Liam", "Kelley", "B", 2), ("Jared", "Davis", "B", 2), ("Cam", "Cote", "C", 1),
    ("Andrew", "Knychalski", "C", 1), ("Eli", "Sydney", "C", 2),
]
WED_T = {1: "5:30–7:00pm", 2: "7:00–8:30pm"}
SAT_T = {1: "8:00–9:30am", 2: "9:30–11:00am"}
SATG = {"Fredericks": 1, "Paré": 2, "Davis": 1, "Sydney": 1}

PHASE = ["Ramp", "Ramp", "Ramp", "Light week", "Build", "Build", "Build", "Light week",
         "Build 2", "Build 2", "Build 2", "Build 2", "Deload", "Peak", "Peak", "Peak", "Peak", "Taper"]
MULT = {"A": [.6, .75, .85, .7, 1, 1, 1, .75, 1, 1, 1, 1, .7, 1, 1, 1, 1, .75]}
MULT["B"] = MULT["A"]
MULT["C"] = [.5, .6, .6, .6, .75, .85, 1, .75, 1, 1, 1, 1, .7, 1, 1, 1, 1, .75]
EFF = {"A": [60, 65, 70, 70, 75, 80, 85, 85, 90, 90, 90, 90, 80, 90, 90, 90, 90, 90],
       "B": [60, 65, 70, 70, 75, 80, 85, 85, 85, 85, 85, 85, 75, 85, 85, 85, 85, 85],
       "C": [55, 60, 65, 65, 70, 75, 80, 80, 80, 80, 80, 80, 70, 80, 80, 80, 80, 80]}
NET = [10, 12, 15, 12, 18, 20, 20, 15, 20, 20, 20, 20, 12, 20, 20, 20, 20, 12]
PEN = {
    "A": {9: 15, 10: 20, 11: 25, 12: 30, 13: 15, 14: 30, 15: 30, 16: 30, 17: 30, 18: 20},
    "B": {9: 15, 10: 20, 11: 20, 12: 25, 13: 15, 14: 25, 15: 25, 16: 25, 17: 25, 18: 15},
    "C": {11: 10, 12: 15, 13: 10, 14: 15, 15: 20, 16: 20, 17: 20, 18: 12},
}
PULL = {"A": {11: 3, 14: 4, 16: 5}, "B": {12: 3, 14: 3, 16: 3}, "C": {}}
CATCHERS = {"Campion"}
LAD = {"A": [(3, "10"), (4, "8"), (4, "5")], "B": [(3, "10"), (3, "8"), (3, "5")], "C": [(2, "10"), (3, "8"), (3, "5")]}
REV = {"A": [(6, "kg"), (6, "kgx16")], "B": [(5, "kg"), (5, "kgx16")], "C": [(4, "16"), (4, "16x10")]}
WW = {"A": (2, 2), "B": (2, 2), "C": (2, 1)}
CLAD = [(3, "10"), (3, "8"), (3, "5")]
NAMES = {"rev": "Reverse throws", "hk": "Half-kneeling throws", "rock": "Rocker throws", "roll": "Roll-ins",
         "drop": "Drop backs", "step": "Step-backs", "ww": "Walking windups",
         "kd": "Knee-down throws", "ex": "Exchange throws", "jp": "Jab-pivot throws",
         "ssr": "Secondary-stance rockers", "wtd": "Walking throwdowns"}
BLOCK = {1: ("roll", ("hk", "rock")), 2: ("roll", ("drop", "step")), 3: ("rock", ("roll", "drop")),
         4: ("step", ("roll", "hk")), 5: ("roll", ("rock", "step"))}


def blk(w):
    return 1 if w <= 4 else 2 if w <= 8 else 3 if w <= 12 else 4 if w <= 16 else 5


def yt(q, src="Tread Athletics"):
    return "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(f"{src} {q}")


VID = {"rev": "https://www.youtube.com/watch?v=G3RKCmTEyKs", "hk": "https://www.youtube.com/watch?v=-PDRv_eZyl4", "rock": "https://www.youtube.com/watch?v=b3QuJtD1-7w", "roll": "https://www.youtube.com/watch?v=v3IBryZpmjc", "drop": "https://www.youtube.com/watch?v=OVSFKjEdG80", "step": "https://www.youtube.com/watch?v=yZ0YJEOehPA", "ww": "https://www.youtube.com/shorts/x0AJaedcHqU", "jband": "https://www.youtube.com/watch?v=IOCWJKUNoJk", "foam": "https://www.youtube.com/watch?v=F0fmIeZUexo", "pa": "https://www.youtube.com/watch?v=kCJDMg2H4Xo", "waiter": "https://www.youtube.com/watch?v=NzrqaRCF5ng", "er": "https://www.youtube.com/watch?v=ybNV36DoRfY", "ir": "https://www.youtube.com/watch?v=MfjCK5_Ss5g", "yt": "https://www.youtube.com/watch?v=hzARk9wm7JU", "wrist": "https://www.youtube.com/watch?v=uspQeLxzN-U", "twist": "https://www.youtube.com/watch?v=Xas60Z7HzQc", "ob": "https://www.youtube.com/watch?v=rDviWORCWEw", "cb": "https://www.youtube.com/watch?v=pD236y4-YRc"}


def scale(lst, m):
    return [[max(1, round(n * m)), bb] for n, bb in lst]


def plyo_item(key, tier, m, core_only=False, catcher=False):
    if key in ("ww", "wtd"):
        sets, per = WW["A" if catcher else tier]
        if core_only and not catcher:
            sets = 1
        return {"n": NAMES[key], "sets": sets, "per": per, "each": ["10", "8", "5"]}
    if key == "rev":
        return {"n": NAMES[key], "r": [list(x) for x in REV[tier]], "note": "2 sets. Second set: your choice of ball."}
    lad = CLAD if catcher else LAD[tier]
    return {"n": NAMES[key], "r": scale(lad, m)}


def plist_for(w, core_only, catcher, wed):
    if catcher:
        return ["rev", "kd", "ex", "wtd"] if wed and core_only else ["rev", "kd", "ex", "jp", "ssr", "wtd"]
    c2, (r1, r2) = BLOCK[blk(w)]
    return ["rev", c2, "ww"] if core_only else ["rev", r1, c2, r2, "ww"]


MOB = {
    "A": [("90/90 hip switches", "2 × 6 each side"), ("Half-kneeling hip flexor stretch", "2 × 30 sec each side"), ("Lateral lunges", "2 × 5 each side")],
    "B": [("Half-kneeling hip flexor stretch", "2 × 30 sec each side"), ("Quadruped T-spine rotation", "2 × 6 each side"), ("Standing hip CARs", "3 slow circles each way, each leg")],
}


def warmup(tier, s=0):
    st = "A" if s % 2 else "B"
    mob = [{"n": n, "txt": t, "note": f"Mobility set {st}" if i == 0 else None} for i, (n, t) in enumerate(MOB[st])]
    for m in mob:
        if m["note"] is None:
            m.pop("note")
    return {"t": "Warm-up", "sub": "Don't rush this", "items": [
        {"n": "Stretch, then light run", "txt": "5 min"},
        {"n": "Foam roll", "txt": "10 passes, full body", "v": VID["foam"]},
        *mob,
        {"n": "J-band series", "txt": "2 × 8 each", "v": VID["jband"]},
    ]}


def recovery(tier, wed=False):
    ball = "16 oz" if tier == "C" else "1 kg"
    return {"t": "Recovery", "items": [
        {"n": "90/90 rotations", "txt": f"{'2 × 4' if wed else '2 × 6'} · {ball}", "note": "Slow, about 2 sec each way"},
        {"n": "Band pull-aparts", "txt": "2 × 10–15 each way", "note": "Palm up, palm down, diagonals, overhead", "v": VID["pa"]},
        {"n": "Waiter walks", "txt": ("4" if tier == "C" else "6") + " × 30 yd", "v": VID["waiter"]},
        {"n": "J-band series", "txt": "1 × 8 each", "v": VID["jband"]},
    ]}


def arm_care(tier, light):
    s = 1 if light else 2
    r = 10 if tier == "C" else 12
    return {"t": "Arm care", "sub": "Encouraged · about 12 min", "items": [
        {"n": "Band external rotation", "txt": f"{s} × {r}", "v": VID["er"]},
        {"n": "Band internal rotation", "txt": f"{s} × {r}", "v": VID["ir"]},
        {"n": "Band pull-aparts", "txt": f"{s} × {r}", "v": VID["pa"]},
        {"n": "Band Y's and T's", "txt": f"{s} × {r - 2} each", "v": VID["yt"]},
        {"n": "Band wrist flexion and extension", "txt": f"{s} × {r} each", "v": VID["wrist"]},
        {"n": "Band forearm twists", "txt": f"{s} × {r}", "v": VID["twist"]},
        {"n": "Open books", "txt": "1 × 8 each side", "v": VID["ob"]},
        {"n": "Cross-body shoulder stretch", "txt": "2 × 30 sec each arm", "v": VID["cb"]},
    ]}


def medball(tier, light=False):
    c = tier == "C"
    if light:
        return {"t": "Med ball", "sub": ("4 lb" if c else "6 lb") + " ball · light week: scoop toss only · into the field net", "items": [
            {"n": "Rotational scoop toss", "txt": "1 × 4 each side", "eff": "Fast, not max", "note": "Sore side or back? Skip this one."}]}
    return {"t": "Med ball", "sub": ("4 lb ball (no 4 lb? use 6 lb, 1 fewer rep)" if c else "6 lb ball") + " · about 3 min · into the field net", "items": [
        {"n": "Rotational scoop toss", "txt": "1 × 4 each side", "eff": "Fast, not max", "note": "Sore side or back? Skip this one."},
        {"n": "Overhead slams", "txt": "1 × 5", "eff": "Fast, not max"},
        {"n": "Step-behind shot put", "txt": "1 × 4 · throwing side", "eff": "Fast, not max"},
    ]}


MB_START = dt.date(2026, 11, 18)
MB_SKIP = {"2026-11-25"}  # velo test day


def build(first, last, tier, grp):
    weeks, sess = [], 0
    cat = last in CATCHERS
    for wi in range(18):
        w = wi + 1
        m, eff = MULT[tier][wi], EFF[tier][wi]
        light = PHASE[wi] in ("Light week", "Deload", "Taper") or w <= 2
        days = []
        for di in range(7):
            d = START + dt.timedelta(days=wi * 7 + di)
            iso = d.isoformat()
            day = {"d": iso, "blocks": []}
            if d < dt.date(2026, 11, 4):
                day.update(type="pre", title="Program starts Wednesday", blocks=[])
            elif d > dt.date(2027, 3, 6):
                day.update(type="off", title="Rest up · HS practice starts Mar 8")
            elif di == 3:  # Wed
                if cat:
                    td = 6 if w >= 9 else 0
                    if PHASE[wi] in ("Deload", "Taper") and td:
                        td = 4
                    core = bool(td)
                    pen = pull = None
                else:
                    pen = PEN[tier].get(w)
                    pull = PULL[tier].get(w)
                    if pen and pull:
                        pen -= 10
                    core = bool(pen)
                sess += 1
                throws = {"t": "Throwing", "items": [plyo_item(k, tier, m, core, cat) for k in plist_for(w, core, cat, True)]}
                if core and not cat:
                    throws["items"].append({"n": "Net throws", "txt": "5–10 throws", "note": f"Long-toss style into the field net. Build up to {eff}%, then go to the bullpen."})
                    if pull:
                        throws["items"].append({"n": "Pulldowns (crow hop into net)", "txt": f"{pull} throws", "note": "Full intent. Before the bullpen.", "big": True})
                    vnote = "Into the 9-hole net. First 5 fastballs on the radar."
                    if iso == "2027-03-03":
                        vnote = "Final velo test: first 5 fastballs on the radar. Video too."
                    throws["items"].append({"n": "Bullpen", "txt": f"5 warm-up + {pen} pitches", "note": vnote, "big": True})
                elif core and cat:
                    throws["items"].append({"n": "Net throws", "txt": "10 throws", "note": f"Build up to {eff}% effort"})
                    tnote = "From the crouch into the net, about 55 ft. Coach radars them."
                    if iso == "2027-03-03":
                        tnote = "Final velo test: throwdowns on the radar. Video too."
                    throws["items"].append({"n": "Throwdowns", "txt": f"{td} throws", "note": tnote, "big": True})
                else:
                    throws["items"].append({"n": "Net throws", "txt": "10 throws", "note": f"90 ft into the net · build to {eff}% effort"})
                if w <= 3:
                    typ, ttl = "mod", "Moderate · with Coach"
                elif PHASE[wi] == "Light week":
                    typ, ttl = "light", "Light week · with Coach"
                elif PHASE[wi] == "Deload":
                    typ, ttl = "light", "Deload · with Coach"
                elif PHASE[wi] == "Taper":
                    typ, ttl = "heavy", "Taper · velo test"
                else:
                    typ, ttl = "heavy", "Heavy day" + ((" · throwdowns" if cat else " · bullpen") if core else "")
                if iso == "2026-11-25":
                    ttl = "Velo test day · with Coach"
                    throws["items"][-1] = {"n": "Net throws (build-up)", "txt": "10 throws", "note": "Build from easy to almost full effort"}
                    if cat:
                        throws["items"].append({"n": "Velo test", "txt": "5 throwdowns on the radar", "note": "Full effort from the crouch into the net. Your first point on the chart.", "big": True})
                    else:
                        throws["items"].append({"n": "Velo test", "txt": "5 throws on the radar", "note": "Full effort into the net, crow hop. Your first point on the chart.", "big": True})
                if iso == "2026-11-04":
                    ttl = "Day 1 · with Coach"
                    day["blocks"].append({"t": "Day 1 check-in", "sub": "With Coach Brooks", "items": [
                        {"n": "Shoulder range of motion", "txt": "Both arms"},
                        {"n": "Mechanics video", "txt": "Side and back, easy effort"},
                        {"n": "Quick questions", "txt": "About 2 min"}]})
                day["blocks"] += [warmup(tier, sess)]
                if not core and d >= MB_START and iso not in MB_SKIP:
                    day["blocks"].append(medball(tier, PHASE[wi] in ("Light week", "Deload", "Taper")))
                day["blocks"] += [throws, recovery(tier, True)]
                day.update(type=typ, title=ttl, group=WED_T[grp], eff=100 if iso == "2026-11-25" else eff)
            elif di == 6:  # Sat
                se = max(50, eff - 10)
                sess += 1
                note = f"90 ft into the net · build to {se}% effort"
                if PHASE[wi] == "Peak":
                    note = f"Flat-ground into the net · {se}% effort"
                throws = {"t": "Throwing", "items": [plyo_item(k, tier, m, False, cat) for k in plist_for(w, False, cat, False)] + [
                    {"n": "Net throws", "txt": "10 throws", "note": note}]}
                day["blocks"] = [warmup(tier, sess)] + ([medball(tier, PHASE[wi] in ("Light week", "Deload", "Taper"))] if d >= MB_START else []) + [throws, recovery(tier, False)]
                ttl = "Moderate · with Coach"
                if iso == "2027-03-06":
                    ttl = "Last session · with Coach"
                day.update(type="mod", title=ttl, group=SAT_T[SATG.get(last, grp)], eff=se)
            elif di == 4:
                day.update(type="off", title="Off day", blocks=[])
            elif di == 5:
                day.update(type="light", title="Light day", blocks=[{"t": "Light mobility", "sub": "Encouraged · about 10 min", "items": [
                    {"n": "Band pull-aparts", "txt": "2 × 12", "v": VID["pa"]},
                    {"n": "Open books", "txt": "1 × 8 each side", "v": VID["ob"]},
                    {"n": "Cross-body shoulder stretch", "txt": "2 × 30 sec each arm", "v": VID["cb"]}]}])
            elif di == 0:
                day.update(type="rec", title="Recovery day", blocks=[{"t": "Recovery routine", "sub": "Encouraged · 15 min max", "items": [
                    {"n": "Open books", "txt": "1 × 8 each side", "v": VID["ob"]},
                    {"n": "Cross-body shoulder stretch", "txt": "2 × 30 sec each arm", "v": VID["cb"]},
                    {"n": "Light band pull-aparts", "txt": "1 × 12", "v": VID["pa"]}]}])
            else:
                day.update(type="arm", title="Arm care day", blocks=[arm_care(tier, light)])
            days.append(day)
        weeks.append({"n": w, "s": (START + dt.timedelta(days=wi * 7)).isoformat(), "phase": PHASE[wi], "block": blk(w), "days": days})
    return {"first": first, "last": last, "wed": WED_T[grp], "sat": SAT_T[SATG.get(last, grp)], "weeks": weeks,
            "velo": [], "team": [], "catcher": cat, "focus": None, "pens": [],
            "lefty": last in LEFTY, "firstpen": "2027-01-13" if tier == "C" else "2026-12-30"}


GUIDE = {
 "r9090": {"name": "90/90 rotations", "g": "Recovery", "how": "Arm out at shoulder height, elbow bent 90°, ball in hand. Rotate the forearm forward and down until it's flat, then back up to straight up.", "cues": "Slow, 2 sec each way. Elbow stays at shoulder height.", "mis": "Rushing, or letting the elbow drop.", "chk": "Felt the back of the shoulder working, no pinch?"},
 "kd": {"name": "Knee-down throws", "g": "Catcher plyos", "how": "Throwing-side knee down like you just blocked or framed. Short arm path, quick release into the wall.", "cues": "Short and quick. Chest to target.", "mis": "Long, looping arm.", "chk": "Quick release with a firm throw?"},
 "ex": {"name": "Exchange throws", "g": "Catcher plyos", "how": "From your stance, catch a feed, transfer to your throwing hand at the chest, and throw into the wall in one motion.", "cues": "Glove to chest. Fast hands, not fast arm.", "mis": "Reaching out to transfer.", "chk": "Clean transfer every rep?"},
 "jp": {"name": "Jab-pivot throws", "g": "Catcher plyos", "how": "From your stance, jab the throwing-side foot, pivot to line up with the wall, throw.", "cues": "Small jab. Get on line.", "mis": "Big step that pulls you off line.", "chk": "Shoulders lined up with the target?"},
 "ssr": {"name": "Secondary-stance rockers", "g": "Catcher plyos", "how": "In your runners-on stance, rock weight back and forth twice, then come up and throw.", "cues": "Stay low until you throw.", "mis": "Standing up early.", "chk": "Weight moved toward the target?"},
 "wtd": {"name": "Walking throwdowns", "g": "Catcher plyos", "how": "Walk two steps toward the wall, drop into your catching footwork, and throw. Full motion at game rhythm.", "cues": "Momentum into the throw.", "mis": "Walking in, then stopping dead.", "chk": "Footwork and throw flowed together?"},
 "tdown": {"name": "Throwdowns", "g": "Throwing", "how": "From the crouch, receive, transfer, and throw into the net about 55 ft away. Full game footwork.", "cues": "Quick feet, firm throw, on line.", "mis": "Rushing the arm ahead of the feet.", "chk": "Each throw on line and pain-free?"},
 "stretch": {"name": "Stretch, then light run", "g": "Warm-up", "how": "Dynamic stretch head to toe, then jog until you break a light sweat.", "cues": "Loose, not tired.", "mis": "Rushing it to get to throwing.", "chk": "Body warm before you pick up a ball?"},
 "foam": {"name": "Foam roll", "g": "Warm-up", "how": "Upper back, lats, glutes, hamstrings, quads, calves. Slow passes, pause on tight spots.", "cues": "Slow. Breathe.", "mis": "Rolling fast over everything.", "chk": "Found and worked your tight spots?"},
 "jband": {"name": "J-band series", "g": "Warm-up", "how": "External rotation, internal rotation, then I's, Y's, T's. Smooth tempo, full control.", "cues": "Elbow pinned on rotations. Shoulders down on I, Y, T.", "mis": "Swinging the band or shrugging.", "chk": "Shoulder warm with no pinch?"},
 "rev": {"name": "Reverse throws", "g": "Plyos", "how": "Face away from the wall. Turn hard through the hips and throw back over your throwing shoulder. Let the arm decelerate fully.", "cues": "Hips lead. Whip, don't muscle.", "mis": "All arm, no turn.", "chk": "Back hip drove it? Arm finished loose?"},
 "hk": {"name": "Half-kneeling throws", "g": "Plyos", "how": "Throwing-side knee down, glove-side foot forward toward the wall. Rotate the trunk and throw.", "cues": "Stay tall. Chest turns, arm follows.", "mis": "Leaning back or falling off to the side.", "chk": "Posture held through release?"},
 "rock": {"name": "Rocker throws", "g": "Plyos", "how": "Sideways to the wall, feet wider than your stride. Rock back and forth twice, throw on the third rock forward.", "cues": "Rhythm. Weight back, then all the way through.", "mis": "Throwing before the weight shifts forward.", "chk": "Finished over a firm front leg?"},
 "roll": {"name": "Roll-ins", "g": "Plyos", "how": "Start turned past sideways, back half to the wall. Roll the hips in, stride, and throw in one motion.", "cues": "Momentum first, arm last.", "mis": "Stopping before the throw.", "chk": "One smooth move from start to release?"},
 "drop": {"name": "Drop backs", "g": "Plyos", "how": "Sideways to the wall. Step the back foot behind the front foot, sink into the back hip, then stride and throw.", "cues": "Load the back hip. Then go.", "mis": "Standing tall with no load.", "chk": "Felt the back hip load before the stride?"},
 "step": {"name": "Step-backs", "g": "Plyos", "how": "Face the wall. Step back with the throwing-side foot, turn sideways, stride and throw.", "cues": "Quick feet, smooth arm.", "mis": "Rushing the arm ahead of the feet.", "chk": "Feet set before the arm went?"},
 "ww": {"name": "Walking windups", "g": "Plyos", "how": "Walk two steps toward the wall, turn sideways, lift, stride, and throw. Full delivery at game rhythm.", "cues": "Athletic and fluid.", "mis": "Walking in, then stopping dead.", "chk": "Momentum carried into the throw?"},
 "net": {"name": "Net throws", "g": "Throwing", "how": "Baseball, 10 throws, 90 ft into the field net. Start easy and add effort every few throws up to today's %.", "cues": "Build, don't jump.", "mis": "Going hard on throw one.", "chk": "Hit today's effort without going over?"},
 "pull": {"name": "Pulldowns", "g": "Throwing", "how": "Crow hop into the net with full intent. Rest 30 to 60 sec between throws.", "cues": "Everything you've got, under control.", "mis": "No rest between throws.", "chk": "Each throw full intent and pain-free?"},
 "pen": {"name": "Bullpen", "g": "Throwing", "how": "Into the 9-hole net. 5 warm-up pitches, then your count. Coach radars the first 5 fastballs.", "cues": "Same delivery every pitch.", "mis": "Overthrowing to chase the radar.", "chk": "Arm feel the same at the end as the start?"},
 "vtest": {"name": "Velo test", "g": "Throwing", "how": "Fully built up first. Crow hop into the net, full intent, 5 throws on the radar. Rest 30 to 60 sec between.", "cues": "Best throw, not wildest throw.", "mis": "Testing before you're warm.", "chk": "All 5 felt good?"},
 "pa": {"name": "Band pull-aparts", "g": "Recovery", "how": "Arms straight at chest height. Pull the band to your chest, slow back. Palm up, palm down, diagonals, overhead.", "cues": "Squeeze the shoulder blades. 2 sec back.", "mis": "Shrugging or bending the elbows.", "chk": "Felt it between the shoulder blades?"},
 "waiter": {"name": "Waiter walks", "g": "Recovery", "how": "Light dumbbell or kettlebell straight overhead. Walk 30 yd. Switch arms.", "cues": "Biceps by the ear. Ribs down.", "mis": "Arm drifting forward or elbow bending.", "chk": "Shoulder steady the whole walk?"},
 "er": {"name": "Band external rotation", "g": "Arm care", "how": "Elbow at your side, bent 90°. Rotate the forearm out against the band, slow back.", "cues": "Elbow pinned. 2 sec back.", "mis": "Elbow drifting off your side.", "chk": "Felt the back of the shoulder?"},
 "ir": {"name": "Band internal rotation", "g": "Arm care", "how": "Elbow at your side, bent 90°. Rotate the forearm in across your stomach, slow back.", "cues": "Elbow pinned. Control both ways.", "mis": "Turning the body to cheat.", "chk": "Only the arm moved?"},
 "iyt": {"name": "Band I's, Y's, T's", "g": "Arm care", "how": "Arms straight. Pull the band overhead (I), up and out (Y), then straight out to the sides (T).", "cues": "Thumbs up. Shoulders down.", "mis": "Shrugging or arching the back.", "chk": "Felt it between the shoulder blades?"},
 "wrist": {"name": "Band wrist flexion and extension", "g": "Arm care", "how": "Forearm on your thigh, band under your foot. Curl the wrist up palm up, then palm down.", "cues": "Only the wrist moves.", "mis": "Lifting the forearm.", "chk": "Forearm burn, no elbow pain?"},
 "twist": {"name": "Band forearm twists", "g": "Arm care", "how": "Elbow at your side, bent 90°, band anchored. Turn the palm down, then palm up, against the band.", "cues": "Slow both ways.", "mis": "Elbow drifting.", "chk": "Felt the forearm working?"},
 "ob": {"name": "Open books", "g": "Mobility", "how": "Lie on your side, knees bent, arms together. Open the top arm across to the other side, eyes follow the hand. Hold 2 sec.", "cues": "Knees stay together.", "mis": "Knees lifting as you open.", "chk": "Felt the upper back open up?"},
 "hip90": {"name": "90/90 hip switches", "g": "Mobility", "how": "Sit with both knees bent 90°, one leg in front, one to the side. Rotate both knees to the other side without using your hands.", "cues": "Sit tall. Knees drop slow.", "mis": "Leaning way back or using hands.", "chk": "Felt both hips rotate?", "v": "https://www.youtube.com/watch?v=n1_ackKRYjE"},
 "hflex": {"name": "Half-kneeling hip flexor stretch", "g": "Mobility", "how": "One knee down, other foot forward. Squeeze the glute on the down side and shift the hips slightly forward. Hold.", "cues": "Squeeze the glute. Ribs down.", "mis": "Arching the low back to fake it.", "chk": "Stretch in the front of the hip, not the back?", "v": "https://www.youtube.com/watch?v=F55tzqJggAY"},
 "tspine": {"name": "Quadruped T-spine rotation", "g": "Mobility", "how": "On hands and knees, sit hips back slightly. One hand behind the head. Rotate the elbow down under you, then up to the ceiling.", "cues": "Hips still. Eyes follow the elbow.", "mis": "Hips swaying to fake the turn.", "chk": "Rotation came from the upper back?", "v": "https://www.youtube.com/watch?v=AzCghjjWt5k"},
 "hcar": {"name": "Standing hip CARs", "g": "Mobility", "how": "Stand tall, hand on a wall. Lift the knee to hip height, open it out to the side, rotate it back and down behind you. Then reverse.", "cues": "Slow. Biggest circle you can control. Stance leg locked in.", "mis": "Rushing, or leaning the body to make the circle bigger.", "chk": "Only the hip moved? Felt it in every part of the circle?", "v": "https://www.youtube.com/watch?v=vybS-uVNrqA"},
 "latl": {"name": "Lateral lunges", "g": "Mobility", "how": "Wide stance. Sit back into one hip, other leg straight, feet flat. Push back to center and switch.", "cues": "Hips back. Chest up.", "mis": "Knee caving or heel lifting.", "chk": "Felt the groin of the straight leg stretch?", "v": "https://www.youtube.com/watch?v=V1MXDVCw4nI"},
 "mbscoop": {"name": "Rotational scoop toss", "g": "Med ball", "how": "Stand sideways to the net, ball at your back hip. Load into the back hip, then turn hard and scoop the ball into the net with both hands. Do both sides.", "cues": "Hips first, arms last. Throw it, don't push it.", "mis": "Arms doing all the work with no hip turn.", "chk": "Felt the turn start from your back hip?"},
 "mbslam": {"name": "Overhead slams", "g": "Med ball", "how": "Feet shoulder width. Reach the ball overhead and up on your toes, then slam it into the ground in front of you. Catch the bounce and reset.", "cues": "Tall, then snap down with your abs.", "mis": "Bending at the back with no reach up first.", "chk": "Stomach did the work, not your low back?"},
 "mbshot": {"name": "Step-behind shot put", "g": "Med ball", "how": "Ball at your throwing-side shoulder, elbow up. Step your back foot behind your front foot, stride toward the net, turn, and push the ball into the net like a shot put.", "cues": "Same stride and hip turn as your delivery.", "mis": "Opening your chest before your front foot lands.", "chk": "Front foot landed before you turned?"},
 "cb": {"name": "Cross-body shoulder stretch", "g": "Mobility", "how": "Bring the arm across your chest. Other hand pulls just above the elbow. Hold.", "cues": "Shoulder down. Gentle.", "mis": "Pulling hard into a pinch.", "chk": "Stretch in the back of the shoulder, not the front?"},
}
for k, v in GUIDE.items():
    if k in VID and k not in ("jband", "drop", "hk"):
        v["v"] = VID[k]
SETUP = {
 "rev": ("back", "4–5 ft", "Back to the wall, 4–5 ft away. Feet shoulder width, toes pointing away from the wall."),
 "hk": ("kneel", "7–9 ft", "Sideways to the wall, 7–9 ft away. Throwing-side knee down, glove-side foot forward toward the wall."),
 "rock": ("side", "9–11 ft", "Sideways to the wall, glove shoulder toward it, 9–11 ft away. Feet a little wider than your stride."),
 "roll": ("roll", "9–11 ft", "9–11 ft from the wall. Start turned past sideways, so your back half faces the wall a little."),
 "drop": ("drop", "9–11 ft", "Sideways to the wall, 9–11 ft away. Your back foot steps behind your front foot."),
 "step": ("face", "9–11 ft", "Face the wall, 9–11 ft away. Step your throwing-side foot back and turn sideways."),
 "ww": ("walk", "16 ft", "Start about 16 ft back, facing the wall. Walk 2 steps, turn sideways, and throw from about 9–11 ft."),
 "kd": ("kd", "9–11 ft", "Face the wall, 9–11 ft away. Throwing-side knee down, like you just blocked."),
 "ex": ("crouch", "9–11 ft", "Catcher's stance facing the wall, 9–11 ft away. Someone feeds you a ball."),
 "jp": ("jp", "9–11 ft", "Catcher's stance facing the wall, 9–11 ft away. Jab your throwing-side foot, pivot sideways, throw."),
 "ssr": ("crouch", "9–11 ft", "Runners-on stance facing the wall, 9–11 ft away."),
 "wtd": ("walk", "16 ft", "Start about 16 ft back, facing the wall. Walk 2 steps into your footwork and throw from about 9–11 ft."),
 "mbscoop": ("side", "7–9 ft", "Sideways to the field net, glove side toward it, 7–9 ft away. Ball at your back hip.", "net"),
 "mbshot": ("drop", "7–9 ft", "Sideways to the field net, 7–9 ft away. Ball at your throwing shoulder. Back foot steps behind your front foot.", "net"),
 "mbslam": ("slam", "", "Open floor, no net needed. Feet shoulder width, ball overhead."),
}
for _k, _v in SETUP.items():
    GUIDE[_k]["set"] = {"k": _v[0], "d": _v[1], "t": _v[2], "w": _v[3] if len(_v) > 3 else "wall"}
LEFTY = {"Paré", "Miller"}
N2K = {"Stretch, then light run": "stretch", "Foam roll": "foam", "J-band series": "jband", "Net throws": "net", "Net throws (build-up)": "net",
       "Pulldowns (crow hop into net)": "pull", "Bullpen": "pen", "Velo test": "vtest", "Band pull-aparts": "pa", "Light band pull-aparts": "pa",
       "Waiter walks": "waiter", "Band external rotation": "er", "Band internal rotation": "ir", "Band Y's and T's": "iyt",
       "Band wrist flexion and extension": "wrist", "Band forearm twists": "twist", "Open books": "ob", "Band I's, Y's, T's": "iyt", "90/90 rotations": "r9090", "Throwdowns": "tdown", "90/90 hip switches": "hip90", "World's greatest stretch": "wgs", "Half-kneeling hip flexor stretch": "hflex", "Quadruped T-spine rotation": "tspine", "Lateral lunges": "latl", "Standing hip CARs": "hcar", "Cross-body shoulder stretch": "cb"}
N2K.update({v: k for k, v in NAMES.items()})
N2K.update({"Rotational scoop toss": "mbscoop", "Overhead slams": "mbslam", "Step-behind shot put": "mbshot"})


def post(data):
    for w in data["weeks"]:
        for d in w["days"]:
            for b in d.get("blocks", []):
                for i, it in enumerate(b["items"]):
                    it.pop("v", None)
                    if it["n"] == "Band Y's and T's":
                        it["n"] = "Band I's, Y's, T's"
                    if it["n"] == "J-band series":
                        it["txt"] = "1 × 10 rotations · 1 × 8 I, Y, T" if b["t"] == "Warm-up" else "1 × 8 each"
                        it["note"] = "External rotation, internal rotation, I's, Y's, T's"
                    k = N2K.get(it["n"])
                    if k:
                        it["k"] = k
    for w in data["weeks"]:
        for d in w["days"]:
            mx = False
            for b in d.get("blocks", []):
                if b["t"] != "Throwing":
                    continue
                for it in b["items"]:
                    n = it["n"]
                    if it.get("eff"):
                        continue
                    if "r" in it or "each" in it:
                        it["eff"] = "70–80%"
                    elif n.startswith("Net throws"):
                        it["eff"] = f"Build to {d.get('eff', 75) if d.get('eff', 75) < 100 else 90}%"
                    elif n == "Bullpen":
                        e = d.get("eff", 85)
                        it["eff"] = f"{e - 5}–{e}%"
                    elif n.startswith("Pulldowns") or n in ("Velo test", "Throwdowns"):
                        it["eff"] = "MAX"
                    if it.get("eff") == "MAX":
                        mx = True
            if d.get("eff"):
                d["effl"] = "MAX" if mx else f"{d['eff'] - 5}–{d['eff']}%"
    for w in data["weeks"]:
        for d in w["days"]:
            if d.get("title"):
                d["title"] = d["title"].replace(" · with Coach", "")
            for b in d.get("blocks", []):
                if b.get("sub") == "With Coach Brooks":
                    b.pop("sub")
    used = {"stretch", "foam", "jband", "net"}
    for w in data["weeks"]:
        for d in w["days"]:
            for b in d.get("blocks", []):
                for it in b["items"]:
                    if it.get("k"):
                        used.add(it["k"])
    data["guide"] = {k: v for k, v in GUIDE.items() if k in used}
    return data


if __name__ == "__main__":
    tpl = open("template.html").read().replace("/*PENSCSS*/", open("pens.css").read()).replace("/*PENSJS*/", open("pens.js").read() + open("setup.js").read())
    logo = "data:image/png;base64," + base64.b64encode(open("logo.png", "rb").read()).decode()
    for f, l, t, g in PLAYERS:
        data = post(build(f, l, t, g))
        slug = urllib.parse.quote(l.lower().replace("é", "e"))
        html = tpl.replace("__TITLE__", f"{f} {l} · Scorps").replace("__LOGO__", logo).replace(
            "__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
        open(f"out/scorps-{slug}.html", "w").write(html)
        print(slug, len(html))
