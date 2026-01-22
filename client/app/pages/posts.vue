<script lang="ts" setup>
import { CirclePlusIcon } from 'lucide-vue-next'

import PostCard from '~/components/widgets/post/PostCard.vue'

const modalStore = useModalStore()
const { posts, deletePost, updatePost } = await usePost()

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
        <PostCard
          v-for="post in posts?.items"
          :key="post.id"
          :post="post"
          @delete-post="deletePost(post.id)"
          @update-post="updatePost(post)"
        />
      </div>

      <div v-else>
        <p>No posts</p>
      </div>
    </div>
  </main>
</template>
