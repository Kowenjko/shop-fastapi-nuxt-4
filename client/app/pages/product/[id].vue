<script lang="ts" setup>
const adding = ref(false)
const showNotification = ref(false)

const cartStore = useCartStore()

const route = useRoute()
const router = useRouter()

const { data: product, error, pending } = await useAPI<ProductI>(PRODUCTS + route.params.id + '/')

const handleAddToCart = async () => {
  if (!product.value) return
  adding.value = true
  const success = await cartStore.addToCart(product.value.id, 1)

  if (success) {
    showNotification.value = true
    setTimeout(() => {
      showNotification.value = false
    }, 3000)
  }

  adding.value = false
}
</script>

<template>
  <div class="min-h-screen bg-white">
    <div class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <ButtonBack @click="router.push(HOME_LINK)" />

      <!-- Состояние загрузки -->
      <LoadingData v-if="pending" />
      <LoadingError v-else-if="error" :is-button-back="true" :error :to="HOME_LINK" />

      <!-- Детальная информация о товаре -->
      <ProductDetailCart v-else-if="product" :product :adding :showNotification @add-to-cart="handleAddToCart" />
    </div>
  </div>
</template>
