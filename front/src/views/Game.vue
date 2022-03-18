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
      @identifyTile="saveTilePosition"
      />
    </div>
    <div class='element player'>
      <BoardComponent :player="game.players[0]" @boardLoaded="boardLoaded"/>
    </div>
    <div class='element opponent'>
      <BoardComponent :player="game.players[1]" />
    </div>
    <div class='element time'>
      <div class='timeUnit' v-for="(timeunit, index) in Array(game.players[0].timeLeft).fill(1)"
      :key="index"></div>
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
let tilePosition = null;
let positionValid = false;

axios.get(`/game?id=${route.params.id}`)
  .then((resp) => {
    game.value = resp.data.game;
  });

const availablePatches = () => game.value.patchesList.slice(0, 3);
const comingupPatches = () => game.value.patchesList.slice(3);

const rotateArray = (m) => m[0].map((val, index) => m.map((row) => row[index]).reverse());
const flipArray = (m) => m.map((row) => row.reverse());

const rotatePatch = (name) => {
  const patch = game.value.patchesList.filter((x) => x.name === name.value)[0];
  patch.arrangement_table = rotateArray(patch.arrangement_table);
};

const flipPatchHorizontally = (name) => {
  const patch = game.value.patchesList.filter((x) => x.name === name.value)[0];
  patch.arrangement_table = flipArray(patch.arrangement_table);
};

const flipPatchVertically = (name) => {
  const patch = game.value.patchesList.filter((x) => x.name === name.value)[0];
  patch.arrangement_table = rotateArray(rotateArray(flipArray(patch.arrangement_table)));
};

const saveTilePosition = (obj) => {
  tilePosition = obj;
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
    range: 50,
  }),
];

const boardLoaded = () => {
  window.availablePatches = availablePatches();

  interact('.draggable')
    .draggable({
      inertia: false,
      modifiers: getModifiers(),
      autoScroll: true,
      listeners: {
        start() {
          positionValid = false;
        },
        move(event) {
          event.interactable.draggable({ modifiers: getModifiers() });
          const { target } = event;
          const x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
          const y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

          target.style.transform = `translate(${x}px, ${y}px) translateX(-50%)`;

          target.setAttribute('data-x', x);
          target.setAttribute('data-y', y);
        },
        end(event) {
          console.log(`moved a distance of ${
            (Math.sqrt((event.pageX - event.x0) ** 2 + (event.pageY - event.y0) ** 2)).toFixed(2)}px`);
          const { target } = event;
          if (!positionValid) {
            target.style.transform = 'translate(0px, 0px) translateX(-50%)';
            target.setAttribute('data-x', 0);
            target.setAttribute('data-y', 0);
          }
        },
      },
    });

  interact('.player .board>div')
    .dropzone({
      ondrop(event) {
        // console.log(event.target);
        // window.target = event.target;
        console.log(`${event.relatedTarget.id} was dropped into 
          x: ${event.target.dataset.x}, 
          y: ${event.target.dataset.y}`);

        const patch = game.value.patchesList.filter((p) => p.name === event.relatedTarget.id)[0];
        const width = patch.arrangement_table[0].length;
        const height = patch.arrangement_table.length;
        positionValid = true;
        console.log(event.target.dataset.x, tilePosition.x, width);
        console.log(event.target.dataset.y, tilePosition.y, height);
        if (event.target.dataset.x - tilePosition.x + width > 9
          || event.target.dataset.y - tilePosition.y + height > 9) {
          positionValid = false;
        }
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
