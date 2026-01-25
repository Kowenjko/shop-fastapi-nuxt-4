export const postAPI = {
  async create(body: PostCreateI) {
    const { $api } = useNuxtApp()
    return await $api<PostI>(BASE_API + POSTS, { method: 'POST', body })
  },

  async update(body: PostCreateI, postId: number) {
    const { $api } = useNuxtApp()
    return await $api<PostsI>(BASE_API + POSTS + postId + '/', { method: 'PUT', body })
  },

  async remove(postId: number) {
    const { $api } = useNuxtApp()
    return await $api(BASE_API + POSTS + postId + '/', { method: 'DELETE' })
  },
}
