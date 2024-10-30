<template>
    <div id="app">
        <NavBar />
        <div class="main">
            <RouterView />
        </div>
        <Footer />
    </div>
</template>

<script>
import { defineComponent } from "vue"
import NavBar from "./components/NavBar.vue"
import Footer from "./components/Footer.vue"

export default defineComponent({
    components: {
        NavBar,
        Footer
    }
})
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
}
.main {
    padding-top: 1em;
    padding-bottom: 5em;
}
</style>
