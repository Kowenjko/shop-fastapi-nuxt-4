<script lang="ts" setup>
import CardContent from '~/components/ui/card/CardContent.vue'

const { item } = defineProps<{ item: CartItemI }>()

const { updating, increaseQuantity, decreaseQuantity, handleRemove } = useCartActions()
</script>

<template>
  <Card class="transition-all hover:shadow-lg">
    <CardContent class="flex gap-6">
      <!-- Изображение товара -->
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
        <p class="mb-3 text-sm text-gray-600">${{ item.price.toFixed(2) }} each</p>

        <CartItemAction
          :quantity="item.quantity"
          :updating
          @minus="decreaseQuantity(item)"
          @plus="increaseQuantity(item)"
          @remove="handleRemove(item)"
        />
      </div>

      <CartItemTotal :subtotal="item.subtotal" />
    </CardContent>
  </Card>
</template>
