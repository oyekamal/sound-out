// Capacitor shell glue. Does nothing in a normal browser (Pages build): only runs inside the Android app.
import { Capacitor } from '@capacitor/core';

export async function initNative(app) {
  if (!Capacitor.isNativePlatform()) return;
  const [{ App }, { StatusBar, Style }] = await Promise.all([import('@capacitor/app'), import('@capacitor/status-bar')]);
  StatusBar.setStyle({ style: Style.Light }).catch(() => {});
  StatusBar.setBackgroundColor({ color: '#f6f1e7' }).catch(() => {});
  // Back button: on Home (or the first-run welcome) leave the app; anywhere else go back to Home.
  App.addListener('backButton', () => {
    const el = document.getElementById('app');
    if (el.querySelector('.home')) return App.exitApp();
    if (el.querySelector('.privacy') || document.querySelector('.gu-wrap')) return app.home();
    if (el.querySelector('.onboard')) return el.querySelector('.existing') ? app.boot() : App.exitApp();
    app.home();   // the For grown-ups screen and the grown-up gate also go Home
  });
}
