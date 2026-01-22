<script lang="ts" setup>
import { UserPenIcon } from 'lucide-vue-next'
const authStore = useAuthStore()
const model = defineModel()
</script>

<template>
  <Card>
    <CardHeader class="relative">
      <CardTitle>{{ authStore.profile?.first_name }} {{ authStore.profile?.last_name }}</CardTitle>
      <Button size="icon" variant="outline" class="absolute -top-3 right-3" @click="model = !model">
        <UserPenIcon />
      </Button>
    </CardHeader>
    <CardContent>
      <p><strong>Email:</strong> {{ authStore.profile?.user.email }}</p>
      <p><strong>Phone:</strong> {{ authStore.profile?.phone }}</p>
      <p><strong>Age:</strong> {{ authStore.profile?.age }}</p>
      <p><strong>Address:</strong> {{ authStore.profile?.city?.full_name || '---' }}</p>
    </CardContent>
  </Card>
</template>
