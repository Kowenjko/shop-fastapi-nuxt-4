<script lang="ts" setup>
import { CirclePlusIcon, PencilIcon, Trash2Icon } from 'lucide-vue-next'

import { postAPI } from '@/api'

const modalStore = useModalStore()

const { data: posts, refresh } = await useAPI<PostsI>(POSTS, { key: 'posts' })

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

definePageMeta({
  layout: 'profile',
  middleware: ['auth'],
})
</script>

<template>
  <main class="relative min-h-screen bg-white">
    <Button @click="modalStore.modalPost.show = true" class="absolute top-4 right-4" variant="outline">
      <CirclePlusIcon /> Create
    </Button>
    <div class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <TitlePage title="Posts" description="This is an post page" />

      <div v-if="posts?.items && posts.items.length > 0" class="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <Card class="mt-8 space-y-6" v-for="post in posts?.items" :key="post.id">
          <CardHeader>
            <CardTitle>{{ post.title }}</CardTitle>
          </CardHeader>
          <CardContent>
            <p class="text-wrap">{{ post.content }}</p>
          </CardContent>
          <CardFooter class="flex justify-between gap-2">
            <ul>
              <li>
                <span class="text-sm text-gray-500"><strong>User:</strong> {{ post.user.username }}</span>
              </li>
            </ul>
            <div class="space-x-2">
              <Button @click="updatePost(post)" size="icon" variant="outline"><PencilIcon /> </Button>
              <Button @click="deletePost(post.id)" size="icon" variant="destructive"><Trash2Icon /> </Button>
            </div>
          </CardFooter>
        </Card>
      </div>

      <div v-else>
        <p>No posts</p>
      </div>
    </div>
  </main>
</template>
