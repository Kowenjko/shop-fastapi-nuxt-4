<script lang="ts" setup>
import { SaveIcon, PencilIcon } from 'lucide-vue-next'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { profileAPI } from '@/api'
import * as z from 'zod'

const { profile } = defineProps<{
  profile: ProfileI
}>()
const authStore = useAuthStore()
const selectRegion = ref(profile?.city?.region || '')
const selectDistrict = ref(profile?.city?.district || '')
const selectCommunity = ref(profile?.city?.community || '')
const selectCity = ref<CityI | null>(profile?.city || null)
const searchCity = ref(profile?.city?.name || '')

const showEditCity = ref(false)

const { data: regions } = await useAPI(BASE_API + CITIES + REGIONS, { key: 'regions' })

const { data: districts } = await useAPI(BASE_API + CITIES + DISTRICTS, {
  key: 'districts',
  query: { region: selectRegion },
  watch: [selectRegion],
})

const { data: communities } = await useAPI(BASE_API + CITIES + COMMUNITIES, {
  key: 'communities',
  query: { region: selectRegion, district: selectDistrict },
  watch: [selectDistrict],
})

const { data: cities } = await useAPI<CitiesI>(BASE_API + CITIES, {
  key: 'cities',
  query: { region: selectRegion, district: selectDistrict, community: selectCommunity, name: searchCity, per_page: 10 },
  watch: [selectCommunity],
})

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

  if (selectCity.value) {
    values.city_id = selectCity.value.id
  } else {
    values.city_id = null
  }

  try {
    const updatedProfile = await profileAPI.update(values)
    authStore.profile = updatedProfile
    emit('close-form')
  } catch (error) {
    console.log(error)
  }
})

watch(selectRegion, () => {
  selectDistrict.value = ''
})

watch(selectDistrict, () => {
  selectCommunity.value = ''
})

watch(selectCommunity, () => {
  selectCity.value = null
  searchCity.value = ''
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
    <div class="flex items-center justify-between border-t border-gray-200 pt-3">
      <div class="space-y-2 space-x-2">
        <Label>City:</Label>
        <Badge v-if="selectRegion">{{ selectRegion }}</Badge>
        <Badge v-if="selectDistrict">{{ selectDistrict }} р-н</Badge>

        <Badge v-if="selectCommunity">{{ selectCommunity }} громада </Badge>
        <Badge v-if="selectCity">{{ selectCity?.city_type?.toLowerCase() }} {{ selectCity?.name }} </Badge>
      </div>
      <div>
        <Button @click="showEditCity = !showEditCity" type="button" variant="outline" size="icon">
          <PencilIcon />
        </Button>
      </div>
    </div>
    <transition name="fade">
      <div v-if="showEditCity" class="grid grid-cols-2 gap-4">
        <div class="w-full space-y-2">
          <Label for="regions">Regions</Label>
          <Select id="regions" v-model="selectRegion" class="w-full">
            <SelectTrigger class="w-full">
              <SelectValue placeholder="Select a region" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectLabel>Regions</SelectLabel>
                <SelectItem v-for="(region, index) in regions" :value="region" :key="index"> {{ region }} </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>
        <div class="w-full space-y-2" v-if="selectRegion">
          <Label for="districts">Districts</Label>
          <Select id="districts" v-model="selectDistrict" class="w-full">
            <SelectTrigger class="w-full">
              <SelectValue placeholder="Select a district" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectLabel>Districts</SelectLabel>
                <SelectItem v-for="(district, index) in districts" :value="district" :key="index">
                  {{ district }}
                </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>
        <div class="w-full space-y-2" v-if="selectDistrict">
          <Label for="districts">Communities</Label>
          <Select id="districts" v-model="selectCommunity" class="w-full">
            <SelectTrigger class="w-full">
              <SelectValue placeholder="Select a community" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectLabel>Communities</SelectLabel>
                <SelectItem v-for="(community, index) in communities" :value="community" :key="index">
                  {{ community }}
                </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>
        <div class="w-full space-y-2" v-if="selectCommunity && cities?.items && cities?.items.length > 0">
          <Label for="districts">City - {{ searchCity }}</Label>
          <Select id="districts" v-model="selectCity" class="w-full">
            <SelectTrigger class="w-full">
              <SelectValue placeholder="Select a city" />
            </SelectTrigger>
            <SelectContent>
              <!-- Search -->
              <div class="border-b p-2">
                <Input v-model="searchCity" placeholder="Search city..." class="h-8" />
              </div>
              <SelectGroup>
                <SelectLabel>Cities</SelectLabel>
                <SelectItem v-for="(city, index) in cities.items" :value="city" :key="index">
                  {{ city?.name }}
                </SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>
      </div>
    </transition>
    <div class="flex justify-end">
      <Button type="submit"> <SaveIcon /> Save </Button>
    </div>
  </form>
</template>
