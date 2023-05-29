<template>
  <div style="width: 100%; height: 100%">
    <LoginComponent v-if="!isAuthenticated" v-on:login="onLogin" />
    <PlayerComponent v-if="isAuthenticated" />
  </div>
</template>

<script>
import LoginComponent from './components/LoginComponent.vue'
import PlayerComponent from './components/PlayerComponent.vue'


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
    LoginComponent,
    PlayerComponent
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
