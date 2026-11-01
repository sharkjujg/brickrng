// BrickRNG badge rules. Each rule is a deterministic predicate over known fields: missing data never matches.
// test(m, poolDate) and evidence(m, poolDate) read the prepared member from prep().
// Collector Milestone from the plan is a player achievement (no subject points), so it is not in this catalog.

export const RULESET = '2'; // 2: common band badges added so no record earns nothing

export const norm = (s) => s.normalize('NFKC').toLowerCase();

const fmt = (n) => n.toLocaleString('en');
const stem = (m) => (typeof m.id === 'string' ? m.id.split('-')[0] : '');
const sub = (m) => (m.theme.length > 1 ? ` (${m.theme.join(' › ')})` : '');
const pcs = (m) => `${m.name} has ${fmt(m.pieces)} pieces`;
const figs = (m) => `${m.name} has ${m.minifigs} minifigure${m.minifigs === 1 ? '' : 's'}`;
const yr = (m) => `${m.name} was released in ${m.year}`;

export function prep(raw) {
  const pos = (x) => (Number.isInteger(x) && x > 0 ? x : null); // zero or absent is unknown, never a real count
  return {
    ...raw,
    year: pos(raw.year), pieces: pos(raw.pieces), colors: pos(raw.colors), parts: pos(raw.parts),
    minifigs: Number.isInteger(raw.minifigs) && raw.minifigs >= 0 ? raw.minifigs : null, // 0 is a real, complete count; absent is unknown
    theme: Array.isArray(raw.theme) ? raw.theme : [],
    licensed: typeof raw.licensed === 'boolean' ? raw.licensed : null,
  };
}

export const RULES = [
  { id: 'vintage-shelf', name: 'Vintage Shelf', family: 'Release era', rule: 'Released before 1990',
    test: (m) => m.year !== null && m.year < 1990, evidence: yr },
  { id: 'early-builder', name: 'Early Builder', family: 'Release era', rule: 'Released before 1980',
    test: (m) => m.year !== null && m.year < 1980, evidence: yr },
  { id: 'tiny-build', name: 'Tiny Build', family: 'Build size', rule: 'Advertised piece count of 50 or fewer',
    test: (m) => m.pieces !== null && m.pieces <= 50, evidence: pcs },
  { id: 'grand-build', name: 'Grand Build', family: 'Build size', rule: 'Advertised piece count of 1,000 or more',
    test: (m) => m.pieces !== null && m.pieces >= 1000, evidence: pcs },
  { id: 'monumental', name: 'Monumental', family: 'Build size', rule: 'Advertised piece count of 5,000 or more',
    test: (m) => m.pieces !== null && m.pieces >= 5000, evidence: pcs },
  { id: 'no-crew', name: 'No Crew', family: 'Crew size', rule: 'A complete minifigure count of exactly 0',
    test: (m) => m.minifigs === 0, evidence: (m) => `${m.name} has no minifigures` },
  { id: 'solo-figure', name: 'Solo Figure', family: 'Crew size', rule: 'A complete minifigure count of exactly 1',
    test: (m) => m.minifigs === 1, evidence: figs },
  { id: 'full-crew', name: 'Full Crew', family: 'Crew size', rule: 'A complete minifigure count of 10 or more',
    test: (m) => m.minifigs !== null && m.minifigs >= 10, evidence: figs },
  { id: 'space-shelf', name: 'Space Shelf', family: 'Theme', rule: 'Theme path includes the Space root',
    test: (m) => m.theme.includes('Space'), evidence: (m) => `${m.name} is in Space${sub(m)}` },
  { id: 'castle-shelf', name: 'Castle Shelf', family: 'Theme', rule: 'Theme path includes the Castle root',
    test: (m) => m.theme.includes('Castle'), evidence: (m) => `${m.name} is in Castle${sub(m)}` },
  { id: 'licensed-world', name: 'Licensed World', family: 'License category', rule: 'Theme is flagged as licensed by review',
    test: (m) => m.licensed === true, evidence: (m) => `${m.name} belongs to a licensed theme${sub(m)}` },
  { id: 'original-world', name: 'Original World', family: 'License category', rule: 'Theme is explicitly flagged as not licensed',
    test: (m) => m.licensed === false, evidence: (m) => `${m.name} belongs to an original theme${sub(m)}` },
  { id: 'one-color', name: 'One Color', family: 'Inventory colors', rule: 'Complete inventory uses exactly one color',
    test: (m) => m.colors === 1, evidence: (m) => `${m.name} uses a single color` },
  { id: 'rainbow-build', name: 'Rainbow Build', family: 'Inventory colors', rule: 'Complete inventory uses 12 or more colors',
    test: (m) => m.colors !== null && m.colors >= 12, evidence: (m) => `${m.name} uses ${m.colors} colors` },
  { id: 'part-variety', name: 'Part Variety', family: 'Part variety', rule: 'Complete inventory has 100 or more distinct parts',
    test: (m) => m.parts !== null && m.parts >= 100, evidence: (m) => `${m.name} has ${m.parts} distinct parts` },
  { id: 'mirror-set-id', name: 'Mirror Set ID', family: 'Identifier', rule: 'Numeric set number (before the dash) reads the same backwards, 3+ digits',
    test: (m) => /^[0-9]{3,}$/.test(stem(m)) && stem(m) === [...stem(m)].reverse().join(''), evidence: (m) => `Set number ${stem(m)} reads the same backwards` },
  { id: 'round-count', name: 'Round Count', family: 'Count pattern', rule: 'Advertised piece count is 100 or more and divisible by 100',
    test: (m) => m.pieces !== null && m.pieces >= 100 && m.pieces % 100 === 0, evidence: pcs },
  { id: 'mid-build', name: 'Mid-Size Build', family: 'Build size', rule: 'Advertised piece count from 51 through 999',
    test: (m) => m.pieces !== null && m.pieces >= 51 && m.pieces <= 999, evidence: pcs },
  { id: 'small-crew', name: 'Small Crew', family: 'Crew size', rule: 'A complete minifigure count from 2 through 9',
    test: (m) => m.minifigs !== null && m.minifigs >= 2 && m.minifigs <= 9, evidence: figs },
];
