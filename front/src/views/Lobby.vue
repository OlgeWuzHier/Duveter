<template>
  <div class='main'>
    <button @click='startGame' class='ripple'>Go!</button>
  </div>
</template>

<script setup>

import { inject } from 'vue';
import { onBeforeRouteLeave, useRouter } from 'vue-router';
import axios from 'axios';
import getUsername from '../helpers/getUsername';

const socket = inject('socket');
const router = useRouter();

const startGame = () => {
  // socket.removeAllListeners();
  // Listen for socket notification about created game
  socket.on(`lobby-${getUsername()}`, (data) => {
    console.log(data);
    router.go({ name: 'Game', params: { id: data.$oid } });
  });
  // Join queue
  axios.post('/queue')
    .then((resp) => {
      // TODO: show waiting for other player on page
      console.log(resp);
    })
    .catch((error) => {
      // TODO: show error on page
      console.log('error', error);
    });
};

const leaveQueue = () => {
  // TODO: Leave queue when page changed/exited
  window.removeEventListener('beforeunload', leaveQueue);
  socket.off(`lobby-${getUsername()}`);
};

onBeforeRouteLeave(leaveQueue);
window.addEventListener('beforeunload', leaveQueue);

</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');
  .main {
    font-family: 'Patrick Hand';
  }

  button {
  margin-top: 5vh;
  position: relative;
  overflow: hidden;
  -webkit-transition: background 400ms;
  transition: background 400ms;
  color: #fff;
  background-color: #6ab04c;
  width: 30%;
  max-width: 400px;
  min-width: 150px;
  padding: 1em 2rem;
  font-family: 'Patrick Hand', sans-serif;
  font-size: 1.5rem;
  outline: 0;
  border: 0;
  border-radius: 0.25rem;
  -webkit-box-shadow: 0 0 0.5rem rgba(0, 0, 0, 0.3);
  box-shadow: 0 0 0.5rem rgba(0, 0, 0, 0.3);
  cursor: pointer;
}

.ripple {
  background-position: center;
  -webkit-transition: background 0.8s;
  transition: background 0.8s;
}
.ripple:hover {
  background: #6ab04c radial-gradient(circle, transparent 1%, #6ab04c 1%) center/15000%;
}
.ripple:active {
  background-color: #badc58;
  background-size: 100%;
  -webkit-transition: background 0s;
  transition: background 0s;
}
</style>
