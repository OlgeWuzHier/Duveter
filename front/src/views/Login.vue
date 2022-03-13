<template>
  <div class="login">
    <h1>Login</h1>
    <form class="login" id="loginform" @submit.prevent="login">
     <label>User name</label>
     <input required v-model="username" type="text" placeholder="Username">
     <label>Password</label>
     <input required v-model="password" type="password" placeholder="***** ***">
     <button type="submit">Login</button>
   </form>
  </div>
</template>

<script setup>

import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

const username = ref('');
const password = ref('');

const login = () => {
  axios.post('/login', { username: username.value, password: password.value })
    .then((resp) => {
      localStorage.setItem('accessToken', resp.data.access_token);
      router.push('/');
    })
    .catch(() => {
      localStorage.removeItem('accessToken');
      document.getElementById('loginform').reset();
    });
};

</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');
  .login {
    font-family: 'Patrick Hand';
  }
</style>
