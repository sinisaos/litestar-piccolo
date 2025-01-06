import { createApp } from 'vue'
import axios from 'axios'
import Cookies from "js-cookie"
import './index.css'
import 'flyonui/flyonui'

import App from './App.vue'
import router from './router'
import store from './store'

axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:8000/'

// CSRF token
axios.interceptors.request.use(function (config) {
  if (
    ["POST", "PUT", "DELETE", "PATCH"].indexOf(
      config.method.toUpperCase()
    ) != -1
  ) {
    const csrfToken = Cookies.get("csrftoken")
    config.headers["X-CSRFToken"] = csrfToken
  }
  return config
})

axios.interceptors.response.use(undefined, function (error) {
  if (error) {
    const originalRequest = error.config
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      store.dispatch('logoutUser')
      return router.push('/login')
    }
  }
})

const app = createApp(App)
app.use(store)
app.use(router)
app.mount('#app')
