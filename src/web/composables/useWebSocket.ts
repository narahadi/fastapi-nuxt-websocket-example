export function useWebSocket() {
    const socket = ref<WebSocket | null>(null)
    const messages = ref<string[]>([])
    const hasNotification = ref(false)
    const { getToken } = useAuth()
  
    const connectWebSocket = () => {
      const token = getToken()
      if (!token) {
        console.error('No token available')
        return
      }
  
      socket.value = new WebSocket(`ws://localhost:8000/ws?token=${token}`)
      
      socket.value.onopen = () => {
        console.log('WebSocket connected')
      }
  
      socket.value.onmessage = (event) => {
        console.log('Received message:', event.data)
        messages.value.push(event.data)
        hasNotification.value = true
      }
  
      socket.value.onclose = (event) => {
        console.log(`WebSocket disconnected: ${event.code} ${event.reason}`)
      }
  
      socket.value.onerror = (error) => {
        console.error('WebSocket error:', error)
      }
    }
  
    onMounted(() => {
      connectWebSocket()
    })
  
    onUnmounted(() => {
      if (socket.value) {
        socket.value.close()
      }
    })
  
    return {
      messages,
      hasNotification
    }
  }