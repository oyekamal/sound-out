// Step screens for Levels 2-4, dispatched from session.js for lessons with level > 1.
import { teach } from './teach.js';
import { rule } from './rule.js';
import { attack } from './attack.js';
import { check, mastery, attackcheck } from './levelcheck.js';
export const LEVEL_STEPS = { teach, rule, attack, check, mastery, attackcheck };
