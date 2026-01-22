<script lang="ts" setup>
import { PencilOffIcon } from 'lucide-vue-next'

const authStore = useAuthStore()
const model = defineModel()
</script>

<template>
  <Card class="mt-2">
    <CardHeader class="relative">
      <CardTitle>Edit {{ authStore.profile?.first_name }} </CardTitle>
      <Button size="icon" variant="outline" class="absolute -top-3 right-3" @click="model = !model">
        <PencilOffIcon />
      </Button>
    </CardHeader>
    <CardContent>
      <ProfileEditForm v-if="authStore.profile" :profile="authStore.profile" @close-form="model = false" />
    </CardContent>
  </Card>
</template>
