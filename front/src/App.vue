<template>
  <div class='main-container'>
    <HeaderComponent/>
    <router-view class='body-elem'/>
  </div>
</template>

<script setup>
import HeaderComponent from '@/components/HeaderComponent.vue';
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');

#app {
  font-family: 'Patrick Hand', Roboto, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.main-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.body-elem {
  order: 1;
  flex-grow: 1;
}
</style>
