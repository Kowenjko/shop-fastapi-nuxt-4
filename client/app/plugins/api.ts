import { defineNuxtPlugin } from '#app'
import { useAuthStore } from '@/stores/auth'

export default defineNuxtPlugin((nuxtApp) => {
  const { baseURL } = useBaseUrlApi()

  //@ts-ignore
  const authStore = useAuthStore(nuxtApp.$pinia)

  const api = $fetch.create({
    baseURL,
    headers: {
      'Content-Type': 'application/json',
    },

    onRequest({ options }) {
      const token = process.client ? authStore.token : null
      if (token) options.headers.set('Authorization', `Bearer ${token}`)
    },

    async onResponseError({ response }) {
      if (process.client) {
        const errorsStore = useErrorsStore()
        errorsStore.setErrors(response._data)
      }
      if (response.status === 401) await nuxtApp.runWithContext(() => navigateTo('/'))
      throw response._data
    },
  })

  return {
    provide: { api },
  }
})
