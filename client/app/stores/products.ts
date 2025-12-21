import { defineStore } from 'pinia'

export const useProductsStore = defineStore('products', () => {
  const selectedCategory = ref<number | null>(null)

  const setCategory = (categoryId: number) => {
    selectedCategory.value = categoryId
  }

  const clearCategoryFilter = () => {
    selectedCategory.value = null
  }

  return {
    selectedCategory,
    setCategory,
    clearCategoryFilter,
  }
})
