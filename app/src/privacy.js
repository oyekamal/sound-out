// "For grown-ups": the privacy policy as plain text, reached from Home behind the grown-up gate. No links: the address is text.
import { h, btn } from './ui.js';

const ROWS = [
  ['A learner profile: an automatic label such as "Child 1" or "Grown-up 1", and the track chosen (child or grown-up)', 'So progress stays separate when more than one person uses a phone'],
  ['Lesson progress, check results, review cards for sounds and words, days practised, stickers', 'To pick the next lesson, bring back what was missed, and show progress'],
  ['Two small flags: whether the first-time demo was shown, and the active profile', 'So the demo is not repeated'],
];

export function privacyScreen(app) {
  const s = h('div', { class: 'privacy track-B' },
    h('header', { class: 'hdr' }, btn('Home', 'home', { class: 'btn ghost small', onclick: () => app.home() })),
    h('h1', {}, 'Privacy'),
    h('h2', { class: 'left' }, 'The short version'),
    h('p', {}, 'Sound Out works completely offline. It has no account, no login, no ads, no analytics and no tracking. Everything a learner does stays on this phone. The developer never sees it.'),
    h('h2', { class: 'left' }, 'What the app stores on this phone'),
    h('table', { class: 'mastery' }, ...ROWS.map(([a, b]) => h('tr', {}, h('td', {}, a), h('td', { class: 'muted' }, b)))),
    h('p', {}, 'The app never asks for a real name, an email, an age or a birthday. Words typed in a writing exercise are compared on screen and not saved.'),
    h('h2', { class: 'left' }, 'What the app does not do'),
    h('p', {}, 'It does not use the internet, show ads, record or listen to anyone, or ask for the microphone, camera, location, contacts or files. Deleting the app deletes everything.'),
    h('h2', { class: 'left' }, 'Full policy'),
    h('p', {}, 'The full privacy policy is at this address (type it into a browser):'),
    h('p', { class: 'url' }, 'oyekamal.github.io/sound-out/privacy.html'));
  app.mount(s);
  return s;
}
