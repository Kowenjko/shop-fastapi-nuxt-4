<script setup lang="ts">
const { isActive, name, count } = defineProps<{ isActive: boolean; name: string; count: number }>()

const emit = defineEmits<{ selectCategory: [] }>()
const selectCategory = () => emit('selectCategory')
</script>

<template>
  <button
    @click="selectCategory"
    :class="[
      'w-full cursor-pointer rounded-lg px-4 py-3 text-left transition-all duration-200',
      isActive ? 'bg-black font-semibold text-white' : 'bg-gray-50 text-gray-700 hover:bg-gray-100',
    ]"
  >
    {{ name }}
    <span v-if="isActive" class="float-right"> ({{ count }}) </span>
  </button>
</template>
