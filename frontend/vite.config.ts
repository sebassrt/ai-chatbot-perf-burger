import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react({
    jsxRuntime: 'classic'
  })],
  base: '/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    target: 'es2015',
    rollupOptions: {
      input: {
        main: 'src/main.tsx'
      },
      output: {
        manualChunks: undefined,
        format: 'iife',
        inlineDynamicImports: true,
        name: 'PerfBurgerApp',
        entryFileNames: 'assets/[name]-[hash].js'
      },
    },
  },
  esbuild: {
    jsxFactory: 'React.createElement',
    jsxFragment: 'React.Fragment'
  }
})
