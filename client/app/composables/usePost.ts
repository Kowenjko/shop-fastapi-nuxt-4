import { postAPI } from '@/api'

export const usePost = async () => {
  const modalStore = useModalStore()

  const { data: posts, refresh } = await useAPI<PostsI>(BASE_API + POSTS, { key: 'posts' })

  const deletePost = async (postId: number) => {
    try {
      await postAPI.remove(postId)

      await refresh()
    } catch (error) {
      console.error('Error deleting post:', error)
    }
  }

  const updatePost = (post: PostI) => {
    modalStore.modalPost.show = true
    //@ts-ignore
    modalStore.modalPost.content = post
  }

  watch(
    () => modalStore.modalPost.show,
    async (newVal) => {
      if (!newVal) {
        await refresh()
      }
    },
  )

  return { posts, deletePost, updatePost }
}
