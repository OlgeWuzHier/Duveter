<template>
  <div class="playerwrapper">
    <div> test </div>
    <div class='board' :style="style">
      <div v-for="(f, index) in Array(81).fill(1)"
        :key="index"
        :data-x="index % 9"
        :data-y="Math.floor(index / 9)"></div>
    </div>
  </div>
</template>

<script setup>
// import { defineProps } from 'vue';
import { defineEmits, onMounted } from 'vue';
// const props = defineProps(['player']);
const emit = defineEmits(['boardLoaded']);

onMounted(() => {
  emit('boardLoaded', true);
});
const style = {
};

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
  display: grid;
  grid-template-columns: repeat(9, 3.5vw);
  grid-template-rows: repeat(9, 3.5vw);
}

.board > div {
  border: 1px solid black;
  box-sizing: border-box;
  height: 3.5vw;
  width: 3.5vw;
}
</style>
