export interface OrderCreateI {
  promocode?: string
}

export interface OrderItemI {
  product_id: number
  name: string
  unit_price: number
  count: number
  total: number
}

export interface OrderI {
  id: number
  promocode: number
  status: string
  items: OrderItemI[]
  created_at: string
  total_items: number
  total_price: number
}

export interface OrderRemoveProductI {
  product_id: number
  order_id: number
}
export interface OrderAddProductI extends OrderRemoveProductI {
  count: number
}

export interface OrderAddProductsI {
  order_id: number
  products: Omit<OrderAddProductI, 'order_id'>[]
}

export interface OrderUpdateCountI extends OrderAddProductI {}

export interface OrderChangeStatusI {
  order_id: number
}
