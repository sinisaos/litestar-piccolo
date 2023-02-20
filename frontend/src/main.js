import 'bootstrap/dist/css/bootstrap.css'
import axios from 'axios'
import Vue from 'vue'
import Vuelidate from 'vuelidate'
import Cookies from "js-cookie"

import App from './App.vue'
import router from './router'
import store from './store'

Vue.use(Vuelidate)

axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:8000/'

Vue.config.productionTip = false

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

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
