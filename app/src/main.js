import './style.css';
import * as db from './db.js';
import { onboarding } from './onboarding.js';
import { home } from './home.js';
import { runSitting } from './session.js';
import { nextOpen, allSittings } from './path.js';
import { stop } from './audio.js';
import './screens/session/index.js'; // Levels 5-7 practice (Library + session screens)

const root = document.getElementById('app');
let profile = null;
const app = {
  mount(el) { root.replaceChildren(el); window.scrollTo(0, 0); },
  async boot() {
    const id = await db.setting('active');
    profile = id ? await db.get('profiles', id) : null;
    if (!profile) return onboarding(app);
    return home(app, profile);
  },
  home() { stop(); return home(app, profile); },
  onboarding() { stop(); return onboarding(app); },
  async firstSitting(p) { profile = p; return app.sitting(allSittings(p.track)[0].key); },
  async sitting(key) { stop(); try { await runSitting(app, profile, key); } catch (e) { console.error(e); app.home(); } },
  nextOpen: (prog, track, key) => nextOpen(prog, track, key),
};
window.__so = window.__so || { trace: [], missing: [] };
window.__so.app = app;
app.boot();
