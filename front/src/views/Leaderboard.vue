<template>
  <div class="leaderboard">
    <h1 :class="modeClass">Hall of fame</h1>
    <div class="results">
      <div v-for="(result, index) in results"
      :key="index"
      class="result-wrapper"
      :class="modeClass">
        <div class="number">{{index + 1}}.</div>
        <div class="nick" :class="(result.username === username) ? 'color-green' : ''">
          {{result.username}}
        </div>
        <div class="score">{{result.score}}</div>
        <div class="date">{{(new Date(result.date.$date)).toLocaleDateString()}}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { computed, onMounted, ref } from 'vue';
import getUsername from '../helpers/getUsername';

const results = ref();
const mode = ref(localStorage.getItem('mode') || 'light');
const username = getUsername();

onMounted(() => {
  window.addEventListener('mode-changed', () => {
    mode.value = localStorage.getItem('mode');
  });
});

axios.get('/leaderboards')
  .then((resp) => {
    results.value = resp.data;
  });

const modeClass = computed(() => (mode.value));
</script>

<style scoped>
.results {
  display: flex;
  flex-wrap: nowrap;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
  row-gap: 10px;
}

h1 {
  margin-top: 3vh;
  margin-bottom: 3vh;
  letter-spacing: 0.05em;
  font-size: 3em;
}

h1.light {
  text-shadow: none;
}

h1.dark {
  filter: drop-shadow(0px 0px 5px #dff9fb);
  text-shadow: 0 0 5px #f9ca24;
}

.result-wrapper {
  height: 5vh;
  width: 75vw;
  font-size: 1.5em;
  flex-grow: 1;
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 1fr;
  grid-template-rows: 1fr;
  line-height: 5vh;
}

.result-wrapper.light {
  background-color: white;
}

.result-wrapper.light:nth-child(2n) {
  background-color: gray;
}

.result-wrapper.dark {
  background-color: #050505;
}

.result-wrapper.dark:nth-child(2n) {
  background-color: #333;
}

.color-green {
  color: #6ab04c;
  text-shadow: 1px 1px 1px black;
}
</style>
