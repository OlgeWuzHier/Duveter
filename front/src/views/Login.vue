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
   <button @click="protect"></button>
  </div>
</template>

<script>
export default {
  name: 'Login',
  components: {
  },
  methods: {
    login() {
      const { username, password } = this;
      this.$http.post('/login', { username, password })
        .then((resp) => {
          const accessToken = resp.data.access_token;
          localStorage.setItem('accessToken', accessToken);
          this.$router.push('/');
        })
        .catch(() => {
          localStorage.removeItem('accessToken');
          document.getElementById('loginform').reset();
        });
    },
    protect() {
      this.$http.get('/protected')
        .then((resp) => {
          console.log(resp);
        });
    },
  },
};
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');
  .login {
    font-family: 'Patrick Hand';
  }
</style>
