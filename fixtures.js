// BrickRNG fixtures for check.html: one row per case, [rule id, field overrides, expected match].
export const V = '2026-11-01';
export const base = { id: '123456-1', name: 'Sample Set', year: 2005, theme: ['City', 'Harbor'], pieces: 300, minifigs: 3,
  licensed: false, colors: 8, parts: 60 };

export const cases = [
  ['vintage-shelf', { year: 1989 }, true], ['vintage-shelf', { year: 1990 }, false], ['vintage-shelf', { year: null }, false], ['vintage-shelf', { year: 0 }, false],
  ['early-builder', { year: 1979 }, true], ['early-builder', { year: 1980 }, false], ['early-builder', { year: '1970' }, false],
  ['tiny-build', { pieces: 50 }, true], ['tiny-build', { pieces: 51 }, false], ['tiny-build', { pieces: 0 }, false], ['tiny-build', { pieces: null }, false],
  ['grand-build', { pieces: 1000 }, true], ['grand-build', { pieces: 999 }, false],
  ['monumental', { pieces: 5000 }, true], ['monumental', { pieces: 4999 }, false],
  ['no-crew', { minifigs: 0 }, true], ['no-crew', { minifigs: null }, false], ['no-crew', { minifigs: undefined }, false], ['no-crew', { minifigs: -1 }, false], ['no-crew', { minifigs: 1 }, false], // unknown is not zero
  ['solo-figure', { minifigs: 1 }, true], ['solo-figure', { minifigs: 2 }, false], ['solo-figure', { minifigs: null }, false],
  ['full-crew', { minifigs: 10 }, true], ['full-crew', { minifigs: 9 }, false], ['full-crew', { minifigs: null }, false],
  ['space-shelf', { theme: ['Space', 'Moon Base'] }, true], ['space-shelf', { theme: ['City', 'Harbor'] }, false], ['space-shelf', { theme: undefined }, false],
  ['castle-shelf', { theme: ['Castle'] }, true], ['castle-shelf', { theme: ['Space'] }, false],
  ['licensed-world', { licensed: true }, true], ['licensed-world', { licensed: false }, false], ['licensed-world', { licensed: null }, false], ['licensed-world', { licensed: 'yes' }, false],
  ['original-world', { licensed: false }, true], ['original-world', { licensed: true }, false], ['original-world', { licensed: null }, false],
  ['one-color', { colors: 1 }, true], ['one-color', { colors: 2 }, false], ['one-color', { colors: 0 }, false], ['one-color', { colors: null }, false],
  ['rainbow-build', { colors: 12 }, true], ['rainbow-build', { colors: 11 }, false], ['rainbow-build', { colors: null }, false],
  ['part-variety', { parts: 100 }, true], ['part-variety', { parts: 99 }, false], ['part-variety', { parts: null }, false],
  ['mirror-set-id', { id: '123321-1' }, true], ['mirror-set-id', { id: '12321-1' }, true], ['mirror-set-id', { id: '123456-1' }, false],
  ['mirror-set-id', { id: '11-1' }, false], ['mirror-set-id', { id: 'ab-1' }, false], ['mirror-set-id', { id: undefined }, false],
  ['round-count', { pieces: 100 }, true], ['round-count', { pieces: 5000 }, true], ['round-count', { pieces: 99 }, false], ['round-count', { pieces: 150 }, false],
  ['round-count', { pieces: 0 }, false],
];

export function poolChecks(raw, pool, ok) {
  const ms = raw.members;
  ok('set numbers look like "number-suffix" (early sets use dots, a few use names) and are unique', new Set(ms.map((m) => m.id)).size === pool.n && ms.every((m) => /^[0-9A-Za-z.-]+-[0-9]+$/.test(m.id)));
  ok('every set has complete basic facts', ms.every((m) => Number.isInteger(m.year) && m.year >= 1949 && m.year <= +raw.meta.capturedAt.slice(0, 4) && Number.isInteger(m.pieces) && m.pieces > 0
    && Array.isArray(m.theme) && m.theme.length >= 1 && m.name));
  ok('unknown counts are null, never 0 for colors and parts', ms.every((m) => ['colors', 'parts'].every((k) => m[k] === null || (Number.isInteger(m[k]) && m[k] > 0))));
  ok('distinct parts never exceed pieces, where known (colors can exceed distinct parts: one shape in several colors)', ms.every((m) => m.parts === null || m.parts <= m.pieces));
  ok('no figures before the first ones (1970s; Rebrickable counts the early stiff figures as minifigures)', ms.every((m) => m.year >= 1970 || !m.minifigs));
  ok('the pool is large enough to be a game (>= 1000)', pool.n >= 1000);
}
