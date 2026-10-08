// Home: Level 2 on the path, locked until the Level 1 mastery check is PASSED; it says "coming soon" until Level 2 ships.
import { h, icon } from '../ui.js';
import { LESSONS } from '../content.js';

export function level2Teaser(prog, track) {
  if (LESSONS.some(l => l.level === 2)) return null;           // Level 2 lessons are on the path: the path locks them
  const passed = prog.lessons['L1.14']?.state === 'checked';
  return h('section', { class: 'lesson level2' }, h('h3', {}, track === 'A' ? 'Level 2: Sounds Together' : 'Level 2 · Sounds Together'),
    h('div', { class: track === 'A' ? 'path' : 'list' },
      h('button', { class: 'node locked wide', disabled: true, 'data-level': '2' }, icon('lock'), h('span', {}, 'Coming soon'))),
    h('p', { class: 'muted small' }, passed ? 'You passed Level 1. Level 2 is coming soon.' : 'Opens when you pass the Level 1 check.'));
}
