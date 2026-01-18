<script lang="ts" setup>
import { SaveIcon } from 'lucide-vue-next'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { profileAPI } from '@/api'
import * as z from 'zod'

const { profile } = defineProps<{
  profile: ProfileI
}>()
const authStore = useAuthStore()

const emit = defineEmits<{
  'close-form': []
}>()

const formSchema = toTypedSchema(
  z.object({
    first_name: z.string().min(2).max(50).optional(),
    last_name: z.string().min(2).max(50).optional(),
    phone: z.string().min(10).max(15).optional(),
    age: z.coerce.number().min(0).optional(),
    city_id: z.string().nullable().optional(),
  }),
)
const form = useForm({
  validationSchema: formSchema,
  initialValues: {
    first_name: profile?.first_name ?? '',
    last_name: profile?.last_name ?? '',
    phone: profile?.phone ?? '',
    age: profile?.age ?? 0,
    city_id: profile?.city?.id ?? null,
  },
})
const onSubmit = form.handleSubmit(async (values) => {
  console.log('Form submitted!', values)

  try {
    const updatedProfile = await profileAPI.update(values)
    authStore.profile = updatedProfile
    emit('close-form')
  } catch (error) {
    console.log(error)
  }
})
</script>

<template>
  <form @submit="onSubmit" class="space-y-3">
    <div class="grid grid-cols-2 gap-4">
      <FormField v-slot="{ componentField }" name="first_name">
        <FormItem>
          <FormLabel>First Name</FormLabel>
          <FormControl>
            <Input type="text" placeholder="First Name" v-bind="componentField" />
          </FormControl>

          <FormMessage />
        </FormItem>
      </FormField>
      <FormField v-slot="{ componentField }" name="last_name">
        <FormItem>
          <FormLabel>Last Name</FormLabel>
          <FormControl>
            <Input type="text" placeholder="Last Name" v-bind="componentField" />
          </FormControl>

          <FormMessage />
        </FormItem>
      </FormField>
    </div>
    <div class="grid grid-cols-2 gap-4">
      <FormField v-slot="{ componentField }" name="phone">
        <FormItem>
          <FormLabel>Phone</FormLabel>
          <FormControl>
            <Input type="text" placeholder="Phone Number" v-bind="componentField" />
          </FormControl>

          <FormMessage />
        </FormItem>
      </FormField>
      <FormField v-slot="{ componentField }" name="age">
        <NumberField
          id="age"
          :model-value="componentField.modelValue"
          @update:modelValue="(v) => componentField.onChange(Number(v))"
          :min="0"
        >
          <Label for="age">Age</Label>
          <NumberFieldContent>
            <NumberFieldDecrement />
            <NumberFieldInput />
            <NumberFieldIncrement />
          </NumberFieldContent>
        </NumberField>
      </FormField>
    </div>
    <div class="flex justify-end">
      <Button type="submit"> <SaveIcon /> Save </Button>
    </div>
  </form>
</template>
