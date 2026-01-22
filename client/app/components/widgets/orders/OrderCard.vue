<script lang="ts" setup>
import { BanIcon, BanknoteArrowUp } from 'lucide-vue-next'

const { order, updating } = defineProps<{
  order: OrderI
  updating: boolean
}>()

const emit = defineEmits<{
  minus: [order_id: number, product_id: number, count: number]
  plus: [order_id: number, product_id: number, count: number]
  remove: [order_id: number, product_id: number]
  cancelOrder: []
  checkoutOrder: []
}>()
</script>

<template>
  <Card :class="{ 'pointer-events-none opacity-50': order.status !== OrderStatus.DRAFT }">
    <CardHeader class="relative">
      <CardTitle>ID - {{ order.id }} </CardTitle>
      <CardDescription>count: {{ order.total_items }} total: ${{ order.total_price }}</CardDescription>
      <div class="absolute -top-3 right-2">
        <Badge v-if="order.status === OrderStatus.CANCELED" variant="destructive">{{ order.status }}</Badge>
        <Badge v-else-if="order.status === OrderStatus.PAID">{{ order.status }}</Badge>
        <Badge v-else variant="outline">{{ order.status }}</Badge>
      </div>
    </CardHeader>
    <CardContent>
      <ul v-if="order.items && order.items.length > 0" class="space-y-6 lg:col-span-2">
        <li class="flex gap-6 border-t pt-6" v-for="item in order.items" :key="item.product_id">
          <div class="h-24 w-24 shrink-0">
            <nuxt-img
              :src="item.image_url"
              :alt="item.name"
              class="h-full w-full rounded-none object-cover"
              @error="noImage()"
            />
          </div>

          <div class="grow">
            <h3 class="mb-2 text-lg font-bold text-black">
              {{ item.name }}
            </h3>
            <p class="mb-3 text-sm text-gray-600">${{ item.unit_price.toFixed(2) }} each</p>
            <CartItemAction
              :quantity="item.count"
              :updating
              @minus="emit('minus', order.id, item.product_id, item.count)"
              @plus="emit('plus', order.id, item.product_id, item.count)"
              @remove="emit('remove', order.id, item.product_id)"
            />
          </div>
          <CartItemTotal :subtotal="item.total" />
        </li>
      </ul>
      <div v-else>No products</div>
    </CardContent>
    <CardFooter class="flex justify-between">
      <p class="text-sm text-gray-500">Ordered on: {{ new Date(order.created_at).toLocaleDateString() }}</p>
      <div class="space-x-2">
        <Button variant="destructive" @click="emit('cancelOrder')"> <BanIcon /> Cancel</Button>
        <Button @click="emit('checkoutOrder')"> <BanknoteArrowUp /> Checkout</Button>
      </div>
    </CardFooter>
  </Card>
</template>
