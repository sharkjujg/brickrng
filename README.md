# BrickRNG

A daily building-set discovery game: roll once per UTC day, draw one set from a pool, and see which badges make it distinctive. Built from `BrickRNG_Building_Plan` (chapters 3-7, 10, 12).

**This is a prototype with an invented catalog.** The plan makes real catalog data, product images and branding a launch gate, and I could not confirm Rebrickable's data terms (its download page sits behind a bot check). So every set here is made up by `tools/make_pool.py`: six-digit set numbers, generated names, and three invented licensed franchises. There is no backend, so results live in the player's browser. Unofficial fan project, not affiliated with or endorsed by the LEGO Group.

## What is built

| Plan area | Status |
| --- | --- |
| Daily roll, unbiased secure draw, one per UTC day, retry-safe | Done, browser-local (the day comes from the host's `Date` header, not the device clock) |
| 17 catalog badges, families, RP = 100 / p, overall rarity tiers, tie rules | Done, pure and tested in `rules.js`. Collector Milestone is a player achievement with no subject points, so it needs accounts and is not built |
| Reveal (skippable, reduced-motion aware), counts panel, share text, permanent result page | Done (placeholder brick, no product image) |
| Badge catalog, badge pages, levels, history, export, delete | Done |
| Pool page (size, selection rule, composition, checksum, possible rarity bands) | Done |
| Sign-in, ranked limit, leaderboards, shelves, Want to Build, friends, hearts, poems, Discord, moderation | Needs a server (plan phases 2 and 3) |

## Using real sets later

Download the catalog tables yourself from Rebrickable (after reading its terms) and write a converter to the pool format below; the engine, rules and site need no changes. Each pool member is `{id, name, year, theme: [root, sub], pieces, minifigs, licensed, colors, parts}`. A field that is unknown must be `null` or absent, never `0`: the rules treat unknown as not matching. Image rights are a separate approval in the plan.

## Run it

No build step.

```
python -m http.server 8765
```

Open <http://localhost:8765>. Open `/check.html` for the self-check; its title becomes `PASS` or `FAIL n`.

## Layout

- `engine.js` generic scoring, tiers, sampling, day helpers (shared with sibling RNG games)
- `rules.js` this game's badge rules; `site.js` its names, copy and card art; `fixtures.js` rule fixtures for `check.html`
- `app.js`, `index.html`, `style.css` the site (hash routes, so it works on any static host)
- `data/pool-v1.json` the published pool; `tools/make_pool.py` regenerates it byte for byte

## Publishing

GitHub Pages serves the repository root from `main`. Push to `main` to update the site.
