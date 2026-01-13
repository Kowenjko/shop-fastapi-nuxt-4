<script lang="ts" setup>
const cartStore = useCartStore()
</script>

<template>
  <div class="mb-8 space-y-6">
    <div class="flex justify-between text-lg text-gray-600">
      <span>Items ({{ cartStore.cartDetails?.items_count }})</span>
      <span>${{ cartStore.totalPrice.toFixed(2) }}</span>
    </div>

    <div class="flex justify-between text-lg text-gray-600">
      <span>Shipping</span>
      <span class="font-medium text-green-600">Free</span>
    </div>

    <div class="border-t border-gray-300 pt-6">
      <div class="flex justify-between text-xl font-bold text-black">
        <span>Total</span>
        <span>${{ cartStore.totalPrice.toFixed(2) }}</span>
      </div>
    </div>
  </div>
</template>
