<!-- src/components/NavBar.vue -->
<template>
    <nav class="navbar">
      <router-link to="/" class="navbar-brand">News Analyzer</router-link>
      <div class="navbar-links">
        <router-link to="/articles" class="nav-link" >Home</router-link>
        <router-link to="/about" class="nav-link">About</router-link>
        <!-- Add more links as needed -->
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: "NavBar",
  };
  </script>
  
  <style scoped>
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #4caf50;
    color: white;
    padding: 10px 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .navbar-brand {
    font-size: 1.5em;
    font-weight: bold;
    color: white;
    text-decoration: none;
  }
  
  .navbar-links {
    display: flex;
    gap: 15px;
  }
  
  .nav-link {
    color: white;
    text-decoration: none;
    font-size: 1em;
  }
  
  .nav-link:hover {
    text-decoration: underline;
  }
  </style>
  