<script lang="ts" setup>
import { UserIcon, ShoppingBasketIcon, LogOutIcon } from 'lucide-vue-next'

const { logout, refresh } = useAuth()
const route = useRoute()

const logoutUSer = async () => {
  await logout()
  await navigateTo(HOME_LINK)
}
</script>

<template>
  <AppHeader />
  <ResizablePanelGroup direction="horizontal">
    <ResizablePanel :default-size="20">
      <ul class="flex flex-col gap-1 p-4">
        <li
          class="rounded p-2 transition-all hover:bg-gray-100"
          :class="{ 'bg-gray-100': route.name === PROFILE_LINK.name }"
        >
          <nuxt-link :to="PROFILE_LINK" class="flex items-center gap-2">
            <UserIcon class="h-5 w-5" />
            <span>Profile</span>
          </nuxt-link>
        </li>
        <li
          class="rounded p-2 transition-all hover:bg-gray-100"
          :class="{ 'bg-gray-100': route.name === ORDERS_LINK.name }"
        >
          <nuxt-link :to="ORDERS_LINK" class="flex items-center gap-2">
            <ShoppingBasketIcon class="h-5 w-5" />
            <span> Orders</span>
          </nuxt-link>
        </li>
        <li class="cursor-pointer border-t border-gray-300">
          <button
            @click="logoutUSer"
            class="mt-1 flex w-full items-center gap-2 rounded p-2 pt-3 transition-all hover:bg-gray-100"
          >
            <LogOutIcon class="h-5 w-5" />
            <span>LogOut</span>
          </button>
        </li>
      </ul>
    </ResizablePanel>
    <ResizableHandle class="border border-black" />
    <ResizablePanel :default-size="80">
      <slot />
    </ResizablePanel>
  </ResizablePanelGroup>

  <AppFooter />
</template>
