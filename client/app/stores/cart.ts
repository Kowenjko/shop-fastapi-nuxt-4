import { defineStore } from 'pinia'
import { cartAPI } from '@/api'

const CART_STORAGE_KEY = 'shopping_cart'

export const useCartStore = defineStore(
  'cart',
  () => {
    const cartItems = ref<CartI>({})

    const cartDetails = ref<ResponseCartI | null>(null)
    const loading = ref(false)

    const itemsCount = computed(() => {
      return Object.values(cartItems.value).reduce((sum, qty) => sum + qty, 0)
    })

    const totalPrice = computed(() => {
      return cartDetails.value?.total || 0
    })

    const hasItems = computed(() => {
      return Object.keys(cartItems.value).length > 0
    })

    /**
     * Получить детальную информацию о корзине
     */
    const fetchCartDetails = async () => {
      if (!hasItems.value) {
        cartDetails.value = { items: [], total: 0, items_count: 0 }
        return
      }

      loading.value = true
      try {
        const response = await cartAPI.getCart({ cart: cartItems.value })
        cartDetails.value = response
      } catch (err) {
        console.error('Error fetching cart details:', err)
      } finally {
        loading.value = false
      }
    }

    /**
     * Добавить товар в корзину
     */
    const addToCart = async (productId: number, quantity = 1) => {
      try {
        const item = {
          product_id: productId,
          quantity: quantity,
        }
        const response = await cartAPI.addItem(item, cartItems.value)
        cartItems.value = response.cart

        await fetchCartDetails()
        return true
      } catch (err) {
        console.error('Error adding to cart:', err)
        return false
      }
    }

    /**
     * Удалить товар из корзины
     */
    const removeFromCart = async (productId: number) => {
      try {
        const response = await cartAPI.removeItem(productId, cartItems.value)
        cartItems.value = response.cart

        await fetchCartDetails()
        return true
      } catch (err) {
        console.error('Error removing from cart:', err)
        return false
      }
    }

    /**
     * Обновить количество товара
     */
    const updateQuantity = async (productId: number, quantity: number) => {
      if (quantity <= 0) {
        return removeFromCart(productId)
      }

      try {
        const item = {
          product_id: productId,
          quantity: quantity,
        }
        const response = await cartAPI.updateItem(item, cartItems.value)
        cartItems.value = response.cart

        await fetchCartDetails()
        return true
      } catch (err) {
        console.error('Error updating cart:', err)
        return false
      }
    }

    const clearCart = () => {
      cartItems.value = {}
      cartDetails.value = null
    }

    return {
      // State
      cartItems,
      cartDetails,
      loading,
      // Getters
      itemsCount,
      totalPrice,
      hasItems,
      // Actions
      addToCart,
      fetchCartDetails,
      updateQuantity,
      removeFromCart,
      clearCart,
    }
  },
  {
    persist: {
      storage: piniaPluginPersistedstate.localStorage(),
      key: CART_STORAGE_KEY,
      pick: ['cartItems'],
    },
  },
)
