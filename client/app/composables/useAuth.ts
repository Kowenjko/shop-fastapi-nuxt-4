import { authAPI } from '@/api'

export const useAuth = () => {
  const loading = ref(false)
  const authStore = useAuthStore()

  const authAction = async <T>(action: () => Promise<T>) => {
    loading.value = true
    try {
      const response = await action()
      //@ts-ignore
      response?.access_token ? authStore.setToken(response.access_token) : authStore.setToken(null)

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

  return { loading, login, register, refresh, logout }
}
