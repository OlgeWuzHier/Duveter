<template>
  <div @mousedown="identify"
    class='patch-elem'
    :style="style"></div>
</template>

<script setup>
/* eslint-disable import/no-dynamic-require */
/* eslint-disable global-require */

import { defineProps, computed, defineEmits } from 'vue';

const props = defineProps(['xIndex', 'yIndex', 'visible', 'background']);
const emit = defineEmits(['identifyTile']);

const style = computed(() => ({
  opacity: props.visible ? '1' : '0',
  'background-image': `url(${require(`../assets/${props.background}.jpg`)})`,
  'background-position': `${-3 * props.xIndex}vw ${-3 * props.yIndex}vw `,
}));

const identify = () => emit('identifyTile', { x: props.xIndex, y: props.yIndex });

</script>

<style scoped>
.patch-elem {
  margin: 0;
  opacity: 0;
}
.visible {
  opacity: 1;
}
</style>
