<script lang="ts" setup>
const { orders, cancelOrder, checkoutOrder, increaseQuantity, decreaseQuantity, handleRemove, updating } =
  await useOrders()

// useOrdersSocket()

definePageMeta({
  layout: 'profile',
  middleware: ['auth'],
})
</script>

<template>
  <div class="min-h-screen bg-white">
    <div class="mx-auto max-w-7xl py-12 pl-4 sm:pl-6 lg:pl-8">
      <TitlePage title="Orders" description="This is an order page" />
      <main>
        <div v-if="orders && orders.length > 0" class="space-y-4">
          <template v-for="order in orders" :key="order.id">
            <OrderCard
              v-if="order.items && order.items.length > 0"
              :order="order"
              :updating="updating"
              @minus="decreaseQuantity"
              @plus="increaseQuantity"
              @remove="handleRemove"
              @cancelOrder="cancelOrder(order.id)"
              @checkoutOrder="checkoutOrder(order.id)"
            />
          </template>
        </div>
        <div v-else>
          <p class="text-center text-lg">You have no orders yet.</p>
        </div>
      </main>
    </div>
  </div>
</template>
