<template>
  <div v-if="game" class="game">
    <div class='element available'>
      <AvailablePatchComponent
      v-for="patch in availablePatches()"
      :key="patch.name"
      :id="`available-${patch.name}`"
      :patch="patch"
      :draggable="true"
      :background="tileBackgrounds[patch.name]"
      @rotate="rotatePatch"
      @flipHorizontal="flipPatchHorizontally"
      @flipVertical="flipPatchVertically"
      @identifyTile="saveTilePosition"
      />
    </div>
    <div class='element player'>
      <BoardComponent
      :player="game.players.filter((p) => p.username === getUsername())[0]"
      @boardLoaded="boardLoaded"
      @exchangeTimeForMoney="exchangeTimeForMoney"
      :backgrounds="tileBackgrounds"
      />
    </div>
    <div class='element opponent'>
      <BoardComponent
      :player="game.players.filter((p) => p.username !== getUsername())[0]"
      :backgrounds="tileBackgrounds"
      />
    </div>
    <div class='element time'>
      <TimeTrackComponent
      :players="game.players"
      :coinFields="game.coinFields"
      :bonusPatchFields="game.bonusPatchFields" />
    </div>
    <div class='element comingup' :style="comingupStyle">
      <div class='patches-container'>
        <PatchComponent
        v-for="patch in comingupPatches()"
        :key="patch.name"
        :id="patch.name"
        :background="tileBackgrounds[patch.name]"
        :patch="patch"
        :draggable="false"/>
      </div>
    </div>
    <div class="overlay" :style="overlayStyle"></div>
  </div>
</template>

<script setup>
/* eslint-disable no-param-reassign */
import interact from 'interactjs';
import AvailablePatchComponent from '@/components/AvailablePatchComponent.vue';
import PatchComponent from '@/components/PatchComponent.vue';
import BoardComponent from '@/components/BoardComponent.vue';
import TimeTrackComponent from '@/components/TimeTrackComponent.vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import {
  ref, inject, computed, onMounted,
} from 'vue';
import getTilesBackgrounds from '../helpers/getTilesBackgrounds';
import getUsername from '../helpers/getUsername';

const socket = inject('socket');
const route = useRoute();
const game = ref();
const mode = ref(localStorage.getItem('mode') || 'light');

let tilePosition = null;
let positionValid = false;

onMounted(() => {
  window.addEventListener('mode-changed', () => {
    mode.value = localStorage.getItem('mode');
  });
});

const isPlayerActive = () => {
  if (game.value.forcePlayer) {
    if (game.value.forcePlayer !== getUsername()) {
      return false;
    }
  } else {
    const player = game.value.players.filter((p) => p.username === getUsername())[0];
    const opponent = game.value.players.filter((p) => p.username !== getUsername())[0];
    if (player.timeLeft < opponent.timeLeft) {
      return false;
    }
  }
  return true;
};

const overlayStyle = computed(() => ({
  position: 'absolute',
  top: 0,
  bottom: 0,
  left: 0,
  right: 0,
  'z-index': 10000,
  background: 'black',
  opacity: (mode.value === 'light') ? 0.25 : 0.4,
  display: isPlayerActive() ? 'none' : 'block',
}));

const comingupStyle = computed(() => ({
  'border-top': `1px solid ${(mode.value === 'light') ? 'black' : 'white'}`,
}));

const availablePatches = () => {
  if (game.value.patchesList[0].name.includes('special')) {
    return game.value.patchesList.slice(0, 1);
  }
  return game.value.patchesList.slice(0, 3);
};

const comingupPatches = () => {
  if (game.value.patchesList[0].name.includes('special')) {
    return game.value.patchesList.slice(1);
  }
  return game.value.patchesList.slice(3);
};

const rotateArray = (m) => m[0].map((val, index) => m.map((row) => row[index]).reverse());
const flipArray = (m) => m.map((row) => row.reverse());

const preparePlayerPatches = () => {
  game.value.players.forEach((player) => {
    player.patches.forEach((patch) => {
      for (let i = patch.rotate; i > 0; i -= 1) {
        patch.arrangement_table = rotateArray(patch.arrangement_table);
      }
      if (patch.flip) {
        patch.arrangement_table = flipArray(patch.arrangement_table);
      }
    });
  });
};

const removePatchRotation = () => {
  availablePatches().forEach((patch) => {
    const domElem = document.getElementById(patch.name);
    if (domElem.dataset && domElem.dataset.rotate) {
      domElem.dataset.rotate = '0';
    }
    if (domElem.dataset && domElem.dataset.flip) {
      domElem.dataset.flip = '0';
    }
  });
};

axios.get(`/game?id=${route.params.id}`)
  .then((resp) => {
    game.value = resp.data.game;
    preparePlayerPatches();
  });

socket.removeAllListeners();
socket.on(route.params.id, (data) => {
  game.value = data;
  preparePlayerPatches();
  removePatchRotation();
});

