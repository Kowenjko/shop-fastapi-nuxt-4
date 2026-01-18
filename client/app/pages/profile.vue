<script lang="ts" setup>
const authStore = useAuthStore()

definePageMeta({
  layout: 'profile',
  middleware: ['auth'],
})
</script>

<template>
  <div class="h-screen bg-white">
    <div class="mx-auto max-w-7xl px-4 pt-12 sm:px-6 lg:px-8">
      <TitlePage title="Profile" description="This is an profile page" />
    </div>
  </div>
</template>
