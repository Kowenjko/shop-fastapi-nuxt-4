<script lang="ts" setup>
const { quantity, updating } = defineProps<{ quantity: number; updating: boolean }>()

const emit = defineEmits<{ minus: []; plus: []; remove: [] }>()

const minus = () => emit('minus')
const plus = () => emit('plus')
const remove = () => emit('remove')
</script>

<template>
  <div class="flex items-center gap-4">
    <div class="flex items-center rounded-none border-2 border-gray-100 text-black">
      <button
        @click="minus"
        :disabled="updating"
        class="px-3 py-2 transition-colors hover:bg-gray-100 disabled:opacity-50"
      >
        <IconMinus class="h-5 w-5" />
      </button>

      <span class="min-w-10 px-4 py-2 text-center font-medium">
        {{ quantity }}
      </span>

      <button
        @click="plus"
        :disabled="updating"
        class="px-3 py-2 transition-colors hover:bg-gray-100 disabled:opacity-50"
      >
        <IconPlus class="h-5 w-5" />
      </button>
    </div>

    <!-- Кнопка удаления -->
    <button
      @click="remove"
      :disabled="updating"
      class="text-red-600 transition-colors hover:text-red-700 disabled:opacity-50"
    >
      <IconTrash class="h-6 w-6" />
    </button>
  </div>
</template>
