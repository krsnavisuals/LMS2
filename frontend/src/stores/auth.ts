import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axiosInstance from '@/axios'
import {
  loginUser as apiLoginUser,
  loginLibrarian as apiLoginLibrarian,
  registerUser as apiRegisterUser
} from '@/api/auth'
import { getIdentityFromToken } from '@/utils/jwt'

export interface User {
  id: number
  username: string
  role: string
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token') || null)
  const user = ref<User | null>(getIdentityFromToken(token.value) || null)

  const isGuest = computed(() => !token.value)
  const isLibrarian = computed(() => user.value && user.value.role == 'librarian' && token.value)
  const isUser = computed(() => user.value && user.value.role == 'user' && token.value)

  const loginUser = async (username: string, password: string) => {
    try {
      const response = await apiLoginUser(username, password)
      token.value = response.token
      user.value = response.user
      if (token.value) localStorage.setItem('token', token.value)
      axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      axiosInstance.defaults.headers['Authorization'] = `Bearer ${token.value}`
      return true
    } catch (error) {
      console.error('Login failed:', error)
      return false
    }
  }
  const registerUser = async (username: string, password: string) => {
    try {
      const response = await apiRegisterUser(username, password)
      token.value = response.token
      user.value = response.user
      if (token.value) localStorage.setItem('token', token.value)
      axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      axiosInstance.defaults.headers['Authorization'] = `Bearer ${token.value}`
      return true
    } catch (error) {
      console.error('Registration failed:', error)
      return false
    }
  }
  const loginLibrarian = async (username: string, password: string) => {
    try {
      const response = await apiLoginLibrarian(username, password)
      token.value = response.token
      user.value = response.user
      if (token.value) localStorage.setItem('token', token.value)
      axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      axiosInstance.defaults.headers['Authorization'] = `Bearer ${token.value}`
      return true
    } catch (error) {
      console.error('Login failed:', error)
      return false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    axiosInstance.defaults.headers.common['Authorization'] = ``
    axiosInstance.defaults.headers['Authorization'] = ``
  }

  return {
    user,
    token,
    isGuest,
    isLibrarian,
    isUser,
    loginLibrarian,
    loginUser,
    registerUser,
    logout
    // checkAuth
  }
})
