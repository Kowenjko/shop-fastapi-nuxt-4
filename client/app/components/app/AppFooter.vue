<script lang="ts" setup>
const nowDate = new Date()
</script>

<template>
  <footer class="border-t-2 border-black bg-white">
    <div class="mx-auto max-w-7xl px-4 py-8">
      <div class="text-center text-gray-600">
        <p class="mb-2">© {{ nowDate.getFullYear() }} FastAPI Shop. All rights reserved.</p>
        <p class="text-sm">FastAPI + Nuxt 4</p>
      </div>
    </div>
  </footer>
</template>
