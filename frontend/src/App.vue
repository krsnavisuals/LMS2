<template>
  <div id="app">
    <navbar-guest v-if="authStore.isGuest"></navbar-guest>
    <navbar-librarian v-if="authStore.isLibrarian"></navbar-librarian>
    <navbar-user v-if="authStore.isUser"></navbar-user>
    <router-view></router-view>
  </div>

  <Notivue v-slot="item">
    <Notification :item="item" />
  </Notivue>
</template>

<script setup lang="ts">
import NavbarGuest from '@/components/NavbarGuest.vue'
import NavbarLibrarian from '@/components/librarian/Navbar.vue'
import NavbarUser from './components/user/Navbar.vue'
import { useAuthStore } from './stores/auth'
import { Notification, Notivue } from 'notivue'

const authStore = useAuthStore()
</script>
