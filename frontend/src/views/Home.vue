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
                                <i> on {{ formatDate(task.created_at) }}</i>
                            </span>
                        </p>
                        <h2>
                            {{ task.name }}
                        </h2>
                        <p class="mb-0">Completed - {{ task.completed }}</p>
                    </div>
                </div>
            </div>
        </div>
        <nav aria-label="page navigation" v-if="tasks.length > 0">
            <ul class="pagination justify-content-center">
                <li class="page-item" v-bind:class="{ disabled: page === 1 }">
                    <a
                        v-on:click.prevent="getTasks(page - 1)"
                        tabindex="-1"
                        class="page-link"
                        href=""
                        >Previous</a
                    >
                </li>
                <li class="page-item" :key="n" v-for="n in totalPages">
                    <a
                        v-bind:class="{ active: n === page }"
                        v-on:click.prevent="getTasks(n)"
                        class="page-link"
                        href=""
                        >{{ n }}</a
                    >
                </li>
                <li
                    class="page-item"
                    v-bind:class="{ disabled: page === totalPages }"
                >
                    <a
                        v-on:click.prevent="getTasks(page + 1)"
                        class="page-link"
                        href=""
                        >Next</a
                    >
                </li>
            </ul>
        </nav>
    </div>
</template>
<script>
import axios from "axios"
import dayjs from "dayjs"
import { defineComponent } from "vue"

export default defineComponent({
    data() {
        return {
            tasks: [],
            page: 1,
            page_size: 15,
            totalPages: 0
        }
    },
    computed: {
        isLoggedIn() {
            return this.$store.getters.isAuthenticated
        }
    },
    methods: {
        formatDate(dateString) {
            const date = dayjs(dateString)
            return date.format("MMMM D, YYYY")
        },
        async getTasks(pageNumber) {
            let response = await axios.get(
                `api/tasks?page=${pageNumber}&page_size=${this.page_size}`
            )
            this.tasks = response.data.tasks
            this.page = response.data.page
            this.page_size = response.data.page_size
            this.totalPages = response.data.total
            return this.tasks
        }
    },
    async mounted() {
        await this.getTasks(this.page)
    }
})
</script>

