<template>
    <section>
        <button
            type="button"
            class="btn btn-success"
            v-on:click="isShow = !isShow"
            id="create-button"
        >
            Create task
        </button>
        <div v-if="isShow">
            <form ref="anyName" @submit.prevent="submit">
                <div class="mb-3">
                    <label for="name" class="form-label">Name</label>
                    <input
                        type="text"
                        name="name"
                        v-model="name"
                        class="form-control"
                    />
                </div>
                <div class="mb-3">
                    <label for="completed" class="form-label">Completed</label>
                    <select class="form-select" v-model="completed">
                        <option value="false">False</option>
                        <option value="true">True</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
            <br />
        </div>
    </section>
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

<style lang="less" scoped>
#create-button {
    margin-bottom: 1em;
}
</style>
