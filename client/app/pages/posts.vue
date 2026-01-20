<script lang="ts" setup>
definePageMeta({
  layout: 'profile',
  middleware: ['auth'],
})
</script>

<template>
  <div class="min-h-screen bg-white">
    <div class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <TitlePage title="Posts" description="This is an post page" />
    </div>
  </div>
</template>
