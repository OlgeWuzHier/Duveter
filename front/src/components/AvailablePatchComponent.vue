<template>
  <div class='available-wrapper'>
    <button class="ripple" @click="rotate">
      <font-awesome-icon :icon="['fas', 'rotate-right']" />
    </button>
    <button class="ripple" @click="flipHorizontal">
      <font-awesome-icon :icon="['fas', 'up-down']" style="transform: rotate(90deg);"/>
    </button>
    <button class="ripple" @click="flipVertical">
      <font-awesome-icon :icon="['fas', 'up-down']" />
    </button>
    <PatchComponent
      :patch="props.patch"
      :id="props.patch.name"
      :draggable="true"
      :background="props.background"
      class="draggable"
      @identifyTile='identifyTile'/>
    <div class="description">
      <font-awesome-icon :icon="['fas', 'coins']" />:
        {{props.patch.price_coins}}
      <font-awesome-icon :icon="['fas', 'clock-rotate-left']" style="transform: scaleX(-1);"/>:
        {{props.patch.price_time}}
      <font-awesome-icon :icon="['fas', 'piggy-bank']" />:
        +{{props.patch.income_value}}
    </div>
  </div>
</template>

<script setup>
import PatchComponent from '@/components/PatchComponent.vue';
import { toRefs, defineProps, defineEmits } from 'vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import {
  faRotateRight, faUpDown, faCoins, faPiggyBank, faClockRotateLeft,
} from '@fortawesome/free-solid-svg-icons';

library.add(faRotateRight, faUpDown, faCoins, faPiggyBank, faClockRotateLeft);
const props = defineProps(['patch', 'draggable', 'background']);
const emit = defineEmits(['rotate', 'flipHorizontal', 'flipVertical', 'identifyTile']);
const patch = toRefs(props.patch);

const rotate = () => emit('rotate', patch.name);
const flipHorizontal = () => emit('flipHorizontal', patch.name);
const flipVertical = () => emit('flipVertical', patch.name);
const identifyTile = (obj) => emit('identifyTile', obj);
</script>

<style scoped>
.available-wrapper {
  flex-grow: 1;
  width: 100%;
  max-height: 34%;
  position: relative;
}
.available-wrapper .wrapper {
  margin: 1% 50% 10%;
  transform: translateX(-50%);
}

button {
  background-color: rgb(0, 50, 80);
  width: 20%;
  margin: 0.15em;
  padding: 0.5em 0.5em;
  min-width: 50px;
}

.ripple:hover {
  background:
    rgb(0, 50, 80) radial-gradient(circle, transparent 1%, rgb(0, 50, 80) 1%) center/15000%;
}
.ripple:active {
  background-color: rgb(0, 100, 130);
}

.description {
  /* color: black; */
  position: absolute;
  box-sizing: border-box;
  width: 100%;
  padding: 10px;
  top: 100%;
  left: 50%;
  transform: translate(-50%, -100%);
  font-size: 1.5em;
  text-align: center;
  z-index: 1000;
}
</style>
