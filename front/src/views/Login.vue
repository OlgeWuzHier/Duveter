<template>
  <div class="login">
    <h1>Login</h1>
    <form class="login-form" id="loginform">
      <div class="form-elem">
        <label for="username">Username:</label>
        <input required v-model="username" type="text" placeholder="Username" id="username">
      </div>
      <div class="form-elem">
        <label for="pwd">Password:</label>
        <input required v-model="password" type="password" placeholder="********" id="pwd">
      </div>
      <div class="button-container">
        <button @click="login">Login</button>
        <button @click="register">Register</button>
      </div>
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
      localStorage.setItem('mode', 'light');
      router.push('/');
    })
    .catch(() => {
      localStorage.removeItem('accessToken');
      document.getElementById('loginform').reset();
    });
};

const register = () => {
  axios.post('/register', { username: username.value, password: password.value })
    .then((resp) => {
      localStorage.setItem('accessToken', resp.data.access_token);
      localStorage.setItem('mode', 'light');
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
  font-size: 1.5em;
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  align-items: center;
}

.form-elem {
  margin: .5em;
  padding: .5em;
}

label {
  margin-right: 2vw;
}

button {
  padding: .5em;
  margin: 1em;
}
</style>
