<template>
  <div class="time-wrapper" :style="timeWrapperBorderStyle">
    <div class='time-track'>
      <div :style="timeTrackBorderStyle" v-for="(timeunit, index) in Array(54).fill(1)"
      :key="index"
      data-row="0">
        <font-awesome-icon
          class="piggy-icon"
          v-if="props.coinFields.includes(53 - index)"
          :icon="['fas', 'piggy-bank']" />
        <font-awesome-icon
          class="bonus-icon"
          v-if="props.bonusPatchFields.includes(53 - index)"
          :icon="['fas', 'square']" />
      </div>
      <div :style="timeTrackBorderStyle" v-for="(timeunit, index) in Array(54).fill(1)"
      :key="index"
      data-row="1">
      <font-awesome-icon
        class="piggy-icon"
        v-if="props.coinFields.includes(53 - index)"
        :icon="['fas', 'piggy-bank']" />
      </div>
    </div>
    <div class="pawn player-pawn" :style="playerPawnStyle"></div>
    <div class="pawn opponent-pawn" :style="opponentPawnStyle"></div>
  </div>
</template>

<script setup>
import {
  defineProps, computed, ref, onMounted,
} from 'vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import {
  faPiggyBank, faSquare,
} from '@fortawesome/free-solid-svg-icons';
import getUsername from '../helpers/getUsername';

const mode = ref(localStorage.getItem('mode') || 'light');

library.add(faPiggyBank, faSquare);
const props = defineProps(['players', 'coinFields', 'bonusPatchFields']);

onMounted(() => {
  window.addEventListener('mode-changed', () => {
    mode.value = localStorage.getItem('mode');
  });
});

const playerPawnStyle = computed(() => ({
  left: `calc(${1 + 2 * (53 - props.players.filter((p) => p.username === getUsername())[0].timeLeft)}*100% / 108)`,
}));

const opponentPawnStyle = computed(() => ({
  left: `calc(${1 + 2 * (53 - props.players.filter((p) => p.username !== getUsername())[0].timeLeft)}*100% / 108)`,
}));

const timeTrackBorderStyle = computed(() => ({
  'border-right': `1px solid ${(mode.value === 'light') ? 'black' : 'white'}`,
}));

const timeWrapperBorderStyle = computed(() => ({
  border: `1px solid ${(mode.value === 'light') ? 'black' : 'white'}`,
  'border-bottom': 'none',
}));

</script>

<style scoped>
.time-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}
.time-track {
  display: grid;
  grid-template-columns: repeat(54, 1fr);
  grid-template-rows: repeat(2, 1fr);
  width: 100%;
  height: 100%;
  text-align: center;
}
.time-track>div {
  position: relative;
}
.bonus-icon {
  display: block;
  position: absolute;
  top: 100%;
  transform: translateY(-50%);
  width: 100%;
  margin: auto;
}
.piggy-icon {
  display: block;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 100%;
  margin: auto;
}
.pawn {
  transition: left 1s;
  left: 0;
  position: absolute;
  width: 1vw;
  height: 1vw;
  border-radius: 40px;
  transform: translateX(calc(100% / 108 - 50%));
  box-shadow: 0px 2px 8px rgba(0, 0, 0, .7);
}
.player-pawn {
  top: 12.5%;
  background: rgb(126, 214, 223);
}
.opponent-pawn {
  top: 62.5%;
  background: rgb(255, 121, 121);
}
</style>
