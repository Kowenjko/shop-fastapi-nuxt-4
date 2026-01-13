<script lang="ts" setup>
import { ShoppingCartIcon } from 'lucide-vue-next'

const emit = defineEmits<{ clearFilter: [] }>()

const clearFilter = () => emit('clearFilter')
</script>

<template>
  <div class="py-12 text-center">
    <ShoppingCartIcon class="mx-auto mb-6 h-28 w-28 text-gray-300" />
    <p class="text-lg font-medium text-gray-500">No products found</p>
    <Button class="mt-4" @click="clearFilter">View all products</Button>
  </div>
</template>
