<script lang="ts" setup>
const modalStore = useModalStore()
const cartStore = useCartStore()

const hideModal = () => (modalStore.modalClearCart.show = false)
const clearCart = () => {
  cartStore.clearCart()
  hideModal()
}
</script>

<template>
  <Modal v-model:open="modalStore.modalClearCart.show">
    <div class="relative min-w-lg rounded-lg bg-white p-5 text-black">
      <button class="absolute top-2 right-2 transition-all hover:scale-110" @click="hideModal">
        <IconClose class="size-6 text-black" />
      </button>
      <div class="py-4 text-center text-2xl font-bold">Clear Cart</div>
      <p class="pb-4 text-center">Are you sure you want to clear your cart?</p>
      <div class="flex gap-2">
        <Button @click="clearCart" variant="destructive" class="w-1/2" size="lg">Clear Cart</Button>
        <Button @click="hideModal" class="w-1/2" size="lg">Cancel</Button>
      </div>
    </div>
  </Modal>
</template>
