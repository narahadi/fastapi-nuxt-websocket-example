<script setup lang="ts">
const username = ref('')
const { login } = useAuth()
const router = useRouter()

const handleLogin = async () => {
  if (username.value.trim()) {
    await login(username.value.trim())
    router.push('/')
  }
}
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
    <div class="p-8 bg-white rounded shadow-md">
      <h1 class="mb-4 text-2xl font-bold">Login</h1>
      <input v-model="username" placeholder="Enter your name" class="w-full p-2 mb-4 border rounded" />
      <button @click="handleLogin" class="w-full p-2 text-white bg-blue-500 rounded hover:bg-blue-600">Enter</button>
    </div>
  </div>
</template>