<template>
<header>
  <img src="@/assets/duveter_logo.png" height="80" alt="Duveter" loading="lazy" class="flexitem"/>
  <nav>
    <router-link class="flexitem navitem" to="/">Play</router-link>
    <router-link class="flexitem navitem" to="/leaderboard">Leaderboard</router-link>
  </nav>
</header>
</template>

<script>
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');
header {
  width: 100%;
  position: sticky;
  top: 0;
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
  justify-content: space-around;
  align-items: center;
  gap: 10px;
}

.flexitem {
  padding-left: 10px;
  padding-right: 10px;
  flex-basis: 30%;
}

.navitem {
  font-family: 'Patrick Hand';
  font-size: 1.5em;
  font-weight: 100;
  color: rgb(155, 201, 255);
}

.navitem:hover {
  background-color: rgb(0, 30, 60);
}

img {
  width: 100%;
  object-fit: contain;
}
</style>
