<script lang="ts" setup>
import { ShoppingCartIcon } from 'lucide-vue-next'
</script>
<template>
  <div class="py-16 text-center">
    <ShoppingCartIcon class="mx-auto mb-6 h-28 w-28 text-gray-300" />

    <h2 class="mb-3 text-2xl font-bold text-black">Your cart is empty</h2>
    <p class="mb-8 text-lg text-gray-500">Add some products to get started!</p>

    <Button as-child>
      <router-link :to="HOME_LINK"> View all products </router-link>
    </Button>
  </div>
</template>
