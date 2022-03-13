<template>
  <div>
    <HeaderComponent/>
    <router-view/>
  </div>
</template>

<script setup>
import HeaderComponent from '@/components/HeaderComponent.vue';
</script>

<style>
#app {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
