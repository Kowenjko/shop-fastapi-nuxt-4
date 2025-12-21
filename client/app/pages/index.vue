<script lang="ts" setup>
const productsStore = useProductsStore()

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
</script>

<template>
  <div class="min-h-screen bg-white">
    <div class="mx-auto max-w-7xl px-4 py-8">
      <TitlePage title="Product Catalog" description="Discover our amazing products" />

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
