import 'mdb-vue-ui-kit/css/mdb.min.css';
import { createApp } from 'vue';
import { io } from 'socket.io-client';
import App from './App.vue';
import router from './router';
import jwtInterceptor from './interceptors/jwtInterceptor';

jwtInterceptor();

createApp(App)
  .provide('socket', io('http://localhost:5000'))
  .use(router)
  .mount('#app');
