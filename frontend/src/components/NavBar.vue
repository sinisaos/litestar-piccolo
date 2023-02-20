<template>
    <header>
        <nav class="navbar navbar-expand-md navbar-light">
            <div class="container">
                <router-link class="navbar-brand" to="/"
                    >Starlite | Piccolo</router-link
                >
                <button
                    class="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarScroll"
                    aria-controls="navbarScroll"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarScroll">
                    <ul
                        v-if="isAuthenticated"
                        class="navbar-nav ms-auto mb-2 mb-md-0"
                    >
                        <li class="nav-link">
                            <input
                                @change="toggleTheme"
                                id="checkbox"
                                type="checkbox"
                                class="switch-checkbox"
                            />
                            <label for="checkbox" id="switch-theme-icon">
                                <span v-if="userTheme === 'light-theme'"
                                    >🌙</span
                                >
                                <span v-else>☀️</span>
                                <div
                                    class="switch-toggle"
                                    :class="{
                                        'switch-toggle-checked':
                                            userTheme === 'dark-theme'
                                    }"
                                ></div>
                            </label>
                        </li>
                        <li class="nav-item dropdown">
                            <a
                                class="nav-link dropdown-toggle"
                                href="#"
                                id="navbarDropdown"
                                role="button"
                                data-bs-toggle="dropdown"
                                aria-expanded="false"
                            >
                                Hello {{ stateUser.user.username }}
                            </a>
                            <ul
                                class="dropdown-menu"
                                aria-labelledby="navbarDropdown"
                            >
                                <li>
                                    <router-link
                                        class="dropdown-item"
                                        to="/profile"
                                        >Profile</router-link
                                    >
                                </li>
                                <li>
                                    <a class="dropdown-item" v-on:click="logout"
                                        >Logout</a
                                    >
                                </li>
                            </ul>
                        </li>
                    </ul>
                    <ul v-else class="navbar-nav ms-auto mb-2 mb-md-0">
                        <li class="nav-link">
                            <input
                                @change="toggleTheme"
                                id="checkbox"
                                type="checkbox"
                                class="switch-checkbox"
                            />
                            <label for="checkbox" id="switch-theme-icon">
                                <span v-if="userTheme === 'light-theme'"
                                    >🌙</span
                                >
                                <span v-else>☀️</span>
                                <div
                                    class="switch-toggle"
                                    :class="{
                                        'switch-toggle-checked':
                                            userTheme === 'dark-theme'
                                    }"
                                ></div>
                            </label>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" to="/login"
                                >Log In</router-link
                            >
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" to="/register"
                                >Register</router-link
                            >
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>
</template>

<script>
import { mapGetters } from "vuex"

export default {
    data() {
        return {
            userTheme: "light-theme"
        }
    },
    computed: {
        ...mapGetters(["isAuthenticated", "stateUser"])
    },
    methods: {
        async logout() {
            await this.$store.dispatch("logoutUser")
            this.$router.push("/").catch((err) => {})
        },
        setTheme(theme) {
            localStorage.setItem("user-theme", theme)
            this.userTheme = theme
            document.documentElement.className = theme
        },
        toggleTheme() {
            const activeTheme = localStorage.getItem("user-theme")
            if (activeTheme === "light-theme") {
                this.setTheme("dark-theme")
            } else {
                this.setTheme("light-theme")
            }
        }
    },
    watch: {
        $route() {
            document.querySelector("#navbarScroll").classList.remove("show")
        }
    }
}
</script>

<style lang="less">
@import "../main.less";
</style>
