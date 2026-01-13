<script lang="ts" setup>
import { ShoppingBagIcon, ShoppingCartIcon, UserIcon, LogOutIcon } from 'lucide-vue-next'

const cartStore = useCartStore()
</script>

<template>
  <header class="sticky top-0 z-50 border-b-2 border-black bg-white">
    <div class="mx-auto max-w-7xl px-4">
      <div class="flex h-20 items-center justify-between">
        <nuxt-link :to="HOME_LINK" class="group flex items-center space-x-2">
          <ShoppingBagIcon class="h-7 w-7 transition-transform group-hover:scale-105" />
          <span class="text-2xl font-bold text-black">FastAPI Shop</span>
        </nuxt-link>
        <!-- Навигация -->

        <div class="flex items-center gap-5">
          <UserIcon class="h-6 w-6" />

          <Menubar class="border-none shadow-none">
            <MenubarMenu>
              <MenubarTrigger class="cursor-pointer">
                <Avatar> <AvatarFallback class="border-2 border-black bg-none">VK</AvatarFallback> </Avatar>
              </MenubarTrigger>
              <MenubarContent>
                <MenubarItem>
                  <nuxt-link :to="PROFILE_LINK">Profile</nuxt-link>
                </MenubarItem>
                <MenubarItem>
                  <nuxt-link :to="ORDERS_LINK">Orders</nuxt-link>
                </MenubarItem>
                <MenubarSeparator />
                <MenubarItem>
                  <LogOutIcon class="h-6 w-6" />
                </MenubarItem>
              </MenubarContent>
            </MenubarMenu>
          </Menubar>

          <nuxt-link :to="CART_LINK">
            <div class="relative">
              <ShoppingCartIcon class="h-6 w-6" />
              <Badge
                v-if="cartStore.itemsCount && cartStore.itemsCount > 0"
                class="absolute -top-3 -right-3 h-5 w-5 rounded-full tabular-nums"
              >
                {{ cartStore.itemsCount }}
              </Badge>
            </div>
          </nuxt-link>
        </div>
      </div>
    </div>
  </header>
</template>
