<script lang="ts" setup>
const {
  disabled = false,
  text,
  isShowTransition = false,
  textNotification = "",
  variant = "default",
} = defineProps<{
  disabled?: boolean;
  text: string;
  isShowTransition?: boolean;
  textNotification?: string;
  variant?: "default" | "destructive";
}>();

const emit = defineEmits<{ onClick: [] }>();

const onClick = () => emit("onClick");

const classes = computed(() => {
  if (variant === "destructive")
    return "bg-white border border-red-500 text-red-500 hover:bg-red-200";
  return "bg-black text-white hover:bg-gray-800";
});
</script>

<template>
  <button
    @click="onClick"
    :disabled
    class="w-full rounded-lg px-4 py-3 font-medium transition-colors disabled:cursor-not-allowed disabled:opacity-50"
    :class="classes"
  >
    {{ text }}
  </button>
  <transition name="fade">
    <div
      v-if="isShowTransition"
      class="mt-2 text-center text-sm font-medium text-green-600"
    >
      {{ textNotification }}
    </div>
  </transition>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