const tileBackgrounds = getTilesBackgrounds();

const rotatePatch = (name) => {
  const patch = game.value.patchesList.filter((x) => x.name === name.value)[0];
  const domElem = document.getElementById(name.value);
  patch.arrangement_table = rotateArray(patch.arrangement_table);
  domElem.dataset.rotate = (+(domElem.dataset.rotate || 0) + 1) % 4;
  if (domElem.dataset.flip === '1') {
    domElem.dataset.rotate = (+(domElem.dataset.rotate || 0) + 2) % 4;
  }
};

const flipPatchHorizontally = (name) => {
  const patch = game.value.patchesList.filter((x) => x.name === name.value)[0];
  const domElem = document.getElementById(name.value);
  patch.arrangement_table.value = flipArray(patch.arrangement_table);
  domElem.dataset.flip = (+(domElem.dataset.flip || 0) + 1) % 2;
};

const flipPatchVertically = (name) => {
  const patch = game.value.patchesList.filter((x) => x.name === name.value)[0];
  const domElem = document.getElementById(name.value);
  patch.arrangement_table = rotateArray(rotateArray(flipArray(patch.arrangement_table)));
  domElem.dataset.flip = (+(domElem.dataset.flip || 0) + 1) % 2;
  domElem.dataset.rotate = (+(domElem.dataset.rotate || 0) + 2) % 4;
};

const saveTilePosition = (obj) => { tilePosition = obj; };

const exchangeTimeForMoney = () => {
  axios.put(`/game?id=${route.params.id}`, {
    timeBalance: 1,
  });
};

const createGrid = () => [...document.querySelectorAll('.player .board>div')]
  .map((d) => ({
    x: d.getBoundingClientRect().left,
    y: d.getBoundingClientRect().top,
  }));

const getBoardArrangementTable = (newPatchArrangementTable, dropPosition) => {
  const player = game.value.players.filter((p) => p.username === getUsername())[0];
  /* eslint-disable no-unused-vars */
  const arrangementTable = Array.from({ length: 9 }, (e) => Array(9).fill(0));
  const tempPatch = {
    arrangement_table: newPatchArrangementTable,
    position: dropPosition,
  };

  [tempPatch, ...player.patches].forEach((patch) => {
    const [x, y] = [patch.position.x, patch.position.y];
    const [width, height] = [patch.arrangement_table[0].length, patch.arrangement_table.length];
    console.log(x, y, width, height);
    for (let i = 0; i < width; i += 1) {
      for (let j = 0; j < height; j += 1) {
        arrangementTable[j + y][i + x] += patch.arrangement_table[j][i];
      }
    }
  });
  return arrangementTable;
};

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
  interact('.draggable').unset();
  interact('.player .board>.board-elem').unset();
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
          const { target } = event;
          if (!positionValid) {
            target.style.transform = 'translate(0px, 0px) translateX(-50%)';
            target.setAttribute('data-x', 0);
            target.setAttribute('data-y', 0);
          }
        },
      },
    });

  interact('.player .board>.board-elem')
    .dropzone({
      ondrop(event) {
        const patch = game.value.patchesList.filter((p) => p.name === event.relatedTarget.id)[0];
        const width = patch.arrangement_table[0].length;
        const height = patch.arrangement_table.length;
        const dropPosition = {
          x: event.target.dataset.x - tilePosition.x,
          y: event.target.dataset.y - tilePosition.y,
        };
        const patchFits = dropPosition.x + width < 10 && dropPosition.x >= 0
          && dropPosition.y + height < 10 && dropPosition.y >= 0;
        const boardArrangementTable = getBoardArrangementTable(
          patch.arrangement_table, dropPosition,
        );
        const patchCollides = !!boardArrangementTable.flat().filter((x) => x > 1).length;
        const canAfford = true; // TODO: Check if user has resources

        console.log(`${event.relatedTarget.id} was dropped into`, dropPosition);

        if (patchFits && !patchCollides && canAfford) {
          positionValid = true;
          axios.put(`/game?id=${route.params.id}`, {
            patch: {
              name: event.relatedTarget.id,
              position: dropPosition,
              flip: +(event.relatedTarget.dataset.flip || 0),
              rotate: +(event.relatedTarget.dataset.rotate || 0),
            },
          }).catch((err) => {
            const { relatedTarget } = event;
            relatedTarget.style.transform = 'translate(0px, 0px) translateX(-50%)';
            relatedTarget.setAttribute('data-x', 0);
            relatedTarget.setAttribute('data-y', 0);
            console.log(err);
          });
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
    justify-content: stretch;
    align-content: stretch;
    overflow: hidden;
  }

  .game {
    position: relative;
  }

  .element {
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
  }

  .comingup {
    border-top: 1px solid black;
    padding-top: 1vw;
    grid-area: comingup;
    overflow-x: auto;
    overflow-y: hidden;
  }

  .patches-container {
    display: flex;
    transform: scale(0.45);
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
</style>
