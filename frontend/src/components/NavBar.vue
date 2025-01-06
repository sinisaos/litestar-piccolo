<template>
    <nav class="navbar rounded-0 justify-between gap-4 shadow">
        <div class="w-full md:flex md:items-center md:gap-2">
            <div class="flex items-center justify-between">
                <div
                    class="navbar-start items-center justify-between max-md:w-full"
                >
                    <router-link
                        class="link text-base-content link-neutral text-xl font-semibold no-underline"
                        to="/"
                        >Starter</router-link
                    >
                    <div class="md:hidden">
                        <button
                            type="button"
                            class="collapse-toggle btn btn-outline btn-secondary btn-sm btn-square"
                            data-collapse="#dropdown-navbar-collapse"
                            aria-controls="dropdown-navbar-collapse"
                            aria-label="Toggle navigation"
                        >
                            <span
                                class="icon-[tabler--menu-2] collapse-open:hidden size-4"
                            ></span>
                            <span
                                class="icon-[tabler--x] collapse-open:block hidden size-4"
                            ></span>
                        </button>
                    </div>
                </div>
            </div>
            <div
                id="dropdown-navbar-collapse"
                class="md:navbar-end collapse hidden grow basis-full overflow-hidden transition-[height] duration-300 max-md:w-full"
            >
                <label class="menu">
                    <input
                        type="checkbox"
                        value="dark"
                        class="switch theme-controller"
                    />
                </label>
                <ul
                    v-if="!isAuthenticated"
                    class="menu md:menu-horizontal gap-2 p-0 text-base max-md:mt-2"
                >
                    <li>
                        <router-link to="/login">Login</router-link>
                    </li>
                    <li>
                        <router-link to="/register">Register</router-link>
                    </li>
                </ul>
                <ul
                    v-if="isAuthenticated"
                    class="menu md:menu-horizontal gap-2 p-0 text-base max-md:mt-2"
                >
                    <li>
                        <router-link to="/profile">Profile</router-link>
                    </li>
                    <li>
                        <a class="dropdown-item" v-on:click="logout">Logout</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
import { defineComponent } from "vue"
import { mapGetters } from "vuex"

export default defineComponent({
    computed: {
        ...mapGetters(["isAuthenticated", "stateUser"])
    },
    methods: {
        async logout() {
            await this.$store.dispatch("logoutUser")
            this.$router.push("/").catch((err) => {})
        }
    }
})
</script>
