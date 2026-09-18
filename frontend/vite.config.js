import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

// /api는 FastAPI로 프록시, PWA 매니페스트 포함
export default defineConfig({
  plugins: [vue(), VitePWA({ registerType: 'autoUpdate', manifest: { name: 'NEXTO', short_name: 'NEXTO', theme_color: '#3b4fbf', display: 'standalone' } })],
  server: { port: 5173, proxy: { '/api': { target: process.env.VITE_API_URL || 'http://localhost:8000', changeOrigin: true } } }
})
