// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  ssr: true,
  css: ['./app/assets/css/main.css'],
  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
  ],
  imports: {
    dirs: ['~/composables/**'],
  },
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_API_BASE_URL,
      apiBaseUrlServer: process.env.NUXT_API_URL_SERVER,
    },
  },

  vite: {
    plugins: [tailwindcss()],
  },

  modules: ['@vueuse/nuxt', '@pinia/nuxt', 'nuxt-typed-router', '@nuxt/image'],
})
