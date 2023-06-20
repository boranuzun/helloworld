<template>
  <head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Chewy" />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Caveat" />
  </head>
  <div class="custom-cursor" id="main-page">
    <my-header />
    <router-view />
    <my-footer />
  </div>
</template>

<script>
import footer from "./components/Footer.vue"
import header from "./components/Header.vue"

export default {
  name: "app",
  components: {
    myFooter: footer,
    myHeader: header
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
}
</style>
