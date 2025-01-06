<template>
    <div class="flex justify-center items-center py-7">
        <div class="card sm:max-w-sm">
            <div class="card">
                <div class="card-title text-center">
                    <h3 class="p-3">Register</h3>
                    <div
                        v-if="error"
                        v-on:click="error = false"
                        class="alert alert-soft alert-error removing:translate-x-5 removing:opacity-0 flex items-center gap-4 transition duration-300"
                        role="alert"
                        id="dismiss-alert1"
                    >
                        User already exists. Please try again.
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
                                :class="{
                                    'is-invalid': v$.username.$error
                                }"
                            />
                            <div
                                class="input-errors"
                                v-for="error of v$.username.$errors"
                                :key="error.$uid"
                            >
                                <div class="error-msg text-red-500">
                                    {{ error.$message }}
                                </div>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email:</label>
                            <input
                                type="text"
                                name="email"
                                v-model="email"
                                class="input max-w-sm"
                                :class="{ 'is-invalid': v$.email.$error }"
                            />
                            <div
                                class="input-errors"
                                v-for="error of v$.email.$errors"
                                :key="error.$uid"
                            >
                                <div class="error-msg text-red-500">
                                    {{ error.$message }}
                                </div>
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
                                class="input max-w-sm"
                                :class="{
                                    'is-invalid': v$.password.$error
                                }"
                            />
                            <div
                                class="input-errors"
                                v-for="error of v$.password.$errors"
                                :key="error.$uid"
                            >
                                <div class="error-msg text-red-500">
                                    {{ error.$message }}
                                </div>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="confirm_password" class="form-label"
                                >Confirm password:</label
                            >
                            <input
                                type="password"
                                name="password"
                                v-model="passwordConfirmation"
                                class="input max-w-sm"
                                :class="{
                                    'is-invalid': v$.passwordConfirmation.$error
                                }"
                            />
                            <div
                                class="input-errors"
                                v-for="error of v$.passwordConfirmation.$errors"
                                :key="error.$uid"
                            >
                                <div class="error-msg text-red-500">
                                    {{ error.$message }}
                                </div>
                            </div>
                        </div>
                        <button type="submit" class="btn btn-primary">
                            Submit
                        </button>
                        <p class="mt-4">
                            Already have account
                            <router-link to="/login"
                                ><b>Sign In</b></router-link
                            >
                        </p>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios"
import { defineComponent } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required, email, minLength, sameAs } from "@vuelidate/validators"

export default defineComponent({
    setup() {
        return { v$: useVuelidate() }
    },
    data() {
        return {
            username: "",
            email: "",
            password: "",
            passwordConfirmation: "",
            error: ""
        }
    },
    validations() {
        return {
            username: { required },
            email: { required, email },
            password: { required, minLength: minLength(6) },
            passwordConfirmation: {
                required,
                sameAsPassword: sameAs(this.password)
            }
        }
    },
    methods: {
        async submit() {
            const payload = {
                username: this.username,
                email: this.email,
                password: this.password,
                passwordConfirm: this.passwordConfirm
            }
            this.v$.$touch()
            if (this.v$.$invalid) {
                return
            }
            await axios.post("accounts/register", payload).then((response) => {
                if (!response.data.error) {
                    alert(
                        "You will be redirected to the login page to complete your registration."
                    )
                    this.$router.push("/login")
                    this.error = false
                } else {
                    this.error = true
                }
            })
        }
    }
})
</script>
