#!/usr/bin/env python3
"""Convert Rebrickable's downloadable CSV tables into data/pool-v1.json, the pool format BrickRNG reads.

Real data is a choice for the site owner: read Rebrickable's Terms (https://rebrickable.com/terms/) and download the
tables yourself from https://rebrickable.com/downloads/ . Put sets, themes, inventories, inventory_minifigs and
inventory_parts (.csv or .csv.gz) in one folder, then:

    python tools/import_rebrickable.py <folder>

Rules of thumb used here: one entry per primary set (set number ending in -1) with at least one part; gear, books and
similar roots are skipped; minifigure, color and part counts come from the newest inventory of each set and are left
unknown (null) when a set has no inventory; unknown never earns a badge. The licensed/original flag is only set for the
theme roots listed below, which is a reviewed list to extend: other themes stay null.
"""
import collections
import csv
import datetime as dt
import gzip
import io
import json
import pathlib
import sys

EXCLUDE_ROOTS = {"Gear", "Books", "Supplemental", "Service Packs", "Educational and Dacta", "Promotional", "Other", "LEGO Brand Store", "Bulk Bricks",
                 "Collectible Minifigures", "FIRST LEGO League", "Power Functions"}  # the plan keeps these out until they are defined as separate categories
# Reviewed by hand against Rebrickable's root theme names: third-party franchises versus themes the LEGO Group created. Everything else stays unknown (null).
LICENSED_ROOTS = {"Star Wars", "Super Heroes Marvel", "Super Heroes DC", "Disney", "Minecraft", "Harry Potter", "Jurassic World", "Jurassic Park", "Super Mario",
                  "Speed Champions", "The Hobbit and Lord of the Rings", "Indiana Jones", "Pokémon", "Sonic The Hedgehog", "Teenage Mutant Ninja Turtles",
                  "Animal Crossing", "Cars", "Ghostbusters", "The Simpsons", "Back to the Future", "Toy Story", "Pirates of the Caribbean", "Avatar", "Wicked"}
ORIGINAL_ROOTS = {"City", "Town", "Castle", "Space", "Pirates", "Technic", "Creator", "Friends", "Ninjago", "Classic", "Train", "Western", "Aquazone", "Monkie Kid",
                  "Hidden Side", "Bionicle", "Duplo", "Explorien", "Rock Raiders", "Racers", "Hero Factory", "Legends of Chima", "Nexo Knights", "Mixels", "Belville",
                  "Scala", "Fabuland", "Adventurers", "Exo-Force", "Dreamzzz", "Elves", "Atlantis", "Alpha Team", "Agents", "Power Miners", "Galidor", "Mindstorms",
                  "Primo", "Juniors", "4 Juniors", "DOTS", "Architecture", "Modular Buildings", "Studios", "Freestyle", "Homemaker", "Znap", "Xtra", "Boat"}
NO_COLOR = {"-1", "9999"}  # Rebrickable's "unknown" and "no/any color" entries are not real element colors


def rows(folder, name):
    for suffix in (".csv", ".csv.gz"):
        p = pathlib.Path(folder) / (name + suffix)
        if p.exists():
            opener = gzip.open if suffix.endswith("gz") else open
            with opener(p, "rt", encoding="utf-8", newline="") as f:
                yield from csv.DictReader(f)
            return
    raise FileNotFoundError(f"{name}.csv or {name}.csv.gz not found in {folder}")


def convert(folder):
    themes = {r["id"]: (r["name"], r["parent_id"]) for r in rows(folder, "themes")}

    def path(tid):
        out = []
        while tid and tid in themes and len(out) < 4:
            name, tid = themes[tid]
            out.append(name)
        return out[::-1]

    sets = {}
    for r in rows(folder, "sets"):
        p = path(r["theme_id"])
        if r["set_num"].endswith("-1") and int(r["num_parts"] or 0) > 0 and p and p[0] not in EXCLUDE_ROOTS and r["year"].isdigit():
            sets[r["set_num"]] = {"id": r["set_num"], "name": r["name"].strip(), "year": int(r["year"]), "theme": p[:3], "pieces": int(r["num_parts"])}

    newest = {}  # set number -> (version, inventory id)
    for r in rows(folder, "inventories"):
        if r["set_num"] in sets and (r["set_num"] not in newest or int(r["version"]) > newest[r["set_num"]][0]):
            newest[r["set_num"]] = (int(r["version"]), r["id"])
    inv_set = {inv: s for s, (_, inv) in newest.items()}

    figs = collections.Counter()
    for r in rows(folder, "inventory_minifigs"):
        if r["inventory_id"] in inv_set:
            figs[inv_set[r["inventory_id"]]] += int(r["quantity"])
    colors, parts = collections.defaultdict(set), collections.defaultdict(set)
    try:
        for r in rows(folder, "inventory_parts"):
            s = inv_set.get(r["inventory_id"])
            if s and r.get("is_spare", "f").lower() not in ("t", "true", "1"):
                parts[s].add(r["part_num"])
                if r["color_id"] not in NO_COLOR:
                    colors[s].add(r["color_id"])
    except FileNotFoundError:
        pass

    members = []
    for sid, m in sets.items():
        has_inv = sid in newest
        root = m["theme"][0]
        m["minifigs"] = figs.get(sid, 0) if has_inv else None  # a set with an inventory and no minifigure rows really has none
        m["licensed"] = True if root in LICENSED_ROOTS else False if root in ORIGINAL_ROOTS else None
        m["colors"] = len(colors[sid]) or None if has_inv else None
        m["parts"] = len(parts[sid]) or None if has_inv else None
        members.append(m)
    members.sort(key=lambda m: (m["year"], m["id"]))
    return members


def write(members, out_path, source_note):
    n = len(members)
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    cov = lambda f: f"known for {sum(m[f] is not None for m in members):,} of {n:,}; unknown never satisfies a badge"
    meta = {"version": "v1", "publishedAt": today, "capturedAt": today, "source": "Rebrickable catalog downloads (https://rebrickable.com/downloads/)",
            "provenance": f"Imported {today} by tools/import_rebrickable.py. {source_note} Rebrickable's terms apply to this data.",
            "selection": "One entry per primary set (number ending in -1) with at least one part; gear, books and similar roots skipped. Piece counts are Rebrickable's part counts.",
            "fieldStatus": {"id": "known", "name": "known", "year": "known (year precision)", "theme": "known (Rebrickable theme tree)", "pieces": "known",
                            "minifigs": cov("minifigs"), "licensed": cov("licensed"), "colors": cov("colors"), "parts": cov("parts")}}
    order = ["id", "name", "year", "theme", "pieces", "minifigs", "licensed", "colors", "parts"]
    lines = ",\n".join("  " + json.dumps({k: m[k] for k in order}, ensure_ascii=False, separators=(",", ":")) for m in members)
    pathlib.Path(out_path).write_bytes(('{"meta":' + json.dumps(meta, ensure_ascii=False) + ',\n"members":[\n' + lines + "\n]}\n").encode("utf-8"))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    ms = convert(sys.argv[1])
    out = pathlib.Path(__file__).resolve().parent.parent / "data" / "pool-v1.json"
    write(ms, out, "Real catalog data.")
    print(f"wrote {out}: {len(ms)} sets")
