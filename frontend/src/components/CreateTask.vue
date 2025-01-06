<template>
    <div class="m-2">
        <button
            type="button"
            class="btn btn-success"
            v-on:click="isShow = !isShow"
        >
            Create task
        </button>
        <div v-if="isShow">
            <form @submit.prevent="submit">
                <div class="pt-3">
                    <label class="label label-text" for="name">Name</label>
                    <input
                        type="text"
                        name="name"
                        v-model="name"
                        class="input max-w-lg"
                    />
                </div>
                <div class="pt-3">
                    <label class="label label-text" for="completed"
                        >Completed</label
                    >
                    <select
                        class="select max-w-lg appearance-none"
                        aria-label="select"
                        v-model="completed"
                    >
                        <option value="false">False</option>
                        <option value="true">True</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary my-2">
                    Submit
                </button>
            </form>
            <br />
        </div>
    </div>
</template>

<script>
import { defineComponent } from "vue"
import { mapGetters, mapActions } from "vuex"

export default defineComponent({
    data() {
        return {
            name: "",
            completed: "",
            taskUser: undefined,
            isShow: false
        }
    },
    computed: {
        ...mapGetters({ user: "stateUser", tasks: "stateTasks" })
    },
    methods: {
        ...mapActions(["createTask"]),
        async submit() {
            let data = {
                name: this.name,
                completed: this.completed,
                task_user: this.user.user.id
            }
            await this.createTask(data)
            this.$store.dispatch("userTasks")
            this.isShow = false
            this.name = this.completed = this.created = ""
        }
    }
})
</script>