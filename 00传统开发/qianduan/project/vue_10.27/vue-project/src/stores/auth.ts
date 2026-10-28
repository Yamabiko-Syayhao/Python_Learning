import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { loginAccount } from '@/api/admin'
import { clearSession, readSession, writeSession } from '@/utils/authSession'
import type { LoginPayload } from '@/types/admin'

export const useAuthStore = defineStore('auth', () => {
  const session = ref(readSession())
  const user = computed(() =>
    session.value ? { ...session.value, username: session.value.userName } : null,
  )
  const isAuthenticated = computed(() => Boolean(session.value?.token))

  async function login(payload: LoginPayload) {
    const result = await loginAccount(payload)
    writeSession(result)
    session.value = result
    return result
  }

  function logout() {
    clearSession()
    session.value = null
  }

  return { user, isAuthenticated, login, logout }
})
