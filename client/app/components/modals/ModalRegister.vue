<script lang="ts" setup>
import { GithubIcon } from 'lucide-vue-next'
const modalStore = useModalStore()

const openModelLogin = () => {
  modalStore.modalRegister.show = false
  modalStore.modalLoginIn.show = true
}
</script>

<template>
  <Dialog v-model:open="modalStore.modalRegister.show">
    <form>
      <DialogContent class="sm:max-w-sm">
        <DialogHeader class="grid grid-cols-4 items-center">
          <div class="col-span-3 space-y-3">
            <DialogTitle>Register your account</DialogTitle>
            <DialogDescription>Enter your data below to register to your account </DialogDescription>
          </div>
          <Button @click="openModelLogin" variant="link"> Login </Button>
        </DialogHeader>

        <div class="grid w-full items-center gap-4">
          <div class="flex flex-col space-y-1.5">
            <Label for="name">User name</Label>
            <Input id="name" placeholder="name" />
          </div>
          <div class="flex flex-col space-y-1.5">
            <Label for="email">Email</Label>
            <Input id="email" type="email" placeholder="m@example.com" />
          </div>
          <div class="flex flex-col space-y-1.5">
            <div class="flex items-center">
              <Label for="password">Password</Label>
            </div>
            <Input id="password" type="password" />
          </div>
          <div class="flex flex-col space-y-1.5">
            <div class="flex items-center">
              <Label for="confirmPassword">Confirm password</Label>
            </div>
            <Input id="confirmPassword" type="password" />
          </div>
        </div>
        <DialogFooter>
          <Button> Register </Button>
          <Button variant="outline" size="icon"> <GithubIcon /> </Button>
        </DialogFooter>
      </DialogContent>
    </form>
  </Dialog>
</template>
