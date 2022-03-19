<template>
  <div class="playerwrapper">
    <div> test </div>
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
import PatchComponent from './PatchComponent.vue';
import getUsername from '../helpers/getUsername';

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

.board {
  z-index: 0;
  position: relative;
  border: 20px solid #f6e58d;
  border-radius: 20px;
  display: grid;
  grid-template-columns: repeat(9, 3vw);
  grid-template-rows: repeat(9, 3vw);
  background: rgba(249, 202, 36, 0.7);
  box-sizing: border-box;
}

.board > .board-elem {
  /* z-index: 100; */
  border: 1px solid rgba(0, 0, 0, 0.7);
  box-sizing: border-box;
  height: 3vw;
  width: 3vw;
}

.board .wrapper {
  position: absolute !important;
  margin: 0;
}
</style>
