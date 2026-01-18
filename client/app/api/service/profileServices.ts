export const profileAPI = {
  async update(body: Partial<ProfileI>): Promise<ProfileI> {
    const { $api } = useNuxtApp()
    return await $api<ProfileI>(PROFILE, { method: 'PUT', body })
  },
}
