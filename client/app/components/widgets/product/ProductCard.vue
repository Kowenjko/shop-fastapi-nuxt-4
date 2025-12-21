<script lang="ts" setup>
import { ref } from 'vue'

const { product } = defineProps<{ product: ProductI }>()

const cartStore = useCartStore()
const adding = ref(false)
const showNotification = ref(false)

const handleAddToCart = async () => {
  adding.value = true
  // const success = await cartStore.addToCart(product.id, 1);

  // if (success) {
  //   showNotification.value = true;
  //   setTimeout(() => {
  //     showNotification.value = false;
  //   }, 2000);
  // }

  adding.value = false
}
</script>

<template>
  <div
    class="overflow-hidden rounded-lg border-2 border-gray-200 bg-white transition-all duration-300 hover:border-black hover:shadow-lg"
  >
    <!-- Изображение товара -->
    <router-link :to="{ ...PRODUCT_DETAIL_LINK, params: { id: product.id } }">
      <div class="aspect-square overflow-hidden bg-gray-100">
        <nuxt-img
          v-if="product.image_url"
          :src="product.image_url"
          :alt="product.name"
          class="h-full w-full object-cover transition-transform duration-300 hover:scale-105"
          placeholder
          width="262"
          height="262"
          format="webp"
        />
        <nuxt-img v-else :src="noImage()" alt="No image" placeholder width="262" height="262" format="webp" />
      </div>
    </router-link>

    <!-- Информация о товаре -->
    <div class="p-4">
      <!-- Категория -->
      <div class="mb-2 text-xs tracking-wide text-gray-500 uppercase">
        {{ product.category.name }}
      </div>

      <!-- Название товара -->
      <router-link :to="{ ...PRODUCT_DETAIL_LINK, params: { id: product.id } }">
        <h3 class="mb-2 text-lg font-semibold text-black transition-colors hover:text-gray-700">
          {{ product.name }}
        </h3>
      </router-link>

      <!-- Цена -->
      <p class="mb-4 text-2xl font-bold text-black">${{ product.price.toFixed(2) }}</p>

      <Button
        @on-click="handleAddToCart"
        :disabled="adding"
        :text="adding ? 'Adding...' : 'Add to Cart'"
        :is-show-transition="showNotification"
        text-notification="✓ Added to cart!"
      />
    </div>
  </div>
</template>
