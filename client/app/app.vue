<script lang="ts" setup>
import 'vue-sonner/style.css'
import { Toaster } from '@/components/ui/sonner'

useHead({
  titleTemplate: (titleChunk) => {
    return titleChunk ? `${titleChunk} - FastAPI Shop` : 'FastAPI Shop'
  },
})
</script>

<template>
  <Suspense>
    <NuxtLayout>
      <NuxtPage />
      <ClientOnly>
        <Toaster position="top-right" />
      </ClientOnly>
    </NuxtLayout>
  </Suspense>
</template>
