<template>
    <div>
        <div class="flex flex-wrap justify-center mt-10">
            <div v-for="(task, index) in tasks" :key="index">
                <div class="card size-64 mx-2 my-2 p-5">
                    <div class="card-body">
                        <h2 class="card-title">
                            {{ task.name }}
                        </h2>
                        <p class="p-2">
                            Posted by
                            <span
                                ><b>{{ task.readable }}</b>
                                <i> on {{ formatDate(task.created_at) }}</i>
                            </span>
                        </p>
                        <p class="p-3">Completed - {{ task.completed }}</p>
                    </div>
                </div>
            </div>
        </div>
        <div
            v-if="tasks?.length > 0"
            class="flex flex-wrap justify-center mt-10 my-10"
        >
            <nav class="flex items-center gap-x-1 col-start-3 col-span-4">
                <button
                    type="button"
                    class="btn btn-outline"
                    v-bind:class="{ disabled: page === 1 }"
                    v-on:click.prevent="getTasks(page - 1)"
                    tabindex="-1"
                    href="#"
                >
                    Previous
                </button>
                <div class="flex items-center gap-x-1">
                    <button
                        type="button"
                        class="btn btn-outline btn-square aria-[current='page']:text-border-primary aria-[current='page']:bg-primary/10"
                        :key="n"
                        v-for="n in totalPages"
                        v-bind:class="{ active: n === page }"
                        v-on:click.prevent="getTasks(n)"
                        href="#"
                    >
                        {{ n }}
                    </button>
                </div>
                <button
                    type="button"
                    class="btn btn-outline"
                    v-bind:class="{ disabled: page === totalPages }"
                    v-on:click.prevent="getTasks(page + 1)"
                    href="#"
                >
                    Next
                </button>
            </nav>
        </div>
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
