<script lang="ts" setup>
import { toTypedSchema } from '@vee-validate/zod'
import { GithubIcon } from 'lucide-vue-next'
import { useForm } from 'vee-validate'
import * as z from 'zod'

const modalStore = useModalStore()
const { register } = useAuth()

const formSchema = toTypedSchema(
  z
    .object({
      username: z.string().min(2).max(50),
      email: z.string().email('Invalid email address'),
      password: z
        .string()
        .min(8, 'Минимум 8 символов')
        // .regex(/[A-Z]/, 'Хотя бы одна заглавная буква')
        .regex(/[0-9]/, 'Хотя бы одна цифра'),
      role: z.enum(['user', 'admin']).default('user'),
      confirmPassword: z.string().min(8, 'Минимум 8 символов'),
    })
    .refine((data) => data.password === data.confirmPassword, {
      path: ['confirmPassword'],
      message: 'Passwords do not match',
    }),
)

const form = useForm({
  validationSchema: formSchema,
  initialValues: {
    role: 'user',
  },
})

const onSubmit = form.handleSubmit(async (values) => {
  console.log('Form submitted!', values)
  try {
    await register(values)
    form.resetForm({
      values: {
        role: 'user',
      },
    })
    modalStore.modalRegister.show = false
  } catch (error) {
    console.log(error)
  }
})

const openModelLogin = () => {
  modalStore.modalRegister.show = false
  modalStore.modalLoginIn.show = true
}

watch(
  () => modalStore.modalRegister.show,
  (newVal) => {
    if (!newVal) {
      form.resetForm({
        values: {
          role: 'user',
        },
      })
    }
  },
)
</script>

<template>
  <Dialog v-model:open="modalStore.modalRegister.show">
    <DialogContent class="sm:max-w-sm">
      <form @submit="onSubmit">
        <DialogHeader class="grid grid-cols-4 items-center">
          <div class="col-span-3 space-y-3">
            <DialogTitle>Register your account</DialogTitle>
            <DialogDescription>Enter your data below to register to your account </DialogDescription>
          </div>
          <Button @click="openModelLogin" variant="link"> Login </Button>
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
          <FormField v-slot="{ componentField }" name="email">
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="m@example.com" v-bind="componentField" />
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
          <FormField v-slot="{ componentField }" name="confirmPassword">
            <FormItem>
              <FormLabel>Confirm Password</FormLabel>
              <FormControl>
                <PasswordInput placeholder="********" v-bind="componentField" />
              </FormControl>

              <FormMessage />
            </FormItem>
          </FormField>
        </div>
        <DialogFooter>
          <Button type="submit"> Register </Button>
          <Button type="button" variant="outline" size="icon"> <GithubIcon /> </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>
