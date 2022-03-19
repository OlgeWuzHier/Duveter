<template>
  <div class='wrapper' :style="style">
    <TileComponent
      v-for="(elem, index) in patch.arrangement_table.value.flat()"
      :key="index"
      :visible="elem"
      :xIndex="index % rows"
      :background="props.background"
      :yIndex="Math.floor(index / rows)"
      @identifyTile='identifyTile' />
  </div>
</template>

<script setup>
import TileComponent from '@/components/TileComponent.vue';
import {
  toRefs, defineProps, defineEmits, computed,
} from 'vue';

const props = defineProps(['patch', 'draggable', 'patternPath', 'background']);
const emit = defineEmits(['identifyTile']);
const patch = toRefs(props.patch);
const rows = computed(() => patch.arrangement_table.value[0].length);

const style = computed(() => ({
  'grid-template-columns': `repeat(${patch.arrangement_table.value[0].length}, 3vw)`,
  'grid-template-rows': `repeat(${patch.arrangement_table.value.length}, 3vw)`,
  position: props.draggable ? 'absolute' : 'static',
}));

const identifyTile = (obj) => emit('identifyTile', obj);
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
