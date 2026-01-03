export function useOrdersSocket(token: string) {
  let socket: WebSocket | null = null

  const connect = () => {
    socket = new WebSocket(`wss://api.shop.local/ws/orders?token=${token}`)

    socket.onopen = () => {
      console.log('WS connected')
    }

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      console.log('Order event:', data)
    }

    socket.onclose = () => {
      console.log('WS closed, reconnecting...')
      setTimeout(connect, 3000)
    }
  }

  onMounted(connect)

  onBeforeUnmount(() => socket?.close())
}
