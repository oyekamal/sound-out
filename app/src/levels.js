// Levels 2-4: the bundles tools/build_levels.py writes (content/levels/L<N>.json) and the tap-gate options
// tools/gen_options.py --level N writes (content/options_L<N>.json). Whatever level bundles exist are playable;
// content.js merges them into the Level 1 data. No import from content.js here (content.js imports this file).
import './levels.css';
const bundles = Object.values(import.meta.glob('../../content/levels/L*.json', { eager: true, import: 'default' })).sort((a, b) => a.level - b.level);
const opts = import.meta.glob('../../content/options_L*.json', { eager: true, import: 'default' });

export const LEVELS = bundles.map(b => b.level);
export const LEVEL_LESSONS = bundles.flatMap(b => b.lessons);
export const LEVEL_LEX = Object.assign({}, ...bundles.map(b => b.lexicon));
export const LEVEL_G2P = Object.assign({}, ...bundles.map(b => b.g2p));
export const LEVEL_OPTIONS = Object.assign({}, ...Object.values(opts));
// every clip key the level screens ask for that is not rendered yet (content/audio_needed.json): played as "audio coming"
export const COMING = new Set(bundles.flatMap(b => b.audioKeys || []));
