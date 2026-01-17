<script lang="ts" setup>
import { toTypedSchema } from '@vee-validate/zod'
import { GithubIcon } from 'lucide-vue-next'
import { useForm } from 'vee-validate'
import * as z from 'zod'

const modalStore = useModalStore()
const { login, loginByProvider } = useAuth()

const formSchema = toTypedSchema(
  z.object({
    username: z.string().min(2).max(50),
    password: z
      .string()
      .min(8, 'Минимум 8 символов')
      // .regex(/[A-Z]/, 'Хотя бы одна заглавная буква')
      .regex(/[0-9]/, 'Хотя бы одна цифра'),
  }),
)

const form = useForm({
  validationSchema: formSchema,
})

const onSubmit = form.handleSubmit(async (values) => {
  console.log('Form submitted!', values)
  try {
    await login(values)
    form.resetForm()
    modalStore.modalLoginIn.show = false
  } catch (error) {
    console.log(error)
  }
})

const openModelRegister = () => {
  modalStore.modalLoginIn.show = false
  modalStore.modalRegister.show = true
}

watch(
  () => modalStore.modalLoginIn.show,
  (newVal) => {
    if (!newVal) {
      form.resetForm()
    }
  },
)
</script>

<template>
  <Dialog v-model:open="modalStore.modalLoginIn.show">
    <DialogContent class="sm:max-w-sm">
      <form @submit="onSubmit">
        <DialogHeader class="grid grid-cols-4 items-center">
          <div class="col-span-3 space-y-3">
            <DialogTitle>Login to your account</DialogTitle>
            <DialogDescription>Enter your email below to login to your account </DialogDescription>
          </div>
          <Button @click="openModelRegister" variant="link"> Sign Up </Button>
        </DialogHeader>

        <div class="grid w-full items-center gap-4">
          <FormField v-slot="{ componentField }" name="username">
            <FormItem>
              <FormLabel>User name</FormLabel>
              <FormControl>
                <Input type="text" placeholder="name" v-bind="componentField" />
              </FormControl>

              <FormMessage />
            </FormItem>
          </FormField>
          <FormField v-slot="{ componentField }" name="password">
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <PasswordInput placeholder="********" v-bind="componentField" />
              </FormControl>

              <FormMessage />
            </FormItem>
          </FormField>
        </div>
        <DialogFooter>
          <Button type="submit"> Login </Button>
          <Button @click="loginByProvider(GITHUB)" type="button" variant="outline" size="icon"> <GithubIcon /> </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>
