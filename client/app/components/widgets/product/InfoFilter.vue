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

    <Button variant="ghost" v-if="selectedCategory" @click="clearFilter"> Clear filter </Button>
  </div>
</template>
