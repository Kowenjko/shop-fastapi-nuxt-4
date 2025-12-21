<script lang="ts" setup>
const {
  totalProductsCount = 0,
  categories,
  productsCount,
} = defineProps<{ totalProductsCount: number; categories?: CategoryI[]; productsCount: number }>()

const productsStore = useProductsStore()

const selectCategory = (categoryId: number | null) => {
  if (categoryId === null) {
    productsStore.clearCategoryFilter()
  } else {
    productsStore.setCategory(categoryId)
  }
}
</script>

<template>
  <div class="rounded-lg border-2 border-gray-200 bg-white p-6">
    <h2 class="mb-6 text-2xl font-bold text-black">Categories</h2>

    <ul class="space-y-2">
      <li>
        <ButtonCategory
          :is-active="!productsStore.selectedCategory"
          name="All Categories"
          :count="totalProductsCount"
          @select-category="selectCategory(null)"
        />
      </li>

      <li v-for="category in categories" :key="category.id">
        <ButtonCategory
          :is-active="productsStore.selectedCategory === category.id"
          :name="category.name"
          :count="productsCount"
          @select-category="selectCategory(category.id!)"
        />
      </li>
    </ul>
  </div>
</template>
