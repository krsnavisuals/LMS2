<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <router-link
        class="navbar-brand fw-medium fs-3 d-flex justify-content-center align-items-center gap-2"
        :to="{ name: 'LibrarianDashboard' }"
      >
        <v-icon name="io-library" scale="2.3"></v-icon>
        Library Management System
      </router-link>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link active-class="active" class="nav-link" :to="{ name: 'LibrarianDashboard' }"
              >Sections Dashboard</router-link
            >
          </li>
          <li class="nav-item">
            <router-link
              active-class="active"
              class="nav-link"
              :to="{ name: 'LibrarianEbookDashboard' }"
              >Ebook Dashboard</router-link
            >
          </li>
          <li class="nav-item">
            <router-link active-class="active" class="nav-link" :to="{ name: 'LibrarianRequest' }"
              >Request</router-link
            >
          </li>
        </ul>
        <form class="d-flex">
          <div class="text-white d-flex align-items-center px-4 gap-1">
            <v-icon name="io-person-circle" scale="2"></v-icon>
            <span class="text-capitalize fs-4">{{ authStore.user.username }}</span>
          </div>
          <button class="btn btn-secondary me-2" @click="goToStats">Stats</button>
          <button class="btn btn-danger" @click="logout">Logout</button>
        </form>
      </div>
    </div>
  </nav>
</template>

<script setup>
import axiosInstance from '@/axios'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'
import { push } from 'notivue'
const authStore = useAuthStore()
console.log('axiosInstance:', axiosInstance)

const logout = () => {
  authStore.logout()
  router.push('/')
  push.success('Logout successful')
}

const goToStats = () => {
  router.push({ name: 'LibrarianStats' })
}
</script>
