<script lang="ts" setup>
const emit = defineEmits<{ proceed: []; clear: [] }>()

const proceed = () => emit('proceed')
const clear = () => emit('clear')
</script>

<template>
  <div class="space-y-2">
    <Button @click="proceed" size="lg" class="w-full"> Create Order </Button>

    <Button @click="navigateTo(HOME_LINK)" size="lg" variant="secondary" class="w-full"> Continue Shopping </Button>

    <Button @click="clear" size="lg" variant="destructive" class="w-full"> Clear Cart </Button>
  </div>
</template>
