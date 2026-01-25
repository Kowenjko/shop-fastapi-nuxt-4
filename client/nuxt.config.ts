// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  ssr: false,
  css: ['./app/assets/css/main.css'],

  nitro: {
    preset: 'node-server',
    externals: {
      inline: ['vue', '@vue/server-renderer'],
    },
  },
  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
  ],
  image: {
    format: ['webp'],
  },
  imports: {
    dirs: ['~/composables/**'],
  },
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_API_BASE_URL || 'http://localhost:8000',
      apiBaseUrlServer: process.env.NUXT_API_URL_SERVER || 'http://localhost:8000',
    },
  },

  vite: {
    plugins: [tailwindcss()],
  },
  shadcn: {
    prefix: '',
    componentDir: './app/components/ui',
  },

  modules: ['@vueuse/nuxt', '@pinia/nuxt', '@nuxt/image', 'pinia-plugin-persistedstate/nuxt', 'shadcn-nuxt'],
})
