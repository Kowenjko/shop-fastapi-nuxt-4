<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { Eye, EyeOff, AlertTriangle } from 'lucide-vue-next'
import { cn } from '@/lib/utils'

interface Props {
  modelValue?: string
  placeholder?: string
  disabled?: boolean
  error?: boolean
  class?: HTMLAttributes['class']
}

const props = defineProps<Props>()
defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

/* ---------------- State ---------------- */
const showPassword = ref(false)
const capsLockOn = ref(false)

/* ---------------- Password strength ---------------- */
const strength = computed(() => {
  const v = props.modelValue ?? ''
  let score = 0

  if (v.length >= 8) score++
  if (/[A-Z]/.test(v)) score++
  if (/[0-9]/.test(v)) score++
  if (/[^A-Za-z0-9]/.test(v)) score++

  return score // 0–4
})

const strengthLabel = computed(() => {
  return ['Very weak', 'Weak', 'Okay', 'Strong', 'Very strong'][strength.value]
})

const strengthColor = computed(() => {
  return ['bg-destructive', 'bg-orange-500', 'bg-yellow-500', 'bg-green-500', 'bg-emerald-600'][strength.value]
})

/* ---------------- Handlers ---------------- */
function onKeyup(e: KeyboardEvent) {
  capsLockOn.value = e?.getModifierState?.('CapsLock')
}
</script>

<template>
  <div class="space-y-1">
    <!-- Input -->
    <div class="relative">
      <input
        :type="showPassword ? 'text' : 'password'"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        @keyup="onKeyup"
        :class="
          cn(
            'flex h-10 w-full rounded-md border bg-background px-3 py-2 pr-10 text-sm',
            'placeholder:text-muted-foreground',
            'focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:outline-none',
            'disabled:cursor-not-allowed disabled:opacity-50',
            error ? 'border-destructive focus-visible:ring-destructive' : 'border-input',
            props.class,
          )
        "
      />

      <!-- Hover show -->
      <button
        type="button"
        class="absolute top-1/2 right-2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
        @mouseenter="showPassword = true"
        @mouseleave="showPassword = false"
        :aria-label="'Show password'"
      >
        <Eye class="h-4 w-4" />
      </button>
    </div>

    <!-- Caps Lock warning -->
    <div v-if="capsLockOn" class="flex items-center gap-1 text-xs text-yellow-600">
      <AlertTriangle class="h-3 w-3" />
      Caps Lock is ON
    </div>

    <!-- Strength bar -->
    <div v-if="modelValue" class="space-y-1">
      <div class="flex gap-1">
        <span v-for="i in 4" :key="i" class="h-1 w-full rounded-full bg-muted">
          <span v-if="i <= strength" class="block h-full rounded-full transition-all" :class="strengthColor" />
        </span>
      </div>
      <p class="text-xs text-muted-foreground">
        {{ strengthLabel }}
      </p>
    </div>
  </div>
</template>
