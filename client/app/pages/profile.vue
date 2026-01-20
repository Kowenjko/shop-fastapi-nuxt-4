<script lang="ts" setup>
import { UserPenIcon, PencilOffIcon } from 'lucide-vue-next'

const authStore = useAuthStore()
const showEdit = ref(false)

definePageMeta({
  layout: 'profile',
  middleware: ['auth'],
})
</script>

<template>
  <div class="h-screen bg-white">
    <div class="mx-auto max-w-7xl px-4 pt-12 sm:px-6 lg:px-8">
      <TitlePage title="Profile" description="This is an profile page" />

      <ClientOnly>
        <Card v-if="!showEdit">
          <CardHeader class="relative">
            <CardTitle>{{ authStore.profile?.first_name }} {{ authStore.profile?.last_name }}</CardTitle>
            <Button size="icon" variant="outline" class="absolute -top-3 right-3" @click="showEdit = !showEdit">
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

        <Card v-if="showEdit" class="mt-2">
          <CardHeader class="relative">
            <CardTitle>Edit {{ authStore.profile?.first_name }} </CardTitle>
            <Button size="icon" variant="outline" class="absolute -top-3 right-3" @click="showEdit = !showEdit">
              <PencilOffIcon />
            </Button>
          </CardHeader>
          <CardContent>
            <ProfileEditForm v-if="authStore.profile" :profile="authStore.profile" @close-form="showEdit = false" />
          </CardContent>
        </Card>
      </ClientOnly>
    </div>
  </div>
</template>
