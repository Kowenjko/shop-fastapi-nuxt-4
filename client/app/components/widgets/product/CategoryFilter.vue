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
  <Card>
    <CardHeader>
      <CardTitle> Categories </CardTitle>
    </CardHeader>

    <CardContent>
      <ul class="space-y-2">
        <li>
          <Button
            @click="selectCategory(null)"
            class="flex w-full justify-between"
            size="lg"
            :variant="productsStore.selectedCategory ? 'ghost' : 'default'"
          >
            <span>All Categories</span>
            <span v-if="!productsStore.selectedCategory">({{ totalProductsCount }})</span>
          </Button>
        </li>

        <li v-for="category in categories" :key="category.id">
          <Button
            @click="selectCategory(category.id!)"
            class="flex w-full justify-between"
            size="lg"
            :variant="productsStore.selectedCategory === category.id ? 'default' : 'ghost'"
          >
            <span>{{ category.name }}</span>
            <span v-if="productsStore.selectedCategory === category.id">({{ productsCount }})</span>
          </Button>
        </li>
      </ul>
    </CardContent>
  </Card>
</template>
