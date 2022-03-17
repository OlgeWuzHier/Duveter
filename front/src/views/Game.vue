<template>
  <div v-if="game">
    <div class='element available'>
      <AvailablePatchComponent
      v-for="patch in availablePatches()"
      :key="patch.name"
      :id="patch.name"
      :patch="patch"
      :draggable="true"
      @rotate="rotatePatch"
      @flipHorizontal="flipPatchHorizontally"
      @flipVertical="flipPatchVertically"
      />
    </div>
    <div class='element player'>
      <BoardComponent :player="game.players[0]" @boardLoaded="boardLoaded"/>
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
        :patch="patch"
        :draggable="false"/>
      </div>
    </div>
  </div>
</template>

<script setup>

// import { inject } from 'vue';
import interact from 'interactjs';
import AvailablePatchComponent from '@/components/AvailablePatchComponent.vue';
import PatchComponent from '@/components/PatchComponent.vue';
import BoardComponent from '@/components/BoardComponent.vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { ref } from 'vue';

// const socket = inject('socket');
const route = useRoute();
const game = ref();

axios.get(`/game?id=${route.params.id}`)
  .then((resp) => {
    game.value = resp.data.game;
  });

const availablePatches = () => game.value.patchesList.slice(0, 3);
const comingupPatches = () => game.value.patchesList.slice(3);

const rotatePatch = (name) => {
  const patch = game.value.patchesList.filter((x) => x.name === name.value)[0];
  const rotate = (m) => m[0].map((val, index) => m.map((row) => row[index]).reverse());
  patch.arrangement_table = rotate(patch.arrangement_table);
};

const flipPatchHorizontally = (name) => {
  const patch = game.value.patchesList.filter((x) => x.name === name.value)[0];
  console.log(patch);
};

const flipPatchVertically = (name) => {
  const patch = game.value.patchesList.filter((x) => x.name === name.value)[0];
  console.log(patch);
};

const createGrid = () => [
  ...document.querySelectorAll('.player .board>div')]
  .map((d) => ({
    x: d.getBoundingClientRect().left,
    y: d.getBoundingClientRect().top,
  }));

const getModifiers = () => [
  interact.modifiers.restrictRect({
    restriction: '.body-elem',
  }),
  interact.modifiers.snap({
    targets: createGrid(),
    relativePoints: [{ x: 0, y: 0 }],
    range: 100,
  }),
];

const boardLoaded = () => {
  interact('.draggable')
    .draggable({
      inertia: false,
      modifiers: getModifiers(),
      autoScroll: true,
      listeners: {
        move(event) {
          event.interactable.draggable({ modifiers: getModifiers() });
          const { target } = event;
          const x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
          const y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

          target.style.transform = `translate(${x}px, ${y}px)  translateX(-50%)`;

          target.setAttribute('data-x', x);
          target.setAttribute('data-y', y);
        },
        end(event) {
          console.log(`moved a distance of ${
            (Math.sqrt((event.pageX - event.x0) ** 2 + (event.pageY - event.y0) ** 2)).toFixed(2)}px`);
        },
      },
    });

  interact('.player .board>div')
    .dropzone({
      ondrop(event) {
        console.log(`${event.relatedTarget.id} was dropped into ${event.target.id}`);
      },
    });
};
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
    background: url(../assets/bg.jpg);
    background-size: cover;
  }

  .element {
    border: 1px solid black;
    box-sizing: border-box;
  }

  .available {
    grid-area: available;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
  }

  .player {
    grid-area: player;
    display: flex;
    flex-direction: column;
    justify-content: space-between;

  }

  .opponent {
    grid-area: opponent;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .time {
    grid-area: time;
    display: flex;
  }

  .timeUnit {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    border: 1px solid blue;
    background-color: gray;
  }

  .comingup {
    grid-area: comingup;
    overflow-x: auto;
    overflow-y: hidden;
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
