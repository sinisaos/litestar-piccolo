import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'

import tasks from './modules/tasks'
import users from './modules/users'


Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    tasks,
    users,
  },
  plugins: [new VuexPersistence().plugin]
})
