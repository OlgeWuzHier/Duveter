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
  </div>
</template>

<script setup>
import PatchComponent from '@/components/PatchComponent.vue';
import { toRefs, defineProps, defineEmits } from 'vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faRotateRight, faUpDown } from '@fortawesome/free-solid-svg-icons';

library.add(faRotateRight, faUpDown);
const props = defineProps(['patch', 'draggable', 'patternPath', 'background']);
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
  position: relative;
}
.available-wrapper .wrapper {
  margin: 10% 50%;
  transform: translateX(-50%);
}
button {
  position: relative;
  overflow: hidden;
  transition: background 400ms;
  color: #fff;
  background-color: rgb(0, 50, 80);
  width: 20%;
  margin: 0.1em;
  padding: 1em 1em;
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
  background:
  rgb(0, 50, 80) radial-gradient(circle, transparent 1%, rgb(0, 50, 80) 1%) center/15000%;
}
.ripple:active {
  background-color: rgb(0, 100, 130);
  background-size: 100%;
  transition: background 0s;
}
</style>
