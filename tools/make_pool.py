#!/usr/bin/env python3
"""Generate data/pool-v1.json: an invented, deterministic set catalog for the BrickRNG prototype.

Same seed -> same bytes. No real product data is involved: set numbers are six digits (real ones are shorter),
names come from word lists, and the three licensed themes are invented franchises.
Usage: python tools/make_pool.py
"""
import hashlib
import json
import pathlib
import random

SEED, N, PUBLISHED = 20261101, 3000, "2026-11-01"
r = random.Random(SEED)

# root theme -> (licensed, first year, last year, popularity weight, sub-themes, adjectives, nouns)
THEMES = {
    "Space": (False, 1978, 2026, 14, ["Moon Base", "Orbital Station", "Rover Squad", "Deep Probe"],
              "Lunar Orbital Stellar Cosmic Solar Nebula Polar Distant Silent Bright".split(), "Station Rover Lander Shuttle Probe Outpost Rocket Telescope Hangar".split()),
    "Castle": (False, 1978, 2026, 14, ["Knights", "Dragon Keep", "Royal Court", "Siege Camp"],
               "Iron Golden Stone Dragon Royal Emerald Shadow Silver Crimson Frost".split(), "Castle Tower Gatehouse Drawbridge Fortress Catapult Stable Keep Chapel".split()),
    "Pirates": (False, 1989, 2026, 8, ["Harbor Raiders", "Treasure Isle", "Navy Patrol"],
                "Black Salty Rusty Hidden Stormy Golden Lost Grim Scarlet".split(), "Galleon Cove Fort Cutter Lagoon Cannon Schooner Lookout Wreck".split()),
    "City": (False, 1960, 2026, 22, ["Fire Brigade", "Harbor", "Airport", "Market Street", "Police"],
             "Central Busy Riverside Downtown Northern Rapid Sunny Old Grand Little".split(), "Station Depot Terminal Bakery Bridge Garage Tower Pier Plaza".split()),
    "Rail": (False, 1966, 2026, 8, ["Express", "Freight Yard", "Depot"],
             "Mountain Coastal Night Silver Express Morning Valley Golden Steel Northern".split(), "Locomotive Junction Roundhouse Viaduct Carriage Signal Platform Tender Crossing".split()),
    "Forest": (False, 1985, 2026, 7, ["Rangers", "Treehouse", "Lake Camp"],
               "Misty Hidden Mossy Amber Quiet Wild Fern Birch Dawn Thicket".split(), "Cabin Lookout Bridge Hollow Camp Cottage Mill Glade Watchtower".split()),
    "Ocean": (False, 1991, 2026, 6, ["Reef Explorers", "Submarine", "Lighthouse"],
              "Deep Coral Tidal Azure Silent Rolling Pearl Windy Kelp Abyssal".split(), "Submarine Reef Lighthouse Trawler Dock Diver Buoy Lagoon Cove".split()),
    "Robotics": (False, 1998, 2026, 6, ["Builders", "Battle Mechs", "Lab Kits"],
                 "Turbo Cyber Steel Hyper Micro Quantum Chrome Pulse Neon Servo".split(), "Walker Crane Rover Arm Droid Loader Forge Drone Sentinel".split()),
    "Seasonal": (False, 1990, 2026, 4, ["Winter Village", "Harvest", "Spring Fair"],
                 "Frosty Cozy Festive Golden Sparkling Merry Snowy Blossom Jolly Bright".split(), "Cottage Sleigh Bakery Market Carousel Lantern Workshop Pavilion Greenhouse".split()),
    # invented franchises: the licensed flag is the reviewed, curated field the plan asks for
    "Skyfarer Saga": (True, 2005, 2022, 5, ["Heroes", "Airships"],
                      "Captain Storm Cloud Wind Sky Thunder Ember Gale Azure Brave".split(), "Airship Harbor Cutter Lighthouse Clocktower Skiff Anchor Citadel Beacon".split()),
    "Mina and the Moth": (True, 2012, 2026, 4, ["Moonlit Garden", "Lantern Festival"],
                          "Moonlit Whispering Tiny Glowing Velvet Dusky Silken Dreamy Twilight Hushed".split(), "Garden Lantern Treehouse Bridge Pond Cottage Orchard Windmill Gazebo".split()),
    "Starlight Cadets": (True, 2016, 2026, 4, ["Academy", "Rescue Squad"],
                         "Rookie Stellar Ace Junior Elite Rapid Cadet Bright Daring Nova".split(), "Academy Cruiser Pod Hangar Simulator Cruiser Tender Shuttle Dock".split()),
}
VARIANTS = "Alpha Beta Prime Classic Deluxe Mini Express Grand Junior Mk2 Origins Remix".split()
ROMAN = ["II", "III", "IV", "V", "VI", "VII"]

