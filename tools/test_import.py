#!/usr/bin/env python3
"""Check import_rebrickable.py against a tiny hand-made set of tables in Rebrickable's column layout.
Usage: python tools/test_import.py   (prints OK or raises)"""
import csv
import pathlib
import tempfile

import import_rebrickable as imp

TABLES = {
    "themes": ("id,name,parent_id", ["1,Space,", "2,Moon Base,1", "3,Gear,", "4,Star Wars,", "5,Mystery Box,"]),
    "sets": ("set_num,name,year,theme_id,num_parts,img_url", [
        "1111-1,Alpha,1999,2,120,x", "2222-1,Beta,2010,4,1500,x", "3333-1,Gear thing,2005,3,10,x", "4444-2,Variant,2001,1,50,x",
        "5555-1,Zero parts,2000,1,0,x", "6666-1,No inventory,1985,1,40,x", "7777-1,Unlisted root,2003,5,30,x"]),
    "inventories": ("id,version,set_num", ["10,1,1111-1", "11,2,1111-1", "20,1,2222-1"]),
    "inventory_minifigs": ("inventory_id,fig_num,quantity", ["11,fig-1,2", "10,fig-9,5"]),  # the older inventory (10) must be ignored
    "inventory_parts": ("inventory_id,part_num,color_id,quantity,is_spare,img_url", [
        "11,3001,1,4,f,x", "11,3002,1,2,f,x", "11,3001,5,1,f,x", "11,3003,5,9,t,x", "20,3001,9999,3,f,x", "20,3001,-1,1,f,x"]),
}
with tempfile.TemporaryDirectory() as d:
    for name, (header, body) in TABLES.items():
        pathlib.Path(d, name + ".csv").write_text(header + "\n" + "\n".join(body) + "\n", encoding="utf-8")
    got = {m["id"]: m for m in imp.convert(d)}

assert list(got) == ["6666-1", "1111-1", "2222-1", "7777-1"] or list(got) == ["6666-1", "1111-1", "7777-1", "2222-1"], list(got)
assert "3333-1" not in got and "4444-2" not in got and "5555-1" not in got, "gear, a -2 variant and a zero-part set must be skipped"
a = got["1111-1"]
assert (a["theme"], a["minifigs"], a["colors"], a["parts"], a["licensed"]) == (["Space", "Moon Base"], 2, 2, 2, False), a  # newest inventory, spares skipped
b = got["2222-1"]
assert (b["minifigs"], b["colors"], b["parts"], b["licensed"]) == (0, None, 1, True), b  # inventory with no minifigs is 0; only no-color rows give unknown colors
c = got["6666-1"]
assert (c["minifigs"], c["colors"], c["parts"]) == (None, None, None), c  # no inventory: unknown, never zero
assert got["7777-1"]["licensed"] is None, "a theme root that is not on either reviewed list stays unknown"
print("OK: import_rebrickable converts the fixture as expected")
