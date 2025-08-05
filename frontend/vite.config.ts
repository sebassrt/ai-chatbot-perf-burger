import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/',
  build: {
    outDir: 'dist',
    assetsDir: '',
    target: 'es2015',
    minify: true,
    lib: {
      entry: 'src/main.tsx',
      name: 'PerfBurgerApp',
      formats: ['umd'],
      fileName: 'perfburger-app'
    },
    rollupOptions: {
      external: [],
      output: {
        globals: {}
      }
    }
  }
})
