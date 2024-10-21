import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

import { createBootstrap } from 'bootstrap-vue-next'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'
app.use(createBootstrap())

import * as IoIcons from 'oh-vue-icons/icons/io'
import * as HiIcons from 'oh-vue-icons/icons/hi'
import { OhVueIcon, addIcons } from 'oh-vue-icons'
const Io = Object.values({ ...IoIcons })
const Hi = Object.values({ ...HiIcons })
app.component('v-icon', OhVueIcon)
addIcons(...Io)
addIcons(...Hi)

// Notivue - for handling toast
import { createNotivue, push } from 'notivue'
import 'notivue/notification.css' // Only needed if using built-in notifications
import 'notivue/animations.css' // Only needed if using built-in animations
const notivue = createNotivue({
  position: 'bottom-right'
})
app.use(notivue)

app.mount('#app')

import axiosInstance from './axios'
axiosInstance.interceptors.response.use(
  function (response) {
    return response
  },
  function (error) {
    console.log('error:', error)
    push.error({
      title: 'Something went wrong',
      message: error.response.data.message
    })
    return Promise.reject(error)
  }
)
