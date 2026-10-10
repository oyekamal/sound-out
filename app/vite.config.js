import { defineConfig } from 'vite';
import { rmSync } from 'node:fs';
import { join, resolve } from 'node:path';
// Review and demo pages that live in public/ for the dev server and the review tools. They never ship: a build removes them from the output.
let out = '';
const REVIEW_ONLY = ['compare.html', 'listen.html', 'voices.html', 'tilo-demo.html', 'compare', 'audition', 'compare-data.json', 'listen-data.json', 'voices-data.json'];
// Production builds only (the dev server needs ws: for hot reload): a Content-Security-Policy that blocks every outside address.
const CSP = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; media-src 'self' blob:; font-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'";
// content/ (lessons, lexicon, options, audio index) lives one level up and is imported as JSON
export default defineConfig(({ command }) => ({
  server: { port: 5317, strictPort: true, fs: { allow: ['..'] } },
  build: { outDir: 'dist' },
  plugins: [{
    name: 'drop-review-pages',
    apply: 'build',
    configResolved(c) { out = resolve(c.root, c.build.outDir); },
    closeBundle() { for (const f of REVIEW_ONLY) rmSync(join(out, f), { recursive: true, force: true }); },
  }, {
    name: 'csp',
    transformIndexHtml: html => command === 'build' ? html.replace('</title>', `</title>\n  <meta http-equiv="Content-Security-Policy" content="${CSP}" />`) : html,
  }],
}));
