<script lang="ts" setup></script>

<template>
  <header class="sticky top-0 z-50 border-b-2 border-black bg-white">
    <div class="mx-auto max-w-7xl px-4">
      <div class="flex h-20 items-center justify-between">
        <nuxt-link to="/" class="group flex items-center space-x-2">
          <IconCart
            class="h-8 w-8 transition-transform group-hover:scale-110"
          />
          <span class="text-2xl font-bold text-black">FastAPI Shop</span>
        </nuxt-link>
        <!-- Навигация -->
        <nav class="flex items-center space-x-8">
          <nuxt-link
            to="/"
            class="relative flex items-center space-x-2 font-medium text-gray-700 transition-colors hover:text-black"
            activeClass="text-semibold !text-black"
            exactActiveClass="text-semibold !text-black"
          >
            About
          </nuxt-link>

          <!-- Корзина -->
          <nuxt-link
            to="/"
            class="relative flex items-center space-x-2 font-medium text-gray-700 transition-colors hover:text-black"
          >
            <IconCart class="h-6 w-6" />
            <span
              class="absolute -top-2 -right-2 flex h-5 w-5 items-center justify-center rounded-full bg-black text-xs font-bold text-white"
            >
              10
            </span>
          </nuxt-link>
        </nav>
      </div>
    </div>
  </header>
</template>
