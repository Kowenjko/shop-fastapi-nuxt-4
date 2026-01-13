<script lang="ts" setup>
const modalStore = useModalStore()
</script>

<template>
  <Dialog v-model:open="modalStore.modalProceedCart.show">
    <DialogContent class="sm:max-w-lg">
      <DialogHeader>
        <DialogTitle>Modal Proceed</DialogTitle>
      </DialogHeader>
      <div class="grid gap-4">Checkout functionality will be implemented soon!</div>
      <DialogFooter>
        <DialogClose as-child>
          <Button variant="outline"> Cancel </Button>
        </DialogClose>
        <Button>Proceed to Checkout</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
