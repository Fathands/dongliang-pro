import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/gateway': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true, // 是否跨域
        secure: false, // 如果是https接口，需要配置这个参数为true`
        rewrite: (path) => path.replace(/^\/gateway/, '') // 不可以省略rewrite
      }
    }
  }
})
