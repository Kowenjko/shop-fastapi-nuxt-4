<script lang="ts" setup>
const productsStore = useProductsStore()

const test = useOrdersSocket('test')

const {
  categories,
  productsCount,
  totalProductsCount,
  loading,
  error,
  filteredProducts,
  fetchCategories,
  fetchProducts,
} = useProducts()

await fetchCategories()
await fetchProducts()

const goToRedirect = () => navigateTo('https://api.shop.local/auth/github/login', { external: true })
const goToRedirectUnlink = () => $fetch('https://api.shop.local/auth/github/unlink?user_id=15')
const goToRedirectLink = () => $fetch('https://api.shop.local/auth/github/link?provider_id=74559496&user_id=15')
// navigateTo('https://api.shop.local/auth/github/link?provider_id=74559496&user_id=15', { external: true })
</script>

<template>
  <div class="min-h-screen bg-white">
    <div class="mx-auto max-w-7xl px-4 py-8">
      <TitlePage title="Product Catalog" description="Discover our amazing products" />

      <div class="flex gap-5 py-4">
        <button @click="goToRedirect">Redirect</button>
        <button @click="goToRedirectLink">Redirect Link</button>
        <button @click="goToRedirectUnlink">Redirect UnLink</button>
      </div>

      <div class="flex gap-8">
        <aside class="w-64 shrink-0">
          <CategoryFilter
            :categories="categories"
            :products-count="productsCount"
            :total-products-count="totalProductsCount"
          />
        </aside>

        <main class="grow">
          <InfoFilter
            :products-count="productsCount"
            :selected-category="productsStore.selectedCategory"
            @clear-filter="productsStore.clearCategoryFilter"
          />

          <LoadingData v-if="loading" />
          <LoadingError v-else-if="error" :error="error" />

          <div v-else-if="filteredProducts.length > 0" class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            <ProductCard v-for="product in filteredProducts" :key="product.id" :product="product" />
          </div>

          <ProductNoFound v-else @clear-filter="productsStore.clearCategoryFilter" />
        </main>
      </div>
    </div>
  </div>
</template>
