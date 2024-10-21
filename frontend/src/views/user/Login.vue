<template>
  <div class="d-flex" style="height: 80vh">
    <div class="container align-self-center">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card shadow rounded-2">
            <div class="card-header">
              <h3 class="text-center">User Login</h3>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" class="form-control" id="username" v-model="username" required />
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="password"
                  required
                />
              </div>
              <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary w-50" @click="login">Login</button>
                <button type="submit" class="btn btn-warning w-50" @click="register">
                  Register
                </button>
              </div>
              <p class="text-end mt-2">
                Not a user? click
                <router-link class="" to="/librarian-login">here</router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'
import { push } from 'notivue'

const username = ref('')
const password = ref('')
const authStore = useAuthStore()

const login = async () => {
  if (await authStore.loginUser(username.value, password.value)) {
    router.push({ name: 'UserCatalog' })
    push.success('Login successful')
  }
}

const register = async () => {
  if (await authStore.registerUser(username.value, password.value)) {
    await authStore.loginUser(username.value, password.value)
    router.push({ name: 'UserCatalog' })
    push.success('Login successful')
  }
}
</script>
