// Scan: rebuild the text the Read-it screen displays for every passage in every level bundle (content/levels/L*.json)
// and compare with the source string (whitespace normalised). Tokenizer markup (the per-grapheme spans) is ignored.
//   node tools/scan_read_text.mjs          # uses app/src/readtext.js (the shipped code)
//   node tools/scan_read_text.mjs --old    # the pre-fix inline logic, for before/after counts
import fs from 'fs';
import path from 'path';
import { splitToken, wordUnits } from '../app/src/readtext.js';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const old = process.argv.includes('--old');
const readJ = p => JSON.parse(fs.readFileSync(path.join(root, p), 'utf8'));

// lexicon as content.js merges it: Level 1 lexicon, then level bundles (heart entries win)
const lexicon = readJ('content/lexicon.json');
const bundles = fs.readdirSync(path.join(root, 'content/levels')).filter(f => /^L\d+\.json$/.test(f)).sort().map(f => readJ('content/levels/' + f));
for (const b of bundles) for (const [k, e] of Object.entries(b.lexicon)) if (!lexicon[k] || (e.kind === 'heart' && lexicon[k].kind !== 'heart')) lexicon[k] = e;
const entry = w => lexicon[w] || lexicon[w.toLowerCase()];

function display(text) {
  const out = [];
  for (const tok of text.split(/\s+/)) {
    if (old) {
      const bare = tok.replace(/[^A-Za-z']/g, '');
      const e = entry(bare === 'I' ? 'I' : bare.toLowerCase());
      const core = e ? e.g.map((g, i) => (i === 0 && /^[A-Z]/.test(bare) ? g.toUpperCase() : g)).join('') : bare;
      out.push(core + tok.replace(/[A-Za-z']/g, ''));
    } else {
      const { lead, core, trail, bare } = splitToken(tok);
      const e = entry(bare === 'I' ? 'I' : bare.toLowerCase());
      out.push(lead + (e ? wordUnits(bare, e).join('') : core) + trail);
    }
  }
  return out.join(' ');
}

let total = 0, bad = 0;
const rows = [];
for (const b of bundles) for (const l of b.lessons) for (const tr of ['A', 'B']) {
  const t = l.read?.[tr]?.text;
  if (!t) continue;
  total++;
  const src = t.split(/\s+/).join(' '), got = display(t);
  if (src !== got) {
    bad++;
    const s = src.split(' '), g = got.split(' ');
    rows.push(`${l.id} ${tr}: ` + s.map((w, i) => w !== g[i] ? `${w} -> ${g[i]}` : null).filter(Boolean).join(' | '));
  }
}
console.log(`levels scanned: ${bundles.map(b => 'L' + b.level).join(',')}`);
console.log(`passages: ${total}, mismatched passages: ${bad}`);
let words = 0; for (const r of rows) words += r.split(' | ').length;
console.log(`mismatched words: ${words}`);
for (const r of rows.slice(0, 12)) console.log('  ' + r.slice(0, 200));
process.exit(bad ? 1 : 0);
