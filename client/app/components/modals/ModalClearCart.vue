<script lang="ts" setup>
const modalStore = useModalStore()
const cartStore = useCartStore()

const clearCart = () => cartStore.clearCart()
</script>

<template>
  <Dialog v-model:open="modalStore.modalClearCart.show">
    <DialogContent class="sm:max-w-lg">
      <DialogHeader>
        <DialogTitle>Clear Cart</DialogTitle>
      </DialogHeader>
      <div class="grid gap-4">Are you sure you want to clear your cart?</div>
      <DialogFooter>
        <DialogClose as-child>
          <Button variant="outline"> Cancel </Button>
        </DialogClose>
        <Button @click="clearCart" variant="destructive">Clear Cart </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
