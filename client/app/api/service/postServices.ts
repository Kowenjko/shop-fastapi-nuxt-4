export const postAPI = {
  async create(body: PostCreateI) {
    const { $api } = useNuxtApp()
    return await $api<PostI>(POSTS, { method: 'POST', body })
  },

  async update(body: PostCreateI, postId: number) {
    const { $api } = useNuxtApp()
    return await $api<PostsI>(POSTS + postId + '/', { method: 'PUT', body })
  },

  async remove(postId: number) {
    const { $api } = useNuxtApp()
    return await $api(POSTS + postId + '/', { method: 'DELETE' })
  },
}
