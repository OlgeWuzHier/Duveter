<template>
  <div @mousedown="identify"
    class='patch-elem'
    :style="style"></div>
</template>

<script setup>
import { defineProps, computed, defineEmits } from 'vue';

const props = defineProps(['xIndex', 'yIndex', 'visible']);
const emit = defineEmits(['identifyTile']);
// const patch = toRefs(props.patch);
// console.log(patch.arrangement_table.value);

const style = computed(() => ({
  // width: `${12 * patch.arrangement_table.value.length}px`,
  // height: `${12 * patch.arrangement_table.value[0].length}px`,
  visibility: props.visible ? 'visible' : 'hidden',
  // background: 'url("../assets/mitchell-luo-8acRvqOAjpw-unsplash.jpg")',
  'background-position': `${-3.5 * props.xIndex}vw ${-3.5 * props.yIndex}vw `,
}));

const identify = () => {
  emit('identifyTile', { x: props.xIndex, y: props.yIndex });
};

</script>

<style scoped>
.patch-elem {
  margin: 0;
  visibility: hidden;
  background: url('../assets/11.jpg');
}
.visible {
  visibility: initial;
}
</style>
