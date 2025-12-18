<script setup lang="ts">
const { isCloseOutside = true } = defineProps<{ isCloseOutside?: boolean }>();

const open = defineModel("open");

const clickOutside = () => {
  if (!isCloseOutside) return;

  open.value = false;
};
</script>

<template>
  <div
    class="fixed top-0 left-0 z-50 flex h-screen w-full scale-0 items-center justify-center bg-black/90 opacity-0 transition-all duration-300"
    :class="{ 'scale-100 opacity-100': open }"
    @click.self="clickOutside"
  >
    <button class="absolute top-4 right-4 text-black" @click="open = false">
      <IconClose class="size-8 text-white" />
    </button>
    <slot />
  </div>
</template>
