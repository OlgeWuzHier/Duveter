<template>
  <header>
    <router-link class="flexitem" to="/">
      <img src="@/assets/duveter_logo.png" alt="Duveter" loading="lazy"/>
    </router-link>
    <nav class="flexitem">
      <router-link class="navitem" to="/">Play</router-link>
      <router-link class="navitem" to="/leaderboard">Leaderboard</router-link>
      <a class="navitem" v-on:click="logout" v-if="logged">Logout</a>
    </nav>
</header>
</template>

<script setup>

import { ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import isAuthenticated from '../helpers/isAuthenticated';

const route = useRoute();
const router = useRouter();

const logged = ref(false);
const logout = () => {
  router.push({ name: 'Login' });
  localStorage.clear();
};
watch(() => route.name, () => {
  logged.value = isAuthenticated();
});

</script>

<style scoped>
header {
  width: 100%;
  height: 80px;
  order: -1;

  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: space-between;
  align-items: center;
  background-color: rgb(0, 50, 80);
}

nav {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: space-between;
  align-items: center;
  gap: 5px;
}

.flexitem {
  flex-basis: 30%;
}

.navitem {
  padding-inline: 15px;
  line-height: 80px;
  font-size: 1.5em;
  color: rgb(155, 201, 255);
  flex-basis: 33%;
}

.navitem:hover {
  background-color: rgb(0, 30, 60);
}

img {
  height: 80px;
  object-fit: contain;
}
</style>
