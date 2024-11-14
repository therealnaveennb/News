<!-- src/App.vue -->
<template>
  <div id="app">
    <NavBar /> <!-- Add the NavBar at the top of the app -->
    <router-view /> <!-- Render the active route component here -->
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue';

export default {
  name: 'App',
  components: {
    NavBar,
  },
};
</script>

<style>
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f9;
  margin: 0;
  padding: 0;
}

#app {
  padding-top: 20px;
}
</style>
