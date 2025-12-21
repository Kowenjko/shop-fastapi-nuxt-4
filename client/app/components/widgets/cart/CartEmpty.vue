<template>
  <div class="py-16 text-center">
    <IconCart class="mx-auto mb-6 h-28 w-28 text-gray-300" />

    <h2 class="mb-3 text-2xl font-bold text-black">Your cart is empty</h2>
    <p class="mb-8 text-lg text-gray-500">Add some products to get started!</p>
    <router-link
      :to="HOME_LINK"
      class="inline-block rounded-none bg-black px-8 py-3 text-lg font-semibold text-white transition-colors hover:bg-gray-900"
    >
      Continue Shopping
    </router-link>
  </div>
</template>
