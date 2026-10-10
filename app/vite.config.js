import { defineConfig } from 'vite';
// Production builds only (the dev server needs ws: for hot reload): a Content-Security-Policy that blocks every outside address.
const CSP = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; media-src 'self' blob:; font-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'";
// content/ (lessons, lexicon, options, audio index) lives one level up and is imported as JSON
export default defineConfig(({ command }) => ({
  server: { port: 5317, strictPort: true, fs: { allow: ['..'] } },
  build: { outDir: 'dist' },
  plugins: [{
    name: 'csp',
    transformIndexHtml: html => command === 'build' ? html.replace('</title>', `</title>\n  <meta http-equiv="Content-Security-Policy" content="${CSP}" />`) : html,
  }],
}));
