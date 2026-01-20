import type { RouteLocationRaw } from 'vue-router'

export const PRODUCT_DETAIL_LINK = {
  name: 'product-id',
} as const satisfies RouteLocationRaw

export const CART_LINK = {
  name: 'cart',
} as const satisfies RouteLocationRaw

export const PROFILE_LINK = {
  name: 'profile',
} as const satisfies RouteLocationRaw

export const ORDERS_LINK = {
  name: 'orders',
} as const satisfies RouteLocationRaw

export const POSTS_LINK = {
  name: 'posts',
} as const satisfies RouteLocationRaw

export const HOME_LINK = {
  name: 'index',
} as const satisfies RouteLocationRaw
