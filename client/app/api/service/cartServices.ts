export const cartAPI = {
  async getCart(cartData: { cart: CartI }) {
    const { $api } = useNuxtApp()
    return await $api<ResponseCartI>(CART, {
      method: 'POST',
      body: { cart: cartData.cart },
    })
  },

  async addItem(item: AddToCartI, cartData: CartI) {
    const { $api } = useNuxtApp()
    return await $api<{ cart: CartI }>(CART + ADD, {
      method: 'POST',
      body: { product_id: item.product_id, quantity: item.quantity, cart: cartData },
    })
  },

  async updateItem(item: AddToCartI, cartData: CartI) {
    const { $api } = useNuxtApp()
    return await $api<{ cart: CartI }>(CART + UPDATE, {
      method: 'PUT',
      body: { product_id: item.product_id, quantity: item.quantity, cart: cartData },
    })
  },

  async removeItem(productId: number, cartData: CartI) {
    const { $api } = useNuxtApp()
    return await $api<{ cart: CartI }>(CART + REMOVE + productId + '/', {
      method: 'DELETE',
      body: { cart: cartData },
    })
  },
}
