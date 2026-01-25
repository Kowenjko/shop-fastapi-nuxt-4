export const authAPI = {
  async login(body: LoginI): Promise<AuthI> {
    const { $api } = useNuxtApp()
    return await $api<AuthI>(BASE_API + AUTH + LOGIN, {
      method: 'POST',
      //@ts-ignore
      body: new URLSearchParams(body),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      credentials: 'include',
    })
  },

  async register(body: RegisterI): Promise<UserI> {
    const { $api } = useNuxtApp()
    return await $api<UserI>(BASE_API + AUTH + REGISTER, { method: 'POST', body })
  },

  async refresh(): Promise<AuthI> {
    const { $api } = useNuxtApp()
    return await $api<AuthI>(BASE_API + AUTH + REFRESH, { method: 'POST', credentials: 'include' })
  },
  async logout() {
    const { $api } = useNuxtApp()
    return await $api(BASE_API + AUTH + LOGOUT, { method: 'POST' })
  },
}
