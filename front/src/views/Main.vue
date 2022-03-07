<template>
  <div class='main'>
    <button @click='startGame'>Go!</button>
  </div>
</template>

<script>
export default {
  name: 'Main',
  components: {
  },
  methods: {
    startGame() {
      // look for available rooms
      this.$http.get('/room')
        .then((resp) => {
          if (resp.data.roomId) {
            // if there's one - join
            console.log('find one');
          } else {
            // if there's not - create and wait for socket event
            console.log('no room');
          }
        });
    },
  },
};
</script>
