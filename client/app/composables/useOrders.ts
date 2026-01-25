import { orderAPI } from '@/api'
import { toast } from 'vue-sonner'

export const useOrders = async () => {
  const updating = ref(false)

  const { data: orders, refresh } = await useAPI<OrderI[]>(BASE_API + ORDERS + USER, { key: 'orders' })

  const cancelOrder = async (order_id: number) => {
    try {
      await orderAPI.cancel({ order_id })
      await refresh()
    } catch (error) {
      console.log(error)
    }
  }
  const checkoutOrder = async (order_id: number) => {
    try {
      await orderAPI.checkout({ order_id })
      await refresh()
    } catch (error) {
      console.log(error)
    }
  }

  const increaseQuantity = async (order_id: number, product_id: number, count: number) => {
    updating.value = true

    try {
      await orderAPI.updateProductCount({ order_id, product_id, count: count + 1 })
      await refresh()
      toast.info('Updating quantity product in order')
    } catch (error) {
    } finally {
      updating.value = false
    }
  }

  const decreaseQuantity = async (order_id: number, product_id: number, count: number) => {
    updating.value = true

    try {
      if (count > 1) {
        await orderAPI.updateProductCount({ order_id, product_id, count: count - 1 })
        toast.info('Updating quantity product in order')
      } else {
        await orderAPI.removeProduct({ order_id, product_id })
        toast.warning('Deleted product from order')
      }
      await refresh()
    } catch (error) {
      console.log(error)
    } finally {
      updating.value = false
    }
  }

  const handleRemove = async (order_id: number, product_id: number) => {
    updating.value = true

    await orderAPI.removeProduct({ order_id, product_id })
    await refresh()
    toast.warning('Deleted product from order')
    try {
    } catch (error) {
      console.log(error)
    } finally {
      updating.value = false
    }
  }

  return {
    orders,
    cancelOrder,
    checkoutOrder,
    increaseQuantity,
    decreaseQuantity,
    handleRemove,
    updating,
  }
}
