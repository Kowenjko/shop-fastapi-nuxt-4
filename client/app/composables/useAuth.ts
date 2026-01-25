import { authAPI } from '@/api'

export const useAuth = () => {
  const loading = ref(false)
  const authStore = useAuthStore()
  const { baseURL } = useBaseUrlApi()
  const { $api } = useNuxtApp()

  const authAction = async <T>(action: () => Promise<T>) => {
    loading.value = true
    try {
      const response = await action()

      //@ts-ignore
      if (response?.access_token) {
        // @ts-ignore
        authStore.setToken(response.access_token)
        const data = await $api<ProfileI>(BASE_API + PROFILE)
        if (data) authStore.profile = data
      } else authStore.setToken(null)

      return response
    } catch (error) {
      authStore.setToken(null)

      console.log(error)
      await navigateTo(HOME_LINK)
    } finally {
      loading.value = false
    }
  }

  const login = (body: LoginI) => authAction(() => authAPI.login(body))
  const register = (body: RegisterI) => authAction(() => authAPI.register(body))
  const refresh = () => authAction(() => authAPI.refresh())
  const logout = () => authAction(() => authAPI.logout())

  const loginByProvider = async (provider: typeof GITHUB | typeof GOOGLE) =>
    navigateTo(baseURL + AUTH + provider + LOGIN, { external: true })

  return { loading, login, register, refresh, logout, loginByProvider }
}
