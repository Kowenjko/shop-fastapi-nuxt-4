import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  const setToken = (newToken: string | null) => (token.value = newToken)
  return { token, isAuthenticated, setToken }
})
