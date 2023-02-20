<template>
    <div class="container">
        <div class="row row-cols-1 row-cols-md-3 g-2">
            <div v-for="(task, index) in tasks" :key="index">
                <div class="card p-2 mb-4 rounded">
                    <div class="card-body">
                        <p class="mb-0">
                            Posted by
                            <span
                                ><b>{{ task.readable }}</b>
                                <vue-moments-ago
                                    prefix=""
                                    suffix="ago"
                                    :date="task.created_at"
                                ></vue-moments-ago
                            ></span>
                        </p>
                        <h2>
                            {{ task.name }}
                        </h2>
                        <p class="mb-0">Completed - {{ task.completed }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import axios from "axios"
import VueMomentsAgo from "vue-moments-ago"

export default {
    data() {
        return {
            tasks: []
        }
    },
    components: {
        VueMomentsAgo
    },
    computed: {
        isLoggedIn() {
            return this.$store.getters.isAuthenticated
        }
    },
    methods: {
        async getTasks() {
            let response = await axios.get("api/tasks")
            this.tasks = response.data
            return this.tasks
        }
    },
    mounted() {
        this.getTasks()
    }
}
</script>

<style lang="less" scoped>
.vue-moments-ago {
    font-size: 1rem;
}
</style>
