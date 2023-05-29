<template>
  <LoginComponent v-if="!isAuthenticated" v-on:login="onLogin" />
</template>

<script>
import LoginComponent from './components/LoginComponent.vue'

export default {
  name: "App",
  data() {
    return {
      isAuthenticated: false
    }
  },
  methods: {
    
  },
  components: {
    LoginComponent
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
