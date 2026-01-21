<script lang="ts" setup>
import {
  ShoppingBagIcon,
  ShoppingCartIcon,
  UserIcon,
  LogOutIcon,
  ShoppingBasketIcon,
  BookOpenTextIcon,
} from 'lucide-vue-next'

const cartStore = useCartStore()
const modalStore = useModalStore()
const authStore = useAuthStore()

const { logout, refresh } = useAuth()

const openModelLogin = () => (modalStore.modalLoginIn.show = true)

const logoutUSer = async () => {
  await logout()
  await navigateTo(HOME_LINK)
}

onMounted(async () => {
  !authStore.isAuthenticated ? await refresh() : null
})
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
          <ClientOnly>
            <Menubar class="border-none shadow-none" v-if="authStore.token">
              <MenubarMenu>
                <MenubarTrigger class="cursor-pointer">
                  <Avatar>
                    <AvatarFallback class="border-2 border-black bg-none">{{ authStore.upperCaseName }}</AvatarFallback>
                  </Avatar>
                </MenubarTrigger>
                <MenubarContent>
                  <MenubarItem>
                    <nuxt-link :to="PROFILE_LINK" class="w-full">
                      <div class="flex gap-2"><UserIcon /> Profile</div>
                    </nuxt-link>
                  </MenubarItem>
                  <MenubarItem>
                    <nuxt-link :to="POSTS_LINK" class="w-full">
                      <div class="flex gap-2"><BookOpenTextIcon /> Posts</div>
                    </nuxt-link>
                  </MenubarItem>
                  <MenubarItem>
                    <nuxt-link :to="ORDERS_LINK" class="w-full">
                      <div class="flex gap-2"><ShoppingBasketIcon /> Orders</div>
                    </nuxt-link>
                  </MenubarItem>
                  <MenubarSeparator />
                  <MenubarItem>
                    <button @click="logoutUSer" class="w-full"><LogOutIcon class="h-6 w-6" /></button>
                  </MenubarItem>
                </MenubarContent>
              </MenubarMenu>
            </Menubar>

            <button v-else @click="openModelLogin" class="rounded-md p-2 transition-all hover:bg-gray-100">
              <UserIcon class="h-6 w-6" />
            </button>
          </ClientOnly>
          <nuxt-link :to="CART_LINK">
            <div class="relative">
              <ShoppingCartIcon class="h-6 w-6" />
              <ClientOnly>
                <Badge
                  v-if="cartStore.itemsCount && cartStore.itemsCount > 0"
                  class="absolute -top-3 -right-3 h-5 w-5 rounded-full tabular-nums"
                >
                  {{ cartStore.itemsCount }}
                </Badge>
              </ClientOnly>
            </div>
          </nuxt-link>
        </div>
      </div>
    </div>
  </header>
</template>
