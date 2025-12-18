<script lang="ts" setup>
const { title = "", description = "" } = defineProps<{
  title: string;
  description: string;
}>();
</script>

<template>
  <div class="mb-8">
    <h1 class="mb-2 text-4xl font-extrabold text-black">{{ title }}</h1>
    <p v-if="description" class="text-gray-500">{{ description }}</p>
  </div>
</template>
