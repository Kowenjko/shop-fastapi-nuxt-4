<script lang="ts" setup>
const cartStore = useCartStore()
const modalStore = useModalStore()

const handleCheckout = () => {
  modalStore.modalProceedCart.show = true
}

const handleClearCart = () => {
  modalStore.modalClearCart.show = true
}

await cartStore.fetchCartDetails()
</script>

<template>
  <div class="min-h-screen bg-white">
    <div class="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <TitlePage title="Shopping Cart" description="Review your items before checkout" />

      <LoadingData v-if="cartStore.loading" text="Loading cart..." />
      <CartEmpty v-else-if="!cartStore.hasItems" />

      <!-- Содержимое корзины -->
      <div v-else class="grid grid-cols-1 gap-8 lg:grid-cols-3">
        <!-- Список товаров -->
        <div class="space-y-6 lg:col-span-2">
          <CartItem v-for="item in cartStore.cartDetails?.items" :key="item.product_id" :item="item" />
        </div>

        <!-- Итоговая информация -->
        <div class="lg:col-span-1">
          <div class="sticky top-24 rounded-none border-2 border-gray-100 bg-white p-8 shadow-sm">
            <h2 class="mb-8 text-2xl font-bold text-black">Order Summary</h2>
            <CartInfo />
            <CartActions @proceed="handleCheckout" @clear="handleClearCart" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
