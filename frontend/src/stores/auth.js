import { defineStore } from 'pinia'
import { demoLogin } from '../api/nexto'

// 데모 세션 토큰 관리
export const useAuthStore = defineStore('auth', {
  state: () => ({ token: localStorage.getItem('nexto_token') }),
  actions: {
    async ensureSession() {
      if (this.token) return
      const { token } = await demoLogin()
      this.token = token; localStorage.setItem('nexto_token', token)
    }
  }
})
