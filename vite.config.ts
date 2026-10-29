import { defineConfig } from 'vite';

export default defineConfig({
  base: './',
  build: {
    outDir: process.env.OUT_DIR || 'dist',
    sourcemap: false,
    rollupOptions: {
      maxParallelFileOps: 128,
    },
  },
});
