# BrickRNG

A daily building-set discovery game: roll once per UTC day, draw one set from a pool, and see which badges make it distinctive. Built from `BrickRNG_Building_Plan` (chapters 3-7, 10, 12).

**This is a prototype with an invented catalog.** The plan makes real catalog data, product images and branding a launch gate, and I could not confirm Rebrickable's data terms (its download page sits behind a bot check). So every set here is made up by `tools/make_pool.py`: six-digit set numbers, generated names, and three invented licensed franchises. There is no backend, so results live in the player's browser. Unofficial fan project, not affiliated with or endorsed by the LEGO Group.

## What is built

| Plan area | Status |
| --- | --- |
| Daily roll, unbiased secure draw, one per UTC day, retry-safe | Done, browser-local (the day comes from the host's `Date` header, not the device clock) |
| 17 catalog badges, families, RP = 100 / p, overall rarity tiers, tie rules | Done, pure and tested in `rules.js`. Collector Milestone is a player achievement with no subject points, so it needs accounts and is not built |
| Animated reveal (name reel, count-up, rarity pulse and burst), skippable, reduced-motion aware; counts panel, share text, permanent result page | Done (placeholder brick, no product image) |
| Hundreds of achievements derived from your rolls, with goals scaled to the pool size (shelves by decade, year, theme, size, minifigures, license) | Done (`achievements.js`) |
| Badge catalog, badge pages, levels, history, export, delete | Done |
| Pool page (size, selection rule, composition, checksum, possible rarity bands) | Done |
| Sign-in, ranked limit, leaderboards, shelves, Want to Build, friends, hearts, poems, Discord, moderation | Needs a server (plan phases 2 and 3) |

## Using real sets (your call, not mine)

Rebrickable's API docs say anyone wanting the full set list must use its CSV downloads, and point to a Terms page about allowed use of the data. That page (and the downloads page) sit behind a bot check, so I could not read them, and accepting a site's terms is not something I should do for you. So the public site stays on the invented catalog.

To switch to real sets: read [Rebrickable's Terms](https://rebrickable.com/terms/), download `sets`, `themes`, `inventories`, `inventory_minifigs` and `inventory_parts` from its [downloads page](https://rebrickable.com/downloads/) into a folder, run `python tools/import_rebrickable.py <folder>` (tested by `python tools/test_import.py`), then `check.html` and push. The importer leaves any unknown value null (never 0), skips gear and books, and only sets the licensed/original flag for the reviewed theme lists at the top of the script. Image rights are a separate approval in the plan, so no product images are used.

## Run it

No build step.

```
python -m http.server 8765
```

Open <http://localhost:8765>. Open `/check.html` for the self-check; its title becomes `PASS` or `FAIL n`.

## Layout

- `engine.js` and `achievements.js` generic scoring, tiers, sampling, day helpers and achievements (shared with sibling RNG games)
- `rules.js` this game's badge rules; `site.js` its names, copy, card art and shelves; `fixtures.js` rule fixtures for `check.html`
- `app.js`, `index.html`, `style.css` the site (hash routes, so it works on any static host)
- `data/pool-v1.json` the published pool; `tools/make_pool.py` regenerates the invented pool byte for byte, `tools/import_rebrickable.py` builds a real one

## Publishing

GitHub Pages serves the repository root from `main`. Push to `main` to update the site.
