<script setup lang="ts">
const { x, y } = useMouse();
</script>

<template>
  <div class="mx-auto flex h-screen max-w-5xl items-center justify-center">
    pos: {{ x }}, {{ y }}
  </div>
</template>
