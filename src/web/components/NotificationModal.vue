<script setup lang="ts">
defineProps<{
  isOpen: boolean
  message: string
}>()

const emit = defineEmits(['close'])

const close = () => {
  emit('close')
}
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
    <div class="p-8 bg-white rounded shadow-md">
      <h2 class="mb-4 text-xl font-bold">Notification</h2>
      <p class="mb-4">{{ message }}</p>
      <button @click="close" class="px-4 py-2 text-white bg-blue-500 rounded hover:bg-blue-600">Close</button>
    </div>
  </div>
</template>