<template>
  <div class="playerwrapper">
    <div class="description">
      <h3>{{props.player.username}}'s board</h3>
      <div>Coins <font-awesome-icon :icon="['fas', 'coins']" />: {{props.player.coins}}</div>
      <div>Income <font-awesome-icon :icon="['fas', 'piggy-bank']" />:
      {{props.player.patches.map(p => p.income_value).reduce((prev, next) => prev + next, 0)}}</div>
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
import { defineEmits, onMounted, defineProps } from 'vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import {
  faCoins, faPiggyBank,
} from '@fortawesome/free-solid-svg-icons';
import getUsername from '../helpers/getUsername';
import PatchComponent from './PatchComponent.vue';

library.add(faCoins, faPiggyBank);
const props = defineProps(['player', 'backgrounds']);
const emit = defineEmits(['boardLoaded']);

onMounted(() => {
  if (getUsername() === props.player.username) {
    emit('boardLoaded', true);
  }
});

</script>

<style scoped>
.playerwrapper {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
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
  grid-template-columns: repeat(9, 3vw);
  grid-template-rows: repeat(9, 3vw);
  box-sizing: border-box;
}

.board > .board-elem {
  /* z-index: 100; */
  border: 1px solid rgba(0, 0, 0, 0.75);
  box-sizing: border-box;
  height: 3vw;
  width: 3vw;
}

.board .wrapper {
  position: absolute !important;
  margin: 0;
}
.description {
  color: black;
  font-size: 1.3em;
}
</style>
