<template>
  <div class="leaderboard">
    <h1>This is a leaderboard page</h1>
    <div class="results">
      <div v-for="(result, index) in results" :key="index" class="result-wrapper">
        <div class="number">{{index + 1}}.</div>
        <div class="nick">{{result.username}}</div>
        <div class="score">{{result.score}}</div>
        <div class="date">{{(new Date(result.date.$date)).toLocaleDateString()}}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';

const results = ref();

axios.get('/leaderboards')
  .then((resp) => {
    results.value = resp.data;
  });
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

.result-wrapper {
  height: 5vh;
  width: 75vw;
  font-size: 1.5em;
  flex-grow: 1;
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 1fr;
  grid-template-rows: 1fr;
  background-color: white;
  line-height: 5vh;
}

.result-wrapper:nth-child(2n) {
  background-color: gray;
}
</style>
