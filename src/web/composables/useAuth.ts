export function useAuth() {
    const token = ref<string | null>(null)
  
    const login = async (username: string) => {
      try {
        const response = await $fetch<{ access_token: string, token_type: string }>('http://localhost:8000/login', {
          method: 'POST',
          body: { username }
        })
        token.value = response.access_token
        localStorage.setItem('token', response.access_token)
      } catch (error) {
        console.error('Login failed:', error)
      }
    }
  
    const logout = () => {
      token.value = null
      localStorage.removeItem('token')
    }
  
    const getToken = () => {
      if (!token.value) {
        token.value = localStorage.getItem('token')
      }
      return token.value
    }
  
    return { login, logout, getToken }
  }