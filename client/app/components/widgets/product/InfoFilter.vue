<script lang="ts" setup>
const { productsCount, selectedCategory } = defineProps<{
  productsCount: number
  selectedCategory: number | null
}>()

const emit = defineEmits<{ clearFilter: [] }>()

const clearFilter = () => emit('clearFilter')
</script>

<template>
  <div class="mb-6 flex items-center justify-between">
    <p class="text-gray-700">
      <span class="font-bold">{{ productsCount }}</span>
      {{ productsCount === 1 ? 'product' : 'products' }} found
    </p>

    <!-- Кнопка сброса фильтра -->
    <button
      v-if="selectedCategory"
      @click="clearFilter"
      class="cursor-pointer text-sm font-medium text-gray-500 transition-colors hover:text-black"
    >
      Clear filter
    </button>
  </div>
</template>
