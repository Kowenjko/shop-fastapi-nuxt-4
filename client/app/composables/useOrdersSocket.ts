import { toast } from 'vue-sonner'

let socket: WebSocket | null = null
let connecting = false

export function useOrdersSocket() {
  const authStore = useAuthStore()

  const connect = () => {
    // защита от повторных подключений
    if (socket || connecting) return
    if (!authStore.token) return

    connecting = true

    socket = new WebSocket(`wss://api.shop.local/ws/orders?token=${authStore.token}`)

    socket.onopen = () => {
      connecting = false
      console.log('🟢 WS connected')
    }

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log('📦 Order event:', data)
        toast.info(`Change status order #${data.order_id} to "${data.new_status}"`)
      } catch (e) {
        console.error('WS parse error', e)
      }
    }

    socket.onclose = () => {
      console.log('🔴 WS closed, reconnecting...')
      socket = null
      connecting = false

      // мягкий reconnect
      setTimeout(connect, 3000)
    }

    socket.onerror = () => {
      socket?.close()
    }
  }

  // подключаемся один раз на клиенте
  if (process.client) {
    onMounted(connect)
  }
}
