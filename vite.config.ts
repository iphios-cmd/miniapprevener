import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
// relative base — удобно для GitHub Pages (project site)
export default defineConfig({
  plugins: [react()],
  base: './',
})