# size class -> (min pieces, max pieces, min colors, max colors, min parts, max parts, share)
CLASSES = {
    "tiny": (8, 50, 1, 4, 3, 20, 18), "small": (51, 200, 3, 9, 20, 80, 32), "medium": (201, 600, 6, 14, 60, 200, 28),
    "large": (601, 1500, 9, 20, 150, 400, 15), "huge": (1501, 4999, 14, 30, 300, 700, 6.5), "monumental": (5000, 9000, 20, 40, 450, 900, 0.5),
}


def size_class(year):
    allowed = ["tiny", "small", "medium"] if year < 1980 else ["tiny", "small", "medium", "large"] if year < 2000 else list(CLASSES)
    return r.choices(allowed, weights=[CLASSES[c][6] for c in allowed])[0]


def make_set(root):
    lic, y0, y1, _, subs, adjs, nouns = THEMES[root]
    year = r.choices(range(y0, y1 + 1), weights=[1 + (y - y0) ** 1.2 / 8 for y in range(y0, y1 + 1)])[0]  # busier in later years
    cls = size_class(year)
    pmin, pmax, cmin, cmax, qmin, qmax, _ = CLASSES[cls]
    pieces = r.randint(pmin, pmax)
    if pieces >= 100 and r.random() < 0.04:
        pieces = max(100, round(pieces, -2))  # marketing-friendly round counts
    colors = r.randint(cmin, min(cmax, 6 if year < 1980 else cmax))
    if cls == "tiny" and pieces <= 30 and r.random() < 0.3:
        colors = 1
    parts = min(r.randint(qmin, qmax), pieces)
    colors = min(colors, parts)
    figs = 0 if year < 1978 else {"tiny": r.choice([0, 0, 0, 1]), "small": r.choice([0, 1, 1, 2]), "medium": r.randint(1, 5),
                                  "large": r.randint(3, 9), "huge": r.randint(6, 14), "monumental": r.randint(8, 20)}[cls]
    return dict(year=year, theme=[root, r.choice(subs)], pieces=pieces, minifigs=figs, licensed=lic, colors=colors, parts=parts), adjs, nouns


roots = list(THEMES)
weights = [THEMES[t][3] for t in roots]
stems, names, sets = set(), set(), []
for _ in range(N):
    s, adjs, nouns = make_set(r.choices(roots, weights=weights)[0])
    base = f"{r.choice(adjs)} {r.choice(nouns)}"
    name = base
    for extra in [None] + VARIANTS + [f"{v} {x}" for v in VARIANTS[:3] for x in ROMAN]:
        name = base if extra is None else f"{base} {extra}"
        if name.lower() not in names:
            break
    names.add(name.lower())
    s["name"] = name
    sets.append(s)

for i in r.sample(range(N), 6):  # plant a few palindromic set numbers
    half = r.randint(100, 999)
    sets[i]["_stem"] = int(f"{half}{str(half)[::-1]}")
for s in sets:
    stem = s.pop("_stem", None)
    while stem is None or stem in stems:
        stem = r.randint(100000, 999999)
    stems.add(stem)
    s["id"] = f"{stem}-1"

sets.sort(key=lambda s: (s["year"], s["id"]))
order = ["id", "name", "year", "theme", "pieces", "minifigs", "licensed", "colors", "parts"]
meta = {"version": "v1", "publishedAt": PUBLISHED, "capturedAt": PUBLISHED, "seed": SEED,
        "provenance": "Invented catalog generated by tools/make_pool.py. No real product data.",
        "selection": "One entry per marketed set; rereleases and packaging variants are collapsed. Theme tree v1 is frozen. Piece counts are the advertised box count.",
        "fieldStatus": {"id": "known", "name": "known", "year": "known (year precision)", "theme": "known (frozen tree v1)",
                        "pieces": "known (advertised count)", "minifigs": "known and complete", "licensed": "known (reviewed flag)",
                        "colors": "known (complete inventory)", "parts": "known (complete inventory)"}}
lines = ",\n".join("  " + json.dumps({k: s[k] for k in order}, ensure_ascii=False, separators=(",", ":")) for s in sets)
out = '{"meta":' + json.dumps(meta, ensure_ascii=False) + ',\n"members":[\n' + lines + "\n]}\n"
path = pathlib.Path(__file__).resolve().parent.parent / "data" / "pool-v1.json"
path.parent.mkdir(exist_ok=True)
path.write_bytes(out.encode("utf-8"))
print(f"wrote {path} ({len(sets)} sets) sha256={hashlib.sha256(out.encode('utf-8')).hexdigest()}")
