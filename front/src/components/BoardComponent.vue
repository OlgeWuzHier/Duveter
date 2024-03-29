<template>
  <div class="playerwrapper">
    <div class="description">
      <h3>{{props.player.username}}'s board</h3>
      <div>Coins <font-awesome-icon :icon="['fas', 'coins']" />: {{props.player.coins}}</div>
      <div>Income <font-awesome-icon :icon="['fas', 'piggy-bank']" />:
      {{props.player.patches.map(p => p.income_value).reduce((prev, next) => prev + next, 0)}}</div>
      <div v-if="props.player.timeLeft <= 0">Score <font-awesome-icon :icon="['fas', 'star']" />:
      {{- 162 + props.player.coins +
        2 * props.player.patches.map(p => p.arrangement_table.flat()).flat()
          .reduce((prev, next) => +prev + +next, 0)}}</div>
      <button class="ripple" :style="buttonStyle" @click="exchangeTimeForMoney">
        +1 <font-awesome-icon :icon="['fas', 'coins']" style="margin-right: 8px;"/>
        -1 <font-awesome-icon :icon="['fas', 'clock-rotate-left']" style="transform: scaleX(-1);"/>
      </button>
    </div>
    <div class='board'>
      <div v-for="(f, index) in Array(81).fill(1)"
        class="board-elem"
        :key="index"
        :data-x="index % 9"
        :data-y="Math.floor(index / 9)"></div>
      <PatchComponent
        v-for="patch in props.player.patches"
        :key="patch.name"
        :id="patch.name"
        :background="props.backgrounds[patch.name]"
        :patch="patch"
        :draggable="false"
      />
    </div>
  </div>
</template>

<script setup>
import {
  defineEmits, onMounted, defineProps, computed,
} from 'vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import {
  faCoins, faPiggyBank, faStar,
} from '@fortawesome/free-solid-svg-icons';
import getUsername from '../helpers/getUsername';
import PatchComponent from './PatchComponent.vue';

library.add(faCoins, faPiggyBank, faStar);
const props = defineProps(['player', 'backgrounds']);
const emit = defineEmits(['boardLoaded', 'exchangeTimeForMoney']);

onMounted(() => {
  if (getUsername() === props.player.username) {
    emit('boardLoaded', true);
  }
});

const exchangeTimeForMoney = () => emit('exchangeTimeForMoney');

const buttonStyle = computed(() => ({
  visibility: getUsername() === props.player.username ? 'visible' : 'hidden',
}));

</script>

<style scoped>
.playerwrapper {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
}

.description {
  font-size: 1.3em;
}

.player .board {
  border: 15px solid rgba(126, 214, 223, .7);
  background: rgba(34, 166, 179, .4);
}

.opponent .board {
  border: 15px solid rgba(255, 121, 121, .7);
  background: rgba(235, 77, 75, .4);
}

.board {
  z-index: 0;
  position: relative;
  border-radius: 20px;
  display: grid;
  grid-template-columns: repeat(9, var(--base-tile-size));
  grid-template-rows: repeat(9, var(--base-tile-size));
  box-sizing: border-box;
}

.board > .board-elem {
  border: 1px solid rgba(0, 0, 0, 0.75);
  box-sizing: border-box;
  height: var(--base-tile-size);
  width: var(--base-tile-size);
}

.board .wrapper {
  position: absolute !important;
  margin: 0;
}

button {
  background-color: rgb(0, 50, 80);
  padding: 0.5em;
  margin-top: 0.5em;
}

.ripple:hover {
  background:
    rgb(0, 50, 80) radial-gradient(circle, transparent 1%, rgb(0, 50, 80) 1%) center/15000%;
}

.ripple:active {
  background-color: rgb(0, 100, 130);
}

</style>
