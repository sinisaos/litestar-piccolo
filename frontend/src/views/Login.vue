<template>
    <div class="container">
        <div class="row justify-content-center mt-5">
            <div class="col-lg-4 col-md-4 col-sm-4">
                <div class="card">
                    <div class="card-title text-center">
                        <h2 class="p-3">Login</h2>
                        <div
                            v-if="error"
                            v-on:click="error = false"
                            class="alert alert-danger"
                            role="alert"
                        >
                            Incorrect username or password
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
                                    class="form-control"
                                    :class="{
                                        'is-invalid': v$.username.$error
                                    }"
                                />
                                <div
                                    v-if="!v$.username.required"
                                    class="invalid-feedback"
                                >
                                    Username is required
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label"
                                    >Password:</label
                                >
                                <input
                                    type="password"
                                    name="password"
                                    v-model="password"
                                    class="form-control"
                                    :class="{
                                        'is-invalid': v$.password.$error
                                    }"
                                />
                                <div
                                    v-if="v$.password.$error"
                                    class="invalid-feedback"
                                >
                                    <span v-if="!v$.password.required"
                                        >Password is required</span
                                    >
                                    <span v-if="!v$.password.minLength"
                                        >Password must be at least 6
                                        characters</span
                                    >
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary">
                                Submit
                            </button>
                            <p class="float-end">
                                Don't have account
                                <router-link to="/register"
                                    >Sign Up</router-link
                                >
                            </p>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { defineComponent } from "vue"
import { mapActions } from "vuex"
import { useVuelidate } from "@vuelidate/core"
import { required, minLength } from "@vuelidate/validators"

export default defineComponent({
    setup() {
        return { v$: useVuelidate() }
    },
    data() {
        return {
            username: "",
            password: "",
            error: false
        }
    },
    validations: {
        username: { required },
        password: { required, minLength: minLength(6) }
    },
    methods: {
        ...mapActions(["loginUser", "registerUser"]),
        async submit() {
            let username = this.username
            let password = this.password
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

