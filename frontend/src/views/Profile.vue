<template>
    <div class="container">
        <h2>Profile</h2>
        <ul class="list-group" v-if="loggedUser">
            <li
                class="
                    list-group-item
                    d-flex
                    justify-content-between
                    align-items-center
                "
            >
                <strong>Username</strong>
                <span>{{ loggedUser.user.username }}</span>
            </li>
            <li
                class="
                    list-group-item
                    d-flex
                    justify-content-between
                    align-items-center
                "
            >
                <strong>Email</strong>
                <span>{{ loggedUser.user.email }}</span>
            </li>
            <li
                class="
                    list-group-item
                    d-flex
                    justify-content-between
                    align-items-center
                "
            >
                <strong>Last login</strong>
                <span>{{
                    loggedUser.user.last_login.slice(0, -7).replace("T", " ")
                }}</span>
            </li>
            <li
                class="
                    list-group-item
                    d-flex
                    justify-content-between
                    align-items-center
                "
            >
                <strong
                    ><router-link to="/dashboard">Tasks</router-link></strong
                >
                <span class="badge bg-primary rounded-pill">{{
                    tasks.length
                }}</span>
            </li>
            <li
                class="
                    list-group-item
                    d-flex
                    justify-content-between
                    align-items-center
                "
            >
                <button v-on:click="deleteAccount()" class="btn btn-danger">
                    Delete Account
                </button>
            </li>
        </ul>
    </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

export default {
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
}
</script>
