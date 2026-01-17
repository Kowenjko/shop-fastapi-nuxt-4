export default defineNuxtRouteMiddleware(async () => {
  const authStore = useAuthStore()

  const { refresh } = useAuth()

  if (authStore.isAuthenticated) return

  try {
    const response = await refresh()
    if (!response) await navigateTo(HOME_LINK)
  } catch {
    await navigateTo(HOME_LINK)
  }
})
