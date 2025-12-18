<script setup lang="ts">
const {
  text = "",
  badge,
  to,
} = defineProps<{
  to: string | { name: string };
  text?: string;
  badge?: number;
}>();
</script>

<template>
  <nuxt-link
    :to
    class="relative flex items-center space-x-2 font-medium text-gray-700 transition-colors hover:text-black"
  >
    <slot />

    <span v-if="text">{{ text }}</span>

    <span
      v-if="badge && badge > 0"
      class="absolute -top-2 -right-2 flex h-5 w-5 items-center justify-center rounded-full bg-black text-xs font-bold text-white"
    >
      {{ badge }}
    </span>
  </nuxt-link>
</template>
