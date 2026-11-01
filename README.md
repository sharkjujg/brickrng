# BrickRNG

A daily building-set discovery game: roll once per UTC day, draw one set from a pool, and see which badges make it distinctive. Built from `BrickRNG_Building_Plan` (chapters 3-7, 10, 12).

**This is a prototype with real data.** The sets are a snapshot of [Rebrickable's catalog downloads](https://rebrickable.com/downloads/) (sets, themes, inventories, minifigure and part tables), converted by `tools/import_rebrickable.py` into `data/pool-v1.json`: one entry per primary set (number ending in -1) with at least one part, with gear, books, bulk bricks, collectible minifigure packs and education lines left out. No product images are used. A count Rebrickable has no inventory for is unknown (null) and never earns a badge. Unofficial fan project, not affiliated with or endorsed by the LEGO Group or Rebrickable. Set data is sourced from Rebrickable® (see the note below). LEGO® is a trademark of the LEGO Group, which does not sponsor, authorize or endorse this web site. There is no backend, so results live in the player's browser.

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

## Rebrickable® terms and LEGO® fair play (reviewed 2026-11-01)

The site owner supplied Rebrickable's Terms of Service and the LEGO Group's Fair Play guidance (the web page and the November 2018 brochure), and this project follows them:

- **Data route (Terms 5.1 and 5.3):** the catalog comes from the public CSV bulk downloads on Rebrickable's Downloads page, converted by `tools/import_rebrickable.py`. The API is not used, no MOC data is touched, and the only automated fetching is of those download files, which the Terms allow.
- **Credit (5.1):** the footer of every page, the About page and the hub say the set data is sourced from Rebrickable®, with a link.
- **Images (5.2):** none are used; the art is generated.
- **AI training (5.3):** the Terms forbid using Rebrickable content to train AI models. That applies to this derived data too.
- **LEGO® trademarks:** the red LEGO logo is never used, no domain or repository name contains the trademark, and the name appears only to refer to the products the catalog lists. The footer and About page carry the disclaimer "LEGO® is a trademark of the LEGO Group, which does not sponsor, authorize or endorse this web site", and the About page names the other LEGO trademarks that appear in set and theme names (the Minifigure, DUPLO®, NINJAGO®, MINDSTORMS®, LEGOLAND®). No LEGO images, instructions or catalog photographs are shown, so no copyright line is needed.

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
