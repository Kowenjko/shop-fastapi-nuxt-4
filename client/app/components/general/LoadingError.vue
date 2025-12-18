<script lang="ts" setup>
const {
  error,
  isButtonBack = false,
  to = null,
} = defineProps<{
  error: string;
  isButtonBack?: boolean;
  to?: string | { name: string } | null;
}>();
</script>

<template>
  <div class="py-16 text-center" v-if="isButtonBack && to">
    <p class="pb-2 text-lg font-medium text-red-600">{{ error }}</p>
    <router-link
      v-if="isButtonBack && to"
      :to
      class="mt-6 rounded-none bg-black px-8 py-3 text-lg font-semibold text-white transition-colors hover:bg-gray-900"
    >
      Return to catalog
    </router-link>
  </div>
  <div class="py-12 text-center" v-else>
    <p class="font-medium text-red-600">{{ error }}</p>
    {{ String(isButtonBack) }}
  </div>
</template>
