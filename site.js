// Everything specific to BrickRNG: names, copy, card art, and which facts the result card shows. app.js is generic.
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const fmt = (n) => n.toLocaleString('en');
const hash = (s) => { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) >>> 0; return h; };

export default {
  key: 'brickrng',
  name: 'BrickRNG',
  pageTitle: 'BrickRNG: a daily building-set discovery game',
  noun: 'set', nouns: 'sets', thing: 'Set',
  worldNote: 'the real world of building sets',
  repo: 'https://github.com/sharkjujg/brickrng',
  headline: 'Discover a set. Once a day.',
  intro: (n) => `Roll once to open today's display case: one set drawn from a pool of <b>${fmt(n)}</b>. Every set has the same 1-in-${fmt(n)} chance. Badges explain what makes it distinctive, and rarer badges earn more rarity points (RP). The daily limit resets at 00:00 UTC. A discovery is a digital badge, not a purchase.`,
  notice: 'Prototype: the sets and counts are real (Rebrickable catalog downloads), but there are no product images or accounts yet, and your results are saved only in this browser. <a href="#/about">What that means</a>',
  header: (m) => ({ title: m.name, sub: `Set ${m.id} · ${m.year}` }),
  label: (m) => `${m.name} (${m.year})`,
  // shelves drive the shelf achievements: every [group, label] a set belongs to
  shelves: (m) => [
    ['Decade', `${Math.floor(m.year / 10) * 10}s`], ['Release year', String(m.year)], ['Theme', m.theme[0]],
    ...(m.theme.length > 1 ? [['Sub-theme', m.theme.join(' › ')]] : []),
    ['Size', m.pieces <= 50 ? 'Tiny (up to 50 pieces)' : m.pieces <= 200 ? 'Small (51 to 200)' : m.pieces <= 600 ? 'Medium (201 to 600)' : m.pieces < 1000 ? 'Large (601 to 999)' : m.pieces < 5000 ? 'Grand (1,000 to 4,999)' : 'Monumental (5,000 or more)'],
    ...(m.minifigs === null ? [] : [['Minifigures', m.minifigs === 0 ? 'None' : m.minifigs === 1 ? 'One' : m.minifigs < 5 ? '2 to 4' : m.minifigs < 10 ? '5 to 9' : '10 or more']]),
    ...(m.licensed === null ? [] : [['License', m.licensed ? 'Licensed worlds' : 'Original worlds']]),
  ],
  facts: (m) => [
    ['Set number', m.id], ['Released', String(m.year)], ['Theme', m.theme.join(' › ')], ['Pieces (Rebrickable count)', fmt(m.pieces)],
    ['Minifigures', m.minifigs === null ? 'unknown (no inventory)' : String(m.minifigs)],
    ['Licensed theme', m.licensed === null ? 'not reviewed' : m.licensed ? 'Yes' : 'No'],
    ['Colors in inventory', m.colors === null ? 'unknown (no inventory)' : String(m.colors)], ['Distinct parts', m.parts === null ? 'unknown (no inventory)' : String(m.parts)],
    ['Counts', "Pieces are Rebrickable's part count; colors and parts come from the set's newest inventory, minus spares"],
    ['Source', 'Rebrickable', `https://rebrickable.com/sets/${encodeURIComponent(m.id)}/`],
  ],
  art(m) { // original placeholder brick: no product image is shown, and it never affects scoring
    const hue = hash(m.theme[0]) % 360;
    const studs = [0, 1, 2, 3].flatMap((i) => [0, 1].map((j) => `<circle cx="${24 + i * 17.3}" cy="${36 + j * 16}" r="6.2"/>`)).join('');
    return `<svg class="avatar" viewBox="0 0 100 100" role="img" aria-label="Placeholder brick for the set. No product image is shown.">
      <rect width="100" height="100" rx="8" fill="hsl(${hue} 30% 90%)"/>
      <rect x="10" y="30" width="80" height="46" rx="5" fill="hsl(${hue} 60% 42%)"/><rect x="10" y="64" width="80" height="12" rx="3" fill="hsl(${hue} 60% 32%)"/>
      <g fill="hsl(${hue} 60% 52%)" stroke="hsl(${hue} 60% 30%)" stroke-width="1">${studs}</g>
      <text x="50" y="92" text-anchor="middle" font-family="system-ui,sans-serif" font-size="8" letter-spacing="1" fill="hsl(${hue} 30% 30%)">NO IMAGE</text></svg>`;
  },
  poolNotice: 'Every set comes from <a href="https://rebrickable.com/downloads/">Rebrickable\'s catalog downloads</a> as a snapshot, converted by <code>tools/import_rebrickable.py</code>: one entry per primary set (number ending in -1) with at least one part, with gear, books, bulk bricks, collectible minifigure packs and education lines left out. A count Rebrickable has no inventory for is unknown and never earns a badge, and the licensed/original flag is set only for a hand-reviewed list of theme roots. Odds describe this pool. They say nothing about how rare a real set is in shops or on the secondhand market, and no product images are used.',
  poolExtra(pool) {
    const tally = (get) => { const c = new Map(); for (const m of pool.members) for (const v of get(m)) c.set(v, (c.get(v) || 0) + 1); return [...c]; };
    const table = (title, rows) => `<table><thead><tr><th>${title}</th><th class="n">Sets</th></tr></thead><tbody>${rows.map(([k, v]) => `<tr><td>${esc(k)}</td><td class="n">${fmt(v)}</td></tr>`).join('')}</tbody></table>`;
    const decades = tally((m) => [`${Math.floor(m.year / 10) * 10}s`]).sort((a, b) => a[0].localeCompare(b[0]));
    const themes = tally((m) => [m.theme[0] + (m.licensed ? ' (licensed)' : '')]).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
    return `<h2>What is in the pool</h2><p class="small muted">Disclosed because a badge is only rare relative to this mix.</p>${table('Decade', decades)}${table('Theme', themes)}`;
  },
  aboutData: `<h2>About the sets</h2>
    <p>Each entry is one marketed set. Only the primary version of each set counts, so rereleases and packaging variants do not multiply its chance. Piece counts are Rebrickable's part counts; colors and distinct parts come from each set's newest inventory, spare parts excluded. The theme tree is frozen per pool version. A minifigure count is known only when Rebrickable has an inventory for the set, and an unknown count is never treated as zero. Price, resale value and retirement status play no part in the game. A discovery here is a digital badge, not a product, a voucher or an official reward.</p>`,
  terms: 'It is not affiliated with, sponsored or endorsed by the LEGO Group or Rebrickable; LEGO and the names of themes and franchises belong to their owners. Catalog facts come from Rebrickable and any errors in the snapshot or the badges are this prototype\'s. Badges describe catalog facts, not value or quality.',
};
