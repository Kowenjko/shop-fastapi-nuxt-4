<script lang="ts" setup>
import { orderAPI } from '@/api'

const modalStore = useModalStore()
const cartStore = useCartStore()

const createOrder = async () => {
  try {
    const order = await orderAPI.create({ promocode: null })

    const products = cartStore.cartDetails?.items.map((item) => ({
      product_id: item.product_id,
      count: item.quantity,
    }))

    if (!products) return
    await orderAPI.addProducts({ order_id: order.id, products })
    modalStore.modalProceedCart.show = false
    cartStore.clearCart()
    await navigateTo(ORDERS_LINK)
  } catch (error) {
    console.log(error)
  }
}
</script>

<template>
  <Dialog v-model:open="modalStore.modalProceedCart.show">
    <DialogContent class="sm:max-w-lg">
      <DialogHeader>
        <DialogTitle>Modal Proceed</DialogTitle>
      </DialogHeader>
      <div class="grid gap-4">Checkout functionality will be implemented soon!</div>
      <DialogFooter>
        <DialogClose as-child>
          <Button variant="outline"> Cancel </Button>
        </DialogClose>
        <Button @click="createOrder">Create Order</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
