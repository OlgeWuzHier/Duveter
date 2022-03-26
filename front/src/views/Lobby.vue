<template>
  <div class='main'>
    <div>
      <h2>Start new game:</h2>
      <button @click='startGame(false)' class='startgame-button ripple'>Play with random!</button>
      <button @click='startGame(true)' class='startgame-button ripple'>Play with AI!</button>
    </div>
    <div v-if="activeGames" class="active-games">
      <h2>Active games:</h2>
      <div v-for="(activeGame, index) in activeGames"
      :key="index"
      class="active-games-wrapper"
      :class="modeClass">
        <div class="player1" :class="(activeGame.player1 === username) ? 'color-green' : ''">
          {{activeGame.player1}}
        </div>
        <div> vs </div>
        <div class="player2" :class="(activeGame.player2 === username) ? 'color-green' : ''">
          {{activeGame.player2}}
        </div>
        <div class="turn">
          {{activeGame.activePlayer === username ? 'Your turn' : 'Waiting...'}}
        </div>
        <a class="join" :href="'/#/game/' + activeGame.id">
          <button class="joingame-button ripple">Join</button>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>

import {
  inject, ref, onMounted, computed,
} from 'vue';
import { onBeforeRouteLeave, useRouter } from 'vue-router';
import axios from 'axios';
import getUsername from '../helpers/getUsername';

const socket = inject('socket');
const router = useRouter();
const username = getUsername();
const activeGames = ref();
const mode = ref(localStorage.getItem('mode') || 'light');

onMounted(() => {
  window.addEventListener('mode-changed', () => {
    mode.value = localStorage.getItem('mode');
  });
});

const modeClass = computed(() => (mode.value));

const getActivePlayer = (game) => {
  if (game.forcePlayer) {
    return game.forcePlayer;
  }
  if (game.players[0].timeLeft > game.players[1].timeLeft) {
    return game.players[0].username;
  }
  return game.players[1].username;
};

axios.get('/game')
  .then((resp) => {
    activeGames.value = resp.data.games.map((game) => ({
      /* eslint-disable no-underscore-dangle */
      id: game._id.$oid,
      player1: game.players[0].username,
      player2: game.players[1].username,
      activePlayer: getActivePlayer(game),
    }));
  });

const startGame = (vsAI) => {
  // socket.removeAllListeners();
  // Listen for socket notification about created game
  socket.on(`lobby-${username}`, (data) => {
    const id = JSON.parse(data).$oid;
    router.push({ name: 'Game', params: { id } });
  });
  // Join queue
  axios.post('/queue', { vsAI })
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
  socket.off(`lobby-${username}`);
};

onBeforeRouteLeave(leaveQueue);
window.addEventListener('beforeunload', leaveQueue);

</script>

<style scoped>
.startgame-button {
  margin: 3vh;
  width: 30%;
  max-width: 400px;
  min-width: 150px;
}

.joingame-button {
  margin: 0;
  padding: 0;
}

h2 {
  margin: 2vh;
  letter-spacing: 0.05em;
  font-size: 3em;
}

.active-games {
  display: flex;
  flex-wrap: nowrap;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  row-gap: 10px;
}

.active-games-wrapper {
  height: 5vh;
  width: 75vw;
  font-size: 1.5em;
  flex-grow: 1;
  display: grid;
  grid-template-columns: 3fr 1fr 3fr 3fr 2fr;
  grid-template-rows: 1fr;
  line-height: 5vh;
}

.active-games-wrapper.light {
  background-color: white;
}

.active-games-wrapper.light:nth-child(2n) {
  background-color: gray;
}

.active-games-wrapper.dark {
  background-color: #050505;
}

.active-games-wrapper.dark:nth-child(2n) {
  background-color: #333;
}

.color-green {
  color: #6ab04c;
  text-shadow: 1px 1px 1px black;
}
</style>
