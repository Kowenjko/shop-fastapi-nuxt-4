import { defineStore } from 'pinia'

export const useErrorsStore = defineStore('errors', () => {
  const errors = ref<any>(null)

  const setErrors = (err: any) => (errors.value = err)
  const clearErrors = () => (errors.value = null)
  const clearErrorsItem = (item: any) => {
    if (errors.value && Object.keys(errors.value).includes(item)) {
      errors.value[item] = null
    }
  }

  return { errors, setErrors, clearErrors, clearErrorsItem }
})
