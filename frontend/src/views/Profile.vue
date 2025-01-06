<template>
    <div class="container mx-auto py-10 my-13">
        <div class="card shadow">
            <div class="card-body">
                <h5 class="card-title mb-2.5">User profile</h5>
                <ul v-if="loggedUser" class="divide-base-content/25 divide-y">
                    <li class="w-72 p-3">
                        <strong>Username </strong>
                        <span>{{ loggedUser.user.username }}</span>
                    </li>
                    <li class="p-3">
                        <strong>Email </strong>
                        <span>{{ loggedUser.user.email }}</span>
                    </li>
                    <li class="p-3">
                        <strong>Last login </strong>
                        <span>{{
                            loggedUser.user.last_login
                                .slice(0, -7)
                                .replace("T", " ")
                        }}</span>
                    </li>
                    <li class="p-3">
                        <strong
                            ><router-link to="/dashboard"
                                >Tasks
                            </router-link></strong
                        >
                        <span
                            class="badge badge-soft badge-info badge-md ms-2 rounded-full"
                            >{{ tasks?.length }}</span
                        >
                    </li>
                    <li class="py-2">
                        <button
                            v-on:click="deleteAccount()"
                            class="btn btn-error"
                        >
                            Delete Account
                        </button>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
import { defineComponent } from "vue"
import { mapGetters, mapActions } from "vuex"

export default defineComponent({
    computed: {
        ...mapGetters({ loggedUser: "stateUser", tasks: "stateTasks" })
    },
    methods: {
        ...mapActions(["deleteUser"]),
        async deleteAccount() {
            if (confirm("Are you sure you want to delete the account!"))
                try {
                    await this.deleteUser(this.loggedUser.user.id)
                    await this.$store.dispatch("logoutUser")
                    this.$router.push("/")
                } catch (error) {
                    console.error(error)
                }
        }
    },
    mounted() {
        this.$store.dispatch("userTasks")
        this.$store.dispatch("userProfile")
    }
})
</script>
