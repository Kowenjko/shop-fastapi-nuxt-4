<script lang="ts" setup>
const modalStore = useModalStore()

const hideModal = () => (modalStore.modalProceedCart.show = false)
</script>

<template>
  <Modal v-model:open="modalStore.modalProceedCart.show">
    <div class="relative min-w-lg rounded-lg bg-white p-5 text-black">
      <button class="absolute top-2 right-2 transition-all hover:scale-110" @click="hideModal">
        <IconClose class="size-6 text-black" />
      </button>
      <div class="py-4 text-center text-2xl font-bold">Modal Proceed</div>
      <p class="pb-4 text-center">Checkout functionality will be implemented soon!</p>

      <Button @click="hideModal" class="w-full" size="lg">Proceed to Checkout</Button>
    </div>
  </Modal>
</template>
