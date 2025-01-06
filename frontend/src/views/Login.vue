<template>
    <div class="flex justify-center items-center py-20">
        <div class="card sm:max-w-sm">
            <div class="card">
                <div class="card-title text-center">
                    <h2 class="p-3">Login</h2>
                    <div
                        v-if="error"
                        v-on:click="error = false"
                        class="alert alert-soft alert-error removing:translate-x-5 removing:opacity-0 flex items-center gap-4 transition duration-300"
                        role="alert"
                        id="dismiss-alert1"
                    >
                        Incorrect username or password
                        <button
                            class="ms-auto leading-none"
                            data-remove-element="#dismiss-alert1"
                            aria-label="Close Button"
                        >
                            <span class="icon-[tabler--x] size-5"></span>
                        </button>
                    </div>
                </div>
                <div class="card-body">
                    <form @submit.prevent="submit">
                        <div class="mb-3">
                            <label for="username" class="form-label"
                                >Username:</label
                            >
                            <input
                                type="text"
                                name="username"
                                v-model="username"
                                class="input max-w-sm"
                            />
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label"
                                >Password:</label
                            >
                            <input
                                type="password"
                                name="password"
                                v-model="password"
                                class="input max-w-sm"
                            />
                        </div>
                        <button type="submit" class="btn btn-primary">
                            Submit
                        </button>
                        <p class="mt-4">
                            Don't have account
                            <router-link to="/register"
                                ><b>Sign Up</b></router-link
                            >
                        </p>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { defineComponent } from "vue"
import { mapActions } from "vuex"

export default defineComponent({
    data() {
        return {
            username: "",
            password: "",
            error: false
        }
    },
    methods: {
        ...mapActions(["loginUser", "registerUser"]),
        async submit() {
            const username = this.username
            const password = this.password
            await this.$store
                .dispatch("loginUser", { username, password })
                .then(() => {
                    this.$router.push("/")
                })
                .catch(() => {
                    this.error = true
                })
        }
    }
})
</script>
