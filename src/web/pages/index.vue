<script setup lang="ts">
const { getToken } = useAuth()
const showModal = ref(false)
const router = useRouter()

onMounted(() => {
  if (!getToken()) {
    router.push('/login')
  }
})

const { messages, hasNotification } = useWebSocket()

const startJob = async () => {
  try {
    await $fetch('http://localhost:8000/start-job', { 
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${getToken()}`
      }
    })
  } catch (error) {
    console.error('Error starting job:', error)
  }
}

const latestMessage = computed(() => {
  return messages.value[messages.value.length - 1] || ''
})

watchEffect(() => {
  if (hasNotification.value) {
    showModal.value = true
  }
})

const closeModal = () => {
  showModal.value = false
  hasNotification.value = false
}
</script>

<template>
  <div class="p-8">
    <h1 class="mb-4 text-2xl font-bold">Dashboard</h1>
    <button @click="startJob" class="px-4 py-2 text-white bg-blue-500 rounded hover:bg-blue-600">Start Background Job</button>
    <div v-if="hasNotification" @click="showModal = true" class="fixed top-5 right-5 cursor-pointer">
      🔔
    </div>
    <NotificationModal 
      :is-open="showModal" 
      :message="latestMessage" 
      @close="closeModal"
    />
    <div class="mt-4">
      <h2 class="text-xl font-bold">Messages:</h2>
      <ul>
        <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
      </ul>
    </div>
  </div>
</template>