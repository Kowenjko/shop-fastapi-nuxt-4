import { defineStore } from 'pinia'

export const useModalStore = defineStore('modals', () => {
  const modalProceedCart = reactive<any>({ show: false, content: null })
  const modalClearCart = reactive({ show: false, content: null })
  const modalLoginIn = reactive({ show: false, content: null })
  const modalRegister = reactive({ show: false, content: null })
  const modalPost = reactive<any>({ show: false, content: null })

  return {
    modalProceedCart,
    modalClearCart,
    modalLoginIn,
    modalRegister,
    modalPost,
  }
})
