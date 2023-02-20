<template>
    <div class="container">
        <h2>Edit task</h2>
        <hr />
        <div v-if="task">
            <form @submit.prevent="submit">
                <div class="mb-3">
                    <label for="name" class="form-label">Name</label>
                    <input
                        type="text"
                        name="name"
                        v-model="form.name"
                        class="form-control"
                    />
                </div>
                <div class="mb-3">
                    <label for="completed" class="form-label">Completed</label>
                    <select class="form-select" v-model="form.completed">
                        <option value="false">False</option>
                        <option value="true">True</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </div>
    </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

export default {
    props: ["id"],
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
}
</script>
