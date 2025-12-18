<script lang="ts" setup>
const emit = defineEmits<{ proceed: []; clear: [] }>();

const proceed = () => emit("proceed");
const clear = () => emit("clear");
</script>

<template>
  <button
    class="mb-4 w-full rounded-none bg-black px-6 py-4 text-lg font-semibold text-white transition-colors hover:bg-gray-900"
    @click="proceed"
  >
    Proceed to Checkout
  </button>

  <router-link
    to="/"
    class="block w-full rounded-none bg-gray-100 px-6 py-4 text-center text-lg font-semibold text-black transition-colors hover:bg-gray-200"
  >
    Continue Shopping
  </router-link>

  <button
    @click="clear"
    class="mt-6 w-full text-base font-medium text-red-600 transition-colors hover:text-red-700"
  >
    Clear Cart
  </button>
</template>
