<script lang="ts" setup>
const emit = defineEmits<{ clearFilter: [] }>();

const clearFilter = () => emit("clearFilter");
</script>

<template>
  <div class="py-12 text-center">
    <IconNoProductFound />
    <p class="text-lg font-medium text-gray-500">No products found</p>
    <button
      @click="clearFilter"
      class="mt-4 font-medium text-black hover:underline"
    >
      View all products
    </button>
  </div>
</template>
