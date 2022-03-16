<template>
  <div class='wrapper' :style="style">
    <TileComponent
      v-for="(elem, index) in patch.arrangement_table.value.flat()"
      :key="elem"
      :visible="elem"
      :xIndex="index % rows"
      :yIndex="Math.floor(index / rows)" />
  </div>
</template>

<script setup>
import TileComponent from '@/components/TileComponent.vue';
import { toRefs, defineProps } from 'vue';

const props = defineProps(['patch']);
const patch = toRefs(props.patch);
const cols = patch.arrangement_table.value.length;
const rows = patch.arrangement_table.value[0].length;

const style = {
  // width: `${12 * patch.arrangement_table.value.length}px`,
  // height: `${12 * patch.arrangement_table.value[0].length}px`,
  'grid-template-columns': `repeat(${rows}, 4vh)`,
  'grid-template-rows': `repeat(${cols}, 4vh)`,
};

</script>

<style scoped>
.wrapper {
  display: grid;
  justify-content: stretch;
  align-content: stretch;
  overflow: hidden;
  margin: 10px;
  column-gap: 0;
  row-gap: 0;
}
</style>
