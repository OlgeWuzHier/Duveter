<template>
  <div class='wrapper' :style="style">
    <TileComponent
      v-for="(elem, index) in props.patch.arrangement_table.flat()"
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
  defineProps, defineEmits, computed,
} from 'vue';

const props = defineProps(['patch', 'draggable', 'background']);
const emit = defineEmits(['identifyTile']);
const rows = computed(() => props.patch.arrangement_table[0].length);

const style = computed(() => ({
  'grid-template-columns': `repeat(${props.patch.arrangement_table[0].length}, var(--base-tile-size))`,
  'grid-template-rows': `repeat(${props.patch.arrangement_table.length}, var(--base-tile-size))`,
  position: props.draggable ? 'absolute' : 'static',
  left: props.patch.position ? `calc(${props.patch.position.x} * var(--base-tile-size))` : 'initial',
  top: props.patch.position ? `calc(${props.patch.position.y} * var(--base-tile-size))` : 'initial',
}));

const identifyTile = (obj) => emit('identifyTile', obj);
</script>

<style scoped>
.wrapper {
  z-index: 10;
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
