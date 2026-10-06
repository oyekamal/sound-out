import { defineConfig } from 'vite';
// content/ (lessons, lexicon, options, audio index) lives one level up and is imported as JSON
export default defineConfig({
  server: { port: 5317, strictPort: true, fs: { allow: ['..'] } },
  build: { outDir: 'dist' },
});
