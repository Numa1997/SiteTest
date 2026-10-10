import { defineConfig } from 'vite';

export default defineConfig({
  base: './',
  // static assets live at the repository root so GitHub Pages can serve them as-is
  publicDir: false,
  build: {
    outDir: process.env.APPDEPLOY_VITE_OUT_DIR || 'dist',
    sourcemap:
      process.env.APPDEPLOY_VITE_SOURCEMAP === 'hidden' ? 'hidden' : false,
    rollupOptions: {
      maxParallelFileOps: 128,
    },
  },
});
