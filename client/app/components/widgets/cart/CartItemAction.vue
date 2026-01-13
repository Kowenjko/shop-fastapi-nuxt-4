<script lang="ts" setup>
import { MinusIcon, PlusIcon, Trash2Icon } from 'lucide-vue-next'

const { quantity, updating } = defineProps<{ quantity: number; updating: boolean }>()

const emit = defineEmits<{ minus: []; plus: []; remove: [] }>()

const minus = () => emit('minus')
const plus = () => emit('plus')
const remove = () => emit('remove')
</script>

<template>
  <div class="flex items-center gap-2">
    <div class="flex items-center rounded-none border-2 border-gray-100 text-black">
      <Button @click="minus" :disabled="updating" variant="ghost" size="icon">
        <MinusIcon class="h-5 w-5" />
      </Button>

      <span class="min-w-10 px-4 py-2 text-center font-medium">
        {{ quantity }}
      </span>

      <Button @click="plus" :disabled="updating" variant="ghost" size="icon">
        <PlusIcon class="h-5 w-5" />
      </Button>
    </div>

    <!-- Кнопка удаления -->
    <Button @click="remove" :disabled="updating" variant="ghost" size="icon">
      <Trash2Icon class="h-6 w-6 text-red-500" />
    </Button>
  </div>
</template>
