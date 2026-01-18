import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const profile = ref<ProfileI | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  const setToken = (newToken: string | null) => (token.value = newToken)

  const upperCaseName = computed(() => {
    if (!profile.value) return ''

    return [profile.value?.first_name, profile.value?.last_name].map((n) => n?.[0]?.toUpperCase() ?? '').join('')
  })
  return { token, profile, isAuthenticated, setToken, upperCaseName }
})
