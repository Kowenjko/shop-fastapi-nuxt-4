export const profileAPI = {
  async update(body: Partial<ProfileI>): Promise<ProfileI> {
    const { $api } = useNuxtApp()
    return await $api<ProfileI>(BASE_API + PROFILE, { method: 'PUT', body })
  },
}
