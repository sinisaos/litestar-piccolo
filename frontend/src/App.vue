<template>
    <div id="app">
        <NavBar />
        <div class="main flex-1">
            <RouterView />
        </div>
    </div>
</template>

<script>
import { defineComponent } from "vue"
import NavBar from "./components/NavBar.vue"

export default defineComponent({
    components: {
        NavBar
    }
})
</script>