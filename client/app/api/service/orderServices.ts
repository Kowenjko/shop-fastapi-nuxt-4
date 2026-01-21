export const orderAPI = {
  async create(body: OrderCreateI) {
    const { $api } = useNuxtApp()
    return await $api<OrderI>(ORDERS, { method: 'POST', body })
  },

  async addProduct(body: OrderAddProductI) {
    const { $api } = useNuxtApp()
    return await $api<OrderI>(POSTS + PRODUCT, { method: 'POST', body })
  },

  async addProducts(body: OrderAddProductsI) {
    const { $api } = useNuxtApp()
    return await $api<OrderI>(POSTS + PRODUCTS, { method: 'POST', body })
  },

  async replaceProducts(body: OrderAddProductsI) {
    const { $api } = useNuxtApp()
    return await $api<OrderI>(POSTS + PRODUCTS, { method: 'PUT', body })
  },

  async updateProductCount(body: OrderUpdateCountI) {
    const { $api } = useNuxtApp()
    return await $api<OrderI>(POSTS + PRODUCTS, { method: 'PATCH', body })
  },

  async removeProduct(body: OrderRemoveProductI) {
    const { $api } = useNuxtApp()
    return await $api<OrderI>(POSTS + PRODUCTS, { method: 'DELETE', body })
  },

  async checkout(body: OrderChangeStatusI) {
    const { $api } = useNuxtApp()
    return await $api<OrderI>(POSTS + CHECKOUT, { method: 'POST', body })
  },

  async cancel(body: OrderChangeStatusI) {
    const { $api } = useNuxtApp()
    return await $api<OrderI>(POSTS + CANCEL, { method: 'POST', body })
  },
}
