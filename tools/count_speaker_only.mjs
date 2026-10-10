// How many picture-card option sets end up speaker-only, before (old random-pool logic) and after (app/src/optionset.js).
//   node tools/count_speaker_only.mjs
// Only the oral screens (app/src/screens/l1oral.js, L1.01: 5 blend + 5 check sets) build picture-card sets; Levels 2-4 use printed-word tap gates.
import fs from 'node:fs'; import path from 'node:path'; import { buildSet } from '../app/src/optionset.js';
const J = f => JSON.parse(fs.readFileSync(new URL('../' + f, import.meta.url)));
const PICS = J('app/public/img/words/pictures.json'), META = J('app/public/img/words/pictures.meta.json'), IDX = J('content/audio_index.json').clips;
const lex = J('content/lexicon.json');
for (const f of fs.readdirSync(new URL('../content/levels', import.meta.url)).filter(f => /^L.*\.json$/.test(f)).sort()) {
  const b = J('content/levels/' + f); for (const [k, e] of Object.entries(b.lexicon)) if (!lex[k] || (e.kind === 'heart' && lex[k].kind !== 'heart')) lex[k] = e;
}
const env = { hasPic: w => !!PICS[w], isAmb: w => !!META[w]?.ambiguous, hasClip: w => !!IDX[`w:${w}`], phones: w => lex[w]?.p || null, isReal: w => lex[w]?.kind === 'real',
  level1: w => (lex[w].lessons || []).some(l => l.startsWith('L1.')), universe: Object.keys(lex).filter(w => lex[w].kind === 'real') };
const FIRST = ['sun', 'top', 'mat', 'pig', 'dog'], BLEND = ['at', 'sat', 'it', 'on', 'mat'], CHECK = ['sat', 'top', 'pig', 'dog', 'mat'];
const sets = [...BLEND.map(w => ({ w, kind: 'blend', pool: BLEND.concat(FIRST) })), ...CHECK.map(w => ({ w, kind: 'check', pool: CHECK.concat(BLEND) }))];
const good = w => env.hasPic(w) && !env.isAmb(w);
let before = 0, after = 0, labelled = 0, swapped = 0;
for (const s of sets) {
  const others = s.pool.filter(x => x !== s.w), n = others.length;
  // old logic: two random distractors from the pool; speaker-only if ANY of the 3 cards has no safe picture. Exact chance over all pairs:
  let bad = 0, tot = 0; for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) { tot++; if (!(good(s.w) && good(others[i]) && good(others[j]))) bad++; }
  before += bad / tot;
  const r = buildSet(s.w, s.pool, env, { seed: `${s.kind[0] === 'c' ? 't' : 'b'}:${s.w}` });
  after += r.speakerOnly ? 1 : 0; labelled += r.labelled ? 1 : 0; swapped += r.swapped;
  console.log(`${s.kind.padEnd(5)} ${s.w.padEnd(4)} old speaker-only chance ${(bad / tot * 100).toFixed(0).padStart(3)}%  new: ${r.words.join(', ')}${r.speakerOnly ? '  SPEAKER-ONLY' : ''}${r.labelled ? '  (target labelled)' : ''}`);
}
console.log('\nlevel  sets  speaker-only before (expected)  speaker-only after');
console.log(`L1     ${String(sets.length).padStart(4)}  ${before.toFixed(1).padStart(30)}  ${String(after).padStart(18)}   (target labelled: ${labelled}, swapped-in distractors: ${swapped})`);
for (const l of [2, 3, 4]) console.log(`L${l}        0                               0                   0   (printed-word tap gates, no picture sets)`);
