import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'https://rcs.fenqile.com',
        headers: {
          referer: 'https://rcs.fenqile.com'
        },
        changeOrigin: true, // 是否跨域
        secure: false, // 如果是https接口，需要配置这个参数为true`
        rewrite: (path) => path.replace(/^\/api/, '') // 不可以省略rewrite
      }
    }
  }
})
