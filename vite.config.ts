import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Project site: https://iphios-cmd.github.io/miniapprevener/
export default defineConfig({
  plugins: [react()],
  base: '/miniapprevener/',
})
