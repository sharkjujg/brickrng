# BrickRNG

A daily building-set discovery game: roll once per UTC day, draw one set from a pool, and see which badges make it distinctive. Built from `BrickRNG_Building_Plan` (chapters 3-7, 10, 12).

**This is a prototype with real data.** The sets are a snapshot of [Rebrickable's catalog downloads](https://rebrickable.com/downloads/) (sets, themes, inventories, minifigure and part tables), converted by `tools/import_rebrickable.py` into `data/pool-v1.json`: one entry per primary set (number ending in -1) with at least one part, with gear, books, bulk bricks, collectible minifigure packs and education lines left out. No product images are used. A count Rebrickable has no inventory for is unknown (null) and never earns a badge. Unofficial fan project, not affiliated with or endorsed by the LEGO Group or Rebrickable. Rebrickable's terms apply to its data (see the note below). There is no backend, so results live in the player's browser.

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

## Data and Rebrickable's terms (please read)

Rebrickable's API documentation says anyone wanting the full set list must use its CSV downloads, and refers to a Terms page about allowed use of the data. That Terms page sits behind a bot check, so **I could not read it**, and I did not work around the check. I used the public bulk files from `cdn.rebrickable.com` that the documentation points to, kept attribution on the site, and used no images. If the terms do not allow this use, delete this repository or replace `data/pool-v1.json`: the importer, the rules and the site do not change.

To refresh the data: download `sets`, `themes`, `inventories`, `inventory_minifigs` and `inventory_parts` (`.csv.gz`) into a folder, run `python tools/import_rebrickable.py <folder>` (the converter is tested by `python tools/test_import.py`), open `check.html`, and push. Which theme roots count as licensed or original is a reviewed list at the top of the script; every other theme stays unknown.

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
- `data/pool-v1.json` the published pool; `tools/import_rebrickable.py` rebuilds it from Rebrickable's CSV downloads

## Publishing

GitHub Pages serves the repository root from `main`. Push to `main` to update the site.
