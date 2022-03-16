<template>
  <div @click="identify" class='patch-elem' :style="style"></div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps(['xIndex', 'yIndex', 'visible']);
// const patch = toRefs(props.patch);
// console.log(patch.arrangement_table.value);

const style = {
  // width: `${12 * patch.arrangement_table.value.length}px`,
  // height: `${12 * patch.arrangement_table.value[0].length}px`,
  visibility: props.visible ? 'visible' : 'hidden',
  // background: 'url("../assets/mitchell-luo-8acRvqOAjpw-unsplash.jpg")',
  'background-position': `${-4 * props.xIndex}vh ${-4 * props.yIndex}vh `,
};

const identify = () => {
  console.log(props.xIndex, props.yIndex);
};

</script>

<style scoped>
.patch-elem {
  margin: 0;
  visibility: hidden;
  background: url('../assets/mitchell-luo-8acRvqOAjpw-unsplash.jpg');
}
.visible {
  visibility: initial;
}
</style>
