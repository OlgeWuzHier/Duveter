<template>
  <div class='wrapper' :style="style">
    <TileComponent
      v-for="(elem, index) in patch.arrangement_table.value.flat()"
      :key="index"
      :visible="elem"
      :xIndex="index % rows"
      :yIndex="Math.floor(index / rows)"
      @identifyTile='identifyTile' />
  </div>
</template>

<script setup>
import TileComponent from '@/components/TileComponent.vue';
import {
  toRefs, defineProps, defineEmits, computed,
} from 'vue';

const props = defineProps(['patch', 'draggable', 'patternPath']);
const emit = defineEmits(['identifyTile']);
const patch = toRefs(props.patch);
const rows = computed(() => patch.arrangement_table.value[0].length);

const style = computed(() => ({
  // width: `${12 * patch.arrangement_table.value.length}px`,
  // height: `${12 * patch.arrangement_table.value[0].length}px`,
  'grid-template-columns': `repeat(${patch.arrangement_table.value[0].length}, 3.5vw)`,
  'grid-template-rows': `repeat(${patch.arrangement_table.value.length}, 3.5vw)`,
  position: props.draggable ? 'absolute' : 'static',
  // margin: props.draggable ? '0px' : '10px',
}));

const identifyTile = (obj) => {
  emit('identifyTile', obj);
};

</script>

<style scoped>
.wrapper {
  position: absolute;
  display: grid;
  justify-content: stretch;
  align-content: stretch;
  overflow: hidden;
  margin: 10px;
  column-gap: 0;
  row-gap: 0;
}
</style>
