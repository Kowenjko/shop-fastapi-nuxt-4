<script lang="ts" setup>
const cartStore = useCartStore()
</script>

<template>
  <header class="sticky top-0 z-50 border-b-2 border-black bg-white">
    <div class="mx-auto max-w-7xl px-4">
      <div class="flex h-20 items-center justify-between">
        <nuxt-link :to="HOME_LINK" class="group flex items-center space-x-2">
          <IconCart class="h-8 w-8 transition-transform group-hover:scale-110" />
          <span class="text-2xl font-bold text-black">FastAPI Shop</span>
        </nuxt-link>
        <!-- Навигация -->
        <nav class="flex items-center space-x-8">
          <nuxt-link
            :to="ABOUT_LINK"
            class="relative flex items-center space-x-2 font-medium text-gray-700 transition-colors hover:text-black"
            activeClass="text-semibold !text-black"
            exactActiveClass="text-semibold !text-black"
          >
            About
          </nuxt-link>

          <!-- Корзина -->
          <button-link
            text="Cart"
            :to="CART_LINK"
            class="relative flex items-center space-x-2 font-medium text-gray-700 transition-colors hover:text-black"
            :badge="cartStore.itemsCount"
          >
            <IconCart class="h-6 w-6" />
          </button-link>
        </nav>
      </div>
    </div>
  </header>
</template>
