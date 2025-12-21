export default defineNuxtPlugin((nuxtApp) => {
  const { baseURL } = useBaseUrlApi()

  const api = $fetch.create({
    baseURL,
    headers: {
      'Content-Type': 'application/json',
    },

    onRequest({ options }) {
      const token = process.client ? useCookie('token')?.value : null
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
