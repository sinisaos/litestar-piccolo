import { createStore } from 'vuex'
import VuexPersistence from 'vuex-persist'

import tasks from './modules/tasks'
import users from './modules/users'


const vuexLocal = new VuexPersistence({
  storage: window.localStorage
})

export default createStore({
  modules: {
    tasks,
    users,
  },
  plugins: [vuexLocal.plugin]
})
