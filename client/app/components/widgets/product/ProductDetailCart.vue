<script lang="ts" setup>
const {
  product,
  adding = false,
  showNotification = false,
} = defineProps<{
  product: ProductI
  adding?: boolean
  showNotification?: boolean
}>()

const emit = defineEmits<{ addToCart: [] }>()

const addToCart = () => emit('addToCart')
</script>

<template>
  <div class="overflow-hidden rounded-none border-2 border-gray-100 bg-white shadow-sm">
    <div class="grid grid-cols-1 gap-8 p-8 md:grid-cols-2">
      <!-- Изображение -->
      <div class="aspect-square overflow-hidden rounded-none bg-gray-50">
        <nuxt-img
          :src="product.image_url"
          :alt="product.name"
          class="h-full w-full object-cover"
          @error="noImage()"
          placeholder
          width="262"
          height="262"
          format="webp"
        />
      </div>

      <!-- Информация -->
      <div class="flex flex-col">
        <!-- Категория -->
        <div class="mb-3 text-sm font-medium tracking-wider text-gray-500 uppercase">
          {{ product.category.name }}
        </div>

        <!-- Название -->
        <h1 class="mb-4 text-3xl font-extrabold text-black sm:text-4xl">
          {{ product.name }}
        </h1>

        <!-- Цена -->
        <div class="mb-6 text-2xl font-bold text-black sm:text-3xl">${{ product.price.toFixed(2) }}</div>

        <!-- Описание -->
        <div class="mb-8">
          <h2 class="mb-3 text-xl font-bold text-black">Description</h2>
          <p class="leading-relaxed text-gray-600">
            {{ product.description || 'No description available.' }}
          </p>
        </div>

        <!-- Кнопка добавления в корзину -->
        <div class="mt-auto">
          <button
            @click="addToCart"
            :disabled="adding"
            class="w-full rounded-none bg-black px-6 py-4 text-lg font-semibold text-white transition-colors hover:bg-gray-900 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {{ adding ? 'Adding to cart...' : 'Add to Cart' }}
          </button>

          <!-- Уведомление об успешном добавлении -->
          <transition name="fade">
            <div
              v-if="showNotification"
              class="mt-4 rounded-none bg-black px-4 py-3 text-center font-medium text-white"
            >
              ✓ Product added to cart!
            </div>
          </transition>
        </div>

        <!-- Дополнительная информация -->
        <div class="mt-8 border-t-2 border-gray-100 pt-6">
          <p class="text-sm text-gray-500">Product ID: {{ product.id }}</p>
          <p class="text-sm text-gray-500">Added: {{ formatDate(product.created_at) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
