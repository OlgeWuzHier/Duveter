<template>
  <div class='main'>
    <button @click='startGame' class='ripple'>Go!</button>
  </div>
</template>

<script setup>

const startGame = () => {
  // look for available rooms
  this.$http.post('/queue')
    .then((resp) => {
      if (resp.data.length) {
        // if there's one - join
        console.log(resp.data.length);
      } else {
        // if there's not - create and wait for socket event
        console.log('no room');
      }
    });
};

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
