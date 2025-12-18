import type { RouteLocationRaw } from "vue-router";

export const PRODUCT_DETAIL_LINK = {
  name: "product-id",
} as const satisfies RouteLocationRaw;

export const CART_LINK = {
  name: "cart",
} as const satisfies RouteLocationRaw;

export const ABOUT_LINK = {
  name: "about",
} as const satisfies RouteLocationRaw;

export const HOME_LINK = {
  name: "index",
} as const satisfies RouteLocationRaw;
