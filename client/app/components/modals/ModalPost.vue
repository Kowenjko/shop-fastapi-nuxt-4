<script lang="ts" setup>
import { postAPI } from '@/api'

import { toTypedSchema } from '@vee-validate/zod'

import { useForm } from 'vee-validate'
import * as z from 'zod'

const modalStore = useModalStore()
const authStore = useAuthStore()

const formSchema = toTypedSchema(
  z.object({
    title: z.string().min(2).max(50),
    content: z.string().min(8),
    user_id: z.number().min(1),
  }),
)

const isEditPost = computed(() => modalStore.modalPost.content !== null)

const form = useForm({
  validationSchema: formSchema,
  initialValues: {
    title: '',
    content: '',
    user_id: authStore.profile?.user?.id || 0,
  },
})

const onSubmit = form.handleSubmit(async (values) => {
  console.log('Form submitted!', values)
  try {
    isEditPost.value ? await postAPI.update(values, modalStore.modalPost.content.id) : await postAPI.create(values)
    form.resetForm()
    modalStore.modalPost.show = false
  } catch (error) {
    console.log(error)
  }
})

watch(
  () => modalStore.modalPost.show,
  (newVal) => {
    if (!newVal) {
      form.resetForm()
      modalStore.modalPost.content = null
    } else {
      if (modalStore.modalPost.content)
        form.setValues({
          title: modalStore.modalPost.content?.title || '',
          content: modalStore.modalPost.content?.content || '',
        })
    }
  },
)
</script>

<template>
  <Dialog v-model:open="modalStore.modalPost.show">
    <DialogContent class="sm:max-w-sm">
      <form @submit="onSubmit">
        <DialogHeader class="">
          <DialogTitle>{{ isEditPost ? 'Edit Post' : 'Create a new post' }}</DialogTitle>
        </DialogHeader>

        <div class="grid w-full items-center gap-4 py-4">
          <FormField v-slot="{ componentField }" name="title">
            <FormItem>
              <FormLabel>Title</FormLabel>
              <FormControl>
                <Input type="text" placeholder="title" v-bind="componentField" />
              </FormControl>

              <FormMessage />
            </FormItem>
          </FormField>
          <FormField v-slot="{ componentField }" name="content">
            <FormItem>
              <FormLabel>Content</FormLabel>
              <FormControl>
                <Textarea placeholder="Type your message here." v-bind="componentField" />
              </FormControl>

              <FormMessage />
            </FormItem>
          </FormField>
        </div>
        <DialogFooter>
          <Button type="submit"> {{ isEditPost ? 'Update' : 'Create' }} </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  </Dialog>
</template>
