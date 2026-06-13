import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig(({ mode }) => ({
  base: '/',
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  // 生产环境构建优化
  build: {
    outDir: 'dist',
    assetsDir: 'static',
    // 启用 gzip 压缩提示
    reportCompressedSize: true,
    // chunk 大小警告阈值
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        // 分割第三方库
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router'],
          'element-plus': ['element-plus'],
          'echarts': ['echarts'],
          'marked': ['marked'],
          'spark-md5': ['spark-md5'],
        }
      }
    },
    // 生产环境移除 console（使用 esbuild minify，避免 terser 兼容性问题）
    minify: 'esbuild',
  },
  // 生产环境禁用 sourcemap
  ...(mode === 'production' && {
    sourcemap: false,
  }),
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8016',
        changeOrigin: true
      }
    }
  }
}))
