import type { FetchError } from 'ofetch'

export const useProducts = () => {
  const products = ref<ProductI[]>([])
  const categories = ref<CategoryI[]>([])

  const loading = ref(false)
  const error = ref<FetchError<any> | null>(null)

  const productsStore = useProductsStore()

  const filteredProducts = computed(() => {
    if (!productsStore.selectedCategory) {
      return products.value
    }
    return products.value.filter((product) => product.category_id === productsStore.selectedCategory)
  })

  const productsCount = computed(() => filteredProducts.value.length)

  const totalProductsCount = computed(() => {
    return products.value.length
  })

  const fetchProducts = async () => {
    error.value = null
    const { data, error: errorProducts, pending } = await useAPI<AllProductI>(PRODUCTS, { key: 'products' })
    loading.value = pending.value
    products.value = data.value?.products || []
    error.value = errorProducts.value || null
  }

  const fetchProductById = async (id: number) => {
    error.value = null

    const { data, error: errorProduct, pending } = await useAPI<ProductI[]>(PRODUCTS + id + '/', { key: 'product' })
    loading.value = pending.value
    error.value = errorProduct.value || null
    return data.value || null
  }

  const fetchCategories = async () => {
    const { data, error: errorCategories } = await useAPI<CategoryI[]>(CATEGORIES, { key: 'categories' })
    categories.value = data.value || []
    error.value = errorCategories.value || null
  }

  return {
    // State
    products,
    categories,
    loading,
    error,
    // Getters
    filteredProducts,
    productsCount,
    totalProductsCount,
    // Actions
    fetchProducts,
    fetchProductById,
    fetchCategories,
  }
}
