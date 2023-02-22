import axios from 'axios'

const state = {
  tasks: undefined,
  task: undefined
}

const getters = {
  stateTasks: state => state.tasks,
  stateTask: state => state.task,
}

const actions = {
  async createTask(context, task) {
    await axios.post('api/tasks', task)
    context.dispatch('userTasks')
  },
  async singleTask(context, id) {
    const response = await axios.get(`api/tasks/${id}`)
    context.commit('setTask', response.data)
  },
  async updateTask(context, task) {
    await axios.patch(`api/tasks/${task.id}`, task.form)
    context.dispatch('userTasks')
  },
  async deleteTask(context, id) {
    await axios.delete(`api/tasks/${id}`)
    context.dispatch('userTasks')
  }
}

const mutations = {
  setTasks(state, tasks) {
    state.tasks = tasks
  },
  setTask(state, task) {
    state.task = task
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
