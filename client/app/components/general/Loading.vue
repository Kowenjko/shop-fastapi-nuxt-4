<script lang="ts" setup>
const { text = "Loading products..." } = defineProps<{ text?: string }>();
</script>

<template>
  <div class="py-12 text-center">
    <div
      class="inline-block h-12 w-12 animate-spin rounded-none border-b-2 border-black"
    ></div>
    <p class="mt-4 text-gray-500">{{ text }}</p>
  </div>
</template>
