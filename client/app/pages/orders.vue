<script lang="ts" setup>
import { orderAPI } from '@/api'

const { data: orders, refresh } = await useAPI<OrderI[]>(ORDERS + USER, { key: 'orders' })

const updating = ref(false)

const increaseQuantity = async (order_id: number, product_id: number, count: number) => {
  updating.value = true

  try {
    await orderAPI.updateProductCount({ order_id, product_id, count: count + 1 })
    await refresh()
  } catch (error) {
  } finally {
    updating.value = false
  }
}

const decreaseQuantity = async (order_id: number, product_id: number, count: number) => {
  updating.value = true

  try {
    if (count > 1) {
      await orderAPI.updateProductCount({ order_id, product_id, count: count - 1 })
    } else {
      await orderAPI.removeProduct({ order_id, product_id })
    }
    await refresh()
  } catch (error) {
    console.log(error)
  } finally {
    updating.value = false
  }
}

const handleRemove = async (order_id: number, product_id: number) => {
  updating.value = true

  await orderAPI.removeProduct({ order_id, product_id })
  await refresh()

  try {
  } catch (error) {
    console.log(error)
  } finally {
    updating.value = false
  }
}

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
          <Card v-for="order in orders" :key="order.id">
            <CardHeader class="relative">
              <CardTitle>ID - {{ order.id }} </CardTitle>
              <CardDescription>count: {{ order.total_items }} total: ${{ order.total_price }}</CardDescription>
              <div class="absolute -top-3 right-2">
                <Badge v-if="order.status === OrderStatus.CANCELED" variant="destructive">{{ order.status }}</Badge>
                <Badge v-if="order.status === OrderStatus.PAID">{{ order.status }}</Badge>
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
                      @minus="decreaseQuantity(order.id, item.product_id, item.count)"
                      @plus="increaseQuantity(order.id, item.product_id, item.count)"
                      @remove="handleRemove(order.id, item.product_id)"
                    />
                  </div>
                  <CartItemTotal :subtotal="item.total" />
                </li>
              </ul>
              <div v-else>No products</div>
            </CardContent>
            <CardFooter>
              <p class="text-sm text-gray-500">Ordered on: {{ new Date(order.created_at).toLocaleDateString() }}</p>
            </CardFooter>
          </Card>
        </div>
        <div v-else>
          <p class="text-center text-lg">You have no orders yet.</p>
        </div>
      </main>
    </div>
  </div>
</template>
