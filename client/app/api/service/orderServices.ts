export const orderAPI = {
  async create(body: OrderCreateI) {
    const { $api } = useNuxtApp()
    return await $api<OrderI>(ORDERS, { method: 'POST', body })
  },

  async addProduct(body: OrderAddProductI) {
    const { $api } = useNuxtApp()
    return await $api<OrderI>(ORDERS + PRODUCT, { method: 'POST', body })
  },

  async addProducts(body: OrderAddProductsI) {
    const { $api } = useNuxtApp()
    return await $api<OrderI>(ORDERS + PRODUCTS, { method: 'POST', body })
  },

  async replaceProducts(body: OrderAddProductsI) {
    const { $api } = useNuxtApp()
    return await $api<OrderI>(ORDERS + PRODUCTS, { method: 'PUT', body })
  },

  async updateProductCount(body: OrderUpdateCountI) {
    const { $api } = useNuxtApp()
    return await $api<OrderI>(ORDERS + PRODUCTS, { method: 'PATCH', body })
  },

  async removeProduct(body: OrderRemoveProductI) {
    const { $api } = useNuxtApp()
    return await $api<OrderI>(ORDERS + PRODUCTS, { method: 'DELETE', body })
  },

  async checkout(body: OrderChangeStatusI) {
    const { $api } = useNuxtApp()
    return await $api<OrderI>(ORDERS + CHECKOUT, { method: 'POST', body })
  },

  async cancel(body: OrderChangeStatusI) {
    const { $api } = useNuxtApp()
    return await $api<OrderI>(ORDERS + CANCEL, { method: 'POST', body })
  },
}
