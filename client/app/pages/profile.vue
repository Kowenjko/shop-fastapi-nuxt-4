<script lang="ts" setup>
const showEdit = ref(false)

definePageMeta({
  layout: 'profile',
  middleware: ['auth'],
})
</script>

<template>
  <div class="h-screen bg-white">
    <div class="mx-auto max-w-7xl pt-12 pl-4 sm:pl-6 lg:pl-8">
      <TitlePage title="Profile" description="This is an profile page" />

      <ClientOnly>
        <ProfileCard v-if="!showEdit" v-model="showEdit" />
        <ProfileEditCard v-if="showEdit" v-model="showEdit" />
      </ClientOnly>
    </div>
  </div>
</template>
