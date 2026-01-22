<script lang="ts" setup>
import { PencilIcon, Trash2Icon } from 'lucide-vue-next'

const { post } = defineProps<{
  post: PostI
}>()

const emit = defineEmits<{
  deletePost: []
  updatePost: []
}>()
</script>

<template>
  <Card class="mt-8 space-y-6">
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
        <Button @click="emit('updatePost')" size="icon" variant="outline"><PencilIcon /> </Button>
        <Button @click="emit('deletePost')" size="icon" variant="destructive"><Trash2Icon /> </Button>
      </div>
    </CardFooter>
  </Card>
</template>
