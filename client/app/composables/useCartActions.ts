import { ref } from "vue";

export const useCartActions = () => {
  const cartStore = useCartStore();
  const updating = ref(false);

  const increaseQuantity = async (item: CartItemI) => {
    // updating.value = true;
    // await cartStore.updateQuantity(item.product_id, item.quantity + 1);
    // updating.value = false;
  };

  const decreaseQuantity = async (item: CartItemI) => {
    updating.value = true;
    // if (item.quantity > 1) {
    //   await cartStore.updateQuantity(item.product_id, item.quantity - 1);
    // } else {
    //   await cartStore.removeFromCart(item.product_id);
    // }
    updating.value = false;
  };

  const handleRemove = async (item: CartItemI) => {
    updating.value = true;
    // await cartStore.removeFromCart(item.product_id);
    updating.value = false;
  };

  return { updating, increaseQuantity, decreaseQuantity, handleRemove };
};
