<template>
    <div class="container mx-auto py-10 my-15">
        <div class="card shadow">
            <div class="card-body">
                <h4 class="card-title mb-2.5">Edit task</h4>
                <div v-if="task">
                    <form @submit.prevent="submit">
                        <div class="mb-3">
                            <label class="label label-text" for="name"
                                >Name</label
                            >
                            <input
                                type="text"
                                name="name"
                                v-model="form.name"
                                class="input max-w-lg"
                            />
                        </div>
                        <div class="mb-3">
                            <label class="label label-text" for="completed"
                                >Completed</label
                            >
                            <select
                                class="select max-w-lg appearance-none"
                                aria-label="select"
                                v-model="form.completed"
                            >
                                <option value="false">False</option>
                                <option value="true">True</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary">
                            Submit
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { defineComponent } from "vue"
import { mapGetters, mapActions } from "vuex"

export default defineComponent({
    props: {
        id: [Number, String],
        required: true
    },
    data() {
        return {
            form: {
                name: "",
                completed: ""
            }
        }
    },
    computed: {
        ...mapGetters({ user: "stateUser", task: "stateTask" })
    },
    methods: {
        ...mapActions(["updateTask", "singleTask"]),
        async submit() {
            let data = {
                id: this.id,
                form: this.form
            }
            try {
                await this.updateTask(data)
                this.$store.dispatch("userTasks")
                this.$router.push("/dashboard")
            } catch (error) {
                console.error(error)
            }
        },
        async getTask() {
            try {
                await this.singleTask(this.id)
                this.form.name = this.task.name
                this.form.completed = this.task.completed
                this.form.created_at = this.task.created_at
                this.form.task_user = this.task.task_user
            } catch (error) {
                console.error(error)
            }
        }
    },
    mounted() {
        this.getTask()
    }
})
</script>
