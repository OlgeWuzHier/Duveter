<template>
  <div v-if="game">
    <div class='element available'>
      <PatchComponent
      v-for="patch in availablePatches()"
      :key="patch.name"
      :id="patch.name"
      :patch="patch"/>
    </div>
    <div class='element player'>
      <BoardComponent :player="game.players[0]"/>
    </div>
    <div class='element opponent'>
      <BoardComponent :player="game.players[1]" />
    </div>
    <div class='element time'>
      <div class='timeUnit' v-for="timeunit in Array(game.players[0].timeLeft).fill(1)"
      :key="timeunit"></div>
    </div>
    <div class='element comingup'>
      <div class='patches-container'>
        <PatchComponent
        v-for="patch in comingupPatches()"
        :key="patch.name"
        :id="patch.name"
        :patch="patch"/>
      </div>
    </div>
  </div>
</template>

<script setup>

// import { inject } from 'vue';
import PatchComponent from '@/components/PatchComponent.vue';
import BoardComponent from '@/components/BoardComponent.vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { ref } from 'vue';

// const socket = inject('socket');
const route = useRoute();
const game = ref();
window.game = game;

axios.get(`/game?id=${route.params.id}`)
  .then((resp) => {
    game.value = resp.data.game;
  });

const availablePatches = () => game.value.patchesList.slice(0, 3);
const comingupPatches = () => game.value.patchesList.slice(3);
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');
  .body-elem {
    font-family: 'Patrick Hand';
    flex-grow: 1;

    display: grid;
    grid-template-columns: 1fr 2fr 2fr;
    grid-template-rows: 11fr 1fr 2fr;
    grid-template-areas:
    'available player opponent'
    'available time time'
    'comingup comingup comingup';
    column-gap: 10px;
    row-gap: 10px;
    justify-content: stretch;
    align-content: stretch;
    overflow: hidden;
    color: white;
  }

  .element {
    background-color: rgb(255, 239, 149);
    overflow: auto;
  }

  .available {
    grid-area: available;
    background-color: pink;
  }

  .player {
    grid-area: player;
    background-color: blue;
  }

  .opponent {
    grid-area: opponent;
    background-color: rebeccapurple;
  }

  .time {
    grid-area: time;
    background-color: goldenrod;
    display: flex;
  }

  .timeUnit {
    width: 30px;
    height: 30px;
    flex-shrink: 0;
    border: 1px solid blue;
    background-color: gray;
  }

  .comingup {
    grid-area: comingup;
    background-color: green;
  }

  .patches-container {
    display: flex;
    transform: scale(0.5);
    transform-origin: top left;
  }

  .wrapper {
    flex-shrink: 0;
  }

  .element-b {
    grid-column: 2 / 3;
    grid-row: 1 / 2;
  }

  .element-c {
    grid-column: 2 / 3;
    grid-row: 2 / 3;
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
