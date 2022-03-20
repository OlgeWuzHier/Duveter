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
  background: url(assets/pw_maze_white.png);
  background-repeat: repeat;
}

button {
  position: relative;
  overflow: hidden;
  transition: background 400ms;
  color: #fff;
  background-color: #6ab04c;
  max-width: 400px;
  min-width: 150px;
  padding: 1em 2rem;
  font-family: 'Patrick Hand', sans-serif;
  font-size: 1.5rem;
  outline: 0;
  border: 0;
  border-radius: 0.25rem;
  box-shadow: 0 0 0.5rem rgba(0, 0, 0, 0.3);
  cursor: pointer;
}

.ripple {
  background-position: center;
  transition: background 0.8s;
}
.ripple:hover {
  background: #6ab04c radial-gradient(circle, transparent 1%, #6ab04c 1%) center/15000%;
}
.ripple:active {
  background-color: #badc58;
  background-size: 100%;
  transition: background 0s;
}
</style>
